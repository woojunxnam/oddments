from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from qa_common import DATA, load_json, load_records, question_audit_hash, write_json


REAUDIT_SUFFIX = "-REAUDIT-2026-08-13.json"


def _audit_results(review_code: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    pattern = f"AUDIT-GPT-PHASE2-*-{review_code}{REAUDIT_SUFFIX}"
    for path in sorted((DATA / "audits").glob(pattern)):
        results.extend(load_json(path)["results"])
    return results


def repair_scope() -> set[str]:
    legal = {
        result["Question_ID"]
        for result in _audit_results("LEGAL")
        if result["Verdict"] != "KEEP"
    }
    realism = {
        result["Question_ID"]
        for result in _audit_results("REALISM")
        if result["Realism_Verdict"] == "FAIL"
    }
    scope = legal | realism
    if len(scope) != 52:
        raise ValueError(f"expected 52 repair questions from PR #10, found {len(scope)}")
    return scope


def frozen_pr10_hashes() -> dict[str, str]:
    frozen: dict[str, str] = {}
    for review_code in ("LEGAL", "REALISM"):
        pattern = f"AUDIT-GPT-PHASE2-*-{review_code}{REAUDIT_SUFFIX}"
        for path in sorted((DATA / "audits").glob(pattern)):
            for qid, value in load_json(path)["question_hashes"].items():
                if qid in frozen and frozen[qid] != value:
                    raise ValueError(f"PR #10 audit hashes disagree for {qid}")
                frozen[qid] = value
    if len(frozen) != 80:
        raise ValueError(f"expected 80 frozen PR #10 hashes, found {len(frozen)}")
    return frozen


def _choices(*texts: str) -> list[dict[str, str]]:
    return [{"id": chr(65 + index), "text": text} for index, text in enumerate(texts)]


SBA_REWRITES: dict[str, dict[str, Any]] = {
    "MA-Q-0011": {
        "stem": "A patient says the pharmacy dispensed only 20 of 30 Adderall tablets because stock was short 10 days ago. The profile instead shows all 30 tablets were dispensed, and the original prescription says \"3 refills.\" What should the pharmacist do?",
        "choices": _choices(
            "Process one of the printed refills.",
            "Dispense 10 tablets as a stock-shortage remainder.",
            "Ask the prescriber to add a refill by telephone.",
            "Decline further dispensing; require a new lawful prescription.",
            "Treat the notation as three future-dated prescriptions.",
        ),
        "correct_choice_ids": ["D"],
        "core": "Because the record shows the Schedule II prescription was completely dispensed, neither a remainder nor a refill remains. The printed refill notation is ineffective, so further dispensing requires a new lawful prescription.",
        "analysis": {
            "A": "The five-refill framework does not apply to Schedule II prescriptions.",
            "B": "A remainder exists only after an actual, documented partial fill; the record shows the full quantity was dispensed.",
            "C": "A telephone change cannot add a refill to a completed Schedule II prescription.",
            "D": "Correct. A completed Schedule II prescription cannot be refilled.",
            "E": "A refill notation does not create separate prescriptions with their own issue and earliest-fill dates.",
        },
        "facts": [
            "Adderall is a federal and Massachusetts Schedule II drug.",
            "Federal law prohibits Schedule II refills; a genuine partial-fill balance is a different legal pathway.",
        ],
        "trap": "Do not convert a claimed shortage into a remainder when the dispensing record documents completion.",
        "steps": [
            "Classify Adderall as Schedule II",
            "Distinguish a completed dispensing from a documented partial-fill balance",
            "Reject refill and oral-change pathways for the completed prescription",
        ],
    },
    "MA-Q-0018": {
        "stem": "A hydromorphone prescription was partially filled at the patient's request 28 days after its issue date. On day 29 the patient requests the documented balance at the same pharmacy and points to two refills printed on the prescription. Which action is lawful?",
        "choices": _choices(
            "Dispense the documented balance before the 30-day issue-date deadline.",
            "Process the first printed refill within six months.",
            "Wait until day 31 and dispense the balance as a refill.",
            "Transfer the printed refill to another pharmacy.",
            "Add a refill after telephone confirmation from the prescriber.",
        ),
        "correct_choice_ids": ["A"],
        "core": "The patient-requested partial-fill pathway may permit the same pharmacy to dispense the documented Schedule II balance before the Massachusetts 30-day issue-date deadline. The printed refill notation remains ineffective.",
        "analysis": {
            "A": "Correct. The balance may be completed by the same pharmacy within the applicable issue-date window.",
            "B": "Schedule II prescriptions cannot use the Schedule III-IV refill framework.",
            "C": "The Massachusetts 30-day validity limit is measured from the issue date, not a later refill date.",
            "D": "There is no valid refill to transfer.",
            "E": "Telephone confirmation cannot add a Schedule II refill.",
        },
        "facts": [
            "Hydromorphone is federal and Massachusetts Schedule II.",
            "Completing a documented partial-fill balance is not a refill.",
        ],
        "trap": "A printed refill number is irrelevant, but that does not erase a lawful documented remainder.",
        "steps": [
            "Classify hydromorphone as Schedule II",
            "Separate a patient-requested partial fill from a refill",
            "Apply the Massachusetts issue-date deadline to the balance",
        ],
    },
    "MA-Q-0023": {
        "stem": "A prescriber telephones an emergency Nucynta order after confirming that immediate treatment is necessary and no signed prescription can be delivered first. What may the pharmacist dispense?",
        "choices": _choices(
            "A fixed 72-hour supply.",
            "The amount needed for the emergency period.",
            "A fixed seven-day supply.",
            "The quantity expected on the follow-up prescription.",
            "Nothing, because Schedule II oral orders are never allowed.",
        ),
        "correct_choice_ids": ["B"],
        "core": "The pharmacist may dispense only the quantity adequate for the emergency period after immediate communication with and reasonable identification of the prescriber. The prescriber must provide the emergency follow-up prescription within seven days.",
        "analysis": {
            "A": "Federal law does not set a fixed 72-hour emergency quantity.",
            "B": "Correct. The quantity is limited to the amount adequate for the emergency period.",
            "C": "Seven days is the follow-up-prescription timing rule, not a supply cap.",
            "D": "A later follow-up prescription documents the emergency quantity; it does not enlarge the initial emergency dispensing.",
            "E": "A defined emergency permits an oral Schedule II authorization when all safeguards are met.",
        },
        "facts": [
            "Nucynta (tapentadol) is federal and Massachusetts Schedule II.",
            "Within seven days after the oral authorization, the prescriber must cause the written follow-up prescription to be delivered or transmit an electronic prescription for the emergency quantity; a mailed paper prescription must be postmarked within that period.",
            "If the follow-up is not delivered, the pharmacist must notify the nearest DEA office.",
        ],
        "trap": "Do not confuse the seven-day follow-up clock with the quantity allowed for the emergency period.",
        "steps": [
            "Confirm that the facts meet the federal emergency definition",
            "Limit the dispensing to the emergency period",
            "Apply the separate seven-day follow-up requirement",
        ],
        "rule_ids": ["FED-CII-EMERGENCY-ORAL", "FED-CII-EMERGENCY-FOLLOWUP", "FED-CS-SCHEDULES"],
    },
    "MA-Q-0024": {
        "stem": "A Massachusetts pharmacy receives a prescription for generic buprenorphine sublingual tablets for opioid use disorder with a 90-day quantity. Which quantity rule should the pharmacist apply?",
        "choices": _choices(
            "A 30-day ceiling applies to every Schedule III opioid.",
            "Every Schedule III prescription permits a 90-day fill.",
            "The initial-opiate seven-day limit controls OUD treatment.",
            "The OUD pathway may permit one fill of up to 90 days.",
            "Five refills may be combined into one 90-day fill.",
        ),
        "correct_choice_ids": ["D"],
        "core": "Massachusetts permits a single fill of up to a 90-day supply for a Schedule II or III drug used to treat opioid use disorder, unless another law prohibits it. Generic buprenorphine sublingual tablets fit that indication-specific pathway.",
        "analysis": {
            "A": "The OUD pathway is an express exception to the general 30-day rule.",
            "B": "The 90-day permission depends on the drug and indication, not Schedule III status alone.",
            "C": "The initial-opiate limit does not govern a drug prescribed for OUD treatment on these facts.",
            "D": "Correct. The prescription may qualify for a single fill of up to 90 days.",
            "E": "Refill authorization does not determine the quantity allowed in one fill.",
        },
        "facts": [
            "Current generic buprenorphine sublingual tablets are used to treat opioid dependence and are Schedule III.",
            "Subutex was the legacy brand for buprenorphine sublingual tablets; the Subutex brand product is discontinued, while generic presentations remain available.",
            "M.G.L. c.94C, §23(d) permits up to a 90-day single fill for Schedule II or III drugs used to treat OUD.",
        ],
        "trap": "Use the current generic presentation; do not present discontinued Subutex as a current brand product.",
        "steps": [
            "Identify the current generic buprenorphine presentation",
            "Classify it as Schedule III",
            "Apply the indication-specific Massachusetts OUD quantity pathway",
        ],
    },
    "MA-Q-0025": {
        "stem": "A Massachusetts specialty pharmacy fills a patient-specific Sublocade prescription, ships the dose to the patient's clinic, and records the transaction as the pharmacy's dispensing; clinic staff will administer it. How should the pharmacy handle PMP reporting?",
        "choices": _choices(
            "Omit it because only Schedule II drugs are reported.",
            "Omit it because clinic administration erases the pharmacy dispensing.",
            "Let the product program replace the PMP submission.",
            "Wait to report unless a refill is later authorized.",
            "Report the covered Schedule III dispensing to MassPAT.",
        ),
        "correct_choice_ids": ["E"],
        "core": "The stated transaction is a patient-specific Schedule III dispensing by the pharmacy, so the general MassPAT reporting rule applies. Later administration at the clinic does not recharacterize the pharmacy's recorded dispensing.",
        "analysis": {
            "A": "MassPAT reporting is not limited to Schedule II drugs.",
            "B": "The stem expressly identifies a pharmacy dispensing, distinct from the clinic's later administration.",
            "C": "A product distribution program does not replace a required state PMP submission.",
            "D": "Reporting follows the dispensing transaction, not the existence of a later refill.",
            "E": "Correct. The pharmacy reports the covered Schedule III dispensing.",
        },
        "facts": [
            "Sublocade is a Schedule III extended-release buprenorphine injection for OUD treatment.",
            "Massachusetts pharmacies report covered prescription dispensings of Schedule II through V drugs to MassPAT.",
        ],
        "trap": "First identify whether the pharmacy dispensed a patient-specific dose; administration is a separate act.",
        "steps": [
            "Identify the pharmacy-to-clinic workflow as a patient-specific dispensing",
            "Classify Sublocade as Schedule III",
            "Apply the Massachusetts dispenser reporting rule",
        ],
    },
    "MA-Q-0031": {
        "stem": "A community pharmacy fills a patient-specific midazolam prescription for home use. The claim is cash-paid and the drug is not an opioid. What should the pharmacist do about MassPAT?",
        "choices": _choices(
            "Report the dispensing because it is Schedule IV.",
            "Exclude it because the claim was paid in cash.",
            "Exclude it because midazolam is not an opioid.",
            "Report only if more than seven days are supplied.",
            "Submit it with the pharmacy's inventory report at month-end.",
        ),
        "correct_choice_ids": ["A"],
        "core": "The transaction is a covered outpatient pharmacy dispensing of a Schedule IV drug. Payment method and non-opioid status do not remove it from the Massachusetts dispenser reporting requirement.",
        "analysis": {
            "A": "Correct. Covered Schedule IV dispensing is reportable.",
            "B": "Cash payment is not a reporting exemption.",
            "C": "MassPAT coverage is not limited to opioids.",
            "D": "The general reporting trigger does not depend on a seven-day quantity threshold.",
            "E": "PMP dispensing data are not monthly inventory reports.",
        },
        "facts": [
            "Midazolam is federal and Massachusetts Schedule IV.",
            "Covered pharmacies report prescription dispensings of Schedule II through V drugs to MassPAT.",
        ],
        "trap": "Separate therapeutic class and payment method from the schedule-based reporting trigger.",
        "steps": [
            "Identify a covered outpatient dispensing",
            "Classify midazolam as Schedule IV",
            "Reject payment and therapeutic-class distractions",
        ],
    },
    "MA-Q-0037": {
        "stem": "A pharmacist fills Belsomra for home use. A coworker says the transaction is not reportable because the drug is neither an opioid nor a benzodiazepine. Which response is correct?",
        "choices": _choices(
            "Agree; MassPAT is limited to those two drug classes.",
            "Agree; insomnia drugs are Massachusetts Schedule VI.",
            "Report it because covered Schedule IV dispensing is reportable.",
            "Report it only after the fifth refill.",
            "Omit it unless the prescriber requests reporting.",
        ),
        "correct_choice_ids": ["C"],
        "core": "Belsomra is Schedule IV, and the stated outpatient dispensing is covered by MassPAT. Reportability does not depend on the drug being an opioid or benzodiazepine.",
        "analysis": {
            "A": "MassPAT reporting extends beyond opioids and benzodiazepines.",
            "B": "Suvorexant remains Schedule IV despite its insomnia indication.",
            "C": "Correct. Schedule IV status brings the covered dispensing within the reporting rule.",
            "D": "Reporting occurs for each covered dispensing, not only after a refill threshold.",
            "E": "Prescriber preference does not control pharmacy PMP reporting.",
        },
        "facts": [
            "Belsomra (suvorexant) is federal and Massachusetts Schedule IV.",
            "Covered Massachusetts pharmacy dispensings of Schedule II through V drugs are reportable to MassPAT.",
        ],
        "trap": "A nonbenzodiazepine hypnotic can still be controlled and reportable.",
        "steps": [
            "Classify Belsomra as Schedule IV",
            "Apply the schedule-based MassPAT reporting rule",
            "Reject therapeutic-class exclusions not found in the reporting rule",
        ],
    },
    "MA-Q-0058": {
        "stem": "On Friday morning, a pharmacy discovers a significant unexplained loss of controlled substances. The investigation cannot be completed that day. Which federal response is correct?",
        "choices": _choices(
            "Wait for the investigation before contacting DEA.",
            "Give oral notice within 24 hours and take no further action.",
            "File Form 106 within one business day instead of separate notice.",
            "Send written DEA notice within one business day and Form 106 within 45 calendar days.",
            "Notify only the Massachusetts Board because the loss occurred in Massachusetts.",
        ),
        "correct_choice_ids": ["D"],
        "core": "The registrant must give the responsible DEA Field Division written notice within one business day of discovery. The separate complete and accurate electronic DEA Form 106 is due within 45 calendar days after discovery, allowing the investigation to inform the documentation without delaying initial notice.",
        "analysis": {
            "A": "The investigation does not postpone the one-business-day written notice.",
            "B": "Oral notice alone does not satisfy the written notice and Form 106 duties.",
            "C": "The regulation creates separate notice and Form 106 requirements with different deadlines.",
            "D": "Correct. Initial written notice and Form 106 completion run on distinct clocks.",
            "E": "State reporting cannot replace the registrant's federal duties.",
        },
        "facts": [
            "Written notice to the responsible DEA Field Division is due within one business day after discovery.",
            "A complete and accurate electronic DEA Form 106 is due within 45 calendar days after discovery.",
            "The duties apply even if the drugs are later recovered or responsible parties are identified.",
        ],
        "trap": "Do not collapse the initial-notification deadline into the later Form 106 completion deadline.",
        "steps": [
            "Identify the event as a significant loss",
            "Apply the one-business-day written-notice clock",
            "Apply the separate 45-calendar-day Form 106 clock",
        ],
    },
}


NATURAL_SBA_DISTRACTORS: dict[str, dict[str, str]] = {
    "MA-Q-0013": {"A": "Reject it because all out-of-state Schedule II prescriptions are prohibited."},
    "MA-Q-0014": {"A": "Use the 72-hour rule for a pharmacy stock shortage."},
    "MA-Q-0016": {"B": "Dispense eight days because extended-release products are exempt."},
    "MA-Q-0019": {"A": "Print the electronic prescription and fax the image."},
    "MA-Q-0027": {"A": "Reject it after five days under the Schedule II narcotic rule."},
    "MA-Q-0028": {"A": "Honor the sixth refill because it appears on the original."},
    "MA-Q-0029": {"A": "Dispense because unused refills remain valid for one year."},
    "MA-Q-0032": {"A": "Dispense because the six-month period remains open."},
    "MA-Q-0034": {"A": "Fill it because federal Schedule IV authority lasts six months."},
    "MA-Q-0035": {"A": "Decline because four prior refills exhaust the federal limit."},
    "MA-Q-0036": {"B": "Transfer it even if the original prescription was paper."},
    "MA-Q-0038": {"A": "Check only whether five refills have been completed."},
    "MA-Q-0052": {"A": "Finish the root-cause analysis before contacting the patient."},
    "MA-Q-0054": {"A": "Close the event after correcting the individual prescription."},
    "MA-Q-0066": {"B": "Wait until a missing form is used before reporting it."},
    "MA-Q-0068": {"A": "Email a scanned Form 222 with an ordinary electronic signature."},
}


NATURAL_SBA_CORRECT: dict[str, str] = {
    "MA-Q-0013": "Dispense under the nonnarcotic Schedule II out-of-state pathway after verification.",
    "MA-Q-0014": "Dispense the documented remainder at the same pharmacy before the 30-day issue-date deadline.",
    "MA-Q-0016": "The initial outpatient opiate supply is limited to seven days absent a documented statutory exception.",
    "MA-Q-0019": "Use a one-time pharmacist-to-pharmacist electronic transfer after confirming state permission and federal compliance.",
    "MA-Q-0027": "The prescription falls within the 30-day out-of-state Schedule IV pathway after verification.",
    "MA-Q-0029": "The prescription is no longer refillable six months after issue.",
    "MA-Q-0034": "The Massachusetts 30-day out-of-state window has expired.",
    "MA-Q-0035": "One additional refill remains within both the five-refill cap and six-month deadline.",
    "MA-Q-0036": "Confirm no prior transfer, preserve the electronic record, and verify state permission.",
    "MA-Q-0038": "Check both the five-refill cap and the six-month issue-date deadline.",
    "MA-Q-0052": "Notify the patient, give harm-minimization directions, and contact the prescriber as professional judgment requires.",
    "MA-Q-0054": "Analyze causes and system factors, then use the findings to improve the process.",
    "MA-Q-0066": "Immediately report the missing forms and available details to DEA.",
    "MA-Q-0068": "Use CSOS software and a valid DEA-issued digital certificate.",
}


SATA_REWRITES: dict[str, dict[str, Any]] = {
    "MA-Q-0041": {
        "stem": "A Massachusetts pharmacy receives a 90-day Depo-Testosterone prescription with two refills. Which statements should the pharmacist apply? Select all that apply.",
        "choices": _choices(
            "A non-opioid Schedule III drug may qualify for a 90-day single fill.",
            "Each covered dispensing is reportable to MassPAT.",
            "Any refills remain subject to federal count and time limits.",
            "Hormone therapy makes the product Schedule VI.",
            "A 90-day fill removes federal refill restrictions.",
        ),
        "key": ["A", "B", "C"],
    },
    "MA-Q-0042": {
        "stem": "The profile shows a phentermine prescription issued four months earlier; four refills have been dispensed and one remains. Which conclusions govern the next fill? Select all that apply.",
        "choices": _choices(
            "The remaining refill may be dispensed before the six-month deadline.",
            "The dispensing is reportable to MassPAT.",
            "The prescription remains refillable for one year.",
            "Phentermine is Schedule II and cannot be refilled.",
            "Weight-loss drugs are excluded from MassPAT.",
        ),
        "key": ["A", "B"],
    },
    "MA-Q-0043": {
        "stem": "A prescriber orders a 90-day supply of phendimetrazine and authorizes refills. Which legal limits govern the pharmacy? Select all that apply.",
        "choices": _choices(
            "Schedule III status permits unlimited refills.",
            "A non-opioid Schedule III prescription may qualify for a single fill of up to 90 days.",
            "Authorized refills remain subject to federal count and time limits.",
            "The weight-loss indication does not change the drug's Schedule III status.",
            "Massachusetts treats the product as Schedule VI.",
        ),
        "key": ["B", "C", "D"],
    },
    "MA-Q-0044": {
        "stem": "A patient requests an authorized refill of Provigil at a Massachusetts pharmacy. Which schedule-based duties govern the transaction? Select all that apply.",
        "choices": _choices(
            "Modafinil is federally noncontrolled.",
            "The prescription expires five days after issue.",
            "Schedule IV refill count and timing limits apply.",
            "Covered dispensing is reportable to MassPAT.",
            "The pharmacist may create a new prescription after five refills.",
        ),
        "key": ["C", "D"],
    },
    "MA-Q-0045": {
        "stem": "A ketamine prescription is presented to a Massachusetts community pharmacy. Which statements must be considered? Select all that apply.",
        "choices": _choices(
            "Ketamine is Schedule II and cannot be refilled.",
            "Massachusetts treats ketamine as Schedule VI.",
            "Schedule III refill limits apply to authorized refills.",
            "Covered outpatient dispensing is reportable to MassPAT.",
            "Its anesthetic indication does not change Schedule III status.",
        ),
        "key": ["C", "D", "E"],
    },
    "MA-Q-0046": {
        "stem": "Before filling Fycompa, profile review shows an issue date five months ago and three of five refills used. Select every correct conclusion.",
        "choices": _choices(
            "The federal six-month issue-date deadline still applies.",
            "Stable seizure control permits indefinite refills.",
            "Antiseizure use makes Fycompa noncontrolled.",
            "A new prescription is required after every fill because it is Schedule II.",
            "Covered Schedule III dispensing is reportable to MassPAT.",
        ),
        "key": ["A", "E"],
    },
    "MA-Q-0047": {
        "stem": "Before dispensing an FDA-approved Xyrem product, a pharmacist checks its controlled-substance and product-specific requirements. Which statements are correct? Select all that apply.",
        "choices": _choices(
            "Current product-specific REMS requirements must be satisfied.",
            "Federal Schedule III refill limits remain applicable.",
            "The approved product falls within the federal Schedule III sodium oxybate exception.",
            "REMS compliance does not replace controlled-substance record duties.",
            "REMS enrollment changes the product to Schedule VI.",
        ),
        "key": ["A", "B", "C", "D"],
    },
    "MA-Q-0048": {
        "stem": "Marinol is presented with authorized refills at a Massachusetts pharmacy. Which schedule and reporting conclusions control? Select all that apply.",
        "choices": _choices(
            "Schedule III refill limits apply.",
            "Every cannabinoid product is Schedule I.",
            "The prescription remains refillable for 12 months.",
            "Covered dispensing is reportable to MassPAT.",
            "The six-month deadline applies even if refills remain.",
        ),
        "key": ["A", "D", "E"],
    },
    "MA-Q-0049": {
        "stem": "A pharmacist compares Syndros oral solution with Marinol capsules. Which statements apply to Syndros? Select all that apply.",
        "choices": _choices(
            "Its Schedule II prescription may not be refilled.",
            "The Massachusetts 30-day Schedule II validity period applies.",
            "It follows the Schedule III refill rule used for Marinol.",
            "The liquid dosage form makes it Schedule VI.",
            "Syndros is Schedule II although Marinol capsules are Schedule III.",
        ),
        "key": ["A", "B", "E"],
    },
    "MA-Q-0050": {
        "stem": "A Massachusetts pharmacy reviews a Lomotil prescription and its dispensing history. Which statements are correct? Select all that apply.",
        "choices": _choices(
            "Lomotil is an unrestricted Schedule VI drug.",
            "Massachusetts Schedule V refill limits apply.",
            "Covered Schedule V dispensing is reportable to MassPAT.",
            "The prescription remains refillable for one year.",
            "The Schedule II 30-day validity rule controls each refill.",
        ),
        "key": ["B", "C"],
    },
    "MA-Q-0073": {
        "stem": "A resident pharmacy will close in three weeks. Which actions are required to protect patients? Select all that apply.",
        "choices": _choices(
            "Identify patients who received prescriptions during the preceding 90 days.",
            "Destroy patient files on the closure date.",
            "Attempt patient notice at least 14 days before closure and post a conspicuous notice.",
            "Process requested file transfers promptly enough to avoid interrupting therapy.",
            "Notify only patients who received controlled substances.",
        ),
        "key": ["A", "C", "D"],
    },
    "MA-Q-0074": {
        "stem": "A resident pharmacy closed yesterday after transferring its controlled-substance stock lawfully. Which post-closure duties remain? Select all that apply.",
        "choices": _choices(
            "Keep unused controlled stock indefinitely at the closed premises.",
            "Submit the original licenses and controlled-substance registration within 14 days.",
            "Attest to the lawful disposal or transfer of controlled substances.",
            "Wait one year before notifying the Board.",
            "Complete the required post-closure submission within 14 days after closing.",
        ),
        "key": ["B", "C", "E"],
    },
    "MA-Q-0075": {
        "stem": "At pickup, a technician trainee encounters a patient question and an unresolved DUR alert. Which assignments comply with Massachusetts personnel rules? Select all that apply.",
        "choices": _choices(
            "Allow the trainee to counsel the patient independently.",
            "Allow the trainee to resolve the DUR alert independently.",
            "Treat trainee registration as pharmacist-intern licensure.",
            "Limit the trainee to duties authorized for that category under pharmacist supervision.",
            "Keep professional-judgment decisions with the pharmacist.",
        ),
        "key": ["D", "E"],
    },
    "MA-Q-0076": {
        "stem": "A pharmacy assigns support personnel to receive and process Schedule II stock. Which safeguards apply? Select all that apply.",
        "choices": _choices(
            "Use only a personnel category authorized for the assigned step by 247 CMR 8.05.",
            "Permit every technician trainee to receive Schedule II stock independently.",
            "Maintain pharmacist supervision and pharmacist-only professional functions.",
            "Allow a cashier to perform any handling step with manager approval.",
            "Ignore personnel-scope rules because the product is Schedule II.",
        ),
        "key": ["A", "C"],
    },
    "MA-Q-0077": {
        "stem": "A pharmacy schedules an intern for a shift without a pharmacist preceptor directing the work. Which statements are correct? Select all that apply.",
        "choices": _choices(
            "A senior technician may serve as the preceptor.",
            "The intern must work under direct supervision of a registered pharmacist preceptor.",
            "Five hundred internship hours permit independent prescription verification.",
            "Intern status does not authorize independent pharmacist practice.",
            "The pharmacist preceptor remains responsible for the supervision relationship.",
        ),
        "key": ["B", "D", "E"],
    },
    "MA-Q-0078": {
        "stem": "A student works a 14-hour pharmacy shift and asks to record every hour as internship credit. Which statements are correct? Select all that apply.",
        "choices": _choices(
            "All 14 hours count because the student remained on site.",
            "No more than 12 hours may be credited for that day.",
            "The rule caps credit at eight hours per week.",
            "Working additional hours does not increase the daily credit cap.",
            "Only time handling controlled substances counts.",
        ),
        "key": ["B", "D"],
    },
    "MA-Q-0079": {
        "stem": "A pharmacist plans continuing education for the two-year Massachusetts renewal cycle. Which statements are generally correct? Select all that apply.",
        "choices": _choices(
            "Complete at least 20 contact hours in each calendar year.",
            "Include at least two contact hours of pharmacy law each calendar year.",
            "Use no more than 15 home-study hours in a calendar year absent an exception.",
            "Carry unused hours freely into the next calendar year.",
            "Do not carry unused annual hours into the next calendar year.",
        ),
        "key": ["A", "B", "C", "E"],
    },
    "MA-Q-0080": {
        "stem": "A pharmacist directly oversees both sterile and complex nonsterile compounding. Which continuing-education statements are correct? Select all that apply.",
        "choices": _choices(
            "Meet the applicable annual sterile-compounding CE requirement.",
            "Use general pharmacy-law CE in place of all compounding CE.",
            "Also assess the annual complex-nonsterile compounding CE requirement.",
            "Apply compounding CE only to technicians.",
            "Treat the applicable requirements as cumulative when both activities are supervised.",
        ),
        "key": ["A", "C", "E"],
    },
    "MA-Q-0081": {
        "stem": "A Massachusetts pharmacist is evaluating eligibility to enter a collaborative practice agreement that includes prescribing. Which qualifications are required? Select all that apply.",
        "choices": _choices(
            "Hold a current unrestricted Massachusetts license, practice in the Commonwealth, and maintain the required $1,000,000 liability coverage.",
            "Complete five years as a licensed pharmacist or satisfy the pre-July 2017 PharmD grandfather or a Board-equivalent education/residency pathway.",
            "Devote practice to the defined therapy area and complete five additional related CE contact hours in each agreement year.",
            "For prescriptive practice, maintain the required state controlled-substance registration, complete required training, and submit the MassHealth participation attestation.",
            "A current PharmD alone satisfies the experience requirement regardless of when the agreement begins.",
        ),
        "key": ["A", "B", "C", "D"],
        "facts": [
            "247 CMR 16.02(1)(a)-(e) requires current unrestricted Massachusetts licensure and practice, specified liability coverage, an experience or qualifying alternative pathway, therapy-area practice, and five additional related CE contact hours each agreement year.",
            "The experience alternatives are a PharmD plus an agreement entered by June 30, 2017, or education/residency criteria the Board determines equivalent to five years of licensed experience.",
            "When prescribing is included, 247 CMR 16.02(1)(f) adds state controlled-substance registration, statutory training, and a signed MassHealth participation/application attestation.",
        ],
        "steps": [
            "Apply the baseline licensure, insurance, experience, practice-focus, and CE requirements",
            "Distinguish five years of experience from the grandfather and Board-equivalent pathways",
            "Add the subsection (f) requirements because prescribing is included",
        ],
    },
    "MA-Q-0082": {
        "stem": "A retail collaborative program receives a physician referral for an adult patient who has not yet consented. Which limits apply before the pharmacist acts? Select all that apply.",
        "choices": _choices(
            "Obtain the required patient notice and consent.",
            "Stay within the agreement, referral, authorized disease states, and retail scope.",
            "Use the written agreement and supervising-physician framework.",
            "Diagnose an unrelated disease independently.",
            "Enroll any walk-in patient automatically.",
        ),
        "key": ["A", "B", "C"],
    },
    "MA-Q-0083": {
        "stem": "A proposed retail collaborative agreement would let a pharmacist prescribe alprazolam and methylphenidate. Which statements are correct? Select all that apply.",
        "choices": _choices(
            "$1,000,000 liability coverage waives the schedule restriction.",
            "Only Schedule II prescribing is prohibited.",
            "The agreement cannot authorize prescribing Schedule II through V drugs.",
            "A supervising physician's signature does not remove that prohibition.",
            "Schedule VI prescribing requires separate compliance with retail CDTM limits.",
        ),
        "key": ["C", "D", "E"],
    },
    "MA-Q-0084": {
        "stem": "A retail collaborating pharmacist issues an authorized Schedule VI prescription for the patient's referred diagnosis. Which actions are required? Select all that apply.",
        "choices": _choices(
            "Add Schedule II refills under the same agreement.",
            "Keep the prescription within the diagnosis and agreement scope.",
            "Send a copy to the supervising physician within 24 hours.",
            "Delay physician notice until the agreement is renewed.",
            "Document the prescription in the patient's collaborative-practice record.",
        ),
        "key": ["B", "C", "E"],
    },
    "MA-Q-0085": {
        "stem": "Prospective review identifies a clinically significant interaction before dispensing. Which actions are appropriate? Select all that apply.",
        "choices": _choices(
            "Ignore the alert because the prescription was electronically signed.",
            "Delegate final resolution to a cashier.",
            "Evaluate and resolve the issue before dispensing using professional judgment.",
            "Dispense first and review the interaction next month.",
            "Contact the prescriber or patient when needed to resolve the concern.",
        ),
        "key": ["C", "E"],
    },
    "MA-Q-0086": {
        "stem": "A pharmacy redesigns its patient-counseling workflow around a pickup signature. Which principles remain applicable? Select all that apply.",
        "choices": _choices(
            "Provide the meaningful counseling opportunity required by 247 CMR 9.18.",
            "Treat every pickup signature as proof that counseling was adequate.",
            "Delegate counseling to an unlicensed cashier.",
            "Use pharmacist judgment and patient-specific information.",
            "Omit counseling whenever a Medication Guide is supplied.",
        ),
        "key": ["A", "D"],
    },
    "MA-Q-0087": {
        "stem": "A lower-priced product is reasonably available and appears on the Massachusetts interchangeable-drug list, but the prescriber marked a valid no-substitution direction. Which facts control? Select all that apply.",
        "choices": _choices(
            "Determine whether the no-substitution direction is valid.",
            "Confirm that the proposed product is listed as interchangeable.",
            "Substitute any drug in the same therapeutic class.",
            "Confirm that the proposed product is reasonably available at a lower retail price.",
            "Honor a valid prescriber direction against substitution.",
        ),
        "key": ["A", "B", "D", "E"],
    },
    "MA-Q-0088": {
        "stem": "A patient returns an unopened bottle that the pharmacy dispensed in error. Which actions are permitted or required? Select all that apply.",
        "choices": _choices(
            "Accept the medication under the dispensing-error return pathway.",
            "Return the sealed bottle directly to saleable stock.",
            "Quarantine it pending proper disposition.",
            "Keep it out of saleable inventory.",
            "Arrange proper disposal after quarantine.",
        ),
        "key": ["A", "C", "D", "E"],
    },
    "MA-Q-0089": {
        "stem": "A pharmacist discovers a dispensing error while the patient may still be exposed to harm. Which duties apply? Select all that apply.",
        "choices": _choices(
            "Immediately notify the patient or representative and give correction and harm-minimization directions.",
            "Finish root-cause analysis before contacting the patient.",
            "Always notify the patient before the prescriber in a strict sequence.",
            "Immediately notify the prescriber when professional judgment indicates it is warranted.",
            "Complete the initial QRE documentation within 24 hours after discovery or notification.",
        ),
        "key": ["A", "D", "E"],
    },
    "MA-Q-0090": {
        "stem": "A resident pharmacy will close in 20 days. Which timing and transfer statements are correct? Select all that apply.",
        "choices": _choices(
            "Delay patient-file transfers until all controlled stock is disposed of.",
            "Send the Board certified written notice at least 14 days before closure.",
            "Identify patients served in the preceding 90 days and attempt notice at least 14 days before closure.",
            "Handle requested file transfers promptly enough to avoid delaying therapy.",
            "Within 14 days after closure, submit original credentials and the controlled-substance disposition attestation.",
        ),
        "key": ["B", "C", "D", "E"],
    },
}


STEM_REWRITES = {
    "MA-Q-0013": "A Massachusetts pharmacy receives a Focalin prescription issued four days ago by a properly registered New Hampshire prescriber. The pharmacist verifies the prescription and prescriber. Which conclusion is most defensible?",
    "MA-Q-0014": "A patient requested a partial fill of Dexedrine at this pharmacy 12 days after issue and returns for the documented balance on day 28. Which rule controls?",
    "MA-Q-0016": "An adult receiving an outpatient opiate for acute pain for the first time presents an eight-day OxyContin prescription with no exception documentation. What is the key issue?",
    "MA-Q-0019": "At the patient's request, one DEA-registered retail pharmacy is asked to transfer an unfilled electronic MS Contin prescription to another DEA-registered retail pharmacy. Which pathway applies?",
    "MA-Q-0027": "A Massachusetts pharmacy receives an Ativan prescription issued 20 days ago by a properly authorized Connecticut practitioner. The pharmacist verifies the prescription and prescriber. What is the key determination?",
    "MA-Q-0028": "A Klonopin prescription states six refills, and the pharmacy has already dispensed five refills within five months. What should the pharmacist recognize about the requested sixth refill?",
    "MA-Q-0029": "A Valium prescription with unused refills was issued seven months ago. Which federal deadline controls?",
    "MA-Q-0032": "A Halcion prescription is five months old and has already been refilled five times. Which fact prevents another refill?",
    "MA-Q-0034": "A patient presents an otherwise authentic out-of-state Ambien prescription 31 days after issue. What is the Massachusetts consequence?",
    "MA-Q-0035": "A Lunesta prescription is four months old and has four prior refills, with one additional refill authorized. What is the most defensible conclusion?",
    "MA-Q-0036": "A patient requests transfer of an unfilled electronic Sonata prescription to a second DEA-registered retail pharmacy. Both pharmacists can communicate directly. What else must be confirmed?",
    "MA-Q-0038": "A Dayvigo prescription is three months old and has two completed refills. Which federal limits must the pharmacist check before the next refill?",
    "MA-Q-0052": "A pharmacist discovers that the wrong strength was dispensed yesterday and the patient may still be taking it. What is the immediate priority?",
    "MA-Q-0054": "A pharmacy corrects repeated product-selection errors but never examines shelving, staffing, or workflow. Which CQI duty remains unmet?",
    "MA-Q-0066": "A pharmacy discovers that several unused DEA Forms 222 are missing. What is the first regulatory response?",
    "MA-Q-0068": "A purchaser wants to replace paper Form 222 orders with electronic Schedule II ordering. What is required?",
}


def _standard_sata_explanation(question: dict[str, Any]) -> None:
    correct = set(question["correct_choice_ids"])
    analyses: dict[str, str] = {}
    for choice in question["choices"]:
        if choice["id"] in correct:
            analyses[choice["id"]] = f"Supported: {choice['text']}"
        else:
            analyses[choice["id"]] = f"Not supported: {choice['text']}"
    selected = [choice["text"] for choice in question["choices"] if choice["id"] in correct]
    question["explanation"]["core_reasoning"] = "The supported conclusions on these facts are: " + " ".join(selected)
    question["explanation"]["choice_analysis"] = analyses
    first_wrong = next(
        (choice["text"] for choice in question["choices"] if choice["id"] not in correct),
        None,
    )
    question["explanation"]["mpje_trap"] = (
        f"Distinguish this near-miss from the controlling rule: '{first_wrong}'"
        if first_wrong
        else "Every listed qualification is required because the agreement expressly includes prescribing."
    )


def _apply_sba(question: dict[str, Any], rewrite: dict[str, Any]) -> None:
    question["stem"] = rewrite["stem"]
    question["choices"] = rewrite["choices"]
    question["correct_choice_ids"] = rewrite["correct_choice_ids"]
    question["explanation"]["core_reasoning"] = rewrite["core"]
    question["explanation"]["choice_analysis"] = rewrite["analysis"]
    question["explanation"]["related_facts"] = rewrite["facts"]
    question["explanation"]["mpje_trap"] = rewrite["trap"]
    question["reasoning_steps"] = rewrite["steps"]
    if "rule_ids" in rewrite:
        question["rule_ids"] = rewrite["rule_ids"]


def _apply_natural_sba(question: dict[str, Any]) -> None:
    question["stem"] = STEM_REWRITES[question["question_id"]]
    replacements = NATURAL_SBA_DISTRACTORS[question["question_id"]]
    for choice in question["choices"]:
        if choice["id"] in replacements:
            choice["text"] = replacements[choice["id"]]
    key = question["correct_choice_ids"][0]
    if question["question_id"] in NATURAL_SBA_CORRECT:
        for choice in question["choices"]:
            if choice["id"] == key:
                choice["text"] = NATURAL_SBA_CORRECT[question["question_id"]]
    correct_text = next(choice["text"] for choice in question["choices"] if choice["id"] == key)
    first_wrong = next(choice["text"] for choice in question["choices"] if choice["id"] != key)
    question["explanation"]["core_reasoning"] = (
        f"{correct_text} By contrast, '{first_wrong}' uses a legal trigger absent from the stem."
    )
    question["explanation"]["choice_analysis"] = {
        choice["id"]: (
            f"The stated facts support this result: {choice['text']}"
            if choice["id"] == key
            else f"This near-miss uses a different trigger: {choice['text']}"
        )
        for choice in question["choices"]
    }
    question["explanation"]["mpje_trap"] = f"Reject '{first_wrong}' because its legal trigger is absent."


def _apply_sata(question: dict[str, Any], rewrite: dict[str, Any]) -> None:
    question["stem"] = rewrite["stem"]
    question["choices"] = rewrite["choices"]
    question["correct_choice_ids"] = rewrite["key"]
    _standard_sata_explanation(question)
    if "facts" in rewrite:
        question["explanation"]["related_facts"] = rewrite["facts"]
    if "steps" in rewrite:
        question["reasoning_steps"] = rewrite["steps"]


def repair_questions() -> list[str]:
    scope = repair_scope()
    frozen = frozen_pr10_hashes()
    paths = {record["question_id"]: path for path, record in load_records(DATA / "questions")}
    before_bytes = {qid: path.read_bytes() for qid, path in paths.items()}

    handled: set[str] = set()
    for qid, rewrite in SBA_REWRITES.items():
        question = load_json(paths[qid])
        _apply_sba(question, rewrite)
        write_json(paths[qid], question)
        handled.add(qid)
    for qid in NATURAL_SBA_DISTRACTORS:
        question = load_json(paths[qid])
        _apply_natural_sba(question)
        write_json(paths[qid], question)
        handled.add(qid)
    for qid, rewrite in SATA_REWRITES.items():
        question = load_json(paths[qid])
        _apply_sata(question, rewrite)
        write_json(paths[qid], question)
        handled.add(qid)

    missing = scope - handled
    extra = handled - scope
    if missing or extra:
        raise ValueError(f"repair implementation mismatch: missing={sorted(missing)}, extra={sorted(extra)}")

    after = {qid: question_audit_hash(load_json(path)) for qid, path in paths.items()}
    changed = {qid for qid in scope if frozen[qid] != after[qid]}
    if changed != scope:
        raise ValueError(f"not every scoped question changed: {sorted(scope - changed)}")
    for qid in sorted(set(frozen) - scope):
        if paths[qid].read_bytes() != before_bytes[qid] or after[qid] != frozen[qid]:
            raise ValueError(f"out-of-scope question changed: {qid}")
    return sorted(changed)


def main() -> int:
    changed = repair_questions()
    print(json.dumps({"changed_count": len(changed), "question_ids": changed}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

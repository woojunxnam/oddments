from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "data" / "questions"

PATCHES = {
    "MA-Q-0136": [
        ("The nurse may load the emergency-kit ADD; routine-dispensing ADD loading is limited to certified technicians or interns under pharmacist supervision.", "The policy uses a broader loader list for emergency-kit use and a narrower supervised loader pathway for routine retail dispensing."),
        ("The nurse may load both machines because the same pharmacy owns both devices and supervises the medication inventory.", "Common ownership does not make the two ADD purposes follow the same loader rule."),
        ("The nurse may load neither machine because routine and emergency ADDs are restricted to pharmacists and pharmacy interns.", "A licensed nurse is an authorized loader for the emergency-kit pathway."),
        ("The nurse may load the routine machine whenever it contains only Schedule VI medications and no federally controlled drugs.", "Limiting inventory to Schedule VI does not broaden the routine-dispensing loader list."),
        ("Both machines use the emergency-kit loader list as long as they are located inside the same Massachusetts retail pharmacy.", "The device's approved purpose, not merely location, determines the applicable loading pathway."),
    ],
    "MA-Q-0138": [
        ("Yes; trainee status is enough when the clinic is licensed and the pharmacist provides remote direction.", "Facility prerequisites still apply to the trainee pathway."),
        ("Yes; limiting the cabinet to Schedule VI removes the location conditions for trainee stocking.", "Schedule does not replace the facility-location requirements."),
        ("No; the pathway requires an on-site pharmacy and an ADD at the same physical address listed on the facility MCSR.", "Both required location conditions are missing in the scenario."),
        ("No; trainees may work with ADD inventory only after becoming nationally certified technicians.", "Eligible trainees have a defined stocking pathway without national certification."),
        ("Yes; a personal DEA registration for the trainee would substitute for the facility-location conditions.", "A personal DEA registration does not cure the facility-location defect."),
    ],
    "MA-Q-0141": [
        ("The cited pharmacy EPT policy covers gonorrhea and chlamydia whenever the partner has not been examined.", "The cited Massachusetts pharmacy EPT policy is not a general STI pathway."),
        ("It does not fit; the cited Massachusetts pharmacy EPT policy is limited to chlamydia treatment.", "The diagnosis in the scenario is outside the policy's chlamydia scope."),
        ("It fits only when gonorrhea is treated with a federally controlled antibiotic.", "Federal controlled-substance status is not the EPT eligibility criterion."),
        ("It fits when the prescription is electronic, even though the diagnosis is gonorrhea alone.", "Prescription format does not expand the policy's diagnosis scope."),
        ("It fits after the partner gives the pharmacy identifying information, regardless of diagnosis.", "Providing identity information does not convert gonorrhea-only treatment into this EPT pathway."),
    ],
    "MA-Q-0151": [
        ("It is a limited bridge for timely palliation until the pharmacy can fill and deliver the full patient prescription.", "The acute-use supply is a bridge to the pharmacy's full patient-specific dispensing."),
        ("It is intended to reduce routine pharmacy deliveries by functioning as standing floor stock for chronic therapy.", "The pathway is not a substitute for routine chronic-medication dispensing."),
        ("It is intended primarily to hold larger reserve quantities when the hospice has frequent Schedule VI use.", "The purpose is timely acute palliation, not inventory expansion based on schedule."),
        ("It is intended mainly for resuscitation drugs used during immediately life-threatening emergencies.", "The circular addresses acute palliative needs rather than a resuscitation-only stock model."),
        ("It transfers ordinary dispensing responsibility from the pharmacy to hospice nursing staff during off-hours.", "The pharmacy remains responsible for the dispensing system and patient-specific supply."),
    ],
    "MA-Q-0153": [
        ("40 units", "Forty units is not the analgesic cap for an 11-20-bed inpatient hospice."),
        ("60 units", "Sixty is the sedative/anticonvulsant cap in this bed tier, not the analgesic cap."),
        ("75 units", "Seventy-five is not the analgesic maximum for the 11-20-bed tier."),
        ("100 units", "An inpatient hospice with 11-20 beds may stock up to 100 Schedule II-V analgesic units in the acute-use ADD."),
        ("150 units", "One hundred fifty is the analgesic cap for the larger bed-capacity tier, not this hospice."),
    ],
    "MA-Q-0162": [
        ("Dispense after confirming the DEA number because registration establishes the prescriber's responsibility for medical purpose.", "A valid registration does not remove the pharmacist's corresponding responsibility."),
        ("Resolve the red flags before dispensing; unresolved legitimacy concerns require declining the fill.", "Corresponding responsibility requires an independent pre-dispensing validity judgment."),
        ("Dispense the first fill, document the concerns, and investigate the red flags before the next dispensing.", "Material red flags must be addressed before the questioned dispensing."),
        ("Change the quantity or directions to a safer-looking regimen without contacting the prescriber, then dispense.", "Unilateral alteration does not establish legitimate medical purpose."),
        ("Transfer the final validity decision to a technician who reviewed the patient's profile and identification.", "The pharmacist retains the professional responsibility for the dispensing decision."),
    ],
    "MA-Q-0166": [
        ("Qualifying Schedule III-V narcotic OUD drugs use a prescription pathway under applicable law; methadone maintenance follows a different federal framework.", "Federal law distinguishes the qualifying Schedule III-V prescription pathway from methadone maintenance."),
        ("A Schedule III narcotic used for OUD is reclassified as Schedule II for the duration of treatment.", "Indication does not reclassify a Schedule III drug."),
        ("Schedule III narcotic OUD therapy must be dispensed through the same OTP pathway used for methadone maintenance.", "The federal framework distinguishes qualifying Schedule III-V prescribing from methadone maintenance."),
        ("The first OUD dose converts the Schedule III medication to noncontrolled status for later outpatient fills.", "Treatment does not remove the drug's federal controlled status."),
        ("The federal OUD rule gives pharmacists independent prescribing authority for qualifying Schedule III-V narcotics.", "The treatment rule does not independently create pharmacist prescriptive authority."),
    ],
    "MA-Q-0168": [
        ("The prescription is invalid because a DEA registration is required for every Massachusetts prescription drug, including Schedule VI.", "Massachusetts Schedule VI status alone does not require a federal DEA registration."),
        ("The MCSR supports Schedule VI-only activity; DEA registration is needed when the practitioner conducts federally controlled Schedule II-V activity.", "The scenario fits the state-only registration distinction for Schedule VI activity."),
        ("The MCSR is relevant only to Schedule I activity, so it does not authorize this Schedule VI prescription.", "The MCSR governs Massachusetts controlled-substance activity beyond Schedule I."),
        ("The pharmacy may place its DEA number on the prescription to cover the practitioner's missing federal registration.", "A pharmacy cannot supply prescriber registration authority by substituting its own DEA number."),
        ("Schedule VI prescribing requires neither an MCSR nor DEA registration when the drug is not federally controlled.", "Schedule VI activity still requires the appropriate Massachusetts registration."),
    ],
    "MA-Q-0180": [
        ("Alprazolam", "Alprazolam is Schedule IV, which falls within the trainee's permitted Schedule III-VI range."),
        ("Pregabalin", "Pregabalin is Schedule V, so pharmacist-verified stock is within the trainee stocking boundary."),
        ("Gabapentin", "Gabapentin is Massachusetts Schedule VI; its PMP status does not move it outside the verified-stock trainee range."),
        ("Warfarin", "Warfarin is an ordinary Massachusetts Schedule VI prescription drug and therefore fits the verified-stock range."),
        ("Methylphenidate", "Methylphenidate is Schedule II, which is outside the trainee's Schedule III-VI stocking authority."),
    ],
    "MA-Q-0186": [
        ("The hospice Schedule II narcotic exception treats this fax as the original prescription.", "Oxycodone is a Schedule II narcotic and the prescription carries the required hospice status fact."),
        ("The fax can be used as the original after oxycodone is changed to Schedule III for hospice dispensing.", "Hospice use does not reclassify oxycodone from Schedule II."),
        ("The fax requires the seven-day follow-up process used for an emergency oral Schedule II authorization.", "That follow-up rule belongs to emergency oral authorization, not this hospice fax exception."),
        ("The fax exception also permits refills because the patient is receiving hospice care.", "The transmission exception does not create Schedule II refill authority."),
        ("The fax exception excludes opioid narcotics and applies to nonnarcotic Schedule II drugs instead.", "The hospice exception is specifically relevant to Schedule II narcotics."),
    ],
    "MA-Q-0190": [
        ("72 hours", "The 72-hour remainder rule addresses a different Schedule II partial-fill situation."),
        ("7 days", "Seven days is associated with an emergency oral Schedule II follow-up rule, not this LTCF endpoint."),
        ("90 days", "Ninety days is not the special federal LTCF/terminal partial-fill duration for one prescription."),
        ("60 days", "The LTCF/terminally ill Schedule II pathway permits partial filling for up to 60 days from issue unless discontinued sooner."),
        ("6 months", "Six months resembles other controlled-substance refill frameworks and does not govern this Schedule II pathway."),
    ],
    "MA-Q-0195": [
        ("The provision creates a three-day retail prescription that the pharmacy may dispense in a single fill.", "The emergency provision is not a routine retail-prescription exception."),
        ("No. The practitioner dispenses one day at a time for up to three days while arranging referral; no retail prescription is authorized.", "The rule is a narrow practitioner-dispensing bridge with daily and three-day limits."),
        ("The pharmacy may create a three-day methadone prescription after documenting the practitioner's telephone request.", "A pharmacy cannot create the practitioner's controlled-substance prescribing authority."),
        ("The practitioner cannot use emergency dispensing outside an OTP even while arranging an immediate treatment referral.", "Federal law contains the narrow non-OTP emergency dispensing pathway."),
        ("The practitioner may issue a 30-day prescription and mark the first three days as emergency supply.", "That structure does not comply with the dispense-only emergency pathway."),
    ],
}

# These SATA items originally used three correct choices. Each replacement converts
# one legally false distractor into a fourth independently true proposition supported
# by the same cited rule/fact set. This reduces a bank-wide three-answer construction
# bias without weakening the substantive legal distinction being tested.
FOUR_CORRECT_PATCHES = {
    "MA-Q-0134": ("D", "Retain retrievable ADD records for at least two years as required by the device policy.", "The ADD policy requires retention of the device records for at least two years."),
    "MA-Q-0135": ("D", "Use single-dose or person-specific packaging that preserves medication identity and traceability.", "Appropriate single-dose/person packaging supports ADD product integrity and traceability."),
    "MA-Q-0137": ("D", "Maintain transaction and reconciliation records for the routine ADD program.", "Routine ADD use remains subject to device transaction and reconciliation accountability."),
    "MA-Q-0140": ("D", "Transfer qualifying stock in manufacturer-sealed or original packaging without further manipulation.", "The no-prior-verification shortcut requires qualifying stock to be transferred without further manipulation."),
    "MA-Q-0152": ("D", "Keep medications in the hospice ADD as pharmacy property until they are dispensed.", "The hospice ADD pathway preserves pharmacy ownership until dispensing."),
    "MA-Q-0161": ("D", "End further partial dispensing from the prescription when it is discontinued, even before 60 days have elapsed.", "Discontinuation ends use of the prescription sooner than the outer 60-day period."),
    "MA-Q-0163": ("D", "Treat technical EPCS authentication as separate from the substantive legitimate-medical-purpose determination.", "Technical authenticity does not by itself resolve the pharmacist's corresponding-responsibility inquiry."),
    "MA-Q-0165": ("D", "Use the emergency provision only as a short bridge while referral for treatment is being arranged.", "The non-OTP emergency pathway exists to bridge the patient while referral is arranged."),
    "MA-Q-0167": ("D", "Keep Schedule VI activity within the practitioner's Massachusetts MCSR authority even though Schedule VI alone does not require DEA registration.", "Schedule VI remains state-controlled activity requiring appropriate MCSR authority."),
    "MA-Q-0169": ("D", "Continue to apply ordinary packaging and labeling requirements to qualifying maintenance medications placed in the package.", "The maintenance-medication allowance does not waive other packaging and labeling requirements."),
    "MA-Q-0170": ("D", "Report medication losses according to the applicable pharmacy licensing-body requirements.", "ADD accountability includes reporting medication losses under applicable licensing requirements."),
    "MA-Q-0175": ("D", "Keep the administered dose tied to the patient-specific prescription rather than treating it as anonymous floor stock.", "The mental-health administration pathway remains patient-specific."),
    "MA-Q-0181": ("D", "Remove expired pharmacist-verified methylphenidate stock using the required electronic validation process.", "A licensed non-trainee technician may perform verified Schedule II-VI expired-stock removal with electronic validation."),
    "MA-Q-0193": ("D", "Methadone remains Schedule II whether it is used for pain or for opioid-use-disorder treatment.", "Indication changes the treatment pathway but does not reclassify methadone."),
}


def _load(qid: str) -> tuple[Path, dict]:
    path = QUESTIONS / f"{qid.lower()}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, question: dict) -> None:
    path.write_text(json.dumps(question, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_text_patches() -> None:
    for qid, rows in PATCHES.items():
        path, question = _load(qid)
        if len(question["choices"]) != len(rows):
            raise RuntimeError(f"{qid}: choice count changed")
        for choice, (text, analysis) in zip(question["choices"], rows):
            choice["text"] = text
            question["explanation"]["choice_analysis"][choice["id"]] = analysis
        _write(path, question)


def apply_four_correct_patches() -> None:
    for qid, (choice_id, text, analysis) in FOUR_CORRECT_PATCHES.items():
        path, question = _load(qid)
        if question["question_type"] != "SATA" or len(question["correct_choice_ids"]) != 3:
            raise RuntimeError(f"{qid}: expected a three-correct SATA before repair")
        choice = next(item for item in question["choices"] if item["id"] == choice_id)
        if choice_id in question["correct_choice_ids"]:
            raise RuntimeError(f"{qid}: {choice_id} already correct")
        choice["text"] = text
        question["explanation"]["choice_analysis"][choice_id] = analysis
        question["correct_choice_ids"] = sorted(question["correct_choice_ids"] + [choice_id])
        _write(path, question)


def redistribute_sata_keys() -> None:
    # Most newly authored SATAs originally placed true statements first, producing
    # an artificial ABC key signature. Rotate the actual choice content by QID in a
    # deterministic five-way cycle, then relabel positions A-E and remap analyses.
    ids = "ABCDE"
    for number in range(131, 211):
        qid = f"MA-Q-{number:04d}"
        path, question = _load(qid)
        if question["question_type"] != "SATA":
            continue
        old_choices = question["choices"]
        old_analysis = question["explanation"]["choice_analysis"]
        old_correct = set(question["correct_choice_ids"])
        shift = number % 5
        rotated = old_choices[shift:] + old_choices[:shift]
        new_choices = []
        new_analysis = {}
        new_correct = []
        for new_id, old_choice in zip(ids, rotated):
            old_id = old_choice["id"]
            new_choices.append({"id": new_id, "text": old_choice["text"]})
            new_analysis[new_id] = old_analysis[old_id]
            if old_id in old_correct:
                new_correct.append(new_id)
        question["choices"] = new_choices
        question["correct_choice_ids"] = new_correct
        question["explanation"]["choice_analysis"] = new_analysis
        _write(path, question)


def main() -> int:
    apply_text_patches()
    apply_four_correct_patches()
    redistribute_sata_keys()
    print(
        f"repaired Batch 2 quality: {len(PATCHES)} wording/duplicate patches, "
        f"{len(FOUR_CORRECT_PATCHES)} SATA count repairs, deterministic SATA key redistribution"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

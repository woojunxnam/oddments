from __future__ import annotations

from collections import Counter
from pathlib import Path

from qa_common import DATA, load_json, write_json


TODAY = "2026-08-14"
RELEASED_WAVE1 = {
    "MA-Q-0092", "MA-Q-0095", "MA-Q-0096", "MA-Q-0115", "MA-Q-0118",
    "MA-Q-0119", "MA-Q-0120", "MA-Q-0122", "MA-Q-0123", "MA-Q-0124",
    "MA-Q-0130",
}
FAILED_REALISM_IDS = [
    "MA-Q-0091", "MA-Q-0093", "MA-Q-0094", "MA-Q-0099", "MA-Q-0100",
    "MA-Q-0101", "MA-Q-0102", "MA-Q-0103", "MA-Q-0104", "MA-Q-0105",
    "MA-Q-0106", "MA-Q-0107", "MA-Q-0108", "MA-Q-0109", "MA-Q-0110",
    "MA-Q-0111", "MA-Q-0112", "MA-Q-0113", "MA-Q-0114", "MA-Q-0116",
    "MA-Q-0117", "MA-Q-0121", "MA-Q-0125", "MA-Q-0126", "MA-Q-0127",
    "MA-Q-0128", "MA-Q-0129",
]


def rule_record(
    rule_id: str,
    title: str,
    jurisdiction: str,
    area: int,
    topic: str,
    subtopic: str,
    summary: str,
    relevance: str,
    authority: list[dict],
    *,
    numeric_facts: list[dict] | None = None,
    exceptions: list[str] | None = None,
    confusions: list[str] | None = None,
    related: list[str] | None = None,
) -> dict:
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "0" * 64,
        "title": title,
        "jurisdiction": jurisdiction,
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": relevance,
        "authority": authority,
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": TODAY,
        "numeric_facts": numeric_facts or [],
        "exceptions": exceptions or [],
        "common_confusions": confusions or [],
        "related_rule_ids": related or [],
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": "Current official primary or official agency source checked on 2026-08-14.",
    }


def choice_rows(rows: list[tuple[str, str, str]]) -> tuple[list[dict], dict]:
    return ([{"id": cid, "text": text} for cid, text, _ in rows], {cid: why for cid, _, why in rows})


def question_record(
    qid: str,
    family_id: str,
    area: int,
    topic: str,
    subtopic: str,
    difficulty: int,
    qtype: str,
    stem: str,
    rows: list[tuple[str, str, str]],
    correct: list[str],
    core: str,
    facts: list[str],
    trap: str,
    rule_ids: list[str],
    drug_ids: list[str],
    reasoning_steps: list[str],
) -> dict:
    choices, analyses = choice_rows(rows)
    return {
        "question_id": qid,
        "family_id": family_id,
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "question_type": qtype,
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": stem,
        "choices": choices,
        "correct_choice_ids": correct,
        "explanation": {
            "core_reasoning": core,
            "choice_analysis": analyses,
            "related_facts": facts,
            "mpje_trap": trap,
        },
        "rule_ids": rule_ids,
        "drug_ids": drug_ids,
        "reasoning_steps": reasoning_steps,
        "verification_status": "AUDIT_PENDING",
        "lifecycle_status": "AUDIT_PENDING",
        "last_legal_review": TODAY,
        "audits": [],
        "duplicate_review_status": "PENDING",
        "independent_audit_status": "PENDING",
        "final_adjudication": None,
        "development_fixture": True,
    }


def family_record(q: dict, primary: list[str], secondary: list[str], trap: str) -> dict:
    return {
        "family_id": q["family_id"],
        "area": q["area"],
        "topic": q["topic"],
        "subtopic": q["subtopic"],
        "primary_rule_ids": primary,
        "secondary_rule_ids": secondary,
        "drug_required": bool(q["drug_ids"]),
        "scenario_types": ["practice decision"],
        "common_traps": [trap],
        "target_difficulties": [q["difficulty"]],
        "target_item_types": [q["question_type"]],
        "max_questions_in_final_bank": 1,
        "current_candidate_count": 1,
        "current_released_count": 0,
    }


def install_new_rules() -> None:
    rules = {
        "FED-CII-EMERGENCY-MISSING-FOLLOWUP": rule_record(
            "FED-CII-EMERGENCY-MISSING-FOLLOWUP",
            "Pharmacy action when emergency Schedule II follow-up is missing",
            "FEDERAL", 3, "Controlled prescriptions", "Emergency follow-up failure",
            "After an emergency oral Schedule II dispensing, if the prescribing practitioner fails to deliver the required follow-up prescription within seven days, the pharmacist must notify the DEA as required by 21 CFR 1306.11(d).",
            "Tests the pharmacist's post-dispensing duty after the emergency supply has already been provided, rather than merely recalling the seven-day prescriber deadline.",
            [{"type": "FEDERAL_REGULATION", "name": "21 CFR 1306.11", "section": "1306.11(d)(4)", "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"}],
            numeric_facts=[{"fact": "Emergency Schedule II follow-up deadline", "value": 7, "unit": "days", "conditions": "After oral emergency authorization"}],
            exceptions=["This rule applies after a lawful emergency oral Schedule II dispensing; it is not a general rule for routine Schedule II prescriptions."],
            confusions=["Treating the prescriber's missed deadline as a recordkeeping issue only and overlooking the pharmacist's DEA-notification duty."],
            related=["FED-CII-EMERGENCY-ORAL", "FED-CII-EMERGENCY-FOLLOWUP"],
        ),
        "FED-CSOS-CREDENTIAL": rule_record(
            "FED-CSOS-CREDENTIAL",
            "CSOS certificate is personal to the subscriber",
            "FEDERAL", 3, "Controlled substance procurement", "CSOS subscriber credential",
            "A DEA CSOS certificate is issued to an individual subscriber and may be used to digitally sign controlled-substance orders only by that individual; another employee may not borrow or share the subscriber's certificate.",
            "Tests whether electronic ordering authority follows the named individual subscriber rather than the pharmacy workstation or job title.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA CSOS Q&A", "section": "About and usage of CSOS certificates", "url": "https://www.deadiversion.usdoj.gov/drugreg/csos/csos-faq.html"}],
            exceptions=["A separate properly authorized subscriber or person with valid power of attorney may use that person's own DEA-issued certificate."],
            confusions=["Assuming a certificate installed on a shared pharmacy computer can be used by any pharmacist or manager."],
            related=["FED-CSOS"],
        ),
        "FED-MIFEPRISTONE-REMS": rule_record(
            "FED-MIFEPRISTONE-REMS",
            "Mifepristone REMS pharmacy and prescriber certification",
            "FEDERAL", 3, "Federal drug requirements", "Mifepristone REMS",
            "Under the current Mifepristone REMS Program, mifepristone for medical termination of pregnancy must be prescribed by a certified prescriber and dispensed by or under a certified prescriber or by a certified pharmacy; retail pharmacies may dispense when certified and compliant with the REMS.",
            "Tests a product-specific restricted-distribution decision instead of treating REMS as a generic warning label.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "FDA Questions and Answers on Mifepristone", "section": "Pharmacy certification and current REMS", "url": "https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/questions-and-answers-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation"}],
            exceptions=["This rule concerns mifepristone used under the referenced REMS indication; other mifepristone uses or products require their own current analysis."],
            confusions=["Assuming retail dispensing is prohibited merely because the drug is subject to a REMS."],
            related=["FED-REMS"],
        ),
        "FED-PSE-LOG-ID": rule_record(
            "FED-PSE-LOG-ID",
            "Pseudoephedrine purchaser identification and logbook",
            "FEDERAL", 3, "Restricted nonprescription products", "Pseudoephedrine ID and logbook",
            "For ordinary retail sales of scheduled listed chemical products, federal CMEA requirements generally require acceptable purchaser identification and a sales logbook; the individual-purchase logbook and ID requirement does not apply to a single sales package containing no more than 60 mg of pseudoephedrine.",
            "Tests the access-control and documentation gate separately from gram-based purchase limits.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA CMEA General Information", "section": "Logbook provisions and identification", "url": "https://www.deadiversion.usdoj.gov/meth/cma2005.html"}],
            numeric_facts=[{"fact": "Single-package logbook/ID exception", "value": 60, "unit": "mg pseudoephedrine", "conditions": "One sales package"}],
            exceptions=["A single sales package containing no more than 60 mg of pseudoephedrine is excepted from the individual logbook/ID transaction requirement described by DEA."],
            confusions=["Passing the daily gram limit does not by itself satisfy the separate purchaser-identification and logbook rules."],
            related=["FED-PSE-QUANTITY"],
        ),
        "FED-PSE-SELF-CERT": rule_record(
            "FED-PSE-SELF-CERT",
            "Pseudoephedrine seller self-certification and employee training",
            "FEDERAL", 3, "Restricted nonprescription products", "CMEA seller compliance",
            "A regulated retail seller of scheduled listed chemical products must satisfy the CMEA self-certification and employee-training requirements before making covered retail sales; DEA's current self-certification system treats separate physical retail locations as separately certified locations.",
            "Tests store-level operational compliance before a sale rather than calculating a patient's purchase quantity.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA CMEA Self-Certification", "section": "Retail seller certification and training", "url": "https://www.deadiversion.usdoj.gov/meth/self_cert.html"}, {"type": "OFFICIAL_GUIDANCE", "name": "DEA CMEA self-certification application", "section": "Physical-location certification", "url": "https://apps.deadiversion.usdoj.gov/CMEA/"}],
            exceptions=["DEA pharmacy registrants may be treated differently for the self-certification fee, but the CMEA training and compliance duties still control covered sales."],
            confusions=["Assuming a chain's certification at one store automatically authorizes all other physical locations."],
            related=["FED-PSE-QUANTITY", "FED-PSE-LOG-ID"],
        ),
        "FED-CLOZAPINE-REMS-REMOVED": rule_record(
            "FED-CLOZAPINE-REMS-REMOVED",
            "Clozapine REMS removed",
            "FEDERAL", 3, "Federal drug requirements", "Clozapine REMS status",
            "FDA removed the Clozapine REMS effective June 13, 2025. Pharmacies no longer need REMS enrollment or REMS verification of patient eligibility or ANC results as a condition of dispensing, although labeling-based clinical monitoring recommendations remain relevant to patient care.",
            "Tests whether the candidate distinguishes a discontinued REMS dispensing gate from continuing clinical monitoring recommendations.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "FDA removes Clozapine REMS", "section": "Pharmacy requirements after REMS removal", "url": "https://www.fda.gov/drugs/drug-safety-and-availability/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine"}],
            exceptions=["A prescriber or pharmacist may still need to address clinically significant ANC information under ordinary standards of care and labeling."],
            confusions=["Continuing to impose the former REMS enrollment and ANC-verification gate after FDA removed it."],
            related=["FED-REMS"],
        ),
        "MA-CS-LABEL": rule_record(
            "MA-CS-LABEL",
            "Massachusetts controlled-substance dispensing label",
            "MA", 3, "Dispensing", "Controlled-substance label",
            "When a pharmacist fills a controlled-substance prescription, Massachusetts law requires the dispensing container label to include the statutory information such as fill date, pharmacy name and address, pharmacist initials, prescription serial number, patient name when applicable, prescriber, drug, directions and required cautionary statements, plus tablet or capsule count when applicable.",
            "Tests the pharmacist's final product-label decision rather than prescription-face validity.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 21", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"}],
            exceptions=["Veterinary prescriptions and any specific statutory labeling exception must be applied according to their own terms."],
            confusions=["Confusing information required on the prescription itself with information required on the dispensed container label."],
            related=["MA-RX-REQUIRED-ELEMENTS"],
        ),
        "MA-CS-II-III-PAMPHLET": rule_record(
            "MA-CS-II-III-PAMPHLET",
            "Massachusetts Schedule II and III consumer education pamphlet",
            "MA", 3, "Dispensing", "Schedule II and III education",
            "Massachusetts requires the designated consumer educational pamphlet when a pharmacy dispenses a narcotic or controlled substance in Schedule II or III, subject to statutory exceptions including outpatient palliative care, long-term-care residents, and treatment of substance use disorder or opioid dependence.",
            "Tests whether a pharmacist applies the education requirement and its statutory indication/setting exceptions to the actual dispensing encounter.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 21", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"}],
            exceptions=["Outpatient palliative care; resident of a long-term care facility; drug prescribed for substance use disorder or opioid-dependence treatment."],
            confusions=["Assuming every Schedule II or III dispensing requires the pamphlet without checking the statutory exception."],
            related=["MA-CII-LESSER-QUANTITY"],
        ),
        "MA-PRESCRIPTION-LOCKBOX": rule_record(
            "MA-PRESCRIPTION-LOCKBOX",
            "Prescription lock boxes at Massachusetts pharmacies",
            "MA", 1, "Pharmacy operations", "Prescription lock boxes",
            "A Massachusetts pharmacy registered to dispense Schedule II, III, IV or V prescription drugs must make prescription lock boxes available for sale at each store location and display the statutorily described notice on or near the pharmacy counter.",
            "Tests a Massachusetts pharmacy-operation requirement that is separate from controlled-substance storage inside the pharmacy.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 21B", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21B"}],
            exceptions=["The statutory definition excludes certain institutional settings as provided in §21B."],
            confusions=["Treating patient lock-box availability as optional counseling rather than a store-level statutory requirement."],
        ),
        "MA-POS-LESSER-PRICE": rule_record(
            "MA-POS-LESSER-PRICE",
            "Massachusetts prescription point-of-sale lesser-price rule",
            "MA", 1, "Pharmacy operations", "Prescription point-of-sale charge",
            "At the point of sale for a prescription drug, a Massachusetts pharmacy must charge the individual the lesser of the applicable health-plan cost-sharing amount or the pharmacy retail price.",
            "Tests the final amount the pharmacy may collect when the insurance cost share exceeds the pharmacy's cash retail price.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 21C", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21C"}],
            confusions=["Assuming an adjudicated insurance copay must always be collected even when the pharmacy retail price is lower."],
        ),
        "MA-HYPODERMIC-SALE": rule_record(
            "MA-HYPODERMIC-SALE",
            "Massachusetts authorized sellers of hypodermic syringes and needles",
            "MA", 2, "Controlled substance law", "Hypodermic syringe and needle sales",
            "Massachusetts law permits hypodermic syringes or needles for administration of controlled substances by injection to be sold only by the categories of sellers listed in M.G.L. c. 94C §27, including a pharmacist and specified licensed or surgical/embalming supply sellers.",
            "Tests who is legally authorized to conduct the sale rather than treating syringes as unrestricted front-store merchandise.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 27", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section27"}],
            confusions=["Assuming any retail employee may independently make the sale merely because the store contains a pharmacy."],
        ),
        "MA-ORAL-CONTROLLED-DOCUMENTATION": rule_record(
            "MA-ORAL-CONTROLLED-DOCUMENTATION",
            "Massachusetts documentation of oral controlled-substance prescriptions",
            "MA", 3, "Prescription format", "Oral controlled prescriptions",
            "On receiving an oral prescription for a controlled substance, the pharmacist must immediately reduce it to writing with the information required by M.G.L. c. 94C §20 and make a reasonable effort to authenticate an unfamiliar prescriber; the subsection requiring later electronic or written documentation expressly does not apply to Schedule VI.",
            "Tests the pharmacist's immediate documentation and authentication duties while distinguishing the Schedule VI follow-up exception.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 20(a)-(c)", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section20"}],
            exceptions=["The follow-up prescription requirement in §20(c) does not apply to Schedule VI, but immediate reduction to writing and validity duties still apply."],
            confusions=["Mistaking the Schedule VI follow-up exception for permission to skip the pharmacist's contemporaneous oral-prescription record."],
        ),
        "MA-COMPOUND-LABEL-CONTACT": rule_record(
            "MA-COMPOUND-LABEL-CONTACT",
            "Massachusetts compounded-drug labeling and pharmacist contact",
            "MA", 3, "Compounding", "Compounded product labeling",
            "Massachusetts requires pharmacy-compounded preparations to bear a label identifying the product as sterile or non-sterile compounded preparation; covered sterile or complex non-sterile compounding pharmacies also place the required pharmacist-contact telephone number on the container, subject to the institutional inpatient exception.",
            "Tests the dispensed compounded product's labeling and communication requirements rather than compounding CE or technique.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 21", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"}],
            exceptions=["The telephone-number paragraph does not apply to the specified institutional-pharmacy inpatient scenario described in §21."],
            confusions=["Assuming ordinary prescription-label elements alone satisfy the additional compounded-preparation labeling duties."],
        ),
        "MA-EXCEPTED-CS-SALE": rule_record(
            "MA-EXCEPTED-CS-SALE",
            "Massachusetts retail sale of excepted controlled-substance preparations",
            "MA", 3, "Controlled substance dispensing", "Excepted preparations",
            "For a controlled-substance preparation that qualifies for the Massachusetts §4 exception, retail sale under §5 requires good-faith medicinal sale, purchaser identification satisfactory to the pharmacist, no more than four ounces to a person during a 48-hour period, and an accurate purchaser/product record.",
            "Tests the special nonprescription-style pathway for an already-qualified excepted preparation without confusing it with ordinary prescription refills.",
            [{"type": "STATUTE", "name": "Massachusetts General Laws c. 94C", "section": "§ 5", "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section5"}],
            numeric_facts=[{"fact": "Maximum amount of excepted preparation", "value": 4, "unit": "ounces", "conditions": "Per person in a 48-hour period"}, {"fact": "Sale window", "value": 48, "unit": "hours", "conditions": "For the four-ounce retail limit"}],
            confusions=["Treating an excepted preparation as an unrestricted OTC product with no identification or record requirement."],
        ),
        "FED-FORM222-POA": rule_record(
            "FED-FORM222-POA",
            "Power of attorney to execute DEA Form 222",
            "FEDERAL", 3, "Controlled substance procurement", "Form 222 signing authority",
            "A DEA registrant may authorize one or more individuals to obtain and execute DEA Forms 222 by granting a compliant power of attorney; the power of attorney is retained and made available for inspection rather than submitted to DEA as each order is placed.",
            "Tests who may sign an executed paper Schedule I/II order and how that authority is documented.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA Form 222 Q&A", "section": "Who can sign executed DEA 222 Order Forms", "url": "https://www.deadiversion.usdoj.gov/faq/form-222-faq.html"}],
            confusions=["Assuming only the person who signed the DEA registration may ever execute a Form 222."],
            related=["FED-FORM222-ORDER"],
        ),
        "FED-CSOS-SUPPLIER-VALIDATION": rule_record(
            "FED-CSOS-SUPPLIER-VALIDATION",
            "Supplier validation of CSOS electronic orders",
            "FEDERAL", 3, "Controlled substance procurement", "CSOS supplier validation",
            "A supplier receiving a CSOS electronic controlled-substance order must validate the DEA-issued digital certificate and the electronic order; an order signed with an expired, revoked, or otherwise invalid certificate may not be treated as a valid electronic Schedule I/II order.",
            "Tests the supplier-side validity gate after an electronic order is received rather than who is allowed to possess a certificate.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA CSOS Program Overview", "section": "Accepting a signed order", "url": "https://www.deadiversion.usdoj.gov/drugreg/csos/overview.html"}, {"type": "FEDERAL_REGULATION", "name": "21 CFR Part 1305", "section": "§ 1305.25", "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.25"}],
            confusions=["Assuming an electronically transmitted purchase order is valid merely because it arrived through the wholesaler's CSOS-capable portal."],
            related=["FED-CSOS"],
        ),
        "FED-FORM222-CANCEL": rule_record(
            "FED-FORM222-CANCEL",
            "Cancellation of submitted DEA Form 222 orders",
            "FEDERAL", 3, "Controlled substance procurement", "Form 222 cancellation",
            "A purchaser may cancel part or all of a submitted paper DEA Form 222 order by notifying the supplier in writing; the supplier documents the cancellation on the original form as required by 21 CFR 1305.19.",
            "Tests the lawful way to stop a pending paper Schedule I/II order after the form has already been sent to the supplier.",
            [{"type": "OFFICIAL_GUIDANCE", "name": "DEA Form 222 Q&A", "section": "Cancellation of submitted DEA Form 222", "url": "https://www.deadiversion.usdoj.gov/faq/form-222-faq.html"}, {"type": "FEDERAL_REGULATION", "name": "21 CFR 1305.19", "section": "1305.19(a)", "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.19"}],
            confusions=["Trying to erase or alter the executed paper form instead of sending the supplier a written cancellation."],
            related=["FED-FORM222-ORDER"],
        ),
    }
    for rid, record in rules.items():
        write_json(DATA / "rules" / f"{rid.lower()}.json", record)


def repair_existing_rules() -> None:
    # Naloxone: distinguish OTC and prescription products.
    p = DATA / "rules" / "ma-naloxone.json"
    r = load_json(p)
    r["content_version"] = max(2, int(r.get("content_version", 1)) + 1)
    r["rule_summary"] = (
        "Massachusetts naloxone access includes patient-specific and statewide standing-order prescription pathways, "
        "including dispensing to a person at risk or another person positioned to assist. OTC naloxone and prescription "
        "naloxone are separate products: DCP controlled-substance regulations apply to prescription naloxone but do not "
        "apply to FDA-labeled OTC naloxone merely because the active ingredient is naloxone."
    )
    if not any(a.get("url") == "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone" for a in r["authority"]):
        r["authority"].append({"type": "OFFICIAL_GUIDANCE", "name": "Massachusetts DCP OTC naloxone advisory", "section": "OTC and prescription naloxone distinction", "url": "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone"})
    r["exceptions"] = [
        "FDA-labeled OTC naloxone is a separate nonprescription product and is not subject to DCP controlled-substance regulation merely because it contains naloxone.",
        "Prescription naloxone remains available through patient-specific prescriptions and authorized standing-order pathways."
    ]
    r["common_confusions"] = ["Treating OTC naloxone and prescription naloxone as one legal product category."]
    r["last_verified"] = TODAY
    r["verification_notes"] = "Current Massachusetts DCP advisory and statutory/Board sources checked on 2026-08-14; record now distinguishes OTC from prescription naloxone."
    write_json(p, r)

    # Initial inventory: add zero-stock commencement rule.
    p = DATA / "rules" / "fed-inventory-initial.json"
    r = load_json(p)
    r["content_version"] = max(2, int(r.get("content_version", 1)) + 1)
    r["rule_summary"] = (
        "A registrant takes an initial controlled-substance inventory on the date it first engages in controlled-substance activity; "
        "if the registrant commences business with no controlled substances on hand, it must record that zero-stock fact as the initial inventory."
    )
    r["exceptions"] = ["Starting business with zero controlled substances does not eliminate the initial-inventory record; the registrant records that none are on hand."]
    r["common_confusions"] = ["Waiting until the first shipment arrives when business already commenced with zero controlled substances on hand."]
    r["last_verified"] = TODAY
    r["verification_notes"] = "21 CFR 1304.11(b), including the zero-stock commencement clause, checked on 2026-08-14."
    write_json(p, r)

    # Biennial inventory: add statutory authority and clarify no delay beyond two years.
    p = DATA / "rules" / "fed-inventory-biennial.json"
    r = load_json(p)
    r["content_version"] = max(2, int(r.get("content_version", 1)) + 1)
    r["rule_summary"] = (
        "After the initial inventory, a registrant must take a new controlled-substance inventory at least every two years. "
        "Current DEA regulation permits any date within two years of the previous biennial inventory; the related statutory general-physical-inventory language does not authorize delaying the DEA inventory beyond that regulatory two-year window."
    )
    if not any(a.get("url") == "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section827" for a in r["authority"]):
        r["authority"].append({"type": "FEDERAL_STATUTE", "name": "21 U.S.C. 827", "section": "§ 827(a)(1)", "url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section827"})
    r["exceptions"] = ["The statutory coordination with a regular general physical inventory does not extend the DEA regulatory deadline past two years from the previous biennial inventory."]
    r["common_confusions"] = ["Reading the statutory general-inventory coordination language as permission to delay the DEA inventory beyond the two-year regulatory limit."]
    r["last_verified"] = TODAY
    r["verification_notes"] = "21 CFR 1304.11(c) and current 21 U.S.C. 827(a)(1) checked together on 2026-08-14."
    write_json(p, r)

    # Form 222 loss: preserve the operational replacement details surfaced by the fresh audit program.
    p = DATA / "rules" / "fed-form222-loss.json"
    r = load_json(p)
    r["content_version"] = max(2, int(r.get("content_version", 1)) + 1)
    r["rule_summary"] = (
        "If a DEA Form 222 is lost or stolen, the registrant executes a replacement form and attaches the required statement identifying the lost/stolen form and confirming the goods were not received; copies are retained as required. Loss or theft of used or unused order forms is reported immediately to the local DEA Diversion Field Office with the serial numbers."
    )
    r["last_verified"] = TODAY
    r["verification_notes"] = "DEA Form 222 Q&A and 21 CFR 1305.16 checked on 2026-08-14; replacement-statement details added."
    write_json(p, r)


def repair_drugs() -> None:
    # Existing naloxone record now means prescription naloxone product/category.
    p = DATA / "drugs" / "naloxone.json"
    d = load_json(p)
    d["content_version"] = max(2, int(d.get("content_version", 1)) + 1)
    d["generic_name"] = "naloxone (prescription product)"
    d["brand_names"] = ["Prescription naloxone products"]
    d["massachusetts_status"] = {"schedule": "VI", "masspat_reportable": False, "drug_of_concern": False}
    d["legal_consequences"] = {
        "refill": {"summary": "Prescription-labeled naloxone remains a Massachusetts Schedule VI prescription product; apply the applicable prescription or standing-order pathway rather than the OTC framework.", "rule_ids": ["MA-NALOXONE", "MA-SCHEDULE-VI"]},
        "transfer": {"summary": "A patient-specific prescription naloxone order follows the current Schedule VI transfer framework; a statewide standing order is a separate authority and should not be treated as an OTC sale.", "rule_ids": ["MA-NALOXONE", "MA-RX-TRANSFER", "MA-SCHEDULE-VI"]},
        "partial_fill": {"summary": "Apply the prescription product's Schedule VI pathway and the terms of the underlying prescription or standing order.", "rule_ids": ["MA-NALOXONE", "MA-SCHEDULE-VI"]},
        "masspat": {"summary": "Prescription naloxone is not routinely a Schedule II-V MassPAT transaction solely because it is Massachusetts Schedule VI.", "rule_ids": ["MA-NALOXONE", "MA-PMP-REPORTING", "MA-SCHEDULE-VI"]},
        "quantity_limit": {"summary": "Apply the naloxone prescription or standing-order terms; do not import Schedule II-V quantity rules merely because the prescription product is Massachusetts Schedule VI.", "rule_ids": ["MA-NALOXONE", "MA-SCHEDULE-VI"]},
    }
    if not any(a.get("url") == "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone" for a in d["authorities"]):
        d["authorities"].append({"type": "OFFICIAL_GUIDANCE", "name": "Massachusetts DCP OTC naloxone advisory", "section": "Prescription naloxone remains DCP-regulated", "url": "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone"})
    d["last_verified"] = TODAY
    d["verification_notes"] = "This record intentionally represents prescription-labeled naloxone. Massachusetts DCP distinguishes it from FDA-labeled OTC naloxone; status rechecked 2026-08-14."
    write_json(p, d)

    otc = {
        "drug_id": "naloxone-otc",
        "content_version": 1,
        "content_hash": "0" * 64,
        "generic_name": "naloxone (OTC product)",
        "brand_names": ["Narcan OTC", "RiVive"],
        "main_indications": ["Emergency treatment of known or suspected opioid overdose using an FDA-labeled OTC naloxone product"],
        "therapeutic_class": "Opioid antagonist",
        "federal_status": {"controlled": False, "schedule": "NONCONTROLLED"},
        "massachusetts_status": {"schedule": "NONCONTROLLED", "masspat_reportable": False, "drug_of_concern": False},
        "legal_consequences": {
            "refill": {"summary": "An FDA-labeled OTC naloxone package is sold as a nonprescription product; prescription-refill rules do not create a refill requirement for the OTC package.", "rule_ids": ["MA-NALOXONE"]},
            "transfer": {"summary": "An OTC naloxone package is not transferred as a prescription merely because prescription naloxone products also exist.", "rule_ids": ["MA-NALOXONE"]},
            "partial_fill": {"summary": "Prescription partial-fill rules do not govern an ordinary sale of an intact FDA-labeled OTC naloxone package.", "rule_ids": ["MA-NALOXONE"]},
            "masspat": {"summary": "Ordinary OTC naloxone sales are not MassPAT dispensing transactions.", "rule_ids": ["MA-NALOXONE", "MA-PMP-REPORTING"]},
            "quantity_limit": {"summary": "The OTC package follows its retail labeling and applicable general retail law, not Massachusetts Schedule VI prescription quantity rules.", "rule_ids": ["MA-NALOXONE"]},
        },
        "verified_rule_dependencies": {},
        "authorities": [
            {"type": "OFFICIAL_GUIDANCE", "name": "Massachusetts DCP OTC naloxone advisory", "section": "OTC naloxone outside DCP controlled-substance regulations", "url": "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone"},
            {"type": "OFFICIAL_GUIDANCE", "name": "Massachusetts OTC naloxone memorandum", "section": "OTC access and products", "url": "https://www.mass.gov/memorandum/over-the-counter-otc-naloxone"},
        ],
        "last_verified": TODAY,
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": "FDA-labeled OTC naloxone is a separate product category from prescription naloxone under current Massachusetts DCP guidance; checked 2026-08-14.",
    }
    write_json(DATA / "drugs" / "naloxone-otc.json", otc)

    # Mifepristone: bind the drug to its product-specific REMS rule.
    p = DATA / "drugs" / "mifepristone.json"
    d = load_json(p)
    d["content_version"] = max(2, int(d.get("content_version", 1)) + 1)
    d["legal_consequences"]["transfer"] = {"summary": "Any dispensing pathway must preserve the current Mifepristone REMS certified-pharmacy and certified-prescriber requirements; ordinary Schedule VI transfer mechanics do not override the REMS.", "rule_ids": ["FED-MIFEPRISTONE-REMS", "MA-RX-TRANSFER", "MA-SCHEDULE-VI"]}
    d["legal_consequences"]["partial_fill"] = {"summary": "Product-specific Mifepristone REMS dispensing requirements continue to control even though the drug is not federally scheduled.", "rule_ids": ["FED-MIFEPRISTONE-REMS", "MA-SCHEDULE-VI"]}
    d["last_verified"] = TODAY
    d["verification_notes"] = "Identity, Schedule VI status, and the current FDA Mifepristone REMS pharmacy/prescriber certification pathway checked on 2026-08-14."
    write_json(p, d)

    # Pseudoephedrine: extend the canonical retail controls beyond gram limits.
    p = DATA / "drugs" / "pseudoephedrine.json"
    d = load_json(p)
    d["content_version"] = max(2, int(d.get("content_version", 1)) + 1)
    d["legal_consequences"]["quantity_limit"] = {"summary": "Covered retail sales require both the federal gram limits and the separate applicable purchaser-ID/logbook and seller self-certification/training controls.", "rule_ids": ["FED-PSE-QUANTITY", "FED-PSE-LOG-ID", "FED-PSE-SELF-CERT"]}
    d["last_verified"] = TODAY
    d["verification_notes"] = "DailyMed identity and current DEA CMEA quantity, ID/logbook, and seller self-certification/training requirements checked on 2026-08-14."
    write_json(p, d)

    # New clozapine record to support the current no-REMS decision.
    clozapine = {
        "drug_id": "clozapine",
        "content_version": 1,
        "content_hash": "0" * 64,
        "generic_name": "clozapine",
        "brand_names": ["Clozaril", "Versacloz"],
        "main_indications": ["Treatment-resistant schizophrenia and reduction of recurrent suicidal behavior in schizophrenia or schizoaffective disorder"],
        "therapeutic_class": "Atypical antipsychotic",
        "federal_status": {"controlled": False, "schedule": "NONCONTROLLED"},
        "massachusetts_status": {"schedule": "VI", "masspat_reportable": False, "drug_of_concern": False},
        "legal_consequences": {
            "refill": {"summary": "Clozapine is not subject to the former federal REMS dispensing gate; ordinary prescription validity and Massachusetts Schedule VI requirements still apply.", "rule_ids": ["FED-CLOZAPINE-REMS-REMOVED", "MA-SCHEDULE-VI"]},
            "transfer": {"summary": "The former Clozapine REMS does not itself bar a lawful prescription transfer; apply the current Massachusetts Schedule VI transfer rule and ordinary clinical review.", "rule_ids": ["FED-CLOZAPINE-REMS-REMOVED", "MA-RX-TRANSFER", "MA-SCHEDULE-VI"]},
            "partial_fill": {"summary": "The former REMS eligibility check is no longer a federal prerequisite to dispensing; apply ordinary prescription and patient-care requirements.", "rule_ids": ["FED-CLOZAPINE-REMS-REMOVED", "MA-SCHEDULE-VI"]},
            "masspat": {"summary": "Clozapine is not routinely MassPAT-reportable solely because Massachusetts classifies prescription-only non-I-V drugs in Schedule VI.", "rule_ids": ["MA-PMP-REPORTING", "MA-SCHEDULE-VI"]},
            "quantity_limit": {"summary": "No former REMS quantity gate should be invented; apply the prescription, labeling, and Massachusetts Schedule VI framework.", "rule_ids": ["FED-CLOZAPINE-REMS-REMOVED", "MA-SCHEDULE-VI"]},
        },
        "verified_rule_dependencies": {},
        "authorities": [
            {"type": "FDA_LABEL", "name": "DailyMed clozapine label search", "section": "Indications and Usage; Warnings", "url": "https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=clozapine"},
            {"type": "OFFICIAL_GUIDANCE", "name": "FDA removes Clozapine REMS", "section": "Effective June 13, 2025", "url": "https://www.fda.gov/drugs/drug-safety-and-availability/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine"},
            {"type": "STATE_REGULATION", "name": "Massachusetts controlled-substance schedules", "section": "105 CMR 700.002", "url": "https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download"},
        ],
        "last_verified": TODAY,
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": "FDA labeling, FDA's current removal of the Clozapine REMS, and Massachusetts Schedule VI framework checked on 2026-08-14.",
    }
    write_json(DATA / "drugs" / "clozapine.json", clozapine)


def build_replacements() -> dict[str, dict]:
    q: dict[str, dict] = {}
    q["MA-Q-0091"] = question_record(
        "MA-Q-0091", "V3_0091_RECALL_LOT_ACTION", 3, "Product safety", "Recall response", 4, "SBA",
        "A wholesaler sends a Class II recall notice identifying one lot of a blood-pressure medication. The pharmacy has bottles from the affected lot and from an unaffected lot, and several patients previously received the affected lot. What is the best immediate pharmacy response?",
        [
            ("A", "Stop dispensing every strength and lot of the drug until the manufacturer ends the recall.", "The recall is lot-specific; unaffected stock is not automatically removed from use unless the notice directs that broader action."),
            ("B", "Segregate the affected lot, preserve lot traceability, and follow the recall notice for inventory and patient follow-up.", "This matches the lot-specific recall response: remove affected stock from availability, preserve traceability, and follow the notice's instructions."),
            ("C", "Continue dispensing the affected lot until each patient confirms whether the medication caused symptoms.", "A recalled lot should not remain available for dispensing while the pharmacy waits for symptom reports."),
            ("D", "Tell every patient taking the drug to stop therapy immediately, regardless of the recalled lot or notice.", "A recall does not automatically mean every patient using every lot should stop therapy; the pharmacy follows the recall's risk and patient instructions."),
            ("E", "Return only unopened affected bottles and leave opened affected bottles available for completion of existing prescriptions.", "Affected stock is segregated from dispensing based on the recall, not kept available because a bottle has already been opened."),
        ], ["B"],
        "The legal and operational decision is lot-specific. The pharmacy removes the identified lot from availability, preserves traceability, and follows the recall notice rather than expanding or narrowing the recall on its own.",
        ["Recall notices may identify specific lots, strengths, or packages.", "Patient instructions depend on the recall notice and risk, not merely on the word 'recall'."],
        "A recall is not an automatic order to stop every patient's therapy or destroy every lot of the product.",
        ["FED-RECALL"], [], ["Identify the exact recalled lot and affected inventory", "Separate inventory action from patient clinical instructions"])

    q["MA-Q-0093"] = question_record(
        "MA-Q-0093", "V3_0093_STORAGE_EXCURSION_STATUS", 3, "Product safety", "Storage excursion", 4, "SBA",
        "A pharmacy refrigerator is found at 68°F after an overnight equipment failure. Several unopened insulin glargine cartons were stored there, and the pharmacy cannot yet determine how long the temperature was outside the labeled storage range. What should the pharmacist do with those cartons before dispensing?",
        [
            ("A", "Dispense them normally because unopened prescription stock cannot be adulterated until it reaches a patient.", "Pharmacy-owned stock can become unsuitable or adulterated before dispensing when storage conditions compromise quality."),
            ("B", "Relabel each carton with the observed temperature and dispense if the patient accepts the excursion.", "Patient consent does not establish the product's strength, quality, or storage integrity."),
            ("C", "Segregate the cartons from saleable stock and resolve product integrity under the labeling/manufacturer information before dispensing.", "A material unresolved storage excursion calls for segregation and quality assessment before the product is made available."),
            ("D", "Return the cartons to refrigeration for one hour; restoring temperature automatically restores legal saleability.", "Returning stock to the refrigerator does not prove that an excursion caused no quality problem."),
            ("E", "Convert the cartons to patient-return inventory and use the ordinary returned-drug resale rule.", "This is pharmacy-owned stock affected by storage conditions, not medication returned from a patient."),
        ], ["C"],
        "The pharmacy must not dispense stock whose storage excursion leaves strength, purity, or quality unresolved. Segregation and product-specific assessment come before any decision to return the stock to saleable inventory.",
        ["Drug integrity can be affected by storage conditions while stock remains pharmacy-owned.", "A patient-return rule and a pharmacy storage-excursion rule address different facts."],
        "Do not confuse a storage excursion with the separate rule governing medications returned by a patient.",
        ["FED-ADULTERATED-MISBRANDED"], ["insulin-glargine"], ["Identify the excursion as a product-integrity issue", "Prevent dispensing until integrity is resolved"])

    q["MA-Q-0094"] = question_record(
        "MA-Q-0094", "V3_0094_CII_STOCK_SHORTAGE_REMAINDER", 3, "Partial filling", "Pharmacy inability", 4, "SBA",
        "A Massachusetts pharmacy receives a valid oxycodone Schedule II prescription for 30 tablets but has only 12 tablets in stock. The patient wants the full prescribed quantity; the pharmacy dispenses 12 solely because it cannot supply the rest. Four days later the remaining stock arrives. What is the controlling federal consequence?",
        [
            ("A", "The balance may be dispensed within 30 days because every Schedule II partial fill uses the patient-requested 30-day pathway.", "The initial partial fill was caused by pharmacy inability, not the patient's election to receive a lesser quantity."),
            ("B", "The pharmacy may treat the remaining 18 tablets as a refill because the original total quantity was not dispensed.", "Schedule II prescriptions are not refilled; the shortage remainder is governed by the specific partial-fill rule."),
            ("C", "The remaining 18 tablets may be transferred to another pharmacy once the original pharmacy receives stock.", "A shortage remainder is not transformed into a transferable refill."),
            ("D", "The ordinary 72-hour shortage-remainder period has passed, so further quantity generally requires prescriber notification and a new prescription.", "For a partial fill caused by inability to supply the full quantity, the federal shortage pathway generally requires the remainder within 72 hours."),
            ("E", "The original pharmacy may dispense the balance at any time before the Massachusetts 30-day Schedule II validity period ends.", "The general prescription-validity period does not displace the shorter federal shortage-remainder rule."),
        ], ["D"],
        "The reason for the partial fill determines the legal pathway. A pharmacy-stock shortage invokes the federal 72-hour remainder framework, not the patient-requested 30-day framework.",
        ["Patient-requested and pharmacy-inability partial fills have different predicates.", "A Schedule II remainder is not a refill."],
        "Ask why the first partial fill occurred before choosing a deadline.",
        ["FED-CII-PARTIAL-72H", "FED-CII-NO-REFILL"], ["oxycodone"], ["Classify why the first partial fill occurred", "Apply the shortage-specific remainder rule", "Reject the refill analogy"])

    q["MA-Q-0099"] = question_record(
        "MA-Q-0099", "V3_0099_CIII_V_PARTIAL_AGGREGATE", 3, "Partial filling", "Schedule III-V aggregate dispensing", 4, "SATA",
        "A clonazepam Schedule IV prescription is written for 90 tablets. The patient asks to receive 30 tablets today and the rest in later partial dispensings. Which statements describe the federal partial-fill framework? Select all that apply.",
        [
            ("A", "Each partial dispensing is recorded in the same manner as a refill.", "Federal law directs the pharmacy to record each Schedule III-V partial filling in the same manner as a refilling."),
            ("B", "The first 30-tablet partial dispensing automatically cancels all authority to dispense the remaining quantity.", "Schedule III-V prescriptions may be partially filled when the regulatory conditions are met."),
            ("C", "The total quantity dispensed through all partial fills may not exceed the quantity prescribed.", "The aggregate of all partial dispensings is capped by the original prescribed quantity."),
            ("D", "The partial-dispensing sequence must remain within the applicable six-month federal prescription period.", "Federal Schedule III-V partial filling may not continue beyond six months after issue."),
            ("E", "The patient may extend the partial-dispensing period indefinitely by requesting smaller quantities each month.", "Patient requests do not extend the federal time limit."),
        ], ["A", "C", "D"],
        "Schedule III-V partial filling is permitted, but it is bounded by recordkeeping, cumulative-quantity, and timing rules. The patient can choose staged dispensing without creating unlimited additional quantity or time.",
        ["Partial fills are recorded like refills.", "Total partial quantities cannot exceed the prescription and must remain within six months."],
        "Do not equate permission to partial-fill with permission to enlarge the quantity or extend the prescription clock.",
        ["FED-CIII-V-PARTIAL", "FED-CS-REFILL-III-IV"], ["clonazepam"], ["Classify the drug as Schedule IV", "Apply the partial-fill record and quantity conditions", "Apply the six-month outer time limit"])

    q["MA-Q-0100"] = question_record(
        "MA-Q-0100", "V3_0100_PDMA_SAMPLE_INVENTORY", 2, "Federal distribution", "Prescription drug samples", 3, "SBA",
        "A manufacturer representative leaves several sealed prescription-drug sample packs marked 'sample - not for resale' at a community pharmacy after a clinic declines them. The pharmacy manager proposes entering them into normal inventory and dispensing them on paid prescriptions. What is the best legal response?",
        [
            ("A", "Do not place the samples into ordinary saleable pharmacy inventory; samples follow the authorized sample-distribution pathway.", "Prescription drug samples are not ordinary saleable inventory and must remain within the authorized sample-distribution framework."),
            ("B", "The pharmacy may sell the samples after removing the 'not for resale' statement from the outer package.", "Relabeling does not convert a prescription drug sample into lawful saleable inventory."),
            ("C", "The pharmacy may bill only cash patients for the samples because insurance billing is the sole federal restriction.", "The restriction concerns the sample-distribution pathway, not merely the method of payment."),
            ("D", "The pharmacy may dispense the samples if a pharmacist records a zero acquisition cost in the perpetual inventory.", "Inventory accounting does not authorize redistribution of prescription drug samples as normal stock."),
            ("E", "The pharmacy may convert the samples to stock after holding them for 30 days without a manufacturer recall.", "No waiting period changes the sample's legal distribution status into ordinary saleable inventory."),
        ], ["A"],
        "The key fact is that the products are prescription drug samples, not ordinary wholesaler-acquired pharmacy stock. A pharmacy cannot cure that distribution restriction by changing billing, inventory value, or packaging.",
        ["Prescription drug sample controls concern distribution channels.", "A 'not for resale' sample does not become ordinary stock because it is unopened."],
        "The issue is the product's lawful distribution channel, not whether the pharmacy can account for it financially.",
        ["FED-PDMA-SAMPLES"], [], ["Identify the products as prescription drug samples", "Separate sample distribution from ordinary pharmacy acquisition and dispensing"])

    q["MA-Q-0101"] = question_record(
        "MA-Q-0101", "V3_0101_CII_LESSER_QUANTITY_ELECTION", 3, "Partial filling", "Patient lesser-quantity election", 3, "SBA",
        "A patient presents a valid oxycodone Schedule II prescription for 20 tablets and tells the pharmacist, before any dispensing, that she wants only 8 tablets because she is concerned about keeping extra opioid tablets at home. The pharmacy has all 20 tablets in stock. Which action is supported by Massachusetts law?",
        [
            ("A", "Refuse the request because Schedule II prescriptions must be dispensed only in the exact quantity written.", "Massachusetts specifically allows a patient to request a lesser Schedule II quantity."),
            ("B", "Dispense all 20 tablets and advise the patient to discard the unwanted tablets at home.", "The law provides a lesser-quantity option; unnecessary dispensing is not required."),
            ("C", "Change the prescription quantity to 8 only after obtaining a replacement prescription from the prescriber.", "The patient's statutory lesser-quantity election can be honored without converting it into a new prescriber-written quantity."),
            ("D", "Dispense the requested lesser quantity and document the partial dispensing in the patient record.", "This applies the Massachusetts patient lesser-quantity option and its documentation requirement."),
            ("E", "Treat the request as a pharmacy-stock shortage and use the federal 72-hour remainder rule.", "The pharmacy can supply the full quantity; the predicate is the patient's election, not pharmacy inability."),
        ], ["D"],
        "Massachusetts gives the patient an option to receive less than the prescribed Schedule II quantity. The pharmacist should identify the patient's election and document the lesser dispensing rather than forcing the full amount or misclassifying it as a stock shortage.",
        ["The lesser-quantity option is patient driven.", "A pharmacy shortage invokes a different partial-fill pathway."],
        "The quantity is lower because the patient chose less, not because the pharmacy lacked stock.",
        ["MA-CII-LESSER-QUANTITY"], ["oxycodone"], ["Confirm the patient is choosing a lesser quantity", "Document the lesser Schedule II dispensing"])

    q["MA-Q-0102"] = question_record(
        "MA-Q-0102", "V3_0102_CONTROLLED_STOCK_SECURITY", 1, "Controlled substance security", "Physical security", 4, "SBA",
        "During closing procedures, a Massachusetts pharmacy discovers that its controlled-substance storage cabinet no longer locks. The inventory reconciles and no theft or loss is known. A technician suggests leaving the controlled stock there overnight because the alarm system covers the building. What is the best response?",
        [
            ("A", "Leave the stock in place because a theft report is required only after an actual loss is proved.", "The absence of a known loss does not eliminate the pharmacy's independent duty to maintain secure controlled-substance storage and access."),
            ("B", "Move or otherwise secure the controlled stock under compliant restricted-access conditions before closing and address the failed security control.", "The operative problem is a known physical-security failure; the pharmacy should restore secure storage/access before leaving the stock unattended."),
            ("C", "Convert all controlled stock to will-call prescriptions so the cabinet no longer contains pharmacy inventory.", "Changing inventory labels does not cure the underlying physical-security failure."),
            ("D", "Wait until the next biennial inventory to determine whether the broken lock caused a reportable discrepancy.", "Biennial inventory does not substitute for ongoing controlled-substance security."),
            ("E", "File DEA Form 106 immediately even though no theft or significant loss has been discovered.", "A security defect requires correction, but the stated facts do not establish a theft or significant loss for a Form 106 event."),
        ], ["B"],
        "Security and loss reporting are separate decisions. Here the pharmacy has discovered a failed security control but no loss; it should secure the controlled substances and restrict access rather than waiting for a discrepancy or inventing a theft report.",
        ["Controlled-substance security is continuous, not limited to inventory dates.", "A security defect and a confirmed significant loss trigger different duties."],
        "Do not wait for a theft to occur before correcting a known controlled-substance security failure.",
        ["MA-CS-SECURITY"], [], ["Separate a security defect from a theft/loss event", "Restore compliant restricted access before leaving the inventory unattended"])

    q["MA-Q-0103"] = question_record(
        "MA-Q-0103", "V3_0103_LICENSEE_CHANGE_REPORT", 1, "Licensure", "Licensee change reporting", 4, "SBA",
        "A Massachusetts pharmacist legally changes her name and moves to a new home address. She updates payroll and her employer's personnel system the same week but makes no update to her Board licensure record. What additional compliance step is required?",
        [
            ("A", "No Board action is needed because employer records are the controlling professional-license record.", "Employer records do not replace the licensee's separate duty to report specified changes to the Board."),
            ("B", "Wait until the next pharmacist license renewal and report both changes only on the renewal application.", "The change-reporting rule uses a shorter reporting period rather than waiting for renewal."),
            ("C", "Report the specified name and contact-information changes to the Board within the applicable 14-day period.", "This applies the Board's individual-licensee change-reporting rule."),
            ("D", "Report only the legal name change; a residential-address change is never part of Board contact information.", "Specified contact-information changes are part of the reporting framework."),
            ("E", "File a pharmacy facility amendment because an individual pharmacist's home-address change alters the pharmacy license.", "The facts concern the individual licensee's record, not a facility relocation or license amendment."),
        ], ["C"],
        "Professional-license reporting is independent of employer HR records. When a specified personal-status or contact change occurs, the licensee must update the Board within the rule's reporting period.",
        ["The trigger is a change in the licensee's reportable information.", "Employer notification and Board notification serve different records."],
        "Do not substitute an employer's internal update for the licensee's direct Board-reporting duty.",
        ["MA-LICENSEE-CHANGE-14D"], [], ["Identify the changes as individual-licensee information", "Apply the Board's 14-day reporting requirement"])

    q["MA-Q-0104"] = question_record(
        "MA-Q-0104", "V3_0104_CII_MISSING_FOLLOWUP", 3, "Controlled prescriptions", "Emergency follow-up failure", 4, "SBA",
        "A pharmacist lawfully dispensed a three-day emergency oral Schedule II prescription after speaking directly with the prescriber. Eight days later, the pharmacy still has not received the required follow-up prescription despite documented requests to the prescriber. What federal step now becomes important for the pharmacist?",
        [
            ("A", "Convert the emergency dispensing into a Schedule III refill so the existing record can remain open.", "A Schedule II emergency dispensing cannot be converted into a Schedule III refill."),
            ("B", "Delete the emergency prescription record because the prescriber failed to complete the follow-up.", "The dispensing record must be retained; deletion would not resolve the missed follow-up duty."),
            ("C", "Wait until 30 days after the oral authorization because the prescriber still has the full Schedule II validity period.", "The emergency follow-up rule uses its own seven-day deadline."),
            ("D", "Reverse the original dispensing claim and treat the medication as an undocumented sample.", "Billing reversal does not change the legal fact that an emergency Schedule II dispensing occurred."),
            ("E", "Notify DEA of the prescriber's failure to deliver the required emergency follow-up prescription.", "After the seven-day follow-up failure, federal law places a DEA-notification duty on the pharmacist."),
        ], ["E"],
        "This question starts after the emergency dispensing has already occurred. Once the prescriber misses the required follow-up deadline, the pharmacist's issue is no longer whether the emergency was valid but what federal post-dispensing notification duty applies.",
        ["The emergency oral Schedule II pathway has a seven-day follow-up requirement.", "The pharmacist has a separate duty when the prescriber fails to deliver that follow-up."],
        "Memorizing 'seven days' is incomplete; know what the pharmacist must do when day seven passes without the follow-up.",
        ["FED-CII-EMERGENCY-MISSING-FOLLOWUP", "FED-CII-EMERGENCY-FOLLOWUP"], [], ["Confirm the dispensing used the emergency oral Schedule II pathway", "Determine that the seven-day follow-up deadline passed", "Apply the pharmacist's DEA-notification duty"])

    q["MA-Q-0105"] = question_record(
        "MA-Q-0105", "V3_0105_CSOS_PERSONAL_CERTIFICATE", 3, "Controlled substance procurement", "CSOS subscriber credential", 4, "SBA",
        "The pharmacist who normally signs a pharmacy's CSOS Schedule II orders is on vacation. Her DEA-issued CSOS certificate is installed on the ordering workstation, and another pharmacist knows the software password but has not been issued that certificate. May the second pharmacist use the installed certificate to sign today's oxycodone order?",
        [
            ("A", "No. The CSOS certificate may be used to sign orders only by the individual subscriber to whom DEA issued it.", "CSOS signing authority is personal to the named subscriber; access to the workstation or password does not transfer that authority."),
            ("B", "Yes, because any pharmacist working under the same pharmacy DEA registration may use any installed certificate.", "The certificate belongs to the individual subscriber, not to every pharmacist associated with the registrant."),
            ("C", "Yes, if the second pharmacist prints the electronic order after signing and stores it with paper Forms 222.", "Printing a record does not cure unauthorized use of another person's digital certificate."),
            ("D", "Yes, but only when the order contains fewer than twenty Schedule II line items.", "Line-item limits do not authorize certificate sharing."),
            ("E", "No, because CSOS can never be used for Schedule II orders when paper Form 222 is available.", "CSOS is an authorized electronic alternative to paper Form 222; the defect here is who would sign with the certificate."),
        ], ["A"],
        "CSOS uses an individual digital identity. The pharmacy may have multiple authorized subscribers, but one employee cannot simply use another subscriber's DEA-issued certificate because the certificate is installed on a shared machine.",
        ["CSOS certificates are issued to individuals.", "A shared workstation does not make a personal signing certificate a shared credential."],
        "Separate the pharmacy's DEA registration from the individual subscriber's authority to apply the digital signature.",
        ["FED-CSOS-CREDENTIAL", "FED-CSOS"], [], ["Identify whose CSOS certificate would sign the order", "Determine whether that individual is the DEA-issued subscriber"])

    q["MA-Q-0106"] = question_record(
        "MA-Q-0106", "V3_0106_MIFEPRISTONE_REMS_GATE", 3, "Federal drug requirements", "Mifepristone REMS", 5, "SATA",
        "A Massachusetts retail pharmacy receives a prescription for mifepristone 200 mg for medical termination of pregnancy through 10 weeks. The pharmacy is not currently certified in the Mifepristone REMS Program. Which statements are correct? Select all that apply.",
        [
            ("A", "Retail pharmacies are categorically prohibited from dispensing mifepristone, even if they become REMS-certified.", "Current FDA rules allow retail pharmacy dispensing when the pharmacy satisfies the REMS certification requirements."),
            ("B", "The pharmacy must satisfy the current Mifepristone REMS pharmacy-certification requirements before dispensing under this pathway.", "Pharmacy certification is a current REMS condition for pharmacy dispensing of the drug for this indication."),
            ("C", "The prescription must come from a prescriber who satisfies the current Mifepristone REMS prescriber-certification requirement.", "The current REMS requires a certified prescriber for this use."),
            ("D", "Massachusetts Schedule VI status does not erase the separate federal product-specific REMS conditions.", "State Schedule VI classification and federal REMS requirements operate as different legal layers."),
            ("E", "The pharmacy can substitute ordinary Schedule VI transfer documentation for REMS certification because mifepristone is not federally controlled.", "Ordinary state prescription mechanics do not replace the product-specific federal REMS gate."),
        ], ["B", "C", "D"],
        "The pharmacist must apply both the ordinary Massachusetts prescription framework and the product-specific federal REMS. Retail dispensing is possible, but only through the current certified-pharmacy/certified-prescriber pathway.",
        ["FDA permits certified retail pharmacies to dispense mifepristone under the REMS.", "A REMS restriction is distinct from controlled-substance scheduling."],
        "Do not infer 'not federally controlled' to mean 'no federal dispensing restriction'.",
        ["FED-MIFEPRISTONE-REMS", "MA-SCHEDULE-VI"], ["mifepristone"], ["Identify the product and REMS-governed indication", "Check pharmacy certification", "Check prescriber certification", "Keep REMS separate from Schedule VI status"])

    q["MA-Q-0107"] = question_record(
        "MA-Q-0107", "V3_0107_PSE_ID_EXCEPTION", 3, "Restricted nonprescription products", "Pseudoephedrine identification", 4, "SBA",
        "A visitor from another country asks to buy one small package containing 60 mg total pseudoephedrine. The visitor has only a foreign passport and no identification document accepted by the federal CMEA retail-ID rule. The sale otherwise stays within all quantity limits. Which federal point is most relevant?",
        [
            ("A", "A foreign passport always satisfies the CMEA retail-ID requirement for any pseudoephedrine quantity.", "DEA guidance states that a foreign passport does not itself satisfy the ordinary CMEA identification rule described for these purchases."),
            ("B", "The sale is prohibited because every pseudoephedrine purchase, including a 60 mg single package, requires the ordinary logbook and ID process.", "Federal law provides a narrow single-package exception at no more than 60 mg."),
            ("C", "A single sales package containing no more than 60 mg may use the narrow exception from the ordinary purchaser-ID and logbook transaction requirement.", "DEA identifies this narrow exception for one sales package containing no more than 60 mg of pseudoephedrine."),
            ("D", "The pharmacist may waive identification for any purchase under the 3.6 gram daily limit.", "The daily quantity limit and the separate ID/logbook gate are different requirements."),
            ("E", "The visitor may buy any amount if another adult with acceptable identification signs the logbook instead.", "The purchaser's own identity and transaction must satisfy the applicable rule; another person cannot simply sign in place of the purchaser."),
        ], ["C"],
        "This is not a gram-limit question. The decisive fact is that the request is for one sales package containing no more than 60 mg, which DEA identifies as a narrow exception to the ordinary individual ID/logbook transaction requirement.",
        ["CMEA quantity limits and ID/logbook rules are separate gates.", "The 60 mg rule is a narrow single-package exception, not a general low-dose waiver."],
        "Passing the daily quantity limit does not answer the ID question; look for the single-package 60 mg exception.",
        ["FED-PSE-LOG-ID", "FED-PSE-QUANTITY"], ["pseudoephedrine"], ["Separate quantity compliance from purchaser-ID compliance", "Recognize the single-package 60 mg exception"])

    q["MA-Q-0108"] = question_record(
        "MA-Q-0108", "V3_0108_PSE_STORE_CERTIFICATION", 1, "Restricted nonprescription products", "CMEA seller compliance", 4, "SBA",
        "A pharmacy chain opens a new Massachusetts location and stocks pseudoephedrine behind the counter. Employees completed the chain's CMEA training, but the new physical location has not yet completed the DEA self-certification process. May the location begin covered retail pseudoephedrine sales because another store in the chain is already certified?",
        [
            ("A", "Yes, because one current chain-level self-certification automatically covers every future physical store.", "DEA's current self-certification process treats separate physical retail locations as separately certified locations."),
            ("B", "No. The new location must satisfy its own applicable CMEA self-certification requirement before covered retail sales begin.", "The physical location needs its own applicable self-certification; another store's certification does not authorize it."),
            ("C", "Yes, if all sales remain below 3.6 grams per purchaser per day.", "Quantity compliance does not replace the seller's certification requirement."),
            ("D", "No, because employee training and DEA self-certification are mutually exclusive alternatives and the chain chose training.", "Training and seller self-certification are related compliance duties, not alternatives."),
            ("E", "Yes, but only for electronic-logbook sales during the first 30 days after opening.", "No startup grace period based on electronic logbook use substitutes for required seller compliance."),
        ], ["B"],
        "CMEA compliance includes store-level seller obligations in addition to transaction-level limits. The new location cannot borrow another location's certification simply because ownership and training materials are shared.",
        ["DEA's online process identifies separate physical locations for self-certification.", "Employee training does not replace the location's applicable certification."],
        "Distinguish chain ownership from the physical-location unit used for CMEA seller certification.",
        ["FED-PSE-SELF-CERT", "FED-PSE-QUANTITY"], ["pseudoephedrine"], ["Identify the seller as a new physical location", "Check training and self-certification as separate prerequisites"])

    q["MA-Q-0109"] = question_record(
        "MA-Q-0109", "V3_0109_CLOZAPINE_REMS_REMOVED", 3, "Federal drug requirements", "Clozapine REMS status", 4, "SBA",
        "A patient presents a valid clozapine prescription in August 2026. A pharmacist trained under the former Clozapine REMS tells a colleague that the pharmacy cannot dispense until the patient is enrolled in the REMS and an ANC result is entered into that program. What is the current federal position?",
        [
            ("A", "The former REMS enrollment and ANC-verification gate remains mandatory for every clozapine dispensing.", "FDA removed the Clozapine REMS and no longer requires those program steps as dispensing prerequisites."),
            ("B", "The pharmacy may ignore any clinically significant blood-count information because removal of the REMS ended all clozapine monitoring concerns.", "Removal of the REMS did not eliminate the drug's clinical neutropenia risk or labeling-based monitoring recommendations."),
            ("C", "The pharmacy must enroll only the prescriber, while pharmacy and patient enrollment are no longer required.", "FDA removed the REMS program itself rather than retaining a prescriber-only enrollment gate."),
            ("D", "FDA removed the Clozapine REMS, so REMS enrollment and REMS ANC verification are no longer federal dispensing prerequisites, although clinical monitoring remains relevant.", "This reflects FDA's current post-REMS framework."),
            ("E", "Clozapine became an over-the-counter drug when the REMS was removed.", "Removal of a REMS does not change clozapine from prescription to OTC status."),
        ], ["D"],
        "FDA removed the Clozapine REMS effective in 2025. The pharmacist should not continue imposing the former program as a legal dispensing gate, while still addressing clinically meaningful monitoring under current labeling and professional practice.",
        ["REMS removal does not convert a prescription drug to OTC status.", "Clinical monitoring and a REMS enrollment gate are different concepts."],
        "A historical safety program may no longer be a current legal prerequisite even though the underlying clinical risk remains.",
        ["FED-CLOZAPINE-REMS-REMOVED", "MA-SCHEDULE-VI"], ["clozapine"], ["Determine the current REMS status as of the dispensing date", "Separate REMS eligibility from ongoing clinical monitoring"])

    q["MA-Q-0110"] = question_record(
        "MA-Q-0110", "V3_0110_CONTROLLED_LABEL_ELEMENTS", 3, "Dispensing", "Controlled-substance label", 4, "SATA",
        "During final verification of a Massachusetts alprazolam prescription, the pharmacist notices that the dispensing label has the patient, drug, directions, pharmacy, prescriber, and prescription number but omits some other information required by M.G.L. c. 94C §21. Which items should be corrected before dispensing? Select all that apply.",
        [
            ("A", "Add the date the prescription is being filled.", "Massachusetts requires the fill date on the controlled-substance container label."),
            ("B", "Add the patient's health-plan member identification number.", "The statute does not make the insurance member ID a required controlled-substance container-label element."),
            ("C", "Add the filling pharmacist's initials.", "The filling pharmacist's initials are among the statutory label elements."),
            ("D", "Add the wholesaler invoice number for the bottle used to fill the prescription.", "The wholesaler invoice number is not a required patient container-label element under this statute."),
            ("E", "Because tablets are being dispensed, add the number of tablets in the container.", "For tablets or capsules, the statute requires the number in the container on the label."),
        ], ["A", "C", "E"],
        "The container label has its own statutory checklist. Final verification should compare the actual label against the Massachusetts dispensing-label requirements rather than importing insurance or wholesaler fields.",
        ["The label rule is distinct from the information required on the prescription itself.", "Tablet or capsule count is expressly addressed by the statute."],
        "A valid prescription can still produce a noncompliant dispensed container if required label information is missing.",
        ["MA-CS-LABEL"], ["alprazolam"], ["Identify this as a dispensing-label review", "Match missing fields to M.G.L. c. 94C §21"])

    q["MA-Q-0111"] = question_record(
        "MA-Q-0111", "V3_0111_SCHEDULE_III_PAMPHLET_EXCEPTION", 3, "Dispensing", "Schedule II and III education", 4, "SBA",
        "A Massachusetts community pharmacy dispenses buprenorphine-naloxone, Schedule III, to a patient specifically for treatment of opioid use disorder. A technician asks whether the state Schedule II/III consumer-education pamphlet must accompany this dispensing. Which conclusion best applies?",
        [
            ("A", "Yes, because every Schedule III dispensing requires the pamphlet with no indication-based exceptions.", "The statute contains express exceptions, including treatment of substance use disorder or opioid dependence."),
            ("B", "The statutory pamphlet requirement has an exception when the Schedule II or III drug is prescribed for substance use disorder or opioid-dependence treatment.", "This dispensing fits the listed treatment exception."),
            ("C", "No, because buprenorphine-naloxone is Massachusetts Schedule VI rather than Schedule III.", "Buprenorphine-naloxone is federally and Massachusetts Schedule III; the exception turns on the treatment use, not Schedule VI status."),
            ("D", "Yes, unless the prescriber writes 'pamphlet not required' on the prescription.", "The statutory exceptions do not depend on a prescriber writing that notation."),
            ("E", "No, because the pamphlet requirement applies only to Schedule II stimulants.", "The statute reaches narcotics or controlled substances in Schedule II or III, subject to its exceptions."),
        ], ["B"],
        "The pharmacist first identifies that the drug falls within Schedule III, then checks the statutory exceptions. Because the prescription is for OUD treatment, the specific exception controls the pamphlet decision.",
        ["The rule covers Schedule II and III but contains setting/indication exceptions.", "Buprenorphine-naloxone remains Schedule III even when used for OUD."],
        "Do not stop after classifying the schedule; the indication can change the pamphlet requirement.",
        ["MA-CS-II-III-PAMPHLET", "FED-CS-SCHEDULES"], ["buprenorphine-naloxone"], ["Classify the medication as Schedule III", "Identify the stated OUD treatment indication", "Apply the statutory exception"])

    q["MA-Q-0112"] = question_record(
        "MA-Q-0112", "V3_0112_PATIENT_LOCKBOX_STORE_DUTY", 1, "Pharmacy operations", "Prescription lock boxes", 3, "SBA",
        "During a Board-readiness walkthrough, a Massachusetts community pharmacy that dispenses Schedule II through V prescriptions has no prescription lock boxes for sale and no notice about them near the pharmacy counter. The manager says patients can buy lock boxes online instead. What is the best compliance assessment?",
        [
            ("A", "The pharmacy complies because online retail availability satisfies the pharmacy's obligation.", "The statute places the availability and notice duties on each covered store location."),
            ("B", "Only pharmacies that dispense more than a threshold number of opioids must carry lock boxes.", "The statutory trigger is the covered pharmacy's registration to dispense Schedule II-V prescription drugs, not an opioid-volume threshold."),
            ("C", "The pharmacy needs only a verbal counseling script; physical availability and signage are optional.", "The statute specifically addresses lock boxes for sale and a posted notice."),
            ("D", "The store should make prescription lock boxes available for sale and display the required notice on or near the pharmacy counter.", "This is the store-level duty created by M.G.L. c. 94C §21B."),
            ("E", "The requirement applies only to institutional pharmacies, not community pharmacies.", "The statute targets covered pharmacies and excludes specified institutional settings rather than limiting the rule to them."),
        ], ["D"],
        "This is a facility-operation requirement, not a counseling preference. A covered store must satisfy both the on-site availability and notice components rather than redirecting patients to outside sellers.",
        ["The duty is tied to each covered store location.", "Patient lock boxes are different from the pharmacy's own controlled-substance storage."],
        "Do not confuse a patient-facing lock-box sales requirement with internal pharmacy security controls.",
        ["MA-PRESCRIPTION-LOCKBOX"], [], ["Identify the pharmacy as a covered Schedule II-V dispenser", "Check both product availability and counter notice"])

    q["MA-Q-0113"] = question_record(
        "MA-Q-0113", "V3_0113_POINT_OF_SALE_LESSER_PRICE", 1, "Pharmacy operations", "Prescription point-of-sale charge", 4, "SBA",
        "At a Massachusetts pharmacy, an insured patient's adjudicated cost-sharing amount for a generic prescription is $18. The pharmacy's current retail cash price for the same prescription is $11. The prescription is otherwise ready for sale. What amount does the Massachusetts point-of-sale rule require the pharmacy to charge?",
        [
            ("A", "$18, because an insurer-adjudicated cost share always overrides the pharmacy retail price.", "Massachusetts requires comparison of the applicable cost share and pharmacy retail price rather than automatically collecting the higher cost share."),
            ("B", "$14.50, because the pharmacy must split the difference between the two prices.", "The statute does not create an averaging formula."),
            ("C", "$11, because the pharmacy charges the lesser of the applicable cost-sharing amount and the pharmacy retail price.", "The retail price is lower on these facts, so it is the amount the statute selects."),
            ("D", "$18 unless the patient affirmatively asks to be treated as an uninsured cash customer before claim adjudication.", "The point-of-sale rule itself requires the lesser amount; it is not conditioned on a special opt-out request in the stated facts."),
            ("E", "$0, because a difference between retail price and cost sharing voids the patient's payment obligation.", "The law chooses the lower amount; it does not automatically eliminate payment."),
        ], ["C"],
        "The pharmacist or point-of-sale process compares the two defined amounts. Because the pharmacy retail price is lower than the applicable cost share, the pharmacy charges the retail price.",
        ["The comparison is made at the point of sale.", "The rule protects against collecting a cost share that exceeds the pharmacy retail price."],
        "An insurance claim result is not automatically the amount the pharmacy may collect when state law requires the lower comparison.",
        ["MA-POS-LESSER-PRICE"], [], ["Identify the two amounts the statute compares", "Select the lesser amount"])

    q["MA-Q-0114"] = question_record(
        "MA-Q-0114", "V3_0114_HYPODERMIC_AUTHORIZED_SELLER", 2, "Controlled substance law", "Hypodermic syringe and needle sales", 3, "SBA",
        "A customer asks a Massachusetts drugstore's front-end clerk to sell a package of hypodermic syringes intended for injection of a controlled substance. The store contains a licensed pharmacy, but the clerk is not a pharmacist and wants to complete the sale independently at the front register. What is the best legal response?",
        [
            ("A", "Route the transaction through an authorized seller under M.G.L. c. 94C §27, such as the pharmacist, rather than having the clerk independently make the sale.", "The statute limits these sales to listed categories of authorized sellers, including a pharmacist."),
            ("B", "The clerk may complete the sale because any employee of a premises containing a pharmacy is automatically treated as a pharmacist for §27.", "The statute identifies authorized seller categories; mere employment by a store containing a pharmacy does not make the clerk a pharmacist."),
            ("C", "The sale is prohibited at every retail pharmacy because syringes may be sold only by hospitals.", "The statute expressly includes pharmacists among authorized sellers."),
            ("D", "The clerk may sell the syringes only after entering the transaction in the DEA pseudoephedrine logbook.", "Pseudoephedrine CMEA logbook requirements do not govern a syringe sale."),
            ("E", "The clerk may complete the sale if the customer presents a Schedule II prescription.", "A Schedule II prescription does not convert an unauthorized seller into a statutory seller under §27."),
        ], ["A"],
        "The question is who may conduct the sale. Massachusetts §27 identifies authorized categories of sellers, including a pharmacist; the existence of a pharmacy inside the store does not automatically give unrelated front-end staff that statutory role.",
        ["The statute regulates the seller category.", "Syringe-sale authority is separate from pseudoephedrine and prescription-fill rules."],
        "Do not substitute the store's pharmacy license for the individual seller category named in the statute.",
        ["MA-HYPODERMIC-SALE"], [], ["Identify the product and intended use described by §27", "Determine whether the proposed seller is within an authorized category"])

    q["MA-Q-0116"] = question_record(
        "MA-Q-0116", "V3_0116_ORAL_SVI_DOCUMENTATION", 3, "Prescription format", "Oral Schedule VI prescription", 5, "SATA",
        "A known Massachusetts prescriber telephones a new warfarin prescription to the pharmacist. Warfarin is a Massachusetts Schedule VI prescription drug. Which actions correctly apply to this oral prescription? Select all that apply.",
        [
            ("A", "Because Schedule VI is excluded from §20(c)'s later follow-up-prescription requirement, the pharmacist does not need to create an oral-prescription record.", "The Schedule VI exception concerns the later follow-up document; the pharmacist still immediately reduces the oral prescription to writing."),
            ("B", "The pharmacist should immediately reduce the oral prescription to writing with the information required by Massachusetts law.", "Section 20(a) requires contemporaneous reduction of the oral controlled-substance prescription to writing."),
            ("C", "The pharmacist must demand a replacement electronic prescription within two days because §20(c) applies identically to Schedule VI.", "Section 20(c) expressly states that its later electronic/written follow-up requirements do not apply to Schedule VI."),
            ("D", "The Schedule VI exception from the later follow-up document does not eliminate the pharmacist's ordinary authenticity and validity responsibilities.", "Schedule VI remains a prescription controlled substance under Massachusetts law; the follow-up exception is not a blanket validity waiver."),
            ("E", "The pharmacist must convert the prescription to Schedule V before an oral transmission can be accepted.", "An oral Schedule VI prescription does not become Schedule V; classification is not changed by transmission method."),
        ], ["B", "D"],
        "Massachusetts separates the immediate oral-prescription record from the later follow-up-document rule. Schedule VI is excepted from the latter, not from the pharmacist's contemporaneous documentation and validity duties.",
        ["M.G.L. c. 94C §20(a) applies to oral controlled-substance prescriptions.", "Section 20(c) expressly excludes Schedule VI from its later follow-up prescription requirement."],
        "A statutory exception can be narrow: identify exactly which step it removes and which duties remain.",
        ["MA-ORAL-CONTROLLED-DOCUMENTATION", "MA-SCHEDULE-VI"], ["warfarin"], ["Classify warfarin as Massachusetts Schedule VI", "Separate immediate oral documentation from later follow-up documentation", "Apply the narrow Schedule VI exception"])

    q["MA-Q-0117"] = question_record(
        "MA-Q-0117", "V3_0117_COMPOUND_PRODUCT_LABEL", 3, "Compounding", "Compounded product labeling", 4, "SBA",
        "A Massachusetts pharmacy licensed for sterile compounding prepares a patient-specific sterile compounded infusion for outpatient use. The ordinary prescription label is complete, but the final container does not identify the preparation as compounded and does not display the pharmacy's required pharmacist-contact telephone number. What should happen before the product leaves the pharmacy?",
        [
            ("A", "Dispense it because ordinary prescription-label elements make all compounded-product labeling requirements optional.", "Massachusetts imposes additional compounded-preparation labeling and, for covered pharmacies, pharmacist-contact requirements."),
            ("B", "Remove the ordinary prescription label and use only the word 'sterile' on the container.", "The additional compounded-product information supplements rather than replaces ordinary applicable labeling duties."),
            ("C", "Correct the container to identify the sterile compounded preparation and include the required pharmacist-contact information before outpatient dispensing.", "The facts describe a covered outpatient sterile compounded preparation missing the additional statutory label/contact elements."),
            ("D", "Dispense it unchanged if the patient has previously received another compounded medication from the pharmacy.", "Prior patient experience does not waive the product-specific label and communication requirements."),
            ("E", "Treat the missing information only as a continuing-education issue for the compounding pharmacist.", "The defect is on the dispensed product and communication label, not merely the pharmacist's CE record."),
        ], ["C"],
        "The pharmacy must verify the compounded product itself, not just the prescription. Massachusetts adds a compounded-preparation designation and, for covered sterile/complex nonsterile compounding pharmacies, required pharmacist contact information for outpatient products.",
        ["Compounded-drug labeling is distinct from compounding CE.", "The institutional inpatient exception does not fit an outpatient dispensing."],
        "A complete ordinary prescription label can still be incomplete for a compounded preparation.",
        ["MA-COMPOUND-LABEL-CONTACT"], [], ["Identify the preparation as outpatient sterile compounded product", "Apply the additional compounded label and contact requirements"])

    q["MA-Q-0121"] = question_record(
        "MA-Q-0121", "V3_0121_EXCEPTED_PREPARATION_RETAIL", 3, "Controlled substance dispensing", "Excepted preparations", 5, "SATA",
        "A Massachusetts pharmacist is considering a nonprescription retail sale of a medicinal preparation that has already been confirmed to qualify for the controlled-substance exception described in M.G.L. c. 94C §4. Which §5 controls still apply to the sale? Select all that apply.",
        [
            ("A", "The purchaser must identify themself to the pharmacist's satisfaction.", "Section 5 conditions the retail exception on purchaser identification satisfactory to the pharmacist."),
            ("B", "The pharmacist must keep the required purchaser/product sale record.", "The statute requires an accurate record including purchaser and preparation information."),
            ("C", "Because the product qualifies for an exception, any amount may be sold in a single transaction without a time-based limit.", "The exception is conditional; §5 imposes a four-ounce per person/48-hour limit."),
            ("D", "The pharmacist must observe the four-ounce-per-person limit during a 48-hour period.", "This is the quantity/time condition stated in §5."),
            ("E", "The sale must be processed as a Schedule II emergency oral prescription.", "The special retail exception is not the Schedule II emergency prescription pathway."),
        ], ["A", "B", "D"],
        "An excepted preparation is not an unrestricted OTC item. The special retail pathway remains conditioned on identification, quantity/time limits, good-faith medicinal sale, and recordkeeping.",
        ["The question assumes the product already qualifies for the underlying §4 exception.", "Section 5 then supplies the retail conditions."],
        "An exception from ordinary prescription control can still carry its own purchaser, quantity, and record requirements.",
        ["MA-EXCEPTED-CS-SALE"], [], ["Accept the stem's premise that the product qualifies under §4", "Apply the separate §5 retail conditions", "Distinguish the pathway from ordinary prescription dispensing"])

    q["MA-Q-0125"] = question_record(
        "MA-Q-0125", "V3_0125_FORM222_DEFECT_PRIORITY", 3, "Controlled substance procurement", "Form 222 defect and validity", 4, "SBA",
        "A supplier receives a paper DEA Form 222 twenty days after execution. The form is otherwise timely, but the purchaser altered a Schedule II quantity after signing by writing over the original number. The purchaser asks the supplier to initial the change and ship the order. What is the best response?",
        [
            ("A", "Fill the order because the form arrived within 60 days and timeliness cures execution defects.", "The 60-day validity period does not cure an altered or defective form."),
            ("B", "Fill only the unaltered line items and correct the altered line after shipment.", "A supplier may not correct and fill a defective executed form in that manner."),
            ("C", "Convert the altered paper form into a CSOS order by scanning it and adding an electronic signature.", "A paper Form 222 is not converted into a valid CSOS order by scanning it."),
            ("D", "Do not fill the defective form; the purchaser must issue a proper replacement order despite the original form still being within 60 days.", "Defect/execution validity is an independent gate from the 60-day time window."),
            ("E", "Wait until day 61 and then fill the form because expiration removes the need to address the alteration.", "Expiration would create an additional reason not to fill the order, not cure the alteration."),
        ], ["D"],
        "A valid Form 222 must satisfy both execution/content rules and the time window. Here the form is timely but defective, so the supplier cannot use the 60-day rule to overlook the alteration.",
        ["Form validity involves more than age.", "A defective Form 222 cannot be corrected by the supplier and then filled as though properly executed."],
        "When two gates apply, passing the timing gate does not cure a separate execution defect.",
        ["FED-FORM222-DEFECT", "FED-FORM222-60DAY"], [], ["Check the 60-day timing gate", "Independently identify the altered form as defective", "Apply the stricter defect consequence"])

    q["MA-Q-0126"] = question_record(
        "MA-Q-0126", "V3_0126_FORM222_LOST_REPLACEMENT", 3, "Controlled substance procurement", "Lost Form 222 replacement", 5, "SBA",
        "A pharmacy mailed an executed paper DEA Form 222 to its supplier. The supplier reports that the form never arrived, no Schedule II goods were shipped, and the pharmacy cannot locate the original. The pharmacy still needs the order. What is the appropriate federal replacement process?",
        [
            ("A", "Send the supplier a photocopy of the lost form and ask it to treat the photocopy as the original order.", "A photocopy does not become the replacement executed Form 222 required after loss."),
            ("B", "Execute a new Form 222, attach the required statement identifying the lost form and nonreceipt of goods, retain the required copies, and make the applicable DEA loss report.", "This follows the replacement-statement and reporting framework for a lost Form 222."),
            ("C", "Ask the supplier to recreate the purchaser's lost form because only suppliers may issue replacement Form 222s.", "The purchaser executes the replacement order and required statement; the supplier does not recreate the purchaser's lost order form."),
            ("D", "Wait 60 days from the lost form's execution date; only after expiration may a replacement order be issued.", "The loss rule does not require waiting for the original form to age out before using the replacement procedure."),
            ("E", "Treat the missing paper form as an inventory significant loss and file only DEA Form 106 without replacing the order.", "A lost order form has its own Form 222 replacement/reporting procedure; it is not the same as loss of controlled-substance inventory."),
        ], ["B"],
        "A lost executed Form 222 is handled through a replacement order plus a statement tying the replacement to the lost form and documenting nonreceipt. The registrant also follows the DEA reporting rule for lost or stolen order forms.",
        ["The replacement statement identifies the lost order form and the fact that goods were not received.", "Loss of an order form and loss of drug inventory are different reportable events."],
        "Do not reach for DEA Form 106 merely because the word 'loss' appears; identify what was lost.",
        ["FED-FORM222-LOSS"], [], ["Determine that the lost item is an executed order form, not drug inventory", "Apply the replacement Form 222 and statement procedure", "Apply the order-form loss reporting duty"])

    q["MA-Q-0127"] = question_record(
        "MA-Q-0127", "V3_0127_FORM222_POA_SIGNATURE", 3, "Controlled substance procurement", "Form 222 signing authority", 4, "SBA",
        "A pharmacy's DEA registrant wants a staff pharmacist to sign paper DEA Forms 222 when the registrant is away. The staff pharmacist is not the person who signed the pharmacy's most recent DEA registration application. Which arrangement can lawfully provide signing authority?",
        [
            ("A", "A verbal instruction from the pharmacy manager made before each order, with no retained authorization record.", "Form 222 signing authority is not created by an undocumented verbal instruction."),
            ("B", "A notation in the pharmacy's employee handbook stating that every licensed pharmacist may sign Form 222 automatically.", "Licensure alone does not create the registrant-specific authority required to execute the order form."),
            ("C", "Use of the registrant's CSOS password to sign the paper form electronically.", "CSOS credentials do not substitute for the paper Form 222 power-of-attorney framework."),
            ("D", "A supplier's written permission authorizing the staff pharmacist to sign the purchaser's order forms.", "The purchaser's registrant grants the authority; the supplier cannot confer it on the purchaser's employee."),
            ("E", "A compliant power of attorney granted by the registrant and retained so it is available for inspection.", "DEA permits a registrant to grant Form 222 execution authority through a compliant power of attorney."),
        ], ["E"],
        "Paper Form 222 signing authority can extend beyond the person who signed the DEA registration, but it must be conferred through the DEA power-of-attorney mechanism rather than job title, supplier consent, or shared credentials.",
        ["The power of attorney is retained for inspection rather than submitted with each order to DEA.", "CSOS certificate authority and paper Form 222 power of attorney are related but distinct mechanisms."],
        "Do not assume 'licensed pharmacist' automatically means 'authorized Form 222 signer'.",
        ["FED-FORM222-POA", "FED-FORM222-ORDER"], [], ["Identify who presently lacks direct registrant signing authority", "Apply the DEA power-of-attorney pathway"])

    q["MA-Q-0128"] = question_record(
        "MA-Q-0128", "V3_0128_CSOS_SUPPLIER_CERTIFICATE_GATE", 3, "Controlled substance procurement", "CSOS supplier validation", 4, "SBA",
        "A wholesaler receives an electronic CSOS order for oxycodone from a pharmacy. The order data are complete, but the wholesaler's validation system shows that the digital certificate used to sign the order was revoked before the order was transmitted. What should the supplier do?",
        [
            ("A", "Ship the order because complete line-item data are enough even when the signing certificate is invalid.", "CSOS validity requires a valid DEA-issued digital certificate as well as complete order data."),
            ("B", "Print the electronic order and treat the printout as a valid paper DEA Form 222.", "Printing does not convert an invalid CSOS signature into a valid paper order form."),
            ("C", "Reject the electronic order rather than fill it on the revoked certificate; the purchaser must submit a valid authorized order.", "Supplier validation includes certificate validity, and a revoked certificate cannot support the required digital signature."),
            ("D", "Ship half the order because a partial shipment reduces the risk created by the revoked certificate.", "Partial shipment does not cure an invalid electronic order."),
            ("E", "Hold the order until 60 days after execution, when the certificate-revocation issue no longer matters.", "Time does not cure an invalid/revoked certificate; a valid order is required."),
        ], ["C"],
        "The supplier has its own CSOS validity gate. Complete product fields are not enough when the required DEA digital certificate is revoked or otherwise invalid.",
        ["CSOS relies on certificate validation and digital signature integrity.", "A printout of an invalid electronic order is not a substitute paper Form 222."],
        "Electronic transmission is not synonymous with valid electronic authorization.",
        ["FED-CSOS-SUPPLIER-VALIDATION", "FED-CSOS"], [], ["Check the electronic order data", "Independently validate the signing certificate", "Reject an order that fails the certificate gate"])

    q["MA-Q-0129"] = question_record(
        "MA-Q-0129", "V3_0129_FORM222_WRITTEN_CANCELLATION", 3, "Controlled substance procurement", "Form 222 cancellation", 4, "SBA",
        "A pharmacy has already mailed a valid paper DEA Form 222 to its supplier for three Schedule II products. Before shipment, the pharmacy decides it no longer needs one line item but wants the other two. What is the appropriate federal way to stop that portion of the order?",
        [
            ("A", "Notify the supplier in writing that the identified portion is canceled so the supplier can document the cancellation on the original Form 222.", "DEA permits cancellation of part or all of a submitted paper Form 222 through written notice to the supplier, with supplier documentation on the original."),
            ("B", "Ask the supplier to erase the unwanted line from the executed original form before filling the remaining lines.", "Erasure or alteration is not the lawful cancellation procedure for an executed Form 222."),
            ("C", "File DEA Form 106 for the unwanted line because canceling an order is treated as a significant loss.", "Cancellation of an unshipped order is not a theft or significant loss of controlled-substance inventory."),
            ("D", "Cancel the entire pharmacy DEA registration because a submitted Form 222 cannot be changed in part.", "DEA expressly provides a mechanism to cancel part or all of a submitted order."),
            ("E", "Wait for delivery, accept the unwanted Schedule II product, and destroy it because pre-shipment cancellation is prohibited.", "The purchaser may cancel before shipment using the written supplier-notification procedure."),
        ], ["A"],
        "Once a paper Form 222 has been submitted, the purchaser does not alter the executed form. It sends written cancellation to the supplier, which documents the canceled item on the original form while processing any remaining valid items.",
        ["DEA permits partial or complete cancellation of a submitted paper Form 222.", "Cancellation is different from a lost form, defective form, or inventory loss."],
        "Identify the transaction state: the form exists and is valid, but the purchaser wants to cancel part of an unshipped order.",
        ["FED-FORM222-CANCEL", "FED-FORM222-ORDER"], [], ["Confirm the submitted Form 222 is otherwise valid", "Identify that only part of the order is being canceled before shipment", "Use written notice to the supplier"])

    assert set(q) == set(FAILED_REALISM_IDS), (set(FAILED_REALISM_IDS) - set(q), set(q) - set(FAILED_REALISM_IDS))
    return q


def apply_naloxone_question_clarifications() -> None:
    p = DATA / "questions" / "ma-q-0097.json"
    q = load_json(p)
    q["stem"] = "A father asks a Massachusetts community pharmacy to obtain a prescription-labeled naloxone product through the pharmacy's authorized naloxone prescription/standing-order pathway because his adult daughter recently survived an opioid overdose. The daughter is not present. Which conclusion is most defensible?"
    q["rule_ids"] = ["MA-NALOXONE", "MA-SCHEDULE-VI"]
    q["explanation"]["related_facts"] = ["Prescription naloxone and FDA-labeled OTC naloxone are separate products under current Massachusetts DCP guidance.", "Massachusetts prescription naloxone access can place rescue medication with a third party positioned to assist."]
    q["verification_status"] = q["lifecycle_status"] = "AUDIT_PENDING"
    q["last_legal_review"] = TODAY
    q["audits"] = []
    q["duplicate_review_status"] = "PENDING"
    q["independent_audit_status"] = "PENDING"
    q["final_adjudication"] = None
    write_json(p, q)

    p = DATA / "questions" / "ma-q-0098.json"
    q = load_json(p)
    q["stem"] = "A patient at risk of opioid overdose asks a Massachusetts pharmacy for a prescription-labeled naloxone product. The patient has no patient-specific naloxone prescription, but the pharmacy participates in an authorized statewide standing-order prescription pathway. What is the key legal point?"
    q["rule_ids"] = ["MA-NALOXONE", "MA-SCHEDULE-VI"]
    q["explanation"]["related_facts"] = ["The statewide standing order can serve as prescription authority for prescription naloxone when its requirements are met.", "FDA-labeled OTC naloxone is a separate product and does not become Schedule VI merely because prescription naloxone also exists."]
    q["verification_status"] = q["lifecycle_status"] = "AUDIT_PENDING"
    q["last_legal_review"] = TODAY
    q["audits"] = []
    q["duplicate_review_status"] = "PENDING"
    q["independent_audit_status"] = "PENDING"
    q["final_adjudication"] = None
    write_json(p, q)


def update_family_matrix(replacements: dict[str, dict]) -> None:
    path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(path)
    new_family_ids = {q["family_id"] for q in replacements.values()}
    matrix["families"] = [f for f in matrix["families"] if f.get("family_id") not in new_family_ids]
    for qid, q in replacements.items():
        primary = [q["rule_ids"][0]]
        secondary = q["rule_ids"][1:]
        matrix["families"].append(family_record(q, primary, secondary, q["explanation"]["mpje_trap"]))

    # Naloxone family records now explicitly acknowledge the Schedule VI prescription layer.
    for f in matrix["families"]:
        if f.get("family_id") in {"EXP1_0097_NALOXONE_THIRD_PARTY", "EXP1_0098_NALOXONE_PATHWAY"}:
            second = list(f.get("secondary_rule_ids", []))
            if "MA-SCHEDULE-VI" not in second:
                second.append("MA-SCHEDULE-VI")
            f["secondary_rule_ids"] = second

    questions = {}
    for qp in sorted((DATA / "questions").glob("*.json")):
        rec = load_json(qp)
        questions[rec["question_id"]] = rec
    candidate_counts = Counter(rec.get("family_id") for rec in questions.values())
    released_counts = Counter(
        rec.get("family_id") for rec in questions.values()
        if rec.get("verification_status") == "RELEASED" and rec.get("lifecycle_status") == "RELEASED"
    )
    known = {f["family_id"] for f in matrix["families"]}
    missing = set(candidate_counts) - known
    if missing:
        raise RuntimeError(f"family matrix missing question families: {sorted(missing)}")
    for f in matrix["families"]:
        f["current_candidate_count"] = candidate_counts.get(f["family_id"], 0)
        f["current_released_count"] = released_counts.get(f["family_id"], 0)
    matrix["last_reviewed"] = TODAY
    write_json(path, matrix)


def main() -> int:
    # Hard release boundary: the already-released Wave 1 questions must be byte-for-byte preserved.
    before = {
        qid: (DATA / "questions" / f"{qid.lower()}.json").read_bytes()
        for qid in RELEASED_WAVE1
    }
    preview_path = Path("site/generated/preview_allowlist.json")
    preview_before = preview_path.read_bytes()

    install_new_rules()
    repair_existing_rules()
    repair_drugs()

    replacements = build_replacements()
    for qid, record in replacements.items():
        write_json(DATA / "questions" / f"{qid.lower()}.json", record)
    apply_naloxone_question_clarifications()
    update_family_matrix(replacements)

    for qid, raw in before.items():
        now = (DATA / "questions" / f"{qid.lower()}.json").read_bytes()
        if now != raw:
            raise RuntimeError(f"released Wave 1 question changed during v3 authoring: {qid}")
    if preview_path.read_bytes() != preview_before:
        raise RuntimeError("public preview allowlist changed during v3 authoring")

    plan = {
        "base_release_count": 58,
        "released_wave1_preserved": sorted(RELEASED_WAVE1),
        "semantic_replacements": {qid: replacements[qid]["family_id"] for qid in sorted(replacements)},
        "naloxone_product_clarifications": ["MA-Q-0097", "MA-Q-0098"],
        "known_dependency_repairs": ["MA-NALOXONE", "FED-INVENTORY-INITIAL", "FED-INVENTORY-BIENNIAL", "FED-FORM222-LOSS"],
        "audit_boundary": "All 29 changed unreleased Batch 1 questions require fresh current-hash independent audits before release.",
    }
    out = Path("repair_specs/exp1_v3/replacement_plan.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    write_json(out, plan)
    print("Batch 1 v3 applied: 27 semantic replacements + 2 naloxone product clarifications; released Wave 1 preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

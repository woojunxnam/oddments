from __future__ import annotations

from pathlib import Path

from qa_common import DATA, ROOT, load_json, semantic_content_hash, write_json

TODAY = "2026-08-17"
REPAIR_IDS = {
    "MA-Q-0009", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017", "MA-Q-0040",
    "MA-Q-0075", "MA-Q-0076", "MA-Q-0078", "MA-Q-0081", "MA-Q-0085",
    "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
}
KEEP_IDS = {
    "MA-Q-0004", "MA-Q-0013", "MA-Q-0020", "MA-Q-0027", "MA-Q-0028",
    "MA-Q-0030", "MA-Q-0032", "MA-Q-0034", "MA-Q-0036", "MA-Q-0059",
    "MA-Q-0060", "MA-Q-0077", "MA-Q-0079", "MA-Q-0080", "MA-Q-0082",
    "MA-Q-0083", "MA-Q-0084",
}


def qpath(qid: str) -> Path:
    return DATA / "questions" / f"ma-q-{qid[-4:]}.json"


def save_question(qid: str, *, updates: dict) -> None:
    q = load_json(qpath(qid))
    if q["question_id"] != qid:
        raise RuntimeError(f"question id mismatch for {qid}")
    q.update(updates)
    # Editor repair must never self-promote release maturity.
    q["verification_status"] = "AUDIT_PENDING"
    q["lifecycle_status"] = "AUDIT_PENDING"
    q["last_legal_review"] = TODAY
    q["audits"] = []
    q["duplicate_review_status"] = "PENDING"
    q["independent_audit_status"] = "PENDING"
    q["final_adjudication"] = None
    q["development_fixture"] = True
    write_json(qpath(qid), q)


def add_counseling_documentation_rule() -> None:
    path = DATA / "rules" / "ma-counseling-documentation.json"
    if path.exists():
        raise RuntimeError("MA-COUNSELING-DOCUMENTATION already exists")
    rule = {
        "rule_id": "MA-COUNSELING-DOCUMENTATION",
        "content_version": 1,
        "content_hash": "0" * 64,
        "title": "Massachusetts counseling refusal documentation",
        "jurisdiction": "MA",
        "area": 2,
        "topic": "Patient care",
        "subtopic": "Counseling documentation",
        "rule_summary": (
            "Under M.G.L. c. 94C, § 21A, the pharmacist or designee must make reasonable efforts to obtain, "
            "record and maintain specified patient information, including any failure to accept the pharmacist's "
            "offer to counsel. The information may be recorded in the patient profile, prescription signature log, "
            "or another record system; absence of a record of refusal creates a presumption that counseling was provided."
        ),
        "exam_relevance": (
            "Tests the separate Massachusetts documentation consequence that follows an offer to counsel rather than "
            "treating the offer, counseling performance, and refusal record as the same duty."
        ),
        "authority": [
            {
                "type": "STATUTE",
                "name": "Massachusetts prospective drug review and counseling statute",
                "section": "M.G.L. c. 94C, § 21A",
                "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21A"
            }
        ],
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": TODAY,
        "numeric_facts": [],
        "exceptions": [
            "The section does not apply to drugs dispensed to hospital or nursing-home inpatients except to the extent required by applicable federal regulations."
        ],
        "common_confusions": [
            "A refusal does not make the offer irrelevant: the statute separately addresses reasonable efforts to record a failure to accept the offer.",
            "A technician or other designee may participate in making the offer, but that does not make the designee the person authorized to provide pharmacist counseling."
        ],
        "related_rule_ids": ["MA-COUNSELING"],
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": "Current Massachusetts General Laws source independently checked by the editor on 2026-08-17; requires fresh independent audit before release."
    }
    rule["content_hash"] = semantic_content_hash(rule, "rule")
    write_json(path, rule)


def update_taxonomy_families() -> None:
    path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(path)
    desired = {
        "P2_0085_MA_PRODUR": 3,
        "P2_0087_MA_INTERCHANGE": 4,
        "P2_0088_MA_RETURN_QUARANTINE": 2,
    }
    seen = set()
    for family in matrix.get("families", []):
        fid = family.get("family_id")
        if fid in desired:
            family["area"] = desired[fid]
            seen.add(fid)
    if seen != set(desired):
        raise RuntimeError(f"missing taxonomy families: {sorted(set(desired) - seen)}")
    matrix["last_reviewed"] = TODAY
    write_json(path, matrix)


def main() -> int:
    if len(REPAIR_IDS) != 13 or len(KEEP_IDS) != 17 or REPAIR_IDS & KEEP_IDS:
        raise RuntimeError("unexpected T1 editor decision partition")

    add_counseling_documentation_rule()

    save_question(
        "MA-Q-0009",
        updates={
            "stem": "During a pharmacy-system configuration audit, the pharmacist reviews rules that would automatically control dispensing or monitoring. Which configurations are legally correct? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Treat pregabalin as Schedule V and submit covered dispensing to MassPAT."},
                {"id": "B", "text": "Treat gabapentin as federally noncontrolled but Massachusetts Schedule VI and MassPAT-reportable."},
                {"id": "C", "text": "Treat methylphenidate as Schedule II and block prescription refills."},
                {"id": "D", "text": "Treat pseudoephedrine as Schedule V solely because CMEA restricts its retail sale."},
                {"id": "E", "text": "Apply the federal Schedule III-IV five-refill/six-month rule to gabapentin solely because Massachusetts places it in Schedule VI."},
            ],
            "correct_choice_ids": ["A", "B", "C"],
            "explanation": {
                "core_reasoning": "A pharmacy system must keep federal schedule, Massachusetts schedule, MassPAT reporting, refill limits, and CMEA retail controls separate. Pregabalin, gabapentin, and methylphenidate require the stated configurations; CMEA does not make pseudoephedrine Schedule V, and Massachusetts Schedule VI status does not import the federal Schedule III-IV refill rule into gabapentin.",
                "choice_analysis": {
                    "A": "Correct. Pregabalin is Schedule V, and covered Massachusetts dispensing is reportable to MassPAT.",
                    "B": "Correct. Gabapentin is not federally scheduled, but Massachusetts treats it as Schedule VI and includes it in PMP reporting.",
                    "C": "Correct. Methylphenidate is Schedule II, for which refills are prohibited.",
                    "D": "Incorrect. CMEA imposes retail controls on pseudoephedrine but does not place it in Schedule V.",
                    "E": "Incorrect. Massachusetts Schedule VI classification does not by itself trigger the federal Schedule III-IV refill ceiling."
                },
                "related_facts": [
                    "Monitoring status and controlled-substance schedule are separate legal concepts.",
                    "A state scheduling rule does not automatically change a drug's federal schedule."
                ],
                "mpje_trap": "Do not convert every monitored or behind-the-counter product into a federally scheduled drug or import federal refill rules from an unrelated schedule."
            },
            "reasoning_steps": [
                "Classify each drug under federal law",
                "Apply Massachusetts scheduling and PMP rules separately",
                "Apply the legal consequence tied to the actual schedule or retail-control pathway"
            ],
        },
    )

    save_question(
        "MA-Q-0015",
        updates={
            "stem": "An adult patient receives a lawful 14-day outpatient prescription for buprenorphine-naloxone specifically for treatment of opioid use disorder. A staff member says Massachusetts' seven-day initial-opiate statute automatically requires the prescription to be reduced to seven days. What is the best response to that specific claim?",
            "choices": [
                {"id": "A", "text": "Agree, because every medication related to an opioid is subject to the seven-day statute regardless of indication."},
                {"id": "B", "text": "Disagree. The seven-day statute expressly does not apply to medications designed for treatment of substance abuse or opioid dependence; the prescription must instead satisfy the other laws governing its OUD pathway."},
                {"id": "C", "text": "Agree unless the patient has previously filled an opioid prescription in Massachusetts."},
                {"id": "D", "text": "Disagree because buprenorphine-naloxone becomes Massachusetts Schedule VI when used for OUD."},
                {"id": "E", "text": "Reduce the quantity to seven days without prescriber involvement because pharmacists may unilaterally rewrite any opioid prescription to comply with supply limits."},
            ],
            "correct_choice_ids": ["B"],
            "explanation": {
                "core_reasoning": "M.G.L. c. 94C, § 19D(c) excludes medications designed for treatment of substance abuse or opioid dependence from the seven-day supply statute. That exclusion answers the narrow seven-day question; it does not waive the separate federal and state requirements that govern buprenorphine-naloxone and OUD treatment.",
                "choice_analysis": {
                    "A": "Incorrect. Section 19D contains an express treatment-indication exclusion.",
                    "B": "Correct. The seven-day statute itself does not apply to the described OUD-treatment medication, while other applicable prescribing/dispensing rules remain in force.",
                    "C": "Incorrect. The statutory exclusion here turns on the OUD-treatment purpose, not prior opioid-fill history.",
                    "D": "Incorrect. Buprenorphine-naloxone remains Schedule III; the result comes from the § 19D treatment exclusion.",
                    "E": "Incorrect. The statutory issue does not create a general pharmacist power to rewrite a prescription."
                },
                "related_facts": ["The adult first-outpatient seven-day rule and the OUD-treatment exclusion must be read together."],
                "mpje_trap": "Do not stop at the word 'opioid'; first determine whether the statute expressly excludes the treatment pathway."
            },
            "drug_ids": ["buprenorphine-naloxone"],
            "reasoning_steps": [
                "Identify the medication and its stated OUD-treatment purpose",
                "Apply the express § 19D(c) exclusion before applying the seven-day ceiling",
                "Keep separate OUD prescribing/dispensing requirements outside the narrow question"
            ],
        },
    )

    save_question(
        "MA-Q-0016",
        updates={
            "stem": "A Massachusetts practitioner issues an adult patient's first outpatient oxycodone prescription for a 10-day supply after an acute fracture. The practitioner documents in the medical record that more than seven days are required for the acute condition and that a non-opiate alternative is not appropriate. What is the most accurate conclusion about the seven-day statute?",
            "choices": [
                {"id": "A", "text": "The prescription must still be limited to seven days because no exception can apply to an adult's first outpatient opiate prescription."},
                {"id": "B", "text": "The documented statutory exception can permit the quantity needed for the acute condition; the seven-day ceiling is not absolute on these facts."},
                {"id": "C", "text": "The exception applies only if the patient is a minor."},
                {"id": "D", "text": "The exception applies automatically to every Schedule II prescription without documentation."},
                {"id": "E", "text": "A pharmacist may create the missing medical-record documentation after dispensing if the prescriber did not do so."},
            ],
            "correct_choice_ids": ["B"],
            "explanation": {
                "core_reasoning": "Section 19D generally limits an adult's first outpatient opiate prescription to seven days, but subsection (b) permits a greater quantity when the practitioner determines it is required for a qualifying acute condition or other listed purpose and documents both the triggering condition and that a non-opiate alternative was not appropriate.",
                "choice_analysis": {
                    "A": "Incorrect. The statute contains a documented exception.",
                    "B": "Correct. The facts state the findings and documentation that activate the statutory exception.",
                    "C": "Incorrect. The exception can apply to adults or minors when its conditions are met.",
                    "D": "Incorrect. Schedule II status alone does not activate the exception; the statutory clinical findings and documentation matter.",
                    "E": "Incorrect. The statute assigns the clinical judgment and medical-record documentation to the practitioner."
                },
                "related_facts": ["The exception can also address chronic pain management, cancer-related pain, and palliative care when the statutory conditions are met."],
                "mpje_trap": "The seven-day number is a general rule, not an absolute ceiling when the statute's documented exception is satisfied."
            },
            "reasoning_steps": [
                "Identify an adult's first outpatient opiate prescription",
                "Check whether a statutory exception applies",
                "Verify the required practitioner documentation before treating the seven-day ceiling as displaced"
            ],
        },
    )

    save_question(
        "MA-Q-0017",
        updates={
            "stem": "A 16-year-old patient has received opiates before and now presents a 10-day Norco prescription for outpatient dental pain. No statutory exception is documented. A staff member says the seven-day rule no longer applies because this is not the minor's first opiate prescription. What should the pharmacist recognize?",
            "choices": [
                {"id": "A", "text": "The staff member is correct; the minor rule applies only to a first opiate prescription, just like the adult rule."},
                {"id": "B", "text": "The staff member is incorrect; the minor provision generally limits an opiate prescription to seven days at any time unless a statutory exception is properly documented."},
                {"id": "C", "text": "The 10-day quantity becomes permissible if a parent signs the prescription at pickup."},
                {"id": "D", "text": "The Schedule II quantity rule automatically overrides the minor-specific seven-day provision."},
                {"id": "E", "text": "Prior opioid exposure converts the patient to the adult first-prescription rule even though the patient is still a minor."},
            ],
            "correct_choice_ids": ["B"],
            "explanation": {
                "core_reasoning": "Section 19D distinguishes adults from minors. The adult ceiling is tied to the first outpatient opiate prescription, while the minor provision applies to an opiate prescription at any time, subject to the statute's documented exceptions.",
                "choice_analysis": {
                    "A": "Incorrect. The minor provision is not limited to the first opiate prescription.",
                    "B": "Correct. Prior opiate history does not remove the minor-specific seven-day rule.",
                    "C": "Incorrect. Parental signature is not a substitute for the practitioner's statutory exception findings and documentation.",
                    "D": "Incorrect. A broader Schedule II quantity rule does not erase the more specific minor supply limit.",
                    "E": "Incorrect. Prior exposure does not change the patient's age or the statutory minor provision."
                },
                "related_facts": ["The statute separately requires discussion with the parent or guardian of a minor about opiate risks and why the prescription is necessary."],
                "mpje_trap": "Do not copy the adult 'first prescription' trigger into the separate minor rule."
            },
            "reasoning_steps": [
                "Identify that the patient is a minor",
                "Separate the minor rule from the adult first-prescription trigger",
                "Check for a documented exception before accepting a supply greater than seven days"
            ],
        },
    )

    save_question(
        "MA-Q-0040",
        updates={
            "stem": "An adult patient's first outpatient tramadol prescription for acute pain requests a 10-day supply and contains no facts supporting a statutory exception. A technician argues that the Massachusetts seven-day opiate rule cannot apply because tramadol is Schedule IV rather than Schedule II. Which conclusion is most accurate?",
            "choices": [
                {"id": "A", "text": "The technician is correct; the seven-day rule applies only to Schedule II narcotics."},
                {"id": "B", "text": "The technician is correct because Schedule IV drugs are never treated as opiates under Massachusetts supply-limit law."},
                {"id": "C", "text": "The prescription is exempt whenever the patient pays cash."},
                {"id": "D", "text": "The pharmacy may ignore the supply issue if MassPAT was checked."},
                {"id": "E", "text": "The technician is incorrect; schedule classification and the seven-day opiate-supply statute are separate questions, so the statutory seven-day rule can still control tramadol on these facts."},
            ],
            "correct_choice_ids": ["E"],
            "explanation": {
                "core_reasoning": "The Massachusetts seven-day statute is triggered by an opiate prescription and its patient/use circumstances, not by a requirement that the drug be Schedule II. Tramadol's Schedule IV status therefore does not by itself remove the adult first-outpatient seven-day rule.",
                "choice_analysis": {
                    "A": "Incorrect. The statute is not written as a Schedule-II-only limit.",
                    "B": "Incorrect. Tramadol's Schedule IV classification does not decide whether the opiate supply-limit statute applies.",
                    "C": "Incorrect. Payment method is not the statutory trigger.",
                    "D": "Incorrect. PMP review does not replace compliance with a separate supply-limit statute.",
                    "E": "Correct. Apply schedule consequences and opiate supply limits as separate legal dimensions."
                },
                "related_facts": ["A qualifying documented exception under § 19D(b) can permit a quantity greater than seven days."],
                "mpje_trap": "Do not assume that every opioid-related supply rule is limited to Schedule II drugs."
            },
            "reasoning_steps": [
                "Classify tramadol under controlled-substance law",
                "Separately identify the opiate seven-day statute",
                "Apply the adult first-outpatient trigger and look for a documented exception"
            ],
        },
    )

    save_question(
        "MA-Q-0075",
        updates={
            "stem": "A Massachusetts pharmacy technician trainee is performing data-entry work while a pharmacist is directly supervising the trainee. At pickup, the patient asks whether the new medication can be taken with warfarin, and the profile shows an unresolved DUR alert. Which actions are appropriate for the trainee? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Resolve the DUR alert independently because the computer generated the warning."},
                {"id": "B", "text": "Counsel the patient on the interaction after reading the drug-information screen."},
                {"id": "C", "text": "Perform final verification if the supervising pharmacist is busy."},
                {"id": "D", "text": "Continue only authorized clerical or technical trainee functions while under direct pharmacist supervision."},
                {"id": "E", "text": "Refer the clinical question and unresolved DUR issue to the pharmacist rather than exercising pharmacist professional judgment."},
            ],
            "correct_choice_ids": ["D", "E"],
            "explanation": {
                "core_reasoning": "A technician trainee may perform authorized technical/support functions only within the trainee supervision framework. Counseling, clinical DUR resolution, and final pharmacist verification require pharmacist-level professional judgment and are not delegated to the trainee.",
                "choice_analysis": {
                    "A": "Incorrect. A software alert does not turn clinical DUR resolution into a trainee function.",
                    "B": "Incorrect. Reading prepared information does not authorize a trainee to provide pharmacist counseling.",
                    "C": "Incorrect. Final verification is pharmacist professional judgment.",
                    "D": "Correct. The trainee may continue authorized technical work under direct pharmacist supervision.",
                    "E": "Correct. Clinical questions and unresolved DUR findings must be referred to the pharmacist."
                },
                "related_facts": ["Massachusetts distinguishes direct supervision requirements for trainees from broader supervision standards applicable to other technician categories."],
                "mpje_trap": "Do not treat registration as a technician trainee as authority to exercise pharmacist clinical judgment."
            },
            "reasoning_steps": [
                "Identify the worker as a technician trainee",
                "Apply the direct-supervision and technical-function boundary",
                "Separate technical support from counseling, DUR resolution, and final verification"
            ],
        },
    )

    save_question(
        "MA-Q-0076",
        updates={
            "stem": "A Massachusetts pharmacy is assigning staff to receive Schedule II stock. The pharmacist has approved written policies and procedures. Which statements correctly distinguish the current technician pathways? Select all that apply.",
            "choices": [
                {"id": "A", "text": "A registered pharmacy technician may assist with transporting Schedule II stock under pharmacist supervision."},
                {"id": "B", "text": "A registered pharmacy technician who is not certified may independently handle and reconcile Schedule II stock once the wholesaler delivery is signed."},
                {"id": "C", "text": "A certified pharmacy technician may assist with transporting and handling Schedule II stock under pharmacist supervision when the pharmacy's approved policies permit it."},
                {"id": "D", "text": "A pharmacy technician trainee may independently assume Schedule II accountability because trainee registration is enough to replace pharmacist oversight."},
                {"id": "E", "text": "The pharmacist remains responsible for Schedule II accountability, security, and professional judgment even when authorized support personnel assist."},
            ],
            "correct_choice_ids": ["A", "C", "E"],
            "explanation": {
                "core_reasoning": "Current Massachusetts technician rules distinguish ordinary registered technicians from certified technicians for Schedule II assistance. A technician may assist with transport; a certified technician may have the broader authorized transport-and-handling role under pharmacist supervision and pharmacy policy. Neither pathway transfers the pharmacist's accountability, security, or professional judgment duties.",
                "choice_analysis": {
                    "A": "Correct. The registered technician pathway permits Schedule II transport assistance under pharmacist supervision.",
                    "B": "Incorrect. Ordinary technician status does not create independent Schedule II handling/accountability authority.",
                    "C": "Correct. Certified-technician status supports the broader authorized transport-and-handling role subject to pharmacist supervision and pharmacy policy.",
                    "D": "Incorrect. Trainee registration does not replace the required pharmacist oversight or create independent Schedule II accountability.",
                    "E": "Correct. Support-personnel assistance does not transfer pharmacist responsibility for the controlled stock."
                },
                "related_facts": ["Credential category matters: trainee, registered technician, and certified technician are not interchangeable legal roles."],
                "mpje_trap": "Do not collapse every technician credential into one Schedule II scope rule."
            },
            "reasoning_steps": [
                "Identify each support-personnel credential",
                "Apply the Schedule II task boundary for that credential",
                "Preserve pharmacist accountability and professional-judgment responsibility"
            ],
        },
    )

    save_question(
        "MA-Q-0078",
        updates={
            "difficulty": 3,
            "stem": "A pharmacy student completes 12 hours of qualifying Massachusetts pharmacy-internship activity in one day. The student then remains at the site for a separate two-hour school seminar, and the preceptor proposes recording all 14 hours as Board internship credit. What should be recorded? Select all that apply.",
            "choices": [
                {"id": "A", "text": "All 14 hours may count if the preceptor signs the log."},
                {"id": "B", "text": "No more than 12 hours may be credited toward the pharmacy internship in one day."},
                {"id": "C", "text": "The extra two hours may automatically be carried forward as credit for the next day."},
                {"id": "D", "text": "The 12-hour credit ceiling applies to pharmacists but not to registered pharmacy interns."},
                {"id": "E", "text": "The separate seminar cannot increase that day's Board internship credit above the 12-hour maximum."},
            ],
            "correct_choice_ids": ["B", "E"],
            "explanation": {
                "core_reasoning": "The issue is pharmacy-internship credit, not permission to extend a work shift. Massachusetts limits pharmacy internship credit to no more than 12 hours in one day, so additional same-day activity cannot increase the Board credit beyond 12 hours.",
                "choice_analysis": {
                    "A": "Incorrect. Preceptor signature cannot waive the daily internship-credit ceiling.",
                    "B": "Correct. Twelve hours is the maximum pharmacy internship credit for one day.",
                    "C": "Incorrect. Same-day excess activity is not automatically shifted into the next day's credit.",
                    "D": "Incorrect. This rule specifically concerns pharmacy internship credit.",
                    "E": "Correct. The proposed extra seminar hours cannot push that day's internship credit above 12."
                },
                "related_facts": ["Separate practice-hour/rest rules should not be confused with the distinct internship-credit calculation tested here."],
                "mpje_trap": "Distinguish time physically spent at a site from hours legally creditable toward the pharmacy internship requirement."
            },
            "reasoning_steps": [
                "Identify that the question asks about internship credit",
                "Apply the 12-hour daily credit maximum",
                "Reject attempts to convert additional same-day activity into extra Board credit"
            ],
        },
    )

    save_question(
        "MA-Q-0081",
        updates={
            "stem": "A Massachusetts pharmacist is evaluating the current statutory qualifications to enter a collaborative practice agreement. Which statements reflect M.G.L. c.112, § 24B1/2(b)? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Hold a current Massachusetts pharmacist license, currently practice in the Commonwealth, and maintain at least $1,000,000 of professional liability insurance."},
                {"id": "B", "text": "Have earned a PharmD degree or completed five years of experience as a licensed pharmacist, or the equivalent."},
                {"id": "C", "text": "Devote a portion of practice to the defined drug-therapy area and complete at least five additional related CE contact hours in each agreement year."},
                {"id": "D", "text": "Apply for the statute's limited MassHealth ordering/referring participation if implementing regulations governing that participation are promulgated."},
                {"id": "E", "text": "A pharmacist with a current PharmD must also complete five years of licensed-practice experience because the degree alternative is no longer recognized by statute."},
            ],
            "correct_choice_ids": ["A", "B", "C", "D"],
            "explanation": {
                "core_reasoning": "The current statute lists licensure/current practice, $1 million liability coverage, a PharmD-or-five-years-or-equivalent qualification, therapy-area practice focus, five additional annual CE contact hours, and a conditional limited MassHealth participation application requirement. The statute does not state that every PharmD holder must also accumulate five years solely to satisfy subsection (b)(3).",
                "choice_analysis": {
                    "A": "Correct. These are express statutory baseline qualifications.",
                    "B": "Correct. The current statutory text uses an alternative: PharmD, five years of licensed experience, or equivalent.",
                    "C": "Correct. Practice focus and five additional related CE contact hours per agreement year are statutory requirements.",
                    "D": "Correct. The MassHealth limited-participation application duty is conditional on the implementing regulations described by the statute.",
                    "E": "Incorrect. It contradicts the current statutory PharmD-or-experience alternative."
                },
                "related_facts": ["Promulgated regulations can add operational requirements, but an exam item should not use older regulatory wording to erase an alternative expressly present in the current statute."],
                "mpje_trap": "Do not memorize an older grandfather formulation without checking the current statute."
            },
            "reasoning_steps": [
                "Read the current statutory qualification list",
                "Recognize the PharmD-or-five-years-or-equivalent structure",
                "Separate statutory baseline qualifications from other operational requirements of a particular agreement"
            ],
        },
    )

    save_question(
        "MA-Q-0085",
        updates={
            "area": 3,
            "stem": "Before dispensing a new prescription, a Massachusetts pharmacist's prospective review identifies a clinically significant interaction. Which actions are consistent with the current prospective drug-review duty? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Let a technician independently resolve the interaction if the dispensing software supplies a recommended override code."},
                {"id": "B", "text": "Skip prospective review because the prescriber sent the prescription electronically."},
                {"id": "C", "text": "Ensure the pharmacist conducts prospective drug review before the new prescription is dispensed or delivered."},
                {"id": "D", "text": "Automatically refuse every prescription that generates an alert without considering the specific problem or communicating when appropriate."},
                {"id": "E", "text": "Take appropriate measures to resolve an identified therapy problem, which may include consultation with the prescriber or patient and documentation of the measures taken."},
            ],
            "correct_choice_ids": ["C", "E"],
            "explanation": {
                "core_reasoning": "Massachusetts requires pharmacist prospective review before each new prescription is dispensed or delivered. When a potential therapy problem is identified, the pharmacist must use professional judgment and take appropriate measures to resolve it; electronic transmission and a software alert do not transfer that duty to a technician or make automatic refusal the only lawful response.",
                "choice_analysis": {
                    "A": "Incorrect. Clinical resolution of a DUR problem requires pharmacist professional judgment.",
                    "B": "Incorrect. Electronic prescribing does not remove the prospective-review requirement.",
                    "C": "Correct. The prospective review occurs before dispensing or delivery of a new prescription.",
                    "D": "Incorrect. The rule requires appropriate resolution, not automatic refusal of every alert.",
                    "E": "Correct. Appropriate resolution can involve prescriber/patient consultation and documentation of the action taken."
                },
                "related_facts": ["Potential problems include therapeutic duplication, contraindications, interactions, dosage or duration problems, allergies, and abuse or misuse."],
                "mpje_trap": "A computer alert is an input to pharmacist review, not a substitute for pharmacist judgment."
            },
            "reasoning_steps": [
                "Identify the prescription as new",
                "Apply the prospective-review timing requirement",
                "Use pharmacist judgment to resolve and document a clinically significant problem"
            ],
        },
    )

    save_question(
        "MA-Q-0086",
        updates={
            "stem": "At pickup of a new prescription, the pharmacist or designee makes the required offer to counsel and the patient declines. Which Massachusetts documentation statements are correct? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Reasonable efforts to obtain, record, and maintain patient information include recording a patient's failure to accept the pharmacist's offer to counsel."},
                {"id": "B", "text": "The refusal information may be recorded in the patient profile, prescription signature log, or another system of records."},
                {"id": "C", "text": "If there is no record that the patient failed to accept the offer, the statute creates a presumption that counseling was provided."},
                {"id": "D", "text": "A counseling refusal is valid only if the patient signs a notarized waiver."},
                {"id": "E", "text": "Because a designee may participate in making the offer, a technician may also provide the pharmacist counseling if the patient later changes their mind."},
            ],
            "correct_choice_ids": ["A", "B", "C"],
            "explanation": {
                "core_reasoning": "Massachusetts separates the offer to counsel from the record consequence when a patient declines. M.G.L. c.94C, § 21A requires reasonable efforts to record and maintain specified patient information including a failure to accept the offer, permits multiple record systems, and creates a presumption that counseling was provided when no refusal is recorded. A designee's role in making the offer does not transfer pharmacist counseling authority to a technician.",
                "choice_analysis": {
                    "A": "Correct. Failure to accept the offer is expressly included in the patient information the pharmacy should reasonably attempt to record and maintain.",
                    "B": "Correct. The statute permits the profile, signature log, or another record system.",
                    "C": "Correct. Absence of a recorded failure to accept creates the statutory presumption that counseling was provided.",
                    "D": "Incorrect. The statute does not require a notarized waiver.",
                    "E": "Incorrect. Authority to participate in the offer does not make a technician the pharmacist who provides counseling."
                },
                "related_facts": ["A patient may decline counseling; the documentation consequence is a separate legal issue from whether the offer was made."],
                "mpje_trap": "Do not confuse 'designee may make the offer' with 'designee may perform pharmacist counseling,' and do not overlook the refusal-record presumption."
            },
            "rule_ids": ["MA-COUNSELING", "MA-COUNSELING-DOCUMENTATION"],
            "reasoning_steps": [
                "Identify that an offer was made and declined",
                "Apply the statutory refusal-documentation rule",
                "Distinguish offer delegation from authority to perform counseling"
            ],
        },
    )

    save_question(
        "MA-Q-0087",
        updates={
            "area": 4,
            "stem": "A less expensive drug product is reasonably available and appears on the Massachusetts interchangeable-drug list, but the prescription contains a valid prescriber no-substitution direction. Which statements correctly describe the product-selection decision? Select all that apply.",
            "choices": [
                {"id": "A", "text": "The valid no-substitution direction prevents the pharmacist from applying the usual required interchange on this prescription."},
                {"id": "B", "text": "The lower price automatically overrides a valid no-substitution direction."},
                {"id": "C", "text": "Without a valid no-substitution direction, the Massachusetts interchange framework generally requires use of the reasonably available, less expensive interchangeable product when its conditions are met."},
                {"id": "D", "text": "The patient may erase the prescriber's valid no-substitution direction and compel interchange without prescriber involvement."},
                {"id": "E", "text": "A pharmacist must ignore the Massachusetts interchangeable-drug list whenever the brand product is in stock."},
            ],
            "correct_choice_ids": ["A", "C"],
            "explanation": {
                "core_reasoning": "Massachusetts product selection depends on both interchange eligibility and the prescriber's substitution direction. A valid no-substitution instruction blocks the otherwise applicable interchange rule; absent that instruction, the interchangeable-list and lower-price/reasonable-availability conditions control.",
                "choice_analysis": {
                    "A": "Correct. A valid prescriber no-substitution direction is a controlling exception to interchange.",
                    "B": "Incorrect. Lower price does not nullify a valid no-substitution instruction.",
                    "C": "Correct. In the absence of a valid no-substitution instruction, the statutory interchange conditions apply.",
                    "D": "Incorrect. The patient cannot simply erase the prescriber's valid direction and convert it into a substitution-authorized prescription.",
                    "E": "Incorrect. Stocking the brand does not eliminate the statutory product-selection framework."
                },
                "related_facts": ["Product-selection law belongs to the NABP Area-4 practice-operations competency rather than prescription-transfer/dispensing mechanics."],
                "mpje_trap": "Do not let price or inventory status override a valid prescriber no-substitution direction."
            },
            "reasoning_steps": [
                "Confirm that the alternative is legally interchangeable",
                "Check price and reasonable availability",
                "Apply the prescriber's substitution direction before selecting the product"
            ],
        },
    )

    save_question(
        "MA-Q-0088",
        updates={
            "area": 2,
            "stem": "A patient returns an unopened bottle that a Massachusetts pharmacy dispensed in error. The product appears intact. Which actions are required or permitted for the returned medication? Select all that apply.",
            "choices": [
                {"id": "A", "text": "Accept the return because it was previously dispensed in error by the pharmacy."},
                {"id": "B", "text": "Do not place the returned medication back into dispensing inventory merely because the container is unopened."},
                {"id": "C", "text": "Segregate or quarantine the returned medication and handle its disposition under the pharmacy's required return/disposal process."},
                {"id": "D", "text": "Return the product directly to active inventory if the patient states it was stored properly."},
                {"id": "E", "text": "Dispense the returned bottle to another patient after a pharmacist visually inspects the seal."},
            ],
            "correct_choice_ids": ["A", "B", "C"],
            "explanation": {
                "core_reasoning": "Massachusetts requires a pharmacy to accept medication that it previously dispensed in error (or that is suspected defective/contaminated), but the return does not make the product reusable inventory. The medication must be segregated/quarantined and handled through the required disposition process rather than redispensed to another patient.",
                "choice_analysis": {
                    "A": "Correct. A pharmacy-dispensing error is a recognized return trigger.",
                    "B": "Correct. An unopened appearance does not restore a patient-returned product to active dispensing inventory.",
                    "C": "Correct. Returned medication must be segregated from usable stock and managed for proper disposition.",
                    "D": "Incorrect. Patient assurance about storage does not authorize return to active inventory.",
                    "E": "Incorrect. Visual inspection does not authorize redispensing the returned medication to another patient."
                },
                "related_facts": ["The rule protects patients by separating correction of an erroneous dispense from reuse of medication after it has left pharmacy control."],
                "mpje_trap": "Do not infer 'unopened' means 'returnable to stock' once the medication has been dispensed to a patient."
            },
            "reasoning_steps": [
                "Identify why the medication is being returned",
                "Separate the duty to accept the return from the question of reuse",
                "Quarantine/segregate and follow the required disposition process"
            ],
        },
    )

    update_taxonomy_families()

    # Record all editor decisions without claiming independent audit status.
    report = {
        "program": "PRE_BATCH3_COVERAGE_REMEDIATION",
        "tranche": "LEGACY_SALVAGE_T1",
        "editor_review_date": TODAY,
        "review_status": "EDITOR_REPAIR_COMPLETE_PENDING_QA_FREEZE_AND_FRESH_INDEPENDENT_AUDIT",
        "independent_audit": False,
        "repair_count": len(REPAIR_IDS),
        "keep_count": len(KEEP_IDS),
        "repair_ids": sorted(REPAIR_IDS),
        "keep_ids": sorted(KEEP_IDS),
        "material_editor_findings": {
            "MA-Q-0081": "Repaired to current M.G.L. c.112 §24B1/2(b); removed the outdated pre-July-2017 PharmD grandfather formulation from the keyed answer.",
            "MA-Q-0086": "Repaired to directly test M.G.L. c.94C §21A counseling-refusal documentation and presumption, creating a legacy candidate for atomic competency 2.3b.",
            "MA-Q-0085": "Repaired for stronger professional-judgment distractors and formally moved from Area 2 to NABP Area 3 (prospective DUR).",
            "MA-Q-0087": "Formally moved from Area 3 to NABP Area 4 (product selection/interchange).",
            "MA-Q-0088": "Formally moved from Area 4 to NABP Area 2 (return/reuse of drugs).",
            "MA-Q-0075": "Clarified technician-trainee direct-supervision and professional-judgment boundaries.",
            "MA-Q-0076": "Rewritten to distinguish registered technician vs certified-technician Schedule II support pathways.",
            "MA-Q-0015/0016/0017/0040": "Diversified four seven-day-opiate items into OUD exclusion, documented adult exception, minor-at-any-time trigger, and tramadol schedule-vs-opiate reasoning pathways."
        },
        "official_sources_checked": [
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21A",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24G",
            "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians",
            "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
            "https://www.deadiversion.usdoj.gov/faq/epcs-faq.html",
            "https://www.ecfr.gov/current/title-21/chapter-II/part-1306",
            "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
        ],
        "boundary": "This editor review may repair canonical AUDIT_PENDING legacy content but may not certify independent LEGAL/REALISM audit results or promote any question to RELEASED."
    }
    write_json(ROOT / "audits" / "remediation" / "2026-08-17" / "T1-EDITOR-REVIEW.json", report)

    print(f"T1 editor repair applied: repaired={len(REPAIR_IDS)} kept={len(KEEP_IDS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Apply the seven minimum repairs required after the Batch 3 measured deficits.

The script is intentionally narrow and fail-closed. It repairs exactly four Area-2
questions and the three Area-4 questions withdrawn for the confirmed compliance-
packaging conflict. It does not release or self-audit any question.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, question_audit_hash, semantic_content_hash, write_json


REPAIR_DATE = "2026-08-20"
SOURCE_MAIN_SHA = "71e09d47395229572731c92d7230ef7f41c24023"
RULE_ID = "MA-COMPLIANCE-PACKAGING"
OLD_RULE_HASH = "ba79ae42fa51d3af30f7a4aa109233a07c127cbd83334bcd7247db0c25ef55d1"
EXPECTED_OLD_HASHES = {
    "MA-Q-0169": "505770da1a192bc506905b2fe88ac8e6ac5425c8d04565c7d2d144cc25120539",
    "MA-Q-0202": "a3c658d418f93ee9174a51fe68151bd47738fb529912efe5963be6169bca289a",
    "MA-Q-0203": "a5f2a0ac6bcbc1296c833f40d80ff7cfd219f328611f0d3253227f72f8d81acd",
    "MA-Q-0340": "d5ec12834f5c57ae2eb13ae5773dd4a0efd88370ef9233d7996d8174b8636855",
    "MA-Q-0348": "0c48c9c7f786dc09647012636911b77594f81607ca70d07c540c4fbfe988e878",
    "MA-Q-0350": "e2b745c2f9caef63b749f1c26ef4cbf2e9993595f57495029f46adf4281dc5e6",
    "MA-Q-0359": "c57a7ed1e6f0d10466a9a3176bffcbff4f149688934110638dfb53db92353a14",
}


REPAIRS = {
    "MA-Q-0169": {
        "family_id": "B2_COMPLIANCE_MULTI_DRUG_SII_III_PROHIBITION",
        "subtopic": "Schedule II/III multi-drug-single-dose prohibition",
        "stem": (
            "A Massachusetts pharmacy is deciding how to package several daily medications for one patient. "
            "Which statements correctly apply the Schedule II/III rule? Select all that apply."
        ),
        "choices": [
            ("A", "A stable maintenance classification permits a Schedule II drug to share a multi-drug single-dose pouch."),
            ("B", "A licensee may not dispense a Schedule II or III controlled substance in a multi-drug single-dose package."),
            ("C", "That prohibition does not by its own terms ban a single-drug single-dose package."),
            ("D", "Every form of compliance packaging is prohibited for every Schedule II or III controlled substance."),
            ("E", "The policy phrase 'unless otherwise prohibited' preserves the regulatory Schedule II/III restriction."),
        ],
        "correct_choice_ids": ["B", "C", "E"],
        "core_reasoning": (
            "247 CMR 9.08(3)(b) prohibits a licensee from dispensing Schedule II or III controlled substances "
            "in a multi-drug-single-dose package. Maintenance status does not create an exception. The text is "
            "specific to multi-drug-single-dose packaging, so it must not be expanded into a ban on every form "
            "of compliance packaging. Current Policy 2023-01 begins its multi-drug section with 'Unless otherwise "
            "prohibited' and therefore preserves the regulation rather than overriding it."
        ),
        "choice_analysis": {
            "A": "Maintenance status does not override 247 CMR 9.08(3)(b).",
            "B": "Correct: this is the express Schedule II/III multi-drug-single-dose prohibition.",
            "C": "Correct: the cited clause is drawn by packaging type and does not itself reach single-drug-single-dose packaging.",
            "D": "This overgeneralizes a packaging-specific prohibition.",
            "E": "Correct: the policy does not displace an otherwise applicable regulatory prohibition.",
        },
        "related_facts": ["Other compatibility, labeling, policy and procedure requirements continue to apply."],
        "mpje_trap": "Turning a precise multi-drug-single-dose prohibition into either a maintenance exception or a universal packaging ban.",
        "reasoning_steps": [
            "Identify the controlled-substance schedule",
            "Identify whether the proposed package is multi-drug-single-dose",
            "Apply the prohibition without expanding it to a different packaging type",
        ],
    },
    "MA-Q-0202": {
        "family_id": "B2_DRUG_PACKAGING_TYPE_SCHEDULE_MATRIX",
        "subtopic": "Packaging type and controlled-substance schedule matrix",
        "stem": (
            "A Massachusetts pharmacy is redesigning one patient's compliance packaging. Assuming all other "
            "requirements are satisfied, which proposed placements are not prohibited by 247 CMR 9.08(3)(b)? "
            "Select all that apply."
        ),
        "choices": [
            ("A", "Place stable Schedule III buprenorphine in the same multi-drug single-dose pouch as the patient's other morning medications."),
            ("B", "Keep Schedule II methylphenidate in a separate single-drug single-dose package rather than the patient's multi-drug pouch."),
            ("C", "Place Schedule IV alprazolam in a multi-drug single-dose package after confirming the other packaging requirements."),
            ("D", "Place stable Schedule III testosterone in a multi-drug single-dose pouch because maintenance status creates an exception."),
            ("E", "Keep Schedule II oxycodone in a separate single-drug single-dose package rather than combining it with other medications."),
        ],
        "correct_choice_ids": ["B", "C", "E"],
        "core_reasoning": (
            "247 CMR 9.08(3)(b) bars Schedule II and III controlled substances from multi-drug-single-dose "
            "packages. It does not create a maintenance exception, does not name Schedule IV, and does not by "
            "its own terms prohibit single-drug-single-dose packaging. The question assumes the remaining "
            "compatibility, labeling and policy requirements are met."
        ),
        "choice_analysis": {
            "A": "Schedule III remains prohibited in a multi-drug-single-dose package.",
            "B": "Correct: the cited prohibition does not itself reach a separate single-drug-single-dose package.",
            "C": "Correct under the stated assumption: Schedule IV is outside the Schedule II/III prohibition.",
            "D": "Maintenance status supplies no exception for Schedule III in a multi-drug package.",
            "E": "Correct: keeping the Schedule II drug in a separate single-drug package avoids the specific multi-drug prohibition.",
        },
        "related_facts": ["A placement not prohibited by paragraph (3)(b) must still satisfy every other applicable requirement."],
        "mpje_trap": "Classifying only the drug schedule and ignoring the packaging type that defines the prohibition.",
        "reasoning_steps": [
            "Classify each drug's schedule",
            "Distinguish multi-drug-single-dose from single-drug-single-dose packaging",
            "Apply the Schedule II/III prohibition and preserve all other requirements",
        ],
    },
    "MA-Q-0203": {
        "family_id": "B2_DRUG_MULTI_DRUG_SIII_EXCLUSION",
        "subtopic": "Schedule III multi-drug-single-dose exclusion",
        "stem": (
            "A patient receives stable Schedule III buprenorphine therapy. The pharmacy proposes to combine each "
            "dose in a multi-drug single-dose pouch with the patient's other morning medications. May maintenance "
            "status justify that placement?"
        ),
        "choices": [
            ("A", "Yes, because a stable maintenance regimen overrides the controlled-substance packaging restriction."),
            ("B", "No; Schedule III drugs may not enter a multi-drug single-dose package under 247 CMR 9.08(3)(b)."),
            ("C", "No, because every controlled substance is prohibited from every form of compliance packaging."),
            ("D", "Yes, if the patient signs a written consent to combine the medications."),
            ("E", "Yes, if the pharmacy limits the package to a 60-day supply."),
        ],
        "correct_choice_ids": ["B"],
        "core_reasoning": (
            "247 CMR 9.08(3)(b) prohibits Schedule II and III controlled substances in a multi-drug-single-dose "
            "package. Buprenorphine's Schedule III status decides this proposal; maintenance status, consent and "
            "a 60-day limit do not create an exception. The rule should not be generalized into a ban on all "
            "controlled substances or every compliance-packaging format."
        ),
        "choice_analysis": {
            "A": "Maintenance status does not override the express Schedule III prohibition.",
            "B": "Correct: Schedule III may not be dispensed in the proposed multi-drug-single-dose pouch.",
            "C": "This overstates both the schedules and packaging types covered by the cited clause.",
            "D": "Patient consent cannot waive the regulatory prohibition.",
            "E": "A duration limit does not create an exception for Schedule III.",
        },
        "related_facts": ["The prohibition is specific to Schedule II/III drugs and multi-drug-single-dose packaging."],
        "mpje_trap": "Importing the policy's 60-day concept into a separate categorical controlled-substance prohibition.",
        "reasoning_steps": [
            "Identify buprenorphine as Schedule III",
            "Identify the proposal as multi-drug-single-dose packaging",
            "Reject conditions that do not create an exception to paragraph (3)(b)",
        ],
    },
    "MA-Q-0340": {
        "stem": (
            "A Massachusetts pharmacist practising collaboratively in a retail drug business is reviewing what the "
            "statute permits her to do there. Which statements are correct? Select all that apply."
        ),
        "choices": [
            ("A", "Patients must be 18 years of age or older in that setting."),
            ("B", "She may initiate a new Schedule II therapy whenever the referral identifies the diagnosis."),
            ("C", "She may extend current therapy prescribed by the supervising physician by 30 days."),
            ("D", "She may modify dosages of any medication the patient is currently taking."),
            ("E", "She may administer vaccines under the terms of her agreement."),
        ],
        "correct_choice_ids": ["A", "C", "E"],
        "core_reasoning": (
            "M.G.L. c. 112, s. 24B1/2(c)(5) limits retail collaborative practice to patients age 18 or older, "
            "permits a 30-day extension of current therapy prescribed by the supervising physician, and includes "
            "vaccine administration under the collaborative agreement. It bars Schedule II through V prescribing "
            "in the retail agreement and limits dosage modification to medications prescribed by the supervising "
            "physician for the named disease states."
        ),
        "choice_analysis": {
            "A": "Correct: the retail setting carries an age floor of 18.",
            "B": "Retail collaborative prescribing may not include Schedule II through V controlled substances.",
            "C": "Correct: the pharmacist may extend the supervising physician's current therapy by 30 days.",
            "D": "The dosage-modification power is limited to the supervising physician's medications for the named conditions.",
            "E": "Correct: vaccine administration is an authorized retail collaborative power under the agreement.",
        },
        "related_facts": ["An agreement that specifically allows initial prescriptions may authorize Schedule VI prescriptions for referred patients."],
        "mpje_trap": "Applying the disease-state qualifier to the vaccine limb or ignoring the Schedule II-V prescribing bar.",
        "reasoning_steps": [
            "Apply the retail age floor",
            "Separate continuation and vaccine powers from controlled-substance prescribing",
            "Keep dosage modification within the supervising physician and named-condition limits",
        ],
    },
    "MA-Q-0348": {
        "stem": (
            "A Massachusetts pharmacy proposes to run a walk-in clinic for a newly designated vaccine during a public "
            "health event. Which statements about what must be in place are correct? Select all that apply."
        ),
        "choices": [
            ("A", "A practitioner standing prescription alone opens this pathway."),
            ("B", "The Commissioner must determine that health care professionals will be insufficient."),
            ("C", "A Commissioner order authorizing the administration removes any need for a prescription."),
            ("D", "Administration must accord with the Commissioner's order as well as a practitioner instrument."),
            ("E", "A designation of the vaccine by the Commissioner is required."),
        ],
        "correct_choice_ids": ["B", "D", "E"],
        "core_reasoning": (
            "105 CMR 700.003(F)(1) requires a vaccine designated by the Commissioner, the Commissioner's "
            "determination that qualified professionals are or will be insufficient, an authorizing Commissioner "
            "order, and administration in accordance with that order and an order or prescription from a duly "
            "registered practitioner. Neither instrument displaces the other conditions."
        ),
        "choice_analysis": {
            "A": "A practitioner instrument alone does not supply the designation, insufficiency determination and Commissioner order.",
            "B": "Correct: the insufficiency determination is a stated condition.",
            "C": "The Commissioner order does not displace the practitioner order or prescription.",
            "D": "Correct: administration must accord with both the Commissioner order and the practitioner instrument.",
            "E": "Correct: the vaccine must be designated by the Commissioner.",
        },
        "related_facts": ["An enrolled student may act only when authorized and supervised by a licensed qualified professional."],
        "mpje_trap": "Treating either the practitioner instrument or the Commissioner order as a single switch that opens the pathway.",
        "reasoning_steps": [
            "Identify the designation and insufficiency determination",
            "Require the Commissioner order",
            "Keep the practitioner order or prescription as a separate cumulative condition",
        ],
    },
    "MA-Q-0350": {
        "stem": (
            "A Massachusetts pharmacy operating under a Commissioner vaccine order is revising its written protocols. "
            "It already covers training and adverse-event response. Which proposed decisions correctly identify "
            "additional protocol subjects that 105 CMR 700.003(F)(2)(b) expressly requires? Select all that apply."
        ),
        "choices": [
            ("A", "Retain procedures for proper storage even when vaccine arrives directly from the distributor."),
            ("B", "Add a regulation-mandated written-consent protocol before every administered dose."),
            ("C", "Retain procedures for return of vaccine even if unused doses are uncommon."),
            ("D", "Add a regulation-mandated rule to report every dose to the immunization registry within 24 hours."),
            ("E", "Retain recordkeeping procedures for vaccine administration."),
        ],
        "correct_choice_ids": ["A", "C", "E"],
        "core_reasoning": (
            "105 CMR 700.003(F)(2)(b) requires written protocols addressing proper storage, handling and return "
            "of vaccine, recordkeeping regarding administration, response to adverse events, and safe and appropriate "
            "administration. The stated paragraph does not add the specific written-consent or 24-hour registry "
            "reporting mandates used as distractors."
        ),
        "choice_analysis": {
            "A": "Correct: proper storage remains an express protocol subject.",
            "B": "The paragraph does not impose this specific written-consent protocol requirement.",
            "C": "Correct: return of vaccine is expressly named and is not excused by infrequent use.",
            "D": "The paragraph does not state this specific 24-hour registry-reporting protocol requirement.",
            "E": "Correct: recordkeeping regarding administration is expressly named.",
        },
        "related_facts": ["Proper training, supervision and adverse-event response also remain part of the pathway."],
        "mpje_trap": "Dropping an express protocol subject because the pharmacy expects the relevant event to be rare.",
        "reasoning_steps": [
            "Separate the subjects already covered from the remaining protocol duties",
            "Test each proposed subject against the express paragraph",
            "Do not infer that operational rarity removes a named protocol subject",
        ],
    },
    "MA-Q-0359": {
        "stem": (
            "A Massachusetts pharmacist is asked in one shift to administer a long-acting injectable antipsychotic, "
            "testosterone for gender-affirming care, and an antibiotic for a sexually transmitted infection. Which "
            "statements about the statutory basis for each are correct? Select all that apply."
        ),
        "choices": [
            ("A", "All three rest on the same statutory clause and share the same conditions."),
            ("B", "The antipsychotic route requires the direction of a prescribing practitioner."),
            ("C", "The antipsychotic route additionally requires departmental regulations."),
            ("D", "The testosterone route rests on a prescription for that purpose."),
            ("E", "The sexually transmitted-infection route additionally requires the departmental regulations that govern the mental-health route."),
        ],
        "correct_choice_ids": ["B", "C", "D"],
        "core_reasoning": (
            "Clause (c) of the definition of Administer creates three differently gated pharmacist routes. "
            "Mental-health and substance-use-disorder medication administration requires both departmental "
            "regulations and direction from a prescribing practitioner. Gender-affirming testosterone rests on "
            "a prescription for that purpose. The sexually transmitted-infection route rests on its own "
            "prescription clause and does not import the regulations attached to the mental-health route."
        ),
        "choice_analysis": {
            "A": "The three routes occupy different subclauses and do not share one condition set.",
            "B": "Correct: practitioner direction is part of the mental-health route.",
            "C": "Correct: departmental regulations are an additional gate for that route.",
            "D": "Correct: a prescription for gender-affirming testosterone supports that route.",
            "E": "The STI route does not import the regulations assigned to the mental-health route.",
        },
        "related_facts": ["The STI clause also reaches prescriptions for prevention of HIV."],
        "mpje_trap": "Carrying the regulation gate from the mental-health subclause into the two prescription-based subclauses.",
        "reasoning_steps": [
            "Split clause (c) into its three subclauses",
            "Assign the regulation and direction gates only to the mental-health route",
            "Keep the two prescription-based routes separate",
        ],
    },
}


def choices(rows: list[tuple[str, str]]) -> list[dict]:
    return [{"id": choice_id, "text": text} for choice_id, text in rows]


def reset_pending(question: dict) -> None:
    question["verification_status"] = "AUDIT_PENDING"
    question["lifecycle_status"] = "AUDIT_PENDING"
    question["last_legal_review"] = REPAIR_DATE
    question["audits"] = []
    question["duplicate_review_status"] = "PENDING"
    question["independent_audit_status"] = "PENDING"
    question["final_adjudication"] = None
    question["development_fixture"] = True


def main() -> int:
    before: dict[str, str] = {}
    for question_id, expected_hash in EXPECTED_OLD_HASHES.items():
        path = DATA / "questions" / f"{question_id.lower()}.json"
        question = load_json(path)
        current_hash = question_audit_hash(question)
        if current_hash != expected_hash:
            raise SystemExit(f"{question_id}: expected {expected_hash}, found {current_hash}")
        before[question_id] = current_hash

    rule_path = DATA / "rules" / "ma-compliance-packaging.json"
    rule = load_json(rule_path)
    if rule.get("content_hash") != OLD_RULE_HASH:
        raise SystemExit(f"{RULE_ID}: expected {OLD_RULE_HASH}, found {rule.get('content_hash')}")
    rule.update({
        "content_version": 2,
        "title": "Schedule II/III multi-drug-single-dose prohibition",
        "subtopic": "Schedule II/III multi-drug-single-dose prohibition",
        "rule_summary": (
            "A licensee may not dispense Schedule II or III controlled substances in a multi-drug-single-dose "
            "package. Maintenance status does not create an exception. The prohibition is specific to that "
            "packaging type and does not by itself prohibit single-drug-single-dose packaging; every other "
            "applicable packaging, labeling, compatibility and dispensing requirement still applies."
        ),
        "exam_relevance": "Tests schedule and packaging-type classification without inventing a maintenance exception or a universal packaging ban.",
        "authority": [
            {
                "type": "PROMULGATED_REGULATION",
                "name": "Massachusetts Board of Registration in Pharmacy regulations",
                "section": "247 CMR 9.08(3)(b), Mass. Register #1536 (12/06/2024)",
                "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
            },
            {
                "type": "BOARD_POLICY",
                "name": "Policy 2023-01: Compliance Packaging and Reusable Dose Planners",
                "section": "Multi-Drug-Single-Dose Packaging (revised 01/09/2025)",
                "url": "https://www.mass.gov/lists/pharmacy-practice-resources",
            },
        ],
        "last_verified": REPAIR_DATE,
        "exceptions": [],
        "common_confusions": [
            "Treating maintenance status as an exception to the Schedule II/III prohibition.",
            "Expanding a multi-drug-single-dose prohibition into a ban on every form of compliance packaging.",
            "Reading 'Unless otherwise prohibited' in Policy 2023-01 as displacing the regulation rather than preserving it.",
        ],
        "related_rule_ids": ["MA-COMPLIANCE-PACKAGING-STANDARDS"],
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": (
            "Controller-authored repair after independent current-hash defect confirmation by "
            "GPT-FRESH-B3-PACKAGING-CONFLICT-V1. Must receive fresh independent legal and realism evidence "
            "at the changed question and rule hashes before release."
        ),
    })
    rule["content_hash"] = semantic_content_hash(rule, "rule")
    write_json(rule_path, rule)

    after: dict[str, str] = {}
    for question_id, repair in REPAIRS.items():
        path = DATA / "questions" / f"{question_id.lower()}.json"
        question = load_json(path)
        for field in ("family_id", "subtopic", "stem"):
            if field in repair:
                question[field] = repair[field]
        question["choices"] = choices(repair["choices"])
        question["correct_choice_ids"] = repair["correct_choice_ids"]
        question["explanation"] = {
            "core_reasoning": repair["core_reasoning"],
            "choice_analysis": repair["choice_analysis"],
            "related_facts": repair["related_facts"],
            "mpje_trap": repair["mpje_trap"],
        }
        question["reasoning_steps"] = repair["reasoning_steps"]
        reset_pending(question)
        write_json(path, question)
        after[question_id] = question_audit_hash(question)
        if after[question_id] == before[question_id]:
            raise SystemExit(f"{question_id}: repair did not change question_audit_hash")

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    family_updates = {
        "B2_COMPLIANCE_MAINTENANCE": (
            "B2_COMPLIANCE_MULTI_DRUG_SII_III_PROHIBITION",
            "Schedule II/III multi-drug-single-dose prohibition",
        ),
        "B2_DRUG_COMPLIANCE_MAINTENANCE": (
            "B2_DRUG_PACKAGING_TYPE_SCHEDULE_MATRIX",
            "Packaging type and controlled-substance schedule matrix",
        ),
        "B2_DRUG_COMPLIANCE_ACUTE_OXY": (
            "B2_DRUG_MULTI_DRUG_SIII_EXCLUSION",
            "Schedule III multi-drug-single-dose exclusion",
        ),
    }
    seen = set()
    for family in matrix["families"]:
        if family["family_id"] in family_updates:
            old_id = family["family_id"]
            family["family_id"], family["subtopic"] = family_updates[old_id]
            seen.add(old_id)
    if seen != set(family_updates):
        raise SystemExit(f"family matrix update mismatch: {sorted(seen)}")
    write_json(matrix_path, matrix)

    report = {
        "record_id": "BATCH3-MINIMUM-DEFICIT-REPAIRS",
        "recorded_by": "GPT_DESKTOP_CONTROLLER_AUTHOR_NOT_AUDITOR",
        "recorded_on": REPAIR_DATE,
        "controller_issue": 83,
        "authorizing_issue": 91,
        "source_main_sha": SOURCE_MAIN_SHA,
        "measured_before": {"released_total": 359, "area_1": 78, "area_2": 116, "area_3": 93, "area_4": 72},
        "minimums": {"released_total": 360, "area_1": 78, "area_2": 120, "area_3": 87, "area_4": 75},
        "selected_area_2": ["MA-Q-0340", "MA-Q-0348", "MA-Q-0350", "MA-Q-0359"],
        "selected_area_4": ["MA-Q-0169", "MA-Q-0202", "MA-Q-0203"],
        "selection_reason": (
            "Exactly four Area-2 and three Area-4 questions are required. The four B3-D items admit narrow "
            "corrections identified by their independent audit, while the three Area-4 items are the exact "
            "questions withdrawn for the confirmed packaging conflict. No surplus question was repaired."
        ),
        "old_question_hashes": before,
        "new_question_hashes": after,
        "rule_hash": {"before": OLD_RULE_HASH, "after": rule["content_hash"]},
        "release_status": "NOT_RELEASED_PENDING_FRESH_INDEPENDENT_REAUDIT",
        "self_audit_performed": False,
        "official_sources": [
            "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
            "https://www.mass.gov/lists/pharmacy-practice-resources",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B%201~2",
            "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c",
            "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section1",
        ],
    }
    write_json(ROOT / "audits/remediation/2026-08-20/BATCH3-MINIMUM-DEFICIT-REPAIRS.json", report)

    print(json.dumps({"question_hashes": after, "rule_hash": rule["content_hash"]}, indent=2))
    print("release status: NOT_RELEASED_PENDING_FRESH_INDEPENDENT_REAUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

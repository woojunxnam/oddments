"""Author the Pre-Batch3 T3 diversity remediation candidates MA-Q-0227 and MA-Q-0228.

Issue #86. The measured gate deficit is headline family diversity, not atomic coverage:
headline 4.3 (Delivery of drugs) rests only on family T2_0215_MA_DRUG_DELIVERY and
headline 4.6 (Central fill) rests only on family T2_0220_MA_CENTRAL_FILL. Each new item
therefore has to test a genuinely different decision path in a new family.

MA-Q-0227 leaves the 247 CMR 9.02 mail/common-carrier integrity duty that MA-Q-0215
already tests and instead tests 247 CMR 9.04(4), the bed-side discharge-delivery rule.
MA-Q-0228 leaves the Policy 2021-02 ownership/written-agreement structure that
MA-Q-0220 already tests and instead tests the policy's central-fill destination,
licensure and scope limits.

Two new canonical rules are required. The existing MA-DRUG-DELIVERY-SHIPPING and
MA-SHARED-PHARMACY-SERVICES records state different propositions and are frozen into
the released MA-Q-0215 / MA-Q-0220 dependency snapshots, so they must not be edited.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, load_json, semantic_content_hash, write_json


AUTHORING_DATE = "2026-08-19"

RULES = [
    {
        "rule_id": "MA-BEDSIDE-DELIVERY",
        "content_version": 1,
        "content_hash": "",
        "title": "Bed-side delivery of discharge prescriptions",
        "jurisdiction": "MA",
        "area": 4,
        "topic": "Pharmacy operations",
        "subtopic": "Bed-side delivery of discharge prescriptions",
        "rule_summary": (
            "Under 247 CMR 9.04(4), a pharmacy that provides bed-side delivery service of discharge "
            "prescriptions to patients in an inpatient healthcare facility must obtain patient consent to "
            "provide such services and may not restrict a patient's freedom of choice of pharmacy services. "
            "A pharmacy that provides bed-side delivery service shall deliver any medications directly to "
            "the patient or the patient's agent."
        ),
        "exam_relevance": (
            "Tests who may lawfully receive a bed-side discharge delivery, which is a different duty from "
            "the mail and common-carrier packing and stability duty in 247 CMR 9.02."
        ),
        "authority": [
            {
                "type": "PROMULGATED_REGULATION",
                "name": "Massachusetts professional practice standards",
                "section": "247 CMR 9.04(4)",
                "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
            }
        ],
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": AUTHORING_DATE,
        "numeric_facts": [],
        "exceptions": [],
        "common_confusions": [
            "Consent to a bed-side delivery program does not authorize handing the medications to facility staff.",
            "Bed-side delivery is a separate provision from the 247 CMR 9.02 rules on prescriptions by mail.",
        ],
        "related_rule_ids": ["MA-DRUG-DELIVERY-SHIPPING"],
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": (
            "247 CMR 9.04(4) read in the current official Board of Registration in Pharmacy publication of "
            "247 CMR 9.00 on 2026-08-19 during Pre-Batch3 T3 authoring under Issue #86. A fresh independent "
            "legal and full-bank realism audit is still required before release."
        ),
    },
    {
        "rule_id": "MA-CENTRAL-FILL-DISPENSING-ROUTE",
        "content_version": 1,
        "content_hash": "",
        "title": "Central fill destination, licensure and scope limits",
        "jurisdiction": "MA",
        "area": 4,
        "topic": "Shared pharmacy services",
        "subtopic": "Central fill dispensing routing",
        "rule_summary": (
            "Board Policy 2021-02 limits where a centrally filled prescription may go and what a central "
            "fill pharmacy may prepare. Centrally filled Schedule II through V controlled substances must be "
            "delivered to the pharmacy where the prescription originated for final dispensing to the patient. "
            "Centrally filled Schedule VI controlled substances may be delivered or shipped directly to the "
            "patient from the central fill pharmacy, except for drugs that require Prescription Monitoring "
            "Program reporting. Any central fill pharmacy dispensing into, within, or from Massachusetts must "
            "itself be licensed by Massachusetts as a resident or non-resident retail pharmacy, and central "
            "filling of compounded sterile preparations or complex non-sterile preparations to be dispensed "
            "into, within, or from Massachusetts is prohibited."
        ),
        "exam_relevance": (
            "Tests the destination, licensure and scope limits of a central-fill workflow, which are separate "
            "from the ownership or written-agreement structure that authorizes the arrangement in the first place."
        ),
        "authority": [
            {
                "type": "BOARD_POLICY",
                "name": "Shared Pharmacy Service Models Including Central Fill, Remote Processing, and Telepharmacy",
                "section": "Policy 2021-02, section IV",
                "url": "https://www.mass.gov/lists/pharmacy-practice-resources",
            }
        ],
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": AUTHORING_DATE,
        "numeric_facts": [],
        "exceptions": [
            "Centrally filled Schedule VI drugs that require Prescription Monitoring Program reporting may "
            "not be shipped directly to the patient from the central fill pharmacy."
        ],
        "common_confusions": [
            "A compliant written shared-services agreement does not by itself permit direct patient shipment "
            "of a centrally filled federally scheduled prescription.",
            "Schedule VI status is not a blanket direct-shipment permission because monitoring-program "
            "reportable drugs are carved out.",
        ],
        "related_rule_ids": ["MA-SHARED-PHARMACY-SERVICES"],
        "verification_status": "OFFICIAL_POLICY_VERIFIED",
        "verification_notes": (
            "Board Policy 2021-02 (adopted 2/19/21; revised 4/7/22 and 2/6/25) read in the current official "
            "Pharmacy Practice Resources publication on 2026-08-19 during Pre-Batch3 T3 authoring under "
            "Issue #86. A fresh independent legal and full-bank realism audit is still required before release."
        ),
    },
]

QUESTIONS = [
    {
        "question_id": "MA-Q-0227",
        "family_id": "T3_0227_MA_BEDSIDE_DISCHARGE_DELIVERY",
        "area": 4,
        "topic": "Pharmacy operations",
        "subtopic": "Bed-side delivery of discharge prescriptions",
        "difficulty": 4,
        "question_type": "SBA",
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": (
            "A Massachusetts pharmacy runs a bed-side delivery service for discharge prescriptions at an "
            "inpatient healthcare facility. To speed up discharges, it proposes that its delivery staff hand "
            "each enrolled patient's medications to the unit charge nurse, who will add them to the discharge "
            "paperwork packet. How should the pharmacy evaluate this proposal?"
        ),
        "choices": [
            {"id": "A", "text": "It works, because the charge nurse is a licensed professional employed by the facility."},
            {"id": "B", "text": "It works, because the patient already consented to the bed-side delivery service."},
            {"id": "C", "text": "It works, provided the facility records receipt of the medications in the chart."},
            {"id": "D", "text": "It fails, because Massachusetts does not allow bed-side delivery of discharge prescriptions."},
            {"id": "E", "text": "It fails, because bed-side delivery medications must reach the patient or the patient's agent."},
        ],
        "correct_choice_ids": ["E"],
        "explanation": {
            "core_reasoning": (
                "247 CMR 9.04(4) governs bed-side delivery of discharge prescriptions in an inpatient "
                "healthcare facility. The pharmacy must obtain the patient's consent, must not restrict the "
                "patient's freedom of choice of pharmacy services, and shall deliver any medications directly "
                "to the patient or the patient's agent. Routing the medications through unit staff and the "
                "discharge paperwork does not meet that delivery requirement, and consent to the service does "
                "not substitute for it."
            ),
            "choice_analysis": {
                "A": "The permitted recipients are the patient or the patient's agent, not any licensed facility employee.",
                "B": "Consent authorizes the service; it does not change who may receive the medications.",
                "C": "Charting receipt by the facility is not the delivery step the regulation requires.",
                "D": "Bed-side delivery of discharge prescriptions is permitted in Massachusetts under stated conditions.",
                "E": "Correct: the medications must be delivered directly to the patient or the patient's agent.",
            },
            "related_facts": [
                "The same provision requires patient consent before a pharmacy provides bed-side delivery service.",
                "The same provision bars a bed-side delivery arrangement from restricting a patient's freedom of choice of pharmacy services.",
            ],
            "mpje_trap": "Consent to a bed-side delivery program is not consent to hand the medications to facility staff.",
        },
        "rule_ids": ["MA-BEDSIDE-DELIVERY"],
        "drug_ids": [],
        "reasoning_steps": [
            "Identify the discharge medications as a bed-side delivery service rather than an ordinary mail or carrier shipment",
            "Separate the consent condition from the condition governing who may receive the medications",
            "Apply the direct-to-patient-or-agent requirement to the proposed nurse handoff",
        ],
    },
    {
        "question_id": "MA-Q-0228",
        "family_id": "T3_0228_MA_CENTRAL_FILL_ROUTING",
        "area": 4,
        "topic": "Shared pharmacy services",
        "subtopic": "Central fill dispensing routing",
        "difficulty": 5,
        "question_type": "SATA",
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": (
            "A Massachusetts retail pharmacy is drafting the operating procedure for a new central-fill "
            "arrangement with a second pharmacy. The draft has to state where each finished prescription goes "
            "and what work the central site may perform. Which statements are correct under current Board "
            "policy? Select all that apply."
        ),
        "choices": [
            {"id": "A", "text": "A centrally filled Schedule IV prescription must go to the pharmacy where the prescription originated for final dispensing to the patient."},
            {"id": "B", "text": "A centrally filled Schedule VI prescription that does not require Prescription Monitoring Program reporting may be shipped directly to the patient by the central fill pharmacy."},
            {"id": "C", "text": "A centrally filled Schedule VI prescription for a drug that does require Prescription Monitoring Program reporting may also be shipped directly to the patient, since it is not federally scheduled."},
            {"id": "D", "text": "A central fill pharmacy sited outside Massachusetts does not need its own Massachusetts pharmacy license while the originating pharmacy holds one."},
            {"id": "E", "text": "Central filling of compounded sterile preparations for dispensing within Massachusetts is not permitted."},
        ],
        "correct_choice_ids": ["A", "B", "E"],
        "explanation": {
            "core_reasoning": (
                "Board Policy 2021-02 sets central-fill destination, licensure and scope limits separately "
                "from the ownership or written-agreement structure that authorizes the arrangement. Centrally "
                "filled Schedule II through V controlled substances must be delivered to the pharmacy where "
                "the prescription originated for final dispensing to the patient. Centrally filled Schedule VI "
                "controlled substances may instead be delivered or shipped directly to the patient, except for "
                "drugs requiring Prescription Monitoring Program reporting. A central fill pharmacy dispensing "
                "into, within, or from Massachusetts must itself hold a Massachusetts resident or non-resident "
                "retail pharmacy license, and central filling of compounded sterile preparations for "
                "Massachusetts dispensing is prohibited."
            ),
            "choice_analysis": {
                "A": "Correct: a centrally filled Schedule II through V prescription returns to the originating pharmacy for final dispensing.",
                "B": "Correct: a Schedule VI prescription outside the monitoring-program reporting category may ship directly from the central fill site.",
                "C": "The monitoring-program reporting category is the stated carve-out, so direct patient shipment is unavailable for it.",
                "D": "A central fill pharmacy dispensing into, within, or from Massachusetts must itself hold a Massachusetts resident or non-resident retail pharmacy license.",
                "E": "Correct: central filling of compounded sterile preparations for Massachusetts dispensing is prohibited.",
            },
            "related_facts": [
                "Participating pharmacies handling federally controlled substances must follow the DEA central-fill requirements and hold DEA registration.",
                "Participants must maintain a policy and procedure covering medications that were never dispensed to patients.",
            ],
            "mpje_trap": (
                "Schedule VI is not a blanket permission to ship a centrally filled prescription straight to "
                "the patient, because monitoring-program reportable drugs are carved out."
            ),
        },
        "rule_ids": ["MA-CENTRAL-FILL-DISPENSING-ROUTE"],
        "drug_ids": [],
        "reasoning_steps": [
            "Separate the central-fill destination rule from the ownership or written-agreement structure",
            "Route a federally scheduled centrally filled prescription back to the originating pharmacy for final dispensing",
            "Apply the Prescription Monitoring Program carve-out to the Schedule VI direct-shipment allowance",
        ],
    },
]

FAMILIES = [
    {
        "family_id": "T3_0227_MA_BEDSIDE_DISCHARGE_DELIVERY",
        "area": 4,
        "topic": "Pharmacy operations",
        "subtopic": "Bed-side delivery of discharge prescriptions",
        "primary_rule_ids": ["MA-BEDSIDE-DELIVERY"],
        "secondary_rule_ids": [],
        "drug_required": False,
        "scenario_types": ["practice scenario"],
        "common_traps": [
            "Do not treat consent to a bed-side delivery program as authority to hand medications to facility staff."
        ],
        "target_difficulties": [4],
        "target_item_types": ["SBA"],
        "max_questions_in_final_bank": 2,
        "current_candidate_count": 1,
        "current_released_count": 0,
    },
    {
        "family_id": "T3_0228_MA_CENTRAL_FILL_ROUTING",
        "area": 4,
        "topic": "Shared pharmacy services",
        "subtopic": "Central fill dispensing routing",
        "primary_rule_ids": ["MA-CENTRAL-FILL-DISPENSING-ROUTE"],
        "secondary_rule_ids": [],
        "drug_required": False,
        "scenario_types": ["operational design scenario"],
        "common_traps": [
            "Do not read Schedule VI status as blanket permission to ship a centrally filled prescription directly to the patient."
        ],
        "target_difficulties": [5],
        "target_item_types": ["SATA"],
        "max_questions_in_final_bank": 2,
        "current_candidate_count": 1,
        "current_released_count": 0,
    },
]

CANDIDATE_STATUS = {
    "verification_status": "AUDIT_PENDING",
    "lifecycle_status": "AUDIT_PENDING",
    "last_legal_review": AUTHORING_DATE,
    "audits": [],
    "duplicate_review_status": "PENDING",
    "independent_audit_status": "PENDING",
    "final_adjudication": None,
    "development_fixture": True,
}

# These released records are frozen dependencies of MA-Q-0215 / MA-Q-0220 and must not move.
PROTECTED_RULES = ("MA-DRUG-DELIVERY-SHIPPING", "MA-SHARED-PHARMACY-SERVICES")


def main() -> int:
    for rule_id in PROTECTED_RULES:
        path = DATA / "rules" / f"{rule_id.lower()}.json"
        record = load_json(path)
        if semantic_content_hash(record, "rule") != record["content_hash"]:
            raise SystemExit(f"{rule_id} is already inconsistent; refusing to author on a drifted tree")

    for rule in RULES:
        rule = dict(rule)
        rule["content_hash"] = semantic_content_hash(rule, "rule")
        path = DATA / "rules" / f"{rule['rule_id'].lower()}.json"
        if path.exists():
            raise SystemExit(f"{path} already exists; refusing to overwrite an existing canonical rule")
        write_json(path, rule)
        print(f"wrote {path.relative_to(DATA.parent).as_posix()} ({rule['content_hash'][:16]}...)")

    for question in QUESTIONS:
        record = {**question, **CANDIDATE_STATUS}
        path = DATA / "questions" / f"{question['question_id'].lower()}.json"
        if path.exists():
            raise SystemExit(f"{path} already exists; refusing to overwrite an existing canonical question")
        write_json(path, record)
        print(f"wrote {path.relative_to(DATA.parent).as_posix()}")

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    existing = {family["family_id"] for family in matrix["families"]}
    for family in FAMILIES:
        if family["family_id"] in existing:
            raise SystemExit(f"family {family['family_id']} already exists")
        matrix["families"].append(family)
    write_json(matrix_path, matrix)
    print(f"added {len(FAMILIES)} families to {matrix_path.relative_to(DATA.parent).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

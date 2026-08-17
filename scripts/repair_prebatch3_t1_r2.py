from __future__ import annotations

from qa_common import DATA, load_json, write_json

TODAY = "2026-08-17"

REPAIRS = {
    "MA-Q-0079": {
        "question_type": "SBA",
        "stem": (
            "A Massachusetts pharmacist is preparing for renewal. In the first calendar year of the two-year "
            "renewal cycle, she completed 24 contact hours. In the second calendar year, she has completed 16 "
            "contact hours. Her pharmacy-law and home-study requirements are otherwise satisfied. What is the "
            "best way to address the remaining CE requirement?"
        ),
        "choices": [
            {"id": "A", "text": "Renew now because the Board looks only at the combined 40-hour total for the two-year cycle."},
            {"id": "B", "text": "Complete 4 more contact hours in the second calendar year because the 20-hour minimum applies to each calendar year."},
            {"id": "C", "text": "Complete only additional pharmacy-law hours; the annual total no longer matters once the law requirement is met."},
            {"id": "D", "text": "Ask the CE provider to redate 4 first-year credits so they count in the second calendar year."},
            {"id": "E", "text": "Repeat all 20 second-year hours because completing more than 20 hours in the first year invalidates the surplus-year record."},
        ],
        "correct_choice_ids": ["B"],
        "explanation": {
            "core_reasoning": (
                "Massachusetts pharmacist CE is measured by calendar year within the renewal cycle. The pharmacist "
                "must satisfy the 20-contact-hour minimum in the second calendar year itself; having completed more "
                "than 20 hours in the first year does not convert the requirement into a simple two-year aggregate."
            ),
            "choice_analysis": {
                "A": "The annual minimum must be satisfied in each calendar year rather than only as a combined cycle total.",
                "B": "This applies the annual 20-contact-hour requirement to the 16-hour second year and identifies the 4-hour shortfall.",
                "C": "Meeting the pharmacy-law component does not eliminate the overall annual contact-hour minimum.",
                "D": "CE credit is not made compliant by administratively shifting completed first-year activity into a later calendar year.",
                "E": "Extra first-year education does not invalidate otherwise valid first-year credit or require repeating the entire second-year minimum from zero."
            },
            "related_facts": [
                "247 CMR 4.03 generally requires 20 contact hours of approved continuing education in each calendar year, including the separately specified pharmacy-law component."
            ],
            "mpje_trap": "Do not turn an annual CE requirement into a two-year pooled-hour calculation."
        },
        "rule_ids": ["MA-PHARMACIST-CE"],
        "drug_ids": [],
        "reasoning_steps": [
            "Identify that the CE minimum is applied by calendar year within the renewal cycle",
            "Compare the second-year total with the annual minimum",
            "Reject attempts to cure an annual shortfall by reallocating prior-year credit"
        ],
    },
    "MA-Q-0082": {
        "question_type": "SBA",
        "stem": (
            "A 58-year-old patient was referred to and consented to retail collaborative drug therapy management "
            "for hypertension under a written agreement that specifically covers hypertension. During a follow-up, "
            "the patient reports new recurrent wheezing and asks the pharmacist to diagnose asthma and start treatment. "
            "Asthma is not included in this patient's referral or current collaborative agreement. What is the most appropriate response?"
        ),
        "choices": [
            {"id": "A", "text": "Manage the wheezing as asthma because asthma appears among disease states that may be eligible for retail collaborative management."},
            {"id": "B", "text": "Diagnose asthma and begin treatment after obtaining a second patient consent, without changing the referral or agreement."},
            {"id": "C", "text": "Begin asthma treatment now and have the supervising physician add asthma to the agreement retroactively by the end of the day."},
            {"id": "D", "text": "Continue authorized hypertension management and return the new wheezing for physician evaluation before expanding collaborative management to that condition."},
            {"id": "E", "text": "Manage the new condition without another referral because the individual-referral limitation applies only to controlled-substance therapy."},
        ],
        "correct_choice_ids": ["D"],
        "explanation": {
            "core_reasoning": (
                "Retail CDTM is patient-, diagnosis-, referral-, and agreement-specific. The fact that asthma can be an "
                "eligible statutory disease state does not let the pharmacist independently diagnose or add it to this "
                "patient's existing hypertension collaboration. The pharmacist should remain within the current authorized "
                "scope and return the new condition to the supervising physician for evaluation and any appropriate referral/agreement update."
            ),
            "choice_analysis": {
                "A": "Statutory eligibility of a disease state does not itself place that disease in this patient's referral and collaborative agreement.",
                "B": "Patient consent alone does not supply the physician diagnosis, referral, and agreement scope required for retail CDTM.",
                "C": "The pharmacist should not act outside the existing collaborative scope and then attempt to validate the action retroactively.",
                "D": "This preserves the existing hypertension collaboration while routing a new diagnosis and scope decision back through the supervising physician.",
                "E": "The referral and collaborative-scope requirements are not limited to controlled substances."
            },
            "related_facts": [
                "M.G.L. c.112, §24B1/2 requires physician referral with a diagnosis, patient notice/consent in the retail setting, and a collaborative agreement that specifically references each disease state being co-managed."
            ],
            "mpje_trap": "A disease appearing on the statutory retail-CDTM list is not automatically added to every patient's existing referral or agreement."
        },
        "rule_ids": ["MA-CDTM-RETAIL-SCOPE"],
        "drug_ids": [],
        "reasoning_steps": [
            "Identify the diagnosis and disease state actually covered by the patient's referral and agreement",
            "Distinguish statutory disease-state eligibility from patient-specific collaborative authority",
            "Route a new diagnosis outside current scope back to the supervising physician"
        ],
    },
    "MA-Q-0083": {
        "question_type": "SBA",
        "stem": (
            "A patient is receiving retail collaborative drug therapy management for diabetes. The supervising physician "
            "has also identified painful diabetic neuropathy as a co-morbidity and asks the collaborating pharmacist to "
            "initiate pregabalin (Schedule V), offering to countersign the pharmacist's order the same day. What is the best legal response?"
        ),
        "choices": [
            {"id": "A", "text": "Initiate pregabalin because the physician identified the neuropathy as a co-morbidity of diabetes."},
            {"id": "B", "text": "Initiate pregabalin if the supervising physician countersigns the pharmacist's order within 24 hours."},
            {"id": "C", "text": "Do not initiate pregabalin under retail collaborative prescribing because the agreement cannot authorize prescribing Schedule II through V controlled substances."},
            {"id": "D", "text": "Initiate a 30-day pregabalin supply because retail collaborative practice permits a 30-day extension of current therapy."},
            {"id": "E", "text": "Initiate pregabalin because the retail prohibition applies to Schedule II through IV but not Schedule V."},
        ],
        "correct_choice_ids": ["C"],
        "explanation": {
            "core_reasoning": (
                "A retail collaborative practice agreement may not permit pharmacist prescribing of Schedule II through V "
                "controlled substances. Pregabalin is Schedule V. Physician involvement, a related co-morbidity, or same-day "
                "countersignature does not convert that prohibited retail-CDTM prescribing authority into a permitted one."
            ),
            "choice_analysis": {
                "A": "Identifying a related co-morbidity does not override the separate statutory Schedule II-V prescribing prohibition.",
                "B": "A countersignature does not expand the retail collaborating pharmacist's statutory prescribing authority.",
                "C": "This applies the express retail-CDTM prohibition on prescribing Schedule II through V controlled substances.",
                "D": "The stem describes initiation, not an extension of current therapy already prescribed by the supervising physician, and the Schedule II-V prescribing restriction still controls.",
                "E": "The statutory retail restriction expressly extends through Schedule V."
            },
            "related_facts": [
                "Pregabalin is a federal and Massachusetts Schedule V controlled substance.",
                "M.G.L. c.112, §24B1/2(c)(5) states that a retail collaborative practice agreement may not permit prescribing Schedule II through V controlled substances."
            ],
            "mpje_trap": "Do not let physician participation or a related disease state erase a separate schedule-based limit on retail collaborative prescribing."
        },
        "rule_ids": ["MA-CDTM-CONTROLLED-LIMIT"],
        "drug_ids": ["pregabalin"],
        "reasoning_steps": [
            "Classify pregabalin as Schedule V",
            "Identify the express Schedule II-V prescribing limitation in retail CDTM",
            "Reject physician countersignature or co-morbidity status as a substitute for statutory prescribing authority"
        ],
    },
    "MA-Q-0084": {
        "question_type": "SBA",
        "stem": (
            "A retail collaborative practice agreement expressly allows initial Schedule VI prescriptions. The supervising "
            "physician referred an adult patient with hypertension, and the collaborating pharmacist issues an authorized "
            "Schedule VI antihypertensive prescription for that referred diagnosis late Friday afternoon. The physician's "
            "office will not reopen until Monday. What should the pharmacist do next?"
        ),
        "choices": [
            {"id": "A", "text": "Arrange to send a copy of the prescription to the supervising physician within 24 hours rather than waiting for the office to reopen."},
            {"id": "B", "text": "Wait until Monday because the 24-hour copy requirement excludes weekends and holidays."},
            {"id": "C", "text": "Keep the prescription only in the pharmacy's collaborative-practice file unless the supervising physician later requests a copy."},
            {"id": "D", "text": "Send the prescription copy to the Board within 24 hours and provide it to the supervising physician at the next scheduled review."},
            {"id": "E", "text": "No copy is required because the agreement already authorizes initial Schedule VI prescribing for the referred diagnosis."},
        ],
        "correct_choice_ids": ["A"],
        "explanation": {
            "core_reasoning": (
                "For a qualifying initial Schedule VI prescription issued by a retail collaborating pharmacist, the statute "
                "requires the prescription to be for the diagnosis identified in the supervising physician's individual "
                "referral and requires a copy of the prescription to be sent to the supervising physician within 24 hours. "
                "The stem already satisfies the agreement and diagnosis conditions, so the remaining immediate duty is the 24-hour copy."
            ),
            "choice_analysis": {
                "A": "This applies the statutory 24-hour requirement to send the prescription copy to the supervising physician.",
                "B": "The statute states a 24-hour period and does not create a routine next-business-day exception in the rule tested here.",
                "C": "Internal pharmacy retention does not replace the required copy to the supervising physician.",
                "D": "The statute directs the copy to the supervising physician, not the Board as a substitute recipient.",
                "E": "Agreement authority to issue the prescription does not eliminate the separate post-prescribing copy requirement."
            },
            "related_facts": [
                "M.G.L. c.112, §24B1/2(c)(5) permits qualifying retail collaborating pharmacists to issue Schedule VI prescriptions when the agreement specifically allows initial prescriptions for referred patients and ties the prescription to the diagnosis in the individual referral.",
                "A copy of such a prescription must be sent to the supervising physician within 24 hours."
            ],
            "mpje_trap": "Separate authority to issue the Schedule VI prescription from the post-prescribing duty to send the supervising physician a copy within 24 hours."
        },
        "rule_ids": ["MA-CDTM-SVI-RX"],
        "drug_ids": [],
        "reasoning_steps": [
            "Confirm that the agreement and individual referral support an initial Schedule VI prescription",
            "Identify the supervising physician as the required recipient of the prescription copy",
            "Apply the 24-hour statutory timing requirement"
        ],
    },
}


def main() -> int:
    for qid, repair in REPAIRS.items():
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        question = load_json(path)
        if question.get("question_id") != qid:
            raise RuntimeError(f"question ID mismatch at {path}")
        for key, value in repair.items():
            question[key] = value
        question["verification_status"] = "AUDIT_PENDING"
        question["lifecycle_status"] = "AUDIT_PENDING"
        question["last_legal_review"] = TODAY
        question["audits"] = []
        question["duplicate_review_status"] = "PENDING"
        question["independent_audit_status"] = "PENDING"
        question["final_adjudication"] = None
        write_json(path, question)
        print(f"repaired {qid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

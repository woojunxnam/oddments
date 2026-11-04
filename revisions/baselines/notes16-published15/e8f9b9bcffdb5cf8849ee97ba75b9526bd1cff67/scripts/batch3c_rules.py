"""Canonical rule records required by Batch 3 tranche B3-C.

Every rule below was read verbatim from the current official publication on 2026-08-20:

  * 247 CMR 9.00 Professional Practice Standards, dated 12/6/24, recovered in full from the
    official PDF at https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download
    (sha256 9e1f9d1d2813f761ee7d275c83e220f371382a2e81e0f485f2b7aaabcddce22a).
  * 247 CMR 16.00 Collaborative Drug Therapy Management, recovered in full from the official PDF
    at https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download
    (sha256 d98c03bcad5f440fcb52da41c5febe7f7c4cbf85db7237051bc6f75cc52506d8).
  * 243 CMR 2.12, recovered in full from the official PDF at
    https://www.mass.gov/doc/243-cmr-2-licensing-and-the-practice-of-medicine-0/download.
  * M.G.L. c. 94C, ss. 19A, 19B, 19E and 21A, and M.G.L. c. 112, s. 24B1/2, read on
    malegislature.gov.

Nothing here is authored from a section heading, a summary, or a secondary source. Area
assignment follows the bank's settled taxonomy: pharmacist practice duties, pharmacist
professional conduct, patient care and collaborative practice are Area 2.
"""

from __future__ import annotations

CMR9 = "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"
CMR16 = "https://www.mass.gov/regulations/247-CMR-1600-collaborative-drug-therapy-management"
CMR243 = "https://www.mass.gov/regulations/243-CMR-200-licensing-and-the-practice-of-medicine"
GL94C21A = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21A"
GL94C19A = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19A"
GL94C19B = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19B"
GL112 = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B%201~2"

VERIFIED = "2026-08-20"


def _rule(rule_id, topic, subtopic, title, summary, relevance, authority,
          confusions, numeric=(), exceptions=(), related=(), area=2):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": "MA",
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": relevance,
        "authority": list(authority),
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": VERIFIED,
        "numeric_facts": list(numeric),
        "exceptions": list(exceptions),
        "common_confusions": list(confusions),
        "related_rule_ids": list(related),
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": (
            "Read verbatim in the current official publication on 2026-08-20 during Batch 3 tranche "
            "B3-C authoring under Issue #91. A fresh independent legal and full-bank realism audit "
            "is still required before release."
        ),
    }


def _reg(section, url=CMR9, name="Massachusetts Board of Registration in Pharmacy regulations"):
    return {"type": "PROMULGATED_REGULATION", "name": name, "section": section, "url": url}


def _stat(section, url):
    return {"type": "STATUTE", "name": "Massachusetts General Laws", "section": section, "url": url}


MED = "Massachusetts Board of Registration in Medicine regulations"


RULES = [
    # ---------------- 247 CMR 9.01 professional conduct and practice standards ----------------
    _rule(
        "MA-CONDUCT-ANTI-CIRCUMVENTION", "Professional conduct", "Circumvention of pharmacy law",
        "Prohibition on indirect circumvention of pharmacy law",
        "A licensee may not process a prescription, dispense a drug, device or other substance, or "
        "administer a controlled substance or vaccine in a manner which is intended, either directly "
        "or indirectly, to circumvent any law or regulation governing the practice of pharmacy. The "
        "standard reaches the design of an arrangement, so step-wise technical compliance is no answer "
        "where the manner is intended to reach a forbidden result.",
        "Tests whether the candidate applies the standard to the design of an arrangement rather than "
        "to each individual step, and recognises that indirect intent is expressly covered.",
        [_reg("247 CMR 9.01(2)")],
        ["Treating each step's technical legality as a defence to the arrangement as a whole",
         "Reading the prohibition as reaching only direct circumvention",
         "Confusing it with the separate 247 CMR 9.01(9) prohibition on fraudulent or deceptive acts, "
         "which turns on deceiving a person rather than on evading a rule"],
        related=["MA-CONDUCT-DECEPTIVE-ACT"],
    ),
    _rule(
        "MA-USP-CURRENCY-DISPLACEMENT", "Professional practice standards", "Governing standard",
        "Current USP standards and their displacement by Board regulation",
        "Unless otherwise regulated by the Board, a licensee shall adhere to the most current standards "
        "established by each chapter of the United States Pharmacopeia. Adherence is mandatory rather "
        "than advisory wherever the Board has not regulated the point, the obligation runs to the most "
        "CURRENT chapter rather than to any edition the pharmacy happens to hold, and a Board "
        "regulation displaces USP where the two differ.",
        "Tests the precedence rule and the currency limb, distinct from the content of any particular "
        "USP chapter.",
        [_reg("247 CMR 9.01(3)")],
        ["Treating USP as advisory where the Board is silent",
         "Following a superseded edition of a real USP chapter and treating that as compliance",
         "Applying USP over a Board regulation that regulates the same point"],
        exceptions=["Where the Board has otherwise regulated the point, the Board regulation governs"],
        related=["MA-HAZARDOUS-DRUG-HANDLING"],
    ),
    _rule(
        "MA-PHARMACIST-COMPETENCE-SCOPE", "Professional practice standards", "Individual competence",
        "Practice within the pharmacist's own education, training and experience",
        "A pharmacist shall practice pharmacy within the scope of his or her education, training and "
        "experience AND within the recognized pharmacist scope of practice. The two limbs are "
        "cumulative, so an act that is lawful for the profession generally may still be outside the "
        "scope of a particular pharmacist who lacks the training and experience for it.",
        "Tests the separation of professional scope from individual competence, which candidates "
        "routinely collapse into a single question.",
        [_reg("247 CMR 9.01(4)")],
        ["Assuming that whatever pharmacists generally may do, this pharmacist may do",
         "Treating employer authorisation or willingness as a substitute for training and experience",
         "Confusing it with technician scope of practice"],
    ),
    _rule(
        "MA-RETURN-ACCEPTANCE-DUTY", "Medication returns", "Mandatory versus discretionary acceptance",
        "Which returned medications a pharmacy must accept",
        "A pharmacy SHALL accept a medication that it previously dispensed to a patient if the "
        "medication was dispensed to the patient in error, or is suspected to be defective or "
        "contaminated. A medication so accepted may not be returned to the pharmacy's inventory and "
        "must be quarantined and properly disposed. A pharmacy is NOT required to accept a medication "
        "from a patient that was properly dispensed and not defective at the time it was dispensed.",
        "Tests the boundary between the returns a pharmacy must take and those it may decline, which "
        "sits upstream of what happens to an accepted return.",
        [_reg("247 CMR 9.01(7)")],
        ["Treating every patient return as mandatory to accept",
         "Treating every patient return as refusable",
         "Returning an accepted item to inventory because it looks intact"],
        exceptions=["No obligation to accept a properly dispensed, non-defective medication"],
        related=["MA-RETURN-QUARANTINE"],
    ),
    _rule(
        "MA-CONDUCT-DECEPTIVE-ACT", "Professional conduct", "Fraud and deception",
        "Prohibition on any fraudulent or deceptive act",
        "A licensee may not engage in any fraudulent or deceptive act. The prohibition is freestanding: "
        "it needs no separate substantive rule to have been broken, and it is complete on the act "
        "without proof that anyone relied on the deception or suffered a loss.",
        "Tests recognition of deception as an independent violation, separate from the underlying "
        "dispensing or record rule.",
        [_reg("247 CMR 9.01(9)")],
        ["Looking for a broken dispensing rule before finding a violation",
         "Requiring proof of reliance or financial loss",
         "Assuming a literally true statement cannot be deceptive"],
        related=["MA-CONDUCT-ANTI-CIRCUMVENTION"],
    ),
    _rule(
        "MA-SUBSTANDARD-RECIPIENT-LIMIT", "Professional conduct", "Transfer of substandard product",
        "Substandard product may go only to an authorised recipient",
        "A licensee may not dispense or distribute any expired, outdated, defective, contaminated, "
        "counterfeit, contraband, or otherwise substandard drug or device to any person or entity who "
        "is not licensed or legally authorized to receive such drug or device. The prohibition is "
        "defined by the recipient's authorisation, not by the intended use of the product, so the same "
        "expired stock may lawfully go to an authorised recipient and unlawfully to an unauthorised one.",
        "Tests the recipient test, which candidates commonly replace with a motive test.",
        [_reg("247 CMR 9.01(12)")],
        ["Deciding by the intended use, such as training or charitable donation, rather than by whether "
         "the recipient is licensed or legally authorized",
         "Assuming an expired product may never be transferred at all",
         "Treating staff as authorised recipients by virtue of employment"],
        exceptions=["Transfer to a person or entity that IS licensed or legally authorized to receive it"],
    ),
    _rule(
        "MA-BLANK-PRESCRIPTION-FORMS", "Professional conduct", "Prescriber forms and steering",
        "Prohibition on supplying practitioners with pharmacy-referencing blank forms",
        "A licensee may not provide any practitioner with blank prescription forms which refer to any "
        "pharmacist or pharmacy. The violation is complete on providing the form: no payment, no "
        "agreement and no patient actually steered is required.",
        "Tests a prohibition whose trigger is the pre-printed reference itself rather than any exchange "
        "of value, which distinguishes it from the referral-remuneration prohibition.",
        [_reg("247 CMR 9.01(14)")],
        ["Looking for remuneration or an agreement before finding a violation",
         "Requiring proof that a patient was actually steered",
         "Assuming supplying the forms free of charge cures it"],
        related=["MA-CONDUCT-REFERRAL-REMUNERATION"],
    ),
    _rule(
        "MA-COMPOUNDING-REFUSAL-LIMIT", "Pharmacy services", "Duty to compound",
        "Limits on refusing to compound customary preparations",
        "A licensee may not refuse to compound simple or moderate non-sterile compounded preparations "
        "customary to the community needs except upon extenuating circumstances or by a waiver of Board "
        "regulation. The duty is bounded by the preparation: it reaches simple or moderate non-sterile "
        "preparations customary to the community, and does not reach sterile or complex preparations.",
        "Tests compounding as an affirmative duty owed to the patient and the two express routes out of "
        "it, against the common assumption that a pharmacy may simply decline to offer the service.",
        [_reg("247 CMR 9.01(15)")],
        ["Assuming a pharmacy may decline any compounding it prefers not to do",
         "Extending the duty to sterile or complex preparations",
         "Treating inconvenience or workload as an extenuating circumstance without more"],
        exceptions=["Extenuating circumstances", "A waiver of Board regulation"],
    ),
    _rule(
        "MA-LICENSEE-CONFIDENTIALITY", "Confidentiality", "Licensee duty",
        "Duty to maintain confidentiality and to protect confidential information",
        "A licensee shall maintain patient confidentiality AND protect a patient's confidential "
        "information. The duty has two limbs: a pharmacist who discloses nothing may still fail it by "
        "leaving confidential information unprotected in the ordinary workflow of the pharmacy.",
        "Tests the affirmative protective limb, which candidates commonly reduce to a rule against "
        "telling people things.",
        [_reg("247 CMR 9.01(16)")],
        ["Reading the duty as non-disclosure only",
         "Assuming no breach where no third party actually read the information",
         "Confusing it with the separate physical requirements of the patient consultation area"],
        related=["MA-COUNSELING-CONSULTATION-AREA"],
    ),
    _rule(
        "MA-PRACTICE-HOUR-CEILING", "Fitness to practise", "Hours and rest",
        "Twelve-hour practice ceiling and eight-hour rest period",
        "A pharmacist, pharmacy intern, or pharmacy technician may not practice in a pharmacy for more "
        "than 12 hours in a 24 hour period without completing an eight CONSECUTIVE hour rest period "
        "prior to resuming work in a pharmacy. In the event of an extenuating circumstance the licensee "
        "may exceed 12 hours in order to act in the best interest of the patient, provided the time in "
        "excess of 12 hours is minimized AND the licensee documents the extenuating circumstance.",
        "Tests a limit on the pharmacist's own practice whose exception is conditioned on both "
        "minimisation and documentation, and whose rest period must be consecutive.",
        [_reg("247 CMR 9.01(17)")],
        ["Treating the exception as unconditional once a patient need exists",
         "Reading the rest period as eight hours in aggregate rather than eight consecutive hours",
         "Forgetting that the documentation duty falls on the licensee, not on the employer"],
        numeric=[{"fact": "Maximum practice time without a completed rest period", "value": 12,
                  "unit": "hours in a 24 hour period", "conditions": "subject to the extenuating-circumstance exception"},
                 {"fact": "Required rest period before resuming work in a pharmacy", "value": 8,
                  "unit": "consecutive hours", "conditions": "after exceeding the 12 hour ceiling"}],
        exceptions=["Extenuating circumstance, provided the excess is minimized and documented"],
    ),
    # ---------------- 247 CMR 9.06, 9.16 and 9.17 ----------------
    _rule(
        "MA-OPIOID-ANTAGONIST-COUNSEL-REFER", "Public health", "Opioid antagonist counter duties",
        "Counselling, pamphlet and referral duties on an opioid antagonist request",
        "A pharmacy that dispenses a naloxone rescue kit or other approved opioid antagonist shall "
        "provide counseling AND the Board-approved opioid antagonist information pamphlet at the time "
        "of dispensing. A pharmacy that does not have one readily available for dispensing at the time "
        "requested shall REFER THE REQUESTOR TO THE NEAREST LOCATION that has one readily available.",
        "Tests two duties arising at the counter, including an affirmative referral duty that survives "
        "the pharmacy's inability to supply.",
        [_reg("247 CMR 9.06(3) and 9.06(4)")],
        ["Assuming a stock-out ends the pharmacy's obligation",
         "Treating the pamphlet as satisfied by verbal counselling alone",
         "Confusing these counter duties with third-party dispensing eligibility"],
        related=["MA-NALOXONE"],
    ),
    _rule(
        "MA-PATIENT-PROFILE-DUTY", "Patient care", "Patient profile",
        "Confidential patient profile, immediate retrieval and the reasonable-effort standard",
        "A pharmacist and pharmacy shall maintain a confidential patient profile for each patient to "
        "whom a prescription is dispensed. The computerized pharmacy system SHALL provide for the "
        "immediate retrieval of information necessary for the pharmacist to identify previously "
        "dispensed drugs at the time the prescription is presented for dispensing. The pharmacist or "
        "the pharmacist's designee shall make a REASONABLE EFFORT to obtain, record and maintain the "
        "patient's identifying details, patient history including known drug allergies and drug "
        "reactions, a comprehensive list of medications and relevant devices dispensed by the pharmacy, "
        "and the pharmacist's comments relevant to the patient's drug therapy.",
        "Tests the difference between an effort-based content duty and an absolute system capability, "
        "and the setting carve-out.",
        [_reg("247 CMR 9.16(7) and 9.16(8)")],
        ["Treating an incomplete profile as automatically non-compliant",
         "Treating the reasonable-effort standard as excusing a pharmacy that never asked",
         "Applying the reasonable-effort standard to the immediate-retrieval system requirement, which "
         "is not qualified by effort"],
        exceptions=["247 CMR 9.16 does not apply to institutional sterile compounding pharmacies"],
    ),
    _rule(
        "MA-DUR-RESPONSE-DOCUMENTATION", "Patient care", "Drug utilization review response",
        "Responsive measures and the duty to document them",
        "On identifying a drug utilization review finding, a pharmacist shall take appropriate measures "
        "to ensure the proper care of the patient, which MAY include consultation with the prescribing "
        "practitioner or direct consultation with the patient or the patient's agent. A pharmacist SHALL "
        "document any measures taken in response to a drug utilization review. The choice of measure is "
        "open; the recording of whatever measure was taken is not.",
        "Tests the split between a discretionary response and a mandatory record of it, which survives "
        "even where the clinical issue was fully resolved.",
        [_reg("247 CMR 9.17(2)")],
        ["Assuming resolution of the clinical issue discharges the documentation duty",
         "Reading the listed measures as an exhaustive menu",
         "Assuming a documented alert in the dispensing system is itself a record of the measure taken"],
        related=["MA-PRODUR"],
    ),
    _rule(
        "MA-DUR-EVIDENTIARY-BASIS", "Patient care", "Basis of drug utilization review",
        "Current standards on which a drug utilization review must rest",
        "The drug utilization review shall be based upon CURRENT standards, which MAY include the "
        "American Hospital Formulary Service Drug Information, the United States Pharmacopoeia Drug "
        "Information, the American Medical Association Drug Evaluations, Plumb's Veterinary Drug "
        "Handbook, and other peer-reviewed medical literature. The named works are permissive examples "
        "rather than a closed list, and the governing requirement is currency.",
        "Tests both that the list is open and that a superseded edition of a listed work fails the "
        "currency requirement.",
        [_reg("247 CMR 9.17(3)")],
        ["Treating the four named works as an exhaustive list",
         "Rejecting current peer-reviewed literature because it is not named",
         "Accepting a superseded edition of a named compendium as a current standard"],
        related=["MA-PRODUR", "MA-DUR-RESPONSE-DOCUMENTATION"],
    ),
    # ---------------- M.G.L. c. 94C s. 21A ----------------
    _rule(
        "MA-PROSPECTIVE-REVIEW-MANDATE", "Patient care", "Prospective drug review",
        "Mandatory prospective drug review with a permissive screening menu",
        "A pharmacist SHALL conduct a prospective drug review before each new prescription is dispensed "
        "or delivered to a patient or a person acting on behalf of such patient. Such review MAY "
        "include, but not be limited to, screening for therapeutic duplication, drug disease "
        "contraindication, drug interactions including serious interactions with nonprescription or "
        "over-the-counter drugs, incorrect drug dosage, duration of drug treatment, drug allergy "
        "interactions and clinical abuse or misuse. The review is compulsory; the screening list is not.",
        "Tests the mandatory-review and permissive-menu structure, and that the trigger is each NEW "
        "prescription including one handed to a person acting on the patient's behalf.",
        [_stat("M.G.L. c. 94C, s. 21A, first paragraph", GL94C21A)],
        ["Treating the screening list as the definition of the duty",
         "Assuming the review is only owed when the patient collects in person",
         "Assuming over-the-counter interactions fall outside the review"],
        exceptions=["The section does not apply to a drug dispensed to an inpatient at a hospital or "
                    "nursing home, except as required by federal regulations under 42 USC 1396r-8"],
        related=["MA-PRODUR"],
    ),
    _rule(
        "MA-COUNSELING-OFFER-METHOD", "Patient care", "Offer to counsel",
        "How the offer to counsel must be made, and the remote-delivery container label",
        "A pharmacist shall offer to counsel any person who presents a NEW prescription for filling. "
        "The offer shall be made either by face to face communication between the pharmacist or the "
        "pharmacist's designee and the patient, or by telephone, except when the patient's needs or "
        "availability require an alternative method. Where a person elects delivery at a location other "
        "than a pharmacy, the requirements may be satisfied by access to a toll-free telephone service, "
        "and the number of that service SHALL BE PRINTED ON A LABEL AFFIXED TO EACH CONTAINER of a "
        "prescription drug dispensed by the pharmacy to a patient.",
        "Tests the permitted methods of the offer and the container-label consequence of the "
        "remote-delivery route, which candidates commonly treat as optional signage.",
        [_stat("M.G.L. c. 94C, s. 21A, second and third paragraphs", GL94C21A)],
        ["Assuming any method is acceptable at the pharmacist's convenience",
         "Treating the toll-free number as satisfied by a notice in the delivery paperwork rather than "
         "a label affixed to each container",
         "Extending the offer duty to refills, when the statutory trigger is a new prescription"],
        related=["MA-COUNSELING-REMOTE-DELIVERY", "MA-COUNSELING-DOCUMENTATION"],
    ),
    _rule(
        "MA-COUNSELING-RECORD-PRESUMPTION", "Patient care", "Counseling record presumption",
        "Presumption arising from the absence of a refusal record",
        "The pharmacist or designee shall make reasonable efforts to obtain, record and maintain "
        "specified patient information, including any additional comments relevant to the patient's "
        "drug use and any failure to accept the pharmacist's offer to counsel. The information may be "
        "recorded in the patient's manual or electronic profile, in the prescription signature log, or "
        "in any other system of records. THE ABSENCE OF ANY RECORD OF A FAILURE TO ACCEPT THE "
        "PHARMACIST'S OFFER TO COUNSEL SHALL CREATE A PRESUMPTION THAT SUCH COUNSELING WAS PROVIDED.",
        "Tests a presumption that runs in the pharmacist's favour on silence, which is the opposite of "
        "the record-keeping intuition candidates bring to documentation questions.",
        [_stat("M.G.L. c. 94C, s. 21A, penultimate paragraphs", GL94C21A)],
        ["Assuming an unrecorded encounter means counselling cannot be shown",
         "Assuming the presumption requires an affirmative record that counselling occurred",
         "Restricting the permitted record to the patient profile alone"],
        related=["MA-COUNSELING-DOCUMENTATION"],
    ),
    # ---------------- M.G.L. c. 94C standing orders ----------------
    _rule(
        "MA-STANDING-ORDER-TRAINING-CONTRAST", "Public health", "Standing-order training preconditions",
        "Training preconditions differ across the standing-order regimes",
        "Before dispensing emergency contraception under the statewide standing order a pharmacist MAY "
        "complete a Commissioner-approved training programme, which must include proper documentation, "
        "quality assurance and referral to additional services. Before dispensing a COVID-19 drug under "
        "a standing order a pharmacist SHALL complete a Commissioner-approved training programme, which "
        "must include evaluation of the patient's medical history and relevant records including recent "
        "laboratory blood work for kidney or liver problems, contraindications with commonly prescribed "
        "medications, clinical monitoring recommendations and follow-up advice.",
        "Tests that two adjacent standing-order regimes impose different training obligations, one "
        "permissive and one mandatory, with different content.",
        [_stat("M.G.L. c. 94C, s. 19A(d)", GL94C19A),
         _stat("M.G.L. c. 94C, s. 19E(c)",
               "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19E")],
        ["Assuming a single training rule governs every statewide standing order",
         "Treating the emergency contraception training as a precondition to dispensing",
         "Treating the COVID-19 training as optional"],
    ),
    _rule(
        "MA-OPIOID-ANTAGONIST-BILLING", "Public health", "Opioid antagonist billing sequence",
        "Insurance identification and claim submission before dispensing an opioid antagonist",
        "A pharmacist or designee who dispenses an opioid antagonist shall, for health insurance billing "
        "and cost-sharing purposes, treat the transaction as the dispensing of a prescription TO THE "
        "PERSON PURCHASING the opioid antagonist regardless of the ultimate user. Unless the purchaser "
        "requests to pay out-of-pocket, the pharmacist or designee shall make a reasonable effort to "
        "identify the purchaser's insurance coverage and to submit a claim to the insurance carrier "
        "PRIOR TO DISPENSING.",
        "Tests whose coverage is billed when purchaser and ultimate user differ, and that the claim "
        "step precedes dispensing unless the purchaser opts out.",
        [_stat("M.G.L. c. 94C, s. 19B(e)", GL94C19B)],
        ["Billing the intended ultimate user rather than the purchaser",
         "Treating the claim as something to be submitted after the product is handed over",
         "Assuming a third-party purchaser must pay cash"],
        related=["MA-NALOXONE"],
    ),
    # ---------------- M.G.L. c. 112 s. 24B1/2 definitions ----------------
    _rule(
        "MA-CDTM-SCOPE-DEFINITION", "Collaborative practice", "Scope and the diagnostic boundary",
        "What collaborative drug therapy management includes, and where it stops",
        "Collaborative drug therapy management is the initiating, monitoring, modifying and "
        "discontinuing of a patient's drug therapy by a pharmacist in accordance with a collaborative "
        "practice agreement. It MAY include collecting and reviewing patient histories; obtaining and "
        "checking vital signs, including pulse, temperature, blood pressure and respiration; and, under "
        "the supervision of, or in direct consultation with, a physician, ordering and evaluating the "
        "results of laboratory tests directly related to drug therapy when performed in accordance with "
        "approved protocols applicable to the practice setting AND WHEN THE EVALUATION SHALL NOT "
        "INCLUDE A DIAGNOSTIC COMPONENT.",
        "Tests both the affirmative content of the authority and the diagnostic boundary that limits it, "
        "including the conditions attached specifically to laboratory work.",
        [_stat("M.G.L. c. 112, s. 24B1/2(a), definition of collaborative drug therapy management", GL112)],
        ["Reading the laboratory limb as free-standing, when it requires physician supervision or direct "
         "consultation and an approved protocol",
         "Treating a diagnostic conclusion as permissible because the test was properly ordered",
         "Assuming vital signs require the same physician involvement as laboratory evaluation"],
        related=["MA-CDTM-RETAIL-SCOPE"],
    ),
    _rule(
        "MA-CDTM-PATIENT-DEFINITION", "Collaborative practice", "Patient eligibility and dual recording",
        "Who is a CDTM patient, and who must record the referral and consent",
        "A CDTM patient is a person referred to a pharmacist by his supervising physician for the purpose "
        "of receiving collaborative drug therapy management services. The supervising physician shall "
        "assess the patient and include a diagnosis when referring. The patient shall be notified of, and "
        "shall consent to, the services in the retail drug business setting. INDIVIDUAL REFERRAL AND "
        "CONSENT SHALL BE RECORDED BY THE PHARMACIST AND THE SUPERVISING PHYSICIAN in the patient's record.",
        "Tests eligibility upstream of any clinical act, and the dual-recording duty that binds both "
        "professionals rather than only the referring physician.",
        [_stat("M.G.L. c. 112, s. 24B1/2(a), definition of patient", GL112)],
        ["Assuming the physician's record alone discharges the recording duty",
         "Treating a referral without a diagnosis as sufficient",
         "Assuming notice and consent are required in every setting rather than in the retail setting"],
        related=["MA-CDTM-RETAIL-SCOPE"],
    ),
    _rule(
        "MA-CPA-CONSTITUTION-CURRENCY", "Collaborative practice", "Validity of the agreement",
        "What makes a collaborative practice agreement validly constituted and current",
        "A collaborative practice agreement is a WRITTEN AND SIGNED agreement between a pharmacist with "
        "training and experience relevant to the scope of the collaborative practice and a supervising "
        "physician that defines the collaborative practice in which they propose to engage. The "
        "collaborative practice shall be within the scope of the supervising physician's practice. Each "
        "agreement shall be subject to review and renewal ON A BIENNIAL BASIS. An agreement shall "
        "include individually developed guidelines for any prescriptive practice of the pharmacist.",
        "Tests the constitutive requirements of the instrument the pharmacist acts under, including the "
        "physician-scope limit and the biennial currency requirement.",
        [_stat("M.G.L. c. 112, s. 24B1/2(a), definition of collaborative practice agreement", GL112)],
        ["Treating an unsigned or oral understanding as an agreement",
         "Overlooking that the collaborative practice must sit inside the supervising physician's own "
         "scope of practice",
         "Assuming an agreement remains effective indefinitely once made"],
        numeric=[{"fact": "Review and renewal cycle for a collaborative practice agreement", "value": 2,
                  "unit": "years", "conditions": "at least; 'on a biennial basis'"}],
        related=["MA-CDTM-QUALIFICATIONS"],
    ),
    _rule(
        "MA-CDTM-EMPLOYMENT-RELATIONSHIPS", "Collaborative practice", "Employment and purpose",
        "Who may employ whom for collaborative drug therapy management",
        "A physician or physician group MAY hire pharmacists for the purpose of practising collaborative "
        "drug therapy management under an agreement for the benefit of a patient of that physician or "
        "group. NO retail pharmacy may employ a physician FOR THE PURPOSE of maintaining, establishing "
        "or entering into a collaborative practice agreement. Nothing prohibits a retail pharmacy from "
        "hiring a physician or licensed medical practitioner for the purpose of conducting QUALITY "
        "ASSURANCE REVIEWS of its pharmacists engaged in collaborative drug therapy management.",
        "Tests a prohibition that turns on the PURPOSE of the employment rather than on the fact of it, "
        "with a quality-assurance carve-out that is easily conflated with the prohibited purpose.",
        [_stat("M.G.L. c. 112, s. 24B1/2(e)", GL112),
         _reg("247 CMR 16.04(7)", CMR16)],
        ["Reading the prohibition as barring a pharmacy from employing any physician at all",
         "Treating a quality-assurance engagement as the prohibited purpose",
         "Assuming the direction of hiring makes no difference"],
    ),
    # ---------------- 247 CMR 16.04 ----------------
    _rule(
        "MA-CDTM-DELEGATION-TERMS", "Collaborative practice", "Delegation of duties",
        "The agreement must name what may and may not be delegated",
        "A collaborative practice agreement SHALL specify those duties of the authorized pharmacist that "
        "may be delegated to other appropriately trained and authorized staff AND those duties under the "
        "agreement that shall not be delegated. It SHALL also specify when and how an authorized "
        "pharmacist may delegate duties under the agreement, and the duration and scope of the "
        "delegation. Pharmacy intern and pharmacy technician duties supporting an authorized pharmacist "
        "must be performed in accordance with 247 CMR 8.01 and 8.02 through 8.06.",
        "Tests that silence in the agreement is not permission, and that four separate things must be "
        "stated before a delegation is good.",
        [_reg("247 CMR 16.04(3)", CMR16)],
        ["Treating an agreement's silence on delegation as permitting it",
         "Assuming that naming the delegable duties is enough without the when, how, duration and scope",
         "Assuming collaborative practice displaces the ordinary intern and technician scope rules"],
    ),
    _rule(
        "MA-CDTM-TERMINATION-DUTIES", "Collaborative practice", "Termination and patient notice",
        "Continuity before termination and written notice to the patient after it",
        "PRIOR TO termination or non-renewal of a CDTM agreement, an authorized pharmacist and "
        "supervising physician shall arrange for an UNINTERRUPTED CONTINUATION of the patient's drug "
        "therapy, in accordance with the terms of the agreement. WHEN an agreement is not renewed or "
        "CDTM is otherwise terminated, an authorized pharmacist and supervising physician shall INFORM "
        "THE PATIENT IN WRITING of the termination and of the procedures in place for the continuation "
        "of the patient's drug therapy.",
        "Tests two duties with different timing and different content, one owed before the agreement "
        "ends and one after, both owed jointly.",
        [_reg("247 CMR 16.04(5)", CMR16)],
        ["Collapsing the two duties into a single notification after termination",
         "Assuming oral notice to the patient suffices",
         "Assuming the duties fall on the physician alone"],
        related=["MA-CDTM-DISCIPLINE-NOTICE"],
    ),
    _rule(
        "MA-CDTM-AGREEMENT-CUSTODY", "Collaborative practice", "Custody of the agreement",
        "Copy with the pharmacist, original with the physician",
        "An authorized pharmacist must maintain a COPY of the current CDTM agreement, INCLUDING COPIES "
        "of the current patient referral and patient consent, IN THE PRIMARY PRACTICE SETTING, readily "
        "retrievable at the request of the Board of Registration in Pharmacy AND the Board of "
        "Registration in Medicine. In accordance with 243 CMR 2.12 the supervising physician must "
        "maintain the ORIGINAL of the current agreement, including the original current referral and "
        "consent, IN THE PATIENT'S MEDICAL RECORD in the custody of the supervising physician.",
        "Tests the custody split and the two-board retrievability requirement, both of which candidates "
        "commonly reduce to keeping the signed agreement somewhere.",
        [_reg("247 CMR 16.04(6)", CMR16),
         {"type": "PROMULGATED_REGULATION", "name": MED, "section": "243 CMR 2.12", "url": CMR243}],
        ["Holding the original on site and treating that as compliance",
         "Holding the agreement without the referral and consent copies",
         "Assuming retrievability to the Board of Registration in Pharmacy alone is enough"],
        related=["MA-CDTM-CE-EVIDENCE"],
    ),
    # ---------------- 243 CMR 2.12 ----------------
    _rule(
        "MA-CDTM-REFERRAL-BY-SETTING", "Collaborative practice", "Meaning of referral",
        "Referral means different things in a community pharmacy and elsewhere",
        "Referral means the individual patient referral by a supervising physician to an authorized "
        "pharmacist for the purpose of receiving CDTM services IN A COMMUNITY PHARMACY SETTING. IN ALL "
        "OTHER PRACTICE SETTINGS, Referral means the CONSULTATION of a supervising physician and an "
        "authorized pharmacist about a patient for that purpose. In the community pharmacy setting the "
        "supervising physician shall execute a written CDTM referral which shall include, but is not "
        "limited to, the patient's name and address, the primary diagnosis for which CDTM services are "
        "authorized, the diagnosis of any comorbid conditions for which they are authorized, any known "
        "patient drug allergies, a statement that the patient has executed a written consent, and any "
        "other specific instructions to the authorized pharmacist.",
        "Tests a definition that changes with the setting, so the formalities required in a community "
        "pharmacy are not required in a hospital, together with the required contents of the written form.",
        [{"type": "PROMULGATED_REGULATION", "name": MED,
          "section": "243 CMR 2.12(1), definition of Referral", "url": CMR243}],
        ["Applying the community-pharmacy written referral formalities in every setting",
         "Assuming a consultation can never amount to a referral",
         "Omitting the statement that written consent has been executed from the written referral"],
        related=["MA-CDTM-PATIENT-DEFINITION"],
    ),
    _rule(
        "MA-CDTM-WRITING-FORM", "Collaborative practice", "Form of collaborative documents",
        "What counts as written for CDTM agreements, referrals and consents",
        "All references to written regarding collaborative practice agreement referrals, consents and "
        "any other related documents shall be: if paper based, written in ink, indelible pencil or any "
        "other means; or transmitted electronically in a format that maintains patient confidentiality "
        "and can be read and stored in a RETRIEVABLE AND READABLE form. Such documents may be "
        "transmitted electronically with electronic signatures without alteration of the information, "
        "provided the electronic transmission accords with M.G.L. c. 94C, s. 23(g) and 105 CMR 721.00.",
        "Tests an asymmetry: the paper route is deliberately permissive while the electronic route "
        "carries confidentiality, readability, retrievability and external-instrument conditions.",
        [{"type": "PROMULGATED_REGULATION", "name": MED,
          "section": "243 CMR 2.12(1)(a) and (b)", "url": CMR243}],
        ["Assuming an electronic copy is automatically more compliant than a handwritten one",
         "Rejecting indelible pencil as informal",
         "Overlooking that an unreadable or unstorable electronic image fails the requirement"],
        related=["MA-CDTM-AGREEMENT-CUSTODY"],
    ),
]

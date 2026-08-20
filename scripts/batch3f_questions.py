"""Tranche B3-F: sixteen Area-3 questions, MA-Q-0391 through MA-Q-0406.

B3-F answers a measured deficit rather than a projection. CLAUDE-FRESH-B3S3-V2 failed all eight
B3-S3 questions on realism, so the legacy salvage contributes nothing and Area 3 tops out at 81
against the Issue #91 minimum of 87. Sixteen gives the six needed plus margin for audit attrition,
which ran at 2 of 33 in B3-C.

Every question rests on a proposition read verbatim from primary text on 2026-08-20, and every one
was probed against the whole bank before drafting. Nine of the sixteen draw on 247 CMR sections that
no rule in the bank had cited: 9.05, 9.07, 9.08, 9.11, 9.12 and 9.22. These are ordinary dispensing
decisions -- what may go in a planner, which fridge is allowed, who gets the Medication Guide --
which is what Issue #91 asked for after the S2 realism failures, and the opposite of another pass
over refill arithmetic.

Structural targets, measured against the Phase-2 pool after the B3-E v2 expansion:

  * 11 SBA / 5 SATA, holding the bank's SBA share steady.
  * SBA keys A x2 / B x2 / C x2 / D x3 / E x2; the heaviest letter takes 27% of the tranche.
  * SATA correct-counts 2-correct x2 / 3-correct x2 / 4-correct x1, so the tranche carries the
    bank's modal three-correct rather than omitting it, which shuffling cannot hide.
  * SATA slot presence A 60% / B 60% / C 60% / D 60% / E 40%, well inside the 80% gate in
    scripts/check_tranche_key_patterns.py.
"""

from __future__ import annotations


def q(qid, area, family, topic, subtopic, difficulty, qtype, stem, choices, correct,
      core, analysis, rules, steps, facts, trap):
    return {
        "question_id": qid,
        "family_id": family,
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "question_type": qtype,
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": stem,
        "choices": [{"id": cid, "text": text} for cid, text in choices],
        "correct_choice_ids": list(correct),
        "explanation": {
            "core_reasoning": core,
            "choice_analysis": analysis,
            "related_facts": list(facts),
            "mpje_trap": trap,
        },
        "rule_ids": list(rules),
        "drug_ids": [],
        "reasoning_steps": list(steps),
    }


QUESTIONS = [

    q("MA-Q-0391", 3, "B3F_EMERGENCY_SUBSTITUTION_DEVIATION", "Dispensing",
      "Substitution in a medical emergency", 4, "SATA",
      "A Massachusetts pharmacist faces a medical emergency at 2 a.m. The only prescription on hand "
      "is marked 'no substitution', the prescribed brand is not in stock, and an interchangeable "
      "product on the Massachusetts list is. The pharmacist dispenses the interchangeable product. "
      "Which statements about this dispensing are correct? Select all that apply.",
      [("A", "A medical emergency permits filling a 'no substitution' prescription this way when the brand is out of stock."),
       ("B", "The pharmacist's own note of the emergency completes what the regulation asks of the pharmacy."),
       ("C", "The date, hour and nature of the emergency must be recorded on the prescription or in the pharmacy system."),
       ("D", "The purchaser must indicate acceptance of the deviation in writing."),
       ("E", "The deviation runs only toward the cheaper product, never toward the brand as written.")],
      ["A", "C", "D"],
      "247 CMR 9.05(1)(a) permits a pharmacist in a medical emergency to fill a prescription marked "
      "'no substitution' by dispensing a less expensive interchangeable product allowed by the "
      "Massachusetts List of Interchangeable Drugs if the particular brand is not in stock. "
      "247 CMR 9.05(1)(b) attaches two conditions to any such instance: the pharmacist must record "
      "the date, hour and nature of the medical emergency on the back of the prescription or in the "
      "computerized pharmacy system, AND the person purchasing the drug product must indicate "
      "acceptance of this deviation from the law in writing.",
      {"A": "Correct: the emergency limb is exactly this situation, brand out of stock.",
       "B": "The pharmacist's record is one of two conditions; the purchaser's written acceptance is the other.",
       "C": "Correct: date, hour and nature, on the prescription or in the system.",
       "D": "Correct: the purchaser indicates acceptance of the deviation in writing.",
       "E": "The same paragraph also permits dispensing the brand as written when no interchangeable product is in stock."},
      ["MA-INTERCHANGE-MEDICAL-EMERGENCY"],
      ["Confirm a medical emergency, which is what opens the paragraph at all",
       "Match the direction of the deviation to which product is missing from stock",
       "Apply both conditions, the pharmacy's record and the purchaser's written acceptance"],
      ["The prescriptions are to be clearly identifiable and available for inspection"],
      "Candidates stop at the permission and miss that the deviation is conditioned on a purchaser "
      "signature as well as a pharmacy record."),

    q("MA-Q-0392", 3, "B3F_REUSABLE_PLANNER_PROVENANCE", "Dispensing",
      "Reusable daily dosage planners", 4, "SBA",
      "A patient asks a Massachusetts pharmacy to set up her medications in a reusable weekly "
      "planner. She brings in a sealed, in-date bottle of her lisinopril that a pharmacy across town "
      "dispensed last month, and asks that it go in alongside the medications this pharmacy supplies. "
      "The pharmacy has a designated preparation space and written planner procedures. What should "
      "the pharmacist do about the lisinopril?",
      [("A", "Include it, since the patient requested the planner service and the bottle is sealed and in date."),
       ("B", "Decline to place it in the planner, because it was dispensed by a different pharmacy."),
       ("C", "Include it after transferring the original prescription to this pharmacy on the spot."),
       ("D", "Include it once the patient signs an acknowledgement that she supplied the product."),
       ("E", "Include it, provided the planner is labelled to show which pharmacy supplied each drug.")],
      ["B"],
      "247 CMR 9.07 lets a pharmacy dispense medications in a reusable daily dosage planner at the "
      "patient's or the patient's agent's request, but the first condition is flat: a pharmacy may "
      "not place any medication in a reusable daily dosage planner that was previously dispensed by "
      "a different pharmacy. The condition is about where the product has already been, so a fresh "
      "transfer, a consent form or a label cannot reach back and cure it.",
      {"A": "The patient's request opens the service; it does not lift the provenance condition.",
       "B": "Correct: 247 CMR 9.07(1) forbids placing another pharmacy's previously dispensed medication in the planner.",
       "C": "Transferring the prescription governs future fills. This physical product has already been dispensed elsewhere.",
       "D": "No acknowledgement is offered as a cure for the provenance condition.",
       "E": "Labelling does not answer the objection, which is to the product's origin rather than to its identification."},
      ["MA-REUSABLE-DOSAGE-PLANNER"],
      ["Confirm the planner service was requested by the patient or her agent",
       "Identify which pharmacy previously dispensed each product offered for the planner",
       "Apply the provenance condition before the housekeeping conditions"],
      ["The pharmacy must also maintain cleaning, labeling, dispensing and hand hygiene procedures"],
      "The sealed, in-date bottle invites a clinical judgment. The regulation asks a provenance "
      "question instead, and answers it without reference to the product's condition."),

    q("MA-Q-0393", 3, "B3F_COMPLIANCE_PACKAGING_LABELING_CONFLICT", "Dispensing",
      "Compliance packaging conditions", 4, "SBA",
      "A Massachusetts pharmacy prepares multi-drug single-dose compliance packages. For one patient "
      "the prescriber asks that a moisture-sensitive tablet be included; the FDA-approved labeling "
      "directs that the product be kept in its original container with the desiccant until use. The "
      "pharmacy has a designated space, full written procedures for this packaging type, and a "
      "compatible package component. What controls whether the tablet may be included?",
      [("A", "The prescriber's request, since compliance packaging is prepared on the prescriber's direction."),
       ("B", "The pharmacy's written procedures, since the regulation asks for procedures rather than outcomes."),
       ("C", "The patient's informed acceptance of any reduction in shelf life."),
       ("D", "The FDA-approved labeling, which the packaging must not contradict."),
       ("E", "The Board's Schedule II and III maintenance-medication policy.")],
      ["D"],
      "247 CMR 9.08(1) lists the conditions on compliance packaging together. Alongside the "
      "designated space, the written procedures and the compatibility requirement sits the condition "
      "that the compliance packaging not conflict with the USP-DI monograph or FDA-approved "
      "labeling. Labeling that directs storage in the original container with a desiccant is in "
      "conflict with removal into a compliance package, and no amount of procedure answers it.",
      {"A": "A prescriber may ask, but 247 CMR 9.08 conditions what the pharmacy may do.",
       "B": "Procedures are one condition among several and do not displace the labeling condition.",
       "C": "Patient acceptance is not among the conditions the regulation lists.",
       "D": "Correct: the packaging may not conflict with the USP-DI monograph or FDA-approved labeling.",
       "E": "That policy governs which controlled substances may be included, not moisture-sensitive product handling."},
      ["MA-COMPLIANCE-PACKAGING-STANDARDS"],
      ["Separate the regulation's conditions from the Board's controlled-substance policy",
       "Read the FDA-approved labeling for a storage direction",
       "Treat a labeling conflict as decisive rather than as a factor to be weighed"],
      ["The regulation also requires that the medications be compatible with each other and with the packaging"],
      "Two plausible authorities are in the room, a prescriber and the pharmacy's own procedures. "
      "The condition that decides the case is the product's own approved labeling."),

    q("MA-Q-0394", 3, "B3F_PPA_VERIFICATION_AND_RECALL", "Dispensing",
      "Pharmacy processing automation", 4, "SATA",
      "A Massachusetts pharmacy is commissioning an automated system that counts tablets, fills "
      "vials and applies labels. To keep cells full, the pharmacy plans to top up a cell without "
      "emptying it first, so two manufacturer lot numbers will sit together. Which statements about "
      "this arrangement are correct? Select all that apply.",
      [("A", "Comingling lot numbers in one cell is prohibited outright."),
       ("B", "The pharmacy must hold a policy to quarantine all comingled lots if a single lot is recalled."),
       ("C", "A pharmacist's visual check of the finished vial satisfies the verification requirement."),
       ("D", "Controlled substance accountability need not be addressed until the system handles Schedule II drugs."),
       ("E", "The system must use a technological verification such as bar code, weight or RFID checking.")],
      ["B", "E"],
      "247 CMR 9.11(1) permits pharmacy processing automation to count, fill and label on two "
      "conditions: the automation uses a technological verification -- bar code, electronic, weight, "
      "radio frequency identification or similar -- to ensure the correct medication is dispensed; "
      "and, if lot numbers are comingled in a single cell, the pharmacy maintains a policy and "
      "procedure to quarantine all comingled lot numbers in the event a single lot is recalled. "
      "247 CMR 9.11(2) requires standing policies covering operation and maintenance, security, "
      "controlled substance accountability, quality assurance, and stocking and return activities.",
      {"A": "Comingling is permitted; it is conditioned on a quarantine policy rather than forbidden.",
       "B": "Correct: the quarantine policy is what makes comingling permissible.",
       "C": "The regulation asks for a technological verification, which a visual check is not.",
       "D": "Controlled substance accountability is a standing policy requirement, not one triggered by schedule.",
       "E": "Correct: the named examples are bar code, electronic, weight and RFID verification."},
      ["MA-PHARMACY-PROCESSING-AUTOMATION"],
      ["Identify the two conditions that permit the automation at all",
       "Recognise comingling as a conditioned practice rather than a prohibited one",
       "Keep the standing policy requirements separate from the two permissive conditions"],
      ["A licensed pharmacist remains responsible for final dispensing process validation under 247 CMR 9.04(1)"],
      "The comingling plan reads like a violation looking for a penalty. The regulation permits it "
      "and asks instead what happens on the day a lot is recalled."),

    q("MA-Q-0395", 3, "B3F_ADD_LOCATION_AND_ORDER", "Dispensing",
      "Automated dispensing devices", 4, "SBA",
      "A Massachusetts pharmacy proposes to place an automated dispensing device holding controlled "
      "substances in the staff room of a group medical practice that is not a licensed health care "
      "facility. Every removal would be logged, the cabinet would be alarmed, and the pharmacy would "
      "maintain full written procedures. What is the correct assessment?",
      [("A", "The arrangement fails, because the device must be located in a licensed health care facility."),
       ("B", "The arrangement works, because the pharmacy's procedures cover accountability and security."),
       ("C", "The arrangement works if the practice registers the cabinet with the Board separately."),
       ("D", "The arrangement works for Schedule III through V, and fails only for Schedule II."),
       ("E", "The arrangement fails, because a pharmacy may not use an automated dispensing device for controlled substances at all.")],
      ["A"],
      "247 CMR 9.12 opens the use of an automated dispensing device for controlled substances on "
      "four conditions, and the first is locational: the device is located in a licensed health care "
      "facility. Dispensing must also be pursuant to a valid patient-specific prescription or order, "
      "utilisation must accord with all laws, regulations and policies, and the pharmacy must "
      "maintain the listed policies. A group practice that is not a licensed health care facility "
      "fails the first condition, whatever the strength of the remaining controls.",
      {"A": "Correct: the location condition is not satisfied by security or procedure.",
       "B": "Those policies are a separate condition and cannot substitute for the location condition.",
       "C": "247 CMR 9.12 does not offer a separate registration route for the host site.",
       "D": "The section governs controlled substances as a class; it does not split by schedule.",
       "E": "Automated dispensing devices are permitted for controlled substances, on conditions."},
      ["MA-AUTOMATED-DISPENSING-DEVICE-CONDITIONS"],
      ["Test the location condition before the operational ones",
       "Confirm whether the host site is a licensed health care facility",
       "Recognise that strong compensating controls do not cure a failed threshold condition"],
      ["Dispensing from the device must also be pursuant to a valid patient-specific prescription or order"],
      "The scenario supplies every control a candidate expects to look for, which makes it easy to "
      "answer on the controls and never reach the threshold question of where the cabinet stands."),

    q("MA-Q-0396", 3, "B3F_REFRIGERATION_EQUIPMENT_STANDARD", "Dispensing",
      "Refrigerated and frozen storage", 3, "SATA",
      "A Massachusetts pharmacy is fitting out a new prescription area. It proposes a dorm-style "
      "refrigerator with a small freezer compartment inside the refrigerator space for the few "
      "frozen products it stocks, with a continuous temperature logger fitted. Which statements are "
      "correct? Select all that apply.",
      [("A", "The pharmacy may not use an appliance with a freezer compartment inside the refrigerator space."),
       ("B", "A freezer unit must be frost-free with an automatic defrost cycle unless the Board approves otherwise."),
       ("C", "A continuous logger showing in-range temperatures makes the appliance acceptable."),
       ("D", "The pharmacy's procedures must include a response protocol for any out-of-range temperature."),
       ("E", "A combination refrigerator/freezer unit would not be permitted either.")],
      ["A", "B", "D"],
      "247 CMR 9.22(2) permits a combination refrigerator/freezer, a standalone refrigerator or a "
      "standalone freezer, requires freezer units to be frost-free with an automatic defrost cycle "
      "unless the Board otherwise approves, and states that a pharmacy may not use an appliance "
      "containing a freezer compartment within the refrigerator space, such as a dorm-style "
      "refrigerator. 247 CMR 9.22(1) requires policies including a protocol to respond to any out of "
      "range temperature and an assessment of the integrity of the medication.",
      {"A": "Correct: the dorm-style appliance is named in the prohibition.",
       "B": "Correct: frost-free with automatic defrost, unless otherwise approved by the Board.",
       "C": "Monitoring is a separate duty; it does not make a prohibited appliance permissible.",
       "D": "Correct: the response protocol is part of the required policies.",
       "E": "A combination refrigerator/freezer is one of the three permitted configurations."},
      ["MA-REFRIGERATED-FROZEN-STORAGE"],
      ["Separate the equipment prohibition from the monitoring duty",
       "Read the permitted configurations before judging the proposed appliance",
       "Note that the out-of-range protocol also calls for a product integrity assessment"],
      ["Temperatures are measured and maintained in accordance with Board guidance"],
      "Good monitoring makes the appliance feel defensible. The regulation prohibits the appliance "
      "itself, so the quality of the logging never comes into it."),

    q("MA-Q-0397", 3, "B3F_TRANSFER_FEE_AND_AGENCY", "Dispensing",
      "Transfer of prescriptions", 3, "SBA",
      "A patient telephones a Massachusetts pharmacy and asks it to bring over a prescription held "
      "at another pharmacy. The receiving pharmacy tells her it will charge a small administrative "
      "fee for the work, and that she must telephone the other pharmacy herself to start the "
      "process. Which statement best describes the receiving pharmacy's position?",
      [("A", "Both the fee and the requirement that she call the other pharmacy are permissible."),
       ("B", "The fee is permissible, but the pharmacy must make the call itself."),
       ("C", "The fee is not permissible, and the pharmacy may act as her agent to obtain the transfer."),
       ("D", "The fee is not permissible, but the patient must still initiate the transfer herself."),
       ("E", "Neither is permissible, because only the transferring pharmacy may charge or initiate.")],
      ["C"],
      "247 CMR 9.14 settles both points. Under 9.14(3) a pharmacy may not charge a fee for "
      "transferring a prescription. Under 9.14(2) the pharmacy may act as the patient's agent in "
      "order to facilitate a transfer, so the patient need not make the approach herself, and under "
      "9.14(1) a pharmacy shall transfer at the request of a patient or agent in a timely manner so "
      "as not to delay patient therapy.",
      {"A": "The fee is prohibited outright by 247 CMR 9.14(3).",
       "B": "The agency point is right, but the fee is prohibited.",
       "C": "Correct: no fee, and the pharmacy may act as the patient's agent.",
       "D": "The fee point is right, but the pharmacy may act as her agent rather than leaving it to her.",
       "E": "The prohibition and the agency permission apply to the pharmacy the patient has approached."},
      ["MA-RX-TRANSFER"],
      ["Check whether a fee may be charged for a transfer",
       "Check who may initiate the transfer on the patient's behalf",
       "Read the timeliness duty as running against delay in patient therapy"],
      ["Schedule VI prescriptions transfer in the same manner as Schedule III through V prescriptions"],
      "The two halves of the pharmacy's answer fail for different reasons, so a candidate who "
      "spots only one of them lands on a distractor that is half right."),

    q("MA-Q-0398", 3, "B3F_PAMPHLET_LTC_EXCEPTION", "Patient information",
      "Consumer educational pamphlet", 4, "SBA",
      "A Massachusetts community pharmacy dispenses a Schedule II opioid for a patient who lives in "
      "a long-term care facility, delivered to the facility for her use there. A technician asks "
      "whether the state consumer educational pamphlet on narcotic drugs must go out with it. What "
      "is the correct answer?",
      [("A", "Yes, because the pamphlet duty attaches to every Schedule II narcotic dispensing."),
       ("B", "Yes, unless the facility confirms in writing that it will counsel the resident itself."),
       ("C", "No, because delivery to a facility is not a dispensing to a consumer."),
       ("D", "No, because the pamphlet is required only for a first fill of a given opioid."),
       ("E", "No, because the patient is a resident of a long-term care facility.")],
      ["E"],
      "M.G.L. c. 94C, s. 21 requires a pharmacist to distribute the pamphlet when dispensing a "
      "narcotic or controlled substance contained in Schedule II or III, and then states three "
      "situations in which pharmacists are not required to distribute it: the patient is receiving "
      "outpatient palliative care under c. 111, s. 227; the patient is a resident of a long-term "
      "care facility; or the drug is prescribed for use in the treatment of substance use disorder "
      "or opioid dependence. The second exception answers this case on its face.",
      {"A": "The general duty is subject to three statutory exceptions.",
       "B": "The statute does not condition the exception on any undertaking by the facility.",
       "C": "The dispensing is still a dispensing; the exception turns on the patient's residence.",
       "D": "Section 21 draws no distinction between a first fill and a later one.",
       "E": "Correct: residence in a long-term care facility is one of the three named exceptions."},
      ["MA-CS-II-III-PAMPHLET"],
      ["Confirm the drug is a Schedule II or III narcotic or controlled substance",
       "Run the three statutory exceptions before concluding the pamphlet is due",
       "Match the facts to the exception that actually fits"],
      ["The department distributes the pamphlets to pharmacies, not including institutional pharmacies"],
      "Two of the wrong answers reach the right result by the wrong route, which is worth as little "
      "as the wrong result when the next patient does not fit that route."),

    q("MA-Q-0399", 3, "B3F_COMPOUNDED_CONTACT_NUMBER", "Dispensing",
      "Compounded preparation labelling", 5, "SATA",
      "A Massachusetts pharmacy licensed for sterile compounding prepares two products on the same "
      "morning: a sterile infusion for an outpatient, and a sterile preparation for a patient "
      "admitted as an inpatient in the same hospital under its institutional licence. Which "
      "statements are correct? Select all that apply.",
      [("A", "Both containers must be labelled as a sterile compounded preparation."),
       ("B", "The outpatient container must also carry the pharmacist-contact telephone number."),
       ("C", "The telephone must be staffed during regular hours of operation and at least 56 hours a week."),
       ("D", "The inpatient preparation must also carry the telephone number, since the pharmacy does sterile compounding."),
       ("E", "The pharmacist reachable on that number must have access to the patient's records.")],
      ["A", "B", "C", "E"],
      "M.G.L. c. 94C, s. 21 sets two distinct duties. All drug preparations compounded by a "
      "board-licensed pharmacy must carry a label notifying users and practitioners that the drug is "
      "a sterile or non-sterile compounded preparation. Separately, pharmacies engaged in sterile or "
      "complex non-sterile compounding must provide a telephone number fostering communication "
      "between patients and a pharmacist employed by the pharmacy who has access to the patient's "
      "records, staffed during regular hours of operation every day and not less than 56 hours per "
      "week, affixed to the container alongside the compounded-preparation label. That telephone "
      "paragraph does not apply to an institutional pharmacy licensed under c. 112, s. 39I where the "
      "sterile preparation is to be administered to an inpatient within the same hospital.",
      {"A": "Correct: the compounded-preparation label duty reaches all such preparations.",
       "B": "Correct: the outpatient container falls squarely within the telephone paragraph.",
       "C": "Correct: staffed during regular hours every day and not less than 56 hours per week.",
       "D": "The telephone paragraph is disapplied for an inpatient preparation within the same hospital.",
       "E": "Correct: the pharmacist reached must have access to the patient's records."},
      ["MA-COMPOUND-LABEL-CONTACT"],
      ["Separate the compounded-preparation label duty from the telephone-number duty",
       "Apply the institutional inpatient carve-out to the telephone duty only",
       "Check the staffing standard attached to the telephone number"],
      ["The carve-out is tied to administration within the same hospital, not merely to inpatient status"],
      "One exception is written into one of the two paragraphs. Reading it as an exception to both "
      "strips the required compounded-preparation label from the inpatient container."),

    q("MA-Q-0400", 3, "B3F_ANTAGONIST_OFFER_MINOR", "Patient information",
      "Opioid antagonist offer", 4, "SBA",
      "A Massachusetts pharmacist is dispensing a Schedule II opioid prescribed for a 15-year-old "
      "patient. The patient's mother is collecting the medication. The pharmacist has already "
      "explained the potential adverse risks of the opioid. What does the statute require next?",
      [("A", "Nothing further, because a minor cannot be dispensed an opioid antagonist."),
       ("B", "Offer to dispense an opioid antagonist to the mother as the minor's parent."),
       ("C", "Offer to dispense an opioid antagonist only if the prescriber has also ordered one."),
       ("D", "Obtain the prescriber's authorisation before raising an opioid antagonist with the family."),
       ("E", "Record that the patient is a minor and treat the antagonist offer as inapplicable.")],
      ["B"],
      "M.G.L. c. 94C, s. 18D(b) requires a pharmacist dispensing an opioid contained in Schedule II "
      "to inform the patient of the potential adverse risks of the prescription opioid and to offer "
      "to dispense an opioid antagonist to the patient, and where applicable to a designee of the "
      "patient, or, for a patient who is a minor, to the minor's parent or guardian. The statute "
      "routes the offer to the parent or guardian rather than removing it.",
      {"A": "The statute redirects the offer for a minor; it does not withdraw it.",
       "B": "Correct: for a minor patient the offer is made to the minor's parent or guardian.",
       "C": "Section 18D states no condition based on a separate order from the prescriber.",
       "D": "The duty is the pharmacist's own and is not gated on prescriber authorisation.",
       "E": "Minority changes who receives the offer, not whether one is made."},
      ["MA-CII-OPIOID-ANTAGONIST-OFFER"],
      ["Confirm the drug is an opioid contained in Schedule II",
       "Identify the correct recipient of the offer for this patient",
       "Keep the offer duty separate from any dispensing that may follow"],
      ["The duty is to offer; the patient or family need not accept or purchase an antagonist"],
      "Minority reads like a reason the duty falls away. The statute treats it as a reason the offer "
      "goes to someone else."),

    q("MA-Q-0401", 3, "B3F_PARTIAL_FILL_DEADLINE_PATHWAY", "Controlled substances",
      "Which partial-fill deadline applies", 5, "SBA",
      "A Massachusetts patient presents a Schedule II oxycodone prescription written by her "
      "Massachusetts physician nine days earlier. She asks the pharmacy to dispense only part of it "
      "today and to hold the balance. A colleague says the initial partial fill is already too late "
      "because it is past the fifth day after the issue date. Which assessment is correct?",
      [("A", "The colleague is right; the five-day limit runs from the issue date for any Schedule II partial fill."),
       ("B", "The colleague is right, but only because the drug is a narcotic rather than a stimulant."),
       ("C", "The colleague is wrong; the five-day limit reaches only prescriptions filled on the out-of-state pathways."),
       ("D", "The colleague is wrong; no deadline governs a patient-requested partial fill of a Schedule II prescription."),
       ("E", "The colleague is wrong; the five-day limit runs from the first dispensing rather than from the issue date.")],
      ["C"],
      "M.G.L. c. 94C, s. 18(d3/4) contains two deadlines with different reach. The remaining portion "
      "must be filled not later than 30 days after the prescription issue date. The five-day limit "
      "on the initial partial dispensing applies only to a prescription filled pursuant to "
      "subsection (d) or (d1/2) -- respectively a nonnarcotic Schedule II prescription issued by an "
      "out-of-state practitioner, and a narcotic Schedule II prescription issued by a practitioner "
      "registered in Maine or a contiguous state. This prescription came from a Massachusetts "
      "physician, so neither pathway is engaged and the initial partial fill on day nine is in time.",
      {"A": "The five-day limit is conditioned on the prescription having been filled under s. 18(d) or (d1/2).",
       "B": "The narcotic distinction separates (d) from (d1/2); both remain out-of-state pathways.",
       "C": "Correct: subsections (d) and (d1/2) are the out-of-state prescriber pathways.",
       "D": "The 30-day remainder deadline still governs, measured from the issue date.",
       "E": "Both deadlines in the subsection are measured from the prescription issue date."},
      ["MA-CII-PARTIAL-FILL-PATHWAY-LIMITS"],
      ["Identify where the prescription was issued and under which subsection it is filled",
       "Match each deadline in s. 18(d3/4) to the pathway it governs",
       "Measure the surviving deadline from the prescription issue date"],
      ["Only the pharmacy that dispensed the lesser quantity may dispense the remaining portion"],
      "The five-day figure is real and sits in the same subsection, which makes it easy to apply to "
      "a prescription the subsection never sends down that path."),

    q("MA-Q-0402", 3, "B3F_MEDGUIDE_PRESCRIBER_DIRECTION", "Patient information",
      "Medication Guide distribution", 5, "SBA",
      "A prescriber telephones a pharmacy about a drug for which FDA requires a Medication Guide. "
      "She has concluded that receiving the Guide would not be in this particular patient's best "
      "interest, and directs that it not be provided. At the counter the patient asks the pharmacist "
      "for written information about the medicine. What must the pharmacist do?",
      [("A", "Provide the Medication Guide, because the patient has requested information."),
       ("B", "Withhold the Guide but supply the manufacturer's patient information leaflet instead."),
       ("C", "Withhold the Guide, because the prescriber's clinical direction controls at the counter."),
       ("D", "Withhold the Guide unless the patient puts the request in writing."),
       ("E", "Contact the prescriber for permission before providing anything in writing.")],
      ["A"],
      "21 CFR 208.26(b) permits the prescribing practitioner who determines that a Medication Guide "
      "is not in a particular patient's best interest to direct that it not be provided to that "
      "patient. The same paragraph then states that the authorized dispenser shall provide a "
      "Medication Guide to any patient who requests information when the drug product is dispensed, "
      "regardless of any such direction by the licensed practitioner. The patient's request at the "
      "counter is the trigger, and it overrides the direction.",
      {"A": "Correct: a request from the patient overrides the prescriber's direction.",
       "B": "The regulation names the Medication Guide, not a substitute document.",
       "C": "The direction stands only until the patient asks for information.",
       "D": "Nothing in 208.26(b) requires the request to be in writing.",
       "E": "The regulation resolves the conflict itself and does not route it back to the prescriber."},
      ["FED-MEDGUIDE-PRESCRIBER-DIRECTION"],
      ["Confirm the product is one for which a Medication Guide is required",
       "Note the prescriber's direction and the authority that permits it",
       "Apply the patient-request override in the same paragraph"],
      ["Without a request, the practitioner's direction is effective for that patient"],
      "The prescriber's direction is lawful, which makes it tempting to treat as final. The same "
      "paragraph that grants it also takes it away the moment the patient asks."),

    q("MA-Q-0403", 3, "B3F_MEDGUIDE_AGENT_DELIVERY", "Patient information",
      "Medication Guide distribution", 3, "SBA",
      "A neighbour collects a prescription on behalf of a housebound patient. The product is one for "
      "which FDA requires a Medication Guide. The pharmacy's practice is to hold the Guide on file "
      "and give it to the patient at the next visit, on the view that the Guide belongs to the "
      "patient personally. What is the correct assessment of that practice?",
      [("A", "It is sound, because a Medication Guide must be provided directly to the patient."),
       ("B", "It is sound, provided the pharmacy telephones the patient to summarise the Guide."),
       ("C", "It is sound only where the collecting person is not a family member."),
       ("D", "It is unsound, because the Guide goes to the patient or the patient's agent at the time of dispensing."),
       ("E", "It is unsound, because the Guide must be posted to the patient within 24 hours of dispensing.")],
      ["D"],
      "21 CFR 208.24(e) requires each authorized dispenser of a product for which a Medication Guide "
      "is required to provide a Medication Guide directly to each patient, or to the patient's "
      "agent, when the product is dispensed to a patient or to a patient's agent, unless an "
      "exemption applies under 208.26. Delivery to an agent is expressly contemplated, so holding "
      "the Guide back until the patient appears defers a duty that has already fallen due.",
      {"A": "The regulation names the patient or the patient's agent, not the patient alone.",
       "B": "A telephone summary is not the provision of a Medication Guide.",
       "C": "The regulation draws no distinction based on the agent's relationship to the patient.",
       "D": "Correct: the Guide goes to the patient or the patient's agent at the time of dispensing.",
       "E": "No such posting deadline appears in Part 208."},
      ["FED-MEDGUIDE-RECIPIENT"],
      ["Confirm a Medication Guide is required for the product",
       "Identify who is receiving the product on this occasion",
       "Provide the Guide to that person at the time of dispensing"],
      ["The container label must itself instruct the dispenser to provide a Medication Guide"],
      "The pharmacy's reasoning is patient-centred and sounds careful, which disguises that it "
      "postpones a duty the regulation attaches to the act of dispensing."),

    q("MA-Q-0404", 3, "B3F_PSE_LIMITS_BY_ACTOR", "Non-prescription products",
      "Pseudoephedrine quantity limits", 5, "SATA",
      "A customer at a Massachusetts pharmacy counter asks to buy 5 grams of pseudoephedrine base "
      "today. He mentions that he bought 5 grams elsewhere eleven days ago. Which statements about "
      "the federal quantity limits are correct? Select all that apply.",
      [("A", "A regulated seller may sell him up to 7.5 grams in a single calendar day."),
       ("B", "The pharmacy is the party federally restricted to 3.6 grams per purchaser per day."),
       ("C", "Today's sale would exceed the 3.6 gram daily seller restriction."),
       ("D", "Buying a further 5 grams within the 30-day window would put the purchaser over the 9 gram limit."),
       ("E", "The 9 gram limit applies to sellers rather than to purchasers.")],
      ["C", "D"],
      "The two limits bind different parties under different instruments. 21 CFR 1314.20(a) restricts "
      "a regulated seller from selling any purchaser more than 3.6 grams of pseudoephedrine base in "
      "a single calendar day, so a 5 gram sale is over the seller's daily ceiling. 21 U.S.C. 844(a) "
      "makes it unlawful for any person to purchase at retail more than 9 grams during a 30-day "
      "period, so a purchaser who already bought 5 grams eleven days ago would cross that "
      "prohibition. The 7.5 gram figure in 21 CFR 1314.20(b) is a 30-day limit and applies to mobile "
      "retail vendors.",
      {"A": "7.5 grams is a 30-day figure for mobile retail vendors, not a daily allowance.",
       "B": "The daily restriction does bind the seller, but this option omits that the sale here exceeds it.",
       "C": "Correct: 5 grams in one day is above the 3.6 gram daily seller restriction.",
       "D": "Correct: 5 plus 5 grams inside 30 days crosses the 9 gram retail purchase prohibition.",
       "E": "The 9 gram limit is framed as a prohibition on the person purchasing at retail."},
      ["FED-PSE-QUANTITY"],
      ["Separate the seller's daily restriction from the purchaser's 30-day prohibition",
       "Apply the daily figure to today's proposed sale",
       "Add the earlier purchase to test the 30-day purchase prohibition"],
      ["Massachusetts requirements apply alongside the federal limits rather than instead of them"],
      "Three real figures are in play and each belongs to a different party or period, so a "
      "candidate who remembers the numbers but not who they bind can pick any of them."),

    q("MA-Q-0405", 3, "B3F_PMP_INPATIENT_EXCLUSION", "Prescription monitoring",
      "Scope of the reporting duty", 4, "SBA",
      "A Massachusetts hospital pharmacy dispenses oxycodone twice for the same patient on the same "
      "day: once against a medication order while she is an inpatient on the ward, and once against "
      "a discharge prescription she takes home that afternoon. Which dispensings must be reported to "
      "the Prescription Monitoring Program?",
      [("A", "Neither, because both were dispensed by a hospital pharmacy."),
       ("B", "Both, because the reporting duty reaches every Schedule II dispensing."),
       ("C", "The inpatient medication order only."),
       ("D", "Both, unless the hospital reports inpatient administration through a separate system."),
       ("E", "The discharge prescription only.")],
      ["E"],
      "105 CMR 700.012(A)(1) applies the reporting requirement to every pharmacy registered with the "
      "Commissioner that dispenses a controlled substance pursuant to a prescription in Schedules II "
      "through V or an additional drug. 105 CMR 700.012(A)(2) then states that 105 CMR 700.012 shall "
      "not apply to the dispensing pursuant to a medication order of a controlled substance to an "
      "inpatient in a hospital. Two facts must coincide for the exclusion, a medication order and an "
      "inpatient; the discharge prescription satisfies neither and is reportable.",
      {"A": "The exclusion turns on the medication order and inpatient status, not on the pharmacy's setting.",
       "B": "The reporting duty is expressly disapplied for inpatient medication orders.",
       "C": "That reverses the exclusion; the medication order is the dispensing that is excluded.",
       "D": "No alternative-reporting condition appears in the paragraph.",
       "E": "Correct: the discharge prescription is dispensed pursuant to a prescription to a patient going home."},
      ["MA-PMP-INPATIENT-EXCLUSION"],
      ["Classify each dispensing as against a medication order or against a prescription",
       "Establish whether the patient was an inpatient at the time of that dispensing",
       "Apply the exclusion only where both facts hold"],
      ["An out-of-state pharmacy delivering such a substance to a person in Massachusetts is within the duty"],
      "Both dispensings happen in the same building on the same day for the same patient, which "
      "invites a single answer for both."),

    q("MA-Q-0406", 3, "B3F_PMP_ADDITIONAL_DRUG_DESIGNATION", "Prescription monitoring",
      "Designation of an additional drug", 4, "SBA",
      "A Massachusetts pharmacist reads a journal piece arguing that a particular Schedule VI "
      "medicine is being diverted and should be watched. Her pharmacy does not report its dispensing "
      "to the Prescription Monitoring Program. What determines whether that dispensing becomes "
      "reportable?",
      [("A", "The pharmacy's own assessment that the drug carries a bona fide potential for abuse."),
       ("B", "Rescheduling of the drug out of Schedule VI into Schedules II through V."),
       ("C", "A prescriber's request that the pharmacy report its dispensing of the drug."),
       ("D", "A determination by the Commissioner, followed by notification to dispensers."),
       ("E", "Publication of the diversion evidence in the professional literature.")],
      ["D"],
      "105 CMR 700.012(C)(8) provides that the Commissioner may determine that a drug is an "
      "additional drug for the purposes of 105 CMR 700.012 because it carries a bona fide potential "
      "for abuse, on factors including addiction risk, known recreational use, known regular "
      "diversion for misuse, and known contribution to overdose. Upon making such a determination "
      "the Commissioner shall notify all dispensers that they must begin to report the dispensing of "
      "that additional drug as directed in 105 CMR 700.012(A). The duty arrives with the "
      "determination and the notification.",
      {"A": "The factors guide the Commissioner's determination; the pharmacy does not make it.",
       "B": "Rescheduling would bring the drug in through 700.012(A)(1), but it is not what the additional-drug route requires.",
       "C": "A prescriber has no role in creating the reporting duty.",
       "D": "Correct: the Commissioner determines, then notifies all dispensers.",
       "E": "Evidence of diversion is one of the factors, not the operative event."},
      ["MA-PMP-ADDITIONAL-DRUG-DESIGNATION"],
      ["Identify the drug's current schedule and reporting status",
       "Locate who holds the power to designate an additional drug",
       "Wait for the determination and the notification before treating the duty as live"],
      ["Gabapentin is reported under this route rather than by rescheduling"],
      "The journal evidence tracks the statutory factors closely, which makes it feel like the "
      "trigger. The trigger is the Commissioner's act, not the evidence behind it."),
]

"""B3-E v2 expansion — 21 questions, MA-Q-0370 through MA-Q-0390.

Area 2 = 4, Area 3 = 10, Area 4 = 7. With the nine already authored at MA-Q-0361..0369 this brings
tranche B3-E to the full thirty identifiers Issue #91 reserved for it, composed Area 2 = 4,
Area 3 = 10, Area 4 = 16.

Every proposition was established in audits/controller/B3E-V2-EXPANSION-CENSUS.json BEFORE authoring
and each returned zero hits on a whole-bank novelty probe.

The four Area-2 questions occupy the SECOND final-bank slot of four families already approved in
AREA2-SOURCE-CENSUS.json. No cap is raised and no new Area-2 family is created. Each second slot
tests a materially different application, recorded family by family in the census.

None of the ten Area-3 questions is a refill-count or quantity-arithmetic item. The repetitive
Schedule-IV refill matrix that caused the S2 realism failures is deliberately not resurrected;
these are dispensing DECISION paths.

Structural targets, against the Phase-2 pool after B3-D v2 plus the existing nine:
  * 13 SBA / 8 SATA.
  * SBA keys A x3 / B x3 / D x3 / C x2 / E x2.
  * SATA correct-counts 2-correct x5 / 4-correct x3, no three-correct item.
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
    # ================= AREA 2 — second slots in approved families =================
    q("MA-Q-0370", 2, "PATIENT_PROFILE_REASONABLE_EFFORT_STANDARD", "Patient care", "Profile retrieval capability", 4, "SATA",
      "A Massachusetts pharmacy's computerized system cannot show what it previously dispensed to a patient until an "
      "overnight batch runs, so at the counter the pharmacist cannot see the patient's earlier fills. The pharmacy "
      "says its staff always ask patients thoroughly about their history. Which statements are correct? Select all "
      "that apply.",
      [("A", "Thorough questioning satisfies the retrieval requirement, since the goal is the same."),
       ("B", "The retrieval requirement is measured by reasonable effort, as the content duty is."),
       ("C", "The system must allow immediate retrieval when the prescription is presented."),
       ("D", "A pharmacy may rely on the overnight batch if it documents the limitation."),
       ("E", "Institutional sterile compounding pharmacies are outside these requirements.")],
      ["C", "E"],
      "247 CMR 9.16(7) states two duties of different character. The CONTENT duty is qualified by reasonable effort, "
      "but the system duty is not: the computerized pharmacy system SHALL provide for the IMMEDIATE RETRIEVAL of "
      "information necessary to identify previously dispensed drugs AT THE TIME THE PRESCRIPTION IS PRESENTED. "
      "247 CMR 9.16(8) excludes institutional sterile compounding pharmacies from 247 CMR 9.16 altogether.",
      {"A": "Questioning the patient goes to the content duty, not to the system capability.",
       "B": "The reasonable-effort standard qualifies the content duty only.",
       "C": "Correct: immediate retrieval at the time of presentation.",
       "D": "Documenting a limitation does not satisfy an unqualified requirement.",
       "E": "Correct: the section does not apply to them."},
      ["MA-PATIENT-PROFILE-DUTY"],
      ["Separate the effort-qualified content duty from the unqualified system duty",
       "Apply the immediate-retrieval requirement to the batch delay",
       "Apply the institutional sterile compounding carve-out"],
      ["The content duty reaches allergies, reactions, dispensed medications and pharmacist comments"],
      "Candidates carry the reasonable-effort standard across the whole paragraph and excuse a system that cannot "
      "retrieve in time."),

    q("MA-Q-0371", 2, "CPA_VALID_CONSTITUTION_AND_BIENNIAL_CURRENCY", "Collaborative practice", "Currency of the agreement", 4, "SBA",
      "A Massachusetts collaborative practice agreement was properly written, signed and within the supervising "
      "physician's scope when it was made twenty-six months ago. Neither party has reviewed it since. The pharmacist "
      "proposes to keep co-managing referred patients while a review is scheduled. What is the position?",
      [("A", "The agreement stands, because nothing in it has changed since it was signed."),
       ("B", "The agreement stands, provided the pharmacist documents that a review is pending."),
       ("C", "The agreement stands until the supervising physician gives notice of termination."),
       ("D", "The agreement is out of currency, because review and renewal fall due biennially."),
       ("E", "The agreement is void, and every act taken under it in month 25 must be reported.")],
      ["D"],
      "The M.G.L. c. 112, s. 24B1/2(a) definition provides that each collaborative practice agreement SHALL BE "
      "SUBJECT TO REVIEW AND RENEWAL ON A BIENNIAL BASIS. Valid constitution at the outset does not keep an "
      "agreement current; the biennial review is a continuing condition, and twenty-six months without one leaves "
      "the agreement outside it.",
      {"A": "Currency is a separate requirement from constitution.",
       "B": "A pending review is not a review.",
       "C": "Termination by the physician is a different event from lapse of currency.",
       "D": "Correct: the biennial review and renewal condition has not been met.",
       "E": "The statute imposes no reporting duty of that kind here."},
      ["MA-CPA-CONSTITUTION-CURRENCY"],
      ["Confirm the agreement was validly constituted",
       "Apply the separate biennial review and renewal condition",
       "Measure the elapsed period against it"],
      ["The agreement must also include individually developed prescriptive guidelines"],
      "Candidates check the formation requirements, find them satisfied, and never ask whether the instrument is "
      "still current."),

    q("MA-Q-0372", 2, "COUNSELLING_OFFER_METHOD_AND_CONTAINER_LABEL", "Patient care", "Method of the offer", 4, "SBA",
      "A Massachusetts pharmacy makes its offer to counsel by printing a line on the receipt inviting the patient to "
      "ask for the pharmacist. Its manager says the statute leaves the method open so long as the patient learns the "
      "offer is available. A second patient that day is deaf and cannot use the telephone. What does the statute "
      "provide?",
      [("A", "Any method reaching the patient qualifies, so the receipt line is sufficient."),
       ("B", "The offer is made face to face or by telephone, with an alternative where needs require."),
       ("C", "The offer must be made face to face in every case, so the telephone is not available."),
       ("D", "A printed offer qualifies where the pharmacy also posts a patient rights sign."),
       ("E", "The pharmacy may decline to counsel the second patient because of the barrier.")],
      ["B"],
      "M.G.L. c. 94C, s. 21A provides that the offer shall be made EITHER by face to face communication between the "
      "pharmacist or the pharmacist's designee and the patient, OR by telephone, EXCEPT WHEN THE PATIENT'S NEEDS OR "
      "AVAILABILITY REQUIRE AN ALTERNATIVE METHOD. The named methods are the rule and the alternative is a "
      "needs-driven exception, not a general licence.",
      {"A": "The statute names the methods rather than leaving them open.",
       "B": "Correct: two named methods plus a needs-driven alternative.",
       "C": "The telephone is expressly available.",
       "D": "The rights sign is a separate requirement and does not change the method.",
       "E": "A patient's needs open the alternative method rather than excusing the offer."},
      ["MA-COUNSELING-OFFER-METHOD"],
      ["Read the two methods the statute names",
       "Read the exception and note that it is triggered by the patient's needs or availability",
       "Apply it to the deaf patient rather than treating the barrier as an excuse"],
      ["A designee may make the offer, though only a pharmacist or intern may counsel"],
      "Candidates read the exception as making every method acceptable, when it is available only where the "
      "patient's needs or availability require it."),

    q("MA-Q-0373", 2, "PROSPECTIVE_DRUG_REVIEW_MANDATORY_VS_MENU", "Patient care", "Setting carve-out", 5, "SATA",
      "A Massachusetts hospital pharmacy dispenses to inpatients on the wards and also operates an outpatient window "
      "in the lobby. Its director asks which prospective drug review and counselling duties under the statute apply "
      "where. Which statements are correct? Select all that apply.",
      [("A", "The section applies in full to inpatients, since the pharmacy is licensed by the Board."),
       ("B", "The section does not apply to a drug dispensed to an inpatient at a hospital."),
       ("C", "The inpatient carve-out yields where federal regulations require otherwise."),
       ("D", "The carve-out reaches the outpatient window as well, since it is the same pharmacy."),
       ("E", "A nursing home dispensing falls outside the carve-out, which names hospitals alone.")],
      ["B", "C"],
      "The final paragraph of M.G.L. c. 94C, s. 21A provides that the section SHALL NOT APPLY to any drug dispensed "
      "to an INPATIENT AT A HOSPITAL OR NURSING HOME, EXCEPT to the extent required by regulations promulgated by "
      "the federal Health Care Financing Administration under 42 USC 1396r-8. The carve-out turns on the patient's "
      "inpatient status, not on the pharmacy's licence, and it names nursing homes alongside hospitals.",
      {"A": "The carve-out is drawn by patient status rather than by who holds the licence.",
       "B": "Correct: inpatient dispensings are outside the section.",
       "C": "Correct: the federal exception is expressly preserved.",
       "D": "Outpatient dispensings remain inside the section.",
       "E": "Nursing homes are named in the carve-out alongside hospitals."},
      ["MA-PROSPECTIVE-REVIEW-MANDATE"],
      ["Read the carve-out as turning on inpatient status",
       "Note that nursing homes are named alongside hospitals",
       "Preserve the federal exception"],
      ["The review is otherwise owed before each new prescription is dispensed or delivered"],
      "Candidates apply the carve-out to the whole pharmacy rather than to the inpatient dispensings within it."),

    # ================= AREA 3 — dispensing decision paths =================
    q("MA-Q-0374", 3, "B3E2_LABEL_PRINTING_AND_EMERGENCY", "Dispensing requirements", "Label production", 4, "SBA",
      "A Massachusetts pharmacy's label printer fails on a Saturday afternoon with patients waiting. The pharmacist "
      "writes labels by hand, in clear block capitals, for the remainder of the shift and again on Monday because the "
      "queue is long, although the printer was repaired that morning. How should the two days be assessed?",
      [("A", "Saturday is permitted as an emergency period; Monday is not."),
       ("B", "Both days are permitted, because each label was legibly written."),
       ("C", "Both days fail, because a label must always be computer printed."),
       ("D", "Saturday fails as well, unless the Board approved the handwriting in advance."),
       ("E", "Monday is permitted, because a queue is itself an emergency for this purpose.")],
      ["A"],
      "247 CMR 9.04(3) requires the label to be clearly printed by a computerized pharmacy system, and permits a "
      "legibly handwritten or typed label only IN THE EVENT OF PRINTING OR EQUIPMENT FAILURE and only DURING AN "
      "EMERGENCY PERIOD. Saturday's printer failure opens the exception; Monday's workload does not, because the "
      "equipment was working.",
      {"A": "Correct: the exception is tied to the failure and to its period.",
       "B": "Legibility is a condition of the exception, not a substitute for it.",
       "C": "The regulation expressly provides for the failure case.",
       "D": "No advance Board approval is contemplated.",
       "E": "A queue is not a printing or equipment failure."},
      ["MA-RX-LABEL-PRINTING"],
      ["Identify whether a printing or equipment failure existed on each day",
       "Confine the exception to the emergency period",
       "Treat workload as outside the trigger"],
      ["The computerized pharmacy system is separately required for processing and profiles"],
      "Candidates read legibility as the whole test and forget the exception has a trigger."),

    q("MA-Q-0375", 3, "B3E2_NDC_RECORDING_FALLBACK", "Dispensing requirements", "Product identification record", 4, "SBA",
      "A Massachusetts pharmacist dispenses a product distributed solely under its generic name. The package carries "
      "no NDC number. The pharmacist can see the manufacturer's name on the carton and also has the repacker's name "
      "on the invoice. What must be recorded in the computerized pharmacy system?",
      [("A", "Either name, since the purpose is to identify the product dispensed."),
       ("B", "The repacker's name, which is the entity that supplied this pharmacy."),
       ("C", "Both names, so that the chain of supply is recorded in full."),
       ("D", "The manufacturer's name, the repacker being a later fallback."),
       ("E", "Neither name; the pharmacist records the generic name and strength.")],
      ["D"],
      "247 CMR 9.04(7) sets an ordered fallback. Where a drug has been distributed solely under a generic name the "
      "pharmacist records the NDC number; if none exists, the NAME OF THE MANUFACTURER; and only IF THE "
      "MANUFACTURER'S NAME IS NOT AVAILABLE, the name of the distributor, packer or repacker. The manufacturer's "
      "name being available, it is the one to record.",
      {"A": "The regulation ranks the options rather than offering a choice.",
       "B": "The repacker is reached only when the manufacturer's name is unavailable.",
       "C": "The regulation calls for one identifier, taken in order.",
       "D": "Correct: the manufacturer's name is the next step after the NDC.",
       "E": "The generic name is what triggers the requirement, not what satisfies it."},
      ["MA-RX-NDC-RECORDING"],
      ["Confirm the drug was distributed solely under a generic name",
       "Work down the fallback chain in order",
       "Stop at the first available identifier"],
      ["The record is made in the computerized pharmacy system"],
      "Candidates treat the listed identifiers as alternatives rather than as a ranked sequence."),

    q("MA-Q-0376", 3, "B3E2_TELEPHONE_NEW_RX_RECEIPT", "Dispensing requirements", "Receipt of a telephoned prescription", 4, "SATA",
      "A prescriber's office telephones a Massachusetts pharmacy with a new prescription while the pharmacist on duty "
      "is counselling another patient. Which statements about who may take the call are correct? Select all that "
      "apply.",
      [("A", "Only the pharmacist may take a new prescription by telephone."),
       ("B", "Any pharmacy employee may take it and pass it to the pharmacist to check."),
       ("C", "A pharmacy intern may receive a new prescription over the telephone."),
       ("D", "An uncertified technician may take it provided the pharmacist verifies it afterwards."),
       ("E", "A certified technician with the on-duty pharmacist's approval may receive it.")],
      ["C", "E"],
      "247 CMR 9.04(8) provides that a pharmacy intern, or a CERTIFIED pharmacy technician WHO HAS THE APPROVAL OF "
      "THE PHARMACIST ON DUTY, may receive new prescriptions over the telephone from a prescriber or authorized "
      "agent. The technician limb carries two conditions and neither is satisfied by later verification.",
      {"A": "The regulation extends the function beyond the pharmacist.",
       "B": "It reaches interns and certified technicians, not any employee.",
       "C": "Correct: interns are named without further condition here.",
       "D": "Certification is required, and later verification does not supply it.",
       "E": "Correct: certification plus the on-duty pharmacist's approval."},
      ["MA-RX-TELEPHONE-RECEIPT"],
      ["Identify who the regulation names",
       "Apply the two conditions attached to the technician limb",
       "Reject after-the-fact verification as a cure"],
      ["The caller may be the prescriber or an authorized agent"],
      "Candidates split between assuming only pharmacists may take the call and assuming any technician may."),

    q("MA-Q-0377", 3, "B3E2_WITHIN_DATE_DAY_ONE", "Dispensing requirements", "Counting the validity period", 4, "SBA",
      "A Massachusetts prescription was written on 1 March. A patient presents it and the pharmacist must decide "
      "whether it is still within a thirty-day window. Which date is the last day on which it remains within date?",
      [("A", "30 March, counting 1 March as day one of the period."),
       ("B", "31 March, counting 2 March as day one of the period."),
       ("C", "1 April, because a partial first day is disregarded entirely."),
       ("D", "29 March, because both the first and the last day are excluded."),
       ("E", "It cannot be determined without knowing the schedule of the drug.")],
      ["B"],
      "247 CMR 9.04(10) provides that in order to determine whether a prescription is within date a pharmacist shall "
      "count THE DAY AFTER THE PRESCRIPTION WAS WRITTEN AS DAY ONE. With 1 March as the date written, 2 March is day "
      "one, so day thirty is 31 March.",
      {"A": "That counts the date of issue as day one, which the regulation excludes.",
       "B": "Correct: day one is 2 March, so the thirtieth day is 31 March.",
       "C": "The regulation fixes the start precisely rather than disregarding a day.",
       "D": "Only the date written is excluded, not the final day.",
       "E": "The counting convention is general and does not vary by schedule."},
      ["MA-RX-DATE-COUNTING"],
      ["Apply the counting convention to fix day one",
       "Count forward the length of the period",
       "Note that the convention does not vary by schedule"],
      ["The length of the window is set by the provision governing that drug"],
      "Candidates start counting on the date the prescription was written, which shifts every boundary by a day."),

    q("MA-Q-0378", 3, "B3E2_OFFSITE_PROCESSING_VERIFICATION", "Dispensing requirements", "Processing outside the premises", 5, "SBA",
      "A Massachusetts pharmacy receives filled and labelled vials from a central facility in another state that is "
      "not licensed by the Board. On arrival the pharmacist inspects each vial against the prescription and finds "
      "everything correct. May the pharmacy dispense them?",
      [("A", "Yes, because the pharmacist has personally checked each finished product."),
       ("B", "Yes, because central fill is a recognised part of ordinary pharmacy practice."),
       ("C", "No, unless the process was verified by a Massachusetts licensed pharmacist."),
       ("D", "No, because a pharmacy may never dispense what it did not process itself."),
       ("E", "No, unless the receiving pharmacy documents the inspection in the patient profile.")],
      ["C"],
      "247 CMR 9.04(11) bars a pharmacy from dispensing medication PROCESSED OUTSIDE ITS LICENSED PHARMACY PREMISES "
      "unless the PROCESS was VERIFIED BY A MASSACHUSETTS LICENSED PHARMACIST or was PERFORMED IN A PHARMACY "
      "LICENSED BY THE BOARD. The facility is not Board-licensed, so the second route is closed, and inspecting the "
      "finished product is not verification of the process.",
      {"A": "The requirement attaches to the process, not to the finished product.",
       "B": "Recognition of the practice does not remove the regulatory condition.",
       "C": "Correct: that is the first of the two available routes.",
       "D": "Off-premises processing is permitted on either of the two conditions.",
       "E": "Documentation does not supply the missing verification."},
      ["MA-RX-OFFSITE-PROCESSING"],
      ["Identify that the processing occurred off the licensed premises",
       "Test the facility against the Board-licensed route",
       "Test the arrangement against the Massachusetts pharmacist verification route"],
      ["The two routes are alternatives; either one satisfies the regulation"],
      "Candidates treat a careful check of the finished product as equivalent to verifying how it was made."),

    q("MA-Q-0379", 3, "B3E2_CUSTOMER_IDENTIFIER_HARDSHIP", "Dispensing requirements", "Positive identification", 5, "SATA",
      "An agent collecting a Schedule IV prescription for a housebound Massachusetts patient has no government "
      "identification with her. The pharmacist believes refusing would cause the patient real hardship. Which "
      "statements about dispensing without a Customer Identifier are correct? Select all that apply.",
      [("A", "The pharmacist's belief about hardship is by itself sufficient."),
       ("B", "The reason for dispensing without an identifier must be documented."),
       ("C", "A regular patient known to the pharmacy is outside the requirement."),
       ("D", "The agent must print her name and address and sign for the dispensing."),
       ("E", "The requirement reaches Schedule VI dispensings on the same terms.")],
      ["B", "D"],
      "247 CMR 9.04(14)(c) permits dispensing without a Customer Identifier only where the licensee has reason to "
      "believe refusal would cause SERIOUS HARDSHIP AND DOCUMENTS THE REASON, AND the ultimate user or agent PRINTS "
      "name and address on the reverse of the prescription or in a prescription log AND SIGNS. The requirement "
      "itself reaches Schedules II through V and designated additional drugs, not Schedule VI generally.",
      {"A": "The belief is one of three cumulative conditions.",
       "B": "Correct: the reason must be documented.",
       "C": "Familiarity is not an exception the regulation recognises.",
       "D": "Correct: printed name and address plus signature.",
       "E": "The requirement is drawn on Schedules II through V and additional drugs."},
      ["MA-RX-CUSTOMER-IDENTIFIER"],
      ["Confirm the dispensing is within the schedules the requirement reaches",
       "Treat the hardship belief as one condition of three",
       "Apply the documentation and signature conditions"],
      ["The Commissioner may waive the requirement for refills or deliveries"],
      "Candidates stop at the hardship belief and dispense without the documentation and signature that go with it."),

    q("MA-Q-0380", 3, "B3E2_PHARMACIST_CONTAINER_LABEL", "Dispensing requirements", "Container label contents", 4, "SATA",
      "A Massachusetts pharmacist is filling a written prescription for a controlled substance dispensed as capsules. "
      "Which items must appear on the label the pharmacist affixes to the container? Select all that apply.",
      [("A", "The prescribing practitioner's registration number."),
       ("B", "The filling pharmacist's initials."),
       ("C", "The serial number of the prescription."),
       ("D", "The number of capsules in the container."),
       ("E", "The date of filling, and the pharmacy name and address.")],
      ["B", "C", "D", "E"],
      "M.G.L. c. 94C, s. 21 requires the pharmacist filling a controlled-substance prescription to affix a label "
      "showing the date of filling, the pharmacy name and address, the FILLING PHARMACIST'S INITIALS, the SERIAL "
      "NUMBER of the prescription, the patient's name, the prescribing practitioner's name, the name of the "
      "controlled substance, directions and cautionary statements, and where dispensed as tablets or capsules the "
      "NUMBER of them in the container. The practitioner's registration number belongs on the prescription under "
      "s. 22, not on the pharmacist's label.",
      {"A": "That is a prescription requirement under s. 22, not a label requirement.",
       "B": "Correct: the filling pharmacist's initials.",
       "C": "Correct: the prescription serial number.",
       "D": "Correct: the count is required for tablets and capsules.",
       "E": "Correct: date of filling with pharmacy name and address."},
      ["MA-CS-LABEL"],
      ["List what the pharmacist's label must carry",
       "Separate it from what the practitioner's prescription must state",
       "Note the count requirement peculiar to tablets and capsules"],
      ["The practitioner's own dispensing label is governed separately by s. 22(b)"],
      "Candidates merge the prescription contents and the label contents into a single list."),

    q("MA-Q-0381", 3, "B3E2_LARGE_PRINT_DIRECTIONS", "Dispensing requirements", "Accessible label directions", 4, "SBA",
      "An eighty-two year old Massachusetts patient collects a prescription and says nothing about the label. The "
      "pharmacy's policy is to print all labels in its standard size. A second patient the same day asks for larger "
      "directions because of impaired vision. What does the statute require?",
      [("A", "Nothing for the first patient; typed directions at no more than ten characters per inch for the second."),
       ("B", "Enlarged directions for both, since the first patient is plainly elderly."),
       ("C", "Nothing for either, because the statute governs the pharmacy's own type standard."),
       ("D", "Enlarged directions for the second patient only if a prescriber orders them."),
       ("E", "Enlarged print across the entire label for the second patient, not the directions alone.")],
      ["A"],
      "M.G.L. c. 94C, s. 21 provides that UPON THE REQUEST of an elderly person as defined in M.G.L. c. 19A, s. 14, "
      "or of a person who is visually impaired, the DIRECTIONS on the label shall be typed in a print size allowing "
      "NO MORE THAN TEN CHARACTERS PER INCH. The duty is triggered by the request, and it reaches the directions.",
      {"A": "Correct: request-triggered, and limited to the directions.",
       "B": "Age without a request does not trigger the duty.",
       "C": "The statute imposes a specific standard on request.",
       "D": "No prescriber order is required.",
       "E": "The statute names the directions rather than the whole label."},
      ["MA-RX-LARGE-PRINT-DIRECTIONS"],
      ["Ask whether a request was made",
       "Apply the character-density standard to the directions",
       "Note that the standard is a maximum density rather than a minimum size"],
      ["The ordinary label contents are governed by the first paragraph of the same section"],
      "Candidates make the duty automatic on apparent age and miss that the statute turns on a request."),

    q("MA-Q-0382", 3, "B3E2_ORAL_RX_VERIFY_AND_FOLLOWUP", "Controlled prescriptions", "Oral prescription follow-up", 5, "SBA",
      "A Massachusetts pharmacist takes an oral controlled-substance prescription from a caller she has never dealt "
      "with, reduces it to writing at once, and dispenses. Eight days later no electronic prescription has arrived "
      "and the prescriber holds no commissioner exception from electronic prescribing. What has gone wrong?",
      [("A", "Nothing; the pharmacist's written record is the complete requirement."),
       ("B", "Only that the pharmacist should have refused an oral prescription outright."),
       ("C", "Only that the written record should have been made within two days rather than at once."),
       ("D", "The pharmacist should have obtained the prescription in writing before dispensing."),
       ("E", "No reasonable effort was made to verify the caller, and the two-day follow-up has lapsed.")],
      ["E"],
      "M.G.L. c. 94C, s. 20(b) requires the pharmacist, where the prescribing practitioner is NOT KNOWN to her, to "
      "make a REASONABLE EFFORT to determine that the oral authorization came from a registered practitioner. "
      "Section 20(c) requires the practitioner to cause an ELECTRONIC prescription to reach the dispensing pharmacy "
      "WITHIN 2 DAYS, the seven-day written route being available only where the commissioner has granted an "
      "exception. Both limbs have failed here.",
      {"A": "The written record answers s. 20(a) only.",
       "B": "Oral prescriptions are permitted in the circumstances the statute allows.",
       "C": "Reducing to writing immediately is what s. 20(a) requires.",
       "D": "That would defeat the oral prescription route entirely.",
       "E": "Correct on both the verification duty and the follow-up window."},
      ["MA-ORAL-CONTROLLED-DOCUMENTATION"],
      ["Note that the caller was unknown to the pharmacist",
       "Apply the reasonable-effort verification duty",
       "Apply the two-day electronic follow-up, the seven-day route needing an exception"],
      ["The pharmacy attaches the follow-up prescription to the record it reduced to writing"],
      "Candidates treat the written record as the whole of the oral prescription procedure."),

    q("MA-Q-0383", 3, "B3E2_CII_PHARMACIST_ENDORSEMENT", "Controlled prescriptions", "Schedule II endorsement and filing", 4, "SBA",
      "A Massachusetts pharmacy fills a written Schedule II prescription. The technician files it with the Schedule "
      "III and IV prescriptions, and the label carries the filling pharmacist's initials but the prescription itself "
      "bears no signature other than the prescriber's. What is missing?",
      [("A", "Nothing; the initials on the label record who filled the prescription."),
       ("B", "Only the separate file, the prescriber's signature being the one required."),
       ("C", "Only the pharmacist's endorsement, Schedule II filing being at the pharmacy's discretion."),
       ("D", "A second pharmacist's countersignature verifying the Schedule II dispensing."),
       ("E", "The filling pharmacist's endorsement on the face, and the separate Schedule II file.")],
      ["E"],
      "M.G.L. c. 94C, s. 23(c) requires the pharmacist filling a written or electronic Schedule II prescription to "
      "ENDORSE HIS OWN SIGNATURE ON THE FACE of it, and s. 23(b) requires written Schedule II prescriptions to be "
      "KEPT IN A SEPARATE FILE. Initials on the label do not discharge the endorsement, and the filing requirement "
      "is not discretionary.",
      {"A": "The endorsement goes on the face of the prescription, not on the label.",
       "B": "The statute requires the filling pharmacist's signature as well.",
       "C": "The separate file is required, not optional.",
       "D": "No countersignature by a second pharmacist is required.",
       "E": "Correct on both the endorsement and the separate file."},
      ["MA-CII-PHARMACIST-ENDORSEMENT"],
      ["Identify the signature the statute requires and whose it is",
       "Distinguish the label initials from the endorsement on the face",
       "Apply the separate-file requirement"],
      ["A Schedule II prescription may not be refilled"],
      "Candidates accept the label initials as the record of who filled it and never look at the face of the "
      "prescription."),

    # ================= AREA 4 — facility, security and licensure =================
    q("MA-Q-0384", 4, "B3E2_CS_PERSONNEL_SCREENING", "Controlled substance security", "Personnel screening", 4, "SBA",
      "A Massachusetts pharmacy wants to hire a warehouse assistant who will work beside the controlled-substance "
      "cage. Eleven years ago his own registration was revoked for a regulatory violation; he has worked without "
      "incident since. The pharmacy proposes to hire him and document the history. What does the regulation permit?",
      [("A", "Hiring is permitted, because eleven incident-free years have passed."),
       ("B", "Hiring is permitted if the pharmacy keeps him away from the cage itself."),
       ("C", "Hiring is permitted once the Commissioner is notified of the history."),
       ("D", "Hiring is barred, because a revoked registration disqualifies him at any time."),
       ("E", "Hiring is barred unless a second registrant vouches for his trustworthiness.")],
      ["D"],
      "105 CMR 700.005(B)(2) provides that NO REGISTRANT SHALL KNOWINGLY EMPLOY any agent or employee who has had an "
      "application for registration denied for violation of any law or regulation, or has had their registration "
      "REVOKED for violation of any law or regulation, AT ANY TIME. The bar carries no look-back period and no cure.",
      {"A": "The words at any time exclude a look-back limit.",
       "B": "The screening duty reaches those who work in or around such areas.",
       "C": "Notification is not a route around the bar.",
       "D": "Correct: the prohibition is absolute.",
       "E": "No vouching mechanism exists."},
      ["MA-CS-PERSONNEL-SCREENING"],
      ["Identify the disqualifying event",
       "Note the absence of any look-back limit",
       "Treat the prohibition as absolute rather than rebuttable"],
      ["Screening documentation must be available to the Commissioner on request"],
      "Candidates assume an old regulatory event fades, as it would under many licensing schemes."),

    q("MA-Q-0385", 4, "B3E2_CLOSURE_DUTIES_BY_TYPE", "Pharmacy licensure", "Closure duties by pharmacy type", 5, "SATA",
      "Three Massachusetts-licensed pharmacies are closing on the same date: a non-resident Drug Store pharmacy, a "
      "resident sterile compounding pharmacy, and an institutional sterile compounding pharmacy. Which statements are "
      "correct? Select all that apply.",
      [("A", "Each must give the Board certified written notice at least 14 days before closing."),
       ("B", "The non-resident pharmacy must make the post-closure submission of original licences."),
       ("C", "The sterile compounding pharmacy must identify a pharmacy able to continue patient care."),
       ("D", "The institutional sterile compounding pharmacy is excused from the patient-notice duty."),
       ("E", "The continuity-of-care pharmacy identified must be licensed by the Board.")],
      ["A", "C", "D", "E"],
      "247 CMR 6.13 requires certified written notice at least 14 days ahead from resident and non-resident "
      "pharmacies alike. 6.13(3) additionally requires a compounding pharmacy to notify the Board of the identity of "
      "a pharmacy LICENSED BY THE BOARD that is suitable and available to provide CONTINUITY OF CARE. 6.13(6) "
      "expressly does NOT apply to non-resident pharmacies, and 6.13(7) excuses institutional sterile compounding "
      "pharmacies from 6.13(3) and 6.13(4).",
      {"A": "Correct: the 14-day certified notice is common to both.",
       "B": "The post-closure submission does not apply to non-resident pharmacies.",
       "C": "Correct: the continuity-of-care identification.",
       "D": "Correct: 6.13(7) excuses them from the patient-notice duty.",
       "E": "Correct: the identified pharmacy must be Board-licensed."},
      ["MA-CLOSURE-DUTIES-BY-TYPE"],
      ["Take each pharmacy type separately",
       "Apply the common 14-day certified notice",
       "Apply the type-specific additions and carve-outs"],
      ["A resident pharmacy's post-closure submission is due within 14 days of closure"],
      "Candidates apply one closure checklist uniformly and miss three type-specific variations."),

    q("MA-Q-0386", 4, "B3E2_PHARMACY_RELOCATION", "Pharmacy licensure", "Relocation", 4, "SBA",
      "A Massachusetts pharmacy has signed a lease on premises two doors along and plans to move in five weeks. Its "
      "manager will write to the Board a week beforehand describing the new layout. What does the regulation "
      "require?",
      [("A", "Written notice a week ahead is sufficient for a move within the same block."),
       ("B", "Board approval before relocating, on an application filed at least 90 days ahead."),
       ("C", "Board approval before relocating, on an application filed at least 14 days ahead."),
       ("D", "Nothing before the move, provided the new address is reported within 14 days."),
       ("E", "A fresh licence application, the existing licence lapsing on the day of the move.")],
      ["B"],
      "247 CMR 6.16 requires a pharmacy to APPLY TO THE BOARD FOR APPROVAL to relocate PRIOR TO RELOCATING and "
      "provides it MAY NOT RELOCATE UNTIL IT RECEIVES APPROVAL. The application is submitted AT LEAST 90 DAYS before "
      "the desired relocation date unless the Board approves otherwise, with the fee and blueprints or equivalent "
      "architectural drawings.",
      {"A": "Distance does not alter the requirement, and notice is not approval.",
       "B": "Correct: prior approval on a 90-day application.",
       "C": "Fourteen days is the closure notice period, not the relocation lead time.",
       "D": "The move may not happen before approval.",
       "E": "The regulation contemplates approval to relocate, not a lapse and reapplication."},
      ["MA-PHARMACY-RELOCATION"],
      ["Note that the regulation requires approval rather than notice",
       "Apply the 90-day application lead time",
       "Note the prohibition on relocating before approval"],
      ["The application carries the fee and drawings depicting the pharmacy layout"],
      "Candidates borrow the familiar 14-day closure period and treat the move as a notification."),

    q("MA-Q-0387", 4, "B3E2_REMODEL_PRIOR_APPROVAL", "Pharmacy licensure", "Remodeling and configuration", 4, "SBA",
      "A Massachusetts Drug Store pharmacy is enlarging its prescription area by taking in an adjoining storeroom. "
      "The contractor is ready and the pharmacy files its application on the morning work is due to begin, enclosing "
      "drawings of the new prescription area. What is wrong?",
      [("A", "Work may not commence until approval, and the counselling area must be depicted too."),
       ("B", "Nothing, provided the pharmacy stops work if the Board later raises an objection."),
       ("C", "Only that the drawings must be certified by an architect for a Drug Store pharmacy."),
       ("D", "Only that a change of square footage requires a fresh licence rather than approval."),
       ("E", "Only that the application should have gone to the Department rather than the Board.")],
      ["A"],
      "247 CMR 6.15(1) provides that a pharmacy shall apply for approval to remodel or change configuration or "
      "square footage and MAY NOT COMMENCE ANY CONSTRUCTION WORK OR REMODELING until it receives approval. Under "
      "6.15(3) the drawings must depict the pharmacy layout, the prescription area AND THE COUNSELING AREA, and a "
      "Massachusetts pharmacy must also submit a written plan to maintain security of controlled substances during "
      "any transportation.",
      {"A": "Correct on both the timing and the missing counselling area.",
       "B": "The prohibition bites before work starts, not after an objection.",
       "C": "Certified blueprints are required of compounding pharmacies, not of a Drug Store pharmacy here.",
       "D": "The regulation calls for approval, not a fresh licence.",
       "E": "The application goes to the Board."},
      ["MA-PHARMACY-REMODEL-APPROVAL"],
      ["Apply the prohibition on commencing work before approval",
       "Check the drawings against the three areas the regulation names",
       "Note the controlled substance transportation security plan"],
      ["A Massachusetts pharmacy must submit the transport security plan"],
      "Candidates treat filing as the trigger and start work while the application is pending."),

    q("MA-Q-0388", 4, "B3E2_ENGINEERING_CONTROL_APPROVAL", "Compounding", "Secondary engineering controls", 5, "SATA",
      "A Massachusetts sterile compounding pharmacy is replacing an ageing cleanroom air handling unit with an "
      "identical new one in the same position. Its director says a like-for-like swap changes nothing and needs no "
      "filing. Which statements are correct? Select all that apply.",
      [("A", "A like-for-like replacement falls outside the approval requirement."),
       ("B", "Board approval is required before replacing any secondary engineering control."),
       ("C", "Ordinary layout drawings suffice, since the configuration is unchanged."),
       ("D", "The submission includes certified blueprints with ISO classification of each control."),
       ("E", "Approval may be sought after the work if the pharmacy suspends compounding.")],
      ["B", "D"],
      "247 CMR 6.15(2) requires a sterile compounding pharmacy to apply for Board approval PRIOR TO MOVING, ADDING, "
      "MODIFYING, REMOVING OR REPLACING ANY SECONDARY ENGINEERING CONTROL and bars it from doing so until approval "
      "is received. Under 6.15(4) the submission includes CERTIFIED blueprints depicting compounding areas and the "
      "location and ISO CLASSIFICATION of each primary and secondary engineering control, a containment strategy, an "
      "environmental monitoring plan, a re-certification plan and a continuity of care plan, each as applicable.",
      {"A": "Replacing is one of the five verbs the regulation names.",
       "B": "Correct: prior approval is required.",
       "C": "Certified blueprints with ISO classification are required.",
       "D": "Correct: that is the first item on the list.",
       "E": "The approval must precede the work."},
      ["MA-ENGINEERING-CONTROL-APPROVAL"],
      ["Test the proposed work against the five verbs the regulation names",
       "Apply the prior-approval requirement",
       "Identify the heavier submission the compounding setting attracts"],
      ["A re-certification plan and a continuity of care plan are included as applicable"],
      "Candidates reason from whether the configuration changes rather than from whether a control is touched."),

    q("MA-Q-0389", 4, "B3E2_MOR_CHANGE_INVENTORY", "Pharmacy licensure", "Change of Manager of Record", 4, "SATA",
      "A Massachusetts pharmacy's Manager of Record is leaving amicably at the end of the month and a successor has "
      "been identified. Which statements about the change of Manager of Record application are correct? Select all "
      "that apply.",
      [("A", "The inventory attestation is signed by both the outgoing and the incoming Manager."),
       ("B", "The inventory covers Schedules II through V and reportable Schedule VI substances."),
       ("C", "A staff pharmacist may sign in place of the outgoing Manager for convenience."),
       ("D", "The original Drug Store Pharmacy licence accompanies the application."),
       ("E", "The Board may require the proposed Manager of Record to appear before it.")],
      ["A", "B", "D", "E"],
      "247 CMR 6.10(2) requires an attestation confirming an inventory of all Schedule II through V substances and "
      "Schedule VI substances required to be reported to the prescription monitoring program, SIGNED BY THE OUTGOING "
      "AND THE PROPOSED INCOMING Manager of Record, together with the ORIGINAL Drug Store Pharmacy licence and the "
      "fees. A staff pharmacist may sign only where the outgoing Manager is unavailable through DEATH, SERIOUS "
      "ILLNESS OR TERMINATION, on notice of the reason. Under 6.10(1) the Board may require the proposed Manager to "
      "appear.",
      {"A": "Correct: both signatures.",
       "B": "Correct: reportable Schedule VI is inside the inventory.",
       "C": "The substitution is confined to death, serious illness or termination.",
       "D": "Correct: the original licence accompanies it.",
       "E": "Correct: the Board may require an appearance."},
      ["MA-MOR-CHANGE-INVENTORY"],
      ["Identify who must sign the attestation",
       "Check what the inventory must cover",
       "Confine the staff-pharmacist substitution to the stated circumstances"],
      ["The Board may find a proposed Manager of Record unsuitable on stated factors"],
      "Candidates treat the departing manager as out of the picture once notice is given."),

    q("MA-Q-0390", 4, "B3E2_PHARMACY_NAME_CHANGE", "Pharmacy licensure", "Notification of a name change", 3, "SBA",
      "A Massachusetts pharmacy rebrands and begins trading under a new name on 1 June. The licence holder, the "
      "premises and the ownership are all unchanged. The manager plans to mention the new name in the pharmacy's "
      "next annual renewal filing in November. What does the regulation require?",
      [("A", "Nothing further, since the licence holder and premises are unchanged."),
       ("B", "Notice at the next renewal, which is what the regulation contemplates."),
       ("C", "Written notice to the Board within 14 days, with authorizing documentation."),
       ("D", "Written notice to the Board within 90 days, as for a change of location."),
       ("E", "A fresh licence application, the old trading name having been surrendered.")],
      ["C"],
      "247 CMR 6.12 requires a licensee to notify the Board WITHIN 14 DAYS, IN WRITING, of any change in the NAME "
      "UNDER WHICH THE PHARMACY OPERATES, accompanied by appropriate authorizing documentation. The requirement is "
      "not displaced by continuity of the licence holder, the premises or the ownership.",
      {"A": "The regulation is directed at the operating name itself.",
       "B": "The clock runs from the change, not to the renewal.",
       "C": "Correct: 14 days, in writing, with authorizing documentation.",
       "D": "Ninety days is the relocation lead time.",
       "E": "No fresh licence application is required for a name change."},
      ["MA-PHARMACY-NAME-CHANGE"],
      ["Identify the change as one in the operating name",
       "Apply the 14-day written notice requirement",
       "Note the authorizing documentation that must accompany it"],
      ["Relocation is separately governed and carries a 90-day lead time"],
      "Candidates treat a rebrand as cosmetic because nothing about the licence or the premises has moved."),
]

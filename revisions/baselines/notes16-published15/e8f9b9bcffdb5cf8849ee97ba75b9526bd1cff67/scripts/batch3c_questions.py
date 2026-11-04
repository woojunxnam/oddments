"""Batch 3 tranche B3-C — 33 Area-2 questions, MA-Q-0295 through MA-Q-0327.

Every question comes from a family approved in AREA2-SOURCE-CENSUS.json and allocated in
BATCH3-CD-AREA2-ALLOCATION.json. Five families carry two questions; each pair is separated by a
stated material difference in application, never by a paraphrase or a cosmetic swap:

  CDTM_AGREEMENT_COPY_VERSUS_ORIGINAL_CUSTODY   what the pharmacist holds  /  to whom it is
                                                retrievable and who holds the original
  CDTM_DELEGATION_MUST_BE_SPECIFIED             silence is not permission  /  what else the
                                                agreement must state before a delegation is good
  CDTM_PATIENT_ELIGIBILITY_AND_DUAL_RECORDING   is this person a CDTM patient at all  /  who must
                                                record the referral and consent once they are
  CDTM_SCOPE_VS_DIAGNOSIS_BOUNDARY              what the authority includes  /  where it stops
  PRACTICE_HOUR_CEILING_AND_REST_PERIOD         may the shift continue  /  what is owed afterwards

Structural targets built into the tranche, measured against the released bank at authoring time
(165 SBA, 98 SATA, answer-position chi-square 1.7576, SATA three-correct share 52.0%):

  * 21 SBA / 12 SATA, holding the bank's SBA share near 63%.
  * SBA keys weighted E x7 / C x4 / D x4 / A x3 / B x3, which pulls the bank answer-position
    chi-square down toward 0.77.
  * SATA correct-counts 2-correct x7 / 3-correct x2 / 4-correct x3.
    A later correction rebalanced this: steering the three-correct share down tranche by
    tranche drove it to zero inside each one, which shuffling cannot hide because
    shuffleQuestionChoices preserves how many options are correct. See
    scripts/check_tranche_key_patterns.py; the counts below are the corrected, measured ones.
  * SATA correct positions spread A 4 / B 5 / C 7 / D 6 / E 10 with varied correct-sets, keeping
    every slot below the 25% concentration threshold.
"""

from __future__ import annotations


def q(qid, family, topic, subtopic, difficulty, qtype, stem, choices, correct,
      core, analysis, rules, steps, facts, trap):
    return {
        "question_id": qid,
        "family_id": family,
        "area": 2,
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
    q("MA-Q-0295", "ANTI_CIRCUMVENTION_STANDARD", "Professional conduct", "Circumvention of pharmacy law", 4, "SBA",
      "A Massachusetts pharmacy arranges a sequence of transfers so that a patient ends up holding a supply the "
      "pharmacy could not lawfully have dispensed to him directly. Each transfer in the sequence, taken on its own, "
      "complies with the governing rules, and every step is documented. How should the arrangement be assessed?",
      [("A", "No violation arises, because each step in the sequence independently complies."),
       ("B", "No violation arises, because the prohibition reaches only direct circumvention."),
       ("C", "A violation arises if the Board shows the patient was harmed by the supply."),
       ("D", "A violation arises if the pharmacy gained financially from the arrangement."),
       ("E", "A violation arises, because the manner was designed to circumvent the law.")],
      ["E"],
      "247 CMR 9.01(2) bars a licensee from processing a prescription, dispensing a drug, device or other substance, "
      "or administering a controlled substance or vaccine in a manner intended, either directly or INDIRECTLY, to "
      "circumvent any law or regulation governing the practice of pharmacy. The standard attaches to the manner and "
      "its design, so the lawfulness of each individual step is not the question.",
      {"A": "Step-wise compliance does not answer a prohibition aimed at the design of the whole.",
       "B": "Indirect circumvention is expressly within the prohibition.",
       "C": "Patient harm is not an element of the standard.",
       "D": "Financial gain is not an element of the standard.",
       "E": "Correct: the manner was intended to reach indirectly what could not be done directly."},
      ["MA-CONDUCT-ANTI-CIRCUMVENTION"],
      ["Identify what the pharmacy could not lawfully do directly",
       "Ask whether the arrangement was designed to reach that result",
       "Apply the indirect limb of 247 CMR 9.01(2) to the manner rather than to each step"],
      ["The prohibition covers processing, dispensing and administering alike"],
      "Candidates audit each step for legality and conclude that a chain of lawful steps must itself be lawful."),

    q("MA-Q-0296", "BLANK_PRESCRIPTION_FORM_PROHIBITION", "Professional conduct", "Prescriber forms", 3, "SBA",
      "A Massachusetts pharmacy has prescription pads printed with its own name and address and supplies them free of "
      "charge to a nearby prescriber. There is no agreement of any kind between them, nothing of value passes, and no "
      "patient is ever sent to the pharmacy as a result. What is the pharmacy's position?",
      [("A", "Compliant, because nothing of value passed to the prescriber."),
       ("B", "Compliant, because no patient was in fact steered to the pharmacy."),
       ("C", "Compliant, provided the prescriber stays free to send prescriptions elsewhere."),
       ("D", "In violation, because supplying forms that refer to a pharmacy is prohibited."),
       ("E", "In violation, but only where the forms are used for controlled substances.")],
      ["D"],
      "247 CMR 9.01(14) states that a licensee may not provide any practitioner with blank prescription forms which "
      "refer to any pharmacist or pharmacy. The violation is complete on providing the forms. Nothing turns on "
      "payment, on an agreement, or on whether any patient was actually steered.",
      {"A": "The prohibition has no remuneration element, unlike 247 CMR 9.01(11).",
       "B": "Actual steering is not required.",
       "C": "The prescriber's freedom of choice is irrelevant to the prohibition.",
       "D": "Correct: the pre-printed reference to the pharmacy is the violation.",
       "E": "The prohibition is not limited by schedule."},
      ["MA-BLANK-PRESCRIPTION-FORMS"],
      ["Identify that the forms carry a reference to a pharmacy",
       "Note that the pharmacy provided them to a practitioner",
       "Apply 247 CMR 9.01(14) without looking for value or for steering"],
      ["247 CMR 9.01(11) separately prohibits remuneration for referrals"],
      "Candidates import the remuneration element of the neighbouring anti-kickback provision into a prohibition that "
      "has none."),

    q("MA-Q-0297", "CDTM_AGREEMENT_COPY_VERSUS_ORIGINAL_CUSTODY", "Collaborative practice", "Custody of the agreement", 4, "SATA",
      "An authorized pharmacist practising collaborative drug therapy management in a Massachusetts community "
      "pharmacy is asked during an inspection to produce the collaborative practice documents. Which statements about "
      "what this pharmacist is required to hold are correct? Select all that apply.",
      [("A", "The pharmacist must hold the signed original rather than a copy."),
       ("B", "A copy of the current collaborative practice agreement must be maintained."),
       ("C", "Copies of the current patient referral and patient consent must be included."),
       ("D", "The documents must be maintained in the primary practice setting."),
       ("E", "The documents must be readily retrievable when they are requested.")],
      ["B", "C", "D", "E"],
      "247 CMR 16.04(6) requires an authorized pharmacist to maintain a COPY of the current CDTM agreement, including "
      "copies of the current patient referral and patient consent, in the primary practice setting, readily "
      "retrievable on request. The original belongs with the supervising physician under 243 CMR 2.12.",
      {"A": "The original is the supervising physician's to keep, in the patient's medical record.",
       "B": "Correct: a copy of the current agreement.",
       "C": "Correct: the referral and consent copies travel with the agreement.",
       "D": "Correct: the primary practice setting is the specified location.",
       "E": "Correct: ready retrievability on request is required."},
      ["MA-CDTM-AGREEMENT-CUSTODY"],
      ["Separate what the pharmacist holds from what the physician holds",
       "Note that the agreement alone is not enough without the referral and consent",
       "Apply the location and retrievability conditions in 247 CMR 16.04(6)"],
      ["243 CMR 2.12 places the original in the physician's custody"],
      "Candidates assume the more formal document, the signed original, must be the one the pharmacist keeps."),

    q("MA-Q-0298", "CDTM_AGREEMENT_COPY_VERSUS_ORIGINAL_CUSTODY", "Collaborative practice", "Retrievability and the original", 4, "SBA",
      "A Massachusetts collaborating pharmacist keeps the required documents on site. An investigator from the Board "
      "of Registration in Medicine asks to see them and the pharmacist answers that they are retrievable only to the "
      "Board of Registration in Pharmacy. Separately, the supervising physician has handed the pharmacist the "
      "original agreement for safekeeping. Which statement is correct?",
      [("A", "The pharmacist is right on retrievability and right to hold the original."),
       ("B", "The pharmacist is right on retrievability but should return the original."),
       ("C", "The pharmacist is wrong on retrievability and right to hold the original."),
       ("D", "Both boards may request the documents, and the physician may pass the original on."),
       ("E", "Both boards may request them, and the original belongs in the physician's record.")],
      ["E"],
      "247 CMR 16.04(6) requires the pharmacist's copy to be readily retrievable at the request of the Board of "
      "Registration in Pharmacy AND the Board of Registration in Medicine. The same paragraph, read with 243 CMR "
      "2.12, requires the supervising physician to maintain the original in the patient's medical record in the "
      "physician's own custody, so the original cannot be parked with the pharmacist.",
      {"A": "Both limbs are wrong.",
       "B": "The retrievability limb reaches both boards, not one.",
       "C": "The original does not belong with the pharmacist.",
       "D": "The custody of the original is fixed by regulation, not by arrangement between the parties.",
       "E": "Correct on both limbs."},
      ["MA-CDTM-AGREEMENT-CUSTODY"],
      ["Read the retrievability limb as naming two boards",
       "Read the custody limb as placing the original in the patient's medical record",
       "Conclude that neither point is open to private arrangement"],
      ["The pharmacist's copy sits in the primary practice setting"],
      "Candidates treat custody as a matter the two professionals may allocate between themselves."),

    q("MA-Q-0299", "CDTM_DELEGATION_MUST_BE_SPECIFIED", "Collaborative practice", "Delegation of duties", 4, "SATA",
      "A Massachusetts collaborating pharmacist wants an appropriately trained certified technician to collect the "
      "vital signs contemplated by her collaborative practice agreement. The agreement says nothing at all about "
      "delegation. Which statements are correct? Select all that apply.",
      [("A", "Silence in the agreement operates as permission to delegate the duty."),
       ("B", "Delegation is permitted because the technician is appropriately trained."),
       ("C", "Delegation is permitted because collecting vital signs is not a dispensing act."),
       ("D", "The agreement must specify which of the pharmacist's duties may be delegated."),
       ("E", "The agreement must specify which duties under it may not be delegated.")],
      ["D", "E"],
      "247 CMR 16.04(3) requires a collaborative practice agreement to specify those duties of the authorized "
      "pharmacist that MAY be delegated to other appropriately trained and authorized staff AND those duties under "
      "the agreement that SHALL NOT be delegated. An agreement that says nothing has not met either requirement, so "
      "there is no delegation power to exercise.",
      {"A": "The regulation requires affirmative specification, so silence is not permission.",
       "B": "Training is necessary but does not supply the missing agreement terms.",
       "C": "The nature of the task does not remove the requirement to specify.",
       "D": "Correct: the delegable duties must be named.",
       "E": "Correct: the non-delegable duties must also be named."},
      ["MA-CDTM-DELEGATION-TERMS"],
      ["Ask what the agreement must contain before any delegation is possible",
       "Note that both the delegable and the non-delegable duties must be specified",
       "Conclude that an agreement silent on delegation confers no delegation power"],
      ["Intern and technician support must still comply with 247 CMR 8.01 and 8.02 through 8.06"],
      "Candidates reason from the competence of the staff member rather than from the content of the agreement."),

    q("MA-Q-0300", "CDTM_DELEGATION_MUST_BE_SPECIFIED", "Collaborative practice", "Terms of a delegation", 4, "SBA",
      "A Massachusetts collaborative practice agreement names three duties of the authorized pharmacist that may be "
      "delegated and two that may not. It says nothing further on the subject. The pharmacist proposes to delegate "
      "one of the named duties to trained staff for the next six weeks. What does the agreement still lack?",
      [("A", "Nothing further, once the delegable and non-delegable duties have been named."),
       ("B", "Board approval of this particular delegation before it may take effect."),
       ("C", "The when and how of delegation, together with its duration and its scope."),
       ("D", "A separate written consent from the patient to the proposed delegation."),
       ("E", "The supervising physician's countersignature on the delegation itself.")],
      ["C"],
      "247 CMR 16.04(3) imposes a second requirement beyond naming the two categories of duty: the agreement shall "
      "specify WHEN AND HOW an authorized pharmacist may delegate duties under the agreement, and the DURATION AND "
      "SCOPE of the delegation. Naming the duties is only half of what the paragraph requires.",
      {"A": "The paragraph contains a further sentence imposing additional required terms.",
       "B": "No Board approval of an individual delegation is required.",
       "C": "Correct: the when, how, duration and scope must all appear in the agreement.",
       "D": "Patient consent to a delegation is not the requirement in issue.",
       "E": "A countersignature on the delegation is not required by the paragraph."},
      ["MA-CDTM-DELEGATION-TERMS"],
      ["Read past the first sentence of 247 CMR 16.04(3)",
       "Identify the four further particulars the agreement must state",
       "Measure the agreement against all of them"],
      ["The same paragraph preserves the ordinary intern and technician scope rules"],
      "Candidates stop at the first sentence of the paragraph and treat the naming of duties as the whole obligation."),

    q("MA-Q-0301", "CDTM_EMPLOYMENT_DIRECTION_AND_PURPOSE", "Collaborative practice", "Employment relationships", 4, "SBA",
      "A Massachusetts retail pharmacy proposes to engage a physician on two footings: to conduct quality assurance "
      "reviews of the pharmacists it employs who practise collaborative drug therapy management, and to enter into "
      "collaborative practice agreements with the pharmacy's patients. Which analysis is correct?",
      [("A", "Both engagements are permitted, since the pharmacy is not itself prescribing."),
       ("B", "Both engagements are prohibited, since a retail pharmacy may not employ a physician."),
       ("C", "The agreement engagement is permitted and the review engagement is prohibited."),
       ("D", "Both are permitted if the physician's pay is unrelated to prescription volume."),
       ("E", "The review engagement is permitted and the agreement engagement is prohibited.")],
      ["E"],
      "M.G.L. c. 112, s. 24B1/2(e), implemented at 247 CMR 16.04(7), bars a retail pharmacy from employing a "
      "physician FOR THE PURPOSE of maintaining, establishing or entering into a collaborative practice agreement, "
      "while expressly preserving the pharmacy's ability to hire a physician or licensed medical practitioner to "
      "conduct quality assurance reviews of its collaborating pharmacists.",
      {"A": "The statute regulates the employment relationship itself, not the act of prescribing.",
       "B": "The quality assurance engagement is expressly preserved.",
       "C": "This reverses the statute: the agreement purpose is the prohibited one.",
       "D": "Compensation structure is not the statutory test; purpose is.",
       "E": "Correct: purpose decides, and only the agreement purpose is barred."},
      ["MA-CDTM-EMPLOYMENT-RELATIONSHIPS"],
      ["Identify the purpose of each proposed engagement",
       "Match each purpose against the statutory prohibition and the carve-out",
       "Note that a physician group may in the reverse direction hire pharmacists"],
      ["A physician or physician group may hire pharmacists for collaborative practice"],
      "Candidates read the provision as a blanket bar on a pharmacy employing any physician."),

    q("MA-Q-0302", "CDTM_PATIENT_ELIGIBILITY_AND_DUAL_RECORDING", "Collaborative practice", "Patient eligibility", 4, "SATA",
      "A Massachusetts community pharmacist is asked to begin collaboratively managing a walk-in who says her "
      "physician mentioned that the pharmacy could help with her blood pressure. Nothing is in writing and the "
      "pharmacist has had no contact with the physician. Which statements are correct? Select all that apply.",
      [("A", "She is a collaborative patient because her own physician suggested it."),
       ("B", "She is a collaborative patient because she has presented herself for the service."),
       ("C", "The supervising physician must assess her and include a diagnosis on referral."),
       ("D", "She becomes a collaborative patient once the pharmacist records the conversation."),
       ("E", "In this setting she must be notified of and must consent to the services.")],
      ["C", "E"],
      "Statutory eligibility is fixed at s. 24B1/2(a) of M.G.L. c. 112: a patient must be REFERRED to the "
      "pharmacist by the supervising physician for the purpose of receiving collaborative services. The supervising physician shall "
      "assess the patient and include a diagnosis when referring, and in the retail drug business setting the patient "
      "shall be notified of and shall consent to the services.",
      {"A": "A remark to the patient is not a referral to the pharmacist.",
       "B": "Presenting for a service does not make a person a collaborative patient.",
       "C": "Correct: assessment and a diagnosis are part of the referral.",
       "D": "A unilateral note by the pharmacist does not create the referral.",
       "E": "Correct: notice and consent are required in the retail setting."},
      ["MA-CDTM-PATIENT-DEFINITION"],
      ["Ask whether a referral running from physician to pharmacist exists",
       "Check that the referral carries an assessment and a diagnosis",
       "Apply the retail-setting notice and consent requirement"],
      ["Individual referral and consent must be recorded by both professionals"],
      "Candidates treat the patient's own account of what a physician said as the referral itself."),

    q("MA-Q-0303", "CDTM_PATIENT_ELIGIBILITY_AND_DUAL_RECORDING", "Collaborative practice", "Recording referral and consent", 4, "SBA",
      "A Massachusetts supervising physician refers a patient for collaborative drug therapy management, records the "
      "referral and the patient's consent in his own chart, and tells the collaborating pharmacist that the "
      "documentation is complete and nothing further is needed. Where must the individual referral and consent be "
      "recorded?",
      [("A", "In the supervising physician's record alone, which is what the statute requires."),
       ("B", "In the pharmacist's record alone, since the pharmacist delivers the service."),
       ("C", "In whichever of the two records the professionals agree should hold them."),
       ("D", "In the patient's record, by the pharmacist and by the supervising physician."),
       ("E", "In a register filed with the Board, separately from the patient's record.")],
      ["D"],
      "The statutory definition of a collaborative patient closes with a recording duty: individual referral "
      "and consent SHALL BE RECORDED BY THE PHARMACIST AND THE SUPERVISING PHYSICIAN in the patient's record. The "
      "duty binds both professionals, so the physician's entry does not discharge the pharmacist's.",
      {"A": "The statute names both professionals, not the physician alone.",
       "B": "The statute names both professionals, not the pharmacist alone.",
       "C": "The allocation is fixed by statute and is not open to agreement.",
       "D": "Correct: a dual recording duty in the patient's record.",
       "E": "No Board-filed register is required by the definition."},
      ["MA-CDTM-PATIENT-DEFINITION"],
      ["Read the closing sentence of the statutory definition of patient",
       "Note that it names the pharmacist and the supervising physician",
       "Conclude that one entry does not discharge the other's duty"],
      ["247 CMR 16.04(6) separately governs custody of the agreement itself"],
      "Candidates assume that documentation held by the referring professional serves for both."),

    q("MA-Q-0304", "CDTM_REFERRAL_MEANING_BY_SETTING", "Collaborative practice", "Meaning of referral", 5, "SBA",
      "On the same morning a Massachusetts hospital pharmacist begins collaboratively managing an inpatient after a "
      "discussion about that patient with the attending supervising physician, and a community pharmacist begins "
      "collaboratively managing a walk-in after an identical discussion with her supervising physician. Neither holds "
      "a signed individual referral. Which analysis is correct?",
      [("A", "Both are properly referred, since a consultation is a referral in any setting."),
       ("B", "The hospital pharmacist is properly referred; the community pharmacist is not."),
       ("C", "The community pharmacist is properly referred; the hospital pharmacist is not."),
       ("D", "Neither is properly referred, because a written referral is always required."),
       ("E", "Neither is properly referred, because a referral must be signed to be effective.")],
      ["B"],
      "243 CMR 2.12(1) defines Referral as the individual patient referral by a supervising physician to an "
      "authorized pharmacist in a COMMUNITY PHARMACY setting, and IN ALL OTHER PRACTICE SETTINGS as the CONSULTATION "
      "of a supervising physician and an authorized pharmacist about a patient for that purpose. The same facts "
      "therefore satisfy the definition in the hospital and fail it in the community pharmacy.",
      {"A": "The definition changes with the setting, so a consultation does not serve everywhere.",
       "B": "Correct: consultation suffices outside the community pharmacy setting.",
       "C": "This reverses the definition.",
       "D": "A written individual referral is required in the community pharmacy setting only.",
       "E": "Signature is not the distinguishing feature; the setting is."},
      ["MA-CDTM-REFERRAL-BY-SETTING"],
      ["Identify the practice setting in each case",
       "Apply the community-pharmacy limb of the definition to the walk-in",
       "Apply the all-other-settings limb to the inpatient"],
      ["The community-pharmacy written referral must state that written consent was executed"],
      "Candidates carry the community-pharmacy formalities into every setting because those formalities are the ones "
      "the regulations describe in detail."),

    q("MA-Q-0305", "CDTM_SCOPE_VS_DIAGNOSIS_BOUNDARY", "Collaborative practice", "Scope of the authority", 4, "SATA",
      "A Massachusetts pharmacist is mapping out what a proposed collaborative practice agreement could cover. Which "
      "activities may fall within collaborative drug therapy management as the statute defines it? Select all that "
      "apply.",
      [("A", "Initiating, monitoring, modifying and discontinuing the patient's drug therapy."),
       ("B", "Collecting and reviewing the patient's history."),
       ("C", "Obtaining and checking pulse, temperature, blood pressure and respiration."),
       ("D", "Settling a diagnosis where a laboratory result plainly supports one."),
       ("E", "Ordering and evaluating laboratory tests directly related to the drug therapy.")],
      ["A", "B", "C", "E"],
      "M.G.L. c. 112, s. 24B1/2(a) defines collaborative drug therapy management as the initiating, monitoring, "
      "modifying and discontinuing of a patient's drug therapy under an agreement, and provides that it may include "
      "collecting and reviewing histories, obtaining and checking the named vital signs, and ordering and evaluating "
      "laboratory tests directly related to drug therapy on the stated conditions.",
      {"A": "Correct: this is the core of the defined activity.",
       "B": "Correct: expressly included.",
       "C": "Correct: the four named vital signs are expressly included.",
       "D": "The evaluation shall not include a diagnostic component.",
       "E": "Correct, subject to physician supervision or direct consultation and an approved protocol."},
      ["MA-CDTM-SCOPE-DEFINITION"],
      ["Read the definition's core verbs",
       "Read the three included activities",
       "Exclude anything that amounts to a diagnostic conclusion"],
      ["Laboratory work requires an approved protocol applicable to the practice setting"],
      "Candidates assume that a pharmacist who may order and evaluate a test may also act on what it shows."),

    q("MA-Q-0306", "CDTM_SCOPE_VS_DIAGNOSIS_BOUNDARY", "Collaborative practice", "The diagnostic boundary", 5, "SBA",
      "A Massachusetts collaborating pharmacist orders a laboratory test directly related to the drug therapy she "
      "co-manages, under an approved protocol for her setting and in direct consultation with the supervising "
      "physician, and then evaluates the result. Her evaluation concludes that the patient has a new condition. What "
      "is the position?",
      [("A", "The ordering may be proper, but the evaluation may not include a diagnostic component."),
       ("B", "The ordering is improper, because a pharmacist may not order laboratory tests."),
       ("C", "Both are proper, because the test was directly related to the therapy managed."),
       ("D", "Both are improper, because laboratory work sits outside collaborative management."),
       ("E", "Both are proper, provided she reports the conclusion to the supervising physician.")],
      ["A"],
      "The laboratory limb of the statutory collaborative-management definition permits ordering and evaluating results "
      "directly related to drug therapy under physician supervision or direct consultation and an approved protocol, "
      "but only WHEN THE EVALUATION SHALL NOT INCLUDE A DIAGNOSTIC COMPONENT. Satisfying the conditions for ordering "
      "does not enlarge what the evaluation may conclude.",
      {"A": "Correct: the conditions on ordering and the limit on evaluating are separate.",
       "B": "Ordering is permitted on the stated conditions, which were met here.",
       "C": "Relatedness to the therapy does not lift the diagnostic limit.",
       "D": "Laboratory work is expressly within the definition on conditions.",
       "E": "Reporting the conclusion does not cure a diagnostic evaluation."},
      ["MA-CDTM-SCOPE-DEFINITION"],
      ["Check the conditions attached to ordering the test",
       "Check the separate limit attached to evaluating the result",
       "Conclude that the second limit is unaffected by satisfying the first"],
      ["The same definition also permits collecting histories and checking vital signs"],
      "Candidates treat compliance with the ordering conditions as authorising whatever the evaluation then finds."),

    q("MA-Q-0307", "CDTM_TERMINATION_CONTINUITY_AND_PATIENT_NOTICE", "Collaborative practice", "Termination duties", 4, "SBA",
      "A Massachusetts collaborative practice agreement will lapse at the end of this month and will not be renewed. "
      "The pharmacist plans to write to each affected patient in the week after the lapse, explaining that the "
      "arrangement has ended and how their therapy will be continued. Which duty has already been missed?",
      [("A", "None; written notice after the lapse discharges both of the duties owed."),
       ("B", "Notice to the Board of Registration in Pharmacy in advance of the lapse."),
       ("C", "Notice to each affected patient's other prescribers in advance of the lapse."),
       ("D", "A written variation of the agreement extending it beyond the lapse date."),
       ("E", "Arranging an uninterrupted continuation of therapy before the lapse.")],
      ["E"],
      "247 CMR 16.04(5) imposes two duties with different timing. PRIOR TO termination or non-renewal, the "
      "authorized pharmacist and supervising physician shall arrange for an uninterrupted continuation of the "
      "patient's drug therapy. WHEN the agreement is not renewed or is otherwise terminated, they shall inform the "
      "patient in writing. The planned letter answers the second duty but not the first.",
      {"A": "The continuity duty falls due before termination, not after it.",
       "B": "No advance notice to the Board is required by the paragraph.",
       "C": "No notice to other prescribers is required by the paragraph.",
       "D": "The paragraph does not require the agreement to be extended.",
       "E": "Correct: continuity must be arranged before the agreement ends."},
      ["MA-CDTM-TERMINATION-DUTIES"],
      ["Separate the two duties in 247 CMR 16.04(5)",
       "Fix the timing of each against the lapse date",
       "Identify which one the plan leaves unperformed"],
      ["Both duties are owed jointly by the pharmacist and the supervising physician"],
      "Candidates see a written notice in the plan, match it to the written-notice duty, and stop looking."),

    q("MA-Q-0308", "CDTM_WRITING_REQUIREMENT_PAPER_OR_ELECTRONIC", "Collaborative practice", "Form of documents", 4, "SATA",
      "A Massachusetts collaborating pharmacist holds two patient referrals. One is written in indelible pencil. The "
      "other arrived by email as a flattened image which the pharmacy system can neither store nor retrieve in "
      "readable form. Which statements are correct? Select all that apply.",
      [("A", "The pencil referral fails, because a paper document must be written in ink."),
       ("B", "The emailed referral succeeds, because electronic transmission is permitted."),
       ("C", "Both fail, because a referral must carry a handwritten signature to be valid."),
       ("D", "The referral in indelible pencil satisfies the writing requirement."),
       ("E", "The emailed referral fails the readable and retrievable requirement.")],
      ["D", "E"],
      "243 CMR 2.12(1) provides that references to written mean, if paper based, written in ink, indelible pencil or "
      "any other means; or transmitted electronically in a format that maintains patient confidentiality and can be "
      "read and stored in a retrievable and readable form. The paper route is deliberately permissive while the "
      "electronic route carries conditions the emailed image does not meet.",
      {"A": "Indelible pencil is named in the regulation alongside ink.",
       "B": "Electronic transmission is permitted only on the stated conditions.",
       "C": "Electronic signatures are expressly contemplated, so a handwritten signature is not essential.",
       "D": "Correct: expressly within the paper limb.",
       "E": "Correct: it can be neither read nor stored retrievably."},
      ["MA-CDTM-WRITING-FORM"],
      ["Classify each document as paper based or electronic",
       "Apply the permissive paper limb to the first",
       "Apply the confidentiality, readability and retrievability conditions to the second"],
      ["Electronic transmission must also accord with M.G.L. c. 94C, s. 23(g) and 105 CMR 721.00"],
      "Candidates assume the electronic document is the more compliant of the two because it looks more formal."),

    q("MA-Q-0309", "COUNSELLING_OFFER_METHOD_AND_CONTAINER_LABEL", "Patient care", "Offer to counsel", 4, "SBA",
      "A Massachusetts pharmacy delivers prescriptions to patients at their homes. With each parcel it encloses "
      "delivery paperwork printed with a toll-free number the patient may call to speak with the pharmacy's "
      "pharmacist. Nothing about the number appears on the medication containers themselves. Which statement is "
      "correct?",
      [("A", "Compliant, because the patient receives the toll-free number with the medication."),
       ("B", "Compliant, because the offer to counsel may be made by any reasonable method."),
       ("C", "Not compliant, because the number must be on a label affixed to each container."),
       ("D", "Not compliant, because home delivery requires a face-to-face offer to counsel."),
       ("E", "Not compliant, because a toll-free service cannot satisfy the counselling duty.")],
      ["C"],
      "M.G.L. c. 94C, s. 21A permits the requirements to be satisfied, where a person elects delivery at a location "
      "other than a pharmacy, by access to a toll-free telephone service, and then provides that the number of that "
      "service SHALL BE PRINTED ON A LABEL AFFIXED TO EACH CONTAINER of a prescription drug dispensed by the pharmacy "
      "to a patient. Enclosing it in the paperwork does not meet that requirement.",
      {"A": "Delivery with the parcel is not the same as a label affixed to each container.",
       "B": "The statute names the acceptable methods rather than leaving it open.",
       "C": "Correct: the container label is the specified place for the number.",
       "D": "The toll-free route is expressly available for remote delivery.",
       "E": "The toll-free service is an expressly permitted route."},
      ["MA-COUNSELING-OFFER-METHOD"],
      ["Identify that the patient elected delivery away from the pharmacy",
       "Confirm the toll-free route is available on those facts",
       "Apply the container-label requirement attached to that route"],
      ["The ordinary offer is made face to face or by telephone"],
      "Candidates accept any means by which the number reaches the patient and miss the container-label sentence."),

    q("MA-Q-0310", "COUNSELLING_RECORD_PRESUMPTION", "Patient care", "Counseling record presumption", 5, "SBA",
      "A Massachusetts pharmacy is asked about a dispensing from last year. Its records contain no entry that the "
      "patient failed to accept the pharmacist's offer to counsel, and no entry that counselling was actually given. "
      "What follows from that state of the records?",
      [("A", "Nothing follows; the records are simply silent about what happened that day."),
       ("B", "A presumption arises that the counselling was provided to that patient."),
       ("C", "A presumption arises that the counselling was not provided to that patient."),
       ("D", "The pharmacy must instead produce the dispensing pharmacist's recollection."),
       ("E", "The pharmacy is in breach, because counselling must be affirmatively recorded.")],
      ["B"],
      "M.G.L. c. 94C, s. 21A provides that THE ABSENCE OF ANY RECORD OF A FAILURE TO ACCEPT THE PHARMACIST'S OFFER "
      "TO COUNSEL SHALL CREATE A PRESUMPTION THAT SUCH COUNSELING WAS PROVIDED. The statute makes silence work in "
      "the pharmacist's favour, which is the reverse of the usual documentation intuition.",
      {"A": "The statute attaches a specific consequence to that silence.",
       "B": "Correct: silence creates a presumption that counselling was provided.",
       "C": "This inverts the statutory presumption.",
       "D": "No recollection evidence is required to raise the presumption.",
       "E": "The statute requires recording a failure to accept, not an affirmative record of counselling."},
      ["MA-COUNSELING-RECORD-PRESUMPTION"],
      ["Identify what the statute says must be recorded, which is a failure to accept",
       "Note that no such record exists here",
       "Apply the presumption the statute attaches to that absence"],
      ["The information may be recorded in the profile, the signature log or any other system of records"],
      "Candidates apply the general documentation instinct that an unrecorded act is an unproven act."),

    q("MA-Q-0311", "CPA_VALID_CONSTITUTION_AND_BIENNIAL_CURRENCY", "Collaborative practice", "Validity of the agreement", 4, "SATA",
      "A Massachusetts pharmacist is reviewing a proposed collaborative practice agreement before signing it. Which "
      "features does the statutory definition require for the agreement to be validly constituted? Select all that "
      "apply.",
      [("A", "It must be written and signed by the pharmacist and the supervising physician."),
       ("B", "The collaborative practice may extend beyond the supervising physician's own scope."),
       ("C", "It is subject to review and renewal on a biennial basis."),
       ("D", "It must be filed with the Board before the pharmacist may act under it."),
       ("E", "It must include individually developed guidelines for any prescriptive practice.")],
      ["A", "C", "E"],
      "A collaborative practice agreement is defined by statute as a written and signed agreement between "
      "a pharmacist with relevant training and experience and a supervising physician. The collaborative "
      "practice must sit within the scope of the supervising physician's practice, each agreement is "
      "subject to review and renewal on a biennial basis, and individually developed guidelines are "
      "required for any prescriptive practice.",
      {"A": "Correct: written and signed.",
       "B": "The statute requires the collaborative practice to sit within the supervising physician's scope.",
       "C": "Correct: biennial review and renewal.",
       "D": "Filing with the Board is not part of the statutory definition.",
       "E": "Correct: individually developed prescriptive guidelines are required."},
      ["MA-CPA-CONSTITUTION-CURRENCY"],
      ["Work through the statutory definition sentence by sentence",
       "Separate what the definition requires from what a pharmacist might assume",
       "Note the currency requirement that keeps the agreement effective"],
      ["247 CMR 16.04(6) separately governs where the agreement must be held"],
      "Candidates add a Board filing step by analogy to licensure processes that do require one."),

    q("MA-Q-0312", "DUR_EVIDENTIARY_BASIS_OPEN_LIST", "Patient care", "Basis of the review", 4, "SATA",
      "Two Massachusetts pharmacists reach opposite conclusions on the same drug utilization review question. One "
      "relies on a current peer-reviewed journal article that is not among the works named in the regulation. The "
      "other relies on a superseded edition of a compendium that is named. Which statements are correct? Select all "
      "that apply.",
      [("A", "The journal article is unacceptable, because the regulation does not name it."),
       ("B", "The journal article may properly be relied upon as peer-reviewed literature."),
       ("C", "Neither may be relied upon, since only the named works are acceptable sources."),
       ("D", "The superseded edition remains acceptable, because the compendium is named."),
       ("E", "The superseded edition fails, because the review must rest on current standards.")],
      ["B", "E"],
      "247 CMR 9.17(3) provides that the review SHALL be based upon CURRENT standards, which MAY INCLUDE four named "
      "works and other peer-reviewed medical literature. The list is open, so an unnamed current source qualifies, "
      "and currency is the governing requirement, so a superseded edition of a named work does not.",
      {"A": "The word may include makes the list illustrative rather than closed.",
       "B": "Correct: other peer-reviewed medical literature is expressly contemplated.",
       "C": "The list is not exhaustive.",
       "D": "Being named does not cure a lack of currency.",
       "E": "Correct: the standard relied on must be current."},
      ["MA-DUR-EVIDENTIARY-BASIS"],
      ["Read may include as illustrative rather than exhaustive",
       "Apply the currency requirement to each source",
       "Assess the two sources separately on those two points"],
      ["The named works include Plumb's Veterinary Drug Handbook"],
      "Candidates treat a named list in a regulation as a closed list of permitted sources."),

    q("MA-Q-0313", "DUR_RESPONSE_MEASURES_AND_DOCUMENTATION", "Patient care", "Response and documentation", 4, "SBA",
      "During prospective review a Massachusetts pharmacist identifies a therapeutic duplication, telephones the "
      "prescriber, agrees a change to the therapy, and dispenses the revised prescription. She makes no note of the "
      "call, on the basis that the clinical issue was fully resolved before anything was dispensed. What remains "
      "outstanding?",
      [("A", "Nothing; resolving the issue clinically discharges what the regulation requires."),
       ("B", "A report of the therapeutic duplication to the Board of Registration in Pharmacy."),
       ("C", "A second prospective review of the revised therapy before it is dispensed."),
       ("D", "Written confirmation from the prescriber of the change that was agreed."),
       ("E", "Documentation of the measures she took in response to the review.")],
      ["E"],
      "247 CMR 9.17(2) leaves the choice of responsive measure open, offering consultation with the prescriber or "
      "with the patient as examples, but then provides that a pharmacist SHALL DOCUMENT ANY MEASURES TAKEN in "
      "response to a drug utilization review. The documentation duty is unconditional and is not discharged by "
      "resolving the underlying problem.",
      {"A": "The paragraph imposes a separate documentation duty.",
       "B": "No report to the Board is required.",
       "C": "No second review is required by the paragraph.",
       "D": "Written prescriber confirmation is not what the paragraph requires.",
       "E": "Correct: the measures taken must be documented."},
      ["MA-DUR-RESPONSE-DOCUMENTATION"],
      ["Separate the discretionary choice of measure from the mandatory record of it",
       "Note that the pharmacist did take an appropriate measure",
       "Identify the documentation duty as the one left unperformed"],
      ["Consultation with the prescriber is an example rather than the required measure"],
      "Candidates treat a resolved clinical problem as a closed file and overlook the freestanding record duty."),

    q("MA-Q-0314", "DUTY_NOT_TO_REFUSE_CUSTOMARY_COMPOUNDING", "Pharmacy services", "Duty to compound", 4, "SBA",
      "A Massachusetts community pharmacy that holds the equipment and the ingredients turns away a request for a "
      "simple non-sterile oral suspension that is customary in its community, telling the parent it prefers not to "
      "compound. Later the same day it declines a request for a sterile preparation. How should the two refusals be "
      "assessed?",
      [("A", "Both are permitted, since compounding is a service a pharmacy may choose to offer."),
       ("B", "Both are prohibited, since a licensee may not refuse to compound on preference."),
       ("C", "The first refusal is permitted and the second refusal is prohibited on these facts."),
       ("D", "The first refusal is prohibited and the second falls outside the duty entirely."),
       ("E", "Both turn on whether another nearby pharmacy could have compounded them instead.")],
      ["D"],
      "247 CMR 9.01(15) provides that a licensee may not refuse to compound SIMPLE OR MODERATE NON-STERILE "
      "compounded preparations customary to the community needs, except upon extenuating circumstances or by a "
      "waiver of Board regulation. A preference not to offer the service is neither. The duty does not extend to "
      "sterile preparations, so the second refusal is outside it.",
      {"A": "The regulation makes customary non-sterile compounding a duty rather than an option.",
       "B": "The duty does not reach sterile preparations.",
       "C": "This reverses the analysis of the two requests.",
       "D": "Correct: the duty catches the first request and does not reach the second.",
       "E": "The availability of another pharmacy is not one of the two stated exceptions."},
      ["MA-COMPOUNDING-REFUSAL-LIMIT"],
      ["Classify each preparation as sterile or non-sterile, simple or otherwise",
       "Apply the duty to the preparation that falls inside it",
       "Test the stated reason against the two express exceptions"],
      ["The two exceptions are extenuating circumstances and a waiver of Board regulation"],
      "Candidates treat compounding as a commercial service the pharmacy is free to decline."),

    q("MA-Q-0315", "FRAUDULENT_OR_DECEPTIVE_ACT_STANDARD", "Professional conduct", "Fraud and deception", 5, "SBA",
      "A Massachusetts pharmacist arranges a dispensing record so that a reviewer will draw a conclusion the "
      "pharmacist knows to be untrue. Every individual entry is literally accurate, no dispensing rule is broken, and "
      "in the event no one relies on the record and no loss is suffered by anyone. What is the position?",
      [("A", "No violation, because every entry the pharmacist made is literally accurate."),
       ("B", "No violation, because no separate dispensing rule was broken by the pharmacist."),
       ("C", "A violation, because a licensee may not engage in any deceptive act."),
       ("D", "A violation if the Board shows a reviewer actually relied on the arrangement."),
       ("E", "A violation if the arrangement produced some financial gain for the pharmacy.")],
      ["C"],
      "247 CMR 9.01(9) provides that a licensee may not engage in any fraudulent or deceptive act. The prohibition "
      "is freestanding: it does not require a separate substantive rule to have been broken, and it is complete on "
      "the act without proof of reliance or loss. Literal accuracy does not answer a charge of deception arranged to "
      "mislead.",
      {"A": "Literal accuracy is consistent with a deceptive arrangement.",
       "B": "The prohibition stands on its own and needs no companion breach.",
       "C": "Correct: the deceptive act is itself the violation.",
       "D": "Reliance is not an element.",
       "E": "Financial gain is not an element."},
      ["MA-CONDUCT-DECEPTIVE-ACT"],
      ["Identify the deceptive character of the arrangement",
       "Note that no reliance or loss element appears in the regulation",
       "Apply the prohibition without searching for a broken dispensing rule"],
      ["247 CMR 9.01(2) separately prohibits arrangements designed to circumvent a rule"],
      "Candidates look for a broken substantive rule and treat its absence as the end of the matter."),

    q("MA-Q-0316", "LICENSEE_CONFIDENTIALITY_AFFIRMATIVE_DUTY", "Confidentiality", "Licensee duty", 4, "SBA",
      "A Massachusetts pharmacist discloses nothing about any patient to anyone. Completed prescriptions sit face up "
      "on an open counter and a printed waiting list showing patient names is visible to everyone standing in the "
      "queue. No one is shown to have read either of them. What is the position?",
      [("A", "Compliant, because the pharmacist made no disclosure to any third party."),
       ("B", "Compliant, because no one is shown to have read the information on display."),
       ("C", "Compliant, provided the pharmacy makes a private consultation area available."),
       ("D", "In breach, but only once a patient complains about the arrangement."),
       ("E", "In breach, because the duty includes protecting confidential information.")],
      ["E"],
      "247 CMR 9.01(16) requires a licensee to MAINTAIN patient confidentiality AND to PROTECT a patient's "
      "confidential information. The second limb is affirmative, so a pharmacist who discloses nothing may still "
      "fail the duty by leaving confidential information exposed in the ordinary workflow of the pharmacy.",
      {"A": "Non-disclosure answers only the first limb of the duty.",
       "B": "The duty is to protect the information, not to prevent proven reading of it.",
       "C": "A consultation area addresses counselling privacy, not exposed records.",
       "D": "A complaint is not an element of the duty.",
       "E": "Correct: the protective limb is breached by the exposure itself."},
      ["MA-LICENSEE-CONFIDENTIALITY"],
      ["Separate the maintain limb from the protect limb",
       "Note that no disclosure occurred",
       "Apply the protective limb to the exposed records and list"],
      ["247 CMR 9.18 separately governs the patient consultation area"],
      "Candidates reduce confidentiality to a rule against telling people things."),

    q("MA-Q-0317", "MANDATORY_VERSUS_DISCRETIONARY_RETURN_ACCEPTANCE", "Medication returns", "Acceptance of returns", 3, "SBA",
      "Two Massachusetts patients present returns at the same pharmacy on the same afternoon. The first was given the "
      "wrong strength by the pharmacy. The second simply changed therapy, and that product was correctly dispensed "
      "and is not defective. How must the pharmacy respond to the two returns?",
      [("A", "It must accept the first return and is not required to accept the second."),
       ("B", "It must accept both returns, because the pharmacy dispensed both products."),
       ("C", "It may decline both returns, because neither product can be dispensed again."),
       ("D", "It must accept the second return and may decline the first for quarantine."),
       ("E", "It must accept both, but may return only the second one to its inventory.")],
      ["A"],
      "247 CMR 9.01(7) requires a pharmacy to accept a medication it previously dispensed where the medication was "
      "dispensed in error or is suspected to be defective or contaminated, and states expressly that a pharmacy is "
      "NOT required to accept a medication that was properly dispensed and not defective at the time.",
      {"A": "Correct: mandatory for the error, discretionary for the change of therapy.",
       "B": "The regulation limits the mandatory limb to error, defect or contamination.",
       "C": "The error return must be accepted.",
       "D": "This reverses the mandatory and discretionary limbs.",
       "E": "An accepted return may not go back into inventory at all."},
      ["MA-RETURN-ACCEPTANCE-DUTY"],
      ["Classify each return by the reason it was brought back",
       "Apply the mandatory limb to the dispensing error",
       "Apply the express carve-out to the properly dispensed product"],
      ["An accepted return must be quarantined and properly disposed"],
      "Candidates apply a single rule to all patient returns rather than sorting them by cause."),

    q("MA-Q-0318", "OPIOID_ANTAGONIST_COUNSELLING_AND_REFERRAL_DUTIES", "Public health", "Opioid antagonist duties", 3, "SATA",
      "A Massachusetts pharmacy supplies a naloxone rescue kit to one walk-in requestor and has none readily "
      "available when a second walk-in asks for one an hour later. Which statements about what the pharmacy owes are "
      "correct? Select all that apply.",
      [("A", "Counselling must be provided to the first requestor at the time of dispensing."),
       ("B", "The opioid antagonist information pamphlet must be provided at that same time."),
       ("C", "The second requestor must be referred to the nearest location holding stock."),
       ("D", "The second requestor may simply be invited to return another day."),
       ("E", "The referral duty applies even though this pharmacy cannot supply the product.")],
      ["A", "B", "C", "E"],
      "247 CMR 9.06(3) requires counselling and the Board-approved opioid antagonist information pamphlet at the "
      "time of dispensing. 247 CMR 9.06(4) requires a pharmacy without one readily available at the time requested "
      "to refer the requestor to the nearest location that has one readily available. The referral duty exists "
      "precisely because the pharmacy cannot supply.",
      {"A": "Correct: counselling at the time of dispensing.",
       "B": "Correct: the pamphlet accompanies the counselling.",
       "C": "Correct: an affirmative referral to the nearest stocked location.",
       "D": "An invitation to return does not discharge the referral duty.",
       "E": "Correct: inability to supply is the trigger for the referral duty."},
      ["MA-OPIOID-ANTAGONIST-COUNSEL-REFER"],
      ["Take the dispensing and the stock-out as two separate events",
       "Apply the counselling and pamphlet duties to the dispensing",
       "Apply the referral duty to the stock-out"],
      ["The pamphlet is a Board-approved document"],
      "Candidates treat a stock-out as ending the pharmacy's obligations to the person in front of them."),

    q("MA-Q-0319", "OPIOID_ANTAGONIST_PURCHASER_BILLING_BEFORE_DISPENSING", "Public health", "Opioid antagonist billing", 5, "SBA",
      "A Massachusetts pharmacy is asked for naloxone by a woman who explains that she intends it for her adult son, "
      "who is not present. She does not ask to pay out of pocket. Whose insurance coverage should the pharmacy "
      "pursue, and at what point?",
      [("A", "The son's coverage, and the claim may be submitted after the product is supplied."),
       ("B", "The son's coverage, and the claim must be submitted before it is supplied."),
       ("C", "The mother's coverage, and the claim may be submitted after it is supplied."),
       ("D", "The mother's coverage, and the claim must be submitted before it is supplied."),
       ("E", "Neither, because a purchase intended for another person must be paid in cash.")],
      ["D"],
      "M.G.L. c. 94C, s. 19B(e) requires the transaction to be treated, for billing and cost-sharing purposes, as "
      "dispensing a prescription TO THE PERSON PURCHASING the opioid antagonist regardless of the ultimate user, and "
      "requires a reasonable effort to identify the purchaser's coverage and submit a claim PRIOR TO DISPENSING "
      "unless the purchaser asks to pay out of pocket.",
      {"A": "The ultimate user's coverage is not the one to pursue.",
       "B": "The purchaser is the mother, not the son.",
       "C": "The timing limb requires the claim before the product is supplied.",
       "D": "Correct on both the purchaser and the timing.",
       "E": "Third-party purchase is expressly contemplated by the statute."},
      ["MA-OPIOID-ANTAGONIST-BILLING"],
      ["Identify the purchaser as distinct from the intended ultimate user",
       "Apply the treat-as-dispensed-to-the-purchaser rule",
       "Apply the before-dispensing timing to the claim"],
      ["The purchaser may still elect to pay out of pocket"],
      "Candidates bill the person who will use the product, which is the intuitive but wrong party here."),

    q("MA-Q-0320", "PATIENT_PROFILE_REASONABLE_EFFORT_STANDARD", "Patient care", "Patient profile", 4, "SATA",
      "At one Massachusetts pharmacy a patient refuses to give any allergy history after being asked on three "
      "separate visits. At another, a patient is never asked because the queue is long. Both patient profiles are "
      "incomplete in exactly the same respect. Which statements are correct? Select all that apply.",
      [("A", "Both pharmacies are compliant, because the standard is only reasonable effort."),
       ("B", "Both pharmacies are in breach, because the profile has to be complete."),
       ("C", "Compliance turns on whether the missing history was clinically significant."),
       ("D", "The first pharmacy made a reasonable effort and is compliant on these facts."),
       ("E", "The second pharmacy made no effort at all and is not compliant.")],
      ["D", "E"],
      "247 CMR 9.16(7) requires the pharmacist or the pharmacist's designee to make a REASONABLE EFFORT to obtain, "
      "record and maintain the listed information. The duty is measured by the effort made, not by the completeness "
      "of the resulting record, so identical gaps produce opposite results depending on what the pharmacy did.",
      {"A": "The second pharmacy made no effort, so the standard is not satisfied there.",
       "B": "An incomplete profile is not automatically a breach.",
       "C": "The standard is the effort made rather than the significance of the gap.",
       "D": "Correct: repeated asking is a reasonable effort.",
       "E": "Correct: a long queue does not excuse never asking."},
      ["MA-PATIENT-PROFILE-DUTY"],
      ["Identify the standard as reasonable effort rather than completeness",
       "Assess what each pharmacy actually did",
       "Reach opposite conclusions on identical records"],
      ["247 CMR 9.16 does not apply to institutional sterile compounding pharmacies"],
      "Candidates grade the record rather than the effort, and so treat the two pharmacies alike."),

    q("MA-Q-0321", "PHARMACIST_INDIVIDUAL_COMPETENCE_SCOPE", "Professional practice standards", "Individual competence", 3, "SBA",
      "A Massachusetts pharmacist is directed by her employer to perform an administration technique that pharmacists "
      "in the Commonwealth are generally authorised to perform. She has never been trained in that technique and has "
      "never performed it. What governs her decision?",
      [("A", "She may proceed, because the act sits within the recognised pharmacist scope."),
       ("B", "She may proceed, because her employer has directed her to perform it."),
       ("C", "She may proceed if a colleague who is trained in it observes her doing it."),
       ("D", "She may not proceed unless the Board grants her an individual authorisation."),
       ("E", "She may not proceed, because it is outside her own training and experience.")],
      ["E"],
      "247 CMR 9.01(4) requires a pharmacist to practise within the scope of his or her own education, training and "
      "experience AND within the recognized pharmacist scope of practice. Both limbs must be satisfied, so an act "
      "well inside the profession's scope may still be outside the scope of a pharmacist who has never been trained "
      "in it.",
      {"A": "That satisfies the second limb only.",
       "B": "An employer direction cannot supply training and experience.",
       "C": "Observation by a colleague is not the regulatory test.",
       "D": "No individual Board authorisation is contemplated; training and experience are the test.",
       "E": "Correct: the individual competence limb is not met."},
      ["MA-PHARMACIST-COMPETENCE-SCOPE"],
      ["Note that the regulation states two cumulative limbs",
       "Confirm the act is within the profession's scope",
       "Test it against this pharmacist's own training and experience"],
      ["The same regulation governs every act of pharmacy practice"],
      "Candidates decide scope questions at the level of the profession and never descend to the individual."),

    q("MA-Q-0322", "PRACTICE_HOUR_CEILING_AND_REST_PERIOD", "Fitness to practise", "Continuing past the ceiling", 4, "SATA",
      "A Massachusetts pharmacist has been on duty for twelve hours when the relief pharmacist calls in sick and "
      "three patients are waiting on urgent therapy. Her district manager tells her to stay until the queue clears. "
      "Which statements about her continuing are correct? Select all that apply.",
      [("A", "She may continue only as an extenuating circumstance in the patient's interest."),
       ("B", "The time she works beyond twelve hours must be minimized."),
       ("C", "She must document the extenuating circumstance that justified continuing."),
       ("D", "The manager's instruction is itself sufficient authority for her to continue."),
       ("E", "The twelve hour ceiling binds pharmacists but not certified pharmacy technicians.")],
      ["A", "B", "C"],
      "247 CMR 9.01(17) sets a ceiling of 12 hours in a 24 hour period, and permits the licensee to exceed it only "
      "in the event of an extenuating circumstance, in order to act in the best interest of the patient, provided "
      "the excess time is minimized and the licensee documents the extenuating circumstance.",
      {"A": "Correct: the exception is framed around an extenuating circumstance and the patient's interest.",
       "B": "Correct: minimisation is an express condition.",
       "C": "Correct: documentation is an express condition and falls on the licensee.",
       "D": "An employer instruction is not one of the regulatory conditions.",
       "E": "The paragraph binds a pharmacist, a pharmacy intern and a pharmacy technician alike."},
      ["MA-PRACTICE-HOUR-CEILING"],
      ["Identify the ceiling and the period over which it runs",
       "Identify the exception and its two conditions",
       "Separate regulatory authority from employer instruction"],
      ["The same paragraph reaches pharmacy interns and pharmacy technicians"],
      "Candidates treat a genuine patient need as opening the exception without the minimisation and documentation "
      "conditions that come with it."),

    q("MA-Q-0323", "PRACTICE_HOUR_CEILING_AND_REST_PERIOD", "Fitness to practise", "Rest before resuming", 4, "SBA",
      "A Massachusetts pharmacist properly worked fourteen hours yesterday under a documented extenuating "
      "circumstance. Since finishing she has rested four hours, worked a short shift in an unrelated setting, and "
      "then rested a further five hours. She now proposes to resume work in a pharmacy. What does the regulation "
      "require of her?",
      [("A", "Nothing further, since she has now rested nine hours in total since that shift."),
       ("B", "An eight consecutive hour rest period before she resumes work in a pharmacy."),
       ("C", "A twenty-four hour break, because the previous shift exceeded twelve hours."),
       ("D", "Notification to the Board before she returns to practice in any pharmacy."),
       ("E", "Nothing further, because the extenuating circumstance was properly documented.")],
      ["B"],
      "247 CMR 9.01(17) requires an eight CONSECUTIVE hour rest period prior to resuming work in a pharmacy where "
      "the 12 hour ceiling has been exceeded. Rest broken into a four hour and a five hour block is not a "
      "consecutive eight hour period, and the documentation that justified the long shift does not substitute for "
      "the rest requirement.",
      {"A": "Nine hours in total is not eight consecutive hours.",
       "B": "Correct: the rest period must be eight consecutive hours.",
       "C": "The regulation specifies eight consecutive hours, not twenty-four.",
       "D": "No Board notification is required.",
       "E": "Documentation and rest are separate requirements."},
      ["MA-PRACTICE-HOUR-CEILING"],
      ["Note that the rest requirement is for consecutive hours",
       "Add up the rest blocks and test them against that requirement",
       "Distinguish the documentation condition from the rest condition"],
      ["The rest requirement bites before resuming work in a pharmacy"],
      "Candidates aggregate rest across the day and treat the total as satisfying a consecutive-hours requirement."),

    q("MA-Q-0324", "PROSPECTIVE_DRUG_REVIEW_MANDATORY_VS_MENU", "Patient care", "Prospective drug review", 4, "SATA",
      "A Massachusetts pharmacist is told by a colleague that the statutory prospective drug review is discharged "
      "once the screening items listed in the statute have been checked, and that it is owed only where the patient "
      "attends the pharmacy in person. Which statements are correct? Select all that apply.",
      [("A", "The listed screening items define the whole of the pharmacist's review duty."),
       ("B", "The review is owed only where the patient attends the pharmacy in person."),
       ("C", "The review is owed before each new prescription is dispensed or delivered."),
       ("D", "The listed screening items are permissive rather than an exhaustive list."),
       ("E", "Interactions with over-the-counter drugs fall outside the statutory review.")],
      ["C", "D"],
      "M.G.L. c. 94C, s. 21A requires a prospective drug review before each new prescription is DISPENSED OR "
      "DELIVERED to a patient or a person acting on behalf of the patient, and provides that the review MAY INCLUDE, "
      "BUT NOT BE LIMITED TO, the listed screening items, which expressly include serious interactions with "
      "nonprescription or over-the-counter drugs.",
      {"A": "The statute says may include but not be limited to.",
       "B": "Delivery to a person acting on the patient's behalf is expressly covered.",
       "C": "Correct: the trigger is each new prescription dispensed or delivered.",
       "D": "Correct: the screening list is illustrative.",
       "E": "Over-the-counter interactions are named in the list."},
      ["MA-PROSPECTIVE-REVIEW-MANDATE"],
      ["Identify the trigger for the duty",
       "Read the screening list as illustrative",
       "Test each of the colleague's two propositions separately"],
      ["The section does not apply to a drug dispensed to a hospital or nursing home inpatient"],
      "Candidates treat a statutory list as a checklist that both defines and exhausts the duty."),

    q("MA-Q-0325", "STANDING_ORDER_TRAINING_PRECONDITION_CONTRAST", "Public health", "Standing-order training", 5, "SBA",
      "A Massachusetts pharmacist has completed no training programme of any kind. She proposes to dispense emergency "
      "contraception under the statewide standing order this week, and to dispense a COVID-19 drug under a standing "
      "order next week. How do the two proposals compare?",
      [("A", "The emergency contraception dispensing may proceed; the COVID-19 drug may not."),
       ("B", "The COVID-19 dispensing may proceed; the emergency contraception may not."),
       ("C", "Both may proceed, because training is a professional expectation rather than a bar."),
       ("D", "Neither may proceed, because both regimes require approved training beforehand."),
       ("E", "Both may proceed once she notifies the Department that she intends to dispense.")],
      ["A"],
      "M.G.L. c. 94C, s. 19A(d) provides that before dispensing emergency contraception a pharmacist MAY complete a "
      "Commissioner-approved training programme. M.G.L. c. 94C, s. 19E(c) provides that before dispensing a COVID-19 "
      "drug a pharmacist SHALL complete such a programme. The two adjacent standing-order regimes differ on exactly "
      "this point.",
      {"A": "Correct: permissive in one regime and mandatory in the other.",
       "B": "This reverses the two provisions.",
       "C": "The COVID-19 training is a statutory precondition.",
       "D": "The emergency contraception training is permissive.",
       "E": "Notification to the Department is not the precondition in issue."},
      ["MA-STANDING-ORDER-TRAINING-CONTRAST"],
      ["Identify which standing-order regime each proposal engages",
       "Read the training provision belonging to each regime",
       "Note that one says may and the other says shall"],
      ["The COVID-19 training must cover review of recent laboratory blood work"],
      "Candidates assume one uniform training rule governs every statewide standing order."),

    q("MA-Q-0326", "SUBSTANDARD_PRODUCT_UNAUTHORISED_RECIPIENT", "Professional conduct", "Transfer of substandard product", 4, "SBA",
      "A Massachusetts pharmacy clearing expired stock offers it in three directions: to a licensed reverse "
      "distributor, to a volunteer overseas aid group that is not licensed to receive drugs, and to one of its own "
      "technicians who wants it for training purposes. Which of the transfers may lawfully proceed?",
      [("A", "All three, because expired stock is no longer a dispensable medicine at all."),
       ("B", "All three, provided each recipient is told that the product has expired."),
       ("C", "The transfer to the licensed reverse distributor, and neither of the other two."),
       ("D", "The transfers to the reverse distributor and the aid group, but not the third."),
       ("E", "None of them, because expired stock may never leave the pharmacy's custody.")],
      ["C"],
      "247 CMR 9.01(12) bars a licensee from dispensing or distributing expired, outdated, defective, contaminated, "
      "counterfeit, contraband or otherwise substandard product to any person or entity who is NOT LICENSED OR "
      "LEGALLY AUTHORIZED TO RECEIVE it. The test is the recipient's authorisation, not the purpose of the transfer, "
      "so only the licensed reverse distributor qualifies.",
      {"A": "Expiry does not remove the product from the regulation; it is what brings it in.",
       "B": "Disclosure is not a cure for an unauthorised recipient.",
       "C": "Correct: only the licensed reverse distributor is an authorised recipient.",
       "D": "A volunteer aid group that is not licensed cannot receive it.",
       "E": "Transfer to an authorised recipient is permitted."},
      ["MA-SUBSTANDARD-RECIPIENT-LIMIT"],
      ["Identify the product as within the listed substandard categories",
       "Assess each proposed recipient for licensure or legal authorisation",
       "Set aside the purpose of each transfer as irrelevant to the test"],
      ["Employment by the pharmacy does not make a technician an authorised recipient"],
      "Candidates sort the transfers by how worthy the purpose looks rather than by the recipient's status."),

    q("MA-Q-0327", "USP_CURRENCY_AND_BOARD_DISPLACEMENT", "Professional practice standards", "Governing standard", 5, "SATA",
      "A Massachusetts pharmacy follows the edition of a United States Pharmacopeia chapter that has sat in its "
      "binder for years, on a practice point the Board has never regulated. On a second point it follows the current "
      "USP chapter although a Board regulation addresses that point differently. Which statements are correct? Select "
      "all that apply.",
      [("A", "The first practice is compliant, because a genuine USP chapter was followed."),
       ("B", "The second practice is compliant, because USP is the recognised professional standard."),
       ("C", "Neither point is governed by USP, since the Board has not adopted those chapters."),
       ("D", "The first practice fails, because the most current USP chapter is the one that governs."),
       ("E", "The second practice fails, because the Board regulation displaces USP on that point.")],
      ["D", "E"],
      "247 CMR 9.01(3) provides that UNLESS OTHERWISE REGULATED BY THE BOARD, a licensee shall adhere to the MOST "
      "CURRENT standards established by each chapter of the United States Pharmacopeia. The currency limb defeats "
      "the first practice and the opening qualification defeats the second.",
      {"A": "A superseded edition is not the most current standard.",
       "B": "The Board regulation displaces USP where the Board has regulated the point.",
       "C": "The regulation makes USP binding where the Board is silent.",
       "D": "Correct: currency is required.",
       "E": "Correct: a Board regulation on the point takes precedence."},
      ["MA-USP-CURRENCY-DISPLACEMENT"],
      ["Ask, for each point, whether the Board has regulated it",
       "Where the Board is silent, require the most current USP chapter",
       "Where the Board has regulated, apply the Board regulation"],
      ["Adherence is mandatory rather than advisory where the Board is silent"],
      "Candidates treat USP as either always binding or always advisory, instead of conditional on Board silence."),
]

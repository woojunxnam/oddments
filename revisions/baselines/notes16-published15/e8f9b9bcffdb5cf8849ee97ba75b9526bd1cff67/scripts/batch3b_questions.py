"""Batch 3 tranche B3-B — 33 questions, MA-Q-0262 through MA-Q-0294.

Area 1 = 19 (247 CMR 10.00 personnel discipline, plus the remaining 247 CMR 3.00, 4.00
and 8.00 paths B3-A did not take). Area 2 = 14 (247 CMR 9.18 counseling, 9.15 validity
and monitoring-program duties, 9.01 professional conduct, and 247 CMR 16.02 collaborative
practice).

Structural targets built into the tranche:
  * SBA keys weighted E x11 / A x6 / C x2 / D x1 to pull the bank's answer-position
    chi-square back under the warning threshold.
  * SATA correct-counts weighted 4-correct x6 / 3-correct x3 / 2-correct x4 so the
    bank-wide three-correct share falls further below the concentration threshold.
  * SATA correct positions spread across all five slots (A 6 / B 8 / C 8 / D 10 / E 9)
    so no single slot exceeds the key-concentration threshold.
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
    # ================= AREA 1 — discipline (247 CMR 10.00) =================
    q("MA-Q-0262", 1, "B3B_0262_MA_CONVICTION_DEFINITION", "Licensure and discipline", "Conviction definition", 4, "SBA",
      "A Massachusetts pharmacist resolved a criminal matter in another state by admitting to sufficient facts, and "
      "the case was continued without a finding and later dismissed. She tells the Board she has no conviction to "
      "report. How should that resolution be characterised for Board purposes?",
      [("A", "Not a conviction, because the case was ultimately dismissed by the court."),
       ("B", "Not a conviction, because no sentence was ever imposed upon her."),
       ("C", "Not a conviction, because the matter arose outside of the Commonwealth."),
       ("D", "A conviction only if the Board separately finds that she committed the crime."),
       ("E", "A conviction, because an admission to sufficient facts and a continuance without a finding are included.")],
      ["E"],
      "247 CMR 10.02 defines conviction to include any admission to or finding of sufficient facts to warrant a "
      "finding of guilt, regardless of adjudication, a continuance without a finding, and any plea of guilty or nolo "
      "contendere, of or to a crime in any jurisdiction, accepted by the court, whether or not a sentence has been "
      "imposed. Each of the features she relies on is expressly inside the definition.",
      {"A": "Regardless of adjudication is part of the definition, so a later dismissal does not remove it.",
       "B": "The definition applies whether or not a sentence has been imposed.",
       "C": "The definition reaches a crime in any jurisdiction.",
       "D": "No separate Board finding is needed; the definition applies on its own terms.",
       "E": "Correct: both features named are inside the regulatory definition."},
      ["MA-DISCIPLINE-CONVICTION-DEFINITION"],
      ["Read the regulatory definition rather than the ordinary meaning of conviction",
       "Match the admission to sufficient facts and the continuance without a finding to the listed items",
       "Disregard the absence of a sentence and the out-of-state forum"],
      ["A conviction of a person licensed by the Board is conclusive evidence of the commission of that crime in a disciplinary proceeding based upon it."],
      "The regulatory definition is broader than the ordinary meaning and expressly covers a continuance without a finding."),

    q("MA-Q-0263", 1, "B3B_0263_MA_DISCIPLINE_REPORT_CLOCKS", "Licensure and discipline", "Disciplinary reporting deadlines", 5, "SATA",
      "A Massachusetts pharmacist is subject to two separate events: another state's board disciplines her nursing "
      "licence, and a week later she is criminally charged in Massachusetts. Which reporting statements are correct? "
      "Select all that apply.",
      [("A", "Neither event is reportable until the criminal matter reaches a final disposition."),
       ("B", "The out-of-state final action against her other health care licence must be reported within seven business days."),
       ("C", "The out-of-state action is reportable only if it involved the practice of pharmacy."),
       ("D", "The pending criminal charge must be reported to the Board in writing within 30 days."),
       ("E", "Both events share a single 30-day reporting deadline.")],
      ["B", "D"],
      "247 CMR 10.03(1)(z) makes it a ground for discipline to fail to report within seven business days any final "
      "action by another governmental authority regarding a registrant, including action against any other health "
      "care related registration the person holds. 247 CMR 10.03(1)(aa) separately requires written report of any "
      "pending criminal charge or conviction within 30 days. The two clocks are different and run from different "
      "triggers.",
      {"A": "The charge duty is triggered by the charge pending, not by final disposition.",
       "B": "Correct: seven business days, and the duty expressly reaches other health care credentials.",
       "C": "The duty covers action against any other health care related registration or licence.",
       "D": "Correct: 30 days in writing, triggered while the charge is merely pending.",
       "E": "The deadlines differ: seven business days and 30 days."},
      ["MA-DISCIPLINE-REPORTING-CLOCKS"],
      ["Classify each event against the two separate reporting grounds",
       "Apply the seven-business-day clock to the out-of-state final action",
       "Apply the 30-day written clock to the pending criminal charge"],
      ["Failing to report accurately is a ground for discipline alongside failing to report at all."],
      "Two clocks run from two triggers, and one is measured in business days while the other is not."),

    q("MA-Q-0264", 1, "B3B_0264_MA_DISCIPLINE_COOPERATION", "Licensure and discipline", "Duty to cooperate with the Board", 4, "SBA",
      "A Massachusetts pharmacist receives a Board request to appear and to produce dispensing records connected to a "
      "complaint. He is confident the complaint is baseless and simply does not respond. The Board later dismisses "
      "the underlying complaint. What is his exposure?",
      [("A", "No exposure, because dismissal of the underlying complaint resolves the matter."),
       ("B", "No exposure, provided he can show the records would not have changed the outcome."),
       ("C", "Exposure only if the Board issues a subpoena that he then ignores."),
       ("D", "Exposure only if the underlying complaint had ultimately been substantiated."),
       ("E", "Exposure, because failing without cause to cooperate is itself a ground for discipline.")],
      ["E"],
      "247 CMR 10.03(1)(q) makes it an independent ground for discipline to fail, without cause, to cooperate with "
      "any Board request to appear or to provide requested information, to fail to respond to a Board subpoena, or to "
      "fail to furnish records, documents, information or testimony to which the Board is legally entitled. The "
      "ground stands on its own and does not depend on the outcome of the underlying complaint.",
      {"A": "Dismissal of the complaint does not dispose of the separate non-cooperation ground.",
       "B": "The materiality of the records is not the test.",
       "C": "The ground covers requests as well as subpoenas.",
       "D": "The ground does not depend on the underlying complaint being substantiated.",
       "E": "Correct: non-cooperation without cause is a standalone ground."},
      ["MA-DISCIPLINE-COOPERATION"],
      ["Separate the underlying complaint from the duty to cooperate",
       "Note that the ground covers requests to appear and to provide information",
       "Apply the ground independently of the complaint's disposition"],
      ["The duty extends to records, documents, information and testimony to which the Board is legally entitled."],
      "Winning on the underlying complaint does not cure a separate failure to cooperate with the investigation."),

    q("MA-Q-0265", 1, "B3B_0265_MA_DISCIPLINE_ACTION_LADDER", "Licensure and discipline", "Disciplinary action types", 5, "SATA",
      "A Massachusetts pharmacist is reviewing the range of actions the Board may take on a complaint. Which "
      "statements are correct? Select all that apply.",
      [("A", "An advisory letter is retained in the Board's files but does not constitute formal disciplinary action."),
       ("B", "Dismissal of the complaint is not among the actions available to the Board."),
       ("C", "A reprimand constitutes formal disciplinary action."),
       ("D", "A censure is a severe reprimand."),
       ("E", "Probation allows practice under conditions imposed by the Board.")],
      ["A", "C", "D", "E"],
      "247 CMR 10.06 lists the available actions. Dismissal of the complaint is the first of them. An advisory letter "
      "is an official written document retained in the Board's files that does not constitute formal disciplinary "
      "action. A reprimand does constitute formal disciplinary action and a censure is a severe reprimand. Probation "
      "constitutes disciplinary action and consists of a period during which the registrant may practise under "
      "conditions imposed by the Board.",
      {"A": "Correct: retained in the files, yet expressly not formal discipline.",
       "B": "Dismissal of the complaint is expressly one of the listed actions.",
       "C": "Correct: a reprimand is formal disciplinary action.",
       "D": "Correct: a censure is characterised as a severe reprimand.",
       "E": "Correct: probation permits practice subject to Board conditions."},
      ["MA-DISCIPLINE-ACTION-TYPES"],
      ["Place each proposed action on the regulatory list",
       "Separate the one non-disciplinary written action from the formal ones",
       "Note that probation preserves practice under conditions"],
      ["Probation may be imposed pursuant to a formal adjudicatory hearing or a consent agreement."],
      "Only the advisory letter is written but non-disciplinary; reprimand, censure and probation are all formal."),

    q("MA-Q-0266", 1, "B3B_0266_MA_VOLUNTARY_SURRENDER", "Licensure and discipline", "Consent agreement and surrender", 5, "SBA",
      "A Massachusetts pharmacist negotiating a consent agreement is considering voluntarily surrendering her "
      "registration for a fixed period. Her counsel asks what the surrender document must say about later "
      "challenging it. What does the regulation require the agreement to state?",
      [("A", "That the surrender may be appealed to the Board within 30 days of the date it is signed."),
       ("B", "That the surrender is reviewable by a court on the administrative record compiled by the Board."),
       ("C", "That the surrender becomes final only after the Board publishes a decision in the matter."),
       ("D", "That the surrender may be withdrawn at any time before reinstatement is formally sought."),
       ("E", "That the surrender deprives her of all privileges of registration and is not subject to judicial review.")],
      ["E"],
      "247 CMR 10.06(6) requires a voluntary surrender agreement to be in writing and signed, to recite the facts on "
      "which it is based and address reinstatement and any Board conditions, to be placed in the registrant's "
      "permanent Board file, and to state that the registrant realises the surrender is an act depriving him or her "
      "of all privileges of registration and is not subject to judicial review.",
      {"A": "No internal appeal window is provided for a negotiated surrender.",
       "B": "The agreement must state the opposite: that it is not subject to judicial review.",
       "C": "Publication of a decision is not the mechanism for a consent surrender.",
       "D": "A withdrawal right is not among the required terms.",
       "E": "Correct: the required statement covers both loss of privileges and no judicial review."},
      ["MA-DISCIPLINE-CONSENT-SURRENDER"],
      ["Identify the surrender as part of a consent agreement rather than an order after hearing",
       "Locate the required contents of a voluntary surrender agreement",
       "Apply the express acknowledgement about judicial review"],
      ["The agreement must also recite the underlying facts and address reinstatement."],
      "A negotiated surrender trades finality for resolution: the waiver of judicial review is written into it."),

    q("MA-Q-0267", 1, "B3B_0267_MA_OUT_OF_STATE_DISCIPLINE", "Licensure and discipline", "Out-of-state discipline", 4, "SBA",
      "Another state disciplined a Massachusetts-licensed pharmacist for conduct that is lawful and consistent with "
      "good professional practice in Massachusetts and is not covered by any statutory protection. May the Board use "
      "that action as the basis for Massachusetts discipline?",
      [("A", "No, because that basis applies only where the conduct also violates Massachusetts law."),
       ("B", "Yes, because any discipline imposed by a sister board is automatically actionable here."),
       ("C", "Yes, provided the other state's process afforded the pharmacist a full hearing."),
       ("D", "Yes, but only after the pharmacist exhausts every available appeal in that state."),
       ("E", "No, because the Board may act only on conduct occurring inside the Commonwealth.")],
      ["A"],
      "247 CMR 10.06(7) permits the Board to initiate action on the basis of another jurisdiction's discipline "
      "provided that the conduct disciplined there constitutes a violation of Massachusetts law. Where the conduct is "
      "lawful and consistent with good practice here, that condition is not met.",
      {"A": "Correct: the conduct-equivalence condition is what gates the out-of-state basis.",
       "B": "The regulation attaches an express condition rather than making it automatic.",
       "C": "The other state's process is not the stated condition.",
       "D": "Exhaustion of appeals elsewhere is not the stated condition.",
       "E": "The Board can reach out-of-state conduct when it violates Massachusetts law."},
      ["MA-DISCIPLINE-OUT-OF-STATE"],
      ["Identify the proposed basis as another jurisdiction's disciplinary action",
       "Apply the condition that the conduct must violate Massachusetts law",
       "Conclude that the condition fails on these facts"],
      ["Being disciplined elsewhere for reasons substantially the same as those in 247 CMR 10.03 is itself a listed ground."],
      "Out-of-state discipline is a doorway, not a verdict: the conduct still has to violate Massachusetts law."),

    q("MA-Q-0268", 1, "B3B_0268_MA_PROTECTED_ACTIVITY_DISCIPLINE", "Licensure and discipline", "Protected activity discipline bar", 4, "SBA",
      "Another jurisdiction sanctioned a Massachusetts pharmacist solely for dispensing medication for reproductive "
      "health care services. The services would have been lawful in Massachusetts and are consistent with good "
      "professional practice here. The Board is considering discipline on the out-of-state ground. What is the "
      "correct outcome?",
      [("A", "Discipline may proceed, because out-of-state sanctions are a listed disciplinary ground."),
       ("B", "Discipline may proceed if the Board first convenes an investigative conference."),
       ("C", "Discipline may proceed but must be limited to an advisory letter in the file."),
       ("D", "Discipline is deferred until the other jurisdiction resolves any pending appeal."),
       ("E", "Discipline may not be imposed, because the protected activity carve-out overrides the listed grounds.")],
      ["E"],
      "247 CMR 10.03(3) applies notwithstanding the grounds for discipline in 247 CMR 10.03, so it overrides the "
      "out-of-state ground rather than sitting beside it. No licensee shall be subject to discipline for dispensing "
      "medication for reproductive health care services, or for any sanction arising from such services, so long as "
      "the services would have been lawful in Massachusetts and are consistent with good professional practice here. "
      "Both qualifiers are met.",
      {"A": "The carve-out is expressed as operating notwithstanding those grounds.",
       "B": "Procedure does not unlock a ground the carve-out removes.",
       "C": "An advisory letter would still treat the protected activity as a basis for Board action.",
       "D": "Deferral would keep the protected conduct alive as a basis.",
       "E": "Correct: the carve-out overrides, and both qualifiers are satisfied."},
      ["MA-DISCIPLINE-PROTECTED-ACTIVITY", "MA-DISCIPLINE-OUT-OF-STATE"],
      ["Identify the sanction as arising solely from protected health care services",
       "Test the lawful-in-Massachusetts and good-practice qualifiers",
       "Apply the carve-out as overriding the listed out-of-state ground"],
      ["Parallel protections appear at 247 CMR 3.05 for licensure and 247 CMR 8.08 for support personnel."],
      "The carve-out is written to override the grounds list, so pointing at a listed ground does not defeat it."),

    q("MA-Q-0269", 1, "B3B_0269_MA_PREHEARING_SUMMARY_CLOCKS", "Licensure and discipline", "Pre-hearing summary action", 5, "SATA",
      "A Massachusetts pharmacy learns that the Board is weighing urgent pre-hearing action against it. Which "
      "statements about the available mechanisms are correct? Select all that apply.",
      [("A", "A hearing on the necessity of a Cease and Desist Notice must be afforded within seven days."),
       ("B", "Where the Board suspends a licence prior to hearing, a hearing on the necessity of that action must be afforded within seven days."),
       ("C", "Pre-hearing suspension requires a prior criminal conviction of the licensee."),
       ("D", "A Cease and Desist Notice or Quarantine Notice is expressly non-disciplinary."),
       ("E", "A Quarantine Notice may only be issued after a formal adjudicatory hearing.")],
      ["B", "D"],
      "247 CMR 10.07 permits suspension or refusal to renew prior to hearing where the Board determines on affidavits "
      "or other documentary evidence that a licensee is an immediate or serious threat, with a hearing limited to the "
      "necessity of the summary action within seven days. 247 CMR 10.08(1) allows the Board or Board President to "
      "issue a non-disciplinary Cease and Desist or Quarantine Notice, and 247 CMR 10.08(3) sets that hearing clock "
      "at 15 business days.",
      {"A": "That clock is 15 business days, not seven days.",
       "B": "Correct: the pre-hearing suspension clock is seven days.",
       "C": "The test is an immediate or serious threat on affidavits or documentary evidence.",
       "D": "Correct: the notices are characterised as requiring non-disciplinary cessation or restriction.",
       "E": "These notices are expressly pre-hearing mechanisms."},
      ["MA-DISCIPLINE-SUMMARY-CLOCKS"],
      ["Separate pre-hearing suspension from a cease and desist or quarantine notice",
       "Attach the correct hearing clock to each mechanism",
       "Note that the notices are non-disciplinary in character"],
      ["The Board or Board President may rescind or amend a summary cease and desist or quarantine notice."],
      "Two urgent mechanisms exist with different clocks, and the faster-sounding one is not the one with 15 days."),

    q("MA-Q-0270", 1, "B3B_0270_MA_PERMITTING_SCOPE_VIOLATION", "Licensure and discipline", "Scope and impairment grounds", 4, "SBA",
      "A Massachusetts pharmacist on duty knowingly lets a pharmacy technician perform final dispensing process "
      "validation during a staffing shortage. No patient is harmed and the prescriptions are all correct. What is the "
      "pharmacist's own exposure?",
      [("A", "No exposure, because no patient harm resulted from the temporary arrangement."),
       ("B", "No exposure, because the technician holds a current Board technician licence."),
       ("C", "Exposure only if the pharmacy failed to document the arrangement contemporaneously."),
       ("D", "Exposure only if the Board first takes disciplinary action against the technician."),
       ("E", "Exposure, because knowingly permitting activity beyond the authorized scope is a ground for discipline.")],
      ["E"],
      "247 CMR 10.03(1) makes it a ground for discipline to engage in conduct beyond the authorized scope of a "
      "pharmacist, intern or technician and, separately, knowingly to permit, aid or abet an unlicensed person to "
      "perform activities requiring a licence. Final dispensing process validation is closed to technicians under 247 "
      "CMR 8.02(6)(d), so the permitting pharmacist is exposed regardless of outcome.",
      {"A": "Absence of harm is not an element of the ground.",
       "B": "A current technician licence does not extend the technician's scope.",
       "C": "Documentation does not authorise an act outside scope.",
       "D": "The pharmacist's ground is independent of any action against the technician.",
       "E": "Correct: knowingly permitting conduct beyond authorized scope is itself a ground."},
      ["MA-DISCIPLINE-SCOPE-AND-IMPAIRMENT"],
      ["Identify final dispensing process validation as outside technician scope",
       "Locate the ground reaching conduct beyond authorized scope and permitting it",
       "Apply the ground to the supervising pharmacist independently of outcome"],
      ["Practising while impaired and continuing to practise after a lapsed registration are separate listed grounds."],
      "A good outcome does not cure a scope violation, and the supervisor carries their own exposure."),

    q("MA-Q-0271", 1, "B3B_0271_MA_DISCIPLINE_PROCEDURE_STAGES", "Licensure and discipline", "Disciplinary procedure stages", 5, "SATA",
      "A Massachusetts pharmacist has received notice of an investigative conference. Which statements about Board "
      "disciplinary procedure are correct? Select all that apply.",
      [("A", "An investigative conference must precede any formal adjudicatory hearing."),
       ("B", "An investigative conference is an informal discussion relating to a complaint held with the Board."),
       ("C", "The Board may schedule an investigative conference at any time before a formal adjudicatory proceeding begins."),
       ("D", "An Order to Show Cause orders the registrant to appear for a formal adjudicatory hearing."),
       ("E", "A communication becomes a complaint once the Board determines, after investigation, that it merits further consideration or action.")],
      ["B", "C", "D", "E"],
      "247 CMR 10.02 defines the investigative conference as an informal discussion, the Order to Show Cause as the "
      "document ordering appearance at a formal adjudicatory hearing, and a complaint as a communication the Board "
      "determines after investigation merits further consideration or action. 247 CMR 10.04 permits a conference at "
      "any time prior to a formal proceeding, and 247 CMR 10.05 lets the Board schedule either a conference or a "
      "formal hearing, so the conference is not a mandatory first step.",
      {"A": "The Board may proceed directly to a formal hearing where it determines one is required.",
       "B": "Correct: the conference is expressly informal.",
       "C": "Correct: it may be scheduled at any time before a formal proceeding commences.",
       "D": "Correct: that is the defined function of an Order to Show Cause.",
       "E": "Correct: the Board's post-investigation determination is what makes it a complaint."},
      ["MA-DISCIPLINE-PROCEDURE-STAGES"],
      ["Classify the conference as informal rather than adjudicatory",
       "Note the Board's discretion to choose the track after investigation",
       "Distinguish the Order to Show Cause as the formal-hearing trigger"],
      ["An adjudicatory hearing is held under M.G.L. c. 30A and 801 CMR 1.01."],
      "An informal conference is available at the Board's option; it is not a required gateway to a formal hearing."),

    q("MA-Q-0272", 1, "B3B_0272_MA_DISCIPLINE_REACH", "Licensure and discipline", "Reach of Board disciplinary authority", 4, "SBA",
      "A single incident at a Massachusetts pharmacy implicates both the pharmacist on duty and the pharmacy's own "
      "operations. The pharmacy argues the Board must choose one target. How should that argument be evaluated?",
      [("A", "It fails, because the Board may take disciplinary action against the pharmacist and the pharmacy alike."),
       ("B", "It succeeds, because a single incident supports only a single disciplinary action."),
       ("C", "It succeeds unless the Board first refers the matter to the Attorney General."),
       ("D", "It succeeds, because entity credentials are disciplined only by the Department of Public Health."),
       ("E", "It fails only where the pharmacist on duty is also the pharmacy's Manager of Record.")],
      ["A"],
      "247 CMR 10.01 provides that the Board may take disciplinary action against a registered pharmacist, a pharmacy "
      "technician, a pharmacy, a pharmacy department, a wholesale licence and a controlled substance registration "
      "issued by the Board. Nothing confines a single incident to a single target, and 247 CMR 10.03(2) preserves the "
      "Board's ability to develop grounds through adjudication as well as rulemaking.",
      {"A": "Correct: the Board's disciplinary reach covers individual and entity credentials together.",
       "B": "No one-action limitation appears in the regulation.",
       "C": "Referral is a separate matter and is not a precondition.",
       "D": "The Board itself disciplines pharmacy and pharmacy department credentials.",
       "E": "The reach does not depend on the pharmacist also being the Manager of Record."},
      ["MA-DISCIPLINE-REACH"],
      ["List the credentials the Board may discipline",
       "Note the absence of any single-target limitation",
       "Apply the reach to both the individual and the entity"],
      ["The grounds in M.G.L. c. 112, § 61 apply alongside those listed in 247 CMR 10.03."],
      "One incident can produce parallel actions against a person and an entity; they are separate credentials."),

    # ================= AREA 1 — remaining 8.00 / 3.00 / 4.00 =================
    q("MA-Q-0273", 1, "B3B_0273_MA_INTERN_EXAM_BAR", "Pharmacy personnel", "Intern conduct consequences", 4, "SBA",
      "A Massachusetts pharmacy intern is found to have violated state drug regulations during his internship. He "
      "assumes the worst outcome is a sanction on his intern licence and that he can still sit for licensure. How "
      "should he be advised?",
      [("A", "He is correct, because examination eligibility turns only on degree and internship hours."),
       ("B", "He is correct, unless the violation involved a controlled substance."),
       ("C", "He is correct, because NABP rather than the Board controls examination access."),
       ("D", "He is wrong, because any regulatory violation permanently bars licensure here."),
       ("E", "He is wrong, because the Board may prohibit him from taking the licensure examination as well.")],
      ["E"],
      "247 CMR 8.01(17) provides that a pharmacy intern found to have engaged in conduct in violation of federal or "
      "state laws or regulations may be prohibited from taking the examination for licensure, in addition to other "
      "sanctions imposed by the Board. The examination bar is an additional consequence, not an alternative one, and "
      "it is discretionary rather than automatic or permanent.",
      {"A": "Examination access is not governed only by degree and hours; conduct can bar it.",
       "B": "The provision is not limited to controlled substance violations.",
       "C": "The Board may prohibit the intern from taking the examination.",
       "D": "The provision is discretionary and is not framed as a permanent bar.",
       "E": "Correct: an examination prohibition may be imposed in addition to other sanctions."},
      ["MA-INTERN-EXAM-BAR"],
      ["Identify the intern as subject to the intern-specific conduct provision",
       "Note that the examination prohibition is additional to other sanctions",
       "Treat the consequence as discretionary rather than automatic"],
      ["Preceptors and interns must submit information regarding the internship on a Board form in a timely manner."],
      "Sanctions on the intern licence and a bar on sitting the examination are cumulative, not alternatives."),

    q("MA-Q-0274", 1, "B3B_0274_MA_TECH_TRAINING_PROGRAMS", "Pharmacy personnel", "Technician training programs", 4, "SATA",
      "A Massachusetts pharmacy is designing a pathway for staff to qualify as pharmacy technicians. Which statements "
      "about Board-approved training are correct? Select all that apply.",
      [("A", "Any training program lasting at least one calendar year automatically qualifies."),
       ("B", "A generic Board-approved program must include a minimum of 120 hours of theoretical and 120 hours of practical instruction."),
       ("C", "A program provided by a branch of the United States Armed Services or Public Health Service may qualify."),
       ("D", "An on-the-job training program may be used only if the pharmacy first obtains a Board waiver."),
       ("E", "On-the-job training guidelines must be provided to the Board on request.")],
      ["B", "C", "E"],
      "247 CMR 8.02(4) lists qualifying programs, including an ASHP-accredited program, a program provided by a "
      "branch of the United States Armed Services or Public Health Service, a Board-approved program with a minimum "
      "of 120 hours of theoretical and 120 hours of practical instruction, and any other Board-approved course. 247 "
      "CMR 8.06(2) permits pharmacist-led on-the-job training under written pharmacy guidelines, copies of which are "
      "provided to the Board on request; no advance waiver is required.",
      {"A": "Duration alone is not a qualifying criterion.",
       "B": "Correct: the generic Board-approved route carries that hour split.",
       "C": "Correct: armed services and Public Health Service programs are named.",
       "D": "On-the-job training needs written guidelines, not a Board waiver.",
       "E": "Correct: the guidelines are produced to the Board on request."},
      ["MA-TECH-TRAINING-PROGRAM-TYPES"],
      ["Match each proposed pathway to the listed program types",
       "Apply the 120-plus-120 hour split to the generic Board-approved route",
       "Treat on-the-job training as guideline-based rather than waiver-based"],
      ["Completing a Board-approved training program supports the assessment-examination route to licensure."],
      "Programme length is not the criterion; the regulation names specific sources and a specific hour split."),

    q("MA-Q-0275", 1, "B3B_0275_MA_TECH_EXAM_CONTENT", "Pharmacy personnel", "Technician examination content", 4, "SATA",
      "A Massachusetts pharmacy is preparing staff for the Board-approved pharmacy technician assessment examination. "
      "Which knowledge areas does the regulation require the examination to cover? Select all that apply.",
      [("A", "Laws and regulations regarding the practice of pharmacy and patient confidentiality."),
       ("B", "The duties and responsibilities of a pharmacy technician in relationship to other pharmacy personnel."),
       ("C", "Sterile compounding gowning procedures and aseptic technique."),
       ("D", "Medical abbreviations and symbols."),
       ("E", "Identification of drugs, dosages, routes of administration and storage requirements.")],
      ["A", "B", "D", "E"],
      "247 CMR 8.02(5) lists the knowledge areas a Board-approved examination shall cover: practice settings; the "
      "duties and responsibilities of a pharmacy technician in relationship to other pharmacy personnel; laws and "
      "regulations regarding the practice of pharmacy and patient confidentiality; medical abbreviations and symbols; "
      "common dosage calculations; and identification of drugs, dosages, routes of administration and storage "
      "requirements. Sterile compounding technique is not among them.",
      {"A": "Correct: law and confidentiality is a named area.",
       "B": "Correct: relationship to other pharmacy personnel is a named area.",
       "C": "Sterile compounding technique is not among the listed examination areas.",
       "D": "Correct: medical abbreviations and symbols is a named area.",
       "E": "Correct: drug, dosage, route and storage identification is a named area."},
      ["MA-TECH-EXAM-CONTENT"],
      ["Recall that the examination content is prescribed rather than open",
       "Match each proposed area against the enumerated list",
       "Exclude areas that belong to other credentialing pathways"],
      ["Practice settings and common dosage calculations are the two remaining listed areas."],
      "The list is specific, so a plausible pharmacy topic can still fall outside the prescribed examination areas."),

    q("MA-Q-0276", 1, "B3B_0276_MA_INTERNSHIP_PROGRAM_CREDIT", "Pharmacy personnel", "Internship program credit", 4, "SBA",
      "A Massachusetts school of pharmacy launches a new clinical pharmacy program and tells students their "
      "participation will count toward the internship requirement. What does the regulation actually require before "
      "that credit is available?",
      [("A", "The school must submit a written program description and the Board determines creditability."),
       ("B", "Nothing further, because clinical pharmacy is already a listed internship setting."),
       ("C", "Each student must individually petition the Board for credit after completing the program."),
       ("D", "The program must be separately accredited by ACPE before any credit is available."),
       ("E", "The preceptor must certify the hours, after which internship credit follows automatically.")],
      ["A"],
      "247 CMR 8.01(12) requires Massachusetts approved colleges and schools of pharmacy to submit to the Board a "
      "written description of each demonstration project or clinical pharmacy program for which internship credit is "
      "desired, and the Board may determine whether student participation may be credited toward the internship "
      "requirement. The determination is the Board's, on the school's submission.",
      {"A": "Correct: the school submits a description and the Board determines creditability.",
       "B": "Being a listed setting does not by itself make a particular program creditable.",
       "C": "The submission duty sits on the school, not on each student.",
       "D": "Separate ACPE accreditation of the program is not the stated mechanism.",
       "E": "Preceptor certification does not replace the Board's determination."},
      ["MA-INTERN-PROGRAM-CREDIT-APPROVAL"],
      ["Identify the new offering as a clinical pharmacy program seeking internship credit",
       "Locate the school's submission duty",
       "Reserve the creditability decision to the Board"],
      ["The Board issues a Summary of Objectives and Procedures for Pharmacy Internship and preceptor guidelines."],
      "A qualifying category is not the same as an approved program; the Board still decides."),

    q("MA-Q-0277", 1, "B3B_0277_MA_LICENSURE_APPLICATION_MECHANICS", "Licensure", "Licensure application mechanics", 3, "SBA",
      "A Massachusetts licensure applicant submits an examination application missing the required proof of date and "
      "place of birth, together with the full fee. The Board declines to consider the application. He asks whether he "
      "will get his fee back. What is the correct position?",
      [("A", "The fee is refundable because the application was never substantively evaluated."),
       ("B", "The fee is refundable on written request within 30 days of the Board's decision."),
       ("C", "The fee is held as a credit against his next licensure application."),
       ("D", "The fee is refundable only if the omission resulted from the Board's own error."),
       ("E", "The fee is non-refundable once the application has been reviewed and acted upon.")],
      ["E"],
      "247 CMR 3.01(3) sets out what a completed application must include, and 247 CMR 3.01(8) permits the Board to "
      "refuse to consider any application that has not been properly completed. 247 CMR 3.01(9) provides that all "
      "fees submitted in connection with a licensure application that is reviewed and acted upon by the Board are "
      "non-refundable.",
      {"A": "Declining to consider an application is itself acting upon it.",
       "B": "No refund window is provided.",
       "C": "The regulation provides for non-refundability, not carry-forward credit.",
       "D": "The non-refundability provision is not conditioned on fault.",
       "E": "Correct: reviewed and acted upon fees are non-refundable."},
      ["MA-LICENSURE-APPLICATION-MECHANICS"],
      ["Identify the application as improperly completed",
       "Note the Board's power to refuse to consider it",
       "Apply the non-refundability provision to the fee already submitted"],
      ["A name change must be notified in writing to the Board or the Board's designee with the application."],
      "Refusing to consider an application is still acting on it, so the fee does not come back."),

    q("MA-Q-0278", 1, "B3B_0278_MA_DUPLICATE_CERTIFICATE", "Licensure", "Duplicate certificate of licensure", 3, "SBA",
      "A Massachusetts pharmacist obtained a duplicate certificate of licensure after losing the original. Months "
      "later the original turns up in a moving box. What does the regulation require her to do?",
      [("A", "Retain both and present whichever the Board requests."),
       ("B", "Return the recovered original to the Board and keep the duplicate."),
       ("C", "Promptly return the duplicate certificate to the Board."),
       ("D", "Destroy the original and note the destruction in her records."),
       ("E", "Report the recovery at her next renewal and keep both.")],
      ["C"],
      "247 CMR 3.03 provides that a duplicate certificate of licensure is obtained by submitting a Board-approved "
      "form with required documentation, and that in the event an original certificate is recovered after a duplicate "
      "has been issued, the duplicate shall be promptly returned to the Board.",
      {"A": "Holding two certificates is what the return requirement is designed to prevent.",
       "B": "It is the duplicate that goes back, not the recovered original.",
       "C": "Correct: the duplicate is promptly returned to the Board.",
       "D": "Destruction of the original is not the prescribed step.",
       "E": "The return duty is prompt rather than deferred to renewal."},
      ["MA-DUPLICATE-CERTIFICATE"],
      ["Identify which certificate was issued later",
       "Apply the return requirement to the duplicate",
       "Act promptly rather than waiting for renewal"],
      ["A duplicate is requested on a Board-approved form with required documentation."],
      "The instinct to surrender the older document is backwards: the duplicate is the one returned."),

    q("MA-Q-0279", 1, "B3B_0279_MA_CE_ALTERNATIVE_CREDIT", "Licensure", "Continuing education alternative credit", 4, "SATA",
      "A Massachusetts pharmacist teaches the same Board-approved continuing education program four times in one year "
      "and separately completes two courses in a postgraduate pharmacy curriculum. Which statements are correct? "
      "Select all that apply.",
      [("A", "As a Board-approved instructor she receives credit for the program taught on a one-time basis annually."),
       ("B", "She receives separate instructor credit for each of the four presentations."),
       ("C", "Postgraduate credit is available only for courses in pharmacy law."),
       ("D", "Postgraduate course credit requires the sponsor or co-sponsor to be Board-authorized or ACPE-accredited."),
       ("E", "Postgraduate credit requires the course to instruct in pharmacy, pharmaceutical sciences, pharmacy practice or pharmacy law.")],
      ["A", "D", "E"],
      "247 CMR 4.07 gives a Board-approved continuing education instructor credit for the program taught on a "
      "one-time basis annually. 247 CMR 4.08 awards contact hours for satisfactory completion of each course within a "
      "postgraduate pharmacy curriculum or Board-approved postgraduate medical program, provided the sponsor or "
      "co-sponsor is Board-authorized or ACPE-accredited and the course instructs in pharmacy, pharmaceutical "
      "sciences, pharmacy practice or pharmacy law.",
      {"A": "Correct: instructor credit is once annually for the program taught.",
       "B": "Repeated presentations of the same program do not multiply the credit.",
       "C": "Pharmacy law is one of four qualifying subject areas, not the only one.",
       "D": "Correct: the sponsor condition applies to postgraduate credit.",
       "E": "Correct: the subject-matter condition names those four areas."},
      ["MA-CE-INSTRUCTOR-AND-POSTGRADUATE"],
      ["Separate instructor credit from postgraduate curriculum credit",
       "Apply the once-annually limit to the repeated teaching",
       "Check both the sponsor and subject-matter conditions for postgraduate credit"],
      ["Contact hours may not be carried over from one calendar year to another."],
      "Teaching a program four times earns the credit once; volume does not convert into hours."),

    q("MA-Q-0280", 1, "B3B_0280_MA_CE_PROGRAM_DELIVERY", "Licensure", "Continuing education program criteria", 5, "SATA",
      "A provider is preparing two Board approval requests: one for a home-study program and one for a live program. "
      "Which statements about the Board's criteria are correct? Select all that apply.",
      [("A", "A home-study program must contain a test to indicate progress and verify completion."),
       ("B", "A home-study program must involve the learner by requiring an active response and providing feedback."),
       ("C", "A live program shall involve direct interaction between the faculty and participants."),
       ("D", "A live program must also supply a bibliography for continued study as a condition of approval."),
       ("E", "Participants shall be given the opportunity to evaluate faculty, learning experiences and facilities.")],
      ["A", "B", "C", "E"],
      "247 CMR 4.05(3) applies the developed-by-a-professional-group, logical-sequence, active-response, completion-"
      "test and bibliography criteria to home-study or other mediated instruction. 247 CMR 4.05(4) applies the "
      "direct-interaction and faculty-credential criteria to live programs. 247 CMR 4.05(7) requires provision for "
      "evaluating participants' attainment of the objectives and an opportunity for participants to evaluate faculty, "
      "learning experiences, instructional methods, facilities and educational resources.",
      {"A": "Correct: the completion test is a home-study criterion.",
       "B": "Correct: active response with feedback is a home-study criterion.",
       "C": "Correct: direct interaction is the live-program criterion.",
       "D": "The bibliography requirement is stated for home-study or other mediated instruction.",
       "E": "Correct: two-way evaluation applies to programs generally."},
      ["MA-CE-PROGRAM-DELIVERY-CRITERIA"],
      ["Sort each criterion by delivery format",
       "Keep the home-study-specific requirements out of the live-program list",
       "Apply the general evaluation requirement to both"],
      ["A request for provider authorization or program approval must be submitted at least 30 days in advance."],
      "The two formats carry different structural criteria, so a home-study requirement does not transplant to a live program."),

    # ================= AREA 2 — counseling (247 CMR 9.18) =================
    q("MA-Q-0281", 2, "B3B_0281_MA_WHO_MAY_COUNSEL", "Patient care", "Who may counsel", 4, "SBA",
      "At a busy Massachusetts pharmacy a patient accepts the offer to counsel on a new prescription. The only "
      "personnel free are a certified pharmacy technician and a pharmacy intern; the pharmacist is verifying another "
      "order. Who may deliver the counseling?",
      [("A", "The certified pharmacy technician, because certification covers patient communication."),
       ("B", "The certified pharmacy technician, provided the pharmacist reviews the encounter afterwards."),
       ("C", "Neither of them, because only the pharmacist personally may counsel a patient."),
       ("D", "Either of them, because both may relay the pharmacist's offer to counsel."),
       ("E", "The pharmacy intern, because counseling shall be made by a pharmacist or a pharmacy intern.")],
      ["E"],
      "247 CMR 9.18(3) provides that counseling shall be made by a pharmacist or a pharmacy intern, and that a "
      "pharmacy technician or other individual may not counsel any patient. Relaying the offer is a separate and "
      "narrower function that technicians may perform.",
      {"A": "Certification does not extend to providing counseling.",
       "B": "Later pharmacist review does not cure counseling delivered by a technician.",
       "C": "A pharmacy intern may also counsel.",
       "D": "Relaying the offer is not the same as delivering counseling.",
       "E": "Correct: the regulation names the pharmacist and the pharmacy intern."},
      ["MA-COUNSELING-WHO-MAY-COUNSEL"],
      ["Separate making the offer from delivering the counseling",
       "Identify the two categories permitted to counsel",
       "Exclude technicians and other individuals from counseling"],
      ["A pharmacist's designee may make the offer to counsel if appropriately trained."],
      "Being allowed to extend the offer is not being allowed to give the counseling."),

    q("MA-Q-0282", 2, "B3B_0282_MA_COUNSELING_DESIGNEE_TRAINING", "Patient care", "Offer by a designee", 3, "SBA",
      "A Massachusetts pharmacy assigns front-counter staff to make the offer to counsel at pickup so the pharmacist "
      "can stay at the verification station. What does the regulation require of that arrangement?",
      [("A", "The pharmacist shall ensure the designee is appropriately trained to make the offer to counsel."),
       ("B", "The designee must hold a pharmacy technician licence before making any offer."),
       ("C", "The arrangement is prohibited, because only a pharmacist may make the offer."),
       ("D", "The designee must document each offer in the patient profile at the time it is made."),
       ("E", "The arrangement requires prior written approval from the Board of Registration.")],
      ["A"],
      "247 CMR 9.18(1) allows a pharmacist or a pharmacist's designee to offer the counseling services of the "
      "pharmacist to each person who receives a prescription medication, and 247 CMR 9.18(2) requires the pharmacist "
      "to ensure the designee is appropriately trained to make the offer.",
      {"A": "Correct: the pharmacist must ensure the designee is appropriately trained.",
       "B": "The regulation refers to a designee rather than requiring a technician licence.",
       "C": "A designee may make the offer.",
       "D": "Contemporaneous profile documentation of every offer is not the stated requirement.",
       "E": "No advance Board approval is required for the arrangement."},
      ["MA-COUNSELING-WHO-MAY-COUNSEL"],
      ["Confirm that a designee may make the offer",
       "Locate the pharmacist's duty regarding that designee",
       "Apply the appropriate-training requirement"],
      ["Counseling itself may only be provided by a pharmacist or a pharmacy intern."],
      "The regulation constrains the designee through a training duty on the pharmacist, not through a credential."),

    q("MA-Q-0283", 2, "B3B_0283_MA_COUNSELING_TRIGGER", "Patient care", "Counseling trigger", 4, "SBA",
      "A Massachusetts patient collects a refill of an anticoagulant after a recent dose change communicated by the "
      "prescriber. A technician tells the pharmacist that counseling is not required because the prescription is a "
      "refill rather than a new drug therapy. How should the pharmacist respond?",
      [("A", "Agree, because the counseling duty attaches only to a prescription for new drug therapy."),
       ("B", "Agree, provided the patient was counseled when this drug was first dispensed to her."),
       ("C", "Agree, unless the patient affirmatively requests counseling from the pharmacist at pickup."),
       ("D", "Disagree, because every refill of any prescription requires counseling without exception."),
       ("E", "Disagree, because counseling is also required where the therapy is significant for the patient's health and safety.")],
      ["E"],
      "247 CMR 9.18(4) requires a pharmacist or pharmacy intern to provide counseling on each new drug therapy and on "
      "each drug therapy that, in the pharmacist's professional judgment, is deemed significant for the health and "
      "safety of the patient. The refill status does not end the inquiry; the professional-judgment limb applies.",
      {"A": "The duty has a second limb beyond new drug therapy.",
       "B": "Prior counseling does not extinguish the professional-judgment limb.",
       "C": "The duty does not depend on a patient request.",
       "D": "The second limb turns on professional judgment rather than applying to every refill.",
       "E": "Correct: the significance limb reaches this refill."},
      ["MA-COUNSELING-TRIGGER-AND-CONTENT"],
      ["Reject refill status as automatically ending the counseling duty",
       "Apply the professional-judgment limb to an anticoagulant dose change",
       "Provide counseling on that basis"],
      ["The information provided is what professional judgment deems necessary for the patient to understand proper use."],
      "The duty is not limited to new therapy; a significant refill still triggers it."),

    q("MA-Q-0284", 2, "B3B_0284_MA_COUNSELING_CONTENT", "Patient care", "Counseling content", 4, "SATA",
      "A Massachusetts pharmacist is counseling a patient on a new inhaled therapy. Which items does the regulation "
      "identify as information counseling may include? Select all that apply.",
      [("A", "The pharmacy's wholesale acquisition cost for the medication."),
       ("B", "Special directions and instructions for preparation, administration and use by the patient."),
       ("C", "Techniques for self-monitoring drug therapy."),
       ("D", "Proper storage and disposal of the medication."),
       ("E", "Action to be taken in the event of a missed dose or adverse reaction.")],
      ["B", "C", "D", "E"],
      "247 CMR 9.18(5) lists the information the pharmacist or intern may provide as professional judgment requires "
      "for the patient to understand proper use: name, description and indication; dosage form, dosage, route and "
      "duration; special directions and instructions; common side and adverse effects, interactions and "
      "contraindications or precautions; techniques for self-monitoring; proper storage and disposal; refill "
      "information; and action on a missed dose or adverse reaction. Acquisition cost is not among them.",
      {"A": "Acquisition cost is not part of the enumerated counseling content.",
       "B": "Correct: special directions and instructions are listed.",
       "C": "Correct: self-monitoring techniques are listed.",
       "D": "Correct: storage and disposal are listed.",
       "E": "Correct: missed dose and adverse reaction actions are listed."},
      ["MA-COUNSELING-TRIGGER-AND-CONTENT"],
      ["Recall that the content list is a professional-judgment menu",
       "Match each proposed item to the enumerated content",
       "Exclude commercial information that is not clinical counseling content"],
      ["The overarching test is what is necessary for the patient to understand the proper use of the prescription."],
      "The list is clinical; plausible-sounding commercial information is outside it."),

    q("MA-Q-0285", 2, "B3B_0285_MA_CONSULTATION_AREA_ACCESS", "Patient care", "Patient consultation area", 4, "SBA",
      "A Massachusetts pharmacy builds a private, well-signed consultation room with solid walls and a door. The only "
      "way a patient can reach it is by walking through the prescription dispensing area. Does the room satisfy the "
      "regulation?",
      [("A", "Yes, because the room provides adequate visual and auditory privacy."),
       ("B", "Yes, because a staff escort accompanies each patient through the area."),
       ("C", "Yes, provided the dispensing area is not visible from the store corridor."),
       ("D", "No, because a consultation area must be located outside the pharmacy department."),
       ("E", "No, because the area must be accessible without the patient traversing the dispensing area.")],
      ["E"],
      "247 CMR 9.18(6) requires a designated patient consultation area with Patient Consultation Area signage, "
      "designed for adequate privacy for confidential visual and auditory counseling, and requires that the private "
      "consultation area be accessible by a patient from outside the prescription dispensing area without having to "
      "traverse a stockroom or the prescription dispensing area. Privacy alone does not satisfy the access condition.",
      {"A": "Privacy is necessary but is not the only condition.",
       "B": "An escort does not change the required access route.",
       "C": "Sightlines from the corridor are not the test.",
       "D": "The regulation prescribes an access route, not a location outside the department.",
       "E": "Correct: the access route condition fails."},
      ["MA-COUNSELING-CONSULTATION-AREA"],
      ["Confirm the privacy condition is met",
       "Test the separate access-route condition",
       "Conclude that traversing the dispensing area defeats compliance"],
      ["The area must also carry signage stating Patient Consultation Area."],
      "A genuinely private room can still fail, because the regulation also dictates how the patient reaches it."),

    q("MA-Q-0286", 2, "B3B_0286_MA_COUNSELING_RIGHTS_SIGN", "Patient care", "Counseling rights sign", 4, "SATA",
      "A Massachusetts pharmacy with two separate dispensing windows is reviewing its counseling-rights signage. "
      "Which statements are correct? Select all that apply.",
      [("A", "A single sign at the store entrance satisfies the requirement for the whole pharmacy."),
       ("B", "The letters may be any size provided the sign is legible from the counter."),
       ("C", "A sign must be posted conspicuously adjacent to each area where prescriptions are dispensed."),
       ("D", "The sign must be at least 11 inches in height by 14 inches in width."),
       ("E", "The sign must be printed in both English and Spanish.")],
      ["C", "D"],
      "247 CMR 9.18(7) requires a sign of not less than 11 inches in height by 14 inches in width, posted "
      "conspicuously adjacent to each area where prescriptions are dispensed, informing customers of their right to "
      "counseling, with letters not less than one half inch in height and specified wording.",
      {"A": "A single entrance sign does not meet the adjacent-to-each-area requirement.",
       "B": "A minimum letter height of one half inch is prescribed.",
       "C": "Correct: adjacent to each dispensing area, so two windows need two signs.",
       "D": "Correct: 11 inches by 14 inches is the stated minimum.",
       "E": "The regulation prescribes wording, not a bilingual requirement."},
      ["MA-COUNSELING-RIGHTS-SIGN"],
      ["Count the areas where prescriptions are dispensed",
       "Apply the per-area posting requirement",
       "Check the prescribed sign dimensions and letter height"],
      ["The prescribed wording tells patients they have the right to know about proper use and effects and to ask the pharmacist."],
      "Two dispensing windows are two areas, and both the sign size and the letter height are prescribed."),

    q("MA-Q-0287", 2, "B3B_0287_MA_COUNSELING_AVAILABILITY", "Patient care", "Counseling availability and devices", 4, "SATA",
      "A Massachusetts community pharmacy is reviewing three practices: opening the front store an hour before a "
      "pharmacist arrives while filling nothing, omitting a measuring device for an adult liquid antibiotic, and "
      "applying its counseling policy to its affiliated inpatient service. Which statements are correct? Select all "
      "that apply.",
      [("A", "Counseling must be available at all times when the pharmacy is open for business."),
       ("B", "The measuring-device duty applies only to paediatric liquid medications."),
       ("C", "A proper measuring device must be dispensed or recommended with all liquid medications."),
       ("D", "The inpatient exclusion removes just the offer requirement and leaves the rest of the section in force."),
       ("E", "247 CMR 9.18 does not apply to pharmacists while practising in an inpatient setting unless otherwise required.")],
      ["A", "C", "E"],
      "247 CMR 9.18(8) requires counseling to be available at all times when the pharmacy is open for business. 247 "
      "CMR 9.18(9) requires a proper measuring device to be dispensed or recommended with all liquid medications, "
      "without a paediatric limitation. 247 CMR 9.18(10) excludes pharmacists practising in an inpatient setting from "
      "the provisions of 247 CMR 9.18 as a whole unless otherwise required by law or regulation.",
      {"A": "Correct: availability tracks the pharmacy being open for business.",
       "B": "No paediatric limitation appears in the provision.",
       "C": "Correct: the duty covers all liquid medications.",
       "D": "The exclusion is expressed as covering the provisions of 247 CMR 9.18, not only the offer.",
       "E": "Correct: the exclusion is stated for pharmacists practising in an inpatient setting."},
      ["MA-COUNSELING-ACCESS-AND-DEVICE"],
      ["Tie counseling availability to the pharmacy being open for business",
       "Apply the measuring-device duty to all liquid medications",
       "Read the inpatient exclusion as covering the whole section"],
      ["Counseling itself may only be delivered by a pharmacist or a pharmacy intern."],
      "The measuring-device duty is not paediatric-only, and the inpatient carve-out is section-wide."),

    # ================= AREA 2 — validity, monitoring, conduct, CDTM =================
    q("MA-Q-0288", 2, "B3B_0288_MA_VALIDITY_DETERMINATIONS", "Pharmacist practice", "Prescription validity determination", 5, "SATA",
      "A Massachusetts pharmacist receives an unusual prescription and telephones the prescriber, who confirms he "
      "wrote it. Which determinations must the pharmacist still make in the exercise of professional judgment before "
      "filling? Select all that apply.",
      [("A", "That the prescription was issued for a legitimate medical purpose by a practitioner acting in the usual course of professional practice."),
       ("B", "That the patient has no outstanding account balance with the pharmacy."),
       ("C", "That there is a valid patient-practitioner relationship."),
       ("D", "That the prescription is authentic."),
       ("E", "That the dispensing is in accordance with M.G.L. c. 94C, § 19(a).")],
      ["A", "C", "D", "E"],
      "247 CMR 9.15(2) provides that a pharmacist may not fill a prescription unless the pharmacist, exercising "
      "professional judgment, determines all four things: legitimate medical purpose by a practitioner acting in the "
      "usual course of practice, a valid patient-practitioner relationship, authenticity, and dispensing in "
      "accordance with M.G.L. c. 94C, § 19(a). The prescriber confirming authorship answers authenticity only.",
      {"A": "Correct: the legitimate-purpose determination remains the pharmacist's own.",
       "B": "An account balance is not a regulatory determination for filling.",
       "C": "Correct: a valid patient-practitioner relationship is a separate determination.",
       "D": "Correct: authenticity is one of the four, and is what the call addressed.",
       "E": "Correct: compliance with M.G.L. c. 94C, § 19(a) is the fourth determination."},
      ["MA-PRESCRIPTION-VALIDITY-DETERMINATION"],
      ["Note that the prescriber's confirmation speaks only to authenticity",
       "Enumerate the four determinations the regulation requires",
       "Keep each determination within the pharmacist's own professional judgment"],
      ["A pharmacist who dispenses medications reported to the monitoring program must register with and maintain login information for it."],
      "Confirming who wrote the prescription resolves one determination out of four."),

    q("MA-Q-0289", 2, "B3B_0289_MA_PMP_REGISTRATION_DUTY", "Pharmacist practice", "Monitoring program registration", 3, "SBA",
      "A newly hired Massachusetts pharmacist dispenses medications reported to the Prescription Monitoring Program. "
      "Her pharmacy holds an institutional MassPAT account that the Manager of Record administers. What does the "
      "regulation require of her personally?",
      [("A", "She shall register with and maintain login information for the monitoring system."),
       ("B", "Nothing further, because the pharmacy's account covers all dispensing staff."),
       ("C", "She must register only if she dispenses Schedule II controlled substances."),
       ("D", "She must register within 30 days of her first Board disciplinary contact."),
       ("E", "She must register only if the Manager of Record delegates monitoring duties to her.")],
      ["A"],
      "247 CMR 9.15(1) requires a pharmacist who dispenses medications reported to the Massachusetts Prescription "
      "Monitoring Program to register with, and maintain login information for, the electronic system authorized by "
      "M.G.L. c. 94C, § 24A, known as PMP or MassPAT. The duty is personal and includes maintaining the login, not "
      "merely enrolling once.",
      {"A": "Correct: personal registration and maintained login information.",
       "B": "A pharmacy-level account does not discharge the individual duty.",
       "C": "The trigger is dispensing medications reported to the program, not a single schedule.",
       "D": "The duty is not linked to disciplinary contact.",
       "E": "The duty does not depend on delegation by the Manager of Record."},
      ["MA-PMP-REGISTRATION-DUTY"],
      ["Identify the trigger as dispensing medications reported to the program",
       "Attach the duty to the individual pharmacist",
       "Include maintaining login information, not only initial registration"],
      ["The pharmacist must separately make the four validity determinations before filling."],
      "An institutional account does not satisfy a duty the regulation places on the dispensing pharmacist."),

    q("MA-Q-0290", 2, "B3B_0290_MA_REFERRAL_REMUNERATION", "Professional conduct", "Referral remuneration", 4, "SBA",
      "A Massachusetts pharmacy offers a nursing home's administrator free catering for staff events. Nothing is said "
      "about individual patients, but the pharmacy hopes the facility will send it more business. How does the "
      "regulation treat the arrangement?",
      [("A", "Permitted, because no referral of any individual patient is being solicited."),
       ("B", "Permitted, because catering is not a payment of money."),
       ("C", "Permitted if the facility discloses the arrangement to its residents."),
       ("D", "Permitted if the value stays below the pharmacy's ordinary annual marketing budget."),
       ("E", "Prohibited, because a licensee may not offer anything of value for the generation of business.")],
      ["E"],
      "247 CMR 9.01(11) bars a licensee from offering, soliciting or receiving remuneration or anything of value to "
      "or from any person who owns, operates, manages or is an employee of a hospital, nursing home or other health "
      "care facility in return for a referral or for the generation of business from the sale or furnishing of drugs, "
      "devices or services to such persons or institutions.",
      {"A": "Generation of business is covered separately from an individual referral.",
       "B": "Anything of value is covered, not only money.",
       "C": "Disclosure is not a stated cure.",
       "D": "No de minimis or budget-based exception is provided.",
       "E": "Correct: offering anything of value for the generation of business is prohibited."},
      ["MA-CONDUCT-REFERRAL-REMUNERATION"],
      ["Identify the recipient as a manager of a health care facility",
       "Classify the catering as anything of value",
       "Apply the generation-of-business limb rather than looking for a named patient"],
      ["The prohibition runs in both directions, covering offering as well as receiving."],
      "The rule does not require a named patient or a cash payment; generation of business and anything of value suffice."),

    q("MA-Q-0291", 2, "B3B_0291_MA_INSTITUTIONAL_DISPENSING", "Professional conduct", "Institutional dispensing limits", 4, "SBA",
      "A Massachusetts clinic pharmacy that does not hold a Drug Store pharmacy licence is asked to fill a "
      "prescription for the adult sibling of a clinic employee. The sibling lives across town and is not a clinic "
      "patient. May the pharmacist dispense?",
      [("A", "No, because the permitted recipients do not extend to that relative."),
       ("B", "Yes, because the family members of employees are always covered."),
       ("C", "Yes, provided the prescription was written by a clinic practitioner."),
       ("D", "Yes, provided the sibling pays the usual and customary retail price."),
       ("E", "Yes, because the restriction applies only to controlled substances.")],
      ["A"],
      "247 CMR 9.01(13) provides that, unless otherwise permitted by law, a pharmacist connected with a hospital or "
      "clinic pharmacy that does not hold a Drug Store pharmacy licence may not dispense to any person other than "
      "inpatients or outpatients of the hospital or clinic, employees of that institution, or those employees' "
      "spouses and children who live in the same house. An adult sibling living elsewhere is outside that class.",
      {"A": "Correct: the permitted class does not include an employee's sibling living elsewhere.",
       "B": "The family limb is confined to spouses and children living in the same house.",
       "C": "The identity of the prescriber does not extend the permitted class.",
       "D": "Payment terms are irrelevant to the restriction.",
       "E": "The restriction is not limited to controlled substances."},
      ["MA-CONDUCT-INSTITUTIONAL-DISPENSING"],
      ["Confirm the institution lacks a Drug Store pharmacy licence",
       "List the permitted recipient classes",
       "Place the adult sibling outside those classes"],
      ["Inpatients and outpatients of the hospital or clinic remain within the permitted class."],
      "The family limb is narrow: spouses and children in the same house, not relatives generally."),

    q("MA-Q-0292", 2, "B3B_0292_MA_CDTM_PRESCRIPTIVE_CONDITIONS", "Collaborative practice", "Prescriptive practice conditions", 5, "SATA",
      "A Massachusetts collaborating pharmacist is negotiating an agreement that will include prescriptive practices. "
      "Which additional conditions attach because of that inclusion? Select all that apply.",
      [("A", "Holding at least $2,000,000 per occurrence of professional liability insurance."),
       ("B", "Maintaining a current controlled substance registration issued by the Department during the term of the agreement."),
       ("C", "Completing at least ten additional contact hours of continuing education each year of the agreement."),
       ("D", "Submitting an attestation under the pains and penalties of perjury regarding MassHealth participation."),
       ("E", "Obtaining a separate Board licence category for collaborating pharmacists.")],
      ["B", "D"],
      "247 CMR 16.02(1)(f) attaches three conditions where prescriptive practices are included: maintaining a current "
      "Department-issued controlled substance registration during the agreement term; completing the training "
      "required by M.G.L. c. 94C, § 18(e) before initially obtaining that registration and at least biennially "
      "thereafter as a condition precedent to renewing the pharmacist licence; and submitting a MassHealth "
      "participation attestation signed under the pains and penalties of perjury.",
      {"A": "The insurance requirement is at least $1,000,000 per occurrence and applies to all agreements.",
       "B": "Correct: the controlled substance registration must be maintained during the term.",
       "C": "The additional continuing education requirement is at least five contact hours each year.",
       "D": "Correct: the sworn MassHealth attestation is one of the three conditions.",
       "E": "No separate Board licence category is created for collaborating pharmacists."},
      ["MA-CDTM-PRESCRIPTIVE-CONDITIONS"],
      ["Separate the conditions that apply to all agreements from the prescriptive-practice overlay",
       "Identify the three overlay conditions",
       "Reject figures that belong to the general qualification list"],
      ["The section 18(e) training is a condition precedent to renewing the pharmacist licence, not only the agreement."],
      "General CDTM qualifications and the prescriptive-practice overlay are different lists with different numbers."),

    q("MA-Q-0293", 2, "B3B_0293_MA_CDTM_CE_EVIDENCE", "Collaborative practice", "CDTM continuing education evidence", 4, "SBA",
      "A Massachusetts collaborating pharmacist completed her required collaborative practice continuing education "
      "two years ago and her current agreement was signed six months ago. She proposes to discard the older "
      "documentation. What does the regulation require?",
      [("A", "She may discard it, because the courses are now more than two years old."),
       ("B", "She may discard it once her pharmacist registration has been renewed."),
       ("C", "She must retain it for at least two years after the date of the current agreement."),
       ("D", "She must retain it for the entire life of her pharmacist licence."),
       ("E", "She must forward it to each supervising physician instead of retaining it.")],
      ["C"],
      "247 CMR 16.02(2) requires an authorized pharmacist participating in collaborative drug therapy management to "
      "maintain evidence of completion of required continuing education for at least two years after the date of the "
      "current collaborative practice agreement. The clock runs from the agreement date, not from the course date or "
      "the registration renewal.",
      {"A": "The retention clock does not run from the course date.",
       "B": "Registration renewal is not the trigger for discarding CDTM evidence.",
       "C": "Correct: two years measured from the date of the current agreement.",
       "D": "The regulation sets a two-year period rather than a lifetime one.",
       "E": "Forwarding to supervising physicians is a different duty, triggered by discipline."},
      ["MA-CDTM-CE-EVIDENCE"],
      ["Identify the applicable retention period for CDTM continuing education evidence",
       "Fix the clock's start at the date of the current agreement",
       "Conclude the older documentation is still within the retention period"],
      ["At least five additional contact hours of Board-approved continuing education are required in each year of the agreement term."],
      "The retention clock starts at the current agreement, so old course dates do not release the records."),

    q("MA-Q-0294", 2, "B3B_0294_MA_CDTM_DISCIPLINE_NOTICE", "Collaborative practice", "CDTM discipline notification", 4, "SBA",
      "A Massachusetts collaborating pharmacist resolves a Board matter by consent agreement that places a condition "
      "on her practice. She works under collaborative practice agreements with three supervising physicians. What "
      "does the regulation require her to do?",
      [("A", "Nothing further, because a consent agreement is not a Board order."),
       ("B", "Notify only the physician whose agreement relates to the conduct at issue."),
       ("C", "Notify the Board that the physicians have been informed, without contacting them."),
       ("D", "Provide written notification of the discipline or practice restriction to each supervising physician."),
       ("E", "Suspend all collaborative practice until the condition has been lifted.")],
      ["D"],
      "247 CMR 16.02(3) provides that whenever an authorized pharmacist participating in collaborative drug therapy "
      "management is disciplined by the Board, whether by agreement or Board order, or is otherwise subject to any "
      "practice restriction, the pharmacist must provide written notification of that discipline or practice "
      "restriction to each supervising physician.",
      {"A": "The duty is expressly triggered by discipline whether by agreement or by order.",
       "B": "Notification runs to each supervising physician.",
       "C": "The notification runs to the physicians, not to the Board.",
       "D": "Correct: written notice of the discipline or restriction to each supervising physician.",
       "E": "Automatic suspension of collaborative practice is not the stated consequence."},
      ["MA-CDTM-DISCIPLINE-NOTICE"],
      ["Recognise a consent agreement as discipline for this purpose",
       "Identify every supervising physician under a current agreement",
       "Provide written notification to each of them"],
      ["A practice restriction imposed outside formal discipline also triggers the duty."],
      "Resolution by agreement still counts as discipline, and the notice goes to every supervising physician."),
]

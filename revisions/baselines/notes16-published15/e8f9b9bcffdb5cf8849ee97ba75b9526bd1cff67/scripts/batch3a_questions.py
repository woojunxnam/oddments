"""Batch 3 tranche B3-A — 33 Area 1 questions, MA-Q-0229 through MA-Q-0261.

Every item is grounded in 247 CMR 3.00, 4.00 or 8.00 as read from the current official
Board publication on 2026-08-19. Each tests an applied decision that a pharmacist,
Manager of Record or preceptor actually has to make, on a decision path no released
question already occupies.

Key positions are steered toward the under-represented E, D and A slots, and SATA
correct-counts toward two and four, to pull the bank's answer-position distribution and
SATA key concentration back toward uniform.
"""

from __future__ import annotations


def q(qid, family, topic, subtopic, difficulty, qtype, stem, choices, correct,
      core, analysis, rules, steps, facts, trap):
    return {
        "question_id": qid,
        "family_id": family,
        "area": 1,
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
    q("MA-Q-0229", "B3A_0229_MA_PRECEPTOR_INTERN_CAP", "Pharmacy personnel", "Preceptor supervision limit", 4, "SBA",
      "A Massachusetts pharmacist preceptor is already directly supervising two pharmacy interns on the same shift. "
      "The pharmacy manager asks the preceptor to take on a third intern for that shift, noting that the pharmacy is "
      "well under its overall support-personnel ratio. How should the preceptor respond?",
      [("A", "Accept, because the overall support-personnel ratio is the only applicable limit."),
       ("B", "Accept, provided the third intern has already completed 1000 internship hours."),
       ("C", "Accept, provided the third intern works only on non-dispensing tasks."),
       ("D", "Decline, because a preceptor may supervise interns only in a teaching hospital."),
       ("E", "Decline, because a preceptor may not directly supervise more than two interns at one time.")],
      ["E"],
      "247 CMR 8.01(16) caps a registered pharmacist preceptor at directly supervising no more than two pharmacy "
      "interns at one time. That cap sits alongside, and independently of, the overall supervisory ratio in 247 CMR "
      "8.06(3), so headroom in the overall ratio does not create headroom for a third intern.",
      {"A": "The overall ratio is a separate limit and does not displace the two-intern preceptor cap.",
       "B": "Accrued internship hours do not change how many interns one preceptor may supervise.",
       "C": "The cap is on direct supervision itself, not on the tasks assigned.",
       "D": "Preceptorship is not restricted to teaching hospitals.",
       "E": "Correct: the preceptor cap is two interns supervised directly at one time."},
      ["MA-PRECEPTOR-INTERN-RATIO"],
      ["Separate the preceptor-side intern cap from the overall support-personnel ratio",
       "Count the interns already under this preceptor's direct supervision",
       "Apply the two-intern limit to the proposed third assignment"],
      ["A pharmacy intern must work under the direct supervision of a registered pharmacist preceptor."],
      "Room in the overall support-personnel ratio is not room for a third intern under one preceptor."),

    q("MA-Q-0230", "B3A_0230_MA_INTERN_SUPERVISING_TECHS", "Pharmacy personnel", "Intern supervisory authority", 4, "SBA",
      "During a busy evening shift a Massachusetts pharmacy intern, who is working under the direct supervision of a "
      "registered pharmacist preceptor, is asked to oversee two pharmacy technicians who are filling prescriptions. "
      "Which statement best describes what the regulation permits?",
      [("A", "The intern may not oversee technicians until licensed as a pharmacist."),
       ("B", "The intern may oversee technicians only if the preceptor leaves the pharmacy."),
       ("C", "The intern may oversee technicians only after 1500 internship hours."),
       ("D", "The intern may supervise pharmacy technicians while remaining under direct preceptor supervision."),
       ("E", "The intern may oversee technicians only in an institutional pharmacy setting.")],
      ["D"],
      "247 CMR 8.01(15) expressly allows a pharmacy intern acting under the direct supervision of a registered "
      "pharmacist preceptor to supervise pharmacy technicians. The intern's own supervised status is a condition of "
      "that authority, not an obstacle to it.",
      {"A": "The regulation grants this authority to interns, not only to licensed pharmacists.",
       "B": "The preceptor's direct supervision is the precondition, so the preceptor leaving would remove it.",
       "C": "No hour threshold gates this authority.",
       "D": "Correct: a supervised intern may supervise pharmacy technicians.",
       "E": "The authority is not limited to institutional settings."},
      ["MA-PRECEPTOR-INTERN-RATIO"],
      ["Confirm the intern is under direct preceptor supervision",
       "Identify the express authority for interns to supervise technicians",
       "Read the intern's supervised status as the condition rather than a bar"],
      ["A registered pharmacist preceptor may not directly supervise more than two interns at one time."],
      "The intern's own need for supervision is the condition of this authority, not a reason it is unavailable."),

    q("MA-Q-0231", "B3A_0231_MA_SUPPORT_RATIO_COMPOSITION", "Pharmacy personnel", "Support personnel supervisory ratios", 5, "SATA",
      "A Massachusetts pharmacist is scheduling a shift and wants to work with four support personnel assisting in "
      "filling prescriptions. Which staffing combinations satisfy the minimum supervisory ratio? Select all that apply.",
      [("A", "One certified pharmacy technician, one pharmacy intern and two pharmacy technicians."),
       ("B", "Two certified pharmacy technicians and two pharmacy technician trainees."),
       ("C", "One pharmacy intern, one pharmacy technician and two pharmacy technician trainees."),
       ("D", "Four pharmacy technicians whose licences are all current."),
       ("E", "One certified pharmacy technician and three pharmacy technician trainees.")],
      ["A", "B"],
      "A four-to-one ratio is available only when the composition conditions in 247 CMR 8.06(3)(a)1 are met: at least "
      "one certified pharmacy technician and one pharmacy intern, or at least two certified pharmacy technicians, or "
      "two pharmacy interns. Otherwise the maximum is three support personnel. Combination A satisfies the first "
      "condition and combination B the second.",
      {"A": "Correct: one certified pharmacy technician plus one intern satisfies the first stated condition.",
       "B": "Correct: two certified pharmacy technicians satisfy the second stated condition.",
       "C": "A single intern with no certified technician does not meet any of the four-person conditions.",
       "D": "Current licences do not substitute for the required credential mix.",
       "E": "One certified technician alone does not unlock the four-person ratio."},
      ["MA-SUPPORT-PERSONNEL-RATIO"],
      ["Recognize that four support personnel is conditional rather than a flat allowance",
       "Test each combination against the three stated credential compositions",
       "Fall back to the three-person maximum where no condition is met"],
      ["Sales clerks, messengers, delivery personnel and secretaries are excluded from the ratio when not supporting the pharmacist professionally."],
      "Four support personnel is not a headcount allowance; the credential mix is the operative condition."),

    q("MA-Q-0232", "B3A_0232_MA_RATIO_EXCLUDED_STAFF", "Pharmacy personnel", "Support personnel ratio exclusions", 4, "SBA",
      "A Massachusetts pharmacist is working with three support personnel who satisfy the applicable supervisory "
      "ratio. A cashier who rings up front-store sales and never assists with prescriptions is also on duty. The "
      "Manager of Record asks whether the cashier pushes the pharmacist over the ratio. What is the correct analysis?",
      [("A", "The cashier is excluded from the ratio because they do not support the pharmacist in a professional capacity."),
       ("B", "The cashier counts as a fourth support person and the ratio is exceeded."),
       ("C", "The cashier counts unless the pharmacy documents a written exemption."),
       ("D", "The cashier counts only during hours when the pharmacy department is open."),
       ("E", "The cashier counts as half of a support person for ratio purposes.")],
      ["A"],
      "247 CMR 8.06(3)(b) excludes sales clerks, messengers, delivery personnel, secretaries and other persons who do "
      "not fall within the definitions of intern, certified pharmacy technician, pharmacy technician or pharmacy "
      "technician trainee, so long as they are not supporting the pharmacist in any professional capacity.",
      {"A": "Correct: the exclusion turns on the absence of professional support to the pharmacist.",
       "B": "The regulation excludes such staff rather than counting them.",
       "C": "No written exemption mechanism is required for the exclusion to apply.",
       "D": "The exclusion does not depend on the pharmacy department's hours.",
       "E": "The regulation does not use fractional counting."},
      ["MA-SUPPORT-PERSONNEL-RATIO"],
      ["Classify the cashier against the four defined support-personnel categories",
       "Test whether the cashier supports the pharmacist in a professional capacity",
       "Apply the exclusion rather than counting the cashier in the ratio"],
      ["The exclusion is lost if such a person begins supporting the pharmacist professionally."],
      "The exclusion depends on what the person actually does, not on their job title alone."),

    q("MA-Q-0233", "B3A_0233_MA_CERT_LAPSE_CONSEQUENCES", "Pharmacy personnel", "Lapsed technician certification", 5, "SATA",
      "A Massachusetts pharmacy learns that a certified pharmacy technician's certification from the certifying body "
      "lapsed last week. The individual's Board pharmacy technician licence remains current. Which consequences "
      "follow? Select all that apply.",
      [("A", "The individual is limited to the duties and responsibilities of a pharmacy technician."),
       ("B", "The individual must use the title pharmacy technician."),
       ("C", "The individual is counted as a pharmacy technician when calculating supervisory ratios."),
       ("D", "The individual may no longer work in the pharmacy in any capacity."),
       ("E", "The individual's Board pharmacy technician licence is automatically suspended.")],
      ["A", "B", "C"],
      "247 CMR 8.04(3) states three consequences when a certified pharmacy technician's certification lapses: the "
      "individual is limited to pharmacy technician duties under 247 CMR 8.02, must use the pharmacy technician "
      "title, and is counted as a pharmacy technician in the 247 CMR 8.06(3) supervisory ratios. The Board licence "
      "and the certifying body's certification are separate credentials.",
      {"A": "Correct: scope reverts to the pharmacy technician duties in 247 CMR 8.02.",
       "B": "Correct: the title must change to pharmacy technician.",
       "C": "Correct: the ratio consequence follows automatically and can break a four-person shift.",
       "D": "The individual may continue working within pharmacy technician scope.",
       "E": "A lapsed certification does not suspend the separate Board licence."},
      ["MA-CERT-TECH-LAPSE"],
      ["Separate the certifying body's certification from the Board technician licence",
       "Apply the scope and title consequences of the lapse",
       "Recompute the shift's supervisory ratio with the individual counted as a pharmacy technician"],
      ["A shift built on two certified pharmacy technicians can fall out of ratio the moment one certification lapses."],
      "The staffing-ratio consequence is the one most often missed; scope and title are only two of the three."),

    q("MA-Q-0234", "B3A_0234_MA_CERT_TECH_NEW_RX_INFO", "Technician scope", "Certified technician communication", 4, "SBA",
      "A prescriber's office telephones a Massachusetts pharmacy to supply the directions that were omitted from a "
      "written prescription already on file. A certified pharmacy technician takes the call after identifying "
      "herself as a certified pharmacy technician. What does the regulation permit?",
      [("A", "She may take the omitted directions only if the prescription is for a Schedule VI drug."),
       ("B", "She may take the omitted directions only if she also performs the final verification."),
       ("C", "She may not take the information because omitted directions require professional judgment."),
       ("D", "She may take the omitted directions with the approval of the pharmacist on duty."),
       ("E", "She may take the omitted directions without any pharmacist involvement.")],
      ["D"],
      "247 CMR 8.04(4)(c) allows a certified pharmacy technician, after identifying herself as such, to receive new "
      "or omitted prescription information from the prescriber or the prescriber's agent with the approval of the "
      "pharmacist on duty. The approval condition is what distinguishes this clerical relay from the professional "
      "functions closed to technicians.",
      {"A": "The Schedule VI limitation applies to prescription transfers, not to receiving omitted information.",
       "B": "Final dispensing process validation is expressly closed to certified pharmacy technicians.",
       "C": "Receiving omitted information supplied by the prescriber is relay, not professional judgment.",
       "D": "Correct: permitted with the approval of the pharmacist on duty.",
       "E": "The pharmacist's approval is a stated condition."},
      ["MA-CERT-TECH-SCOPE"],
      ["Identify the caller as the prescriber's office supplying omitted information",
       "Confirm the certified pharmacy technician self-identified as required",
       "Apply the pharmacist-approval condition to the relay"],
      ["A plain pharmacy technician's telephone authority is limited to refills where no information has changed."],
      "Self-identification and pharmacist approval are both conditions, not formalities to be assumed."),

    q("MA-Q-0235", "B3A_0235_MA_CERT_TECH_TRANSFER_LIMIT", "Technician scope", "Certified technician transfers", 4, "SBA",
      "A Massachusetts certified pharmacy technician asks whether he may handle prescription transfers to another "
      "pharmacy. The pharmacist on duty is willing to approve. Which transfers may he perform?",
      [("A", "Transfers of any prescription, because the pharmacist has approved."),
       ("B", "Transfers of Schedules III through VI only."),
       ("C", "Transfers of Schedule VI controlled substances only."),
       ("D", "No transfers, because transfers always require a pharmacist."),
       ("E", "Transfers of any non-controlled prescription and Schedule V.")],
      ["C"],
      "247 CMR 8.04(4)(d) permits a certified pharmacy technician, with the approval of the pharmacist on duty, to "
      "perform prescription transfers between pharmacies for controlled substances in Schedule VI only, in accordance "
      "with 247 CMR 9.00. Pharmacist approval is necessary but does not widen the schedule boundary.",
      {"A": "Pharmacist approval does not extend the authority beyond Schedule VI.",
       "B": "The authority does not reach Schedules III through V.",
       "C": "Correct: Schedule VI only, with the pharmacist's approval.",
       "D": "A limited transfer authority does exist for certified pharmacy technicians.",
       "E": "Schedule V is outside the stated authority."},
      ["MA-CERT-TECH-SCOPE"],
      ["Confirm the individual holds certified pharmacy technician status",
       "Obtain the pharmacist on duty's approval as a precondition",
       "Restrict the transfers performed to Schedule VI controlled substances"],
      ["A plain pharmacy technician has no prescription transfer authority."],
      "Pharmacist approval is a precondition to a narrow authority, not a way to expand it."),

    q("MA-Q-0236", "B3A_0236_MA_TECH_REFILL_CHANGED_INFO", "Technician scope", "Technician refill authority", 4, "SBA",
      "A Massachusetts pharmacy technician telephones a prescriber's office for refill authorization. The office "
      "authorizes the refill but also increases the daily dose. The pharmacist on duty had approved the technician "
      "making refill calls. What should happen next?",
      [("A", "The technician may accept the change because the pharmacist pre-approved the call."),
       ("B", "The technician may accept the change if she reads it back to the prescriber's agent."),
       ("C", "The technician may accept the change and flag it for the pharmacist's final verification."),
       ("D", "The technician may accept the change only if she is a certified pharmacy technician."),
       ("E", "The technician may not accept the change because information has changed from the previous prescription.")],
      ["E"],
      "247 CMR 8.02(6)(c) permits a pharmacy technician to request and accept refill authorizations with the "
      "pharmacist's approval only if no information has changed from the previous prescription. A dose increase is "
      "changed information, so the interaction moves outside technician authority.",
      {"A": "The pharmacist's approval is limited to unchanged refills.",
       "B": "Reading back a change does not bring it inside technician authority.",
       "C": "Later pharmacist verification does not cure the technician accepting changed information.",
       "D": "Certified status governs receiving new or omitted information, not accepting a therapy change on a refill call.",
       "E": "Correct: the unchanged-information condition fails once the dose changes."},
      ["MA-TECH-REFILL-RELAY"],
      ["Identify the interaction as a refill authorization request by a pharmacy technician",
       "Test the unchanged-information condition against the dose increase",
       "Hand the call to the pharmacist once the condition fails"],
      ["A pharmacy technician may relay the pharmacist's offer to counsel but may not provide counseling."],
      "Pre-approval of refill calls is not approval to accept a therapy change discovered during the call."),

    q("MA-Q-0237", "B3A_0237_MA_TRAINEE_TELEPHONE_BAR", "Pharmacy personnel", "Technician trainee limits", 3, "SBA",
      "A Massachusetts pharmacy technician trainee working under the direct supervision of a pharmacist is asked to "
      "answer the pharmacy telephone during a staffing crunch and take a new prescription from a prescriber's agent. "
      "Which statement is correct?",
      [("A", "The trainee may take the prescription while under direct supervision."),
       ("B", "The trainee may take the prescription if the pharmacist listens on a second handset."),
       ("C", "The trainee may take the prescription if it is for a Schedule VI drug."),
       ("D", "The trainee may not take prescriptions over the telephone."),
       ("E", "The trainee may take the prescription after 500 hours of trainee employment.")],
      ["D"],
      "247 CMR 8.03(4)(b) allows a pharmacy technician trainee to perform the duties of a pharmacy technician under "
      "direct pharmacist supervision, but 247 CMR 8.03(4)(c) carves out an express exception: a trainee may not take "
      "prescriptions over the telephone. Direct supervision does not lift that carve-out.",
      {"A": "Direct supervision is the general condition, but the telephone carve-out overrides it.",
       "B": "Monitoring the call does not remove the express prohibition.",
       "C": "The prohibition is not limited by schedule.",
       "D": "Correct: trainees may not take prescriptions over the telephone.",
       "E": "The 500-hour figure relates to technician licensure eligibility, not telephone authority."},
      ["MA-TECH-TRAINEE-LIMITS"],
      ["Start from the general rule that a trainee may perform technician duties under direct supervision",
       "Locate the express telephone carve-out that applies to trainees only",
       "Apply the carve-out despite the supervision being in place"],
      ["A pharmacy technician trainee must be at least 16 years of age, while a pharmacy technician must be at least 18."],
      "A general grant of technician duties does not survive an express carve-out written into the same section."),

    q("MA-Q-0238", "B3A_0238_MA_TRAINEE_EMPLOYMENT_LIMIT", "Pharmacy personnel", "Trainee employment limit", 5, "SATA",
      "A Massachusetts pharmacy technician trainee has now worked 1520 hours over ten months. Which statements "
      "correctly describe the trainee employment limit? Select all that apply.",
      [("A", "The limit is 1500 hours or one year, whichever period is shorter."),
       ("B", "The Board may grant an extension beyond the limit."),
       ("C", "The limit does not yet apply if the individual has not reached 18 years of age."),
       ("D", "The limit is suspended whenever the employing pharmacy is short staffed."),
       ("E", "An individual who exceeded the limit before turning 18 must apply for a technician licence within 30 days of the 18th birthday.")],
      ["A", "B", "C", "E"],
      "247 CMR 8.03(5) limits trainee employment to 1500 hours or one year, whichever is shorter, subject to three "
      "exceptions: a Board-granted extension, the individual not yet having reached 18, or the individual not yet "
      "having completed 500 trainee hours. It also requires an individual who exceeded the limit before turning 18 to "
      "apply for a pharmacy technician licence within 30 days of the 18th birthday. Employer staffing pressure is not "
      "among the exceptions.",
      {"A": "Correct: the shorter of the two periods governs.",
       "B": "Correct: a Board-granted extension is one of the three stated exceptions.",
       "C": "Correct: not yet having reached 18 is a stated exception.",
       "D": "Staffing pressure is not one of the stated exceptions.",
       "E": "Correct: the 30-day application deadline runs from the 18th birthday."},
      ["MA-TECH-TRAINEE-LIMITS"],
      ["Read the limit as the shorter of 1500 hours and one year",
       "Check each proposed exception against the three the regulation states",
       "Apply the 30-day post-birthday application deadline where the limit was already exceeded"],
      ["Trainee eligibility also requires good moral character and no drug-related felony conviction."],
      "Only three exceptions exist, and employer convenience is not one of them."),

    q("MA-Q-0239", "B3A_0239_MA_TECH_ELIGIBILITY_ROUTES", "Pharmacy personnel", "Technician licensure eligibility", 4, "SATA",
      "An applicant for a Massachusetts pharmacy technician licence is 19, holds a high school diploma, is of good "
      "moral character and has no drug-related felony. Which of the following, standing alone, satisfies the "
      "remaining eligibility requirement? Select all that apply.",
      [("A", "Certification conferred by a Board-approved certifying body."),
       ("B", "A substantially equivalent pharmacy technician licence in good standing in another state."),
       ("C", "A Board-approved passing score on a Board-approved assessment examination taken after completing a Board-approved training program."),
       ("D", "Twelve months of employment as a pharmacy cashier in a licensed pharmacy."),
       ("E", "A letter from the employing Manager of Record attesting to the applicant's competence.")],
      ["A", "B", "C"],
      "247 CMR 8.02(3)(e) sets out three alternative routes: certification by a Board-approved certifying body, a "
      "substantially equivalent out-of-state licence in good standing, or a Board-approved passing score on a "
      "Board-approved assessment examination taken after either a Board-approved training program or a minimum of 500 "
      "hours as a pharmacy technician trainee. They are alternatives, and none of them is an employer attestation of "
      "general competence.",
      {"A": "Correct: certification by a Board-approved certifying body is a complete route.",
       "B": "Correct: a substantially equivalent out-of-state licence in good standing is a complete route.",
       "C": "Correct: the examination route is complete once its training prerequisite is satisfied.",
       "D": "Cashier employment is not pharmacy technician trainee experience and satisfies no route.",
       "E": "An employer letter of competence is not one of the routes."},
      ["MA-TECH-LICENSE-ELIGIBILITY"],
      ["Confirm the age, education, character and felony conditions are already met",
       "Treat the three statutory routes as alternatives rather than cumulative",
       "Reject proposals that substitute employer attestation for a stated route"],
      ["The 500-hour trainee alternative must be attested under the pains and penalties of perjury and witnessed by the employer."],
      "The routes are alternatives, so satisfying one is enough, but an employer attestation is not among them."),

    q("MA-Q-0240", "B3A_0240_MA_TECH_LICENCE_LAPSE", "Pharmacy personnel", "Technician licence renewal", 4, "SBA",
      "A Massachusetts pharmacy technician realises that her licence expired on her birthdate three weeks ago and "
      "that she has worked six shifts since. She intends to renew immediately and pay all back and late fees. How "
      "should the Manager of Record characterise the six shifts?",
      [("A", "Compliant, because renewal with back and late fees cures the gap retroactively."),
       ("B", "Compliant, because a technician licence carries a 30-day grace period."),
       ("C", "Compliant, provided a pharmacist directly supervised each shift."),
       ("D", "Non-compliant, but only if the Board opens an investigation."),
       ("E", "Non-compliant, because practice after the expiration date constitutes unlicensed practice.")],
      ["E"],
      "247 CMR 8.07(1) expires a pharmacy technician licence every two years on the licensee's birthdate, and 247 CMR "
      "8.07(2) provides that any practice after the expiration date constitutes unlicensed practice subject to the "
      "penalties established for it. The renewal mechanism in 247 CMR 8.07(3) restores the licence prospectively; it "
      "does not reclassify the shifts already worked.",
      {"A": "Paying back and late fees restores the licence but does not retroactively license past shifts.",
       "B": "No grace period is provided.",
       "C": "Supervision does not substitute for the individual's own licence.",
       "D": "The characterisation does not depend on whether the Board investigates.",
       "E": "Correct: practice after expiration is unlicensed practice."},
      ["MA-TECH-LICENSE-RENEWAL"],
      ["Fix the expiration date on the licensee's birthdate rather than a calendar date",
       "Classify work performed after that date as unlicensed practice",
       "Separate prospective renewal from retroactive cure"],
      ["A technician licence lapsed for more than two years may require other Board-determined conditions before renewal."],
      "Renewal is prospective; it does not convert shifts already worked into licensed practice."),

    q("MA-Q-0241", "B3A_0241_MA_CII_TRANSPORT_VS_HANDLE", "Pharmacy personnel", "Schedule II support handling", 5, "SATA",
      "A Massachusetts pharmacist is deciding which support personnel may assist with Schedule II controlled "
      "substances during a delivery to a satellite site. Which statements are correct? Select all that apply.",
      [("A", "Accountability for and security of Schedule II controlled substances is the direct responsibility of the pharmacist."),
       ("B", "A pharmacy technician may assist in transporting Schedule II controlled substances under pharmacist supervision."),
       ("C", "A certified pharmacy technician may assist in transporting and handling Schedule II controlled substances under pharmacist supervision."),
       ("D", "Written pharmacy policies and procedures must evidence the pharmacist's approval of the individual."),
       ("E", "A pharmacy technician trainee may handle non-abuse-deterrent hydrocodone-only extended release medication if supervised.")],
      ["A", "B", "C", "D"],
      "247 CMR 8.05(1) places accountability and security for Schedule II drugs directly on the pharmacist. 247 CMR "
      "8.05(2) permits a pharmacy technician to assist in transporting and a certified pharmacy technician to assist "
      "in transporting and handling, in each case under supervision, with the pharmacist's approval evidenced by "
      "written policies and procedures. 247 CMR 8.05(3) bars every technician grade from handling non-abuse-deterrent "
      "hydrocodone-only extended release medication; only supervised interns may.",
      {"A": "Correct: the pharmacist holds direct accountability and security responsibility.",
       "B": "Correct: transporting assistance is within pharmacy technician scope under supervision.",
       "C": "Correct: certified status adds handling to transporting.",
       "D": "Correct: written policies and procedures must evidence the approval and be available to the Board.",
       "E": "Trainees are barred from that medication regardless of supervision; the carve-out covers interns."},
      ["MA-CII-SUPPORT-HANDLING"],
      ["Separate transporting assistance from handling assistance across technician grades",
       "Require the pharmacist's documented approval as a precondition",
       "Apply the hydrocodone-only extended release bar across every technician grade"],
      ["The written policies and procedures must be made available to the Board on request."],
      "Certification widens Schedule II assistance but does not lift the hydrocodone-only extended release bar."),

    q("MA-Q-0242", "B3A_0242_MA_INTERN_WITHDRAWAL_NOTICE", "Pharmacy personnel", "Intern withdrawal notification", 3, "SBA",
      "A Massachusetts pharmacy intern withdraws from her PharmD program at the end of a semester. She plans to "
      "reapply next year and continues working shifts at the pharmacy. What does the regulation require of her?",
      [("A", "Nothing, because her intern licence remains valid until its expiration date."),
       ("B", "Written notification to the Board within 14 days of the withdrawal."),
       ("C", "Written notification to the Board within 30 days of the withdrawal."),
       ("D", "Notification by her preceptor rather than by her."),
       ("E", "Notification only if she does not reapply within one year.")],
      ["B"],
      "247 CMR 8.01(18) requires a pharmacy intern to provide written notification to the Board within 14 days of "
      "withdrawal from an approved college or school of pharmacy or PharmD program. The duty is the intern's own and "
      "is triggered by the withdrawal itself, not by any later decision about reapplying.",
      {"A": "Withdrawal triggers an affirmative duty regardless of the licence's expiration date.",
       "B": "Correct: written notice to the Board within 14 days.",
       "C": "The deadline is 14 days, not 30.",
       "D": "The duty runs to the intern personally.",
       "E": "The duty is not deferred pending a reapplication decision."},
      ["MA-INTERN-WITHDRAWAL-NOTICE"],
      ["Identify withdrawal from the program as the triggering event",
       "Apply the intern's personal written notification duty",
       "Measure the 14-day deadline from the withdrawal"],
      ["An intern who has graduated from an approved school may continue acting as an intern until becoming licensed as a pharmacist."],
      "Graduation and withdrawal are different events: one continues intern capacity, the other triggers a report."),

    q("MA-Q-0243", "B3A_0243_MA_PHARMD_RESIDENCY_CREDENTIAL", "Pharmacy personnel", "Residency credential", 4, "SBA",
      "A PharmD graduate of an ACPE-accredited school has accepted a pharmacy residency at a Massachusetts hospital "
      "and will begin next month. She has not yet passed NAPLEX or MPJE. Which arrangement satisfies the regulation?",
      [("A", "She may practise on the strength of her residency appointment and PharmD degree."),
       ("B", "She may practise unsupervised because a residency is a Board-approved training program."),
       ("C", "She may practise only after obtaining a Massachusetts pharmacist licence."),
       ("D", "She must hold a Massachusetts pharmacy intern licence and be supervised by a pharmacist."),
       ("E", "She must hold an out-of-state licence recognised for reciprocity.")],
      ["D"],
      "247 CMR 8.01(8) requires a PharmD graduate who has accepted a Massachusetts residency to apply for and obtain a "
      "pharmacy intern licence until obtaining a Massachusetts pharmacist licence, and provides that a graduate "
      "enrolled in a Massachusetts residency shall either hold a Massachusetts pharmacist licence or hold a "
      "Massachusetts intern licence and be supervised by a pharmacist.",
      {"A": "A residency appointment and a degree are not practice credentials.",
       "B": "The regulation does not treat a residency as authorising unsupervised practice.",
       "C": "A pharmacist licence is one permitted route, but the intern licence route is also available and is the applicable one here.",
       "D": "Correct: an intern licence with pharmacist supervision is the applicable arrangement.",
       "E": "Reciprocity is not the mechanism contemplated for this graduate."},
      ["MA-PHARMD-RESIDENCY-CREDENTIAL"],
      ["Note that the graduate holds no Massachusetts pharmacist licence yet",
       "Identify the two credentials the regulation allows during a Massachusetts residency",
       "Apply the intern licence plus supervision route to the facts"],
      ["A pharmacy intern must work under the direct supervision of a registered pharmacist preceptor."],
      "A residency is a training position, not a licence; the graduate still needs one of two named credentials."),

    q("MA-Q-0244", "B3A_0244_MA_FOREIGN_GRADUATE_ENTRY", "Pharmacy personnel", "Foreign graduate internship entry", 4, "SBA",
      "A graduate of a non-approved foreign school of pharmacy wants to begin a Massachusetts pharmacy internship "
      "next month. He holds NABP authorization to sit for the FPGEE that was issued twenty months ago. What does the "
      "regulation require before the internship may commence?",
      [("A", "Nothing further, because an FPGEE authorization does not expire once issued."),
       ("B", "FPGEC certification from NABP, which replaces the internship requirement."),
       ("C", "A current authorization issued within the preceding year, provided to the Board."),
       ("D", "A passing MPJE score achieved before the internship may start."),
       ("E", "A letter from the assigned preceptor confirming the supervision arrangements.")],
      ["C"],
      "247 CMR 8.01(7) requires a graduate of a non-approved college or school of pharmacy, before commencing a "
      "Massachusetts internship, to hold NABP authorization to sit for the FPGEE issued within the preceding year and "
      "to provide a copy to the Board with any other required documentation. An authorization issued twenty months "
      "ago falls outside that window.",
      {"A": "The authorization must have been issued within the preceding year.",
       "B": "FPGEC certification relates to examination eligibility and does not replace the internship.",
       "C": "Correct: a currently dated authorization must be held and provided to the Board.",
       "D": "MPJE follows the internship pathway rather than preceding it.",
       "E": "A preceptor letter is not the stated precondition."},
      ["MA-FOREIGN-GRADUATE-INTERNSHIP"],
      ["Identify the applicant as a graduate of a non-approved school",
       "Apply the pre-internship FPGEE authorization requirement",
       "Test the twenty-month-old authorization against the one-year currency window"],
      ["FPGEC certification from NABP is separately required for examination eligibility under 247 CMR 3.01(2)."],
      "FPGEE authorization to begin an internship and FPGEC certification for examination are different documents."),

    q("MA-Q-0245", "B3A_0245_MA_INTERNSHIP_HOUR_COMPOSITION", "Pharmacy personnel", "Internship hour composition", 5, "SATA",
      "A Massachusetts preceptor is reviewing a candidate's internship record against the Board-approved internship "
      "requirement. Which statements are correct? Select all that apply.",
      [("A", "One pathway requires at least 1500 hours, of which at least 1000 are in a Board-approved pharmacy or pharmacy-related setting."),
       ("B", "On that pathway at least 500 hours must be in clinical pharmacy, a demonstration project, manufacturing, or analytical or industrial pharmacy."),
       ("C", "An alternative pathway is at least 1500 intern hours acquired through experiential pharmacy education for a graduate of an ACPE-accredited institution."),
       ("D", "The Board may grant credit for out-of-state internship experience on appropriate documentation."),
       ("E", "All 1500 hours must be acquired within a single calendar year.")],
      ["A", "B", "C", "D"],
      "247 CMR 8.01(1) sets a 1500-hour requirement with a 1000-hour and 500-hour internal composition on the first "
      "pathway and an alternative 1500-hour experiential pathway for graduates of ACPE-accredited institutions. 247 "
      "CMR 8.01(11) allows credit for out-of-state experience on an affidavit or certificate from the jurisdiction "
      "where it was acquired, and 247 CMR 8.01(5) provides that hours may be acquired throughout a calendar year "
      "rather than compressed into one.",
      {"A": "Correct: the 1000-hour component sits inside the 1500-hour total.",
       "B": "Correct: the 500-hour component names those four settings.",
       "C": "Correct: the experiential pathway is an alternative for ACPE-accredited graduates.",
       "D": "Correct: out-of-state experience is creditable on documentation.",
       "E": "No single-calendar-year confinement is imposed; hours may be acquired throughout a calendar year."},
      ["MA-INTERN-HOUR-COMPOSITION"],
      ["Distinguish the two internship pathways",
       "Check the internal 1000-hour and 500-hour composition on the first pathway",
       "Apply the documentation route for out-of-state experience"],
      ["A pharmacy intern may not receive more than 12 hours of internship credit per day."],
      "The headline 1500 hours hides an internal composition that a raw hour count can satisfy without meeting."),

    q("MA-Q-0246", "B3A_0246_MA_SUPPORT_TITLE_ACCURACY", "Pharmacy personnel", "Support personnel identification", 3, "SBA",
      "A Massachusetts pharmacy has just learned that a staff member's technician certification lapsed. The staff "
      "member continues to wear a name tag reading Certified Pharmacy Technician while the pharmacy sorts out the "
      "paperwork. What should the pharmacy do about the name tag?",
      [("A", "Change the tag to read Pharmacy Technician."),
       ("B", "Leave the tag unchanged until the certification is restored."),
       ("C", "Remove the name tag entirely until the certification is restored."),
       ("D", "Change the tag to read Pharmacy Technician Trainee."),
       ("E", "Leave the tag unchanged if the pharmacist on duty documents the lapse.")],
      ["A"],
      "247 CMR 8.04(3)(b) requires an individual whose certification has lapsed to use the title pharmacy technician, "
      "and 247 CMR 8.02(6)(a) requires a pharmacy technician to wear a name tag with the individual's first name and "
      "that title. The displayed title must track the credential actually held.",
      {"A": "Correct: the individual must use the pharmacy technician title.",
       "B": "Continuing to display a lapsed credential misstates the individual's status.",
       "C": "A name tag is still required; the title on it changes.",
       "D": "Trainee is a different credential the individual does not hold.",
       "E": "Internal documentation does not authorise displaying a lapsed credential."},
      ["MA-SUPPORT-NAME-TAGS", "MA-CERT-TECH-LAPSE"],
      ["Establish which credential the individual currently holds",
       "Match the required title to that credential",
       "Correct the displayed title rather than removing identification"],
      ["Interns wear a tag showing their name and the words pharmacy intern."],
      "The tag must state the credential actually held, not the role the pharmacy would like to assign."),

    q("MA-Q-0247", "B3A_0247_MA_MOR_SUPPORT_DOCUMENTATION", "Pharmacy management", "Support personnel documentation", 4, "SBA",
      "A Board inspector asks a Massachusetts Manager of Record for written descriptions of the duties delegated to "
      "the pharmacy's technicians and their scopes of responsibility. The Manager of Record has never filed such "
      "documents with the Board. What is the correct position?",
      [("A", "The documents were required to be filed with the Board in advance and the omission is a violation."),
       ("B", "No such documents are required in a retail setting."),
       ("C", "The documents are required only for certified pharmacy technicians."),
       ("D", "The documents must be made available to the Board on request, so they must be produced now."),
       ("E", "The documents are required only if the pharmacy uses on-the-job training.")],
      ["D"],
      "247 CMR 8.06(1) requires a pharmacist Manager of Record, or an institutional Director of Pharmacy, to make "
      "available to the Board on request a list of currently employed certified pharmacy technicians, pharmacy "
      "technicians and trainees, a written description of the duties delegated to them, and a written description of "
      "their scopes of responsibility. The obligation is production on request rather than advance filing.",
      {"A": "The regulation requires availability on request, not advance filing.",
       "B": "The requirement is not limited to institutional settings.",
       "C": "The requirement covers all three support categories.",
       "D": "Correct: the documents must be produced on the Board's request.",
       "E": "On-the-job training guidelines are a separate requirement under 247 CMR 8.06(2)."},
      ["MA-SUPPORT-DOCUMENTATION-DUTY"],
      ["Identify the Manager of Record as the duty holder",
       "Recognise the obligation as production on request rather than pre-filing",
       "Produce the list, delegated duties and scopes of responsibility"],
      ["Copies of on-the-job training program guidelines must also be provided to the Board on request."],
      "Never having filed the documents is not a defence when the duty is to have them available on request."),

    q("MA-Q-0248", "B3A_0248_MA_EXAM_ELIGIBILITY_PATHWAYS", "Licensure", "Examination eligibility", 4, "SATA",
      "Two applicants seek Massachusetts pharmacist licensure by examination. One graduated from an ACPE-accredited "
      "school; the other graduated from a non-approved foreign school. Which statements are correct? Select all that apply.",
      [("A", "Both applicants must have completed a pharmacy internship in accordance with 247 CMR 8.01(1)."),
       ("B", "The foreign graduate must have received official FPGEC certification from NABP."),
       ("C", "Both applicants must be 18 years of age or older by the scheduled examination date."),
       ("D", "FPGEC certification relieves the foreign graduate of the internship requirement."),
       ("E", "The ACPE-accredited graduate is exempt from the good moral character requirement.")],
      ["A", "B", "C"],
      "247 CMR 3.01(1) and (2) impose the internship requirement, the age requirement measured by the scheduled "
      "examination date and the good moral character requirement on both pathways. FPGEC certification substitutes "
      "for the accredited degree on the foreign pathway; it does not substitute for the internship.",
      {"A": "Correct: the internship requirement applies on both pathways.",
       "B": "Correct: official FPGEC certification from NABP is required on the foreign pathway.",
       "C": "Correct: the age requirement is measured by the scheduled examination date.",
       "D": "FPGEC certification replaces the accredited degree, not the internship.",
       "E": "Good moral character is required on both pathways."},
      ["MA-PHARMACIST-EXAM-ELIGIBILITY"],
      ["Separate the requirements common to both pathways from the pathway-specific ones",
       "Identify what FPGEC certification actually substitutes for",
       "Confirm the internship requirement survives on the foreign pathway"],
      ["The foreign graduate must also submit an official copy of the FPGEC certificate and the Board must receive official NABP notification."],
      "FPGEC certification stands in for the accredited degree, not for the internship."),

    q("MA-Q-0249", "B3A_0249_MA_EXAM_ONE_YEAR_LINKAGE", "Licensure", "Examination scoring and retake", 5, "SBA",
      "A Massachusetts applicant passed NAPLEX but failed MPJE. Fourteen months after the original MPJE "
      "administration date she applies to retake MPJE. What is the consequence of the delay?",
      [("A", "Her NAPLEX score is unaffected because NAPLEX and MPJE are scored independently."),
       ("B", "She may retake MPJE once more before any additional requirement applies."),
       ("C", "She must obtain a Board waiver before retaking MPJE."),
       ("D", "She must apply to retake both NAPLEX and MPJE."),
       ("E", "She must complete additional internship hours before retaking MPJE.")],
      ["D"],
      "247 CMR 3.01(7) requires an applicant who fails either examination to reapply for that examination within one "
      "year of the original administration date for both scores to be considered together. If the applicant does not "
      "pass both within that one-year period, the applicant must apply to retake both NAPLEX and MPJE.",
      {"A": "The scores are considered together only within the one-year window.",
       "B": "The regulation keys the consequence to the window, not to a count of attempts.",
       "C": "No waiver mechanism is provided for the window.",
       "D": "Correct: missing the window forces a retake of both examinations.",
       "E": "Additional internship hours are not the stated consequence."},
      ["MA-PHARMACIST-EXAM-SCORING"],
      ["Identify the original MPJE administration date as the start of the window",
       "Measure the fourteen-month delay against the one-year window",
       "Apply the consequence that both examinations must be retaken"],
      ["A passing score is not less than 75% on each of NAPLEX and MPJE."],
      "The one-year clock governs whether an already-passed score still counts, not how many retakes are allowed."),

    q("MA-Q-0250", "B3A_0250_MA_RECIPROCITY_FINAL_DETERMINATION", "Licensure", "Licensure by reciprocity", 4, "SBA",
      "An applicant for Massachusetts licensure by reciprocity is notified by NABP that she does not meet the "
      "requirements for licence transfer. She believes NABP misread her disciplinary history. What avenue does the "
      "regulation give her?",
      [("A", "She may appeal to NABP only, because NABP administers the transfer program."),
       ("B", "She may reapply after one year with corrected documentation."),
       ("C", "She must instead apply for licensure by examination."),
       ("D", "She may request in writing that the Board review the basis of NABP's decision."),
       ("E", "She may request a hearing before the Division of Administrative Law Appeals.")],
      ["D"],
      "247 CMR 3.02(1)(a) allows an applicant notified by NABP that she does not meet the reciprocity requirements to "
      "request in writing that the Board review the basis of that decision, and 247 CMR 3.02(1)(b) makes the Board "
      "the final determiner of eligibility. NABP acts as the Board's agent for the preliminary evaluation only.",
      {"A": "NABP conducts the preliminary evaluation; the Board makes the final determination.",
       "B": "Waiting a year is not the remedy the regulation provides.",
       "C": "Switching to examination is not required when Board review is available.",
       "D": "Correct: a written request for Board review of NABP's basis.",
       "E": "The regulation directs the request to the Board."},
      ["MA-LICENSURE-RECIPROCITY"],
      ["Characterise NABP's role as preliminary evaluation on the Board's behalf",
       "Locate the applicant's right to request Board review of that basis",
       "Direct the written request to the Board as final determiner"],
      ["An approved reciprocity application is valid for one year after the date of NABP approval."],
      "NABP's preliminary decision is not the last word; the Board retains the final determination."),

    q("MA-Q-0251", "B3A_0251_MA_RECIPROCITY_REQUIREMENTS", "Licensure", "Reciprocity requirements", 4, "SATA",
      "A pharmacist licensed by examination in another state seeks Massachusetts licensure by reciprocity. Which "
      "statements are correct? Select all that apply.",
      [("A", "The applicant must be in good standing in all states where the applicant holds a licence."),
       ("B", "A passing MPJE score of at least 75% is required."),
       ("C", "Documentation of internship experience in accordance with 247 CMR 8.01 is required."),
       ("D", "The applicant may be required to appear personally before the Board."),
       ("E", "Reciprocity waives the MPJE because the applicant already passed a jurisprudence examination elsewhere.")],
      ["A", "B", "C", "D"],
      "247 CMR 3.02 requires good standing in all states where the applicant is licensed and a jurisdiction whose "
      "competency requirements are equal to those of Massachusetts. 247 CMR 3.02(2)(a) and (3)(a) require documented "
      "internship experience, a passing MPJE score of at least 75%, and personal appearance before the Board if "
      "requested. MPJE is not waived on the reciprocity pathway.",
      {"A": "Correct: good standing must extend to every state where the applicant holds a licence.",
       "B": "Correct: a passing MPJE score of at least 75% is required.",
       "C": "Correct: internship experience must be documented.",
       "D": "Correct: personal appearance may be required.",
       "E": "MPJE is expressly required on the reciprocity pathway."},
      ["MA-LICENSURE-RECIPROCITY"],
      ["Confirm the applicant was licensed by examination elsewhere",
       "Apply the good-standing requirement across all held licences",
       "Retain the Massachusetts MPJE and internship documentation requirements"],
      ["The Board must recognise the other jurisdiction for reciprocity purposes."],
      "Reciprocity transfers a licence, not the Massachusetts jurisprudence requirement."),

    q("MA-Q-0252", "B3A_0252_MA_RETIRED_STATUS_LIMITS", "Licensure", "Retired licence status", 4, "SATA",
      "A Massachusetts pharmacist is considering petitioning for retired licence status. Which statements are "
      "correct? Select all that apply.",
      [("A", "Retired status is a nondisciplinary status."),
       ("B", "A licensee with retired status may not practise."),
       ("C", "Eligibility requires that the licence is not surrendered, suspended or revoked at the time of the petition."),
       ("D", "Retired status prevents the Board from taking disciplinary action against the licensee."),
       ("E", "The Board must review any later petition to return the licence to current status.")],
      ["A", "B", "C"],
      "247 CMR 3.04 makes retired status nondisciplinary, bars practice while retired, and conditions eligibility on "
      "the licence not being surrendered, suspended or revoked and on an intent to retire permanently from active "
      "practice in the Commonwealth and all other jurisdictions. It expressly preserves the Board's power to "
      "discipline a retired licensee and expressly permits the Board to decline to review a reinstatement petition.",
      {"A": "Correct: the regulation calls retired status nondisciplinary.",
       "B": "Correct: a retired licensee may not practise.",
       "C": "Correct: the licence must be free of surrender, suspension or revocation at the time of the petition.",
       "D": "The Board may still discipline a licensee whose status is retired.",
       "E": "The Board may decline to review a petition for reinstatement or return to current status."},
      ["MA-LICENSURE-RETIREMENT"],
      ["Classify retired status as voluntary and nondisciplinary",
       "Apply the bar on practice while retired",
       "Preserve the Board's disciplinary reach and its discretion over reinstatement"],
      ["The licensee must demonstrate intent to retire permanently from practice in all jurisdictions, not only Massachusetts."],
      "Nondisciplinary does not mean protected; retirement is neither a shield nor a guaranteed round trip."),

    q("MA-Q-0253", "B3A_0253_MA_PROTECTED_ACTIVITY_LICENSURE", "Licensure", "Protected health care activity", 4, "SBA",
      "A pharmacist applying to renew a Massachusetts registration discloses an out-of-state disciplinary sanction "
      "imposed solely for dispensing medication for gender-affirming health care services. The services would have "
      "been lawful in Massachusetts and consistent with good professional practice here. How should the renewal be "
      "treated?",
      [("A", "Renewal must be denied because any out-of-state discipline is disqualifying."),
       ("B", "Renewal may be granted only after the other state vacates its sanction."),
       ("C", "Renewal must be deferred pending a Massachusetts investigation of the same conduct."),
       ("D", "Renewal may not be denied on the basis of that sanction."),
       ("E", "Renewal may be granted only with a probationary condition.")],
      ["D"],
      "247 CMR 3.05 provides that no person shall be denied initial licensure or renewal due to any complaint, "
      "criminal charge, conviction, judgment, discipline or other sanction arising from providing or assisting in "
      "providing, or dispensing medication for, reproductive or gender-affirming health care services, so long as the "
      "services would have been lawful in Massachusetts and are consistent with standards for good professional "
      "practice here. Both qualifiers are satisfied on these facts.",
      {"A": "The regulation removes this category of sanction as a basis for denial.",
       "B": "The protection does not depend on the other state vacating its action.",
       "C": "Deferring renewal pending investigation of the protected conduct would defeat the protection.",
       "D": "Correct: the sanction may not be used as a basis for denial.",
       "E": "Attaching probation on that basis would be denial in substance."},
      ["MA-PROTECTED-HEALTH-CARE-LICENSURE"],
      ["Identify the sanction as arising solely from protected health care activity",
       "Test the lawful-in-Massachusetts and good-practice qualifiers",
       "Apply the bar on using that sanction as a basis for denial"],
      ["Parallel protections apply to pharmacy support personnel under 247 CMR 8.08 and to pharmacies under 247 CMR 6.18."],
      "The protection is conditional on the two qualifiers, but once they are met the sanction cannot be recycled as a denial basis."),

    q("MA-Q-0254", "B3A_0254_MA_REGISTRATION_LAPSE_LADDER", "Licensure", "Personal registration renewal", 5, "SBA",
      "A Massachusetts pharmacist stopped practising and let his personal registration lapse. It has now been "
      "lapsed for about 30 months. It was never suspended or revoked. He wants to return to practice. What does the "
      "regulation require?",
      [("A", "Payment of back and late fees only."),
       ("B", "Completion of additional continuing education contact hours only."),
       ("C", "Taking and passing both NAPLEX and MPJE."),
       ("D", "Taking and passing the MPJE and meeting all other Board conditions."),
       ("E", "Application for licensure by reciprocity from another state.")],
      ["D"],
      "247 CMR 4.02(5) provides that an applicant who has failed to renew for more than two years, and whose "
      "registration has not been suspended or revoked, shall take and pass the MPJE and meet all other Board-"
      "determined conditions. The NAPLEX possibility in 247 CMR 4.02(7) belongs to the disciplinary ladder, not to a "
      "simple failure to renew.",
      {"A": "Fees alone address a short lapse, not one beyond two years.",
       "B": "Additional contact hours are the tool for a lapse of more than 60 days, not beyond two years.",
       "C": "NAPLEX may be added where a registration was revoked or suspended for more than two years, which is not this case.",
       "D": "Correct: MPJE plus all other Board conditions.",
       "E": "Reciprocity is not the route back from a lapsed Massachusetts registration."},
      ["MA-PHARMACIST-REGISTRATION-RENEWAL", "MA-REGISTRATION-DISCIPLINE-REINSTATEMENT"],
      ["Establish that the lapse was a failure to renew rather than discipline",
       "Place the 30-month lapse beyond the two-year threshold",
       "Apply the MPJE requirement without importing the disciplinary NAPLEX condition"],
      ["Personal registrations expire on December 31st of each even-numbered year."],
      "The failure-to-renew ladder and the post-discipline ladder look alike but carry different consequences."),

    q("MA-Q-0255", "B3A_0255_MA_DISCIPLINE_REINSTATEMENT_TIERS", "Licensure", "Reinstatement after discipline", 5, "SATA",
      "A Massachusetts pharmacist's personal registration was suspended for nine months as a disciplinary sanction. "
      "The suspension has ended and she seeks renewal. Which statements are correct? Select all that apply.",
      [("A", "She shall take and pass the MPJE as a prerequisite to renewal."),
       ("B", "She shall meet all conditions determined by the Board."),
       ("C", "The Board may also require her to take and pass the NAPLEX."),
       ("D", "Her suspension falls in the band between six months and two years."),
       ("E", "Serving the suspension period is by itself sufficient for renewal.")],
      ["A", "B", "D"],
      "247 CMR 4.02(6) applies to a registration revoked or suspended for between six months and two years and "
      "requires the applicant to take and pass the MPJE and meet all Board-determined conditions. The additional "
      "NAPLEX possibility appears only in 247 CMR 4.02(7), which governs revocation or suspension for more than two "
      "years. A nine-month suspension sits in the first band.",
      {"A": "Correct: MPJE is required in this band.",
       "B": "Correct: all Board-determined conditions must also be met.",
       "C": "The NAPLEX possibility belongs to the longer band, not to a nine-month suspension.",
       "D": "Correct: nine months falls between six months and two years.",
       "E": "Serving the suspension does not by itself restore the registration."},
      ["MA-REGISTRATION-DISCIPLINE-REINSTATEMENT"],
      ["Place the nine-month suspension in the correct regulatory band",
       "Apply the MPJE and Board-conditions requirements for that band",
       "Withhold the NAPLEX condition reserved for the longer band"],
      ["A registration revoked or suspended for more than two years may also require NAPLEX."],
      "The two reinstatement bands differ precisely in whether NAPLEX may be added."),

    q("MA-Q-0256", "B3A_0256_MA_CE_ANNUAL_STRUCTURE", "Licensure", "Continuing education structure", 5, "SBA",
      "A Massachusetts pharmacist completed no continuing education in the first calendar year of her two-year "
      "renewal cycle. She plans to complete all 40 contact hours in the second calendar year, including 30 hours of "
      "home study. Why does this plan fail?",
      [("A", "Because contact hours may not be earned in the second year of a cycle."),
       ("B", "Because home study may not be applied toward the requirement at all."),
       ("C", "Because 40 contact hours exceed the annual maximum permitted."),
       ("D", "Because a minimum of 20 contact hours is required in each calendar year and hours may not be carried over."),
       ("E", "Because pharmacy law hours must be completed before any other subject area.")],
      ["D"],
      "247 CMR 4.03(4) requires a minimum of 20 contact hours in each calendar year of the two-year cycle, and 247 "
      "CMR 4.03(5) bars carrying hours from one calendar year to another. A year with zero hours therefore cannot be "
      "repaired later. The plan also breaches the 15-hour annual home-study cap in 247 CMR 4.03(4)(b).",
      {"A": "Hours may be earned in the second year; the problem is the empty first year.",
       "B": "Home study is permitted up to 15 contact hours per calendar year.",
       "C": "There is no annual maximum of 40; there is a daily maximum of eight.",
       "D": "Correct: the annual minimum plus the no-carry-over rule defeats the plan.",
       "E": "No sequencing requirement applies among subject areas."},
      ["MA-CE-ANNUAL-STRUCTURE"],
      ["Read the 40-hour cycle total together with the 20-hour annual minimum",
       "Apply the bar on carrying hours between calendar years",
       "Check the home-study proposal against the 15-hour annual cap"],
      ["A registrant may not earn more than eight contact hours of continuing education in a calendar day."],
      "The cycle total is not a single pot; the annual minimum and no-carry-over rule make an empty year unrecoverable."),

    q("MA-Q-0257", "B3A_0257_MA_CE_PRACTICE_OVERLAYS", "Licensure", "Practice-specific continuing education", 5, "SATA",
      "A Massachusetts pharmacist oversees sterile compounding in a pharmacy licensed under M.G.L. c. 112, § 39G and "
      "also administers vaccines. Which continuing education overlays apply to her? Select all that apply.",
      [("A", "At least five contact hours per calendar year in sterile compounding."),
       ("B", "At least one contact hour on immunizations during the two-year renewal cycle."),
       ("C", "At least two contact hours per calendar year in pharmacy law."),
       ("D", "At least three contact hours per calendar year in complex non-sterile compounding."),
       ("E", "At least ten contact hours per calendar year in sterile compounding because she both oversees and practises in a licensed setting.")],
      ["A", "B", "C"],
      "247 CMR 4.03(4)(c) requires five contact hours per calendar year in sterile compounding for a registrant who "
      "oversees or is directly engaged in it or practises in a § 39G or § 39I pharmacy. 247 CMR 4.03(4)(e) requires "
      "one immunization contact hour per two-year cycle. 247 CMR 4.03(4)(a) requires two pharmacy law contact hours "
      "per calendar year of every registrant. The complex non-sterile overlay attaches to § 39H practice, which is "
      "not present, and the overlays are not doubled for satisfying more than one trigger.",
      {"A": "Correct: five contact hours per calendar year for sterile compounding.",
       "B": "Correct: one immunization contact hour across the two-year cycle.",
       "C": "Correct: the pharmacy law overlay applies to every registrant each calendar year.",
       "D": "The complex non-sterile overlay attaches to § 39H practice, which these facts do not include.",
       "E": "Meeting more than one trigger for the same overlay does not multiply the requirement."},
      ["MA-CE-PRACTICE-SPECIFIC", "MA-CE-ANNUAL-STRUCTURE"],
      ["Identify each practice trigger the pharmacist actually meets",
       "Match each trigger to its overlay and to whether it is annual or per cycle",
       "Refuse to double an overlay that has more than one qualifying trigger"],
      ["The compounding overlays are measured per calendar year while the immunization overlay is measured per renewal cycle."],
      "Overlaps in triggers do not add up; the sterile compounding overlay is five hours however many triggers apply."),

    q("MA-Q-0258", "B3A_0258_MA_CE_RELIEF_MECHANISMS", "Licensure", "Continuing education relief", 4, "SBA",
      "A Massachusetts pharmacist was hospitalised for much of the renewal cycle and completed only part of her "
      "required continuing education. She wants to renew. What does the regulation direct her to do?",
      [("A", "Self-certify the shortfall on the renewal application and renew without further steps."),
       ("B", "Renew now and complete the missing contact hours within the following calendar year."),
       ("C", "Submit a sworn detailed statement of the extenuating circumstances for the Board to determine."),
       ("D", "Apply for retired status until the missing contact hours can be completed."),
       ("E", "Request that her employer certify the extenuating circumstances directly to the Board.")],
      ["C"],
      "247 CMR 4.03(6) provides that a registrant who has failed to complete the requisite contact hours shall submit "
      "to the Board a detailed statement, signed under the penalties of perjury, setting out the extenuating "
      "circumstances with detail and specificity, and the Board then determines whether renewal is granted and "
      "notifies the applicant of its determination and reasons.",
      {"A": "Self-certification of a shortfall is not the mechanism provided.",
       "B": "There is no make-up allowance in the following year; hours may not be carried over.",
       "C": "Correct: a sworn detailed statement, with the Board determining the outcome.",
       "D": "Retired status bars practice and is not a continuing education mechanism.",
       "E": "The statement is the registrant's own and is signed under the penalties of perjury."},
      ["MA-CE-EXEMPTIONS", "MA-CE-ANNUAL-STRUCTURE"],
      ["Identify the shortfall as a continuing education failure rather than a lapse in registration",
       "Locate the extenuating-circumstances mechanism",
       "Submit a sworn detailed statement and leave the determination to the Board"],
      ["A registrant is not required to complete continuing education in the calendar year of graduation from an approved school."],
      "Extenuating circumstances are a Board determination on a sworn statement, not a self-applied exemption."),

    q("MA-Q-0259", "B3A_0259_MA_CE_MILITARY_RELIEF", "Licensure", "Military continuing education relief", 4, "SBA",
      "A Massachusetts pharmacist entered active armed forces service in November of an even-numbered year and was "
      "released from active duty the following spring. Which statement correctly describes the effect on her "
      "registration and continuing education?",
      [("A", "Her registration lapsed on December 31st of that even-numbered year."),
       ("B", "Her registration remains valid until 90 days following release from active duty, and the continuing education requirement does not apply to that biennial cycle."),
       ("C", "Her registration remains valid indefinitely while she is on active duty and continuing education is merely deferred."),
       ("D", "Her registration remains valid for 90 days but the continuing education requirement still applies to that cycle."),
       ("E", "Her registration remains valid only if she requested a waiver before deploying.")],
      ["B"],
      "247 CMR 4.02(8), applying M.G.L. c. 112, § 1B(c), keeps the registration of a registrant in active armed "
      "forces service valid until 90 days following release from active duty, and provides that the continuing "
      "education requirement does not apply to the biennial cycle immediately preceding December 31st of an "
      "even-numbered year where the registrant is in active service after October 1st of that year. Entering service "
      "in November satisfies that date condition.",
      {"A": "The provision preserves validity rather than allowing the registration to lapse.",
       "B": "Correct: validity to 90 days after release, with the continuing education requirement disapplied for that cycle.",
       "C": "Validity is measured to 90 days after release, and the requirement is disapplied rather than deferred.",
       "D": "The continuing education requirement does not apply to that cycle.",
       "E": "No advance waiver request is required."},
      ["MA-CE-EXEMPTIONS"],
      ["Confirm active service began after October 1st of the even-numbered year",
       "Apply the 90-day post-release validity period",
       "Disapply the continuing education requirement for the affected biennial cycle"],
      ["Personal registrations otherwise expire on December 31st of each even-numbered year."],
      "The relief turns on the October 1st date condition, not merely on having served at some point in the cycle."),

    q("MA-Q-0260", "B3A_0260_MA_CE_RECORD_CONTENT", "Licensure", "Continuing education records", 4, "SATA",
      "A Massachusetts pharmacist is selected for a random continuing education audit. Which elements must her "
      "documentation or statements of credit contain? Select all that apply.",
      [("A", "The name of the authorized provider."),
       ("B", "The title and number of the continuing education program."),
       ("C", "The date of completion of the program."),
       ("D", "The number of contact hours earned."),
       ("E", "The registrant's employer at the time of the program.")],
      ["A", "B", "C", "D"],
      "247 CMR 4.06(1) requires documentation or a statement of credit containing the name of the authorized "
      "provider, the participant's name, the title and number of the program, the date of completion and the number "
      "of contact hours earned, retained for at least two years from the date of completion. 247 CMR 4.06(2) requires "
      "production to the Board on request and in response to random audits. The registrant's employer is not among "
      "the required elements.",
      {"A": "Correct: the authorized provider's name is required.",
       "B": "Correct: the program title and number are required.",
       "C": "Correct: the completion date is required.",
       "D": "Correct: the contact hours earned are required.",
       "E": "The employer is not a required element of the documentation."},
      ["MA-CE-RECORDKEEPING"],
      ["Identify the audit as triggering the production duty",
       "Check the documentation against the five required elements",
       "Confirm retention runs at least two years from the date of completion"],
      ["Retention is measured from the date of completion rather than from the renewal date."],
      "A bare attendance confirmation is not enough; specific data elements are prescribed."),

    q("MA-Q-0261", "B3A_0261_MA_CE_PROVIDER_CLOCKS", "Licensure", "Continuing education provider approval", 5, "SBA",
      "A Massachusetts provider submitted a program approval request 20 days before the planned presentation date "
      "and the Executive Director's designee denied it. The provider wants to challenge the denial. Which statement "
      "correctly describes the position?",
      [("A", "The submission was timely, so the denial can only have been substantive."),
       ("B", "The provider may appeal to the full Board by written petition within 30 days of the notice of denial."),
       ("C", "The provider must resubmit rather than appeal, because a designee's decision is unreviewable."),
       ("D", "The provider may appeal only if it holds current ACPE accreditation."),
       ("E", "The provider must appeal within 30 days of the planned presentation date.")],
      ["B"],
      "247 CMR 4.04(2) requires a request to be submitted no less than 30 days before the proposed presentation, so a "
      "20-day submission is untimely. 247 CMR 4.04(4) separately allows a provider whose request is denied by the "
      "Executive Director or designee to appeal to the full Board by written petition submitted within 30 days of the "
      "notice of denial. The two 30-day periods run from different events.",
      {"A": "A 20-day submission is untimely against the 30-day advance requirement.",
       "B": "Correct: written petition to the full Board within 30 days of the notice of denial.",
       "C": "A designee's denial is expressly reviewable by the full Board.",
       "D": "ACPE standing bears on authorized-provider status, not on the right to appeal.",
       "E": "The appeal clock runs from the notice of denial, not from the presentation date."},
      ["MA-CE-PROVIDER-APPROVAL"],
      ["Test the submission against the 30-day advance requirement",
       "Separate the advance-submission clock from the appeal clock",
       "Measure the appeal window from the notice of denial"],
      ["A provider in good standing with ACPE or AMA CME Category 1 is considered an authorized provider."],
      "Two 30-day clocks appear in the same section and run from different events."),
]

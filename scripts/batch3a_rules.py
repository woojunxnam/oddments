"""Canonical Area 1 rule records required by Batch 3 tranche B3-A.

Every rule here was read from the current official Board of Registration in Pharmacy
publication of 247 CMR 3.00, 4.00 and 8.00 on 2026-08-19 (247 CMR 3.00 and 8.00 revised
4/25/25 effective 1/9/25; 247 CMR 4.00 as currently published). No existing rule states
these propositions, and the existing Area 1 rules are frozen inside released questions'
dependency snapshots, so they are not edited.
"""

from __future__ import annotations

CMR3 = "https://www.mass.gov/regulations/247-CMR-300-pharmacist-licensure-requirements"
CMR4 = "https://www.mass.gov/regulations/247-CMR-400-personal-registration-renewal-continuing-education-requirement"
CMR8 = "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians"

VERIFIED = "2026-08-19"
NOTES = (
    "Read in the current official Board of Registration in Pharmacy publication of {part} on "
    "2026-08-19 during Batch 3 tranche B3-A authoring under Issue #91. A fresh independent legal "
    "and full-bank realism audit is still required before release."
)


def _rule(rule_id, title, subtopic, summary, relevance, section, url, part,
          confusions, topic="Pharmacy personnel", numeric=(), exceptions=(), related=()):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": "MA",
        "area": 1,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": relevance,
        "authority": [
            {
                "type": "PROMULGATED_REGULATION",
                "name": "Massachusetts Board of Registration in Pharmacy regulations",
                "section": section,
                "url": url,
            }
        ],
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": VERIFIED,
        "numeric_facts": list(numeric),
        "exceptions": list(exceptions),
        "common_confusions": list(confusions),
        "related_rule_ids": list(related),
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": NOTES.format(part=part),
    }


RULES = [
    # ---------------- 247 CMR 8.00 — interns, technicians, supervision ----------------
    _rule(
        "MA-PRECEPTOR-INTERN-RATIO",
        "Preceptor limit on directly supervised pharmacy interns",
        "Preceptor supervision limit",
        "Under 247 CMR 8.01(16) a registered pharmacist preceptor shall not directly supervise more "
        "than two pharmacy interns at one time. Separately, 247 CMR 8.01(15) allows a pharmacy intern "
        "who is acting under the direct supervision of a registered pharmacist preceptor to supervise "
        "pharmacy technicians.",
        "Tests the preceptor-side cap on interns and the distinct fact that a supervised intern may "
        "itself supervise technicians, rather than the overall support-personnel ratio.",
        "247 CMR 8.01(15) and (16)", CMR8, "247 CMR 8.00",
        ["The two-intern preceptor cap is separate from the overall supervisory ratio in 247 CMR 8.06(3).",
         "An intern supervising technicians does not stop the intern from needing direct preceptor supervision."],
        numeric=[{"fact": "maximum interns directly supervised by one preceptor", "value": 2, "unit": "interns",
                  "conditions": "at one time"}],
        related=["MA-SUPPORT-PERSONNEL-RATIO", "MA-INTERN-SUPERVISION"],
    ),
    _rule(
        "MA-SUPPORT-PERSONNEL-RATIO",
        "Minimum supervisory ratios for pharmacy support personnel",
        "Support personnel supervisory ratios",
        "Under 247 CMR 8.06(3)(a) a pharmacist using interns, certified pharmacy technicians, pharmacy "
        "technicians and pharmacy technician trainees to assist in filling prescriptions may supervise a "
        "maximum of four support personnel only if at least one of the four is a certified pharmacy "
        "technician and one is a pharmacy intern, or at least two are certified pharmacy technicians, or "
        "two are pharmacy interns; otherwise the maximum is three support personnel and at least one of "
        "the three must be a pharmacy intern or a certified pharmacy technician. Under 247 CMR 8.06(3)(b) "
        "sales clerks, messengers, delivery personnel, secretaries and other persons outside those "
        "definitions are excluded from the ratio so long as they are not supporting the pharmacist in any "
        "professional capacity.",
        "Tests the composition conditions that unlock a four-to-one ratio rather than a flat headcount, "
        "and which staff are excluded from the count entirely.",
        "247 CMR 8.06(3)", CMR8, "247 CMR 8.00",
        ["A four-to-one ratio is not available on headcount alone; the credential mix is the condition.",
         "Non-professional staff are excluded from the ratio, not counted as a fourth support person."],
        numeric=[{"fact": "maximum support personnel per pharmacist", "value": 4, "unit": "personnel",
                  "conditions": "only when the credential composition conditions in 247 CMR 8.06(3)(a)1 are met"},
                 {"fact": "default maximum support personnel per pharmacist", "value": 3, "unit": "personnel",
                  "conditions": "at least one must be a pharmacy intern or certified pharmacy technician"}],
        related=["MA-PRECEPTOR-INTERN-RATIO", "MA-CERT-TECH-LAPSE"],
    ),
    _rule(
        "MA-CERT-TECH-LAPSE",
        "Consequences when certified pharmacy technician certification lapses",
        "Lapsed technician certification",
        "Under 247 CMR 8.04(3), if a certified pharmacy technician's certification lapses the individual "
        "is limited to the duties and responsibilities of a pharmacy technician under 247 CMR 8.02, must "
        "use the title pharmacy technician, and is counted as a pharmacy technician when calculating the "
        "supervisory ratios in 247 CMR 8.06(3). The underlying Board pharmacy technician license is a "
        "separate credential from the certifying body's certification.",
        "Tests the three simultaneous consequences of a lapsed certification, including the staffing-ratio "
        "consequence that is easy to overlook.",
        "247 CMR 8.04(3)", CMR8, "247 CMR 8.00",
        ["A lapsed certification is not the same as a lapsed Board technician license.",
         "The ratio consequence is often missed: the person still counts, but as a plain technician."],
        related=["MA-SUPPORT-PERSONNEL-RATIO", "MA-CERT-TECH-SCOPE"],
    ),
    _rule(
        "MA-CERT-TECH-SCOPE",
        "Certified pharmacy technician expanded communication and transfer scope",
        "Certified technician scope",
        "Under 247 CMR 8.04(4)(c) a certified pharmacy technician, after identifying him or herself as "
        "such, may request refill authorizations from the prescriber or the prescriber's agent and, with "
        "the approval of the pharmacist on duty, receive new or omitted prescription information, "
        "including communicating information recorded on a patient profile that does not require "
        "professional judgment or interpretation. Under 247 CMR 8.04(4)(d) a certified pharmacy "
        "technician may, with the approval of the pharmacist on duty, perform prescription transfers "
        "between pharmacies for Schedule VI controlled substances only. Under 247 CMR 8.04(4)(e) a "
        "certified pharmacy technician may not administer medications or vaccines, perform drug "
        "utilization review, conduct clinical conflict resolution, contact prescribers about therapy "
        "clarification or modification, provide patient counseling, or perform final dispensing process "
        "validation.",
        "Tests the boundary between a certified technician's expanded clerical communication scope and the "
        "professional judgment functions that remain closed to it.",
        "247 CMR 8.04(4)", CMR8, "247 CMR 8.00",
        ["Receiving new prescription information is clerical relay; contacting a prescriber about therapy is not.",
         "The transfer authority is limited to Schedule VI and still needs the pharmacist's approval."],
        exceptions=["Prescription transfer authority extends only to Schedule VI controlled substances."],
        related=["MA-TECH-REFILL-RELAY", "MA-CERT-TECH-LAPSE"],
    ),
    _rule(
        "MA-TECH-REFILL-RELAY",
        "Pharmacy technician refill authorization and offer-to-counsel relay",
        "Technician communication scope",
        "Under 247 CMR 8.02(6)(c) a pharmacy technician may, with the approval of the pharmacist on duty, "
        "request and accept refill authorizations from a prescriber or the prescriber's agent only if no "
        "information has changed from the previous prescription. Under 247 CMR 8.02(6)(b) a pharmacy "
        "technician may relay the pharmacist's offer to counsel. Under 247 CMR 8.02(6)(d) a pharmacy "
        "technician may not administer medications or vaccines, perform drug utilization review, conduct "
        "clinical conflict resolution, contact prescribers about therapy clarification or modification, "
        "provide patient counseling, or perform final dispensing process validation.",
        "Tests the unchanged-information condition on technician refill authority and the separation "
        "between relaying an offer to counsel and providing counseling.",
        "247 CMR 8.02(6)", CMR8, "247 CMR 8.00",
        ["A changed quantity, strength or directions takes the refill outside technician authority.",
         "Relaying the offer to counsel is not counseling."],
        exceptions=["Refill authority is unavailable when any information has changed from the previous prescription."],
        related=["MA-CERT-TECH-SCOPE"],
    ),
    _rule(
        "MA-TECH-TRAINEE-LIMITS",
        "Pharmacy technician trainee eligibility, telephone bar and employment limit",
        "Technician trainee limits",
        "Under 247 CMR 8.03(2) a pharmacy technician trainee must be at least 16 years of age, a high "
        "school graduate or equivalent or currently enrolled in such a program, of good moral character, "
        "and not convicted of a drug-related felony. Under 247 CMR 8.03(4)(b) and (c) a trainee may be "
        "authorized to perform the duties of a pharmacy technician under the direct supervision of a "
        "pharmacist but may not take prescriptions over the telephone. Under 247 CMR 8.03(5) an "
        "individual may not work as a trainee for more than 1500 hours or more than one year, whichever "
        "is shorter, unless the Board grants an extension, the individual has not yet reached 18 years of "
        "age, or the individual has not yet completed at least 500 hours as a trainee; an individual who "
        "worked beyond those limits before turning 18 shall apply for a pharmacy technician license "
        "within 30 days of the 18th birthday.",
        "Tests the trainee-specific age floor, the telephone-prescription bar, and the whichever-is-shorter "
        "employment limit with its three exceptions.",
        "247 CMR 8.03", CMR8, "247 CMR 8.00",
        ["The trainee age floor is 16, while the pharmacy technician age floor is 18.",
         "The 1500-hour and one-year limits apply as whichever is shorter, not whichever is longer."],
        numeric=[{"fact": "minimum trainee age", "value": 16, "unit": "years", "conditions": "at application"},
                 {"fact": "maximum trainee employment", "value": 1500, "unit": "hours",
                  "conditions": "or one year, whichever is shorter, subject to three stated exceptions"},
                 {"fact": "deadline to apply for a technician license after turning 18", "value": 30,
                  "unit": "days", "conditions": "if the trainee already exceeded the 1500-hour or one-year limit"}],
        exceptions=["Board-granted extension", "individual has not yet reached 18 years of age",
                    "individual has not yet completed 500 hours as a trainee"],
        related=["MA-TECH-LICENSE-ELIGIBILITY"],
    ),
    _rule(
        "MA-TECH-LICENSE-ELIGIBILITY",
        "Pharmacy technician licensure eligibility pathways",
        "Technician licensure eligibility",
        "Under 247 CMR 8.02(3) an applicant for a pharmacy technician license shall be at least 18 years "
        "old, a high school graduate or equivalent or currently enrolled in such a program, of good moral "
        "character, not convicted of a drug-related felony or having admitted to sufficient facts to "
        "warrant such a finding, and shall satisfy one of three alternatives: hold certification from a "
        "Board-approved certifying body; hold a substantially equivalent technician license in good "
        "standing in another state; or achieve a Board-approved passing score on a Board-approved "
        "assessment examination after completing either a Board-approved training program or a minimum of "
        "500 hours of employment as a pharmacy technician trainee attested under the pains and penalties "
        "of perjury and witnessed by the employer.",
        "Tests that the three eligibility routes are alternatives rather than cumulative requirements, and "
        "that the examination route itself has a prerequisite.",
        "247 CMR 8.02(3)", CMR8, "247 CMR 8.00",
        ["The three routes are alternatives; certification is not required if another route is satisfied.",
         "The assessment examination is not a standalone route; it follows training or 500 trainee hours."],
        numeric=[{"fact": "minimum technician age", "value": 18, "unit": "years", "conditions": "at application"},
                 {"fact": "trainee hours supporting the examination route", "value": 500, "unit": "hours",
                  "conditions": "attested under the pains and penalties of perjury and witnessed by the employer"}],
        related=["MA-TECH-TRAINEE-LIMITS", "MA-TECH-LICENSE-RENEWAL"],
    ),
    _rule(
        "MA-TECH-LICENSE-RENEWAL",
        "Pharmacy technician license expiration and lapse consequences",
        "Technician licence renewal",
        "Under 247 CMR 8.07(1) a pharmacy technician license expires every two years on the birthdate of "
        "the licensee. Under 247 CMR 8.07(2) any practice as a pharmacy technician after the expiration "
        "date constitutes unlicensed practice and subjects the individual to the penalties established "
        "for unlicensed practice. Under 247 CMR 8.07(3) a lapsed license may be renewed on filing a "
        "renewal application with the annual license fee, applicable back fees and a late fee, and under "
        "247 CMR 8.07(4) a license lapsed more than two years may require other Board-determined "
        "conditions before renewal.",
        "Tests that the technician renewal cycle keys to the licensee's birthdate rather than a calendar "
        "date, and that lapse converts continued work into unlicensed practice immediately.",
        "247 CMR 8.07", CMR8, "247 CMR 8.00",
        ["Technician expiration keys to the birthdate, unlike the pharmacist December 31 even-year cycle.",
         "Paying back fees later does not retroactively make the interim practice licensed."],
        numeric=[{"fact": "technician licence term", "value": 2, "unit": "years",
                  "conditions": "expiring on the licensee's birthdate"}],
        related=["MA-PHARMACIST-REGISTRATION-RENEWAL", "MA-TECH-LICENSE-ELIGIBILITY"],
    ),
    _rule(
        "MA-CII-SUPPORT-HANDLING",
        "Support personnel handling of Schedule II and hydrocodone-only extended release",
        "Schedule II support handling",
        "Under 247 CMR 8.05(1) accountability for and security of Schedule II controlled substances is "
        "the direct responsibility of the pharmacist. Under 247 CMR 8.05(2), and only under a "
        "pharmacist's supervision, a pharmacy technician may assist in transporting Schedule II "
        "controlled substances and a certified pharmacy technician may assist in transporting and "
        "handling them, provided the pharmacist has approved the individual and the approval is evidenced "
        "by written pharmacy policies and procedures available to the Board on request. Under 247 CMR "
        "8.05(3) no certified pharmacy technician, pharmacy technician or pharmacy technician trainee may "
        "handle any hydrocodone-only extended release medication that is not in an abuse-deterrent form, "
        "while pharmacy interns under the direct supervision of a registered pharmacist may.",
        "Tests the transport-versus-handle distinction between technician grades and the separate "
        "hydrocodone-only extended release carve-out that reaches every technician grade.",
        "247 CMR 8.05", CMR8, "247 CMR 8.00",
        ["A plain technician may assist in transporting but not in handling Schedule II drugs.",
         "The hydrocodone-only extended release bar is not lifted by certification; interns are treated differently."],
        exceptions=["Pharmacy interns under direct pharmacist supervision may handle non-abuse-deterrent "
                    "hydrocodone-only extended release medication."],
        related=["MA-TECH-CII"],
    ),
    _rule(
        "MA-INTERN-WITHDRAWAL-NOTICE",
        "Pharmacy intern notification of withdrawal from a pharmacy program",
        "Intern withdrawal notification",
        "Under 247 CMR 8.01(18) a pharmacy intern shall provide written notification to the Board within "
        "14 days of his or her withdrawal from an approved college or school of pharmacy or PharmD "
        "program. Under 247 CMR 8.01(10) an intern who has graduated from an approved college or school "
        "of pharmacy may continue to act as a pharmacy intern until becoming licensed as a pharmacist.",
        "Tests an affirmative reporting duty that sits on the intern personally, and separates withdrawal "
        "from graduation, which does not end intern capacity.",
        "247 CMR 8.01(10) and (18)", CMR8, "247 CMR 8.00",
        ["Graduation does not end intern status; withdrawal triggers a reporting duty.",
         "The duty runs to the Board and is the intern's own, not only the employer's."],
        numeric=[{"fact": "intern withdrawal notification deadline", "value": 14, "unit": "days",
                  "conditions": "from withdrawal from the approved college/school or PharmD program"}],
        related=["MA-INTERN-SUPERVISION"],
    ),
    _rule(
        "MA-PHARMD-RESIDENCY-CREDENTIAL",
        "Credential required for a PharmD graduate in a Massachusetts residency",
        "Residency credential",
        "Under 247 CMR 8.01(8) a PharmD graduate from an approved college or school of pharmacy who has "
        "accepted a residency in Massachusetts shall apply for and obtain a pharmacy intern license until "
        "obtaining a Massachusetts pharmacist license; a PharmD graduate enrolled in a Massachusetts "
        "residency shall either hold a Massachusetts pharmacist license or hold a Massachusetts pharmacy "
        "intern license and be supervised by a pharmacist.",
        "Tests that a residency position is not itself a practice credential and that the graduate must "
        "hold one of two specific Massachusetts credentials.",
        "247 CMR 8.01(8)", CMR8, "247 CMR 8.00",
        ["A residency appointment is not a licence; the graduate still needs an intern or pharmacist licence.",
         "Holding a PharmD degree alone does not authorize unsupervised practice."],
        related=["MA-INTERN-SUPERVISION", "MA-INTERN-WITHDRAWAL-NOTICE"],
    ),
    _rule(
        "MA-FOREIGN-GRADUATE-INTERNSHIP",
        "Authorization required before a foreign graduate begins a Massachusetts internship",
        "Foreign graduate internship entry",
        "Under 247 CMR 8.01(7), before commencing a pharmacy internship in Massachusetts a graduate of a "
        "non-approved college or school of pharmacy must hold NABP authorization to sit for the FPGEE "
        "issued within the preceding year and must provide a copy of that authorization to the Board "
        "along with any other documentation the Board requires.",
        "Tests the pre-internship gate and its currency window for foreign graduates, which is distinct "
        "from the FPGEC certification required later for examination.",
        "247 CMR 8.01(7)", CMR8, "247 CMR 8.00",
        ["FPGEE authorization to begin an internship is not the same as FPGEC certification for examination.",
         "The authorization must have been issued within the preceding year."],
        numeric=[{"fact": "FPGEE authorization currency window", "value": 1, "unit": "year",
                  "conditions": "issued within the preceding year before starting the internship"}],
        related=["MA-PHARMACIST-EXAM-ELIGIBILITY"],
    ),
    _rule(
        "MA-INTERN-HOUR-COMPOSITION",
        "Composition of the Board-approved pharmacy internship requirement",
        "Internship hour composition",
        "Under 247 CMR 8.01(1) a candidate for pharmacist licensure shall have completed a Board-approved "
        "pharmacy internship consisting of at least 1500 hours of Board-approved internship experience, "
        "of which at least 1000 hours is acquired in a Board-approved pharmacy or pharmacy-related "
        "setting and at least 500 hours in any one or combination of Board-approved internships in "
        "clinical pharmacy, a demonstration project, manufacturing, or analytical or industrial pharmacy; "
        "alternatively the requirement is met by at least 1500 intern hours acquired through experiential "
        "pharmacy education where the student is a graduate of an ACPE-accredited college or university. "
        "Under 247 CMR 8.01(11) the Board may grant credit for out-of-state internship experience on an "
        "affidavit or certificate of approval from the jurisdiction where it was acquired.",
        "Tests the internal composition of the 1500 hours and the existence of an alternative experiential "
        "pathway, rather than the headline hour total alone.",
        "247 CMR 8.01(1) and (11)", CMR8, "247 CMR 8.00",
        ["The 1500 hours is not undifferentiated; 1000 and 500 hour components apply on the first pathway.",
         "Out-of-state experience is creditable on documentation, not automatically excluded."],
        numeric=[{"fact": "total Board-approved internship hours", "value": 1500, "unit": "hours", "conditions": ""},
                 {"fact": "hours in a pharmacy or pharmacy-related setting", "value": 1000, "unit": "hours",
                  "conditions": "component of the first pathway"},
                 {"fact": "hours in clinical, demonstration, manufacturing or analytical settings", "value": 500,
                  "unit": "hours", "conditions": "component of the first pathway"}],
        related=["MA-INTERN-12H", "MA-PHARMACIST-EXAM-ELIGIBILITY"],
    ),
    _rule(
        "MA-SUPPORT-NAME-TAGS",
        "Required name tags and titles for pharmacy support personnel",
        "Support personnel identification",
        "Under 247 CMR 8.01(14) a pharmacy intern shall wear a name tag indicating the intern's name and "
        "the words pharmacy intern. Under 247 CMR 8.02(6)(a) a pharmacy technician shall wear a name tag "
        "with the individual's first name and the title Pharmacy Technician. Under 247 CMR 8.03(4)(a) a "
        "pharmacy technician trainee shall wear a name tag with the individual's first name and the title "
        "Pharmacy Technician Trainee. Under 247 CMR 8.04(4)(a) a certified pharmacy technician shall wear "
        "a name tag with the individual's first name and the title Certified Pharmacy Technician.",
        "Tests that the displayed title must match the actual credential held, which interacts with the "
        "consequences of a lapsed certification.",
        "247 CMR 8.01(14), 8.02(6)(a), 8.03(4)(a) and 8.04(4)(a)", CMR8, "247 CMR 8.00",
        ["The title on the tag must track the credential actually held, not the role assigned.",
         "A lapsed certification requires reverting to the pharmacy technician title."],
        related=["MA-CERT-TECH-LAPSE"],
    ),
    _rule(
        "MA-SUPPORT-DOCUMENTATION-DUTY",
        "Manager of Record documentation duties for support personnel",
        "Support personnel documentation",
        "Under 247 CMR 8.06(1) a pharmacist Manager of Record, or the Director of Pharmacy in an "
        "institutional pharmacy, that uses certified pharmacy technicians, pharmacy technicians or "
        "pharmacy technician trainees shall make available to the Board on request a list of currently "
        "employed such personnel, a written description of the duties delegated to them, and a written "
        "description of their scopes of responsibility. Under 247 CMR 8.06(2) on-the-job training programs "
        "shall comply with written pharmacy guidelines consistent with professional, ethical and legal "
        "standards, and copies shall be provided to the Board on request.",
        "Tests a documentation duty that attaches to the Manager of Record rather than to the individual "
        "technician, and is produced on Board request rather than filed in advance.",
        "247 CMR 8.06(1) and (2)", CMR8, "247 CMR 8.00",
        ["These documents are produced on request; they are not a pre-filed Board submission.",
         "The duty sits with the Manager of Record or Director of Pharmacy, not the technician."],
        topic="Pharmacy management",
        related=["MA-SUPPORT-PERSONNEL-RATIO"],
    ),
    # ---------------- 247 CMR 3.00 — pharmacist licensure ----------------
    _rule(
        "MA-PHARMACIST-EXAM-ELIGIBILITY",
        "Eligibility for pharmacist licensure by examination",
        "Examination eligibility",
        "Under 247 CMR 3.01(1) a graduate of an ACPE-accredited or Board-approved college or school of "
        "pharmacy is eligible for examination if the applicant is 18 years of age or older by the "
        "scheduled examination date, holds a doctor of pharmacy degree from such a school, has completed "
        "a pharmacy internship in accordance with 247 CMR 8.01(1), and is of good moral character. Under "
        "247 CMR 3.01(2) a graduate of a non-approved college or school of pharmacy is eligible if the "
        "applicant is 18 or older by that date, has received official FPGEC certification from NABP, has "
        "submitted an official copy of the FPGEC certificate with official NABP notification to the "
        "Board, has completed an internship in accordance with 247 CMR 8.01(1), and is of good moral "
        "character.",
        "Tests that the internship requirement applies on both pathways and that FPGEC certification is "
        "the foreign-graduate substitute for the accredited degree, not for the internship.",
        "247 CMR 3.01(1) and (2)", CMR3, "247 CMR 3.00",
        ["FPGEC certification replaces the accredited degree, not the internship requirement.",
         "The age requirement is measured by the scheduled examination date."],
        topic="Licensure",
        related=["MA-INTERN-HOUR-COMPOSITION", "MA-PHARMACIST-EXAM-SCORING"],
    ),
    _rule(
        "MA-PHARMACIST-EXAM-SCORING",
        "NAPLEX and MPJE scoring and re-examination timing",
        "Examination scoring and retake",
        "Under 247 CMR 3.01(4) and (5) an applicant for pharmacist licensure must pass both NAPLEX and "
        "MPJE, achieving a score of not less than 75% on each. Under 247 CMR 3.01(6) an applicant who "
        "fails either or both may be re-examined on submitting a new application with all required fees. "
        "Under 247 CMR 3.01(7) an applicant who fails either examination must reapply to sit for the "
        "failed examination within one year of the administration date of the original examination for "
        "both scores to be considered together; if the applicant does not pass both within that one-year "
        "period the applicant must apply to retake both NAPLEX and MPJE.",
        "Tests the one-year linkage window between the two examinations, which is the operative deadline "
        "rather than a limit on attempts.",
        "247 CMR 3.01(4) through (7)", CMR3, "247 CMR 3.00",
        ["The one-year window governs whether both scores count together, not how many retakes are allowed.",
         "Missing the window forces a retake of the already-passed examination as well."],
        numeric=[{"fact": "minimum passing score", "value": 75, "unit": "percent",
                  "conditions": "on each of NAPLEX and MPJE"},
                 {"fact": "window to reapply for a failed examination", "value": 1, "unit": "year",
                  "conditions": "from the administration date of the original examination, for both scores to count together"}],
        topic="Licensure",
        related=["MA-PHARMACIST-EXAM-ELIGIBILITY"],
    ),
    _rule(
        "MA-LICENSURE-RECIPROCITY",
        "Pharmacist licensure by reciprocity",
        "Licensure by reciprocity",
        "Under 247 CMR 3.02 the Board may grant licensure by reciprocity to an applicant who proves "
        "licensure by examination in another state or jurisdiction and good standing in all states where "
        "the applicant holds a license, provided that jurisdiction requires a degree of competency equal "
        "to that required in Massachusetts and the Board recognizes it for reciprocity. The applicant "
        "submits a preliminary application to NABP, which as agent of the Board conducts the preliminary "
        "evaluation, but under 247 CMR 3.02(1)(b) the Board makes the final determination of eligibility "
        "and under 247 CMR 3.02(1)(a) an applicant notified by NABP that they do not qualify may request "
        "in writing that the Board review the basis of that decision. Under 247 CMR 3.02(1)(c) a "
        "reciprocity application is valid for one year after NABP approval, and under 247 CMR 3.02(2)(a) "
        "and (3)(a) the requirements include documented internship experience, a passing MPJE score of at "
        "least 75%, and personal appearance before the Board if requested.",
        "Tests that NABP performs only the preliminary evaluation while the Board retains the final "
        "determination, and that MPJE is still required on the reciprocity pathway.",
        "247 CMR 3.02", CMR3, "247 CMR 3.00",
        ["NABP's preliminary decision is reviewable by the Board; it is not final.",
         "Reciprocity does not waive MPJE or the internship documentation."],
        numeric=[{"fact": "validity of an approved reciprocity application", "value": 1, "unit": "year",
                  "conditions": "after the date of NABP approval"}],
        topic="Licensure",
        related=["MA-PHARMACIST-EXAM-SCORING"],
    ),
    _rule(
        "MA-LICENSURE-RETIREMENT",
        "Retired licensure status and its limits",
        "Retired licence status",
        "Under 247 CMR 3.04(1) a licensee may petition the Board to place a license on retired status, "
        "which is a nondisciplinary status, and the Board may decline to review any petition for "
        "reinstatement or return to current status from a licensee whose status was changed to retired. "
        "Under 247 CMR 3.04(2) eligibility requires that the license is not surrendered, suspended or "
        "revoked at the time of the petition and that the licensee demonstrates an intent to retire "
        "permanently from active practice in the Commonwealth and in all other jurisdictions. Under 247 "
        "CMR 3.04(3) a licensee with retired status may not practice, and under 247 CMR 3.04(4) retired "
        "status does not prevent the Board from initiating or pursuing disciplinary action.",
        "Tests that retired status is voluntary and nondisciplinary yet neither permits practice nor "
        "shields the licensee from Board action.",
        "247 CMR 3.04", CMR3, "247 CMR 3.00",
        ["Retired status is nondisciplinary but is not a safe harbour from discipline.",
         "The intent to retire must extend to all jurisdictions, not only Massachusetts."],
        topic="Licensure",
        related=["MA-PHARMACIST-REGISTRATION-RENEWAL"],
    ),
    _rule(
        "MA-PROTECTED-HEALTH-CARE-LICENSURE",
        "Legally protected health care activity and licensure decisions",
        "Protected health care activity",
        "Under 247 CMR 3.05 no person shall be denied initial licensure or renewal due to any complaint, "
        "criminal charge, conviction, judgment, discipline or other sanction arising from providing or "
        "assisting in providing, or dispensing medication for, reproductive health care services or "
        "gender-affirming health care services as defined at M.G.L. c. 12, § 11I½, so long as the "
        "services would have been lawful in Massachusetts and are consistent with standards for good "
        "professional practice in Massachusetts. Parallel protections apply to pharmacy support personnel "
        "under 247 CMR 8.08 and to pharmacies under 247 CMR 6.18.",
        "Tests that an out-of-state sanction for protected health care activity cannot be imported as a "
        "Massachusetts licensure bar, subject to the lawful-in-Massachusetts qualifier.",
        "247 CMR 3.05, 8.08", CMR3, "247 CMR 3.00",
        ["The protection is not unconditional: the services must have been lawful in Massachusetts.",
         "The protection covers renewal as well as initial licensure."],
        topic="Licensure",
        related=["MA-LICENSURE-RECIPROCITY"],
    ),
    # ---------------- 247 CMR 4.00 — renewal and continuing education ----------------
    _rule(
        "MA-PHARMACIST-REGISTRATION-RENEWAL",
        "Pharmacist personal registration expiration, lapse and reinstatement",
        "Personal registration renewal",
        "Under 247 CMR 4.02(1) all personal registrations expire on December 31st of each even-numbered "
        "year and shall be renewed before January 1st of the following year to continue practice. Under "
        "247 CMR 4.02(3) any practice of pharmacy after expiration constitutes unlicensed practice. Under "
        "247 CMR 4.02(4) an applicant who failed to renew for more than 60 days, whose registration was "
        "not suspended or revoked, may renew on satisfying Board-imposed conditions, which may include "
        "additional continuing education contact hours. Under 247 CMR 4.02(5) an applicant who failed to "
        "renew for more than two years, whose registration was not suspended or revoked, shall take and "
        "pass the MPJE and meet all other Board conditions.",
        "Tests the escalating consequences of lapse length, including the point at which MPJE becomes a "
        "precondition to renewal.",
        "247 CMR 4.02(1) through (5)", CMR4, "247 CMR 4.00",
        ["The pharmacist cycle keys to December 31 of an even-numbered year, unlike the technician birthdate cycle.",
         "The 60-day and two-year thresholds carry different consequences."],
        numeric=[{"fact": "personal registration expiry", "value": "December 31 of each even-numbered year",
                  "unit": "date", "conditions": "renew before January 1 of the following year"},
                 {"fact": "lapse threshold for Board-imposed conditions", "value": 60, "unit": "days", "conditions": ""},
                 {"fact": "lapse threshold requiring MPJE", "value": 2, "unit": "years", "conditions": ""}],
        topic="Licensure",
        related=["MA-REGISTRATION-DISCIPLINE-REINSTATEMENT", "MA-TECH-LICENSE-RENEWAL"],
    ),
    _rule(
        "MA-REGISTRATION-DISCIPLINE-REINSTATEMENT",
        "Reinstatement conditions after suspension or revocation",
        "Reinstatement after discipline",
        "Under 247 CMR 4.02(6) an applicant for personal registration renewal whose registration has been "
        "revoked, or suspended for between six months and two years, shall take and pass the MPJE and "
        "meet all conditions determined by the Board. Under 247 CMR 4.02(7) an applicant whose "
        "registration has been revoked or suspended for more than two years shall take and pass the MPJE "
        "and meet all other Board conditions, which may include taking and passing the NAPLEX.",
        "Tests the two-tier reinstatement ladder after discipline, where NAPLEX becomes available to the "
        "Board only beyond the two-year threshold.",
        "247 CMR 4.02(6) and (7)", CMR4, "247 CMR 4.00",
        ["A disciplinary lapse follows a different ladder from a simple failure to renew.",
         "NAPLEX is a possible additional condition only in the longer tier."],
        numeric=[{"fact": "suspension band requiring MPJE", "value": "six months to two years", "unit": "period",
                  "conditions": ""},
                 {"fact": "threshold at which NAPLEX may also be required", "value": 2, "unit": "years",
                  "conditions": "revoked or suspended for more than two years"}],
        topic="Licensure",
        related=["MA-PHARMACIST-REGISTRATION-RENEWAL"],
    ),
    _rule(
        "MA-CE-ANNUAL-STRUCTURE",
        "Annual structure of the pharmacist continuing education requirement",
        "Continuing education structure",
        "Under 247 CMR 4.03(3) and (4) a registrant seeking renewal must complete a minimum of 40 contact "
        "hours across the two-year cycle and a minimum of 20 contact hours in each calendar year of that "
        "cycle. Under 247 CMR 4.03(4)(a) at least two contact hours per calendar year must be in pharmacy "
        "law. Under 247 CMR 4.03(4)(b) no more than 15 contact hours per calendar year acquired through "
        "home study or other mediated instruction may be applied toward the 20-hour annual minimum. Under "
        "247 CMR 4.03(5) contact hours may not be carried over from one calendar year to another, and "
        "under 247 CMR 4.03(7) a registrant may not earn more than eight contact hours in a calendar day.",
        "Tests the per-calendar-year structure, the home-study cap and the no-carry-over rule, which "
        "together defeat a single end-of-cycle catch-up.",
        "247 CMR 4.03(3) through (7)", CMR4, "247 CMR 4.00",
        ["The 40-hour total cannot be earned in one year because of the 20-hour annual minimum and no carry-over.",
         "The 15-hour home-study cap is per calendar year, not per cycle."],
        numeric=[{"fact": "contact hours per two-year cycle", "value": 40, "unit": "contact hours", "conditions": ""},
                 {"fact": "contact hours per calendar year", "value": 20, "unit": "contact hours", "conditions": ""},
                 {"fact": "pharmacy law contact hours per calendar year", "value": 2, "unit": "contact hours",
                  "conditions": ""},
                 {"fact": "home study cap per calendar year", "value": 15, "unit": "contact hours", "conditions": ""},
                 {"fact": "maximum contact hours in a calendar day", "value": 8, "unit": "contact hours",
                  "conditions": ""}],
        topic="Licensure",
        related=["MA-CE-PRACTICE-SPECIFIC", "MA-CE-EXEMPTIONS"],
    ),
    _rule(
        "MA-CE-PRACTICE-SPECIFIC",
        "Practice-specific continuing education overlays",
        "Practice-specific continuing education",
        "Under 247 CMR 4.03(4)(c) a registrant who oversees or is directly engaged in sterile compounding, "
        "or who practices in a pharmacy licensed under M.G.L. c. 112, § 39G or 39I, must complete at "
        "least five contact hours per calendar year in sterile compounding. Under 247 CMR 4.03(4)(d) a "
        "registrant who oversees or is directly engaged in complex non-sterile compounding, or who "
        "practices in a pharmacy licensed under M.G.L. c. 112, § 39H, must complete at least three "
        "contact hours per calendar year in complex non-sterile compounding. Under 247 CMR 4.03(4)(e) a "
        "registrant who oversees or is engaged in administering vaccines must complete at least one "
        "contact hour on immunizations during the two-year renewal cycle.",
        "Tests overlays that attach to the practice setting or activity and differ in whether they are "
        "measured per calendar year or per cycle.",
        "247 CMR 4.03(4)(c) through (e)", CMR4, "247 CMR 4.00",
        ["The compounding overlays are per calendar year while the immunization overlay is per cycle.",
         "The overlays attach to the licensed setting as well as to personal engagement in the activity."],
        numeric=[{"fact": "sterile compounding contact hours", "value": 5, "unit": "contact hours",
                  "conditions": "per calendar year"},
                 {"fact": "complex non-sterile compounding contact hours", "value": 3, "unit": "contact hours",
                  "conditions": "per calendar year"},
                 {"fact": "immunization contact hours", "value": 1, "unit": "contact hour",
                  "conditions": "during the two-year renewal cycle"}],
        topic="Licensure",
        related=["MA-CE-ANNUAL-STRUCTURE"],
    ),
    _rule(
        "MA-CE-EXEMPTIONS",
        "Continuing education relief for new graduates, extenuating circumstances and active duty",
        "Continuing education relief",
        "Under 247 CMR 4.03(8) a registrant is not required to complete continuing education in the "
        "calendar year in which the registrant graduated from an approved college or school of pharmacy. "
        "Under 247 CMR 4.03(6) a registrant who failed to complete the required contact hours, or who "
        "cannot meet the home-study limit because of a physical disability, shall submit a detailed "
        "statement signed under the penalties of perjury setting out the extenuating circumstances, and "
        "the Board determines whether renewal is granted. Under 247 CMR 4.02(8) and M.G.L. c. 112, "
        "§ 1B(c) the registration of a registrant in active armed forces service remains valid until 90 "
        "days after release from active duty, and the continuing education requirement does not apply to "
        "the biennial cycle immediately preceding December 31st of an even-numbered year if the "
        "registrant is in active service after October 1st of that year.",
        "Tests that continuing education relief is granted by defined mechanisms rather than by informal "
        "hardship, and that the military provision is conditioned on a date.",
        "247 CMR 4.02(8), 4.03(6) and 4.03(8)", CMR4, "247 CMR 4.00",
        ["Extenuating circumstances require a sworn statement and a Board determination, not self-certification.",
         "The military continuing education relief turns on active service after October 1st of the even-numbered year."],
        numeric=[{"fact": "registration validity after release from active duty", "value": 90, "unit": "days",
                  "conditions": "following release from active duty"}],
        topic="Licensure",
        related=["MA-CE-ANNUAL-STRUCTURE", "MA-CE-RECORDKEEPING"],
    ),
    _rule(
        "MA-CE-RECORDKEEPING",
        "Pharmacist continuing education recordkeeping and audit response",
        "Continuing education records",
        "Under 247 CMR 4.06(1) a pharmacist shall maintain documentation or a statement of credit "
        "demonstrating successful completion of the required contact hours for at least two years from "
        "the date of completion, and that documentation must contain the name of the authorized provider, "
        "the participant's name, the title and number of the program, the date of completion and the "
        "number of contact hours earned. Under 247 CMR 4.06(2) a pharmacist shall provide that "
        "documentation to the Board on request and in response to random audits.",
        "Tests the content requirements of continuing education documentation and the two-year retention "
        "period measured from completion rather than from renewal.",
        "247 CMR 4.06", CMR4, "247 CMR 4.00",
        ["Retention runs from the date of completion, not from the renewal date.",
         "A bare attendance list is insufficient; five specific data elements are required."],
        numeric=[{"fact": "continuing education record retention", "value": 2, "unit": "years",
                  "conditions": "from the date of completion"}],
        topic="Licensure",
        related=["MA-CE-ANNUAL-STRUCTURE", "MA-CE-PROVIDER-APPROVAL"],
    ),
    _rule(
        "MA-CE-PROVIDER-APPROVAL",
        "Board approval of continuing pharmacy education providers and credit for teaching",
        "Continuing education provider approval",
        "Under 247 CMR 4.04(2) each request for provider authorization or program approval shall be "
        "submitted to the Board no less than 30 days before the proposed program's presentation, and "
        "under 247 CMR 4.04(4) a denial by the Executive Director or designee may be appealed to the full "
        "Board by written petition submitted within 30 days of the notice of denial. Under 247 CMR "
        "4.04(5) a person or agency documenting current program approval from and good standing with "
        "either ACPE or AMA CME Category 1 is considered an authorized provider. Under 247 CMR 4.07 a "
        "registered pharmacist who is a Board-approved continuing education instructor receives credit "
        "for the program taught on a one-time basis annually.",
        "Tests the two distinct 30-day clocks in the provider process and the once-a-year limit on credit "
        "for repeatedly teaching the same program.",
        "247 CMR 4.04 and 4.07", CMR4, "247 CMR 4.00",
        ["The 30-day submission clock and the 30-day appeal clock are separate deadlines.",
         "Teaching the same program repeatedly yields credit only once annually."],
        numeric=[{"fact": "advance submission before a program", "value": 30, "unit": "days", "conditions": ""},
                 {"fact": "appeal window after a denial", "value": 30, "unit": "days", "conditions": ""}],
        topic="Licensure",
        related=["MA-CE-ANNUAL-STRUCTURE", "MA-CE-RECORDKEEPING"],
    ),
]

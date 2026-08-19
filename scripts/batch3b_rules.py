"""Canonical rule records required by Batch 3 tranche B3-B.

Every rule was read verbatim from the current official Board of Registration in Pharmacy
publication on 2026-08-19: 247 CMR 3.00, 4.00 and 8.00 (revised 4/25/25, effective
1/9/25), 247 CMR 9.00 (12/6/24), 247 CMR 10.00 (revised 4/25/25, effective 1/9/25) and
247 CMR 16.00. Nothing here is authored from a section heading alone.

Area assignment follows the bank's existing taxonomy: personnel licensure and personnel
discipline are Area 1, and pharmacist practice duties are Area 2.
"""

from __future__ import annotations

CMR3 = "https://www.mass.gov/regulations/247-CMR-300-pharmacist-licensure-requirements"
CMR4 = "https://www.mass.gov/regulations/247-CMR-400-personal-registration-renewal-continuing-education-requirement"
CMR8 = "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians"
CMR9 = "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"
CMR10 = "https://www.mass.gov/regulations/247-CMR-1000-disciplinary-proceedings"
CMR16 = "https://www.mass.gov/regulations/247-CMR-1600-collaborative-drug-therapy-management"

VERIFIED = "2026-08-19"
NOTE = (
    "Read verbatim in the current official Board of Registration in Pharmacy publication of {part} "
    "on 2026-08-19 during Batch 3 tranche B3-B authoring under Issue #91. A fresh independent legal "
    "and full-bank realism audit is still required before release."
)


def _rule(rule_id, area, topic, subtopic, title, summary, relevance, section, url, part,
          confusions, numeric=(), exceptions=(), related=()):
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
        "verification_notes": NOTE.format(part=part),
    }


RULES = [
    # ---------------- Area 1 — 247 CMR 10.00 personnel discipline ----------------
    _rule(
        "MA-DISCIPLINE-CONVICTION-DEFINITION", 1, "Licensure and discipline", "Conviction definition",
        "Meaning of conviction in Board disciplinary proceedings",
        "Under 247 CMR 10.02 conviction includes any guilty verdict or finding of guilt and any admission "
        "to or finding of sufficient facts to warrant a finding of guilt, regardless of adjudication, a "
        "continuance without a finding, and any plea of guilty or nolo contendere, of or to a crime in any "
        "jurisdiction, which has been accepted by the court, whether or not a sentence has been imposed. A "
        "conviction of any person licensed or registered by the Board is conclusive evidence of the "
        "commission of that crime in any disciplinary proceeding based upon the conviction.",
        "Tests that dispositions a licensee may think are not convictions still count, and that the "
        "conviction cannot be relitigated before the Board.",
        "247 CMR 10.02", CMR10, "247 CMR 10.00",
        ["A continuance without a finding is a conviction for Board purposes.",
         "Because a conviction is conclusive evidence, the underlying facts cannot be re-argued to the Board."],
        related=["MA-DISCIPLINE-REPORTING-CLOCKS"],
    ),
    _rule(
        "MA-DISCIPLINE-REPORTING-CLOCKS", 1, "Licensure and discipline", "Disciplinary reporting deadlines",
        "Licensee duties to report discipline and criminal charges",
        "Under 247 CMR 10.03(1)(y) and (z) it is a ground for discipline to fail to report, or to fail to "
        "report accurately, to the Board within seven business days any discipline on the basis of actions "
        "listed in 247 CMR 10.03(1), and any final action, including licence surrender or resignation, "
        "regarding a registrant or licensee by any other governmental authority in this state or another "
        "jurisdiction, including action against any other health care related registration or licence the "
        "person holds. Under 247 CMR 10.03(1)(aa) it is a separate ground to fail to report to the Board in "
        "writing within 30 days any pending criminal charge or conviction, in Massachusetts or any other "
        "jurisdiction.",
        "Tests two different reporting clocks running from two different triggers, one measured in business "
        "days and the other in calendar days.",
        "247 CMR 10.03(1)(y), (z) and (aa)", CMR10, "247 CMR 10.00",
        ["Discipline is reported within seven business days; a pending criminal charge within 30 days.",
         "The charge reporting duty attaches when the charge is pending, not only on conviction."],
        numeric=[{"fact": "reporting deadline for discipline or final action", "value": 7, "unit": "business days",
                  "conditions": ""},
                 {"fact": "reporting deadline for a pending criminal charge or conviction", "value": 30,
                  "unit": "days", "conditions": "in writing"}],
        related=["MA-DISCIPLINE-CONVICTION-DEFINITION", "MA-DISCIPLINE-COOPERATION"],
    ),
    _rule(
        "MA-DISCIPLINE-COOPERATION", 1, "Licensure and discipline", "Duty to cooperate with the Board",
        "Failure to cooperate with the Board as an independent ground",
        "Under 247 CMR 10.03(1)(q) it is an independent ground for discipline to fail, without cause, to "
        "cooperate with any request by the Board to appear before it or to provide requested information, "
        "to fail to respond to a Board subpoena, or to fail to furnish the Board, its investigators or "
        "representatives with records, documents, information or testimony to which the Board is legally "
        "entitled.",
        "Tests that non-cooperation is itself sanctionable regardless of the merits of the underlying "
        "complaint.",
        "247 CMR 10.03(1)(q)", CMR10, "247 CMR 10.00",
        ["Non-cooperation is a standalone ground even if the original complaint is dismissed.",
         "The duty covers appearance, information, subpoenas, records and testimony."],
        related=["MA-DISCIPLINE-REPORTING-CLOCKS"],
    ),
    _rule(
        "MA-DISCIPLINE-ACTION-TYPES", 1, "Licensure and discipline", "Disciplinary action types",
        "Reprimand, censure and probation as formal disciplinary action",
        "Under 247 CMR 10.06 the actions available to the Board include dismissal of the complaint; an "
        "advisory letter, which is an official written document retained in the Board's files delineating "
        "the Board's concerns and which does not constitute formal disciplinary action; reprimand or "
        "censure, where a reprimand constitutes formal disciplinary action and a censure is a severe "
        "reprimand; probation, which constitutes disciplinary action and consists of a period during which "
        "the registrant may practise under conditions imposed by the Board pursuant to a formal "
        "adjudicatory hearing or consent agreement; and suspension or revocation.",
        "Tests the ladder of Board actions and which rungs are formal discipline, in particular that "
        "probation permits continued practice under conditions.",
        "247 CMR 10.06(1) through (5)", CMR10, "247 CMR 10.00",
        ["A censure is a severe reprimand, not a separate lesser category.",
         "Probation permits practice under conditions; it is not a suspension."],
        related=["MA-DISCIPLINE-CONSENT-SURRENDER", "MA-DISCIPLINARY-PROCESS"],
    ),
    _rule(
        "MA-DISCIPLINE-CONSENT-SURRENDER", 1, "Licensure and discipline", "Consent agreement and surrender",
        "Consent agreements and voluntary surrender terms",
        "Under 247 CMR 10.06(6) a consent agreement is a resolution of a complaint agreed upon by the Board "
        "and the registrant which may contain conditions on professional conduct and practice and may "
        "include voluntary suspension or surrender, permanently or for a fixed period. A voluntary "
        "surrender agreement shall be in writing and signed by the registrant and the Board; shall recite "
        "the facts on which it is based and include provisions addressing reinstatement and any conditions "
        "the Board elects to impose; shall state that the registrant realises the surrender deprives him or "
        "her of all privileges of registration and is not subject to judicial review; and shall be placed "
        "in the registrant's Board file as part of the permanent Board records.",
        "Tests that voluntary surrender is a negotiated disciplinary resolution with an express waiver of "
        "judicial review, not an informal exit.",
        "247 CMR 10.06(6)", CMR10, "247 CMR 10.00",
        ["Voluntary surrender is expressly not subject to judicial review.",
         "The agreement must recite the underlying facts and address reinstatement."],
        related=["MA-DISCIPLINE-ACTION-TYPES"],
    ),
    _rule(
        "MA-DISCIPLINE-OUT-OF-STATE", 1, "Licensure and discipline", "Out-of-state discipline",
        "Out-of-state discipline as a basis for Massachusetts action",
        "Under 247 CMR 10.06(7) disciplinary action taken against a Massachusetts registrant or licensee by "
        "another state or jurisdiction in which that person is also registered may be the basis for the "
        "Board initiating disciplinary action, provided that the conduct disciplined in the other "
        "jurisdiction constitutes a violation of Massachusetts law. Under 247 CMR 10.03(1)(t) having been "
        "disciplined in another jurisdiction for reasons substantially the same as those in 247 CMR 10.03 "
        "is itself a ground for discipline.",
        "Tests the conduct-equivalence condition that keeps out-of-state discipline from importing "
        "automatically.",
        "247 CMR 10.03(1)(t) and 10.06(7)", CMR10, "247 CMR 10.00",
        ["Out-of-state discipline is not automatically actionable; the conduct must violate Massachusetts law.",
         "This is separate from the protected health care activity carve-out."],
        related=["MA-DISCIPLINE-PROTECTED-ACTIVITY", "MA-DISCIPLINE-CONVICTION-DEFINITION"],
    ),
    _rule(
        "MA-DISCIPLINE-PROTECTED-ACTIVITY", 1, "Licensure and discipline", "Protected activity discipline bar",
        "Discipline bar for protected reproductive and gender-affirming health care",
        "Under 247 CMR 10.03(3), notwithstanding the grounds for discipline in 247 CMR 10.03, no licensee "
        "shall be subject to discipline for providing or assisting in providing, or dispensing medication "
        "for, reproductive health care services or gender-affirming health care services as defined at "
        "M.G.L. c. 12, § 11I½, or for any conviction, judgment, discipline or other sanction arising from "
        "such health care services, so long as the services provided would have been lawful in "
        "Massachusetts and are consistent with standards for good professional practice in Massachusetts.",
        "Tests that the carve-out overrides the general grounds, including the out-of-state discipline "
        "ground, subject to its two qualifiers.",
        "247 CMR 10.03(3)", CMR10, "247 CMR 10.00",
        ["The carve-out overrides the out-of-state discipline ground rather than sitting alongside it.",
         "It is conditional on the services being lawful in Massachusetts and consistent with good practice."],
        related=["MA-DISCIPLINE-OUT-OF-STATE", "MA-PROTECTED-HEALTH-CARE-LICENSURE"],
    ),
    _rule(
        "MA-DISCIPLINE-SUMMARY-CLOCKS", 1, "Licensure and discipline", "Pre-hearing summary action",
        "Suspension prior to hearing and summary cease and desist timing",
        "Under 247 CMR 10.07, if based on affidavits or other documentary evidence the Board determines a "
        "licensee is an immediate or serious threat to the public health, safety or welfare, the Board may "
        "suspend or refuse to renew a licence pending a final hearing, and a hearing limited to the "
        "necessity of the summary action shall be afforded within seven days of the Board's action. Under "
        "247 CMR 10.08(1) the Board or Board President may instead issue a non-disciplinary Cease and "
        "Desist Notice or Quarantine Notice, and under 247 CMR 10.08(3) a hearing limited to the necessity "
        "of such a notice shall be afforded within 15 business days of the action.",
        "Tests two different pre-hearing mechanisms with two different hearing clocks and different "
        "disciplinary character.",
        "247 CMR 10.07 and 10.08", CMR10, "247 CMR 10.00",
        ["Summary suspension carries a seven-day hearing clock; a cease and desist notice carries 15 business days.",
         "A cease and desist or quarantine notice is expressly non-disciplinary."],
        numeric=[{"fact": "hearing clock after suspension prior to hearing", "value": 7, "unit": "days",
                  "conditions": "limited to the necessity of the summary action"},
                 {"fact": "hearing clock after a cease and desist or quarantine notice", "value": 15,
                  "unit": "business days", "conditions": "limited to the necessity of the notice"}],
        related=["MA-DISCIPLINE-ACTION-TYPES"],
    ),
    _rule(
        "MA-DISCIPLINE-SCOPE-AND-IMPAIRMENT", 1, "Licensure and discipline", "Scope and impairment grounds",
        "Grounds reaching scope violations, impairment and unlicensed practice",
        "Under 247 CMR 10.03(1) grounds for discipline include engaging in conduct beyond the authorized "
        "scope of a pharmacist, pharmacy intern or pharmacy technician; practising the profession while the "
        "ability to practise is impaired by illness, use of alcohol, drugs, chemicals or any other "
        "substance, or as a result of any mental or physical condition; engaging in abuse or illegal use of "
        "prescription drugs or controlled substances; continuing to practise after a registration is "
        "lapsed, suspended or revoked; and knowingly permitting, aiding or abetting an unlicensed person to "
        "perform activities requiring a licence or registration.",
        "Tests that a supervising pharmacist who lets support personnel exceed scope is independently "
        "exposed, alongside the impairment and lapsed-registration grounds.",
        "247 CMR 10.03(1)(f) through (i) and (m)", CMR10, "247 CMR 10.00",
        ["Permitting another person to exceed scope is a ground against the permitting licensee.",
         "Impairment is a ground even without any dispensing error."],
        related=["MA-DISCIPLINE-ACTION-TYPES", "MA-URAMP"],
    ),
    _rule(
        "MA-DISCIPLINE-PROCEDURE-STAGES", 1, "Licensure and discipline", "Disciplinary procedure stages",
        "Complaint, investigative conference and adjudicatory hearing",
        "Under 247 CMR 10.02 a complaint is a communication filed with the Board or the Division of Health "
        "Professions Licensure which the Board determines, after investigation, merits further "
        "consideration or action; an investigative conference is an informal discussion relating to a "
        "complaint held with the Board; an adjudicatory hearing is a formal administrative hearing under "
        "M.G.L. c. 30A and 801 CMR 1.01; and an Order to Show Cause is a document served by the Board "
        "ordering the registrant to appear for a formal adjudicatory hearing. Under 247 CMR 10.04 the Board "
        "may schedule an investigative conference at any time prior to the commencement of a formal "
        "adjudicatory proceeding, with timely notice including a general statement of the issues, and under "
        "247 CMR 10.05 after receiving a complaint and investigative materials the Board may schedule "
        "either an investigative conference or a formal adjudicatory hearing.",
        "Tests the informal-versus-formal distinction and that the Board chooses the track after "
        "investigation rather than following a fixed sequence.",
        "247 CMR 10.02, 10.04 and 10.05", CMR10, "247 CMR 10.00",
        ["An investigative conference is informal and is not a prerequisite to a formal hearing.",
         "A communication becomes a complaint only once the Board determines it merits further action."],
        related=["MA-DISCIPLINE-ACTION-TYPES"],
    ),
    _rule(
        "MA-DISCIPLINE-REACH", 1, "Licensure and discipline", "Reach of Board disciplinary authority",
        "Credentials reachable by Board disciplinary action",
        "Under 247 CMR 10.01 the Board may take disciplinary action against a registered pharmacist, a "
        "pharmacy technician, a pharmacy, a pharmacy department, a wholesale licence, and a controlled "
        "substance registration issued by the Board. Under 247 CMR 10.03(1) the Board may impose "
        "disciplinary action on the grounds listed in M.G.L. c. 112, § 61 or on the grounds listed in 247 "
        "CMR 10.03, and under 247 CMR 10.03(2) nothing in that section limits the Board's adoption of "
        "policies and grounds for discipline through adjudication as well as through rulemaking.",
        "Tests that the Board's disciplinary reach extends across individual and entity credentials and "
        "that the listed grounds are not exhaustive.",
        "247 CMR 10.01 and 10.03(1) and (2)", CMR10, "247 CMR 10.00",
        ["The enumerated grounds are not a closed list; M.G.L. c. 112, § 61 grounds also apply.",
         "One incident can expose both the individual and the pharmacy credential."],
        related=["MA-DISCIPLINE-ACTION-TYPES"],
    ),
    # ---------------- Area 1 — remaining 247 CMR 8.00 / 3.00 / 4.00 ----------------
    _rule(
        "MA-INTERN-EXAM-BAR", 1, "Pharmacy personnel", "Intern conduct consequences",
        "Consequence of intern misconduct for licensure examination",
        "Under 247 CMR 8.01(17) a pharmacy intern found to have engaged in conduct in violation of federal "
        "or state laws or regulations may be prohibited from taking the examination for licensure, in "
        "addition to other sanctions imposed by the Board. Under 247 CMR 8.01(9) preceptors and interns "
        "shall, in a timely manner, submit on a Board form such information as the Board may require "
        "regarding the internship.",
        "Tests that intern misconduct can bar examination access rather than only producing sanctions on "
        "the intern licence.",
        "247 CMR 8.01(9) and (17)", CMR8, "247 CMR 8.00",
        ["Examination prohibition is in addition to, not instead of, other sanctions.",
         "The internship reporting duty runs on both the preceptor and the intern."],
        related=["MA-INTERN-WITHDRAWAL-NOTICE", "MA-PHARMACIST-EXAM-ELIGIBILITY"],
    ),
    _rule(
        "MA-TECH-TRAINING-PROGRAM-TYPES", 1, "Pharmacy personnel", "Technician training programs",
        "Board-approved pharmacy technician training programs",
        "Under 247 CMR 8.02(4) a Board-approved training program may include a pharmacy technician training "
        "program accredited by the American Society of Health System Pharmacists; a program provided by a "
        "branch of the United States Armed Services or Public Health Service; a Board-approved program "
        "which includes a minimum of 120 hours of theoretical and 120 hours of practical instruction; or "
        "any other pharmacy technician training course approved by the Board. Under 247 CMR 8.06(2) a "
        "pharmacist may train a technician or trainee through an on-the-job training program complying with "
        "written pharmacy guidelines consistent with professional, ethical and legal standards, copies of "
        "which shall be provided to the Board on request.",
        "Tests the specific hour split that a generic Board-approved program must meet and the separate "
        "status of on-the-job training.",
        "247 CMR 8.02(4) and 8.06(2)", CMR8, "247 CMR 8.00",
        ["The 120-hour theoretical and 120-hour practical split applies to the generic Board-approved route.",
         "On-the-job training is governed by written pharmacy guidelines produced on request."],
        numeric=[{"fact": "theoretical instruction in a generic Board-approved program", "value": 120,
                  "unit": "hours", "conditions": ""},
                 {"fact": "practical instruction in a generic Board-approved program", "value": 120,
                  "unit": "hours", "conditions": ""}],
        related=["MA-TECH-LICENSE-ELIGIBILITY", "MA-SUPPORT-DOCUMENTATION-DUTY"],
    ),
    _rule(
        "MA-TECH-EXAM-CONTENT", 1, "Pharmacy personnel", "Technician examination content",
        "Knowledge areas of the Board-approved technician examination",
        "Under 247 CMR 8.02(5) a Board-approved pharmacy technician examination shall cover practice "
        "settings; the duties and responsibilities of a pharmacy technician in relationship to other "
        "pharmacy personnel; laws and regulations regarding the practice of pharmacy and patient "
        "confidentiality; medical abbreviations and symbols; common dosage calculations; and "
        "identification of drugs, dosages, routes of administration and storage requirements.",
        "Tests the defined scope of the technician assessment examination, which is broader than "
        "calculations alone.",
        "247 CMR 8.02(5)", CMR8, "247 CMR 8.00",
        ["The examination is not limited to calculations; law and confidentiality are named areas.",
         "Duties in relationship to other pharmacy personnel is a distinct named area."],
        related=["MA-TECH-LICENSE-ELIGIBILITY", "MA-TECH-TRAINING-PROGRAM-TYPES"],
    ),
    _rule(
        "MA-INTERN-PROGRAM-CREDIT-APPROVAL", 1, "Pharmacy personnel", "Internship program credit",
        "Board control of internship credit for school programs",
        "Under 247 CMR 8.01(12) Massachusetts approved colleges and schools of pharmacy shall submit to the "
        "Board a written description of each demonstration project or clinical pharmacy program for which "
        "pharmacy internship credit is desired, and the Board may determine whether student participation "
        "in such projects or programs may be credited to the internship requirement. Under 247 CMR 8.01(13) "
        "the Board issues a Summary of Objectives and Procedures for Pharmacy Internship and guidelines for "
        "registered pharmacist preceptors and pharmacy interns.",
        "Tests that internship credit for a school program is a Board determination on a submitted "
        "description rather than a school decision.",
        "247 CMR 8.01(12) and (13)", CMR8, "247 CMR 8.00",
        ["The school proposes; the Board determines whether the program counts.",
         "This is separate from the out-of-state experience credit route."],
        related=["MA-INTERN-HOUR-COMPOSITION"],
    ),
    _rule(
        "MA-LICENSURE-APPLICATION-MECHANICS", 1, "Licensure", "Licensure application mechanics",
        "Completeness, name changes and non-refundable fees on licensure applications",
        "Under 247 CMR 3.01(3) a completed application for examination shall be fully and correctly "
        "completed by the applicant; include a recent passport-size photograph; include a certified birth "
        "certificate or other sufficient proof of place and date of birth; in the case of a name change, "
        "include written notification to the Board or the Board's designee of the name change; and include "
        "payment of all required fees unless waived under M.G.L. c. 112, § 1B. Under 247 CMR 3.01(8) the "
        "Board may refuse to consider any application that has not been properly completed, and under 247 "
        "CMR 3.01(9) all fees submitted in connection with a licensure application reviewed and acted upon "
        "by the Board are non-refundable.",
        "Tests that an incomplete application may simply not be considered and that fees are not recovered "
        "when that happens.",
        "247 CMR 3.01(3), (8) and (9)", CMR3, "247 CMR 3.00",
        ["The Board may decline to consider an incomplete application rather than curing it.",
         "Fees are non-refundable once the application has been reviewed and acted upon."],
        related=["MA-PHARMACIST-EXAM-ELIGIBILITY"],
    ),
    _rule(
        "MA-DUPLICATE-CERTIFICATE", 1, "Licensure", "Duplicate certificate of licensure",
        "Duplicate certificate of licensure and return of a recovered original",
        "Under 247 CMR 3.03, to request a duplicate certificate of licensure a registrant shall submit a "
        "Board-approved form and required documentation, and in the event that an original certificate of "
        "licensure is recovered after a duplicate has been issued, the duplicate shall be promptly returned "
        "to the Board.",
        "Tests the return obligation that attaches when the original resurfaces, so that only one "
        "certificate remains in circulation.",
        "247 CMR 3.03", CMR3, "247 CMR 3.00",
        ["It is the duplicate that is returned when the original is recovered, not the original.",
         "The return duty is prompt and does not wait for the next renewal."],
        related=["MA-LICENSURE-APPLICATION-MECHANICS"],
    ),
    _rule(
        "MA-CE-INSTRUCTOR-AND-POSTGRADUATE", 1, "Licensure", "Continuing education alternative credit",
        "Continuing education credit for instructors and postgraduate curricula",
        "Under 247 CMR 4.07 a registered pharmacist who is a Board-approved continuing education instructor "
        "receives continuing education credit for the program taught on a one-time basis annually. Under "
        "247 CMR 4.08 a registered pharmacist who enrols in a postgraduate pharmacy curriculum, "
        "postgraduate pharmacy program or Board-approved postgraduate medical program shall be awarded "
        "contact hours for satisfactory completion of each course within that curriculum, provided the "
        "sponsor or co-sponsor is a Board-authorized or ACPE-accredited provider and the course provides "
        "instruction in pharmacy, pharmaceutical sciences, pharmacy practice or pharmacy law.",
        "Tests two alternative credit routes and the conditions that limit them, including the once-a-year "
        "cap on credit for teaching.",
        "247 CMR 4.07 and 4.08", CMR4, "247 CMR 4.00",
        ["Teaching the same program repeatedly yields credit only once annually.",
         "Postgraduate course credit requires both an authorized sponsor and a qualifying subject area."],
        related=["MA-CE-ANNUAL-STRUCTURE", "MA-CE-PROVIDER-APPROVAL"],
    ),
    _rule(
        "MA-CE-PROGRAM-DELIVERY-CRITERIA", 1, "Licensure", "Continuing education program criteria",
        "Board criteria for home-study and live continuing education programs",
        "Under 247 CMR 4.05(3) an intended home-study or other mediated instruction program shall be "
        "developed by a professional group, follow a logical sequence, involve the learner by requiring an "
        "active response to materials and provide feedback, contain a test to indicate progress and verify "
        "completion, and supply a bibliography for continued study. Under 247 CMR 4.05(4) a live program "
        "shall involve direct interaction between the faculty and participants, and the faculty should "
        "possess appropriate credentials related to the discipline being taught. Under 247 CMR 4.05(7) "
        "provision shall be made for evaluating participants' attainment of the stated learner objectives "
        "and participants shall be given the opportunity to evaluate the program.",
        "Tests the different structural requirements the Board applies to home-study versus live programs.",
        "247 CMR 4.05(3), (4) and (7)", CMR4, "247 CMR 4.00",
        ["A home-study program must contain a completion test; a live program must involve direct interaction.",
         "Two-way evaluation is required: of the participant and by the participant."],
        related=["MA-CE-PROVIDER-APPROVAL"],
    ),
    # ---------------- Area 2 — 247 CMR 9.18 patient counseling ----------------
    _rule(
        "MA-COUNSELING-WHO-MAY-COUNSEL", 2, "Patient care", "Who may counsel",
        "Persons permitted to make the offer and to counsel",
        "Under 247 CMR 9.18(1) a pharmacist or a pharmacist's designee shall offer the counseling services "
        "of the pharmacist to each person who receives a prescription medication, and under 247 CMR 9.18(2) "
        "a pharmacist shall ensure his or her designee is appropriately trained to make the offer to "
        "counsel. Under 247 CMR 9.18(3) counseling shall be made by a pharmacist or a pharmacy intern, and "
        "a pharmacy technician or other individual may not counsel any patient.",
        "Tests the split between who may extend the offer and who may deliver the counseling, and that an "
        "intern may counsel while a technician may not.",
        "247 CMR 9.18(1) through (3)", CMR9, "247 CMR 9.00",
        ["A designee may make the offer but a technician may never provide the counseling itself.",
         "A pharmacy intern may counsel; the bar applies to technicians and other individuals."],
        related=["MA-COUNSELING", "MA-COUNSELING-TRIGGER-AND-CONTENT"],
    ),
    _rule(
        "MA-COUNSELING-TRIGGER-AND-CONTENT", 2, "Patient care", "Counseling trigger and content",
        "When counseling must be provided and what it may cover",
        "Under 247 CMR 9.18(4) a pharmacist or pharmacy intern shall provide counseling on each new drug "
        "therapy and on each drug therapy that in the pharmacist's professional judgment is deemed "
        "significant for the health and safety of the patient. Under 247 CMR 9.18(5) the pharmacist or "
        "intern shall provide such information as, in professional judgment, is necessary for the patient "
        "to understand proper use, which may include the name, description and indication of the "
        "medication; dosage form, dosage, route and duration; special directions; common side and adverse "
        "effects, interactions, contraindications and precautions; techniques for self-monitoring; proper "
        "storage and disposal; refill information; and action to take on a missed dose or adverse reaction.",
        "Tests that the trigger is not limited to new prescriptions and that the content list is a "
        "professional-judgment menu rather than a mandatory script.",
        "247 CMR 9.18(4) and (5)", CMR9, "247 CMR 9.00",
        ["A refill can trigger counseling where the therapy is significant for health and safety.",
         "The enumerated content is what counseling may include, applied through professional judgment."],
        related=["MA-COUNSELING-WHO-MAY-COUNSEL", "MA-COUNSELING-ACCESS-AND-DEVICE"],
    ),
    _rule(
        "MA-COUNSELING-CONSULTATION-AREA", 2, "Patient care", "Patient consultation area",
        "Designated patient consultation area requirements",
        "Under 247 CMR 9.18(6) a pharmacy shall have a designated patient consultation area, with signage "
        "stating Patient Consultation Area, designed to provide adequate privacy for confidential visual "
        "and auditory patient counseling, and the private consultation area shall be accessible by a "
        "patient from the outside of the prescription dispensing area without having to traverse a "
        "stockroom or the prescription dispensing area.",
        "Tests the access-route condition, which a compliant-looking private room can still fail.",
        "247 CMR 9.18(6)", CMR9, "247 CMR 9.00",
        ["Privacy alone is insufficient; the patient must reach the area without crossing the dispensing area or stockroom.",
         "The area requires its own Patient Consultation Area signage."],
        related=["MA-COUNSELING-RIGHTS-SIGN"],
    ),
    _rule(
        "MA-COUNSELING-RIGHTS-SIGN", 2, "Patient care", "Counseling rights sign",
        "Required posted notice of the right to counseling",
        "Under 247 CMR 9.18(7) a pharmacy shall post a sign of not less than 11 inches in height by 14 "
        "inches in width in a conspicuous place, adjacent to each area where prescriptions are dispensed, "
        "informing customers of their right to counseling by a pharmacist. The sign shall read, in letters "
        "not less than one half inch in height: Dear patients, you have the right to know about the proper "
        "use of your medication and its effects. If you need more information please ask the pharmacist.",
        "Tests the prescribed dimensions, letter height, placement and fixed wording of the notice.",
        "247 CMR 9.18(7)", CMR9, "247 CMR 9.00",
        ["The sign is required adjacent to each dispensing area, not once per store.",
         "Both the minimum sign size and the minimum letter height are prescribed."],
        numeric=[{"fact": "minimum sign height", "value": 11, "unit": "inches", "conditions": ""},
                 {"fact": "minimum sign width", "value": 14, "unit": "inches", "conditions": ""},
                 {"fact": "minimum letter height", "value": 0.5, "unit": "inches", "conditions": ""}],
        related=["MA-COUNSELING-CONSULTATION-AREA"],
    ),
    _rule(
        "MA-COUNSELING-ACCESS-AND-DEVICE", 2, "Patient care", "Counseling availability and measuring device",
        "Counseling availability, measuring devices and the inpatient exclusion",
        "Under 247 CMR 9.18(8) a pharmacy and pharmacist shall ensure counseling is available at all times "
        "when the pharmacy is open for business. Under 247 CMR 9.18(9) a pharmacy and pharmacist shall "
        "dispense or recommend a proper measuring device with all liquid medications. Under 247 CMR "
        "9.18(10) the provisions of 247 CMR 9.18 do not apply to pharmacists while practising in an "
        "inpatient setting, unless otherwise required by law or regulation.",
        "Tests three separate operational duties, including a measuring-device duty that is not limited to "
        "paediatric or controlled liquids.",
        "247 CMR 9.18(8) through (10)", CMR9, "247 CMR 9.00",
        ["The measuring-device duty applies to all liquid medications, not only paediatric ones.",
         "The inpatient exclusion covers the whole counseling section, not merely the offer."],
        exceptions=["247 CMR 9.18 does not apply to pharmacists practising in an inpatient setting unless "
                    "otherwise required by law or regulation."],
        related=["MA-COUNSELING-TRIGGER-AND-CONTENT"],
    ),
    # ---------------- Area 2 — 247 CMR 9.15 and 9.01 ----------------
    _rule(
        "MA-PRESCRIPTION-VALIDITY-DETERMINATION", 2, "Pharmacist practice", "Prescription validity determination",
        "Determinations a pharmacist must make before filling",
        "Under 247 CMR 9.15(2) a pharmacist may not fill a prescription unless the pharmacist, in the "
        "exercise of professional judgment, determines that the prescription was issued for a legitimate "
        "medical purpose by a practitioner acting in the usual course of professional practice; that there "
        "is a valid patient-practitioner relationship; that the prescription is authentic; and that the "
        "dispensing is in accordance with M.G.L. c. 94C, § 19(a).",
        "Tests that four separate determinations must all be satisfied and that they are the pharmacist's "
        "own professional judgment rather than the prescriber's assurance.",
        "247 CMR 9.15(2)", CMR9, "247 CMR 9.00",
        ["Authenticity and a valid patient-practitioner relationship are separate determinations.",
         "The prescriber's assurance does not discharge the pharmacist's own judgment."],
        related=["MA-PMP-REGISTRATION-DUTY"],
    ),
    _rule(
        "MA-PMP-REGISTRATION-DUTY", 2, "Pharmacist practice", "Monitoring program registration duty",
        "Pharmacist duty to register with the Prescription Monitoring Program",
        "Under 247 CMR 9.15(1) a pharmacist who dispenses medications reported to the Massachusetts "
        "Prescription Monitoring Program shall register with, and maintain login information for, the "
        "electronic system to monitor the prescribing and dispensing of controlled substances authorized by "
        "M.G.L. c. 94C, § 24A, known as PMP or MassPAT.",
        "Tests a personal registration duty triggered by dispensing reportable medications, distinct from "
        "the pharmacy's reporting obligations.",
        "247 CMR 9.15(1)", CMR9, "247 CMR 9.00",
        ["The duty is personal to the dispensing pharmacist, not satisfied by the pharmacy's account.",
         "It includes maintaining login information, not merely registering once."],
        related=["MA-PRESCRIPTION-VALIDITY-DETERMINATION", "MA-PMP-REPORTING"],
    ),
    _rule(
        "MA-CONDUCT-REFERRAL-REMUNERATION", 2, "Professional conduct", "Referral remuneration",
        "Prohibition on remuneration for referrals or business generation",
        "Under 247 CMR 9.01(11) a licensee may not offer, solicit or receive remuneration or anything of "
        "value to or from any person who owns, operates, manages or is an employee of a hospital, nursing "
        "home or other health care facility in return for a referral to a pharmacy, pharmacist, pharmacy "
        "technician or pharmacy intern, or for the generation of business from the sale or furnishing of "
        "any drugs, devices or services to any such persons or institutions.",
        "Tests that the prohibition runs in both directions and covers anything of value, not only cash "
        "payments.",
        "247 CMR 9.01(11)", CMR9, "247 CMR 9.00",
        ["The bar covers offering as well as receiving, and anything of value rather than money alone.",
         "Generating business is covered even without an individual patient referral."],
        related=["MA-CONDUCT-INSTITUTIONAL-DISPENSING"],
    ),
    _rule(
        "MA-CONDUCT-INSTITUTIONAL-DISPENSING", 2, "Professional conduct", "Institutional dispensing limits",
        "Dispensing limits for a hospital or clinic pharmacy without a Drug Store licence",
        "Under 247 CMR 9.01(13), unless otherwise permitted by law, a pharmacist connected with or employed "
        "by a hospital or clinic pharmacy that does not hold a Drug Store pharmacy licence may not dispense "
        "drugs to any person other than inpatients or outpatients of the hospital or clinic, or to "
        "employees of that hospital or clinic, or to those employees' spouses and children who live in the "
        "same house.",
        "Tests the closed list of permitted recipients where the institution lacks a Drug Store licence.",
        "247 CMR 9.01(13)", CMR9, "247 CMR 9.00",
        ["The permitted class is defined by relationship to the institution, not by clinical need.",
         "Family coverage reaches an employee's spouse and children living in the same house."],
        related=["MA-CONDUCT-REFERRAL-REMUNERATION"],
    ),
    # ---------------- Area 2 — 247 CMR 16.00 CDTM ----------------
    _rule(
        "MA-CDTM-PRESCRIPTIVE-CONDITIONS", 2, "Collaborative practice", "Prescriptive practice conditions",
        "Additional conditions where a CDTM agreement includes prescriptive practices",
        "Under 247 CMR 16.02(1)(f), if prescriptive practices are included in a collaborative practice "
        "agreement the pharmacist must maintain a current controlled substance registration issued by the "
        "Department during the term of the agreement pursuant to M.G.L. c. 94C, §§ 7 and 9 and 105 CMR "
        "700.000; complete the training required under M.G.L. c. 94C, § 18(e) before initially obtaining "
        "that controlled substance registration and at least biennially thereafter as a condition precedent "
        "to renewing the pharmacist licence; and submit an attestation, signed under the pains and "
        "penalties of perjury, that the pharmacist participates in, or has applied to participate in, "
        "MassHealth either as a provider of services or for the limited purpose of ordering and referring "
        "services covered by MassHealth.",
        "Tests three conditions that attach only when prescriptive practices are included, one of which is "
        "tied to pharmacist licence renewal rather than to the agreement.",
        "247 CMR 16.02(1)(f)", CMR16, "247 CMR 16.00",
        ["These conditions attach only if the agreement includes prescriptive practices.",
         "The section 18(e) training is a condition precedent to renewing the pharmacist licence, not just the agreement."],
        related=["MA-CDTM-QUALIFICATIONS", "MA-CDTM-CE-EVIDENCE"],
    ),
    _rule(
        "MA-CDTM-CE-EVIDENCE", 2, "Collaborative practice", "CDTM continuing education evidence",
        "Retention of collaborative practice continuing education evidence",
        "Under 247 CMR 16.02(2) an authorized pharmacist participating in collaborative drug therapy "
        "management must maintain evidence of completion of required continuing education for at least two "
        "years after the date of the current collaborative practice agreement. This sits on top of the "
        "247 CMR 16.02(1)(e) requirement to complete at least five additional contact hours of "
        "Board-approved continuing education in each year of the agreement term, addressing areas of "
        "practice generally related to the particular agreement.",
        "Tests a retention clock measured from the date of the current agreement rather than from the "
        "course or the renewal.",
        "247 CMR 16.02(1)(e) and (2)", CMR16, "247 CMR 16.00",
        ["Retention runs from the date of the current agreement, not from course completion.",
         "The five CDTM contact hours are additional to the ordinary renewal requirement."],
        numeric=[{"fact": "CDTM continuing education evidence retention", "value": 2, "unit": "years",
                  "conditions": "after the date of the current collaborative practice agreement"},
                 {"fact": "additional CDTM contact hours", "value": 5, "unit": "contact hours",
                  "conditions": "in each year of the agreement term"}],
        related=["MA-CDTM-PRESCRIPTIVE-CONDITIONS", "MA-CE-ANNUAL-STRUCTURE"],
    ),
    _rule(
        "MA-CDTM-DISCIPLINE-NOTICE", 2, "Collaborative practice", "CDTM discipline notification",
        "Duty to notify supervising physicians of discipline or practice restriction",
        "Under 247 CMR 16.02(3), whenever an authorized pharmacist participating in collaborative drug "
        "therapy management is disciplined by the Board, whether by agreement or Board order, or is "
        "otherwise subject to any practice restriction, the authorized pharmacist must provide written "
        "notification of that discipline or practice restriction to each supervising physician.",
        "Tests a notification duty owed to each supervising physician that is triggered by a consent "
        "agreement as well as by a Board order.",
        "247 CMR 16.02(3)", CMR16, "247 CMR 16.00",
        ["Discipline by agreement triggers the duty just as a Board order does.",
         "Notice runs to each supervising physician, not only to the primary one."],
        related=["MA-CDTM-PRESCRIPTIVE-CONDITIONS", "MA-DISCIPLINE-CONSENT-SURRENDER"],
    ),
]

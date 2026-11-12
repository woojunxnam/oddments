/* New Massachusetts MPJE privacy moderate/hard practice, 2026-11-11; independent legal audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "privacy": {
    "moderate": [
      {
        "question": "A patient posts a negative public review of a pharmacy and openly mentions taking a prescription medicine. The pharmacy manager plans a public reply listing the patient's other prescriptions to justify the pharmacy's actions. What is the HIPAA issue?",
        "choices": [
          "The patient's public post automatically authorizes any pharmacy reply containing PHI",
          "PHI may always be revealed to defend a business's online reputation",
          "Only an employee's printed paper records are protected, not social media messages",
          "The patient's own public statement does not authorize the pharmacy to disclose additional protected prescription information in its public response"
        ],
        "answer": "D",
        "explanations": [
          "A patient's public statement does not itself grant a covered pharmacy permission to disclose other PHI.",
          "Marketing or reputation management is not an unrestricted HIPAA disclosure exception.",
          "An unauthorized electronic disclosure can implicate HIPAA even when no paper record is involved.",
          "Correct. The pharmacy needs a proper HIPAA basis for its own disclosure; a public review is not blanket patient authorization."
        ],
        "citation": "HHS HIPAA Privacy Rule — Permitted Uses and Disclosures",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html"
      },
      {
        "question": "A pharmacist must send relevant medication and allergy history to a physician treating the same patient. No specific patient authorization is available. Which HIPAA rule generally permits the exchange?",
        "choices": [
          "Relevant disclosure to another treating provider generally can occur without a separate HIPAA authorization, and the minimum-necessary rule does not apply to provider treatment disclosures",
          "Any exchange between professionals requires a new notarized patient authorization",
          "A pharmacist may send information only if the patient pays cash",
          "Disclosure for treatment is categorically prohibited when OTC drugs are listed"
        ],
        "answer": "A",
        "explanations": [
          "Correct. HIPAA generally permits treatment disclosures without authorization, and disclosures to or requests by providers for treatment are exempt from minimum necessary.",
          "TPO is an established permissible disclosure route.",
          "Payment type is not a prerequisite to provider treatment disclosures.",
          "OTC therapy information may be relevant to safe treatment."
        ],
        "citation": "HHS HIPAA Minimum Necessary Guidance, 45 CFR 164.502(b)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html"
      },
      {
        "question": "A patient requests that the pharmacy not disclose information about a medication to the health plan. The patient paid in full out of pocket, the disclosure would be only for payment, and no law independently requires it. What must the covered pharmacy do?",
        "choices": [
          "The pharmacy may refuse any request to restrict health-plan disclosures",
          "Disclose the item to the health plan because every pharmacy claim must be billed",
          "Honor the qualifying HIPAA restriction on disclosure of that paid-in-full item to the health plan",
          "Tell the patient HIPAA restrictions are available only to Medicare recipients"
        ],
        "answer": "C",
        "explanations": [
          "The paid-in-full health-plan restriction is an important exception to the general rule that restrictions are discretionary.",
          "The pharmacy need not submit an unnecessary payment disclosure contrary to a qualifying restriction.",
          "Correct. HIPAA requires agreeing when the item was fully paid out of pocket and disclosure is only for payment/operations and not legally required.",
          "Plan type is not the defining criterion."
        ],
        "citation": "HHS HIPAA — Required Health-Plan Restriction for Paid-in-Full Services",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/under-hipaa-may-an-individual-request-that-a-covered-entity-restrict-how-it-uses-or-discloses-that-individuals-protect-health-information/index.html"
      },
      {
        "question": "A patient's friend arrives to pick up a specific previously filled prescription, knows the patient's name, and there is no indication that the patient objected. Is a prior written authorization naming the friend invariably required by HIPAA?",
        "choices": [
          "Yes, a notarized release is always necessary for any pickup",
          "No; a pharmacist may use reasonable professional judgment to infer that the friend is involved in care and permit pickup, disclosing only relevant information",
          "Yes, unless the friend has a prescriber DEA number",
          "No, because any friend may also receive the patient's entire medication history"
        ],
        "answer": "B",
        "explanations": [
          "HHS expressly permits reasonable inference for pickup.",
          "Correct. Under 45 CFR 164.510(b), prior listing of the friend is not universally required.",
          "DEA prescriber registration is not a family pickup authorization.",
          "The permission extends to involvement in care, not unlimited access to the entire profile."
        ],
        "citation": "HHS HIPAA FAQ — Family/Friend Prescription Pickup, 45 CFR 164.510(b)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/can-a-patient-have-a-friend-or-family-member-pick-up-a-prescription/index.html"
      },
      {
        "question": "A covered pharmacy receives a valid patient request for access to their designated-record-set information on September 1, 2026. No lawful extension has been invoked. When must the pharmacy generally act?",
        "choices": [
          "Within 30 calendar days after receipt, subject to the rule's written-notice extension pathway when properly used",
          "Only within six years, because HIPAA requires six-year retention",
          "Within five business days in every circumstance",
          "Only after the patient's next annual visit"
        ],
        "answer": "A",
        "explanations": [
          "Correct. HIPAA generally requires acting within 30 calendar days, with a possible additional 30 days after timely written notice.",
          "The six-year documentation concept is not an access-response deadline.",
          "Five business days is not the general federal HIPAA access clock.",
          "Patient access rights are not restricted to annual appointments."
        ],
        "citation": "HHS HIPAA Access Timelines, 45 CFR 164.524(b)(2)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/how-timely-must-a-covered-entity-be/index.html"
      },
      {
        "question": "A pharmacy manager says HIPAA requires destroying every patient's medical records exactly six years after the most recent fill. Which statement is correct?",
        "choices": [
          "HIPAA's six-year policy-document rule is also a universal medical record destruction deadline",
          "No other state retention rules can apply to a Massachusetts pharmacy",
          "Any pharmacy may immediately destroy all controlled-substance records after dispensing",
          "HIPAA does not prescribe a universal medical-record retention period; applicable Massachusetts record laws and safeguards must also be considered"
        ],
        "answer": "D",
        "explanations": [
          "Required HIPAA compliance documentation and medical-record retention are distinct.",
          "State and other federal laws may establish record retention requirements.",
          "Controlled-drug record keeping is subject to its own regulatory deadlines.",
          "Correct. HHS explicitly states that HIPAA Privacy Rule does not impose a general medical-record retention schedule."
        ],
        "citation": "HHS HIPAA Medical Record Retention FAQ",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/does-hipaa-require-covered-entities-to-keep-medical-records-for-any-period/index.html"
      },
      {
        "question": "A covered pharmacy discovers a reportable breach of unsecured PHI affecting 34 patients. It will notify the affected individuals under HIPAA. When is its HHS Secretary report generally due?",
        "choices": [
          "At the same moment every affected individual is counseled",
          "Exactly one year after the patient's next prescription",
          "Within 60 days after the end of the calendar year in which the breach was discovered, unless submitted earlier",
          "Only when the number of affected patients reaches 500"
        ],
        "answer": "C",
        "explanations": [
          "The individual-notice and HHS-small-breach schedules are distinct.",
          "An arbitrary anniversary of a prescription is not the federal reporting rule.",
          "Correct. For breaches of fewer than 500 people, HHS allows annual Secretary reporting within 60 days after year-end.",
          "Breaches affecting fewer than 500 people are still reportable to HHS."
        ],
        "citation": "HHS HIPAA Breach Notification Rule, 45 CFR 164.400–414",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
      },
      {
        "question": "A Massachusetts pharmacist receives patient records from a federally assisted SUD treatment program covered by 42 CFR Part 2. A staff member assumes the 2026 Part 2 update eliminates all special patient consent. What is correct?",
        "choices": [
          "Every SUD record is now public to all pharmacists for any purpose",
          "Part 2 still applies; the update permits a single consent for future TPO uses/disclosures while preserving special limits, including uses against the patient in legal proceedings",
          "The special privacy rules apply only to drugs in federal Schedule II",
          "A pharmacy may post the Part 2 records in an employee group chat"
        ],
        "answer": "B",
        "explanations": [
          "Part 2 continues to impose special confidentiality rules.",
          "Correct. The 2024 final rule, required for compliance February 16, 2026, permits a broad TPO consent but not unlimited disclosure.",
          "Part 2 status relates to covered SUD program records, not merely a drug schedule.",
          "An employee group chat is not automatically a permissible purpose or recipient."
        ],
        "citation": "HHS — 42 CFR Part 2 Final Rule Fact Sheet (compliance February 16, 2026)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html"
      },
      {
        "question": "A Massachusetts pharmacy maintains electronic patient names, Social Security numbers, and bank account numbers. The owner says that meeting HIPAA automatically means there is no separate Massachusetts information-security obligation. Which rule is relevant?",
        "choices": [
          "201 CMR 17.00 requires a comprehensive written information security program with appropriate administrative, physical, and technical safeguards for covered MA residents' personal information",
          "201 CMR 17.00 applies only to government hospitals and never to pharmacies",
          "MA privacy law requires storing customer passwords on open shelves",
          "A federal HIPAA policy always replaces every state security requirement"
        ],
        "answer": "A",
        "explanations": [
          "Correct. MA 201 CMR 17 imposes a state written security-program duty for covered personal information.",
          "The regulation covers relevant private businesses handling MA personal information.",
          "Open storage of credentials conflicts with security responsibilities.",
          "State and federal privacy/security requirements can both apply."
        ],
        "citation": "201 CMR 17.03–17.04 — Massachusetts Written Information Security Program",
        "sourceUrl": "https://www.mass.gov/regulations/201-CMR-1700-standards-for-the-protection-of-personal-information-of-ma-residents"
      },
      {
        "question": "A Massachusetts pharmacy reviews HIPAA reproductive-health privacy training written in early 2025, claiming that the entire special 2024 rule remains unchanged. What should it recognize as of November 2026?",
        "choices": [
          "All HIPAA protections for medical information disappeared in 2025",
          "The entire HIPAA privacy rule was vacated by the court",
          "The 2024 rule has never been subject to a court ruling",
          "A June 18, 2025 federal court decision vacated most of that specific reproductive-health final rule, while other HIPAA protections and remaining NPP changes continue to apply"
        ],
        "answer": "D",
        "explanations": [
          "Vacating most of one 2024 amendment did not eliminate general HIPAA privacy protections.",
          "The court order was limited, not a cancellation of all HIPAA.",
          "HHS public guidance describes the court order and its effect.",
          "Correct. HHS identifies partial vacatur and surviving Notice of Privacy Practices requirements effective by February 16, 2026."
        ],
        "citation": "HHS HIPAA Reproductive-Health Privacy Rule Vacatur Notice, June 18, 2025",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/phi-reproductive-health/index.html"
      }
    ],
    "hard": [
      {
        "question": "A pharmacist discovers that a billing service was provided PHI for payment purposes. The patient has now asked the pharmacy to keep a different prescription secret from the health plan and has paid in full out of pocket for that specific item. No disclosure is required by law. Which workflow is compliant?",
        "choices": [
          "Share all current prescriptions with the health plan because one past payment disclosure permanently allows every future claim",
          "Reject the patient's request because restrictions are never mandatory",
          "Restrict the paid-in-full item's PHI from payment/operations disclosure to the health plan, while separately handling permitted earlier treatment/payment information and legal requirements",
          "Delete every medication record, including controlled-substance dispensing records, to enforce the restriction"
        ],
        "answer": "C",
        "explanations": [
          "Prior legitimate payment disclosures do not automatically override a later qualifying request for a distinct item.",
          "Paid-in-full health-plan restriction is mandatory when HIPAA conditions are met.",
          "Correct. Apply the restriction to the paid-in-full item while preserving separate lawful uses, records and any legally required disclosures.",
          "Record destruction is not how the specific health-plan disclosure restriction is implemented."
        ],
        "citation": "HHS HIPAA — Required Health-Plan Restriction for Paid-in-Full Services",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/under-hipaa-may-an-individual-request-that-a-covered-entity-restrict-how-it-uses-or-discloses-that-individuals-protect-health-information/index.html"
      },
      {
        "question": "A pharmacy's unsecured PHI breach affects 620 residents of Massachusetts and no one else. It is a HIPAA reportable breach, and there is no law-enforcement delay. Which notifications generally apply?",
        "choices": [
          "Notify affected individuals, HHS Secretary, and prominent media outlets serving the affected state, without unreasonable delay and no later than 60 days",
          "Notify HHS only after the end of the next calendar year",
          "Notify only the pharmacy wholesaler and insurer",
          "Notify the media only if the breach includes at least 5,000 people"
        ],
        "answer": "A",
        "explanations": [
          "Correct. HIPAA requires individual and HHS notice for 500+; media notice applies when more than 500 residents of one state/jurisdiction are affected.",
          "Annual HHS reporting is for breaches involving fewer than 500 individuals.",
          "Wholesale and insurer notification cannot replace required HIPAA breach notices.",
          "The media threshold is more than 500 affected residents of a state/jurisdiction."
        ],
        "citation": "HHS HIPAA Breach Notification Rule, 45 CFR 164.400–414",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
      },
      {
        "question": "An employee emails a patient's medication list to an unrelated address. The recipient later claims deletion without forwarding it. The pharmacy manager proposes immediately treating it as 'no breach' with no record. What is the best HIPAA response?",
        "choices": [
          "Any email sent to the wrong recipient is automatically exempt from HIPAA breach rules",
          "Conduct and document a HIPAA breach risk assessment, considering the unauthorized recipient, PHI sensitivity, whether it was accessed, and mitigation, before deciding whether notification is required",
          "All wrong-recipient emails require notifying 500 media outlets",
          "Delete the employee's account to prove the original email was not sent"
        ],
        "answer": "B",
        "explanations": [
          "HIPAA's breach determination requires considering exceptions and risk of compromise.",
          "Correct. Recipient mitigation can matter but does not justify skipping assessment and documentation.",
          "Media notice depends on jurisdictional scope and threshold, not every error.",
          "Deleting an account does not eliminate the disclosure event or evidence."
        ],
        "citation": "HHS HIPAA Breach Notification Rule, 45 CFR 164.400–414",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
      },
      {
        "question": "A patient explicitly told a pharmacy not to disclose a particular sensitive therapy to the patient's adult sibling. The sibling later arrives to pick up a different medicine and asks for the patient's full medication profile. What does HIPAA allow?",
        "choices": [
          "The sibling is automatically entitled to every patient medication record because they may pick up prescriptions",
          "Patient objection never matters when a person is related by blood",
          "The pharmacy may share the full history if the sibling presents a driver's license",
          "Do not reveal the objected-to therapy or unrestricted profile; a permissible pickup disclosure remains limited to information directly relevant to the sibling's involvement"
        ],
        "answer": "D",
        "explanations": [
          "Pickup permission does not grant wholesale access to PHI.",
          "HIPAA specifically respects a patient's objection to family disclosure.",
          "Identity verification does not independently grant full records access.",
          "Correct. Apply the patient objection and 45 CFR 164.510(b)'s relevant-information limit to the specific pickup situation."
        ],
        "citation": "HHS HIPAA FAQ — Family/Friend Prescription Pickup, 45 CFR 164.510(b)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/can-a-patient-have-a-friend-or-family-member-pick-up-a-prescription/index.html"
      },
      {
        "question": "A federally assisted Part 2 program receives a patient's single consent for all future treatment, payment and operations disclosures. Separately maintained SUD counseling notes analyze the clinician's session with that patient. Can the program include the notes under the same general TPO consent?",
        "choices": [
          "No; separate SUD counseling notes require separate patient consent, distinct from the broad Part 2 TPO consent",
          "Yes; the 2026 rules abolished the separate-consent concept entirely",
          "Yes, provided the notes contain the patient's date of birth",
          "Only if a pharmacy technician initials the consent form"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The 2024 Part 2 final rule preserves specific consent for separately maintained SUD counseling notes.",
          "Part 2 TPO alignment is not an unrestricted waiver.",
          "Demographic data does not resolve the special note category.",
          "A technician signature does not replace required patient consent."
        ],
        "citation": "HHS — 42 CFR Part 2 Final Rule Fact Sheet (compliance February 16, 2026)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html"
      },
      {
        "question": "A health plan lawfully received a Part 2 SUD treatment record under a patient's broad TPO consent. An investigative agency requests it to prosecute the patient, without a separate patient consent or required court order. Which rule controls?",
        "choices": [
          "HIPAA TPO redisclosure automatically permits any prosecution use",
          "The health plan must provide it because the record was previously shared for payment",
          "The plan's normal HIPAA redisclosure permissions do not override Part 2's special restriction on use of the record in legal proceedings against the patient",
          "The records are unprotected as soon as transmitted electronically"
        ],
        "answer": "C",
        "explanations": [
          "Part 2 expressly retains legal-proceedings protections beyond general TPO redisclosures.",
          "Payment-related access does not equal prosecutorial authorization.",
          "Correct. A Part 2 TPO consent does not authorize use against the patient in legal proceedings without the separate legal conditions.",
          "Electronic transfer does not remove Part 2's restrictions."
        ],
        "citation": "HHS Part 2 Patient Records and Redisclosure Guidance (2026)",
        "sourceUrl": "https://www.hhs.gov/hipaa/part-2/index.html"
      },
      {
        "question": "A Massachusetts pharmacy detects unauthorized acquisition of customer Social Security numbers and medication records, meeting the separate Massachusetts security-breach definition as well as HIPAA's reportable unsecured-PHI definition. Which compliance analysis is correct?",
        "choices": [
          "Only HHS must be notified because HIPAA fully preempts all Massachusetts data-breach rules",
          "Assess and fulfill both HIPAA and M.G.L. c.93H obligations, including MA Attorney General, consumer affairs director and affected resident notice as applicable",
          "Only the drug manufacturer must receive notice",
          "The pharmacy can avoid all notification by permanently closing its website"
        ],
        "answer": "B",
        "explanations": [
          "Federal and MA notification obligations can both apply when their triggers are met.",
          "Correct. c.93H §3 has its own Massachusetts notification recipients and timing standards.",
          "Manufacturer notice is not the general legal substitute.",
          "Closing a website does not cancel a past breach or notification duties."
        ],
        "citation": "M.G.L. c.93H §3(b) — Massachusetts Security Breach Notification",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter93H/Section3"
      },
      {
        "question": "A patient submits a valid access request to an MA pharmacy. The pharmacy's outside records vendor says it will take 25 days to locate the records and asks the pharmacy to start its 30-day clock when the vendor finishes. What is required by HIPAA?",
        "choices": [
          "Start the clock on the vendor's completion date, regardless of when the patient asked",
          "Do not give the records because outsourcing creates a permanent exception",
          "The patient must directly sue the vendor before the pharmacy responds",
          "Start the 30-calendar-day period when the covered pharmacy received the request; vendor delays count toward that clock, and any extension requires timely written notice"
        ],
        "answer": "D",
        "explanations": [
          "HIPAA measures access response from covered-entity receipt, not vendor delivery.",
          "Using a business associate does not extinguish the individual's access right.",
          "A civil lawsuit is not a prerequisite to normal HIPAA access.",
          "Correct. HHS expressly states vendor delays consume the original 30-calendar-day access period."
        ],
        "citation": "HHS HIPAA Access Timelines, 45 CFR 164.524(b)(2)",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/how-timely-must-a-covered-entity-be/index.html"
      },
      {
        "question": "An employee says that because a pharmacy is subject to HIPAA Security Rule safeguards, Massachusetts 201 CMR 17.03 cannot also require a WISP for customer names paired with bank account numbers. Which statement is correct?",
        "choices": [
          "HIPAA security and Massachusetts WISP are separate frameworks; a covered pharmacy must meet relevant requirements of both, with a written program and appropriate administrative, technical and physical safeguards",
          "HIPAA automatically exempts pharmacies from every MA data-security regulation",
          "A WISP is only necessary after 500 affected residents have been breached",
          "A WISP requires no staff oversight or risk evaluation"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Massachusetts requires a comprehensive written information-security program for covered resident personal information, alongside HIPAA when applicable.",
          "State duties are not generally canceled by HIPAA-covered status.",
          "WISP is a preventive obligation, not only a post-breach trigger.",
          "The regulation addresses supervision and risk-based protection."
        ],
        "citation": "201 CMR 17.03–17.04 — Massachusetts Written Information Security Program",
        "sourceUrl": "https://www.mass.gov/regulations/201-CMR-1700-standards-for-the-protection-of-personal-information-of-ma-residents"
      },
      {
        "question": "A compliance officer reads a 2024-era handbook saying the new HIPAA reproductive-health attestation rule and every associated restriction automatically remain enforceable through 2026. An MA pharmacist asks what to do before changing a workflow. Which answer is best?",
        "choices": [
          "Continue the handbook unchanged because federal court rulings never affect HHS regulations",
          "Ignore all current HIPAA privacy rules because the 2025 decision vacated them",
          "Recognize the June 2025 court vacatur of most of the specific 2024 reproductive-health rule, apply surviving general HIPAA/MA law and NPP requirements, and verify current HHS guidance before changing controls",
          "Release protected information upon any request because the special rule was challenged"
        ],
        "answer": "C",
        "explanations": [
          "HHS confirms the specific court vacatur and the need to distinguish affected provisions.",
          "General HIPAA privacy rules remain in force.",
          "Correct. The vacatur was not a wholesale repeal of HIPAA; remaining 2026 NPP modifications and state rules still matter.",
          "Removal of one special amendment does not create unlimited disclosure permission."
        ],
        "citation": "HHS HIPAA Reproductive-Health Privacy Rule Vacatur Notice, June 18, 2025",
        "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/phi-reproductive-health/index.html"
      }
    ]
  }
});

/* Individually authored and checked against primary authorities, November 10, 2026.
   Chapters 5–6: Prescription Validity and Schedule II Core.
   No synthetic answer-choice generation. */
Object.assign(window.MPJE_SUPPLEMENTAL_VERIFIED || (window.MPJE_SUPPLEMENTAL_VERIFIED = {}), {
  "prescription-validity": [
    {
      "question": "A Massachusetts prescriber issues a properly completed, personally signed paper prescription for lisinopril, a Schedule VI drug. The electronic prescribing system is working. What should the dispensing pharmacist know?",
      "choices": [
        "Schedule VI prescriptions may be issued on paper under a specific Massachusetts ePrescribing exception, if all other requirements are met",
        "Any paper Schedule VI prescription is void after 2021 regardless of its contents",
        "The pharmacist must convert the paper order into a Schedule II emergency prescription",
        "The prescriber must obtain a DEA Schedule II registration before issuing lisinopril"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 105 CMR 721.070(A)(9) exempts Schedule VI prescriptions from the electronic issuance requirement; other format, authorization and clinical rules still matter.",
        "Massachusetts expressly lists Schedule VI among the exceptions, so an otherwise lawful paper order is not automatically void.",
        "A routine antihypertensive prescription is not an emergency Schedule II order.",
        "Lisinopril is not federally Schedule II; state authority for Schedule VI is a separate question."
      ],
      "citation": "105 CMR 721.070(A)(9)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A veterinarian in Massachusetts issues a lawful paper prescription for a pet. The pharmacist asks whether it is automatically invalid because the veterinarian did not transmit an ePrescription. What is correct?",
      "choices": [
        "All veterinary prescriptions must be electronically transmitted with no exception",
        "The pharmacy must refuse any veterinary prescription unless it is faxed",
        "The pharmacist should reclassify every veterinary drug as Schedule VI",
        "Veterinarian prescriptions are an expressly listed Massachusetts ePrescribing exception; other applicable law still governs"
      ],
      "answer": "D",
      "explanations": [
        "The Massachusetts regulation explicitly makes an exception for prescriptions issued by veterinarians.",
        "There is no universal requirement to substitute fax transmission for a valid veterinary paper prescription.",
        "The veterinary context does not automatically change a drug's controlled-substance schedule.",
        "Correct. 105 CMR 721.070(A)(1) allows a qualifying veterinary prescription to be written or oral when otherwise lawful."
      ],
      "citation": "105 CMR 721.070(A)(1)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A practitioner orders a patient-specific compounded drug preparation that requires nonstandard directions not supported by the ePrescribing workflow. Which Massachusetts ePrescribing rule is relevant?",
      "choices": [
        "Compounded products must always be generated as electronic prescriptions and can never use paper",
        "Compounded drug preparations are among the listed exceptions, subject to applicable law and Department guidance",
        "The pharmacist can dispense any compound without a valid prescription",
        "Any over-the-counter product becomes a Schedule II drug after compounding"
      ],
      "answer": "B",
      "explanations": [
        "105 CMR 721.070(A)(8) specifically recognizes a compounded-preparation exception.",
        "Correct. The exception permits another lawful prescription format for qualifying compounded drug preparations; it does not remove clinical or statutory safeguards.",
        "The exception is about the form of a prescription, not a general exemption from having one.",
        "Compounding does not automatically change a drug's federal schedule or authorize dispensing without a prescription."
      ],
      "citation": "105 CMR 721.070(A)(8)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "An office prints an electronic prescription and transmits its image by ordinary fax. There was no documented electronic failover, and the office tells the pharmacist it counts as a secure electronic transmission. Which statement is correct?",
      "choices": [
        "Ordinary facsimile is always identical to a compliant electronic transmission",
        "A fax replaces the prescriber's electronic signature in all cases",
        "Ordinary fax transmission is not an electronic transmission under 105 CMR 721.010; the prescription must independently satisfy a lawful paper/fax exception",
        "Any faxed image automatically meets federal EPCS requirements"
      ],
      "answer": "C",
      "explanations": [
        "Massachusetts expressly distinguishes electronic transmission from fax.",
        "The electronic-signature and transmission rules are not waived simply because a document was faxed.",
        "Correct. 105 CMR 721.010 excludes facsimile from Electronic Transmission, and 721.040 addresses invalid noncompliant electronic prescriptions.",
        "Federal EPCS security requirements cannot be satisfied solely by sending a printed image through ordinary fax."
      ],
      "citation": "105 CMR 721.010 (Electronic Transmission); 721.040(C)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A Massachusetts prescriber issues a Schedule II opioid prescription and omits the required patient partial-fill notation. Which statement best identifies the missing legal element?",
      "choices": [
        "No notation is required unless the patient is younger than 18",
        "The prescription must state that the patient may request dispensing of less than the full prescribed quantity",
        "The pharmacist may add 'five refills' instead of a partial-fill statement",
        "The notation requirement applies only to Schedule VI prescriptions"
      ],
      "answer": "B",
      "explanations": [
        "105 CMR 721.020(D)(7) does not limit the notation to minors.",
        "Correct. A Schedule II opioid prescription must include the notation concerning the patient's option to request a smaller quantity.",
        "Refill wording is a different issue; Schedule II refills are prohibited.",
        "The notation is specifically tied to opioid substances in Schedule II."
      ],
      "citation": "105 CMR 721.020(D)(7)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A Massachusetts certified nurse practitioner who is still practicing under required supervision sends an otherwise valid prescription but leaves out the supervising qualified health professional's name. How does the pharmacist evaluate the form?",
      "choices": [
        "The supervising professional's name is required unless the nurse has authority for independent practice",
        "Any state-licensed nurse practitioner must list a DEA number instead of a supervisor's name, without exception",
        "The pharmacist may fill any prescription with an NPI, regardless of the supervising-practitioner field",
        "A pharmacy technician may replace the supervisor's name with the patient's insurance ID"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 105 CMR 721.020(E) requires the supervising qualified healthcare professional's name unless the issuing nurse is authorized for independent practice.",
        "A DEA registration number has a distinct function and does not universally replace the supervising professional's identity.",
        "An NPI does not substitute for a legally required prescriber-field entry.",
        "Technicians cannot invent missing prescriber information or override a formal prescription requirement."
      ],
      "citation": "105 CMR 721.020(E)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "An ePrescription for metformin (Schedule VI) unexpectedly converts to a computer-generated fax during transmission. The prescription includes the required information except signature; the pharmacist promptly records it and reasonably authenticates the unfamiliar prescriber. No other exception is violated. Which is most accurate?",
      "choices": [
        "Every computer-generated fax requires an emergency Schedule II follow-up order",
        "A failover can only occur for gabapentin because it is reported to the PMP",
        "A Schedule VI fax is always invalid even when the electronic system fails",
        "This may qualify as a Schedule VI failover treated as an oral prescription, without a written or electronic follow-up"
      ],
      "answer": "D",
      "explanations": [
        "105 CMR 721.020(G) provides a specific Schedule VI failover pathway.",
        "Gabapentin is an additional drug excluded from the no-follow-up pathway; it is not the required model for this exception.",
        "An authenticated failover may satisfy the limited regulatory exception.",
        "Correct. With the listed information, recording, authentication, and non-additional-drug conditions met, 105 CMR 721.020(G) allows no separate follow-up."
      ],
      "citation": "105 CMR 721.010 (Failover); 721.020(G)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A community prescriber writes two different medications on the same outpatient prescription form. Which rule generally applies to Massachusetts prescriptions outside the hospital multi-drug exception?",
      "choices": [
        "A prescription form may contain unlimited drug products if the pharmacy uses separate labels",
        "Two medications are allowed if the pharmacist separates them into two dispensing bags",
        "Each drug product must have its own prescription form or record, except for the specified hospital setting",
        "The requirement is waived whenever both prescriptions are Schedule VI"
      ],
      "answer": "C",
      "explanations": [
        "Labels or packaging do not substitute for the form or record rule.",
        "Bagging medications separately does not cure a noncompliant prescription record.",
        "Correct. 105 CMR 721.050 requires separate prescription forms or records for multiple drug products, with a specific hospital exception.",
        "The rule covers prescriptions generally and does not create a blanket Schedule VI exception."
      ],
      "citation": "105 CMR 721.050",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "An electronic prescription form uses 'no substitution' as its default selection, requiring the prescriber to uncheck it for generic substitution. What is the compliance issue?",
      "choices": [
        "The pharmacy may ignore any non-default selection and always substitute",
        "Massachusetts allows 'no substitution' only as the system's default",
        "A prescriber's electronic signature automatically satisfies the 'no substitution' instruction",
        "The 'no substitution' choice must be an independent, non-default element of the prescription form"
      ],
      "answer": "D",
      "explanations": [
        "A lawful no-substitution instruction is permitted; the problem is how the field is presented.",
        "105 CMR 721.020(B) prohibits using 'no substitution' as the default.",
        "The brand-selection requirement cannot be satisfied by the signature alone.",
        "Correct. The regulation requires a distinct non-default 'no substitution' element with the specified interchange statement."
      ],
      "citation": "105 CMR 721.020(B)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    },
    {
      "question": "A pharmacist receives an otherwise valid paper Schedule IV prescription from a properly licensed Massachusetts prescriber. The pharmacist does not know whether the prescriber holds a waiver from electronic prescribing. What does 105 CMR 721.070(C) say?",
      "choices": [
        "The pharmacist is not required to verify that the valid written prescription falls under an ePrescribing exception, although all other validity checks remain",
        "The pharmacist must call DPH before filling every paper Schedule IV prescription",
        "The prescription must be destroyed because the pharmacist cannot see a waiver letter",
        "A paper prescription becomes federally Schedule VI if the prescriber's waiver cannot be confirmed"
      ],
      "answer": "A",
      "explanations": [
        "Correct. The regulation expressly relieves the pharmacist of verifying the prescriber's ePrescribing exception for an otherwise valid written/oral order.",
        "The rule does not create a universal DPH call obligation for every written Schedule IV prescription.",
        "The absence of waiver proof alone does not require destroying an otherwise valid prescription.",
        "A prescription's format does not alter the federal scheduling of the drug."
      ],
      "citation": "105 CMR 721.070(C)",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
    }
  ],
  "cii-core": [
    {
      "question": "An otherwise valid Massachusetts prescription for extended-release morphine (Schedule II) contains 'Refills: 1.' After dispensing the first fill, the patient requests that refill. How should the pharmacist proceed?",
      "choices": [
        "Refill once because the prescriber explicitly authorized it",
        "Refill once if the patient has not yet used the full 30-day supply",
        "Do not refill the Schedule II prescription; obtain a new legally valid prescription if more medication is needed",
        "Convert the unused refill to a Schedule III order without prescriber involvement"
      ],
      "answer": "C",
      "explanations": [
        "Schedule II refill restrictions cannot be waived by writing a refill number.",
        "Waiting until the first supply is used does not authorize a CII refill.",
        "Correct. Federal 21 CFR 1306.12(a) and M.G.L. c.94C §23(b) prohibit Schedule II refills.",
        "A pharmacist cannot unilaterally change the drug's schedule or create a new prescriber order."
      ],
      "citation": "M.G.L. c. 94C § 23(b); 21 CFR 1306.12(a)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"
    },
    {
      "question": "A Massachusetts pharmacy receives an otherwise valid Schedule II prescription 36 days after the original issue date, with no special sequential earliest-fill instructions. Which issue controls whether it can be dispensed?",
      "choices": [
        "The prescription becomes invalid 30 days after issuance, independently of the quantity it authorizes",
        "The pharmacist can dispense it if the intended therapy lasts only 10 days",
        "The patient may extend the prescription validity by requesting a partial fill",
        "Federal law requires all Schedule II prescriptions to remain valid indefinitely"
      ],
      "answer": "A",
      "explanations": [
        "Correct. M.G.L. c.94C §23(a) provides a 30-day state validity period for written or electronic CII orders.",
        "Days' supply does not reset the written prescription's validity clock.",
        "Partial-fill options do not cure an expired original prescription.",
        "Federal law does not eliminate Massachusetts's specific Schedule II expiration rule."
      ],
      "citation": "M.G.L. c. 94C § 23(a)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"
    },
    {
      "question": "A prescriber issues an otherwise lawful Massachusetts prescription for 60 days of methylphenidate for ADHD. The pharmacist confirms no other statutory restriction applies. Is a single 60-day fill permitted?",
      "choices": [
        "No, every federally Schedule II drug is limited to a maximum 7-day supply",
        "No, all Schedule II prescriptions are capped at 30 days in Massachusetts",
        "Yes, but only when the patient is receiving hospice care",
        "Yes. Massachusetts allows a single fill of up to 90 days for eligible non-opioid Schedule II or III drugs"
      ],
      "answer": "D",
      "explanations": [
        "A seven-day first-opioid prescription rule is not a general Schedule II stimulant limit.",
        "Current Massachusetts §23(d) distinguishes eligible non-opioid drugs from other CII/CIII products.",
        "Hospice status is not the controlling fact for a non-opioid stimulant's §23(d) category.",
        "Correct. Methylphenidate is expressly named among non-opioid drugs eligible for up to a 90-day single fill."
      ],
      "citation": "M.G.L. c. 94C § 23(d)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"
    },
    {
      "question": "An outpatient presents a 60-day prescription for oxycodone to treat chronic pain. The patient is not receiving opioid-use-disorder treatment and no implantable infusion pump is involved. Under the Massachusetts single-fill quantity rule, what is the issue?",
      "choices": [
        "No issue; all Schedule II opioids may receive up to 90 days per single fill",
        "This ordinary Schedule II opioid prescription exceeds the general 30-day single-fill limit",
        "It must be treated as a Schedule III prescription because it is for chronic pain",
        "The pharmacist may ignore days' supply when the prescriber writes the diagnosis"
      ],
      "answer": "B",
      "explanations": [
        "The 90-day exception does not generally cover Schedule II opioids for pain treatment.",
        "Correct. Under M.G.L. c.94C §23(d), other CII and CIII prescriptions are generally limited to 30 days per single fill.",
        "Clinical indication does not reschedule oxycodone.",
        "A diagnosis does not override a statutory maximum for a single fill."
      ],
      "citation": "M.G.L. c. 94C § 23(d)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"
    },
    {
      "question": "A prescriber intends to issue three separate, otherwise valid Schedule II prescriptions that together provide a total 90-day supply, with the second and third to be filled later. Which safeguard is specifically required by federal law?",
      "choices": [
        "The pharmacist must promise to fill all three immediately",
        "The practitioner must label every prescription as a 'refill'",
        "The practitioner must provide written earliest-fill-date instructions on each later prescription and determine no undue diversion risk, consistent with state law",
        "The prescriber may postdate the signature instead of documenting the earliest fill date"
      ],
      "answer": "C",
      "explanations": [
        "Multiple Schedule II prescriptions are not authority to fill all later prescriptions immediately.",
        "Each is a separate prescription; it is not a refill of the first.",
        "Correct. 21 CFR 1306.12(b)(1) requires earliest-fill-date instructions for later prescriptions and a diversion-risk judgment.",
        "Federal issuance requirements do not instruct practitioners to alter the genuine issuance date to a future date."
      ],
      "citation": "21 CFR 1306.12(b)(1)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.12"
    },
    {
      "question": "During a genuine Schedule II prescribing emergency, an office nurse calls the pharmacy with an oxycodone order and explains that the physician authorized the nurse to communicate it. Which is the correct federal rule?",
      "choices": [
        "The nurse may always call a Schedule II emergency prescription on behalf of the physician",
        "The emergency oral Schedule II authorization must be personally communicated by the prescribing individual practitioner",
        "A nurse may call it if the pharmacy manager approves",
        "An agent may always transmit an emergency oral CII order if a written confirmation arrives the same day"
      ],
      "answer": "B",
      "explanations": [
        "DEA's published policy does not delegate emergency oral Schedule II communication to an agent.",
        "Correct. DEA's October 6, 2010 policy expressly requires the prescriber personally to communicate the oral emergency CII authorization.",
        "Pharmacy manager approval does not override federal prescriber-communication restrictions.",
        "A later paper order does not cure the required initial prescriber-to-pharmacist communication."
      ],
      "citation": "DEA Federal Register 75 FR 61613; 21 CFR 1306.11(d)",
      "sourceUrl": "https://www.govinfo.gov/content/pkg/FR-2010-10-06/html/2010-25136.htm"
    },
    {
      "question": "A prescriber requests a 30-day supply of a Schedule II opioid by telephone at midnight because the clinic is closed. The patient has an acute condition but a legally sufficient non-Schedule-II alternative is available. Which description of the emergency exception is accurate?",
      "choices": [
        "The federal oral CII emergency exception requires more than after-hours convenience; the defined emergency conditions must be satisfied",
        "Any nighttime telephone order automatically satisfies the emergency requirement",
        "The emergency exception permits the entire 30-day supply whenever a prescriber calls",
        "A registered pharmacist can independently declare an emergency and call in the patient's prescription"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 21 CFR 1306.11(d), together with the emergency definition, requires immediate necessity, no appropriate alternative and inability to provide an otherwise compliant order.",
        "Time of day alone does not satisfy the federal emergency definition.",
        "Even when permitted, the quantity must be limited to the emergency period, not a routine full treatment supply.",
        "The prescriber must make the required judgment; the pharmacist cannot manufacture an order."
      ],
      "citation": "21 CFR 1306.11(d)(1); 21 CFR 290.10",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
    },
    {
      "question": "A qualifying emergency oral Schedule II prescription is communicated on a Monday. The prescriber asks whether the federal follow-up deadline is seven business days because Massachusetts regulations mention business days. Which answer is safest?",
      "choices": [
        "The follow-up is optional if the patient has already taken the medication",
        "Massachusetts automatically extends every federal emergency follow-up deadline to 14 days",
        "The pharmacy can postpone federal documentation until the next monthly inspection",
        "Federal law requires the qualifying follow-up within seven calendar days, even if a state wording suggests a longer business-day period"
      ],
      "answer": "D",
      "explanations": [
        "21 CFR 1306.11(d)(4) imposes a mandatory follow-up.",
        "A state regulation cannot lengthen a stricter applicable federal deadline.",
        "A later inspection is unrelated to the legal follow-up obligation.",
        "Correct. Apply the stricter federal seven-day deadline; the Massachusetts seven-business-day language does not extend it."
      ],
      "citation": "21 CFR 1306.11(d)(4); 105 CMR 721.060(B)(4)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
    },
    {
      "question": "A pharmacist receives a properly signed faxed Schedule II prescription for a resident of a long-term care facility. The pharmacy verifies the patient's LTCF status and all other requirements. Under federal law, may that fax serve as the original prescription?",
      "choices": [
        "Never; every faxed Schedule II order always requires a separate paper original",
        "Only if the drug is also Schedule VI in Massachusetts",
        "Yes. A qualifying Schedule II prescription for a long-term care facility resident may use the fax as the original",
        "Only when the drug is delivered to a veterinarian"
      ],
      "answer": "C",
      "explanations": [
        "21 CFR 1306.11(f) creates a specific LTCF exception to the usual original-paper rule.",
        "An LTCF Schedule II prescription is federally controlled, not automatically Schedule VI.",
        "Correct. Under 21 CFR 1306.11(f), the signed qualifying fax may serve as the original prescription.",
        "Veterinary dispensing is unrelated to the LTCF fax exception."
      ],
      "citation": "21 CFR 1306.11(f)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
    },
    {
      "question": "A pharmacist dispensed an emergency oral Schedule II prescription, but the practitioner failed to supply the required signed follow-up within the federal period. What federal action is required of the pharmacist?",
      "choices": [
        "Simply save the original oral record and take no further action",
        "Notify the nearest DEA office of the practitioner's failure to provide the follow-up",
        "Convert the prescription into a five-refill Schedule III order",
        "Ask a pharmacy technician to sign a replacement prescription on behalf of the prescriber"
      ],
      "answer": "B",
      "explanations": [
        "The federal rule imposes a reporting duty on the pharmacist when the follow-up does not arrive.",
        "Correct. 21 CFR 1306.11(d)(4) requires DEA notification of the missing follow-up.",
        "A dispensing pharmacist cannot change controlled-substance scheduling or legally create refills.",
        "A pharmacy technician cannot provide the prescriber's required signed follow-up."
      ],
      "citation": "21 CFR 1306.11(d)(4)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
    }
  ]
});

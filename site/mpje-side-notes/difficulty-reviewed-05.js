/* Hand-authored difficulty expansion: Chapter 05. Official regulatory references checked 2026-11-11. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "prescription-validity": {
    "moderate": [
      {
        "question": "A patient brings an otherwise lawful, personally signed paper prescription for lisinopril from a Massachusetts practitioner. The clinic's EPCS system works normally. What is the pharmacist's best conclusion?",
        "choices": [
          "The paper form is invalid for every medication after 2024",
          "Schedule VI is an ePrescribing exception, so an otherwise lawful paper prescription is not invalid merely because it was not electronic",
          "The pharmacist must obtain a DEA Form 222 for the lisinopril",
          "The pharmacist must treat lisinopril as Schedule II for first-fill purposes"
        ],
        "answer": "B",
        "explanations": [
          "Schedule VI is expressly excepted from mandatory electronic prescribing.",
          "Correct. 105 CMR 721.070(A)(9) exempts MA Schedule VI prescriptions from the electronic issuance requirement.",
          "DEA Form 222 applies to ordering Schedule I–II controlled inventory, not this ordinary prescription.",
          "Lisinopril is not a Schedule II controlled substance."
        ],
        "citation": "105 CMR 721.070(A)–(C)",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "A veterinarian issues an otherwise valid paper prescription for a dog's Schedule IV medication. An MA pharmacy technician says every controlled-drug prescription must be electronic. What is correct?",
        "choices": [
          "Paper prescriptions issued by veterinarians are an enumerated Massachusetts ePrescribing exception, but other controlled-drug requirements still apply",
          "The veterinarian must submit the prescription electronically because the drug is Schedule IV",
          "Any veterinary prescription is exempt from every DEA requirement",
          "Only Schedule II veterinary prescriptions can be paper"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Veterinary-issued prescriptions are excepted from mandatory ePrescribing under 105 CMR 721.070(A)(1).",
          "The regulation expressly includes veterinarians among exemptions.",
          "The exception does not remove all federal controlled-substance rules.",
          "The listed exemption is not limited to Schedule II."
        ],
        "citation": "105 CMR 721.070(A)–(C)",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "An MA pharmacist receives an otherwise valid signed paper Schedule IV prescription. The prescriber may have a hardship waiver, but the pharmacy has not seen one. What does the Massachusetts regulation require?",
        "choices": [
          "The pharmacist must contact DPH to verify every waiver before dispensing",
          "The pharmacist must refuse every paper Schedule III–V prescription",
          "Every written controlled-drug prescription may be converted into an oral CII emergency",
          "The pharmacist is not required to verify whether the prescriber properly qualifies for an ePrescribing exception"
        ],
        "answer": "D",
        "explanations": [
          "105 CMR 721.070(C) does not impose that waiver-checking duty.",
          "Otherwise valid paper orders are not automatically barred on format alone.",
          "An ordinary written prescription does not establish an emergency CII oral authorization.",
          "Correct. The pharmacist evaluates prescription validity, but need not prove the prescriber's ePrescribing exception."
        ],
        "citation": "105 CMR 721.070(A)–(C)",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "A clinic sends a scanned picture of a signed routine Schedule II prescription by fax and labels the fax 'EPCS.' No LTCF, hospice, or qualifying infusion exception applies. What is true?",
        "choices": [
          "Printing a signed prescription and faxing it meets the federal EPCS transmission requirements",
          "A fax is a direct EPCS whenever the prescriber uses an electronic medical record",
          "Faxing does not turn the paper prescription into an EPCS, and the original signed paper is ordinarily needed for routine CII dispensing",
          "The fax creates authorization for five refills"
        ],
        "answer": "C",
        "explanations": [
          "EPCS requires compliant electronic creation, signing, and transmission.",
          "An image from an EMR is not the required electronic controlled-prescription record.",
          "Correct. A routine CII fax ordinarily does not replace the original signed paper order.",
          "Schedule II refills are prohibited."
        ],
        "citation": "21 CFR §1306.11(a), (d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
      },
      {
        "question": "A Massachusetts prescriber explicitly authorizes an office employee to communicate a routine oral Schedule IV prescription to a pharmacy. Which statement about the employee is correct?",
        "choices": [
          "The employee may create and personally sign a new CII paper prescription",
          "The authorized employee can relay the prescriber's oral order, but that does not confer authority to sign the practitioner's prescription",
          "Any employee may invent a drug and dose as long as the prescriber is busy",
          "An employee can change the named patient after dispensing"
        ],
        "answer": "B",
        "explanations": [
          "Communicating a message is different from authenticating a practitioner's signed prescription.",
          "Correct. M.G.L. c.94C §18(b) allows express agents to communicate oral orders; it does not grant independent prescribing authority.",
          "Agents cannot originate unauthorized therapy.",
          "Patient identity cannot be changed by an employee to repair a prescription."
        ],
        "citation": "M.G.L. c.94C §18(a)–(b)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "An otherwise valid Massachusetts Schedule II prescription omits the patient's street address. The pharmacist independently knows the correct address from the patient profile. Under the Board's permitted-change policy, what is ordinarily possible?",
        "choices": [
          "Add the omitted patient address without consulting the prescriber, with appropriate documentation",
          "Change the patient's name to that of a relative",
          "Add unlimited refills while adding the address",
          "Replace the prescriber's signature with the pharmacist's"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Policy 2018-01 permits adding an omitted patient address to CII without consultation.",
          "Changing the patient is prohibited.",
          "Schedule II refills are not authorized.",
          "A pharmacist cannot substitute for the required prescriber signature."
        ],
        "citation": "Board Policy 2018-01 (revised Jan. 2024)",
        "sourceUrl": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download"
      },
      {
        "question": "The name of the prescribing practitioner on a Schedule II prescription is incorrect, and the clinic asks the pharmacist to replace it with a different prescriber after a phone call. What is required?",
        "choices": [
          "Make the change if the drug remains the same",
          "Change the name after the patient signs a waiver",
          "A new prescription is required; the prescriber name is not a field that may be changed or added under MA policy",
          "Only the pharmacy technician may update this field"
        ],
        "answer": "C",
        "explanations": [
          "Prescriber identity is nonchangeable under the state policy.",
          "Patient agreement does not authorize changing prescriber identity.",
          "Correct. Board Policy 2018-01 specifically forbids changing or adding the prescriber's name.",
          "Technicians have no special authority to alter an invalid prescriber identity."
        ],
        "citation": "Board Policy 2018-01 (revised Jan. 2024)",
        "sourceUrl": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download"
      },
      {
        "question": "A prescriber calls to change the controlled drug on an already-issued valid prescription from hydrocodone to oxycodone. What is the appropriate legal route?",
        "choices": [
          "Substitute one controlled ingredient for another as long as the schedule matches",
          "Use the original prescription because the two drugs are both opioids",
          "Record only the changed tablet color",
          "Obtain a new valid prescription for the different controlled substance"
        ],
        "answer": "D",
        "explanations": [
          "Matching controlled schedules does not make a different drug interchangeable.",
          "Opioid class membership does not authorize changing the prescribed substance.",
          "Appearance is not the legal issue.",
          "Correct. MA Policy 2018-01 forbids changing the controlled substance prescribed, apart from lawful generic substitution."
        ],
        "citation": "Board Policy 2018-01 (revised Jan. 2024)",
        "sourceUrl": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download"
      },
      {
        "question": "An electronic prescription for a Schedule III drug arrives, but its required dose field was altered in transmission. The original prescriber confirms what the dose should have been. How does federal EPCS law treat that altered electronic record?",
        "choices": [
          "Once an electronic prescription's required content changes during transmission, that record is invalid for dispensing",
          "A telephone confirmation always retroactively validates the altered EPCS",
          "Only Schedule II EPCS can become invalid during transmission",
          "The prescription is automatically valid if the pharmacy prints it"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 21 CFR 1306.08(d) says altered required prescription information invalidates the electronic controlled order.",
          "Verification does not by itself reverse the electronic invalidation.",
          "The rule applies to electronic controlled-substance prescriptions, not only CII.",
          "Printing cannot restore the unaltered electronic record."
        ],
        "citation": "21 CFR §1306.08(a)–(d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
      },
      {
        "question": "An ePrescription system automatically checks 'no substitution' on every new Massachusetts prescription, and prescribers must uncheck it to permit generic substitution. What must be corrected?",
        "choices": [
          "Nothing: the default must always prevent substitution",
          "The physician may use their electronic signature as the only no-substitution mark",
          "The system's default conflicts with the Massachusetts requirement that no-substitution not be selected by default",
          "State law requires no-substitution to appear only on paper"
        ],
        "answer": "C",
        "explanations": [
          "105 CMR 721.020(B) disallows no-substitution as a default.",
          "The signature is not a substitute for the unique no-substitution element.",
          "Correct. A default no-substitution setting violates the regulation's format requirement.",
          "The rule applies across permitted prescription formats."
        ],
        "citation": "105 CMR 721.020(B)–(G), 721.040, 721.050",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      }
    ],
    "hard": [
      {
        "question": "An MA prescriber issues a personally signed, otherwise compliant paper Schedule II prescription during a documented electronic outage. The patient reaches the pharmacy before electronic service returns. The pharmacist has not verified whether the prescriber applied for a waiver. Which approach is correct?",
        "choices": [
          "Refuse because every paper Schedule II prescription requires a prescriber waiver",
          "Convert the paper into an oral refill to make it electronic",
          "Dispense solely on the basis that a patient states there was an outage, without checking the controlled-drug prescription",
          "The outage may be an ePrescribing exception; the pharmacist need not independently verify the exception but must still meet all federal and state Schedule II dispensing requirements"
        ],
        "answer": "D",
        "explanations": [
          "Technical outage is its own exception, distinct from a hardship waiver.",
          "An oral refill cannot substitute for a CII original.",
          "Controlled-drug validity and authenticity remain necessary.",
          "Correct. MA allows temporary technological failures, while federal CII original and other requirements remain."
        ],
        "citation": "105 CMR 721.070(A)–(C)",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "At midnight an office nurse calls with a new oxycodone order, says there is a medical emergency, and offers to mail a signed prescription in seven days. The physician does not communicate orally with the pharmacist. Which statement is most accurate?",
        "choices": [
          "Emergency circumstances always allow a nurse to provide the federal CII oral authorization",
          "The pharmacist must obtain the prescribing practitioner's direct oral authorization for the federal emergency CII pathway, plus apply the emergency quantity and follow-up safeguards",
          "The promised mail follow-up alone makes the nurse's call a valid CII emergency order",
          "The pharmacy can dispense a 90-day supply solely because the case is urgent"
        ],
        "answer": "B",
        "explanations": [
          "Federal §1306.11(d) requires oral authorization of the prescribing individual practitioner.",
          "Correct. State agency communication rules do not eliminate the federal emergency CII conditions.",
          "Follow-up is additional to, not a replacement for, lawful initial authorization.",
          "Emergency quantity is limited to what is needed during the emergency."
        ],
        "citation": "21 CFR §1306.11(a), (d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
      },
      {
        "question": "A Massachusetts physician transmits a faxed, manually signed paper oxycodone prescription for an ordinary outpatient. The physician was exempt from mandatory electronic issuance because of a network outage. The patient asks whether the fax itself permits immediate CII dispensing. What is correct?",
        "choices": [
          "The Massachusetts ePrescribing exception does not remove the separate federal original-prescription requirement for routine Schedule II faxed paper orders",
          "The fax must be accepted as a federal original because an outage occurred",
          "An electronic outage automatically creates three refills",
          "An office nurse can authenticate the fax by phone and replace the prescriber signature"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Separate MA issuance exceptions and federal fax-as-original requirements both apply.",
          "The outage exception does not expand the narrow fax-as-original categories.",
          "CII refills remain prohibited.",
          "An agent's authentication does not replace the practitioner's original signature."
        ],
        "citation": "21 CFR §1306.11(a), (d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"
      },
      {
        "question": "A community prescriber sends a single outpatient prescription record containing two different medicines and clear directions for both. It is not a hospital-setting prescription. Which statement matches Massachusetts formatting rules?",
        "choices": [
          "Two different drugs are always allowed on one outpatient form if they share a prescriber",
          "Only Schedule II drugs require separate records",
          "A pharmacist may fix the problem by deleting one drug without another prescription",
          "Each drug product must ordinarily be on its own prescription form or record outside the special hospital-setting allowance"
        ],
        "answer": "D",
        "explanations": [
          "Clarity alone does not remove the separate-record requirement outside hospitals.",
          "The format rule is not restricted to CII.",
          "Deleting a prescription element does not authorize a second independent prescription.",
          "Correct. 105 CMR 721.050 contains a conditional hospital-setting exception."
        ],
        "citation": "105 CMR 721.020(B)–(G), 721.040, 721.050",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "A hospital physician places two drugs in one hospital-setting prescription record, but directions are given for only one of them. The hospital points to Massachusetts' multiple-product exception. What is the best response?",
        "choices": [
          "Both drugs may be dispensed because hospitals may omit all instructions",
          "The rule allows any number of drugs on a hospital order without checking identity",
          "The hospital exception still requires clear directions for the use and interchange of each drug; clarify the missing information",
          "The pharmacist must treat both products as Schedule VI without reviewing them"
        ],
        "answer": "C",
        "explanations": [
          "The hospital allowance is conditional, not a waiver of directions.",
          "Patient and medication requirements remain in force.",
          "Correct. Under 105 CMR 721.050, each product's directions and interchange instructions must be clear.",
          "The setting does not override scheduling."
        ],
        "citation": "105 CMR 721.020(B)–(G), 721.040, 721.050",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "A controlled Schedule IV prescription is electronically signed, but the intermediary modifies a required quantity field before it reaches the pharmacy. The prescriber's assistant then telephones with the correct quantity. Which approach best satisfies the federal electronic controlled-substance rules?",
        "choices": [
          "Fill the altered EPCS, since the assistant's telephone call cures data alteration",
          "Do not fill the altered EPCS; obtain a new legally compliant order rather than treating the altered record as valid",
          "Print it, add the assistant's initials, and treat it as a signed paper original",
          "Give the patient a partial fill without a valid prescription"
        ],
        "answer": "B",
        "explanations": [
          "Federal EPCS alteration is invalid even with later verbal explanation.",
          "Correct. A compliant replacement order or other independent lawful prescription route is needed.",
          "A printout does not bear an original manual prescriber signature.",
          "Partial filling does not eliminate prescription-validity requirements."
        ],
        "citation": "21 CFR §1306.08(a)–(d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
      },
      {
        "question": "A Massachusetts pharmacist receives a signed Schedule II prescription with a Do Not Fill Before instruction for November 20. On November 18 the clinic asks the pharmacist by telephone to change the earliest date to November 18. Which action is consistent with MA policy?",
        "choices": [
          "Do not edit the Schedule II earliest-fill date; obtain a new valid prescription if a different date is intended",
          "Change the earliest date because the prescriber approved",
          "Erase the restriction if the patient has no remaining opioid supply",
          "Change the date after adding a notation that the drug is non-opioid"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Policy 2018-01 lists a Schedule II earliest-fill date among information that may never be changed or added.",
          "Verbal prescriber approval does not override the specific prohibition.",
          "Patient need does not authorize editing a prohibited field.",
          "The prohibition is not limited to opioid Schedule II drugs."
        ],
        "citation": "Board Policy 2018-01 (revised Jan. 2024)",
        "sourceUrl": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download"
      },
      {
        "question": "A Schedule II prescription arrives without an issue date but includes a valid prescriber signature. The prescriber tells the pharmacist the actual date written. The clinic also asks the pharmacist to change the prescriber's name to a different physician. How should the pharmacist handle the two requests?",
        "choices": [
          "Both changes may be made after any phone call",
          "Both fields are automatically optional for a Schedule II order",
          "The pharmacist may change the prescriber name but never add a missing issue date",
          "An omitted date of issue may be added after the permitted consultation, but a different prescriber name requires a new prescription"
        ],
        "answer": "D",
        "explanations": [
          "The policy distinguishes permitted additions from prohibited prescriber identity changes.",
          "Issue date and prescriber identity remain important legally required elements.",
          "Changing the prescriber name is prohibited; adding an omitted date can be allowed.",
          "Correct. Policy 2018-01 allows adding the omitted CII issue date after consultation, but not changing the prescriber's name."
        ],
        "citation": "Board Policy 2018-01 (revised Jan. 2024)",
        "sourceUrl": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download"
      },
      {
        "question": "An MA Schedule VI ePrescription for amoxicillin unexpectedly becomes a computer-generated fax during transmission. The fax lacks a manual signature, contains all otherwise required details, is promptly entered in the pharmacy record, and an unfamiliar prescriber is reasonably authenticated. The product is not an Additional Drug. What is the best classification?",
        "choices": [
          "It is automatically a valid EPCS because a fax is electronic transmission",
          "It qualifies as a Schedule II oral emergency and needs a seven-day written follow-up",
          "It may qualify as a permitted Schedule VI failover treated as an oral prescription without a separate follow-up, if all 105 CMR 721.020(G) conditions hold",
          "All unsigned faxed prescriptions must be discarded without exception"
        ],
        "answer": "C",
        "explanations": [
          "105 CMR 721 defines fax as distinct from electronic transmission.",
          "Failover is a distinct Schedule VI pathway, not a CII emergency.",
          "Correct. The regulation creates conditional failover treatment for qualifying Schedule VI prescriptions.",
          "A qualifying failover can be accepted even without a manual signature."
        ],
        "citation": "105 CMR 721.020(B)–(G), 721.040, 721.050",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "An MA pharmacy's software receives a Schedule VI gabapentin ePrescription as a computer-generated fax after a transmission defect. The fax meets all other failover elements, but gabapentin is subject to Massachusetts Additional Drug reporting. Which conclusion is most accurate?",
        "choices": [
          "Every Schedule VI fax is a permitted failover even if listed as an Additional Drug",
          "The 105 CMR 721.020(G) failover exception excludes an Additional Drug; use another lawful prescription pathway",
          "The Additional Drug designation converts gabapentin into a federal Schedule II medication",
          "The pharmacist may ignore the distinction if the quantity is 30 tablets"
        ],
        "answer": "B",
        "explanations": [
          "The regulation explicitly excludes Additional Drugs from this failover pathway.",
          "Correct. Schedule VI status alone does not override the Additional Drug carveout.",
          "Massachusetts' reporting category does not change gabapentin's federal schedule.",
          "Quantity does not remove a form-specific exception."
        ],
        "citation": "105 CMR 721.020(B)–(G), 721.040, 721.050",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      }
    ]
  }
});

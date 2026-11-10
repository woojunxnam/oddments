/* Hand-authored Massachusetts MPJE supplemental scenarios for Chapters 13–14, 2026-11-10. */
Object.assign(window.MPJE_SUPPLEMENTAL_VERIFIED || (window.MPJE_SUPPLEMENTAL_VERIFIED = {}), {
  "privacy": [
    {
      "question": "A pharmacist opens the prescription profile of a famous athlete who is not a pharmacy patient under the pharmacist's care. The pharmacist is curious but does not disclose the information. What is correct?",
      "choices": [
        "Access is acceptable because nothing was printed",
        "Curiosity access is not a permitted treatment, payment or operations purpose and can violate HIPAA even without further disclosure",
        "HIPAA applies only when records are sent outside the pharmacy",
        "The pharmacist may access anyone's record if they hold an active license"
      ],
      "answer": "B",
      "explanations": [
        "Printing is not the test for authorized access.",
        "Correct. Accessing PHI without a legitimate authorized purpose can violate HIPAA.",
        "HIPAA regulates impermissible use and access as well as disclosures.",
        "Professional licensure does not authorize unrestricted record access."
      ],
      "citation": "HIPAA Privacy Rule — permitted uses and disclosures",
      "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/uses-and-disclosures-for-treatment-payment-and-health-care-operations/index.html"
    },
    {
      "question": "A patient is taking a medication that may interact with a new prescription. The pharmacist contacts the treating prescriber and shares the relevant medication history. Does HIPAA always require a separate written patient authorization first?",
      "choices": [
        "No. HIPAA generally permits relevant disclosures for treatment without a separate written authorization",
        "Yes. Any communication between a pharmacist and prescriber requires a signed HIPAA authorization",
        "No, because HIPAA does not apply to pharmacies",
        "Yes, unless the patient is over age 65"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Treatment disclosures are ordinarily permitted under HIPAA without a special patient authorization.",
        "HIPAA allows covered providers to exchange relevant information for treatment.",
        "Pharmacies are generally covered entities when conducting covered transactions.",
        "Age alone does not control treatment-disclosure authorization."
      ],
      "citation": "45 CFR 164.506 — treatment disclosures",
      "sourceUrl": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-164.506"
    },
    {
      "question": "A patient's adult sibling arrives to collect an ordinary prescription. The patient previously identified the sibling as someone who may help with pickup, and there is no indication of an objection. What may the pharmacy do?",
      "choices": [
        "Disclose the patient's entire medical history to the sibling",
        "Refuse any prescription pickup by anyone other than the patient",
        "Treat the sibling as the patient's legal guardian automatically",
        "Use professional judgment to disclose information directly relevant to the sibling's involvement in the patient's care or pickup"
      ],
      "answer": "D",
      "explanations": [
        "Permission for pickup does not authorize unlimited unrelated disclosures.",
        "HIPAA permits appropriate involvement by family or friends.",
        "A sibling does not automatically become a legal personal representative.",
        "Correct. HIPAA permits relevant disclosures to persons involved in care or payment, subject to the rule's conditions."
      ],
      "citation": "45 CFR 164.510(b) — family and friends",
      "sourceUrl": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-164.510"
    },
    {
      "question": "A patient submits a valid written request for access to their HIPAA designated-record-set information. The pharmacy has no grounds for a lawful extension. What is the general federal deadline?",
      "choices": [
        "Within seven business days",
        "Within 90 days in all cases",
        "Within 30 calendar days after receiving the request",
        "Only after the patient pays an annual HIPAA membership fee"
      ],
      "answer": "C",
      "explanations": [
        "Seven business days is not the standard HIPAA access response period.",
        "HIPAA's usual access period is shorter than 90 days.",
        "Correct. 45 CFR 164.524(b)(2) generally requires action within 30 days; a qualifying extension has specific conditions.",
        "HIPAA access rights do not require purchasing a membership."
      ],
      "citation": "45 CFR 164.524(b)(2) — access response",
      "sourceUrl": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-164.524"
    },
    {
      "question": "A pharmacy has a patient profile containing prescription histories and clinical notes. A trainee says HIPAA requires every pharmacy to destroy all medical records after six years. Which correction is best?",
      "choices": [
        "HIPAA's six-year documentation retention requirement is not a universal six-year patient-medical-record destruction rule; applicable state record laws also matter",
        "Every prescription must be destroyed exactly six years after dispensing",
        "HIPAA requires permanent retention of every medical record without exception",
        "HIPAA's documentation retention rule applies only to paper records"
      ],
      "answer": "A",
      "explanations": [
        "Correct. HIPAA has documentation retention rules, but it does not establish a universal medical-record destruction deadline.",
        "A pharmacy must follow applicable pharmacy and record-retention laws.",
        "HIPAA does not impose indefinite retention of every medical record.",
        "HIPAA protections and documentation duties are not limited to paper records."
      ],
      "citation": "HHS — HIPAA does not prescribe a universal medical-record retention period",
      "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/faq/does-hipaa-require-covered-entities-to-keep-medical-records-for-any-period/index.html"
    },
    {
      "question": "A covered pharmacy discovers a breach of unsecured PHI affecting 18 patients. Which general federal notification principle applies, assuming no exception to the breach definition?",
      "choices": [
        "Breaches involving fewer than 500 people never require individual notification",
        "Affected individuals generally must be notified without unreasonable delay and no later than 60 days after discovery",
        "The pharmacy may wait until the next biennial pharmacy renewal",
        "The pharmacy must post the full patient list publicly"
      ],
      "answer": "B",
      "explanations": [
        "The fewer-than-500 distinction affects some reporting logistics, not whether affected individuals are notified.",
        "Correct. HIPAA's breach notification rule generally sets a 60-day outside limit for notifying affected individuals.",
        "State licensure cycles do not extend federal breach-notification deadlines.",
        "Publicly listing patient names would compound the privacy harm."
      ],
      "citation": "45 CFR 164.404 — individual breach notification",
      "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
    },
    {
      "question": "A pharmacist receives substance-use-disorder treatment records from a federally assisted Part 2 program. A trainee says all SUD records are automatically identical to ordinary HIPAA records. What is the best response?",
      "choices": [
        "Part 2 never applies to pharmacy information",
        "Only DEA, not HHS, administers Part 2 privacy requirements",
        "Part 2 provides additional protections for qualifying SUD-program records; apply its current consent and redisclosure framework",
        "Part 2 permits unrestricted sharing of all SUD-program records with employers"
      ],
      "answer": "C",
      "explanations": [
        "Part 2 may apply when qualifying program records are received.",
        "HHS administers the Part 2 confidentiality regulations.",
        "Correct. Qualifying Part 2 records have specialized protections, including updated 2024 rule provisions.",
        "Employment-related disclosure is not universally permitted."
      ],
      "citation": "42 CFR Part 2 — HHS confidentiality guidance",
      "sourceUrl": "https://www.hhs.gov/hipaa/part-2/index.html"
    },
    {
      "question": "A Massachusetts pharmacy stores patient names, Social Security numbers and payment information in an electronic database. The owner assumes HIPAA alone addresses every information-security duty. Which distinction is important?",
      "choices": [
        "Massachusetts 201 CMR 17.00 applies only to veterinarians",
        "A pharmacy is exempt from state security requirements if it has a DEA registration",
        "Only HIPAA's paper privacy notice matters",
        "Massachusetts 201 CMR 17.00 can impose separate written information-security-program duties for personal information about Massachusetts residents"
      ],
      "answer": "D",
      "explanations": [
        "The Massachusetts security regulation is not limited to veterinary practice.",
        "DEA registration does not displace Massachusetts information-security duties.",
        "HIPAA privacy notices do not replace technical and administrative security safeguards.",
        "Correct. Massachusetts WISP requirements can apply independently of HIPAA."
      ],
      "citation": "201 CMR 17.00 — Massachusetts information security",
      "sourceUrl": "https://www.mass.gov/regulations/201-CMR-1700-standards-for-the-protection-of-personal-information-of-ma-residents"
    },
    {
      "question": "A pharmacy employee sends a patient medication list to the wrong email address. The recipient says they deleted it immediately. What is the appropriate next step?",
      "choices": [
        "Treat the incident as a potential privacy/security event and assess whether breach-notification requirements apply",
        "Assume deletion means no documentation or assessment is necessary",
        "Post the patient's diagnosis on social media to warn them",
        "Automatically delete the pharmacy's entire patient database"
      ],
      "answer": "A",
      "explanations": [
        "Correct. An impermissible disclosure requires assessment; mitigation may affect the breach risk evaluation but does not eliminate the need to assess.",
        "Deletion by the recipient does not automatically resolve all HIPAA duties.",
        "Public posting would create another unauthorized disclosure.",
        "Deleting unrelated records is not an appropriate incident response."
      ],
      "citation": "HHS — Breach Notification Rule",
      "sourceUrl": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html"
    },
    {
      "question": "A pharmacy staff member tells a neighbor that a patient recently received an HIV-prevention prescription. The neighbor is not involved in the patient's care. What is the central problem?",
      "choices": [
        "The disclosure is permitted because the drug is Schedule VI",
        "The disclosure is a non-treatment disclosure of potentially identifiable protected information without a permissible basis",
        "HIPAA applies only to hospitalized patients",
        "Patient privacy does not apply to HIV-prevention medication"
      ],
      "answer": "B",
      "explanations": [
        "Drug schedule does not determine whether the disclosure is permissible.",
        "Correct. Disclosure to an uninvolved neighbor without a valid basis can violate HIPAA and relevant state privacy laws.",
        "Pharmacy patient information is protected even in outpatient settings.",
        "Sensitive medication history remains protected patient information."
      ],
      "citation": "45 CFR 164.502 — uses and disclosures",
      "sourceUrl": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-164.502"
    }
  ],
  "vaccination-administration": [
    {
      "question": "A pharmacy technician trainee completes a vaccination course and asks to administer influenza vaccine under Massachusetts Board Policy 2023-02. What is the correct response?",
      "choices": [
        "Yes, any trainee can vaccinate after watching one injection",
        "Yes, if a pharmacist signs the vaccine label",
        "No. The state policy authorizes appropriately qualified licensed technicians, not technician trainees, to administer vaccines",
        "No pharmacy personnel may ever administer influenza vaccine"
      ],
      "answer": "C",
      "explanations": [
        "Training alone does not grant the trainee the policy's licensed-technician authority.",
        "A pharmacist signature cannot substitute for the required personnel qualification.",
        "Correct. The state policy distinguishes licensed technicians from trainees for vaccination administration.",
        "Qualified pharmacists, interns and certain technicians may vaccinate under applicable rules."
      ],
      "citation": "Board Policy 2023-02 — technician qualifications",
      "sourceUrl": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download"
    },
    {
      "question": "A pharmacist plans to administer a routine vaccine under the ordinary Massachusetts state pharmacy authorization pathway to a patient aged four. What age distinction must be considered?",
      "choices": [
        "The ordinary state policy generally uses age five as its minimum, while a separate federal PREP Act pathway may have different age conditions",
        "All vaccines at pharmacies have an unconditional minimum age of 18",
        "The age limit depends only on whether the patient has insurance",
        "Any child aged two may receive any vaccine from any pharmacy employee"
      ],
      "answer": "A",
      "explanations": [
        "Correct. The state policy generally uses age five; separate federal PREP Act authority must be evaluated on its own terms.",
        "The ordinary state pathway is not universally restricted to adults.",
        "Insurance does not establish vaccination scope of practice.",
        "Personnel, vaccine type, patient age and applicable legal authority all matter."
      ],
      "citation": "Board Policy 2023-02 — age and scope",
      "sourceUrl": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download"
    },
    {
      "question": "A licensed Massachusetts pharmacy technician is not nationally certified but wants to administer eligible vaccines under Board Policy 2023-02. What alternative qualification is relevant?",
      "choices": [
        "No alternative exists; national certification is mandatory in every case",
        "Any pharmacy cashier experience is enough",
        "The technician may vaccinate without documented experience",
        "The technician may qualify through the policy's specified 500-hour experience route, together with other required training and safeguards"
      ],
      "answer": "D",
      "explanations": [
        "The policy recognizes an experience-based alternative.",
        "Cashier experience alone is not the policy's qualification standard.",
        "Documented training and experience conditions remain applicable.",
        "Correct. The policy provides a 500-hour route for eligible licensed technicians, with additional requirements."
      ],
      "citation": "Board Policy 2023-02 — technician qualification",
      "sourceUrl": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download"
    },
    {
      "question": "Before a pharmacist administers a vaccine covered by the federal VIS requirement, the patient asks whether the Vaccine Information Statement may be provided after injection. What is correct?",
      "choices": [
        "VIS is optional for every vaccine given at a pharmacy",
        "The current VIS must be given before each covered vaccine dose, as required by federal law",
        "VIS may be withheld whenever the pharmacist has a standing order",
        "VIS is the same as a prescription medication guide"
      ],
      "answer": "B",
      "explanations": [
        "VIS distribution is required for vaccines covered by the federal law.",
        "Correct. The required current VIS must be given before administration of each covered dose.",
        "Standing orders do not remove the VIS duty.",
        "VIS and FDA Medication Guides are distinct documents."
      ],
      "citation": "CDC — Vaccine Information Statement instructions",
      "sourceUrl": "https://www.cdc.gov/vaccines/hcp/about-vis/instructions.html"
    },
    {
      "question": "A Massachusetts pharmacy administers an eligible vaccine and a patient objects to data sharing through MIIS. What is the best approach?",
      "choices": [
        "Skip all MIIS reporting because the patient objects",
        "Destroy the vaccination record to protect confidentiality",
        "Follow MIIS reporting requirements and process the patient's objection using the applicable opt-out procedures",
        "Report only the vaccine lot number and no patient information"
      ],
      "answer": "C",
      "explanations": [
        "An objection does not automatically eliminate required reporting.",
        "Pharmacy vaccination records must be maintained as required.",
        "Correct. Massachusetts has MIIS reporting duties and a distinct objection/opt-out mechanism.",
        "MIIS reporting requirements are not satisfied by arbitrarily omitting required data."
      ],
      "citation": "105 CMR 222 — MIIS reporting and objection",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download"
    },
    {
      "question": "A pharmacy intern has completed an approved immunization training program and wants to administer a vaccine under direct pharmacist supervision. Which principle is correct?",
      "choices": [
        "An appropriately qualified licensed intern may administer eligible vaccines under the applicable Massachusetts policy and supervision requirements",
        "Interns are always prohibited from vaccine administration regardless of training",
        "Any intern may vaccinate independently without supervision",
        "A pharmacy technician trainee may automatically act as the intern's supervising pharmacist"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Massachusetts recognizes qualified interns under the applicable vaccination authorization and supervision requirements.",
        "The policy does not impose a universal ban on trained interns.",
        "The required supervision cannot be waived by the intern.",
        "A technician trainee cannot serve as the supervising pharmacist."
      ],
      "citation": "Board Policy 2023-02 — intern administration",
      "sourceUrl": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download"
    },
    {
      "question": "A pharmacist administers a qualifying nonvaccine injectable medication under Massachusetts Circular Letter DCP 26-03-124. Which patient age is within the ordinary authorized range?",
      "choices": [
        "Age 12",
        "Age 16",
        "Age 17",
        "Age 18 or older, assuming the medication and all other requirements qualify"
      ],
      "answer": "D",
      "explanations": [
        "The circular's ordinary minimum age is higher.",
        "The circular does not establish an age-16 general pathway.",
        "Age 17 is below the specified threshold.",
        "Correct. DCP 26-03-124 authorizes eligible administration to patients aged 18 or older."
      ],
      "citation": "DCP 26-03-124 — pharmacist administration of medications",
      "sourceUrl": "https://www.mass.gov/news/circular-letter-dcp-26-03-124-pharmacist-administration-of-medications"
    },
    {
      "question": "A pharmacist plans to administer a medication intravenously under DCP 26-03-124 because the prescriber wrote 'for pharmacist administration.' Is this authorized by that circular?",
      "choices": [
        "Yes. A prescriber notation permits any route",
        "No. The circular does not authorize IV administration under its pharmacist/intern medication-administration pathway",
        "Yes, but only if the pharmacist has a PharmD",
        "Yes, if the medication is not a controlled substance"
      ],
      "answer": "B",
      "explanations": [
        "A prescriber notation cannot expand the circular's authorized routes.",
        "Correct. The circular's authority excludes intravenous administration.",
        "Education does not override the route restriction.",
        "The route restriction is not waived by a drug's controlled status."
      ],
      "citation": "DCP 26-03-124 — route restrictions",
      "sourceUrl": "https://www.mass.gov/news/circular-letter-dcp-26-03-124-pharmacist-administration-of-medications"
    },
    {
      "question": "A pharmacy administers a routine vaccine to an adult. The pharmacist wants to delay entering the event into MIIS for two weeks. What is the usual Massachusetts reporting deadline?",
      "choices": [
        "Within 72 hours after administration, subject to specific regulatory exceptions",
        "Only at the end of the calendar year",
        "Within 90 days after the patient's next visit",
        "Reporting is never required for pharmacy-administered vaccines"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Massachusetts MIIS regulations generally require reporting within 72 hours.",
        "An annual report does not replace the standard event deadline.",
        "The next patient visit is not the reporting clock.",
        "Pharmacy vaccine administration is generally subject to MIIS reporting."
      ],
      "citation": "105 CMR 222 — 72-hour reporting",
      "sourceUrl": "https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download"
    },
    {
      "question": "A pharmacist gives an eligible vaccine, then discovers the vaccine was stored outside the recommended temperature range. What is the appropriate general response?",
      "choices": [
        "Assume the dose is effective because the patient already received it",
        "Hide the excursion if no immediate adverse reaction occurs",
        "Assess the storage excursion under vaccine-handling guidance, document and take required clinical and reporting steps",
        "Administer a second dose immediately without reviewing product-specific guidance"
      ],
      "answer": "C",
      "explanations": [
        "Administration does not establish that storage conditions preserved potency.",
        "Failure to disclose and investigate undermines patient safety.",
        "Correct. Evaluate the excursion and the need for patient follow-up using current vaccine and manufacturer guidance.",
        "Revaccination decisions require evaluation; immediate automatic repeat dosing may be inappropriate."
      ],
      "citation": "CDC — Vaccine Storage and Handling Toolkit",
      "sourceUrl": "https://www.cdc.gov/vaccines/hcp/storage-handling/index.html"
    }
  ]
});

/* Hand-authored moderate and hard cases for Chapter 09. Source review: 2026-11-11; independent audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "pmp-oud": {
    "moderate": [
      {
        "question": "A Massachusetts prescriber issues a benzodiazepine prescription and a technician says checking MassPAT is only the pharmacist's job after dispensing. What distinction is legally correct?",
        "choices": [
          "The prescriber has a mandatory pre-issuance MassPAT query duty for benzodiazepines unless an exception applies; pharmacy reporting after dispensing is different",
          "Only pharmacies may query MassPAT and the prescriber may not use it",
          "Schedule IV benzodiazepines are never involved in mandatory querying",
          "The prescriber may substitute a pharmacy claim receipt for the PMP query"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Pre-prescribing query and post-dispensing reporting are distinct duties under Massachusetts law.",
          "Registered prescribers have their own PMP querying duties.",
          "DPH has specifically designated benzodiazepines for mandatory PMP checks, subject to exceptions.",
          "An insurance receipt does not fulfill a PMP query."
        ],
        "citation": "105 CMR 700.012(G); DPH benzodiazepine PMP notice",
        "sourceUrl": "https://www.mass.gov/new-mandate-notice/pmp-utilization-for-benzodiazepines"
      },
      {
        "question": "A pharmacist dispenses gabapentin under a lawful Schedule VI prescription. The pharmacy reports only federally scheduled drugs. What must change?",
        "choices": [
          "No change is necessary because gabapentin is not federally scheduled",
          "Classify gabapentin as federal Schedule II before dispensing",
          "Report gabapentin to the Massachusetts PMP as an Additional Drug despite its Schedule VI status",
          "Submit gabapentin only if the patient also takes oxycodone"
        ],
        "answer": "C",
        "explanations": [
          "Massachusetts requires reporting of designated Additional Drugs.",
          "The MA designation does not alter federal scheduling.",
          "Correct. Gabapentin is a Schedule VI drug required to be reported to MA's PMP.",
          "Concurrent opioid treatment is not a condition for gabapentin reporting."
        ],
        "citation": "DCP PMP Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "During a reporting period an MA pharmacy dispenses no Schedule II–V drugs or gabapentin. There is no approved zero-report waiver. What must be submitted?",
        "choices": [
          "A fictional prescription with quantity zero",
          "A Zero Report for the period instead of no submission",
          "Only a single report at the end of the calendar year",
          "The prescriber's name as the patient name"
        ],
        "answer": "B",
        "explanations": [
          "A Zero Report is not a fictitious dispensing event.",
          "Correct. The DCP submission guide requires zero reporting when there are no reportable dispensings and no waiver.",
          "Routine PMP reporting is not an annual-only duty.",
          "Inaccurate patient data is not a valid zero-report substitute."
        ],
        "citation": "DCP PMP Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "A pharmacy dispenses a reportable Schedule III drug on Tuesday. Its data clerk proposes submitting PMP records at the end of the month. What is required?",
        "choices": [
          "Monthly submissions are always enough for community pharmacies",
          "Reporting may wait until the prescriber's DEA renewal",
          "Submitting is unnecessary when the patient picks up in person",
          "Follow the DCP 24-hour or next-business-day transmission requirements instead of waiting until month end"
        ],
        "answer": "D",
        "explanations": [
          "The state's reporting deadline is more frequent than monthly.",
          "DEA renewal timing is not the PMP dispensing-reporting deadline.",
          "An ordinary qualifying pickup is reportable.",
          "Correct. MA's dispenser guide uses a 24-hour/next-business-day standard."
        ],
        "citation": "DCP PMP Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "A patient collecting a Schedule IV drug lacks government-issued ID. The MA pharmacist reasonably concludes that withholding the drug would cause serious hardship. Which route can qualify?",
        "choices": [
          "Document the hardship and obtain the patient's or agent's printed name, address, and signature in the appropriate record",
          "Dispense without ID or any additional documentation",
          "Ask the patient to promise to bring ID next year and discard the record",
          "Change the drug to Schedule VI to avoid the rule"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 9.04(14)(c) permits a narrow hardship exception with documentation and a signed record.",
          "Serious hardship does not waive the documentation conditions.",
          "A future promise alone does not satisfy the regulation.",
          "Changing a drug's schedule is not within pharmacist authority."
        ],
        "citation": "247 CMR 9.04(14)(a)–(d)",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A Massachusetts pharmacy reports naloxone dispensings through daily PMP submissions. A technician expects those records to appear in every patient's prescription-monitoring profile. What is correct?",
        "choices": [
          "Daily submission is unlawful because naloxone is not Schedule II",
          "Each naloxone kit must be coded as methadone",
          "Daily reporting is preferred, but naloxone data are collected without appearing on the patient's PMP profile",
          "All naloxone dispensing must instead be submitted on DEA Form 222"
        ],
        "answer": "C",
        "explanations": [
          "MA Board policy explicitly permits daily naloxone PMP reports.",
          "Mislabeling naloxone as methadone would be inaccurate.",
          "Correct. Naloxone data submitted to the PMP are for reporting only, not patient-profile display.",
          "DEA Form 222 is not a naloxone dispensing report."
        ],
        "citation": "Board Policy 2024-01, revised 2025, §§I–II",
        "sourceUrl": "https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download"
      },
      {
        "question": "A Massachusetts pharmacy dispenses a valid oxycodone Schedule II prescription. The patient says the physician discussed risks and asks to skip any naloxone discussion. What separate duty applies to the pharmacist?",
        "choices": [
          "The patient must purchase naloxone for the opioid fill to be legal",
          "The pharmacist must inform the patient of opioid risks and offer an opioid antagonist, without requiring its purchase",
          "The pharmacist must authorize a refill if naloxone is declined",
          "The offer is required only after a previous overdose"
        ],
        "answer": "B",
        "explanations": [
          "The statute requires an offer, not mandatory acceptance.",
          "Correct. c.94C §18D imposes a pharmacist duty for Schedule II opioid dispensing.",
          "Schedule II refills are prohibited.",
          "The statutory offer is not limited to patients with prior overdose."
        ],
        "citation": "M.G.L. c.94C §18D(b)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18D"
      },
      {
        "question": "A prescriber writes an adult's ordinary first outpatient opiate prescription for ten days of uncomplicated pain treatment, with no documented statutory exception. Which rule matters?",
        "choices": [
          "All first opioid prescriptions have an unrestricted 30-day limit",
          "An adult's first outpatient opioid prescription is exempt from every time limit",
          "Only Schedule III opioids are subject to the limit",
          "MA generally caps an adult's first outpatient opiate prescription at seven days unless a qualifying exception is documented"
        ],
        "answer": "D",
        "explanations": [
          "The initial-outpatient seven-day rule is distinct from the usual 30-day single-fill maximum.",
          "The adult first-opiate limit is an explicit statutory rule.",
          "The rule concerns opiates and is not restricted to Schedule III.",
          "Correct. M.G.L. c.94C §19D(a)–(b) establishes seven days and enumerated exceptions."
        ],
        "citation": "M.G.L. c.94C §19D(a)–(c)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D"
      },
      {
        "question": "A practitioner with appropriate DEA registration and state prescribing authority treats OUD with buprenorphine. The prescription does not show a historical X-waiver number. What is the federal assessment?",
        "choices": [
          "An X-waiver number is no longer required for qualified buprenorphine treatment, although all other prescribing requirements still apply",
          "Every buprenorphine prescription must contain an X-number",
          "Only OTPs may dispense prescriptions for office-based buprenorphine therapy",
          "The prescription is automatically treated as OTC"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The federal DATA/X-waiver requirement was eliminated, without eliminating practitioner authority and prescription-validity requirements.",
          "The old X-number is no longer federally required.",
          "Qualified office-based buprenorphine OUD prescribing is allowed.",
          "Buprenorphine is still controlled."
        ],
        "citation": "DEA Buprenorphine MOUD Q&A; CAA 2023 §1262",
        "sourceUrl": "https://www.deadiversion.usdoj.gov/faq/buprenorphine-faq.html"
      },
      {
        "question": "A community pharmacy receives an ordinary prescription for methadone tablets solely for OUD maintenance, unrelated to an authorized OTP or other lawful pathway. What distinction controls?",
        "choices": [
          "Every community prescriber may issue an ordinary maintenance prescription for methadone",
          "Methadone prescriptions for pain and methadone OUD maintenance are legally identical",
          "Schedule II methadone maintenance generally follows the regulated OTP pathway rather than ordinary retail prescribing, with narrow exceptions",
          "Co-prescribed alprazolam makes the prescription valid"
        ],
        "answer": "C",
        "explanations": [
          "Schedule II methadone maintenance is subject to special federal restrictions.",
          "Pain treatment and OUD maintenance have distinct legal pathways.",
          "Correct. §1306.07(a) requires OTP registration for maintenance/detox dispensing absent a separate exception.",
          "Co-prescribed controlled drugs do not create OTP authority."
        ],
        "citation": "21 CFR §1306.07(a)–(d)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.07"
      }
    ],
    "hard": [
      {
        "question": "A hospital administers an opioid to an admitted inpatient under a medication order. At discharge, the hospital's outpatient pharmacy fills a separate Schedule II prescription for home use. How should these events be treated for MA PMP reporting?",
        "choices": [
          "Report the inpatient administration as an ordinary retail prescription",
          "Ignore the outpatient dispensing because the hospital treated the patient earlier",
          "Both inpatient medication orders and retail discharge fills are exempt",
          "The inpatient medication order and outpatient dispensing are distinct; report the outpatient prescription dispensing as required"
        ],
        "answer": "D",
        "explanations": [
          "MA's inpatient medication-order exception is not equivalent to outpatient retail dispensing.",
          "A discharge prescription is a separate reportable transaction.",
          "Hospital location alone does not exempt its outpatient prescription dispensing.",
          "Correct. §24A(b) and 105 CMR 700.012 distinguish inpatient medication orders from outpatient dispensing."
        ],
        "citation": "M.G.L. c.94C §24A(b)–(d); 105 CMR 700.012(A)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section24A"
      },
      {
        "question": "A patient takes alprazolam and receives a new outpatient oxycodone prescription. The pharmacist says the prescriber's MassPAT query means no other legal duties remain at the pharmacy. Which response is best?",
        "choices": [
          "Only prescribers have responsibilities after consulting MassPAT",
          "The prescriber's PMP query, the pharmacy's reporting of opioid dispensing, and the pharmacist's Schedule II opioid risk/antagonist offer are separate responsibilities",
          "Marking 'MassPAT checked' automatically cancels the pharmacist's naloxone offer",
          "Checking PMP authorizes two Schedule II refills"
        ],
        "answer": "B",
        "explanations": [
          "Both pharmacies and prescribers have distinct legal duties.",
          "Correct. Query, reporting, and the pharmacist risk/antagonist offer should not be conflated.",
          "The pharmacist's duty under §18D is independent of the prescriber's query.",
          "Schedule II refills are prohibited regardless of a PMP query."
        ],
        "citation": "M.G.L. c.94C §18D(b)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18D"
      },
      {
        "question": "An MA pharmacy fills three gabapentin prescriptions but no federally scheduled II–V prescriptions during the reporting period. The reporting software proposes a Zero Report. What is correct?",
        "choices": [
          "The gabapentin dispensings must be reported; a Zero Report is not appropriate because reportable Additional Drug activity occurred",
          "Gabapentin must be reclassified as federal Schedule V before a report can be sent",
          "No PMP report is required unless oxycodone was dispensed",
          "A single fictitious Schedule II report can replace the three gabapentin reports"
        ],
        "answer": "A",
        "explanations": [
          "Correct. MA requires gabapentin submissions even though it is Schedule VI.",
          "Massachusetts' additional-drug designation does not affect federal scheduling.",
          "Opioids are not required for gabapentin to be reportable.",
          "Reporting fictitious claims is not a lawful substitute."
        ],
        "citation": "MA DCP Pharmacy Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "A pharmacy sends Schedule II dispensing transactions to the MassPAT clearinghouse on time. The next week two entries are listed as rejected due to invalid required data. How should the pharmacy respond?",
        "choices": [
          "No action; uploading a file is the entire reporting requirement",
          "Replace rejected items with a Zero Report",
          "Correct the rejected records and resubmit them rather than treating an attempted upload as completed reporting",
          "Ask the prescriber to classify the medication as OTC"
        ],
        "answer": "C",
        "explanations": [
          "An unsuccessful submission is not an accepted dispensing report.",
          "A Zero Report is only appropriate when there are no reportable dispensings.",
          "Correct. DCP guidance requires correction and resubmission of rejected reports.",
          "Controlled-substance status cannot be changed to fix data submission errors."
        ],
        "citation": "MA DCP Pharmacy Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "A New Hampshire pharmacy is authorized to mail a patient's Schedule IV medication to the patient's Massachusetts home. Its manager claims Massachusetts PMP rules apply only to pharmacies physically in Massachusetts. What is correct?",
        "choices": [
          "Only the New Hampshire prescriber reports it, never the pharmacy",
          "An MA delivery is reportable only if it is fentanyl",
          "Reporting is the customer's responsibility",
          "MA PMP reporting extends to qualifying out-of-state pharmacies delivering reportable controlled substances to Massachusetts recipients"
        ],
        "answer": "D",
        "explanations": [
          "Dispensers have an independent reporting duty.",
          "MA reporting extends to Schedule II–V and certain additional drugs, not fentanyl alone.",
          "The patient is not the required pharmacy reporter.",
          "Correct. The DCP and 105 CMR 700.012 apply to covered out-of-state dispensers delivering into MA."
        ],
        "citation": "MA DCP Pharmacy Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      },
      {
        "question": "A Massachusetts pharmacy does not use the preferred daily PMP reporting method for naloxone dispensed under the statewide standing order. Which alternative is described by the Board's revised 2024-01 policy?",
        "choices": [
          "Email the annual report of the prior calendar year's dispensed naloxone doses and required metrics by January 15",
          "Do not report naloxone because it is not a Schedule II drug",
          "Report only naloxone kits given with oxycodone",
          "Submit a monthly Schedule II methadone inventory instead"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The Board policy specifies a January 15 annual report if daily PMP naloxone reporting is not used.",
          "Naloxone has a separate reporting requirement.",
          "Standalone naloxone dispensing is also within the required reporting scope.",
          "An unrelated DEA controlled-drug inventory is not a substitute."
        ],
        "citation": "Board Policy 2024-01 (2025 revision), §II",
        "sourceUrl": "https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download"
      },
      {
        "question": "A physician writes an adult patient's first outpatient Schedule II opioid prescription for cancer pain, covering 14 days. The physician documents why treatment beyond seven days is necessary and why a non-opiate alternative is inappropriate. No other restriction applies. Which analysis is correct?",
        "choices": [
          "The first-outpatient seven-day statute has absolutely no exceptions",
          "The documented cancer-pain exception may allow more than seven days, but all other prescription validity and Schedule II restrictions still apply",
          "The exception creates two automatic refills",
          "Using the drug for cancer pain reclassifies it as Schedule III"
        ],
        "answer": "B",
        "explanations": [
          "c.94C §19D(b) has an explicit exception for qualifying documented cancer pain.",
          "Correct. The exception to the seven-day limitation does not waive other controlled-prescription rules.",
          "Schedule II refills remain prohibited.",
          "An indication does not change federal scheduling."
        ],
        "citation": "M.G.L. c.94C §19D(a)–(c)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D"
      },
      {
        "question": "An emergency department practitioner who is not an opioid treatment program needs to bridge one patient's OUD treatment while arranging a referral. Which action is within federal §1306.07(b), assuming other law permits it?",
        "choices": [
          "Write an unlimited take-home methadone maintenance prescription",
          "Start an indefinitely renewable outpatient methadone regimen",
          "Directly dispense, rather than prescribe, up to a three-day emergency supply at one time without renewal or extension",
          "Waive all other controlled-substance registration requirements"
        ],
        "answer": "C",
        "explanations": [
          "The emergency rule is for direct dispensing, not unrestricted maintenance prescribing.",
          "The emergency treatment may not be renewed or extended.",
          "Correct. The three-day rule permits a short direct-dispensing bridge to treatment referral.",
          "Other state and federal requirements remain applicable."
        ],
        "citation": "21 CFR §1306.07(b)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.07"
      },
      {
        "question": "A pharmacist knows a patient has an active voluntary non-opiate directive and has not revoked it. The pharmacy receives a standard outpatient oxycodone prescription that conflicts with the directive. What is the key §18B legal issue?",
        "choices": [
          "An outpatient prescription always overrides a known directive",
          "The pharmacy may erase the directive without obtaining valid revocation",
          "The pharmacist may replace oxycodone with another prescribed drug without authorization",
          "The usual outpatient-prescription presumption is not a safe harbor for knowingly dispensing contrary to an active directive"
        ],
        "answer": "D",
        "explanations": [
          "§18B(c) limits the presumption when the pharmacist knowingly acts contrary to the directive.",
          "Revocation has its own process; a pharmacist may not arbitrarily erase the directive.",
          "Drug substitution does not cure the conflict with no prescriber authorization.",
          "Correct. The statute explicitly distinguishes knowing action against a directive."
        ],
        "citation": "M.G.L. c.94C §18B(c)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18B"
      },
      {
        "question": "A Massachusetts pharmacy is closed on a holiday and dispenses no reportable medications. A technician assumes an automatic Zero Report waiver applies to every closed day. What should the manager check?",
        "choices": [
          "Whether another pharmacy can enter a fabricated transaction for that day",
          "Whether the pharmacy has a waiver covering closed days; absent an applicable waiver, follow the DCP Zero Report requirement",
          "Whether naloxone became federal Schedule V on the holiday",
          "Whether the physician's office is also closed"
        ],
        "answer": "B",
        "explanations": [
          "Inventing transactions is not an acceptable reporting substitute.",
          "Correct. The dispenser guide allows applying for a closed-day waiver; closure is not itself proof one exists.",
          "Naloxone scheduling is unrelated to a waiver for zero reporting.",
          "Prescriber office closure does not determine a pharmacy's reporting status."
        ],
        "citation": "MA DCP Pharmacy Reporting and Data Submission; Dispenser Guide v5.2",
        "sourceUrl": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      }
    ]
  }
});

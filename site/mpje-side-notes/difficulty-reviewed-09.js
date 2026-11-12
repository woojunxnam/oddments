/* Chapter 9 initial moderate cases; hard tier appended in follow-up commit. */
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
    ]
  }
});

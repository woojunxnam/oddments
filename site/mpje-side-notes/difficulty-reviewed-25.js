/* Original Massachusetts MPJE Chapter 25: reporting clocks and record retention, 10 moderate + 10 hard application cases. Official source author review 2026-11-12; independent legal audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "numbers-records": {
    "moderate": [
      {
        "question": "At 10:00 a.m. Monday, an MA pharmacist is told that a wrong-drug prescription reached the patient, who has not reported injury. The store intends to finish a root-cause review next month. What is the first CQI timeline?",
        "choices": [
          "Wait until the monthly CQI meeting before contacting the patient",
          "File a serious-injury Board report automatically even with no evidence of injury",
          "Provide immediate appropriate notification and mitigation, and document the QRE initially within 24 hours after the pharmacist learned of it",
          "Keep the matter undocumented unless a prescriber files a complaint"
        ],
        "answer": "C",
        "explanations": [
          "247 CMR 15.03 calls for prompt patient safety action.",
          "Serious injury/death has a separate Board reporting trigger; not every QRE is that category.",
          "Correct. MA requires immediate patient-related steps and initial QRE documentation within 24 hours.",
          "QRE documentation is not conditional on a complaint."
        ],
        "citation": "247 CMR 15.03(1)–(3) — Quality-Related Event Notification and Documentation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"
      },
      {
        "question": "A pharmacy analyzes an ordinary Quality-Related Event under its CQI program and intends to delete the file 13 months after the QRE report. What is the minimum Massachusetts record period?",
        "choices": [
          "At least two years from the date of the QRE report, with records in an orderly and retrievable form",
          "One year from the patient complaint",
          "At least 30 days after the next refill",
          "Exactly six months because CQI is internal"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 15.04(2) requires records of QREs for at least two years from the report date.",
          "A one-year period is too short.",
          "Prescription refill timing is unrelated to CQI retention.",
          "Internal quality status does not remove the state retention duty."
        ],
        "citation": "247 CMR 15.04 — CQI Records Retained at Least Two Years",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"
      },
      {
        "question": "A Massachusetts pharmacy manager discovers on Tuesday that a previous dispensing error caused a patient's serious injury. What Board reporting clock applies to that discovery, independent of ordinary CQI records?",
        "choices": [
          "Only the federal DEA one-business-day theft deadline",
          "Within seven business days after discovery of serious injury or death related to improper dispensing",
          "The first business day after the pharmacy's next annual inspection",
          "Within 60 days after the patient signs a liability release"
        ],
        "answer": "B",
        "explanations": [
          "DEA theft reporting is a different type of event.",
          "Correct. 247 CMR 20.02(1) uses seven business days after discovering serious injury/death caused by improper dispensing.",
          "Annual inspections do not start the serious-injury report clock.",
          "Patient settlement paperwork does not replace Board notification."
        ],
        "citation": "247 CMR 20.02(1)–(5) — Serious Improper Dispensing and Adverse Drug Events",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
      },
      {
        "question": "A pharmacy reports to the Massachusetts Board a serious adverse drug event related to a drug compounded at that pharmacy. The report is filed November 12. Which record-retention rule applies?",
        "choices": [
          "Discard the incident file after two years because it is a QRE",
          "Keep it only until the adverse event resolves",
          "Keep every medical record for exactly 15 years under HIPAA",
          "Retain the serious event records for at least five years from the date the report was filed with the Board"
        ],
        "answer": "D",
        "explanations": [
          "The event has a distinct §20.02 retention requirement in addition to CQI.",
          "Event resolution does not stop the retention rule.",
          "HIPAA does not set a universal 15-year medical-record rule.",
          "Correct. 247 CMR 20.02(4) measures five years from Board report filing."
        ],
        "citation": "247 CMR 20.02(1)–(5) — Serious Improper Dispensing and Adverse Drug Events",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
      },
      {
        "question": "A licensed MA pharmacy learns that a compounded sterile product it previously dispensed may contain a defective ingredient. It has unopened units in stock and affected units at several hospitals. What should happen immediately?",
        "choices": [
          "Initiate the required recall, segregate remaining stock and start appropriate tracing and notification, without postponing action until every test result is definitive",
          "Keep dispensing until the Board assigns a recall class",
          "Wait seven days before taking inventory action",
          "Sell the remainder at a discount if the hospital agrees"
        ],
        "answer": "A",
        "explanations": [
          "Correct. c.112 §39D(e) mandates immediate recall when a compounded preparation is or may be defective.",
          "An FDA classification is not a prerequisite for immediate protective action.",
          "The seven-day log obligation does not postpone recall.",
          "Discounting a potentially defective preparation is not a lawful risk control."
        ],
        "citation": "M.G.L. c.112 §39D(e) — Recall and Defective Drug Preparation Log",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D"
      },
      {
        "question": "A Massachusetts sterile compounding facility receives a laboratory report showing an action-level environmental monitoring result on Thursday. It proposes filing a Board notice after seven calendar days because that is the defective-compound deadline. Which deadline instead applies to the EM result?",
        "choices": [
          "Any EM action-level result is exempt from Board notice",
          "Report an action-level microbiological result to the Board within one business day after receiving the microbiology report, as required by Policy 2026-03",
          "Report only after two years of negative follow-up samples",
          "Report solely to the product's wholesaler within 15 calendar days"
        ],
        "answer": "B",
        "explanations": [
          "The current MA environmental policy imposes a separate clock.",
          "Correct. Policy 2026-03 triggers the one-business-day reporting period on receipt of the microbiology report.",
          "Future samples do not remove the initial report deadline.",
          "The wholesaler is not a substitute for the Board's environmental-monitoring notice."
        ],
        "citation": "MA Board Policy 2026-03 — Action-Level Environmental Monitoring Results",
        "sourceUrl": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download"
      },
      {
        "question": "A federally registered pharmacy discovers a confirmed theft of oxycodone and sends its DEA Form 106 after 20 days, but made no other DEA report. Which independent federal step was missed?",
        "choices": [
          "DEA requires only a six-month stock summary after theft",
          "The pharmacy must send its 503B product list in June",
          "DEA must receive the initial written notice within one business day of discovery, separate from the later Form 106 deadline",
          "No federal report is due unless the thief is identified"
        ],
        "answer": "C",
        "explanations": [
          "The initial DEA theft/significant-loss notice has a short deadline.",
          "503B product reporting concerns outsourcing facilities, not theft reporting.",
          "Correct. 21 CFR 1301.76(b) requires initial written notification within one business day; Form 106 follows within 45 days.",
          "Identifying the suspect is not a prerequisite for federal reporting."
        ],
        "citation": "21 CFR §1301.76(b) — Theft and Significant Loss Notice / Form 106",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.76"
      },
      {
        "question": "An MA pharmacist suspects a received drug might be counterfeit and quarantines it, but has not yet determined it is illegitimate. Which federal 24-hour reporting trigger should be distinguished?",
        "choices": [
          "Every initial suspicion must always be reported as a confirmed illegitimate product within one minute",
          "The product becomes eligible for sale again automatically after 24 hours",
          "Only a federal theft report is relevant to drug authenticity",
          "The DSCSA notification clock starts when the trading partner determines the product is illegitimate; suspect-product quarantine and investigation occur earlier"
        ],
        "answer": "D",
        "explanations": [
          "Suspect and illegitimate are distinct defined DSCSA stages.",
          "Elapsed time alone does not authenticate a package.",
          "DEA loss rules are different from FDA counterfeit-product reporting.",
          "Correct. FDA requires notification within 24 hours after an illegitimate-product determination."
        ],
        "citation": "FDA — Notify FDA of Illegitimate Products Within 24 Hours",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
      },
      {
        "question": "A Massachusetts nuclear pharmacy keeps ordinary acquisition and disposition records for only 24 months, reasoning that federal DEA stock records are often two years. Which nuclear-specific minimum matters?",
        "choices": [
          "Retain the relevant radiopharmaceutical acquisition and disposition records for at least three years under 247 CMR 13.05",
          "Keep all nuclear records only until radioactive decay is complete",
          "Retain the records for only 30 days unless a patient requests access",
          "A nuclear pharmacy is exempt from any state acquisition records"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Massachusetts's enacted nuclear pharmacy rule sets a distinct three-year minimum.",
          "Physical radioactive decay does not eliminate transaction documentation.",
          "Thirty days is not the specific nuclear retention requirement.",
          "Nuclear dispensing remains subject to acquisition and disposition accountability."
        ],
        "citation": "247 CMR 13.05(5) — Nuclear Pharmacy Acquisition/Disposition Records",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-13-registration-requirements-and-minimal-professional-standards-for-nuclear-pharmacies/download"
      },
      {
        "question": "A Massachusetts drug store maintains a camera recording of ordinary pharmacy activity for ten days and deletes it automatically. No theft or diversion is known or suspected. What is the state minimum for routine security video?",
        "choices": [
          "Ten days is the universal required minimum",
          "At least fourteen days for ordinary video, with a longer two-year rule for known or suspected theft/diversion footage",
          "Every video must be preserved for exactly six years regardless of content",
          "The rule applies only to Schedule VI products"
        ],
        "answer": "B",
        "explanations": [
          "Ten days is below the ordinary 14-day requirement.",
          "Correct. 247 CMR 9.21(4) differentiates 14-day routine retention from the two-year theft/diversion period.",
          "Six years is associated with different federal records, not all pharmacy footage.",
          "Pharmacy controlled-stock security video is not Schedule VI-only."
        ],
        "citation": "247 CMR 9.21(4),(8) — Security Footage and CII Reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      }
    ],
    "hard": [
      {
        "question": "An MA pharmacist discovers a dispensing error Monday at 9 a.m. and immediately contacts the patient; on Thursday a physician confirms the error caused serious injury, and the MOR learns of the confirmation that same day. Which deadlines should be evaluated separately?",
        "choices": [
          "Both events trigger only the 15-calendar-day federal 503B report",
          "The seven-business-day serious-injury Board clock starts on Monday even though the injury was not then known",
          "QRE initial documentation was due within 24 hours of pharmacist discovery Monday; the separate seven-business-day Board clock follows discovery of the related serious injury Thursday",
          "All documentation may wait until a single annual CQI report"
        ],
        "answer": "C",
        "explanations": [
          "503B outsourcing adverse-event reporting is a different rule.",
          "The §20.02 clock is tied to discovery of serious injury/death related to improper dispensing.",
          "Correct. QRE discovery and subsequent injury discovery can create different event-triggered clocks.",
          "Annual review does not suspend either prompt duty."
        ],
        "citation": "247 CMR 20.02(1)–(5) — Serious Improper Dispensing and Adverse Drug Events",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
      },
      {
        "question": "An MA pharmacy knows its compounded sterile drug may be defective and recalls it Monday. Its MOR plans to submit the defective-drug log at the end of the month and discard the log after three years. What should change?",
        "choices": [
          "Immediate recall is correct, but the log must be made available to the Board within seven days of recall and retained for at least ten years",
          "No Board log is needed if affected products were compounded for a hospital",
          "Only a two-year QRE record is required after recall",
          "The pharmacy must wait for a confirmed serious injury before recording a recall"
        ],
        "answer": "A",
        "explanations": [
          "Correct. c.112 §39D(e) imposes immediate recall, seven-day log availability and ten-year defective preparation log retention.",
          "Compounded products distributed to hospitals are within the defined recall reach.",
          "The specific defective-preparation rule is longer than ordinary QRE retention.",
          "Potential defect triggers recall without awaiting patient harm."
        ],
        "citation": "M.G.L. c.112 §39D(e) — Recall and Defective Drug Preparation Log",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D"
      },
      {
        "question": "A Massachusetts pharmacy confirms oxycodone theft on Friday and wants a single report to satisfy all regulators. Which set of clocks is most accurate, assuming federal and state reporting applies?",
        "choices": [
          "All notices are due only after 45 business days",
          "DEA initial written notice within one business day and Form 106 within 45 days, plus the separate Massachusetts Board confirmed-loss report within seven calendar days",
          "Only MassPAT reporting within 24 hours applies",
          "An insurer report replaces the DEA and Board notices"
        ],
        "answer": "B",
        "explanations": [
          "Federal law contains distinct initial and form deadlines.",
          "Correct. Federal §1301.76 and MA Policy 2026-01 have separate recipients and units of time.",
          "MassPAT reports dispensing, not confirmed theft.",
          "Insurance notice does not replace regulatory theft notification."
        ],
        "citation": "21 CFR §1301.76(b) — Theft and Significant Loss Notice / Form 106",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.76"
      },
      {
        "question": "A pharmacy receives serious unexpected adverse-event information on April 3 regarding an earlier drug it compounded as a registered 503B outsourcing facility. It has not compounded anything this year and wants to wait for its June zero-product report. What is wrong?",
        "choices": [
          "No federal event report can be required when recent 503B production is zero",
          "The required reporting period is six years because that is the tracing-record clock",
          "The next June product report is the only federal report for a 503B firm",
          "The serious/unexpected adverse-event Alert report is separately due as soon as possible and within 15 calendar days from initial information receipt"
        ],
        "answer": "D",
        "explanations": [
          "Current production volume does not erase reports involving an earlier 503B product.",
          "Record-retention and adverse-event submission clocks are different.",
          "Periodic compounded-product reporting is distinct from safety event reporting.",
          "Correct. FDA 503B guidance applies the 21 CFR 310.305 15-day Alert reporting requirement."
        ],
        "citation": "FDA — Adverse Event Reports for 503B Outsourcing Facilities",
        "sourceUrl": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adverse-event-reporting-outsourcing-facilities-under-section-503b-federal-food-drug-and-cosmetic-act"
      },
      {
        "question": "A covered pharmacy maintains HIPAA privacy policies and training documents for six years, but the owner believes this proves that every medical record can be destroyed after the same six years. What is the legally correct distinction?",
        "choices": [
          "HIPAA's six-year documentation retention is not a universal patient medical-record destruction deadline; other state and federal pharmacy record requirements may be longer or shorter",
          "All patient prescriptions must be destroyed exactly six years after dispensing",
          "Only DSCSA records can ever be retained for longer than six years",
          "Six years is the minimum for every nuclear pharmacy record regardless of its own regulation"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 45 CFR 164.530(j) addresses specified privacy-rule documentation and does not create a uniform medical-record retention schedule.",
          "Other laws set prescription, controlled and clinical record retention periods.",
          "Several different federal/state laws can impose longer retention for specific matters.",
          "Nuclear pharmacy has a separate three-year minimum for certain records."
        ],
        "citation": "45 CFR 164.530(j) — HIPAA Documentation Retention",
        "sourceUrl": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530"
      },
      {
        "question": "A pharmacy learns of a suspected theft of controlled stock and identifies a security-camera recording relevant to the event. The usual fourteen-day overwriting schedule would erase it tomorrow. Which rule changes the retention period?",
        "choices": [
          "The ordinary fourteen-day storage limit always takes precedence",
          "Any suspected diversion requires keeping the relevant recording for at least two years under 247 CMR 9.21 rather than letting the routine retention overwrite it",
          "Only a manufacturer can preserve camera footage",
          "All camera video becomes a six-year HIPAA document"
        ],
        "answer": "B",
        "explanations": [
          "The state security rule expressly provides a longer period for theft/diversion footage.",
          "Correct. Suspected diversion invokes the two-year preservation requirement for the relevant recording.",
          "The pharmacy retains security-video obligations.",
          "HIPAA documentation retention is a distinct category."
        ],
        "citation": "247 CMR 9.21(4),(8) — Security Footage and CII Reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "An MA sterile compounding pharmacy receives an action-level microbiology report on Wednesday and finds that a defective CSP batch distributed last week may have resulted from the same environmental problem. What distinct duties must be assessed?",
        "choices": [
          "Only the ordinary two-year QRE retention rule applies",
          "An action-level EM notice removes the obligation to recall defective CSPs",
          "Report the action-level result under the one-business-day Policy 2026-03 clock and separately evaluate immediate defective-CSP recall, reporting and log requirements under §39D",
          "All action-level results automatically change the drug's federal schedule"
        ],
        "answer": "C",
        "explanations": [
          "Environmental and defective-product statutes may both apply.",
          "One report does not eliminate another independent product-quality obligation.",
          "Correct. EM notification and defective compounded-drug recall/reporting have separate triggers and timelines.",
          "Drug schedule is unrelated to an environmental-monitoring deviation."
        ],
        "citation": "MA Board Policy 2026-03 — Action-Level Environmental Monitoring Results",
        "sourceUrl": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download"
      },
      {
        "question": "A Massachusetts pharmacy destroys controlled-substance acquisition and dispensing records after two years but keeps all its DSCSA package-level transaction records only one year. Which federal recordkeeping issue should it check?",
        "choices": [
          "DSCSA records and DEA inventory records have the same compulsory one-year limit",
          "Neither DSCSA nor DEA requires documentation after a purchase is complete",
          "Records must be kept only when a drug recall has already occurred",
          "DSCSA tracing records generally must be retained six years, a separate federal period from the DEA minimum for controlled-substance records"
        ],
        "answer": "D",
        "explanations": [
          "Different statutory programs set different retention periods.",
          "Document preservation is not solely contingent on active investigations.",
          "Recalls are not the only DSCSA record-retention trigger.",
          "Correct. DSCSA tracing and investigation records have a six-year requirement independent of DEA recordkeeping."
        ],
        "citation": "FDA — DSCSA Product Tracing Requirements FAQ and Records",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/drug-supply-chain-security-act-product-tracing-requirements-frequently-asked-questions"
      },
      {
        "question": "An MA pharmacy's serious improper-dispensing injury was discovered September 1, but the MOR filed the required Board report September 8. The manager proposes retaining related records for five years from the discovery date rather than from the report date. Which rule applies?",
        "choices": [
          "The five-year §20.02(4) period runs from filing the report with the Board, not the initial discovery date",
          "The records can be destroyed two years after September 1 because CQI overrides Board reporting",
          "The law measures retention from the prescription's original issue date",
          "The patient can verbally waive all required records"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 20.02(4) explicitly measures five years from the Board report filing date.",
          "The serious-injury retention provision is separate from ordinary CQI records.",
          "Prescription issue date is not the specified §20.02 record trigger.",
          "Individual preference cannot waive a statutory pharmacy retention duty."
        ],
        "citation": "247 CMR 20.02(1)–(5) — Serious Improper Dispensing and Adverse Drug Events",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
      },
      {
        "question": "A drug store stores refrigerated vaccines and has automated overnight monitoring, but the temperature excursions and staff actions are erased after six months. A staff member says the six-month interval is enough because no products were lost. What is the relevant Massachusetts record rule?",
        "choices": [
          "No temperature logs need to be kept once the refrigerator returns to the proper range",
          "247 CMR 9.22(4) requires recording out-of-range events and actions taken and retaining the temperature records for at least one year",
          "Only microbiological ISO 5 monitoring records must ever be retained",
          "All refrigerator data are required to be filed with the DEA every 45 days"
        ],
        "answer": "B",
        "explanations": [
          "Temperature logging duties apply even without confirmed spoiled product.",
          "Correct. 247 CMR 9.22 addresses excursion/action documentation and one-year record retention.",
          "Cold-chain logs are separate from sterile cleanroom microbiological monitoring.",
          "DEA 45-day Form 106 deadlines are unrelated to refrigerator logs."
        ],
        "citation": "247 CMR 9.22(4) — Temperature Logs and Excursion Documentation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      }
    ]
  }
});

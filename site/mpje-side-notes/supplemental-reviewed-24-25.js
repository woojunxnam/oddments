/* Manually authored MPJE cases for Chapters 24–25. Reviewed November 11, 2026. */
Object.assign(window.MPJE_SUPPLEMENTAL_VERIFIED || (window.MPJE_SUPPLEMENTAL_VERIFIED = {}), {
  "fda-supply-chain": [
    {
      "question": "A pharmacy company has 24 full-time licensed pharmacists and qualified technicians combined as of November 27, 2026. Which statement about FDA's small-dispenser DSCSA exemption is accurate?",
      "choices": [
        "It exempts the company from all federal pharmacy law",
        "It may qualify for the specified enhanced tracing exemptions through November 27, 2027",
        "It can automatically dispense suspect drugs",
        "It must have fewer than five employees"
      ],
      "answer": "B",
      "explanations": [
        "The exemption is limited to specified DSCSA requirements.",
        "Correct. FDA's August 2026 exemption uses a company-wide threshold of 25 or fewer qualifying full-time staff.",
        "Suspect product safeguards remain applicable.",
        "The FDA threshold is not five employees."
      ],
      "citation": "FDA August 6, 2026 small-dispenser exemption",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
    },
    {
      "question": "A chain has four pharmacy locations, each with 10 full-time qualified pharmacists and technicians, for a company total of 40. Can each store claim the FDA small-dispenser exemption based solely on its own headcount?",
      "choices": [
        "Yes, the threshold applies separately to each store",
        "Yes, if each store has a unique DEA number",
        "No, FDA measures the specified employee count at the company-owner level",
        "No, because only hospitals can qualify"
      ],
      "answer": "C",
      "explanations": [
        "FDA's eligibility calculation is company-wide.",
        "A separate DEA number does not change the company's staffing total.",
        "Correct. The 25-person threshold applies to the company that owns the dispenser.",
        "The exemption is intended for qualifying small dispensers, including community pharmacies."
      ],
      "citation": "FDA DSCSA small-dispenser definition",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
    },
    {
      "question": "A qualifying small dispenser is exempt from specified enhanced electronic tracing requirements. A suspicious package arrives with an apparently altered serial number. What should it do?",
      "choices": [
        "Continue suspect-product investigation and quarantine obligations despite the limited exemption",
        "Dispense it because all DSCSA duties are waived",
        "Delete its trading partner information",
        "Return it to saleable stock without assessment"
      ],
      "answer": "A",
      "explanations": [
        "Correct. The exemption does not eliminate core suspect-product safeguards.",
        "A tracing exemption does not authorize dispensing suspect stock.",
        "Trading-partner records remain important.",
        "Unverified product must not be released without appropriate investigation."
      ],
      "citation": "FDA DSCSA exemptions and suspect-product duties",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
    },
    {
      "question": "A pharmacy has credible evidence that a prescription drug is counterfeit and determines it is illegitimate at noon Monday. When is FDA notification ordinarily required?",
      "choices": [
        "At the next annual inventory",
        "Only after the patient reports harm",
        "Within 30 days",
        "Within 24 hours after determining illegitimacy"
      ],
      "answer": "D",
      "explanations": [
        "Annual inventory is unrelated to the DSCSA notification trigger.",
        "Patient injury is not required for the notification.",
        "The federal notification window is shorter.",
        "Correct. The 24-hour period begins upon determination of illegitimacy."
      ],
      "citation": "FD&C Act §582(d)(4); FDA illegitimate-product notifications",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
    },
    {
      "question": "A shipment has unusual packaging, but the pharmacy has not yet determined whether the product is illegitimate. What distinction is important?",
      "choices": [
        "Any suspicion automatically triggers the illegitimate-product notification deadline",
        "Suspect-product investigation and quarantine precede the separate 24-hour notification triggered by a determination of illegitimacy",
        "The pharmacy may dispense while investigating",
        "Only DEA can decide whether a product is illegitimate"
      ],
      "answer": "B",
      "explanations": [
        "Suspicion and determination are distinct DSCSA events.",
        "Correct. The FDA 24-hour clock attaches to an illegitimate-product determination.",
        "Suspect product should not simply be distributed.",
        "FDA and trading partners have DSCSA roles; DEA does not exclusively decide illegitimacy."
      ],
      "citation": "FDA suspect versus illegitimate product",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
    },
    {
      "question": "A pharmacy receives a product with an NDC listed in FDA's directory. What does that listing prove?",
      "choices": [
        "The product has an approved NDA",
        "The product is automatically interchangeable with every generic",
        "An NDC listing does not by itself establish FDA approval",
        "The product is exempt from recalls"
      ],
      "answer": "C",
      "explanations": [
        "Listing and marketing approval are different processes.",
        "NDC listing does not establish therapeutic equivalence.",
        "Correct. FDA explicitly cautions that NDC listing does not mean the product is FDA approved.",
        "Listed products can be recalled."
      ],
      "citation": "FDA NDC directory and product listing",
      "sourceUrl": "https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-product-file-definitions"
    },
    {
      "question": "FDA announces a Class I recall for a product in a pharmacy's stock. What does Class I signify?",
      "choices": [
        "A reasonable probability of serious adverse health consequences or death",
        "A minor labeling issue with no possible harm",
        "A recall that applies only to devices",
        "A recall initiated only by a pharmacist"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Class I is the most serious FDA recall classification.",
        "Minor or remote-risk issues are not Class I by definition.",
        "Drug recalls can be Class I.",
        "The class describes health hazard, not the initiating professional."
      ],
      "citation": "FDA recall classification definitions",
      "sourceUrl": "https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions"
    },
    {
      "question": "A drug is approved for one indication, but a licensed prescriber orders it for a different clinical indication. Which federal distinction is correct?",
      "choices": [
        "All off-label prescribing is automatically prohibited",
        "Off-label prescribing makes the drug an unapproved compounded product",
        "The pharmacist must report every off-label order as a recall",
        "FDA approval of a drug does not mean every lawful prescriber use must be an FDA-labeled indication"
      ],
      "answer": "D",
      "explanations": [
        "Off-label prescribing is not categorically illegal.",
        "Using an approved drug off-label does not make the product compounded.",
        "A recall is a separate safety action.",
        "Correct. Prescriber-directed off-label use is distinct from FDA approval of marketed indications."
      ],
      "citation": "FDA — understanding unapproved use of approved drugs",
      "sourceUrl": "https://www.fda.gov/drugs/understanding-unapproved-use-approved-drugs-label"
    },
    {
      "question": "A pharmacy transfers a package to another pharmacy solely to fill a prescription for an identified patient. What DSCSA concept may apply?",
      "choices": [
        "All transfers between pharmacies are illegal",
        "A specific-patient-need exception may distinguish this transfer from ordinary stock replenishment",
        "Any transfer eliminates the need for an authorized trading partner",
        "A patient-specific transfer is automatically a wholesale purchase for resale"
      ],
      "answer": "B",
      "explanations": [
        "Pharmacy-to-pharmacy transfers can have different legal treatment depending on purpose.",
        "Correct. The specific-patient-need exception differs from routine inventory replenishment.",
        "Other legal and licensure requirements still matter.",
        "Patient-specific fulfillment is not the same as routine stock transfer."
      ],
      "citation": "FD&C Act §581 — specific patient need",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-integrity/drug-supply-chain-security-act-dscsa"
    },
    {
      "question": "A pharmacy receives an FDA recall notice that has not yet been assigned Class I, II, or III. What should it do?",
      "choices": [
        "Ignore it until FDA classifies the recall",
        "Dispense all affected inventory immediately",
        "Identify and segregate affected stock and follow recall instructions without waiting for classification",
        "Assume the recall is voluntary and has no legal significance"
      ],
      "answer": "C",
      "explanations": [
        "A pending classification does not eliminate recall risk.",
        "Accelerated dispensing would undermine the recall.",
        "Correct. Recall action should follow product identification and instructions, regardless of pending classification.",
        "Recall handling depends on the actual action and risk, not merely the classification label."
      ],
      "citation": "FDA recall information and definitions",
      "sourceUrl": "https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions"
    }
  ],
  "numbers-records": [
    {
      "question": "A pharmacist discovers a quality-related dispensing error at 10 AM. Under Massachusetts CQI requirements, when is initial QRE documentation due?",
      "choices": [
        "Within 24 hours after discovery by or description to the pharmacist",
        "Within 30 days",
        "At the next annual inspection",
        "Only if the patient is hospitalized"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 247 CMR 15.03(2) requires initial documentation within 24 hours.",
        "Thirty days is too late.",
        "Inspection timing does not control initial documentation.",
        "QRE documentation is not restricted to hospitalizations."
      ],
      "citation": "247 CMR 15.03(2)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"
    },
    {
      "question": "A pharmacist learns that an incorrect medication was dispensed and the patient was seriously injured. Which Massachusetts Board reporting deadline generally applies to the Manager of Record?",
      "choices": [
        "One year",
        "Within seven business days of discovery of serious injury or death related to improper dispensing",
        "Within 72 calendar hours for every case",
        "Only after the pharmacy license expires"
      ],
      "answer": "B",
      "explanations": [
        "The reporting duty is much sooner.",
        "Correct. 247 CMR 20.02(1) establishes seven business days.",
        "The regulation specifies seven business days for this event.",
        "License renewal does not postpone reporting."
      ],
      "citation": "247 CMR 20.02(1)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    },
    {
      "question": "A pharmacy reports a serious improper-dispensing event to the Board. How long must the related records be retained under 247 CMR 20.02(4)?",
      "choices": [
        "One year from dispensing",
        "Two years from discovery",
        "Five years from the date the report was filed with the Board",
        "Ten years from the original prescription"
      ],
      "answer": "C",
      "explanations": [
        "The required retention is longer.",
        "Two years is associated with other record categories.",
        "Correct. The regulation specifies five years from Board filing.",
        "Ten years is not the general 20.02(4) rule."
      ],
      "citation": "247 CMR 20.02(4)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    },
    {
      "question": "A Massachusetts pharmacist discovers a QRE and plans to tell the patient only after completing a month-long root-cause analysis. What is the correct initial response?",
      "choices": [
        "Wait until the analysis is final",
        "Tell only the pharmacy's insurance company",
        "Delete the erroneous dispensing record",
        "Immediately address patient notification, correction instructions and harm mitigation as required by 247 CMR 15.03"
      ],
      "answer": "D",
      "explanations": [
        "QRE response begins promptly, not after a month.",
        "Insurance notification does not replace patient care.",
        "Records must be preserved for investigation.",
        "Correct. The pharmacist must take immediate notification and harm-minimization steps."
      ],
      "citation": "247 CMR 15.03(1)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"
    },
    {
      "question": "A pharmacy records an ordinary QRE and assumes that a serious injury will never require any additional Board report because the event is already in its CQI system. What is wrong?",
      "choices": [
        "The 247 CMR 20.02 serious-event reporting duty is separate from CQI documentation",
        "CQI replaces every Massachusetts reporting requirement",
        "The Board receives all QRE reports automatically",
        "Only DEA receives serious injury reports"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 247 CMR 20.02(3) explicitly makes reporting additional to CQI.",
        "CQI does not replace serious-event reports.",
        "Internal CQI records are not automatically Board filings.",
        "The Massachusetts Board has its own reporting authority."
      ],
      "citation": "247 CMR 20.02(3)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    },
    {
      "question": "A pharmacy receives an FDA-regulated DSCSA illegitimate-product determination at 2 PM. Which clock is relevant to the FDA notification?",
      "choices": [
        "Seven business days",
        "Fifteen calendar days",
        "Twenty-four hours after the determination",
        "The next monthly inventory"
      ],
      "answer": "C",
      "explanations": [
        "The DSCSA deadline is shorter.",
        "Fifteen days applies to some other FDA reporting systems.",
        "Correct. FDA requires notification within 24 hours of determining illegitimacy.",
        "Inventory cycles do not extend the notification deadline."
      ],
      "citation": "DSCSA illegitimate-product 24-hour reporting",
      "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
    },
    {
      "question": "A pharmacy has its federally required controlled-substance inventory but discards all controlled-substance acquisition and disposition records after six months. Which is correct?",
      "choices": [
        "Six months is sufficient if the pharmacy is busy",
        "Federal DEA records generally must be retained for at least two years, with longer state requirements where applicable",
        "Records may be discarded after any patient refill",
        "Records are needed only for Schedule II drugs"
      ],
      "answer": "B",
      "explanations": [
        "The federal retention minimum is longer.",
        "Correct. 21 CFR 1304.04 generally establishes at least two years for required controlled-substance records.",
        "A refill does not erase acquisition or disposition records.",
        "Federal records cover more than Schedule II."
      ],
      "citation": "21 CFR 1304.04",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.04"
    },
    {
      "question": "A Massachusetts pharmacy's serious-adverse-event report is filed with the Board on November 11, 2026. Which event determines the five-year retention period for that report's records?",
      "choices": [
        "The original drug's FDA approval date",
        "The date the pharmacy first opened",
        "The date the patient first became a customer",
        "The date the report was filed with the Board"
      ],
      "answer": "D",
      "explanations": [
        "FDA approval is unrelated to the event record's retention clock.",
        "Facility opening is unrelated.",
        "Patient enrollment is unrelated.",
        "Correct. 247 CMR 20.02(4) measures five years from Board filing."
      ],
      "citation": "247 CMR 20.02(4)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    },
    {
      "question": "A trainee confuses a pharmacy's internal QRE record with a serious adverse drug event report. What is the key distinction?",
      "choices": [
        "Both are always sent to DEA on Form 222",
        "Every QRE automatically requires an FDA MedWatch submission",
        "CQI/QRE documentation and reportable serious adverse drug events have different triggers and external reporting duties",
        "Neither requires documentation if the patient recovers"
      ],
      "answer": "C",
      "explanations": [
        "DEA Form 222 is an ordering document.",
        "Not every QRE triggers federal MedWatch reporting.",
        "Correct. 247 CMR 15 and 20 describe distinct documentation and reporting systems.",
        "Recovery does not erase applicable records and reporting duties."
      ],
      "citation": "247 CMR 15.03; 247 CMR 20.02",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    },
    {
      "question": "A Massachusetts pharmacy employee discovers a serious adverse drug event linked to a product compounded at the pharmacy. Who must the MOR notify under 247 CMR 20.02(2)?",
      "choices": [
        "The Board, FDA MedWatch, and the Betsy Lehman Center",
        "Only the pharmacy's insurance carrier",
        "Only the original drug wholesaler",
        "Only the patient's employer"
      ],
      "answer": "A",
      "explanations": [
        "Correct. The regulation names all three recipients.",
        "Insurance notification does not replace regulatory reporting.",
        "A wholesaler is not the only statutory recipient.",
        "Employer notification is not the statutory pathway and may breach privacy."
      ],
      "citation": "247 CMR 20.02(2)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-20-reporting/download"
    }
  ]
});

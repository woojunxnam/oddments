/* Original Massachusetts MPJE Chapter 21 moderate/hard nonsterile compounding cases. Author-source review November 12, 2026; independent legal audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "nonsterile-compounding": {
    "moderate": [
      {
        "question": "A pharmacist reconstitutes an antibiotic powder using the exact water amount and procedure stated in the manufacturer's FDA-approved labeling. No other ingredient is added. What is the proper classification?",
        "choices": [
          "This is automatically hazardous complex nonsterile compounding",
          "This requires an FDA 503B outsourcing facility registration",
          "It is manufacturer-directed reconstitution, generally distinct from USP <795> compounding, although safe handling remains required",
          "All reconstitution is sterile compounding regardless of route"
        ],
        "answer": "C",
        "explanations": [
          "Nonhazardous manufacturer-directed reconstitution does not necessarily meet the complex-compounding definition.",
          "A licensed pharmacy does not become a 503B outsourcing facility merely by reconstitution.",
          "Correct. USP <795> and Policy 2023-07 exclude preparation as directed in the manufacturer's labeling from their nonsterile compounding definition.",
          "Oral suspension reconstitution is not automatically a sterile process."
        ],
        "citation": "MA Board Policy 2023-07, Non-Sterile Compounding (revised 2025)",
        "sourceUrl": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download"
      },
      {
        "question": "A Massachusetts pharmacist adds a patient-requested flavor to an otherwise valid Schedule VI liquid medication, after confirming the resulting formula and BUD. The prescriber did not specifically request flavoring. Which handling is permissible?",
        "choices": [
          "The patient or agent may request flavoring of a Schedule VI medicine, with appropriate documentation and quality controls",
          "Flavoring any controlled-drug schedule is automatically legal without documentation",
          "A new federal DEA Form 222 must be executed before flavoring",
          "The flavored drug becomes FDA-approved as a new finished product"
        ],
        "answer": "A",
        "explanations": [
          "Correct. MA Policy 2023-07 specifically allows Schedule VI flavoring on a patient or agent request with required record updates.",
          "The Schedule VI exception does not authorize undocumented changes to all schedules.",
          "Form 222 concerns Schedule I/II inventory purchasing, not nonsterile flavoring.",
          "Compounding or flavoring does not by itself constitute new FDA approval."
        ],
        "citation": "MA Board Policy 2023-07, Non-Sterile Compounding (revised 2025)",
        "sourceUrl": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download"
      },
      {
        "question": "A pharmacy prepares customized capsules from bulk powder for a particular patient. Its facility has only a regular retail pharmacy license. Which Massachusetts requirement has not been satisfied?",
        "choices": [
          "The patient's prescription automatically substitutes for the specialty license",
          "Only a sterile-compounding license can authorize capsules",
          "No special license is needed if the capsules are for oral use",
          "Customized capsules are among the Board's complex nonsterile examples and require the separate specialty license"
        ],
        "answer": "D",
        "explanations": [
          "Patient-specific orders do not waive pharmacy facility licensure.",
          "Oral capsule production is not necessarily sterile compounding.",
          "Route of administration does not eliminate the defined complex category.",
          "Correct. Policy 2023-07 and M.G.L. c.112 §39H require additional complex nonsterile licensing."
        ],
        "citation": "M.G.L. c.112 §39H, Complex Nonsterile Pharmacy License",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39H"
      },
      {
        "question": "A pharmacist plans to compound from a bulk API supplied without a certificate of analysis. Its manufacturer also cannot be verified as FDA-registered. What is the best first response?",
        "choices": [
          "Proceed because the supplier's website claims purity",
          "Do not use the bulk drug until applicable 503A eligibility, FDA manufacturer registration and a valid certificate of analysis are verified",
          "Use the API as long as the patient signs a consent",
          "Label the preparation as FDA-approved to address missing supplier documentation"
        ],
        "answer": "B",
        "explanations": [
          "Marketing descriptions are insufficient under 503A.",
          "Correct. FDA requires qualified bulk substance status, a valid COA and manufacture at an FDA-registered establishment.",
          "Patient agreement does not waive statutory ingredient requirements.",
          "An unsupported FDA-approval claim is improper."
        ],
        "citation": "FDA — Section 503A Bulk Drug Substances",
        "sourceUrl": "https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503a-fdc-act"
      },
      {
        "question": "A state-licensed pharmacy compounds a nonsterile medication in anticipation of future requests, although it has no past prescriptions for that preparation. It intends to distribute the supply without identifying patients. What is the 503A problem?",
        "choices": [
          "Federal 503A allows unlimited anonymous office stock whenever a pharmacist is licensed",
          "The pharmacy becomes a 503B outsourcing facility automatically",
          "503A only permits limited anticipatory compounding based on an established prescription history, and dispensing requires the appropriate identified-patient prescription",
          "Any nonsterile preparation may be sold to a clinic without patient-specific requirements"
        ],
        "answer": "C",
        "explanations": [
          "Anticipatory compounding is limited rather than unlimited.",
          "503B is a separate registered facility framework.",
          "Correct. The 503A patient-specific pathway does not permit unbounded anonymous stock distribution.",
          "Nonsterile form does not create a general office-stock exemption."
        ],
        "citation": "FDA — FD&C Act Provisions for §503A and §503B",
        "sourceUrl": "https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding"
      },
      {
        "question": "A pharmacist prepares a nonpreserved aqueous oral suspension without preparation-specific BUD evidence or a USP monograph, and all components remain suitable longer than the default. What is the default USP <795> maximum?",
        "choices": [
          "14 days, refrigerated",
          "35 days at room temperature without preservative",
          "90 days without refrigeration",
          "180 days because the medication is not sterile"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The current default maximum for nonpreserved aqueous CNSPs is 14 days refrigerated.",
          "35 days applies to preserved aqueous products.",
          "90 days is the default for nonaqueous oral liquids.",
          "180 days concerns other nonaqueous preparations."
        ],
        "citation": "USP General Chapter <795> (2023 revised nonsterile standards)",
        "sourceUrl": "https://doi.usp.org/USPNF/USPNF_M99595_06_01.html"
      },
      {
        "question": "An otherwise suitable preserved aqueous compounded gel has no monograph or formula-specific stability study. Under USP <795>, which default BUD upper limit and storage arrangement is the closest match?",
        "choices": [
          "14 days only in a freezer",
          "180 days at any temperature",
          "90 days because every liquid and gel is nonaqueous",
          "35 days at controlled room temperature or in a refrigerator, subject to shorter stability limits"
        ],
        "answer": "D",
        "explanations": [
          "14 days refrigerated is the nonpreserved aqueous default.",
          "The nonaqueous 'other' category has different conditions.",
          "Water activity and preservation govern classification, not merely dosage-form appearance.",
          "Correct. Revised USP <795> gives preserved aqueous dosage forms up to 35 days."
        ],
        "citation": "USP General Chapter <795> (2023 revised nonsterile standards)",
        "sourceUrl": "https://doi.usp.org/USPNF/USPNF_M99595_06_01.html"
      },
      {
        "question": "A pharmacist checks and releases complex nonsterile suppositories but has completed only the general 20 continuing-education hours this year. What separate Massachusetts requirement remains?",
        "choices": [
          "An additional five hours of sterile-compounding CE regardless of product type",
          "Three hours of qualifying complex nonsterile compounding CE during the calendar year, which may count within the general 20 hours",
          "No special CE applies to final verification responsibilities",
          "Only a one-time employer orientation is needed"
        ],
        "answer": "B",
        "explanations": [
          "Five hours applies to sterile-compounding duties.",
          "Correct. Board Policy 2021-04 applies the three-hour complex nonsterile CE rule to those performing final verification and other listed functions.",
          "Final verification is among the duties triggering the CE rule.",
          "General orientation does not replace continuing education."
        ],
        "citation": "Board Policy 2021-04 (revised 2025), Complex Nonsterile Compounding CE",
        "sourceUrl": "https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download"
      },
      {
        "question": "A pharmacy has a master formulation record for a nonsterile product but does not document the actual ingredient lots, quantities, personnel or assigned BUD of today's patient-specific batch. What must be created?",
        "choices": [
          "Only a new DEA Form 106 after every batch",
          "Only a patient billing record",
          "A compounding record for the actual preparation event, distinct from the reusable master formulation",
          "No record until a defect is detected"
        ],
        "answer": "C",
        "explanations": [
          "Form 106 concerns federally reportable controlled-drug theft or significant loss.",
          "Billing details are not batch production records.",
          "Correct. Board Policy 2023-07 calls for a compounding record for each CNSP, containing the preparation-specific accountability details.",
          "Documentation is expected for routine compounding, not merely after a defect."
        ],
        "citation": "MA Board Policy 2023-07, Non-Sterile Compounding (revised 2025)",
        "sourceUrl": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download"
      },
      {
        "question": "A pharmacy produces a nonaqueous oral liquid with no qualifying monograph or stability data for a longer BUD. Which default USP <795> category applies?",
        "choices": [
          "14 days refrigerated because every liquid is aqueous",
          "35 days because all liquids contain a preservative",
          "180 days because it is nonaqueous",
          "Up to 90 days at controlled room temperature or refrigerated storage, unless other factors shorten the BUD"
        ],
        "answer": "D",
        "explanations": [
          "The formula is nonaqueous, so the nonpreserved aqueous limit does not control.",
          "Preservation does not define every liquid formula.",
          "Other nonaqueous dosage forms have a separate 180-day default.",
          "Correct. Nonaqueous oral liquids have a default upper limit of 90 days."
        ],
        "citation": "USP General Chapter <795> (2023 revised nonsterile standards)",
        "sourceUrl": "https://doi.usp.org/USPNF/USPNF_M99595_06_01.html"
      }
    ],
    "hard": [
      {
        "question": "An FDA-approved tablet containing an allergenic dye is commercially available. A prescriber documents an individual patient's confirmed dye allergy and orders the same active ingredient in a dye-free compounded preparation. The pharmacy meets ingredient and licensing rules. What is the significance of the clinical documentation?",
        "choices": [
          "Any lower-priced version of an approved drug is a sufficient medical difference",
          "FDA approval of the original tablet automatically authorizes its compounded copy",
          "The documented medically significant patient-specific change can support a conditional copy exception, but the pharmacy still must comply with 503A and Massachusetts safeguards",
          "The patient's allergy makes all prescriptions and recordkeeping optional"
        ],
        "answer": "C",
        "explanations": [
          "Cost savings alone does not establish a significant medical difference.",
          "FDA approval of a comparator does not validate each compounded version.",
          "Correct. MA Policy 2020-02 recognizes a prescriber-documented patient-specific significant difference such as removal of an allergenic ingredient.",
          "A clinical reason does not remove requirements for a valid prescription and preparation records."
        ],
        "citation": "MA Board Policy 2020-02, Copies of Commercially Available Drugs",
        "sourceUrl": "https://www.mass.gov/doc/2020-02-compounding-copies-of-commercially-available-drugs/download"
      },
      {
        "question": "A pharmacist compounds hazardous NIOSH-listed nonsterile capsules in the same room and containment hood used for ordinary nonhazardous creams. The pharmacy holds a complex nonsterile specialty license. What is still required?",
        "choices": [
          "Separate hazardous-drug containment controls and a room/hood arrangement that does not mix HD and non-HD nonsterile compounding",
          "The specialty license automatically waives all hazardous handling requirements",
          "Use a pharmacy technician's vaccination certificate instead of containment controls",
          "Store all unused ingredients beside customer refreshments to dilute exposure"
        ],
        "answer": "A",
        "explanations": [
          "Correct. MA Policy 2023-07 requires separation of hazardous and nonhazardous compounding rooms/PECs with appropriate containment.",
          "Facility licensure is not a substitute for engineering controls.",
          "Unrelated credentials do not validate hazardous-drug handling.",
          "Food storage is not an acceptable contamination or exposure control."
        ],
        "citation": "MA Board Policy 2023-07, Non-Sterile Compounding (revised Feb 2025)",
        "sourceUrl": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download"
      },
      {
        "question": "A compounding technician uses a commercial premeasured kit and adds flavor to the final Schedule VI medicine. The only record is a patient name and date; component lot, additives, quantity, BUD and preparer are missing. What does the Massachusetts nonsterile policy permit?",
        "choices": [
          "All premeasured kits are exempt from any preparation record",
          "A sufficiently detailed combined compounding log can serve as MFR and compounding record, but it must contain the required component, quantity, lot, BUD and personnel information",
          "Medication labeling replaces all component traceability requirements",
          "A kit automatically qualifies as FDA approval of any newly mixed preparation"
        ],
        "answer": "B",
        "explanations": [
          "Board Policy 2023-07 requires preparation accountability even for kits.",
          "Correct. A combined log is permitted for eligible kit/flavoring preparations only when required details are documented.",
          "A patient label alone does not establish actual batch history.",
          "Mixing a kit does not confer new FDA approval."
        ],
        "citation": "MA Board Policy 2023-07, Non-Sterile Compounding (revised Feb 2025)",
        "sourceUrl": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download"
      },
      {
        "question": "A preserved aqueous compounded suspension could qualify for a 35-day default BUD, but one formulation component expires in 18 days. There is no supporting evidence that it remains stable longer. What BUD should be assigned?",
        "choices": [
          "Thirty-five days is mandatory even when a component expires sooner",
          "One hundred eighty days because the formula contains a preservative",
          "The compounded drug inherits the longest expiration date among its ingredients",
          "No later than the earlier applicable component expiration/stability limit, despite the general 35-day aqueous default"
        ],
        "answer": "D",
        "explanations": [
          "USP default BUDs are maximums and do not override a shorter known limit.",
          "Preservation does not turn an aqueous preparation into a nonaqueous one.",
          "The BUD must consider all components, not only the longest-lasting ingredient.",
          "Correct. BUD assignments must observe the shorter scientifically justified stability and ingredient limits."
        ],
        "citation": "USP General Chapter <795> (revised compounding standard)",
        "sourceUrl": "https://doi.usp.org/USPNF/USPNF_M99595_06_01.html"
      },
      {
        "question": "A Massachusetts pharmacy wants to make an otherwise identical copy of a nationally available FDA-approved drug only because its local wholesaler is temporarily out of stock. The prescriber has not documented any unique patient need. Which answer best distinguishes the issues?",
        "choices": [
          "The pharmacy may automatically make indefinite copies whenever a single wholesaler runs out",
          "A local stockout is equivalent to FDA's national shortage listing",
          "A local stockout or lower cost alone is not a sufficient documented medical difference under Massachusetts policy, and the federal 503A copy restriction must be assessed separately",
          "A pharmacy may replace a nonsterile prescription with an FDA-approved label from the commercial product"
        ],
        "answer": "C",
        "explanations": [
          "Local availability alone is not an unrestricted copy exception.",
          "FDA drug-shortage status is a distinct federal determination.",
          "Correct. Both Massachusetts patient-specific difference requirements and federal 503A copying conditions must be satisfied.",
          "Using another product's label does not validate unauthorized compounding."
        ],
        "citation": "MA Board Policy 2020-02, Copies of Commercially Available Drugs",
        "sourceUrl": "https://www.mass.gov/doc/2020-02-compounding-copies-of-commercially-available-drugs/download"
      },
      {
        "question": "A compounder compares two federal 5% thresholds and claims both use the number of Schedule II dosage units distributed to other pharmacies as their denominator. Which distinction is correct?",
        "choices": [
          "FDA's 503A interstate distribution limit concerns compounded prescription orders and MOU/enforcement issues; DEA's practitioner-distribution exemption concerns controlled dosage units and is a separate rule",
          "The two thresholds share the same DEA-controlled dosage-unit denominator",
          "FDA's delayed enforcement means the statutory 503A provision was permanently repealed",
          "Both rules apply only to prescriptions paid for with cash"
        ],
        "answer": "A",
        "explanations": [
          "Correct. FDA 503A interstate compounded-order measures and DEA §1307.11 stock-distribution measures have different activities and denominators.",
          "DEA stock distribution is not the denominator for FDA's 503A limit.",
          "Enforcement postponement does not itself repeal a statute.",
          "Payment arrangements do not determine either threshold."
        ],
        "citation": "FDA — Memorandum of Understanding for Interstate Compounded Drug Distribution",
        "sourceUrl": "https://www.fda.gov/drugs/human-drug-compounding/memorandum-understanding-addressing-certain-distributions-compounded-drugs"
      },
      {
        "question": "A pharmacist makes batches of a compounded hormone preparation for unspecified walk-in customers without any established prescription history. The product is later sold in bulk to a clinic as stock while the pharmacy claims 503A protections. What is the main federal problem?",
        "choices": [
          "The preparation is valid because it was compounded by a licensed pharmacist",
          "503A permits limited anticipatory work based on established histories, not unrestricted anonymous office-stock distribution without identified-patient prescriptions",
          "Every pharmacy is automatically FDA-registered under 503B",
          "Sales to a clinic automatically make the preparation FDA-approved"
        ],
        "answer": "B",
        "explanations": [
          "Pharmacist licensure is necessary but not sufficient to satisfy 503A.",
          "Correct. 503A anticipatory compounding and individual prescription requirements cannot be replaced by an unrestricted clinic-stock program.",
          "503B outsourcing registration is a separate pathway with distinct requirements.",
          "Distribution does not confer FDA product approval."
        ],
        "citation": "FDA — FD&C Act §503A and §503B Compounding Provisions",
        "sourceUrl": "https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding"
      },
      {
        "question": "A Massachusetts pharmacy plans to compound customized oral systemic capsules and a complex nonsterile transdermal formulation. It has current pharmacist training and valid patient prescriptions, but only a standard Drug Store license. Which statement is correct?",
        "choices": [
          "Staff competency automatically grants the pharmacy any needed facility license",
          "Only hazardous versions of these preparations can be complex",
          "Both products qualify as manufacturer-directed reconstitution",
          "An additional Massachusetts complex nonsterile specialty license is required; pharmacist training and patient prescriptions are separate requirements"
        ],
        "answer": "D",
        "explanations": [
          "Training alone does not satisfy facility licensing.",
          "Nonhazardous capsule and transdermal preparation can still be categorized as complex.",
          "Both preparations involve genuine compounding beyond reconstitution.",
          "Correct. M.G.L. c.112 §39H and Board policy require the applicable facility license."
        ],
        "citation": "M.G.L. c.112 §39H — Complex Nonsterile Compounding Licensure",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39H"
      },
      {
        "question": "A compounding pharmacist chooses a 365-day BUD for a nonaqueous oral liquid solely because a supplier brochure says the product is oil-based. No monograph or formula-specific stability test exists. What is the problem?",
        "choices": [
          "Oil-based products are automatically exempt from USP <795>",
          "Every nonaqueous formula receives a one-year default BUD",
          "The default nonaqueous oral liquid category is up to 90 days, and a longer BUD requires the applicable specific scientific support and may be capped under USP <795>",
          "Manufacturers' expiration dates for unrelated drugs control the compounded preparation"
        ],
        "answer": "C",
        "explanations": [
          "The physical vehicle does not create a universal exemption.",
          "USP treats nonaqueous oral liquids separately from other nonaqueous dosage forms.",
          "Correct. An unsupported 365-day BUD is inconsistent with the default and stability-evidence limits.",
          "A different finished product's expiration does not establish this preparation's stability."
        ],
        "citation": "USP General Chapter <795> (revised compounding standard)",
        "sourceUrl": "https://doi.usp.org/USPNF/USPNF_M99595_06_01.html"
      },
      {
        "question": "A pharmacy receives tablets clearly marked 'Drug sample — not for resale.' The pharmacist wants to crush them and add them to a custom cream, then charge a patient for the compounded product. What does Massachusetts 247 CMR 9.01 prohibit?",
        "choices": [
          "Using drug samples not for resale for the purpose of compounding, repacking or resale, even if the finished dosage form is changed",
          "Only using drug samples in a Schedule II prescription",
          "Compounding from such samples is always permitted if the patient signs consent",
          "Changing from tablets to cream makes the sample eligible for resale"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 9.01(6) forbids accepting or purchasing samples not for resale to compound or resell.",
          "The restriction is not confined to Schedule II.",
          "Patient consent does not remove the sample prohibition.",
          "Altered dosage form does not cure the original resale restriction."
        ],
        "citation": "247 CMR 9.01(6) — Drug samples not for resale",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      }
    ]
  }
});

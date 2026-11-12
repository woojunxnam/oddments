/* Chapter 21 nonsterile compounding; moderate cases staged, hard cases follow. Author verification 2026-11-12; independent audit pending. */
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
    ]
  }
});

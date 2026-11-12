/* Hand-authored Chapter 10 Moderate items; Hard cases appended in next commit. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "label-interchange": {
    "moderate": [
      {
        "question": "An MA physician writes a brand-name prescription and properly marks 'no substitution.' The pharmacist finds a cheaper, AB-rated generic. What is the usual Massachusetts requirement?",
        "choices": [
          "Dispense the cheaper generic because AB status overrides the prescriber's instruction",
          "Dispense the exact prescribed product instead of routinely interchanging it",
          "Substitute any generic when the pharmacist thinks it is safe",
          "Provide the generic and change the name on the original order"
        ],
        "answer": "B",
        "explanations": [
          "FDA TE status does not override a legally valid no-substitution instruction.",
          "Correct. M.G.L. c.112 §12D requires the exact product where the prescriber properly directs no substitution.",
          "A pharmacist's routine cost decision does not override the instruction.",
          "Altering the original prescribed name is not a solution."
        ],
        "citation": "M.G.L. c.112 §12D (interchange and no substitution)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12D"
      },
      {
        "question": "A Massachusetts patient has a new brand-name prescription with no restriction on interchange. A less expensive, reasonably available equivalent appears on the current Massachusetts interchangeable-drug list. What is generally expected?",
        "choices": [
          "Keep the more expensive brand because the prescriber wrote a brand name",
          "Choose a drug with any active ingredient but the same indication",
          "Refuse to dispense either medicine",
          "Dispense the interchangeable product as directed by §12D, with the required interchange labeling"
        ],
        "answer": "D",
        "explanations": [
          "An unrestricted brand-name prescription generally remains subject to mandatory lawful interchange.",
          "Clinical indication alone does not establish interchangeability.",
          "Lawful interchange is not a reason to refuse an otherwise valid order.",
          "Correct. Massachusetts requires eligible less expensive interchangeable products, subject to specific exceptions."
        ],
        "citation": "M.G.L. c.112 §12D (interchange and no substitution)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12D"
      },
      {
        "question": "An FDA Orange Book record lists two products with AB1 and AB2 ratings, respectively, and neither record shows any common AB-number rating. Which conclusion is supported?",
        "choices": [
          "AB1 and AB2 should not be assumed therapeutically equivalent to each other solely because both begin with 'AB'",
          "The numerical suffix is irrelevant to therapeutic equivalence",
          "The two products are legally Schedule I because their suffixes differ",
          "Every AB rating makes all products of the active ingredient interchangeable"
        ],
        "answer": "A",
        "explanations": [
          "Correct. FDA groups AB1/AB2 by their applicable reference drugs; absence of a common code does not establish equivalence across groups.",
          "Numerical suffixes distinguish specific equivalence groups.",
          "Orange Book TE codes do not determine controlled-substance schedules.",
          "Common ingredient alone is insufficient for every interchange."
        ],
        "citation": "FDA Orange Book Preface, §1.7 (TE codes)",
        "sourceUrl": "https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface"
      },
      {
        "question": "A pharmacist reviews an authorized generic produced under the brand holder's NDA, not a separate ANDA. The trainee cannot find its own Orange Book AB rating and concludes it is not equivalent to the brand. What is correct?",
        "choices": [
          "Authorized generics are always unapproved compounded drugs",
          "A product must have a separate ANDA to be identical to the brand",
          "An authorized generic is the approved brand product marketed without its brand name and can be interchangeable without a distinct Orange Book listing, if no-substitution is not directed",
          "The pharmacist may ignore the brand's ingredients because all generics are the same"
        ],
        "answer": "C",
        "explanations": [
          "Authorized generics are manufactured under approved NDA marketing arrangements.",
          "They are generally marketed under the brand's NDA, not a separate ANDA.",
          "Correct. MA DCP Circular 22-01-112 recognizes authorized generic interchange where no substitution is not specified.",
          "Identity must still be verified for the actual product."
        ],
        "citation": "MA DCP Circular 22-01-112: Dispensing Authorized Generics",
        "sourceUrl": "https://www.mass.gov/news/dispensing-authorized-generics-circular-letter-dcp-22-01-112"
      },
      {
        "question": "A Massachusetts pharmacy prepares a Schedule II tablet prescription label with pharmacy, patient, drug, directions and date, but the label omits the number of tablets in the container. What should be corrected?",
        "choices": [
          "No change; tablet quantity is only needed on the insurance claim",
          "Add the number of tablets or capsules because §21 requires it on the container label",
          "Remove the patient's name from every human prescription",
          "Replace the drug name with the pharmacy's internal stock code"
        ],
        "answer": "B",
        "explanations": [
          "Insurance claim content is not a substitute for statutory label content.",
          "Correct. M.G.L. c.94C §21 requires the number of tablets or capsules in the container.",
          "Human patient identification is ordinarily required.",
          "An internal code does not replace the controlled-substance name."
        ],
        "citation": "M.G.L. c.94C §21 (patient-label requirements)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"
      },
      {
        "question": "An elderly patient requests more readable prescription-label directions because the print is too small. Which Massachusetts labeling accommodation applies?",
        "choices": [
          "Allow the technician to omit the directions entirely",
          "Provide only a verbal explanation without changing the label",
          "Tell the patient that federal law forbids larger print",
          "On request, type directions in a print size allowing no more than ten characters per inch"
        ],
        "answer": "D",
        "explanations": [
          "The legal accommodation concerns how the directions are printed, not removal.",
          "Oral counseling may help but does not replace the specified requested accommodation.",
          "The state statute expressly addresses larger-readable directions.",
          "Correct. c.94C §21 establishes a ten-characters-per-inch maximum on request for elderly or visually impaired persons."
        ],
        "citation": "M.G.L. c.94C §21 (patient-label requirements)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"
      },
      {
        "question": "A pharmacist wants to substitute a biosimilar for a brand-name biological product at the pharmacy without contacting its prescriber. The FDA Purple Book identifies the candidate as biosimilar but not interchangeable. Which assessment is appropriate?",
        "choices": [
          "Biosimilarity alone does not establish the FDA interchangeability status required for the usual automatic pharmacy-level substitution",
          "Every biosimilar is automatically interchangeable for all states",
          "The Orange Book AB number alone is always sufficient for biologic substitution",
          "The pharmacist may substitute any biosimilar despite patient-specific written prohibition"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Pharmacy-level biologic substitution generally requires an FDA interchangeable designation and state-law conditions.",
          "FDA distinguishes biosimilar approval from interchangeability.",
          "Biologic interchangeability is checked through applicable FDA biologic resources.",
          "MA §12EE preserves written patient-specific prescriber prohibition."
        ],
        "citation": "FDA: Biosimilars Basics / Interchangeable biosimilars",
        "sourceUrl": "https://www.fda.gov/drugs/biosimilars/biosimilars-basics-patients"
      },
      {
        "question": "A Massachusetts pharmacist lawfully substitutes an FDA-interchangeable biological product for a prescribed brand biologic. The pharmacist assumes telling the patient verbally is sufficient and the prescriber need not be informed. What is missing?",
        "choices": [
          "No notification is ever required for biological substitutions",
          "The pharmacist must contact the FDA instead of the prescriber",
          "Massachusetts requires the specified prescriber notification and written patient/representative notification after a qualifying biologic substitution",
          "Only the manufacturer is entitled to notification"
        ],
        "answer": "C",
        "explanations": [
          "§12EE(d)–(e) imposes specific notification duties.",
          "FDA substitution approval does not replace state notification to the treating practitioner.",
          "Correct. Appropriate prescriber notification and written patient notice are distinct requirements.",
          "Manufacturer notification is not the statutory substitute."
        ],
        "citation": "M.G.L. c.112 §12EE(b)–(f)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12EE"
      },
      {
        "question": "A Massachusetts insured patient fills an otherwise lawful prescription. The insurance copayment would be $27 but the pharmacy's cash retail price is $15. What does §21C require at the point of sale?",
        "choices": [
          "Charge $27 because an insurance copayment is always mandatory",
          "Charge the lesser $15 amount under the statutory retail-versus-cost-sharing comparison",
          "Charge $42 by adding both amounts",
          "Charge the higher amount so the insurer receives a discount"
        ],
        "answer": "B",
        "explanations": [
          "Massachusetts specifically limits the individual's amount to the lesser cost.",
          "Correct. §21C(b) requires charging the lesser of applicable cost sharing and pharmacy retail price.",
          "The statute does not require adding the two amounts.",
          "A higher price would conflict with the statutory comparison."
        ],
        "citation": "M.G.L. c.94C §21C(b)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21C"
      },
      {
        "question": "An MA pharmacy makes a lawful interchangeable biologic substitution and then asks how long the substitution record must be kept under M.G.L. c.112 §12EE(f). What is the minimum specified by that provision?",
        "choices": [
          "Only through the patient's next refill",
          "Exactly 30 days after the first substitution",
          "Only until the prescriber is notified",
          "Not less than one year from the date of the last entry in the profile record, without limiting other applicable retention rules"
        ],
        "answer": "D",
        "explanations": [
          "The statute does not tie the minimum to the next refill.",
          "It specifies a one-year minimum measured from the last profile entry.",
          "Notice completion does not end retention duties.",
          "Correct. §12EE(f) sets the stated minimum and does not override other professional record-retention rules."
        ],
        "citation": "M.G.L. c.112 §12EE(b)–(f)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12EE"
      }
    ]
  }
});

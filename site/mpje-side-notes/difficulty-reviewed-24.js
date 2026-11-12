/* Massachusetts MPJE Chapter 24 FDA and DSCSA supply-chain law: 10 moderate + 10 hard original scenarios. Official FDA source author-review 2026-11-12; independent audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "fda-supply-chain": {
    "moderate": [
      {
        "question": "A three-location pharmacy company has 24 full-time licensed pharmacists and qualified pharmacy technicians combined across its sites on November 27, 2026. What may this mean for FDA's newly announced small-dispenser DSCSA exemption?",
        "choices": [
          "Each location must have no more than five employees regardless of company size",
          "The company may qualify for specified enhanced DSCSA exemptions through November 27, 2027, but its remaining supply-chain obligations continue",
          "The exemption automatically makes all suspect products legitimate",
          "Each store must separately submit a paid FDA manufacturer application"
        ],
        "answer": "B",
        "explanations": [
          "The exemption measures qualifying full-time employees at the company level.",
          "Correct. FDA's August 2026 exemption uses the company-wide 25-or-fewer test as of November 27, 2026 and covers only specified duties.",
          "DSCSA protections for suspect/illegitimate products are not generally abolished.",
          "FDA has not imposed this unrelated manufacturer application as a condition for the blanket exemption."
        ],
        "citation": "FDA DSCSA Small-Dispenser Exemption (issued Aug. 6, 2026; through Nov. 27, 2027)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
      },
      {
        "question": "A pharmacy belongs to a chain with 32 full-time qualified pharmacy technicians and pharmacists company-wide, although only four of them work at the specific store. Which conclusion follows from FDA's August 2026 small-dispenser exemption?",
        "choices": [
          "The store cannot qualify solely from its four-person headcount; FDA uses the company's qualifying workforce total",
          "The store automatically qualifies because fewer than 25 employees work at that address",
          "The FDA counts only pharmacists and never qualified technicians",
          "The number of part-time cashiers determines exemption eligibility"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The exemption explicitly uses company-level full-time licensed pharmacists plus qualified technicians.",
          "Store-level arithmetic cannot override company workforce totals.",
          "Qualified pharmacy technicians are included in the threshold.",
          "The test concerns qualified licensed pharmacists/technicians, not retail cashiers."
        ],
        "citation": "FDA DSCSA Small-Dispenser Exemption (issued Aug. 6, 2026; through Nov. 27, 2027)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
      },
      {
        "question": "A Massachusetts dispenser receives a sealed prescription-drug package with altered serial information suggesting falsification. The pharmacy has not yet determined whether the product is illegitimate. What is the appropriate DSCSA action?",
        "choices": [
          "Dispense it because a suspect product is not yet legally proven counterfeit",
          "Notify patients the batch is FDA-approved because it arrived sealed",
          "Quarantine and investigate the suspect product and withhold it from distribution while its status is assessed",
          "Return it to open sale stock until FDA formally issues a recall"
        ],
        "answer": "C",
        "explanations": [
          "Suspicion triggers quarantine/investigation requirements before proof of illegitimacy.",
          "Packaging appearance does not prove authenticity or drug approval.",
          "Correct. DSCSA requires action on suspect product even before a formal illegitimate determination.",
          "Recall classification is separate from immediate suspect-product duties."
        ],
        "citation": "FDA — DSCSA Title II, FD&C Act §582 suspect/illegitimate product rules",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/title-ii-drug-quality-and-security-act"
      },
      {
        "question": "At noon Monday, a dispensing pharmacy determines with credible evidence that a prescription product is counterfeit. No exemption applies. Which DSCSA notice must the pharmacy make?",
        "choices": [
          "Notify FDA only on its next annual inventory date",
          "Wait 45 days and file a DEA Form 106",
          "Notify only its insurance carrier within 30 days",
          "Notify FDA and appropriate immediate trading partners within 24 hours after the illegitimate determination"
        ],
        "answer": "D",
        "explanations": [
          "The federal illegitimate-product notification period is 24 hours.",
          "DEA theft/loss reporting is distinct from DSCSA illegitimate-product reporting.",
          "Insurance notice does not replace required FDA and trading partner notification.",
          "Correct. FDA's DSCSA instructions specify FDA and immediate trading partner notification within 24 hours."
        ],
        "citation": "FDA — Notify FDA of Illegitimate Products",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
      },
      {
        "question": "A wholesale drug distributor offers to sell a pharmacy deeply discounted prescription-drug stock, but the pharmacy has not verified that the distributor is authorized. Which decision aligns with DSCSA?",
        "choices": [
          "Purchase only from authorized trading partners, verifying appropriate wholesale-distributor licensing or authorization before relying on the source",
          "Any seller with a valid tax ID automatically qualifies as an authorized wholesale distributor",
          "Patient willingness to pay cash cures the distributor authorization defect",
          "An NDC printed on the package makes the source legally authorized"
        ],
        "answer": "A",
        "explanations": [
          "Correct. DSCSA requires relevant trading partners to be authorized; FDA maintains licensure verification resources.",
          "Tax registration is not a state wholesale drug distribution credential.",
          "Payment method does not override trading partner requirements.",
          "NDC information does not substitute for licensing checks."
        ],
        "citation": "FDA — Authorized Wholesale Distributors and Third-Party Logistics Providers",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-integrity/check-licensure-wholesale-drug-distributors-and-third-party-logistics-providers"
      },
      {
        "question": "A pharmacy purchases a prescription drug with a valid-looking National Drug Code in FDA's NDC Directory. The owner claims that entry proves the exact drug was approved under an NDA or ANDA. What is the correction?",
        "choices": [
          "FDA's NDC directory is a federal controlled-substance schedule",
          "NDC assignment and listing do not, by themselves, establish FDA approval of the marketed drug",
          "A product is automatically interchangeable with every brand that has a similar NDC",
          "Every NDC listed is a biologic licensed under a BLA"
        ],
        "answer": "B",
        "explanations": [
          "NDC listing concerns drug identification/listing, not controlled-substance schedules.",
          "Correct. FDA explicitly warns that NDC Directory inclusion is not evidence of FDA approval.",
          "NDC similarity does not demonstrate pharmaceutical/therapeutic equivalence.",
          "Biologic licensing and NDC listing are distinct regulatory categories."
        ],
        "citation": "FDA — NDC Product File Definitions (NDC listing not product approval)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-product-file-definitions"
      },
      {
        "question": "FDA classifies a recall of a blood-pressure medication as Class I because of a serious contamination risk. Which explanation best distinguishes Class I from other recall categories?",
        "choices": [
          "Class I always denotes a clerical labeling problem with no health implications",
          "Class I means the product is being removed merely for marketing preference",
          "Class I signifies a reasonable probability that use or exposure will cause serious adverse health consequences or death",
          "Class I means the recalled product has already been safely disposed of"
        ],
        "answer": "C",
        "explanations": [
          "Minor labeling issues generally would not meet the Class I definition absent serious risk.",
          "Marketing preference may be a market withdrawal rather than an FDA-classified recall.",
          "Correct. FDA uses its highest risk category for a reasonable probability of serious harm or death.",
          "Recall class addresses health risk rather than completion status."
        ],
        "citation": "FDA — Recalls Background and Class I–III Definitions",
        "sourceUrl": "https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions"
      },
      {
        "question": "A physician prescribes an FDA-approved medication for a patient condition not listed in its approved labeling, and the medication is otherwise legally prescribed. What does FDA's off-label framework say?",
        "choices": [
          "FDA has approved the new indication by virtue of the physician's prescription",
          "A pharmacist must change the drug to an investigational product automatically",
          "The prescription is invalid solely because the use is off-label",
          "FDA generally regulates manufacturers' marketing approval; qualified clinicians may prescribe an approved drug for an unapproved use under applicable medical and pharmacy law"
        ],
        "answer": "D",
        "explanations": [
          "Prescriber choice does not create FDA approval for the new indication.",
          "An approved product used off-label is not automatically an IND study product.",
          "Off-label status alone is not a blanket federal prescription prohibition.",
          "Correct. FDA distinguishes lawful clinician-directed off-label use from FDA marketing approval for a claim."
        ],
        "citation": "FDA — Understanding Unapproved Use of Approved Drugs (Off-label)",
        "sourceUrl": "https://www.fda.gov/drugs/understanding-unapproved-use-approved-drugs-label"
      },
      {
        "question": "A developer wishes to market a generic version of an existing FDA-approved small-molecule prescription drug using bioequivalence to its reference listed drug, rather than repeating all innovator clinical trials. Which application is designed for this?",
        "choices": [
          "Abbreviated New Drug Application (ANDA), if statutory sameness and bioequivalence requirements are met",
          "Biologics License Application for every small-molecule tablet",
          "IND as the final ordinary generic marketing approval",
          "A DEA Form 222 drug manufacturing approval"
        ],
        "answer": "A",
        "explanations": [
          "Correct. An ANDA provides the abbreviated route for qualifying generic versions of approved drugs.",
          "BLAs principally address regulated biologics.",
          "IND supports investigational clinical development, not ordinary generic approval.",
          "DEA order forms do not confer FDA marketing approval."
        ],
        "citation": "FDA — Abbreviated New Drug Application (ANDA)",
        "sourceUrl": "https://www.fda.gov/drugs/types-applications/abbreviated-new-drug-application-anda"
      },
      {
        "question": "A pharmacist sees the FDA's 2026 NDC-format final rule and assumes all NDCs must already be in the new standardized twelve-digit format in November 2026. Which timing distinction is correct?",
        "choices": [
          "The rule was withdrawn, so NDC identifiers never change",
          "The new format's required implementation date is March 7, 2033, rather than its 2026 publication date",
          "Only DEA-registered drugs receive twelve-digit NDCs",
          "The new rule instantly creates FDA approval for listed products"
        ],
        "answer": "B",
        "explanations": [
          "FDA finalized a format transition rather than withdrawing it.",
          "Correct. FDA states the new standardized 12-digit NDC rule becomes effective in 2033, not in November 2026.",
          "NDC identifiers are not confined to controlled drugs.",
          "NDC format regulation does not substitute for marketing approval."
        ],
        "citation": "FDA — NDC Format Rule and 2033 Transition",
        "sourceUrl": "https://www.fda.gov/drugs/electronic-drug-registration-and-listing-system-edrls/national-drug-code-format"
      }
    ],
    "hard": [
      {
        "question": "A chain's Pharmacy A employs 11 full-time pharmacists/qualified technicians and Pharmacy B employs 18, with one shared corporate owner and no others. The company expects the new FDA small-dispenser exemption after November 27, 2026. What is the correct calculation?",
        "choices": [
          "Each location is separately below 25, so both automatically qualify",
          "Only pharmacists count; the 18 technicians are excluded",
          "The company has 29 qualifying employees in total, which exceeds the 25-person cutoff for that FDA exemption",
          "Every pharmacy company qualifies regardless of headcount until 2027"
        ],
        "answer": "C",
        "explanations": [
          "The FDA criterion is company-wide, not location-by-location.",
          "Qualified technicians count alongside licensed pharmacists.",
          "Correct. Eleven plus eighteen is twenty-nine, exceeding FDA's 25-or-fewer company test.",
          "FDA issued the extension to defined small dispensers, not every company."
        ],
        "citation": "FDA DSCSA Small-Dispenser Exemption (issued Aug. 6, 2026; through Nov. 27, 2027)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
      },
      {
        "question": "A dispensary expects to qualify for FDA's 2026–27 exemption from certain enhanced DSCSA electronic tracing requirements. It receives a package suspected of falsified serialization. The manager says the exemption permits sale without further investigation. Which analysis is correct?",
        "choices": [
          "Every enhanced requirement is permanently repealed by the exemption",
          "An exemption makes product identification unimportant",
          "FDA's small-dispenser exemption automatically changes a suspect product into legitimate inventory",
          "The exemption is limited and does not relieve applicable authorized-partner, suspect-product quarantine/investigation and illegitimate-product notification safeguards"
        ],
        "answer": "D",
        "explanations": [
          "FDA did not repeal DSCSA as a whole.",
          "Product legitimacy and verification remain relevant.",
          "Exempt status does not prove the package is genuine.",
          "Correct. Exemptions concern specified enhanced tracing provisions and preserve other supply-chain safeguards."
        ],
        "citation": "FDA DSCSA Small-Dispenser Exemption (issued Aug. 6, 2026; through Nov. 27, 2027)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act"
      },
      {
        "question": "A pharmacy identifies an apparently falsified lot number Monday at 9 a.m. and quarantines the package as suspect. By Wednesday at 2 p.m., its investigation establishes the product is illegitimate. Which event starts the FDA 24-hour illegitimate-product notification clock?",
        "choices": [
          "The Wednesday determination of illegitimacy, not merely the earlier initial suspicion, begins the 24-hour reporting period",
          "The date the prescription was originally issued",
          "The next FDA national recall notice, whether or not one is issued",
          "One year after the package was quarantined"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Suspect quarantine occurs first; the 24-hour notification is triggered when the product is determined illegitimate.",
          "Prescription issuance does not govern FDA product-authenticity reporting.",
          "A formal recall is not a prerequisite for an illegitimate-product report.",
          "An annual delay is not the FDA reporting clock."
        ],
        "citation": "FDA — Notify FDA of Illegitimate Products",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products"
      },
      {
        "question": "A pharmacy receives a supposedly 'FDA-approved generic' that has an NDC but no approval record and arrives from a trading partner whose authorization cannot be confirmed. The pharmacy wants to dispense it because the price is lower. What should happen?",
        "choices": [
          "Accept it because any NDC proves approval and a low price proves authenticity",
          "Independently verify the trading partner's authorization, examine product authenticity and applicable approval status; NDC listing alone cannot settle those requirements",
          "Dispense after changing the NDC to resemble another approved drug",
          "Report the item as a valid 503B compounded product without further evaluation"
        ],
        "answer": "B",
        "explanations": [
          "NDC alone does not establish FDA approval or supply-chain compliance.",
          "Correct. Authorized supplier checks, product verification and genuine FDA approval are separate questions.",
          "Changing an identifier to disguise a product is inappropriate.",
          "503B status cannot simply be assigned by the receiving pharmacy."
        ],
        "citation": "FDA — NDC Product File Definitions (NDC listing not product approval)",
        "sourceUrl": "https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-product-file-definitions"
      },
      {
        "question": "A pharmacy receives an FDA safety recall for a batch of injectable medicine not yet assigned a recall class. Staff want to keep dispensing it until FDA announces whether it is Class I or II. What is best?",
        "choices": [
          "A class assignment is legally required before any product can be quarantined",
          "Unclassified recalls may be ignored because only Class I matters",
          "Apply the recall and quarantine/trace affected lots based on the notice without waiting for final classification",
          "Any unclassified recall allows the pharmacy to sell the product at half price"
        ],
        "answer": "C",
        "explanations": [
          "Recall actions need not wait for an assigned class.",
          "Other recall classifications and unclassified notices may require action.",
          "Correct. FDA recall status/classification is separate from prompt response to known affected inventory.",
          "Discounting recalled stock does not resolve safety risk."
        ],
        "citation": "FDA — Recalls Background and Class I–III Definitions",
        "sourceUrl": "https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions"
      },
      {
        "question": "A manufacturer removes drug stock from its own warehouse before any of those units have been marketed or released for sale. A pharmacist says this is automatically the same as recalling dispensed patient drugs. Which FDA distinction applies?",
        "choices": [
          "All factory removals are Class I recalls by definition",
          "Only patient-dispensed stock can ever be removed from distribution",
          "A market withdrawal always occurs when a product has not yet been marketed",
          "A stock recovery is removal or correction of product that has not been marketed or has not left the firm's direct control; it is distinct from a recall"
        ],
        "answer": "D",
        "explanations": [
          "Recall classification depends on actual marketed-product risks.",
          "Stock recovery can occur before product reaches commerce.",
          "Market withdrawals generally concern minor/no-violation situations, not this specific unmarketed stock definition.",
          "Correct. FDA's recall glossary defines stock recovery separately from a recall."
        ],
        "citation": "FDA — Regulatory Procedures Manual: Recall, Market Withdrawal, Stock Recovery",
        "sourceUrl": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/regulatory-procedures-manual/ch-11-glossary"
      },
      {
        "question": "A hospital needs a novel investigational drug for a clinical study before marketing approval. A pharmacist insists that filing an NDA is the ordinary first document authorizing the clinical trial. Which federal route fits?",
        "choices": [
          "An Investigational New Drug (IND) submission addresses human clinical investigations, whereas an NDA is a later marketing-approval application",
          "An NDC listing alone grants authority for all human trials",
          "A retail refill authorization is the same as a federal clinical-trial application",
          "A 510(k) medical device clearance is the routine drug IND substitute"
        ],
        "answer": "A",
        "explanations": [
          "Correct. An IND is the FDA investigational clinical-trial mechanism; NDA generally seeks marketing approval.",
          "NDC listing does not authorize clinical investigation.",
          "Prescription refills are distinct from drug-development regulatory submissions.",
          "Device 510(k) procedures are separate from an IND for drugs."
        ],
        "citation": "FDA — Investigational New Drug Application",
        "sourceUrl": "https://www.fda.gov/drugs/types-applications/investigational-new-drug-application-ind"
      },
      {
        "question": "A company wants to market an injectable therapeutic monoclonal antibody and cites the small-molecule generic ANDA process. Which application distinction is most important?",
        "choices": [
          "Every therapeutic monoclonal antibody receives an ANDA regardless of biological licensing",
          "The appropriate pathway generally involves a BLA or biosimilar application framework under applicable FDA biological-product authority rather than an ordinary small-molecule ANDA",
          "An NDC automatically grants biologic licensure",
          "An emergency-use letter grants indefinite routine commercial approval"
        ],
        "answer": "B",
        "explanations": [
          "FDA biological licensing does not automatically use the conventional small-molecule ANDA.",
          "Correct. BLAs and relevant biosimilar pathways govern many therapeutic biologics.",
          "NDC listing is not product licensure.",
          "EUA is a distinct conditional emergency authority."
        ],
        "citation": "FDA — Biologics License Applications (BLA)",
        "sourceUrl": "https://www.fda.gov/vaccines-blood-biologics/development-approval-process-cber/biologics-license-applications-bla-process-cber"
      },
      {
        "question": "A drug store receives a product labeled 'OTC' and the employee insists every lawful nonprescription drug must have an individual NDA approval. What is the correct federal distinction?",
        "choices": [
          "OTC designation makes every product exempt from safety and labeling rules",
          "An OTC product may only be marketed by compounding pharmacies under 503A",
          "Some OTC medicines are individually application-approved, while qualifying others may be marketed under an applicable OTC monograph without their own NDA",
          "All OTC monograph products are automatically Schedule II"
        ],
        "answer": "C",
        "explanations": [
          "OTC products remain subject to federal requirements.",
          "503A is a separate compounding framework.",
          "Correct. FDA has both OTC drug approval and monograph-based marketing pathways.",
          "OTC marketing is not a DEA controlled-schedule designation."
        ],
        "citation": "FDA — OTC Drug Monographs and the OTC Drug Review Process",
        "sourceUrl": "https://www.fda.gov/drugs/otc-drug-review-process-otc-drug-monographs"
      },
      {
        "question": "A drug store suspects a product is diverted and quarantines it under DSCSA. The supplier asks it to send the suspected inventory to a different store for immediate dispensing so it can be sold while the authenticity investigation continues. What is the pharmacist's best response?",
        "choices": [
          "Transfer all suspect products because the supplier promised a future refund",
          "Use a paper return authorization to override product quarantine",
          "Repackage the product with a new serialization label and continue selling",
          "Keep suspect product out of distribution while it is investigated, and follow the appropriate notification/disposition procedures if it is later determined illegitimate"
        ],
        "answer": "D",
        "explanations": [
          "A supplier promise does not remove DSCSA quarantine duties.",
          "Return paperwork does not automatically authorize further sale of suspect stock.",
          "Changing identifiers would not establish authenticity.",
          "Correct. DSCSA requires quarantine/investigation and additional actions after an illegitimate determination."
        ],
        "citation": "FDA — DSCSA Title II, FD&C Act §582 suspect/illegitimate product rules",
        "sourceUrl": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/title-ii-drug-quality-and-security-act"
      }
    ]
  }
});

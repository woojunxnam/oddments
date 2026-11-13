/* Chapter 30 — Original Exam Simulation Set 3; legal sources rechecked November 13, 2026. */
window.MPJE_CH30_BATCHES = window.MPJE_CH30_BATCHES || [];
window.MPJE_CH30_BATCHES.push({id:'set-3',title:'Simulation 3 — CE, MassPAT, Compounding and Inventory',questions:[
  {
    "id": "CH30-011",
    "type": "single",
    "question": "A Massachusetts pharmacist is preparing to renew personal pharmacist registration in December 2026. The pharmacist does not compound or immunize. The CE record shows: 2025 — 22 contact hours, including 18 home-study/mediated hours (including two pharmacy-law hours) and four live hours; 2026 — 24 contact hours, including 10 home-study hours, 14 live hours and at least two pharmacy-law hours. All courses are Board-acceptable; no more than eight hours were earned in a single day; no exception applies. Which conclusion is MOST accurate?",
    "choices": [
      "The pharmacist qualifies because 46 total contact hours exceed the 40-hour biennial requirement.",
      "The pharmacist qualifies because extra CE completed in 2026 can offset a 2025 shortage.",
      "The pharmacist does not qualify because only 19 of the 2025 hours can count toward that calendar year's minimum.",
      "The pharmacist does not qualify because completing more than 20 CE hours per year is prohibited."
    ],
    "correct": [
      "C"
    ],
    "feedback": [
      "247 CMR 4.03 requires at least 20 allowable hours in each calendar year; the two-year aggregate alone does not cure an annual shortfall.",
      "247 CMR 4.03 does not permit carrying surplus CE between calendar years.",
      "At most 15 of the 18 home-study hours count in 2025; with four live hours, only 19 hours count, one short of the annual minimum.",
      "The rule sets an annual CE minimum, not a maximum of 20 hours; the annual and home-study limits must both be satisfied."
    ],
    "sources": [
      [
        "247 CMR 4.03",
        "https://www.mass.gov/regulations/247-CMR-400-personal-registration-renewal-continuing-education-requirement"
      ]
    ]
  },
  {
    "id": "CH30-012",
    "type": "multi",
    "question": "A chain operates a Massachusetts community pharmacy and an out-of-state mail-order pharmacy. Both dispense controlled substances to Massachusetts patients. No reporting waivers apply and the prescriptions are valid. Which statements correctly describe MassPAT obligations under 105 CMR 700.012? SELECT ALL THAT APPLY.",
    "choices": [
      "A Massachusetts pharmacy generally must report a dispensed Schedule IV alprazolam prescription by the end of the next business day.",
      "An out-of-state pharmacy must report a Schedule IV tramadol prescription it delivers to a person in Massachusetts.",
      "A hospital must report morphine supplied to an inpatient under an inpatient medication order through the same outpatient pharmacy reporting rule.",
      "A community pharmacy must report covered outpatient dispensing even if the prescriber was exempt from checking MassPAT because the patient receives hospice care."
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "feedback": [
      "105 CMR 700.012(A)(1),(5) generally requires Schedules II-V dispensing reports by the end of the next business day.",
      "The reporting rule extends to out-of-state pharmacies delivering covered controlled substances to people in Massachusetts.",
      "105 CMR 700.012(A)(2) excludes dispensing pursuant to an inpatient medication order in a hospital.",
      "The hospice exception to a prescriber's mandatory MassPAT check does not waive the dispensing pharmacy's independent reporting duty."
    ],
    "sources": [
      [
        "105 CMR 700.012",
        "https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download"
      ],
      [
        "PMP Data Reporting",
        "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission"
      ]
    ]
  },
  {
    "id": "CH30-013",
    "type": "single",
    "question": "A Massachusetts pharmacy compounds two patient-specific nonsterile preparations compliant with USP <795>. Preparation X is a nonpreserved aqueous oral suspension (water activity 0.95). Preparation Y is a nonaqueous oral liquid (water activity 0.45). Neither has an applicable USP–NF compounded-preparation monograph or formulation-specific stability data. Ingredients remain unexpired; no factor requires a shorter beyond-use date (BUD). Which pair of MAXIMUM default BUDs and storage conditions is correct?",
    "choices": [
      "X: 14 days at controlled room temperature; Y: 90 days refrigerated or at controlled room temperature.",
      "X: 35 days refrigerated; Y: 90 days refrigerated or at controlled room temperature.",
      "X: 14 days refrigerated; Y: 180 days refrigerated or at controlled room temperature.",
      "X: 14 days refrigerated; Y: 90 days refrigerated or at controlled room temperature."
    ],
    "correct": [
      "D"
    ],
    "feedback": [
      "The aqueous nonpreserved preparation requires refrigeration for the 14-day default BUD.",
      "The 35-day refrigerated default applies to preserved aqueous preparations; X is nonpreserved.",
      "The 180-day default does not apply to nonaqueous oral liquids; their separate default BUD is 90 days.",
      "USP <795> Table 4 permits at most 14 days refrigerated for nonpreserved aqueous dosage forms and 90 days at room temperature or refrigerated for nonaqueous oral liquids, absent a shorter limit."
    ],
    "sources": [
      [
        "USP <795>",
        "https://www.usp.org/compounding/general-chapter-795"
      ]
    ]
  },
  {
    "id": "CH30-014",
    "type": "multi",
    "question": "A Massachusetts community pharmacy offers routine vaccinations under valid standing orders. A 55-year-old patient requests an indicated recombinant zoster vaccine. A pharmacist and a licensed pharmacy technician with all required immunizer training, CPR and competency qualifications are on duty. There are no contraindications, and state policy authorizes the vaccine. Which actions comply with Massachusetts requirements? SELECT ALL THAT APPLY.",
    "choices": [
      "After the pharmacist counsels the patient and selects the vaccine, the qualified technician may physically prepare and administer it with pharmacist approval and direct supervision.",
      "Before administering the recombinant zoster vaccine, the pharmacy must review the Massachusetts Immunization Information System (MIIS) for prior administration.",
      "A pharmacy technician trainee may administer the vaccine if the trainee completes the same course and receives direct pharmacist supervision.",
      "The Vaccine Information Statement may be provided immediately after administration if the patient consented beforehand."
    ],
    "correct": [
      "A",
      "B"
    ],
    "feedback": [
      "MA Board Policy 2023-02 permits a qualifying licensed technician to physically prepare and administer a vaccine after pharmacist counseling and selection, with approval and direct supervision.",
      "Policy 2023-02 requires pre-administration MIIS review for vaccines other than influenza and COVID-19; recombinant zoster vaccine is covered.",
      "The policy excludes technician trainees from vaccine administration; training alone does not grant trainee authority.",
      "The applicable VIS must be given before vaccination, not afterward, notwithstanding consent."
    ],
    "sources": [
      [
        "MA Policy 2023-02",
        "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download"
      ],
      [
        "CDC VIS",
        "https://www.cdc.gov/vaccines/hcp/vis/about/index.html"
      ]
    ]
  },
  {
    "id": "CH30-015",
    "type": "single",
    "question": "During a biennial controlled-substance inventory, a Massachusetts retail pharmacy finds: an opened Schedule II oxycodone bottle with 42 tablets; an opened 2,000-tablet Schedule III bottle with approximately 1,250 tablets; an opened 1,000-tablet Schedule IV bottle with approximately 400 tablets; and ten expired Schedule II tablets segregated for reverse distribution. The pharmacy maintains its required Schedule II perpetual inventory. Which inventory procedure is MOST appropriate under federal and Massachusetts requirements?",
    "choices": [
      "Exactly count Schedule II and Schedule IV; estimate Schedule III; remove the expired Schedule II from the perpetual inventory.",
      "Exactly count Schedule II and Schedule III; the Schedule IV quantity may be estimated; include expired Schedule II tablets in inventory and perpetual reconciliation.",
      "Estimate all opened bottles using electronic stock balances; include expired Schedule II only once the reverse distributor receives it.",
      "Exactly count every opened bottle; secure expired Schedule II separately and exclude it from perpetual reconciliation."
    ],
    "correct": [
      "B"
    ],
    "feedback": [
      "An opened Schedule III container with more than 1,000 tablets requires an exact count; expired Schedule II stock remains subject to control until properly transferred/disposed.",
      "21 CFR 1304.11(e)(6) requires exact counts for Schedule II and for opened Schedule III-V containers with more than 1,000 tablets/capsules; estimation may be used for the smaller opened Schedule IV container. 247 CMR 9.21 retains expired Schedule II in perpetual reconciliation.",
      "Electronic balances do not replace federally required actual counts, and expired drugs remain on hand until proper transfer/disposal.",
      "Exact-counting all containers is acceptable, but excluding expired Schedule II stock from the perpetual reconciliation is not permitted under 247 CMR 9.21."
    ],
    "sources": [
      [
        "21 CFR 1304.11",
        "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
      ],
      [
        "247 CMR 9.21",
        "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      ]
    ]
  }
]});

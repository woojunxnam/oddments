/* Exact historical snapshots for explicitly verified bank signatures. Never a blanket compatibility whitelist. */
window.MPJE_CH30_BANK_REVISIONS = {
  "schema": "MPJE_CH30_BANK_REVISIONS",
  "reviewedAt": "2026-11-22",
  "targets": {
    "MPJE_CH30_FORM_C_MOCK": {
      "currentSignature": "236a05d2",
      "priorSignatures": [
        "74d451e6"
      ],
      "archivedQuestionIds": [
        "E30-342"
      ],
      "excludedQuestionIds": [],
      "reasons": {
        "D016": "The earlier question did not specify formal import entry or exclude bond exceptions, so its unconditional bond requirement was not established.",
        "D067": "The earlier question gave only the original bottle size; it did not establish that more than 1,000 Schedule IV tablets remained at inventory."
      }
    },
    "MPJE_CH30_FORM_D_MOCK": {
      "currentSignature": "6c908108",
      "priorSignatures": [
        "234f9a2a"
      ],
      "archivedQuestionIds": [
        "D007",
        "D010",
        "D015",
        "D016",
        "D018",
        "D022",
        "D029",
        "D031",
        "D067"
      ],
      "excludedQuestionIds": [
        "D016",
        "D067"
      ],
      "reasons": {
        "D016": "The earlier question did not specify formal import entry or exclude bond exceptions, so its unconditional bond requirement was not established.",
        "D067": "The earlier question gave only the original bottle size; it did not establish that more than 1,000 Schedule IV tablets remained at inventory."
      }
    },
    "MPJE_CH30_MIXED_MOCK_FORMS": {
      "currentSignature": "96e7e972",
      "priorSignatures": [
        "48ec9bb4",
        "77edd81d"
      ],
      "archivedQuestionIds": [
        "E30-342",
        "D007",
        "D010",
        "D015",
        "D016",
        "D018",
        "D022",
        "D029",
        "D031",
        "D067",
        "E30-190"
      ],
      "excludedQuestionIds": [
        "D016",
        "D067"
      ],
      "reasons": {
        "D016": "The earlier question did not specify formal import entry or exclude bond exceptions, so its unconditional bond requirement was not established.",
        "D067": "The earlier question gave only the original bottle size; it did not establish that more than 1,000 Schedule IV tablets remained at inventory."
      },
      "snapshotsBySignature": {
        "77edd81d": {
          "E30-190": {
            "id": "E30-190",
            "set": 38,
            "area": 4,
            "kind": "multi",
            "topicKey": "sterile-hazardous-compounding",
            "topic": "USP <797> Category 2 nonhazardous sterile IV bag: ISO-classified suite versus SCA and tested BUD limits",
            "stem": "A Massachusetts hospital pharmacy aseptically compounds a NONHAZARDOUS Category 2 IV preparation from only sterile manufactured components. It has a qualified ISO Class 5 laminar airflow PEC in a properly maintained ISO Class 7 positive-pressure buffer room with an ISO Class 8 anteroom, and suitable personnel/monitoring. No sterility test is performed, stability data support at least 10 days under refrigeration, and no component imposes a shorter BUD. Under the currently official USP <797>, which statements are correct? SELECT ALL THAT APPLY.",
            "choices": [
              {
                "text": "The stated ISO 5 PEC in an appropriate classified buffer/anteroom cleanroom suite can support Category 2 compounding when other <797> requirements are satisfied.",
                "why": "Correct. The normal Category 2 nonhazardous aseptic-compounding configuration is an ISO 5 PEC in a properly classified cleanroom suite (e.g., ISO 7 buffer and ISO 8 anteroom). Facility and personnel/EM requirements still apply."
              },
              {
                "text": "Moving the ISO 5 hood to a nonclassified segregated compounding area automatically retains all Category 2 BUDs because ISO 5 primary airflow alone determines category eligibility.",
                "why": "Incorrect. Category 2 preparation requires the appropriate classified cleanroom environment; an unclassified SCA generally supports only Category 1 and its shorter BUD limits under USP <797>. ISO 5 primary control by itself does not make an SCA an ISO-classified Category 2 suite."
              },
              {
                "text": "For an aseptically prepared Category 2 CSP containing only sterile starting components and no sterility test, a BUD of up to four days at controlled room temperature or ten days refrigerated may be assigned when supported by stability and all other conditions.",
                "why": "Correct. USP <797> §14.3/Table 12 gives these maximum BUDs for this particular sterile-starting-component, aseptic, untested Category 2 formulation. Shorter stability limits would supersede them; not all Category 2 formulations share these values."
              },
              {
                "text": "Because the product is Category 2, it always requires completed sterility testing before any BUD can be assigned, even for a short BUD.",
                "why": "Incorrect. USP <797> includes explicit Category 2 maximum BUDs WITHOUT sterility testing for specified sterile-component cases. Longer assigned BUDs or other category formulations may have separate testing requirements, but sterility testing is not universally mandatory for every Category 2 CSP."
              }
            ],
            "correct": [
              "A",
              "C"
            ],
            "citation": "Official USP <797> §§4.1 and 14.3/Table 13 (revision official Nov. 1, 2023); USP <797> official FAQs updated Dec. 11, 2023, Q181 and room-classification guidance; 247 CMR 9.01(3)",
            "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
            "verified": "2026-11-17",
            "note": "Category 2 nonhazardous sterile CSPs require a properly classified cleanroom suite and ISO 5 PEC. From sterile components without sterility testing, maxima are four days at room temperature or ten days refrigerated when stability supports them. Citation corrected from Table 12 to Table 13 (Category 2 BUDs), confirmed by official Massachusetts Board sterile compounding inspection template, item 73.4 and 73.5; Table 12 applies to Category 1. No stem, choice, key, or practice revision changed."
          }
        }
      }
    }
  },
  "snapshots": {
    "E30-342": {
      "id": "E30-342",
      "slotId": "C102",
      "area": 4,
      "kind": "single",
      "topic": "compounding",
      "stem": "A Massachusetts sterile compounding pharmacy formerly produced Category 2 NONHAZARDOUS CSPs under a validated ISO Class 5 primary engineering control (PEC) inside a properly classified cleanroom suite. After renovation, the same PEC is moved into an UNCLASSIFIED segregated compounding area (SCA) while all personnel qualifications remain current. Management proposes assigning the same Category 2 refrigerated BUDs as before solely because the hood still meets ISO Class 5. What is the best response?",
      "choices": [
        {
          "text": "Keep the old BUDs, since the ISO Class 5 primary airflow is the only relevant classification for every CSP category.",
          "why": "Incorrect. The surrounding environmental classification and location requirements matter; ISO 5 PEC status alone does not preserve every Category 2 environmental condition."
        },
        {
          "text": "Apply the old BUDs if staff have passed their competency evaluations, because trained staff replace the need for a classified buffer room.",
          "why": "Incorrect. Personnel competency is required but does not substitute for the facility's engineering and environmental standards."
        },
        {
          "text": "Requalify the changed facility and reassess category and BUD; an ISO 5 PEC in an SCA does not retain Category 2 BUDs automatically.",
          "why": "Correct. An ISO 5 PEC in an SCA is not the same environment as a classified cleanroom suite for default Category 2 limits; changes require qualification and reassessment."
        },
        {
          "text": "Use the maximal Category 2 BUD whenever preparations contain only sterile manufactured ingredients, regardless of room classification.",
          "why": "Incorrect. Sterile starting components and a certified PEC do not independently grant Category 2 BUD authority absent the required setting and controls."
        }
      ],
      "correct": [
        "C"
      ],
      "citation": "USP <797> §§4.1, 5, 14; USP <797> official FAQ (Dec. 2023); 247 CMR 9.01(3)",
      "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
      "verified": "2026-11-18",
      "legalHold": "CURRENT_USP797_NORMATIVE_CHAPTER_UNAVAILABLE_HOLD",
      "reviewStatus": "AUTHOR_DRAFT_PENDING_FINAL_OPTION_APPROVAL"
    },
    "D007": {
      "id": "D007",
      "slotId": "D007",
      "area": 1,
      "kind": "multi",
      "topic": "DSCSA official records request",
      "stem": "An appropriate state or federal official requests the transaction information, statement, and history received by a pharmacy to investigate an illegitimate prescription drug. Assume no applicable relief or special alternative deadline was set. What is required? SELECT ALL THAT APPLY.",
      "choices": [
        {
          "text": "The pharmacy must respond no later than two business days after the qualifying request.",
          "why": "Correct. Section 582(d)(1)(D) sets a two-business-day deadline unless an alternate reasonable time is determined based on the request."
        },
        {
          "text": "The pharmacy may defer a response until its ordinary annual inventory.",
          "why": "Incorrect. The statutory clock for a qualifying official request is much shorter."
        },
        {
          "text": "A written third-party storage arrangement removes the dispenser's legal duty to respond.",
          "why": "Incorrect. A recordkeeping service does not release the dispenser from its statutory obligations."
        },
        {
          "text": "The pharmacy must supply the applicable received tracing records, subject to statutory scope.",
          "why": "Correct. An appropriate official can request the transaction information, statement and history received from the prior owner."
        }
      ],
      "correct": [
        "A",
        "D"
      ],
      "citation": "21 U.S.C. §360eee-1(d)(1)(B),(D)",
      "url": "https://uscode.house.gov/us/usc/t21/s360eee-1/",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_SOURCE_CHECK_PASS_NEEDS_FINAL_LEGAL_RELEASE_GATE",
      "legalHold": null,
      "revision": 1
    },
    "D010": {
      "id": "D010",
      "slotId": "D010",
      "area": 1,
      "kind": "single",
      "topic": "FDA EUA patient scope",
      "stem": "An inpatient team proposes Gohibic (vilobelimab) under its COVID-19 EUA for a hospitalized adult whose invasive mechanical ventilation began 62 hours earlier. The FDA authorization describes initiation within 48 hours after ventilation or ECMO begins. No other lawful access route is established. What should the pharmacist conclude?",
      "choices": [
        {
          "text": "It is FDA-approved for ventilated adults.",
          "why": "Incorrect. The cited FDA COVID-19 pathway is an EUA, not general approval without a time condition."
        },
        {
          "text": "A high-risk adult status alone substitutes for the EUA's ventilation-time condition.",
          "why": "Incorrect. The EUA imposes a timing window beyond patient age and hospitalization."
        },
        {
          "text": "Initiation at 62 hours is outside this EUA's 48-hour window.",
          "why": "Correct. FDA lists Gohibic EUA use for hospitalized adults when initiated within 48 hours of starting IMV or ECMO."
        },
        {
          "text": "The FDA EUA starts the 48-hour clock at the pharmacy's first purchase of Gohibic.",
          "why": "Incorrect. The clock refers to the patient's start of invasive mechanical ventilation or ECMO."
        }
      ],
      "correct": [
        "C"
      ],
      "citation": "21 U.S.C. §360bbb-3; FDA Gohibic authorized use, April 2026 amendment",
      "url": "https://www.fda.gov/drugs/emergency-preparedness-drugs/emergency-use-authorizations-drugs-and-non-vaccine-biological-products",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_SOURCE_CHECK_PASS_NEEDS_FINAL_LEGAL_RELEASE_GATE",
      "legalHold": null,
      "revision": 1
    },
    "D015": {
      "id": "D015",
      "slotId": "D015",
      "area": 1,
      "kind": "single",
      "topic": "503A API quality",
      "stem": "A 503A pharmacy compounds from an eligible bulk substance with a valid USP monograph. The bulk supplier's manufacturing establishment is FDA-registered, but the shipment has NO valid certificate of analysis. Assume all other conditions are met. Which federal 503A requirement is still unsatisfied?",
      "choices": [
        {
          "text": "The compound requires its own FDA-approved NDA.",
          "why": "Incorrect. Eligible patient-specific 503A preparations may qualify for statutory exemptions from new drug approval, subject to 503A conditions."
        },
        {
          "text": "The source substance must be in a DEA Schedule II container.",
          "why": "Incorrect. Drug scheduling does not supply the missing 503A documentation condition."
        },
        {
          "text": "The substance must come from an overseas manufacturer rather than a registered domestic establishment.",
          "why": "Incorrect. FDA registration and applicable quality requirements matter, not a blanket foreign-source requirement."
        },
        {
          "text": "The bulk substance must be accompanied by a valid certificate of analysis.",
          "why": "Correct. Section 503A bulk-substance conditions require a valid COA in addition to eligibility and manufacturing-establishment registration."
        }
      ],
      "correct": [
        "D"
      ],
      "citation": "FD&C Act §503A(b)(1)(A)(i), 21 U.S.C. §353a(b)(1)(A)(i); FDA 503A bulk drug substances",
      "url": "https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503a-fdc-act",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_SOURCE_CHECK_PASS_NEEDS_FINAL_LEGAL_RELEASE_GATE",
      "legalHold": null,
      "revision": 1
    },
    "D016": {
      "id": "D016",
      "slotId": "D016",
      "area": 1,
      "kind": "single",
      "topic": "FDA import enforcement policy",
      "stem": "COMMERCIAL IMPORT FILE\nA U.S. pharmacy chain intends to import a medicine made at an FDA-registered foreign plant in compliance with its U.S.-approved NDA. The importer argues that because both conditions are met, no separate import-entry filing is necessary. What federal import procedure still applies?",
      "choices": [
        {
          "text": "The pharmacy license substitutes for import entry.",
          "why": "Incorrect. State pharmacy licensure does not replace federal customs import-entry procedures."
        },
        {
          "text": "Manufacturer registration eliminates the entry bond and notice.",
          "why": "Incorrect. Facility registration and lawful product approval do not remove import entry reporting requirements."
        },
        {
          "text": "Submit an entry notice and bond pending FDA admissibility review.",
          "why": "Correct. FDA describes notice of entry and entry bond under customs procedures while FDA reviews admissibility of imported regulated goods."
        },
        {
          "text": "A personal traveler's import policy governs this corporate shipment.",
          "why": "Incorrect. This is commercial importation rather than a noncommercial personal import."
        }
      ],
      "correct": [
        "C"
      ],
      "citation": "21 U.S.C. §381(a); FDA import requirements for FDA-approved human drug products",
      "url": "https://www.fda.gov/industry/fda-basics-industry/what-must-i-do-import-human-drug-product-has-been-approved-fda-us",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_SOURCE_CHECK_PASS_NEEDS_FINAL_LEGAL_RELEASE_GATE",
      "legalHold": null,
      "revision": 1
    },
    "D018": {
      "id": "D018",
      "slotId": "D018",
      "area": 1,
      "kind": "single",
      "topic": "OSHA HCS exemption",
      "stem": "Under OSHA's Hazard Communication Standard, which drug presentation fits its express 'solid, final form for direct administration to the patient' exemption?",
      "choices": [
        {
          "text": "An intact finished tablet intended to be handed directly to the patient for administration.",
          "why": "Correct. 29 CFR 1910.1200(b)(6)(vii) excepts a covered drug in solid final form for direct patient administration; other rules may still govern it."
        },
        {
          "text": "An antineoplastic powder transferred into open containers for staff mixing.",
          "why": "Incorrect. Open powder handling is not an intact solid finished tablet for direct patient administration."
        },
        {
          "text": "A drug tablet manufactured specifically to be crushed by employees before routine administration.",
          "why": "Incorrect. OSHA explains that tablets intended for employee crushing before administration are not in final form under this exemption."
        },
        {
          "text": "A concentrated hazardous-drug solution being diluted by a technician for infusion.",
          "why": "Incorrect. A liquid requiring manipulation is outside the stated solid-final-form exemption."
        }
      ],
      "correct": [
        "A"
      ],
      "citation": "29 CFR 1910.1200(b)(6)(vii); OSHA Hospital Pharmacy HCS eTool",
      "url": "https://www.osha.gov/etools/hospitals/pharmacy/hazard-communication-standard",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_SOURCE_CHECK_PASS_NEEDS_FINAL_LEGAL_RELEASE_GATE",
      "legalHold": null,
      "revision": 1
    },
    "D022": {
      "id": "D022",
      "slotId": "D022",
      "area": 1,
      "kind": "single",
      "topic": "em_repeat_60day",
      "stem": "Two sterile-compounding environmental-monitoring reports from the SAME ISO Class 7 room show action-level results on October 1 and November 15, 2026. The samples were from different sites and were not consecutive monitoring events. What additional response does Massachusetts Board Policy 2026-03 expressly require?",
      "choices": [
        {
          "text": "Engage a microbiologist after repeat action-level results in the same ISO area within 60 days.",
          "why": "Correct. The policy mandates a microbiologist for repeat EM action-level results in the same ISO area within 60 days, consecutive or non-consecutive."
        },
        {
          "text": "Engage a microbiologist only when repeat samples occur at the exact same site on consecutive dates.",
          "why": "Incorrect. The 60-day rule applies to the same ISO classified AREA, not only the identical surface and not only consecutive samples."
        },
        {
          "text": "Restart the monitoring clock because the two results were not consecutive.",
          "why": "Incorrect. The express language covers both consecutive and non-consecutive repeats within the specified time."
        },
        {
          "text": "Postpone microbiologist review until at least three action-level samples have occurred.",
          "why": "Incorrect. The policy triggers additional microbiologist engagement with a qualifying repeat; a third action result is not necessary."
        }
      ],
      "correct": [
        "A"
      ],
      "citation": "Board Policy 2026-03 §III(G) (repeat action-level EM results within 60 days)",
      "url": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_OFFICIAL_SOURCE_CHECK_PENDING_RELEASE_FREEZE",
      "legalHold": null,
      "revision": 4
    },
    "D029": {
      "id": "D029",
      "slotId": "D029",
      "area": 1,
      "kind": "single",
      "topic": "auto_validation",
      "stem": "A 503A pharmacy considers an automated nonsterile compounder with no documented FDA approval. What does the Massachusetts Board's November 2025 memorandum require the pharmacy to check?",
      "choices": [
        {
          "text": "Reject it because every device requires FDA clearance.",
          "why": "Incorrect. The memorandum permits a documented manufacturer-validation pathway where FDA approval is not required or applicable."
        },
        {
          "text": "Check FDA approval requirements or documented manufacturer validation for the device.",
          "why": "Correct. The Board memo asks the pharmacy to assess FDA approval status or other manufacturer validation documentation for nonsterile compounding."
        },
        {
          "text": "Use the device because a vendor advertises it as 'automated,' without checking validation.",
          "why": "Incorrect. Marketing claims alone do not satisfy the pharmacy's documentation responsibility."
        },
        {
          "text": "Rely solely on a pharmacist's current license instead of reviewing device validation.",
          "why": "Incorrect. Pharmacist credentials do not replace equipment validation and compounding-quality requirements."
        }
      ],
      "correct": [
        "B"
      ],
      "citation": "MA Board Memorandum 2025-11-06: Automated Non-Sterile Compounding Devices ¶1",
      "url": "https://www.mass.gov/doc/automated-non-sterile-compounding-devices-pdf/download",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_OFFICIAL_SOURCE_CHECK_PENDING_RELEASE_FREEZE",
      "legalHold": null,
      "revision": 3
    },
    "D031": {
      "id": "D031",
      "slotId": "D031",
      "area": 1,
      "kind": "single",
      "topic": "auto_cleanability",
      "stem": "A nonsterile automated compounder handles a penicillin formulation, then an unrelated drug. Residue cannot be removed from an internal channel by any validated cleaning method. What must the pharmacy establish before sequential use?",
      "choices": [
        {
          "text": "Continue production when the same trained technician operates both batches.",
          "why": "Incorrect. The memo requires confirmation that the device is readily cleanable; a consistent operator does not replace residue controls."
        },
        {
          "text": "Use the manufacturer's marketing statement of accuracy to establish drug-residue clearance.",
          "why": "Incorrect. Accuracy claims do not demonstrate cleanability or absence of cross-contamination."
        },
        {
          "text": "Resolve whether the machine is cleanable enough to minimize drug cross-contamination.",
          "why": "Correct. The Board explicitly requires pharmacies to confirm device cleanability to minimize cross-contamination."
        },
        {
          "text": "Assign a shorter beyond-use date to the second product and skip the cleaning question.",
          "why": "Incorrect. A changed BUD does not remedy possible cross-contamination introduced by uncleanable equipment."
        }
      ],
      "correct": [
        "C"
      ],
      "citation": "Board Memorandum 2025-11-06: Automated Non-Sterile Compounding Devices ¶3; 247 CMR 9.01(3)",
      "url": "https://www.mass.gov/doc/automated-non-sterile-compounding-devices-pdf/download",
      "verified": "2026-11-18",
      "reviewStatus": "AUTHOR_OFFICIAL_SOURCE_CHECK_PENDING_RELEASE_FREEZE",
      "legalHold": null,
      "revision": 3
    },
    "D067": {
      "id": "D067",
      "slotId": "D067",
      "area": 3,
      "kind": "single",
      "topic": "Federal scheduled-drug counting",
      "stem": "At the federal biennial inventory, the pharmacy has a partially filled Schedule IV bottle originally containing 1,500 tablets and a partially filled Schedule II bottle originally containing 100 tablets. Which counting rule applies?",
      "choices": [
        {
          "text": "Estimate the remaining count in both.",
          "why": "Schedule II quantities require an exact count."
        },
        {
          "text": "Estimate Schedule IV because it is not Schedule II, and count Schedule II exactly.",
          "why": "A Schedule III–V container holding more than 1,000 tablets or capsules requires an exact count."
        },
        {
          "text": "Exact-count both the Schedule II and the over-1,000-tablet Schedule IV bottles.",
          "why": "Schedule II always requires an exact count; the >1,000 tablet Schedule IV container also does."
        },
        {
          "text": "Count only unopened bottles.",
          "why": "The inventory must include all controlled substances on hand, including opened containers."
        }
      ],
      "correct": [
        "C"
      ],
      "citation": "21 CFR 1304.11(e)(6)(i)–(ii)",
      "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11",
      "verified": "2026-11-20",
      "reviewStatus": "AUTHOR_PRIMARY_SOURCE_CHECKED_NO_EXTERNAL_CERTIFICATION",
      "legalHold": null,
      "revision": 1
    },
    "E30-190": {
      "id": "E30-190",
      "set": 38,
      "area": 4,
      "kind": "multi",
      "topicKey": "sterile-hazardous-compounding",
      "topic": "USP <797> Category 2 nonhazardous sterile IV bag: ISO-classified suite versus SCA and tested BUD limits",
      "stem": "A Massachusetts hospital pharmacy aseptically compounds a NONHAZARDOUS Category 2 IV preparation from only sterile manufactured components. It has a qualified ISO Class 5 laminar airflow PEC in a properly maintained ISO Class 7 positive-pressure buffer room with an ISO Class 8 anteroom, and suitable personnel/monitoring. No sterility test is performed, stability data support at least 10 days under refrigeration, and no component imposes a shorter BUD. Under the currently official USP <797>, which statements are correct? SELECT ALL THAT APPLY.",
      "choices": [
        {
          "text": "The stated ISO 5 PEC in an appropriate classified buffer/anteroom cleanroom suite can support Category 2 compounding when other <797> requirements are satisfied.",
          "why": "Correct. The normal Category 2 nonhazardous aseptic-compounding configuration is an ISO 5 PEC in a properly classified cleanroom suite (e.g., ISO 7 buffer and ISO 8 anteroom). Facility and personnel/EM requirements still apply."
        },
        {
          "text": "Moving the ISO 5 hood to a nonclassified segregated compounding area automatically retains all Category 2 BUDs because ISO 5 primary airflow alone determines category eligibility.",
          "why": "Incorrect. Category 2 preparation requires the appropriate classified cleanroom environment; an unclassified SCA generally supports only Category 1 and its shorter BUD limits under USP <797>. ISO 5 primary control by itself does not make an SCA an ISO-classified Category 2 suite."
        },
        {
          "text": "For an aseptically prepared Category 2 CSP containing only sterile starting components and no sterility test, a BUD of up to four days at controlled room temperature or ten days refrigerated may be assigned when supported by stability and all other conditions.",
          "why": "Correct. USP <797> §14.3/Table 13 gives these maximum BUDs for this particular sterile-starting-component, aseptic, untested Category 2 formulation. Shorter stability limits would supersede them; not all Category 2 formulations share these values."
        },
        {
          "text": "Because the product is Category 2, it always requires completed sterility testing before any BUD can be assigned, even for a short BUD.",
          "why": "Incorrect. USP <797> includes explicit Category 2 maximum BUDs WITHOUT sterility testing for specified sterile-component cases. Longer assigned BUDs or other category formulations may have separate testing requirements, but sterility testing is not universally mandatory for every Category 2 CSP."
        }
      ],
      "correct": [
        "A",
        "C"
      ],
      "citation": "Official USP <797> §§4.1 and 14.3/Table 13 (revision official Nov. 1, 2023); USP <797> official FAQs updated Dec. 11, 2023, Q181 and room-classification guidance; 247 CMR 9.01(3)",
      "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
      "verified": "2026-11-17",
      "note": "Category 2 nonhazardous sterile CSPs require a properly classified cleanroom suite and ISO 5 PEC. From sterile components without sterility testing, maxima are four days at room temperature or ten days refrigerated when stability supports them. Citation corrected from Table 12 to Table 13 (Category 2 BUDs), confirmed by official Massachusetts Board sterile compounding inspection template, item 73.4 and 73.5; Table 12 applies to Category 1. No stem, choice, key, or practice revision changed."
    }
  }
};

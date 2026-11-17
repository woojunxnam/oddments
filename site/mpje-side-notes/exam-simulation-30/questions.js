/* Chapter 30 original MPJE scenarios (not secure exam questions).
   Area = primary 2026 NABP MPJE Competency Statement for balanced study only; multi-domain cases are classified by their main tested task.
   Authoring policy for EVERY NEXT five-question set: Area 1 x1, Area 2 x2, Area 3 x1, Area 4 x1; 3 SBA + 2 SATA; unique IDs, official-source verification, full A-D rationales.
   Random 10 sampling target: Area 1 x2, Area 2 x3, Area 3 x3, Area 4 x2; no within-set duplicates.
   Pre-2027 areas will be superseded in NABP exam blueprint starting March 1, 2027; do not silently relabel the legacy scheme. */
window.MPJE_CH30_QUESTIONS = [
  {
    "id": "E30-001",
    "set": 1,
    "area": 1,
    "kind": "single",
    "topic": "CDTM qualifications",
    "topicKey": "cdtm",
    "stem": "A Massachusetts pharmacist earned a PharmD in 2022 and has practiced as a licensed pharmacist for four years. The pharmacist holds an unrestricted Massachusetts license, maintains the required liability insurance, and wishes to enter a FIRST CDTM agreement in November 2026. The Board has not determined that any education or residency is equivalent to five years of experience. Which statement is MOST accurate?",
    "choices": [
      {
        "text": "The pharmacist qualifies because a PharmD automatically replaces the experience requirement.",
        "why": "The PharmD exception in 247 CMR 16.02(1)(c) applies only when the pharmacist entered a CDTM agreement on or before June 30, 2017."
      },
      {
        "text": "The pharmacist qualifies once the supervising physician signs the agreement.",
        "why": "Physician agreement and other CDTM conditions cannot replace the pharmacist's separate statutory qualification."
      },
      {
        "text": "The pharmacist does not yet qualify absent five years of licensed experience or a recognized exception.",
        "why": "247 CMR 16.02(1)(c) requires five years of licensed experience unless a precisely defined historic PharmD or Board-recognized equivalent qualification applies."
      },
      {
        "text": "The pharmacist can qualify immediately by completing five additional CDTM CE hours.",
        "why": "Five additional relevant contact hours are an annual requirement during an agreement, not a substitute for the five-year qualification."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 16.02(1)(c),(e)",
    "url": "https://www.mass.gov/regulations/247-CMR-1600-collaborative-drug-therapy-management",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-002",
    "set": 1,
    "area": 1,
    "kind": "multi",
    "topic": "Certified technician scope",
    "topicKey": "technician-scope",
    "stem": "A certified Massachusetts pharmacy technician holds current Board-accepted certification. A pharmacist on duty approves the delegated task. Which activities may this technician legally perform? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Receive a new or omitted prescription detail from a prescriber without exercising professional judgment, when otherwise permitted by law.",
        "why": "247 CMR 8.04(4)(c) allows certified technicians, with pharmacist approval and identification, to receive permitted new or omitted prescription information not requiring professional judgment."
      },
      {
        "text": "Personally counsel a patient about a serious drug interaction after pharmacist review.",
        "why": "A technician cannot counsel or resolve a clinical conflict under 247 CMR 8.04(4)(e), regardless of prior pharmacist review."
      },
      {
        "text": "Transfer a Schedule VI prescription between pharmacies with pharmacist approval and under transfer rules.",
        "why": "247 CMR 8.04(4)(d) expressly authorizes this limited prescription-transfer function for certified pharmacy technicians."
      },
      {
        "text": "Perform final dispensing validation after the prescription passes an automated barcode check.",
        "why": "Final dispensing process validation remains a pharmacist function under 247 CMR 9.04(1); automation does not delegate it to a technician."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 8.04(4)(c)–(e); 247 CMR 9.04(1)",
    "url": "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-003",
    "set": 1,
    "area": 2,
    "kind": "single",
    "topic": "Counseling and final validation",
    "topicKey": "counseling-dur",
    "stem": "A Massachusetts patient picks up a chronic-medication refill and a newly prescribed inhaler. The patient declines counseling for the refill but accepts it for the inhaler. A pharmacist, pharmacy intern, and suitably trained pharmacy technician are on duty. Which workflow BEST complies with Massachusetts law?",
    "choices": [
      {
        "text": "The technician offers counseling for both drugs and personally counsels on the inhaler; the pharmacist validates.",
        "why": "A technician may relay the offer but may not provide the clinical counseling under 247 CMR 9.18(3)."
      },
      {
        "text": "The technician offers counseling for both drugs; the intern counsels on the inhaler; the pharmacist completes final validation.",
        "why": "247 CMR 9.18 permits a trained designee to offer counseling to each recipient and a pharmacist or pharmacy intern to counsel; 247 CMR 9.04(1) reserves final dispensing validation to the pharmacist."
      },
      {
        "text": "The technician offers counseling only for the inhaler; the intern counsels; the pharmacist validates.",
        "why": "247 CMR 9.18(1) requires offering counseling to each person receiving prescription medication, not just new prescriptions."
      },
      {
        "text": "The technician offers counseling for both; the intern counsels and completes the final dispensing validation.",
        "why": "An intern may counsel, but final dispensing validation must be completed by the licensed pharmacist."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.18(1)–(4); 247 CMR 9.04(1)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-004",
    "set": 1,
    "area": 4,
    "kind": "multi",
    "topic": "USP <800> sterile hazardous drug",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts facility prepares a sterile injectable antineoplastic drug designated hazardous under applicable NIOSH criteria. The drug requires manipulation and is subject to USP <800>. Which statements correctly describe sterile hazardous-drug compounding? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A sterile hazardous-drug preparation must be made in an externally vented containment primary engineering control providing ISO Class 5 or better air quality.",
        "why": "USP <800> requires an externally vented C-PEC with ISO Class 5 or better air quality for sterile hazardous drug manipulation."
      },
      {
        "text": "The containment secondary engineering control must maintain negative pressure compared with adjacent areas, including outside active compounding periods.",
        "why": "USP <800> requires continuous negative pressure for the appropriate containment secondary engineering control."
      },
      {
        "text": "Outdoor exhaust from the containment secondary engineering control must in every case pass through an additional HEPA filter.",
        "why": "Externally vented secondary room exhaust is required, but universal additional HEPA filtration of that outdoor exhaust is not the categorical USP <800> rule."
      },
      {
        "text": "A closed-system drug-transfer device must be used during every hazardous-drug compounding procedure.",
        "why": "USP <800> recommends a CSTD for hazardous-drug compounding rather than mandating it for every compounding procedure; administration standards differ."
      }
    ],
    "correct": [
      "A",
      "B"
    ],
    "citation": "USP <800> containment engineering controls and CSTD provisions",
    "url": "https://www.usp.org/compounding/general-chapter-hazardous-drugs-handling-healthcare",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-005",
    "set": 1,
    "area": 3,
    "kind": "single",
    "topic": "Controlled-drug pickup identification",
    "topicKey": "controlled-pickup-id",
    "stem": "A Massachusetts patient comes to pick up a valid Schedule II prescription but lacks government-issued identification. The pharmacist reasonably believes that refusing to dispense would cause serious hardship. No other identifier exemption applies. Which action is permitted if all other dispensing conditions are satisfied?",
    "choices": [
      {
        "text": "Dispense only after the prescriber orally confirms identity and authorizes pickup.",
        "why": "Prescriber confirmation does not, by itself, substitute for the documented hardship pathway in 247 CMR 9.04(14)."
      },
      {
        "text": "Document the serious-hardship reason and have the customer print a name and address and sign the reverse of the prescription or a prescription log.",
        "why": "247 CMR 9.04(14)(c) allows this alternative identification procedure if the serious-hardship criteria and documentation requirements are met."
      },
      {
        "text": "Dispense using the existing patient history without a hardship notation or signed log.",
        "why": "An established pharmacy relationship alone does not replace the state customer-identifier requirement."
      },
      {
        "text": "Refuse all Schedule II pickups without government identification, regardless of hardship.",
        "why": "247 CMR 9.04(14)(c) expressly recognizes a properly documented serious-hardship exception."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.04(14)(c)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-006",
    "set": 2,
    "area": 3,
    "kind": "single",
    "topic": "Out-of-state Schedule II partial fills",
    "topicKey": "cii-partial-fills",
    "stem": "A Rhode Island physician issues a valid methylphenidate Schedule II prescription for 60 tablets on November 4, 2026. The patient presents it to a Massachusetts pharmacy on November 8, requests a 20-tablet initial partial fill, and receives 20 tablets. On November 27, the patient requests the remaining 40 tablets from that SAME pharmacy. The initial patient-requested partial fill was documented, and all other requirements are met. What is the MOST accurate answer?",
    "choices": [
      {
        "text": "A new prescription is mandatory because completion must occur within 72 hours.",
        "why": "The 72-hour stock-shortage rule is different from the patient-requested partial-fill rules."
      },
      {
        "text": "The remaining 40 tablets may be dispensed because the initial and subsequent fills meet their respective deadlines.",
        "why": "105 CMR 721.055 requires initial presentation of an out-of-state Schedule II prescription within five calendar days and completion at the same pharmacy no later than 30 days after issuance, consistent with federal requirements."
      },
      {
        "text": "An out-of-state Schedule II prescription can never be partially filled in Massachusetts.",
        "why": "105 CMR 721.055 specifically provides for patient-requested partial fills of qualifying out-of-state Schedule II prescriptions."
      },
      {
        "text": "The prescriber must issue a new prescription merely because the patient requested a partial fill.",
        "why": "When properly documented and completed within the legal window, a patient-requested partial fill does not automatically require a new prescription."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "105 CMR 721.055(A)–(C); 21 CFR 1306.13",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-007",
    "set": 2,
    "area": 3,
    "kind": "multi",
    "topic": "Unfilled prescription transfers",
    "topicKey": "refills-transfers",
    "stem": "A patient asks a Massachusetts pharmacy to transfer several NEVER-FILLED prescriptions to another licensed Massachusetts pharmacy for INITIAL dispensing. Systems and pharmacist-to-pharmacist procedures otherwise comply with law. Which transfers are permitted? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A never-filled original electronic Schedule II prescription, transferred electronically once at the patient's request.",
        "why": "Board Policy 2023-10 and 21 CFR 1306.08 allow the one-time electronic transfer of an unfilled original EPCS for initial dispensing."
      },
      {
        "text": "A never-filled paper Schedule IV prescription scanned and sent as though it were a valid original electronic controlled-substance prescription.",
        "why": "Scanning a paper prescription into a computer does not transform it into EPCS; federal controlled paper originals are not transferable for initial filling under this provision."
      },
      {
        "text": "A never-filled oral Schedule VI prescription transferred under Massachusetts pharmacy transfer rules.",
        "why": "Policy 2023-10 permits initial-dispensing transfer of unfilled oral, paper, fax, and electronic Schedule VI prescriptions under state rules."
      },
      {
        "text": "An original electronic Schedule III prescription transferred to a second receiving pharmacy after it already underwent its one initial-dispensing transfer.",
        "why": "The EPCS initial-dispensing transfer permitted by 21 CFR 1306.08 is one-time, not unlimited."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Board Policy 2023-10; 21 CFR 1306.08",
    "url": "https://www.mass.gov/doc/2023-10-unfilled-prescriptions-pdf/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-008",
    "set": 2,
    "area": 2,
    "kind": "single",
    "topic": "Emergency oral Schedule II follow-up",
    "topicKey": "controlled-prescriptions",
    "stem": "A Massachusetts pharmacist receives a qualifying emergency oral prescription for a Schedule II medication and satisfies verification, documentation, quantity, and other legal requirements. The prescriber proposes sending the follow-up prescription within seven BUSINESS days. What is MOST appropriate?",
    "choices": [
      {
        "text": "Accept seven business days because Massachusetts rules displace the federal timetable.",
        "why": "A longer state deadline cannot override the stricter federal seven-day deadline in 21 CFR 1306.11(d)."
      },
      {
        "text": "Explain that federal law requires the compliant follow-up within seven CALENDAR days and requires emergency-order documentation.",
        "why": "21 CFR 1306.11(d) uses seven days, not business days; Massachusetts' separately worded timeframe does not eliminate the federal requirement."
      },
      {
        "text": "Require the follow-up in 72 hours because every emergency oral Schedule II order is a partial fill.",
        "why": "The 72-hour shortage partial-fill rule is not the emergency oral prescription follow-up deadline."
      },
      {
        "text": "Accept the plan without any follow-up because the pharmacist verified the prescriber.",
        "why": "Verification does not dispense with the required follow-up or the DEA notification required if follow-up is not received."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1306.11(d); 105 CMR 721.060",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-009",
    "set": 2,
    "area": 2,
    "kind": "multi",
    "topic": "CQI dispensing event",
    "topicKey": "quality-safety",
    "stem": "A Massachusetts community pharmacy dispenses the wrong strength. The patient has the medication but calls BEFORE taking any dose, and the pharmacist confirms the error. The patient is uninjured. Under the state's continuous quality improvement rules, which statements are true? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist must promptly notify the patient and provide correction directions and instructions to reduce negative impact.",
        "why": "247 CMR 15.03(1) requires prompt appropriate patient notification, correction instructions, and harm-minimization guidance."
      },
      {
        "text": "The pharmacist must initially document the quality-related event within 24 hours of learning of it.",
        "why": "247 CMR 15.03(2)(a) requires initial QRE documentation within 24 hours of discovery or notification."
      },
      {
        "text": "There is no QRE because the patient did not swallow the medication.",
        "why": "Incorrect dispensing received by the patient is a QRE even without ingestion or resulting injury."
      },
      {
        "text": "The pharmacist must notify the prescriber in EVERY case, irrespective of professional judgment.",
        "why": "The regulation requires prescriber notification when indicated in the pharmacist's professional judgment; it is not unconditional."
      }
    ],
    "correct": [
      "A",
      "B"
    ],
    "citation": "247 CMR 15.03(1)–(2), QRE patient notification and initial 24-hour record (official MA Board version dated Dec. 6, 2024); 247 CMR 15.02(1) CQI scope",
    "url": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download",
    "verified": "2026-11-17"
  },
  {
    "id": "E30-010",
    "set": 2,
    "area": 3,
    "kind": "single",
    "topic": "Schedule II–III 90-day supply",
    "topicKey": "controlled-quantity",
    "stem": "A Massachusetts pharmacist receives four otherwise valid new prescriptions, each requesting a 90-day supply. Assume no other patient, federal, or payer restriction bars the full quantity. Which prescription MAY be filled as one 90-day dispensing under Massachusetts law?",
    "choices": [
      {
        "text": "Methylphenidate, Schedule II, for ADHD.",
        "why": "M.G.L. c.94C §23(d) and Policy 2024-05 permit a 90-day supply of non-opioid Schedule II–III drugs, including stimulants, when otherwise lawful."
      },
      {
        "text": "Hydrocodone/acetaminophen, Schedule II, for chronic pain.",
        "why": "This opioid analgesic is outside the stated 90-day exceptions; the general 30-day Schedule II–III limit applies."
      },
      {
        "text": "Acetaminophen/codeine, Schedule III, for postoperative pain.",
        "why": "The Schedule III opioid is not a non-opioid or OUD-treatment exception; the 30-day limit applies."
      },
      {
        "text": "Buprenorphine transdermal analgesic patches, Schedule III, for chronic pain rather than opioid use disorder.",
        "why": "Buprenorphine products used for OUD have a special exception, but this analgesic use is not the OUD-treatment exception."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.94C §23(d); Board Policy 2024-05",
    "url": "https://www.mass.gov/news/policy-2024-05-schedules-ii-and-iii-quantity-limits",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-011",
    "set": 3,
    "area": 1,
    "kind": "single",
    "topic": "Biennial pharmacist CE",
    "topicKey": "licensure-ce",
    "stem": "A Massachusetts pharmacist seeks renewal in December 2026. The pharmacist does not compound or immunize and has no CE waiver. In 2025, the pharmacist earns 22 contact hours: 18 home-study/mediated hours (including two law hours) and four live hours. In 2026, the pharmacist earns 24 hours: ten home study and 14 live (including two law hours). Every activity is approved; no more than eight hours are earned on any one day. Which conclusion is MOST accurate?",
    "choices": [
      {
        "text": "The pharmacist qualifies because 46 earned hours exceed the biennial 40-hour requirement.",
        "why": "The 40-hour total does not override the minimum 20 allowable hours in EACH calendar year and the 15-home-study-hour annual cap."
      },
      {
        "text": "The pharmacist qualifies because the extra 2026 hours can compensate for a 2025 deficit.",
        "why": "247 CMR 4.03(5) does not allow CE hours to be carried between calendar years."
      },
      {
        "text": "The pharmacist does not qualify because only 19 allowable CE hours count in 2025.",
        "why": "Only 15 of 18 home-study hours count toward 2025's minimum, plus four live hours, for 19; the 2026 surplus does not cure this."
      },
      {
        "text": "The pharmacist does not qualify because no more than 20 hours may be earned per year.",
        "why": "Twenty hours is an annual MINIMUM, not a ceiling; the problem is the annual home-study limit."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 4.03(3)–(7)",
    "url": "https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-012",
    "set": 3,
    "area": 3,
    "kind": "multi",
    "topic": "MassPAT reporting",
    "topicKey": "masspat",
    "stem": "A Massachusetts community pharmacy and a nonresident mail-order pharmacy dispense controlled substances to Massachusetts patients. No reporting waiver applies. Which statements correctly distinguish MassPAT pharmacy reporting duties from prescriber query duties? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The Massachusetts pharmacy generally reports outpatient Schedule IV alprazolam dispensing by the end of the next business day.",
        "why": "105 CMR 700.012 and the DPH pharmacy reporting instructions require covered Schedule II–V dispensing reports within the applicable 24-hour or next-business-day deadline."
      },
      {
        "text": "The nonresident pharmacy reports a Schedule IV tramadol prescription mailed to a person in Massachusetts.",
        "why": "The reporting obligation extends to out-of-state pharmacies delivering covered prescriptions to Massachusetts residents."
      },
      {
        "text": "Morphine given to a hospitalized inpatient under an inpatient medication order must be reported as a retail outpatient fill.",
        "why": "105 CMR 700.012 excludes controlled substances dispensed pursuant to inpatient hospital medication orders from this pharmacy reporting requirement."
      },
      {
        "text": "A pharmacist still reports a covered outpatient dispensing even if the prescriber qualified for a hospice exemption from mandatory MassPAT lookup.",
        "why": "An exemption from a prescriber's obligation to query MassPAT does not by itself exempt the dispensing pharmacy from submitting data."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "105 CMR 700.012(A),(G)",
    "url": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-013",
    "set": 3,
    "area": 4,
    "kind": "single",
    "topic": "USP <795> BUD",
    "topicKey": "nonsterile-compounding",
    "stem": "A Massachusetts pharmacy compounds patient-specific nonsterile preparations under USP <795>: X is a NONPRESERVED aqueous oral suspension (water activity 0.95); Y is a nonaqueous oral liquid (water activity 0.45). There is no applicable USP–NF monograph or preparation-specific stability data, and no shorter BUD factor. Which pair matches the DEFAULT maximum beyond-use dates?",
    "choices": [
      {
        "text": "X: 14 days at controlled room temperature; Y: 90 days at room temperature or refrigerated.",
        "why": "X must be refrigerated under the default BUD; room temperature is not its default 14-day storage condition."
      },
      {
        "text": "X: 35 days refrigerated; Y: 90 days at room temperature or refrigerated.",
        "why": "Thirty-five days is the preserved aqueous category, not nonpreserved aqueous."
      },
      {
        "text": "X: 14 days refrigerated; Y: 180 days at room temperature or refrigerated.",
        "why": "The 180-day default applies to OTHER nonaqueous dosage forms, not nonaqueous oral liquids."
      },
      {
        "text": "X: 14 days refrigerated; Y: 90 days at room temperature or refrigerated.",
        "why": "USP <795> Table 4 gives 14 days refrigerated for nonpreserved aqueous preparations and 90 days at controlled room temperature or refrigerated for nonaqueous oral liquids."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "USP <795>, Section 10, Table 4",
    "url": "https://www.usp.org/compounding/general-chapter-795",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-014",
    "set": 3,
    "area": 2,
    "kind": "multi",
    "topic": "Vaccination workflow",
    "topicKey": "immunization",
    "stem": "A Massachusetts pharmacy vaccinates a 55-year-old against herpes zoster under an otherwise valid standing order. A qualified pharmacist is on duty; the patient is eligible and has no contraindication. Under the Massachusetts vaccine workflow and federal VIS requirements, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A properly qualified pharmacist may select, counsel about, and administer the vaccine under a valid applicable standing order.",
        "why": "MA vaccine administration authority and Board Policy 2023-02 permit a properly qualified pharmacist to vaccinate an eligible patient under the applicable standing order."
      },
      {
        "text": "The pharmacy must review the Massachusetts Immunization Information System (MIIS) before giving this non-influenza, non-COVID-19 vaccine.",
        "why": "Board Policy 2023-02 requires checking MIIS before vaccines other than influenza and COVID-19, including recombinant zoster vaccine."
      },
      {
        "text": "A pharmacy technician trainee may independently administer the vaccine after completing a short training course.",
        "why": "A trainee has no independent vaccination authority merely from training; pharmacist and technician authority and supervision have separate legal limits."
      },
      {
        "text": "The appropriate Vaccine Information Statement may be furnished after the injection if the patient already signed a consent form.",
        "why": "The Vaccine Information Statement must be provided before vaccination; consent does not replace the VIS delivery rule."
      }
    ],
    "correct": [
      "A",
      "B"
    ],
    "citation": "Board Policy 2023-02 (revised 2025); 42 USC 300aa-26",
    "url": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download",
    "verified": "2026-11-13",
    "note": "Revised from the original chat version to avoid treating the general technician scope regulation and vaccine-specific Board policy as interchangeable."
  },
  {
    "id": "E30-015",
    "set": 3,
    "area": 4,
    "kind": "single",
    "topic": "Federal inventory exact count",
    "topicKey": "controlled-inventory",
    "stem": "A Massachusetts retail pharmacy performs its biennial controlled-substance inventory and has: (1) an opened Schedule II oxycodone bottle with 42 tablets; (2) an opened 2,000-tablet Schedule III container holding about 1,250 tablets; (3) an opened 1,000-tablet Schedule IV container holding about 400 tablets; and (4) ten expired Schedule II tablets secured and awaiting reverse distribution. The pharmacy maintains a Schedule II perpetual inventory. Which method is MOST accurate?",
    "choices": [
      {
        "text": "Exactly count Schedule II and IV, estimate Schedule III, and remove expired Schedule II from perpetual records.",
        "why": "Federal law requires an exact count for an opened container of more than 1,000 Schedule III tablets; expired Schedule II stock remains inventoried."
      },
      {
        "text": "Exactly count Schedule II and the 2,000-tablet Schedule III container; estimate the Schedule IV container; retain expired Schedule II in inventory and reconciliation.",
        "why": "21 CFR 1304.11(e)(6) requires exact Schedule II counts and exact counts for opened Schedule III–V containers exceeding 1,000 tablets/capsules; 247 CMR 9.21 requires the expired Schedule II stock to stay in perpetual inventory and reconciliation."
      },
      {
        "text": "Estimate all opened bottles based on electronic data and add expired Schedule II only when the reverse distributor receives them.",
        "why": "Electronic records do not remove the federal exact-count rules, and the expired product remains controlled stock until transferred or destroyed."
      },
      {
        "text": "Exactly count every opened bottle but exclude expired Schedule II from perpetual reconciliation.",
        "why": "Exact counting above minimum is allowed, but 247 CMR 9.21(10) includes expired and pending-destruction Schedule II stock in inventory duties."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1304.11(e)(6); 247 CMR 9.21(8),(10)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-016",
    "set": 4,
    "area": 1,
    "kind": "single",
    "topic": "Pharmacist break",
    "topicKey": "workforce-supervision",
    "stem": "A Massachusetts community pharmacy has only one pharmacist. During a scheduled 25-minute meal break, the pharmacist remains on the premises but outside the prescription area. Before leaving, the pharmacist has prepared, visually checked and performed prospective DUR on a NEW prescription for a patient. The pharmacy has compliant break policies and preserves drug security. Which pickup procedure is MOST consistent with 247 CMR 9.19(17)?",
    "choices": [
      {
        "text": "The patient may pick it up during the break without additional records because the pharmacist checked it.",
        "why": "The special new-prescription exception requires a log, including the patient's phone number, and post-break follow-up counseling as appropriate."
      },
      {
        "text": "The patient cannot pick up any new prescription until the pharmacist physically returns to the prescription area.",
        "why": "A narrowly specified exception permits release of a previously prepared, visibly checked, DUR-reviewed new prescription during a compliant temporary absence."
      },
      {
        "text": "The new prescription may be released with a transaction log including the patient's phone number; the pharmacist must call afterward within a reasonable time about pertinent counseling.",
        "why": "247 CMR 9.19(17)(b) specifies the log and pharmacist follow-up for a new prescription already prepared, visibly checked and DUR-reviewed."
      },
      {
        "text": "A technician may complete final validation during the break because the pharmacist remains in the building.",
        "why": "247 CMR 9.04(1) requires pharmacist final validation. A temporary break does not transfer this responsibility to technicians."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 9.19(17)(a)–(e); 247 CMR 9.04(1)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-017",
    "set": 4,
    "area": 4,
    "kind": "multi",
    "topic": "Pharmacy closure notices",
    "topicKey": "pharmacy-operations",
    "stem": "A Massachusetts resident community pharmacy plans a permanent closure on December 20, 2026. Assume no Board waiver. Under 247 CMR 6.13, which actions are required? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Notify the Board in writing by certified mail at least 14 days before the planned closure with the required information.",
        "why": "247 CMR 6.13(1) requires the resident pharmacy's advance certified-mail Board notice with closure details and other specified items."
      },
      {
        "text": "Attempt to notify patients whose prescriptions were filled in the prior 90 days at least 14 days before closure, using an approved method.",
        "why": "247 CMR 6.13(4) establishes this 90-day lookback and advance-notice rule and also requires conspicuous posted notice."
      },
      {
        "text": "Destroy all patient prescription files at the moment the pharmacy stops dispensing to prevent privacy violations.",
        "why": "Patient files must be handled or transferred in accordance with closure and record-retention laws, not summarily destroyed."
      },
      {
        "text": "Submit the original pharmacy license and controlled-substance registration plus the required disposition attestation to the Board within 14 days after closure.",
        "why": "247 CMR 6.13(6) requires those submissions after closure for a resident pharmacy, with controlled-substance disposition compliance."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "247 CMR 6.13(1),(4)–(6)",
    "url": "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-018",
    "set": 4,
    "area": 4,
    "kind": "single",
    "topic": "Theft and significant loss reports",
    "topicKey": "security-loss",
    "stem": "On a Monday, a Massachusetts DEA-registered resident community pharmacy confirms an actual theft of a bottle of Schedule II oxycodone and becomes aware of it that morning. No holidays or special exemptions apply. Which reporting plan BEST meets federal and Massachusetts reporting rules?",
    "choices": [
      {
        "text": "Notify the DEA after the pharmacy's next full inventory and submit the Massachusetts report at the next license renewal.",
        "why": "21 CFR 1301.76(b) requires prompt DEA written notice within one business day of discovery; Massachusetts has its own shorter reporting window than renewal."
      },
      {
        "text": "Provide written notice to the local DEA Diversion Field Office within one business day, complete DEA Form 106 as required, and submit the Massachusetts RLCS and applicable Form 106 to the Board within seven calendar days.",
        "why": "DEA requires written notification within one business day and subsequent Form 106. Massachusetts Board Policy 2026-01 requires its loss report and Form 106 if applicable within seven calendar days for confirmed thefts."
      },
      {
        "text": "Report only to the Massachusetts Board within seven calendar days because state reporting satisfies DEA notice.",
        "why": "State Board reporting does not replace separate federal DEA notification and Form 106 duties."
      },
      {
        "text": "Submit DEA Form 106 immediately but omit Massachusetts reporting if all missing tablets are later recovered.",
        "why": "Confirmed theft is reportable under Massachusetts Policy 2026-01 regardless of quantity; later recovery does not erase the original federal theft reporting duty."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1301.76(b); MA Board Policy 2026-01; 247 CMR 20.03(7)",
    "url": "https://www.mass.gov/doc/2026-01-loss-or-theft-of-controlled-substances-pdf/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-019",
    "set": 4,
    "area": 4,
    "kind": "multi",
    "topic": "Generic and authorized-generic interchange",
    "topicKey": "interchange",
    "stem": "A Massachusetts pharmacy evaluates prescriptions for a brand product for which a less expensive, reasonably available interchangeable product is listed, along with a different FDA-authorized generic. No patient-specific exception or safety issue applies. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "If the prescriber has not indicated 'no substitution,' the pharmacist is generally required to dispense the less expensive, reasonably available interchangeable listed product.",
        "why": "M.G.L. c.112 §12D, 105 CMR 720 and the DPH interchange policy generally mandate the lower-cost eligible interchangeable drug unless the prescriber prohibits substitution."
      },
      {
        "text": "A clear 'no substitution' direction by the prescriber may always be disregarded whenever a generic is less expensive.",
        "why": "A valid prescriber prohibition prevents mandated interchange; lower price alone cannot override a lawful no-substitution instruction."
      },
      {
        "text": "For a product newly listed as interchangeable, a prescriber can prevent midstream interchange by issuing a new prescription indicating 'no substitution.'",
        "why": "The Massachusetts midstream interchange policy specifies a new properly marked no-substitution prescription as the mechanism to prevent the switch."
      },
      {
        "text": "An FDA-authorized generic may be interchanged with the brand when there is no 'no substitution' direction, even if the authorized generic does not have a separate Orange Book therapeutic-equivalence listing.",
        "why": "DPH Circular DCP 22-01-112 explains that an authorized generic is the same approved product marketed without the brand name and may be interchanged when the prescriber does not prohibit substitution."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "M.G.L. c.112 §12D; 105 CMR 720; DCP 22-01-112",
    "url": "https://www.mass.gov/info-details/policy-on-drug-interchangeability-and-midstream-interchange",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-020",
    "set": 4,
    "area": 2,
    "kind": "single",
    "topic": "Opiate seven-day exception",
    "topicKey": "opioid-oud",
    "stem": "A Massachusetts practitioner plans a 10-day outpatient oxycodone prescription for a 17-year-old after acute surgery. The practitioner determines in professional medical judgment that more than seven days is required for the acute condition, documents that condition and why a non-opiate alternative is inappropriate, and discusses opiate risks and necessity with the minor's parent. All other prescription and dispensing rules are satisfied. Which statement is MOST accurate under M.G.L. c.94C §19D?",
    "choices": [
      {
        "text": "The prescription is prohibited because no minor may receive more than a seven-day opiate supply.",
        "why": "Section 19D(b) permits documented medical-necessity exceptions for adult or minor patients when its conditions are met."
      },
      {
        "text": "It is permitted only if the minor has cancer or is receiving palliative care.",
        "why": "Section 19D(b) also includes an acute medical condition and chronic pain management when the required professional judgment and documentation are satisfied."
      },
      {
        "text": "It may be issued under the documented medical-necessity exception, despite the standard seven-day limit for minors.",
        "why": "Section 19D(a) establishes the ordinary minor limit, while subsection (b) expressly permits exceptions for acute medical needs with required documentation and consideration of non-opiate alternatives."
      },
      {
        "text": "The pharmacist may extend any original seven-day opiate prescription to ten days after the parent signs consent.",
        "why": "The statute's prescribing exception depends on the practitioner's medical judgment and documentation; it does not give the pharmacist general authority to extend the prescription based only on parental consent."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c.94C §19D(a)–(c)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-021",
    "set": 5,
    "area": 2,
    "kind": "single",
    "topic": "Emergency OUD treatment — DEA three-day rule",
    "topicKey": "opioid-oud",
    "stem": "A DEA-registered practitioner in a Massachusetts emergency department is not registered as an opioid treatment program (OTP). A patient with opioid use disorder needs short-term withdrawal treatment while the department arranges referral to an OTP. Assume Massachusetts and other applicable laws permit the contemplated on-site dispensing, and no separate prescription authorization is being used. Under the federal exception in 21 CFR 1306.07(b), which action is MOST appropriate?",
    "choices": [
      {
        "text": "Write an outpatient prescription for a three-day supply of methadone and send it to a community pharmacy for the patient to pick up.",
        "why": "The special emergency provision in 21 CFR 1306.07(b) permits the practitioner to dispense, but not prescribe, a narcotic drug while referral arrangements are made. A community pharmacy prescription is not authorized by this exception."
      },
      {
        "text": "Directly dispense no more than a three-day supply of the narcotic medication at one time while arranging referral; do not renew or extend this emergency course.",
        "why": "The amended 21 CFR 1306.07(b) permits a non-OTP practitioner to dispense, but not prescribe, up to a three-day supply at one time while arranging referral; the emergency treatment cannot be renewed or extended."
      },
      {
        "text": "Directly dispense a seven-day supply whenever the nearest OTP cannot offer an appointment within three days.",
        "why": "An unavailable appointment does not expand the special federal three-day maximum. Other independent treatment authorities are outside the stated emergency exception."
      },
      {
        "text": "Dispense only one day's medication at a time for up to three consecutive days, because a three-day supply may never be given at once.",
        "why": "This describes the older pre-August-2023 federal limitation. The revised regulation allows up to three days' supply to be dispensed at one time, subject to the other requirements."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1306.07(b) (amended effective Aug. 8, 2023)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.07",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-022",
    "set": 5,
    "area": 2,
    "kind": "multi",
    "topic": "When a Schedule II fax serves as the original",
    "topicKey": "controlled-prescriptions",
    "stem": "A Massachusetts pharmacy receives otherwise valid, prescriber-transmitted facsimile prescriptions for Schedule II medications. Assume an applicable Massachusetts exception permits paper/fax transmission, all necessary federal prescription elements are present, and no oral emergency authorization is involved. In which cases may the fax itself serve as the original prescription under 21 CFR 1306.11? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A fax for morphine oral solution for a patient enrolled in a state-licensed hospice program; the prescription notes that the patient is a hospice patient.",
        "why": "21 CFR 1306.11(g) permits a facsimile to serve as the original for a Schedule II narcotic prescribed to a qualifying hospice patient when the required hospice notation is included."
      },
      {
        "text": "A fax for oxycodone tablets for a homebound patient with a terminal diagnosis who is not enrolled in hospice, does not reside in an LTCF, and will not receive an infusion.",
        "why": "A terminal diagnosis alone does not meet the special hospice-fax condition. Nor does this ordinary oral prescription meet the LTCF or compounded infusion exception, so the original signed paper prescription is generally required."
      },
      {
        "text": "A fax for methylphenidate tablets for a resident of a qualifying long-term care facility (LTCF).",
        "why": "21 CFR 1306.11(f) allows a facsimile to serve as the original for a Schedule II prescription for an LTCF resident; unlike the hospice exception, the provision is not limited to narcotics."
      },
      {
        "text": "A fax for a Schedule II narcotic to be compounded specifically for direct administration to the patient by intrathecal infusion.",
        "why": "21 CFR 1306.11(e) allows the fax as the original when a Schedule II narcotic is to be compounded for direct administration by a qualifying parenteral, including intraspinal, infusion."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "21 CFR 1306.11(a), (e)–(g)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-023",
    "set": 5,
    "area": 2,
    "kind": "single",
    "topic": "Returned prescription drugs — Massachusetts",
    "topicKey": "quality-safety",
    "stem": "A patient brings two sealed prescription packages back to the same Massachusetts pharmacy. Package X contains the wrong strength, which the pharmacy confirms it dispensed in error. Package Y was correctly dispensed, is not suspected to be defective or contaminated, and the patient simply no longer wants it. Neither medication has been taken, and the packages appear unopened. Which response BEST complies with 247 CMR 9.01?",
    "choices": [
      {
        "text": "Accept both packages and return them to saleable inventory after the pharmacist confirms the seals are intact.",
        "why": "247 CMR 9.01(5) and (7) do not permit re-dispensing or returning error-related or suspected defective/contaminated patient returns to saleable stock merely because they are sealed."
      },
      {
        "text": "Refuse both returns unless the patient proves an actual injury from taking the wrongly dispensed medication.",
        "why": "247 CMR 9.01(7) requires the pharmacy to accept a medication it dispensed in error; proof of ingestion or injury is not a condition."
      },
      {
        "text": "Accept both packages because all previously dispensed medication must be taken back, then dispose of only Package X.",
        "why": "The rule requires acceptance of medication dispensed in error or suspected defective/contaminated; it does not require accepting a properly dispensed, nondefective medication merely because it is unwanted."
      },
      {
        "text": "Accept Package X, quarantine it and properly dispose of it; the pharmacy is not required by this provision to accept Package Y.",
        "why": "Under 247 CMR 9.01(7), wrongly dispensed medication must be accepted and cannot return to inventory. Properly dispensed medication that was not defective at dispensing need not be accepted."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 9.01(5), (7)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-024",
    "set": 5,
    "area": 4,
    "kind": "multi",
    "topic": "DEA five-percent rule — pharmacy-to-pharmacy distribution",
    "topicKey": "controlled-inventory",
    "stem": "A DEA-registered Massachusetts retail pharmacy wishes to transfer controlled-substance stock to a second DEA-registered retail pharmacy for that pharmacy's general dispensing to patients (not a patient-specific prescription transfer). Assume every other Massachusetts and federal condition is satisfied. Under 21 CFR 1307.11, which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "If the annual volume of qualifying distributions is exactly 5% of the total controlled-substance dosage units distributed and dispensed in the same calendar year, the distributing pharmacy may use the exemption from separate distributor registration if all other conditions are met.",
        "why": "The 5% ceiling in 21 CFR 1307.11(a)(1)(iv) is inclusive: qualifying distributions must not exceed 5% of the total dosage units distributed and dispensed during that calendar year."
      },
      {
        "text": "A Schedule II transfer under this exemption needs only matching electronic inventory entries at both pharmacies; DEA Form 222 or an appropriate electronic order is unnecessary.",
        "why": "21 CFR 1307.11(a)(1)(iii) and Part 1305 still require the controlled-substance order form or compliant electronic ordering method when Schedule II stock is distributed."
      },
      {
        "text": "The receiving pharmacy must be registered to dispense the controlled substance, and the distribution and receipt must be properly documented by both parties.",
        "why": "21 CFR 1307.11(a)(1)(i)–(ii) requires the receiving practitioner to be registered to dispense and both the distributing and receiving parties to maintain transaction records."
      },
      {
        "text": "The 5% limit is measured by the wholesale dollar value of the stock transferred, rather than the number of controlled-substance dosage units.",
        "why": "The regulation uses dosage units, not purchase cost, prescription revenue, number of packages, or wholesale dollar value."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 CFR 1307.11(a)(1), (b); 21 CFR Part 1305",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-025",
    "set": 5,
    "area": 4,
    "kind": "single",
    "topic": "Compounding commercially available drug copies",
    "topicKey": "nonsterile-compounding",
    "stem": "A Massachusetts community pharmacy receives requests to compound a preparation with the same active ingredient, similar strength, and route as an FDA-approved product that remains commercially available and is not on the FDA drug shortages list. Assume the pharmacy otherwise meets applicable 503A, Massachusetts, and USP requirements. Which request BEST supports lawful patient-specific compounding of an essentially similar preparation?",
    "choices": [
      {
        "text": "A prescriber requests the compounded preparation solely because it would cost the patient 30% less than the commercially available product.",
        "why": "M.G.L. c.112 §39D and Massachusetts Board Policy 2020-02 expressly reject price difference alone as the significant medical difference needed to justify compounding a copy."
      },
      {
        "text": "A pharmacist documents an individual patient's reported preference for a dye-free version, but the prescriber makes no patient-specific determination of a medically significant difference.",
        "why": "The Massachusetts requirement calls for documented medical need as determined by the prescribing practitioner. The pharmacist's unilateral preference documentation does not substitute for that prescriber determination."
      },
      {
        "text": "A prescriber provides a patient-specific prescription and documents that a dye in the approved product causes this patient's allergic reaction and that removal creates a significant clinical difference.",
        "why": "M.G.L. c.112 §39D and Board Policy 2020-02 recognize a patient-specific, prescriber-documented medical need such as removal of a dye as a potential significant difference; all other compounding safeguards still apply."
      },
      {
        "text": "The pharmacy routinely prepares copies for future walk-in patients because its local wholesaler is temporarily out of stock, even though the approved product remains commercially available.",
        "why": "Local inventory inconvenience alone does not authorize routine compounding of essentially identical products. Patient-specific conditions and the federal 503A restriction against routinely compounding copies still apply."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c.112 §39D(a); MA Board Policy 2020-02; FD&C Act §503A(b)(1)(D)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-026",
    "set": 6,
    "area": 1,
    "kind": "single",
    "topic": "2026 Massachusetts supervisory ratios",
    "topicKey": "workforce-supervision",
    "stem": "A Massachusetts community pharmacy is not providing vaccination services. One pharmacist supervises four Massachusetts-licensed support personnel who are actively filling prescriptions. A fifth licensed technician is on the premises but performs only inventory receiving and does not participate in prescription preparation or filling. No waiver or dedicated-trainer arrangement applies. Under Board Policy 2026-02, which four-person filling team satisfies the ordinary 1:4 supervisory ratio?",
    "choices": [
      {
        "text": "One certified pharmacy technician and three noncertified pharmacy technicians.",
        "why": "Policy 2026-02 does not allow a four-person filling team with only one certified technician and no intern. At 1:4, the permitted compositions include two certified technicians, two interns, or a certified technician together with an intern."
      },
      {
        "text": "Two certified pharmacy technicians and two noncertified pharmacy technicians.",
        "why": "Policy 2026-02, Section I(A)(1)(b), permits 1:4 when at least two active support personnel are licensed certified pharmacy technicians. The fifth employee doing only inventory receiving need not be included in the filling ratio under Section I(C)."
      },
      {
        "text": "One licensed pharmacy intern and three noncertified pharmacy technicians.",
        "why": "A single pharmacy intern permits only the ordinary 1:3 composition unless another qualifying person is present. Four active support personnel need an additional certified technician or a second intern."
      },
      {
        "text": "Four licensed pharmacy interns performing prescription-filling duties under the same pharmacist.",
        "why": "Four interns filling prescriptions are not permitted under the ordinary intern-supervision provisions. The exceptional four-intern supervisory arrangements in Policy 2026-02 do not authorize four interns to fill prescriptions in a nonvaccinating community pharmacy."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "MA Board Policy 2026-02 §§I(A), I(C), II; 247 CMR 8.01(16)",
    "url": "https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-027",
    "set": 6,
    "area": 2,
    "kind": "single",
    "topic": "Pharmacist prescribing of oral HIV PrEP",
    "topicKey": "public-health-prescribing",
    "stem": "In November 2026, a Massachusetts-licensed community pharmacist plans to independently prescribe an FDA-approved oral HIV pre-exposure prophylaxis (PrEP) medication for an eligible adult. The pharmacist holds an NPI, completed an appropriately accredited 2.5-hour course addressing HIV risk assessment, symptoms, and prevention modalities (not only pharmacology), and will follow the applicable statewide PrEP guidance, counseling, documentation, and referral requirements. The prescription and dispensing will occur at the SAME pharmacy. The pharmacist does not hold a separate Massachusetts Controlled Substance Registration (MCSR). Which statement is MOST accurate?",
    "choices": [
      {
        "text": "The pharmacist must first obtain a physician-signed collaborative drug therapy management agreement, even though the 2026 state pharmacist-prescribing guidance is followed.",
        "why": "M.G.L. c.94C §19F independently authorizes qualifying pharmacists to prescribe covered HIV-prevention medications under statewide guidance. A separate CDTM agreement is not required simply to invoke this authority."
      },
      {
        "text": "The pharmacist cannot prescribe because a personal MCSR is mandatory for every prescription issued by a pharmacist, even when it is dispensed at the same pharmacy.",
        "why": "Massachusetts Circular DCP 26-08-125 expressly states that a pharmacist need not obtain a personal MCSR when both the prescribing and dispensing occur at one pharmacy location, provided all other applicable conditions are met."
      },
      {
        "text": "The pharmacist may omit the NPI and document the encounter only if the pharmacy transfers the resulting prescription to a different pharmacy for dispensing.",
        "why": "DCP 26-08-125 requires the pharmacist to obtain an NPI and document prescribing and dispensing activities. Dispensing elsewhere would also fall outside the circular's specifically described same-location MCSR exemption."
      },
      {
        "text": "The pharmacist may prescribe and dispense oral PrEP under §19F without a separate personal MCSR in this same-location situation, provided all other applicable requirements are met.",
        "why": "DCP 26-08-125 permits pharmacist prescribing of covered HIV-prevention medications under statewide guidance and qualifying training. It requires an NPI and expressly waives a separate pharmacist MCSR when prescribing and dispensing both occur at a single pharmacy location."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §19F; DCP Circular 26-08-125, General Prescribing Requirements and HIV Prevention",
    "url": "https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-028",
    "set": 6,
    "area": 2,
    "kind": "multi",
    "topic": "2026 Part 2 consent and SUD counseling notes",
    "topicKey": "privacy-part2",
    "stem": "A HIPAA-covered Massachusetts pharmacy receives ordinary substance-use-disorder treatment records from a federally assisted 42 CFR Part 2 program pursuant to the patient's valid, written single consent for future treatment, payment, and health care operations (TPO). The pharmacy is also asked to obtain a separately maintained set of the treating counselor's SUD counseling notes, but the patient has NOT given any separate consent for those notes. No other disclosure exception or state-specific restriction applies. Under the Part 2 rule with a February 16, 2026 compliance date, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The single TPO consent automatically authorizes the pharmacy to obtain the separately maintained SUD counseling notes on the same terms as the ordinary treatment record.",
        "why": "The 2024 Part 2 rule expressly creates special protection for separately maintained SUD counseling notes; a broad TPO consent does not replace the separate patient consent required for those notes."
      },
      {
        "text": "For the ordinary Part 2 treatment records received under the valid TPO consent, the HIPAA-covered pharmacy may make later disclosures as HIPAA permits, subject to Part 2's additional prohibition on using records in proceedings against the patient.",
        "why": "HHS's 2024 Part 2 final rule allows HIPAA-covered entities receiving Part 2 records under a single TPO consent to redisclose according to HIPAA, except for the more protective restriction on legal proceedings against the patient."
      },
      {
        "text": "Once the pharmacy has the ordinary records under a TPO consent, a general subpoena alone makes their use in criminal proceedings against that patient permissible.",
        "why": "Part 2's special protection against using SUD records against the patient remains in force. A general subpoena alone is not equivalent to the specific patient consent or Part 2-compliant court-order process required for such proceedings."
      },
      {
        "text": "The pharmacy generally needs separate consent for the separately maintained SUD counseling notes; the ordinary TPO consent does not cover that special note category.",
        "why": "The revised 42 CFR Part 2 rule treats separately maintained SUD counseling notes analogously to psychotherapy notes and requires specific patient consent, rather than relying on a broad TPO consent."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "42 CFR Part 2 (2024 final rule; compliance Feb. 16, 2026); HHS Part 2 Final Rule Fact Sheet, Patient Consent and SUD Counseling Notes",
    "url": "https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-029",
    "set": 6,
    "area": 3,
    "kind": "single",
    "topic": "PPPA prescription packaging and patient waiver",
    "topicKey": "label-packaging",
    "stem": "A Massachusetts patient with limited hand dexterity specifically requests a conventional (non-child-resistant) container for ONE newly prescribed oral medication subject to the federal Poison Prevention Packaging Act (PPPA). The pharmacist documents that request and dispenses the medication accordingly. Two weeks later, the patient presents a DIFFERENT new prescription for another PPPA-covered oral medication. No blanket packaging request was made, the prescriber has not requested conventional packaging for the second prescription, and the patient makes no new packaging request. What is the BEST legally supported dispensing approach?",
    "choices": [
      {
        "text": "The first prescription may use conventional packaging at the patient's request, but the second generally needs child-resistant packaging absent a new specific request, a valid blanket request, or a prescriber direction.",
        "why": "CPSC's PPPA guidance permits a patient-specific packaging request while explaining that a request for one prescription does not extend to an unrelated future prescription. Without a separate exemption or request, the second prescription uses compliant packaging."
      },
      {
        "text": "The first conventional container was impermissible because only a prescriber, not a patient, can authorize dispensing without child-resistant packaging.",
        "why": "The PPPA permits a consumer or the prescribing practitioner to specifically request conventional packaging for a covered prescription; a patient request is legally sufficient for the first prescription."
      },
      {
        "text": "Use conventional packaging for the second prescription because the first documented request permanently waives child-resistant packaging for all future prescriptions.",
        "why": "CPSC expressly distinguishes a specific request for one prescription from a request covering all medications. The first request does not automatically become a blanket waiver for other prescriptions."
      },
      {
        "text": "The pharmacist may independently choose conventional packaging for the second prescription based on the patient's known dexterity limitations, without a new patient or prescriber request.",
        "why": "The patient's difficulty opening packaging can inform counseling but does not independently authorize the pharmacist to waive special packaging. The choice must come from the patient or prescriber unless another specific exemption applies."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "Poison Prevention Packaging Act §4(b); 16 CFR 1701.1; CPSC Poison Prevention Packaging Guide (Jan. 2023), p. 12",
    "url": "https://www.cpsc.gov/s3fs-public/PoisonPreventionPackagingAGuideforHealthcareProfessionals.pdf",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-030",
    "set": 6,
    "area": 4,
    "kind": "multi",
    "topic": "DSCSA verification: suspect versus illegitimate product",
    "topicKey": "dscsa",
    "stem": "A Massachusetts community pharmacy is a dispenser subject to the Drug Supply Chain Security Act (DSCSA). It finds a questionable product identifier on a prescription drug package that it holds in inventory and determines the package is a SUSPECT product. The pharmacy begins an investigation with its trading partners. Later, evidence establishes that it is an ILLEGITIMATE product. Assume no applicable waiver, exemption, or enforcement-discretion relief. Which statements accurately describe the dispenser's federal DSCSA obligations? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "At the point the package is determined to be suspect, it must be quarantined apart from product intended for distribution while the pharmacy promptly investigates.",
        "why": "FD&C Act §582(d)(4)(A) requires the dispenser to quarantine a suspect product and promptly investigate its legitimacy; it cannot simply continue dispensing it while verifying the identifier."
      },
      {
        "text": "The pharmacy must notify FDA and all immediate trading partners within 24 hours of the initial SUSPECT classification, even before it determines the product is illegitimate.",
        "why": "The federal 24-hour illegitimate-product notification requirement for dispensers is triggered by the determination of illegitimacy, not merely by the initial classification of a product as suspect."
      },
      {
        "text": "After determining that the product is illegitimate, the pharmacy must notify FDA and appropriate immediate trading partners within 24 hours of that determination.",
        "why": "Under §582(d)(4)(B)(ii), the dispenser must notify FDA and immediate trading partners that it has reason to believe may have received the illegitimate product within 24 hours after determining illegitimacy."
      },
      {
        "text": "The pharmacy must retain records of the suspect-product investigation for at least six years after the investigation is concluded.",
        "why": "FD&C Act §582(d)(4)(A)(iv) requires dispensers to retain suspect-product investigation records for at least six years after the conclusion of the investigation, regardless of the outcome."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "FD&C Act §582(d)(4)(A)–(B) (21 U.S.C. §360eee-1); FDA DSCSA Verification Systems Guidance (Dec. 2023)",
    "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/title-ii-drug-quality-and-security-act",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-031",
    "set": 7,
    "area": 1,
    "kind": "single",
    "topic": "Internship eligibility: ACPE experiential hours",
    "topicKey": "intern-education",
    "stem": "Two first-time Massachusetts pharmacist-licensure applicants submit internship records in November 2026. Applicant X graduated from an ACPE-accredited PharmD program in 2026 and has Board-acceptable verification of 1,500 hours acquired through experiential pharmacy education, but no additional paid internship. Applicant Y graduated from an ACPE-accredited program in 2011 and can verify only 1,000 school rotation hours; Y has no other Board-approved internship hours. Assume all other licensure requirements can be met. Which interpretation of the Massachusetts internship requirement is MOST accurate?",
    "choices": [
      {
        "text": "Both applicants satisfy the requirement because an ACPE pharmacy degree always replaces separate internship-hour documentation regardless of graduation year.",
        "why": "The Board's 2012-and-later ACPE graduate policy is not automatically retroactive to the 2011 graduate. Applicant Y has only 1,000 verified hours, with no additional approved internship hours."
      },
      {
        "text": "Applicant X must obtain 500 additional hours outside the PharmD curriculum because every applicant must separately complete the 1,000-plus-500 internship pathway.",
        "why": "247 CMR 8.01(1)(b) provides a separate route for 1,500 qualifying hours from ACPE experiential pharmacy education. The 1,000-plus-500 route is not a mandatory extra requirement for X."
      },
      {
        "text": "Applicant Y qualifies through the pre-2012 graduation policy, but Applicant X must complete 500 hours after graduation.",
        "why": "The Board's guidance for graduates through 2011 describes 1,000 school rotation hours plus 500 additional verified hours. It does not impose an extra post-graduation 500-hour requirement on a 2026 ACPE graduate."
      },
      {
        "text": "Applicant X satisfies the internship-hour requirement through qualifying ACPE experiential education; Applicant Y needs additional Board-acceptable internship hours.",
        "why": "247 CMR 8.01(1)(b) recognizes 1,500 hours of ACPE experiential pharmacy education. The Board's guidance treats 2012-and-later ACPE graduates as satisfying the intern-hour requirement, but the 2011 applicant with only 1,000 documented school rotation hours has not fulfilled the historic additional-hour requirement."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 8.01(1)(a)–(b); MA Board, Intern Hours Requirement for Pharmacist Licensure (2012 graduate transition)",
    "url": "https://www.mass.gov/info-details/intern-hours-requirement-for-pharmacist-licensure",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-032",
    "set": 7,
    "area": 2,
    "kind": "single",
    "topic": "Clozapine: FDA REMS removal versus ANC monitoring",
    "topicKey": "rems",
    "stem": "In November 2026 a Massachusetts community pharmacist receives a valid first prescription for clozapine. The pharmacy is not enrolled in the former Clozapine REMS, and the patient's absolute neutrophil count (ANC) has not been entered into a REMS portal. The pharmacist has assessed the prescription and the prescriber will arrange ANC monitoring according to current labeling. No other dispensing concern exists. Which conclusion BEST reflects FDA requirements in effect on this date?",
    "choices": [
      {
        "text": "Dispensing must wait until both the patient and pharmacy reenroll in the Clozapine REMS and the ANC is uploaded to the REMS portal.",
        "why": "FDA eliminated the Clozapine REMS effective June 13, 2025. Enrollment and REMS ANC submission are no longer federal prerequisites to clozapine dispensing."
      },
      {
        "text": "The prescription may be dispensed without former REMS enrollment or REMS ANC verification, while the drug's neutropenia warnings and clinical ANC monitoring guidance remain important.",
        "why": "FDA formally removed the Clozapine REMS effective June 13, 2025. Pharmacies no longer verify eligibility through the REMS, but the boxed neutropenia warning and recommendations for prescriber ANC monitoring remain in the labeling."
      },
      {
        "text": "The removal of the Clozapine REMS also removed the boxed warning and the clinical need for ANC monitoring during treatment.",
        "why": "FDA retained the warning about severe neutropenia and expressly advises prescribers to continue ANC monitoring as outlined in labeling; removing an administrative REMS does not remove the safety risk."
      },
      {
        "text": "The REMS exemption is limited to patients who have already taken clozapine for six months; new-start prescriptions still require mandatory pharmacy certification.",
        "why": "The FDA removal applies to clozapine prescriptions generally, including new starts; it is not a conditional six-month grandfathering or stabilization exemption."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "FDA Drug Safety Communication, Aug. 27, 2025: Clozapine REMS eliminated effective June 13, 2025; 247 CMR 9.01(21)",
    "url": "https://www.fda.gov/drugs/drug-safety-communications/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-033",
    "set": 7,
    "area": 2,
    "kind": "multi",
    "topic": "HIPAA breach thresholds: exactly 500 affected residents",
    "topicKey": "hipaa-breach",
    "stem": "A HIPAA-covered Massachusetts pharmacy and its business associate discover a reportable breach of UNSECURED protected health information affecting EXACTLY 500 Massachusetts residents. The parties confirm the breach is reportable after risk assessment, have valid contact information for affected people, and have no applicable law-enforcement delay. Consider only the FEDERAL HIPAA Breach Notification Rule; any separate Massachusetts notification obligations must be addressed independently. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The covered pharmacy must notify affected individuals without unreasonable delay and no later than 60 calendar days after the breach is discovered under HIPAA.",
        "why": "45 CFR 164.404 requires individual notification without unreasonable delay and not later than 60 calendar days after discovery. The exact 500-person count does not eliminate individual notice."
      },
      {
        "text": "The covered pharmacy must notify the HHS Secretary for this breach on the timetable for 500 or more individuals, rather than waiting for the annual report for smaller breaches.",
        "why": "45 CFR 164.408(b) applies to breaches involving 500 or more people, including exactly 500. The Secretary is notified contemporaneously with individual notice, subject to the rule's timing requirements."
      },
      {
        "text": "Because exactly 500 Massachusetts residents were affected, the pharmacy must also provide federal media notice to prominent Massachusetts outlets.",
        "why": "45 CFR 164.406 requires media notice when a breach involves MORE THAN 500 residents of a state or jurisdiction. Exactly 500 triggers HHS reporting at the larger-breach threshold but not the federal media-notification requirement."
      },
      {
        "text": "The business associate must notify the covered pharmacy without unreasonable delay and no later than 60 calendar days after the business associate's discovery of the breach.",
        "why": "45 CFR 164.410 requires a business associate to notify the covered entity without unreasonable delay and not later than 60 calendar days after discovery. The covered entity remains responsible for ensuring required individual notifications occur."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "45 CFR 164.404, 164.406 (>500 state residents), 164.408 (≥500 individuals), 164.410; HHS HIPAA Breach Notification Rule",
    "url": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-034",
    "set": 7,
    "area": 3,
    "kind": "multi",
    "topic": "Schedule IV refill transfers: shared online database exception",
    "topicKey": "refills-transfers",
    "stem": "A patient has a valid, previously filled Schedule IV prescription with authorized refills remaining. Two Massachusetts pharmacies (X and Y) do NOT share a real-time online database. Another pair (R and S) electronically share the same real-time online prescription database. The patient requests refill transfers, all pharmacies are properly registered, and no separate restrictions apply. Under current federal requirements and Massachusetts pharmacy law, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A refill transfer between X and Y is generally limited to one transfer and must be communicated directly between two licensed pharmacists under the federal controlled-substance transfer procedure.",
        "why": "21 CFR 1306.25(a) provides a one-time rule for Schedule III–V refill transfers between pharmacies lacking a shared real-time online database. Subsection (b)(1) requires direct pharmacist-to-pharmacist communication."
      },
      {
        "text": "A Massachusetts certified pharmacy technician may independently communicate the Schedule IV refill transfer with on-duty pharmacist approval because technician transfer authority extends to every Schedule II–VI prescription.",
        "why": "247 CMR 8.04(4)(d) allows a certified technician with pharmacist approval to transfer Schedule VI prescriptions. It does not extend to Schedule IV transfers; federal 21 CFR 1306.25(b)(1) requires two licensed pharmacists."
      },
      {
        "text": "R and S may use the shared real-time online database exception for additional Schedule IV refill transfers, but only within the refills legally available and authorized by the prescriber.",
        "why": "21 CFR 1306.25(a) permits multiple transfers when pharmacies electronically share a real-time online database, only up to the maximum authorized refills and applicable law; the other documentation requirements remain."
      },
      {
        "text": "The original and transferred Schedule IV prescription records must be retained for at least two years measured from the date of the last refill.",
        "why": "21 CFR 1306.25(c) requires both original and transferred prescription records be kept two years from the last refill; that clock is not simply two years after the original issue date."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "21 CFR 1306.25(a)–(e); 247 CMR 9.14(1)–(3); 247 CMR 8.04(4)(d)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.25",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-035",
    "set": 7,
    "area": 4,
    "kind": "single",
    "topic": "USP <797> immediate-use CSP: 3 products versus 4 containers",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "At 8:15 a.m., appropriately trained personnel begin preparing a patient-specific immediate-use compounded sterile preparation (CSP) in a hospital patient-care area. They use TWO vials of the same sterile drug, ONE vial of Sterile Water for Injection, and ONE bag of sterile normal saline: four physical containers, but three different sterile products. Aseptic technique, compatibility, preparation-specific conditions, and all other USP <797> immediate-use requirements are satisfied. A different clinician, not witnessed by the preparer, will begin administration at 12:05 p.m. The CSP bears the required immediate-use label. Which conclusion is MOST accurate?",
    "choices": [
      {
        "text": "The CSP must be discarded because immediate-use preparations are limited to three physical vials or bags, regardless of whether they contain the same sterile product.",
        "why": "USP <797> limits immediate-use preparation to three DIFFERENT sterile products, not three total containers. Two vials of an identical sterile drug count as one different product."
      },
      {
        "text": "The CSP must be discarded because administration must start within one hour of the end of compounding, even when all other immediate-use requirements are satisfied.",
        "why": "The revised USP <797> immediate-use standard permits administration to begin within four hours following the START of preparation, not a universal one-hour period following completion."
      },
      {
        "text": "The CSP can qualify for immediate-use administration because it contains only three different sterile products, administration begins within four hours of the start, and the required label is present.",
        "why": "USP <797> Section 1.3 and USP's official FAQs permit multiple containers of the same sterile product as long as there are no more than three different sterile products. From 8:15 a.m. to 12:05 p.m. is 3 hours 50 minutes, within the four-hour start-of-preparation limit. When the preparer does not administer or witness administration, the immediate-use label is required."
      },
      {
        "text": "The CSP may be administered as late as 12:35 p.m. because the four-hour period begins when preparation is finished rather than when it starts.",
        "why": "The four-hour immediate-use clock starts when preparation BEGINS (8:15 a.m. in this case); administration at 12:35 p.m. would exceed that time limit regardless of the completion time."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "USP <797> §1.3 Immediate-Use CSPs; USP official <797> FAQs (Dec. 11, 2023), items 22, 25, 40",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-036",
    "set": 8,
    "area": 1,
    "kind": "single",
    "topic": "Community CDTM: prescribing, documentation and physician notification",
    "topicKey": "cdtm",
    "stem": "A Massachusetts community pharmacist has all required CDTM qualifications and a current MCSR. A supervising physician and pharmacist have signed a collaborative practice agreement with written diabetes-management prescribing protocols. A 52-year-old patient has a patient-specific written referral identifying diabetes, has provided written informed consent, and is already receiving metformin (Massachusetts Schedule VI) prescribed by that physician. The pharmacist proposes to modify the metformin dose under the protocol. No urgent circumstances or other legal restrictions apply. Which plan is FULLY consistent with 247 CMR 16.03 and 16.04?",
    "choices": [
      {
        "text": "Modify metformin under the protocol, document the change in the patient's medical record, and forward a copy of the modification to the supervising physician within 72 hours.",
        "why": "The appropriate therapy and medical-record documentation are not enough: 247 CMR 16.03(5)(e)2 requires a copy of a modification to be provided to the supervising physician within 24 hours of issuance unless more urgent notification is needed."
      },
      {
        "text": "Modify metformin under the protocol and send the physician a copy within 24 hours, but record the action only in a pharmacy dispensing worksheet rather than the patient's medical record.",
        "why": "The 24-hour notification is appropriate, but 247 CMR 16.03(5)(e)2 and 16.04(2)(e) also require the action to be noted in the patient's medical record; a dispensing worksheet alone does not satisfy that duty."
      },
      {
        "text": "Modify metformin under the protocol, note the action in the patient's medical record, and send the supervising physician a copy of the modification within 24 hours.",
        "why": "The patient-specific referral, written consent, covered diagnosis, authorized Schedule VI therapy, permanent medical-record documentation, and 24-hour transmission of the medication modification satisfy the stated community-CDTM requirements."
      },
      {
        "text": "Instead of modifying metformin, use the same CDTM agreement to increase the patient's Schedule IV clonazepam dose after the supervising physician verbally approves and receives written notice within 24 hours.",
        "why": "247 CMR 16.03(5)(e)3 prohibits a community-pharmacy CDTM pharmacist from prescribing Schedule II through V controlled substances even if the physician approves and receives prompt notice."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 16.03(5)(c)–(e), 16.04(1)–(2): community CDTM patient referral, limited prescribing, and physician notification",
    "url": "https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-037",
    "set": 8,
    "area": 2,
    "kind": "single",
    "topic": "MIIS objection: reporting versus data-sharing access",
    "topicKey": "immunization",
    "stem": "At a Massachusetts community pharmacy, a properly qualified pharmacist administers an indicated recombinant zoster vaccine to a 55-year-old patient under a valid standing order. All screening and pre-administration VIS requirements are met. At the visit, the patient completes a Massachusetts Immunization Information System (MIIS) data-sharing objection form and gives it directly to the pharmacist. The pharmacy has MIIS GUI access and no regulatory waiver. Which response MOST accurately satisfies Massachusetts requirements?",
    "choices": [
      {
        "text": "Do not report this dose to MIIS because the patient's written data-sharing objection exempts the pharmacy from submitting the immunization record.",
        "why": "105 CMR 222.100 requires reporting of new immunizations within 72 hours. An objection to MIIS data sharing limits access among MIIS users; it does not cancel the provider's reporting duty."
      },
      {
        "text": "Report the immunization to MIIS within 72 hours; forward the objection form to DPH within 24 hours of receipt and change the patient's MIIS data-sharing status in the GUI.",
        "why": "105 CMR 222.100(A) requires reporting within 72 hours. Section 222.105(B)(2) separately requires a provider receiving the objection form to send it to DPH within 24 hours and update the recipient's data-sharing status in the MIIS GUI."
      },
      {
        "text": "Report the immunization within 72 hours and retain the objection in the pharmacy's records, but leave the patient's MIIS data-sharing setting unchanged until DPH contacts the pharmacy.",
        "why": "The provider must not merely retain the objection: 105 CMR 222.105(B)(2) requires the form to be returned to DPH within 24 hours and the sharing status to be changed in the GUI."
      },
      {
        "text": "Forward the patient's objection form to DPH within 72 hours, then report the vaccination only if the patient subsequently withdraws the objection.",
        "why": "The form must be forwarded within 24 hours of receipt, not 72 hours. The dose must still be reported within 72 hours even when data sharing has been restricted."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "105 CMR 222.100(A) and 222.105(A)–(B): immunization reporting and MIIS data-sharing objections",
    "url": "https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-038",
    "set": 8,
    "area": 2,
    "kind": "multi",
    "topic": "Mail-delivered liquid prescriptions: counseling refusal and DUR",
    "topicKey": "counseling-dur",
    "stem": "A Massachusetts community pharmacy fills a NEW oral antibiotic suspension and sends it to a patient who elected delivery to their home. The pharmacy provides the patient with a toll-free number enabling direct contact with its pharmacist; the patient is reached, is offered pharmacist counseling, and expressly declines. A pharmacy technician prepares the package, and the pharmacist has not yet performed the prospective drug utilization review (DUR). Assume no inpatient exception or other special waiver applies. Which actions or conclusions are consistent with Massachusetts law? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "For a patient electing delivery away from the pharmacy, access to a toll-free telephone service facilitating communication with the pharmacist may satisfy the statutory counseling-access requirement.",
        "why": "M.G.L. c.94C, §21A allows counseling-access obligations for delivery outside a pharmacy to be met by giving the recipient access to a toll-free telephone service for communication with the pharmacist."
      },
      {
        "text": "The technician's completion of a computerized interaction screen substitutes for the pharmacist's prospective DUR, allowing this new prescription to be released without pharmacist review.",
        "why": "M.G.L. c.94C, §21A and 247 CMR 9.17 place the prospective drug review responsibility on a pharmacist before a new prescription is dispensed or delivered. A technician's computerized screening alone does not replace it."
      },
      {
        "text": "The pharmacy should record the patient's refusal of counseling in the appropriate patient record or signature log, even though the offer was made.",
        "why": "M.G.L. c.94C, §21A requires reasonable efforts to document patient information, including any failure to accept a counseling offer; 130 CMR 406.446 likewise specifies documenting patient refusals for MassHealth prescriptions."
      },
      {
        "text": "The pharmacist or pharmacy must dispense or recommend an appropriate measuring device for the liquid antibiotic suspension.",
        "why": "247 CMR 9.18(9) requires a pharmacy and pharmacist to dispense or recommend a proper measuring device with liquid medications, independent of the patient's decision to decline counseling."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "M.G.L. c.94C §21A; 247 CMR 9.17 and 9.18(9); 130 CMR 406.446: mail-delivery counseling, DUR, refusal and measuring devices",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21A",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-039",
    "set": 8,
    "area": 3,
    "kind": "multi",
    "topic": "MassPAT additional drugs and naloxone: reporting versus visibility",
    "topicKey": "masspat",
    "stem": "A Massachusetts community pharmacy dispenses prescribed gabapentin (Massachusetts Schedule VI), a Schedule IV tramadol prescription, and naloxone to eligible Massachusetts residents. A separate patient receives gabapentin from a federal Veterans Affairs (VA) pharmacy. The community pharmacy is reviewing its MassPAT data obligations and what prescribers will see on patient PMP profiles. Assume no waivers apply to the community pharmacy. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Prescribed gabapentin dispensed at the Massachusetts community pharmacy must be reported to the PMP, even though it remains a Massachusetts Schedule VI drug.",
        "why": "Massachusetts DPH designates gabapentin an additional drug for PMP reporting under 105 CMR 700.012. Schedule VI classification does not remove the community pharmacy's reporting obligation."
      },
      {
        "text": "The VA pharmacy's gabapentin dispensing may not appear in MassPAT because federal VA reporting is limited by statute to federally controlled Schedule II–V prescriptions.",
        "why": "The Massachusetts DPH reporting guidance explains that VA pharmacies are limited by federal statute to reporting Schedule II–V dispensings, so their Schedule VI gabapentin transactions will not appear on a patient's PMP report."
      },
      {
        "text": "An out-of-state mail pharmacy delivering prescribed gabapentin to a Massachusetts resident is exempt from Massachusetts PMP reporting solely because gabapentin is not federally scheduled.",
        "why": "105 CMR 700.012(A)(1) extends reporting to covered out-of-state pharmacies delivering controlled substances or designated additional drugs to people in Massachusetts. Gabapentin's federal unscheduled status alone is not an exemption."
      },
      {
        "text": "DPH permits naloxone dispensing information to be included in daily PMP submissions for data collection; that naloxone information does not appear on the patient's PMP profile, and patient ID collection is not required for those dispensings.",
        "why": "Massachusetts DPH describes daily PMP submission as its preferred naloxone-reporting method under M.G.L. c.94C §19B, clarifies that naloxone entries are data-collection-only and not visible on patient profiles, and does not require patient ID for naloxone submissions."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "105 CMR 700.012(A)(1),(5),(8); DPH Pharmacy Reporting and Data Submission: Gabapentin, VA dispensings, and naloxone",
    "url": "https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-040",
    "set": 8,
    "area": 4,
    "kind": "single",
    "topic": "DEA Form 222: partial stock shipments and sixty-day expiration",
    "topicKey": "controlled-inventory",
    "stem": "A DEA-registered Massachusetts retail pharmacy executed a valid PAPER DEA Form 222 on September 1, 2026, ordering ten commercial containers of a Schedule II medication. The supplier shipped four containers on September 12. It can ship the other six 45 days after the form was executed, directly to the registered location printed on the order. The pharmacy maintains a copy of its order and is able to document the actual quantity and receipt date for each shipment. No military procurement or other exception applies. Which statement BEST describes the lawful procedure under 21 CFR 1305.13?",
    "choices": [
      {
        "text": "The supplier may supply the remaining six containers through additional shipments within 60 days of the form date, and the purchaser must record the containers furnished and the receipt dates on its retained copy.",
        "why": "21 CFR 1305.13(b) permits partial shipments completing the balance within 60 days after the Form 222 date. Subsection (e) requires the purchaser to record the number of containers received and receipt dates on its retained copy."
      },
      {
        "text": "The first partial shipment automatically closes the paper DEA Form 222, so an entirely new form is required for the remaining six containers even within 60 days.",
        "why": "A supplier may supply the unfilled balance of a Form 222 in later partial shipments during the 60-day validity period. A new form is not inherently necessary merely because the first shipment was partial."
      },
      {
        "text": "The 60-day validity clock starts with the first shipment on September 12 rather than the execution date, so the supplier can ship the balance for 60 days after that shipment.",
        "why": "21 CFR 1305.13(b) measures the 60-day limit from the date of the DEA Form 222 as executed by the purchaser, not from the first shipment or the supplier's acknowledgment."
      },
      {
        "text": "The pharmacy may redirect the remaining containers to a different branch with its own DEA registration without changing the paper DEA Form 222 because both locations belong to the same owner.",
        "why": "21 CFR 1305.13(c) generally requires the supplier to ship to the purchaser and location printed on the Form 222. Common ownership and separate DEA registration do not independently authorize delivery to another location."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "21 CFR 1305.13(a)–(e): DEA Form 222 partial shipments, location, purchaser records and 60-day limit",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-041",
    "set": 9,
    "area": 1,
    "kind": "single",
    "topic": "Pharmacy technician trainee: cumulative hours and telephone prescriptions",
    "topicKey": "technician-scope",
    "stem": "A Massachusetts-licensed pharmacy technician trainee is 19 years old and has worked 1,505 cumulative hours as a trainee over ten months. The person has neither obtained a pharmacy technician license nor received a Board extension, and no other exception to the trainee employment limit applies. A pharmacist offers to supervise the trainee for another month and asks the trainee to accept new verbal prescriptions from prescribers during that period. Which statement is MOST accurate?",
    "choices": [
      {
        "text": "The trainee can continue filling prescriptions until one full year has elapsed but must refer telephone prescriptions to the pharmacist.",
        "why": "The employment limit in 247 CMR 8.03(5) is 1,500 hours OR one year, whichever occurs first, absent a stated exception. Already exceeding 1,500 hours disqualifies continued trainee work despite having fewer than 12 months of experience."
      },
      {
        "text": "The trainee may continue working if a certified pharmacy technician directly supervises the filling work and a pharmacist later validates each prescription.",
        "why": "The regulation requires direct supervision by a pharmacist and does not permit additional trainee employment beyond the statutory hour limit through certified-technician supervision or a final pharmacist check. Taking prescriptions by telephone is also prohibited for trainees."
      },
      {
        "text": "The trainee cannot continue working as a trainee under these facts, and receiving prescriptions by telephone is prohibited for trainees even before reaching the employment limit.",
        "why": "247 CMR 8.03(5) bars trainee employment after 1,500 hours or one year, whichever is shorter, absent an exception; none applies. Separately, 247 CMR 8.03(4)(c) prohibits a trainee from taking prescriptions over the telephone."
      },
      {
        "text": "The trainee may restart a new 1,500-hour limit on January 1 because the trainee-hour maximum is measured separately for each calendar year.",
        "why": "The regulatory 1,500-hour trainee period is cumulative employment, not an annual allowance that resets each January. The pharmacist cannot create an exception by changing the calendar year."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 8.03(4)(b)–(c), 8.03(5): trainee scope and 1,500-hour/one-year limit",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-042",
    "set": 9,
    "area": 2,
    "kind": "multi",
    "topic": "Pharmacist-initiated contraception: initial visit, screening and supply",
    "topicKey": "public-health-prescribing",
    "stem": "In November 2026, a Massachusetts-licensed pharmacist with the appropriate contraceptive-prescribing training and an NPI evaluates a clinically eligible adult requesting a first oral hormonal contraceptive. The pharmacist uses the required self-screening risk assessment, provides counseling, and will meet all documentation and dispensing requirements. No previous contraception prescription, CDTM agreement, or primary-care visit is documented. Under M.G.L. c.94C §19F and current DPH Circular DCP 26-08-125, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist may prescribe an eligible FDA-approved self-administered oral hormonal contraceptive without proof that a primary care practitioner previously prescribed contraception for this patient.",
        "why": "The amended §19F(a) authorizes pharmacist-initiated oral hormonal contraceptive prescribing regardless of the patient's previous prescription history, provided applicable screening, training and clinical safeguards are met."
      },
      {
        "text": "A patient-specific collaborative drug therapy management agreement or authorization from a physician is a mandatory prerequisite for an initial pharmacist-issued oral contraceptive prescription.",
        "why": "The independent pharmacist-prescribing authority in M.G.L. c.94C §19F does not require a CDTM agreement or a patient-specific physician prescription when the pharmacist follows its specific requirements."
      },
      {
        "text": "The pharmacy must not require the patient to make a scheduled pharmacist appointment solely to obtain the authorized oral contraceptive prescription and dispensing.",
        "why": "The 2026 DPH circular states that a scheduled pharmacist appointment shall not be required for oral hormonal contraceptive or patch prescribing/dispensing under §19F."
      },
      {
        "text": "The pharmacist may issue a valid oral hormonal contraceptive prescription for up to a 12-month supply when the required self-screening, training, counseling and other requirements are satisfied.",
        "why": "Circular DCP 26-08-125 permits a prescription for up to, but not more than, a 12-month supply, subject to manufacturer labeling and clinical eligibility."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "M.G.L. c.94C §19F(a)–(c); DPH Circular DCP 26-08-125 (Aug. 25, 2026), Hormonal Contraceptives",
    "url": "https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-043",
    "set": 9,
    "area": 2,
    "kind": "single",
    "topic": "Naloxone for a third party: standing order and purchaser insurance",
    "topicKey": "opioid-oud",
    "stem": "A Massachusetts resident asks a community pharmacist for a naloxone rescue kit to keep available for a coworker at risk of overdose. The resident has no individual naloxone prescription and wants to use the resident's own prescription insurance. The pharmacy participates in the Massachusetts statewide naloxone standing order; no coverage exclusion or other dispensing restriction is present. Which workflow is MOST consistent with Massachusetts law and Board Policy 2024-01?",
    "choices": [
      {
        "text": "Decline to dispense until the coworker is present and presents an individual naloxone prescription, because insurance billing must be under the intended recipient's name.",
        "why": "M.G.L. c.94C §19B and the statewide standing order permit a person to obtain naloxone to administer to someone else. An individual prescription or the intended recipient's presence is not necessary under that pathway."
      },
      {
        "text": "Provide naloxone only as a retail OTC purchase; the statewide standing order cannot be used when the purchaser intends to help another individual.",
        "why": "The statewide standing order expressly supports dispensing to a person purchasing naloxone for another individual, including handling the transaction as a prescription for insurance billing."
      },
      {
        "text": "Dispense under the standing order but bill the coworker's prescription insurance even though the purchaser is the resident, because the coworker will ultimately use the medication.",
        "why": "For insurance billing and cost sharing, §19B(e) directs the pharmacy to treat the purchaser as the prescription recipient regardless of who ultimately uses the antagonist. Billing the coworker solely because of intended use would disregard this distinction."
      },
      {
        "text": "Dispense under the statewide standing order, make a reasonable effort to identify and bill the purchaser's insurance, and provide naloxone counseling and the required opioid-antagonist information material.",
        "why": "M.G.L. c.94C §19B permits third-party naloxone purchase and calls for reasonable purchaser-insurance identification/claim submission unless the purchaser elects to pay out of pocket. Board Policy 2024-01 also requires counseling and an opioid-antagonist information pamphlet."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §19B(b)–(e); MA Board Policy 2024-01 Naloxone Dispensing, §§I(B), I(D)–(G)",
    "url": "https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-044",
    "set": 9,
    "area": 3,
    "kind": "single",
    "topic": "Behind-the-counter pseudoephedrine: daily and 30-day base limits",
    "topicKey": "otc-pseudoephedrine",
    "stem": "A self-certified Massachusetts community pharmacy sells scheduled listed pseudoephedrine products in person, not by mail order or mobile vendor. A purchaser who presents valid government-issued photo identification has already bought 2.70 grams of pseudoephedrine BASE on the current calendar day and 8.30 grams during the relevant rolling 30-day period (including today's earlier purchases). All proposed quantities below are stated in pseudoephedrine BASE equivalents; there is no other applicable restriction or exemption. Which proposed transaction is legally permissible under the federal CMEA rules?",
    "choices": [
      {
        "text": "Sell an additional 0.90 grams with a signed log entry, because the calendar-day amount becomes exactly 3.60 grams.",
        "why": "The single-day quantity would be within the 3.6-gram daily limit, but the 30-day total would become 9.20 grams, above the separate 9-gram purchaser limit in 21 U.S.C. §844(a). Both limits must be satisfied."
      },
      {
        "text": "Sell an additional 0.60 grams with compliant photo-ID verification and logbook documentation, because the daily and rolling 30-day totals remain below their respective limits.",
        "why": "The resulting quantities are 3.30 grams today (2.70 + 0.60), below 3.60 grams, and 8.90 grams in 30 days (8.30 + 0.60), below 9.00 grams. The seller must also comply with the behind-the-counter and logbook requirements."
      },
      {
        "text": "Sell an additional 0.75 grams in two separate transactions at different registers, each with its own log entry, because no single transaction exceeds the daily limit.",
        "why": "Splitting does not evade the aggregate purchase limit. The 30-day total would be 9.05 grams, above 9.00 grams, even though the same-day total would be 3.45 grams."
      },
      {
        "text": "Sell an additional 0.60 grams without a photo ID or logbook signature because a quantity below the 3.60-gram daily ceiling is exempt from the identification requirement.",
        "why": "The low quantity does not create a general photo-ID and logbook exception; normal CMEA retail identification and recordkeeping apply to this sale."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 U.S.C. §§830(d)–(e), 844(a); 21 CFR 1314.20, 1314.25: retail pseudoephedrine base limits and sales records",
    "url": "https://www.fda.gov/drugs/fda-drug-info-rounds-video/combat-methamphetamine-epidemic-act-march-2017",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-045",
    "set": 9,
    "area": 4,
    "kind": "multi",
    "topic": "USP <800>: hazardous antineoplastic drug storage and environmental controls",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts institutional pharmacy handles a NIOSH Table 1 ANTINEOPLASTIC hazardous drug that must be crushed or otherwise manipulated for compounding. A portion of the same hazardous antineoplastic inventory requires refrigeration. The facility is reviewing compliant hazardous-drug storage under USP <800>; assume no other exemption applies. Which requirements or conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The Table 1 antineoplastic stock requiring manipulation must be stored separately from nonhazardous inventory in an externally ventilated negative-pressure room with at least 12 air changes per hour.",
        "why": "USP <800> storage requirements, summarized in USP's January 2026 FAQs, apply to NIOSH Table 1 antineoplastic drugs requiring manipulation beyond counting/repackaging final dosage forms. Such stock requires separation and externally vented negative-pressure storage with at least 12 ACPH."
      },
      {
        "text": "All sterile and nonsterile hazardous drugs must always be stored in separate rooms, regardless of their other storage or compounding conditions.",
        "why": "USP <800> permits storage of sterile and nonsterile hazardous drugs together, although hazardous inventory for nonsterile compounding should not be stored inside the sterile compounding area to avoid unnecessary traffic."
      },
      {
        "text": "Refrigerated NIOSH Table 1 antineoplastic drugs must be kept in a dedicated hazardous-drug refrigerator located in a negative-pressure area with at least 12 air changes per hour.",
        "why": "USP <800> requires refrigerated Table 1 antineoplastic hazardous drugs to be kept in a dedicated refrigerator in an appropriate negative-pressure storage or containment area with at least 12 ACPH."
      },
      {
        "text": "Negative pressure may be shut off overnight when the hazardous-drug storage room is unoccupied, provided the ventilation is restored before handling resumes.",
        "why": "USP <800> requires the negative-pressure condition of the hazardous-drug storage room to be maintained at all times; reducing or turning it off during nonuse is not permitted."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "USP <800> §5.2 Storage; USP <800> FAQs (Jan. 21, 2026), questions 25, 26 and 28; NIOSH 2024 HD list classification",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_800_FAQs_January2026.pdf?version=0",
    "verified": "2026-11-13"
  },
  {
    "id": "E30-046",
    "set": 10,
    "area": 1,
    "kind": "single",
    "topic": "Expired pharmacist registration: reactivation versus automatic renewal",
    "topicKey": "licensure-ce",
    "stem": "A pharmacist allowed a Massachusetts registration to expire on December 31, 2022, but has continuously practiced under an unrestricted New Hampshire license. In November 2026, the pharmacist wants to resume work in a Massachusetts community pharmacy. Neither license has been suspended or revoked, and no military-service extension or waiver applies. The pharmacist can document the required continuing education and pay the outstanding fees. Which statement BEST describes the Massachusetts reactivation requirements?",
    "choices": [
      {
        "text": "The pharmacist must complete the reactivation process, pass the MPJE, and satisfy the Board's other conditions before resuming Massachusetts practice.",
        "why": "Under 247 CMR 4.02(5), an otherwise nondisciplinary registration that has expired for more than two years requires passing the MPJE and meeting Board conditions before renewal. The current Massachusetts Pharmacist Licensing page describes reactivation application approval followed by MPJE eligibility. Active practice in another state does not itself reactivate the Massachusetts registration."
      },
      {
        "text": "Payment of the overdue fees and proof of current CE restore authority to practice as soon as a complete application is submitted.",
        "why": "Submitting the application and paying fees do not establish an active Massachusetts registration. The greater-than-two-year lapse invokes the additional requirements of 247 CMR 4.02(5). Practicing while the registration remains expired is unlicensed practice under 4.02(3)."
      },
      {
        "text": "Continuous practice under the New Hampshire license eliminates the MPJE requirement, although the pharmacist must still submit CE and fees.",
        "why": "The greater-than-two-year expiration rule does not contain an automatic MPJE exemption for a pharmacist who has practiced in another jurisdiction. Other-state license verification is part of the reactivation process, not a substitute for the required examination."
      },
      {
        "text": "Every pharmacist whose registration has expired for more than two years must automatically retake both the NAPLEX and the MPJE.",
        "why": "Section 4.02(5) expressly requires the MPJE and other Board-determined conditions; it does not automatically mandate the NAPLEX for every nondisciplinary expiration. The stem does not describe a suspended or revoked license, and Board-specific conditions should not be converted into a universal NAPLEX requirement."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 4.02(3)-(5), pharmacy practice not authorized after license expiration; Massachusetts Board Policy 2020-01 (adopted Feb. 6, 2020, revised May 14, 2021) reactivation after expiration more than one renewal cycle; Board approval of petition first, MPJE pass before license reactivation",
    "url": "https://www.mass.gov/doc/2020-01-pharmacist-license-reactivation-after-expiration-beyond-one-renewal-cycle-pdf/download",
    "verified": "2026-11-17",
    "note": "For licenses expired MORE THAN TWO YEARS, Board Policy 2020-01 first requires a written reactivation petition (CE, résumé, state license verification, fees); AFTER Board approval, MPJE must be passed before the Board reactivates. NAPLEX is not universally required if the pharmacist practiced elsewhere; Board may impose it for another factual setting."
  },
  {
    "id": "E30-047",
    "set": 10,
    "area": 2,
    "kind": "single",
    "topic": "Chlamydia EPT: paper prescription, unnamed partner and separate patient record",
    "topicKey": "expedited-partner-therapy",
    "stem": "A patient diagnosed with chlamydia brings two separate, otherwise valid prescriptions from an authorized Massachusetts practitioner: one for the patient's own treatment and a signed paper prescription for an unexamined sex partner. The second prescription uses 'EPT' instead of the partner's name and address. The partner's identity is unavailable. The pharmacist has no clinical reason to withhold the appropriately prescribed Schedule VI therapy. Which dispensing approach is BEST supported by Massachusetts requirements?",
    "choices": [
      {
        "text": "Request a replacement electronic prescription identifying the partner by name and address before dispensing the partner's treatment.",
        "why": "The EPT framework expressly permits 'Expedited Partner Therapy,' 'E.P.T.' or 'EPT' in place of the partner's name and address. An otherwise lawful paper EPT prescription is also covered by the ePrescribing exception in 105 CMR 721.070(A)(7); a replacement is not necessary solely for these features."
      },
      {
        "text": "Fill both prescriptions under the diagnosed patient's profile and place the patient's name on both labels because that patient is collecting the drugs.",
        "why": "The partner's treatment requires its own prescription and appropriate EPT profile and label. The collecting patient's identity should not be substituted as the treated recipient merely because the patient presents both prescriptions."
      },
      {
        "text": "Process the partner's separate prescription using an EPT patient profile and an EPT label rather than substituting the diagnosed patient's identity.",
        "why": "Board/Drug Control Program Policy 2020-08 permits a separate EPT prescription for chlamydia with 'EPT' replacing the partner's name and address and directs creation of the corresponding EPT patient profile and prescription label. The absence of a direct examination is intrinsic to authorized EPT, not an automatic reason for refusal."
      },
      {
        "text": "Require confirmation that the practitioner examined the partner before dispensing, even though the prescription is expressly designated EPT.",
        "why": "The Massachusetts EPT policy concerns treatment of the sex partner of a person diagnosed with chlamydia without examining or testing that partner. Requiring a prior examination in every such case would defeat this specifically authorized pathway. Clinical concerns must still be addressed when present."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "MA Board/DCP Policy 2020-08, sections I-II; 105 CMR 721.020(D)(4) and 721.070(A)(7); 105 CMR 700.003 EPT provision",
    "url": "https://www.mass.gov/policy-statement/expedited-partner-therapy-prescriptions",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-048",
    "set": 10,
    "area": 2,
    "kind": "multi",
    "topic": "HIPAA access to one's own records: fees, electronic format and off-site storage",
    "topicKey": "hipaa-access",
    "stem": "An adult submits a valid request directly to a HIPAA-covered Massachusetts pharmacy for an electronic PDF copy of the adult's own prescription and billing records. The records belong to the designated record set and are held electronically by the pharmacy's business associate. A PDF is readily producible. Identity has been verified, but the patient owes an unrelated unpaid prescription bill. No permitted ground for denying access or special confidentiality restriction applies. Considering the federal HIPAA access rule, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy may withhold the records until the patient pays the outstanding prescription bill, even if any lawful copying charge has been paid.",
        "why": "HHS expressly states that unpaid charges for health care services are not a basis for denying an individual's access to their own PHI. Any permissible copying fee is a separate matter and does not turn the unrelated prescription debt into a lawful access condition."
      },
      {
        "text": "Any fee charged for the copy must be reasonable and cost-based; permitted copying labor may be included, but search and retrieval costs may not.",
        "why": "45 CFR 164.524(c)(4) limits an individual's copy fee to specified costs, including copying labor and applicable supplies or postage. HHS clarifies that searching for and retrieving the records are not chargeable components of this individual-access fee. This request is for the patient's own copy, not a third-party records request."
      },
      {
        "text": "The pharmacy must provide the electronic PDF requested rather than insist on paper solely for administrative convenience.",
        "why": "Under 45 CFR 164.524(c)(2)(ii), electronically maintained PHI must be provided in the requested electronic form and format when readily producible. The stem establishes that PDF is readily producible, so convenience alone does not justify substituting paper."
      },
      {
        "text": "Because the business associate holds the records off-site, the pharmacy automatically has 60 days to respond without sending an extension notice.",
        "why": "The ordinary outer limit is 30 calendar days from receipt of the request, including when records are held by a business associate. Only one extension of up to 30 additional days is available when needed, with written reasons and a completion date provided within the initial period. Off-site storage does not automatically grant 60 days."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "45 CFR 164.524(b)(2), (c)(2)(ii), (c)(4); HHS individual-access FAQs on unpaid bills, fees and business-associate records",
    "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.524",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-049",
    "set": 10,
    "area": 3,
    "kind": "single",
    "topic": "Schedule II stock-shortage partial fill: elapsed hours across a weekend",
    "topicKey": "cii-partial-fills",
    "stem": "A Massachusetts pharmacy receives an otherwise valid in-state electronic Schedule II prescription for 60 tablets. At 4:00 p.m. Friday, it dispenses its only 10 tablets and records a partial fill solely because of insufficient stock. The patient is not terminally ill or an LTCF resident. Neither the patient nor prescriber has requested a partial fill under the separate request-based pathway. The remaining stock arrives at 5:00 p.m. Monday; no clock change occurred over the weekend. What is the MOST appropriate action under the stock-shortage partial-fill provision?",
    "choices": [
      {
        "text": "Dispense the remaining 50 tablets under the original prescription because fewer than 30 days have elapsed since it was issued.",
        "why": "The separate 30-day request-based pathway is not the documented basis for this partial fill. Under 21 CFR 1306.13(a), the stock-shortage balance must be supplied within 72 hours of the first partial filling; the stem expressly excludes the other pathways."
      },
      {
        "text": "Start a new 72-hour completion period when the shipment arrives and dispense the balance within that new period.",
        "why": "The shortage deadline runs from the first partial dispensing, not from replenishment or the date the pharmacist learns that stock is available. New inventory does not restart the clock."
      },
      {
        "text": "Dispense the balance because Saturday and Sunday are excluded when calculating the 72-hour completion period.",
        "why": "The regulation specifies 72 hours, not 72 business hours. Friday at 4:00 p.m. to Monday at 5:00 p.m. is 73 elapsed hours when no clock change occurs, so the shortage-completion period has ended."
      },
      {
        "text": "Do not dispense the remaining balance under the original shortage partial fill; notify the prescriber, and obtain a new prescription before supplying any further quantity.",
        "why": "21 CFR 1306.13(a) requires prescriber notification when the balance is not or cannot be filled within 72 hours and states that no further quantity may be supplied beyond that period without a new prescription. The state request-based rule in 105 CMR 721.055 is a distinct route, not an automatic extension of this shortage fill."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1306.13(a), contrasted with 1306.13(b)-(c) and 105 CMR 721.055",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-050",
    "set": 10,
    "area": 4,
    "kind": "multi",
    "topic": "Controlled-drug collection: patient returns versus pharmacy inventory and sealed liners",
    "topicKey": "security-loss",
    "stem": "A Massachusetts retail pharmacy has modified its DEA registration to become an authorized collector and meets applicable state and environmental requirements. Its patient drug-collection receptacle is at the pharmacy's registered premises, not at an LTCF. The inner liner needs replacement. Separately, the pharmacy has expired Schedule II stock that has never been dispensed to a patient. Which procedures comply with the federal disposal rules? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Place the expired pharmacy stock into the patient collection receptacle after documenting a deduction from the pharmacy's inventory.",
        "why": "A patient collection receptacle is not a disposal route for the registrant's own controlled-substance inventory. The pharmacy must use an authorized registrant-disposal method under 21 CFR 1317.05(a), such as transfer to a reverse distributor; an inventory entry does not convert the stock into an ultimate-user return."
      },
      {
        "text": "Have the inner liner installed and removed by, or under the supervision of, at least two collector employees, and have two employees seal it immediately upon removal.",
        "why": "For this on-site retail receptacle, 21 CFR 1317.75(g) requires at least two collector employees for installation/removal or their supervision. Section 1317.60(c) additionally requires two employees to seal the liner immediately after removal. The separate LTCF staffing rules are not the scenario presented."
      },
      {
        "text": "Reopen the sealed liner with two pharmacist witnesses to count the controlled substances before sending it for destruction.",
        "why": "Two witnesses do not create an exception to the prohibition. Under 21 CFR 1317.60(c), a sealed liner must not be opened, x-rayed, analyzed or otherwise penetrated. Section 1317.75(c) also prohibits counting, sorting or inventorying individual contents after deposit."
      },
      {
        "text": "Arrange a lawful transfer of the pharmacy's expired stock to a registered reverse distributor separately from the ultimate-user collection process.",
        "why": "21 CFR 1317.05(a)(2) authorizes disposal of practitioner inventory through delivery to a reverse distributor by the permitted pickup/carrier arrangements. Applicable controlled-substance transfer records and state requirements still apply; this is distinct from accepting patients' medications into a collection receptacle."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "21 CFR 1317.05(a)(2), 1317.60(c), 1317.75(b)-(c),(g); DEA Disposal Q&A",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1317",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-051",
    "set": 11,
    "area": 1,
    "kind": "single",
    "topic": "Unexpected Manager of Record absence: interim appointment, inventory, and 100-day trigger",
    "topicKey": "workforce-supervision",
    "stem": "A Massachusetts resident retail pharmacy's Manager of Record (MOR) is unexpectedly hospitalized. The pharmacy learns that the MOR is likely to be unavailable for 45 days, cannot participate in the controlled-substance inventory, and has not resigned or been terminated. A Massachusetts-registered staff pharmacist is available to help. The absence ultimately lasts 105 days. Under 247 CMR 9.23(5), which response MOST completely satisfies the requirements?",
    "choices": [
      {
        "text": "Appoint a Board-registered Interim Manager within five days of the unplanned absence; have another registered pharmacist perform the required controlled-substance inventory because the MOR is unavailable; submit an application to change the MOR when the absence reaches 100 days.",
        "why": "247 CMR 9.23(5)(b) requires an Interim Manager within five days of an unplanned absence likely to last at least 30 days. Section 9.23(5)(c) allows another registered pharmacist to perform the controlled-substance inventory if the MOR is unexpectedly unavailable. Section 9.23(5)(d) requires a change-of-MOR application if the absence reaches 100 days."
      },
      {
        "text": "Appoint an Interim Manager within 14 calendar days; have another registered pharmacist complete the required inventory; submit a change-of-MOR application when the absence reaches 100 days.",
        "why": "The inventory and 100-day elements are appropriate, but the deadline for appointing an Interim Manager for this unplanned absence is five days, not 14. The separate notification period for a resignation or change of MOR is not the interim-appointment deadline."
      },
      {
        "text": "Appoint an Interim Manager within five days and file a change-of-MOR application after 100 days, but postpone the controlled-substance inventory until the hospitalized MOR can sign it.",
        "why": "An unexpected absence does not waive the inventory requirement. The regulation specifically provides that another registered pharmacist shall perform the controlled-substance inventory if the MOR is unexpectedly unavailable."
      },
      {
        "text": "Appoint an Interim Manager within five days and have another registered pharmacist perform the inventory; a change-of-MOR application is unnecessary after 100 days as long as the Interim Manager remains licensed.",
        "why": "An Interim Manager's continuing licensure does not erase the separate 100-day threshold in 247 CMR 9.23(5)(d). An application for a change of MOR is required when the original MOR has been away for 100 days or more."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 9.23(5)(b)–(d); MA Board Information for Managers of Record (unplanned absence guidance)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-052",
    "set": 11,
    "area": 2,
    "kind": "single",
    "topic": "Mifepristone REMS: delivery after the four-calendar-day window",
    "topicKey": "rems",
    "stem": "A specially certified Massachusetts retail pharmacy receives an otherwise valid prescription for mifepristone for medication abortion from a certified prescriber. The required Patient Agreement Form has been completed, the pharmacy has verified prescriber certification, and no clinical or other state-law restriction is present. The pharmacy's tracked shipping service estimates the medication will reach the patient MORE THAN FOUR CALENDAR DAYS after the pharmacy received the prescription. Under the FDA Mifepristone REMS, which action is MOST appropriate?",
    "choices": [
      {
        "text": "Ship without additional contact because using a tracked carrier automatically waives the REMS delivery timeframe.",
        "why": "Tracking is a separate pharmacy-certification safeguard. When delivery will take more than four calendar days after receipt of the prescription, the REMS also requires confirmation with the certified prescriber that dispensing remains appropriate and documentation of the decision."
      },
      {
        "text": "Require in-person pickup, because a certified retail pharmacy may not dispense mifepristone through a shipping service.",
        "why": "The current Mifepristone REMS permits dispensing by specially certified retail pharmacies and does not impose a categorical in-person dispensing rule. The pharmacy must follow tracking and other REMS safeguards."
      },
      {
        "text": "Reject the prescription permanently and require a new prescription even if the certified prescriber determines that delayed delivery would still be appropriate.",
        "why": "The REMS provides a mechanism for delayed delivery: contact and confirm the certified prescriber's clinical determination and document it. It does not universally require a newly issued prescription merely because shipping exceeds four calendar days."
      },
      {
        "text": "Contact the certified prescriber, confirm that dispensing remains appropriate despite delivery taking more than four calendar days, document the prescriber's decision, and use a compliant tracked service if dispensing proceeds.",
        "why": "The FDA-approved pharmacy-certification requirements specifically direct a certified pharmacy to confirm with the prescriber the appropriateness of dispensing when delivery exceeds four calendar days after receipt of the prescription, and to document that decision. Tracked shipping and all other REMS safeguards still apply."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "FDA Mifepristone REMS Pharmacy Agreement requirements; FDA 2023 REMS modification review, pharmacy certification §2(a)(iv)(b)–(c)",
    "url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2023/020687Orig1s025.pdf",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-053",
    "set": 11,
    "area": 2,
    "kind": "multi",
    "topic": "HIPAA: fully self-paid prescription and mandatory restriction on health-plan disclosures",
    "topicKey": "hipaa-access",
    "stem": "A HIPAA-covered Massachusetts community pharmacy dispenses a routine Schedule VI medication. The patient pays its entire charge out of pocket and explicitly asks the pharmacy NOT to disclose information solely about that prescription to the patient's health plan for PAYMENT or HEALTH CARE OPERATIONS. No law independently requires such a disclosure. A second, unrelated prescription is only partially paid for by the patient; the health plan pays the rest, and the pharmacy has not voluntarily agreed to a restriction for it. Later, another treating clinician requests relevant prescription history for treatment. Assume no other federal or Massachusetts confidentiality rule applies. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy must honor the requested health-plan restriction for the fully self-paid prescription, as long as the contemplated disclosure is for payment or health care operations and is not required by law.",
        "why": "45 CFR 164.522(a)(1)(vi) requires a covered health care provider to agree to an individual's requested restriction on disclosures to a health plan for payment or health care operations if the individual paid in full for the item or service and disclosure is not otherwise required by law."
      },
      {
        "text": "HIPAA automatically obligates the pharmacy to extend the identical restriction to the second prescription even though the health plan paid part of its cost.",
        "why": "The mandatory exception turns on full payment of the specific item or service by the individual or someone other than the health plan. The pharmacy may voluntarily agree to other restrictions, but it is not automatically required to extend this one to a different, partly plan-paid prescription."
      },
      {
        "text": "The pharmacy may disclose relevant prescription history to another clinician for the patient's treatment without a separate HIPAA authorization, when otherwise permitted; the stated restriction concerning health-plan payment or operations does not itself prohibit that treatment disclosure.",
        "why": "The mandatory self-pay restriction concerns specified disclosures to a health plan for payment or health care operations, not all permitted treatment disclosures to another treating provider. HIPAA generally permits provider-to-provider treatment disclosures without a separate patient authorization, subject to other applicable law and any separately agreed restriction."
      },
      {
        "text": "For disclosure of the fully paid prescription to a treating clinician, HIPAA always requires a minimum-necessary determination and an individual authorization before any information may be released.",
        "why": "Disclosures to, or requests by, a health care provider for treatment are exempt from HIPAA's minimum-necessary requirement under 45 CFR 164.502(b)(2)(i). HIPAA does not ordinarily require a signed authorization for permissible disclosures for treatment."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "45 CFR 164.522(a)(1)(vi) (fully paid health-plan restriction); 45 CFR 164.506 (TPO); 45 CFR 164.502(b)(2)(i) (treatment exemption)",
    "url": "https://www.hhs.gov/hipaa/for-professionals/faq/under-hipaa-may-an-individual-request-that-a-covered-entity-restrict-how-it-uses-or-discloses-that-individuals-protect-health-information/index.html",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-054",
    "set": 11,
    "area": 3,
    "kind": "multi",
    "topic": "Schedule IV partial filling versus a separately authorized refill",
    "topicKey": "controlled-quantity",
    "stem": "On May 1, 2026, a Massachusetts prescriber issues an otherwise valid Schedule IV prescription for 90 tablets with ZERO authorized refills. The patient requests and receives 30 tablets on May 3 and another 30 tablets on June 3 as documented PARTIAL FILLS of the same 90-tablet prescription. On November 14, 2026, the patient asks for the last 30 tablets. Assume no change in prescriber authorization, no other restriction, and all relevant pharmacy documentation was made for the earlier installments. Under the federal Schedule III–V partial-filling rule, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The June partial dispensing was automatically unlawful because the prescription authorized zero refills, even though the total dispensed had not reached 90 tablets.",
        "why": "21 CFR 1306.23 permits a Schedule III–V prescription to be partially filled and requires each partial to be recorded in the same manner as a refill. A partial fill of the original prescribed total is not automatically a new authorized refill merely because the documentation resembles refill records."
      },
      {
        "text": "Each partial filling must be documented in the same manner as a refilling, and the combined quantity from all portions cannot exceed the prescribed 90 tablets.",
        "why": "21 CFR 1306.23(a) requires refill-style records for each partial filling; subsection (b) prohibits the sum of all partial quantities from exceeding the amount prescribed."
      },
      {
        "text": "The final 30 tablets cannot be supplied on November 14 under the May 1 prescription, because no Schedule III–V partial dispensing is allowed more than six months after the original issue date.",
        "why": "21 CFR 1306.23(c) bars partial dispensing after six months from the date the prescription was issued. November 14 is well beyond six months from May 1, even though some of the original prescribed quantity remains."
      },
      {
        "text": "A pharmacist cannot reset the six-month clock by documenting the June 3 installment as a refill; the six months are measured from the original prescription issue date.",
        "why": "The six-month maximum in 21 CFR 1306.23(c) runs from the date the practitioner issued the original prescription, not the date of the most recent partial dispensing or pharmacy record entry."
      }
    ],
    "correct": [
      "B",
      "C",
      "D"
    ],
    "citation": "21 CFR 1306.23(a)–(c) (Schedule III–V partial fills); 21 CFR 1306.22(a) (Schedule III–IV refills); DEA Pharmacist's Manual, partial dispensing",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.23",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-055",
    "set": 11,
    "area": 4,
    "kind": "single",
    "topic": "Massachusetts central fill: federal controlled drugs versus PMP-reportable Schedule VI",
    "topicKey": "pharmacy-operations",
    "stem": "A Massachusetts-licensed originating retail pharmacy uses a properly licensed and DEA-registered central-fill pharmacy. The shared-service records, patient notice and opt-out mechanism, relevant DEA requirements, and all other conditions are satisfied. Three different prescriptions are to be centrally filled: Schedule II oxycodone, Massachusetts Schedule VI gabapentin (reportable to MassPAT), and Massachusetts Schedule VI lisinopril (not reportable to MassPAT). Under the Board's Shared Pharmacy Services Policy 2021-02, as revised February 6, 2025, which delivery plan is MOST appropriate?",
    "choices": [
      {
        "text": "Have the central-fill pharmacy send gabapentin and lisinopril directly to the patient while sending oxycodone to the originating pharmacy, because only federally scheduled drugs need to be routed through the originating pharmacy.",
        "why": "The central-fill policy specifically excludes Schedule VI products requiring MassPAT reporting, such as gabapentin, from the Schedule VI direct-to-patient shipment exception. Gabapentin's federal nonscheduled status alone does not make direct shipment from central fill permissible."
      },
      {
        "text": "Send centrally filled oxycodone and gabapentin to the originating pharmacy for final dispensing; the non-PMP-reportable lisinopril may instead be shipped directly to the patient by central fill when all other requirements are met.",
        "why": "Policy 2021-02 IV(b)(iii) requires centrally filled Schedule II–V drugs to be delivered to the originating pharmacy. Section IV(b)(iv) permits direct patient shipment of Schedule VI drugs except those requiring PMP reporting, such as gabapentin. Lisinopril is a Schedule VI example not subject to PMP reporting."
      },
      {
        "text": "Route every Schedule VI prescription through the originating pharmacy, because the Board categorically prohibits all direct-to-patient shipment from central-fill pharmacies regardless of PMP reporting.",
        "why": "The Board's revised policy expressly allows certain non-PMP-reportable Schedule VI prescriptions to be delivered or shipped directly from central fill to the patient. Therefore this blanket description is incorrect."
      },
      {
        "text": "Send oxycodone and lisinopril directly to the patient while routing gabapentin through the originating pharmacy, because the central-fill pharmacy's DEA registration replaces the originating pharmacy's final-dispensing duty for Schedule II medications.",
        "why": "Even when the central-fill pharmacy is properly DEA registered, the Board policy expressly directs centrally filled Schedule II–V controlled substances to the pharmacy where the prescription originated for final dispensing, not directly to the patient."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "MA Board Policy 2021-02, revised Feb. 6, 2025, §§III(k)–(l), IV(b)(i)–(v), Shared Pharmacy Service Models",
    "url": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download",
    "verified": "2026-11-14"
  },
  {
    "id": "E30-056",
    "set": 12,
    "area": 1,
    "kind": "single",
    "topic": "Intern supervision: four-intern vaccination-clinic exception and 12-hour credit limit",
    "topicKey": "intern-education",
    "stem": "A Massachusetts pharmacist preceptor is comparing staffing plans for an institutional pharmacy's dispensing area and a separate, exclusively immunization-focused outreach clinic. Unless otherwise stated, every pharmacy intern holds an active Massachusetts intern license, is properly qualified for the proposed activities, and will be directly supervised; there is no separate Board waiver. Under 247 CMR 8.01 and Board Policy 2026-02, which arrangement is permissible?",
    "choices": [
      {
        "text": "One pharmacist directly supervises three licensed pharmacy interns concurrently filling and dispensing prescriptions in the institutional pharmacy, because the Board permits four interns whenever a pharmacist stays on the premises.",
        "why": "247 CMR 8.01(16) ordinarily limits a pharmacist preceptor to directly supervising two pharmacy interns at a time. Policy 2026-02 allows up to four only under specifically limited conditions, including an exclusive immunization clinic, not three interns concurrently filling prescriptions."
      },
      {
        "text": "One pharmacist preceptor directly supervises four appropriately licensed and qualified pharmacy interns exclusively conducting an immunization clinic, with all applicable immunization requirements satisfied.",
        "why": "Policy 2026-02, Section II(B), expressly permits a preceptor to directly supervise up to four pharmacy interns at one time when exclusively conducting immunization clinics. Their active Massachusetts intern licenses, appropriate qualifications, and continuing direct supervision remain necessary."
      },
      {
        "text": "An unlicensed PharmD student may begin a hospital internship under close preceptor supervision as long as the student does not handle Schedule II medications before obtaining a Massachusetts intern license.",
        "why": "Policy 2026-02, Section II(E), requires pharmacy students, including foreign pharmacy students, to be licensed as Massachusetts pharmacy interns before starting an internship in any practice setting, including hospitals. Avoiding Schedule II products does not replace intern licensure."
      },
      {
        "text": "A licensed intern who works 14 hours in one day during an emergency may receive all 14 hours as Massachusetts pharmacy internship credit when the pharmacist documents the emergency.",
        "why": "247 CMR 8.01(4) limits pharmacy internship credit to no more than 12 hours per day. An exception permitting extended work in certain circumstances does not change the independent 12-hour daily internship-credit limit."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 8.01(3)–(4),(16); Board Policy 2026-02, Section II(A)–(E) (adopted Sept. 3, 2026)",
    "url": "https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-057",
    "set": 12,
    "area": 2,
    "kind": "single",
    "topic": "Buprenorphine prescriptions after the DATA/X-waiver repeal and MATE Act",
    "topicKey": "opioid-oud",
    "stem": "A Massachusetts community pharmacist receives a buprenorphine/naloxone sublingual prescription for opioid use disorder from a Massachusetts-authorized practitioner with a current DEA registration that includes Schedule III authority. The pharmacist confirms a legitimate medical purpose, proper prescription elements, and compliance with all applicable state requirements. The practitioner treats more than 275 patients with OUD, has no former DATA/X-waiver number, and has satisfied the applicable federal training or alternative-qualification attestation at DEA registration renewal. Which conclusion is MOST accurate in November 2026?",
    "choices": [
      {
        "text": "The pharmacist must reject the prescription until the practitioner obtains a new X-waiver identifier, because the repeal applies only to patients who began treatment before 2023.",
        "why": "The Consolidated Appropriations Act of 2023 eliminated the federal DATA-waiver requirement effective December 29, 2022, for authorized practitioners. This change is not limited to patients already receiving treatment, and an X-waiver number is no longer a prescription requirement."
      },
      {
        "text": "The pharmacist may dispense only after confirming that the practitioner treats no more than 275 OUD patients, because the former federal patient-cap system is still enforced for office-based treatment.",
        "why": "The former federal DATA-waiver patient caps were removed along with the waiver requirement. The pharmacist must still evaluate an otherwise valid controlled-substance prescription and applicable state law, but the old numerical patient cap is not a federal reason to reject this prescription."
      },
      {
        "text": "Before dispensing any buprenorphine prescription, federal law requires the pharmacist to obtain and retain the prescriber's eight-hour MATE Act course certificate for that individual patient.",
        "why": "The MATE Act training, credentialing, or education attestation is a condition associated with the qualified practitioner's first applicable DEA registration or renewal, not a requirement that the dispensing pharmacy collect a training certificate for each prescription. Recognized alternative qualification pathways also exist."
      },
      {
        "text": "The pharmacist may dispense after the usual Schedule III validity and corresponding-responsibility checks; no X-waiver number or former federal patient cap is required, and MATE Act attestation is handled through the practitioner’s DEA registration process.",
        "why": "DEA and SAMHSA confirm that the DATA/X-waiver identifier and associated federal patient caps were eliminated. The qualified practitioner must maintain ordinary Schedule III prescribing authority, comply with applicable registration/training obligations, and issue prescriptions for a legitimate medical purpose. The pharmacist retains normal corresponding responsibility."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "Consolidated Appropriations Act of 2023 §§1262–1263; 21 U.S.C. §823(l); 21 CFR 1306.04(a); DEA Buprenorphine (MOUD) Q&A (Nov. 28, 2023)",
    "url": "https://www.deadiversion.usdoj.gov/faq/buprenorphine-faq.html",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-058",
    "set": 12,
    "area": 2,
    "kind": "multi",
    "topic": "Massachusetts ePrescribing outage: oral Schedule IV follow-up and pharmacist verification duties",
    "topicKey": "controlled-prescriptions",
    "stem": "A Massachusetts-authorized practitioner cannot use ePrescribing because of a temporary electrical failure. The practitioner telephones an otherwise valid Schedule IV lorazepam prescription to a community pharmacist. The pharmacist verifies the order, its legitimate medical purpose, and the prescriber's identity and records the oral prescription. No effort to circumvent ePrescribing and no other exception is involved. Which conclusions are supported by Massachusetts and federal law? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The temporary electrical failure can qualify as an ePrescribing exception; the pharmacist may accept an otherwise lawful oral Schedule IV prescription.",
        "why": "Correct. 105 CMR 721.070(A)(2) expressly permits an oral or written prescription during temporary technological or electrical failure. Federal 21 CFR 1306.21 generally allows lawful Schedule IV oral orders when ordinary authenticity and prescription requirements are satisfied."
      },
      {
        "text": "Because federal law permits oral Schedule IV prescriptions, Massachusetts never requires the prescriber to send a follow-up prescription documenting the oral order.",
        "why": "Incorrect. M.G.L. c.94C §20(c) imposes a subsequent prescription duty for oral Schedule II–V prescriptions, and 105 CMR 721.070(B) implements follow-up for oral prescriptions issued under ePrescribing exceptions. No universal absence of follow-up can be inferred from federal Schedule IV rules."
      },
      {
        "text": "A separate written or electronic follow-up documenting the earlier oral order is required under Massachusetts law, and the dispensing pharmacy must associate the follow-up with its written record of the oral prescription.",
        "why": "Correct. The follow-up and pharmacy record-attachment duties are supported by M.G.L. c.94C §20(c) and 105 CMR 721.070(B). The statute describes a two-day electronic default or seven-calendar-day written exception, whereas the DPH implementing rule uses seven BUSINESS days for an ePrescribing exception. Because these differ, this question deliberately does not assert one universal deadline; practitioners should comply with applicable requirements and obtain agency clarification when necessary."
      },
      {
        "text": "The pharmacist is not required to independently verify that the prescriber qualifies for an ePrescribing exception when the oral prescription is otherwise valid, but must still establish authenticity and legal dispensing requirements.",
        "why": "Correct. 105 CMR 721.070(C) specifically relieves the pharmacist from verifying the qualifying ePrescribing exception. That narrow exception does not excuse pharmacist verification of an oral prescription's lawful source or medical legitimacy."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "M.G.L. c.94C §20(a)-(c); 105 CMR 721.070(A)(2),(B),(C); 21 CFR 1306.21; DPH DCP 19-12-108 (statute/regulation follow-up day-count discrepancy noted; not resolved)",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-17",
    "note": "Revision 2 removes an unresolvable numeric 7 BUSINESS-day distractor: M.G.L. c.94C §20(c) refers to two days (ordinary electronic follow-up) or seven DAYS (commissioner exception), but 105 CMR 721.070(B) says seven BUSINESS days for qualifying eRx exceptions. This rewritten question tests only common, independently supported oral-Rx follow-up and record linkage requirements. A/C/D remain correct. Agency reconciliation is still required for real deadline calculations.",
    "revision": 2
  },
  {
    "id": "E30-059",
    "set": 12,
    "area": 3,
    "kind": "single",
    "topic": "Out-of-state controlled prescriptions: 30-day limit, mandatory verification and Schedule II narcotic geography",
    "topicKey": "controlled-quantity",
    "stem": "A Massachusetts walk-in retail pharmacist evaluates FOUR unrelated prescriptions written by practitioners who are not registered in Massachusetts but are properly licensed, authorized, and DEA-registered in the states where they reside or practice. Assume every prescription otherwise satisfies federal and Massachusetts requirements, no special M.G.L. c.94C §18A exception applies, and the pharmacy is not acting as a mail-order pharmacy. Under M.G.L. c.94C §18, which prescription may the pharmacist legally fill?",
    "choices": [
      {
        "text": "A Rhode Island prescriber's Schedule IV temazepam prescription issued 24 days ago, after the pharmacist independently verifies the prescription with the prescriber and confirms its validity.",
        "why": "Under M.G.L. c.94C §18(c), a Massachusetts retail pharmacist may fill an otherwise valid out-of-state Schedule III–VI prescription issued within the preceding 30 days. For Schedule III–V drugs, the pharmacist must verify the prescription by telephone or other means. This 24-day-old, verified Schedule IV prescription satisfies those stated conditions."
      },
      {
        "text": "A Connecticut prescriber's Schedule IV zolpidem prescription issued 33 days ago, after the pharmacist directly verifies the prescription and confirms it was valid when issued.",
        "why": "Verification does not extend M.G.L. c.94C §18(c)'s requirement that an out-of-state Schedule III–VI prescription be issued within the preceding 30 days. At 33 days, it is outside that authorization."
      },
      {
        "text": "A New Hampshire prescriber's Schedule III prescription issued 10 days ago when the pharmacist cannot obtain prescriber verification despite documented, reasonable good-faith efforts.",
        "why": "Section 18(c) specifically prohibits filling out-of-state Schedule III–V prescriptions when the required prescriber verification cannot be obtained. Documented good-faith attempts protect the pharmacist's refusal; they do not substitute for successful verification."
      },
      {
        "text": "A Florida prescriber's Schedule II narcotic oxycodone prescription issued two days ago and successfully verified, even though the prescriber is not licensed or registered in Maine or a state contiguous with Massachusetts.",
        "why": "Section 18(d½) generally restricts out-of-state Schedule II narcotic prescriptions filled for Massachusetts patients to authorized practitioners in Maine or a state contiguous with Massachusetts, subject to specified exceptions excluded by the question. Florida does not qualify merely because the prescription is recent and verified."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.94C §18(c),(d½): out-of-state Schedule III–VI prescriptions and Schedule II narcotic limitations",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-060",
    "set": 12,
    "area": 4,
    "kind": "multi",
    "topic": "Nonsterile compounding: manufacturer reconstitution, patient-requested flavoring and premeasured kits",
    "topicKey": "nonsterile-compounding",
    "stem": "A Massachusetts community pharmacy without a complex nonsterile-compounding specialty license has appropriate facilities and staff for routine nonhazardous Schedule VI dispensing. For Patient A, staff reconstitute a commercially manufactured antibiotic powder exactly according to its FDA-approved labeling. For Patient B, staff add a flavoring agent to a conventional oral suspension at the patient's request, confirming suitable stability and concentration and recording the change. For Patient C, staff use a premeasured compounding kit to prepare a patient-specific nonsterile drug. No hazardous ingredients, complex technique, or additional restriction applies. Under Massachusetts Board Policy 2023-07 (revised February 6, 2025), which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Adding flavor to the conventionally manufactured suspension is treated the same as manufacturer-directed reconstitution; neither activity counts as nonsterile compounding, so no compounding record or special label statement is needed for Patient B.",
        "why": "Policy 2023-07, Section III(B), excludes simple manufacturer-directed reconstitution from the compounding definition, but Section III(C) explicitly classifies flavoring a conventionally manufactured nonsterile drug as compounding. Compounding records and the appropriate nonsterile-compounded and flavoring label statements remain necessary."
      },
      {
        "text": "Reconstituting the antibiotic exactly in accordance with the manufacturer's labeling does not itself constitute nonsterile compounding; the Board recommends a reconstitution log for such manufactured products.",
        "why": "Policy 2023-07, Section III(B), excludes straightforward, manufacturer-directed reconstitution from the nonsterile-compounding definition. Section VI(A) recommends a reconstitution log or similar documentation for commercially available products; this recommendation is not equivalent to saying that this activity is a separately compounded preparation."
      },
      {
        "text": "For a Schedule VI preparation, a patient or the patient's agent may request flavoring without a new prescriber order when appropriate; the pharmacy must comply with compounding documentation and add the applicable nonsterile-compounded and flavored labeling.",
        "why": "Policy 2023-07, Section II(B), permits patient- or agent-requested flavoring of Schedule VI medications, with prescription updates under Board Policy 2018-01. Sections III(C), V(B), and VI(B)–(C) require stability attention, a compounding record, and appropriate compounded-preparation and flavoring label statements."
      },
      {
        "text": "A premeasured kit does not escape the nonsterile-compounding rules merely because its ingredients were measured beforehand; applicable USP requirements and a compounding record still apply.",
        "why": "Policy 2023-07, Section III(E), states that premeasured compounding kits remain compounding and must meet relevant USP standards. Section VI(C) permits appropriate compounding record and master formulation information to be captured on a retrievable log sheet, rather than waiving it."
      }
    ],
    "correct": [
      "B",
      "C",
      "D"
    ],
    "citation": "Massachusetts Board Policy 2023-07 §§II(B),III(B)–(E),V(B),VI(A)–(C) (revised Feb. 6, 2025)",
    "url": "https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-061",
    "set": 13,
    "area": 1,
    "kind": "multi",
    "topic": "CDTM agreement: biennial renewal, original records, and continuity of care",
    "topicKey": "cdtm",
    "stem": "A qualified Massachusetts community pharmacist and supervising physician signed a compliant collaborative drug therapy management (CDTM) agreement on November 1, 2024. The pharmacist maintains the required professional qualifications, annual CDTM continuing education, and written patient referrals and consent. As of November 15, 2026, neither professional has reviewed or renewed the agreement, and they are considering ending the collaborative service. No replacement agreement has been executed. Which statements accurately describe the obligations under 247 CMR 16.04? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist may continue initiating and modifying therapy under the original agreement indefinitely because both professionals remain licensed and no written termination has been issued.",
        "why": "Maintaining individual qualifications does not extend an unrenewed agreement indefinitely. Section 16.04(4) requires the pharmacist and supervising physician to review and renew the agreement at least every two years; an expired agreement is not a current basis to exercise CDTM authority."
      },
      {
        "text": "The authorized pharmacist and supervising physician must review and renew their collaborative practice agreement at least every two years; the original referral and consent do not replace this renewal duty.",
        "why": "247 CMR 16.04(4) imposes biennial review and renewal on the agreement itself. A valid prior patient referral, consent, and current licensure are separate prerequisites and cannot automatically extend the expired agreement."
      },
      {
        "text": "The pharmacist must keep the originals of the agreement, the patient referral, and consent exclusively at the pharmacy, while the supervising physician may retain copies instead.",
        "why": "This reverses 247 CMR 16.04(6): the pharmacist maintains readily retrievable copies at the primary practice site, while the supervising physician retains the originals of the current agreement, referral, and consent in the patient's medical record."
      },
      {
        "text": "Before nonrenewal or termination, the pharmacist and supervising physician must arrange uninterrupted continuation of the patient's drug therapy and inform the patient in writing of the termination and how therapy will continue.",
        "why": "247 CMR 16.04(5) requires an uninterrupted-care arrangement before termination or nonrenewal and written patient notification describing the termination and procedures for continuation of drug therapy; simply ending the agreement without transition planning is insufficient."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 16.04(4)–(6): biennial renewal, termination, written patient notice, and original-versus-copy records",
    "url": "https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-062",
    "set": 13,
    "area": 2,
    "kind": "single",
    "topic": "2025 Massachusetts vaccination policy: noncertified technician with 500 post-license hours",
    "topicKey": "immunization",
    "stem": "A Massachusetts community pharmacy plans to administer an indicated routine influenza vaccine to an eligible FIVE-year-old under a valid standing order. The supervising pharmacist is properly immunization-trained, has current CPR certification, will assess and counsel the patient, and will select the vaccine. All otherwise applicable documentation, VIS, storage, consent, and reporting rules are satisfied. Which proposed vaccinator is permitted by Board/DPH Policy 2023-02, revised September 4, 2025?",
    "choices": [
      {
        "text": "A licensed pharmacy technician trainee with 650 hours of trainee employment, the required immunization coursework, current CPR certification, and direct pharmacist supervision.",
        "why": "Policy 2023-02 explicitly prohibits pharmacy technician trainees (PTTs) from administering vaccines, regardless of training, experience, direct supervision, or the age of the patient."
      },
      {
        "text": "A Massachusetts-licensed but non-nationally-certified pharmacy technician with 400 hours worked after receiving the technician license, an ACPE-accredited six-hour training program, two documented hours of on-the-job training, and current CPR certification.",
        "why": "A pharmacy technician must be nationally certified OR have at least 500 hours worked after obtaining the technician license. This technician is not nationally certified and has only 400 qualifying post-license hours, so completing the other training does not cure the shortfall."
      },
      {
        "text": "A Massachusetts-licensed but non-nationally-certified pharmacy technician with 600 hours worked after licensure, the ACPE-accredited six-hour course including at least two hours of live hands-on training, two additional documented on-the-job training hours, current CPR, and the directly supervising pharmacist's approval.",
        "why": "Under Policy 2023-02 Section III(D), a licensed technician may qualify through national certification OR at least 500 post-license hours. The additional six-hour ACPE course (including two live hands-on hours), two documented on-the-job hours, CPR, pharmacist approval and direct supervision satisfy the described qualifications; the pharmacist, not the technician, performs assessment, counseling and vaccine selection."
      },
      {
        "text": "A fully trained licensed pharmacist may administer the indicated routine influenza vaccine to a FOUR-year-old under this pharmacy policy whenever the child's parent gives informed consent.",
        "why": "Policy 2023-02 Section II and 105 CMR 700.004(B)(6) establish a five-years-and-older age limit for pharmacy vaccine administration under this authority. Parental consent does not itself waive that minimum."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "Massachusetts Board/DPH Policy 2023-02, revised Sept. 4, 2025, §§I–III; 105 CMR 700.004(B)(6)",
    "url": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-063",
    "set": 13,
    "area": 2,
    "kind": "single",
    "topic": "iPLEDGE isotretinoin: REMS authorization, 30-day limit, no refills, and 7-day window",
    "topicKey": "rems",
    "stem": "A Massachusetts REMS-certified pharmacy receives a first-treatment isotretinoin prescription for a patient who can become pregnant. The prescriber is certified, the patient has completed both required pre-treatment pregnancy tests in medical settings, the latest negative test specimen was collected five days ago, and the iPLEDGE system currently confirms the patient is authorized for dispensing. The otherwise valid prescription specifies a 90-day supply with two authorized refills. Assume no other state-law or clinical concern. Which action BEST complies with the iPLEDGE REMS?",
    "choices": [
      {
        "text": "Ask the prescriber to issue or correct the order to a compliant prescription with no refills and no more than a 30-day supply; dispense only with REMS authorization, the Medication Guide, and within the patient's valid seven-day prescription window.",
        "why": "FDA-approved isotretinoin labeling requires certified-pharmacy authorization for each dispensing, a maximum 30-day supply, a Medication Guide and no refills. A patient who can become pregnant must obtain the medication within the seven-day prescription window tied to the pregnancy-test specimen collection. A corrected compliant order addresses the inappropriate 90-day quantity and refills."
      },
      {
        "text": "Dispense the first 30 days from the 90-day prescription and keep both authorized refills available for the next two months, provided the pharmacist rechecks iPLEDGE at each refill.",
        "why": "The iPLEDGE requirements explicitly prohibit dispensing refills. A subsequent treatment cycle needs its own appropriately authorized prescription; splitting a 90-day prescription into repeated refills does not make the order compliant."
      },
      {
        "text": "Dispense the full 90-day supply immediately because the two negative pretreatment tests and a current REMS authorization cover the entire initial treatment course.",
        "why": "Even with documented pretreatment testing and a positive authorization-to-dispense result, the maximum supply per dispensing is 30 days. A REMS authorization does not override that per-fill limit or allow the two refills."
      },
      {
        "text": "Hold the prescription until at least 30 days after the most recent pregnancy-test collection because the REMS prohibits dispensing within the first week after a negative test.",
        "why": "For a patient who can become pregnant, the REMS provides a seven-day dispensing window linked to pregnancy-test collection, not a mandatory 30-day waiting period after the latest negative test. Waiting would risk missing the valid window; the pharmacy should obtain a corrected, compliant prescription and proceed if authorization remains valid."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "FDA iPLEDGE REMS revised requirements IMPLEMENTED Nov. 15, 2026; FDA iPLEDGE REMS official update and Q&A, first-course pregnancy tests in medical setting, seven-day window, 30-day dispensing and no refills; FDA current isotretinoin label §5.2",
    "url": "https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/ipledge-risk-evaluation-and-mitigation-strategy-rems",
    "verified": "2026-11-17",
    "note": "The FDA implemented changes on Nov. 15, 2026. PRETREATMENT pregnancy tests still require a medical setting; selected MONTHLY tests during/after treatment may be at home if prescriber permits; missed 7-day window no longer imposes old extra waiting period. The patient in this question is a FIRST-treatment patient within the 7-day window; 30-day maximum and no refill remain correct."
  },
  {
    "id": "E30-064",
    "set": 13,
    "area": 3,
    "kind": "multi",
    "topic": "LTCF Schedule II partial fills: federal 60-day option versus Massachusetts 30-day prescription validity",
    "topicKey": "cii-partial-fills",
    "stem": "A Massachusetts retail pharmacy receives an otherwise valid WRITTEN Schedule II prescription for 30 morphine tablets for a documented resident of a long-term care facility (LTCF). The prescription was issued October 1, 2026. The pharmacist made properly documented unit-dose partial dispensings on October 3 and October 20; the remaining authorized balance has not been dispensed and treatment has not been discontinued. On November 4, the LTCF asks for another partial dispensing under the ORIGINAL prescription. There is no stock shortage, patient-requested partial-fill pathway, or other special exception. Under federal law AND Massachusetts law, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The federal LTCF provision permits Schedule II prescriptions to be dispensed in partial quantities, including individual dosage units, if the pharmacist notes LTCF status and meets the applicable recordkeeping requirements.",
        "why": "21 CFR 1306.13(c) permits unit-dose partial fillings for LTCF patients and requires the prescription to be designated 'LTCF patient.' It is a separate mechanism from the 72-hour shortage or patient-requested 30-day partial-fill pathways."
      },
      {
        "text": "The November 4 installment is permitted because federal law allows LTCF Schedule II prescriptions to remain valid up to 60 days and therefore overrides Massachusetts' 30-day expiration rule.",
        "why": "The federal 60-day period is a maximum permission, not preemption of a more restrictive state law. Massachusetts M.G.L. c.94C §23(a) invalidates written or electronic Schedule II prescriptions 30 days after issuance. November 4 is beyond 30 days after October 1; the original prescription cannot be used for that installment."
      },
      {
        "text": "For each authorized partial dispensing, the pharmacist must record the date, quantity dispensed, remaining authorized quantity, and dispenser identity; the sum of the installments may not exceed the prescribed amount.",
        "why": "21 CFR 1306.13(c) requires a readily retrievable partial-fill record with date, quantity, remaining quantity and pharmacist identification; all partial quantities together must stay at or below the original total prescribed."
      },
      {
        "text": "Despite the federal LTCF provision's maximum 60-day validity, Massachusetts' 30-day expiration rule prevents a further partial dispensing on November 4 under this October 1 written prescription.",
        "why": "Massachusetts M.G.L. c.94C §23(a) imposes a 30-day expiration on written or electronic Schedule II prescriptions. A federal regulation allowing up to 60 days for LTCF partial filling does not eliminate the stricter Massachusetts expiration; a new lawful prescription is needed for further dispensing after it becomes invalid."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "21 CFR 1306.13(c)–(d) LTCF/terminal-illness partial fills; M.G.L. c.94C §23(a) 30-day Massachusetts Schedule II expiration",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-065",
    "set": 13,
    "area": 4,
    "kind": "single",
    "topic": "Pharmacy change of ownership: new license versus MOR continuity and 14/45-day deadlines",
    "topicKey": "pharmacy-operations",
    "stem": "An operating Massachusetts retail pharmacy is being purchased by a different parent company, and the pharmacy's federal employer identification number (FEIN) will change. The location, pharmacy name, and Massachusetts-licensed Manager of Record will remain unchanged. The parties plan to transfer ownership in six weeks and can prepare the controlled-substance inventory, an official bill of sale, and all other required records. No waiver applies. Which approach BEST meets 247 CMR 6.11 and the Board's July 2026 Pharmacy Application Checklist?",
    "choices": [
      {
        "text": "Continue dispensing under the current pharmacy license after the sale because retaining the pharmacy address and Manager of Record means the Board regards the change only as an administrative update.",
        "why": "The Board's July 2026 checklist treats changes to direct or parent-company ownership or to the FEIN as ownership changes requiring closure of the current pharmacy license and a new application. The same location, name, and MOR do not make the old license transferable to the new owner."
      },
      {
        "text": "Have the outgoing licensee notify the Board at least 14 days before the proposed transfer and address the required closure and controlled-substance transfer steps; the incoming owner must apply for a new pharmacy license at least 14 days in advance, with approval before operating under the new ownership.",
        "why": "247 CMR 6.11 requires advance notification by the outgoing licensee and a new application by the proposed new licensee at least 14 days before ownership transfer, supported by controlled-substance transfer/inventory documentation and bill of sale. The Board's July 2026 checklist clarifies that the old license closes and recommends filing at least 45 days early for review, but 45 days is not the minimum mandated by §6.11."
      },
      {
        "text": "Submit an application for a change of Manager of Record at least 45 days before the sale; a new pharmacy license is unnecessary because the pharmacy name and dispensing staff will stay the same.",
        "why": "Changing the manager is not the same as transferring the pharmacy license to a new owner. The question states that the MOR remains unchanged; ownership/FEIN changes instead trigger the new-license process under §6.11 and the Board checklist."
      },
      {
        "text": "Transfer ownership first and have the buyer apply for a new pharmacy license within 14 calendar days afterward, while continuing to use the seller's license during application processing.",
        "why": "Section 6.11 calls for the proposed new licensee's application at least 14 days BEFORE ownership transfer, not after. The incoming owner does not gain authority to operate under the seller's former license merely because an application is pending."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 6.11(1)–(3); Massachusetts Board Pharmacy Application Checklist (revised July 15, 2026), Ownership Changes",
    "url": "https://www.mass.gov/doc/pharmacy-application-checklist/download",
    "verified": "2026-11-15"
  },
  {
    "id": "E30-066",
    "set": 14,
    "area": 1,
    "kind": "single",
    "topic": "Schedule II handling: ordinary versus certified technicians and the hydrocodone-ER prohibition",
    "topicKey": "technician-scope",
    "stem": "A Massachusetts community pharmacy is preparing valid Schedule II prescriptions. The on-duty pharmacist directly supervises a licensed pharmacy technician and a licensed certified pharmacy technician, has approved permitted Schedule II handling under written pharmacy policies, and will personally complete final dispensing validation. The pharmacy has immediate-release oxycodone tablets and a hydrocodone-only extended-release product that is NOT abuse-deterrent. Which staff assignment is permissible?",
    "choices": [
      {
        "text": "Assign the licensed, noncertified pharmacy technician to COUNT the oxycodone tablets, because a technician may assist with transporting Schedule II stock.",
        "why": "Incorrect. Under 247 CMR 8.05(2), a licensed pharmacy technician may assist in TRANSPORTING Schedule II controlled substances under supervision and approved written procedures; that permission does not extend to handling or counting the stock. Counting is not merely transport."
      },
      {
        "text": "Assign the licensed certified pharmacy technician to COUNT the oxycodone tablets under the pharmacist's supervision and documented approval.",
        "why": "Correct. 247 CMR 8.05(2)(b) permits a licensed certified pharmacy technician to assist in transporting AND HANDLING Schedule II controlled substances under pharmacist supervision when the pharmacist has approved the role as reflected in the pharmacy's written policies. The pharmacist remains accountable and performs final validation."
      },
      {
        "text": "Assign the licensed certified pharmacy technician to COUNT the non-abuse-deterrent hydrocodone-only extended-release product because certification removes all Schedule II handling exclusions.",
        "why": "Incorrect. 247 CMR 8.05(3) specifically prohibits certified pharmacy technicians, pharmacy technicians, and technician trainees from handling hydrocodone-only extended-release medication that is not abuse-deterrent. Certification does not override that product-specific exception."
      },
      {
        "text": "Assign the licensed pharmacy technician to perform the FINAL patient dispensing validation of the oxycodone after the computer's barcode verification.",
        "why": "Incorrect. 247 CMR 8.02(6)(d) prohibits pharmacy technicians from performing final dispensing-process validation. Computer checks or later pharmacist review do not transfer that professional task to a technician."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 8.02(6)(d); 247 CMR 8.05(1)–(3) (technician Schedule II handling and product-specific exclusion)",
    "url": "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-067",
    "set": 14,
    "area": 2,
    "kind": "multi",
    "topic": "CQI annual education, written on-site program, and off-site quality-event records",
    "topicKey": "quality-safety",
    "stem": "A Massachusetts community pharmacy has confirmed several quality-related events (QREs). The pharmacist has already addressed immediate patient needs and made each required initial event report on time. A corporate quality team offers centralized electronic storage of QRE records, while the pharmacy's Manager of Record revises the local continuous quality improvement (CQI) program. Under 247 CMR 15.02–15.04, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy must keep a written description of its CQI program ON THE PREMISES and make that description readily available to pharmacy personnel.",
        "why": "Correct. 247 CMR 15.04(1) requires the written CQI program description to be maintained on the pharmacy premises and readily available to pharmacy personnel. This differs from the location allowed for individual QRE records."
      },
      {
        "text": "QRE records may be maintained off-site if they are kept in an orderly manner, filed by date, and retained for at least TWO YEARS from the QRE REPORT date.",
        "why": "Correct. 247 CMR 15.04(2)–(4) sets a minimum two-year period from the date of the QRE report, requires orderly date filing, and expressly permits off-site storage. The on-premises program DESCRIPTION requirement does not require every event record to be on-site."
      },
      {
        "text": "Once all personnel finish onboarding, annual CQI education may be discontinued if no QRE caused documented patient injury that year.",
        "why": "Incorrect. 247 CMR 15.02(1)(f) requires ongoing CQI education for pharmacy personnel at least annually. The duty does not depend on whether any patient was harmed or how many events occurred."
      },
      {
        "text": "The CQI process must analyze system and workflow contributors and inform pharmacy personnel about policy or process changes resulting from CQI recommendations.",
        "why": "Correct. 247 CMR 15.02(1)(d)–(e) requires cause analysis and improvements; 247 CMR 15.03(3)(a)–(b) requires consideration of systemic factors and communicating resulting changes to personnel."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "247 CMR 15.02(1)(d)–(f); 15.03(3); 15.04(1)–(4)",
    "url": "https://www.mass.gov/regulations/247-CMR-1500-continuous-quality-improvement-program",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-068",
    "set": 14,
    "area": 2,
    "kind": "single",
    "topic": "2026 Part 2 public-health disclosure: de-identified records versus identifiable patient data",
    "topicKey": "privacy-part2",
    "stem": "A federally assisted Massachusetts substance-use-disorder treatment program with an on-site pharmacy is subject to 42 CFR Part 2. The local public-health authority requests data to plan overdose-prevention services. The program can provide either (1) patient records fully de-identified under the HIPAA standard, with no reasonable basis to identify a patient, or (2) a named list linking patients to SUD diagnoses and prescriptions. No affected patient has consented; no Part 2 court order or other disclosure exception applies. Under the Part 2 rules applicable in November 2026, which approach is permissible?",
    "choices": [
      {
        "text": "Release both datasets, because HIPAA's public-health disclosure permission automatically overrides the stricter Part 2 protections.",
        "why": "Incorrect. HIPAA's general public-health disclosure permissions do not automatically authorize a Part 2 program to release identifiable Part 2 records. Part 2's specific limits still apply."
      },
      {
        "text": "Release the named list only if the recipient promises confidentiality; the de-identified dataset still requires each patient's consent.",
        "why": "Incorrect. The public-health authority's confidentiality promise is not itself Part 2 consent or another lawful exception. Conversely, 42 CFR 2.54 expressly permits qualifying de-identified disclosure without patient consent."
      },
      {
        "text": "Release the properly de-identified records to the public-health authority without patient consent, but do not release the named list solely under the Part 2 public-health exception.",
        "why": "Correct. 42 CFR 2.54 permits disclosure to a defined public-health authority WITHOUT consent only where record content meets 45 CFR 164.514(b)'s de-identification standard and there is no reasonable basis to identify any patient. Identifiable SUD records require some other valid authorization or exception, none of which is present here."
      },
      {
        "text": "Withhold both datasets, because Part 2 always requires written patient consent even when information is properly de-identified for a public-health authority.",
        "why": "Incorrect. This ignores the express exception in 42 CFR 2.54, added by the 2024 rule with required compliance as of February 16, 2026, for records de-identified to the HIPAA standard."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "42 CFR 2.54(a)–(b); 45 CFR 164.514(b); HHS 2024 Part 2 Final Rule (compliance February 16, 2026)",
    "url": "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2/section-2.54",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-069",
    "set": 14,
    "area": 3,
    "kind": "multi",
    "topic": "Schedule II/III consumer pamphlet: ordinary pain, LTCF, and OUD exceptions",
    "topicKey": "label-packaging",
    "stem": "A Massachusetts RETAIL pharmacy dispenses four separate, otherwise lawful prescriptions. All required prescription labeling, counseling, and clinical checks have been completed. Under M.G.L. c.94C §21, for which dispensings is the pharmacy REQUIRED to give the consumer pamphlet addressing narcotic risks and non-opioid pain-treatment alternatives? SELECT ALL THAT APPLY. Assume no exception other than those stated.",
    "choices": [
      {
        "text": "Schedule II oxycodone for routine postoperative pain in a community-dwelling adult who is not receiving outpatient palliative care.",
        "why": "Correct. Section 21 requires the pamphlet when a retail pharmacy dispenses a Schedule II or III narcotic or controlled substance, absent a listed exception. Routine outpatient postoperative pain does not qualify for the palliative-care, LTCF, or SUD-treatment exceptions."
      },
      {
        "text": "Schedule II oxycodone prescribed to a patient who is a resident of a long-term care facility.",
        "why": "Incorrect as a REQUIRED-pamphlet choice. Section 21 expressly says pharmacists are not required to distribute the pamphlet when the patient resides in a long-term care facility. Optional provision is different from a legal requirement."
      },
      {
        "text": "Schedule III transdermal buprenorphine prescribed for CHRONIC PAIN, not for opioid use disorder or opioid dependence, to a community-dwelling adult.",
        "why": "Correct. The Schedule III controlled-substance pamphlet rule applies and the special exception for medication prescribed to treat SUD or opioid dependence does NOT apply when buprenorphine is prescribed for chronic pain. Drug name alone does not establish the exception."
      },
      {
        "text": "Schedule III buprenorphine/naloxone prescribed specifically for treatment of opioid use disorder to a community-dwelling adult.",
        "why": "Incorrect as a REQUIRED-pamphlet choice. M.G.L. c.94C §21 expressly removes the distribution requirement when the controlled substance is prescribed for treatment of SUD or opioid dependence. The indication, not simply the Schedule, determines this exception."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "M.G.L. c.94C §21, third paragraph (Schedule II/III consumer pamphlet and palliative-care, LTCF, OUD exceptions)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-070",
    "set": 14,
    "area": 4,
    "kind": "single",
    "topic": "Interchangeable biologic substitution: permissive authority, dual notice, and records",
    "topicKey": "interchange",
    "stem": "A Massachusetts retail pharmacy receives a valid prescription for a biological medication identified by its BRAND name. The prescriber has not given a patient-specific written 'no substitution' instruction. The proposed alternative is FDA-designated INTERCHANGEABLE with the prescribed reference biologic, and the pharmacist judges substitution appropriate. The pharmacy cannot enter a note in the prescriber's interoperable EHR, but it maintains a patient record accessible to the prescriber upon request. Which procedure BEST complies with M.G.L. c.112 §12EE?",
    "choices": [
      {
        "text": "Substitution is mandatory whenever the interchangeable biologic costs less, and no patient or prescriber notice is necessary if the original prescription remains in the file.",
        "why": "Incorrect. Section 12EE(b) says a pharmacist MAY substitute an interchangeable biologic, not that every eligible substitution is mandatory. Sections 12EE(d)–(f) also impose notification and recordkeeping duties after substitution."
      },
      {
        "text": "The pharmacist must obtain a new, individually signed prescriber authorization before every substitution because the pharmacy cannot enter data directly into the prescriber's interoperable EHR.",
        "why": "Incorrect. When no patient-specific written prohibition applies, §12EE(b) permits substitution; §12EE(d) provides alternative prescriber notification methods when the pharmacy cannot annotate an interoperable EHR. Prior affirmative authorization is not universally required by this section."
      },
      {
        "text": "The pharmacist may substitute and give only a verbal notice to the patient, provided that the pharmacy destroys the interchange record after the next refill is completed.",
        "why": "Incorrect. Section 12EE(e) requires WRITTEN patient notification, and §12EE(f) requires a substitution record retained for at least one year from the last entry in the profile record. Verbal notice alone and early destruction do not meet those obligations."
      },
      {
        "text": "The pharmacist may substitute, notify the prescriber within a reasonable time through the accessible pharmacy-record route, notify the patient in writing, and retain the substitution record for at least one year from the last profile entry.",
        "why": "Correct. Under §12EE(b)–(f), FDA interchangeability and absence of a patient-specific written no-substitution instruction permit the switch. Where an interoperable-EHR notation is not possible, a pharmacy-record notation accessible by the prescriber on request is a permitted notice method; the patient receives written notice, and records are retained at least one year from the last profile entry."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.112 §12EE(b)–(f) (interchangeable biologics, prescriber/patient notices, minimum retention)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12EE",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-071",
    "set": 15,
    "area": 1,
    "kind": "single",
    "topic": "Late-year license transfer: October 1 CE grace period versus permanent exemption",
    "topicKey": "licensure-ce",
    "stem": "Two pharmacists who graduated from ACPE-accredited PharmD programs in 2019 receive their FIRST Massachusetts pharmacist licenses by license transfer in 2026. Pharmacist X is licensed on September 30; Pharmacist Y is licensed on October 1. Neither performs immunization, compounding, or CDTM duties, and neither qualifies for another waiver. Both are reviewing their 2026 continuing education obligations before the December 2026 renewal. Under Massachusetts Board Policy 2021-04, as revised September 4, 2025, which statement is MOST accurate?",
    "choices": [
      {
        "text": "Both pharmacists have until April 30, 2027 to complete their 2026 CE because their first Massachusetts licenses were issued in the final four months of 2026.",
        "why": "Incorrect. Board Policy 2021-04, §II sets a specific cutoff of ON OR AFTER OCTOBER 1 for initial licensure through exam or transfer. September 30 does not satisfy that cutoff, even though it is late in the calendar year."
      },
      {
        "text": "Neither pharmacist qualifies for a grace period because 247 CMR 4.03 imposes the standard annual CE requirement regardless of the date of first Massachusetts licensure.",
        "why": "Incorrect. Although 247 CMR 4.03 sets the general annual CE requirement, Board Policy 2021-04, §II specifically grants qualifying late-year examination and transfer licensees a grace period through April 30 of the following year."
      },
      {
        "text": "Only Pharmacist Y qualifies for a grace period through April 30, 2027 to obtain the required 2026 CE; it is not a permanent exemption and does not eliminate the separate 2027 CE requirement.",
        "why": "Correct. Board Policy 2021-04, §II covers licenses obtained by examination or transfer on or after October 1. Y qualifies on October 1; X does not on September 30. Both graduated in 2019, so the separate graduation-year exception in 247 CMR 4.03(8) does not apply. Annual CE obligations remain separate."
      },
      {
        "text": "Pharmacist Y is exempt from all 2026 CE because receiving a license on October 1 is equivalent to graduating from an accredited pharmacy school in that calendar year.",
        "why": "Incorrect. The graduation-year CE exemption in 247 CMR 4.03(8) depends on the actual year of graduation, here 2019. A late-year license TRANSFER creates a deadline extension under Board policy, not a graduation-year exemption."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 4.03(4),(5),(8); Massachusetts Board Policy 2021-04 §II (revised Sept. 4, 2025)",
    "url": "https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-072",
    "set": 15,
    "area": 2,
    "kind": "single",
    "topic": "Chlamydia EPT stock-out referral and disease-specific scope",
    "topicKey": "expedited-partner-therapy",
    "stem": "At a Massachusetts retail pharmacy, a patient being treated for laboratory-confirmed chlamydia presents a separate, otherwise valid prescription for the patient's unexamined partner. The partner prescription properly identifies the recipient as 'EPT' rather than by name. The pharmacy cannot obtain the prescribed medication in time to dispense it. Later, another patient asks the pharmacist to process a similar EPT prescription for a partner exposed ONLY to gonorrhea, relying solely on Massachusetts Board/DCP Policy 2020-08. No other independent prescribing or dispensing authorization has been established. Which response BEST follows that policy?",
    "choices": [
      {
        "text": "Keep the unfilled chlamydia EPT prescription without referring the patient elsewhere, because stock shortages relieve pharmacists of all EPT-related responsibilities.",
        "why": "Incorrect. Joint Board/DCP Policy 2020-08, §II requires a pharmacist who is unable or unwilling to fill a qualifying EPT prescription to REFER the patient to an alternate pharmacy. A stock-out is not an exception to that obligation."
      },
      {
        "text": "Process the gonorrhea-only EPT request under Policy 2020-08 because every sexually transmitted infection is covered whenever a partner cannot attend an appointment.",
        "why": "Incorrect. Policy 2020-08 expressly applies ONLY to chlamydia treatment. Its specific authority cannot be extended to gonorrhea merely because it is another STI; a separate applicable authority would have to be established."
      },
      {
        "text": "Require the chlamydia partner to undergo an examination and provide a legal name before giving a referral, because EPT prescriptions without a name are invalid.",
        "why": "Incorrect. Section I of Policy 2020-08 explicitly allows a separate chlamydia EPT prescription to substitute 'EPT', 'E.P.T.' or 'Expedited Partner Therapy' for the partner's name and address without an exam."
      },
      {
        "text": "Refer the patient with the unfilled CHLAMYDIA EPT prescription to another pharmacy, while recognizing that Policy 2020-08 alone does not authorize a GONORRHEA-only EPT prescription.",
        "why": "Correct. Under Board/DCP Policy 2020-08, §II(2), an unable or unwilling pharmacist must refer the patient to an alternate pharmacy. The policy states that it applies only to chlamydia; the gonorrhea request requires its own independent legal basis rather than an assumed extension."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "Massachusetts Board/Drug Control Program Joint Policy 2020-08 §§I–II (Expedited Partner Therapy Prescriptions; May 25, 2023)",
    "url": "https://www.mass.gov/policy-statement/expedited-partner-therapy-prescriptions",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-073",
    "set": 15,
    "area": 2,
    "kind": "multi",
    "topic": "HIPAA breach triage: encryption, compromised keys and risk assessment",
    "topicKey": "hipaa-breach",
    "stem": "A HIPAA-covered Massachusetts retail pharmacy examines four separate possible privacy incidents. Consider ONLY the federal HIPAA Breach Notification Rule; there is no applicable law-enforcement delay, and no exception beyond the facts stated should be assumed. Which conclusions are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A hard drive containing ePHI encrypted in accordance with HHS guidance is stolen, but the separate decryption key is not compromised; theft of that drive alone does not trigger federal breach notification.",
        "why": "Correct. 45 CFR 164.402 defines unsecured PHI, and HHS encryption guidance recognizes qualifying encrypted ePHI with uncompromised decryption keys as secured. The federal breach-notification obligation does not arise solely because such secured data were stolen."
      },
      {
        "text": "An unencrypted USB drive with identifiable prescription records is stolen; no one can prove the thief opened the files, so the pharmacy can automatically close the incident without risk assessment or notification.",
        "why": "Incorrect. An impermissible disclosure or acquisition of unsecured PHI is presumed a breach unless an exception applies or a documented assessment shows low probability of compromise. Lack of proof of actual viewing is relevant but is not automatically conclusive."
      },
      {
        "text": "For an impermissible disclosure of unsecured PHI, a documented four-factor assessment supporting a low probability of compromise can rebut the presumption of breach and make federal notification unnecessary.",
        "why": "Correct. Under 45 CFR 164.402, the assessment considers the nature and extent of PHI, the recipient, actual acquisition/viewing, and mitigation. A supportable low-probability finding may mean notification is not required; without it, the breach presumption applies."
      },
      {
        "text": "If an appropriately encrypted laptop and its accessible decryption key are stolen together, the original encryption always guarantees the HIPAA notification safe harbor without further analysis.",
        "why": "Incorrect. Under HHS guidance, a confidential key or decryption process enabling access must not have been breached. When the key is stolen with the device, encryption does not automatically establish the safe harbor; further assessment is needed."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "45 CFR 164.402; HHS HIPAA Breach Notification Rule, Definitions and Guidance to Render PHI Unusable, Unreadable, or Indecipherable",
    "url": "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-074",
    "set": 15,
    "area": 3,
    "kind": "multi",
    "topic": "New prescription corrections: earliest-fill dates, DEA number and PMP-sensitive Schedule VI days' supply",
    "topicKey": "rx-amendments",
    "stem": "A Massachusetts pharmacist evaluates FOUR separate, otherwise authorized NEW prescriptions before initial dispensing. Assume any added identifier is verified, the authorized overall quantity remains unchanged, all modifications are documented, and there are no separate clinical safety concerns. Under Massachusetts Board/DCP Policy 2018-01, revised January 11, 2024, which actions are permitted as stated? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "After consulting the prescriber by telephone, change the 'earliest date to be filled' on a Schedule II prescription instead of requiring a new prescription.",
        "why": "Incorrect. Policy 2018-01, §II(E) lists a Schedule II EARLIEST FILL DATE among elements that may never be changed or added. Prescriber consultation does not cure the restriction; a new prescription is required."
      },
      {
        "text": "Verify and add a missing prescriber's DEA registration number to a Schedule II prescription WITHOUT contacting the prescriber, recording the modification.",
        "why": "Correct. Policy 2018-01, §III(A)(i)(d) permits adding the DEA number without consultation. Section IV requires recording the date, the change and the pharmacist, while the prescription must remain otherwise valid."
      },
      {
        "text": "Convert a PMP-reportable Massachusetts Schedule VI gabapentin prescription from a 30-day supply with 11 refills to a 90-day supply with three refills WITHOUT consulting the prescriber because it is Schedule VI.",
        "why": "Incorrect. Policy 2018-01, §III(C)(iii)(a) only permits independent days'-supply conversion for Schedule VI drugs NOT subject to PMP reporting. Gabapentin is a Massachusetts PMP additional drug, so the premise does not meet the exception."
      },
      {
        "text": "For a non-PMP-reportable Schedule VI amlodipine prescription, use professional judgment to convert a 30-day supply with 11 refills into a 90-day supply with three refills WITHOUT prescriber consultation, preserving the overall amount and documenting the change.",
        "why": "Correct. Policy 2018-01, §III(C)(iii) explicitly recognizes this conversion for non-PMP-reportable Schedule VI drugs where professionally appropriate. Section IV requires documentation. The case rules out separate clinical concerns."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "MA Board/DCP Policy 2018-01 §§II(E), III(A)(i)(d), III(C)(iii)(a), IV (revised Jan. 11, 2024)",
    "url": "https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-075",
    "set": 15,
    "area": 4,
    "kind": "single",
    "topic": "2026 FDA DSCSA small dispenser exemption: corporate employee count and residual duties",
    "topicKey": "dscsa",
    "stem": "A corporate entity owns THREE Massachusetts retail pharmacies. As of November 27, 2026, across the ENTIRE company it has 16 full-time licensed pharmacists, nine full-time qualified pharmacy technicians, and 20 full-time cashiers who are not pharmacists or pharmacy technicians. On December 1, 2026, one location identifies a SUSPECT prescription-drug package while management is implementing FDA's August 6, 2026 DSCSA exemption. No other waiver or exemption applies. Which interpretation is MOST accurate?",
    "choices": [
      {
        "text": "The company qualifies for the specified small-dispenser exemptions until November 27, 2027 because it has 25 qualifying full-time pharmacists/technicians across the corporation; suspect-product quarantine, investigation and other non-exempt DSCSA requirements remain.",
        "why": "Correct. FDA's August 6, 2026 notice counts full-time LICENSED PHARMACISTS and QUALIFIED PHARMACY TECHNICIANS across the corporate entity as of November 27, 2026. Sixteen plus nine equals 25; cashiers do not count under this exemption definition. The specified enhanced tracing and product-identifier verification exemptions do not waive other section 582 obligations."
      },
      {
        "text": "The company is ineligible because FDA counts all 45 full-time employees, including cashiers, toward the 25-person exemption threshold.",
        "why": "Incorrect. FDA's August 2026 notice expressly limits the qualifying employee count to licensed pharmacists and qualified pharmacy technicians across the owning company. Non-pharmacy cashiers are excluded from that count."
      },
      {
        "text": "The company qualifies, but the pharmacies must obtain individual FDA approval of a special exemption application before using their existing transaction-information methods.",
        "why": "Incorrect. The FDA's August 2026 notice announces a class-wide exemption; small dispensers and their trading partners utilizing it do NOT have to submit extra information to FDA or await individual approval."
      },
      {
        "text": "Each store is counted separately regardless of corporate ownership, and the exemption suspends all suspect-product investigation and quarantine obligations for stores under the threshold.",
        "why": "Incorrect. The notice uses corporate-entity-wide counting, not store-by-store headcounts. It also retains non-exempt section 582 requirements; suspect-product quarantine and investigation obligations are not automatically erased."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "FDA DSCSA Exemptions for Small Business Dispensers (Aug. 6, 2026), FD&C Act §§582(a)(3), 582(d)(4), 582(g)(1), effective Nov. 27, 2026–Nov. 27, 2027",
    "url": "https://www.fda.gov/media/194424/download",
    "verified": "2026-11-16"
  },
  {
    "id": "E30-076",
    "set": 16,
    "area": 1,
    "kind": "single",
    "topic": "PGY1 resident: intern licensure, technician supervision and pharmacist-only validation",
    "topicKey": "intern-education",
    "stem": "An ACPE-accredited PharmD graduate begins a PGY1 residency in a Massachusetts hospital. The resident has passed the NAPLEX and holds a current Massachusetts pharmacy intern license, but the Board has NOT issued a Massachusetts pharmacist license. A licensed pharmacist preceptor is on the premises, directly supervises the resident, and can complete final dispensing validation. A licensed pharmacy technician also needs supervision. Assume staffing ratios and all other duties are otherwise compliant. Which arrangement is permitted?",
    "choices": [
      {
        "text": "Allow the resident to serve as the only pharmacist on duty during a staff pharmacist's absence because passing the NAPLEX and entering an accredited residency temporarily confer pharmacist authority.",
        "why": "Incorrect. 247 CMR 8.01(8) requires a Massachusetts residency graduate to hold either a Massachusetts pharmacist license or a Massachusetts intern license with pharmacist supervision. NAPLEX success and residency status alone do not provide pharmacist licensure or permit the resident to replace the pharmacist on duty."
      },
      {
        "text": "Allow the resident to work under direct supervision as a licensed pharmacy intern and supervise the technician in that supervised role, while the licensed pharmacist retains responsibility for final dispensing validation.",
        "why": "Correct. Under 247 CMR 8.01(8) and (10), an approved PharmD graduate may work as a licensed pharmacy intern during residency until pharmacist licensure. Section 8.01(15) allows an intern acting under direct supervision of a registered pharmacist preceptor to supervise technicians. Section 9.04(1) reserves final dispensing validation to a licensed pharmacist."
      },
      {
        "text": "Have the resident independently perform the final validation of prescriptions because a pharmacist's on-site availability automatically converts an intern's validation into licensed pharmacist validation.",
        "why": "Incorrect. The resident remains an intern until licensed as a pharmacist. Although the intern may perform supervised functions, 247 CMR 9.04(1) makes a licensed pharmacist responsible for final dispensing-process validation. On-site supervision does not change the resident's license category."
      },
      {
        "text": "Require the resident to stop all pharmacy-intern activities immediately upon graduation, even though the Massachusetts intern license remains active, until the pharmacist license is issued.",
        "why": "Incorrect. 247 CMR 8.01(10) expressly allows graduates of an approved pharmacy school to continue acting as pharmacy interns until licensed as pharmacists, and 8.01(8) specifically addresses the supervised intern pathway during Massachusetts residencies."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 8.01(8), (10), (15); 247 CMR 9.04(1)",
    "url": "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians",
    "verified": "2026-11-16",
    "note": "MPJE trap: PharmD graduation, passing NAPLEX and starting residency do not by themselves confer Massachusetts pharmacist authority. A licensed intern may supervise technicians only in the permitted supervised arrangement."
  },
  {
    "id": "E30-077",
    "set": 16,
    "area": 2,
    "kind": "multi",
    "topic": "VAERS: mandatory adverse-event reports versus encouraged vaccination-error reporting",
    "topicKey": "immunization",
    "stem": "A Massachusetts retail pharmacy administers routinely recommended, FDA-licensed, NON-COVID, NON-MPOX adult vaccines under appropriate standing orders. Later, the pharmacy learns of four separate events: (1) an event identified in the manufacturer's labeling as a contraindication to later doses; (2) an event in the VAERS Table of Reportable Events Following Vaccination occurring within the specified interval for the vaccine; (3) transient injection-site soreness that is neither in the table nor a labeled contraindication; and (4) a vaccine-administration error with no adverse event. Consider the general federal National Childhood Vaccine Injury Act (NCVIA)/VAERS rules, with no additional vaccine-program reporting condition. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The event the manufacturer lists as a contraindication to subsequent doses must be reported to VAERS by the healthcare provider.",
        "why": "Correct. The NCVIA and VAERS healthcare-provider guidance require a provider to report an adverse event listed by the vaccine manufacturer as a contraindication to further doses. This duty is not erased merely because the clinician has not proved vaccine causation."
      },
      {
        "text": "Transient injection-site soreness that is neither in the applicable reportable-events table nor a labeled contraindication must automatically be reported under the NCVIA's mandatory provider categories.",
        "why": "Incorrect. Ordinary mild soreness that does not meet a Table of Reportable Events criterion or a manufacturer-listed contraindication is not automatically mandatory under those two federal NCVIA reporting categories. VAERS can accept voluntary reports, and clinically significant events are encouraged for reporting."
      },
      {
        "text": "A VAERS-table event occurring within its specified postvaccination time interval is federally reportable even when a causal relationship has not been conclusively established.",
        "why": "Correct. The NCVIA/VAERS provider reporting requirement uses the listed event and specified interval, not a requirement to prove causation. VAERS is a safety-monitoring system rather than a determination that a vaccine caused each event."
      },
      {
        "text": "The administration error with no associated adverse event may be reported to VAERS and is encouraged, but an error alone does not automatically meet the two general NCVIA mandatory adverse-event categories under the stated assumptions.",
        "why": "Correct. VAERS explicitly accepts vaccination-error reports and encourages reporting errors. For the ordinary licensed vaccines and facts stated, the two general NCVIA mandatory categories concern specified adverse events and labeled contraindications, not every error by itself; particular programs or emergency authorizations may impose additional duties."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "42 U.S.C. §300aa-25(b); VAERS Healthcare Provider Guidance and FAQs; Massachusetts DPH Vaccine Administration and Clinical Guidance (reporting recommendations)",
    "url": "https://vaers.hhs.gov/resources/infoproviders.html",
    "verified": "2026-11-16",
    "note": "MPJE trap: distinguish REQUIRED VAERS reports (specified table events or label contraindications) from ENCOURAGED reports of other significant events and vaccination errors. Special vaccines and programs can impose additional reporting requirements."
  },
  {
    "id": "E30-078",
    "set": 16,
    "area": 2,
    "kind": "single",
    "topic": "42 CFR Part 2: limited disclosure in a bona fide medical emergency and immediate documentation",
    "topicKey": "privacy-part2",
    "stem": "An unconscious patient arrives at a Massachusetts emergency department following a suspected overdose. The treating emergency physician contacts a federally assisted substance-use-disorder (SUD) treatment program subject to 42 CFR Part 2 to learn the patient's most recent medication dose before providing emergency treatment. No patient consent is on file, and prior written consent cannot be obtained while the patient is unconscious. The physician reasonably needs this information now to prevent a dangerous dosing error. No other disclosure authority is asserted. Which response BEST complies with 42 CFR 2.51?",
    "choices": [
      {
        "text": "Withhold all identifying SUD treatment information until the patient can sign a consent, because Part 2 has no exception for medical emergencies.",
        "why": "Incorrect. Section 2.51(a)(1) permits disclosure to medical personnel to the extent necessary for a bona fide medical emergency when prior written consent cannot be obtained. It does not categorically require waiting for the patient to regain consciousness."
      },
      {
        "text": "Provide the patient's entire SUD treatment file to the emergency department's administrative and billing staff because HIPAA treatment/payment/operations permissions automatically override Part 2.",
        "why": "Incorrect. The specific 42 CFR 2.51 emergency exception permits necessary disclosure to medical personnel. It does not authorize release of an entire record to administrative staff merely because the emergency department may otherwise be a HIPAA-covered entity."
      },
      {
        "text": "Provide the necessary dosing details to the treating physician, but document only that an emergency occurred when the program next performs its routine quarterly privacy audit.",
        "why": "Incorrect. Although limited disclosure to treating medical personnel can be permissible, 42 CFR 2.51(c) requires WRITTEN documentation immediately following disclosure, including recipient and facility affiliation, person disclosing, date/time, and nature of the emergency. A delayed generic audit entry is insufficient."
      },
      {
        "text": "Disclose only the medication information necessary to the treating emergency physician now, then immediately document the recipient and affiliation, person making disclosure, date/time, and nature of the emergency in the patient's record.",
        "why": "Correct. A bona fide emergency where prior written consent cannot be obtained meets 42 CFR 2.51(a)(1). The information may be disclosed only to medical personnel and only to the necessary extent. Section 2.51(c) requires specified written documentation in the patient's record immediately after disclosure."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "42 CFR 2.51(a)(1), (c) (medical emergency disclosures and immediate documentation; 2024 rule text, confirmed applicable in November 2026)",
    "url": "https://www.govinfo.gov/content/pkg/CFR-2024-title42-vol1/pdf/CFR-2024-title42-vol1-sec2-51.pdf",
    "verified": "2026-11-16",
    "note": "MPJE trap: Part 2 does allow limited disclosure in a bona fide medical emergency without prior written consent when that consent cannot be obtained. The written documentation must follow immediately—not at the next audit."
  },
  {
    "id": "E30-079",
    "set": 16,
    "area": 3,
    "kind": "single",
    "topic": "Schedule V: Massachusetts six-month expiration and five-refill maximum",
    "topicKey": "refills-transfers",
    "stem": "On November 16, 2026, a Massachusetts community pharmacist reviews FOUR independent prescriptions for substances correctly classified as Schedule V in Massachusetts. Each prescription was otherwise properly issued by an authorized practitioner, has a legitimate medical purpose, has appropriately recorded prior dispensings, and satisfies all other dispensing and identification requirements. No new authorization or exception is available. Under 247 CMR 9.04(13), which request MAY be dispensed under the ORIGINAL prescription?",
    "choices": [
      {
        "text": "A prescription issued May 20, 2026, first dispensed May 21, with FOUR subsequent refills already dispensed and FIVE refills originally authorized; the patient requests the FIFTH refill today.",
        "why": "Correct. November 16 is within six months of the May 20 issuance date, and the requested dispensing is refill number five (following the original fill and four earlier refills). 247 CMR 9.04(13) permits up to five Schedule V refills within the six-month validity period, assuming all other requirements are met."
      },
      {
        "text": "A prescription issued June 20, 2026, initially dispensed June 21, with FIVE refills already dispensed; the prescriber wrote '7 refills' and the patient requests a SIXTH refill today.",
        "why": "Incorrect. Even though the date is within six months, 247 CMR 9.04(13) expressly prohibits refilling a Schedule V prescription more than five times. An original prescription authorizing additional refills cannot override the Massachusetts limit."
      },
      {
        "text": "A prescription issued May 1, 2026, initially dispensed May 3, with only TWO refills used; the patient requests the THIRD refill today.",
        "why": "Incorrect. The November 16 request is more than six months after the May 1 issuance date. Under 247 CMR 9.04(13), unused authorized refills do not extend the Schedule V prescription's six-month expiration window."
      },
      {
        "text": "A prescription issued May 1, 2026, which has NEVER been filled and still has all its authorized refills available; the patient asks for the INITIAL fill today.",
        "why": "Incorrect. Section 9.04(13) prohibits BOTH an initial fill and a refill more than six months after Schedule V prescription issuance. Having zero earlier fills does not rescue an expired original."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 9.04(10), (13) (Schedule V fill/refill expiry and limit); comparison: federal 21 CFR 1306.22–1306.23",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "MPJE trap: Massachusetts applies its explicit six-month/five-refill rule to Schedule V, not only Schedules III and IV. Count from issuance, not the first dispensing date; initial fills also expire."
  },
  {
    "id": "E30-080",
    "set": 16,
    "area": 4,
    "kind": "multi",
    "topic": "Massachusetts Schedule II perpetual inventory: ten-day reconciliation, personnel and expired stock",
    "topicKey": "controlled-inventory",
    "stem": "A Massachusetts resident retail pharmacy maintains electronic Schedule II perpetual inventory records. Some expired Schedule II tablets remain physically secured on the pharmacy premises pending lawful reverse distribution. Its most recent physical reconciliation was TEN DAYS ago. Today the Manager of Record (MOR) is temporarily absent, a designated licensed pharmacist is present, and a licensed certified pharmacy technician and an unlicensed cashier are available. The pharmacy already performs the federal biennial inventory separately. Under 247 CMR 9.21(8) and (10), which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Because the pharmacy completes a federal biennial inventory, electronic Schedule II perpetual records need no separate physical reconciliation until the next federal biennial inventory.",
        "why": "Incorrect. Federal biennial inventories do not displace Massachusetts' separate 247 CMR 9.21(8)(c) rule requiring a physical reconciliation of EACH Schedule II perpetual inventory at least once every ten days."
      },
      {
        "text": "The pharmacy must perform an accurate physical count and reconcile each Schedule II perpetual record at least every ten days, including Schedule II stock that is expired, quarantined or awaiting reverse distribution.",
        "why": "Correct. Section 9.21(8)(c) requires reconciliation at least once every ten days using a physical count. Section 9.21(10) explicitly extends the security and inventory provisions to expired, quarantined and pending-reverse-distribution controlled stock; it is not excluded merely because it is unsaleable."
      },
      {
        "text": "The certified technician may make routine entries in the Schedule II perpetual ledger, but a discrepancy adjustment is reserved for the MOR or, during the MOR's absence, a pharmacist designee who reports the adjustment to the MOR.",
        "why": "Correct. 247 CMR 9.21(8)(f) allows a certified technician to make ledger entries, while (8)(d) restricts discrepancy-based inventory adjustments to the MOR or a pharmacist designee when the MOR is absent, with reporting to the MOR. Ordinary data entry is not the same as discrepancy adjustment."
      },
      {
        "text": "The unlicensed cashier may not enter data into or adjust the Schedule II perpetual inventory, even if a licensed pharmacist intends to review the entry afterward.",
        "why": "Correct. 247 CMR 9.21(8)(e) expressly prohibits an unlicensed individual from making ANY entry into, or adjustment of, the Schedule II perpetual inventory. A future pharmacist review does not create an exception."
      }
    ],
    "correct": [
      "B",
      "C",
      "D"
    ],
    "citation": "247 CMR 9.21(8)(a)–(f), 9.21(10); 21 CFR 1304.11(c) (separate federal biennial inventory)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "MPJE trap: do not confuse the federal biennial inventory with Massachusetts' every-ten-day Schedule II perpetual reconciliation. Certified technician data entry is allowed, but unlicensed entry and unauthorized discrepancy adjustments are not."
  },
  {
    "id": "E30-081",
    "set": 17,
    "area": 1,
    "kind": "single",
    "topic": "Technician refill authority: unchanged Schedule VI refills versus dose modification",
    "topicKey": "technician-scope",
    "stem": "A Massachusetts community pharmacy employs a Massachusetts-licensed pharmacy technician who is not nationally certified and a separately licensed certified pharmacy technician. The on-duty pharmacist has approved appropriate delegated work and will perform final dispensing validation. A prescriber's authorized agent agrees to add three refills to an existing Schedule VI lisinopril prescription with NO change in drug, strength, directions, or other prescription information. In a separate call, the agent proposes a dose increase on another patient's lisinopril prescription but describes it as 'just a refill.' Assume the communication method is otherwise legally permitted and all prescriptions are legitimate. Which division of responsibility BEST complies with 247 CMR 8.02 and 8.04?",
    "choices": [
      {
        "text": "The noncertified licensed technician may request an unchanged refill authorization but cannot receive it; only a certified technician may accept even an unchanged refill.",
        "why": "Incorrect. 247 CMR 8.02(6)(c) permits a licensed pharmacy technician, with the on-duty pharmacist's approval, to request AND accept authorizations for refills when no prescription information changes. National certification is not a prerequisite for this limited unchanged-refill activity."
      },
      {
        "text": "Either licensed technician may accept the dose increase as a refill authorization if the prescriber's agent agrees and the pharmacist validates the dispensed product afterward.",
        "why": "Incorrect. Changing the prescribed dose is therapy modification, not an unchanged refill. 247 CMR 8.02(6)(d) and 8.04(4)(e) prohibit pharmacy technicians, including certified technicians, from contacting prescribers concerning therapy modification. A later pharmacist final check does not grant authority for the prohibited communication."
      },
      {
        "text": "With the on-duty pharmacist's approval, the noncertified licensed technician may request and receive the unchanged refill authorization; the proposed dose modification must be referred to the pharmacist rather than handled independently by either technician.",
        "why": "Correct. Under 247 CMR 8.02(6)(c), an ordinary licensed technician can request and accept a refill authorization if nothing has changed and the pharmacist approves. Section 8.02(6)(d) and 8.04(4)(e) reserve therapy clarification or modification to the pharmacist, regardless of whether a technician holds national certification."
      },
      {
        "text": "The certified technician may independently clarify or authorize the dose modification because 247 CMR 8.04 permits receipt of new or omitted prescription information, while the noncertified technician must transfer both calls to a pharmacist.",
        "why": "Incorrect. Although a certified technician has additional limited authority to receive new or omitted prescription details with pharmacist approval, 247 CMR 8.04(4)(e) expressly prohibits therapy clarification or modification. The ordinary licensed technician may handle the unchanged refill under 8.02(6)(c)."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 8.02(6)(c)–(d); 247 CMR 8.04(4)(c),(e)",
    "url": "https://www.mass.gov/regulations/247-CMR-800-pharmacy-interns-and-technicians",
    "verified": "2026-11-16",
    "note": "MPJE trap: 'Refill authorization' does not mean a technician can negotiate or accept an altered regimen. Certification increases some technical duties, not permission to modify therapy."
  },
  {
    "id": "E30-082",
    "set": 17,
    "area": 2,
    "kind": "multi",
    "topic": "Naloxone standing order: third-party access, Schedule II offers and reporting alternative",
    "topicKey": "naloxone-dispensing",
    "stem": "A Massachusetts community pharmacy stocks prescription naloxone rescue kits and participates in the statewide naloxone standing order. An adult asks to obtain a kit to help a sibling who is at risk of opioid overdose, but has no patient-specific prescription. That afternoon, the pharmacy dispenses a lawful Schedule II oxycodone prescription to an unrelated patient. For its naloxone dispensings, the pharmacy chooses NOT to submit naloxone data through its daily Massachusetts PMP transmissions. It follows all other applicable counseling, labeling and dispensing requirements. Under M.G.L. c.94C §§19B–19C and Massachusetts Board Policy 2024-01 (revised February 6, 2025), which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A licensed pharmacist may dispense a naloxone rescue kit to the person seeking to assist the sibling under the statewide standing order without requiring a separate patient-specific prescription for the sibling.",
        "why": "Correct. M.G.L. c.94C §19B and the July 2026 statewide standing order permit a licensed pharmacist to supply a naloxone rescue kit to a family member, friend, or other person positioned to help someone at risk of overdose; Board Policy 2024-01, §I(B), allows dispensing under that order rather than requiring an individual prescriber-issued prescription."
      },
      {
        "text": "The pharmacist may omit any offer of naloxone to the unrelated oxycodone patient because federal approval of some OTC naloxone products superseded the Massachusetts Schedule II opioid offer requirement.",
        "why": "Incorrect. Board Policy 2024-01, §I(C), specifically states that a pharmacy MUST offer to dispense naloxone whenever a Schedule II opioid is dispensed. The separate existence of FDA-approved OTC naloxone does not remove the state standing-order policy's offer requirement."
      },
      {
        "text": "For insurance and cost-sharing under the statewide standing order, the pharmacy must always label the kit and create its prescription profile using the purchasing person's legal name and address; the words 'Naloxone Rescue Kit' cannot replace those fields.",
        "why": "Incorrect. Policy 2024-01, §I(E), expressly instructs use of 'Naloxone Rescue Kit' in place of the name and address when creating the profile and prescription label for the standing-order insurance transaction. The option reverses the Board's specific labeling direction."
      },
      {
        "text": "Because the pharmacy does not report naloxone through its daily PMP submissions, it must send the required report for the preceding calendar year by January 15, including the total number of naloxone DOSES dispensed and the number of those doses paid for with insurance.",
        "why": "Correct. Board Policy 2024-01, §II(B), specifies an alternative annual report due January 15 when a pharmacy chooses not to report naloxone through the PMP. It includes pharmacy name/ZIP, total doses (not the number of kits or prescriptions), and the number of doses paid for by insurance."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "M.G.L. c.94C §§19B–19C; MA Board Policy 2024-01 §§I(B)–(E), II(A)–(B), revised Feb. 6, 2025; 2026 Statewide Standing Order for Pharmacy Naloxone",
    "url": "https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download",
    "verified": "2026-11-16",
    "note": "MPJE trap: OTC naloxone sales and prescription naloxone dispensing under the statewide standing order are distinct. The Schedule II opioid offer, specific profile label, and daily-PMP versus January-15 annual reporting alternatives matter."
  },
  {
    "id": "E30-083",
    "set": 17,
    "area": 2,
    "kind": "single",
    "topic": "HIPAA amendment: 60-day response, one extension and linked record correction",
    "topicKey": "hipaa-amendment",
    "stem": "A HIPAA-covered Massachusetts pharmacy receives an adult patient's valid request to correct a dispensing date in the pharmacy's designated record set. The record was created by the pharmacy, the pharmacy confirms it is inaccurate, and no regulatory ground for denying amendment applies. On day 55 after receipt, the pharmacy knows its records team cannot finish processing by day 60. The patient has received no extension notice. Which proposed plan BEST satisfies the federal HIPAA amendment rule?",
    "choices": [
      {
        "text": "Treat the request like a right-of-access request, which requires action within 30 days; because that date has passed, automatically deny the amendment and ask the patient to submit a new request.",
        "why": "Incorrect. HIPAA differentiates access under 45 CFR 164.524, generally 30 days, from AMENDMENT under 45 CFR 164.526(b)(2), generally 60 days. Expiration of an unrelated access deadline does not justify denying a valid request to correct inaccurate PHI."
      },
      {
        "text": "Treat the pharmacy software vendor as the sole creator of the record, deny responsibility for correction, and refer the patient to the vendor even though the pharmacy created the inaccurate dispensing entry.",
        "why": "Incorrect. Section 164.526(a)(2)(i) permits denial in some circumstances when the covered entity did not create the record. Here the covered pharmacy itself created the inaccurate record; using a software vendor does not make that denial ground applicable."
      },
      {
        "text": "Notify the patient orally on day 60 that two successive 30-day extensions will be taken, and silently overwrite the original date without attaching a record of the accepted amendment.",
        "why": "Incorrect. Section 164.526(b)(2)(ii) permits only ONE extension of no more than 30 days and requires a written explanation and completion date within the original 60-day window. Section 164.526(c)(1) requires identifying affected records and appending or linking the amendment rather than an undocumented silent change."
      },
      {
        "text": "Before the original 60-day deadline, provide written reasons and a completion date for ONE extension of no more than 30 days; upon accepting the correction, identify the affected record, append or link the amendment, notify the patient, and address notification to appropriate recipients.",
        "why": "Correct. Section 164.526(b)(2) allows one written-notice extension of up to 30 days beyond the 60-day amendment response window. Section 164.526(c)(1)–(3) requires linking or appending the amendment, notifying the individual, obtaining the individual's identification/agreement where relevant, and making reasonable efforts to inform appropriate prior recipients and business associates."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "45 CFR 164.526(a)(1)–(2), (b)(2), (c)(1)–(3); distinction from HIPAA access deadline at 45 CFR 164.524(b)(2)",
    "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.526",
    "verified": "2026-11-16",
    "note": "MPJE trap: HIPAA AMENDMENT is generally 60 days, with one possible written-notice 30-day extension; HIPAA ACCESS is generally 30 days. Accepted amendments must be linked to the designated record set."
  },
  {
    "id": "E30-084",
    "set": 17,
    "area": 3,
    "kind": "single",
    "topic": "Massachusetts Schedule VI transfer: one-year issuance limit, remaining refills and no fee",
    "topicKey": "refills-transfers",
    "stem": "On November 16, 2026, a patient requests that Massachusetts Pharmacy A transfer TWO previously filled Schedule VI maintenance-drug prescriptions to licensed Massachusetts Pharmacy B. Prescription X was issued February 3, 2026 and has TWO authorized refills remaining. Prescription Y was issued October 20, 2025 and also has TWO authorized refills remaining; its most recent dispensing occurred October 10, 2026. Both were legitimate when issued. The patient has requested the transfers, the pharmacies can follow the applicable transfer procedure, and no new prescriber authorization has been issued. Pharmacy A proposes a $12 processing charge. Under 247 CMR 9.14, which response is MOST accurate?",
    "choices": [
      {
        "text": "Transfer both prescriptions because the one-year Schedule VI transfer period is measured from the most recent dispensing date, not the date each original prescription was issued.",
        "why": "Incorrect. 247 CMR 9.14(4)(c) expressly prohibits transferring a Schedule VI prescription authorizing refills more than one year after the prescription's ISSUE DATE. Prescription Y was issued October 20, 2025; the October 2026 dispensing does not restart that window."
      },
      {
        "text": "Transfer Prescription X in a timely manner without charging a transfer fee, but do not transfer Prescription Y for refills under the original prescription because more than one year has elapsed since issuance.",
        "why": "Correct. Section 9.14(1) requires timely transfers on patient request, §9.14(3) forbids a transfer fee, §9.14(4)(b) permits transfer of Schedule VI prescriptions with authorized refills remaining, and §9.14(4)(c) establishes the one-year issue-date limit. X qualifies; Y is outside its original time window."
      },
      {
        "text": "Refuse Prescription X because any Schedule VI prescription that has previously been dispensed can no longer be transferred; transfer Prescription Y because its last refill was recent.",
        "why": "Incorrect. The regulation explicitly permits transferring a Schedule VI prescription with remaining authorized refills. It is not categorically limited to never-filled prescriptions. Prescription Y is too old based on its issuance date, regardless of recent dispensing."
      },
      {
        "text": "Transfer Prescription X but charge the $12 fee if necessary to cover staff time; keep Prescription Y at Pharmacy A until the patient uses the remaining refills there.",
        "why": "Incorrect. Section 9.14(3) does not permit a processing or labor fee for the transfer. Moreover, the expired one-year issue-date limit cannot be bypassed merely by keeping Prescription Y at the original pharmacy for dispensing under the old authorization."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.14(1)–(4): timely transfer, no fee, Schedule VI remaining refills and one-year issuance limitation",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "MPJE trap: for Schedule VI transfer, the one-year restriction is counted from original issuance, not the latest refill. A pharmacy cannot charge for transferring a prescription."
  },
  {
    "id": "E30-085",
    "set": 17,
    "area": 4,
    "kind": "multi",
    "topic": "Paper and electronic pharmacy record segregation: Massachusetts versus DEA requirements",
    "topicKey": "pharmacy-recordkeeping",
    "stem": "A DEA-registered Massachusetts community pharmacy is preparing for a joint federal and state recordkeeping inspection. It has paper Schedule II, paper Schedule III–V, and paper Massachusetts Schedule VI prescriptions, together with electronic controlled-substance prescription records. It also retains purchasing, return, disposal, and destruction records. There is no exception for an institutional sterile-compounding pharmacy. Which proposed practices comply with BOTH applicable Massachusetts and federal requirements? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Keep paper Schedule II prescriptions in a separate Schedule II prescription file at the DEA-registered pharmacy location, rather than mixing them with ordinary Schedule VI paper prescriptions.",
        "why": "Correct. Federal 21 CFR 1304.04(h)(1)–(2) requires Schedule II pharmacy inventories/records separately and paper Schedule II prescriptions in a separate file at the registered location. Massachusetts 247 CMR 9.16(2) also requires paper Schedule II prescription segregation."
      },
      {
        "text": "Segregate the paper Schedule III–V prescriptions and separately segregate Massachusetts Schedule VI paper prescriptions, even though federal law provides a red-'C' filing method for some readily retrievable Schedule III–V prescriptions.",
        "why": "Correct. Massachusetts 247 CMR 9.16(3)–(4) expressly requires segregation of paper prescriptions for Schedules III–V and for Massachusetts Schedule VI. Federal 21 CFR 1304.04(h)(4) contains a red-'C' readily-retrievable method, but that federal allowance does not eliminate a more restrictive Massachusetts filing requirement."
      },
      {
        "text": "Store electronic Schedule II–V prescriptions only on a remote vendor system that cannot promptly retrieve or print records at the pharmacy, because off-site electronic storage always removes the DEA registered-location retrieval requirement.",
        "why": "Incorrect. Under 21 CFR 1304.04(h)(5), electronic controlled prescriptions may reside on computers elsewhere only if they are readily retrievable at the registered location and printable or transferable in a readily understandable format. Massachusetts 247 CMR 9.16(2)–(6) also demands electronic separability and printable records."
      },
      {
        "text": "Keep prescription records plus purchasing, returns, disposal, and destruction records readily retrievable for at least TWO YEARS, and maintain the capacity to print readable electronic prescriptions and stored prescription images.",
        "why": "Correct. Massachusetts 247 CMR 9.16(1) requires at least two years of readily retrievable prescription, purchasing, return, disposal, and destruction records, while (5)–(6) requires readable printouts of electronic prescriptions and electronically stored images. Federal 21 CFR 1304.04(a) sets a general two-year DEA minimum for records covered by Part 1304."
      }
    ],
    "correct": [
      "A",
      "B",
      "D"
    ],
    "citation": "247 CMR 9.16(1)–(6); 21 CFR 1304.04(a), (h)(1)–(5) (paper, electronic, readily retrievable and separately maintained records)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "MPJE trap: DEA's red-'C' federal filing option does not supersede Massachusetts requirements for paper prescription segregation. Electronic records must remain separable, retrievable and printable."
  },
  {
    "id": "E30-086",
    "set": 18,
    "area": 1,
    "kind": "multi",
    "topic": "CDTM continuing qualifications: insurance, prescribing registrations, annual CE, and Board restrictions",
    "topicKey": "cdtm",
    "stem": "A Massachusetts community pharmacist has seven years of licensed practice and participates in a current hypertension collaborative drug therapy management (CDTM) agreement with TWO supervising physicians. The agreement authorizes patient-specific prescribing. The pharmacist's liability policy has a $1 million annual aggregate limit but covers only $250,000 per occurrence, and the Board has just imposed a practice restriction through an agreed disciplinary disposition. The pharmacist is reviewing what must be corrected or reported before continuing CDTM activities. Under 247 CMR 16.02, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist must maintain professional liability insurance specifically covering CDTM with at least $1 million PER OCCURRENCE throughout the agreement; the stated aggregate limit does not cure the inadequate per-occurrence limit.",
        "why": "Correct. 247 CMR 16.02(1)(b) expressly requires liability insurance of at least $1,000,000 per occurrence, specifically covering drug therapy management, throughout the collaborative practice agreement. The described $250,000 per-occurrence coverage is insufficient even with a $1 million aggregate."
      },
      {
        "text": "Completion of five CDTM-related CE hours during the FIRST year satisfies the additional CDTM education requirement for the full two-year agreement because the ordinary pharmacist license requires continuing education separately.",
        "why": "Incorrect. Section 16.02(1)(e) requires at least five ADDITIONAL Board-approved contact hours in EACH year of the CDTM agreement, addressing practice areas generally related to that agreement. Completing five hours in only one year does not cover another year."
      },
      {
        "text": "Because prescribing is included, the pharmacist must maintain the applicable Massachusetts controlled-substance registration and meet the prescribing-related training and MassHealth participation/application attestation requirements.",
        "why": "Correct. Section 16.02(1)(f) adds a current Department-issued MCSR, the applicable initial and biennial training, and a signed MassHealth participation-or-application attestation when prescriptive practices form part of the CDTM agreement. Ordinary licensure or a physician's signature does not replace these obligations."
      },
      {
        "text": "The pharmacist must give WRITTEN notice of the Board-imposed practice restriction to EACH supervising physician, even though the restriction resulted from an agreement rather than a formal Board order.",
        "why": "Correct. Section 16.02(3) expressly applies to Board discipline by agreement or order and to other practice restrictions, requiring written notification to every supervising physician. Having two physicians does not allow notification of only one."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "247 CMR 16.02(1)(b),(e)–(f), (3); Massachusetts Board of Registration in Pharmacy, Collaborative Drug Therapy Management regulation",
    "url": "https://www.mass.gov/regulations/247-CMR-1600-collaborative-drug-therapy-management",
    "verified": "2026-11-16",
    "note": "Remember PER OCCURRENCE insurance, five ADDITIONAL CDTM CE hours EACH year, extra credentials for CDTM prescribing, and written notice to every supervising physician of Board restrictions."
  },
  {
    "id": "E30-087",
    "set": 18,
    "area": 2,
    "kind": "single",
    "topic": "Prospective DUR: flagged therapeutic duplication during an anticoagulant switch",
    "topicKey": "counseling-dur",
    "stem": "A Massachusetts community pharmacy receives a valid new electronic apixaban prescription from an authorized practitioner. The patient's profile still lists rivaroxaban as active, and the computer flags potentially dangerous therapeutic duplication. The patient says the physician intended a switch but cannot recall exactly when the previous anticoagulant was to be stopped. A certified technician suggests clearing the alert because the new prescription is electronically authenticated. No dispensing has yet occurred. Which action is MOST consistent with 247 CMR 9.17 and the pharmacist's professional responsibility?",
    "choices": [
      {
        "text": "Allow the technician to close the alert and dispense immediately, because electronic prescriber authentication satisfies the pharmacist's prospective review obligation for a clinically significant therapy change.",
        "why": "Incorrect. An electronically authenticated prescription may still present a clinically significant drug-therapy problem. Section 9.17(1) places the prospective DUR responsibility on the pharmacist and specifically includes therapeutic duplication and significant changes in therapy. Technician or software clearance cannot substitute for the pharmacist's clinical review."
      },
      {
        "text": "Have the pharmacist assess the duplication BEFORE dispensing, obtain sufficient clarification from the patient and/or prescriber as clinically necessary, document the measures taken in response to DUR, and dispense only after the therapy plan is determined appropriate.",
        "why": "Correct. Under 247 CMR 9.17(1)–(2), the pharmacist must conduct prospective DUR before dispensing, make a reasonable effort to identify therapeutic duplication and significant therapy changes, take appropriate patient-protective measures, and document the measures taken. Contact with the prescriber is a possible means of clarification, not a universal fixed requirement for every alert."
      },
      {
        "text": "Permanently refuse every prescription whenever the computer detects two drugs in the same therapeutic class, even if further investigation confirms that the old drug was discontinued before the new one starts.",
        "why": "Incorrect. Section 9.17 requires professional assessment and appropriate measures, not categorical refusal whenever an automated duplicate-therapy warning appears. A clinically appropriate transition may be lawful once properly evaluated."
      },
      {
        "text": "Dispense now and perform the pharmacist's prospective DUR at the patient's next refill, because the patient verbally confirmed that a switch was intended.",
        "why": "Incorrect. The statute and 247 CMR 9.17(1) require prospective DUR BEFORE a new prescription is dispensed or delivered. The patient's uncertain timing does not justify postponing assessment of a potentially significant overlap."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.17(1)(b),(i), (2); M.G.L. c.94C §21A (prospective drug review)",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "Computerized flags support—but do not replace—pharmacist judgment. Investigate clinically significant duplication before dispensing and document what you did; there is no automatic mandatory refusal for every alert."
  },
  {
    "id": "E30-088",
    "set": 18,
    "area": 2,
    "kind": "single",
    "topic": "2026 Massachusetts pharmacist HIV PEP: sexually active minor, 72-hour exposure window, and no baseline-test delay",
    "topicKey": "public-health-prescribing",
    "stem": "In November 2026, a properly trained Massachusetts pharmacist who is otherwise qualified under the applicable statewide oral HIV PEP prescribing guidance evaluates a clinically eligible 25-year-old adult. Thirty-six hours earlier, the patient shared injection equipment with someone whose HIV status is unknown; the pharmacist has assessed the exposure and documented a sufficiently substantial risk to warrant PEP after individualized clinical evaluation. The patient gives consent and has no known HIV infection, symptoms suggesting acute HIV, interacting medicines, or other protocol exclusion. A baseline blood-based HIV test has been ordered urgently, but the result is not yet available; no appropriate rapid test is immediately accessible. What is the BEST next action?",
    "choices": [
      {
        "text": "Defer all PEP until the laboratory HIV-negative result arrives even if the delay causes initiation to occur more than 72 hours after exposure.",
        "why": "Incorrect. CDC 2025 nPEP recommendations emphasize starting indicated PEP as soon as possible, no later than 72 hours, without delaying the first dose for pending laboratory results. Baseline HIV testing should still be obtained promptly and interpreted."
      },
      {
        "text": "Decline because Massachusetts pharmacist HIV PEP prescribing always requires a patient-specific physician-signed CDTM agreement, even when all applicable statewide prescribing criteria are satisfied.",
        "why": "Incorrect. M.G.L. c.94C §19F and Massachusetts DPH Circular DCP 26-08-125 independently authorize appropriately qualified pharmacists to prescribe specified HIV prevention medications under statewide guidance. A separate patient-specific CDTM agreement is not inherently required for that distinct authority."
      },
      {
        "text": "Issue a 90-day PrEP prescription with two refills as a substitute for urgent PEP and postpone follow-up HIV testing until a refill is requested.",
        "why": "Incorrect. An exposure that occurred 36 hours ago calls for the PEP pathway when clinically indicated. PEP is a 28-day course with baseline and follow-up testing; it is not interchangeable with routine PrEP, which is intended for prospective prevention."
      },
      {
        "text": "Arrange timely baseline HIV testing and follow-up, initiate an appropriate 28-day oral PEP regimen promptly without awaiting a pending laboratory result, and coordinate the medical evaluation and monitoring required by the statewide protocol.",
        "why": "Correct. CDC 2025 nPEP recommendations support starting eligible patients' 28-day PEP as soon as possible within 72 hours without waiting for pending laboratory test results, while still performing baseline and follow-up HIV evaluation. M.G.L. c.94C §19F and DPH Circular DCP 26-08-125 authorize appropriately qualified Massachusetts pharmacists to prescribe covered HIV-prevention medications under statewide guidance. The stem explicitly assumes other state-protocol eligibility requirements are met."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §19F; Massachusetts DPH Circular DCP 26-08-125 (Aug. 25, 2026); CDC MMWR 2025 nPEP recommendations (72 hours, baseline testing and 28-day treatment); Massachusetts statewide oral PEP protocol exists (Sept. 2026 DOCX), details not independently authenticated",
    "url": "https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download",
    "verified": "2026-11-17",
    "note": "Revision 2 replaces original adolescent eligibility/50-kg/no-refills case because the September 2026 DPH pharmacist PEP DOCX was confirmed on the agency site but could not be read to authenticate exact minor/weight/quantity rules. This case instead explicitly assumes eligible adult, established pharmacist qualifications and applicable statewide guidance, and tests CDC-verified PEP timing, baseline testing and 28-day course. Do not infer this validates pediatric pharmacist-prescribing rules. Key D retained.",
    "revision": 2
  },
  {
    "id": "E30-089",
    "set": 18,
    "area": 3,
    "kind": "single",
    "topic": "Return to stock: an uncollected prescription, required container labeling, and lot-specific recall holds",
    "topicKey": "label-packaging",
    "stem": "A Massachusetts community pharmacy filled a patient-specific, nonhazardous Schedule VI tablet prescription, but the patient NEVER picked it up and the prescription was NEVER delivered. Staff want to return the tablets to available pharmacy stock for possible later lawful dispensing. The pharmacy also learns that one manufacturer's lot of this medication is being recalled; it is not yet known whether the prepared tablets came from the recalled lot. The pharmacy has a compliant general return-to-stock policy. Which approach BEST complies with 247 CMR 9.13?",
    "choices": [
      {
        "text": "Pour the uncollected tablets into the manufacturer's bulk stock bottle after comparing the NDC; a pharmacist's visual check overcomes the regulation's restriction on refilling bulk bottles.",
        "why": "Incorrect. Section 9.13(1)(a) expressly states that a pharmacy may NOT return a medication to the manufacturer's stock bottle. NDC matching or pharmacist inspection does not create an exception."
      },
      {
        "text": "Destroy the tablets in all circumstances, because creation of a patient label makes the preparation legally equivalent to a medication already dispensed to a patient.",
        "why": "Incorrect. Section 9.13(1) expressly allows return to stock when a prescription was PREPARED but the medication was NOT dispensed. This is different from a patient returning medication after it was dispensed under 247 CMR 9.01(5)–(7)."
      },
      {
        "text": "Retain the tablets in the original patient container or an appropriate alternate container labeled with product, strength, manufacturer/supplier or NDC, and the expiration assigned at filling; do not dispense this potentially recalled return-to-stock medication unless its actual lot is confirmed outside the recall.",
        "why": "Correct. Section 9.13(1)(b) requires the four return-to-stock labeling elements and permits the original patient container or an appropriate alternative. Section 9.13(3) prohibits dispensing returned-to-stock medication potentially subject to a recall until the pharmacy can confirm the specific lot is NOT included. The product cannot simply be poured back into the manufacturer bottle."
      },
      {
        "text": "Place the tablets in an unlabeled internal bag and use them for another patient as soon as a barcode scan matches the product, because recall restrictions apply only to medication remaining in the original manufacturer's packaging.",
        "why": "Incorrect. Return-to-stock containers require specific identifying information under §9.13(1)(b), and §9.13(3) applies to potentially recalled medication that has been returned to stock, not just to manufacturer's original containers. A matching product barcode is not confirmation that a lot is outside the recall."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 9.13(1)(a)–(b), (2)–(3); compare 247 CMR 9.01(5)–(7) for medication returned AFTER dispensing",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "PREPARED but never dispensed can be returned to stock with a labeled container; never pour it into the manufacturer's stock bottle. A recalled-or-possibly-recalled lot cannot be redispensed until the lot is verified to be excluded."
  },
  {
    "id": "E30-090",
    "set": 18,
    "area": 4,
    "kind": "multi",
    "topic": "Automated pickup APS versus robotic PPA: schedule restrictions, cold products, and mixed-lot recall controls",
    "topicKey": "automation-systems",
    "stem": "A Massachusetts licensed community pharmacy plans TWO separate technologies: a wall-secured Automated Pharmacy System (APS) for patients to collect already filled prescriptions and a Pharmacy Processing Automation (PPA) machine to count and fill prescription containers. The pharmacy maintains the applicable policies and all requirements not explicitly addressed below. Which proposed arrangements are permitted under 247 CMR 9.10–9.11? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Use a continuously video-monitored, technology-verified APS located in the SAME BUILDING as the pharmacy to release an otherwise valid Schedule IV prescription after hours, with patient choice, an identifying electronic audit trail and a pharmacist consultation opportunity whenever it dispenses.",
        "why": "Correct. 247 CMR 9.10(1)(a)–(h) permits an APS to release Schedule IV–VI medications during or after pharmacy operating hours when, among other conditions, it remains in the same building, is secured and video-monitored, verifies the drug and patient, keeps a traceable audit trail, offers pharmacist consultation whenever dispensing, and permits the patient to decline APS use."
      },
      {
        "text": "Use that same APS to release a Schedule II oxycodone prescription after hours because DEA registration, camera surveillance, and barcode verification make the device eligible for EVERY controlled-substance schedule.",
        "why": "Incorrect. Section 9.10(1) limits retail APS dispensing to Schedules IV–VI. Added identification technology and DEA registration do not expand the APS's legal scope to Schedule II."
      },
      {
        "text": "If the PPA machine commingles different manufacturing lot numbers in one dispensing cell, maintain a procedure to quarantine ALL commingled lot numbers whenever one lot is recalled.",
        "why": "Correct. 247 CMR 9.11(1)(b) specifically requires a pharmacy whose PPA commingles lot numbers in a single cell to maintain a policy and procedure to quarantine all the commingled lot numbers if one lot number is recalled. Verification technology remains required under §9.11(1)(a)."
      },
      {
        "text": "Stock insulin that REQUIRES refrigeration in the APS for patient pickup if the appliance incorporates a reliable temperature logger and a pharmacist verifies stability before loading.",
        "why": "Incorrect. Section 9.10(1)(d) categorically prohibits stocking any medication requiring refrigeration or reconstitution in an APS. Temperature logging cannot override this rule."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 9.10(1)(a)–(h), 9.11(1)(a)–(b); Massachusetts Board of Registration in Pharmacy, Professional Practice Standards",
    "url": "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards",
    "verified": "2026-11-16",
    "note": "APS patient pickup is restricted to Schedules IV–VI and no refrigerated or reconstituted drugs. PPA robotic filling has its own mixed-lot recall quarantine rule. Never confuse APS, PPA and healthcare-facility ADD."
  },
  {
    "id": "E30-091",
    "set": 19,
    "area": 1,
    "kind": "single",
    "topic": "Dedicated training personnel: when a trainer is excluded but the supervised trainee still counts",
    "topicKey": "workforce-supervision",
    "stem": "A Massachusetts community pharmacy is NOT providing vaccination services. One pharmacist supervises a prescription-filling team of FOUR licensed support personnel: TWO licensed certified pharmacy technicians, ONE licensed noncertified technician, and ONE licensed pharmacy technician trainee (PTT). The PTT is directly supervised by an ADDITIONAL licensed certified technician assigned exclusively as the PTT's dedicated trainer. The trainer and trainee have appropriate name badges and were designated on the pharmacy's published staffing schedule BEFORE that training day; written training policies are in place. The trainer does not independently fill, process, or otherwise support prescriptions. No separate Board waiver applies. Under Massachusetts Board Policy 2026-02, which staffing conclusion is MOST accurate?",
    "choices": [
      {
        "text": "The pharmacist may count only the two certified technicians and the noncertified technician, because a dedicated trainer and the associated PTT are BOTH excluded from the supervisory ratio.",
        "why": "Incorrect. Board Policy 2026-02, Section III(A)(2)(c), specifically counts a supervised 'Trainee' in the pharmacist ratio as a pharmacy technician. Excluding the dedicated trainer does not also exempt the trainee while the trainee performs prescription-support duties."
      },
      {
        "text": "The four-person filling team meets the ordinary 1:4 ratio with two certified technicians; the separately designated trainer may be excluded while working solely in the trainer–trainee role, but the PTT remains counted among the four.",
        "why": "Correct. Policy 2026-02, Section I(A)(1)(b), permits 1:4 with at least two licensed certified technicians. Sections III and III(A)–(B) exclude a properly designated trainer who performs NO independent pharmacy-support duties, while requiring the actively participating trainee to count as a pharmacy technician. The advance schedule, badges, and supervision meet the stated training conditions."
      },
      {
        "text": "The dedicated trainer can remain excluded if the trainer starts independently preparing an additional patient's prescription, as long as another technician checks the work.",
        "why": "Incorrect. Under Policy 2026-02, Sections III and III(A)(1)(c), a trainer who performs professional support work outside the trainer–trainee relationship must be counted. That would make five counted filling-support personnel here, exceeding the ordinary 1:4 ratio at a pharmacy not providing vaccinations."
      },
      {
        "text": "The pharmacy may use the 1:6 immunization-service ratio regardless of whether it vaccinates anyone, so the number and certification status of the support staff are irrelevant.",
        "why": "Incorrect. Policy 2026-02, Section I(B), makes the 1:6 provision conditional on a pharmacy providing vaccination services and on the minimum qualifying certified/intern support mix. Neither condition can be presumed at this nonvaccinating pharmacy."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "Massachusetts Board Policy 2026-02, §§I(A)(1)(b), I(B), III(A)–(B) (adopted Sept. 3, 2026); 247 CMR 8.00",
    "url": "https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download",
    "verified": "2026-11-16",
    "note": "The trainer exemption is conditional. Count the active trainee, not the dedicated trainer who only trains, and do not apply the 1:6 vaccination ratio to a nonvaccinating site."
  },
  {
    "id": "E30-092",
    "set": 19,
    "area": 2,
    "kind": "single",
    "topic": "HIPAA confidential communications: reasonable alternate-contact request versus proving endangerment",
    "topicKey": "hipaa-communications",
    "stem": "A HIPAA-covered Massachusetts community pharmacy routinely calls a household landline and mails refill notices to the patient's home. An adult patient asks that FUTURE prescription-related communications instead be sent only to the patient's personal mobile number because several other people share the household. The pharmacy can reasonably accommodate the request using its existing workflow. The patient supplies the alternate number but refuses to describe the personal reason for confidentiality. No separate disclosure law or unusual operational burden applies. Which response BEST follows the federal HIPAA confidential-communications rule?",
    "choices": [
      {
        "text": "The pharmacy must reject the request until the patient proves that a communication to the household could endanger the patient's safety; this is required for every covered provider.",
        "why": "Incorrect. Under 45 CFR 164.522(b)(1)(i), a covered HEALTH CARE PROVIDER must accommodate a reasonable alternative-contact request without a required endangerment statement. The express endangerment-statement condition in 164.522(b)(1)(ii) applies to HEALTH PLANS, not automatically to this pharmacy."
      },
      {
        "text": "The pharmacy may require a signed explanation identifying the sensitive diagnosis that motivated the request; without it, the pharmacy has no duty to use the supplied alternate contact method.",
        "why": "Incorrect. 45 CFR 164.522(b)(2)(iii) explicitly prohibits a covered health care provider from conditioning confidential communications on an explanation of the patient's reason. Requiring a diagnosis disclosure would contradict the rule."
      },
      {
        "text": "The pharmacy must withhold all future prescription counseling, refill reminders and treatment communications until the patient signs a separate HIPAA authorization covering each communication.",
        "why": "Incorrect. Section 164.522(b) concerns reasonable changes to the means or location of communications. It does not turn routine permitted provider–patient treatment or prescription communications into disclosures requiring individual HIPAA authorizations."
      },
      {
        "text": "The pharmacy must accommodate this reasonable alternate-contact request; it may require the request in writing and an alternate address or contact method, but cannot demand an explanation of the patient's reason as a condition of accommodating it.",
        "why": "Correct. 45 CFR 164.522(b)(1)(i) obligates covered providers to accommodate reasonable confidential communications requests. Section 164.522(b)(2) permits a written request and information concerning alternate contact or payment when appropriate, but expressly prohibits a provider from demanding a reason."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "45 CFR 164.522(b)(1)(i)–(ii), (b)(2)(i)–(iv); HHS OCR guidance, alternative confidential communications",
    "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.522",
    "verified": "2026-11-16",
    "note": "Do not confuse a provider with a health plan. A provider must accommodate a reasonable confidentiality request and cannot require the patient to explain why."
  },
  {
    "id": "E30-093",
    "set": 19,
    "area": 2,
    "kind": "multi",
    "topic": "NCVIA vaccine records: VIS edition and distribution date versus lot and vaccinator identification",
    "topicKey": "immunization",
    "stem": "A Massachusetts community pharmacist correctly administers a federally covered inactivated influenza vaccination to an adult under a valid standing order. The pharmacy provided the current Vaccine Information Statement (VIS) before the injection, and all Massachusetts MIIS reporting and clinical requirements have been met. An internal audit finds that the patient's permanent immunization record lacks some federal documentation elements, although the electronic system contains the patient's name and the administered dose. Under the federal National Childhood Vaccine Injury Act (NCVIA) and CDC VIS instructions, which additions or practices are required or permitted as described? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Record the vaccine's administration date, manufacturer, and lot number in the patient's permanent medical record or an authorized permanent office log.",
        "why": "Correct. 42 U.S.C. 300aa-25(a)(1)–(2) requires the vaccine administration date plus manufacturer and lot number in the patient's permanent record or a qualifying permanent office log, even where the dose is already recorded in the state registry."
      },
      {
        "text": "Omit the name, address and professional title of the vaccinator because the patient is an adult and the pharmacy's name is visible on the retail receipt.",
        "why": "Incorrect. Section 300aa-25(a)(3) applies to covered vaccinations given to any person, not just children, and requires the vaccinating provider's name, address and, if appropriate, title in the permanent record or qualifying log. A retail receipt without those elements is not a substitute."
      },
      {
        "text": "Document BOTH the edition date of the VIS furnished and the date it was given; recording only the vaccination date does not meet the separate VIS documentation requirement.",
        "why": "Correct. CDC's Instructions for Using VISs, implementing 42 U.S.C. 300aa-26, require documentation of the specific VIS edition date AND the date the VIS was provided. Those are distinct from the administration date required by §300aa-25."
      },
      {
        "text": "Document the name, address and appropriate title of the vaccinating healthcare provider in the recipient's permanent medical record OR in a permanent office log accessible to the patient's legal representative on request.",
        "why": "Correct. Section 300aa-25(a) explicitly permits an appropriate permanent office log or file accessible to the legal representative rather than requiring that every field appear exclusively in the main electronic patient chart. The vaccinator identity and address must still be recorded."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "42 U.S.C. §300aa-25(a)(1)–(4); 42 U.S.C. §300aa-26; CDC Instructions for Using VISs, 'Record information for each VIS provided'",
    "url": "https://www.cdc.gov/vaccines/hcp/about-vis/instructions.html",
    "verified": "2026-11-16",
    "note": "Federal vaccine documentation has two linked sets: vaccine administration/manufacturer/lot/vaccinator, plus VIS edition and date provided. An adult recipient is not exempt."
  },
  {
    "id": "E30-094",
    "set": 19,
    "area": 3,
    "kind": "single",
    "topic": "CMEA pseudoephedrine: mobile retail vendor 7.5-gram limit versus ordinary 9-gram purchaser limit",
    "topicKey": "otc-pseudoephedrine",
    "stem": "Four INDEPENDENT prospective purchasers are at different federally compliant, self-certified sellers in Massachusetts, seeking additional over-the-counter pseudoephedrine. All quantities are PSE BASE equivalents, all earlier purchases below are within the relevant 30-day window, all required photo IDs and sales records are available, and no state-specific or other restrictions apply. Each proposed sale would occur in a single transaction. Under the federal Combat Methamphetamine Epidemic Act (CMEA), which proposed sale is permissible?",
    "choices": [
      {
        "text": "A MOBILE retail vendor sells an additional 0.60 gram to a purchaser who has already obtained 7.20 grams from that mobile vendor within the preceding 30 days, with no purchases earlier today.",
        "why": "Incorrect. 21 U.S.C. 830(e)(1)(A)(ix)(II) and 21 CFR 1314.20(b) limit mobile retail vendor sales to 7.5 grams of pseudoephedrine base per purchaser in any 30-day period. The resulting 7.80 grams exceeds that mobile-vendor limit, despite being below the general 9-gram individual-purchase ceiling."
      },
      {
        "text": "A conventional walk-in retail pharmacy sells another 0.50 gram to a purchaser who already purchased 8.60 grams of pseudoephedrine base at retail in the same 30-day period, with no earlier purchases today.",
        "why": "Incorrect. Although the calendar-day quantity would be below 3.6 grams, the federal individual retail-purchase limit is 9 grams per 30 days under 21 U.S.C. 844(a). The proposed 9.10 grams exceeds it."
      },
      {
        "text": "A MOBILE retail vendor sells an additional 0.60 gram to a purchaser who previously bought 6.90 grams from that vendor in the current 30-day period and made no other purchases today.",
        "why": "Correct. A mobile retail vendor's 30-day ceiling is 7.5 grams of pseudoephedrine base, and 6.90 + 0.60 = exactly 7.50 grams. The same calendar day's sale is below the federal 3.6-gram daily limit. The scenario assumes compliance with all other seller and buyer requirements."
      },
      {
        "text": "A conventional walk-in retail pharmacy sells another 0.60 gram to a purchaser who already purchased 3.10 grams from that pharmacy earlier on the SAME calendar day, despite having bought only 3.10 grams in the entire 30-day period.",
        "why": "Incorrect. Federal 21 U.S.C. 830(d)(1) and 21 CFR 1314.20(a) limit sales to 3.6 grams per purchaser in a single calendar day regardless of how many transactions occur. The combined 3.70 grams exceeds that daily limit despite remaining below the general 30-day ceiling."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 U.S.C. 830(d)(1), (e)(1)(A)(ix), 844(a); 21 CFR 1314.20(a)–(b); DEA CMEA General Information",
    "url": "https://www.deadiversion.usdoj.gov/meth/cma2005.html",
    "verified": "2026-11-16",
    "note": "The 3.6 g/day rule applies to retail sales; a mobile vendor has an additional 7.5 g/30-day sales ceiling, while the individual retail purchase limit is generally 9 g/30 days."
  },
  {
    "id": "E30-095",
    "set": 19,
    "area": 4,
    "kind": "multi",
    "topic": "Federal compounding: limited 503A anticipatory stock versus 503B outsourcing office-use distribution",
    "topicKey": "federal-compounding-models",
    "stem": "Two Massachusetts-based entities are reviewing federal human-drug compounding exemptions. Pharmacy A is a state-licensed community pharmacy whose pharmacists compound under section 503A, NOT an FDA-registered outsourcing facility. Facility B is an FDA-registered 503B outsourcing facility compounding sterile products. Assume all other respective federal and Massachusetts compounding, product-quality, licensure and distribution conditions are met unless a choice expressly violates the cited patient-prescription requirement. Which statements correctly describe these different pathways? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Pharmacy A may compound LIMITED quantities before receiving an identified patient's valid prescription if a documented history of valid orders for that drug arose from established relationships with the patients or the prescribers expected to write those orders; distribution still requires the valid patient-specific prescription.",
        "why": "Correct. FD&C Act §503A(a)(2) (21 U.S.C. 353a(a)(2)) allows LIMITED anticipatory compounding based on historical valid prescriptions within established pharmacist/patient or pharmacist/prescriber relationships. FDA's final §503A prescription-requirement guidance states that anticipated doses may not be distributed before a valid individual-patient prescription is received."
      },
      {
        "text": "Pharmacy A qualifies for the 503A exemptions by sending a compounded batch to a physician's office for use on unnamed future patients based only on a general 'office stock' purchase order.",
        "why": "Incorrect. A general office-use purchase order without any patient-specific prescription does not satisfy the federal §503A patient-prescription requirement. FDA distinguishes 503A from the qualified §503B outsourcing pathway, which can supply office stock. State authorization alone cannot replace the federal requirement for the 503A exemptions."
      },
      {
        "text": "Facility B, if compliant with all §503B conditions, may compound and distribute eligible sterile products for office stock without prescriptions identifying individual patients, while remaining subject to applicable current good manufacturing practice (CGMP) requirements.",
        "why": "Correct. FD&C Act §503B(d)(4)(C) expressly permits an outsourcing facility to obtain or not obtain prescriptions for identified individual patients. FDA explains that qualifying 503B facilities may supply office stock but remain subject to CGMP and other §503B requirements."
      },
      {
        "text": "Facility B is exempt from CGMP merely because its batches are compounded rather than conventionally manufactured, exactly as a qualifying 503A pharmacy is.",
        "why": "Incorrect. The FD&C Act §503A exemption includes CGMP requirements only when every 503A condition is satisfied, whereas §503B does NOT exempt qualifying outsourcing-facility compounding from CGMP. The two pathways are not interchangeable."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "FD&C Act §§503A(a)(1)–(2), 503B(d)(4)(C) (21 U.S.C. §§353a, 353b); FDA Human Drug Compounding Laws and Prescription-Requirement-Under-503A Final Guidance",
    "url": "https://www.fda.gov/drugs/human-drug-compounding/human-drug-compounding-laws",
    "verified": "2026-11-16",
    "note": "503A anticipatory compounding is limited and tied to historical patient-specific prescription demand; 503B outsourcing facilities may supply office stock but remain subject to CGMP."
  },
  {
    "id": "E30-096",
    "set": 20,
    "area": 1,
    "kind": "single",
    "topic": "Reciprocal discipline: another state's consent probation versus a Massachusetts advisory letter",
    "topicKey": "board-discipline",
    "stem": "A Massachusetts-licensed pharmacist also holds a New Hampshire license. The New Hampshire board places that license on probation by a signed consent agreement after finding falsified controlled-substance inventory records; the same conduct would violate Massachusetts pharmacy law. In an unrelated Massachusetts matter, the Massachusetts Board issues only an ADVISORY LETTER, not a reprimand or probation order. Which description BEST reflects the Massachusetts Board's authority and the status of that letter?",
    "choices": [
      {
        "text": "The Massachusetts Board cannot initiate reciprocal discipline because the New Hampshire case was resolved by consent instead of a contested hearing; its advisory letter is non-disciplinary.",
        "why": "Incorrect. Under 247 CMR 10.06(6)–(7), a consent agreement can impose discipline, and out-of-state discipline may support a Massachusetts proceeding when the conduct violates Massachusetts law. A contested hearing in New Hampshire is not an absolute prerequisite to initiating Massachusetts action."
      },
      {
        "text": "The New Hampshire probation automatically suspends the Massachusetts pharmacist license, and the Massachusetts advisory letter is itself a formal reprimand.",
        "why": "Incorrect. Section 10.06(7) makes out-of-state action a possible basis for INITIATING Massachusetts discipline, not an automatic Massachusetts suspension. Section 10.06(2) explicitly says an advisory letter is not formal disciplinary action."
      },
      {
        "text": "The Massachusetts Board must immediately impose identical probation whenever any state disciplines a pharmacist, regardless of whether the underlying conduct would violate Massachusetts law.",
        "why": "Incorrect. Section 10.06(7) uses MAY and conditions reciprocal action on conduct that constitutes a Massachusetts-law violation. Disciplinary action is not automatically identical or mandatory, and statutory protections can also restrict particular reciprocal discipline."
      },
      {
        "text": "The Massachusetts Board MAY initiate its own proceeding based on the New Hampshire discipline because the underlying conduct would violate Massachusetts law; the Massachusetts advisory letter itself is not formal discipline.",
        "why": "Correct. Section 10.06(7) permits, rather than automatically imposes, disciplinary proceedings based on another state's action when the underlying conduct would violate Massachusetts law. Section 10.06(2) states that an advisory letter identifies concerns but does NOT constitute formal disciplinary action; probation and reprimand are different formal sanctions under 10.06(3)–(4)."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 10.06(2)–(4),(6)–(7); 247 CMR 10.03(1)(t); M.G.L. c.112 §32 (protected-services limitation where applicable)",
    "url": "https://www.mass.gov/regulations/247-CMR-1000-disciplinary-proceedings",
    "verified": "2026-11-16",
    "note": "A Board advisory letter is not a reprimand. Out-of-state probation under a consent agreement can support a new MA proceeding, but does not automatically suspend a Massachusetts license; the underlying conduct must meet the MA-law test."
  },
  {
    "id": "E30-097",
    "set": 20,
    "area": 2,
    "kind": "multi",
    "topic": "Physician assistant prescriptive scope: full versus temporary license, DEA number, and CII review",
    "topicKey": "prescriber-authority",
    "stem": "A Massachusetts pharmacy receives prescriptions prepared by physician assistants (PAs). For the fully licensed PA, current Massachusetts controlled-substance registration (MCSR), individual DEA registration for the appropriate schedules, mutually approved written prescribing guidelines, supervising-physician arrangements and other prescription formalities are in place. A second PA holds only a TEMPORARY Massachusetts PA license. No emergency or other exception changes the stated licensing rules. Which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The fully licensed PA may issue a Schedule II prescription using ONLY the supervising physician's DEA number when the physician has approved the written prescribing guidelines.",
        "why": "Incorrect. The Massachusetts PA practice FAQ and M.G.L. c.94C require a PA who prescribes federally controlled Schedules II–V to have the PA's OWN appropriate DEA registration, in addition to the required MCSR; a physician's DEA number is not interchangeable with the PA's registration."
      },
      {
        "text": "The fully licensed PA may issue a Schedule III prescription within the PA's authorized scope using the PA's own registrations; Massachusetts does not universally require the supervising physician's name to appear on the PA's prescription.",
        "why": "Correct. 263 CMR 5.06(1),(4),(7) permits an appropriately registered, fully licensed PA to prescribe within the agreed guidelines and applicable law. Massachusetts PA Board FAQs state that the supervising physician's name is NOT required on a PA prescription, while the PA must possess the PA's own MCSR and DEA authorization for Schedules II–V."
      },
      {
        "text": "A PA holding only a temporary license may issue an otherwise permitted WRITTEN prescription in the temporary PA's own name and signature, provided the supervising physician cosigns it after the patient receives the prescription.",
        "why": "Incorrect. Under 263 CMR 5.06(2)(a),(c), a temporarily licensed PA may PREPARE a written prescription, but the supervising or designated physician must sign it BEFORE issuance and it must be issued in that physician's name. After-the-fact cosignature is not sufficient."
      },
      {
        "text": "A Schedule II prescription issued by a fully licensed PA is subject to the supervising or designated physician's review within 96 hours after issuance, even when the PA was authorized to issue it.",
        "why": "Correct. 263 CMR 5.06(3) specifically requires the supervising physician (or designated temporary supervisor) to review the PA's Schedule II prescription or medication order WITHIN 96 HOURS after issuance. This is a distinct follow-up duty from an improperly delayed countersignature for a temporary PA."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "263 CMR 5.06(1)–(4),(7); M.G.L. c.94C §§7,9,20; Massachusetts PA Board FAQs on DEA numbers and supervisor name",
    "url": "https://www.mass.gov/info-details/frequently-asked-questions-about-physician-assistants-practice",
    "verified": "2026-11-16",
    "note": "A fully licensed PA needs independent MCSR/DEA authority for Schedule II–V drugs; the supervising MD's DEA number cannot be borrowed. Temporary PA prescriptions require prior MD authorization; a fully licensed PA's Schedule II order gets physician review within 96 hours."
  },
  {
    "id": "E30-098",
    "set": 20,
    "area": 2,
    "kind": "single",
    "topic": "Independent nurse practitioner: supervisor-name omission and pharmacist verification",
    "topicKey": "prescriber-authority",
    "stem": "A Massachusetts-licensed nurse practitioner (NP) has obtained independent prescriptive-practice authority after completing the required supervised experience. The NP transmits an otherwise valid, properly signed electronic Schedule IV prescription using the NP's own current appropriate MCSR and DEA registrations. The prescription does NOT identify a supervising physician, and the pharmacist has no clinical or authenticity concerns. Under Massachusetts law and DPH Circular DCP 21-10-111, which conclusion is BEST?",
    "choices": [
      {
        "text": "The pharmacist may dispense without independently obtaining proof of the NP's independent-practice status solely because the supervisor's name is absent, while continuing ordinary validity and patient-safety checks.",
        "why": "Correct. M.G.L. c.112 §80E permits independent prescriptive practice after the relevant experience and authorization. 105 CMR 721.020(E) requires a supervisor name for certain nurse prescribers UNLESS they have independent authority; Circular DCP 21-10-111 says a pharmacist is NOT required to verify that status solely because the name is missing on an otherwise valid prescription."
      },
      {
        "text": "The pharmacist must always reject any NP-controlled prescription that lacks a supervising physician's name, even when the NP has valid independent prescriptive authority.",
        "why": "Incorrect. Massachusetts explicitly exempts independently authorized NPs from the supervising-professional-name requirement. A blanket rejection would ignore 105 CMR 721.020(E), M.G.L. c.112 §80E and DPH's pharmacist-specific clarification."
      },
      {
        "text": "The pharmacist must contact the NP's former supervising physician to authorize this prescription, because two years of supervised experience never permits independent Schedule IV prescriptive practice.",
        "why": "Incorrect. M.G.L. c.112 §80E provides an independent-practice pathway after the required supervised experience and authorization. Under the facts stated, there is no current supervising physician from whom patient-specific permission is required."
      },
      {
        "text": "The pharmacist may fill this Schedule IV order only if the NP substitutes a supervising physician's DEA number, because nurse practitioners may hold MCSRs but not their own DEA registrations.",
        "why": "Incorrect. Properly authorized nurse practitioners may hold their own appropriate MCSR and DEA registrations for federally controlled drugs. Using another practitioner's DEA number would not cure a problem and contradicts the NP's individual registration."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.112 §80E; 105 CMR 721.020(E); DPH Circular DCP 21-10-111 (supervised versus independent prescribers); MA Board of Nursing APRN prescriptive-authority guidance",
    "url": "https://www.mass.gov/circular-letter/circular-letter-dcp-21-10-111-out-of-state-schedule-ii-prescriptions-and-supervised-prescribing-2",
    "verified": "2026-11-16",
    "note": "Independent NP prescribers need no supervisor's name on the Rx. An otherwise valid prescription does not become automatically invalid because that field is absent, and a pharmacist need not separately prove independent status for that reason alone."
  },
  {
    "id": "E30-099",
    "set": 20,
    "area": 3,
    "kind": "multi",
    "topic": "Codeine dosage forms and gabapentin: Federal Schedules II/III/V versus MA Schedule VI",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacist is classifying four products in November 2026. Each named codeine product is a lawfully marketed prescription product in the stated strength; combination products contain their nonnarcotic ingredients in recognized therapeutic quantities. The gabapentin product is conventional prescription-only oral gabapentin. Under current federal DEA schedules and Massachusetts 105 CMR 700.002 and PMP rules, which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A single-ingredient codeine sulfate 30-mg oral tablet is a Schedule II controlled substance, rather than a Schedule III product solely because its unit dose is below 90 mg.",
        "why": "Correct. Codeine alone is generally Schedule II under 21 CFR 1308.12. The Schedule III allowance for codeine doses up to 90 mg per unit requires a qualifying COMBINATION with recognized nonnarcotic active ingredient(s), which the single-ingredient tablet lacks. 105 CMR 700.002 incorporates the federal schedule."
      },
      {
        "text": "An acetaminophen 300 mg/codeine 30 mg oral tablet is Schedule II merely because codeine appears in its ingredient list, so the qualifying combination-drug rules do not apply.",
        "why": "Incorrect. Under 21 CFR 1308.13 and DEA's classification guidance, a qualifying codeine 30 mg/acetaminophen 300 mg combination meets Schedule III requirements (no more than 90 mg codeine per dosage unit with a recognized therapeutic nonnarcotic ingredient). Massachusetts 105 CMR 700.002 generally tracks this federal Schedule III designation."
      },
      {
        "text": "A promethazine/codeine syrup containing 10 mg of codeine per 5 mL (200 mg per 100 mL) with qualifying nonnarcotic promethazine is Schedule V, not Schedule III solely because it contains codeine.",
        "why": "Correct. The codeine concentration is exactly 200 mg per 100 mL, within the Schedule V ceiling for qualifying codeine combination cough preparations under 21 CFR 1308.15. Under 105 CMR 700.002(E), Massachusetts includes federally Schedule V products in its Schedule V."
      },
      {
        "text": "Prescription gabapentin is NOT a federally scheduled controlled substance, but remains Massachusetts Schedule VI and must be reported to MassPAT under the state's additional-drug reporting rule.",
        "why": "Correct. Gabapentin is not listed as federally controlled in DEA Schedules II–V. Massachusetts 105 CMR 700.002(F) defines unscheduled prescription medicines as Schedule VI, and the DPH PMP reporting guidance specifically includes gabapentin as an additional reportable drug without changing its schedule."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "21 CFR 1308.12(b)(1)(i), 1308.13(e), 1308.15(c)(1); 105 CMR 700.002(B),(C),(E),(F); MA DPH MassPAT pharmacy reporting and data submission",
    "url": "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c",
    "verified": "2026-11-16",
    "note": "Classify the actual product and formulation, not just the ingredient: single-ingredient codeine II; qualifying codeine/APAP III; qualifying low-dose codeine cough product V; gabapentin is MA VI but still PMP-reportable."
  },
  {
    "id": "E30-100",
    "set": 20,
    "area": 4,
    "kind": "single",
    "topic": "USP <797> Category 1: ISO 5 PEC in an SCA, garbing and short refrigerated BUD",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts pharmacy prepares a NONHAZARDOUS Category 1 compounded sterile preparation (CSP) from sterile ingredients in an ISO Class 5 primary engineering control inside an otherwise suitable UNCLASSIFIED segregated compounding area (SCA). Personnel meet applicable USP <797> aseptic training, garbing and environmental requirements; manufacturer stability supports at least 48 hours refrigerated, with no additional shorter limiting factor. Which BUD/facility decision is permitted under the currently applicable USP <797>?",
    "choices": [
      {
        "text": "Assign a 24-hour controlled-room-temperature BUD because ISO Class 5 air quality allows a Category 1 CSP to exceed the usual 12-hour controlled-room-temperature maximum.",
        "why": "Incorrect. ISO Class 5 PECs are required for Category 1 sterile compounding but do not independently extend the Category 1 beyond-use limit. Under USP <797>, Category 1 CSPs are limited to no more than 12 hours at controlled room temperature or 24 hours refrigerated, assuming no shorter restriction."
      },
      {
        "text": "Assign a BUD no longer than 24 hours when refrigerated (or 12 hours at controlled room temperature), using the ISO Class 5 PEC in the SCA and the same minimum compounding-garb requirements applicable to Category 2.",
        "why": "Correct. USP <797> §§3–4, 14 permits Category 1 compounding in an ISO Class 5 PEC within a qualifying unclassified SCA. The current Category 1 BUD ceilings are 12 hours at controlled room temperature and 24 hours refrigerated. USP's December 2023 official FAQ explains that minimum garbing, including sterile gloves, is not relaxed merely because the PEC is in an SCA."
      },
      {
        "text": "Assign the Category 2 four-day controlled-room-temperature BUD in the same SCA merely by performing extra sterility testing, without relocating the ISO Class 5 PEC to a compliant cleanroom suite.",
        "why": "Incorrect. Category 2 CSPs require the applicable cleanroom suite and other Category 2 controls under USP <797>; a Category 1 SCA is not automatically upgraded into a Category 2 compounding environment through supplemental testing."
      },
      {
        "text": "Assign a 48-hour refrigerated BUD because the ingredients are sterile and the manufacturer supports at least 48 hours of chemical stability, regardless of Category 1's microbiological limits.",
        "why": "Incorrect. Chemical stability data do not override USP <797>'s Category 1 microbiological BUD ceilings. When using Category 1 conditions, the shorter Category 1 limit remains controlling even if physical or chemical stability extends beyond it."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "USP <797> §§3–4, 14 (Category 1 CSP environment and BUD limits); USP <797> Official FAQs (Dec. 11, 2023), Questions 31, 74 and 93; 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
    "verified": "2026-11-16",
    "note": "Category 1 may use an ISO Class 5 PEC in a suitable unclassified SCA, but garbing stays rigorous and BUD remains ≤12 h room temperature or ≤24 h refrigerated. Manufacturer chemical stability is not permission for a longer BUD."
  },
  {
    "id": "E30-101",
    "set": 21,
    "area": 1,
    "kind": "single",
    "topic": "Emergency pharmacist-license suspension: affidavit evidence and seven-day necessity hearing",
    "topicKey": "board-discipline",
    "stem": "The Massachusetts Board obtains sworn affidavits and dispensing records indicating that a licensed pharmacist presents an immediate or serious threat to public safety. The allegations have not yet been adjudicated at a final merits hearing. Under 247 CMR 10.07, which action is authorized?",
    "choices": [
      {
        "text": "The Board may issue an advisory letter but cannot suspend the pharmacist's license until a final merits hearing or a criminal conviction.",
        "why": "Incorrect. An advisory letter is a different, non-disciplinary response under 247 CMR 10.06(2). Section 10.07 specifically permits a prehearing suspension or refusal to renew when affidavits or other documentary evidence establish an immediate or serious public threat; a criminal conviction is not a universal prerequisite."
      },
      {
        "text": "The Board may suspend or refuse to renew the license pending the final merits hearing, but must afford a hearing on the necessity of that summary action within seven days of its action.",
        "why": "Correct. Section 10.07 allows temporary summary action based on affidavits or other documentary evidence of an immediate or serious threat to public health, safety, or welfare. A separate hearing focused on whether the summary action is needed must be afforded within seven days, even though the full merits hearing may occur later."
      },
      {
        "text": "The Board may suspend the license before a merits hearing, but the pharmacist is entitled to no hearing about that suspension until the final allegations are resolved.",
        "why": "Incorrect. Although summary action may precede a final merits adjudication, 247 CMR 10.07 expressly guarantees a prompt, limited hearing about its necessity within seven days of the Board's action. A later full hearing does not substitute for the limited summary-action hearing."
      },
      {
        "text": "A Board cease-and-desist notice is the only possible immediate remedy; license suspension or refusal to renew is reserved for matters already finally adjudicated.",
        "why": "Incorrect. Summary cease-and-desist and quarantine notices are distinct enforcement tools under 247 CMR 10.06(8)–(9), but 10.07 separately permits a license suspension or refusal to renew before the final merits hearing when the stated threat and evidence standards are met."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 10.07 (Suspension Prior to Hearing, effective Jan. 9, 2025); contrast 247 CMR 10.06(2),(8)–(9)",
    "url": "https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download",
    "verified": "2026-11-16",
    "note": "Distinguish a prehearing summary suspension from the final merits proceeding. A limited necessity hearing is due within seven days; there is no automatic requirement to await a criminal conviction."
  },
  {
    "id": "E30-102",
    "set": 21,
    "area": 2,
    "kind": "single",
    "topic": "Dentist's Schedule II–IV authority: dental purpose, personal use and nonemergency immediate-family restriction",
    "topicKey": "prescriber-authority",
    "stem": "A Massachusetts dentist holds a valid license, MCSR and applicable DEA registration. Assume each proposed prescription meets all other state and federal requirements, including ePrescribing and opioid limits. Which prescription is within the dentist's authority under 234 CMR 5.06?",
    "choices": [
      {
        "text": "Schedule II oxycodone for the dentist's spouse after an elective dental procedure, when no emergency exists.",
        "why": "Incorrect. Although treating genuine dental pain can be within the practice of dentistry, 234 CMR 5.06(3) separately prohibits a dentist from prescribing Schedule II substances to immediate family, including a spouse, except in an emergency. The scenario expressly states that no emergency exists."
      },
      {
        "text": "Schedule IV zolpidem to an unrelated patient for chronic insomnia that has no connection to dental treatment.",
        "why": "Incorrect. The patient is unrelated, but 234 CMR 5.06(2) limits controlled-substance prescribing by dentists to legitimate DENTAL purposes in the ordinary course of professional practice. An unrelated chronic sleep disorder does not become a dental indication simply because the prescriber has a DEA registration."
      },
      {
        "text": "A properly limited Schedule II oxycodone prescription for an unrelated patient with acute postoperative pain following an extraction performed by the dentist.",
        "why": "Correct. Under 234 CMR 5.06(1)–(2), a properly registered dentist may prescribe controlled substances for legitimate dental purposes in the usual course of practice. Appropriate acute post-extraction pain in an unrelated patient meets the scope condition on the stipulated facts, unlike self-use, a nonemergency immediate-family Schedule II prescription, or unrelated disease management."
      },
      {
        "text": "Schedule III acetaminophen/codeine for the dentist's own recurring tension headaches because the dentist can independently confirm the diagnosis.",
        "why": "Incorrect. Section 5.06(2) explicitly prohibits a dentist from prescribing Schedule II–IV controlled substances for PERSONAL use, regardless of professional expertise or a self-diagnosis. Chronic tension headaches unrelated to dental care also fall outside the stated dental-purpose limitation."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "234 CMR 5.06(1)–(3); M.G.L. c.94C §§7, 9 and 18 (otherwise valid practitioner prescribing)",
    "url": "https://www.mass.gov/files/documents/2017/10/06/234cmr5.pdf",
    "verified": "2026-11-16",
    "note": "DEA registration alone does not grant unlimited prescribing scope: dentists prescribe for legitimate dental purposes, cannot prescribe Schedule II–IV for self-use, and generally cannot prescribe Schedule II to immediate family absent an emergency."
  },
  {
    "id": "E30-103",
    "set": 21,
    "area": 2,
    "kind": "multi",
    "topic": "FDA Medication Guides: refill delivery, patient-agent pickup and prescriber no-guide direction",
    "topicKey": "medication-guides",
    "stem": "A Massachusetts community pharmacy dispenses two separate FDA-approved outpatient prescriptions for which a Medication Guide is required under 21 CFR Part 208. One is an ordinary refill collected by a patient's agent. For the other, the practitioner has directed that the Medication Guide not be provided because of significant concerns about its effect, but the patient explicitly requests the Guide at dispensing. No other FDA exemption applies. Which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Because the manufacturer is responsible for supplying Medication Guides to distributors, the dispensing pharmacy has no independent obligation to provide one to a patient or agent.",
        "why": "Incorrect. Manufacturer and wholesaler supply duties under 21 CFR 208.24(b)–(c) exist alongside the DISPENSER'S separate duty under 208.24(e) to provide a Medication Guide when a covered prescription drug is dispensed to a patient or agent. Availability from the manufacturer does not remove the pharmacy's delivery obligation."
      },
      {
        "text": "For the refill collected by the patient's agent, the dispenser must provide the Medication Guide directly to that agent, unless a valid exemption applies.",
        "why": "Correct. Under 21 CFR 208.24(e), the Medication Guide is furnished when a covered product is dispensed to a patient OR the patient's agent. The rule does not provide a routine refill exception merely because an earlier supply was accompanied by a Guide; the scenario excludes other exemptions."
      },
      {
        "text": "A Medication Guide furnished at the first fill automatically satisfies all later outpatient refills of the same product, so no Guide is needed at subsequent dispensings.",
        "why": "Incorrect. Section 208.24(e) links the dispensing duty to the current dispensing event, not only to the first fill. Without a regulatory exemption or qualifying patient-specific direction, a previous handout does not eliminate the duty at the next refill."
      },
      {
        "text": "Despite the practitioner's direction not to provide the Guide, the dispenser must provide it when the patient affirmatively requests the information at dispensing.",
        "why": "Correct. Under 21 CFR 208.26(b), the prescriber may direct withholding for a particular patient when significant concerns warrant it, BUT the authorized dispenser SHALL furnish the Medication Guide to any patient who requests the information when the drug is dispensed, notwithstanding that direction."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "21 CFR 208.24(b)–(e) and 208.26(b) (FDA Medication Guide requirements in force November 2026); proposed Patient Medication Information rule not yet effective",
    "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-208/subpart-B/section-208.24",
    "verified": "2026-11-16",
    "note": "Separate manufacturer supply duties from dispenser duties. A Guide is normally furnished at each applicable outpatient dispensing, including a refill or pickup by an agent; a patient's request overrides a prescriber's patient-specific no-guide direction."
  },
  {
    "id": "E30-104",
    "set": 21,
    "area": 3,
    "kind": "single",
    "topic": "Dronabinol formulation-specific schedules: FDA-approved sesame-oil softgel versus oral solution",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacist receives otherwise valid prescriptions for (X) FDA-approved synthetic dronabinol in sesame oil encapsulated as a soft-gel capsule and (Y) FDA-approved dronabinol oral solution. Neither is a different cannabinoid formulation or an unapproved cannabis product. Which federal AND Massachusetts schedule classification and refill consequence is correct?",
    "choices": [
      {
        "text": "X is Schedule II and cannot be refilled; Y is Schedule III and may have otherwise valid authorized refills.",
        "why": "Incorrect. The schedules are reversed: the FDA-approved synthetic dronabinol sesame-oil soft-gel formulation is specifically in federal Schedule III under 21 CFR 1308.13(g)(1), while the FDA-approved dronabinol oral solution is federal Schedule II under 1308.12(f)(2). Massachusetts 105 CMR 700.002 incorporates those listings."
      },
      {
        "text": "Both are Schedule III, because one active ingredient necessarily carries one DEA schedule across all FDA-approved formulations.",
        "why": "Incorrect. Federal law schedules these precise FDA-approved preparations in DIFFERENT subsections. The capsules are Schedule III, but the oral solution is Schedule II. Classifying only by active ingredient and ignoring dosage form would produce an invalid dispensing/refill decision."
      },
      {
        "text": "Both are Schedule II, because the active ingredient is related to tetrahydrocannabinol and no FDA-approved preparation is eligible for Schedule III.",
        "why": "Incorrect. 21 CFR 1308.13(g)(1) explicitly names the FDA-approved synthetic dronabinol in sesame oil and a soft-gel capsule as Schedule III, even though the approved oral solution is Schedule II under 1308.12(f)(2)."
      },
      {
        "text": "X is Schedule III and can have otherwise lawful authorized refills; Y is Schedule II and cannot be refilled under the original prescription.",
        "why": "Correct. DEA regulations separately list the FDA-approved sesame-oil soft-gel capsule as Schedule III and the approved dronabinol oral solution as Schedule II. Massachusetts follows the corresponding federal Schedules II and III under 105 CMR 700.002(B)–(C). Under 21 CFR 1306.12(a), Schedule II prescriptions cannot be refilled; Schedule III may be refilled if properly authorized within applicable limits."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1308.12(f)(2), 1308.13(g)(1), 1306.12(a); 105 CMR 700.002(B)–(C); DEA Controlled Substances—Alphabetical Order (updated Nov. 12, 2026)",
    "url": "https://www.deadiversion.usdoj.gov/schedules/orangebook/c_cs_alpha.pdf",
    "verified": "2026-11-16",
    "note": "Two FDA-approved dosage forms of dronabinol have distinct federal and Massachusetts schedules: sesame-oil soft-gel capsule III versus oral solution II. Refills differ accordingly."
  },
  {
    "id": "E30-105",
    "set": 21,
    "area": 4,
    "kind": "multi",
    "topic": "USP <800> receiving: antineoplastic HD unpacking location, chemotherapy gloves and packaging recommendations",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts institutional pharmacy receives intact external shipping cartons containing NIOSH Table 1 antineoplastic hazardous drugs. It has a designated neutral-pressure receiving zone within an existing room and a positive-pressure ISO 7 sterile compounding room. Appropriate receiving procedures and a trained staff are available. Under USP <800> receiving requirements and USP's January 2026 FAQs, which actions or conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Unpack the external shipping cartons in the designated neutral-pressure receiving zone within the existing room; a separate dedicated room is not required solely for this function.",
        "why": "Correct. USP <800> §5.1 and the January 2026 USP FAQ #71 require unpacking NIOSH Table 1 antineoplastics in neutral/normal- or negative-pressure areas relative to surroundings. USP states that a designated area WITHIN an existing room is acceptable and a separate room is not mandatory."
      },
      {
        "text": "Unpack the cartons in the positive-pressure ISO 7 sterile compounding room because the classified environment provides superior protection from external contamination.",
        "why": "Incorrect. USP <800> §5.1 expressly prohibits unpacking antineoplastic HDs from external shipping containers in sterile compounding areas or positive-pressure areas. ISO classification and product protection do not override the occupational contamination-control requirement."
      },
      {
        "text": "Personnel unpacking the Table 1 antineoplastic HD cartons must wear at least one pair of chemotherapy gloves tested to ASTM D6978.",
        "why": "Correct. USP <800> §10 and official USP FAQ #68 require at least one pair of ASTM D6978-tested chemotherapy gloves when unpacking NIOSH Table 1 antineoplastic HDs. Additional PPE should be determined by facility policy and the risk associated with intact or damaged packages."
      },
      {
        "text": "Reject every shipment lacking an impervious plastic outer bag because USP <800> mandates that all suppliers ship HDs inside impervious plastic.",
        "why": "Incorrect. USP's January 2026 FAQ #69 describes impervious-plastic shipping as RECOMMENDED for suppliers, not an absolute mandatory packaging requirement. A pharmacy must still use safe receiving procedures and evaluate the condition and containment of the shipment."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "USP <800> §§5.1,10 (receiving and PPE); USP <800> Official FAQs updated Jan. 21, 2026, Questions 68–71 (technical support, not formal interpretation); 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_800_FAQs_January2026.pdf?version=0",
    "verified": "2026-11-16",
    "note": "Unpack antineoplastic HDs in a neutral/negative-pressure area, not a sterile or positive-pressure room; wear chemotherapy gloves meeting ASTM D6978. USP recommends supplier impervious-plastic packaging but does not require it in every shipment."
  },
  {
    "id": "E30-106",
    "set": 22,
    "area": 1,
    "kind": "single",
    "topic": "Practicing while impaired and discretionary URAMP license outcomes",
    "topicKey": "board-discipline",
    "stem": "A Massachusetts pharmacist is unable to perform final prescription checks safely due to sedation from a legally prescribed medication. No patient has been harmed. An impairment-related Board complaint is pending, and the pharmacist applies to the Unified Recovery and Monitoring Program (URAMP). Which statement accurately describes Massachusetts law?",
    "choices": [
      {
        "text": "The pharmacist cannot be disciplined without proof of a patient injury because the sedating drug was lawfully prescribed.",
        "why": "Incorrect. 247 CMR 10.03(1)(g) lists practicing while impaired by medication, illness, or another condition as a ground for discipline. A lawful prescription and lack of a known error do not eliminate unsafe impairment. The pharmacist should stop unsafe professional tasks."
      },
      {
        "text": "Impaired practice may warrant discipline; after URAMP admission, the Board may dismiss a related complaint or impose non-disciplinary license conditions.",
        "why": "Correct. Under 247 CMR 10.03(1)(g), actual impaired professional practice is a possible disciplinary ground even if the medication was legally obtained. M.G.L. c.112 §65G(g) authorizes, but does not require, the Board to dismiss related pending matters after URAMP admission; non-disciplinary license conditions may remain."
      },
      {
        "text": "The pharmacist can be admitted to URAMP only after a final formal disciplinary hearing has resolved the pending complaint.",
        "why": "Incorrect. Section 65G(f)–(g) expressly provides for applicants or Board referrals and addresses pending complaints upon admission. A final adjudicatory finding is not required before a pharmacist seeks appropriate recovery monitoring."
      },
      {
        "text": "Submitting a URAMP application automatically dismisses the pending complaint and guarantees unrestricted pharmacist practice.",
        "why": "Incorrect. The statutory discretion arises on admission, not submission of an application, and the Board MAY, rather than MUST, dismiss a related complaint. Section 65G(g) also permits public non-disciplinary restrictions or conditions during monitoring."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 10.03(1)(g) (eff. Jan. 9, 2025); M.G.L. c.112 §65G(f)–(g); Massachusetts DPH URAMP Frequently Asked Questions",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section65G",
    "verified": "2026-11-16",
    "note": "Legal use of medication does not excuse impaired pharmacy practice. URAMP admission may offer non-disciplinary monitoring, but dismissal of a related complaint is discretionary."
  },
  {
    "id": "E30-107",
    "set": 22,
    "area": 2,
    "kind": "single",
    "topic": "Podiatrist Schedule II prescriptions within foot and ankle scope",
    "topicKey": "prescriber-authority",
    "stem": "An actively licensed Massachusetts podiatrist has a personal DEA registration and Massachusetts Controlled Substances Registration. The podiatrist writes two otherwise valid Schedule II prescriptions: one for brief postoperative pain after performing foot surgery, and another to treat an unrelated migraine with no connection to any foot or ankle condition. Assume legitimate patient relationships and compliance with all other opioid and electronic-prescribing requirements. Which assessment is correct?",
    "choices": [
      {
        "text": "Both prescriptions are within scope because DEA and Massachusetts registrations allow the podiatrist to prescribe for any medical diagnosis.",
        "why": "Incorrect. Prescribing registrations are necessary for covered controlled drugs but do not enlarge the podiatrist's authorized clinical scope. Under 249 CMR 4.01–4.02 and 21 CFR 1306.04(a), prescriptions must arise from legitimate medical purpose within lawful professional practice."
      },
      {
        "text": "Neither is within scope because Massachusetts excludes podiatrists from prescribing any Schedule II medications.",
        "why": "Incorrect. 249 CMR 4.02 expressly permits reasonable prescription and controlled substances in podiatric practice; it does not impose a blanket Schedule II prohibition. Appropriate postoperative foot pain is a podiatric indication."
      },
      {
        "text": "Only the migraine prescription is valid because podiatrists may make systemic diagnoses but cannot prescribe for postoperative foot pain.",
        "why": "Incorrect. Podiatrists may assess systemic problems affecting the foot but do not thereby acquire unlimited authority to treat unrelated migraine. Foot-surgery pain is connected to the practitioner's authorized podiatric treatment."
      },
      {
        "text": "The postoperative foot-pain prescription can be within the podiatrist's authority, but the unrelated migraine prescription exceeds that professional scope.",
        "why": "Correct. Under 249 CMR 4.01–4.02, a properly registered podiatrist may prescribe reasonable controlled medication, including Schedule II, within podiatric practice. The unrelated migraine is outside that scope. The pharmacist should verify authority and not dispense a prescription solely because DEA/MCSR numbers are valid."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "249 CMR 4.01–4.02 (eff. Oct. 14, 2022); M.G.L. c.94C §§9,18(a); 247 CMR 9.15(2); 21 CFR 1306.04(a)",
    "url": "https://www.mass.gov/regulations/249-CMR-400-practice-of-podiatric-medicine",
    "verified": "2026-11-16",
    "note": "A podiatrist may prescribe Schedule II controlled substances for care within podiatric scope; DEA/MCSR registration does not authorize unrelated general medical treatment."
  },
  {
    "id": "E30-108",
    "set": 22,
    "area": 2,
    "kind": "multi",
    "topic": "FD&C Act adulteration versus misbranding: insanitary holding, low potency and false labeling",
    "topicKey": "drug-integrity",
    "stem": "A Massachusetts pharmacy evaluates a supplier's quality alert. Lot X was held in insanitary conditions where contamination could occur, though cultures are negative. Compendial lot Y tests materially below its represented strength without an accurately labeled exception. Lot Z has materially false strength information on the label. No patient injury or FDA recall has been reported. Which conclusions are supported by the Federal Food, Drug, and Cosmetic Act? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Lot X may be adulterated even though no finished unit has cultured positive for contamination.",
        "why": "Correct. 21 U.S.C. §351(a)(2)(A) covers drugs held under insanitary conditions WHEREBY they MAY have been contaminated or rendered injurious. A positive test or actual patient injury is not required. The pharmacy should not return a questionable lot to dispensable inventory without resolving the hazard."
      },
      {
        "text": "Lot Y cannot be adulterated as long as its container is sealed and the manufacturer intended to meet the labeled strength.",
        "why": "Incorrect. Under 21 U.S.C. §351(b), a compendial drug with strength different from the compendial standard is adulterated absent an applicable plainly labeled difference. The stem excludes such disclosure; an intact seal and a claim of intended potency do not cure a subpotent lot."
      },
      {
        "text": "Lot Z may be misbranded because a materially false label claim is misleading even without proof that a patient was harmed.",
        "why": "Correct. 21 U.S.C. §352(a)(1) defines a drug as misbranded when labeling is false or misleading in any particular. Patient harm, a broken seal, or a formal FDA recall is not a necessary element of the violation."
      },
      {
        "text": "The pharmacy may dispense the lots normally until FDA formally orders a recall, because adulteration and misbranding have no effect before then.",
        "why": "Incorrect. 21 U.S.C. §§351–352 define adulteration/misbranding independently of a recall, and federal prohibitions under §331 apply to unlawful distribution and acts affecting products held for sale. Pharmacies must evaluate and segregate unsafe stock rather than assume it may be dispensed until a recall notice."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 U.S.C. §§351(a)(2)(A),351(b),352(a)(1),331(a),(k); 247 CMR 9.01 (pharmacy safety duties)",
    "url": "https://uscode.house.gov/us/usc/t21/s351/",
    "verified": "2026-11-16",
    "note": "Insanitary holding can mean adulteration without proven contamination; material false labeling can mean misbranding without injury. Subpotency can independently make a compendial drug adulterated."
  },
  {
    "id": "E30-109",
    "set": 22,
    "area": 3,
    "kind": "single",
    "topic": "Required Schedule II opioid partial-fill statement omitted from an otherwise valid e-prescription",
    "topicKey": "rx-amendments",
    "stem": "A Massachusetts community pharmacy receives an otherwise complete and authentic electronic prescription for oxycodone (Schedule II). It lacks the mandatory statement that the patient may request a partial fill. The patient presently wants the full quantity, and the pharmacist can reach the prescriber or the prescriber's authorized agent. What should the pharmacist do under Massachusetts law and DPH guidance?",
    "choices": [
      {
        "text": "Confirm the missing statement with the prescriber or authorized agent and document the notation on the prescription in writing or electronically.",
        "why": "Correct. M.G.L. c.94C §22(c) and 105 CMR 721.020(D)(7) require that notation on Schedule II opioid prescriptions regardless of whether a partial fill is sought. Massachusetts DPH specifically directs pharmacist contact with the prescriber or authorized agent and written/electronic documentation of the confirmed notation."
      },
      {
        "text": "Dispense without a notation because the statutory statement is required only when a patient actually requests a partial fill.",
        "why": "Incorrect. M.G.L. c.94C §22(c) applies to any Schedule II opioid prescription. The patient's request for the full quantity does not make the missing notation optional. Obtain confirmation and document it."
      },
      {
        "text": "Add the standard partial-fill language through a pharmacy technician without any prescriber or authorized-agent confirmation.",
        "why": "Incorrect. DPH's clarification does not authorize the pharmacy to fabricate the omitted prescriber statement unilaterally. The pharmacist must contact the prescriber or authorized agent for confirmation before recording the missing notation."
      },
      {
        "text": "Reject the electronic prescription and require a new one because confirmation and documentation of that omission are always forbidden.",
        "why": "Incorrect. DPH expressly provides the confirmation-and-documentation procedure for this particular omission on an otherwise lawful prescription. Another genuinely invalid aspect might require a new prescription, but this specific omission does not automatically do so."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.94C §22(c) (partial-fill opioid notice); 105 CMR 721.020(D)(7) and 721.055 (effective Sept. 27, 2024); Massachusetts DPH Circular DCP 18-10-104 (Nov. 1, 2018) expressly superseding outdated DCP 16-12-665, pp.1–2",
    "url": "https://www.mass.gov/doc/circular-letter-dcp-18-10-104-patient-requests-for-partial-fill-of-schedule-ii-prescriptions-0/download",
    "verified": "2026-11-17",
    "note": "DCP 18-10-104 explicitly instructs: if an opioid Schedule II prescription lacks the required patient-request partial-fill notice, the pharmacist MUST contact the prescriber or authorized agent to confirm and then document it. The earlier 2016 remainder-void circular was superseded; a lawful patient-requested balance may be supplied at the ORIGINAL pharmacy within 30 days."
  },
  {
    "id": "E30-110",
    "set": 22,
    "area": 4,
    "kind": "multi",
    "topic": "Failed home delivery, cold-chain excursion, and controlled-substance shipping procedures",
    "topicKey": "medication-delivery-shipping",
    "stem": "A Massachusetts pharmacy sends prescriptions to patients using a common carrier. A refrigerated noncontrolled biologic comes back unopened after a failed delivery; its temperature logger shows an excursion outside the labeled range, and no product-specific stability assessment has been obtained. The pharmacy also sends Schedule III prescriptions through the carrier. Which conclusions comply with 247 CMR 9.02 and medication-integrity duties? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The returned biologic may be immediately resent, because an intact package seal establishes stability despite the logged temperature excursion.",
        "why": "Incorrect. A sealed container does not establish product stability after exposure outside the labeled storage range. Under 247 CMR 9.02(2), the pharmacy must ensure transport does not adversely affect integrity or stability. The unresolved excursion requires evaluation before redelivery."
      },
      {
        "text": "Common-carrier dispensing is permitted, but the pharmacy must ensure that packing, shipping and transportation do not undermine medication stability.",
        "why": "Correct. 247 CMR 9.02(1) allows mail/common-carrier dispensing consistent with applicable law. Section 9.02(2) makes preservation of drug integrity and stability a pharmacy responsibility, not exclusively the carrier's."
      },
      {
        "text": "Every logged temperature excursion mandates immediate destruction under 247 CMR 9.02, even if reliable product-specific stability data support use.",
        "why": "Incorrect. Section 9.02 does not set a universal automatic-discard threshold. A specific medicine's labeled conditions, temperature history, and scientifically supported stability assessment determine whether it remains suitable; absent such support, keep it from dispensing."
      },
      {
        "text": "The biologic should be held pending a supported stability determination, and the pharmacy must maintain its own policies for transporting and delivering controlled substances.",
        "why": "Correct. Redelivery before resolving the excursion would not satisfy the pharmacy's §9.02(2) integrity responsibility. Section 9.02(3) separately requires pharmacy policies and procedures for packing, shipping, transportation and delivery of controlled substances, even when a commercial carrier is used."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 9.02(1)–(3) (Prescriptions by Mail; eff. Dec. 6, 2024); 247 CMR 9.01; relevant manufacturer-labeled storage and product-specific stability data",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A commercial carrier does not shift drug-integrity responsibility away from the pharmacy. Evaluate unresolved cold-chain excursions before redelivery and maintain procedures specific to controlled-substance shipping."
  },
  {
    "id": "E30-111",
    "set": 23,
    "area": 1,
    "kind": "single",
    "topicKey": "technician-scope",
    "topic": "Underage pharmacy technician trainee: one-year/1,500-hour exemption and age-18 application",
    "stem": "A Massachusetts-licensed pharmacy technician trainee started employment at age 16, has worked 1,620 cumulative trainee hours in 15 months, and is still 17. The Board has not granted an extension. The trainee turns 18 next week. Under 247 CMR 8.03(5), which statement is accurate?",
    "choices": [
      {
        "text": "Because the trainee is not yet 18, the hours/one-year employment cap has an exception; a technician-license application must be submitted within 30 days of turning 18.",
        "why": "Correct. 247 CMR 8.03(5)(b) expressly excepts a person who has not yet reached age 18 from the earlier of one year or 1,500 hours. A person who exceeded either threshold before turning 18 must submit an application for a pharmacy technician license within 30 days of the eighteenth birthday. The pharmacy should plan the timely application and verify continuing lawful licensure."
      },
      {
        "text": "The trainee's license automatically ends at the 1,500th hour, even while age 17; a Board extension is the only possible exception.",
        "why": "Incorrect. The regulation lists alternative exceptions, including the person not yet having reached age 18. A Board extension is not the sole exception; the pharmacy must still follow the post-eighteenth-birthday application requirement."
      },
      {
        "text": "The trainee can continue indefinitely under the trainee license after turning 18 because the excess hours were accrued before the birthday.",
        "why": "Incorrect. The under-18 exception does not permanently remove the ordinary employment limitation. Section 8.03(5) specifically requires the person who previously exceeded the limit to apply for a technician license within 30 days of turning 18."
      },
      {
        "text": "The trainee must immediately obtain a pharmacist-intern license on the eighteenth birthday, because technician applicants are not eligible until age 21.",
        "why": "Incorrect. Section 8.02(3)(a) generally sets 18 as the age for pharmacy technician licensure; pharmacy intern licensure is a different educational pathway under §8.01. The required application here is for a pharmacy technician license, not a pharmacist-intern license."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 8.03(5)(a)–(c), final sentence; 247 CMR 8.02(3)(a) (Board corrected text Apr. 25, 2025; effective 2018)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-16",
    "note": "The under-18 exception can extend trainee employment beyond one year or 1,500 hours, but a trainee who already exceeded the cap must apply for a technician license within 30 days after turning 18."
  },
  {
    "id": "E30-112",
    "set": 23,
    "area": 2,
    "kind": "single",
    "topicKey": "institutional-pharmacy-practice",
    "topic": "Clinic pharmacy dispensing: current clinic patients/employee health versus outside retail prescriptions",
    "stem": "A Massachusetts licensed clinic maintains a clinic pharmacy that is not registered as a retail drug business. It has no pharmacy-services authorization on the facility license and no separate M.G.L. c.94C §9(e) authorization to dispense take-home controlled substances. A clinic practitioner legally authorized to prescribe issues several orders. Which proposed dispensing fits 105 CMR 722.091?",
    "choices": [
      {
        "text": "Fill a take-home Schedule III prescription for a clinic employee because an employee health benefit overrides the facility-license requirement.",
        "why": "Incorrect. Although §722.091(A) permits lawful prescriptions for clinic employees under employee health policies, §722.091(B) separately prohibits dispensing controlled substances other than for immediate administration unless the facility has the specified pharmacy-services licensing or §9(e) authorization."
      },
      {
        "text": "Fill an otherwise lawful noncontrolled prescription for a current clinic employee pursuant to the clinic's employee health policy.",
        "why": "Correct. Section 722.091(A) expressly allows prescriptions for current clinic patients and employees under employee health policies when issued by a legally authorized clinic practitioner. The case assumes no additional obstacle, and no take-home controlled substance is involved."
      },
      {
        "text": "Fill a noncontrolled prescription for any unrelated walk-in customer who chooses the clinic pharmacy for convenience.",
        "why": "Incorrect. Clinic pharmacies under §722.091(A) are not unrestricted retail pharmacies; dispensing is tied to current clinic patients, employees within the described policies, or medication orders for immediate administration by clinic practitioners."
      },
      {
        "text": "Fill a take-home Schedule IV prescription for anyone on the clinic's payroll because it is less restricted than Schedule II.",
        "why": "Incorrect. Section 722.091(B)'s facility-authorization condition covers controlled substances dispensed for take-home use, not only Schedule II medications. A payroll relationship does not itself supply the missing authorization."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "105 CMR 722.020 (Clinic Pharmacy, Clinic Employee, Clinic Patient); 105 CMR 722.091(A)–(B) (effective Sept. 27, 2024)",
    "url": "https://www.mass.gov/doc/105-cmr-722-dispensing-procedures-for-clinic-and-hospital-pharmacies/download",
    "verified": "2026-11-16",
    "note": "A non-retail clinic pharmacy may supply authorized medication orders or eligible clinic patients/employees; take-home controlled-substance dispensing requires the separate facility authorization in §722.091(B)."
  },
  {
    "id": "E30-113",
    "set": 23,
    "area": 2,
    "kind": "multi",
    "topicKey": "patient-package-inserts",
    "topic": "FDA patient package inserts for contraceptives and estrogen products versus voluntary labeling",
    "stem": "A Massachusetts pharmacy handles FDA-regulated patient labeling. It dispenses outpatient oral contraceptives and prescription estrogen products, plus a third medication whose FDA-approved Patient Information leaflet is voluntary under federal regulations. No acute-care or long-term-care institutional schedule applies. Which statements about Patient Package Inserts (PPIs) are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A required oral-contraceptive PPI must accompany each outpatient package dispensed to the patient or appropriate agent.",
        "why": "Correct. 21 CFR 310.501(a) requires a patient package insert in or accompanying each package of an oral contraceptive drug product supplied to patients or their agents. Providing an insert at only the first fill does not satisfy the ordinary outpatient requirement."
      },
      {
        "text": "An FDA-approved PPI for every prescription medicine is federally required to accompany every refill merely because the manufacturer authored patient information.",
        "why": "Incorrect. FDA states that PPIs for non-estrogen, non-oral-contraceptive drugs may be voluntarily submitted and FDA-approved without the special mandatory distribution rule. The pharmacist must distinguish specific federally required PPIs from voluntary patient labeling and from 21 CFR Part 208 Medication Guides."
      },
      {
        "text": "Prescription estrogen products covered by 21 CFR 310.515 generally require a PPI to accompany dispensing; oral contraceptives with estrogen and progestogen are instead addressed under §310.501.",
        "why": "Correct. Section 310.515(a),(e) requires estrogen product patient inserts and expressly excepts estrogen-progestogen oral contraceptives because §310.501 governs those contraceptives. The practitioner and pharmacist must apply the correct drug-class rule."
      },
      {
        "text": "An outpatient pharmacy may replace each mandatory PPI with a generic verbal counseling offer because written instructions are not required once a pharmacist offers counseling.",
        "why": "Incorrect. Counseling requirements and the federal package-insert mandate serve different purposes. Sections 310.501(a) and 310.515(a) impose patient-facing written labeling obligations not displaced by offering verbal counseling."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 CFR 310.501(a),(b)(2); 21 CFR 310.515(a),(b),(e); FDA Patient Labeling Resources (mandatory versus voluntary PPIs)",
    "url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/patient-labeling-resources",
    "verified": "2026-11-16",
    "note": "Oral contraceptives and covered estrogen products require FDA PPIs at outpatient dispensing. Other FDA-approved patient-information leaflets may be voluntary; PPI mandates are separate from Medication Guides."
  },
  {
    "id": "E30-114",
    "set": 23,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "Brand and generic schedule identification: pregabalin Lyrica versus lisdexamfetamine Vyvanse",
    "stem": "A Massachusetts pharmacist receives valid prescriptions for Lyrica (pregabalin) capsules and Vyvanse (lisdexamfetamine) capsules. Both prescriptions were written by an authorized prescriber for a legitimate purpose. Which statement correctly identifies both federal and Massachusetts schedules and their basic refill implications?",
    "choices": [
      {
        "text": "Lyrica is Schedule IV in both systems and may be refilled within applicable limits; Vyvanse is Schedule II with no refills.",
        "why": "Incorrect. Lisdexamfetamine is Schedule II, but pregabalin is expressly listed in federal Schedule V, not IV, at 21 CFR 1308.15(e)(7). Massachusetts Schedule V follows the applicable Schedule V classification. The pharmacist must use the schedule of the actual molecule, not the broad therapeutic class."
      },
      {
        "text": "Lyrica is Schedule V in both systems and may have properly authorized refills; Vyvanse is Schedule III and may have five refills.",
        "why": "Incorrect. Pregabalin is Schedule V, but lisdexamfetamine is specifically listed in 21 CFR 1308.12(d)(5) as Schedule II. Schedule II prescriptions cannot be refilled under 21 CFR 1306.12(a), regardless of an otherwise routine ADHD treatment."
      },
      {
        "text": "Lyrica is Schedule V in both systems and may have lawfully authorized refills; Vyvanse is Schedule II in both systems and cannot be refilled.",
        "why": "Correct. Pregabalin is in 21 CFR 1308.15(e)(7) and the corresponding Massachusetts Schedule V; lisdexamfetamine is in 21 CFR 1308.12(d)(5) and Massachusetts Schedule II. Valid Schedule V refills are possible within federal/state limits; an original Schedule II prescription may not be refilled."
      },
      {
        "text": "Lyrica is unscheduled federally and only Schedule VI in Massachusetts; Vyvanse is Schedule II in both systems.",
        "why": "Incorrect. This wrongly treats pregabalin like gabapentin. Pregabalin is federally controlled in Schedule V and is classified as Schedule V in Massachusetts, while lisdexamfetamine is Schedule II."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 1308.15(e)(7) (pregabalin), 1308.12(d)(5) (lisdexamfetamine), 1306.12(a); 105 CMR 700.002(B),(E); 21 CFR 1306.22 (Schedule III–V refills)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.15",
    "verified": "2026-11-16",
    "note": "Pregabalin (Lyrica) is a controlled Schedule V drug; lisdexamfetamine (Vyvanse) is Schedule II. Brand name and indication do not determine the schedule by themselves."
  },
  {
    "id": "E30-115",
    "set": 23,
    "area": 4,
    "kind": "multi",
    "topicKey": "nonresident-pharmacy-licensing",
    "topic": "Massachusetts nonresident pharmacy license combinations for shipment of sterile and complex nonsterile compounds",
    "stem": "Three out-of-state pharmacies want to mail prescriptions to Massachusetts residents. Each holds a valid license in its own state and is otherwise compliant. Pharmacy A ships conventional prescription products; B ships compounded sterile preparations; C ships complex nonsterile compounded preparations. Which Massachusetts licensure statements are correct under 247 CMR 6.02? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A nonresident pharmacy shipping prescription controlled substances into Massachusetts must hold the Massachusetts nonresident Drug Store Pharmacy license; its home-state license alone does not replace this requirement.",
        "why": "Correct. 247 CMR 6.02(4) expressly requires a nonresident Drug Store Pharmacy license to dispense or ship controlled substances into Massachusetts. This includes Massachusetts Schedule VI prescription drugs as defined by M.G.L. c.94C; other state licensure alone is not an exemption."
      },
      {
        "text": "Shipping sterile compounded prescriptions into Massachusetts requires both a Massachusetts nonresident Drug Store Pharmacy license and a Massachusetts nonresident sterile compounding pharmacy license.",
        "why": "Correct. Section 6.02(5) expressly requires the combination of those two nonresident licenses before an out-of-state pharmacy dispenses or ships a sterile compounded preparation into Massachusetts."
      },
      {
        "text": "Shipping complex nonsterile compounded prescriptions requires only a nonresident complex nonsterile compounding license; a nonresident Drug Store Pharmacy license is optional.",
        "why": "Incorrect. Section 6.02(6) expressly requires BOTH the nonresident Drug Store Pharmacy license and the nonresident complex nonsterile compounding pharmacy license for that shipment category."
      },
      {
        "text": "A nonresident Drug Store Pharmacy license automatically authorizes shipment of compounded sterile doses without any additional specialty license.",
        "why": "Incorrect. Sections 6.02(4) and (5) separate the baseline nonresident Drug Store Pharmacy license from the distinct nonresident sterile compounding pharmacy authorization. The specialty license is not supplied automatically."
      }
    ],
    "correct": [
      "A",
      "B"
    ],
    "citation": "247 CMR 6.02(4)–(6); 247 CMR 6.09 (nonresident pharmacy applications); M.G.L. c.94C §1 Schedule VI definition (247 CMR 6.00 effective Apr. 25, 2025)",
    "url": "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download",
    "verified": "2026-11-16",
    "note": "Nonresident pharmacies need Massachusetts-specific licenses. Sterile and complex nonsterile compounded shipments each require the general nonresident Drug Store Pharmacy license PLUS the applicable nonresident specialty compounding license."
  },
  {
    "id": "E30-116",
    "set": 24,
    "area": 1,
    "kind": "single",
    "topicKey": "board-reporting",
    "topic": "Individual pharmacist disclosure: an arrest and an out-of-state disciplinary action",
    "stem": "A Massachusetts-licensed pharmacist is arrested in another state for a misdemeanor, before any criminal charge or conviction. In an independent later event, another state's licensing board formally disciplines the pharmacist's professional license. The pharmacist reviews BOTH 247 CMR 20.03 and the grounds for discipline in 247 CMR 10.03. Which reporting approach is BEST supported by the two published regulations?",
    "choices": [
      {
        "text": "Neither event requires a report until the pharmacist has a final criminal conviction in Massachusetts.",
        "why": "Incorrect. 247 CMR 20.03(3) separately requires reporting any arrest, pending charge, or conviction. Out-of-state professional discipline is also reportable under §20.03(4) and can trigger the additional reporting provisions in §10.03."
      },
      {
        "text": "Report the arrest within 14 calendar days under §20.03(3); report the out-of-state disciplinary action within the 14-calendar-day §20.03(4) period AND meet any independently applicable, shorter seven-business-day §10.03(1)(y)-(z) reporting obligation.",
        "why": "Correct. 247 CMR 20.03(3)-(4) expressly provides 14 calendar days for arrests and reportable discipline. Separately, §10.03(1)(y)-(z) lists failure to report qualifying discipline or governmental final actions within seven business days as a possible disciplinary ground. A pharmacist must not assume that the 14-day provision universally overrides this potentially earlier duty; the exact action and deadlines should be assessed together."
      },
      {
        "text": "Defer both reports until the next biennial pharmacist renewal, as §10.03 governs only discipline imposed by the Massachusetts Board itself.",
        "why": "Incorrect. Neither §20.03 nor §10.03 authorizes waiting for renewal, and the §10.03 reporting duties may extend to acts of other licensing authorities."
      },
      {
        "text": "Only the employer reports these individual matters, and seven business days is automatically the sole deadline for both the arrest and the disciplinary action.",
        "why": "Incorrect. §§20.03(3)-(4) address individual licensee duties directly. The separate §10.03 seven-business-day requirement concerns qualifying disciplinary and governmental actions, not a generic seven-day arrest rule. §10.03(1)(aa) also addresses pending charges or convictions on a different clock."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 20.03(3)-(4); 247 CMR 10.03(1)(y)-(aa); Massachusetts Board Mandatory Disclosure Form, revised Dec. 6, 2024; concurrent triggers, not claimed supersession",
    "url": "https://www.mass.gov/doc/247-cmr-20-reporting/download",
    "verified": "2026-11-17",
    "note": "Revision 2 expressly distinguishes the 14-calendar-day §20.03 report from the potentially sooner seven-business-day §10.03(1)(y)-(z) discipline/final governmental action requirements. The Board disclosure form confirms 14 calendar days but does not expressly repeal §10.03. Option B remains correct; never advise that 14 calendar days is automatically sufficient for qualifying reciprocal discipline. §10.03(1)(aa) concerns pending criminal charge/conviction separately.",
    "revision": 2
  },
  {
    "id": "E30-117",
    "set": 24,
    "area": 2,
    "kind": "multi",
    "topicKey": "prescriber-authority",
    "topic": "Hospital DEA registration and unique institutional suffix for otherwise authorized resident prescribers",
    "stem": "A Massachusetts hospital has a current DEA hospital registration. A physician resident is legally authorized under Massachusetts law to prescribe the relevant Schedule II drug, but lacks an individual DEA registration. The hospital has verified the resident's authority and may grant use of its registration. Assume any necessary state controlled-substance registration and ePrescribing rules are separately met. Which federal DEA conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The resident may use the hospital DEA registration while prescribing in the usual course of practice within the resident's hospital employment, if the institution authorizes it and assigns a unique internal suffix.",
        "why": "Correct. 21 CFR 1301.22(c)(1)–(5) allows an individual practitioner who is an agent or employee of a registered hospital to prescribe under the hospital registration if practicing lawfully within employment and the hospital verifies authority, authorizes the use, and assigns a practitioner-specific suffix."
      },
      {
        "text": "The resident may use the hospital's number for unrelated private-office prescriptions because holding hospital privileges is enough, even when acting outside hospital employment.",
        "why": "Incorrect. Section 1301.22(c)(4) confines the exemption to the scope of the individual's employment at the registered hospital/institution. Privileges alone do not authorize using the institutional registration for a private practice."
      },
      {
        "text": "The institution may use one shared suffix for all residents and has no duty to keep a current list connecting suffixes to individual prescribers.",
        "why": "Incorrect. Section 1301.22(c)(5) requires an individual code number for EACH authorized practitioner, and §1301.22(c)(6) requires a CURRENT list identifying each authorized practitioner by code available for verification."
      },
      {
        "text": "The hospital must maintain a current roster connecting unique internal codes to prescribers and make the information available to other registrants or law-enforcement agencies on request.",
        "why": "Correct. This is expressly required by 21 CFR 1301.22(c)(6). The pharmacist receiving such a prescription should verify the specific prescriber's authorization and suffix as appropriate rather than rejecting all institutional identifiers."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "21 CFR 1301.22(c)(1)–(6); DEA Pharmacist's Manual and DEA Medical Resident Guidance; 21 CFR 1306.04(a); applicable 105 CMR 700 and 721 must also be satisfied",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.22",
    "verified": "2026-11-16",
    "note": "Hospital-employed and state-authorized practitioners can use the hospital DEA registration with unique individual suffixes and a current roster, but only within authorized employment and clinical scope."
  },
  {
    "id": "E30-118",
    "set": 24,
    "area": 2,
    "kind": "single",
    "topicKey": "controlled-prescriptions",
    "topic": "Massachusetts prescription formats: multiple drug products on one record in hospital versus other settings",
    "stem": "A practitioner plans to prescribe two different prescription drug products on one record. In one case the prescriptions are issued for community outpatient dispensing; in a separate case they are issued in the hospital setting with clear use and interchange directions for each product. All other requirements are met. Which decision correctly applies 105 CMR 721.050?",
    "choices": [
      {
        "text": "Both records are valid solely because the practitioner clearly separates the drug names and dosing directions.",
        "why": "Incorrect. Section 721.050 ordinarily directs practitioners prescribing more than one drug product to place EACH prescription on a separate form or record. Clarity alone does not authorize combining community prescriptions under the hospital exception."
      },
      {
        "text": "Neither record is permitted because Massachusetts never allows more than one drug product on a prescription form or record.",
        "why": "Incorrect. Section 721.050 explicitly allows more than one drug product in the hospital setting on a single form or record if clear directions for each drug's use and interchange are provided."
      },
      {
        "text": "Separate records are required for the ordinary outpatient case; the hospital record may include multiple drug products if each has clear directions for use and interchange.",
        "why": "Correct. 105 CMR 721.050 generally requires separate forms or records per drug product, but provides a narrow hospital-setting exception with clear instructions for EACH product. The pharmacist should verify the applicable setting and readable product-specific directions."
      },
      {
        "text": "The separate-record requirement applies only to Schedule II drugs; ordinary Schedule VI prescriptions may always be combined at community pharmacies.",
        "why": "Incorrect. Section 721.050 uses the broader phrase 'more than one Drug Product' and does not confine its separate-record rule to Schedule II drugs or exempt ordinary Schedule VI community prescriptions."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "105 CMR 721.050 (Prescribing More than One Drug Product); 105 CMR 721.020(A),(D) (effective Sept. 27, 2024)",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-16",
    "note": "Massachusetts generally uses one prescription form or record per drug product; a hospital setting may combine drugs on one record when each product has clear directions for use and interchange."
  },
  {
    "id": "E30-119",
    "set": 24,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "Diphenoxylate/atropine Lomotil Schedule V threshold versus diphenoxylate itself",
    "stem": "A Massachusetts pharmacist reviews the schedule of FDA-approved Lomotil tablets containing 2.5 mg diphenoxylate hydrochloride and 25 micrograms atropine sulfate per unit. For comparison, the pharmacist also checks the federal schedule of diphenoxylate itself outside this qualifying combination. Assume no separate exception or rescheduling order. Which classification is correct?",
    "choices": [
      {
        "text": "The qualifying diphenoxylate/atropine combination is Schedule II, as is diphenoxylate by itself.",
        "why": "Incorrect. The Schedule V exemption for certain combination products is product-specific: 21 CFR 1308.15(c)(4) covers no more than 2.5 mg diphenoxylate AND at least 25 micrograms atropine sulfate per dosage unit. The qualifying combination is not Schedule II."
      },
      {
        "text": "The qualifying diphenoxylate/atropine combination is Schedule V in federal and Massachusetts law, while diphenoxylate itself is federally Schedule II.",
        "why": "Correct. 21 CFR 1308.15(c)(4) explicitly defines the qualifying Schedule V combination by dosage-unit content; 21 CFR 1308.12(c)(8) separately lists diphenoxylate as Schedule II. Massachusetts adopts the corresponding schedules in 105 CMR 700.002. The pharmacist must classify the actual formulation."
      },
      {
        "text": "Both the qualifying combination and the individual active diphenoxylate ingredient are Schedule V because a low-dose antidiarrheal indication controls scheduling.",
        "why": "Incorrect. Indication and dose do not automatically reschedule the isolated active substance. The Schedule V provision is limited to qualifying combinations with the specified atropine content; uncombined diphenoxylate is listed under federal Schedule II."
      },
      {
        "text": "The qualifying combination is Schedule III, and diphenoxylate alone is Schedule II, because any mixture with atropine is automatically Schedule III.",
        "why": "Incorrect. The pertinent federal combination schedule is V, not III. The governing provision uses exact diphenoxylate and atropine quantities, not a class-wide rule for all mixtures."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1308.15(c)(4) (combination threshold); 21 CFR 1308.12(c)(8) (diphenoxylate); 105 CMR 700.002(B),(E) (Massachusetts corresponding schedules)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.15",
    "verified": "2026-11-16",
    "note": "Lomotil's qualifying 2.5-mg diphenoxylate/25-mcg atropine product is Schedule V, whereas diphenoxylate alone is Schedule II; never infer an ingredient's schedule from a specific combination."
  },
  {
    "id": "E30-120",
    "set": 24,
    "area": 4,
    "kind": "multi",
    "topicKey": "sterile-hazardous-compounding",
    "topic": "USP <797> initial garbing versus media-fill competency: distinct assessments and numbers",
    "stem": "A Massachusetts sterile compounding pharmacy trains a new employee for Category 2 compounded sterile preparations (CSPs). The trainee has no previous sterile-compounding qualification. The facility follows the currently official USP <797> requirements and the USP FAQ explanations of §§2.2–2.3. Which procedures are correct BEFORE the employee begins compounding CSPs? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Complete an initial garbing competency with visual observation and gloved fingertip/thumb sampling successfully on at least three separate occasions in succession.",
        "why": "Correct. USP <797> §2.2 and official USP FAQ 50 and 57 call for THREE successful initial garbing evaluations (each distinct complete hygiene and garbing with glove fingertip/thumb sampling), consecutively. One garbing session with three plates does not count as three evaluations."
      },
      {
        "text": "Require three separate successful media-fill tests as the initial aseptic manipulation competency because the three-test rule applies identically to garbing and media fill.",
        "why": "Incorrect. USP FAQ 50 distinguishes the initial three complete GARBlNG competency evaluations from ASEPTIC manipulation competency, which includes one successfully completed initial media-fill test and gloved fingertip/thumb sampling following that media fill."
      },
      {
        "text": "Complete an initial aseptic manipulation competency including a media-fill test and gloved fingertip/thumb sampling after that test.",
        "why": "Correct. USP <797> §2.3 and USP FAQ 50 identify the media fill plus post-media-fill gloved fingertip/thumb sampling as the initial aseptic manipulation competency; it is separate from initial garbing evaluation."
      },
      {
        "text": "Permit the trainee to compound for patients immediately under observation without initial garbing qualification, because only independent compounding requires successful garbing tests.",
        "why": "Incorrect. USP FAQ 49 clarifies that personnel must successfully complete initial garbing competency BEFORE any compounding, whether independently or under supervision. Observing the worker is not an exemption."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Current USP <797> §§2.2–2.3 (official Nov. 1, 2023); USP <797> Official FAQ updated Dec. 11, 2023, Q49–50, 57; 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
    "verified": "2026-11-16",
    "note": "Initial garbing qualification takes three separate successful evaluations; initial aseptic manipulation requires one successful media-fill assessment with post-media-fill fingertip/thumb sampling. Both are distinct and prerequisite to assigned CSP work."
  },
  {
    "id": "E30-121",
    "set": 25,
    "area": 1,
    "kind": "multi",
    "topicKey": "technician-scope",
    "topic": "A nationally certified technician's certification lapse while Massachusetts technician license remains active",
    "stem": "A Massachusetts community pharmacy has an employee with a current Massachusetts pharmacy technician license whose certification from a Board-approved national certifying body expired yesterday. The pharmacist is reviewing the employee's duties, name badge, and supervisory-ratio roster. Under 247 CMR 8.04(3), which changes or conclusions are required? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The worker remains eligible to perform ordinary licensed pharmacy technician functions under 247 CMR 8.02, assuming the Massachusetts license remains valid.",
        "why": "Correct. 247 CMR 8.04(3)(a) expressly limits a formerly certified person with lapsed certification to the duties of an ordinary pharmacy technician; it does not automatically revoke the person's separately valid Massachusetts pharmacy technician license. The pharmacist still performs required clinical checks and final validation."
      },
      {
        "text": "The worker may continue to use the 'Certified Pharmacy Technician' title and expanded certified duties indefinitely because state technician licensure is active.",
        "why": "Incorrect. Section 8.04(3)(a)–(b) explicitly requires a downgrade to ordinary technician duties and title after national certification lapses. The manager should revise the worker's badge and assignments instead of using the expired credential."
      },
      {
        "text": "For the supervisory-ratio calculation the employee must be counted as an ordinary pharmacy technician, not a certified pharmacy technician.",
        "why": "Correct. Section 8.04(3)(c) expressly directs that a person whose national certification lapses be counted as a pharmacy technician under §8.06(3). Scheduling decisions must reflect that reclassification."
      },
      {
        "text": "The worker must cease all pharmacy technician duties and apply for an entirely new Massachusetts technician license, even though the existing Massachusetts license is current.",
        "why": "Incorrect. The specific §8.04(3) rule permits ordinary technician duties and requires proper title and ratio treatment while state licensure remains valid. A lapsed national certification alone does not imply that a new state license is necessary."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 8.04(3)(a)–(c); 247 CMR 8.02(6); 247 CMR 8.06(3) (corrected Apr. 25, 2025)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-16",
    "note": "When national technician certification lapses but the Massachusetts technician license remains active, the worker may perform ordinary technician duties but must change title and be counted as ordinary in staffing ratios."
  },
  {
    "id": "E30-122",
    "set": 25,
    "area": 2,
    "kind": "single",
    "topicKey": "institutional-pharmacy-practice",
    "topic": "Hospital ED/discharge patient outpatient dispensing: 14-day supply and no hospital refill",
    "stem": "A Massachusetts hospital pharmacy receives an otherwise valid prescription for an emergency department patient who has completed treatment and is leaving the hospital. The prescribed medication is routinely stocked by community retail pharmacies and is available in quantities that permit dispensing exactly a 14-day supply. The prescriber orders 30 days plus two refills. No waiver applies. What may the hospital pharmacy dispense under 105 CMR 722.090?",
    "choices": [
      {
        "text": "The full prescribed 30-day supply and two refills, because the emergency department is part of the hospital.",
        "why": "Incorrect. Section 722.090(B) allows a hospital pharmacy to fill an emergency room or discharge patient's prescription for no more than a 14-day supply, and §722.090(B)(1) specifically forbids that hospital pharmacy from refilling those prescriptions. The ordinary retail-available drug has none of the stated exceptions."
      },
      {
        "text": "At most an initial 14-day supply without refills at the hospital pharmacy; the remaining continuing therapy needs an appropriate lawful outpatient dispensing arrangement.",
        "why": "Correct. 105 CMR 722.090(B) limits ED and discharge patient prescriptions to a 14-day supply, and (B)(1) bars hospital-pharmacy refills of those prescriptions. The manufacturer's smallest-package and unavailable-in-retail exceptions are inapplicable under the stated facts."
      },
      {
        "text": "A 72-hour emergency supply only, regardless of the prescriber's authorization, because no outpatient hospital pharmacy may dispense more than three days.",
        "why": "Incorrect. Section 722.090(B) normally establishes a 14-day limit, not a general 72-hour emergency supply limit. The pharmacist must not import an unrelated controlled-substance emergency rule into institutional pharmacy dispensing."
      },
      {
        "text": "No take-home supply at all, because hospital pharmacies may dispense only to admitted inpatients and never to emergency department patients.",
        "why": "Incorrect. Section 722.090(B) expressly authorizes eligible prescriptions for emergency room and discharge patients, subject to the 14-day cap, no-refills rule, and stated exceptions. The pharmacist should follow the specific patient category rather than reject all discharge prescriptions."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "105 CMR 722.090(A)–(C), especially (B)(1)–(2) (regulation published Sept. 27, 2024; substantive §722.090(B) text dates May 5, 2017)",
    "url": "https://www.mass.gov/doc/105-cmr-722-dispensing-procedures-for-clinic-and-hospital-pharmacies/download",
    "verified": "2026-11-16",
    "note": "Hospital ED and discharge take-home prescriptions normally have a 14-day initial supply maximum and NO hospital-pharmacy refills. Manufacturer minimum package and unavailable-at-retail exceptions are separate."
  },
  {
    "id": "E30-123",
    "set": 25,
    "area": 2,
    "kind": "multi",
    "topicKey": "controlled-prescriptions",
    "topic": "ePrescribing exemption duties: pharmacist verification versus invalid electronic-to-fax transmissions",
    "stem": "A Massachusetts retail pharmacist receives several otherwise authentic prescriptions in November 2026. A prescriber may rely on an enumerated exception from electronic prescribing, but the pharmacist did not personally witness the underlying reason. In another case, a purported electronic prescription arrived only as a fax (not a verified technical failover). Which legal conclusions follow 105 CMR 721.040 and 721.070? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist is not required to independently verify that an otherwise valid written or oral prescription falls within a prescriber's ePrescribing exception, though other validity and safety checks remain required.",
        "why": "Correct. Section 721.070(C) expressly says a pharmacist receiving an otherwise valid Written or Oral Prescription is not required to verify that the issuance properly falls under an enumerated exception, including waiver status. This does not excuse verification of the prescription's authenticity, prescriber authority, or clinical appropriateness."
      },
      {
        "text": "Any purported electronic prescription that arrives by ordinary facsimile is valid because the sending prescriber signed it electronically, even when no qualifying failover occurred.",
        "why": "Incorrect. Section 721.040(C) declares an Electronic Prescription transmitted by a means other than compliant Electronic Transmission invalid, except for a verified Failover under §721.020(G). A routine fax is not automatically a valid electronic prescription."
      },
      {
        "text": "A properly issued Massachusetts Schedule VI prescription falls under an express state ePrescribing exception, so it need not be transmitted electronically solely because it is a prescription drug.",
        "why": "Correct. Section 721.070(A)(9) expressly lists prescriptions for controlled substances in Massachusetts Schedule VI as an exception to mandatory ePrescribing. Oral/written prescriptions must still meet all other applicable legal conditions."
      },
      {
        "text": "Massachusetts permits a prescriber to choose paper or telephone for any Schedule II–V prescription merely for convenience, and the pharmacist must accept it as valid without further checks.",
        "why": "Incorrect. Section 721.070(A) limits exceptions and prohibits use of them to circumvent ePrescribing. Section 721.070(C)'s no-duty-to-verify-the-exception rule does not legalize a nonauthentic or otherwise invalid controlled prescription or remove federal requirements."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "105 CMR 721.040(C), 721.020(G), 721.070(A)(2),(9) and 721.070(C) (effective Sept. 27, 2024); M.G.L. c.94C §§20,22",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-16",
    "note": "The pharmacist need not audit the prescriber's ePrescribing-exception basis for an otherwise valid paper/oral Rx. Schedule VI is excepted, but faxing an electronic Rx is invalid unless it qualifies as verified failover."
  },
  {
    "id": "E30-124",
    "set": 25,
    "area": 3,
    "kind": "single",
    "topicKey": "schedule-ii-fax-exceptions",
    "topic": "DEA Schedule II fax-as-original exceptions: LTCF residents, hospice narcotics and ordinary outpatients",
    "stem": "A Massachusetts pharmacist receives practitioner-signed PAPER Schedule II prescriptions transmitted by fax for three patients: (1) a current long-term care facility resident, (2) a patient in an eligible hospice program whose narcotic prescription bears the required hospice notation, and (3) an ordinary community outpatient with no listed federal fax exception. Assume each paper prescription is otherwise lawful under a Massachusetts ePrescribing exception and meets federal requirements. Which federal dispensing determination is correct?",
    "choices": [
      {
        "text": "The fax is the original signed prescription for all three, because an authenticated fax has the same federal legal status as an electronic controlled-substance prescription.",
        "why": "Incorrect. Under 21 CFR 1306.11(a), a fax of an ordinary paper Schedule II prescription generally does NOT replace the manually signed original; it may be transmitted for advance review, but the original must be presented before dispensing unless a specific exception applies. Fax is not DEA-compliant EPCS."
      },
      {
        "text": "The ordinary outpatient qualifies for a fax-as-original exception, but the LTCF and hospice prescriptions require paper originals at the pharmacy.",
        "why": "Incorrect. This reverses the federal exceptions. Section 1306.11(f) allows fax to serve as original for a resident of a Long Term Care Facility; §1306.11(g) permits it for qualifying narcotic hospice prescriptions with the required notation. An ordinary outpatient without an exception requires the original."
      },
      {
        "text": "The fax may serve as the original for the LTCF resident and for the appropriately noted hospice narcotic prescription, but not for the ordinary outpatient's nonexceptional Schedule II prescription.",
        "why": "Correct. Federal 21 CFR 1306.11(f) and (g) create two fax-as-original exceptions. Under §1306.11(a), the ordinary outpatient fax is not sufficient by itself; the pharmacist must obtain and review the original signed paper prescription before filling unless another legitimate exception applies. This assumes the separate Massachusetts issuance/format rules are already satisfied."
      },
      {
        "text": "Only the hospice case qualifies if the pharmacist gets a verbal confirmation; all LTCF Schedule II medications are excluded from fax-as-original status.",
        "why": "Incorrect. Section 1306.11(f) expressly covers any Schedule II prescription for a qualifying LTCF resident without a narcotic-only limitation, whereas §1306.11(g) is specific to hospice narcotics. Oral confirmation alone does not replace a missing original in an ordinary nonexceptional case."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 1306.11(a),(e)–(g); 21 CFR 1306.05; 105 CMR 721.020(F),721.070(A),(C) (assumed valid MA ePrescribing exception)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11",
    "verified": "2026-11-16",
    "note": "A signed Schedule II fax is normally NOT the original. Federal exceptions permit fax-as-original for LTCF residents and appropriately documented hospice Schedule II narcotics (also qualifying direct parenteral infusion)."
  },
  {
    "id": "E30-125",
    "set": 25,
    "area": 4,
    "kind": "single",
    "topicKey": "sterile-hazardous-compounding",
    "topic": "USP <797> Category 3 extended BUD: additional sterility testing and ongoing facility requirements",
    "stem": "A Massachusetts sterile compounding pharmacy wants to assign a beyond-use date longer than the Category 2 BUD limit to one nonhazardous compounded sterile preparation. It has a compliant cleanroom suite and trained staff but has not implemented Category 3 additional qualifications or sterility testing. Manufacturer component expiration does not limit the proposed date. Which approach is consistent with the currently official USP <797> standard?",
    "choices": [
      {
        "text": "Assign the longer Category 3 BUD because working in an ISO 5 primary engineering control is the only extra condition for Category 3 classification.",
        "why": "Incorrect. USP <797> §14.4 and USP FAQ Q12 require additional Category 3 quality assurance, including sterility testing, applicable endotoxin testing, more stringent personnel and environmental controls, and stability evidence. ISO 5 airflow alone is not sufficient."
      },
      {
        "text": "Assign the Category 3 BUD as long as a compounder signs a policy waiver, even if sterility and applicable endotoxin tests are omitted.",
        "why": "Incorrect. A facility's internal policy cannot waive the compendial Category 3 requirements. USP FAQ Q12 describes the additional testing and other requirements; an authorized shorter BUD may be used rather than labeling a noncompliant CSP Category 3."
      },
      {
        "text": "Treat every CSP manufactured in a facility that meets Category 3 requirements as a Category 3 product and never use a shorter Category 2 BUD.",
        "why": "Incorrect. USP FAQ Q174 explicitly permits a facility otherwise capable of Category 3 compounding to assign a shorter Category 2 BUD to a particular CSP. The qualification level of the facility does not force every product to take the extended date."
      },
      {
        "text": "Do not assign the extended Category 3 BUD until all additional Category 3 requirements and required testing for that CSP are met; a suitable shorter BUD may be chosen.",
        "why": "Correct. USP <797> §§14.3–14.4 and USP FAQ Q12, Q174 and Q182 condition longer-than-Category-2 BUDs on additional Category 3 safeguards including sterility testing and, where indicated, endotoxin testing and supportable stability. The pharmacy must apply those requirements rather than extrapolate from cleanroom classification alone."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "Official USP <797> §§14.3–14.4 (revision official Nov. 1, 2023); USP <797> FAQs Dec. 11, 2023, Q12, 174, 182; 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
    "verified": "2026-11-16",
    "note": "Category 3 CSP BUDs beyond Category 2 limits require additional compounding qualifications, controls, testing and stability support; a facility may instead give an individual CSP a shorter Category 2 BUD."
  },
  {
    "id": "E30-126",
    "set": 26,
    "area": 1,
    "kind": "single",
    "topicKey": "workforce-supervision",
    "topic": "Retail Manager of Record: planned six-week absence and simultaneous management restriction",
    "stem": "The Massachusetts pharmacist Manager of Record (MOR) of Retail Pharmacy A plans to be away for six weeks. Before leaving, the MOR proposes that Pharmacy A wait five days to name an interim manager, and that the pharmacist simultaneously become MOR of a separate Retail Pharmacy B. Both retail stores have sufficient staffing. Which approach meets 247 CMR 9.23?",
    "choices": [
      {
        "text": "Appoint the interim MOR five days after departure; that deadline applies to all absences over 30 days, even those planned in advance.",
        "why": "Incorrect. Section 9.23(5)(a) requires appointment of an Interim Manager registered by the Board BEFORE a planned absence expected to last 30 days or longer. The five-day period in §9.23(5)(b) is for UNPLANNED absences."
      },
      {
        "text": "Appoint a Board-registered interim manager before the planned absence and do not concurrently serve as MOR for the second retail pharmacy.",
        "why": "Correct. 247 CMR 9.23(5)(a) requires the interim appointment before a planned 30-day-or-longer absence. Section 9.23(3) prohibits a retail pharmacy MOR from being MOR of more than one pharmacy at a time. A controlled-substance inventory and required signatures under §9.23(5)(c) also need appropriate handling before departure."
      },
      {
        "text": "Maintain both MOR titles if the pharmacist averages 30 combined hours per week across the two locations.",
        "why": "Incorrect. Section 9.23(3) forbids simultaneous retail MOR positions, and §9.23(4) independently requires an MOR to work an average of at least 30 hours PER WEEK at the pharmacy managed; combining hours between pharmacies cannot cure either problem."
      },
      {
        "text": "No interim manager is required as long as the pharmacist intends to return and another pharmacist handles final dispensing.",
        "why": "Incorrect. When a planned absence is expected to last at least 30 days, §9.23(5)(a) expressly requires a Board-registered Interim Manager before it begins. Staffing a working pharmacist at the counter is not automatically the designated interim appointment."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.23(3)–(5)(a),(c) (effective Dec. 6, 2024); compare 247 CMR 9.23(5)(b),(d) for unplanned absences and 100-day changes",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "For an expected 30-day-or-longer planned MOR absence, name a Board-registered Interim Manager beforehand. A retail pharmacist cannot simultaneously be MOR of two pharmacies."
  },
  {
    "id": "E30-127",
    "set": 26,
    "area": 2,
    "kind": "multi",
    "topicKey": "quality-safety",
    "topic": "Previously dispensed medication: mandatory acceptance of defective/error returns versus restocking",
    "stem": "Three people contact the SAME Massachusetts pharmacy about medications it previously dispensed. Patient X received the wrong drug. Patient Y's product is suspected to be contaminated. Patient Z received the correct, nondefective drug but no longer wants it. Assume no other specific legal return exception. Which practices follow 247 CMR 9.01? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Accept X's wrongly dispensed medication and Y's suspected defective or contaminated medication, then quarantine and properly dispose of the returned items.",
        "why": "Correct. Under 247 CMR 9.01(7)(a)–(b), a pharmacy SHALL accept its previously dispensed drug if it was dispensed in error or is suspected to be defective/contaminated. The accepted item cannot go back to inventory and must be quarantined and properly disposed of."
      },
      {
        "text": "Put Y's returned medication back on the shelf if its bottle is unopened and a pharmacist sees no visible damage.",
        "why": "Incorrect. Section 9.01(7) specifically prohibits putting medications accepted under its error/defect provision back into inventory, regardless of whether a retail seal appears intact. Visual appearance does not eliminate a possible contamination defect."
      },
      {
        "text": "Accept Z's properly dispensed, nondefective medication as a mandatory return and routinely redispense it to another patient after cleaning the label.",
        "why": "Incorrect. Section 9.01(7) says a pharmacy is not required to accept a medication that was properly dispensed and not defective, and §9.01(5) generally bars redispensing a previously dispensed medication absent a specific exception."
      },
      {
        "text": "The pharmacy is not required by this regulation to take back Z's properly dispensed, nondefective medication, while X's and Y's returns cannot be restocked.",
        "why": "Correct. The last sentence of §9.01(7) excludes mandatory acceptance of a properly dispensed nondefective medicine. It mandates quarantine/disposal rather than restoration of returned error/defect stock."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.01(5),(7)(a)–(b) (effective Dec. 6, 2024); distinct from 247 CMR 9.13 undelivered return-to-stock",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A dispensed-in-error or suspected defective product must be accepted back and quarantined/disposed; an otherwise correct, nondefective patient return is not mandatory and is not freely reusable."
  },
  {
    "id": "E30-128",
    "set": 26,
    "area": 2,
    "kind": "single",
    "topicKey": "controlled-prescriptions",
    "topic": "Corresponding pharmacist responsibility: authentic controlled Rx without valid patient-practitioner relationship",
    "stem": "A Massachusetts community pharmacist receives an authentic Schedule IV prescription from a registered, ordinarily authorized physician. The prescriber confirms that the intended patient has never been examined, contacted, or otherwise assessed by the physician or any collaborating practitioner and that no patient–practitioner relationship was established. No standing-order, emergency, or statutory exception applies. Which response follows Massachusetts pharmacy law?",
    "choices": [
      {
        "text": "Dispense after confirming the physician's DEA number because registration and signature establish all required conditions.",
        "why": "Incorrect. 247 CMR 9.15(2)(a)–(c) requires the pharmacist to determine legitimacy, a VALID patient–practitioner relationship, and authenticity. A valid registration and authentic signature alone do not resolve the missing relationship."
      },
      {
        "text": "Dispense if the patient pays cash because payer type is not relevant to the Board's validation criteria.",
        "why": "Incorrect. Whether payment is cash or insured does not waive 247 CMR 9.15(2)(b). The issue is the absence of a valid patient–practitioner relationship, not financial coverage."
      },
      {
        "text": "Do not dispense this prescription as described; clarify or obtain appropriate lawful prescribing care rather than rely solely on registration and authentication.",
        "why": "Correct. Section 9.15(2) prohibits filling unless the pharmacist's professional judgment establishes legitimate purpose, valid patient–practitioner relationship, authenticity and legal compliance. Federal 21 CFR 1306.04(a) also imposes a corresponding dispensing responsibility for legitimate controlled prescriptions."
      },
      {
        "text": "Treat the prescriber confirmation as permission to create a new relationship retroactively in the pharmacy computer and proceed.",
        "why": "Incorrect. A pharmacist cannot manufacture a clinical relationship from identity verification or a documentation shortcut. The relationship must be real and legally adequate; this case expressly excludes exceptions and any clinician-patient interaction."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 9.15(2)(a)–(d); 21 CFR 1306.04(a) (legitimate medical purpose and corresponding responsibility)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "An authentic, registered prescriber's controlled prescription still cannot be filled where a valid patient–practitioner relationship and other 247 CMR 9.15(2) criteria are absent."
  },
  {
    "id": "E30-129",
    "set": 26,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "Hydrocodone/acetaminophen rescheduling versus buprenorphine/naloxone and tramadol",
    "stem": "A Massachusetts pharmacist verifies three separately issued, legitimate prescriptions: hydrocodone/acetaminophen (Vicodin), buprenorphine/naloxone (Suboxone), and tramadol (Ultram). Which federal and corresponding Massachusetts schedule assignments are correct in November 2026?",
    "choices": [
      {
        "text": "Vicodin III, Suboxone III, and tramadol IV; hydrocodone combinations remained Schedule III after 2014.",
        "why": "Incorrect. DEA moved ALL hydrocodone combination products to Schedule II effective October 6, 2014. Codeine combination exceptions do not apply to hydrocodone/acetaminophen."
      },
      {
        "text": "Vicodin II, Suboxone II, and tramadol IV; all opioid agonists are Schedule II if prescribed for human pain or OUD.",
        "why": "Incorrect. Buprenorphine, including the named buprenorphine/naloxone combination, is listed in Schedule III under 21 CFR 1308.13(e)(2), regardless of the therapeutic indication. Hydrocodone combinations are Schedule II."
      },
      {
        "text": "Vicodin II, Suboxone III, and tramadol V; the weaker opioid's lower potency makes tramadol Schedule V.",
        "why": "Incorrect. Tramadol is specifically listed in Schedule IV under 21 CFR 1308.14(b)(3). Subjective opioid potency does not determine a drug's legal schedule."
      },
      {
        "text": "Vicodin II, Suboxone III, and tramadol IV; Massachusetts uses the same II–IV classifications through 105 CMR 700.002.",
        "why": "Correct. Hydrocodone combination products are Schedule II, buprenorphine is Schedule III and tramadol is Schedule IV. 105 CMR 700.002(B)–(D) adopts the federal corresponding controlled schedules. The pharmacist must use those product-specific categories when applying refills and dispensing limits."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1308.12(b)(1)(vi) hydrocodone; 21 CFR 1308.13(e)(2) buprenorphine; 21 CFR 1308.14(b)(3) tramadol; 105 CMR 700.002(B)–(D); DEA 2014 hydrocodone combination rescheduling",
    "url": "https://www.deadiversion.usdoj.gov/schedules/schedules.html",
    "verified": "2026-11-16",
    "note": "Hydrocodone combinations (Vicodin) are Schedule II, buprenorphine/naloxone (Suboxone) III, and tramadol (Ultram) IV federally and in Massachusetts."
  },
  {
    "id": "E30-130",
    "set": 26,
    "area": 4,
    "kind": "multi",
    "topicKey": "nonsterile-compounding",
    "topic": "USP <795> default BUD distinction: preserved versus nonpreserved aqueous and nonaqueous oral liquids",
    "stem": "A Massachusetts pharmacy compounds four different NONHAZARDOUS nonsterile preparations. There is no USP–NF compounded preparation monograph, formulation-specific stability study, or shorter component limitation, and all have otherwise compliant packaging. Under currently official USP <795> Section 10, which default beyond-use-date (BUD) statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A nonpreserved aqueous suspension (water activity at least 0.60) generally has a maximum 14-day BUD and requires refrigerated storage.",
        "why": "Correct. Official revised USP <795> Table 4 classifies nonpreserved aqueous CNSPs with water activity at least 0.60 as 14 days refrigerated unless shorter stability or an applicable authoritative formula imposes otherwise."
      },
      {
        "text": "A preserved aqueous solution with no substantiated specific stability has a default maximum BUD of 90 days at room temperature.",
        "why": "Incorrect. Under USP <795> Table 4, preserved aqueous CNSPs generally have a 35-day maximum BUD at controlled room temperature or refrigerated, not 90 days. Ninety days is the category for nonaqueous ORAL liquids."
      },
      {
        "text": "A properly preserved aqueous CNSP generally has a 35-day maximum BUD under the stated assumptions and may be stored at controlled room temperature or refrigerated.",
        "why": "Correct. Revised USP <795> Table 4 specifies preserved aqueous forms with water activity at least 0.60: 35 days, controlled room temperature or refrigerated. Preservative effectiveness and drug-specific stability must still be adequate."
      },
      {
        "text": "A nonaqueous oral liquid can automatically use the 180-day maximum reserved for other nonaqueous preparations such as capsules.",
        "why": "Incorrect. USP <795> distinguishes nonaqueous ORAL LIQUIDS (90 days) from OTHER nonaqueous preparations (180 days). Category selection depends on dosage form and water activity, not merely the absence of free water."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Current USP <795> Section 10.3/Table 4 (official Nov. 1, 2023); USP General Chapter <795> 2022 Open Forum BUD slide; 247 CMR 9.01(3)",
    "url": "https://www.usp.org/sites/default/files/usp/document/events-and-training/2022-11-08-gc-795-open-forum-website-posting.pdf",
    "verified": "2026-11-16",
    "note": "Under revised USP <795>, nonpreserved aqueous = 14 days refrigerated; preserved aqueous = 35 days at controlled room temp or refrigerated; nonaqueous oral liquid = 90 days, other nonaqueous = 180."
  },
  {
    "id": "E30-131",
    "set": 27,
    "area": 1,
    "kind": "single",
    "topicKey": "board-reporting",
    "topic": "Board personal-licensee profile update and changed legal name: separate 14-day compliance",
    "stem": "A Massachusetts pharmacist updates a personal mailing address and telephone number, and legally changes their surname following a court order. The pharmacist's professional license is otherwise in good standing. Under 247 CMR 20.03(1)–(2), which action is required?",
    "choices": [
      {
        "text": "Notify the Board only at the next biennial renewal; neither a contact change nor name change is reportable earlier.",
        "why": "Incorrect. Section 20.03(1) requires the online licensing profile to be updated within 14 calendar days of mailing-address, telephone or email changes; subsection (2) independently addresses changes of name within the same 14-day period."
      },
      {
        "text": "Update personal contact information within 30 business days; a name change requires no evidence as long as the online profile was edited.",
        "why": "Incorrect. Massachusetts uses 14 CALENDAR days rather than 30 business days, and §20.03(2) requires a sworn name-change statement plus a copy of valid picture identification and any other Board-required records."
      },
      {
        "text": "Update the contact details in the DPH online licensing profile within 14 calendar days and submit the required sworn name-change statement and identification within 14 calendar days.",
        "why": "Correct. These are separate duties imposed by §20.03(1)–(2). Editing the profile addresses changes to mailing address, telephone and email; a legal name change additionally requires the sworn statement, ID and any Board-requested supporting documentation."
      },
      {
        "text": "Submit a sworn statement only for the telephone number, and treat the legal surname change as automatically transferred from court records.",
        "why": "Incorrect. The sworn-statement procedure attaches to the NAME change under §20.03(2), not merely the phone number. A court order does not by itself update a pharmacist's DPH license profile."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 20.03(1)–(2) (effective Dec. 6, 2024); Massachusetts Board Reporting Requirements Overview",
    "url": "https://www.mass.gov/doc/247-cmr-20-reporting/download",
    "verified": "2026-11-16",
    "note": "Pharmacist mailing/phone/email updates are due within 14 CALENDAR days in the DPH portal; legal name changes have a separate sworn-statement plus photo-ID requirement, also within 14 calendar days."
  },
  {
    "id": "E30-132",
    "set": 27,
    "area": 2,
    "kind": "single",
    "topicKey": "drug-integrity",
    "topic": "PDMA-marked drug samples offered to a pharmacy for repackaging and resale",
    "stem": "A community pharmacy is offered manufacturer-labeled prescription samples bearing 'drug sample—not for resale.' The pharmacist proposes to use the samples to make compounded prescriptions, relabel part of the stock into ordinary pharmacy vials, and bill patients for the resulting medications. No specific exception applies. What does Massachusetts pharmacy law require?",
    "choices": [
      {
        "text": "Allow repackaging but not compounding, because the package label bans sale only in the original sample container.",
        "why": "Incorrect. 247 CMR 9.01(6) expressly prohibits accepting or purchasing medications designated 'drug samples not for resale' for purposes of compounding, REPACKING or any kind of resale. Removing the sample label does not erase the restriction."
      },
      {
        "text": "Decline the proposal: a pharmacy may not accept or buy these samples for compounding, repacking, or resale, regardless of whether it could charge only for labor.",
        "why": "Correct. The exact §9.01(6) prohibition attaches to accepting/purchasing samples for compounding, repacking or reselling. The federal PDMA framework in the FD&C Act also restricts drug-sample distribution and sale; a payment characterization does not convert sample stock into saleable prescription inventory."
      },
      {
        "text": "Use the samples as ingredients if the FDA-approved commercial medicine is not being chemically changed.",
        "why": "Incorrect. The specific ban in §9.01(6) is activity- and product-marking-based; it does not depend on whether the active substance is chemically altered. Samples cannot be accepted for compounding under the proposed activity."
      },
      {
        "text": "Release the sample stock to patients as ordinary saleable prescriptions if the pharmacy adds a manufacturer lot number and expiration date.",
        "why": "Incorrect. Ordinary stock-labeling completeness does not lift the sample-resale restriction. This differs from a valid commercial product or an uncollected prescription eligible for return to stock under an entirely different rule."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.01(6) (effective Dec. 6, 2024); Federal Food, Drug, and Cosmetic Act §503(c)–(d), 21 U.S.C. §353(c)–(d) (PDMA sample distribution and sale)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A pharmacy must not accept or purchase medicines marked 'drug samples not for resale' for compounding, repacking or resale; relabeling and charging only a service fee do not cure the prohibition."
  },
  {
    "id": "E30-133",
    "set": 27,
    "area": 2,
    "kind": "multi",
    "topicKey": "controlled-prescriptions",
    "topic": "Prescription format: patient address, veterinary exemption and practitioner registration across schedules",
    "stem": "A Massachusetts pharmacist reviews otherwise authentic outpatient prescriptions issued by authorized practitioners. None is a standing order, expedited partner therapy, or another special exception except the one expressly identified. Which statements about the required prescription contents under 105 CMR 721.020 are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "For an ordinary Schedule VI human prescription, the issuance date, practitioner registration number, drug identification/strength/quantity, directions, and authorized refill information remain required.",
        "why": "Correct. Section 721.020(C)–(D)(1)–(6) specifies the prescriber identification, issuance date, drug details, patient information, directions, and refill statement across Massachusetts prescription drugs, including Schedule VI. Schedule VI is not generally exempt from these basic elements."
      },
      {
        "text": "A community prescription for an ordinary adult human patient may omit the patient's address whenever the pharmacist can verify the patient's phone number.",
        "why": "Incorrect. Section 721.020(D)(4) generally requires patient NAME and ADDRESS. The rule lists limited exemptions such as veterinary orders, specified naloxone/opioid-antagonist prescriptions, and certain specified 721.070 exceptions; a verified phone number alone is not one."
      },
      {
        "text": "A veterinary prescription may omit the patient's name and address under the expressly listed 721.020(D)(4) exception; the other applicable veterinary and controlled-prescription requirements still apply.",
        "why": "Correct. 105 CMR 721.020(D)(4) expressly lists veterinary prescriptions as an exception to the patient name/address field, without exempting the practitioner, medication, directions, or other requirements. The pharmacist still needs an authentic, lawful veterinary order."
      },
      {
        "text": "The practitioner registration number is a required field only for federal Schedule II products; Schedule III–VI prescriptions have no registration-number requirement.",
        "why": "Incorrect. Section 721.020(D)(1) requires a practitioner registration number without limiting the field to Schedule II. For Massachusetts Schedule VI the MCSR may satisfy the state identification requirement, while federal Schedules II–V have applicable DEA registration requirements."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "105 CMR 721.020(C),(D)(1)–(6) (effective Sept. 27, 2024); DPH Elements of a Written Prescription; M.G.L. c.94C §22(a)",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-16",
    "note": "Massachusetts prescriptions generally need prescriber registration, issuance date, drug/strength/quantity, patient address, directions and refill statement. Veterinary prescriptions receive a specific patient name/address exception."
  },
  {
    "id": "E30-134",
    "set": 27,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "FDA-approved Xyrem (sodium oxybate) versus unapproved gamma-hydroxybutyrate scheduling",
    "stem": "A Massachusetts pharmacist compares (X) FDA-approved Xyrem (sodium oxybate), issued under all otherwise required special dispensing restrictions, with (Y) a separate unapproved gamma-hydroxybutyric acid (GHB) preparation. Which federal AND Massachusetts controlled schedules apply to these two distinct products?",
    "choices": [
      {
        "text": "Both are Schedule I because they contain chemically related gamma-hydroxybutyric acid.",
        "why": "Incorrect. Federal 21 CFR 1308.13(c)(6) specifically places FDA-approved drug products containing GHB or its salts in Schedule III; unapproved GHB is separately controlled in Schedule I under 1308.11(e)(1). Massachusetts follows the corresponding federal categories."
      },
      {
        "text": "Xyrem is Schedule III while unapproved GHB is Schedule I; the FDA-approved-drug-product exception does not extend to illicit or unapproved preparations.",
        "why": "Correct. 21 CFR 1308.13(c)(6) specifically covers FDA-approved products containing gamma-hydroxybutyric acid/sodium oxybate, while §1308.11(e)(1) covers ordinary GHB as Schedule I. Massachusetts 105 CMR 700.002(A),(C) incorporates those respective federal classifications. Applicable REMS and product restrictions also still apply to Xyrem."
      },
      {
        "text": "Xyrem is Schedule IV and unapproved GHB is Schedule II because a medically indicated dose reduces both by one controlled schedule.",
        "why": "Incorrect. Controlled-substance schedules are set by federal law, not by a pharmacist's dose-dependent inference. The listed categories are Schedule III for approved GHB-containing drug products and Schedule I for unapproved GHB."
      },
      {
        "text": "Xyrem is Massachusetts Schedule VI because it is FDA approved, whereas unapproved GHB is Massachusetts Schedule III.",
        "why": "Incorrect. Massachusetts Schedule VI does not capture drugs already in federally incorporated Schedules I–V. FDA approval alone does not make a controlled drug Schedule VI; the special §1308.13(c)(6) listing makes the approved product Schedule III."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1308.11(e)(6) (GHB); 21 CFR 1308.13(c)(6) (FDA-approved GHB-containing drug products); 105 CMR 700.002(A),(C); DEA Nov. 2026 GHB fact sheet",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.13",
    "verified": "2026-11-16",
    "note": "FDA-approved sodium oxybate products such as Xyrem are federally and Massachusetts Schedule III, but unapproved GHB is Schedule I; the product's FDA-approved status is decisive."
  },
  {
    "id": "E30-135",
    "set": 27,
    "area": 4,
    "kind": "multi",
    "topicKey": "pharmacy-operations",
    "topic": "Unannounced Board inspection and plan-of-correction deadlines after deficiencies",
    "stem": "Massachusetts Board pharmacy inspectors visit a licensed community pharmacy without notice and cite deficiencies. The Board's written notice does not specify a shorter or longer plan-of-correction deadline. The first submitted plan is later returned as unacceptable. Under 247 CMR 9.24–9.25, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Board inspectors may make an unannounced visit and inspect staff, activities and relevant pharmacy records; the pharmacy must supply requested inspection documents.",
        "why": "Correct. 247 CMR 9.24(1),(3) gives the Board or its designees authority to inspect licensed pharmacies at any time without notice and requires provision of requested documents during an inspection or investigation."
      },
      {
        "text": "Inspectors must provide 72 hours' notice unless they first obtain a court order, because prescription records are categorically exempt from Board inspection.",
        "why": "Incorrect. Section 9.24(1) permits unannounced regulatory inspections, and §9.24(3) requires requested documents; pharmacy confidentiality obligations do not establish the proposed universal advance-notice rule."
      },
      {
        "text": "The pharmacy need submit only one general corrective promise without dates, responsible persons, or MOR signature.",
        "why": "Incorrect. Section 9.25(2) requires corrective steps for EACH cited violation, projected completion/implementation dates and responsible individuals; §9.25(3) requires the MOR and, where applicable, supervising licensee signatures."
      },
      {
        "text": "The first written plan is due within 21 days unless the Board directs a different period, and an unacceptable plan must be revised within seven days.",
        "why": "Correct. Section 9.25(1) sets 21 days OR the timeframe directed by the Board; §9.25(5) requires resubmission of a corrected plan within seven days after the Board returns the prior plan as unacceptable."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.24(1)–(3) and 9.25(1)–(5) (effective Dec. 6, 2024)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A Board pharmacy inspection can be unannounced; requested records must be provided. A detailed signed plan of correction is due in 21 days unless otherwise directed, with seven days to revise an unacceptable plan."
  },
  {
    "id": "E30-136",
    "set": 28,
    "area": 1,
    "kind": "single",
    "topicKey": "workforce-supervision",
    "topic": "Pharmacy workforce: more than 12 working hours and the eight-hour consecutive rest exception",
    "stem": "A Massachusetts pharmacy technician has already practiced in a retail pharmacy for 12 hours in the preceding 24-hour period. A last-minute staffing emergency threatens access to urgent patient prescriptions. The technician can work only 45 more minutes, and management is able to document the extenuating circumstances and minimize the extra work. Which statement most accurately applies 247 CMR 9.01(17)?",
    "choices": [
      {
        "text": "An extenuating circumstance may permit the additional minimized, documented work in the patient's best interest; ordinarily eight consecutive hours of rest are required before resuming practice.",
        "why": "Correct. Section 9.01(17) limits pharmacist, intern and technician practice to 12 hours in a 24-hour period without completing eight consecutive hours' rest prior to resumption. An extenuating circumstance permits extra time to serve a patient's best interests only when minimized and documented. The exception is not routine scheduling permission."
      },
      {
        "text": "The exception is available to licensed pharmacists only; technicians can never work beyond 12 hours, regardless of a documented patient need.",
        "why": "Incorrect. Section 9.01(17) expressly includes pharmacy technicians as well as pharmacists and interns in both the work/rest provision and the extenuating-circumstance clause."
      },
      {
        "text": "The pharmacy can routinely schedule a 15-hour shift whenever the technician agrees, because a signed employee consent substitutes for a rest period.",
        "why": "Incorrect. Employee agreement alone is not an enumerated exception. The regulation requires a genuine extenuating circumstance serving patient interests, minimal extra time and documentation."
      },
      {
        "text": "A 30-minute meal break automatically resets the 12-hour limit, so neither a consecutive eight-hour rest period nor any written explanation is needed.",
        "why": "Incorrect. Section 9.01(17) specifies EIGHT CONSECUTIVE HOURS of rest, not a meal break, before resuming ordinary practice following the limit. A separate meal-break rule does not replace this requirement."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 9.01(17) (effective Dec. 6, 2024); distinguish pharmacy meal-break arrangements from consecutive rest",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "Pharmacists, pharmacy interns and technicians ordinarily need eight consecutive hours' rest after 12 hours of pharmacy practice in a 24-hour period; documented, minimized patient-interest exceptions are narrow."
  },
  {
    "id": "E30-137",
    "set": 28,
    "area": 2,
    "kind": "single",
    "topicKey": "counseling-dur",
    "topic": "Offer to counsel versus actual counseling: trained technician and pharmacy intern",
    "stem": "A Massachusetts retail pharmacy has a trained technician, a pharmacy intern and an on-duty pharmacist. The technician offers counseling to a patient with a newly prescribed drug. The patient accepts and asks how to take the drug with food and what to do after a missed dose. Under 247 CMR 9.18, who may fulfill the requested counseling?",
    "choices": [
      {
        "text": "The trained technician alone may answer the clinical counseling questions because the technician appropriately offered counseling.",
        "why": "Incorrect. Section 9.18(2) allows a properly trained designee to make the OFFER, but §9.18(3) expressly limits the actual counseling to a pharmacist or pharmacy intern. Asking about food interactions and missed doses requires counseling, not mere administrative intake."
      },
      {
        "text": "Only the pharmacist may counsel, because Massachusetts prohibits even a properly supervised pharmacy intern from advising patients.",
        "why": "Incorrect. Section 9.18(3) explicitly authorizes counseling by a pharmacist OR pharmacy intern; supervised intern counseling is not categorically forbidden."
      },
      {
        "text": "The pharmacist or the pharmacy intern may provide the counseling; the trained technician's role may be to offer it, but not to provide clinical counseling.",
        "why": "Correct. Under §9.18(1)–(4), an appropriately trained designee can make the offer, but only a pharmacist or pharmacy intern counsels each new drug therapy. Relevant content in §9.18(5) includes food interactions and missed-dose instructions."
      },
      {
        "text": "No counseling is required once the patient receives a printed drug-information leaflet; the technician may simply mark the offer completed.",
        "why": "Incorrect. A leaflet does not erase the pharmacist/intern counseling duty for a new drug therapy when counseling is sought. Sections 9.18(3)–(5) require qualified counseling on information needed for safe use."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 9.18(1)–(5) (effective Dec. 6, 2024); compare 9.18(10) for inpatient practice exclusion",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A trained technician may OFFER counseling, but only the pharmacist or pharmacy intern may actually counsel the outpatient, including on food interactions and missed doses."
  },
  {
    "id": "E30-138",
    "set": 28,
    "area": 2,
    "kind": "multi",
    "topicKey": "patient-choice-dispensing",
    "topic": "Bedside discharge prescription delivery: patient consent, pharmacy choice and direct delivery",
    "stem": "A community pharmacy offers a bedside delivery service at a Massachusetts inpatient healthcare facility for patients being discharged. A hospital discharge planner wants all patients automatically enrolled in the hospital's preferred community pharmacy, with medications dropped at the nurses' station whether or not the patient agrees. Under 247 CMR 9.04(4), which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy may waive individual patient consent because the patient is already hospitalized and an authorized discharge planner selected the pharmacy.",
        "why": "Incorrect. Section 9.04(4) expressly requires consent from the patient to provide bedside discharge prescription delivery. A hospital's preferred-pharmacy workflow does not create an automatic exemption."
      },
      {
        "text": "The bedside-delivery pharmacy must obtain patient consent to use the service and cannot restrict the patient's freedom to choose a pharmacy.",
        "why": "Correct. Both duties are expressly stated in 247 CMR 9.04(4). A bedside-delivery program should be opt-in and protect patient choice, not function as an exclusive mandatory hospital arrangement."
      },
      {
        "text": "The pharmacy may leave a patient's discharge medication at the nurses' station for later pickup by anyone available because it has fulfilled the delivery requirement by reaching the building.",
        "why": "Incorrect. Section 9.04(4) requires bedside-service prescriptions to be delivered DIRECTLY to the patient or patient's agent. Unattended placement at a station is not the prescribed delivery to the intended recipient."
      },
      {
        "text": "For a consenting patient who selects the pharmacy, the bedside service must deliver medications directly to that patient or the patient's authorized agent.",
        "why": "Correct. Section 9.04(4) couples the consent and freedom-of-choice conditions with direct handoff to the patient or patient's agent. All other controlled, labeling, and counseling rules still apply."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 9.04(4) (bed-side discharge prescription delivery, effective Dec. 6, 2024); 247 CMR 9.02 not a substitute for bedside-delivery consent",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "For bedside discharge prescription service, obtain the patient's consent, respect the patient's choice of pharmacy, and deliver medication directly to the patient or agent."
  },
  {
    "id": "E30-139",
    "set": 28,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "Vimpat lacosamide, Ketalar ketamine, and Ambien zolpidem: three distinct schedules",
    "stem": "A Massachusetts community pharmacist reviews otherwise lawful prescriptions for oral lacosamide (Vimpat), ketamine (Ketalar), and zolpidem (Ambien). All products are conventional, non-exempt FDA-approved medicines. Which classification accurately states their federal and Massachusetts controlled schedules?",
    "choices": [
      {
        "text": "Vimpat Schedule V, Ketalar Schedule III, Ambien Schedule IV.",
        "why": "Correct. Lacosamide is specifically listed in 21 CFR 1308.15(e)(5), ketamine in §1308.13(c)(7), and zolpidem in §1308.14(c)(59). Massachusetts 105 CMR 700.002(C)–(E) adopts these categories. The pharmacist should apply refill and dispensing limits to each product's actual schedule."
      },
      {
        "text": "Vimpat Schedule IV, Ketalar Schedule II, Ambien Schedule IV.",
        "why": "Incorrect. Lacosamide is Schedule V, not IV, and ketamine is Schedule III, not II. Zolpidem is Schedule IV; the other two classifications make this option invalid."
      },
      {
        "text": "Vimpat Schedule V, Ketalar Schedule IV, Ambien Schedule III.",
        "why": "Incorrect. Lacosamide is V, but ketamine is III rather than IV and zolpidem is IV rather than III under the federal controlled-substance schedules."
      },
      {
        "text": "All three are Schedule VI in Massachusetts because they are not conventional opioid or stimulant prescriptions.",
        "why": "Incorrect. Massachusetts Schedule VI covers prescription drugs not in the other incorporated schedules. Lacosamide, ketamine and zolpidem are explicitly federally scheduled and therefore retain the corresponding MA Schedules V, III and IV."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "21 CFR 1308.15(e)(5) (lacosamide); 21 CFR 1308.13(c)(7) (ketamine); 21 CFR 1308.14(c)(59) (zolpidem); 105 CMR 700.002(C)–(E)",
    "url": "https://www.deadiversion.usdoj.gov/schedules/schedules.html",
    "verified": "2026-11-16",
    "note": "Lacosamide/Vimpat = Schedule V, ketamine/Ketalar = Schedule III, zolpidem/Ambien = Schedule IV in federal and Massachusetts law."
  },
  {
    "id": "E30-140",
    "set": 28,
    "area": 4,
    "kind": "multi",
    "topicKey": "sterile-hazardous-compounding",
    "topic": "USP <800> risk assessments: intact final dosage form versus manipulated antineoplastic and HD API",
    "stem": "A Massachusetts pharmacy handles NIOSH-listed hazardous drugs (HDs) and considers documented assessments of risk (AOR) to use alternative containment. It receives commercially manufactured, intact Table 1 antineoplastic tablets for counting only; it also crushes a different Table 1 antineoplastic into an oral suspension, and compounds from a hazardous API. Under USP <800> and USP's January 2026 technical FAQs, which conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A documented product- and dosage-form-specific AOR may permit alternative containment when only counting intact commercially manufactured Table 1 antineoplastic tablets, absent manufacturer instructions requiring more.",
        "why": "Correct. USP <800> and FAQ 14 allow an AOR for final manufactured antineoplastic dosage forms not further manipulated beyond counting or repackaging, unless a manufacturer requires otherwise. The pharmacy must implement and document appropriate alternative controls and assess the individual drug and dosage form."
      },
      {
        "text": "The AOR can replace all required containment when a Table 1 antineoplastic is crushed into a compounded suspension, as long as one technician wears a disposable face mask.",
        "why": "Incorrect. Crushing Table 1 antineoplastic products is manipulation that triggers the full USP <800> containment strategies and work practices, not a general AOR exception. A face mask alone does not replace required engineering controls and PPE."
      },
      {
        "text": "One single AOR covering all Table 1 products is automatically sufficient, even where dosage forms and handling activities are entirely different.",
        "why": "Incorrect. USP FAQ 12 explicitly explains that each HD and dosage form must be identified individually in the risk assessment; tablet counting, capsule opening, and crushing involve different exposure risks. Group-wide generic assessment without the drug/dosage-form specifics is inadequate."
      },
      {
        "text": "A hazardous active pharmaceutical ingredient used in compounding remains subject to full USP <800> containment requirements; a pharmacy cannot substitute a reduced-containment AOR for that API.",
        "why": "Correct. USP <800> and USP FAQ 14, 18 require full containment for hazardous APIs and for manipulated Table 1 antineoplastics. AOR alternatives are available only to eligible dosage forms or other listed hazardous drugs as the standard specifies."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "USP <800> §§2–5 (hazardous drug list, assessment of risk and engineering controls); USP <800> FAQs updated Jan. 21, 2026, Q11–14 and Q18 (technical support, not a formal interpretation); 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_800_FAQs_January2026.pdf?version=0",
    "verified": "2026-11-16",
    "note": "AOR may be considered for intact final HD forms without additional manipulation; crushing Table 1 antineoplastics and compounding from hazardous APIs require full USP <800> containment. Assess each drug and dosage form."
  },
  {
    "id": "E30-141",
    "set": 29,
    "area": 1,
    "kind": "multi",
    "topic": "MOR: serious dispensing injury vs pharmacy-compounded serious adverse event",
    "topicKey": "board-reporting",
    "stem": "A resident Massachusetts pharmacy learns that an improper dispensing caused serious injury to a patient. Separately, a patient experiences a serious adverse drug event linked to a preparation compounded by that pharmacy. Under 247 CMR 20.02, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The Manager of Record must report the serious-injury improper dispensing to the Board within seven business days of discovering the injury.",
        "why": "Correct. Section 20.02(1) imposes this specific seven-BUSINESS-day duty on the MOR for improper dispensing resulting in serious injury or death. The pharmacy's separate CQI responsibilities remain in force."
      },
      {
        "text": "The pharmacy can postpone reports of both incidents until renewal if it promptly documents them in the CQI log.",
        "why": "Incorrect. CQI documentation does not replace the separately required §20.02(1)–(2) reports. The statute uses an event-specific reporting clock, not a license-renewal deadline."
      },
      {
        "text": "The MOR must report the compounded-product serious adverse drug event to the Board, FDA MedWatch and Betsy Lehman Center.",
        "why": "Correct. Section 20.02(2) lists all three recipients, with reporting due within seven business days of any employee's awareness. This is distinct from ordinary medication errors that do not qualify as the specified compounded/manufactured event."
      },
      {
        "text": "Once the pharmacy completes CQI documentation, it may destroy the serious-event reports after two years.",
        "why": "Incorrect. Section 20.02(4) requires the records for reportable events to remain readily retrievable for at least FIVE years from the date the report is filed. The general QRE minimum under 247 CMR 15.04 cannot shorten it."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 20.02(1)–(5) (effective Dec. 6, 2024); 247 CMR 15.03–15.04",
    "url": "https://www.mass.gov/doc/247-cmr-20-reporting/download",
    "verified": "2026-11-16",
    "note": "Serious-injury improper dispensing and pharmacy-compounded-drug serious adverse events have seven-business-day MOR reports; the latter goes to three agencies. Retain §20.02 records five years."
  },
  {
    "id": "E30-142",
    "set": 29,
    "area": 2,
    "kind": "single",
    "topic": "Expanded optometrist authority: ocular oral anti-infective versus opioid, systemic and injection limits",
    "topicKey": "prescriber-authority",
    "stem": "A Massachusetts optometrist holds the special glaucoma/ocular certification required by M.G.L. c.112 §66C and the proper state prescriptive registration. Assume every candidate prescription is authentic and all other legal conditions are met. Which proposed prescription is within this optometrist's professional scope?",
    "choices": [
      {
        "text": "Oxycodone for severe ocular postoperative pain, because the pain arises from eye treatment.",
        "why": "Incorrect. M.G.L. c.112 §66C(a)(D) expressly excludes opioid substances and drug products from the qualified optometrist's authority, even in an ocular setting."
      },
      {
        "text": "An appropriate oral anti-infective for an ocular infection being managed by the optometrist.",
        "why": "Correct. Section 66C(a)(ii) authorizes necessary eye-related medicines INCLUDING oral anti-infective drugs for properly certified optometrists. The patient and condition must remain within lawful optometric practice."
      },
      {
        "text": "Lisinopril for unrelated systemic hypertension that the optometrist discovered during an eye visit.",
        "why": "Incorrect. Section 66C(a)(A) forbids therapeutic agents for treatment of systemic diseases. Discovering hypertension during an eye examination does not confer general medical prescriptive authority."
      },
      {
        "text": "An agent administered by routine subcutaneous injection to treat an ocular disorder.",
        "why": "Incorrect. Section 66C(a)(C) excludes specified injection routes including subcutaneous, intramuscular, intravenous and intraocular routes. Certification does not eliminate those restrictions."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "M.G.L. c.112 §66C(a)(i)–(ii),(a)(A)–(D), effective Jan. 1, 2021; M.G.L. c.94C §7(h)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section66C",
    "verified": "2026-11-16",
    "note": "A specially certified optometrist may use appropriate eye-related oral anti-infectives but cannot prescribe opioids, systemic disease treatment or the barred injections."
  },
  {
    "id": "E30-143",
    "set": 29,
    "area": 2,
    "kind": "single",
    "topic": "Patient refusal of counseling and Massachusetts statutory documentation presumption",
    "topicKey": "counseling-dur",
    "stem": "A Massachusetts pharmacist offers counseling for a new outpatient prescription. The patient clearly declines, and the pharmacist completes the necessary prospective drug review. A staff member asks whether the patient's refusal needs a record. Which interpretation follows M.G.L. c.94C §21A?",
    "choices": [
      {
        "text": "The pharmacist must force a counseling session despite the patient's refusal because new prescriptions never permit refusal.",
        "why": "Incorrect. Section 21A explicitly permits the person presenting the prescription to decline the offer; the pharmacist need not provide counseling after refusal, although the offer and DUR duties remain."
      },
      {
        "text": "No attempt to document refusal is appropriate, because the statute presumes refusal whenever the record is silent.",
        "why": "Incorrect. Section 21A requires reasonable efforts to maintain relevant patient data, including failure to accept counseling. Missing a refusal record leads to a presumption of counseling provided, not declined."
      },
      {
        "text": "The pharmacy should reasonably record the refusal; without a recorded refusal, §21A presumes that counseling was provided.",
        "why": "Correct. Section 21A directs reasonable efforts to document any failure to accept the offer and provides the specified presumption. A truthful refusal record matters even though the patient may lawfully decline."
      },
      {
        "text": "The staff member may record that counseling took place because offering counseling is legally the same as delivering a counseling session.",
        "why": "Incorrect. An offer and the actual service are not identical. The pharmacist should not record counseling as performed when the patient declined; documenting the refusal is the proper course."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c.94C §21A (counseling refusal and record presumption); 247 CMR 9.18",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21A",
    "verified": "2026-11-16",
    "note": "Patients can decline counseling; record the refusal when possible. An absent refusal record creates the statutory presumption that counseling was actually provided."
  },
  {
    "id": "E30-144",
    "set": 29,
    "area": 3,
    "kind": "single",
    "topic": "Specific schedules: testosterone cypionate, phentermine, phenobarbital",
    "topicKey": "drug-schedule-identification",
    "stem": "Which federal and corresponding Massachusetts schedules correctly classify ordinary prescription testosterone cypionate injection, phentermine capsules and phenobarbital tablets in November 2026?",
    "choices": [
      {
        "text": "Testosterone III, phentermine IV, phenobarbital IV.",
        "why": "Correct. Testosterone is a listed Schedule III anabolic steroid at 21 CFR 1308.13(g). Phentermine and phenobarbital are expressly Schedule IV under §1308.14(f)(9) and (c)(49). Massachusetts uses corresponding Schedules III–IV."
      },
      {
        "text": "Testosterone VI, phentermine II, phenobarbital III.",
        "why": "Incorrect. Being FDA-approved hormone therapy does not exempt testosterone from Schedule III, and neither phentermine nor phenobarbital has the stated II/III classification."
      },
      {
        "text": "Testosterone III, phentermine III, phenobarbital II.",
        "why": "Incorrect. Only the testosterone classification is correct; phentermine is Schedule IV and phenobarbital is Schedule IV regardless of their indications."
      },
      {
        "text": "All three are Schedule IV because each is a prescription-only medicine.",
        "why": "Incorrect. Prescription-only status does not make every drug Schedule IV. Testosterone remains Schedule III as an anabolic steroid."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "21 CFR 1308.13(f)(84) (testosterone), 1308.14(c)(49) (phenobarbital), 1308.14(f)(10) (phentermine; shifted on Nov. 12, 2026); 105 CMR 700.002(C)–(D)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308",
    "verified": "2026-11-16",
    "note": "Testosterone is Schedule III; phentermine and phenobarbital are Schedule IV in the federal and corresponding Massachusetts systems."
  },
  {
    "id": "E30-145",
    "set": 29,
    "area": 4,
    "kind": "multi",
    "topic": "On-site refrigerated storage: dorm unit, logs, foods and integrity assessment",
    "topicKey": "medication-delivery-shipping",
    "stem": "A Massachusetts pharmacy is considering a dorm-style refrigerator with an interior freezer compartment for medicines. Management proposes storing lunches in the same refrigerator and keeping temperature excursion logs only six months. Which statements comply with 247 CMR 9.22? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The proposed dorm-style refrigerator is prohibited because its freezer compartment is within the refrigerator space.",
        "why": "Correct. Section 9.22(2) explicitly bans this design. The pharmacy must use appropriate combination or standalone equipment with compliant freezer design."
      },
      {
        "text": "Food is permitted if it stays on a shelf separate from the medication stock.",
        "why": "Incorrect. Section 9.22(5) prohibits food or beverages in a refrigerator/freezer used to store medications, without a shelf-based exception."
      },
      {
        "text": "Temperature logs must identify excursions and the pharmacy response, and must be retained for at least one year.",
        "why": "Correct. Section 9.22(4) requires out-of-range readings and response actions to be documented with a one-year minimum. The pharmacy's policy must include integrity assessment under §9.22(1)."
      },
      {
        "text": "An intact commercial package eliminates the need to assess drug integrity after an out-of-range temperature.",
        "why": "Incorrect. Section 9.22(1) requires an excursion response protocol including integrity assessment. An intact seal is not proof of stability under the actual temperature conditions."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 9.22(1)–(5), effective Dec. 6, 2024",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "No dorm-style refrigerators or food. Document temperature excursions and actions, assess drug integrity, and retain logs at least one year."
  },
  {
    "id": "E30-146",
    "set": 30,
    "area": 1,
    "kind": "single",
    "topic": "Annual specialty CE for temporary sterile and complex nonsterile compounding verification",
    "topicKey": "licensure-ce",
    "stem": "During 2026, a Massachusetts pharmacist verifies several compounded sterile preparations and several complex nonsterile preparations during brief coverage shifts. Other approved annual CE totals 20 hours, including required law and live hours, but none concerns compounding. No Board waiver applies. What additional specialty CE compliance is necessary?",
    "choices": [
      {
        "text": "None, because temporary compounding coverage does not require subject-specific CE.",
        "why": "Incorrect. Under 247 CMR 4.03(4)(c)–(d) and Board Policy 2021-04, even limited involvement in verifying sterile or complex nonsterile preparations triggers the corresponding annual specialty education."
      },
      {
        "text": "Five hours in sterile compounding only; complex nonsterile education is unnecessary when a pharmacist also does sterile work.",
        "why": "Incorrect. The applicable five sterile and three complex nonsterile annual requirements are independent; sterile responsibility does not extinguish complex nonsterile responsibility."
      },
      {
        "text": "Exactly eight specialty hours in addition to the annual 20, because compounding education is legally excluded from general CE credit.",
        "why": "Incorrect. Board Policy 2021-04 §VII allows appropriate specialty compounding education to count toward the annual 20-hour general requirement. The issue is required content, not necessarily eight hours above 20."
      },
      {
        "text": "Five sterile-compounding and three complex-nonsterile-compounding CE hours in the calendar year; qualifying specialty credit may count within the general annual 20.",
        "why": "Correct. Section 4.03(4)(c)–(d) specifies five annual sterile and three annual complex nonsterile hours for relevant work. The Board's revised CE policy applies to temporary verification and allows qualified specialty hours toward general CE."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 4.03(4)(c)–(d); Massachusetts Board Policy 2021-04 §§V–VII, revised Sept. 4, 2025",
    "url": "https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download",
    "verified": "2026-11-16",
    "note": "Sterile verification triggers five annual subject hours and complex nonsterile verification three. Eligible specialty CE may count toward annual general CE."
  },
  {
    "id": "E30-147",
    "set": 30,
    "area": 2,
    "kind": "multi",
    "topic": "CQI quality-related error: 24-hour documentation versus separate serious-event Board reports",
    "topicKey": "quality-safety",
    "stem": "A Massachusetts community pharmacist discovers a Quality-Related Event: a patient received the wrong prescription drug, but there is no known serious injury. The pharmacy has a CQI program. Which measures are required under 247 CMR 15? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist must promptly address patient notification, corrective directions and measures to minimize potential harm.",
        "why": "Correct. Under 247 CMR 15.03(1), staff alert the pharmacist/MOR immediately; the pharmacist addresses the patient and any professionally indicated prescriber/healthcare-team contact and corrective steps without waiting for injury."
      },
      {
        "text": "Initial event documentation may be delayed until the next monthly CQI meeting because no serious injury has occurred.",
        "why": "Incorrect. Section 15.03(2)(a) requires the informed or discovering pharmacist to complete initial documentation within 24 hours. The separate serious-injury reporting threshold under 20.02 is not a CQI exemption."
      },
      {
        "text": "Maintain QRE records for at least two years and provide pharmacy personnel with CQI education at least annually.",
        "why": "Correct. Section 15.04(2) mandates two-year QRE records; §15.02(1)(f) requires at least annual CQI education. More serious events may carry additional and longer reporting requirements."
      },
      {
        "text": "A wrong-drug dispensing is excluded from CQI unless the patient is hospitalized or dies.",
        "why": "Incorrect. A qualifying dispensing QRE triggers §15 event handling and documentation independent of whether it produced serious harm."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 15.02(1)(f), 15.03(1)–(3), 15.04(1)–(4); 247 CMR 20.02 (separate serious-event reporting)",
    "url": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download",
    "verified": "2026-11-16",
    "note": "A QRE needs immediate clinical response, documentation within 24 hours and at least two-year records, even with no serious injury."
  },
  {
    "id": "E30-148",
    "set": 30,
    "area": 2,
    "kind": "single",
    "topic": "Hospital pharmacy and on-premises hospital-owned skilled nursing residents",
    "topicKey": "institutional-pharmacy-practice",
    "stem": "A Massachusetts hospital pharmacy wants to provide medication orders for residents of a skilled nursing facility on its premises and solely owned by the hospital. The hospital DOES NOT meet the federal criteria for a 'sole community hospital' in 42 CFR 412.92. Under 105 CMR 722.090(A), which conclusion is correct?",
    "choices": [
      {
        "text": "Ownership and location alone do not establish the specific hospital-patient exception; the owning hospital must also satisfy the referenced federal sole-community-hospital criteria.",
        "why": "Correct. Section 722.090(A) requires the nursing facility to be solely owned by a qualifying sole community hospital and located on its premises. Without the separate federal-status condition, that special pathway is not established. The pharmacy should evaluate any other independently lawful arrangement."
      },
      {
        "text": "All nursing-facility residents automatically count as hospital inpatients if their facility shares an address with a hospital.",
        "why": "Incorrect. Section 722.090(A) has more conditions than location, and it expressly ties its nursing-facility exception to a sole community hospital."
      },
      {
        "text": "Hospital ownership alone is enough even if the facility is off-site and the hospital lacks the federal designation.",
        "why": "Incorrect. Both on-premises status and the referenced owning-hospital qualification are conditions. Ownership does not waive either of them."
      },
      {
        "text": "The law never permits a hospital pharmacy to serve any nursing-facility resident under any circumstances.",
        "why": "Incorrect. Qualifying solely hospital-owned on-premises facilities at a sole community hospital CAN fall within §722.090(A); the scenario fails a particular condition, not a universal prohibition."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "105 CMR 722.090(A) (hospital-based SNF/LTCF exception); 42 CFR 412.92 sole community hospital",
    "url": "https://www.mass.gov/doc/105-cmr-722-dispensing-procedures-for-clinic-and-hospital-pharmacies/download",
    "verified": "2026-11-16",
    "note": "Hospital ownership and an on-premises SNF are not enough: 105 CMR 722.090(A) also requires the hospital's sole-community-hospital status for this exception."
  },
  {
    "id": "E30-149",
    "set": 30,
    "area": 3,
    "kind": "single",
    "topic": "DEA multiple Schedule II prescriptions versus Massachusetts 30-day original validity",
    "topicKey": "controlled-quantity",
    "stem": "A Massachusetts practitioner issues three separate authentic electronic prescriptions for methylphenidate on November 1, 2026, each for 30 days. The second and third give earliest-fill dates December 15 and January 15, and diversion risk and legitimate-purpose conditions are satisfied. No new prescription is issued afterward. What follows from 21 CFR 1306.12(b) and M.G.L. c.94C §23(a)?",
    "choices": [
      {
        "text": "The delayed prescriptions remain valid because DEA permits separate prescriptions totaling up to 90 days, overriding all state issue-date expiration rules.",
        "why": "Incorrect. DEA §1306.12(b) conditions multiple issuance on applicable STATE law. Massachusetts Schedule II paper/electronic prescriptions expire 30 days after issue; a later earliest-fill date cannot extend that period."
      },
      {
        "text": "Issuing multiple Schedule II prescriptions is always an illegal refill; therefore none of the prescriptions, including the first, can be dispensed.",
        "why": "Incorrect. Federal law can permit separately issued Schedule II prescriptions; they are not all automatically refills. But each must independently remain valid under Massachusetts law at dispensing."
      },
      {
        "text": "The federal multiple-prescription option is conditional on state law, and both delayed originals would already be invalid under the Massachusetts 30-day validity limit.",
        "why": "Correct. Federal 21 CFR 1306.12(b)(1)(iv) requires state-law permission. M.G.L. c.94C §23(a) invalidates Schedule II prescriptions 30 days after issuance, counting under 247 CMR 9.04(10). The proposed dates occur well beyond that window."
      },
      {
        "text": "The pharmacist may merge all three authorizations into one 90-day dispensing from the first prescription to avoid the delayed-date problem.",
        "why": "Incorrect. A permission for selected nonopioid Schedules II–III 90-day SINGLE fills does not let the pharmacist rewrite the prescriber's three separately issued, future-dated prescriptions into one 90-day order."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 1306.12(b)(1)(i)–(v); M.G.L. c.94C §23(a),(d); 247 CMR 9.04(10)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23",
    "verified": "2026-11-16",
    "note": "DEA's up-to-90-day separate CII prescriptions are subject to state law. Massachusetts CII prescriptions expire 30 days after original issue, regardless of later earliest-fill wording."
  },
  {
    "id": "E30-150",
    "set": 30,
    "area": 4,
    "kind": "multi",
    "topic": "Emergency medication kits: reconciliation and Board-approved facility types",
    "topicKey": "controlled-inventory",
    "stem": "A Massachusetts pharmacy supplies emergency medication kits and proposes delivering them to any facility on request, without formal kit procedures or reconciliation against medication orders. Which statements accurately describe 247 CMR 9.09? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy must have procedures for kit security, maintenance and use.",
        "why": "Correct. Section 9.09(1) expressly requires pharmacy policies and procedures for proper dispensing through emergency kits, including security, maintenance and use."
      },
      {
        "text": "Any assisted living or commercial facility is eligible if its administrator agrees to accept the kit.",
        "why": "Incorrect. Under §9.09(3), pharmacies may provide kits ONLY to types of facilities approved by the Massachusetts Board, not to any willing recipient."
      },
      {
        "text": "Once medications are removed, the pharmacy has no responsibility to reconcile dispensing with valid prescriptions or orders.",
        "why": "Incorrect. Section 9.09(2) expressly obliges the pharmacy to reconcile medication dispensed through the kits with prescriptions or medication orders."
      },
      {
        "text": "The pharmacy must reconcile kit use with orders and may provide kits only to Board-approved facility types.",
        "why": "Correct. These two independent requirements appear in 247 CMR 9.09(2) and (3). The pharmacist should verify both records and destination authorization."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.09(1)–(3), effective Dec. 6, 2024",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "Emergency kits require secure documented procedures, reconciliation of use with prescriptions/orders and Board-approved facility types."
  },
  {
    "id": "E30-151",
    "set": 31,
    "area": 1,
    "kind": "single",
    "topic": "Pharmacist license available on site, badge first name and pharmacist title, NABP e-profile",
    "topicKey": "licensure-ce",
    "stem": "A Massachusetts pharmacist keeps a current Board-issued license readily available at the pharmacy but not wall-posted. The pharmacist's badge states only 'Staff Member' without a first name, and the pharmacist has no NABP e-profile number. What does 247 CMR 9.01(18)–(20) require?",
    "choices": [
      {
        "text": "Post the license on the wall; the generic badge and lack of e-profile are permissible.",
        "why": "Incorrect. The license may be carried, wall-posted OR readily available. However, the pharmacist must have the required identifying badge and maintain an NABP e-profile number."
      },
      {
        "text": "Keeping the license readily available is acceptable, but the badge must show at least the pharmacist's first name and recognized pharmacist title, and an NABP e-profile is required.",
        "why": "Correct. Section 9.01(18) permits three license-availability options; (19) requires first name plus 'Pharmacist,' 'Registered Pharmacist' or 'R.Ph.' on the badge; (20) requires the pharmacist to maintain an NABP e-profile number."
      },
      {
        "text": "The pharmacy manager's NABP e-profile satisfies the requirement for every pharmacist and staff can use generic role badges.",
        "why": "Incorrect. The requirement in §9.01(20) applies to each pharmacist personally. Section 9.01(19) does not allow pharmacists to conceal their title behind a nonspecific badge."
      },
      {
        "text": "All license, badge and e-profile requirements apply only at biennial renewal and can be deferred in daily practice.",
        "why": "Incorrect. Sections 9.01(18)–(20) are ongoing professional practice obligations, not renewal-only administrative tasks."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.01(18)–(20), effective Dec. 6, 2024",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "A current license may be carried, posted or readily available, but a pharmacist must wear a first-name/pharmacist-title badge and keep an NABP e-profile."
  },
  {
    "id": "E30-152",
    "set": 31,
    "area": 2,
    "kind": "single",
    "topic": "Licensed certified professional midwife versus APRN nurse-midwife Schedule VI limitations",
    "topicKey": "prescriber-authority",
    "stem": "A Massachusetts pharmacist evaluates medication orders issued by a licensed certified PROFESSIONAL midwife (not an APRN certified nurse-midwife). The professional midwife holds the required Massachusetts Controlled Substances Registration and is practicing within the officially recognized midwifery scope. Which interpretation of M.G.L. c.112 §295 is correct?",
    "choices": [
      {
        "text": "The midwife may order and administer covered Schedule VI medicines such as oxytocin and vitamin K in authorized practice, but cannot use Schedule II–V drugs under this license.",
        "why": "Correct. Section 295(a) lists authorized medicines such as oxytocin and vitamin K; §295(b)(i) prohibits controlled drugs other than Massachusetts Schedule VI for licensed certified professional midwives. The LCPM license must not be confused with an APRN certified nurse-midwife credential."
      },
      {
        "text": "The license gives exactly the same Schedule II–V prescribing privileges as an APRN certified nurse-midwife, because both titles contain 'midwife'.",
        "why": "Incorrect. Licensed certified professional midwives and APRN nurse-midwives have separate legal scopes. Section 295(b) prohibits the former from Schedule II–V use under this authority."
      },
      {
        "text": "Even approved Schedule VI medicines are prohibited to LCPMs because Massachusetts calls them 'controlled substances'.",
        "why": "Incorrect. Section 295(a) specifically permits named agents within approved practice and §295(b) explicitly excepts Schedule VI medicines from its exclusion."
      },
      {
        "text": "A clinic may authorize a Schedule IV analgesic simply by including it in its midwifery policy, bypassing §295's schedule restriction.",
        "why": "Incorrect. Internal policies cannot expand statutory authority. Section 295(b) excludes Schedule II–V drugs for this practitioner class regardless of a clinic's preference."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.112 §295(a)–(b), effective Nov. 21, 2024; 274 CMR 3.07, effective Sept. 11, 2026; M.G.L. c.94C §7(j)",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section295",
    "verified": "2026-11-16",
    "note": "Licensed certified professional midwives may use authorized Schedule VI agents but not Schedule II–V under their separate scope. Do not confuse them with APRN certified nurse-midwives."
  },
  {
    "id": "E30-153",
    "set": 31,
    "area": 2,
    "kind": "multi",
    "topic": "Massachusetts emergency interchange despite no-substitution: listed product and written buyer acceptance",
    "topicKey": "generic-interchange-emergency",
    "stem": "A Massachusetts community pharmacy receives an authentic brand prescription marked 'no substitution.' The brand is unavailable during an actual medical emergency, but a less expensive drug on the Massachusetts List of Interchangeable Drugs is available. No additional restriction applies. Under 247 CMR 9.05(1), which actions are permissible or required? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist may dispense the eligible less expensive interchangeable medicine in the qualifying emergency even though the brand order says 'no substitution'.",
        "why": "Correct. Section 9.05(1)(a) permits this limited emergency exception if the prescribed brand is unavailable and the alternative is on the state interchange list. It is not routine discretionary substitution."
      },
      {
        "text": "The pharmacist may replace the drug with any other medicine treating the same disease, whether or not it is legally interchangeable.",
        "why": "Incorrect. The exception is for a qualifying, listed interchangeable drug, not simply a medication with a related therapeutic indication."
      },
      {
        "text": "Document the date, hour and nature of the medical emergency and obtain the purchaser's written acceptance of the deviation.",
        "why": "Correct. Section 9.05(1)(b) demands BOTH a documented emergency and purchaser written acceptance. The pharmacy must retain an identifiable prescription for Board review."
      },
      {
        "text": "Documenting the emergency is sufficient; the patient or purchaser may not be asked to accept the change in writing.",
        "why": "Incorrect. Purchaser written acceptance is expressly required by §9.05(1)(b) in addition to documenting the medical emergency."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 9.05(1)(a)–(b), effective Dec. 6, 2024",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "In a real emergency, a listed less expensive interchangeable product may replace an unavailable 'no substitution' brand, but the emergency and written buyer acceptance must be documented."
  },
  {
    "id": "E30-154",
    "set": 31,
    "area": 3,
    "kind": "single",
    "topic": "Epidiolex federal CBD decontrol versus nabilone Cesamet Schedule II in Massachusetts",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacy classifies (X) FDA-approved Epidiolex cannabidiol oral solution with no more than 0.1% THC and (Y) FDA-approved Cesamet nabilone capsules. Which statement accurately describes the CURRENT federal and corresponding Massachusetts schedules in November 2026?",
    "choices": [
      {
        "text": "Epidiolex is still federal Schedule V and Cesamet is not federally controlled because its ingredient is synthetic.",
        "why": "Incorrect. FDA-approved qualifying CBD products such as Epidiolex were removed from federal Schedule V in 2020, while nabilone remains expressly Schedule II in 21 CFR 1308.12(f)(1)."
      },
      {
        "text": "Both are Schedule I because any cannabis-related medicine must be federally prohibited even after FDA approval.",
        "why": "Incorrect. The two specific approved products have different current statuses; neither is properly characterized as Schedule I in this case."
      },
      {
        "text": "Epidiolex is federally unscheduled but Massachusetts Schedule VI as a prescription medicine; Cesamet/nabilone is Schedule II in both federal and Massachusetts systems.",
        "why": "Correct. DEA's 2020 federal rule eliminated Schedule V control of qualifying FDA-approved CBD formulations, while Massachusetts includes other nonscheduled prescription drugs in Schedule VI. Nabilone remains Schedule II under §1308.12(f)(1), adopted correspondingly by Massachusetts."
      },
      {
        "text": "Epidiolex is Massachusetts Schedule III because it treats epilepsy, while Cesamet is Schedule IV because it treats chemotherapy nausea.",
        "why": "Incorrect. Therapeutic indications do not replace formal scheduling. The correct distinction is qualifying CBD product federal decontrol/state VI versus nabilone federal and state II."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "85 FR 51639 (Aug. 21, 2020), removal of FDA-approved CBD Schedule V listing; 21 CFR 1308.12(f)(1) nabilone; 105 CMR 700.002(B),(F); DEA Drugs of Abuse Guide 2024",
    "url": "https://www.dea.gov/sites/default/files/2024-12/2024-Drugs-of-Abuse-508.pdf",
    "verified": "2026-11-16",
    "note": "Epidiolex is now federally unscheduled and Massachusetts Schedule VI; Cesamet (nabilone) remains Schedule II. The old federal Epidiolex V classification is superseded."
  },
  {
    "id": "E30-155",
    "set": 31,
    "area": 4,
    "kind": "multi",
    "topic": "Hospital controlled automated dispensing device versus retail patient pickup machine",
    "topicKey": "automation-systems",
    "stem": "A licensed Massachusetts pharmacy proposes controlled-substance use of an automated dispensing device (ADD) inside a licensed hospital, with hospital nursing staff obtaining medicines near the point of care. A community pharmacy also has a separate patient-pickup automated pharmacy system (APS). Which statements follow 247 CMR 9.12 and Board ADD requirements? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The ADD must be in a licensed healthcare facility and dispensing must be pursuant to a valid patient-specific prescription or medication order.",
        "why": "Correct. Section 9.12(1)–(2) imposes both conditions. A healthcare-facility ADD is not an unrestricted medication supply solely because it uses secure cabinets."
      },
      {
        "text": "An institutional ADD is identical to an outpatient APS, so the APS rule allowing Schedule IV–VI patient pickup substitutes for ADD authorization.",
        "why": "Incorrect. Sections 9.10 and 9.12 govern different systems and purposes. The community APS rule does not replace healthcare facility ADD requirements."
      },
      {
        "text": "The pharmacy's ADD procedures must address location, maintenance, security, controlled-substance accountability, quality assurance, stocking/returns and confidentiality.",
        "why": "Correct. Section 9.12(4)(a)–(g) expressly enumerates these requirements, irrespective of whether the manufacturer also provides device instructions."
      },
      {
        "text": "A complete electronic access log allows ADD dispensing without a valid patient-specific order.",
        "why": "Incorrect. Section 9.12(2) still requires a valid prescription or order; electronic audit trails cannot independently create prescribing authority."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "247 CMR 9.12(1)–(4) and 9.10 (distinguish ADD versus APS), effective Dec. 6, 2024; Board Policy 2019-02, revised Jan. 9, 2025",
    "url": "https://www.mass.gov/policy-statement/automated-dispensing-device-use",
    "verified": "2026-11-16",
    "note": "Institutional ADDs require a licensed healthcare facility, patient-specific orders and pharmacy-defined accountability controls; they are not outpatient APS devices."
  },
  {
    "id": "E30-156",
    "set": 32,
    "area": 1,
    "kind": "single",
    "topic": "Expired pharmacist registration: no practice during lapse and renewal conditions after 60 days",
    "topicKey": "licensure-ce",
    "stem": "A Massachusetts pharmacist's personal registration expired on December 31 of an even-numbered year. The pharmacist did not renew, has not been suspended or revoked, and now applies 65 days after expiration. A pharmacy proposes that the pharmacist immediately resume final prescription validation while the late-renewal application is reviewed. Which statement BEST reflects 247 CMR 4.02?",
    "choices": [
      {
        "text": "The pharmacist may work during the first 90 days after expiration because late fees automatically preserve practice authority.",
        "why": "Incorrect. Section 4.02(3) treats ANY pharmacy practice after the personal registration expires as unlicensed practice. The regulation creates no general 90-day right to practice while a late renewal is pending; fees do not restore an expired license automatically."
      },
      {
        "text": "The pharmacist cannot resume practice until the registration is renewed; for a lapse exceeding 60 days, the Board may impose renewal conditions, including additional CE.",
        "why": "Correct. Under 247 CMR 4.02(1),(3) registration expires December 31 of even-numbered years, and practice after expiration is unlicensed. Subsection (4) permits an applicant lapsed more than 60 days, without suspension or revocation, to seek renewal subject to conditions the Board may impose, including additional CE. The pharmacist must verify active renewal before validating prescriptions."
      },
      {
        "text": "The Board must require a new NAPLEX and MPJE after every 60-day lapse, even when the registration has not been revoked.",
        "why": "Incorrect. Section 4.02(4) gives the Board discretion to impose conditions such as further continuing education after a lapse exceeding 60 days; it does not automatically require both exams at that threshold. A separate more-than-two-year lapse provision in §4.02(5) requires MPJE, not the proposed universal rule."
      },
      {
        "text": "The pharmacist may resume upon paying the regular renewal fee because the Board's authority to add conditions applies only to pharmacy facility licenses.",
        "why": "Incorrect. Section 4.02 specifically governs PERSONAL pharmacist registrations; payment alone is not permission to practice with an expired registration, and subsection (4) expressly covers delayed individual renewal conditions."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 4.02(1)–(5), Personal Registration Expiration and Renewal (MA Register 1330, Jan. 13, 2017)",
    "url": "https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download",
    "verified": "2026-11-16",
    "note": "Massachusetts pharmacist registrations expire December 31 of even years. There is no grace period to practice after expiration; after more than 60 days the Board may require additional renewal conditions, while more than two years triggers the separate MPJE rule."
  },
  {
    "id": "E30-157",
    "set": 32,
    "area": 2,
    "kind": "multi",
    "topic": "HIPAA family disclosures: express objection, absent patient and incapacitated patient",
    "topicKey": "hipaa-family-disclosures",
    "stem": "A HIPAA-covered Massachusetts pharmacy is considering disclosure of ordinary outpatient medication information to family or caregivers. No 42 CFR Part 2 record, controlled-drug pickup identification requirement, or stricter special confidentiality rule applies. In case X, a capable patient is present and expressly objects to sharing with a friend. In case Y, an absent patient's friend asks to collect a specific filled prescription on the patient's behalf. In case Z, an incapacitated patient cannot be asked and a caregiver needs medication instructions relevant to ongoing care. Which interpretations of 45 CFR 164.510(b) are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "In case X, the pharmacy may reveal the medication information to the friend over the capable patient's express objection merely because the friend says they help with care.",
        "why": "Incorrect. Section 164.510(b)(2) allows sharing with someone involved in care when the present, capable patient agrees, has an opportunity to object without objecting, or the professional reasonably infers no objection. An actual express objection to this disclosure defeats the claimed permission absent a different legal basis."
      },
      {
        "text": "In case Y, the pharmacy may use professional judgment and common practice to allow the friend to pick up the specified prescription without a prefiled written authorization naming the friend.",
        "why": "Correct. Under §164.510(b)(3), when the patient is absent the pharmacist may make a reasonable best-interest inference permitting a person to collect filled prescriptions. HHS expressly identifies friends picking up a named patient's prescription as an allowed common-practice example. Any separate state or controlled-product requirements still apply, and HIPAA does not require automatic release."
      },
      {
        "text": "In case Z, the pharmacy may use professional judgment to share only information directly relevant to the caregiver's involvement when disclosure is in the incapacitated patient's best interest.",
        "why": "Correct. Section 164.510(b)(3) permits a best-interest disclosure when incapacity makes it impracticable to obtain agreement or objection, but limits the protected information to what is directly relevant to that person's involvement in care or payment. The pharmacist should tailor the instructions and avoid unrelated profile history."
      },
      {
        "text": "Because HIPAA recognizes family involvement, a spouse automatically has access to the patient's entire prescription history even when the patient objected and much of the history is unrelated.",
        "why": "Incorrect. Section 164.510(b)(1) limits discretionary family disclosure to information directly relevant to the person's involvement; a spouse is not automatically entitled to the entire profile, and an expressed objection matters. Formal patient access under another HIPAA provision is a different issue."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "45 CFR 164.510(b)(1)–(3) (disclosures relevant to care, opportunity to object, best-interest professional judgment); HHS OCR FAQ, family and pharmacy prescription pickups",
    "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.510",
    "verified": "2026-11-16",
    "note": "Under ordinary HIPAA rules, a friend may collect a named patient's filled prescription based on reasonable professional judgment when the patient is absent. A capable patient's objection controls; incapacitated-patient disclosures must be in the patient's best interest and directly relevant."
  },
  {
    "id": "E30-158",
    "set": 32,
    "area": 2,
    "kind": "single",
    "topic": "FDA Class I recall risk determination before formal FDA classification",
    "topicKey": "drug-integrity",
    "stem": "A Massachusetts pharmacy receives a credible manufacturer's voluntary recall notice for a particular lot of injectable medicine. The notice describes a defect creating a REASONABLE PROBABILITY of serious adverse health consequences or death, although no injury has yet been confirmed. FDA has not assigned or published a recall class. Which response and interpretation is best supported by 21 CFR 7.3(m) and FDA recall guidance?",
    "choices": [
      {
        "text": "It must be Class III because no actual patient injury has been confirmed, and the pharmacy should await FDA's final classification before addressing affected stock.",
        "why": "Incorrect. Class III is for exposure NOT likely to cause adverse health consequences. Class determination is based on expected risk, not whether actual injury has already occurred; FDA explains that companies can initiate recalls before FDA classifies them. The pharmacy should promptly identify and segregate the affected product rather than keep distributing it."
      },
      {
        "text": "It cannot be a valid recall because only FDA may initiate one; a manufacturer warning before FDA classification has no practical relevance.",
        "why": "Incorrect. Recalls commonly begin on a firm's own initiative. FDA may classify them after receiving necessary information, so an unclassified manufacturer's recall notice still calls for a timely pharmacy response."
      },
      {
        "text": "The described hazard meets the Class I risk DEFINITION; a manufacturer may start a recall before FDA classifies it, so the pharmacy should segregate the affected lot and follow appropriate recall procedures.",
        "why": "Correct. 21 CFR 7.3(m)(1) defines Class I by a reasonable probability of serious health consequences or death. FDA's Enforcement Report guidance explains that voluntary recalls are often initiated BEFORE formal classification. The pharmacist should treat the credible notice as a patient/product integrity concern and prevent dispensing affected stock while handling the recall; this does not claim that FDA has already assigned Class I."
      },
      {
        "text": "Any voluntary medicine recall is Class II regardless of its severity, and the pharmacy must continue filling until FDA posts the event.",
        "why": "Incorrect. Voluntary describes how the recall is initiated, not its hazard classification. Class II is defined by temporary/reversible harm or a remote chance of serious harm; it does not fit the described reasonable probability of severe harm. There is no general requirement to keep dispensing pending FDA's database posting."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 7.3(m)(1)–(3), 7.40–7.42; FDA Enforcement Report Information and Definitions (FDA classification may follow company-initiated voluntary recall); 247 CMR 9.01 product integrity duties",
    "url": "https://www.fda.gov/safety/enforcement-reports/enforcement-report-information-and-definitions",
    "verified": "2026-11-16",
    "note": "Recall Class I describes a reasonable probability of severe injury or death, not proof of an actual injury. Voluntary recalls may begin before FDA assigns a class; segregate affected inventory and follow recall instructions rather than awaiting posting."
  },
  {
    "id": "E30-159",
    "set": 32,
    "area": 3,
    "kind": "single",
    "topic": "Antiseizure medication schedules: perampanel Fycompa, clobazam Onfi, brivaracetam Briviact",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacist reviews three otherwise lawful outpatient prescriptions: Fycompa (perampanel), Onfi (clobazam), and Briviact (brivaracetam). Which combination correctly identifies their current FEDERAL and corresponding MASSACHUSETTS schedules as of November 2026?",
    "choices": [
      {
        "text": "Fycompa Schedule IV, Onfi Schedule III, Briviact Schedule V.",
        "why": "Incorrect. Perampanel is specifically Schedule III under 21 CFR 1308.13(c)(11), not IV; clobazam is Schedule IV under §1308.14(c)(12), not III. Brivaracetam is V."
      },
      {
        "text": "Fycompa Schedule III, Onfi Schedule IV, Briviact Schedule IV.",
        "why": "Incorrect. Perampanel and clobazam are correctly III and IV, but brivaracetam is explicitly listed as Schedule V at 21 CFR 1308.15(e)(1). All antiseizure agents do not share a controlled schedule."
      },
      {
        "text": "Fycompa Schedule II, Onfi Schedule IV, Briviact Schedule V.",
        "why": "Incorrect. Clobazam and brivaracetam are IV and V, but perampanel's specific federal listing in §1308.13(c)(11) makes it Schedule III, not II. The name or indication cannot override the schedule."
      },
      {
        "text": "Fycompa Schedule III, Onfi Schedule IV, Briviact Schedule V.",
        "why": "Correct. 21 CFR 1308.13(c)(11) lists perampanel as Schedule III, §1308.14(c)(12) lists clobazam as IV, and §1308.15(e)(1) lists brivaracetam as V. Massachusetts 105 CMR 700.002(C)–(E) adopts the corresponding federal schedules; the pharmacist applies each drug's specific refill/record rules."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1308.13(c)(11) (perampanel), 1308.14(c)(12) (clobazam), 1308.15(e)(1) (brivaracetam); 105 CMR 700.002(C)–(E)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.13",
    "verified": "2026-11-16",
    "note": "Fycompa/perampanel is Schedule III, Onfi/clobazam is IV, and Briviact/brivaracetam is V under federal and Massachusetts law. Distinguish individual antiseizure drugs by their actual listings."
  },
  {
    "id": "E30-160",
    "set": 32,
    "area": 4,
    "kind": "multi",
    "topic": "September 2026 Board policy: viable ISO 7 buffer environmental action-level reporting and limited CSP BUD",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts sterile compounding pharmacy receives a microbiology report showing 11 CFU per cubic meter from VIABLE AIR sampling in its ISO Class 7 BUFFER room. There is no ISO 5 or non-viable particle action-level finding, and the Board has not directed a more restrictive plan. The pharmacy begins immediate assessment, develops and implements a remediation plan, completes a documented risk and product-risk assessment, and schedules repeat monitoring. Under Board Policy 2026-03 (adopted September 3, 2026), which conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The result exceeds the ISO 7 viable-air action level, and the MOR, designated PIC or pharmacist designee must report the result to the Board within one business day of receiving the microbiology report.",
        "why": "Correct. Policy 2026-03 establishes an ISO 7 viable-air action level of MORE THAN 10 CFU/m³; 11 exceeds it. Section II requires notification using the Board reporting form within ONE BUSINESS DAY of receipt of the microbiology report by the MOR, designated PIC or pharmacist designee. This is a Board policy requirement, not a federal DEA reporting deadline."
      },
      {
        "text": "Because the remediation plan has begun, the pharmacy can immediately assign the usual unrestricted Category 2 BUDs to all CSPs prepared in the affected ISO 7 buffer room.",
        "why": "Incorrect. During remediation of a VIABLE ISO 7 buffer-room action level, Policy 2026-03 §V caps applicable CSP BUDs at 24 hours room temperature or four days refrigerated, unless the Board directs otherwise. Restoration of usual BUDs depends on proper remediation confirmed by repeat sampling below action levels."
      },
      {
        "text": "The same limited-BUD permission applies to a NON-VIABLE particle action level, so a pharmacy never needs to stop compounding for particle-count findings.",
        "why": "Incorrect. Section III(D) differentiates non-viable particle action levels: absent other Board direction, compounding must be suspended until full remediation and recertification of all classified areas. The reduced-BUD pathway in §V applies to VIABLE action levels under specified safeguards."
      },
      {
        "text": "After the required initial assessment and remedial steps, the pharmacy may consider compounding during remediation in the affected ISO 7 buffer room only with the capped 24-hour room-temperature or four-day refrigerated BUD, subject to the policy's risk controls.",
        "why": "Correct. Section V requires initiated remediation, repeat EM scheduling, documented risk assessment and mitigation before considering continuation in ISO 7 buffer rooms with those reduced BUDs. This is conditional permission, not an automatic duty to compound; the pharmacy should preserve patient continuity with a safe plan."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "Massachusetts Board Policy 2026-03, §§I–II, III(A),(D)–(F), IV(B), V (adopted Sept. 3, 2026; supersedes Policy 2023-09); USP <797> official Nov. 1, 2023; 247 CMR 9.01(3)",
    "url": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download",
    "verified": "2026-11-16",
    "note": "New Board Policy 2026-03: ISO 7 viable-air results over 10 CFU/m³ are action levels; report within one business day. During qualifying ISO 7 buffer remediation, BUDs are capped at 24 hours room temperature or four days refrigerated; non-viable particle failures require suspension/recertification."
  },
  {
    "id": "E30-161",
    "set": 33,
    "area": 1,
    "kind": "single",
    "topic": "Individual license discipline: knowingly permitting unlicensed final validation",
    "topicKey": "board-discipline",
    "stem": "A Massachusetts-licensed supervising pharmacist knows that an employee has no pharmacist or intern license. To reduce the queue, the pharmacist knowingly lets that employee perform independent final clinical and dispensing validation of prescriptions. The pharmacy has no applicable waiver. No patient has yet been harmed. Which statement BEST describes the pharmacist's Board exposure?",
    "choices": [
      {
        "text": "The pharmacist's license cannot be disciplined unless the Board documents a specific patient's physical injury.",
        "why": "Incorrect. 247 CMR 10.03(1)(m) makes KNOWINGLY permitting, aiding or abetting unlicensed pharmacy activities a disciplinary ground; the provision does not require patient injury. The pharmacist must stop unlicensed validation immediately."
      },
      {
        "text": "The pharmacy owner alone is accountable because an individual pharmacist cannot be disciplined for an employee's unlawful work.",
        "why": "Incorrect. Section 10.03(1)(m) addresses the licensee who knowingly enables unlicensed work. The individual supervisor's responsibility is not removed by the owner's hiring or staffing decisions."
      },
      {
        "text": "The pharmacist may face discipline for knowingly permitting unlicensed activity, even before a patient is harmed; independent final validation must return to a licensed pharmacist.",
        "why": "Correct. Under 247 CMR 10.03(1)(m) and 247 CMR 9.04(1), the pharmacist must not knowingly allow an unlicensed person to perform tasks requiring professional pharmacy licensure. Actual harm is not a prerequisite to this ground, and any incident must be addressed under applicable patient-safety policies."
      },
      {
        "text": "The employee may validate dispensing independently if a pharmacist later signs a weekly supervisory log.",
        "why": "Incorrect. A retrospective log does not authorize a nonpharmacist to perform independent final dispensing validation. 247 CMR 9.04(1) requires pharmacist final validation; deliberate circumvention can separately support Board discipline."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 10.03(1)(m), (k) (grounds for individual discipline; effective Jan. 9, 2025); 247 CMR 9.04(1) (pharmacist final validation; effective Dec. 6, 2024)",
    "url": "https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download",
    "verified": "2026-11-16",
    "note": "Knowingly assigning licensed-professional pharmacy work to an unlicensed worker may support individual Board discipline even without actual patient injury; final dispensing validation remains a pharmacist duty."
  },
  {
    "id": "E30-162",
    "set": 33,
    "area": 2,
    "kind": "single",
    "topic": "Community pharmacy CDTM patient-age limitation despite parent consent",
    "topicKey": "cdtm-patient-practice",
    "stem": "A properly qualified Massachusetts community pharmacist holds an active CDTM agreement for asthma, including individual physician referral, physician-approved protocol, the required MCSR and detailed patient consent documentation. An otherwise eligible patient is 17 years old and a parent signs the written consent. The pharmacist plans to initiate a Schedule VI inhaler under that CDTM agreement. What is the best legal assessment?",
    "choices": [
      {
        "text": "The prescribing is permitted because a parent's written consent removes any CDTM minimum age.",
        "why": "Incorrect. 247 CMR 16.03(5)(a) specifically limits the community-pharmacy CDTM setting to patients age 18 or OLDER. Parent consent does not convert a 17-year-old into an eligible adult under the rule."
      },
      {
        "text": "The community pharmacist cannot use the CDTM prescribing authority for this 17-year-old; an authorized practitioner must arrange another lawful path to treatment.",
        "why": "Correct. Even with properly documented referral and consent, §16.03(5)(a)'s adult-patient requirement remains. The pharmacist should refer the minor to an authorized treating practitioner and must not treat the collaboration as overriding that patient-eligibility limit."
      },
      {
        "text": "The prescription may be issued because CDTM prohibits only Schedule II–V medicines and therefore any Schedule VI patient is eligible.",
        "why": "Incorrect. Section 16.03(5)(e) restricts controlled-drug scheduling, but §16.03(5)(a) imposes a SEPARATE adult-only community CDTM rule. Compliance with one requirement does not waive the other."
      },
      {
        "text": "The pharmacist may instead prescribe Schedule IV for the minor if the physician modifies the written referral.",
        "why": "Incorrect. Community-pharmacy CDTM authority cannot include Schedules II–V under §16.03(5)(e)3 and cannot be used for a 17-year-old under subsection (5)(a). Physician referral wording cannot override either restriction."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 16.03(5)(a),(c)–(e); 247 CMR 16.04(1)–(2) (community CDTM patient eligibility and limited prescribing, effective Dec. 15, 2017)",
    "url": "https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download",
    "verified": "2026-11-16",
    "note": "Massachusetts community-pharmacy CDTM is limited to patients age 18 or older, requires patient-specific written referral and consent, and cannot authorize Schedule II–V prescribing."
  },
  {
    "id": "E30-163",
    "set": 33,
    "area": 2,
    "kind": "multi",
    "topic": "DSCSA authorized trading partners and six-year product tracing record responsibility",
    "topicKey": "drug-integrity",
    "stem": "A Massachusetts community pharmacy purchases covered finished human prescription medicines from wholesalers and contracts with an outside records vendor. The pharmacy is NOT subject to a relevant DSCSA waiver, exemption, or enforcement-discretion relief. Under FD&C Act §582(d), which actions or conclusions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy may purchase covered product from any low-price distributor if it records the distributor's address, even if the distributor is not an authorized trading partner.",
        "why": "Incorrect. Under 21 U.S.C. §360eee-1(d)(3), a dispenser's trading partners must be AUTHORIZED. Keeping an address or favorable invoice does not replace verification of authorized trading-partner status."
      },
      {
        "text": "The pharmacy must conduct covered transactions with authorized trading partners and maintain applicable tracing records for at least six years after the transaction.",
        "why": "Correct. Section 582(d)(1)(A)(iii) requires retention of transaction information and statements (and applicable history) for not less than SIX years, and §582(d)(3) restricts dispenser trading partners to authorized entities. These duties are separate from investigating suspect products."
      },
      {
        "text": "A written agreement may allow a third party to maintain the tracing records, but the pharmacy remains responsible for its statutory recordkeeping obligations.",
        "why": "Correct. Section 582(d)(1)(B) expressly allows a written third-party records arrangement, while requiring the dispenser to keep the agreement and remaining liable for compliance. The pharmacist should ensure records are accessible when required."
      },
      {
        "text": "Once the third-party vendor accepts the records, all DSCSA duties transfer legally from the pharmacy to that vendor, so a pharmacy may discard its own agreement.",
        "why": "Incorrect. Section 582(d)(1)(B) expressly provides that a third-party retention agreement does NOT relieve the dispenser of the statutory duty and requires maintaining a copy of that agreement."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "FD&C Act §582(d)(1)(A)(iii), (d)(1)(B), (d)(3) (21 U.S.C. §360eee-1); FDA Drug Supply Chain Security Act product tracing and authorized trading partner guidance",
    "url": "https://uscode.house.gov/us/usc/119-120/t21/s360eee-1/",
    "verified": "2026-11-16",
    "note": "Under DSCSA, dispensers use authorized trading partners and retain required tracing data for six years. A written vendor retention agreement is allowed but does not transfer legal responsibility."
  },
  {
    "id": "E30-164",
    "set": 33,
    "area": 3,
    "kind": "single",
    "topic": "Insomnia medicines: Quviviq and Belsomra versus Rozerem controlled schedules",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacist reviews three otherwise valid prescriptions: Quviviq (daridorexant), Belsomra (suvorexant), and Rozerem (ramelteon). Which federal and corresponding Massachusetts scheduling description is correct as of November 2026?",
    "choices": [
      {
        "text": "Quviviq is Schedule III, Belsomra is Schedule IV, and Rozerem is Schedule VI.",
        "why": "Incorrect. Daridorexant is specifically listed in federal Schedule IV under 21 CFR 1308.14(c)(17), not III. Belsomra is IV and ramelteon is not federally scheduled, making the first classification wrong."
      },
      {
        "text": "All three are Schedule IV because each treats insomnia and requires a prescription.",
        "why": "Incorrect. Clinical indication and prescription status do not control DEA scheduling. Ramelteon is not federally scheduled (its current FDA label states DEA Schedule: None) and is Massachusetts Schedule VI as a prescription-only drug."
      },
      {
        "text": "Quviviq and Rozerem are Schedule VI and Belsomra is Schedule IV.",
        "why": "Incorrect. Rozerem is a Massachusetts Schedule VI prescription medicine, but daridorexant/Quviviq is federally controlled Schedule IV, and Massachusetts adopts the corresponding Schedule IV."
      },
      {
        "text": "Quviviq and Belsomra are Schedule IV federally and in Massachusetts; Rozerem is federally unscheduled and Massachusetts Schedule VI.",
        "why": "Correct. Daridorexant (21 CFR 1308.14(c)(17)) and suvorexant (§1308.14(c)(54)) are Schedule IV; ramelteon is not federally controlled according to its FDA/DailyMed product labeling and is a Massachusetts prescription-only Schedule VI drug under 105 CMR 700.002(F)."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1308.14(c)(17),(54); 105 CMR 700.002(D),(F); current FDA DailyMed Rozerem labeling (DEA Schedule: None, Apr. 15, 2026)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.14",
    "verified": "2026-11-16",
    "note": "Quviviq/daridorexant and Belsomra/suvorexant are C-IV, while Rozerem/ramelteon is federally unscheduled but a Massachusetts Schedule VI prescription medicine."
  },
  {
    "id": "E30-165",
    "set": 33,
    "area": 4,
    "kind": "multi",
    "topic": "USP <800> antineoplastic automation and pneumatic-tube transport restrictions",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts hospital pharmacy handles final dosage forms of NIOSH Table 1 antineoplastic hazardous drugs (HDs), a separate non-antineoplastic hazardous tablet, and liquid HD solutions. It is evaluating automated pill counters and pneumatic-tube carriers using the January 2026 USP <800> technical FAQs. Which decisions are consistent with those standards? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Keep the NIOSH Table 1 antineoplastic tablets out of automated counting or packaging machinery because breakage and powder contamination can expose workers.",
        "why": "Correct. USP <800> Section 12 and FAQ #85 prohibit placing Table 1 antineoplastic tablets and capsules into automated counting or packaging machines. Manual or otherwise compliant handling avoids machinery contamination."
      },
      {
        "text": "A liquid hazardous drug may be sent by pneumatic tube as long as the bottle has a child-resistant closure.",
        "why": "Incorrect. USP <800> and FAQ #80 specifically prohibit liquid hazardous drugs in pneumatic tubes due to breakage and contamination risks. A child-resistant cap is not an exception."
      },
      {
        "text": "For a hazardous tablet that is NOT a Table 1 antineoplastic, facility-specific assessment of risk and SOPs may support an automated counting process when safe and otherwise permitted.",
        "why": "Correct. FAQ #85 expressly distinguishes non-Table 1 antineoplastic HD tablets, which MAY be eligible for an assessed alternative using automated systems. The facility must evaluate product, exposure and contamination risks and establish controls."
      },
      {
        "text": "Every hazardous-drug dosage form is categorically prohibited from any mechanical transport, including conveyors or carts, regardless of product-specific risk assessment.",
        "why": "Incorrect. FAQ #80 restricts pneumatic tubes for liquid HDs and Table 1 antineoplastic HDs, while #86 permits risk-based handling of eligible final dosage forms on conveyors. The absolute ban on ALL mechanical transport is unsupported."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Current USP <800> §12 (final dosage form dispensing and transport); USP <800> FAQs updated Jan. 21, 2026, Q80, 85–86 (technical support, not official interpretation); 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_800_FAQs_January2026.pdf?version=0",
    "verified": "2026-11-16",
    "note": "Do not use automated counting for NIOSH Table 1 antineoplastic tablets or pneumatic tubes for liquid HDs. Evaluate other HD dosage forms individually under USP <800> and facility SOPs."
  },
  {
    "id": "E30-166",
    "set": 34,
    "area": 1,
    "kind": "single",
    "topic": "Foreign pharmacy graduate: one-year FPGEE authorization before Massachusetts internship",
    "topicKey": "intern-education",
    "stem": "A graduate of a foreign pharmacy school not approved by the Massachusetts Board is seeking to start an internship in a Massachusetts community pharmacy. NABP authorized the graduate to sit for the FPGEE 14 months ago. The graduate holds no newer authorization and otherwise has all paperwork ready. Which action is required under 247 CMR 8.01(7) before the internship begins?",
    "choices": [
      {
        "text": "Obtain NABP authorization to sit for the FPGEE issued within the preceding year and furnish a copy to the Board with its other required documentation.",
        "why": "Correct. For a graduate of a non-approved pharmacy college or school, §8.01(7) expressly requires FPGEE test authorization issued WITHIN THE PRECEDING YEAR before starting a Massachusetts pharmacy internship, with a copy submitted to the Board. The 14-month-old authorization is insufficient."
      },
      {
        "text": "Begin the internship immediately because any FPGEE authorization, regardless of issue date, remains acceptable if the candidate has not yet taken the examination.",
        "why": "Incorrect. Section 8.01(7) contains a specific one-year recency condition on the authorization. No general indefinite-validity substitute is provided."
      },
      {
        "text": "Complete 500 hours before submitting an FPGEE authorization, because the document is necessary only when the graduate applies for the pharmacist MPJE.",
        "why": "Incorrect. The regulation requires the authorization BEFORE COMMENCEMENT of the Massachusetts internship, rather than only after hours accrue or at MPJE scheduling."
      },
      {
        "text": "Use a licensed pharmacy technician credential in place of the FPGEE authorization to receive pharmacy intern credit.",
        "why": "Incorrect. Pharmacy technician licensure and an applicant's foreign-graduate pharmacist-intern eligibility are separate pathways. A technician credential cannot waive §8.01(7)'s NABP authorization requirement."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 8.01(7) (Graduates of Non-approved Colleges/Schools of Pharmacy; effective Jan. 9, 2025), plus other applicable pharmacy intern licensing prerequisites",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-16",
    "note": "A Massachusetts foreign-school graduate from a non-approved program must have NABP FPGEE eligibility authorization issued within the preceding year before starting an internship."
  },
  {
    "id": "E30-167",
    "set": 34,
    "area": 2,
    "kind": "single",
    "topic": "Outpatient methadone analgesia versus methadone maintenance for opioid use disorder",
    "topicKey": "opioid-oud",
    "stem": "A Massachusetts community pharmacist receives two authentic methadone Schedule II prescriptions from a DEA-registered non-OTP physician. Prescription X is for severe persistent pain treated in the physician's usual professional practice; prescription Y explicitly orders a daily outpatient supply for OUD maintenance instead of referral to an opioid treatment program. Assume X otherwise satisfies state and federal prescribing limits and is clinically appropriate. Which statement BEST addresses the prescriber's federal authority?",
    "choices": [
      {
        "text": "Neither prescription may be filled because all methadone prescribing requires certification as a federal opioid treatment program.",
        "why": "Incorrect. Methadone is Schedule II and may be legitimately prescribed for pain by an appropriately registered practitioner in the usual course of practice. The special OTP restriction concerns its use for ongoing OUD maintenance or detoxification, not every analgesic prescription."
      },
      {
        "text": "Both may be filled because the individual DEA registration permits a non-OTP physician to use methadone for any outpatient purpose.",
        "why": "Incorrect. A conventional DEA practitioner registration does not authorize a routine non-OTP take-home methadone prescription for OUD maintenance. The limited three-day emergency rule concerns direct dispensing, not ordinary outpatient maintenance prescriptions."
      },
      {
        "text": "X can fall within ordinary legitimate pain prescribing, whereas Y is not a lawful routine non-OTP outpatient prescription for methadone OUD maintenance.",
        "why": "Correct. Methadone is available for severe persistent pain by otherwise qualified DEA-registered prescribers under 21 CFR 1306.04(a). Under 21 CFR 1306.07(a) and the DEA's Aug. 2026 methadone guidance, ongoing methadone OUD maintenance is provided through a certified opioid treatment program; §1306.07(b)'s limited emergency dispensing exception does not convert Y into a routine prescription."
      },
      {
        "text": "Y is valid as a refillable Schedule II prescription if the patient has previously received methadone at a hospital, but X must be rejected.",
        "why": "Incorrect. Previous inpatient administration does not authorize outpatient methadone maintenance by a non-OTP prescriber, and Schedule II prescriptions generally cannot be refilled. Legitimate pain treatment is not automatically prohibited."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 1306.04(a), 1306.07(a)–(c), 1306.12(a); DEA Methadone Drug Fact Sheet updated Aug. 2026; applicable M.G.L. c.94C",
    "url": "https://www.deadiversion.usdoj.gov/drug_chem_info/methadone/methadone.pdf",
    "verified": "2026-11-16",
    "note": "Methadone can be legitimately prescribed for pain, but ongoing methadone treatment of OUD normally requires a certified opioid treatment program; the emergency three-day rule authorizes limited dispensing, not an outpatient maintenance prescription."
  },
  {
    "id": "E30-168",
    "set": 34,
    "area": 2,
    "kind": "multi",
    "topic": "Community pharmacy nonsterile compounding service: permissible refusal versus routine business preference",
    "topicKey": "pharmacist-compounding-duty",
    "stem": "A Massachusetts community pharmacy receives several prescriptions for SIMPLE or MODERATE nonsterile compounded preparations customary to community needs. The pharmacists have appropriate training and facilities. Management does not want to compound because a nearby chain offers cheaper commercially manufactured products. There is no extenuating circumstance or Board waiver. Which interpretations of 247 CMR 9.01(15) are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy may decline any simple or moderate customary nonsterile compounded prescription solely to improve its margin, without documenting an exception.",
        "why": "Incorrect. 247 CMR 9.01(15) prohibits refusing simple or moderate customary nonsterile preparations except for extenuating circumstances or a waiver of Board regulation. A routine business preference alone is not the stated legal exception."
      },
      {
        "text": "The professional-practice rule generally forbids refusing those customary simple or moderate nonsterile preparations when neither an extenuating circumstance nor Board waiver exists.",
        "why": "Correct. Section 9.01(15) creates a specific duty for licensees, in contrast to a general assumption that compounding is always discretionary. Staff should assess patient safety and comply with the applicable USP <795> standards."
      },
      {
        "text": "The pharmacy must accept any hazardous sterile Category 3 compound under the same provision even when personnel and facilities are not competent to prepare it.",
        "why": "Incorrect. Section 9.01(15) is specifically about SIMPLE or MODERATE NONSTERILE compounded preparations customary to the community; it does not mandate complex sterile or hazardous compounding without competent facilities and current USP compliance."
      },
      {
        "text": "A genuine extenuating circumstance or Board regulatory waiver can provide an exception to that particular nonsterile compounding non-refusal rule.",
        "why": "Correct. Section 9.01(15) expressly permits refusal under extenuating circumstances or Board waiver. The licensee should document the applicable basis and still protect patient continuity and safety."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 9.01(4),(15) (professional practice standard, effective Dec. 6, 2024); USP <795> current compendial nonsterile standards",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "Massachusetts licensees generally must not refuse simple/moderate nonsterile compounding customary to the community without extenuating circumstances or a Board waiver; this is not a mandate to prepare every sterile or hazardous product."
  },
  {
    "id": "E30-169",
    "set": 34,
    "area": 3,
    "kind": "single",
    "topic": "Muscle relaxants: Soma carisoprodol controlled versus Flexeril and Lioresal",
    "topicKey": "drug-schedule-identification",
    "stem": "Three otherwise valid outpatient prescriptions reach a Massachusetts pharmacy: Soma (carisoprodol), Flexeril (cyclobenzaprine), and Lioresal (baclofen). All are conventional prescription products. Which federal and corresponding Massachusetts schedule classification is correct?",
    "choices": [
      {
        "text": "Soma is Schedule II, Flexeril Schedule IV, and Lioresal Schedule VI because a muscle relaxant's abuse potential tracks its sedative strength.",
        "why": "Incorrect. Carisoprodol was placed in Schedule IV effective Jan. 11, 2012, not Schedule II. Cyclobenzaprine is not federally scheduled and is not Schedule IV. Clinical sedation is not the controlling schedule list."
      },
      {
        "text": "Soma is federally and Massachusetts Schedule IV; Flexeril and Lioresal are federally unscheduled but Massachusetts Schedule VI prescription drugs.",
        "why": "Correct. 21 CFR 1308.14(c)(7) expressly controls carisoprodol in Schedule IV; FDA-approved prescription cyclobenzaprine and baclofen are not in federal Schedules I–V and are treated as Massachusetts Schedule VI under 105 CMR 700.002(F). Specific ingredient status controls, not drug-class labels."
      },
      {
        "text": "Soma and Flexeril are Schedule IV, while Lioresal is Schedule III because it can be used for neurologic disease.",
        "why": "Incorrect. Cyclobenzaprine is not a federal controlled substance and baclofen is not Schedule III; the indications do not set a drug schedule."
      },
      {
        "text": "All three are Schedule VI because none is a DEA-controlled opioid, stimulant, or benzodiazepine.",
        "why": "Incorrect. Schedule IV includes non-benzodiazepine depressants such as carisoprodol. A muscle relaxant can be controlled despite not belonging to the named example classes."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 1308.14(c)(7) (carisoprodol); DEA final rule 76 FR 77330, effective Jan. 11, 2012; 105 CMR 700.002(D),(F); FDA prescription-only status for cyclobenzaprine and baclofen",
    "url": "https://www.deadiversion.usdoj.gov/drug_chem_info/carisoprodol/carisoprodol.html",
    "verified": "2026-11-16",
    "note": "Carisoprodol/Soma is federal and Massachusetts Schedule IV; cyclobenzaprine/Flexeril and baclofen/Lioresal are federally unscheduled but Massachusetts Schedule VI prescription medicines."
  },
  {
    "id": "E30-170",
    "set": 34,
    "area": 4,
    "kind": "multi",
    "topic": "Massachusetts multi-drug single-dose packs: sixty-day cap, Schedule exclusions, same-patient repackaging",
    "topicKey": "compliance-packaging",
    "stem": "A Massachusetts pharmacy offers multi-drug-single-dose solid oral compliance packaging for patients receiving stable daily medicines. It has appropriate staff training, compatible medication packaging, labeling and controlled-substance accounting policies. Which actions comply with 247 CMR 9.08? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Package a 30-day supply of daily Schedule IV and Schedule VI tablets together in compliant multi-drug-single-dose cells when the medications are compatible and all other rules are met.",
        "why": "Correct. Section 9.08(3) prohibits Schedule II and III medicines and PRN orders in multi-drug-single-dose packs, but does not categorically bar appropriate Schedule IV and VI daily medication together; the pharmacy must meet all packaging, compatibility and labeling requirements."
      },
      {
        "text": "Include a Schedule II stimulant in the same multi-drug-single-dose cells if the patient has authorized monthly refills and the packet is tamper-evident.",
        "why": "Incorrect. Section 9.08(3)(b) categorically prohibits Schedule II and III drugs in multi-drug-single-dose packs; Schedule II also is generally not refillable. Tamper-evidence does not create an exception."
      },
      {
        "text": "Supply a 90-day supply in multi-drug-single-dose packages if the medicines' commercial expiration dates are at least one year away.",
        "why": "Incorrect. Section 9.08(3)(a) caps these packages at 60 days, and the packaging BUD is independently limited by §9.08(5)(d) to the earliest manufacturer's expiration or 60 days. A manufacturer's long expiry does not remove these caps."
      },
      {
        "text": "When a pharmacy previously dispensed a multi-drug pack to a patient and one drug is discontinued, it may accept that pack, remove the discontinued medicine and relabel/re-dispense the remaining medicines to that SAME patient while recording the pharmacist's changes.",
        "why": "Correct. Section 9.08(4)(a) permits limited return and repackaging for the original patient after a therapy change, with updated labeling and documented pharmacy accountability. Removed medicines must not return to stock or be dispensed to a different patient."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.08(1), (3)(a)–(c), (4)(a)–(c), (5)(d) (Compliance Packaging, effective Dec. 6, 2024)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "Massachusetts multi-drug-single-dose packaging excludes Schedules II–III and PRN medications, is limited to 60 days, and allows carefully documented same-patient repackaging after therapy changes."
  },
  {
    "id": "E30-171",
    "set": 35,
    "area": 1,
    "kind": "single",
    "topic": "Board subpoena noncompliance as independent professional disciplinary ground",
    "topicKey": "board-discipline",
    "stem": "During a Massachusetts Board of Registration in Pharmacy investigation, a pharmacist is lawfully requested to produce specified pharmacy records and appear in response to a valid Board subpoena. The pharmacist refuses without cause because no final disciplinary order has yet been entered. Which assessment is correct?",
    "choices": [
      {
        "text": "The pharmacist need cooperate only if the Board has first imposed formal discipline after a full merits hearing.",
        "why": "Incorrect. 247 CMR 10.03(1)(q) expressly addresses failure without cause to cooperate with the Board's request or subpoena; the duty can arise DURING investigation and is not conditional on a prior final sanction."
      },
      {
        "text": "No disciplinary exposure exists if the pharmacy owner, rather than the pharmacist, controls the physical record storage.",
        "why": "Incorrect. The legal duty attaches to a licensee's cooperation and legally available records/information. Employment ownership alone is not a categorical basis to refuse lawful Board investigatory requests without cause."
      },
      {
        "text": "Refusing to appear or furnish legally entitled records is permissible until the pharmacist has received a criminal court subpoena.",
        "why": "Incorrect. The pharmacy Board has its own regulatory investigation and subpoena authority. Section 10.03(1)(q) does not require a separate criminal case or court-issued criminal subpoena."
      },
      {
        "text": "Without cause, failure to cooperate with Board requests or a valid subpoena may itself support discipline, even before the Board adjudicates the underlying allegation.",
        "why": "Correct. Section 10.03(1)(q) identifies failure to cooperate, appear, respond to subpoena, or furnish information to which the Board is legally entitled as independent grounds for action. The pharmacist should arrange lawful and confidential production rather than ignore the investigative demand."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 10.03(1)(q) (grounds for discipline, effective Jan. 9, 2025); 247 CMR 9.24(1)–(3) (Board pharmacy inspections and records)",
    "url": "https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download",
    "verified": "2026-11-16",
    "note": "Failure without cause to cooperate with a lawful Massachusetts Board request or subpoena can independently support discipline; a final underlying order is not required first."
  },
  {
    "id": "E30-172",
    "set": 35,
    "area": 2,
    "kind": "single",
    "topic": "FDA Medication Guides: inpatient professional administration and home self-administration distinction",
    "topicKey": "medication-guides",
    "stem": "A Massachusetts hospital uses a medication whose FDA-approved labeling requires a Medication Guide. One adult patient receives doses administered by nurses during inpatient admission; a different patient is discharged home with a prescription that the patient will self-administer. No special Medication Guide REMS/ETASU term applies, neither patient has requested a guide during inpatient care, and no practitioner withholding instruction exists. Which is the best description of FDA's CURRENT guidance?",
    "choices": [
      {
        "text": "Every nurse-administered inpatient dose must legally be accompanied by a new physical Medication Guide, without exception or FDA enforcement discretion.",
        "why": "Incorrect. FDA's published Medication Guide distribution guidance provides enforcement discretion for medication dispensed to a healthcare professional for inpatient administration absent a more specific requirement; automatic guide distribution at every such dose is not the agency's stated policy."
      },
      {
        "text": "FDA generally exercises enforcement discretion for routine healthcare-professional administration in an inpatient setting, but a Medication Guide is ordinarily provided when dispensed directly for outpatient self-administration at home.",
        "why": "Correct. FDA Medication Guides distribution guidance and 21 CFR 208.24(e) distinguish inpatient professional administration from direct patient/agent outpatient dispensing. The inpatient practice reflects a nonbinding FDA enforcement-discretion policy, not an amendment of all Part 208 legal language. REMS-specific distribution terms and patient requests must still be honored."
      },
      {
        "text": "Once the patient has been hospitalized, no Medication Guide is required for any subsequently dispensed take-home supply because the first dose occurred in a hospital.",
        "why": "Incorrect. The status of the particular dispensing matters. A take-home outpatient prescription intended for self-administration generally requires a Medication Guide even if earlier doses were administered by hospital staff."
      },
      {
        "text": "Hospital inpatient distribution discretion automatically eliminates all drug-specific REMS requirements to review or provide Medication Guides.",
        "why": "Incorrect. FDA's guidance expressly preserves Medication Guide distribution required by a product-specific REMS with elements to assure safe use. A general enforcement-discretion policy does not void those conditions."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "21 CFR 208.24(e), 208.26(b); FDA Guidance 'Medication Guides—Distribution Requirements and Inclusion in REMS' (nonbinding enforcement discretion), and FDA Medication Guides Distribution for Health Care Professionals (Mar. 2020)",
    "url": "https://www.fda.gov/drugs/drug-safety-and-availability/questions-and-answers-guidance-industry-medication-guides-distribution-requirements-and-inclusion",
    "verified": "2026-11-16",
    "note": "FDA generally exercises Medication Guide distribution discretion for inpatient professional administration, but outpatient take-home dispensing ordinarily requires the Guide; drug-specific REMS terms and patient requests remain important."
  },
  {
    "id": "E30-173",
    "set": 35,
    "area": 2,
    "kind": "multi",
    "topic": "Pharmacy referral kickbacks and pharmacy-branded blank prescription forms",
    "topicKey": "professional-ethics-referrals",
    "stem": "A Massachusetts community pharmacist is negotiating with a nursing-home admissions coordinator who offers to steer residents' prescriptions to the pharmacy for a monthly referral payment. The pharmacist also considers supplying medical offices with blank prescription forms printed with the pharmacy's contact details. Under 247 CMR 9.01, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacist may not pay the facility employee for referral or generation of pharmacy business, even if residents retain freedom to choose another pharmacy.",
        "why": "Correct. 247 CMR 9.01(11) forbids remuneration or things of value to or from specified healthcare facility owners or employees IN RETURN FOR referral or pharmacy-related business. A theoretical choice to opt out does not legalize the referral payment."
      },
      {
        "text": "The payment is permitted if it is described in the contract as a consulting fee for generating new prescriptions, regardless of the actual referral purpose.",
        "why": "Incorrect. The regulation covers direct or indirect payment in exchange for referral/business; relabeling the same quid pro quo as a consulting fee does not change its purpose. Legitimate independent services would require their own analysis rather than this stated referral bargain."
      },
      {
        "text": "The pharmacist may freely distribute blank prescription forms bearing that pharmacy's name because the forms are not signed prescriptions yet.",
        "why": "Incorrect. Section 9.01(14) expressly forbids a pharmacy licensee from giving practitioners blank prescription forms that refer to a pharmacist or pharmacy. Unsigned status is not an exception."
      },
      {
        "text": "The pharmacist should not give practitioners blank prescription forms that refer to the pharmacy, regardless of whether a particular patient has yet been selected.",
        "why": "Correct. The independent prohibition in §9.01(14) applies to the act of supplying such preprinted blank forms; it is separate from the ban on referral remuneration."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.01(11),(14) (referral remuneration and blank pharmacy-identified prescription forms; effective Dec. 6, 2024)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-16",
    "note": "Massachusetts forbids referral kickbacks to healthcare facility employees and providing practitioners with pharmacy-identified blank prescription forms, even without a completed patient prescription."
  },
  {
    "id": "E30-174",
    "set": 35,
    "area": 3,
    "kind": "single",
    "topic": "Narcolepsy medicine scheduling: Sunosi and Provigil versus Wakix",
    "topicKey": "drug-schedule-identification",
    "stem": "A Massachusetts pharmacist receives otherwise valid prescriptions for Sunosi (solriamfetol), Provigil (modafinil) and Wakix (pitolisant). Which description correctly matches federal DEA and corresponding Massachusetts schedules in November 2026?",
    "choices": [
      {
        "text": "All three drugs are Schedule IV because all treat excessive daytime sleepiness associated with narcolepsy.",
        "why": "Incorrect. Solriamfetol and modafinil are Schedule IV, but pitolisant is not a federally controlled substance and is a Massachusetts Schedule VI prescription drug. Indication does not make scheduling uniform."
      },
      {
        "text": "Sunosi Schedule II, Provigil Schedule IV and Wakix Schedule VI.",
        "why": "Incorrect. Solriamfetol is federally Schedule IV under 21 CFR 1308.14(f), not Schedule II. The other two classifications do not salvage this option."
      },
      {
        "text": "Sunosi and Provigil are Schedule IV federally and in Massachusetts; Wakix is federally unscheduled and Massachusetts Schedule VI.",
        "why": "Correct. 21 CFR 1308.14(f)(13) controls solriamfetol and §1308.14(f)(7) modafinil in Schedule IV. FDA's 2026 Wakix labeling lists pitolisant as an unscheduled prescription product; Massachusetts Schedule VI covers prescription drugs outside federal/MA Schedules I–V."
      },
      {
        "text": "Wakix is Schedule III and both Sunosi and Provigil are federal Schedule V because treatment of narcolepsy is less restrictive than treating ADHD.",
        "why": "Incorrect. The applicable federal Schedule IV listings expressly include solriamfetol and modafinil, and pitolisant is unscheduled. Comparing indications cannot override the DEA list."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "21 CFR 1308.14(f)(7),(14) (modafinil, solriamfetol; renumbered Nov. 12, 2026); 105 CMR 700.002(D),(F); FDA Wakix/pitolisant labeling updated Feb. 2026 (DEA Schedule: None)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.14",
    "verified": "2026-11-16",
    "note": "Solriamfetol/Sunosi and modafinil/Provigil are federal/MA Schedule IV; pitolisant/Wakix is federally unscheduled and Massachusetts Schedule VI."
  },
  {
    "id": "E30-175",
    "set": 35,
    "area": 4,
    "kind": "multi",
    "topic": "USP <800> and <797> placement: Category 1 hazardous CSP in a C-SCA versus Category 2",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts sterile compounding pharmacy has an appropriately designed negative-pressure containment segregated compounding area (C-SCA) with a suitable ISO Class 5 containment primary engineering control and qualified personnel. It plans to compound non-antineoplastic and antineoplastic hazardous sterile preparations under the current USP <797> Category system. Which statements are supported by USP <800> and its January 2026 technical FAQ? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Any Category 2 or 3 hazardous CSP may be compounded routinely in the C-SCA whenever the ISO 5 containment hood is certified.",
        "why": "Incorrect. USP <800> FAQ #5 explains that the earlier low/medium risk wording now maps to Category 1 only in a C-SCA; ISO 5 performance alone does not make the segregated area eligible for Categories 2 or 3."
      },
      {
        "text": "Category 1 hazardous CSPs, including sterile-to-sterile and nonsterile-to-sterile preparations, may be compounded in a compliant C-SCA when all applicable containment and USP <797> requirements are met.",
        "why": "Correct. USP <800> FAQ #5 explicitly recognizes Category 1 HD CSPs of both described component types in a C-SCA. The pharmacy must satisfy the negative-pressure containment, ISO 5 C-PEC and applicable Category 1 BUD/quality limits."
      },
      {
        "text": "For Category 2 hazardous CSPs, the pharmacy must use an appropriately classified compliant cleanroom suite rather than treating the C-SCA as universally sufficient.",
        "why": "Correct. Under the current USP <797> Category classification and USP <800> FAQ #5, Category 2 HD CSPs do not qualify for the C-SCA-only pathway. A compliant sterile hazardous cleanroom suite is necessary for those Category 2 operations."
      },
      {
        "text": "The old 'low-risk/medium-risk' terminology remains the current USP <797> primary classification, so the Category 1/2/3 distinction must be ignored.",
        "why": "Incorrect. USP <797> replaced older risk-level labels with Categories 1, 2 and 3. USP's 2026 FAQ #5 explicitly explains how to apply the current categories to the legacy wording in <800>."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "Current USP <797> Category 1–3 framework (official Nov. 1, 2023); USP <800> §5 and Jan. 21, 2026 FAQs Q5 (compendial applicability and Category 1 HD CSPs in C-SCA, informational technical support); 247 CMR 9.01(3)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_800_FAQs_January2026.pdf?version=0",
    "verified": "2026-11-16",
    "note": "A compliant C-SCA can be used for Category 1 hazardous CSPs (including nonsterile-to-sterile), not routine Category 2/3 hazardous CSPs. Apply the current <797> categories."
  },
  {
    "id": "E30-176",
    "set": 36,
    "area": 1,
    "kind": "single",
    "topicKey": "technician-scope",
    "topic": "New telephone Schedule VI prescription: certified technician reception versus ordinary technician and trainee",
    "stem": "At a Massachusetts community pharmacy, a prescriber's authorized agent calls in a NEW, otherwise valid Schedule VI amlodipine prescription. A certified pharmacy technician with a current Massachusetts technician license, a noncertified licensed technician and a licensed trainee are present. The on-duty pharmacist approves appropriate delegation and will personally perform DUR and final dispensing validation. Who MAY receive and record this new oral information as described?",
    "choices": [
      {
        "text": "The certified technician may receive the new or omitted prescription information with the on-duty pharmacist's approval, but may not independently resolve therapy changes or validate final dispensing.",
        "why": "Correct. 247 CMR 8.04(4)(c) authorizes a licensed certified technician, identifying themself as such and with pharmacist approval, to receive NEW or omitted prescription information unless other law prohibits it. The delegated intake does not permit therapy clarification, counseling, DUR or final validation under §8.04(4)(e) and 247 CMR 9.04(1)."
      },
      {
        "text": "The trainee may take the new prescription by telephone if the supervising pharmacist signs it after the call.",
        "why": "Incorrect. 247 CMR 8.03(4)(c) expressly prohibits a technician trainee from taking prescriptions over the telephone. Later pharmacist validation does not transform prohibited telephone reception into a lawful trainee task."
      },
      {
        "text": "The noncertified licensed technician may independently accept any NEW oral Schedule VI order because ordinary refill-authorizations and new-prescription intake have identical scope.",
        "why": "Incorrect. 247 CMR 8.02 allows ordinary licensed technicians to request and receive refill authorization for an unchanged Schedule VI prescription subject to restrictions; §8.04(4)(c) grants the additional specified NEW-information reception to certified technicians. New orders and unchanged refills are not the same activity."
      },
      {
        "text": "No technician may record new Schedule VI oral information, because federal DEA Schedule II oral-emergency restrictions apply to every Massachusetts Schedule VI medicine.",
        "why": "Incorrect. Conventional amlodipine is Massachusetts Schedule VI and is not federal Schedule II. The certified-technician delegation provision applies to new information for otherwise lawful orders; federal emergency Schedule II prescription limitations are not a universal ban on Schedule VI technician intake."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 8.02(6), 8.03(4)(c), 8.04(4)(c),(e); 247 CMR 9.04(1); 105 CMR 721.030 (Massachusetts oral prescription format)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-17",
    "note": "A licensed certified technician may, with pharmacist approval, take new or omitted lawful prescription information; an ordinary technician's narrower unchanged refill role and a trainee's explicit telephone ban are different. Final clinical validation remains pharmacist-only."
  },
  {
    "id": "E30-177",
    "set": 36,
    "area": 2,
    "kind": "single",
    "topicKey": "prescriber-authority",
    "topic": "New nurse practitioner with valid individual MCSR and DEA but no required supervised prescribing guidelines",
    "stem": "A Massachusetts-licensed certified nurse practitioner has only nine months of qualifying prescriptive-practice experience. The NP has an active individual Massachusetts Controlled Substances Registration and DEA registration for Schedule III. An otherwise authentic Schedule III prescription is sent for a patient within the NP's usual specialty. When the pharmacist calls about an unrelated discrepancy, the NP volunteers that no mutually agreed written prescriptive-practice guidelines or qualified healthcare professional supervision have ever been established. No special exception applies. What is the best dispensing decision?",
    "choices": [
      {
        "text": "Dispense because possession of both individual registration numbers automatically establishes independent prescriptive practice.",
        "why": "Incorrect. MCSR and DEA registrations are necessary for the applicable controlled schedules, but 244 CMR 4.06 also requires supervised prescriptive practice with mutually agreed guidelines during the initial qualifying period for a CNP. The prescriber has explicitly disclosed the missing legal practice condition."
      },
      {
        "text": "Treat the supervising physician's DEA number as a substitute for the NP's registered prescriber identity, without resolving the missing guidelines.",
        "why": "Incorrect. Borrowing another practitioner's DEA identifier is not a remedy for a missing required supervised-prescribing arrangement. The pharmacist should not alter the prescriber identity or overlook a known scope deficiency."
      },
      {
        "text": "Dispense because a pharmacist is never required to inquire about NP supervision, even after receiving an explicit statement that required prescribing guidelines do not exist.",
        "why": "Incorrect. Pharmacists generally are not required to independently investigate a qualifying NP's independent-practice status merely because a supervisor name is absent, but this pharmacist has affirmative information that the still-supervised NP lacks the required practice arrangement. Ordinary lawful-authority and corresponding-responsibility checks still apply."
      },
      {
        "text": "Do not dispense under the disclosed circumstances until authorized prescriptive practice is established or an appropriately authorized practitioner issues a valid prescription.",
        "why": "Correct. Under 244 CMR 4.06, a CNP below the supervised experience threshold must practice with the required mutually agreed prescriptive guidelines and qualified healthcare professional supervision. Knowing those conditions are absent is materially different from merely not seeing a supervisor's name on a valid independent NP prescription; valid DEA/MCSR numbers alone cannot supply professional scope."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "244 CMR 4.07(2)(c) (NP supervised prescriptive-practice guidelines/transition); M.G.L. c.112 §80E; 105 CMR 700.004; 21 CFR 1306.04(a); MA DPH Circular DCP 21-10-111",
    "url": "https://www.mass.gov/regulations/244-CMR-406-prescriptive-authority",
    "verified": "2026-11-17",
    "note": "Separate individual DEA/MCSR registration from state-law prescriber authorization. A newly prescribing NP who still needs guidelines/supervision cannot cure their known absence by presenting valid controlled-drug registration numbers."
  },
  {
    "id": "E30-178",
    "set": 36,
    "area": 2,
    "kind": "multi",
    "topicKey": "controlled-prescriptions",
    "topic": "Controlled-prescription red flags despite authentic registration and an established patient relationship",
    "stem": "A Massachusetts pharmacist reviews four separate Schedule II–IV controlled prescriptions issued by credentialed prescribers for existing patients. Each signature and DEA number is authentic. The pharmacist has information about whether the order is clinically and legally legitimate, and will document relevant investigation. Under 247 CMR 9.15 and DEA's corresponding responsibility, which actions or conclusions are defensible? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Fill a Schedule II prescription without further review whenever its DEA number is active, because registration conclusively proves legitimate medical purpose.",
        "why": "Incorrect. 247 CMR 9.15(2) and 21 CFR 1306.04(a) impose the pharmacist's own corresponding responsibility. Registration and signature authenticity do not automatically establish legitimate purpose or safe dispensing when clinical red flags exist."
      },
      {
        "text": "Investigate an unexpectedly early opioid refill with conflicting medical history, consult the prescriber as needed and withhold dispensing if the legitimate purpose cannot be established.",
        "why": "Correct. A genuine early refill plus inconsistent history warrants professional judgment, clarification and documentation. The pharmacist must determine legitimacy and lawfulness before filling, but no automatic refusal rule is inferred solely from the early timing."
      },
      {
        "text": "Automatically reject every cash-paid opioid prescription, even when the prescriber verifies the legitimate purpose, the patient relationship is established and no unresolved concern remains.",
        "why": "Incorrect. Cash payment may be a red flag when viewed in context but neither 247 CMR 9.15 nor DEA corresponding-responsibility rules make all cash purchases unlawful. Assess actual concerns rather than impose an invented categorical ban."
      },
      {
        "text": "After resolving a plausible red flag with credible clinical documentation and appropriate verification, dispense an otherwise lawful prescription if professional judgment supports legitimate purpose and safety.",
        "why": "Correct. The law requires a genuine decision based on legitimate purpose, valid relationship, authenticity and legal compliance; it does not require permanent denial of a resolved red flag. The pharmacist should document the reasoning and perform clinical DUR."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 9.15(2)(a)–(d), 9.17 (prospective DUR); 21 CFR 1306.04(a); Massachusetts Board advisory 'Controlled Substance Prescriptions' (revised 2025), discussion of red flags and independent pharmacy judgment",
    "url": "https://www.mass.gov/doc/controlled-substance-prescriptions-pdf/download",
    "verified": "2026-11-17",
    "note": "A genuine patient relationship, verified DEA number and authentic signature do not eliminate the pharmacist's duty to investigate credible controlled-drug red flags. A resolved red flag is not necessarily grounds for automatic refusal."
  },
  {
    "id": "E30-179",
    "set": 36,
    "area": 3,
    "kind": "single",
    "topicKey": "cii-partial-fills",
    "topic": "Patient-requested Schedule II remainder at originating pharmacy within 30 days versus expired stock-shortage clock",
    "stem": "On November 3, 2026, an authorized in-state prescriber issues a valid electronic Schedule II prescription for 60 tablets. On November 4, the patient asks the pharmacy to dispense only 20 tablets even though all 60 are in stock; the pharmacist properly documents the patient-requested partial fill. On November 22, the patient asks for the remaining 40 tablets at the SAME pharmacy, and the prescription remains otherwise valid. No stock shortage, LTCF status or hospice exception applies. What may the pharmacist do under current Massachusetts law?",
    "choices": [
      {
        "text": "Dispense the remaining 40 tablets if federal conditions and documentation are satisfied, because a patient-requested partial fill may be completed by the original pharmacy within 30 days of the prescription issue date.",
        "why": "Correct. M.G.L. c.94C §18(d¾) and 105 CMR 721.055(B) permit patient-requested remainders only at the original pharmacy and no later than 30 days from issue, with documentation under subsection (C). November 22 is inside 30 days of November 3. This is NOT a partial fill caused by insufficient stock."
      },
      {
        "text": "Treat the balance as void immediately after the first smaller dispense because the 2016 DPH circular still controls despite the later amendment.",
        "why": "Incorrect. The older 2016 DPH circular's remainder-void wording was superseded; 2018 statutory amendments and current 105 CMR 721.055(B) expressly permit the remaining balance to be dispensed upon patient request at the original pharmacy within the issue-date limit."
      },
      {
        "text": "Refuse the balance because the 72-hour completion limit for a Schedule II stock shortage governs every type of partial fill.",
        "why": "Incorrect. The 72-hour federal shortage pathway addresses dispensing LESS than the full quantity because the pharmacy cannot supply it. Here full stock was available and the patient affirmatively requested less; 105 CMR 721.055's separate remainder rule governs."
      },
      {
        "text": "Direct the patient to any other licensed pharmacy to obtain the remaining 40 tablets under the first pharmacy's partial-fill record.",
        "why": "Incorrect. Section 721.055(B)(1) and c.94C §18(d¾) specify that ONLY the pharmacy which originally dispensed the smaller quantity may dispense the remaining portion under this patient-requested pathway."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.94C §18(d¾) (amended by Acts 2018 c.208); 105 CMR 721.055(A)–(C) (effective Sept. 27, 2024); 21 CFR 1306.13; DPH Circular DCP 18-10-104 superseding 2016 Circular DCP 16-12-665",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-17",
    "note": "A Schedule II patient-requested partial fill differs from a pharmacy stock-shortage partial. The original pharmacy may dispense the patient-requested remainder within 30 days after issue, subject to federal rules and required documentation."
  },
  {
    "id": "E30-180",
    "set": 36,
    "area": 4,
    "kind": "multi",
    "topicKey": "controlled-inventory",
    "topic": "Expired pharmacy controlled stock: reverse distributor transfer, DEA Form 41 destruction and distinct Forms 106/222",
    "stem": "A Massachusetts DEA-registered retail pharmacy identifies expired Schedule II and Schedule III stock that remains in its own inventory; there is NO theft, loss or damage. It plans to transfer the expired stock to an appropriately registered reverse distributor for lawful destruction and to replenish usable Schedule II stock from a wholesaler. Which federal controlled-substance procedures are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Document the lawful transfer of expired controlled stock to the registered reverse distributor; the reverse distributor performing destruction completes its required DEA Form 41 record.",
        "why": "Correct. Under 21 CFR 1317.05 and 1304.21, a practitioner registrant may transfer lawfully held expired controlled inventory to a reverse distributor at its registered location, with shipment and transfer records. The reverse distributor documents destruction on DEA Form 41, rather than treating a pharmacy's transfer invoice as the reverse distributor's destruction record."
      },
      {
        "text": "The retail pharmacy must report the ordinary expired stock on DEA Form 106 within one business day, even though no theft or significant loss occurred.",
        "why": "Incorrect. DEA Form 106 is for theft or significant loss under 21 CFR 1301.76(b), not an ordinary accountable inventory of expired medication awaiting lawful reverse distribution. The pharmacy still keeps complete inventory/transfer records."
      },
      {
        "text": "Use a compliant paper DEA Form 222 or an authorized electronic CSOS order to acquire replacement Schedule II stock, independently of any destruction documentation.",
        "why": "Correct. DEA Form 222 or the corresponding CSOS process is an ordering/transfer authorization for Schedule I or II acquisitions under 21 CFR Part 1305; it is separate from records for sending expired stock to a reverse distributor."
      },
      {
        "text": "DEA Form 41 replaces all Schedule II ordering forms and automatically authorizes the pharmacy to acquire the exact quantity it discarded.",
        "why": "Incorrect. Form 41 documents destruction, not permission to order new Schedule II products. Schedule II ordering still uses the authorized Part 1305 mechanism, and inventory disposal does not generate an automatic replacement allotment."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 CFR 1317.05(a)(2), 1317.10, 1304.21(d)–(e), 1305.03–1305.13, 1301.76(b); DEA Disposal Q&A (Forms 41/106/222 and reverse distributor responsibilities)",
    "url": "https://www.deadiversion.usdoj.gov/faq/disp-destr-faq.html",
    "verified": "2026-11-17",
    "note": "Form 106 reports theft/significant loss, Form 41 documents controlled-substance destruction (reverse distributor when that entity destroys), and Form 222/CSOS orders Schedule II stock. A registrant's transfer to a reverse distributor requires its own records."
  },
  {
    "id": "E30-181",
    "set": 37,
    "area": 1,
    "kind": "single",
    "topicKey": "intern-education",
    "topic": "Board credit for another state's supervised pharmacy internship documented only by an employer's log",
    "stem": "A Massachusetts pharmacist-licensure candidate earned 600 supervised intern hours at a licensed pharmacy in another state, before moving to Massachusetts. The candidate presents a signed employer time sheet, but NO affidavit or certificate from the state where the experience was acquired confirming that those hours were approved in that jurisdiction. All other intern-licensure and school requirements are satisfied. What does 247 CMR 8.01(11) allow the Massachusetts Board to do?",
    "choices": [
      {
        "text": "Automatically accept the 600 hours because a signed time sheet is the exact proof required for all out-of-state internship credit.",
        "why": "Incorrect. Section 8.01(11) expressly contemplates an AFFIDAVIT or certificate of approval from the JURISDICTION where the experience was acquired, indicating that the experience was duly approved there. A supervisor's time sheet alone is not the specified jurisdictional approval."
      },
      {
        "text": "Reject the hours permanently because Massachusetts can never approve internship experience acquired outside the Commonwealth.",
        "why": "Incorrect. Section 8.01(11) expressly provides a route for the Board to GRANT credit for otherwise qualified out-of-state experience when appropriate approval proof from the jurisdiction is supplied. It is not categorically disallowed."
      },
      {
        "text": "Consider granting credit once the candidate produces an affidavit or certificate of approval issued by the jurisdiction where the hours were earned; credit is not automatic on an employer log alone.",
        "why": "Correct. Under 247 CMR 8.01(11), the Board MAY grant credit for out-of-state pharmacy internship experience when documentation issued by the other jurisdiction indicates those hours were duly approved there. The intern should obtain that official proof and request Board acceptance."
      },
      {
        "text": "Accept the hours only if the candidate first completes another 600 hours in Massachusetts, because the Board must match each out-of-state hour one-to-one.",
        "why": "Incorrect. Section 8.01(11) imposes no universal 1:1 Massachusetts match. The issue is the Board's discretionary credit and the other state's official internship approval; overall licensure hour requirements are evaluated separately."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 8.01(1),(9),(11), corrected Apr. 25, 2025 (out-of-state internship credit and jurisdiction-issued approval proof)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-17",
    "note": "Out-of-state supervised pharmacy internship experience may receive Massachusetts Board credit, but present the OTHER jurisdiction's affidavit/certificate indicating duly approved hours; employer hours alone do not guarantee credit."
  },
  {
    "id": "E30-182",
    "set": 37,
    "area": 2,
    "kind": "multi",
    "topicKey": "naloxone-dispensing",
    "topic": "OTC naloxone versus prescription-labeled naloxone under statewide standing order for a third party",
    "stem": "An adult in Massachusetts wants naloxone to help a neighbor at risk of opioid overdose. A grocery store has FDA-labeled OTC naloxone nasal spray on its shelf. A nearby pharmacy has both the same OTC-labeled product and a DIFFERENT naloxone presentation labeled 'Rx only.' The pharmacy participates in the current Massachusetts statewide naloxone standing order. Which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The adult may purchase the OTC-labeled naloxone directly without an individual prescription; Massachusetts Drug Control Program prescribing/controlled-substance rules do not apply to activities involving that OTC product.",
        "why": "Correct. The Massachusetts DPH Drug Control Program's October 10, 2024 advisory distinguishes OTC naloxone products from prescription naloxone. An FDA-approved OTC-labeled product may be bought at ordinary retail without an individual or standing-order prescription; no MCSR is required for OTC-product activities."
      },
      {
        "text": "Because naloxone is a single active ingredient, all its formulations require identical pharmacy-only controlled-prescription processing even when FDA approves one presentation for OTC sale.",
        "why": "Incorrect. FDA labeling makes OTC and Rx-only products legally distinct under Massachusetts' 2024 DPH advisory. A product labeled OTC does not automatically inherit prescription-only obligations of a separate Rx-labeled presentation."
      },
      {
        "text": "A Massachusetts pharmacy may dispense Rx-labeled naloxone for use by another person under the statewide standing order, without a separate patient-specific prescription for the neighbor, while applying the prescription-pathway rules.",
        "why": "Correct. M.G.L. c.94C §19B and Board Policy 2024-01 allow an individual to obtain prescription naloxone for a person at risk, and the statewide standing order serves as the required authorizing prescription. Product-specific counseling, labeling and related prescription reporting rules still apply."
      },
      {
        "text": "The existence of a retail OTC naloxone alternative automatically cancels Massachusetts' statewide standing order for Rx-labeled naloxone and makes prescription insurance billing unlawful.",
        "why": "Incorrect. The DPH and Board expressly maintain the standing-order pathway for Rx-labeled naloxone despite some OTC products. Eligible pharmacy prescriptions under the standing order can be processed through insurance subject to plan terms."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "M.G.L. c.94C §§19B–19C; MA DPH Advisory 'DCP Regulations and Over-The-Counter Naloxone' (Oct. 10, 2024); Board Policy 2024-01 revised Feb. 6, 2025; 2026 statewide naloxone standing order",
    "url": "https://www.mass.gov/news/dcp-regulations-and-over-the-counter-naloxone",
    "verified": "2026-11-17",
    "note": "OTC-labeled naloxone can be purchased without a prescription, whereas Rx-labeled naloxone may still be dispensed under the Massachusetts statewide standing order, including for someone seeking to help a third party."
  },
  {
    "id": "E30-183",
    "set": 37,
    "area": 2,
    "kind": "single",
    "topicKey": "rems",
    "topic": "Current SPRAVATO REMS: pharmacy-to-certified-setting distribution versus patient take-home nasal spray",
    "stem": "A Massachusetts community pharmacy is certified under the current SPRAVATO REMS. It receives an otherwise legitimate esketamine (SPRAVATO) prescription for an adult patient whose outpatient psychiatric clinic is ALSO REMS-certified. The patient requests that the pharmacy mail the sealed product to the patient's home for unsupervised self-administration, avoiding travel. The prescribing clinic instead offers to supervise administration on site. What is the legally appropriate REMS decision?",
    "choices": [
      {
        "text": "Mail the product directly to the patient's home if the pharmacist provides a Medication Guide and a telephone number for questions.",
        "why": "Incorrect. The current SPRAVATO REMS requires certified pharmacies to dispense it ONLY to certified healthcare settings. Direct patient home dispensing cannot be substituted by counseling or an enclosed Medication Guide."
      },
      {
        "text": "Dispense or ship to the REMS-certified healthcare setting for observed self-administration and required professional monitoring; do not dispense for unsupervised home use.",
        "why": "Correct. Current SPRAVATO labeling and REMS require the product to be dispensed and administered only in certified healthcare settings, with patients self-administering under direct observation and monitoring by providers for at least two hours. The pharmacy must verify the destination's certification."
      },
      {
        "text": "Dispense to any licensed clinic, even if it is not REMS-certified, because the prescriber's own DEA registration satisfies the REMS certification.",
        "why": "Incorrect. DEA registration for Schedule III esketamine and healthcare-setting SPRAVATO REMS certification are separate conditions. A pharmacy participating in the REMS may dispense only to a certified healthcare setting."
      },
      {
        "text": "Give the patient one nasal device for unsupervised use and reserve two devices for the clinic because only the first dose needs onsite observation.",
        "why": "Incorrect. The REMS does not create a routine first-dose-only supervised requirement. Treatment sessions must occur in certified settings with observation/monitoring, so distributing a patient take-home device violates the stated program safeguards."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "FDA SPRAVATO (esketamine) current prescribing information §5.5 (REMS), certified pharmacy/healthcare setting and two-hour monitoring; 21 CFR 208 and current FDA REMS database",
    "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d81a6a79-a74a-44b7-822c-0dfa3036eaed",
    "verified": "2026-11-17",
    "note": "SPRAVATO is Schedule III but also subject to a product-specific REMS: certified pharmacies supply ONLY certified healthcare settings, where the patient self-administers under direct observation and at least two hours' monitoring."
  },
  {
    "id": "E30-184",
    "set": 37,
    "area": 3,
    "kind": "single",
    "topicKey": "masspat",
    "topic": "MassPAT prescriber lookup: inpatient administered benzodiazepine order versus discharge prescription",
    "stem": "A Massachusetts hospital prescriber orders lorazepam (a Schedule IV benzodiazepine) to be administered by nurses to an admitted inpatient during hospitalization. On discharge, the prescriber issues a separate outpatient lorazepam prescription that may be filled at a community pharmacy. The hospital's pharmacy later dispenses the outpatient prescription to the departing patient. Assume no special emergency exception and all other requirements are met. Which interpretation of MassPAT obligations is correct?",
    "choices": [
      {
        "text": "MassPAT lookup is exempt for BOTH orders because the patient was admitted when the drug was first considered, and hospital outpatient prescriptions are not reportable.",
        "why": "Incorrect. Massachusetts DPH PMP FAQ expressly states the inpatient-medication-order exception applies only to doses administered in the healthcare setting, NOT discharge outpatient prescriptions. A covered outpatient pharmacy dispensing can also trigger dispensing-report requirements."
      },
      {
        "text": "The physician must query MassPAT before every inpatient-administered lorazepam dose, but no query is needed before writing the outpatient discharge prescription.",
        "why": "Incorrect. This reverses the relevant distinction in the DPH FAQ: inpatient medication orders administered in the facility qualify for the exemption, whereas an outpatient prescription at discharge requires query before issuance."
      },
      {
        "text": "The pharmacist alone must query MassPAT before issuing the physician's discharge prescription; the physician has no MassPAT query duty when ordering benzodiazepines.",
        "why": "Incorrect. M.G.L. c.94C §24A imposes the specified QUERY responsibility on the PRESCRIBER before writing certain controlled prescriptions, including benzodiazepines, subject to exceptions. Separately, the dispensing pharmacy has its OWN reporting duties under 105 CMR 700.012."
      },
      {
        "text": "The inpatient-administered medication order qualifies for the inpatient MassPAT query exception; the discharge outpatient benzodiazepine prescription requires the prescriber to query MassPAT, and the pharmacy reports the covered outpatient dispensing.",
        "why": "Correct. The DPH MassPAT FAQ states discharge prescriptions that may be filled by a retail or hospital outpatient pharmacy are NOT covered by the inpatient administration exemption. Under c.94C §24A and 105 CMR 700.012, prescriber query and pharmacy submission are separate obligations."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §24A (prescriber query of PMP for benzodiazepines/narcotics); 105 CMR 700.012(A),(G) (dispenser reporting); MA DPH 'Prescription Monitoring Program frequently asked questions' question 'Opioid Rx’s to an inpatient at discharge'",
    "url": "https://www.mass.gov/info-details/prescription-monitoring-program-frequently-asked-questions",
    "verified": "2026-11-17",
    "note": "MassPAT's inpatient query exemption applies to medication orders administered in the facility, not an outpatient benzodiazepine prescription at discharge. Prescriber query and pharmacy daily dispensing reporting are different duties."
  },
  {
    "id": "E30-185",
    "set": 37,
    "area": 4,
    "kind": "multi",
    "topicKey": "sterile-hazardous-compounding",
    "topic": "USP <800> chemotherapy spill in patient-care area: trained response, readily available spill kit and hazardous waste",
    "stem": "During transport in a Massachusetts hospital oncology unit, a small container of a hazardous antineoplastic drug breaks, causing a visible spill. No one is injured yet, but trained hazardous-drug spill responders and an appropriately supplied spill kit are available. The hospital follows applicable USP <800> and hazardous-waste rules. Which steps are appropriate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Keep visitors and unprotected personnel away while trained designated workers promptly contain and clean the spill with appropriate hazardous-drug protective equipment and supplies.",
        "why": "Correct. USP <800> §16 requires hazardous drug spills to be contained and cleaned immediately by trained personnel using suitable protective equipment and spill-management supplies. An unprotected bystander should not be assigned the exposure."
      },
      {
        "text": "Allow nearby nurses to continue preparing and administering drugs directly through the contaminated area until routine housekeeping is available at the end of the shift.",
        "why": "Incorrect. USP <800> calls for prompt spill control; continuing routine work in the exposed area risks spreading contamination. Restrict traffic and initiate trained response rather than waiting until a normal end-of-shift cleaning cycle."
      },
      {
        "text": "Place contaminated absorbents and protective equipment into the appropriate hazardous-drug waste stream, and document and evaluate any personnel exposure as required by facility procedures.",
        "why": "Correct. Spill cleanup is not ordinary trash disposal: contaminated materials must be disposed of in accordance with applicable hazardous-drug/waste policies. The pharmacy and facility must maintain spill documentation and evaluate possible employee exposure."
      },
      {
        "text": "Flush contaminated materials into the nearest sink because a drug dissolved in water is no longer a hazardous substance and requires no spill records.",
        "why": "Incorrect. Dilution does not erase a drug's hazardous status. USP <800> and hazardous-waste requirements do not authorize routine sink disposal of hazardous-drug spill waste; the response and any exposure require appropriate procedures."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Current USP <800> §16 (Spill Control) and §15 (Deactivating, Decontaminating, Cleaning and Disinfecting); USP <800> FAQs Jan. 21, 2026; 247 CMR 9.01(3), applicable federal/state hazardous waste requirements",
    "url": "https://www.usp.org/compounding/general-chapter-hazardous-drugs-handling-healthcare",
    "verified": "2026-11-17",
    "note": "Hazardous-drug spills need prompt trained containment, appropriate PPE and readily available kits. Isolate the area, handle contamination as hazardous waste, and document/evaluate any exposed personnel; routine housekeeping or drains are not substitutes."
  },
  {
    "id": "E30-186",
    "set": 38,
    "area": 1,
    "kind": "single",
    "topicKey": "workforce-supervision",
    "topic": "Category 2 sterile-compounding technician: overdue ongoing aseptic competency despite passing initial test",
    "stem": "A Massachusetts sterile compounding pharmacy qualified a licensed technician for Category 2 CSPs eight months ago. The technician initially passed the required garbing and aseptic manipulation assessments, but has completed neither the scheduled repeat garbing nor media-fill-based aseptic manipulation competency during the intervening eight months. The technician wants to resume preparation tomorrow under a pharmacist's direct observation, and the pharmacist offers to perform final validation afterward. What should the designated supervisor require first?",
    "choices": [
      {
        "text": "Allow the technician to compound because initial media-fill qualification is permanent as long as a pharmacist signs every final CSP label.",
        "why": "Incorrect. Current USP <797> §§2.2–2.3 require ongoing garbing and aseptic-manipulation competency at least EVERY SIX MONTHS for Category 1 and 2 personnel who compound. Pharmacist final validation does not replace those personnel qualification prerequisites."
      },
      {
        "text": "Require successful overdue ongoing garbing and aseptic-manipulation competency evaluations before returning the technician to Category 2 compounding; retain the pharmacist's independent final validation.",
        "why": "Correct. The technician's last successful ongoing assessments were eight months ago, exceeding the Category 2 six-month interval. USP <797> requires those activities at the specified intervals, including media-fill assessment followed by glove sampling and associated testing. Massachusetts pharmacists remain responsible for final validation under 247 CMR 9.04(1)."
      },
      {
        "text": "Ask only for a renewed national technician certification because certification alone resets USP <797> competency intervals.",
        "why": "Incorrect. Professional certification is not the same as facility-specific cleanroom garbing and aseptic compounding qualification. USP <797> personnel competency recurs regardless of national technician certification status."
      },
      {
        "text": "Permit Category 2 compounding under observation until one year has elapsed because Category 2 personnel follow the annual oversight-only competency interval.",
        "why": "Incorrect. The every-12-month interval applies to some personnel who have DIRECT OVERSIGHT but do not compound; Category 1/2 active compounding personnel must satisfy the SIX-month competency intervals. Being observed does not make the compounding technician an oversight-only person."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "Current USP <797> §§2.2–2.3/Table 1 and associated aseptic manipulation competency requirements (official Nov. 1, 2023); USP official FAQs updated Dec. 11, 2023; 247 CMR 9.01(3), 9.04(1)",
    "url": "https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0",
    "verified": "2026-11-17",
    "note": "Category 1/2 personnel who actively compound sterile preparations require recurring garbing and aseptic-manipulation competency at least every six months. Oversight-only yearly assessments and the pharmacist's final check do not extend that interval."
  },
  {
    "id": "E30-187",
    "set": 38,
    "area": 2,
    "kind": "single",
    "topicKey": "bulk-compounding-eligibility",
    "topic": "FDA 503A bulk drug eligibility: nomination alone without monograph, approved-product component or actual 503A list",
    "stem": "A Massachusetts state-licensed 503A compounding pharmacy has a patient-specific prescription requesting a nonsterile medicine compounded from bulk Substance X. FDA confirms that X has NO applicable USP/NF monograph, is NOT a component of an FDA-approved drug, and is NOT on FDA's established 503A bulks list. A supplier notes only that someone NOMINATED X for future FDA review; the supplier provides a valid certificate of analysis and is FDA-registered. Assume no temporary enforcement-discretion statement applicable to X is being invoked. Which conclusion is correct about qualifying for the FD&C Act §503A bulk-ingredient exemptions?",
    "choices": [
      {
        "text": "A nomination automatically places X on the 503A bulks list until FDA expressly rejects the nomination.",
        "why": "Incorrect. FDA distinguishes substances nominated for evaluation from substances actually included on the established 503A bulks list. A nomination alone does not satisfy 21 U.S.C. §353a(b)(1)(A)'s statutory ingredient eligibility requirement."
      },
      {
        "text": "The supplier's certificate of analysis and FDA establishment registration independently make X eligible even though none of the three listed substantive ingredient pathways applies.",
        "why": "Incorrect. Valid COA and supplier registration are additional necessary conditions for qualifying 503A bulk substances, not substitutes for an applicable USP/NF monograph, FDA-approved product component status, or inclusion on the established 503A list."
      },
      {
        "text": "The individual patient prescription makes all bulk ingredients eligible, regardless of their legal monograph, FDA approval or bulks-list status.",
        "why": "Incorrect. A patient-specific prescription is a separate prerequisite for the 503A exemption pathway and does not override §503A's limits on which BULK DRUG SUBSTANCES may be used."
      },
      {
        "text": "Do not treat the proposed compound as satisfying the statutory 503A bulk-substance exemption on the stated evidence; select a lawfully eligible ingredient or pursue another authorized route.",
        "why": "Correct. FDA's 503A bulks explanation and FD&C Act §503A(b)(1)(A) require one of three substantive eligibility bases: a compliant applicable compendial monograph, FDA-approved-drug component, or actual inclusion on the established 503A bulks list, with COA and manufacturer registration additionally required. No route is satisfied for X. A separate FDA enforcement-discretion policy, if any, requires its own current specific analysis."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "FD&C Act §503A(b)(1)(A) (21 U.S.C. §353a(b)(1)(A)); FDA 'Bulk Drug Substances Used in Compounding Under Section 503A' (updated 2026); FDA 503A bulks list regulations and category-status distinctions",
    "url": "https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503a-fdc-act",
    "verified": "2026-11-17",
    "note": "A 503A pharmacy's valid patient Rx and supplier COA do not by themselves make a bulk API eligible. Check USP/NF monograph, FDA-approved-product component, or the actual FDA 503A bulks list; mere nomination is not list inclusion."
  },
  {
    "id": "E30-188",
    "set": 38,
    "area": 2,
    "kind": "multi",
    "topicKey": "interchange-product-equivalence",
    "topic": "Massachusetts nonemergency drug interchange: same active ingredient but strength and dosage form must match",
    "stem": "A Massachusetts pharmacist receives an otherwise valid prescription for a brand-name extended-release oral tablet (Drug A, 100 mg). The patient has not requested the brand, and the prescriber has not indicated 'no substitution.' Products available include (X) a cheaper FDA Orange Book A-rated generic extended-release TABLET 100 mg of Drug A, (Y) the same drug as an FDA-approved immediate-release tablet 100 mg, and (Z) the same extended-release drug as a 50-mg tablet. Assume all other prescription and safety requirements are satisfied. Under 105 CMR 720 and Massachusetts pharmacy interchange rules, which statements are accurate? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Product X can qualify for ordinary interchange because the same drug, strength and dosage form has a therapeutically equivalent A-rated generic and the prescriber did not prohibit substitution.",
        "why": "Correct. 105 CMR 720.050 and 720.200 base interchange on products therapeutically equivalent to the prescribed drug in the same active ingredient, dosage form and strength (or separately specifically listed). The stated Orange Book A rating supports the appropriate same-strength ER tablet substitution."
      },
      {
        "text": "Product Y is automatically interchangeable because its milligram strength is the same, even though its release mechanism and dosage form differ.",
        "why": "Incorrect. Identical strength alone is insufficient: immediate-release and extended-release forms are not treated as automatically equivalent. Under 105 CMR 720.020, pharmaceutical equivalence includes dosage form/route and in practice an appropriate Orange Book equivalence designation; a prescriber-authorized change may be needed."
      },
      {
        "text": "Product Z is automatically equivalent if the pharmacy gives two 50-mg tablets instead of one 100-mg tablet, because arithmetic equality replaces the legal same-strength requirement.",
        "why": "Incorrect. Different tablet strength and tablet count are not the identical 100-mg dosage-unit product contemplated by an ordinary legally interchangeable equivalent. The pharmacist may clarify a distinct therapeutic substitution with the practitioner, but cannot infer automatic equivalence from arithmetic."
      },
      {
        "text": "If the pharmacist needs a product with a different dosage form or strength, the pharmacist should obtain an appropriate lawful prescriber clarification or authorization rather than silently treat it as mandatory generic interchange.",
        "why": "Correct. The Massachusetts List of Interchangeable Drug Products operates on equivalent active ingredients, forms and strengths. A clinically plausible change in formulation or dosage may require prescriber consultation and documentation rather than substitution under the ordinary interchange mandate."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "105 CMR 720.020 (pharmaceutical/interchangeable equivalence), 720.050 and 720.200 Appendix A (Massachusetts List and Orange Book A-rated equivalent comparison); M.G.L. c.112 §12D; 247 CMR 9.05",
    "url": "https://www.mass.gov/regulations/105-CMR-72000-list-of-interchangeable-drug-products",
    "verified": "2026-11-17",
    "note": "Massachusetts nonemergency generic interchange depends on recognized therapeutic equivalence of the actual dosage form and strength, not merely the same chemical name or equal total milligrams from a different formulation."
  },
  {
    "id": "E30-189",
    "set": 38,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "Actual 2026 exempt Fioricet NDC versus federal CIII butalbital combination product",
    "stem": "A Massachusetts pharmacist checks two actual butalbital combination capsules in November 2026. Product A: Fioricet 50 mg butalbital/300 mg acetaminophen/40 mg caffeine, package NDC 52544-080-01 (product NDC 52544-080), appears on DEA's April 1, 2026 exempt prescription-product list; its FDA DailyMed label says DEA Schedule 'None'. Product B: butalbital/acetaminophen/caffeine 50/325/40 capsules, NDC 72162-2665-1, which FDA DailyMed labels DEA Schedule CIII. DEA's November 9, 2026 determination removed specified INACTIVE NDC exemptions, not active ones. Both require prescriptions. Which classification applies?",
    "choices": [
      {
        "text": "Both become federal CIII after November 9 because DEA revoked every butalbital-containing combination exemption.",
        "why": "Incorrect. The October 9 final DEA determination targeted specified inactive NDCs and expressly did not revoke active exemption listings, including Fioricet product 52544-080."
      },
      {
        "text": "Both are federally exempt because acetaminophen and caffeine always cancel out butalbital control regardless of the actual marketed product and NDC.",
        "why": "Incorrect. Exemption under 21 CFR 1308.31–.32 is PRODUCT-specific, not an entire-ingredient-class exemption. Product B has its own FDA DailyMed federal CIII listing."
      },
      {
        "text": "Product A remains federally exempt and Massachusetts Schedule VI as an otherwise noncontrolled prescription drug; Product B is federally and Massachusetts Schedule III.",
        "why": "Correct. DEA's April 2026 exempt table lists Fioricet 52544-080; FDA DailyMed labels its 52544-080-01 package 'DEA None'. FDA DailyMed July 2026 labels Product B NDC 72162-2665-1 CIII. MA 105 CMR 700.002(C),(F) applies the respective III and VI classifications."
      },
      {
        "text": "The pharmacy can assign both products the exemption tied to NDC 52544-080 because their therapeutic purpose and butalbital amount are similar.",
        "why": "Incorrect. Each product's current DEA exemption and marketed NDC must be verified independently. Product B's different 50/325/40 preparation does not inherit exemption from Fioricet 50/300/40."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "DEA Table of Exempted Prescription Products Apr. 1, 2026 (NDC 52544-080); 91 FR 64618 Oct. 9, 2026 effective Nov. 9; FDA DailyMed Fioricet NDC 52544-080-01 (DEA None) and butalbital/APAP/caffeine NDC 72162-2665-1 (CIII); 105 CMR 700.002(C),(F)",
    "url": "https://deaecom.gov/schedules/exempt/exempt_rx_list.pdf",
    "verified": "2026-11-17",
    "note": "Specific verified exemption and two actual FDA marketed NDCs replace prior hypothetical unconfirmed products. DEA's Oct 9 final revocation removed only specified inactive NDCs.",
    "revision": 2
  },
  {
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
  },
  {
    "id": "E30-191",
    "set": 39,
    "area": 1,
    "kind": "multi",
    "topicKey": "workforce-supervision",
    "topic": "Pediatric vaccine roles: intern/technician credentials and pharmacist clinical selection",
    "stem": "A Massachusetts pharmacy offers routine influenza vaccine to an eligible FIVE-YEAR-OLD under a valid standing order. A qualified pharmacist selects the formulation, completes screening/counseling, consent, VIS, MIIS and emergency procedures, and supervises vaccinators. Each proposed worker has CPR; further credentials and vaccine training are specified below. Which workers can administer under Board Policy 2023-02 revised Sept. 4, 2025? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A Massachusetts-registered pharmacy intern with all required intern vaccination training and direct pharmacist supervision.",
        "why": "Correct. Board Policy 2023-02 permits suitably trained registered pharmacy interns to administer designated vaccines to patients age five and older with required pharmacist supervision."
      },
      {
        "text": "A licensed noncertified pharmacy technician who completed all vaccine training but has only 420 documented post-license hours, no accepted national certification, and pharmacist supervision.",
        "why": "Incorrect. The policy's technician pathway requires national certification OR at least 500 documented hours worked AFTER technician licensure in addition to vaccine training."
      },
      {
        "text": "A licensed noncertified pharmacy technician with 520 documented post-license work hours, all required vaccine-specific training and the supervising pharmacist's approval.",
        "why": "Correct. Policy 2023-02 §III(D) permits a qualified licensed technician with 500+ post-license hours as an alternative to national certification, subject to the training and supervision described."
      },
      {
        "text": "A nationally certified and vaccine-trained technician administering after the pharmacy's algorithm selected the vaccine, without the pharmacist completing the patient-specific clinical assessment and formulation selection.",
        "why": "Incorrect. The supervising pharmacist, not a technician or automated algorithm alone, remains responsible for patient assessment, vaccine selection and counseling under the policy."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Massachusetts Board Vaccine Administration Policy 2023-02, revised Sept. 4, 2025, §§II–IV; 247 CMR 8.00",
    "url": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download",
    "verified": "2026-11-17",
    "note": "Some threshold overlap with E30-062 remains; distinguishes intern eligibility and nondelegable pharmacist vaccine-selection tasks.",
    "revision": 2
  },
  {
    "id": "E30-192",
    "set": 39,
    "area": 2,
    "kind": "single",
    "topicKey": "public-health-prescribing",
    "topic": "HIV prevention: transition from a finite PEP course to indicated PrEP assessment",
    "stem": "A properly trained Massachusetts pharmacist independently supplied a guideline-concordant 28-day oral HIV postexposure prophylaxis (PEP) regimen after a qualifying recent exposure. At follow-up, the patient reports finishing the course but continuing HIV exposure risk. The patient asks the pharmacist to provide another 28-day PEP course each month instead of discussing other prevention. The pharmacist's practice meets the applicable MCSR and prescribing requirements. What is the MOST appropriate next step under Massachusetts' 2026 HIV prevention prescribing framework?",
    "choices": [
      {
        "text": "Automatically dispense monthly PEP courses without reassessment because an initial PEP prescription establishes permanent ongoing eligibility.",
        "why": "Incorrect. PEP is a time-limited response to an exposure, not a standing indefinitely renewable substitute for ongoing prevention. Continuing risk calls for current clinical assessment."
      },
      {
        "text": "Refuse to discuss oral PrEP because pharmacist prescribing authority applies only before any PEP exposure has occurred.",
        "why": "Incorrect. Massachusetts authorizes appropriately trained pharmacists to prescribe oral PrEP under the separate statewide guidance when the patient meets its requirements. Prior PEP use does not, by itself, bar a PrEP assessment."
      },
      {
        "text": "Evaluate the patient for an appropriate transition to oral PrEP using the current PrEP guidance, required HIV screening and clinical assessment, and arrange follow-up or referral as indicated; do not automatically renew PEP.",
        "why": "Correct. Massachusetts c.94C §19F and DPH Circular DCP 26-08-125 authorize pharmacist prescribing for both HIV PEP and oral PrEP, each under its own statewide guideline. Ongoing exposure risk after completing a PEP course requires PrEP eligibility/testing and follow-up evaluation, not automatic repeated PEP."
      },
      {
        "text": "Start oral PrEP without any HIV-status evaluation because a recent course of PEP is proof that the patient is HIV-negative.",
        "why": "Incorrect. Taking PEP does not substitute for the required HIV evaluation before PrEP initiation; potential acute HIV infection and the guideline's testing/follow-up remain important."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c.94C §19F; DPH Circular DCP 26-08-125, Pharmacist Prescribing of Certain Medications; Massachusetts Pharmacist Oral PrEP Guidelines 8-2026 and PEP Guidelines 9-2026",
    "url": "https://www.mass.gov/lists/guidelines-for-pharmacists-to-prescribe-oral-prep-pep-sti-treatment-and-doxypep",
    "verified": "2026-11-17",
    "note": "PEP is a finite postexposure course; sustained risk after PEP prompts a NEW PrEP evaluation under its separate guideline and required testing, not automatic monthly PEP renewal."
  },
  {
    "id": "E30-193",
    "set": 39,
    "area": 2,
    "kind": "single",
    "topicKey": "public-health-prescribing",
    "topic": "Pharmacist STI treatment authority versus gonorrhea EPT",
    "stem": "A Massachusetts pharmacist has a valid license/MCSR, has completed accredited STI-TREATMENT prescribing training, and is prepared to apply the 2026 statewide STI treatment guideline. A 24-year-old patient has documentation of a positive gonorrhea test and asks for appropriate pharmacist-prescribed treatment. The patient ALSO asks for a separate prescription for an unexamined partner labeled only 'EPT' based on the Board's expedited partner therapy policy. Assume no other diagnosis, contraindication or independent prescriber order. Which is the BEST legal distinction?",
    "choices": [
      {
        "text": "Neither request is within any pharmacist pathway because Massachusetts pharmacists may independently prescribe for chlamydia but never for gonorrhea.",
        "why": "Incorrect. The 2026 Massachusetts independent pharmacist STI-treatment guidance expressly includes gonorrhea as well as chlamydia; the existence of a condition-specific pathway does not mean the pharmacist must refuse all gonorrhea evaluation."
      },
      {
        "text": "The pharmacist may evaluate and prescribe treatment for the diagnosed patient IF every requirement of the 2026 guideline is met, but cannot extend the CHLAMYDIA-only EPT prescription mechanism to an unexamined gonorrhea partner.",
        "why": "Correct. These are two different authorities: 2026 pharmacist independent STI-treatment guidelines cover eligible gonorrhea patients, whereas Board Policy 2020-08's special EPT protocol is limited to partners of people diagnosed with chlamydia. The partner requires an appropriate authorized clinical/prescribing route."
      },
      {
        "text": "The 2026 pharmacist authority automatically amends all EPT policies to include gonorrhea, so both prescriptions may be issued without further partner assessment.",
        "why": "Incorrect. A new authority to treat a patient does not expand the separate EPT policy. Massachusetts Policy 2020-08 explicitly states that its EPT procedure applies only to chlamydia."
      },
      {
        "text": "The pharmacist may supply the partner's gonorrhea treatment as EPT only if the first patient promises to deliver it personally.",
        "why": "Incorrect. Promised delivery by the index patient does not change the disease-specific scope of the Board's EPT policy; gonorrhea is not covered by that chlamydia-only mechanism."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "M.G.L. c.94C §19F; DPH Pharmacist Guidance for STI Treatment 8-2026, including gonorrhea; Massachusetts Board/DCP Policy 2020-08 Expedited Partner Therapy Prescriptions (May 25, 2023), chlamydia only",
    "url": "https://www.mass.gov/policy-statement/expedited-partner-therapy-prescriptions",
    "verified": "2026-11-17",
    "note": "Separate independently prescribed gonorrhea treatment for an assessed patient from chlamydia-only EPT for an unexamined partner. The 2026 STI authority does not silently expand EPT."
  },
  {
    "id": "E30-194",
    "set": 39,
    "area": 3,
    "kind": "single",
    "topicKey": "label-packaging",
    "topic": "Prescription labeling: pharmacist initials and Schedule VI label validity",
    "stem": "A Massachusetts retail pharmacy fills a valid non-compounded Schedule VI tablet prescription in the correct child-resistant container. The computer-generated label shows the date filled, pharmacy name/address, prescription serial, patient's name, prescriber's name, medicine, directions, applicable cautions and tablet count. HOWEVER, it shows only the pharmacy's internal employee login number in a back-office record; the label itself omits the filling pharmacist's initials. The pharmacist has completed the final clinical/dispensing review. What must occur before lawful handoff?",
    "choices": [
      {
        "text": "Nothing further; the prescription serial number legally substitutes for the pharmacist's initials when records are computerized.",
        "why": "Incorrect. M.G.L. c.94C §21 specifies both the pharmacy's serial number and the filling pharmacist's initials as distinct label elements; an internal login does not erase the separate label obligation."
      },
      {
        "text": "Dispense as labeled because Schedule VI drugs are outside the Massachusetts controlled-substance labeling law.",
        "why": "Incorrect. Massachusetts Schedule VI is part of the state controlled-substance scheme, and §21 labeling applies. Federal noncontrol does not remove the state label elements."
      },
      {
        "text": "Obtain a new prescription signed by the prescriber because any omission on a dispensing label invalidates the original order.",
        "why": "Incorrect. The stated prescription itself is valid; the defect is on the pharmacy-generated DISPENSING LABEL. It is corrected by the pharmacy, without obtaining a new prescriber order."
      },
      {
        "text": "Correct the container label to include the filling pharmacist's initials, while retaining all other mandatory information, before dispensing.",
        "why": "Correct. M.G.L. c.94C §21 requires the filling pharmacist's initials on the affixed label in addition to date, pharmacy identifiers, Rx serial, patient/prescriber/drug, directions, cautions, and quantity for tablets or capsules. Final electronic validation alone does not replace the specified label."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §21 (current as amended effective January 1, 2026), first paragraph; 247 CMR 9.04 dispensing and labeling responsibility",
    "url": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21",
    "verified": "2026-11-17",
    "note": "For Massachusetts Schedule VI as well as federally controlled prescriptions, distinguish an otherwise valid order from a defective final container label. Pharmacist initials remain an express label element."
  },
  {
    "id": "E30-195",
    "set": 39,
    "area": 4,
    "kind": "multi",
    "topicKey": "pharmacy-operations",
    "topic": "Shared pharmacy services: jointly accountable pharmacies, notice, audit trail and annual review",
    "stem": "Two Massachusetts-licensed retail pharmacies begin a central-fill/shared-processing arrangement in 2026. The originating pharmacy receives the prescription; its partner performs remote processing and physical filling. Both have authorized personnel, an appropriate written agreement and a secure common information system. The corporate compliance officer proposes the following operating procedures under revised Board Policy 2021-02. Which procedures are required or correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The retail pharmacy informs patients that another pharmacy may process or fill their prescriptions and provides a workable patient opt-out mechanism.",
        "why": "Correct. Massachusetts Board Policy 2021-02, General Requirements III(k)–(l), expressly requires retail patient notification and a mechanism to opt out of the shared-service model."
      },
      {
        "text": "Only the originating pharmacy is responsible for errors, because the central pharmacy's professional responsibility ends when it ships the product.",
        "why": "Incorrect. Section III(i) makes ALL participating pharmacies jointly responsible for properly processed and filled prescriptions; division of tasks does not erase either participant's accountability."
      },
      {
        "text": "The pharmacies maintain a transaction audit trail that can identify the date/time and personnel involved at EACH step, and review documented joint procedures at least annually.",
        "why": "Correct. Policy III(h) mandates a traceable step-by-step date/time/personnel audit trail, while III(n)–(o) requires jointly maintained policies and documented review at least annually."
      },
      {
        "text": "After signing the original agreement, the two pharmacies may skip documented personnel training and a continuity plan because the central site has a pharmacist-in-charge.",
        "why": "Incorrect. Policy III(m) and III(p) require documented participant training and a continuity-of-care plan if a shared-services participant cannot operate; a PIC does not eliminate these requirements."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Massachusetts Board Policy 2021-02, Shared Pharmacy Service Models, revised February 6, 2025, §§III(h)–(p), IV",
    "url": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download",
    "verified": "2026-11-17",
    "note": "Central fill/remote processing is NOT outsourcing accountability. All participating pharmacies share liability, retain traceable audit logs, notify retail patients/opt out, and jointly review procedures annually."
  },
  {
    "id": "E30-196",
    "set": 40,
    "area": 1,
    "kind": "single",
    "topicKey": "technician-scope",
    "topic": "Technician licensure: drug-related felony eligibility versus other Board discretion",
    "stem": "A 25-year-old applicant for an initial Massachusetts pharmacy technician license has completed a Board-approved training path, passed the applicable assessment and has no problem with age or education. The disclosed court record establishes that the applicant previously ADMITTED TO SUFFICIENT FACTS WARRANTING A FINDING OF GUILTY to a DRUG-RELATED FELONY; the criminal case was continued without a formal guilty verdict. The applicant argues that the absence of a conviction makes this record irrelevant. What is the MOST accurate assessment of the stated eligibility condition?",
    "choices": [
      {
        "text": "The applicant satisfies 247 CMR 8.02(3)(d) because a drug-related offense matters only after a formally entered guilty verdict.",
        "why": "Incorrect. The text expressly covers both conviction of a drug-related felony AND an admission to sufficient facts warranting such a finding. Absence of a formal judgment does not automatically satisfy that condition."
      },
      {
        "text": "The applicant is barred from every type of Massachusetts professional license forever, without any need to read the relevant profession's rule.",
        "why": "Incorrect. The question concerns the specific pharmacy technician eligibility condition in 247 CMR 8.02, not an automatic permanent prohibition from every health profession."
      },
      {
        "text": "The applicant does not meet the express pharmacy technician application condition under 247 CMR 8.02(3)(d); the Board must evaluate the disclosed record under the applicable legal standards rather than treating it as irrelevant.",
        "why": "Correct. The technician application rule expressly requires that an applicant not have been convicted of a drug-related felony OR admitted to sufficient facts to warrant such findings. The problem asks about satisfying that stated condition, not about speculative later relief or a blanket rule for unrelated arrests."
      },
      {
        "text": "The applicant may conceal the admission and file a clean application because Board suitability review covers only paid work history.",
        "why": "Incorrect. An applicant must not provide false information on licensure materials. Concealment does not cure an express eligibility issue and can introduce independent professional-conduct concerns."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 8.02(3)(a)–(e), Pharmacy Technicians: application eligibility including drug-related felony conviction OR admission to sufficient facts; 247 CMR 10.03(1)(p) false information",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-17",
    "note": "For technician APPLICATIONS, the rule explicitly names admissions to sufficient facts for a drug-related felony; do not misapply it as an automatic bar for any arrest or any misdemeanor."
  },
  {
    "id": "E30-197",
    "set": 40,
    "area": 2,
    "kind": "multi",
    "topicKey": "institutional-pharmacy-practice",
    "topic": "Hospital inpatient and outpatient classification versus private-physician office patients",
    "stem": "A Massachusetts hospital maintains a properly registered hospital pharmacy but no separately licensed open-to-public retail drug-store pharmacy. Its pharmacist receives four otherwise valid medication requests. Each is for a routine drug in a quantity allowed for the patient class; there is no emergency-department, discharge, sole-community-hospital nursing-facility or other special exception. Under 105 CMR 722.020 and 722.090(A), which requests fall within the ordinary hospital-pharmacy patient categories? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A medication order for a patient formally admitted for overnight care in the hospital.",
        "why": "Correct. A formally admitted hospital inpatient is expressly within 105 CMR 722.090(A), and 722.020 defines the inpatient class."
      },
      {
        "text": "An ordinary prescription for a person who visits a physician's PRIVATE office located inside the hospital building but is not registered as a hospital clinic outpatient.",
        "why": "Incorrect. Under the definition in 105 CMR 722.020, an individual seen in a private physician office is NOT deemed a hospital outpatient merely because that office is physically inside the hospital."
      },
      {
        "text": "A prescription for a patient formally registered in the hospital's outpatient department and currently receiving treatment at the hospital's specialty clinic.",
        "why": "Correct. Hospital outpatient status in 105 CMR 722.020 requires formal registration and current services at a hospital clinic. Section 722.090(A) permits hospital pharmacy prescriptions for hospital outpatients."
      },
      {
        "text": "A walk-in community resident with a prescription from an independent outside practice who has no hospital patient or employee relationship.",
        "why": "Incorrect. A general community walk-in who fits none of 722.090(A)'s groups does not become a hospital patient because the facility has an in-house pharmacy; ordinary retail dispensing requires a distinct lawful route."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "105 CMR 722.020 definitions Hospital Inpatient and Hospital Outpatient; 105 CMR 722.090(A), Hospital Pharmacies; separate emergency/discharge 722.090(B) not invoked",
    "url": "https://www.mass.gov/doc/105-cmr-722-dispensing-procedures-for-clinic-and-hospital-pharmacies/download",
    "verified": "2026-11-17",
    "note": "Hospital outpatient means currently treated AND formally registered at a hospital clinic, not merely anyone seen in a private office in the building. Ordinary hospital pharmacy serves qualifying inpatient/outpatient/employee classes."
  },
  {
    "id": "E30-198",
    "set": 40,
    "area": 2,
    "kind": "single",
    "topicKey": "cdtm-patient-practice",
    "topic": "Hospital CDTM agreement: medical executive committee or designee approval",
    "stem": "A licensed Massachusetts hospital pharmacist and an authorized supervising physician draft a written collaborative drug therapy management (CDTM) agreement to adjust inpatient anticoagulant therapy under approved protocols. The pharmacist has satisfied all professional CDTM eligibility requirements and the proposed agreement includes required protocol/supervision safeguards. The physician and pharmacist have both signed, but the HOSPITAL MEDICAL STAFF EXECUTIVE COMMITTEE (or its designee) has not approved the hospital program. Which assessment is BEST?",
    "choices": [
      {
        "text": "The physician's signature alone is sufficient for hospital CDTM because medical staff executive committee approval is a rule only for community pharmacies.",
        "why": "Incorrect. Hospital CDTM is a specifically listed practice setting requiring approval by the medical staff executive committee or designee in addition to otherwise compliant supervising-physician arrangements."
      },
      {
        "text": "The hospital may proceed if a community pharmacy somewhere in the health system has a Board-recognized CDTM agreement.",
        "why": "Incorrect. A separate community site's protocol does not substitute for the hospital-specific setting approval required by Massachusetts CDTM rules."
      },
      {
        "text": "The pharmacist must instead apply the community CDTM rule requiring an adult community-patient referral to cure the missing hospital committee approval.",
        "why": "Incorrect. Community-specific patient eligibility/referral mechanics are not a replacement for the institutional practice-setting approval mechanism. The institutional agreement must meet its own rules."
      },
      {
        "text": "Obtain approval by the hospital medical staff executive committee or authorized designee before operating under the hospital CDTM agreement, along with all other applicable requirements.",
        "why": "Correct. 247 CMR 16.03(1) (and parallel physician regulation) makes licensed hospital CDTM subject to approval by the medical staff executive committee or designee. The signatures and professional qualifications do not replace institutional approval."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 16.03(1), hospital CDTM setting requiring medical staff executive committee or designee approval; 243 CMR 2.12(4)(a), parallel physician CDTM requirements",
    "url": "https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download",
    "verified": "2026-11-17",
    "note": "Hospital CDTM approval is distinct from a retail/community patient-referral/consent question: the licensed hospital's medical staff executive committee or designee must approve the hospital setting."
  },
  {
    "id": "E30-199",
    "set": 40,
    "area": 3,
    "kind": "multi",
    "topicKey": "rx-amendments",
    "topic": "New Schedule II prescription corrections: missing identifier versus forbidden name/signature change",
    "stem": "A Massachusetts pharmacist receives four SEPARATE new Schedule II prescriptions, each otherwise valid and clinically appropriate. In each case the pharmacist has verified the underlying information, has documented the proposed change with the date and pharmacist identity, and no federal law imposes a stricter special rule. The prescriber is not available for consultation. Under Massachusetts Board/DCP Joint Policy 2018-01, which actions may be taken AS STATED without contacting the prescriber? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "ADD a patient's previously omitted street address to a correctly identified patient's new Schedule II prescription, after confirming the address.",
        "why": "Correct. Joint Policy 2018-01 §III(A)(i)(c)(i) expressly permits adding a missing patient address without consultation; CHANGING an existing patient address is different."
      },
      {
        "text": "CHANGE the named patient to a different individual after the family explains that the prescriber selected the wrong chart.",
        "why": "Incorrect. Section II(A) says the patient's name cannot be changed to a DIFFERENT patient on prescriptions in Schedules II–VI; a new prescription is required, even if the explanation is credible."
      },
      {
        "text": "ADD the correctly verified omitted prescriber's DEA registration number without calling the prescriber, with the change properly documented.",
        "why": "Correct. Section III(A)(i)(d) expressly allows addition of the prescriber's DEA number without consultation; the professional must still verify the number and legality of the prescription."
      },
      {
        "text": "ADD a missing prescriber signature based only on an office printout or a telephone assurance by a technician.",
        "why": "Incorrect. Under Joint Policy 2018-01 §II(D), a prescriber's signature may NEVER be changed or added through the permitted-correction policy; a new valid prescription is required."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Joint Board/Drug Control Program Policy 2018-01, Permitted Prescription Changes and Additions, §§II(A),(D), III(A)(i)(c)–(d), IV, revised through August 1, 2019; 21 CFR 1306.05",
    "url": "https://www.mass.gov/doc/joint-policy-2018-01-permitted-prescription-changes-and-additions/download",
    "verified": "2026-11-17",
    "note": "New Schedule II: a MISSING patient address or verified DEA number can be added without prescriber call, with documentation; changing patient identity or adding an omitted prescriber signature is prohibited."
  },
  {
    "id": "E30-200",
    "set": 40,
    "area": 4,
    "kind": "single",
    "topicKey": "nonresident-pharmacy-licensing",
    "topic": "Out-of-state conventional Schedule VI delivery and Massachusetts nonresident license",
    "stem": "A licensed Rhode Island community pharmacy, with no Massachusetts physical premises, intends to ship only ordinary noncompounded lisinopril and amlodipine prescriptions to Massachusetts residential addresses. Its home-state pharmacy license is active, it holds any necessary Rhode Island registrations, and it does NOT compound sterile or complex nonsterile medicines. Management claims no Massachusetts registration is needed because these are not DEA-scheduled products. What is the required Massachusetts licensing approach BEFORE dispensing/shipping to those Massachusetts patients?",
    "choices": [
      {
        "text": "No Massachusetts pharmacy license, because federal nonscheduled prescriptions can never be Massachusetts controlled substances.",
        "why": "Incorrect. Massachusetts defines ordinary prescription drugs such as these as state Schedule VI controlled substances; MA nonresident pharmacy licensing applies regardless of their absence from federal DEA Schedules II–V."
      },
      {
        "text": "Obtain the Massachusetts nonresident Drug Store Pharmacy license required by 247 CMR 6.02(4); specialized sterile/complex nonsterile compounding endorsements are not needed for the stated conventional drugs.",
        "why": "Correct. 247 CMR 6.02(4) prohibits an out-of-state pharmacy from dispensing or shipping ANY Massachusetts controlled substance into the Commonwealth without a nonresident Drug Store Pharmacy license. State Schedule VI is included. Specialty compounding licenses are conditional on actual compounding type."
      },
      {
        "text": "Obtain a Massachusetts sterile compounding pharmacy license but not a nonresident Drug Store Pharmacy license, because a shipping service counts as sterile preparation.",
        "why": "Incorrect. The pharmacy is shipping conventional manufactured oral tablets; transporting the product does not itself constitute sterile compounding or replace the required nonresident Drug Store Pharmacy license."
      },
      {
        "text": "Only register the Rhode Island pharmacy technician staff with the Massachusetts Board, then ship without licensing the pharmacy premises.",
        "why": "Incorrect. Individual technician credentials do not license the out-of-state pharmacy facility to dispense/ship Massachusetts controlled substances."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 6.02(4)–(6), License Requirements; 105 CMR 700.002 definition and Massachusetts Schedule VI; 2025 Massachusetts nonresident pharmacy registration requirements",
    "url": "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download",
    "verified": "2026-11-17",
    "note": "Ordinary federal-noncontrolled prescription drugs are Massachusetts Schedule VI. Shipping them from another state requires a MA NONRESIDENT Drug Store Pharmacy license; specialty licenses depend on compounding."
  },
  {
    "id": "E30-201",
    "set": 41,
    "area": 1,
    "kind": "single",
    "topicKey": "board-discipline",
    "topic": "Falsification of CE records during a pharmacy licensure audit",
    "stem": "A Massachusetts pharmacist receives a legitimate Board request to provide continuing-education records supporting the pharmacist's recent license renewal. The pharmacist discovers a documented CE deficiency and deliberately edits a completion certificate to show credits never earned, then submits the altered certificate to the Board. No patient has yet been harmed and the pharmacist later completes additional authentic education. Under 247 CMR 10.03, which statement is MOST accurate?",
    "choices": [
      {
        "text": "The deliberate fabrication is an independent potential disciplinary ground for deceit/fraud and false licensure-related information; later education and lack of proven patient injury do not make it permissible.",
        "why": "Correct. 247 CMR 10.03(1)(l) covers conduct capable of deceiving or defrauding, and §10.03(1)(p)/(o) covers false renewal information/fraudulent procurement; the Board need not first establish patient harm from a particular dispensing error."
      },
      {
        "text": "The Board may act only if a patient can demonstrate financial damages caused by the forged certificate.",
        "why": "Incorrect. Board disciplinary grounds cover deceit and fraudulent license-renewal representations independent of a civil damages claim or actual patient injury."
      },
      {
        "text": "A certificate is automatically accurate if the pharmacist later earns an equal number of unrelated CE credits.",
        "why": "Incorrect. Subsequent education does not retroactively make a prior false attestation or fabricated dated certificate truthful."
      },
      {
        "text": "The Board must accept the certificate because it has no authority to request or review renewal/CE documentation.",
        "why": "Incorrect. Massachusetts CE rules require supporting records, and the Board has statutory/regulatory authority to inspect documentation and take action on dishonest license-renewal submissions."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 10.03(1)(l),(o),(p), Grounds for Discipline; 247 CMR 4.00 continuing education documentation; M.G.L. c.112 §61",
    "url": "https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download",
    "verified": "2026-11-17",
    "note": "CE insufficiency and knowingly submitting FAKE CE proof are different violations. A fabricated Board submission itself creates a disciplinary basis without a separate injured patient."
  },
  {
    "id": "E30-202",
    "set": 41,
    "area": 2,
    "kind": "single",
    "topicKey": "drug-integrity",
    "topic": "FDA 2026 DSCSA small-dispenser relief does not waive suspect-product quarantine",
    "stem": "On NOVEMBER 17, 2026, a Massachusetts pharmacy owned by a company with only 14 full-time licensed pharmacists/qualified pharmacy technicians receives a prescription-drug carton with signs of tampering and an unexpectedly altered product identifier. The pharmacist has a credible reason to believe the carton is a SUSPECT PRODUCT. Management cites FDA's August 6, 2026 small-dispenser exemption notice, extending certain electronic tracing requirements through November 27, 2027, and asks that the product be dispensed immediately. What is the best response?",
    "choices": [
      {
        "text": "Dispense the carton, since FDA's DSCSA notice waives every requirement in section 582 for any pharmacy with 25 or fewer full-time pharmacy professionals.",
        "why": "Incorrect. FDA's August 2026 notice identifies limited specific exemptions from §582(g)(1) and certain §582(d)(4) identifier checks; it explicitly does NOT waive other section 582 duties, including the initial quarantine/investigation obligation for a suspect product."
      },
      {
        "text": "Hold the carton only after FDA individually denies the pharmacy's exemption application; all smaller pharmacies must file a waiver request first.",
        "why": "Incorrect. FDA's published class exemption does not require individual submission; suspected-product response is a separate statutory duty and is not delayed until FDA answers a waiver application."
      },
      {
        "text": "Quarantine the suspect product, investigate as required, follow applicable notification and disposition duties if it proves illegitimate, and do not treat the electronic-tracing exemption as permission to dispense it.",
        "why": "Correct. FD&C Act §582(d)(4)(A)(i) requires quarantining and investigating suspect product. FDA's Aug. 6, 2026 notice expressly states that its relief is limited to named requirements and does not apply to other §582 obligations. The 2024 relief still applies through Nov. 27, 2026, with the announced successor interval thereafter."
      },
      {
        "text": "Ship the carton back to the wholesaler without recording the suspect-product investigation because returns are exempt from all DSCSA verification duties.",
        "why": "Incorrect. Merely returning a suspicious package without following the statutory suspect-product verification and disposition process is not justified by the exemption. A return may occur only through the lawful response process."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "FD&C Act §582(d)(4)(A)(i) (21 U.S.C. §360eee-1(d)(4)); FDA August 6, 2026 'DSCSA Exemptions from Certain Requirements ... Until November 27, 2027' (pp.1–3); FDA 2024 small-dispenser exemption remains applicable to Nov. 27, 2026",
    "url": "https://www.fda.gov/media/194424/download",
    "verified": "2026-11-17",
    "note": "FDA small-dispenser relief is narrow. 2024 relief lasts until Nov. 27, 2026; announced 2026 extension addresses certain identifier and electronic-tracing requirements through Nov. 27, 2027, not suspect-product quarantine."
  },
  {
    "id": "E30-203",
    "set": 41,
    "area": 2,
    "kind": "multi",
    "topicKey": "privacy-part2",
    "topic": "42 CFR Part 2 patient notice at first service and right to decline fundraising",
    "stem": "A federally assisted Massachusetts SUD treatment program subject to 42 CFR Part 2 begins ordinary outpatient services for a new adult patient in November 2026. The program posts its privacy notice online but has not provided it to the patient. The program wants to use its Part 2 records to send fundraising letters for the benefit of the program. The patient specifically asks NOT to receive fundraising communications. Which statements comply with current Part 2? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The program must furnish its Part 2 Notice of Privacy Practices to this patient no later than the initial service delivery; merely posting it online does not satisfy the patient-specific notice obligation.",
        "why": "Correct. 42 CFR 2.22(a),(b),(c)(1) requires a plain-language Part 2 notice by first nonemergency service delivery. Website availability is a separate duty, not a substitute for furnishing the notice."
      },
      {
        "text": "The program needs a separate signed opt-IN from every patient before engaging in any fundraising under Part 2, even if patients have a clear and conspicuous chance to decline.",
        "why": "Incorrect. Under 42 CFR 2.22(b)(1)(iii)(B), fundraising for the benefit of the program uses a clear, conspicuous OPT-OUT approach. This circumstance does not require universal separate opt-in consent for fundraising."
      },
      {
        "text": "The program must give a clear opportunity to elect not to receive fundraising communications before using records for that purpose and must honor the patient's expressed opt-out.",
        "why": "Correct. Sections 2.22(b)(1)(iii)(B) and (b)(1)(iv)(G) make opt-out notice and the patient's election central to the Part 2 fundraising pathway; treatment enrollment does not revoke this right."
      },
      {
        "text": "Because the patient is already receiving services, the clinic may continue fundraising letters after the opt-out so long as the mailing does not list the patient's SUD diagnosis.",
        "why": "Incorrect. The patient's express election to refuse fundraising communications remains applicable. Omitting a diagnosis does not nullify 42 CFR 2.22's right to elect not to receive them."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "42 CFR 2.22(a), (b)(1)(iii)(B), (b)(1)(iv)(G), (c)(1), (c)(3); HHS Part 2 Final Rule (compliance February 16, 2026)",
    "url": "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2/subpart-B/section-2.22",
    "verified": "2026-11-17",
    "note": "Tests first-service notice and fundraising opt-out, distinct from E30-028's Part 2 TPO consent and SUD counseling-note disclosure.",
    "revision": 2
  },
  {
    "id": "E30-204",
    "set": 41,
    "area": 3,
    "kind": "single",
    "topicKey": "otc-pseudoephedrine",
    "topic": "CMEA in-person pseudoephedrine sale: photo identification, required buyer logbook signature",
    "stem": "A DEA-self-certified Massachusetts pharmacy with trained personnel proposes an ordinary in-person OTC sale of a MULTI-DOSE pseudoephedrine package containing much more than 60 mg of pseudoephedrine base. The buyer is over 18, presents acceptable government-issued photo identification, and is under both federal quantity limits. The seller properly enters product and quantity data in an electronic CMEA logbook, but the buyer refuses to SIGN or electronically attest to the required purchaser entry. No state-specific exception applies. What should the pharmacist direct?",
    "choices": [
      {
        "text": "Complete the transaction because satisfying the gram limits replaces the buyer's signature requirement.",
        "why": "Incorrect. Federal weight limits and identity/logbook requirements are separate. The absence of an over-limit purchase does not eliminate the purchaser-signature obligation."
      },
      {
        "text": "Have the technician sign as the purchaser, since the store has already authenticated the buyer's photo ID.",
        "why": "Incorrect. A seller may enter factual log data subject to verification, but cannot substitute the employee's signature for the purchaser's required signature or attestation."
      },
      {
        "text": "Apply the single-package 60-mg logbook exception to any product sold in one box, regardless of pseudoephedrine content.",
        "why": "Incorrect. 21 CFR 1314.30(a)'s narrow exception applies to a single SALES PACKAGE containing no more than 60 milligrams of pseudoephedrine, not every single box. The question explicitly excludes that threshold."
      },
      {
        "text": "Do not complete the sale until the purchaser supplies the required signature/attestation and the other 21 CFR 1314.30 conditions are met.",
        "why": "Correct. Under 21 CFR 1314.30(b), the purchaser generally must present acceptable photo ID and sign the written/electronic logbook. The 60-mg single-package exception does not apply to the stated multi-dose package."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1314.30(a)–(d), Combat Methamphetamine Epidemic Act (CMEA): purchaser identification, signed logbook and 60-mg single-package exception; 21 CFR 1314.40 retailer certification",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1314/section-1314.30",
    "verified": "2026-11-17",
    "note": "CMEA sale compliance is not only 3.6-g/9-g limits: for ordinary OTC pseudoephedrine the buyer needs acceptable ID and a SIGNED logbook; a single package is not automatically the ≤60-mg exception."
  },
  {
    "id": "E30-205",
    "set": 41,
    "area": 4,
    "kind": "multi",
    "topicKey": "federal-compounding-models",
    "topic": "503B outsourcing: FDA CGMP, mandatory Massachusetts registration, inspections and adverse reports",
    "stem": "A corporation operates a facility that compounds and distributes sterile drugs without having prescriptions for each identified patient. It elects FDA outsourcing-facility status under FD&C Act §503B and wants to ship these compounded preparations into Massachusetts. It is not a Massachusetts-licensed retail pharmacy and does not claim any temporary exception. The chief executive proposes the following compliance interpretations. Which are legally supported? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "FDA §503B registration alone automatically authorizes shipment into Massachusetts without any Massachusetts outsourcing facility registration.",
        "why": "Incorrect. FDA §503B registration is a federal pathway; 247 CMR 21.04 separately requires a Massachusetts NONRESIDENT outsourcing facility registration when the facility is outside the Commonwealth."
      },
      {
        "text": "Properly registered §503B outsourcing facilities remain subject to FDA CGMP standards and applicable FDA adverse-event/product reporting requirements.",
        "why": "Correct. 503B does NOT exempt compounded drugs from CGMP; FDA expressly states outsourcing facilities must report adverse events and required product information, alongside federal registration and inspections."
      },
      {
        "text": "A corporation can treat any FDA-registered facility as FDA-approved, so the compounded products require no independent quality review.",
        "why": "Incorrect. FDA makes clear §503B registration is not FDA product approval or a determination of CGMP compliance. Each facility's quality/compliance requires appropriate review."
      },
      {
        "text": "An out-of-state §503B facility supplying Massachusetts must satisfy the state's separate nonresident outsourcing registration pathway, including proof of valid current FDA outsourcing registration.",
        "why": "Correct. 247 CMR 21.04 and 21.05 require specific state registration and continuing current FDA status for nonresident outsourcing facilities; federal enrollment does not displace state oversight."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "FD&C Act §503B (21 U.S.C. §353b); 247 CMR 21.04 and 21.05 (Massachusetts nonresident outsourcing facility registration); FDA Information for Outsourcing Facilities, CGMP/adverse events",
    "url": "https://www.mass.gov/doc/247-cmr-21-registration-of-outsourcing-facilities/download",
    "verified": "2026-11-17",
    "note": "503B facility registration with FDA does not constitute product approval or substitute for 247 CMR 21 nonresident registration. CGMP and FDA adverse-event reporting still apply."
  },
  {
    "id": "E30-206",
    "set": 42,
    "area": 1,
    "kind": "multi",
    "topicKey": "licensure-ce",
    "topic": "License transfer: NABP preliminary approval is not Board licensure",
    "stem": "A Connecticut pharmacist, originally licensed there by examination and in good standing in every state where licensed, is applying to Massachusetts by reciprocity. NABP approved the preliminary transfer eight months ago; the applicant has submitted internship documentation and has passed the Massachusetts MPJE. The Massachusetts Board has not yet approved/issued the actual pharmacist license. Which statements are true? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The applicant may practice in a Massachusetts pharmacy as a licensed pharmacist immediately because NABP has approved the transfer.",
        "why": "Incorrect. NABP conducts preliminary evaluation; Board-issued Massachusetts licensure, not preliminary NABP approval, is required to practice as a Massachusetts pharmacist."
      },
      {
        "text": "The Massachusetts Board retains final authority to determine eligibility for pharmacist licensure by reciprocity.",
        "why": "Correct. 247 CMR 3.02(1)(b) expressly assigns final eligibility determination to the Board notwithstanding NABP's initial screening."
      },
      {
        "text": "An applicant licensed by examination elsewhere must always pass NAPLEX again to use the Massachusetts reciprocity pathway.",
        "why": "Incorrect. 247 CMR 3.02(2)(a) for ACPE graduates requires NABP approval, appropriate internship documentation and an MPJE passing result; it does not universally require repeat NAPLEX."
      },
      {
        "text": "A NABP-approved reciprocity application is valid for one year after NABP approval, and good standing in all licensing jurisdictions is required.",
        "why": "Correct. 247 CMR 3.02 opening paragraphs and (1)(c) state both the across-jurisdictions good-standing condition and one-year validity of NABP approval."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "247 CMR 3.02 (2025 revision), introductory paragraphs, (1)(b)–(c), (2)(a); Massachusetts Board pharmacist license application guidance",
    "url": "https://www.mass.gov/doc/247-cmr-3-pharmacist-licensure-requirements/download",
    "verified": "2026-11-17",
    "note": "NABP approval is PRELIMINARY, Board decision final. Even an MPJE pass is not permission to practice pending MA license issuance; NABP-approved reciprocity application has a 1-year window."
  },
  {
    "id": "E30-207",
    "set": 42,
    "area": 2,
    "kind": "single",
    "topicKey": "public-health-prescribing",
    "topic": "Return combined oral contraception Rx: new migraine with aura",
    "stem": "Eight months after a Massachusetts pharmacist prescribed a combined estrogen/progestin pill, a 26-year-old requests a NEW prescription for that product. A current self-screen documents newly diagnosed migraine WITH visual aura. No other contraceptive method has yet been screened and no separate emergency-supply exception is present. Under the 2026 DPH pharmacist prescribing guidelines and CDC U.S. MEC, which decision is BEST?",
    "choices": [
      {
        "text": "Supply another 30 days of the combined pill while contacting the original clinician because previous well-tolerated use justifies a short bridge after a newly identified risk.",
        "why": "Incorrect. Migraine with aura is CDC U.S. MEC Category 4 for combined hormonal contraception. A short repeat does not remove that established contraindication."
      },
      {
        "text": "Switch immediately to any progestin-only product without completing a new patient-specific screening because the aura contraindication automatically establishes another method's eligibility.",
        "why": "Incorrect. Progestin-only options do not share the same categorical aura risk, but each new method still requires its own eligibility assessment and relevant screening."
      },
      {
        "text": "Decline to issue the requested combined pill, record/counsel about the new contraindication, and evaluate a guideline-appropriate alternative or arrange clinical referral.",
        "why": "Correct. CDC U.S. MEC Category 4 applies to combined hormonal contraceptives for migraine with aura; MA DCP 26-08-125 requires risk-based screening and appropriate response."
      },
      {
        "text": "Issue the same combined pill with instructions to stop if another episode occurs because a single report of visual aura does not satisfy the CDC contraindication.",
        "why": "Incorrect. Migraine WITH aura is Category 4; there is no requirement for another subsequent aura episode before acting on the current diagnosis."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c94C §19F; DPH Circular DCP 26-08-125 Aug. 25, 2026; CDC U.S. MEC 2024, CHC with migraine with aura Category 4",
    "url": "https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download",
    "verified": "2026-11-17",
    "note": "Return-visit contraindication vs initial prescribing; practical distractors examine bridge and alternative contraception screening.",
    "revision": 2
  },
  {
    "id": "E30-208",
    "set": 42,
    "area": 2,
    "kind": "single",
    "topicKey": "prescriber-authority",
    "topic": "Veterinary Schedule VI prescription: no NPI or DEA needed",
    "stem": "A duly licensed Massachusetts veterinarian holding an MCSR examines a dog and sends an otherwise valid Schedule VI prescription for oral amoxicillin to a Massachusetts community pharmacy. The clinic has an established veterinarian-client-patient relationship. The software blocks dispensing because the veterinarian has neither a human-health NPI nor a federal DEA registration number. No federally controlled Schedule II–V medication is involved. Which action is legally appropriate?",
    "choices": [
      {
        "text": "Confirm the veterinarian's license/MCSR and animal-patient order, then use the veterinary processing workflow; neither NPI nor DEA registration is required for this Schedule VI prescription.",
        "why": "Correct. The Board's January 2025 Veterinary Prescriptions recommendations specifically note that veterinarians do not have NPIs, DEA numbers are not required for Schedule VI, and MCSR is the pertinent identifier. A software field cannot add a legal prerequisite."
      },
      {
        "text": "Demand an NPI because every electronically processed Massachusetts prescription must list one, including all veterinary animal orders.",
        "why": "Incorrect. NPIs identify human health providers, not veterinarians as animal-only prescribers; the Board specifically cautions pharmacies about software configurations."
      },
      {
        "text": "Demand a DEA number because Massachusetts Schedule VI is identical to the federal DEA-controlled Schedule V.",
        "why": "Incorrect. MA Schedule VI covers ordinary prescription-only drugs not in federal Schedules I–V; this amoxicillin order requires an MCSR rather than a DEA number."
      },
      {
        "text": "Rewrite the order in the dog's owner's name for treatment of the owner's own infection because a veterinarian can prescribe for an animal's immediate household.",
        "why": "Incorrect. Veterinary prescribing privileges relate to animal patients; an animal prescription cannot become a lawful human prescription for the owner."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "M.G.L. c.94C §22(a) veterinary exception; 105 CMR 700.002(F); Board Best Practice Recommendations, 'Veterinary Prescriptions,' January 9, 2025, p.6",
    "url": "https://www.mass.gov/doc/best-practice-recommendations-pdf/download",
    "verified": "2026-11-17",
    "note": "Animal Schedule VI Rx: verify vet MCSR/license but do not demand NPI or DEA. Never transfer veterinary prescriber authority to human patients."
  },
  {
    "id": "E30-209",
    "set": 42,
    "area": 3,
    "kind": "single",
    "topicKey": "drug-schedule-identification",
    "topic": "FDA-labeled Rx-only codeine/promethazine Schedule V: state and federal no-Rx sale",
    "stem": "A Massachusetts customer requests 60 mL of FDA-marketed promethazine hydrochloride/codeine phosphate oral solution (6.25 mg/10 mg per 5 mL), product NDC 70752-139. Its actual FDA DailyMed label says 'Rx Only' and federal 'CV'. The customer presents photo ID and offers to sign the federal nonprescription Schedule V purchase log, but NO authorized prescription has been issued. No emergency or other exception applies. What is the pharmacist's lawful response?",
    "choices": [
      {
        "text": "Sell the 60 mL under federal 21 CFR 1306.26 because small Schedule V quantities are automatically nonprescription after identification and logbook entry.",
        "why": "Incorrect. The exact marketed NDC is FDA Rx Only, and federal §1306.26(f) cannot override another law requiring a prescription. Massachusetts c94C §17(c) requires a valid Rx for this Schedule V product."
      },
      {
        "text": "Do not dispense without a valid prescriber prescription; the FDA Rx-only labeling and Massachusetts Schedule V prescription requirement are not replaced by the customer's ID, requested quantity or log signature.",
        "why": "Correct. FDA DailyMed NDC 70752-139 lists Rx Only and Schedule CV. M.G.L. c94C §17(c) requires a prescription outside specific exceptions; 21 CFR 1306.26(f) does not supersede stricter state law."
      },
      {
        "text": "Dispense as long as the prescriber's office confirms the customer has a cough without actually issuing a prescription, because the clinical indication is the only required authorization.",
        "why": "Incorrect. Confirming a diagnosis is not issuing a prescription. The patient must have an appropriately authorized order under Massachusetts c94C §17."
      },
      {
        "text": "Reclassify the syrup as Massachusetts Schedule VI because it also contains promethazine, and apply the Schedule VI pharmacist emergency continuity supply pathway.",
        "why": "Incorrect. The codeine combination is federally Schedule V per its FDA label and Massachusetts follows the federal V classification. An additional nonnarcotic ingredient does not turn this specifically labeled C-V product into Schedule VI."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "FDA DailyMed promethazine HCl/codeine phosphate NDC 70752-139 (Rx Only, Schedule CV); M.G.L. c94C §17(c); 21 CFR 1306.26(f); 105 CMR 700.002(E)",
    "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9aca56ec-28f8-4679-9f90-ec3e82deb9ac",
    "verified": "2026-11-17",
    "note": "Real FDA-labeled Rx-only product, replacing an unsupported hypothetical OTC codeine NDC.",
    "revision": 2
  },
  {
    "id": "E30-210",
    "set": 42,
    "area": 4,
    "kind": "multi",
    "topicKey": "controlled-inventory",
    "topic": "DEA CSOS: personal certificate and linked receipt record",
    "stem": "A Massachusetts pharmacy uses DEA-approved CSOS to buy Schedule II stock from a DEA-registered wholesaler. An authorized purchaser has a current personal DEA CSOS certificate, and both parties can archive electronic orders. Which statements about lawful order execution and receipt are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The authorized person's valid DEA-certificate digital signature may serve for a compliant electronic Schedule II order without an additional paper DEA Form 222.",
        "why": "Correct. 21 CFR 1305.21(a) authorizes a personally signed electronic order; DEA confirms CSOS is the compliant electronic alternative to paper Form 222."
      },
      {
        "text": "The PIC may lend an individual CSOS private-signing certificate to any technician whenever the pharmacist is absent.",
        "why": "Incorrect. DEA CSOS certificates are issued to specific authorized individuals and cannot be shared as a generic pharmacy credential."
      },
      {
        "text": "On receipt, the purchaser records actual quantity for each item and the date received, electronically links those details to the initial order, and archives the record.",
        "why": "Correct. 21 CFR 1305.22(g) requires precisely this purchaser receipt record. A signed order by itself does not establish quantities received."
      },
      {
        "text": "The supplier is exempt from checking the certificate's expiration and revocation because only the purchaser is responsible for authentication.",
        "why": "Incorrect. 21 CFR 1305.22(c) directs supplier validation of signature integrity, certificate expiry/revocation, and eligibility before fulfilling."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 CFR 1305.21(a) and 1305.22(c),(g); DEA CSOS Ordering and FAQ, current 2026",
    "url": "https://www.deadiversion.usdoj.gov/faq/csos-faq.html",
    "verified": "2026-11-17",
    "note": "CSOS replaces paper 222, not individual certificate control or actual-receipt recordkeeping. Electronically attach quantity/date received to original order."
  },
  {
    "id": "E30-211",
    "set": 43,
    "area": 1,
    "kind": "single",
    "topicKey": "board-waivers",
    "topic": "Board waiver fifth-anniversary expiration and pending successor petition",
    "stem": "A Massachusetts pharmacy received a specific 247 CMR Board waiver on November 15, 2021. The manager submitted a new waiver petition November 1, 2026, but as of November 17, 2026 the Board has NOT granted a subsequent waiver. The original fifth anniversary passed two days ago; no independent extension was granted. Which procedure is permitted today?",
    "choices": [
      {
        "text": "Continue under the 2021 waiver because the timely and complete renewal petition automatically preserves the earlier authorization.",
        "why": "Incorrect. 247 CMR 14.01(5)(b)–(d) gives no automatic renewal stay when a successive petition is filed."
      },
      {
        "text": "Continue for a default 30-day administrative grace period starting on the fifth anniversary, subject only to later Board review.",
        "why": "Incorrect. The waiver expires on its fifth anniversary and §14.01(5)(d) provides no automatic 30-day grace."
      },
      {
        "text": "Continue if the MOR documents that patient-safety controls are unchanged from 2021, without waiting for Board waiver approval.",
        "why": "Incorrect. A manager's safety analysis does not replace the Board's grant of a subsequent waiver."
      },
      {
        "text": "Comply with the underlying 247 CMR requirement after the old waiver expired unless and until the Board grants another waiver.",
        "why": "Correct. Section 14.01(5)(d) requires following applicable regulations once a waiver expires unless the Board granted a subsequent waiver."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "247 CMR 14.01(5)(b)–(d), Petition for Waiver, effective Sept. 22, 2017",
    "url": "https://www.mass.gov/doc/247-cmr-14-petition-for-waiver/download",
    "verified": "2026-11-17",
    "note": "Submission of a successor petition is not an extension of the fifth-anniversary waiver.",
    "revision": 2
  },
  {
    "id": "E30-212",
    "set": 43,
    "area": 2,
    "kind": "multi",
    "topicKey": "controlled-prescriptions",
    "topic": "CT-issued alprazolam and gabapentin: separate authenticity and reporting duties",
    "stem": "A Connecticut doctor with active Connecticut license and DEA registration examined the patient IN CONNECTICUT and, with legitimate medical purpose and no red flags, issued two otherwise valid electronic prescriptions four days ago for Massachusetts dispensing: alprazolam (Schedule IV federal/MA) and gabapentin (MA Schedule VI and separately MassPAT-reportable). The MA pharmacist can verify the doctor's basic licensing data but has NOT completed telephone-or-other-means verification of the out-of-state Schedule IV order. Neither prescription involves a Massachusetts telehealth encounter. Which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Gabapentin may be dispensed after ordinary legal/clinical authenticity review without the special §18(c) Schedule III–V verification step, but its MA PMP reporting duty still applies.",
        "why": "Correct. M.G.L. c.94C §18(c) requires special telephone/other verification for out-of-state Schedules III–V, not VI. Gabapentin still is a separately reportable state Schedule VI drug of concern."
      },
      {
        "text": "A Connecticut practitioner must hold a Massachusetts MCSR for every otherwise eligible prescription issued in Connecticut to be dispensed in Massachusetts.",
        "why": "Incorrect. §18(c) supplies an out-of-state prescriber pathway if authorized in the prescriber's state and appropriately DEA-registered; it is not a blanket MA-MCSR requirement."
      },
      {
        "text": "The pharmacist must not dispense the out-of-state Schedule IV alprazolam until required additional verification by telephone or other means succeeds, despite the secure electronic transmission.",
        "why": "Correct. §18(c) expressly requires separate out-of-state verification for Schedules III–V and directs that an Rx whose verification cannot be obtained may not be filled."
      },
      {
        "text": "Gabapentin is exempt from all MassPAT submissions solely because its Massachusetts designation is Schedule VI.",
        "why": "Incorrect. DPH states the opposite: pharmacies report Schedule II–V dispenses AND gabapentin, which is a special additional Schedule VI drug of concern."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "M.G.L. c.94C §18(c); 105 CMR 700.002(F), 700.012; Massachusetts DPH Pharmacy Reporting and Data Submission (gabapentin)",
    "url": "https://www.mass.gov/info-details/mass-general-laws-c94c-ss-18",
    "verified": "2026-11-17",
    "note": "One CT prescriber, two controls: out-of-state SIV alprazolam demands special authenticity verification; SVI gabapentin does not, but MUST be reported to MassPAT."
  },
  {
    "id": "E30-213",
    "set": 43,
    "area": 2,
    "kind": "single",
    "topicKey": "public-health-prescribing",
    "topic": "Injectable cabotegravir: dispensing by administration is not authority to prescribe",
    "stem": "A 28-year-old brings a valid prescriber-issued order for FDA-approved cabotegravir long-acting IM injection to prevent HIV. A Massachusetts pharmacist has appropriate training and CPR certification and can meet all screening, consent, documentation and product handling rules. The patient also asks the pharmacist to prescribe future injectable cabotegravir doses independently, citing pharmacists' separate authority to initiate ORAL PrEP. What is the best response under current 2026 DPH circulars?",
    "choices": [
      {
        "text": "Refuse to administer cabotegravir because pharmacists can give vaccines but never injectable HIV-prevention drugs.",
        "why": "Incorrect. DCP 26-03-124 specifically includes cabotegravir as a pharmacy-administered HIV-prevention drug for eligible adults under a valid prescription."
      },
      {
        "text": "Administer the already-prescribed eligible dose if all DCP 26-03-124 safeguards are met, but do not assume the ORAL-PrEP independent prescribing guidance authorizes new pharmacist-originated injectable orders.",
        "why": "Correct. DCP 26-03-124 independently permits properly trained pharmacist or intern IM administration under a lawful prescription. DCP 26-08-125 and the statewide ORAL PrEP guideline are different prescribing authority; administration does not confer carte-blanche injectable prescribing."
      },
      {
        "text": "Authorize all future injections because any patient's valid first prescription delegates all future prescribing authority to the administering pharmacy.",
        "why": "Incorrect. A valid prescription permits the stated administration subject to the order and safeguards; it does not transfer general independent prescribing authority."
      },
      {
        "text": "Replace the IM injection with an IV infusion at the patient's request, since injection route does not matter under the 2026 DPH policy.",
        "why": "Incorrect. Circular DCP 26-03-124 restricts authorized administration to prescribed subcutaneous or intramuscular routes consistent with product labeling; intravenous administration is excluded."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "DPH Circular DCP 26-03-124 March 11, 2026, pp.1–3 (administration/eligible cabotegravir/valid Rx); DCP 26-08-125 Aug. 25, 2026 (prescribing); Statewide Pharmacist Oral PrEP Guidelines 8-2026",
    "url": "https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download",
    "verified": "2026-11-17",
    "note": "Prescribing and administering are different authorities. A pharmacist may administer prescribed adult IM cabotegravir under circular 26-03; oral PrEP prescribing guidance does not automatically authorize issuing future injectable Rx."
  },
  {
    "id": "E30-214",
    "set": 43,
    "area": 3,
    "kind": "multi",
    "topicKey": "drug-schedule-identification",
    "topic": "Xcopri versus Keppra: federal/MA scheduling, original refill expiration and MassPAT",
    "stem": "A Massachusetts pharmacist receives requests for refills under two otherwise lawful outpatient prescriptions, each issued EIGHT MONTHS AGO with unused refills. Product X is regular XCOPRI (cenobamate) oral tablets and Product Y is regular KEPPRA (levetiracetam) oral tablets. No updated Rx, emergency authority or other exception applies. Which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Xcopri is Massachusetts Schedule VI because all antiseizure medicines follow the same state classification; its eight-month-old Rx is usable for a year.",
        "why": "Incorrect. Cenobamate is expressly DEA Schedule V under 21 CFR 1308.15; Massachusetts adopts that Schedule V designation, which has a six-month refill expiration."
      },
      {
        "text": "Xcopri is federal and MA Schedule V; its original eight-month-old Rx cannot be used for refills, and a new lawful outpatient dispensing is MassPAT-reportable.",
        "why": "Correct. 21 CFR 1308.15 lists cenobamate; MA 105 CMR 700.002(E) adopts federal V, 247 CMR 9.04(13) limits the Rx to six months, and PMP reporting covers Schedules II–V."
      },
      {
        "text": "Keppra must also be federal Schedule V because levetiracetam and cenobamate both treat seizures.",
        "why": "Incorrect. Drug indication or class does not determine DEA schedule. Levetiracetam is not DEA-scheduled; as a prescription drug it is Massachusetts Schedule VI."
      },
      {
        "text": "Keppra is federal nonscheduled and MA Schedule VI; its unchanged eight-month-old Rx can be refilled under the one-year rule when other conditions are met, and it is not routinely reported to MassPAT.",
        "why": "Correct. 105 CMR 700.002(F) places unscheduled Rx levetiracetam in MA VI, and 247 CMR 9.04(12) allows one year. DPH additionally reports gabapentin, not ordinary levetiracetam, among Schedule VI drugs."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "21 CFR 1308.15 (cenobamate); 105 CMR 700.002(E),(F); 247 CMR 9.04(12)–(13); DPH Pharmacy Reporting and Data Submission; FDA Keppra Rx labeling",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.15",
    "verified": "2026-11-17",
    "note": "Same epilepsy indication, different control: cenobamate federal/MA V 6-month Rx + PMP; levetiracetam federal nonscheduled/MA VI 1-year Rx and no usual PMP reporting."
  },
  {
    "id": "E30-215",
    "set": 43,
    "area": 4,
    "kind": "single",
    "topicKey": "sterile-hazardous-compounding",
    "topic": "ISO5 viable air 18 CFU: 2026 Board recall and reporting",
    "stem": "A Massachusetts sterile-compounding pharmacy receives a FINAL viable-air report showing 18 CFU recovered at its ISO Class 5 primary engineering control. Some CSPs prepared there have already been dispensed and are WITHIN their assigned BUDs; another separate ISO 5 PEC has acceptable results. No remediation has been completed. What is the best response under Board Policy 2026-03?",
    "choices": [
      {
        "text": "Stop affected routine compounding, promptly investigate, notify the Board within one business day of report receipt, consult a microbiologist, recall the within-BUD CSPs, contact prescribers and monitor for adverse events; make risk-based decisions about the unaffected PEC.",
        "why": "Correct. Policy 2026-03 §§II,III(C),V mandates reporting in one business day; ISO5 >15 CFU is significant loss of control with microbiologist, recall, prescriber contact and surveillance requirements."
      },
      {
        "text": "Report the result, but continue Category 1 CSPs in the contaminated PEC with their shorter BUDs while a single repeat sample is pending.",
        "why": "Incorrect. A significant loss of ISO5 control invokes stricter policy response; simply shortening BUD does not permit unrestricted routine compounding in an affected PEC."
      },
      {
        "text": "Quarantine undistributed CSPs but delay recall of already-dispensed within-BUD CSPs until a second sample establishes persistence of the 18-CFU excursion.",
        "why": "Incorrect. The finalized report exceeds the >15 CFU significant loss criterion; the policy requires a within-BUD CSP recall rather than awaiting another positive sample."
      },
      {
        "text": "Notify the Board within one business day measured from SAMPLE COLLECTION and recall only expired CSPs that were prepared before that sample.",
        "why": "Incorrect. The Board notification clock starts when the microbiology report is RECEIVED; required recall concerns CSPs still WITHIN their BUDs."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "Board Policy 2026-03 adopted Sept. 3, 2026, §§II,III(C),V; USP <797>; 247 CMR 9.01(3)",
    "url": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download",
    "verified": "2026-11-17",
    "note": "18 CFU ISO5 triggers action (>1 CFU) and significant loss (>15 CFU); reporting, recall and subsequent risk-based re-entry requirements.",
    "revision": 2
  },
  {
    "id": "E30-216",
    "set": 44,
    "area": 1,
    "kind": "multi",
    "topic": "Civil pharmacy negligence: limited prior-authorization notice duty versus Board discipline",
    "topicKey": "board-discipline",
    "stem": "A Massachusetts pharmacy repeatedly receives a valid antiseizure prescription, but the patient's insurer requires prior authorization (PA). Staff know that the patient risks an interruption of essential treatment. They tell the patient only that there is an 'insurance problem' and do not inform the prescriber that a PA is required. Based on the Massachusetts Supreme Judicial Court's pharmacy-negligence decisions, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The pharmacy must guarantee approval of the insurance authorization and keep contacting the prescriber until the prescriber confirms receiving every message.",
        "why": "Incorrect. Correa expressly rejected an open-ended duty to ensure that the physician received and acted on a PA request; the duty is to take reasonable notification steps, not to guarantee insurer coverage or prescriber response."
      },
      {
        "text": "A pharmacy may owe a limited duty to take reasonable steps to notify BOTH the patient and prescriber that prior authorization is needed.",
        "why": "Correct. In Correa v. Schoeck, 479 Mass. 686 (2018), the SJC recognized a limited duty to take reasonable steps to notify the patient and prescribing clinician of a PA barrier at each attempted fill; no universal duty to obtain the insurer's approval was imposed."
      },
      {
        "text": "Once an insurer rejects a claim, Massachusetts law categorically eliminates any pharmacy duty to communicate the reason to a patient or prescriber.",
        "why": "Incorrect. The specific PA communication duty recognized in Correa is a counterexample. A payment rejection is not an automatic blanket exemption from reasonable patient/prescriber notice, particularly where a serious treatment gap is known."
      },
      {
        "text": "A civil negligence duty does not require a prior formal Board disciplinary order; proving civil liability still requires the applicable elements, including breach, causation, and injury.",
        "why": "Correct. Civil negligence and professional license discipline are separate processes. The SJC's limited duty analysis does not depend on a Board conviction, but proving duty alone does not establish compensable negligence without breach and injury caused by it."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "Correa v. Schoeck, 479 Mass. 686, 694–702 (2018); Cottam v. CVS Pharmacy, 436 Mass. 316, 319–326 (2002); distinguish 247 CMR 10.03 Board discipline",
    "url": "https://law.justia.com/cases/massachusetts/supreme-court/volumes/479/479mass686.html",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Novelty vs E30-096/101/161/201: asks about a specific MA Supreme Judicial Court civil duty in insurance PA communication, not automatic Board sanction; original exam-style case, not recalled content."
  },
  {
    "id": "E30-217",
    "set": 44,
    "area": 2,
    "kind": "single",
    "topic": "Limited-English-proficiency counseling: interpreter access and HIPAA",
    "topicKey": "counseling-dur",
    "stem": "A Massachusetts pharmacy is covered by Section 1557 because it receives qualifying HHS financial assistance. A patient who has limited English proficiency accepts counseling for a new medicine but cannot understand the pharmacist's English explanation. The pharmacy has immediate access to a qualified remote interpreter. What should it do?",
    "choices": [
      {
        "text": "Arrange accurate, timely qualified language assistance without charging the patient, and counsel through the interpreter while protecting privacy; HIPAA ordinarily permits necessary treatment-related disclosure without separate authorization.",
        "why": "Correct. 45 CFR 92.201 requires meaningful, timely, accurate, no-cost language assistance in covered health programs. An appropriate qualified interpreter can facilitate counseling while protecting confidentiality; HIPAA generally permits provider use of interpreters for treatment or health care operations."
      },
      {
        "text": "Ask the patient's 12-year-old child to interpret as the default because a family member is always the preferred source of medical interpretation.",
        "why": "Incorrect. Section 1557's language-access protections generally prohibit reliance on accompanying minors for interpreting except narrowly defined exigent circumstances; convenience and assumed fluency do not establish qualified medical interpretation."
      },
      {
        "text": "Require the patient to pay for the remote interpreter before any counseling because the drug itself is covered by insurance.",
        "why": "Incorrect. Section 1557's required language assistance must be free of charge to the individual with limited English proficiency. Drug insurance coverage does not transfer this accessibility cost to the patient."
      },
      {
        "text": "Have any bilingual cashier translate clinical directions without checking competence or confidentiality, because fluent conversation automatically qualifies that employee as a medical interpreter.",
        "why": "Incorrect. Qualified interpretation requires accuracy, impartiality, relevant terminology and privacy safeguards. Being conversationally bilingual is not a categorical substitute for qualified healthcare interpretation."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "45 CFR 92.201(a)–(c) (meaningful access; qualified language assistance); 45 CFR 164.506(c) (HIPAA TPO); HHS OCR Section 1557 language-access guidance",
    "url": "https://www.hhs.gov/sites/default/files/ocr-dcl-section-1557-language-access.pdf",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Tests LEP access and interpreter privacy, distinct from E30-003/092/137 delegation of counseling and alternative contact."
  },
  {
    "id": "E30-218",
    "set": 44,
    "area": 2,
    "kind": "single",
    "topic": "Controlled substance office stock disguised as patient prescription",
    "topicKey": "controlled-prescriptions",
    "stem": "A DEA-registered physician sends a Schedule II oxycodone 'prescription' to a retail pharmacy listing the clinic as the patient and requesting 80 tablets for a shared cabinet. The physician intends to dispense doses later to whichever patients need them. No individual patient is named. What is the pharmacist's best response?",
    "choices": [
      {
        "text": "Fill the order as a normal outpatient prescription because the physician has a DEA registration and will document each future patient later.",
        "why": "Incorrect. A practitioner's valid DEA registration does not turn general office inventory into a patient-specific prescription. 21 CFR 1306.04(b) explicitly prohibits using an individual-practitioner prescription to obtain stock for future general dispensing."
      },
      {
        "text": "Enter the doctor's own name as the patient and dispense, provided the doctor initials the pharmacy's stock log.",
        "why": "Incorrect. Relabeling the clinic's planned office stock as a personal prescription would not create a legitimate patient-specific order. Documented intent still remains supply for general office dispensing."
      },
      {
        "text": "Dispense it if the practice promises to provide patient names at month's end, because retrospective patient assignment satisfies 21 CFR 1306.05.",
        "why": "Incorrect. A prescription must be legitimate at issuance and bear required patient information; a month-end accounting cannot retroactively convert a general stock replenishment into lawful patient-specific prescribing."
      },
      {
        "text": "Do not fill it as a prescription; distinguish acquisition of practitioner office inventory through lawful controlled-substance ordering/distribution from an order for a particular patient's treatment.",
        "why": "Correct. 21 CFR 1306.04(b) prohibits an individual practitioner issuing a controlled prescription to supply general dispensing stock. If the practitioner may lawfully acquire stock, that requires appropriate registrant purchasing or transfer processes rather than a disguised retail prescription."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "21 CFR 1306.04(a)–(b) (legitimate medical purpose; prohibition on Rx for office stock); 21 CFR 1306.05(a) (patient information); 21 CFR Part 1305 for qualifying Schedule II registrant orders",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.04",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Differs from E30-024 pharmacy-to-pharmacy five-percent distribution and E30-178 patient-specific red flags; physician is buying general office stock rather than treating a named patient."
  },
  {
    "id": "E30-219",
    "set": 44,
    "area": 3,
    "kind": "single",
    "topic": "Poison Prevention Packaging Act: product exceptions versus patient waiver",
    "topicKey": "label-packaging",
    "stem": "A pharmacy dispenses (X) sublingual nitroglycerin tablets, (Y) a cyclic oral contraceptive in the manufacturer's mnemonic dispenser, and (Z) ordinary oral antibiotic tablets. The patient and prescribers have requested no conventional-container waiver. Which description follows the federal PPPA prescription-drug packaging provisions?",
    "choices": [
      {
        "text": "All three products universally require child-resistant packaging because every drug taken by mouth is included with no exceptions.",
        "why": "Incorrect. 16 CFR 1700.14(a)(10) expressly excepts specified products, including sublingual nitroglycerin and qualifying cyclic hormonal contraceptives in manufacturer mnemonic dispensers."
      },
      {
        "text": "X and the qualifying Y are listed exemptions; Z ordinarily needs compliant special packaging unless a separate valid exception or consumer/prescriber request applies.",
        "why": "Correct. Section 1700.14(a)(10)(i) exempts sublingual nitroglycerin; (iv) exempts certain cyclically administered contraceptives in manufacturers' mnemonic packages. An otherwise covered ordinary oral antibiotic remains subject to special-packaging requirements absent a valid exception."
      },
      {
        "text": "Every package of any hormonal contraceptive is exempt, including loose tablets moved into an ordinary pharmacy vial regardless of the container.",
        "why": "Incorrect. The cited cyclic contraceptive exception is tied to a qualifying manufacturer's mnemonic dispenser and specified hormone activity; it does not convert all repackaged contraceptive tablets into a blanket exemption."
      },
      {
        "text": "A pharmacist may choose non-child-resistant packaging for Z based solely on convenience without an applicable statutory exemption or any patient/prescriber request.",
        "why": "Incorrect. The pharmacist cannot unilaterally replace PPPA-compliant packaging simply for convenience. A qualifying request or specific product-based exception is needed under the PPPA."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "16 CFR 1700.14(a)(10)(i),(iv) (special-packaging exemptions); 16 CFR 1701.1 and PPPA consumer/prescriber conventional-packaging requests; CPSC Healthcare Professional Guide (2023)",
    "url": "https://www.ecfr.gov/current/title-16/chapter-II/subchapter-E/part-1700/section-1700.14",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Unlike E30-029, tests expressly exempt product/package types rather than carrying forward a patient-specific child-resistant waiver."
  },
  {
    "id": "E30-220",
    "set": 44,
    "area": 4,
    "kind": "multi",
    "topic": "DEA pharmacy closure/ownership transfer: registration and controlled-stock records",
    "topicKey": "controlled-inventory",
    "stem": "A Massachusetts DEA-registered pharmacy is being acquired by a different legal owner, which will operate under its own appropriate DEA authority. The outgoing registrant will discontinue its controlled-substance business by transferring remaining stock, including Schedule II medications, to the buyer. No DEA Special Agent in Charge waiver of advance notice applies. Which steps meet 21 CFR 1301.52? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Send the required transfer information to the DEA Special Agent in Charge at least 14 days before the proposed controlled-stock business transfer, absent an individual waiver.",
        "why": "Correct. Under 21 CFR 1301.52(d), a registrant discontinuing controlled business by transferring stock to another person generally submits prescribed information to the local Special Agent in Charge at least 14 days in advance unless this period is waived."
      },
      {
        "text": "Skip the transfer-date inventory because the seller's annual accounting statement already lists the acquisition price of all narcotics.",
        "why": "Incorrect. A financial asset valuation does not replace the mandatory complete controlled-substance inventory required at the transfer, nor does it satisfy the required registrant records."
      },
      {
        "text": "Take a complete inventory on the transfer date serving as the seller's final and buyer's initial inventory, preserve copies for both parties, and use DEA Form 222 or authorized electronic ordering for Schedule II transfers.",
        "why": "Correct. Section 1301.52(d)(1)-(2) uses the on-transfer inventory for both registrants and directs Schedule I–II transfers to Part 1305 order forms, in addition to transferring the required controlled-substance records."
      },
      {
        "text": "Continue indefinitely using the seller's DEA registration at the new entity solely because the pharmacy name and Manager of Record did not change.",
        "why": "Incorrect. Under §1301.52(a)-(b), DEA registration does not automatically transfer to a different legal registrant. DEA authority must independently support the acquiring registrant's operations; name or MOR continuity is not a substitute."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "21 CFR 1301.52(a)–(b),(d)(1)–(2); 21 CFR 1304.11 (inventory); 21 CFR Part 1305 (Schedule II orders); 247 CMR 6.11 (separate MA pharmacy ownership process)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.52",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Novel DEA final/initial inventory and 14-day business-transfer reporting compared with E30-065 MA facility licensing and E30-180 reverse distributor destruction."
  },
  {
    "id": "E30-221",
    "set": 45,
    "area": 1,
    "kind": "single",
    "topic": "Technician immunization authorization: biennial continuing training",
    "topicKey": "technician-scope",
    "stem": "A Massachusetts licensed, nationally certified pharmacy technician completed the full initial vaccine-administration training and on-the-job skills assessment in 2023. The technician has current CPR certification and remains otherwise qualified, but completed NO immunization-related CE or updated training in the last three years. The pharmacy plans to assign vaccines tomorrow. What requirement must be addressed first under revised Board Policy 2023-02?",
    "choices": [
      {
        "text": "Repeat an entire new 1,500-hour pharmacy technician trainee experience because immunization authorization always expires after two years.",
        "why": "Incorrect. Policy 2023-02 establishes a biennial immunization education/update requirement, not an automatic reset of the technician licensure/training-employment pathway after two years."
      },
      {
        "text": "No additional training is necessary while national certification and CPR remain active, because vaccine training is permanently valid once completed.",
        "why": "Incorrect. National technician certification and CPR are separate prerequisites. The policy expressly adds periodic immunization-specific education or updated training regardless of those other credentials."
      },
      {
        "text": "Complete at least two hours of immunization-related continuing education or updated training within the required two-year cycle before returning to the vaccinator role.",
        "why": "Correct. Revised Policy 2023-02, §III(D)(5), requires at least two hours of immunization-related continuing education or updated training every two years. The prior initial six-hour program and two on-the-job hours do not substitute for maintaining this ongoing requirement."
      },
      {
        "text": "A supervising pharmacist may waive the biennial education entirely by reviewing the technician's last five administered vaccines.",
        "why": "Incorrect. Supervising-pharmacist clinical oversight does not create an exception to the Board's specified two-hours-every-two-years requirement. Reviewing past injections alone is not the stated education or updated training."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "Massachusetts Board Policy 2023-02, revised September 4, 2025, §III(D)(1)–(5): initial qualifications and two-hour immunization CE/updated training every two years",
    "url": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Unlike E30-062/191, tests continued eligibility after initial training rather than 500 post-license work hours or vaccine selection."
  },
  {
    "id": "E30-222",
    "set": 45,
    "area": 2,
    "kind": "multi",
    "topic": "Community CDTM: adding a different diagnosis to an individual referral",
    "topicKey": "cdtm-patient-practice",
    "stem": "A community pharmacist's current CDTM agreement includes protocols for hypertension and diabetes. One adult patient has signed informed consent, but the supervising physician's written patient-specific referral identifies HYPERTENSION only and no diabetes comorbidity. The patient asks the pharmacist to start diabetes drug therapy under the existing agreement. Which statements follow 247 CMR 16.03–16.04? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The supervising physician should include the patient's diabetes diagnosis in a valid written referral or subsequent referral before CDTM management of that added condition.",
        "why": "Correct. Under 247 CMR 16.03(5)(c)(2), the supervising physician must specify each primary and secondary diagnosis in the written patient referral or a subsequent referral. Community-CDTM prescribing for comorbidities additionally must be authorized in the patient referral."
      },
      {
        "text": "The pharmacist may start any diabetes drug listed in the general CDTM protocol solely because that disease appears in the agreement, even though it is absent from this patient's referral.",
        "why": "Incorrect. The community pathway requires the physician's individual referral to specify the patient's primary and secondary diagnoses; a broad agreement listing diabetes does not automatically make the patient referred for that condition."
      },
      {
        "text": "A new individual referral automatically permits the community pharmacist to initiate a Schedule III controlled medication whenever the physician agrees orally.",
        "why": "Incorrect. The patient-specific referral cannot extend community CDTM prescribing beyond the authorized Schedule VI scope under 247 CMR 16.03(5), even when a physician is aware of the new condition."
      },
      {
        "text": "The physician must obtain and record written informed consent for this collaboration, provide the patient a copy, and maintain the original consent while supplying the pharmacist a copy as required.",
        "why": "Correct. Sections 16.03(5)(c)-(d) and 16.04(1) require patient-specific written informed consent and defined distribution/record custody. The physician retains the original and transmits a copy to the pharmacist within 24 hours."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 16.03(5)(c)(1)–(4),(d),(e)(1)(b)(ix),(e)(3)–(4); 247 CMR 16.04(1) (patient-specific referral/consent and community CDTM prescriptive limits)",
    "url": "https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Distinct from E30-036 diabetes dose modification already under a diabetes-specific referral; tests a new diagnosis absent from the individual referral."
  },
  {
    "id": "E30-223",
    "set": 45,
    "area": 2,
    "kind": "single",
    "topic": "PDMA practitioner sample distribution versus retail-pharmacy resale",
    "topicKey": "drug-integrity",
    "stem": "A manufacturer proposes sending sealed 'Drug Sample — Not for Resale' packages by courier to a hospital pharmacy at the signed WRITTEN request of a physician licensed to prescribe the drug. The manufacturer verifies the physician's authority before shipment; a hospital recipient signs the required receipt, and the samples will be provided only under lawful practitioner sample procedures. Which assessment is most accurate?",
    "choices": [
      {
        "text": "This hospital-practitioner sample route can be lawful, but the samples may not then become ordinary retail saleable stock or be used for pharmacy repackaging/compounding resale.",
        "why": "Correct. Federal PDMA rules recognize the licensed-practitioner request and hospital-pharmacy recipient with documented receipt. Massachusetts 247 CMR 9.01(6) separately prohibits pharmacies accepting/purchasing samples for compounding, repacking, or reselling them."
      },
      {
        "text": "The manufacturer must refuse because all shipment of drug samples to any pharmacy is forbidden, even when a physician has submitted the specific request allowed by federal law.",
        "why": "Incorrect. 21 CFR 203.30–203.31 expressly permit qualifying manufacturer or authorized-distributor shipments to a hospital or other healthcare-entity pharmacy at a licensed practitioner's written request when verification, delivery receipt and other rules are met."
      },
      {
        "text": "A hospital recipient can sell the samples to outpatients at full retail price as soon as the receipt is signed because the receipt converts the inventory to commercial product.",
        "why": "Incorrect. The signed receipt provides required traceability and confirmation of sample delivery; it does not authorize selling products marked as drug samples not for resale."
      },
      {
        "text": "Only a verbal promise by the physician is needed, and the supplier need not verify prescribing licensure or obtain a documented delivery receipt.",
        "why": "Incorrect. 21 CFR 203.30(a) imposes an advance signed written request, verification of the requester's prescriptive authority, and a written recipient receipt returned to the manufacturer or distributor, among other requirements."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "21 CFR 203.30(a)(1)–(4),(b)–(c), 203.31(a) (PDMA drug sample requests and receipts); 247 CMR 9.01(6) (sample resale/compounding/repackaging restriction)",
    "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-203/subpart-D/section-203.30",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Unlike E30-132, which tests illegal pharmacy resale of samples, tests the authorized clinician-request sample supply chain and recipient records."
  },
  {
    "id": "E30-224",
    "set": 45,
    "area": 3,
    "kind": "single",
    "topic": "Unfilled electronic CII transfer: direct licensed-pharmacist communication and electronic annotations",
    "topicKey": "refills-transfers",
    "stem": "A patient requests transfer of an UNFILLED electronic Schedule II prescription from Massachusetts retail Pharmacy A to another registered Massachusetts retail Pharmacy B. Both systems can transfer the original EPCS without altering any content. Pharmacy A instead proposes to print a PDF, email it to B's technician, and delete the old electronic record. Which procedure complies with Massachusetts Policy 2023-10 and 21 CFR 1306.08?",
    "choices": [
      {
        "text": "A may send the printed PDF to a technician at B because the transfer remains electronically documented in an email attachment.",
        "why": "Incorrect. Federal 21 CFR 1306.08(f)(1) requires an EPCS initial-fill transfer to stay in electronic prescription form; a PDF, email document or fax intermediary is not lawful conversion of that electronic prescription."
      },
      {
        "text": "The certified technician at A can conduct the entire Schedule II transfer without pharmacist involvement when the pharmacies share a cloud platform.",
        "why": "Incorrect. Section 1306.08(f)(3) requires communication directly between TWO licensed pharmacists for the controlled initial-fill transfer. Massachusetts technician authority for Schedule VI transfers does not extend to Schedule II EPCS."
      },
      {
        "text": "A may delete the transmitting pharmacy's EPCS record after sending it once because DEA requires the receiving pharmacy alone to retain proof of the transfer.",
        "why": "Incorrect. 21 CFR 1306.08(f)(4)-(h) requires specified annotations at both transferring and receiving pharmacies and retention of electronic transfer records by both for two years."
      },
      {
        "text": "Use the authorized one-time electronic EPCS transmission directly between licensed pharmacists, preserve the full prescription unchanged, and record the transferring/receiving pharmacy and pharmacist details at both sites.",
        "why": "Correct. Massachusetts Policy 2023-10 adopts 21 CFR 1306.08(e)-(h) for unfilled Schedule II–V EPCS. The electronic prescription stays intact, both pharmacists communicate directly, required dates/DEA IDs/names are annotated and retained at both pharmacies."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "MA Board Policy 2023-10 I–II (Unfilled Prescriptions); 21 CFR 1306.08(e)–(h) (initial-fill EPCS transfer, documentation, retention); 247 CMR 9.14",
    "url": "https://www.mass.gov/doc/2023-10-unfilled-prescriptions-pdf/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Compared with E30-007 generic permission to transfer unfilled Rx, tests conversion prohibition, licensed-pharmacist actor, annotations and bilateral records."
  },
  {
    "id": "E30-225",
    "set": 45,
    "area": 4,
    "kind": "multi",
    "topic": "After 2026 viable-air action result: repeat EM and normal BUD restoration",
    "topicKey": "sterile-hazardous-compounding",
    "stem": "A Massachusetts sterile-compounding pharmacy had an above-action-level VIABLE AIR result in its ISO 7 buffer room. It notified the Board and performed an RCA, appropriate remediation, CAPA and risk assessment; no nonviable particle excursion or additional Board restriction exists. The pharmacy now wants to return to ordinary beyond-use dates. Under Board Policy 2026-03, which actions are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Immediately restore ordinary Category 2 BUDs after completing a deep clean, without microbiology results, because the original excursion was viable rather than nonviable.",
        "why": "Incorrect. Under §IV(B)(2), restoration of standard BUDs depends on repeat EM falling below action levels; deep cleaning alone, particularly a sample collected immediately after cleaning, is not accepted proof of sustained control."
      },
      {
        "text": "Perform repeat environmental monitoring based on the affected ISO-classified area and action-level type; re-sample ALL sampling locations in the affected ISO area at the same time.",
        "why": "Correct. Policy 2026-03 §IV(B)(1) permits repeat EM focused on the affected classified area/type as supported by the monitoring plan, but requires all sampling locations within that affected area to be re-sampled simultaneously."
      },
      {
        "text": "If proper remediation has occurred and repeat EM is below the policy's action levels, the pharmacy may resume its standard BUDs or compounding, as otherwise permitted.",
        "why": "Correct. Policy §IV(B)(2) expressly allows restoration of standard BUDs or resumption of compounding when repeat EM is below action levels, subject to compliance with otherwise applicable sterile standards."
      },
      {
        "text": "If repeat EM still exceeds the action level, it is sufficient to record a numerical improvement and ignore the Board's response and remediation requirements.",
        "why": "Incorrect. Section IV(B)(3) sends repeated action-level results back to §III response duties. A smaller but still above-threshold CFU reading is not clearance and cannot automatically support normal BUDs."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "MA Board Policy 2026-03 §IV(A)–(C), especially IV(B)(1)–(3), Environmental Monitoring action level response (adopted September 3, 2026); USP <797> applicable EM standards",
    "url": "https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "This asks how to establish successful remediation and RESTORE normal BUDs, rather than E30-160 initial ISO7 excursion treatment or E30-215 ISO5 18CFU initial recall. Board policy directly verified; subscribed USP full text not represented as accessed."
  },
  {
    "id": "E30-226",
    "set": 46,
    "area": 1,
    "kind": "single",
    "topic": "Pharmacist continuing education audit: proof and retention",
    "topicKey": "licensure-ce",
    "stem": "A Massachusetts pharmacist earned three hours of qualifying non-ACPE professional education 18 months ago. Those credits do NOT appear in NABP CPE Monitor, and the Board requests proof during a random CE audit. The pharmacist has only a calendar entry showing the seminar title. Which action best addresses 247 CMR 4.06 and Board Policy 2021-04?",
    "choices": [
      {
        "text": "Tell the Board that CPE Monitor is the only acceptable record and therefore the missing non-ACPE credit cannot be checked.",
        "why": "Incorrect. Board Policy 2021-04 recognizes certain non-ACPE credits but requires the pharmacist to retain sufficient completion documentation when the education does not appear in CPE Monitor; the Board may request those records."
      },
      {
        "text": "Provide retained evidence of successful completion showing the approved provider, participant, program title/number, completion date, and hours; maintain such records for the required period and provide them on audit.",
        "why": "Correct. 247 CMR 4.06(1)-(2) requires documentation or statements of credit containing the specified identifying details, maintained at least two years from completion and submitted on Board request/random audit. Policy 2021-04 further describes evidence expected for non-ACPE activity."
      },
      {
        "text": "Submit the personal calendar entry alone because a pharmacist's own note is automatically equivalent to a statement of completed contact hours.",
        "why": "Incorrect. An unauthenticated calendar entry showing only a seminar title does not demonstrate successful completion or identify all required provider, participant, activity, date and credit details."
      },
      {
        "text": "Refuse the audit request until the next license renewal because the Board may verify CE only at the end of a biennial renewal period.",
        "why": "Incorrect. Section 4.06(2) expressly permits random audits and Board requests for documentation independent of the moment of renewal."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 4.06(1)–(2) (CE completion records retained at least two years and provided on audit); Board Policy 2021-04 §I (most recent two full calendar years; non-ACPE certificate details)",
    "url": "https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Tests authentic CE records on random audit, not E30-201 deliberate fabrication or E30-146 compounding specialty hour quota."
  },
  {
    "id": "E30-227",
    "set": 46,
    "area": 2,
    "kind": "multi",
    "topic": "42 CFR Part 2 intermediary: patient request for disclosure recipient list",
    "topicKey": "privacy-part2",
    "stem": "A federally assisted Part 2 treatment program received a patient's valid written consent using a GENERAL designation for disclosures through a named intermediary. The patient now sends that intermediary a WRITTEN request for a list of recipients of identifying records disclosed under that designation in the preceding three years. Which statements accurately describe 42 CFR 2.24? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The intermediary may refuse to identify recipient organizations because the patient previously consented to disclosures through a general designation.",
        "why": "Incorrect. The list requirement specifically protects patients who used general-designation consents; prior consent does not waive their ability to learn who received information under that designation."
      },
      {
        "text": "The intermediary must respond to the patient's qualifying written request within 30 days of receipt.",
        "why": "Correct. Under 42 CFR 2.24(b)(1), an intermediary named on the general-designation consent must respond in 30 or fewer days after receiving the qualifying written request."
      },
      {
        "text": "This intermediary list automatically establishes an unrestricted, immediately effective right to a full accounting of every HIPAA treatment disclosure through any technology, regardless of applicable HHS compliance-date limits.",
        "why": "Incorrect. The narrow §2.24 intermediary list is not the broader §2.25 electronic-health-record accounting right. HHS has stated that the §2.25 accounting compliance date depends on the separate HIPAA accounting rule update; the two rights should not be conflated."
      },
      {
        "text": "For disclosures within the permitted three-year lookback, the list must identify the entities receiving information, disclosure date, and a brief description of the patient-identifying information disclosed.",
        "why": "Correct. Section 2.24(a) limits the written request to the previous three years and §2.24(b)(2) specifies recipient entity name(s), date and a brief description of identifying information."
      }
    ],
    "correct": [
      "B",
      "D"
    ],
    "citation": "42 CFR 2.24(a)–(b) (specific intermediary's 30-day response and 3-year request); contrast 42 CFR 2.25 and HHS 2024 Part 2 final-rule fact sheet (accounting compliance-date caveat)",
    "url": "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2/section-2.24",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Distinct from E30-028 consent/SUD notes and E30-203 notice/fundraising; narrower intermediary-rights rule avoids treating the deferred general accounting implementation as effective."
  },
  {
    "id": "E30-228",
    "set": 46,
    "area": 2,
    "kind": "single",
    "topic": "Lenalidomide REMS: expired pharmacy confirmation number",
    "topicKey": "rems",
    "stem": "A Lenalidomide REMS-certified pharmacy has a valid new lenalidomide prescription from a certified prescriber for an appropriately enrolled patient. All risk-category and pregnancy-test obligations have been met. The pharmacy obtained the required REMS CONFIRMATION number 26 hours ago but has not yet handed over or shipped the drug. The confirmation was not renewed. What must it do?",
    "choices": [
      {
        "text": "Do not dispense until the expired confirmation has been canceled and a new valid REMS confirmation is obtained; continue the required counseling and Medication Guide steps.",
        "why": "Correct. The active Lenalidomide REMS pharmacy procedures state that a confirmation number is valid for only 24 hours. When it has expired, the pharmacy must cancel the old number and obtain a new one before dispensing while complying with the remaining REMS safeguards."
      },
      {
        "text": "Dispense immediately because once a confirmation number is issued it remains valid until the prescriber writes the next prescription.",
        "why": "Incorrect. The Lenalidomide REMS Pharmacy Guide limits a pharmacy confirmation number's validity to 24 hours. A confirmation obtained 26 hours earlier is no longer sufficient for dispensing."
      },
      {
        "text": "Convert the order into an ordinary Schedule VI prescription with automatic refills because enrollment in the REMS makes subsequent confirmation optional.",
        "why": "Incorrect. A REMS is a distribution/safe-use restriction, not a controlled-schedule exception. Lenalidomide REMS independently requires confirmation before each dispensing and does not allow ordinary automatic refills."
      },
      {
        "text": "Send the medication without the Medication Guide if the prescriber countersigns the expired number, because pharmacist certification alone satisfies the REMS.",
        "why": "Incorrect. A prescriber countersignature cannot extend the 24-hour program confirmation; pharmacist certification also does not cancel the Medication Guide and patient-counseling requirements."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "FDA-approved Lenalidomide REMS Pharmacy Guide, steps 3–4: valid 24-hour pharmacy confirmation, cancellation/reissue when expired, Medication Guide; 247 CMR 9.01(21) (comply with product REMS)",
    "url": "https://www.lenalidomiderems.com/pharmacist-resources/index.html",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Specific current program source: https://www.lenalidomiderems.com/media/wp-content/uploads/LEN_Pharmacy_Guide.pdf. Distinct from E30-063 isotretinoin windows and E30-183 esketamine REMS site administration."
  },
  {
    "id": "E30-229",
    "set": 46,
    "area": 3,
    "kind": "single",
    "topic": "Massachusetts generic interchange: special container label and manufacturer",
    "topicKey": "label-packaging",
    "stem": "A Massachusetts Drug Store Pharmacy receives a brand-name tablet prescription without 'no substitution' and lawfully dispenses a LOWER-COST interchangeable generic manufactured by Company Z. The pharmacist accurately applies all routine label elements. Which additional interchange labeling follows 247 CMR 9.05(3)?",
    "choices": [
      {
        "text": "The label needs only the originally prescribed brand name; the identity of the actual lower-cost generic manufacturer is confidential commercial information.",
        "why": "Incorrect. Section 9.05(3)(a) specifically requires the label to identify the actual generic product and its manufacturer in an interchange statement; showing only the prescribed brand would not communicate what was dispensed."
      },
      {
        "text": "The pharmacy may label the generic as if it were the brand when both are therapeutically equivalent, with no interchange statement if the price is lower.",
        "why": "Incorrect. Therapeutic interchangeability authorizes selection under applicable circumstances but does not waive the separate container labeling obligation in §9.05(3)."
      },
      {
        "text": "Use 'Interchange' (or the commonly understood abbreviation 'IC') with the generic drug name and Company Z as manufacturer; the prescribed brand may additionally be identified in the permitted form.",
        "why": "Correct. Section 9.05(3)(a),(c)-(d) requires the 'Interchange' generic name/manufacturer presentation for a less expensive dispensed generic and permits recognized abbreviations, e.g. 'IC', plus an optional 'for [prescribed brand]' notation."
      },
      {
        "text": "The pharmacy must print the manufacturer's complete legal corporate name in full and is never permitted to abbreviate 'interchange' or the manufacturer's name.",
        "why": "Incorrect. Section 9.05(3)(d) expressly allows commonly understood abbreviations, including 'IC' and recognized abbreviations for manufacturer names."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 9.05(3)(a)–(e), generic/brand interchange container label and abbreviations; M.G.L. c.112 §12D (interchange authority)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Not E30-194 missing pharmacist initials or E30-019 whether interchange is required; tests exact label identifying actual substituted product and manufacturer."
  },
  {
    "id": "E30-230",
    "set": 46,
    "area": 4,
    "kind": "multi",
    "topic": "Hospital nursing-unit controlled-stock accountability and witnessed waste",
    "topicKey": "pharmacy-operations",
    "stem": "A Massachusetts hospital moves bulk Schedule II–V controlled drugs from its pharmacy to an authorized nursing-unit medication cart. Its procedures are being evaluated against the Massachusetts DPH 'General accountability guidelines for controlled substances in hospitals and clinics with pharmacies.' Which measures comply? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Use a double-locked, permanently affixed cabinet or medication cart for nursing-unit Schedule II–V stock, with hard-copy or electronic perpetual inventory.",
        "why": "Correct. Massachusetts DPH's nursing-unit accountability guidance states that Schedule II–V controlled drugs must be in a double-locked, permanently affixed unit/cart with perpetual inventory records."
      },
      {
        "text": "Permit any unlicensed visitor to access the cart if the nurse on duty says the visitor is trustworthy and the medication orders are patient-specific.",
        "why": "Incorrect. The DPH guidance restricts controlled-substance access to licensed, authorized staff; familiarity or visitor trust does not replace controlled inventory security."
      },
      {
        "text": "Have unused Schedule II–V portions wasted under the facility's controlled procedures by two licensed staff with co-signed documentation, unless more restrictive hospital policy applies.",
        "why": "Correct. The state DPH accountability guidance specifies two licensed staff and co-signature for disposal of unused Schedule II–V portions, subject to stricter facility policy."
      },
      {
        "text": "Skip documented nursing/pharmacy management accountability reviews once the cart has a software audit log, because electronic data eliminates ongoing diversion monitoring.",
        "why": "Incorrect. DPH calls for a documented quality-assurance review of controlled substances administered on nursing units not less than once weekly; an access log does not replace the management review."
      }
    ],
    "correct": [
      "A",
      "C"
    ],
    "citation": "Massachusetts DPH General Accountability Guidelines for Controlled Substances in Hospitals and Clinics with Pharmacies, Nursing Units—General and Schedule II–V; 105 CMR 700.005 (security and accountability); 247 CMR 9.12 (separate institutional ADD)",
    "url": "https://www.mass.gov/info-details/general-accountability-guidelines-for-controlled-substances-in-hospitals-and-clinics-with-pharmacies",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Explicitly tests documented nursing-unit stock security and waste, not E30-155 patient-specific order authorization for a hospital automated dispensing device. DPH guidance is identified as guidance rather than represented as independently enacted regulation."
  },
  {
    "id": "E30-231",
    "set": 47,
    "area": 1,
    "kind": "single",
    "topic": "PharmD graduate residency before pharmacist licensure: continuing pharmacy intern status",
    "topicKey": "intern-education",
    "stem": "A 2026 PharmD graduate from an approved pharmacy school has accepted a Massachusetts hospital residency. Their Massachusetts pharmacy INTERN license is active, but the Board has not issued a pharmacist license. The resident will work under the direct supervision of a registered pharmacist preceptor. What is permissible under 247 CMR 8.01?",
    "choices": [
      {
        "text": "The graduate is automatically a Massachusetts pharmacist as soon as the PharmD diploma is awarded and may independently perform final dispensing validation.",
        "why": "Incorrect. A degree or residency acceptance is not a Board-issued pharmacist license. 247 CMR 9.04(1) reserves final dispensing validation to the licensed pharmacist, regardless of graduation status."
      },
      {
        "text": "The graduate must cease all pharmacy-intern duties on graduation day even with an active intern license and a supervising preceptor.",
        "why": "Incorrect. Section 8.01(10) expressly permits a graduate of an approved school to continue acting in the capacity of pharmacy intern until becoming licensed as a pharmacist."
      },
      {
        "text": "The graduate may continue to practice in the pharmacy-INTERN capacity with an active Massachusetts intern license and appropriate pharmacist supervision during the residency, until pharmacist licensure is obtained.",
        "why": "Correct. 247 CMR 8.01(8) allows approved-school PharmD residents to hold a Massachusetts pharmacy intern license with pharmacist supervision, and subsection (10) preserves the intern role for graduates before pharmacist licensure."
      },
      {
        "text": "The hospital may replace the intern license with an out-of-state pharmacist license because any United States state license automatically permits independent Massachusetts residency dispensing.",
        "why": "Incorrect. The specific Massachusetts license or authorized intern status remains necessary. A pharmacist license in another state does not independently grant Massachusetts pharmacist authority."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "247 CMR 8.01(3),(8)(a)–(b),(10) (PharmD graduate resident and intern continuation); 247 CMR 9.04(1) (pharmacist final dispensing process validation)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Differentiates post-graduation supervised hospital resident status from E30-166 foreign graduate FPGEE authorization and E30-181 acceptance of out-of-state hours."
  },
  {
    "id": "E30-232",
    "set": 47,
    "area": 2,
    "kind": "multi",
    "topic": "MIIS pre-vaccination lookup: influenza versus zoster and COVID-19",
    "topicKey": "immunization",
    "stem": "A Massachusetts pharmacy offers routine adult influenza, recombinant zoster, and COVID-19 immunizations under otherwise valid standing orders. The pharmacist has current access to the Massachusetts Immunization Information System (MIIS), and the patients have no separate exemption. Under Board Policy 2023-02 revised 2025, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The same policy mandates MIIS review before each COVID-19 dose and gives no other way to verify prior vaccine formulation or dates.",
        "why": "Incorrect. Section IV(F) RECOMMENDS checking earlier COVID-19 vaccine formulation and dates and recognizes MIIS, pharmacy/EHR records or the vaccination card; that is not the identical mandatory pre-lookup rule used for zoster."
      },
      {
        "text": "Because influenza is excepted from pre-administration MIIS review, any influenza vaccine given at this pharmacy may be omitted entirely from MIIS reporting.",
        "why": "Incorrect. Section IV(G) requires pharmacy personnel to report administered vaccination information to MIIS, and 105 CMR 222.100 generally imposes a 72-hour reporting duty. A lookup exception is not a reporting waiver."
      },
      {
        "text": "The policy excludes INFLUENZA vaccination from its general mandatory pre-administration MIIS lookup requirement.",
        "why": "Correct. Policy 2023-02 §IV(E) requires reviewing MIIS before vaccines OTHER THAN influenza or COVID-19. The exemption is to that particular pre-administration lookup, not to the separate vaccine-record reporting requirements."
      },
      {
        "text": "For a routine recombinant ZOSTER vaccine, the pharmacy must check MIIS before administration to make sure the requested vaccination was not already administered by another provider.",
        "why": "Correct. The zoster vaccine is not one of the influenza/COVID-19 exceptions listed in §IV(E); the pharmacy must review MIIS in advance under the Board's vaccination policy."
      }
    ],
    "correct": [
      "C",
      "D"
    ],
    "citation": "Board Policy 2023-02 §§IV(E)–(G), revised September 4, 2025; 105 CMR 222.100(A) (MIIS immunization reporting)",
    "url": "https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Does not repeat E30-037 patient's MIIS data-sharing objection or E30-093 federal VIS/record fields; focuses on influenza/COVID-19 exception vs zoster mandatory precheck."
  },
  {
    "id": "E30-233",
    "set": 47,
    "area": 2,
    "kind": "single",
    "topic": "2026 Part 2 unsecured SUD-record breach notification under HIPAA-equivalent rule",
    "topicKey": "hipaa-breach",
    "stem": "A federally assisted substance-use-disorder treatment program subject to 42 CFR Part 2 discovers and confirms a BREACH of unsecured Part 2 patient records affecting 120 individuals. No low-probability-of-compromise finding or other exception applies. Under the Part 2 breach rule in force during November 2026, which notification plan is most accurate?",
    "choices": [
      {
        "text": "Because fewer than 500 individuals are affected, Part 2 requires neither patient notices nor reporting to HHS.",
        "why": "Incorrect. The HIPAA-equivalent breach rules apply to Part 2 records. The 500-person threshold changes some Secretary/media notification timing, but does not eliminate the obligation to notify affected patients of an actual breach."
      },
      {
        "text": "Give the notice only to the facility's qualified service organization because any Part 2 breach notice to patients would itself violate Part 2 confidentiality rules.",
        "why": "Incorrect. Part 2's confidentiality protections do not prohibit the specific notifications required by §2.16(b). An appropriately handled qualified service organization does not replace individual breach notices."
      },
      {
        "text": "Report to the Massachusetts Board of Pharmacy within seven business days and omit HHS notification, because Part 2 programs are not HIPAA covered entities.",
        "why": "Incorrect. Part 2 independently establishes breach notification obligations even for programs not otherwise HIPAA covered; a Board pharmacy-reporting clock does not replace Part 2's HHS/individual notifications."
      },
      {
        "text": "Notify the affected patients without unreasonable delay (no later than 60 calendar days after discovery) and report this under-500 breach to HHS within 60 days after the end of the calendar year.",
        "why": "Correct. 42 CFR 2.16(b) applies HIPAA Breach Notification Rule requirements. 45 CFR 164.404 requires individual notification without unreasonable delay and within 60 calendar days, while §164.408(c) permits the annual HHS report for breaches affecting fewer than 500 people within 60 days after the end of the calendar year."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "42 CFR 2.16(b) (Part 2 unsecured-record breach adopts HIPAA Breach Rule); 45 CFR 164.404(b) (individual notices), 164.408(c) (under-500 Secretary annual report); HHS OCR Part 2 breach guidance (compliance February 16, 2026)",
    "url": "https://www.hhs.gov/hipaa/part-2/index.html",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "E30-033 tests exactly-500 HIPAA breach media boundary; E30-073 tests encryption/compromise risk. This scenario tests Part 2 applicability to a 120-patient unsecured SUD record breach after February 2026."
  },
  {
    "id": "E30-234",
    "set": 47,
    "area": 3,
    "kind": "single",
    "topic": "Automatic-refill program: patient enrollment consent and opt-out",
    "topicKey": "refills-transfers",
    "stem": "A Massachusetts retail pharmacy wants to activate automatic monthly refills for a patient's valid Schedule VI maintenance prescription. The patient has authorized refills on file but has NEVER agreed to enroll in auto-refill. The patient later says they do not want automated fills. Which workflow follows 247 CMR 9.19(13)?",
    "choices": [
      {
        "text": "Obtain and record the patient's or agent's consent BEFORE enrollment and give the patient a way to discontinue participation; authorized refills alone do not waive either requirement.",
        "why": "Correct. Section 9.19(13) requires prior recorded patient/agent consent and a mechanism to end participation in an automatic refill program. Refill validity and amount remain independently governed by prescription laws."
      },
      {
        "text": "Enroll the patient automatically because having refills remaining on the original prescription is legally the same as consenting to a pharmacy's automatic refill program.",
        "why": "Incorrect. Prescription refill authorization from the prescriber and patient agreement to participate in pharmacy AUTOMATION are separate matters. §9.19(13) expressly requires obtaining and recording patient/agent consent before enrollment."
      },
      {
        "text": "A pharmacy may refuse to process any future ordinary refill unless the patient agrees to join its automatic refill system permanently.",
        "why": "Incorrect. Section 9.19(13) recognizes a patient's ability to stop the program. Participating in auto-refill is not an additional legal prerequisite to otherwise authorized ordinary refills."
      },
      {
        "text": "Once enrolled, the pharmacy may continue automatically dispensing after the prescription expires because the original enrollment consent replaces future prescriptions.",
        "why": "Incorrect. Auto-refill consent cannot extend the legal issuance/refill validity of the underlying Schedule VI prescription under 247 CMR 9.04(12)."
      }
    ],
    "correct": [
      "A"
    ],
    "citation": "247 CMR 9.19(13) (patient/agent recorded consent before auto-refill enrollment; discontinuation method); 247 CMR 9.04(12) (separate Schedule VI prescription validity)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Under-tested patient-choice automatic-refill practice, distinct from E30-084 transferring remaining refills and E30-089 unclaimed return-to-stock."
  },
  {
    "id": "E30-235",
    "set": 47,
    "area": 4,
    "kind": "multi",
    "topic": "Workplace prescription collection and direct handoff: lawful pharmacy-agent workflow",
    "topicKey": "medication-delivery-shipping",
    "stem": "A Massachusetts community pharmacy offers to collect prescriptions at a nearby factory for employees and eligible family members, then deliver completed prescriptions to the factory. It uses its own identified, authorized agents and satisfies other dispensing and counseling requirements. Under 247 CMR 9.04(9), which steps are lawful or required? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Limit the service to employees or others regularly affiliated with the location and eligible immediate family members who live at the same address as those employees or affiliates.",
        "why": "Correct. Section 9.04(9)(a) allows this particular workplace/group-affiliation collection pathway only for persons regularly employed/affiliated or their immediate family members residing at the same address."
      },
      {
        "text": "Have a pharmacist, pharmacy employee or authorized pharmacy agent personally collect prescriptions and dispense the medications DIRECTLY to each patient or the patient's agent.",
        "why": "Correct. Sections 9.04(9)(b)-(c) require in-person collection by an authorized pharmacy representative and direct handoff of filled medications to the patient or agent. A generic employer mailroom drop does not satisfy this narrow program."
      },
      {
        "text": "Leave prescriptions not immediately collected in a locked workplace drawer overnight so that the employer can distribute them later, rather than returning them to the pharmacy.",
        "why": "Incorrect. Section 9.04(9)(c)-(d) requires direct dispensing to the patient or agent and the return of medication not directly dispensed; medications may not be left or stored at the workplace."
      },
      {
        "text": "Assume the employer is solely responsible for the pharmacy's delivery agent, so the pharmacy and pharmacist have no legal accountability for that agent's conduct.",
        "why": "Incorrect. Section 9.04(9)(e) expressly holds the pharmacy and pharmacist responsible for conduct of the pharmacy employee or authorized agent acting on their behalf."
      }
    ],
    "correct": [
      "A",
      "B"
    ],
    "citation": "247 CMR 9.04(9)(a)–(e) (collection at industrial plants/workplaces, eligible recipients, direct handoff and undistributed return)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Distinct from E30-110 failed mail delivery with temperature excursion and E30-138 inpatient bedside-delivery consent. Tests workplace direct custody and pharmacy-agent accountability."
  },
  {
    "id": "E30-236",
    "set": 48,
    "area": 1,
    "kind": "single",
    "topic": "National certified technician credential lapses while Massachusetts technician license remains valid",
    "topicKey": "technician-scope",
    "stem": "A Massachusetts pharmacy technician has a CURRENT state pharmacy technician license, but their nationally recognized pharmacy technician certification expired last week. The MOR wants to count the employee as a certified technician in a 1:4 filling team and assign new telephone Schedule VI prescription intake. No renewal of national certification has occurred. What is correct?",
    "choices": [
      {
        "text": "The Massachusetts technician license also expires automatically the instant national certification lapses; the individual can perform no ordinary licensed technician duties.",
        "why": "Incorrect. Under 247 CMR 8.04(3), loss of national certification changes the person's CERTIFIED status and permitted role, not necessarily the separate validity of their current Massachusetts technician license."
      },
      {
        "text": "The individual may continue within ordinary licensed pharmacy technician duties, must use the 'Pharmacy Technician' title, and counts as a regular (noncertified) technician for supervisory ratios; the certified-only telephone new-prescription authority no longer applies.",
        "why": "Correct. 247 CMR 8.04(3)(a)-(c) provides all three consequences when certification lapses: reduced scope to §8.02, ordinary technician title, and ordinary-technician counting in §8.06 ratios. New information intake under §8.04(4)(c) requires current certified status."
      },
      {
        "text": "The employee can remain counted as certified for 90 days after certification expiration if the supervising pharmacist signs the personnel roster.",
        "why": "Incorrect. Section 8.04(3) contains no automatic 90-day national-certification grace period allowing certified scope or staffing-ratio credit; a manager's signature cannot invent a regulatory extension."
      },
      {
        "text": "A currently state-licensed technician whose national certification lapses may still perform final pharmacist dispensing validation if barcode and machine checks are available.",
        "why": "Incorrect. Final dispensing-process validation remains a pharmacist function under 247 CMR 9.04(1). Neither ordinary nor certified technician status permits taking over the final clinical validation responsibility."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 8.04(3)(a)–(c) (certification lapse: duties/title/ratios); 247 CMR 8.04(4)(c) and 8.02(6) (new Rx phone reception vs regular scope); 247 CMR 9.04(1)",
    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Different from E30-062/191 technician vaccine 500h qualification and E30-026 staffing-qualified 1:4 compositions; specifically tests national certification expiry and role downgrade."
  },
  {
    "id": "E30-237",
    "set": 48,
    "area": 2,
    "kind": "multi",
    "topic": "Schedule VI prescription continuity supply after expired prescription or zero authorized refills",
    "topicKey": "controlled-prescriptions",
    "stem": "A Massachusetts patient taking a stable Schedule VI maintenance medication has an expired prescription with no remaining refills. The pharmacist has tried but cannot obtain prescriber authorization in a timely manner and has assessed that continuing therapy is appropriate. Another patient asks for the same emergency authority for Schedule IV alprazolam. No other refill, emergency or waiver provision applies. Under 247 CMR 9.04(12), which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "The Schedule VI pharmacist may automatically supply a 90-day quantity on any expired prescription solely because the patient previously used the medicine for years.",
        "why": "Incorrect. The narrowly defined 14-day or smallest-available-unit-of-use limit controls; historical adherence does not confer unlimited extension of a stale prescription."
      },
      {
        "text": "For the Schedule VI patient, a pharmacist may exercise professional judgment to dispense a continuity quantity not exceeding 14 days OR the smallest available unit-of-use packaging in the stated circumstance.",
        "why": "Correct. Current 247 CMR 9.04(12) expressly authorizes pharmacist-judgment dispensing of up to 14 days or the smallest available unit-of-use package when a Schedule VI prescription is expired or lacks refills and prescriber authorization cannot be obtained promptly."
      },
      {
        "text": "Even though the normal one-year Schedule VI refill period has expired, the narrow continuity pathway may still apply if all its conditions are met; it is not an ordinary authorized refill.",
        "why": "Correct. Subsection 9.04(12) explicitly addresses expired/no-refill Schedule VI cases and grants a separate narrow dispensing pathway when timely prescriber authorization cannot be obtained. The pharmacist must still use professional judgment."
      },
      {
        "text": "The same §9.04(12) authority automatically permits a pharmacist to extend any expired Schedule IV benzodiazepine prescription for 14 days.",
        "why": "Incorrect. Section 9.04(12) is written specifically for Massachusetts Schedule VI. A federally controlled Schedule IV refill is subject to its separate federal and state rules and cannot be extended merely by importing this Schedule VI exception."
      }
    ],
    "correct": [
      "B",
      "C"
    ],
    "citation": "247 CMR 9.04(12) (MA Schedule VI one-year validity and narrow 14-day/smallest-unit-of-use emergency continuity supply); compare 247 CMR 9.04(13) and 21 CFR 1306.22 for federal CIII–V",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "New short-quantity continuity decision not previously tested in the 215 originals; current 2024 regulation says 14 days, NOT the 30 days in an older inspection-template excerpt."
  },
  {
    "id": "E30-238",
    "set": 48,
    "area": 2,
    "kind": "single",
    "topic": "Veterinarian federal Schedule III prescriptive authorization vs Schedule VI-only registration",
    "topicKey": "prescriber-authority",
    "stem": "A properly licensed Massachusetts veterinarian examines a dog after surgery and issues an otherwise complete patient-specific prescription for federally Schedule III buprenorphine for appropriate veterinary pain management. The veterinarian holds a Massachusetts Controlled Substance Registration (MCSR) covering Schedule VI ONLY and has NO DEA registration. The pharmacy has independently verified these facts. What should it do?",
    "choices": [
      {
        "text": "Dispense the Schedule III prescription because veterinarians are exempt from federal DEA registration whenever the medication is for an animal.",
        "why": "Incorrect. Veterinarian status does not grant blanket exemption from federal controlled-substance registration for Schedule II–V prescribing. Massachusetts DPH specifically distinguishes DEA registration for Schedules II–V from Schedule VI-only MCSR authority."
      },
      {
        "text": "Change the patient to the dog's owner and fill under the owner's human medical history because veterinarians may use a patient's relative to avoid controlled-registration limitations.",
        "why": "Incorrect. The patient is an animal being treated within a legitimate veterinarian-client-patient relationship. Rewriting the patient does not create DEA prescribing authority and can make the prescription fictitious."
      },
      {
        "text": "Do not dispense this Schedule III prescription on the stated registrations; the veterinarian must have appropriate DEA and Massachusetts controlled-schedule prescribing authority, although Schedule VI veterinary prescriptions follow a separate MCSR-only route.",
        "why": "Correct. M.G.L. c.94C §§7,18 and 105 CMR 700.004 require appropriate registrations/schedule authorization; DEA registration is needed for federally scheduled III drugs. The same veterinarian could prescribe lawful Schedule VI-only products under the narrower Massachusetts MCSR if other conditions are met."
      },
      {
        "text": "Apply the federal Schedule III five-refill allowance instead of verifying the prescriber's DEA number; remaining refills cure missing initial prescriptive authority.",
        "why": "Incorrect. Refill rules do not make an order valid when the practitioner lacks required authority for the federal controlled schedule at issuance."
      }
    ],
    "correct": [
      "C"
    ],
    "citation": "M.G.L. c.94C §§7,18(a); 105 CMR 700.004(C)–(D) (MCSR schedule authorizations); DEA 21 CFR 1306.03–1306.05; Massachusetts DPH Veterinary Prescriptions Best Practice Recommendations (January 9, 2025)",
    "url": "https://www.mass.gov/info-details/learn-about-massachusetts-controlled-substances-registration-mcsr-for-practitioners",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Contrast E30-208, where veterinarian has lawful VI MCSR to prescribe ordinary amoxicillin without a DEA number. This one tests missing federally scheduled III authority after a genuine animal exam."
  },
  {
    "id": "E30-239",
    "set": 48,
    "area": 3,
    "kind": "single",
    "topic": "MassPAT additional drug gabapentin: positive identification and hardship exception",
    "topicKey": "masspat",
    "stem": "A Massachusetts pharmacy dispenses prescribed gabapentin, a Massachusetts Schedule VI drug designated for PMP reporting, to an authorized patient representative at the counter. The representative has no government-issued ID. The pharmacist has credible facts showing that refusal today would cause serious hardship for the patient and can document the reason. What does 247 CMR 9.04(14) allow?",
    "choices": [
      {
        "text": "Ignore the ID requirement solely because gabapentin is federally nonscheduled; Massachusetts Schedule VI products cannot be designated additional drugs.",
        "why": "Incorrect. DPH designated gabapentin an additional PMP-reportable drug under 105 CMR 700.012(A)(1). Section 9.04(14) expressly extends positive identification to such additional drugs even though they are Massachusetts Schedule VI."
      },
      {
        "text": "Dispense under the narrow serious-hardship exception after documenting the reason and having the agent print a name and address and sign the reverse of the prescription or the pharmacy's paper/electronic log, provided all other dispensing rules are satisfied.",
        "why": "Correct. Section 9.04(14)(b)-(c) generally requires customer positive identification for PMP additional drugs. The specific alternative permits dispensing where denial would cause serious hardship, provided the justification is documented and the ultimate user or agent writes the specified information and signs."
      },
      {
        "text": "Require an ID without exception; 247 CMR 9.04(14) allows hardship alternatives for Schedule II–V drugs but explicitly excludes PMP additional drugs.",
        "why": "Incorrect. Section 9.04(14)(c) expressly covers both federal Schedule II–V products AND additional drugs in its documented serious-hardship alternative."
      },
      {
        "text": "Automatically treat a photo of a neighbor's driver's license as the representative's positive identification and omit all pharmacy documentation because the drug is not DEA controlled.",
        "why": "Incorrect. Customer identification concerns the actual ultimate user or agent presenting the prescription. Someone else's ID does not satisfy the rule, and a hardship-based dispensing requires the specific signed log and documented reason."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 9.04(14)(a)–(d) (positive identification for Schedules II–V and 'additional drugs', documented serious-hardship alternative); 105 CMR 700.012(A)(1) (gabapentin additional-drug reporting)",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Different from E30-005 Schedule II hardship-only case and E30-039 MassPAT reporting without physical pickup ID; integrates the additional-drug patient identity rule."
  },
  {
    "id": "E30-240",
    "set": 48,
    "area": 4,
    "kind": "multi",
    "topic": "Ransomware downtime: pharmacy continuity procedures, patient profiles and DUR records",
    "topicKey": "pharmacy-operations",
    "stem": "A Massachusetts retail pharmacy discovers ransomware and disables its compromised pharmacy computer system to protect patient records. The pharmacist can still obtain reliable lawful prescriptions, consult independent medication-history sources and perform a documented prospective DUR when safe, but new dispensing transactions cannot yet be entered into the normal electronic patient profiles. Under 247 CMR 9.19(22), 9.16 and 9.17, which operational responses are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "Follow a readily accessible written computer-downtime procedure that describes how prescriptions can be processed during downtime and how all medications dispensed will be entered into patient profiles when the system returns.",
        "why": "Correct. Section 9.19(22)(a)-(b) requires a downtime policy that includes a lawful filling process and later incorporation into the computerized pharmacy patient record. A breach does not eliminate the documentation/reconciliation obligation."
      },
      {
        "text": "Suspend all prospective DUR for the outage because the computer system normally generates interaction alerts; any technician may then dispense without pharmacist review.",
        "why": "Incorrect. Section 9.19(22)(d) requires an appropriate DUR process during downtime, and §9.17 keeps pharmacist prospective DUR obligations in force. A computerized alert is a tool, not a substitute for pharmacist judgment."
      },
      {
        "text": "Erase all original electronic prescription records after recovery and generate replacement records with new fictitious dispensing times so the breach will not appear in inspection logs.",
        "why": "Incorrect. Falsifying or deleting records to conceal the incident violates pharmacy recordkeeping duties and undermines lawful traceability. Downtime procedures call for accurate reconciliation, not fabrication or erasure."
      },
      {
        "text": "Protect confidentiality and use reliable alternative procedures for reviewing relevant patient history and documenting any clinical interventions; reconcile dispensing and DUR records when the system is restored.",
        "why": "Correct. Sections 9.16–9.17 require confidential, retrievable patient records and appropriate prospective review. The downtime plan must preserve continuity and ensure eventual patient-profile entry, without pretending records are currently accessible if they are not."
      }
    ],
    "correct": [
      "A",
      "D"
    ],
    "citation": "247 CMR 9.19(22)(a)–(d) (mandatory pharmacy computer downtime plan), 9.16(1),(7) (record retention/confidential profile), 9.17(1)–(2) (prospective DUR); HIPAA Security Rule 45 CFR 164.308–312 separately governs covered electronic PHI",
    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download",
    "verified": "2026-11-17",
    "revision": 1,
    "note": "Ransomware is the scenario; exact binding action tested is the Board's computer downtime continuity, profile reconciliation and DUR SOP, not a speculative cyber breach report deadline. Distinct from E30-085 controlled record segregation."
  }
];

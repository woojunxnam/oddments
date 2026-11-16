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
    "citation": "247 CMR 15.01; 247 CMR 15.03",
    "url": "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download",
    "verified": "2026-11-13"
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
    "citation": "247 CMR 4.02(3)-(5); Massachusetts Board of Registration in Pharmacy, Pharmacist Licensing: License Reactivation",
    "url": "https://www.mass.gov/pharmacist-licensing",
    "verified": "2026-11-14"
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
    "stem": "A Massachusetts-authorized practitioner has a temporary electrical failure that disables the electronic prescribing system. The practitioner issues an otherwise valid ORAL Schedule IV lorazepam prescription directly to a community pharmacist, who appropriately verifies the prescriber and prescription, assesses the legitimate medical purpose, and documents the oral order. There is no effort to circumvent electronic prescribing, and no other waiver or emergency exception is involved. Under 105 CMR 721.070 and applicable federal law, which statements are correct? SELECT ALL THAT APPLY.",
    "choices": [
      {
        "text": "A temporary technological or electrical failure can justify a non-electronic prescription under Massachusetts ePrescribing exceptions; an otherwise lawful oral Schedule IV prescription may be accepted.",
        "why": "105 CMR 721.070(A)(2) provides a temporary technology/electrical-failure exception to the state electronic prescribing mandate. Schedule IV prescriptions may otherwise be issued orally under federal law, including 21 CFR 1306.21, provided all applicable prescription requirements are met."
      },
      {
        "text": "Because federal rules permit oral Schedule IV prescriptions, the practitioner has no obligation to send written or electronic documentation afterward under Massachusetts law.",
        "why": "105 CMR 721.070(B) separately obligates a practitioner issuing an oral Schedule II–V prescription under an ePrescribing exception to cause a written or electronic prescription to be delivered within seven business days or any shorter period required by federal law. The absence of a general federal Schedule IV follow-up requirement does not erase this Massachusetts requirement."
      },
      {
        "text": "The practitioner must arrange a written or electronic follow-up within seven business days, or a shorter applicable federal deadline; a written follow-up must identify that it documents the earlier oral prescription.",
        "why": "105 CMR 721.070(B) requires the timely confirming written/electronic prescription. For a written confirmation, the practitioner must indicate that it is being issued to document an oral prescription. The seven-business-day Massachusetts period yields to any shorter applicable federal deadline."
      },
      {
        "text": "A pharmacist receiving an otherwise valid oral prescription does not have to independently establish that the prescriber qualified for an ePrescribing exception, although the pharmacist remains responsible for the prescription's authenticity, legality, and proper dispensing.",
        "why": "105 CMR 721.070(C) expressly states that the pharmacist need not verify whether an otherwise valid written or oral prescription properly falls under an ePrescribing exception. This narrow rule does not eliminate corresponding responsibility or other identity and prescription-validity checks."
      }
    ],
    "correct": [
      "A",
      "C",
      "D"
    ],
    "citation": "105 CMR 721.070(A)(2),(B),(C); 21 CFR 1306.21 (Schedule III–V oral prescriptions)",
    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download",
    "verified": "2026-11-15"
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
    "citation": "FDA iPLEDGE REMS, current FDA isotretinoin prescribing information (DailyMed), §5.2: certified pharmacy/authorization, seven-day window, 30-day supply, Medication Guide, no refills",
    "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9f1c8971-c6dc-4708-848b-5cee50b6c32a",
    "verified": "2026-11-15"
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
    "stem": "A properly trained and otherwise authorized Massachusetts pharmacist evaluates a sexually active 17-year-old who weighs 50 kg. Thirty-six hours earlier the patient sustained a percutaneous exposure to a blood-contaminated used syringe of a source with unknown HIV status. The patient reasonably fears HIV exposure, provides informed consent, has no known HIV infection or symptoms suggesting HIV, no relevant hypersensitivity or interacting therapy, and otherwise satisfies the September 2026 statewide pharmacist oral HIV post-exposure prophylaxis (PEP) protocol. A blood-based baseline HIV test is not immediately available at the pharmacy. Which plan is BEST supported by Massachusetts law and the DPH PEP guideline?",
    "choices": [
      {
        "text": "Delay any PEP prescription until a laboratory HIV-negative result is documented, even if testing would push treatment beyond 72 hours after exposure.",
        "why": "Incorrect. The September 2026 Massachusetts pharmacist PEP guidance states that a baseline HIV test is NOT required before initiating otherwise eligible PEP. A known positive or indeterminate test would require referral rather than PEP, but lack of an immediately available baseline test alone must not automatically delay time-sensitive initiation."
      },
      {
        "text": "Refuse pharmacist-prescribed PEP solely because the patient is under 18, even though the patient is sexually active and meets the other protocol conditions.",
        "why": "Incorrect. The DPH PEP guideline expressly permits eligible patients younger than 18 who are sexually active and have a reasonable concern about exposure; M.G.L. c.112 §12F permits qualifying minors to consent to HIV-prevention care without parental consent."
      },
      {
        "text": "Treat this as continuous HIV pre-exposure prophylaxis (PrEP), dispense a 90-day course with two refills, and defer follow-up until the second refill.",
        "why": "Incorrect. The patient presents following a recent potential exposure and needs the distinct PEP pathway. The September 2026 pharmacist PEP protocol calls for a 28-day course, authorizes no more than a 30-day supply with NO refills, and emphasizes prompt medical referral and follow-up testing."
      },
      {
        "text": "Complete the required PEP intake and consent, initiate an appropriate oral PEP regimen promptly within the 72-hour window without waiting solely for a baseline negative HIV test, prescribe no more than a 30-day supply with no refills, and arrange urgent follow-up evaluation and testing.",
        "why": "Correct. Under DPH's September 2026 statewide pharmacist PEP guidance, eligible sexually active minors may receive timely pharmacist-prescribed oral PEP when they satisfy exposure, weight, clinical, consent, and training conditions. A baseline HIV test is reviewed if available but is not a prerequisite to starting PEP. Treatment is taken for 28 days; authorized dispensing is at most 30 days with no refills, with referral and follow-up."
      }
    ],
    "correct": [
      "D"
    ],
    "citation": "M.G.L. c.94C §19F; M.G.L. c.112 §12F; DPH Statewide Guidance for Pharmacist Prescribing of HIV PEP (Sept. 2026), §§2, 4–6.4; DCP Circular 26-08-125",
    "url": "https://www.mass.gov/doc/pharmacist-pep-guidelines-9-2026/download",
    "verified": "2026-11-16",
    "note": "A sexually active minor may be eligible for pharmacist PEP in Massachusetts. Prompt 72-hour initiation matters; no baseline HIV test is required before starting if otherwise eligible. PEP is a 28-day regimen, with at most a 30-day supply and no refills."
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
    "citation": "21 CFR 1308.12(c), 1308.13(e), 1308.15(c); 105 CMR 700.002(B),(C),(E),(F); MA DPH MassPAT pharmacy reporting and data submission",
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
    "citation": "M.G.L. c.94C §22(c) (amended Nov. 5, 2025); 105 CMR 721.020(D)(7) (eff. Sept. 27, 2024); Massachusetts DPH Circular DCP 16-12-665; distinguish current 105 CMR 721.055(B) (remainder)",
    "url": "https://www.mass.gov/circular-letter/schedule-ii-opioids-prescription-form-requirements-and-patient-requests-for-partial-fill",
    "verified": "2026-11-16",
    "note": "A Schedule II opioid prescription needs its patient-request partial-fill notation even if the patient wants all tablets. The pharmacist can document it after prescriber/agent confirmation; do not rely on superseded 2016 'remainder void' guidance."
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
    "stem": "A Massachusetts-licensed pharmacist is arrested in another state for a misdemeanor. No charge is filed at first, and no conviction has occurred. Separately, a licensing board in another state later imposes formal professional discipline. Under 247 CMR 20.03, what Massachusetts reporting requirement applies?",
    "choices": [
      {
        "text": "Only a conviction must be reported; an arrest with no filed charge and a separate out-of-state license action are not reportable.",
        "why": "Incorrect. 247 CMR 20.03(3) expressly lists ANY arrest, pending criminal charge, or conviction by an individual licensee. Section 20.03(4) separately requires reporting of disciplinary actions, as defined by 247 CMR 2.00; neither provision is limited to a Massachusetts conviction."
      },
      {
        "text": "Both events must be reported by the individual to the Massachusetts Board within 14 calendar days of each respective event.",
        "why": "Correct. Section 20.03(3) requires a licensed individual to report an arrest within 14 calendar days even before a conviction or charge; §20.03(4) imposes a 14-calendar-day duty to report the other jurisdiction's disciplinary action. A pending appeal does not change the explicit reporting language."
      },
      {
        "text": "The pharmacist may defer both reports until the next license renewal so that every criminal or disciplinary matter can be resolved.",
        "why": "Incorrect. The regulation uses prompt 14-calendar-day reporting, not renewal-cycle disclosure. Late reporting would independently risk regulatory noncompliance."
      },
      {
        "text": "Only the pharmacist's employer must report an arrest or personal licensing action, and only within seven business days.",
        "why": "Incorrect. Sections 20.03(3)–(4) apply directly to licensed INDIVIDUALS; they do not shift that duty to the employer or use a seven-business-day period. Seven business days is separately used for certain serious pharmacy dispensing-event reports under §20.02."
      }
    ],
    "correct": [
      "B"
    ],
    "citation": "247 CMR 20.03(3)–(4) (effective Dec. 6, 2024), 247 CMR 2.00 disciplinary-action definition; distinguish 247 CMR 20.02 serious-event reporting",
    "url": "https://www.mass.gov/doc/247-cmr-20-reporting/download",
    "verified": "2026-11-16",
    "note": "Massachusetts-licensed pharmacists report any arrest, pending charge, conviction and licensing-board disciplinary action within 14 CALENDAR days; separate from seven-BUSINESS-day pharmacy serious-event reporting."
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
  }
];

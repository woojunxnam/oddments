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
  }
];

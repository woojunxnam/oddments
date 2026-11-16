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
  }
];

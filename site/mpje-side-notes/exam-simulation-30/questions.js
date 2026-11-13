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
  }
];

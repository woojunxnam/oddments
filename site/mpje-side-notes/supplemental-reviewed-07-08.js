/* Manually authored MPJE scenarios, chapters 7–8; official sources checked 2026-11-10. */
Object.assign(window.MPJE_SUPPLEMENTAL_VERIFIED || (window.MPJE_SUPPLEMENTAL_VERIFIED = {}), {
  "cii-partial-outstate": [
    {
      "question": "A pharmacist can dispense only 12 of 30 prescribed Schedule II tablets because the pharmacy has insufficient inventory. At hour 80, the rest arrives. What is required?",
      "choices": [
        "Dispense the remaining 18 because the patient was promised them",
        "Dispense the remainder if the prescriber gives oral permission",
        "Do not dispense the remainder under the original shortage partial fill; notify the prescriber and obtain a new prescription",
        "Treat the remaining tablets as a Schedule III refill"
      ],
      "answer": "C",
      "explanations": [
        "A promise does not override the 72-hour shortage-partial limit.",
        "The regulation requires a new prescription once the 72 hours expire.",
        "Correct. 21 CFR 1306.13(a) ends the shortage-partial pathway after 72 hours and requires prescriber notification.",
        "The medication's schedule cannot be changed to authorize a refill."
      ],
      "citation": "21 CFR 1306.13(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
    },
    {
      "question": "A patient requests only 10 tablets of a valid 30-tablet Schedule II prescription, although the pharmacy has all 30 in stock. What rule determines the remaining quantity?",
      "choices": [
        "The shortage 72-hour rule always applies",
        "The patient-requested partial-fill pathway may apply, with the remainder ordinarily limited to 30 days after prescription issuance",
        "The pharmacy may supply the remainder at any time over the next year",
        "No partial dispensing is permitted if stock is sufficient"
      ],
      "answer": "B",
      "explanations": [
        "The shortage provision applies when the pharmacist cannot supply the full amount.",
        "Correct. Under 21 CFR 1306.13(b), patient-requested partial filling is distinct from inventory-shortage partial filling.",
        "Federal law does not authorize a year-long remainder window.",
        "A patient may request a lawful partial fill even when sufficient stock exists."
      ],
      "citation": "21 CFR 1306.13(b)(1)–(2)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
    },
    {
      "question": "A valid emergency oral Schedule II order was partially dispensed at the patient's request. When must the remaining portion be filled, if otherwise lawful?",
      "choices": [
        "Within 72 hours after the emergency prescription was issued",
        "Within 30 days after the first partial dispensing",
        "Within six months after the emergency call",
        "Within 72 business hours after the pharmacist receives stock"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Emergency oral CII partial remainders under 21 CFR 1306.13(b)(2) use 72 hours from issuance.",
        "The 30-day general patient-requested window excludes emergency oral prescriptions.",
        "Six months is not an emergency oral CII remainder period.",
        "The regulation specifies hours after issuance, not business hours after restocking."
      ],
      "citation": "21 CFR 1306.13(b)(2)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
    },
    {
      "question": "An adult patient's neighbor, who is not a caregiver named in a medical power of attorney, asks the pharmacy to partially fill the patient's Schedule II prescription on the patient's behalf. Which response is best?",
      "choices": [
        "Any neighbor may request partial filling if they know the patient's address",
        "A neighbor's request is sufficient if the pharmacist recognizes the neighbor",
        "Only the prescriber can request a partial fill",
        "Do not rely on the neighbor's request; obtain the patient's request or a request from a person specifically authorized under the rule"
      ],
      "answer": "D",
      "explanations": [
        "Knowing an address does not establish authority to request a partial fill.",
        "Familiarity does not replace the regulation's defined requester categories.",
        "The patient and certain representatives can also request partial fills.",
        "Correct. Federal law identifies the patient, a minor's parent/guardian, or an adult's caregiver named in a medical power of attorney, as well as the prescriber."
      ],
      "citation": "21 CFR 1306.13(b)(1)(iii)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
    },
    {
      "question": "A prescriber in California issues a nonnarcotic Schedule II methylphenidate prescription four days ago. The patient presents it at a Massachusetts pharmacy. What is the key out-of-state requirement?",
      "choices": [
        "California is not contiguous, so no Schedule II prescription can be filled",
        "The pharmacist must authenticate and verify the prescription and prescriber, and the statutory five-day period applies",
        "The prescription is valid for 30 days because all Massachusetts CII prescriptions use that period",
        "The pharmacy must dispense it without contacting the prescriber"
      ],
      "answer": "B",
      "explanations": [
        "The Massachusetts nonnarcotic CII pathway is not limited to neighboring states.",
        "Correct. M.G.L. c.94C §18(d) permits eligible out-of-state nonnarcotic CII prescriptions within five days, with verification.",
        "The special out-of-state period differs from ordinary in-state CII validity.",
        "The statute requires verification by telephone or other means."
      ],
      "citation": "M.G.L. c.94C §18(d)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
    },
    {
      "question": "A Florida physician writes an oxycodone prescription for a patient who wants to pick it up at a Massachusetts pharmacy. The prescription was issued yesterday. What is the primary statutory obstacle?",
      "choices": [
        "Oxycodone is not a federally controlled medication",
        "A Massachusetts pharmacy may fill all out-of-state narcotic CII prescriptions within 30 days",
        "Ordinary in-state filling of out-of-state narcotic CII prescriptions is limited to prescribers in Maine and states contiguous with Massachusetts",
        "Florida prescriptions are never valid for any Schedule VI medication"
      ],
      "answer": "C",
      "explanations": [
        "Oxycodone is a narcotic Schedule II controlled substance.",
        "The ordinary out-of-state narcotic CII pathway is narrower than the nonnarcotic pathway.",
        "Correct. Section 18(d½) limits this ordinary pickup pathway to Maine and contiguous-state practitioners; separate shipment exceptions have additional conditions.",
        "The question concerns narcotic CII, not the separate Schedule VI rules."
      ],
      "citation": "M.G.L. c.94C §18(d½)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
    },
    {
      "question": "A Massachusetts pharmacist receives a qualifying Vermont Schedule II opioid prescription issued six days ago. The patient says that the standard Massachusetts CII validity is 30 days. What is correct?",
      "choices": [
        "The special out-of-state CII five-day issuance limit applies, so the prescription cannot be filled through that pathway",
        "The 30-day in-state rule overrides the out-of-state five-day rule",
        "The patient may extend the prescription by signing a waiver",
        "Any out-of-state CII prescription may be refilled once"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Section 18(d½) requires the qualifying out-of-state narcotic CII prescription to have been issued within the preceding five days.",
        "The general in-state validity rule does not replace the special out-of-state requirement.",
        "Patient consent cannot extend statutory prescription validity.",
        "Schedule II prescriptions cannot be refilled."
      ],
      "citation": "M.G.L. c.94C §18(d½)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
    },
    {
      "question": "A pharmacist dispenses a verified, qualifying out-of-state nonnarcotic Schedule II prescription under Massachusetts §18(d). What additional state reporting requirement applies?",
      "choices": [
        "Report the patient's name and address in a public database within 24 hours",
        "Mail the original prescription to the prescriber the same day",
        "No separate reporting exists beyond ordinary pharmacy records",
        "Deliver a copy to the department within 30 days, omitting the patient's name and address"
      ],
      "answer": "D",
      "explanations": [
        "The statute expressly excludes patient name and address from the copy.",
        "The specified statutory recipient is the department, not the prescriber.",
        "Section 18(d) imposes a separate copy-submission requirement.",
        "Correct. The statute specifies a 30-day deadline and removal of patient-identifying information."
      ],
      "citation": "M.G.L. c.94C §18(d)",
      "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
    },
    {
      "question": "A patient in a long-term care facility has a qualifying Schedule II prescription partially dispensed. What documentation is required under the federal LTCF partial-fill provision?",
      "choices": [
        "No record of each partial dispensing is needed",
        "Record the LTCF designation and each partial fill's date, quantity, remaining amount and dispensing pharmacist",
        "Only the total quantity prescribed is recorded at the first dispensing",
        "The pharmacy may omit the LTCF notation if the prescriber verbally agrees"
      ],
      "answer": "B",
      "explanations": [
        "The regulation requires records for each partial dispensing.",
        "Correct. 21 CFR 1306.13(c) requires the designation and specific dispensing records.",
        "The record must track each individual partial fill.",
        "The LTCF or terminal-illness notation is an express federal condition."
      ],
      "citation": "21 CFR 1306.13(c)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
    },
    {
      "question": "A Schedule II electronic prescription has already been partially dispensed at Pharmacy A. The patient requests that Pharmacy A transfer its remaining balance electronically to Pharmacy B under the federal initial-transfer rule. What is correct?",
      "choices": [
        "Any remaining balance can always be transferred once",
        "The patient can convert the balance into a new electronic prescription",
        "The federal initial-transfer provision is for prescriptions before initial dispensing; it does not authorize transferring a previously partially dispensed CII balance",
        "The receiving pharmacy may treat the remainder as a Schedule VI prescription"
      ],
      "answer": "C",
      "explanations": [
        "The initial-transfer rule is not a general transfer of CII partial remainders.",
        "The patient cannot create a new prescriber-issued prescription.",
        "Correct. 21 CFR 1306.08(e) concerns transfer for initial dispensing; the original has already been partially dispensed.",
        "Transfer does not change controlled-substance classification."
      ],
      "citation": "21 CFR 1306.08(e)–(f)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
    }
  ],
  "refills-transfer": [
    {
      "question": "A Schedule IV diazepam prescription was issued January 1 and first dispensed February 1. The patient requests another refill August 2. What date controls the federal six-month refill window?",
      "choices": [
        "February 1, the date of first dispensing",
        "The date of the most recent refill",
        "The date the patient first paid a copayment",
        "January 1, the date the prescription was issued"
      ],
      "answer": "D",
      "explanations": [
        "First dispensing does not restart the statutory window.",
        "Refills do not restart the original issue-date clock.",
        "Payment is unrelated to controlled-prescription validity.",
        "Correct. 21 CFR 1306.22(a) measures six months from issuance."
      ],
      "citation": "21 CFR 1306.22(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22"
    },
    {
      "question": "A Schedule III prescription has already been refilled five times. The prescriber originally wrote 'PRN refills.' Which action is correct?",
      "choices": [
        "Do not authorize a sixth refill under the original prescription; obtain a new valid prescription",
        "Dispense a sixth refill because 'PRN' means unlimited",
        "Refill once if the patient has taken the medication for at least six months",
        "Convert the prescription into Schedule VI to permit more refills"
      ],
      "answer": "A",
      "explanations": [
        "Correct. Schedule III–IV prescriptions cannot be refilled more than five times under 21 CFR 1306.22(a).",
        "An open-ended notation does not override federal limits.",
        "Duration of treatment does not waive the refill-count ceiling.",
        "The pharmacist cannot change the drug's legal schedule."
      ],
      "citation": "21 CFR 1306.22(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22"
    },
    {
      "question": "A patient asks to transfer the remaining authorized refills of a Schedule IV prescription between two unrelated pharmacies that do not share a real-time online database. The prescription was already transferred once for refills. What is the federal rule?",
      "choices": [
        "The prescription can be transferred repeatedly without limit",
        "The one-time refill-transfer allowance has already been used; obtain a new prescription or determine another lawful route",
        "A second transfer is permitted whenever the patient moves",
        "A second transfer is mandatory if the first pharmacy has no inventory"
      ],
      "answer": "B",
      "explanations": [
        "The ordinary rule permits only one refill transfer between unrelated pharmacies.",
        "Correct. 21 CFR 1306.25(a) provides a one-time rule, with a real-time shared-database exception.",
        "Patient relocation does not itself override the transfer limit.",
        "Inventory shortages do not create an unlimited transfer right."
      ],
      "citation": "21 CFR 1306.25(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.25"
    },
    {
      "question": "Two chain pharmacies electronically share a real-time, online database. A Schedule III prescription has valid remaining refills. What does federal law allow regarding refill transfers?",
      "choices": [
        "Only one transfer is ever allowed even within a real-time shared database",
        "The shared database allows unlimited refills beyond the prescriber's authorization",
        "Transfers may occur up to the maximum refills allowed by law and the prescriber's authorization",
        "The pharmacist may transfer Schedule II refills under the same rule"
      ],
      "answer": "C",
      "explanations": [
        "The real-time database exception permits additional transfers within the legal limits.",
        "The exception does not create new authorized refills.",
        "Correct. 21 CFR 1306.25(a) expressly provides this exception.",
        "Schedule II prescriptions do not have refills."
      ],
      "citation": "21 CFR 1306.25(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.25"
    },
    {
      "question": "A patient requests transfer of an original, never-dispensed Schedule II electronic prescription from Retail Pharmacy A to Retail Pharmacy B. Which transfer method is required under the federal rule?",
      "choices": [
        "Transfer the prescription in its electronic form directly between the retail pharmacies, if state law permits",
        "Print and fax it to the receiving pharmacy as the original electronic prescription",
        "Read the electronic prescription over the telephone as a routine Schedule II refill transfer",
        "Give the patient a screenshot to serve as the original"
      ],
      "answer": "A",
      "explanations": [
        "Correct. 21 CFR 1306.08(f)(1) requires an electronic-to-electronic transfer, with other conditions.",
        "Converting the EPCS into a fax does not satisfy the electronic transfer rule.",
        "An ordinary oral transfer is not the authorized initial EPCS transfer method.",
        "A screenshot is not the original controlled electronic prescription."
      ],
      "citation": "21 CFR 1306.08(e)–(f)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
    },
    {
      "question": "A never-dispensed Schedule III EPCS is lawfully transferred to another retail pharmacy for its first fill. It includes two authorized refills. What happens to those refills under the federal initial-transfer rule?",
      "choices": [
        "They are automatically canceled by the transfer",
        "They remain at the original pharmacy for later dispensing",
        "They must be separately transferred through a second oral call",
        "They transfer with the initial electronic prescription to the receiving pharmacy"
      ],
      "answer": "D",
      "explanations": [
        "The federal rule explicitly addresses accompanying authorized refills.",
        "The original pharmacy no longer retains separate refill authority for that transferred original.",
        "A separate oral call is not required to convey the authorized refills under this rule.",
        "Correct. 21 CFR 1306.08(e) transfers authorized Schedule III–V refills with the initial EPCS."
      ],
      "citation": "21 CFR 1306.08(e)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
    },
    {
      "question": "A pharmacist receives a Schedule VI maintenance-medication refill request after all authorized refills have been used. The prescriber cannot be reached. The pharmacist finds a 30-day Board policy and a 14-day regulation. What is the safest study conclusion?",
      "choices": [
        "All Schedule VI prescriptions can automatically be extended for 30 days",
        "The regulation and policy describe overlapping but potentially conflicting limits; do not assume a blanket 30-day authority without clarification",
        "The Board policy automatically repeals 247 CMR 9.04(12)",
        "The pharmacist must treat every Schedule VI medication as Schedule II"
      ],
      "answer": "B",
      "explanations": [
        "The two official documents do not support an unconditional extension for every Schedule VI drug.",
        "Correct. The published regulation says up to 14 days; Board Policy 2023-04 describes a narrower up-to-30-day path. The overlap requires care.",
        "A policy does not silently amend the text of a regulation.",
        "A continuity rule does not change a medication's schedule."
      ],
      "citation": "247 CMR 9.04(12); Board Policy 2023-04",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
    },
    {
      "question": "A pharmacist uses the published 247 CMR 9.04(12) continuity pathway because a Schedule VI prescription has expired and a timely new prescription cannot be obtained. What maximum does the regulation itself state?",
      "choices": [
        "Three days",
        "Seven days",
        "Up to a 14-day supply",
        "Unlimited until the prescriber responds"
      ],
      "answer": "C",
      "explanations": [
        "The cited regulatory text states a different maximum.",
        "The regulation does not specify seven days as the ceiling.",
        "Correct. 247 CMR 9.04(12) states a 14-day maximum, distinct from the separate Board policy wording.",
        "The regulation does not authorize unlimited dispensing."
      ],
      "citation": "247 CMR 9.04(12)",
      "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
    },
    {
      "question": "A pharmacy has an original Schedule IV prescription issued two months ago, and the patient asks the pharmacy to transfer it for its first dispensing. Which federal pathway is specific to a qualifying never-dispensed electronic prescription?",
      "choices": [
        "21 CFR 1306.08(e)–(f), permitting a one-time electronic initial transfer",
        "21 CFR 1306.13(a), which covers CII inventory-shortage partial fills",
        "21 CFR 1306.25 alone, which governs transfer of remaining refills after initial dispensing",
        "The federal emergency oral Schedule II rule"
      ],
      "answer": "A",
      "explanations": [
        "Correct. The initial electronic transfer pathway is separate from the ordinary refill-transfer rule.",
        "That provision concerns partial filling, not electronic transfer.",
        "Section 1306.25 addresses refill transfers; the question is an original unfilled EPCS.",
        "The emergency oral CII rule does not govern this Schedule IV transfer."
      ],
      "citation": "21 CFR 1306.08(e)–(f)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
    },
    {
      "question": "A pharmacist transfers an authorized Schedule IV refill to another pharmacy. Which statement about the original prescription's age is correct?",
      "choices": [
        "The transfer date becomes the new issue date",
        "The receiving pharmacy receives a new six-month period",
        "The prescriber's original date no longer matters after transfer",
        "The original issue date remains controlling for the federal six-month refill limit"
      ],
      "answer": "D",
      "explanations": [
        "Transfer does not reset the federal clock.",
        "A transferred refill is not a new prescriber-issued prescription.",
        "The original issuance date remains legally relevant.",
        "Correct. 21 CFR 1306.22(a) measures the six months from original issuance, regardless of later transfers."
      ],
      "citation": "21 CFR 1306.22(a)",
      "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22"
    }
  ]
});

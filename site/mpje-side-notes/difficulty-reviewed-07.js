/* Hand-authored difficulty expansion: Chapter 07. Federal and MA sources checked 2026-11-11; independent audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "cii-partial-outstate": {
    "moderate": [
      {
        "question": "A pharmacist dispenses 12 of 30 prescribed oxycodone tablets because only 12 are in stock. The other 18 arrive 80 hours later. What action follows the federal shortage-partial rule?",
        "choices": [
          "Dispense the remaining 18 because 30 days have not elapsed",
          "Treat the remainder as a normal CII refill",
          "Do not supply the remainder on that prescription after the 72-hour period; notify the prescriber and obtain a new prescription if more medication is needed",
          "Dispense the remainder if the patient signs a request"
        ],
        "answer": "C",
        "explanations": [
          "The stock-shortage partial-fill pathway generally has a 72-hour remainder window, not 30 days.",
          "Partial fills and refills are legally distinct.",
          "Correct. For a shortage partial, federal §1306.13(a) sets 72 hours from the first dispensing and prescriber notification if the balance is not completed.",
          "A new patient request cannot retroactively extend the lapsed stock-shortage partial-fill window."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A patient asks a Massachusetts pharmacist to dispense only 10 of 30 oxycodone tablets, although the pharmacy has enough to fill all 30. Which description is correct?",
        "choices": [
          "This may be a patient-requested partial fill rather than a refill, with documented requests, quantity limits, and remainder deadlines",
          "All partial filling of CII is allowed only when the pharmacy runs out of stock",
          "The prescription becomes a Schedule III order when fewer tablets are taken",
          "The remainder can automatically be transferred to any pharmacy"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Patient-requested CII partial fills have a separate federal framework, provided Massachusetts conditions are satisfied.",
          "Stock shortage is only one partial-fill pathway.",
          "Quantity does not change the drug's schedule.",
          "Massachusetts imposes same-pharmacy requirements on eligible patient-requested remaining portions."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "An adult patient's neighbor asks to request a patient-initiated Schedule II partial fill by phone. The neighbor is not named in the adult's medical power of attorney. Who may make the qualifying request under the federal rule?",
        "choices": [
          "Any adult who can provide the patient's date of birth",
          "Only the prescribing practitioner, never the patient",
          "Any household member who promises to pick up the medication",
          "The patient or an eligible representative, such as a caregiver named in the adult patient's medical power of attorney"
        ],
        "answer": "D",
        "explanations": [
          "Knowing demographic information does not establish the specified caregiver authority.",
          "Federal rules allow the patient to request the partial fill personally.",
          "Household membership alone is not the specified legal authorization.",
          "Correct. §1306.13(b) restricts eligible adult-caregiver requests to the specified representative."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A parent phones an MA pharmacy to request a partial fill for their 15-year-old child's valid Schedule II prescription. The pharmacist has verified parental authority. Is a telephone request by that parent permitted federally?",
        "choices": [
          "Never; all patient-requested partial fills must be written and notarized",
          "Yes, a parent or legal guardian of a minor may make a qualifying partial-fill request by phone to the pharmacist",
          "Only an adult caregiver named in the minor's medical power of attorney can request it",
          "Only pharmacy technicians can accept such requests"
        ],
        "answer": "B",
        "explanations": [
          "Federal §1306.13(b)(4) expressly permits an eligible request by phone.",
          "Correct. A parent or legal guardian of a minor can make the request, subject to all other requirements.",
          "Medical-power-of-attorney caregiver language relates to adults.",
          "The rule specifies a call to the pharmacist."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A valid emergency oral Schedule II prescription is partially dispensed at the patient's request. The patient asks to receive the balance five days after the prescription was issued. What rule applies?",
        "choices": [
          "The remainder may always be filled for six months",
          "Any CII emergency oral remainder is due within 30 business days",
          "The patient-requested emergency-oral remainder must be filled within 72 hours after the prescription is issued",
          "The remainder automatically converts to a Schedule IV refill"
        ],
        "answer": "C",
        "explanations": [
          "Schedule II refills are not authorized, and an emergency-oral remainder has a short clock.",
          "The federal emergency-oral partial-fill deadline is 72 hours, not 30 business days.",
          "Correct. Federal §1306.13(b)(2) creates the 72-hour-from-issuance exception to the usual 30-day remainder limit.",
          "Controlled classification does not change through partial dispensing."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A California physician issues a properly signed prescription for methylphenidate (a nonnarcotic Schedule II drug) four days before the patient presents it at an MA pharmacy. What should the pharmacist know?",
        "choices": [
          "It is automatically invalid because all out-of-state Schedule II prescriptions are forbidden",
          "It is valid without confirming the out-of-state prescriber's authority",
          "It must be treated as an ordinary six-month Schedule IV refill",
          "It may qualify for Massachusetts' out-of-state nonnarcotic CII pathway if the required practitioner verification, first-fill deadline, and other conditions are met"
        ],
        "answer": "D",
        "explanations": [
          "Massachusetts has a statutory pathway for qualifying out-of-state nonnarcotic CII prescriptions.",
          "Practitioner credentials and prescription authenticity must be verified.",
          "Methylphenidate remains a Schedule II controlled drug.",
          "Correct. M.G.L. c.94C §18(d) has conditions including initial dispensing within five days."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A Florida practitioner issues an otherwise genuine oxycodone prescription three days ago. The patient wants to pick it up in person at a Massachusetts retail pharmacy. Which Massachusetts out-of-state rule is most relevant?",
        "choices": [
          "Ordinary in-state pickup of out-of-state narcotic CII is restricted to specified neighboring-state prescribers, so this Florida order does not qualify through that pathway",
          "Any U.S. Schedule II opioid prescription qualifies for ordinary Massachusetts walk-in pickup within 30 days",
          "A prescription is valid if it is signed by a pharmacist in Florida",
          "All out-of-state CII drugs are nonnarcotic if prescribed for pain"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Massachusetts §18(d½) limits the walk-in narcotic CII pathway to Maine or a state contiguous to Massachusetts, subject to additional conditions.",
          "The five-day limit alone is not enough; geography and drug type matter.",
          "Prescriber authority, not pharmacist signature, is required.",
          "Oxycodone is a narcotic Schedule II substance."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A properly authorized Vermont prescriber wrote an otherwise valid Schedule II oxycodone prescription four days ago. At the Massachusetts pharmacy, the prescriber can be verified. Which statement is most accurate?",
        "choices": [
          "Vermont narcotic CII prescriptions are excluded under all circumstances",
          "The prescription may qualify for MA dispensing because Vermont is a neighboring state, provided the five-day initial-fill and verification conditions are satisfied",
          "The pharmacist may refill the prescription five times",
          "The pharmacy can ignore the statutory out-of-state reporting rule"
        ],
        "answer": "B",
        "explanations": [
          "Vermont is within the states covered by the relevant MA statutory pathway.",
          "Correct. The neighboring-state narcotic CII pathway is conditional, not automatic.",
          "CII prescriptions cannot be refilled.",
          "Eligible out-of-state CII dispensings have a separate reporting duty."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A qualifying out-of-state nonnarcotic Schedule II prescription is filled at an MA pharmacy under c.94C §18(d). What additional action does Massachusetts require?",
        "choices": [
          "Send the patient’s full name and address to every surrounding pharmacy",
          "File an original copy with the out-of-state medical board within one year",
          "Keep no record because the prescription is controlled by another state",
          "Provide the required prescription copy or report to the Massachusetts department within 30 days, excluding the patient's name and address as specified"
        ],
        "answer": "D",
        "explanations": [
          "The special report excludes the identifying patient name and address.",
          "The reporting duty is to the MA department, not the outside board.",
          "Controlled prescriptions remain subject to records and reporting.",
          "Correct. §18(d) sets the 30-day reporting rule with specified exclusions."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A terminally ill patient's Schedule II prescription is being partially filled under the special federal pathway. Which notation must the pharmacist document?",
        "choices": [
          "Only 'remaining refills: five'",
          "Only the pharmacy's latest weekly inventory count",
          "That the patient is 'terminally ill' (or 'LTCF patient,' when applicable) along with each partial-fill record",
          "That the patient will be traveling out of state"
        ],
        "answer": "C",
        "explanations": [
          "These partial dispensings are not ordinary refills.",
          "Inventory counts do not replace patient-category and dispensing records.",
          "Correct. Federal §1306.13(c) requires the relevant LTCF or terminal-illness notation and itemized partial-fill records.",
          "Travel plans do not substitute for the required federal notation."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      }
    ],
    "hard": [
      {
        "question": "A patient personally requests 10 of 30 oxycodone tablets from a valid MA prescription. Pharmacy A dispenses 10. On the next day, the patient asks Pharmacy B to dispense the remaining 20 using the same original prescription. What is the best legal conclusion?",
        "choices": [
          "Pharmacy B may always give the balance if A confirms by phone",
          "Under Massachusetts' patient-requested partial-fill rule, the remainder must be dispensed by the same pharmacy that made the initial partial fill",
          "Federal EPCS initial-transfer rules permit unrestricted transfer after part of a CII has already been dispensed",
          "Pharmacy B must label the remaining 20 as a refill"
        ],
        "answer": "B",
        "explanations": [
          "Confirmation alone does not waive the MA same-pharmacy condition.",
          "Correct. M.G.L. c.94C §18(d¾) governs remaining patient-requested CII portions.",
          "Federal initial-dispensing EPCS transfers are for never-dispensed prescriptions and do not erase the MA partial-fill condition.",
          "A remaining portion is not a refill, but may have to be dispensed by the same pharmacy."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "An otherwise qualifying California prescription for methylphenidate was issued six days ago and has never been filled. The pharmacist verifies all practitioner credentials. Which statement is correct?",
        "choices": [
          "It is timely because Massachusetts allows all Schedule II first fills within 30 days",
          "Verification alone eliminates the special out-of-state first-fill window",
          "It can be dispensed once if the patient accepts a 7-day supply",
          "It misses Massachusetts' five-day initial-fill requirement for this out-of-state nonnarcotic Schedule II pathway"
        ],
        "answer": "D",
        "explanations": [
          "The MA ordinary CII issue-date window does not displace the five-day out-of-state limit.",
          "Both verification and timing conditions apply.",
          "A smaller quantity cannot reset an expired initial-fill clock.",
          "Correct. §18(d) requires initial dispensing within five days of issuance."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "An MA pharmacy initially dispenses 10 of 30 oxycodone tablets from a qualifying Maine prescriber's out-of-state narcotic CII prescription within its five-day initial-fill window. The patient returns to the same pharmacy 12 days after issuance for the remaining 20. Which distinction matters most?",
        "choices": [
          "The five-day rule governs the initial fill, while any remainder must independently satisfy the applicable 30-day partial-fill clock, original-pharmacy rule, and other conditions",
          "Any out-of-state narcotic CII remainder must be dispensed within five minutes",
          "Initial dispensing five days after issue always makes the prescription refillable for six months",
          "Once the first partial was lawful, remaining tablets may be dispensed without documentation"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Massachusetts distinguishes the out-of-state initial dispensing window from an otherwise permitted same-pharmacy remainder.",
          "Five minutes is not a legal dispensing deadline.",
          "Schedule II cannot be refilled.",
          "Each partial must be recorded and the aggregate cannot exceed the prescribed total."
        ],
        "citation": "105 CMR 721.055(A)–(C)",
        "sourceUrl": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
      },
      {
        "question": "A pharmacist dispenses 25 of 40 morphine tablets because of insufficient stock, then obtains more inventory 75 hours after the first partial. The patient asks the pharmacist to treat the late 15 as a new patient-requested partial fill. What is correct?",
        "choices": [
          "The pharmacist may reclassify the first shortage fill without documenting anything",
          "The remaining 15 are authorized as a refill because the supply is for pain",
          "The shortage pathway's 72-hour remainder period has ended; a new prescription is required before providing additional tablets",
          "The original prescription becomes valid again if a different pharmacist signs it"
        ],
        "answer": "C",
        "explanations": [
          "The original shortage was already partially dispensed under the shortage rule; retrospective relabeling does not extend that clock.",
          "Schedule II refills are prohibited.",
          "Correct. Federal §1306.13(a) prohibits supplying the remaining quantity beyond the shortage partial's 72-hour period on the same prescription.",
          "Changing a pharmacist does not reset a statutory clock."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A pharmacy sees federal 21 CFR §1306.13(c) permit up to 60 days from issue for terminally ill patients' Schedule II partial fills. The patient is in Massachusetts and the state prescription law may impose a tighter limit. What should the pharmacist do?",
        "choices": [
          "Assume federal 60 days overrides every state restriction",
          "Apply federal 60 days and simply ignore state requirements",
          "Treat every LTCF partial dispensing as an automatically authorized refill",
          "Evaluate both federal and Massachusetts validity and partial-fill requirements; the federal 60-day ceiling is not permission to disregard a more restrictive state rule"
        ],
        "answer": "D",
        "explanations": [
          "Federal allowance does not preempt stricter state dispensing restrictions in this context.",
          "Both sets of dispensing requirements must be met.",
          "CII partial filling is distinct from a refill.",
          "Correct. Federal §1306.13(c) defines a federal maximum, not a blanket exemption from MA law."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A patient has an otherwise genuine Florida oxycodone prescription and asks a Massachusetts pharmacy to mail it to the patient's Florida address under a qualifying nonresident mail-order arrangement. The clerk assumes Florida prescriptions are always prohibited. What is the correct response?",
        "choices": [
          "All out-of-state narcotic CII prescriptions are forbidden in MA even for qualified out-of-state mail order",
          "Massachusetts' separate nonresident mail-delivery exception may apply only if its detailed statutory criteria are met; this is not ordinary walk-in dispensing",
          "The pharmacy may send it without checking credentials because it will be shipped",
          "Converting the order to Schedule III is the only legal way to ship it"
        ],
        "answer": "B",
        "explanations": [
          "Massachusetts has a separately conditioned out-of-state narcotic CII mail-delivery pathway.",
          "Correct. M.G.L. c.94C §18(d½) includes a distinct conditional mail-delivery provision.",
          "Practitioner and pharmacy compliance remain necessary.",
          "The schedule is based on the drug and not shipping method."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A valid Schedule II EPCS remains completely unfilled at Pharmacy A. The patient requests an electronic transfer to Pharmacy B for initial dispensing, and state law permits the transfer. What must be true under federal law?",
        "choices": [
          "One-time initial transfer must remain electronic and be communicated directly between licensed pharmacists, with required records",
          "Pharmacy A can fax a picture instead of transmitting the controlled ePrescription",
          "Pharmacy A can perform unlimited initial transfers",
          "The prescription can be transferred only after Pharmacy A dispenses part of the drug"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Federal 21 CFR §1306.08(e)–(g) allows qualifying one-time unfilled EPCS transfer between retail pharmacies.",
          "Electronic original must remain electronic without conversion to fax.",
          "Initial transfers are limited to one time.",
          "Initial dispensing is, by definition, before it has been filled."
        ],
        "citation": "21 CFR §1306.08(e)–(h)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"
      },
      {
        "question": "An out-of-state physician's otherwise valid Schedule IV diazepam prescription is first presented to an MA pharmacy 21 days after issue. The pharmacy verifies the prescriber's authority and all other conditions. Which age-based rule applies?",
        "choices": [
          "All out-of-state prescriptions have a five-day first-fill window",
          "The Massachusetts five-day out-of-state Schedule II rule automatically extends to Schedule IV",
          "Massachusetts' out-of-state Schedule III–VI route generally requires presentation within 30 days, with separate controlled-drug requirements",
          "Any out-of-state Schedule IV prescription must be rejected, even within 30 days"
        ],
        "answer": "C",
        "explanations": [
          "The five-day MA out-of-state rule is for qualifying Schedule II prescriptions.",
          "The controlled schedule changes which rule applies.",
          "Correct. M.G.L. c.94C §18(c) includes out-of-state Schedule III–VI within a 30-day period.",
          "Massachusetts provides a conditioned pathway for out-of-state III–VI prescriptions."
        ],
        "citation": "M.G.L. c.94C §18(c)–(d¾)",
        "sourceUrl": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
      },
      {
        "question": "A pharmacist dispenses a first 10-tablet portion from a qualifying Massachusetts patient-requested Schedule II prescription, issued August 1. The patient asks for the remaining 20 on September 2. The pharmacy has the balance in stock. What is correct?",
        "choices": [
          "The patient may automatically obtain the balance within six months",
          "The original 30-day remainder deadline has passed, so the balance cannot be supplied on this prescription",
          "The remaining 20 is an ordinary authorized CII refill",
          "The pharmacy may reset the issue date to September 2"
        ],
        "answer": "B",
        "explanations": [
          "The partial-fill remainder deadline is not six months.",
          "Correct. Federal §1306.13(b) and MA patient-requested partial-fill rules cap remaining quantities within 30 days after issue.",
          "Schedule II refills are prohibited.",
          "The legally issued date cannot simply be replaced."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      },
      {
        "question": "A prescriber explicitly limits each partial dispensing to a maximum of five oxycodone tablets in a valid Schedule II prescription. The patient's authorized caregiver asks the pharmacist to provide 15 tablets as the first partial. What does federal law require?",
        "choices": [
          "The caregiver request overrides the prescriber's maximum if a medical power of attorney exists",
          "The technician can raise the authorized quantity as a clerical correction",
          "The pharmacy can supply 15 because the total prescribed is still 30",
          "Patient or authorized representative cannot request a larger partial quantity than the prescribing practitioner specified"
        ],
        "answer": "D",
        "explanations": [
          "Proper representative status does not override a prescriber's stated partial-quantity limit.",
          "A technician cannot override the practitioner's order.",
          "An aggregate cap does not waive per-partial prescriber restrictions.",
          "Correct. Federal §1306.13(b)(4) prohibits eligible requestors from exceeding the partial quantity specified by the practitioner."
        ],
        "citation": "21 CFR §1306.13(a)–(c)",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"
      }
    ]
  }
});

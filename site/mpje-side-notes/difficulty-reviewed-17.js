/* Original Chapter 17 moderate/hard MA MPJE stock-ordering and inventory scenarios. Official-source author review: 2026-11-12. Independent legal audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "ordering-inventory": {
    "moderate": [
      {
        "question": "A Massachusetts pharmacy's regular wholesaler ships 3 of the 5 oxycodone packages ordered on a valid DEA Form 222. The rest arrive 55 days after the form was executed. Which handling is appropriate?",
        "choices": [
          "Reject all partial shipments because the entire order must ship simultaneously",
          "Record the packages received and their receipt dates on the purchaser's retained copy; a balance can be supplied within the 60-day window",
          "Reset the DEA Form 222 execution date to the first shipment's date",
          "Use a Schedule IV refill transfer to receive the unshipped packages"
        ],
        "answer": "B",
        "explanations": [
          "Federal law permits multiple shipments to complete an order within its deadline.",
          "Correct. §1305.13 permits partial shipments within 60 days of execution and requires receipt dates and quantities on the purchaser copy.",
          "The clock starts at execution, not receipt of the first shipment.",
          "Patient refill transfers cannot substitute for stock ordering documentation."
        ],
        "citation": "21 CFR §1305.13(b),(e): DEA Form 222 partial shipments and receipt records",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13"
      },
      {
        "question": "A Massachusetts pharmacy hires a new pharmacist and asks them to sign the pharmacy's paper Schedule II purchasing forms. The pharmacist has no current power of attorney. What should be done?",
        "choices": [
          "Have the appropriate registrant grant a compliant power of attorney before the pharmacist signs Form 222 orders on the registrant's behalf",
          "Use the pharmacist's personal NPI as authorization to sign immediately",
          "Let the pharmacist sign based only on the manager's verbal permission",
          "Assign the signature to an unlicensed clerk because the inventory belongs to the pharmacy"
        ],
        "answer": "A",
        "explanations": [
          "Correct. A registrant may authorize an individual to sign Schedule I/II orders through an executed POA under §1305.05.",
          "An NPI is not a DEA purchasing authorization.",
          "Verbal permission is not the required executed POA.",
          "An unlicensed clerk's signature without proper delegation does not cure the issue."
        ],
        "citation": "21 CFR §1305.05(a),(d)–(f): Power of attorney for Schedule I/II ordering",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.05"
      },
      {
        "question": "At opening, a new DEA-registered pharmacy has zero controlled substances in stock but expects a shipment tomorrow. What should the initial controlled-drug inventory show?",
        "choices": [
          "Nothing; inventories may begin after the first two-year interval",
          "A fabricated balance of the expected order",
          "An accurate inventory showing zero controlled substances on the day controlled-activity operations begin",
          "Only the pharmacy's intended drug order list"
        ],
        "answer": "C",
        "explanations": [
          "Initial inventory is required when the registrant first engages in covered controlled activity.",
          "Controlled drugs not yet on hand must not be counted as inventory.",
          "Correct. 21 CFR 1304.11(b) expressly requires documenting a zero initial inventory when none is on hand.",
          "A planned purchasing list is not an actual stock count."
        ],
        "citation": "21 CFR §1304.11(a)–(e): Initial, biennial, and newly controlled inventories",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
      },
      {
        "question": "A Massachusetts pharmacy last completed its DEA biennial Schedule II–V inventory 25 months ago. However, its Schedule II perpetual record is reconciled every ten days. What does the pharmacist still need to recognize?",
        "choices": [
          "The ten-day MA reconciliation automatically replaces the federal biennial inventory",
          "The pharmacy may wait another 23 months",
          "DEA inventories are required only for Schedule II drugs",
          "The required federal biennial inventory is overdue; MA ten-day CII reconciliation is a separate requirement"
        ],
        "answer": "D",
        "explanations": [
          "State perpetual-record reconciliation and federal general inventory have separate triggers.",
          "Federal §1304.11(c) requires inventory at least once every two years.",
          "Federal controlled-inventory duties extend beyond Schedule II.",
          "Correct. The pharmacy must satisfy both the two-year federal clock and MA Schedule II reconciliation."
        ],
        "citation": "21 CFR §1304.11(a)–(e): Initial, biennial, and newly controlled inventories",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
      },
      {
        "question": "A registered Massachusetts pharmacy holds a partly opened bottle of Schedule II hydromorphone tablets during its required DEA physical inventory. Which counting method applies?",
        "choices": [
          "Estimate the tablets from the bottle's label because the bottle is open",
          "Use the stock computer's calculated balance instead of counting",
          "Make an exact physical count of Schedule II tablets, regardless of bottle size",
          "Record one commercial container without noting its quantity"
        ],
        "answer": "C",
        "explanations": [
          "Estimate counting is not permitted for Schedule II inventory.",
          "Perpetual electronic records do not substitute for the required physical count.",
          "Correct. §1304.11 requires exact counts for Schedule II drugs.",
          "Container count without actual units is inadequate for an opened bottle."
        ],
        "citation": "21 CFR §1304.11(a)–(e): Initial, biennial, and newly controlled inventories",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
      },
      {
        "question": "A pharmacy's controlled-substance software has been automatically adjusting Schedule II quantities. During a required ten-day physical reconciliation, a discrepancy is discovered. Who may make an authorized discrepancy adjustment under Massachusetts 247 CMR 9.21?",
        "choices": [
          "Any unlicensed pharmacy clerk with login access",
          "The pharmacist manager of record; in their absence a pharmacist designee may act and report to the manager",
          "A trained technician alone, without pharmacist involvement",
          "The IT vendor, because the inventory is electronic"
        ],
        "answer": "B",
        "explanations": [
          "Unlicensed workers may not make perpetual inventory adjustments.",
          "Correct. §9.21(8)(d) reserves discrepancy adjustments to the pharmacist MOR, or pharmacist designee in the MOR's absence.",
          "A certified technician may make permitted entries, not independently authorize discrepancy adjustments.",
          "A vendor cannot override the regulation's pharmacist responsibilities."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A DEA-registered pharmacy distributes a modest stock quantity of Schedule III testosterone to another DEA-registered practitioner rather than dispensing it to a patient. Both maintain required records, and the transaction stays within the federal percentage exception. Which statement is correct?",
        "choices": [
          "This is practitioner-to-practitioner stock distribution rather than patient dispensing and may qualify for §1307.11 without a distributor registration",
          "Every stock transfer must be processed as a new prescription to a fictitious patient",
          "A DEA Form 222 must be used for all Schedule III orders",
          "The recipient can be unregistered if the supplier records the sale"
        ],
        "answer": "A",
        "explanations": [
          "Correct. §1307.11 provides a conditional dispenser-to-practitioner distribution exception, with registration and record requirements.",
          "Stock distribution is not patient-specific dispensing.",
          "DEA Form 222 governs Schedule I/II ordering, not ordinary Schedule III distribution.",
          "The receiving practitioner must be registered to dispense the substance."
        ],
        "citation": "21 CFR §1307.11(a)–(c): Dispenser distribution to another practitioner",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11"
      },
      {
        "question": "A Massachusetts pharmacy receives an electronic CSOS Schedule II order and asks whether it should print and treat the transaction as a paper DEA Form 222. Which answer is best?",
        "choices": [
          "CSOS ordering automatically replaces the pharmacy's electronic prescribing platform",
          "Each electronic CSOS order is an authorized refill of a Schedule II prescription",
          "CSOS permits Schedule III–VI orders only, not Schedule II stock",
          "An authorized CSOS order is an independent electronic Schedule I/II purchasing route with its own receipt record requirements; it is not an EPCS patient prescription"
        ],
        "answer": "D",
        "explanations": [
          "Stock ordering and prescribing are separate electronic processes.",
          "Schedule II prescriptions cannot be refilled.",
          "CSOS is specifically designed for qualifying Schedule I/II ordering.",
          "Correct. §1305.22 regulates electronic controlled-stock orders and receipt confirmation."
        ],
        "citation": "21 CFR §1305.22: Electronic Schedule I/II receipt recording",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.22"
      },
      {
        "question": "A Massachusetts pharmacy performs an accurate physical reconciliation of its Schedule II perpetual inventory every fourteen days. The pharmacist believes this is frequent enough because federal biennial inventory is maintained. What is correct?",
        "choices": [
          "Fourteen days complies with Massachusetts' ten-day physical reconciliation requirement",
          "The federal two-year inventory waives the state reconciliation requirement",
          "MA requires an accurate physical Schedule II reconciliation at least once every ten days, separately from the federal inventory",
          "Reconciliation is needed only if a theft has been confirmed"
        ],
        "answer": "C",
        "explanations": [
          "Fourteen days is longer than the MA maximum interval.",
          "Federal and state controlled-stock duties are separate.",
          "Correct. 247 CMR 9.21(8)(c) specifies reconciliation at least once in each ten-day period.",
          "The requirement is routine and not contingent on a confirmed theft."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A pharmacy completes an MA Schedule II reconciliation and has multiple expired, quarantined tablets awaiting reverse distribution. A technician proposes excluding those tablets from physical counts because they are not available for sale. What is the correct rule?",
        "choices": [
          "Expired CII doses are never subject to controlled-stock security",
          "Expired, quarantined and pending-reverse-distribution controlled substances remain subject to the relevant §9.21 inventory and security provisions",
          "Only salable units belong in the perpetual record",
          "Expired CII stock can be discarded without documentation because it will not be dispensed"
        ],
        "answer": "B",
        "explanations": [
          "Regulated controlled inventory includes stock awaiting destruction or return.",
          "Correct. 247 CMR 9.21(10) applies its requirements to expired, quarantined or pending reverse distribution controlled drugs.",
          "Sale status is not the relevant legal distinction.",
          "Disposal remains regulated and must be documented."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      }
    ],
    "hard": [
      {
        "question": "A registered pharmacy distributed 120 controlled-substance dosage units to other registered practitioners under §1307.11 in a calendar year and dispensed or distributed 4,000 controlled dosage units in total that year. If all other conditions were met, what conclusion follows?",
        "choices": [
          "120 of 4,000 units is under the federal five-percent ceiling, so the quantity does not by itself require distributor registration",
          "The five-percent rule compares 120 units with the 200 Schedule II tablets in a single bottle",
          "The five-percent rule permits no transfers of Schedule II even with Form 222",
          "All 120 units must be attributed to a patient's prescription instead of stock distribution"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 120 / 4,000 = 3%, which is below the §1307.11 annual five-percent dosage-unit threshold.",
          "The denominator is the calendar-year total controlled dosage units dispensed and distributed, not one package.",
          "Qualifying Schedule II distributions can occur with required order forms and records.",
          "Converting a stock transfer into a fictitious patient dispensing is inappropriate."
        ],
        "citation": "21 CFR §1307.11(a)–(c): Dispenser distribution to another practitioner",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11"
      },
      {
        "question": "A pharmacy places a Schedule II stock order on a valid Form 222 dated January 1. Half arrives by January 10; the remaining quantity is shipped March 10. The manager asks whether it can be recorded against the January form. Which rule controls?",
        "choices": [
          "Partial orders are valid for one year, measured from the first delivery",
          "The second delivery is allowed if the patient has a new prescription",
          "Every partial shipment extends the order's 60-day validity by another 60 days",
          "The unfilled balance cannot be supplied under the original ordinary Form 222 after its 60-day validity period; a new authorized order is needed"
        ],
        "answer": "D",
        "explanations": [
          "§1305.13's standard validity is not one year.",
          "Patient orders do not govern pharmacy stock purchasing.",
          "The first shipment does not restart the validity clock.",
          "Correct. The 60-day period begins with purchaser execution and ordinarily is not extended by partial shipments."
        ],
        "citation": "21 CFR §1305.13(b),(e): DEA Form 222 partial shipments and receipt records",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13"
      },
      {
        "question": "A new MA pharmacy has a valid DEA initial zero inventory, then receives Schedule II stock. It completes a federal inventory two years later but never establishes a perpetual inventory. What must be corrected?",
        "choices": [
          "The zero initial inventory authorizes dispensing without any later records",
          "MA requires an ongoing Schedule II perpetual inventory and reconciliation at least every ten days, independently of federal initial/biennial inventory",
          "Only Schedule V drugs need continuous state inventory",
          "Federal biennial inventory replaces every Massachusetts requirement"
        ],
        "answer": "B",
        "explanations": [
          "Initial zero stock does not waive later recordkeeping.",
          "Correct. MA §9.21(8) requires continuous transaction records and physical ten-day reconciliation for CII.",
          "The specific MA perpetual inventory applies to Schedule II.",
          "Separate federal and state record requirements both apply."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A pharmacy's perpetual inventory shows 120 methylphenidate tablets. A current count shows 113. A certified technician identifies a possible error and proposes correcting the database to 113 immediately without pharmacist review. What is correct?",
        "choices": [
          "The technician's certification gives unlimited authority to adjust discrepancy balances",
          "All discrepancies are automatically insignificant and may be discarded",
          "The MOR must investigate, and an adjustment resulting from a discrepancy is reserved to the pharmacist MOR or an authorized pharmacist designee in the MOR's absence",
          "Physical counts are invalid if they disagree with electronic balances"
        ],
        "answer": "C",
        "explanations": [
          "Certified technicians may make entries but do not independently adjust discrepancies.",
          "A loss may require investigation and separate reporting.",
          "Correct. 247 CMR 9.21(8)(c)–(f) specifies pharmacist investigation and adjustment authority.",
          "Discrepancies require review, not rejection of the count."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A pharmacist is given POA to sign DEA Forms 222, but the authorizing corporate officer and pharmacist both sign without the two witnesses required by federal regulation. The pharmacy places a Schedule II order. Which legal problem is present?",
        "choices": [
          "The POA does not meet §1305.05's execution requirements and should be properly executed before the pharmacist acts as attorney-in-fact",
          "POA never requires any witness when a pharmacy is incorporated",
          "A copy of the pharmacist's NPI cures the missing witnesses",
          "A pharmacy employee may sign CII orders without authorization whenever medication is urgently needed"
        ],
        "answer": "A",
        "explanations": [
          "Correct. §1305.05(d) requires authorizer, agent, and two witnesses; electronic signing may be used but does not eliminate required signatories.",
          "Corporate registrants have specific authorized officer signature rules and witnesses.",
          "An NPI is not a substitute for a lawful controlled-order POA.",
          "An urgent stock need does not erase ordering authorization."
        ],
        "citation": "21 CFR §1305.05(a),(d)–(f): Power of attorney for Schedule I/II ordering",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.05"
      },
      {
        "question": "A MA pharmacy closes temporarily and moves all its Schedule II stock to a wholesale distributor. The MOR claims the transaction is 'patient returns' and can skip Form 222 and the MA inventory adjustment process. What is correct?",
        "choices": [
          "Any movement of controlled stock is legally treated as a patient return",
          "Closing a location authorizes disposal into ordinary trash",
          "Stock transfer is always exempt from documentation when the pharmacy closes",
          "Document a lawful registrant-to-registrant stock transaction with applicable Schedule II order-form/CSOS requirements, MA closing/inventory rules and correct perpetual balances"
        ],
        "answer": "D",
        "explanations": [
          "Registrant stock transfer differs from patient-returned drugs.",
          "Controlled inventory disposal is regulated.",
          "A closure triggers, not eliminates, relevant transfer and inventory obligations.",
          "Correct. Federal Schedule II stock orders and MA facility stock accounting both remain relevant; the specific lawful closure pathway must be verified."
        ],
        "citation": "247 CMR 6.10: Change of manager of record and inventory",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download"
      },
      {
        "question": "A registered pharmacist sees CSOS orders for Schedule II supplies but the receiving clerk does not record the received quantity or receipt date in the pharmacy's electronic controlled-order records. The vendor says the digital signature alone proves receipt. What should be done?",
        "choices": [
          "Treat the digital signature as proof that every ordered package was actually received",
          "Record the actual packages or units received and receipt dates in the electronic order record as required by DEA receipt rules",
          "Skip receipt records because CSOS is not subject to inventory law",
          "Enter the amount ordered as received even if some cartons were missing"
        ],
        "answer": "B",
        "explanations": [
          "Placing an order is not the same as confirming delivery.",
          "Correct. 21 CFR 1305.22 requires the purchaser to enter relevant receipt data for electronic controlled-substance orders.",
          "Electronic orders are regulated controlled stock transactions.",
          "Accurate receipt quantities, not assumed order quantities, must be documented."
        ],
        "citation": "21 CFR §1305.22: Electronic Schedule I/II receipt recording",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.22"
      },
      {
        "question": "A pharmacy has a Schedule III controlled substance container holding 1,500 tablets during a federal inventory. The owner asks to estimate from weight because an estimate is common for opened Schedule III bottles. Which federal rule applies?",
        "choices": [
          "Every Schedule III bottle can be estimated regardless of size",
          "The estimate rule applies when the bottle holds more than 1,000 tablets",
          "For a Schedule III–V container holding more than 1,000 tablets or capsules, an exact count is required rather than a good-faith estimate",
          "Only Schedule II drugs must ever be included in federal inventory"
        ],
        "answer": "C",
        "explanations": [
          "§1304.11 sets an exception to estimation for large containers.",
          "The more-than-1,000 threshold requires greater precision, not less.",
          "Correct. Federal §1304.11(e)(6)(ii) requires exact count for CIII–V containers with more than 1,000 tablets/capsules.",
          "Federal inventories cover Schedules II–V as applicable."
        ],
        "citation": "21 CFR §1304.11(a)–(e): Initial, biennial, and newly controlled inventories",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"
      },
      {
        "question": "A pharmacy uses its Schedule II perpetual inventory for 10-day reconciliation. A manager argues expired oxycodone can be omitted while still on the premises because it has a red 'quarantine' tag; current physical count then appears to match. What is the compliance concern?",
        "choices": [
          "§9.21 specifically extends its stock-security and perpetual inventory rules to quarantined and expired controlled drugs, so the count must include applicable on-premises amounts and discrepancies investigated",
          "Quarantine removes the substance from DEA control until it is sold",
          "A red label makes any quantity legally irrelevant",
          "Only patient-ready stock is subject to Massachusetts inventory"
        ],
        "answer": "A",
        "explanations": [
          "Correct. §9.21(8) and (10) cover expired/quarantined controlled stock pending authorized transfer/disposal.",
          "Controlled classification persists while the medication is secured in quarantine.",
          "Label color does not change inventory obligations.",
          "Non-saleable controlled drug stock still requires inventory security and records."
        ],
        "citation": "247 CMR 9.21(7)–(11): Controlled stock delivery, perpetual inventory, reconciliation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A pharmacy was permitted to distribute Schedule II stock to a registered clinic under the §1307.11 five-percent exception, but the proposed 100-tablet distribution would now put the pharmacy over the annual dosage-unit threshold. The clinic promises to write prescriptions for those tablets afterward. What is correct?",
        "choices": [
          "Later patient prescriptions retroactively change the transaction into retail dispensing",
          "The five-percent ceiling applies only to Schedule VI products",
          "A registered receiving clinic can waive the distributor-registration threshold",
          "Before exceeding five percent, the pharmacy must obtain the appropriate distribution registration; writing patient prescriptions later does not cure the stock transaction"
        ],
        "answer": "D",
        "explanations": [
          "Stock distribution to another practitioner is a distinct transaction.",
          "The threshold applies to federally controlled substances distributed under the section.",
          "Receiving registrant authority does not waive distributing registrant restrictions.",
          "Correct. §1307.11(b) requires a distributor registration when the anticipated calendar-year transfers exceed the threshold."
        ],
        "citation": "21 CFR §1307.11(a)–(c): Dispenser distribution to another practitioner",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11"
      }
    ]
  }
});

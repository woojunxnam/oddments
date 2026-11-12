/* Massachusetts MPJE Chapter 20 shared services and automation: original 10 moderate/10 hard cases. Primary source author review 2026-11-12; independent audit pending. */
Object.assign(window.MPJE_DIFFICULTY_REVIEWED || (window.MPJE_DIFFICULTY_REVIEWED = {}), {
  "shared-automation": {
    "moderate": [
      {
        "question": "Two separately owned Massachusetts pharmacies want to share prescription entry and clinical review. Both are licensed, but they have no written agreement allocating responsibilities. What must they arrange before participating?",
        "choices": [
          "Obtain a written agreement stating the shared services and each participant's responsibilities, or have common ownership",
          "Operate without an agreement because different owners automatically qualify",
          "Have the retail patient sign a federal Schedule II refill authorization",
          "Treat the arrangement as ordinary medication wholesaling rather than shared pharmacy service"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Board Policy 2021-02 §III requires common ownership or a written contract allocating shared responsibilities.",
          "Licensure alone does not replace the ownership or contract requirement.",
          "Patient refill authorization cannot create a service contract between pharmacies.",
          "Processing another pharmacy's prescriptions is shared service, not necessarily wholesaling."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A retail pharmacy uses a central-fill partner under a compliant shared-services arrangement. A patient asks not to have future prescriptions filled by that partner. What policy protection applies?",
        "choices": [
          "The patient must use central fill because the pharmacy's technology contract is binding",
          "The pharmacy may conceal central fill to avoid confusing patients",
          "The patient must provide a letter from a prescriber to exercise choice",
          "The retail pharmacy must notify patients about shared processing or filling and provide an opt-out mechanism"
        ],
        "answer": "D",
        "explanations": [
          "Retail patient choice is specifically protected in the MA shared-services policy.",
          "Disclosure is required rather than prohibited.",
          "The policy does not condition the opt-out mechanism on prescriber authorization.",
          "Correct. Policy 2021-02 §III(k)–(l) requires notice and a mechanism for patients to opt out."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A Massachusetts-licensed pharmacy technician processes the data for an MA retail prescription from an authorized remote workstation. A pharmacist later conducts required clinical verification. Which distinction makes this potentially permissible?",
        "choices": [
          "Remote processing automatically allows the technician to dispense the final product",
          "Remote data processing may be permitted for a licensed technician under Board policy, while pharmacist verification and physical dispensing remain separate duties",
          "Remote processing transfers the technician's license to any state",
          "Any employee may electronically sign Schedule II prescriptions for physicians"
        ],
        "answer": "B",
        "explanations": [
          "Remote processing specifically excludes final product verification and dispensing.",
          "Correct. Policy 2021-02 §V addresses licensed technician remote processing subject to verification and other safeguards.",
          "A Massachusetts technician registration does not confer multi-state licensure.",
          "Remote pharmacy processing does not grant prescriber signing authority."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §§V–VI — Remote Processing and Telepharmacy",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A Massachusetts pharmacy proposes a pickup locker inside its pharmacy building. It will stock a Schedule II analgesic and a Schedule VI tablet. Which controlled-drug distinction governs the automated pharmacy system?",
        "choices": [
          "Both may be stocked because every schedule is allowed in an APS",
          "Only Schedule II and III may be stocked when the locker is indoors",
          "247 CMR 9.10 permits APS dispensing of Schedules IV–VI, not Schedule II analgesics",
          "Drug schedules do not matter if the locker has electronic locks"
        ],
        "answer": "C",
        "explanations": [
          "247 CMR 9.10 identifies specific permissible schedules.",
          "Schedule II and III are not included in the APS permission.",
          "Correct. The APS dispensing authority explicitly covers Schedules IV–VI.",
          "Electronic locks do not expand the authorized schedules."
        ],
        "citation": "247 CMR 9.10(1)–(2) — Automated Pharmacy Systems",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A pharmacy plans to place unreconstituted antibiotic suspension powder and refrigerated insulin inside its patient pickup APS. Both would be labeled for later dispensing. What does Massachusetts require?",
        "choices": [
          "Only the insulin is forbidden, while any product needing reconstitution is allowed",
          "The APS may hold both if an automatic camera is present",
          "Both are permitted because the products are commercially manufactured",
          "Neither product may be stocked in the APS when it requires refrigeration or reconstitution"
        ],
        "answer": "D",
        "explanations": [
          "Both refrigeration and reconstitution are exclusion criteria.",
          "Video monitoring cannot waive product limitations.",
          "Commercial manufacture does not remove the APS restrictions.",
          "Correct. 247 CMR 9.10(1)(d) forbids medications requiring refrigeration or reconstitution in an APS."
        ],
        "citation": "247 CMR 9.10(1)–(2) — Automated Pharmacy Systems",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A Massachusetts pharmacy uses a robotic packaging machine to count and label medications. It stores two manufacturing lots in one automated cell. A recall applies to only one of the lots. Which control is required?",
        "choices": [
          "The pharmacy must have a procedure to quarantine all commingled lots when any one lot is recalled",
          "The pharmacy may ignore the recall because the machine counted correctly",
          "Only the recalled lot should be quarantined, even if the pharmacy cannot distinguish the lots",
          "All products become Schedule II when loaded into pharmacy automation"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 9.11(1)(b) expressly requires procedures for quarantine of all commingled lots upon a recall.",
          "Counting verification does not resolve a recall traceability problem.",
          "Commingled lots cannot be confidently separated once identities are lost.",
          "Automation does not alter a product's legal schedule."
        ],
        "citation": "247 CMR 9.11(1)–(2) — Pharmacy Processing Automation",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A licensed Massachusetts hospital maintains an automated dispensing device near nursing units. The device holds controlled medications and releases drugs to nurses under patient-specific orders. Which legal category applies?",
        "choices": [
          "The device is a retail APS dispensing directly to anonymous customers",
          "It is a medication wholesaler and has no patient-order requirement",
          "It is an ADD in a licensed health care facility, subject to a valid patient-specific prescription or order, security, records and policy requirements",
          "It can be treated as a medication manufacturer exempt from all pharmacy rules"
        ],
        "answer": "C",
        "explanations": [
          "A patient-care ADD differs from a retail patient pickup APS.",
          "ADD use is not merely wholesale distribution.",
          "Correct. 247 CMR 9.12 conditions controlled ADD dispensing on facility location, patient-specific order, and required safeguards.",
          "Healthcare automation does not create a manufacturer exemption."
        ],
        "citation": "247 CMR 9.12(1)–(4) — Automated Dispensing Devices",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A Massachusetts community pharmacy uses a retail APS overnight but provides pharmacist consultation by telephone only until the pharmacy closes at 8 p.m. What must be corrected?",
        "choices": [
          "The consultation service is required only for Schedule IV drugs",
          "The pharmacy must provide an opportunity for pharmacist consultation throughout all hours that the APS dispenses medications",
          "A pharmacy technician's voicemail is always enough to meet the standard",
          "After-hours use eliminates all patient counseling and privacy protections"
        ],
        "answer": "B",
        "explanations": [
          "The consultation requirement applies to permitted APS drug dispensing generally.",
          "Correct. Enacted 247 CMR 9.10(1)(g) uses all hours of APS operation, not only normal pharmacy hours.",
          "Recorded voicemail without pharmacist access does not ensure a consultation opportunity.",
          "Operation beyond regular business hours does not waive legal duties."
        ],
        "citation": "247 CMR 9.10(1)–(2) — Automated Pharmacy Systems",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A Massachusetts pharmacy uses telepharmacy video technology to verify final patient-specific products remotely. The owner proposes removing the only pharmacist physically on duty at the dispensing pharmacy. Which requirement applies?",
        "choices": [
          "Remote high-resolution verification automatically eliminates every on-site pharmacist requirement",
          "Policy 2021-02 still requires at least one licensed pharmacist on the premises of the Board-licensed pharmacy that dispenses the final product",
          "A trained technician can replace the on-site pharmacist when a video camera is present",
          "An automated pickup locker grants a general exemption from telepharmacy supervision"
        ],
        "answer": "B",
        "explanations": [
          "Remote verification is authorized for certain functions but does not waive an on-site pharmacist.",
          "Correct. Policy 2021-02 §VI(b)(ii) expressly requires one pharmacist on the dispensing pharmacy premises.",
          "Technician participation cannot eliminate this particular pharmacist presence requirement.",
          "APS permissions are distinct from telepharmacy staffing obligations."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §VI — Telepharmacy",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A pharmacist reviews a Schedule II central-fill prescription sent electronically by the originating retail pharmacy. The central-fill partner claims that electronic transmission alone replaces all other central-fill records. What is required?",
        "choices": [
          "Central fill may dispense without verifying a valid patient prescription",
          "Either pharmacy may omit its registration and legal records if a shared system exists",
          "Both pharmacies must preserve the federal central-fill record and prescription transmission information specified by 21 CFR 1306.15",
          "All electronically transmitted prescriptions are automatically refills"
        ],
        "answer": "C",
        "explanations": [
          "A valid underlying prescription remains essential.",
          "Participating registrants retain their regulatory records.",
          "Correct. §1306.15 specifies the respective records and information that must accompany central-fill Schedule II activities.",
          "An electronic central-fill transmission is not a prescription refill."
        ],
        "citation": "21 CFR §1306.15(a)–(d) — Central Filling of Schedule II Prescriptions",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.15"
      }
    ],
    "hard": [
      {
        "question": "A pickup locker is installed just outside a pharmacy building. It offers refrigerated insulin and Schedule III medication. The pharmacy has video surveillance but no access to a pharmacist overnight. Which option identifies the controlling problems?",
        "choices": [
          "An outdoor APS, refrigerated stock, Schedule III dispensing and missing consultation access each conflict with conditions of 247 CMR 9.10",
          "The video camera automatically cures all other APS deficiencies",
          "Any medication may be kept in a pickup locker if the patient provides a PIN",
          "Schedule III medicines are permitted in APS whenever the refrigeration issue is corrected"
        ],
        "answer": "A",
        "explanations": [
          "Correct. The rule requires the same building, permits only Schedules IV–VI, forbids refrigerated/reconstitution stock and requires pharmacist consultation whenever operating.",
          "Surveillance is one condition, not an override.",
          "A PIN alone does not establish all required safeguards.",
          "Schedule III remains outside the specified APS authority."
        ],
        "citation": "247 CMR 9.10(1)–(2) — Automated Pharmacy Systems",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "A retail pharmacy arranges shared filling with a separately owned pharmacy using a written contract. It never informs patients and has no opt-out process. After a wrong-drug error, the retail pharmacy blames the central-fill site and denies responsibility. Which analysis is best?",
        "choices": [
          "The retail pharmacy has no responsibility because another pharmacy filled the container",
          "Common ownership is mandatory even if there is a written agreement",
          "Both participants remain jointly responsible, and the retail pharmacy also failed the patient notification and opt-out conditions",
          "The patient is solely responsible because the prescription was released"
        ],
        "answer": "C",
        "explanations": [
          "Shared services involve joint accountability.",
          "The policy allows a written contract in place of common ownership.",
          "Correct. Policy 2021-02 requires patient notification/opt-out and treats participants as jointly responsible for properly processed and filled prescriptions.",
          "Patient pickup does not replace professional accountability."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A Massachusetts-licensed central-fill retail pharmacy offers to prepare a patient-specific compounded sterile IV bag for another retail pharmacy, then send it back for patient dispensing. Both parties have an agreement and use a secure database. What is the remaining Massachusetts restriction?",
        "choices": [
          "Shared-service contracts automatically authorize all sterile and complex nonsterile compounding",
          "Only a physician's signature is needed because sterility is a clinical issue",
          "The central filling of compounded sterile preparations or complex nonsterile preparations for Massachusetts dispensing is prohibited under Board Policy 2021-02",
          "Being a nonresident central-fill pharmacy removes the prohibition"
        ],
        "answer": "C",
        "explanations": [
          "An agreement does not override the explicit compounding restriction.",
          "Patient orders are necessary but not enough to permit prohibited central-fill compounding.",
          "Correct. Policy 2021-02 §IV(b)(v) explicitly prohibits this central-fill compounding pathway.",
          "The restriction includes preparations dispensed into, within or from Massachusetts."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §IV(b)(v) — Central Fill Compounding",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A licensed certified technician is authorized under the relevant MA ADD policy to load certain unverified, non-patient-specific Schedule VI stock with electronic validation. The drug is gabapentin, which is specifically PMP-reportable. What should the pharmacy conclude?",
        "choices": [
          "Certified status permits unverified gabapentin stocking because it is Schedule VI",
          "An unlicensed trainee could load the gabapentin instead",
          "All Schedule VI medicines qualify regardless of PMP classification",
          "The narrow certified-technician no-prior-verification exception excludes PMP-reportable Schedule VI stock such as gabapentin"
        ],
        "answer": "D",
        "explanations": [
          "Board policy excludes PMP-reportable Schedule VI drugs from the special exception.",
          "Moving the task to an unlicensed trainee does not remove safeguards.",
          "Schedule VI includes different reporting subcategories.",
          "Correct. Policy 2023-08 excludes Additional Drugs/reportable Schedule VI from the limited no-prior-verification pathway."
        ],
        "citation": "MA Joint Policy 2023-08 — Pharmacy Technician Stocking of Automated Dispensing Devices",
        "sourceUrl": "https://www.mass.gov/doc/2023-08-pharmacy-technician-stocking-of-automated-dispensing-devices-pdf/download"
      },
      {
        "question": "An authorized central-fill pharmacy prepares Schedule II oxycodone for an originating pharmacy. The central-fill pharmacy contracts with a shipping carrier, and the controlled medication is stolen while being delivered between sites. Which registrant has the federal loss-reporting responsibility under 21 CFR 1301.76(d)?",
        "choices": [
          "The originating pharmacy always reports, regardless of shipping contracts",
          "The central-fill pharmacy that contracted with the shipping carrier has the specified in-transit theft/loss reporting responsibility",
          "No registrant needs to report because the patient has not collected the prescription",
          "The prescriber must report because the order was signed under the prescriber's DEA number"
        ],
        "answer": "B",
        "explanations": [
          "The federal rule distinguishes who contracted the carrier.",
          "Correct. §1301.76(d) places in-transit reporting responsibility on the central-fill pharmacy when it contracts the carrier.",
          "Loss before patient pickup remains reportable when federal criteria apply.",
          "The prescriber is not automatically responsible for a pharmacy's carrier contract."
        ],
        "citation": "21 CFR §1301.76(d) — Central-fill in-transit loss",
        "sourceUrl": "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.76"
      },
      {
        "question": "A licensed technician completes prescription data entry remotely from home for a Massachusetts community pharmacy. The pharmacist verifies the prescription electronically, but the pharmacy fails to maintain a secure audit trail showing who processed the order and when. What is missing?",
        "choices": [
          "Nothing; remote work eliminates the need for an audit trail",
          "The pharmacy must cancel all remote processing because a technician was involved",
          "Shared pharmacy policies require a secure accessible record and audit trail of each step, including involved individuals and date/time",
          "Only the prescriber's clinical chart is relevant to remote processing"
        ],
        "answer": "C",
        "explanations": [
          "Remote processing remains subject to data security and audit trail obligations.",
          "Licensed pharmacy technicians may qualify for defined remote processing.",
          "Correct. Board Policy 2021-02 §III(d)–(h) includes secure shared information and per-step audit trails.",
          "Prescriber notes do not replace pharmacy audit records."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "A hospital proposes an ADD in a licensed long-term care facility, with security and electronic audit logs, but plans to allow withdrawal of controlled medication from general ward stock without an identified patient order. Which legal requirement has not been met?",
        "choices": [
          "An ADD may dispense controlled substances only pursuant to a valid patient-specific prescription or order, even in a licensed facility",
          "Any drug may be removed under an anonymous standing instruction",
          "The facility's state license converts all controlled drugs into Schedule VI",
          "Continuous video allows dispensing without a patient order"
        ],
        "answer": "A",
        "explanations": [
          "Correct. 247 CMR 9.12(2) requires a valid patient-specific prescription or order.",
          "The ADD permission does not authorize anonymous controlled dispensing.",
          "Facility licensure does not change drug scheduling.",
          "Security technology does not substitute for the prescription requirement."
        ],
        "citation": "247 CMR 9.12(1)–(4) — Automated Dispensing Devices",
        "sourceUrl": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
      },
      {
        "question": "An MA central-fill pharmacy prepares an ordinary Schedule VI lisinopril prescription and a separate Schedule VI gabapentin prescription for patients at the originating pharmacy. It plans to ship both directly to the patients. What is the state-law distinction?",
        "choices": [
          "Both are eligible for direct shipment whenever the originating pharmacy signed an agreement",
          "Neither may ever be shipped by any pharmacy because they are Schedule VI",
          "Only the gabapentin may be shipped directly because it has additional PMP reporting",
          "Non-PMP-reportable Schedule VI may be shipped directly under the policy, but PMP-reportable drugs such as gabapentin are excluded from that direct-to-patient central-fill option"
        ],
        "answer": "D",
        "explanations": [
          "The Board policy makes a specific exception for PMP-reportable Schedule VI.",
          "Schedule VI non-PMP-reportable central-fill medicines may be directly shipped under specified conditions.",
          "Gabapentin is specifically excluded from this exception.",
          "Correct. Policy 2021-02 §IV(b)(iv) distinguishes reportable Schedule VI drugs from other Schedule VI central-fill shipments."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §IV(b)(iv) — Direct Shipment Exception",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "Two pharmacy corporations with a written shared-services contract wish to host a pharmacy data-processing team in Canada. They will use encryption and US-licensed pharmacists for review. What does the Massachusetts Board's shared-services policy require?",
        "choices": [
          "Any international location qualifies if the files are encrypted",
          "Shared Pharmacy Services under Policy 2021-02 must occur within the United States, independent of ownership, contracts and encryption",
          "The Board policy's US limitation applies only to patient pickup lockers",
          "A shared-services contract can automatically waive the geographic restriction"
        ],
        "answer": "B",
        "explanations": [
          "Encryption alone does not eliminate the geographic requirement.",
          "Correct. Policy 2021-02 §III(b) explicitly limits these shared services to within the United States.",
          "Pickup lockers are a separate category.",
          "Written agreements allocate responsibilities but do not waive all policy conditions."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      },
      {
        "question": "An MA retail pharmacy has a compliant shared-service arrangement, but one participant becomes unable to process prescriptions after a ransomware outage. The other pharmacy continues dispensing without a documented continuity-of-care arrangement. Which safeguard was missing?",
        "choices": [
          "The participating pharmacies must establish and maintain a continuity plan identifying how patients' prescription needs will be met when any participant cannot process or fill orders",
          "Patient treatment may be suspended indefinitely once the agreement is signed",
          "Only the cloud software provider needs an emergency plan",
          "A shared-service outage automatically turns all controlled prescriptions into Schedule VI"
        ],
        "answer": "A",
        "explanations": [
          "Correct. Policy 2021-02 §III(p) specifically requires a continuity-of-care plan for a participant's inability to process or fill.",
          "Therapy continuity remains a professional obligation.",
          "The pharmacies, not solely the vendor, must prepare the plan.",
          "Information system failure does not change controlled schedules."
        ],
        "citation": "MA Board Policy 2021-02 (revised 2025), §III — Shared Pharmacy Service requirements",
        "sourceUrl": "https://www.mass.gov/doc/2021-02-shared-pharmacy-service-models-including-central-fill-remote-processing-and-telepharmacy-pdf/download"
      }
    ]
  }
});

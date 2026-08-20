"""Canonical rule records required by the B3-E v2 expansion, MA-Q-0370 through MA-Q-0390.

Every rule below was read verbatim from the current official publication on 2026-08-20:

  * 247 CMR 9.00 Professional Practice Standards, official PDF
    (sha256 9e1f9d1d2813f761ee7d275c83e220f371382a2e81e0f485f2b7aaabcddce22a).
  * 247 CMR 6.00 Licensure of Pharmacies, official PDF
    (sha256 8d1def57328d628a0c2e5a3a7adac28afa2d361585c09550b571f92eafa919f1).
  * 105 CMR 700.000, official PDF
    (sha256 78c4d84206d280f7aaee0d95bd9c07229366205dfd65fd177ac7847d861a2bcd).
  * M.G.L. c. 94C ss. 21 and 23, read on malegislature.gov.

Two further propositions in this expansion reuse rules that already exist: MA-CS-LABEL for the
M.G.L. c. 94C s. 21 container label, and MA-ORAL-CONTROLLED-DOCUMENTATION for s. 20. No rule is
duplicated.

See audits/controller/B3E-V2-EXPANSION-CENSUS.json for the novelty probe and source survey.
"""

from __future__ import annotations

CMR9 = "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"
CMR6 = "https://www.mass.gov/regulations/247-CMR-600-licensure-of-pharmacies"
CMR700 = "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c"
GL21 = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21"
GL23 = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"

VERIFIED = "2026-08-20"
BORP = "Massachusetts Board of Registration in Pharmacy regulations"
DPH = "Massachusetts Department of Public Health regulations"


def _rule(rule_id, area, topic, subtopic, title, summary, relevance, authority,
          confusions, numeric=(), exceptions=(), related=()):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": "MA",
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": relevance,
        "authority": list(authority),
        "status": "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": VERIFIED,
        "numeric_facts": list(numeric),
        "exceptions": list(exceptions),
        "common_confusions": list(confusions),
        "related_rule_ids": list(related),
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": (
            "Read verbatim in the current official publication on 2026-08-20 during the Batch 3 "
            "tranche B3-E v2 expansion under Issue #91. A fresh independent legal and full-bank "
            "realism audit is still required before release."
        ),
    }


def _b(section, url=CMR9):
    return {"type": "PROMULGATED_REGULATION", "name": BORP, "section": section, "url": url}


def _d(section):
    return {"type": "PROMULGATED_REGULATION", "name": DPH, "section": section, "url": CMR700}


def _s(section, url):
    return {"type": "STATUTE", "name": "Massachusetts General Laws", "section": section, "url": url}


RULES = [
    # ================= AREA 3 — dispensing decision paths =================
    _rule(
        "MA-RX-LABEL-PRINTING", 3, "Dispensing requirements", "Label production",
        "Prescription labels must be computer printed, with a narrow emergency alternative",
        "A licensee shall ensure the label affixed to a prescription drug container or package is "
        "CLEARLY PRINTED BY A COMPUTERIZED PHARMACY SYSTEM. In the event of printing or equipment "
        "failure, a prescription label may be legibly handwritten or typed DURING AN EMERGENCY "
        "PERIOD. The alternative is tied to a failure and to a period, not to convenience.",
        "Tests that a handwritten label is a failure-contingent exception rather than a general "
        "option, and that legibility is the standard when it applies.",
        [_b("247 CMR 9.04(3)")],
        ["Treating a handwritten label as always acceptable if it is legible",
         "Assuming the exception covers a busy period rather than an equipment failure",
         "Assuming a pharmacy may operate without a computerized pharmacy system at all"],
        exceptions=["Legibly handwritten or typed during an emergency period of printing or "
                    "equipment failure"],
        related=["MA-CS-LABEL"],
    ),
    _rule(
        "MA-RX-NDC-RECORDING", 3, "Dispensing requirements", "Product identification record",
        "Recording product identity when a drug is distributed solely under a generic name",
        "Whenever a prescription drug has been distributed SOLELY UNDER A GENERIC NAME, the "
        "dispensing pharmacist shall record the NDC number in the computerized pharmacy system. In "
        "the event an NDC number does not exist, the pharmacist shall record the NAME OF THE "
        "MANUFACTURER, or, if the manufacturer's name is not available, the name of the "
        "DISTRIBUTOR, PACKER, OR REPACKER. The fallbacks run in that order.",
        "Tests an ordered fallback chain, which candidates routinely flatten into a single "
        "requirement to record something identifying.",
        [_b("247 CMR 9.04(7)")],
        ["Recording the distributor while the manufacturer's name is available",
         "Treating the requirement as applying to every dispensing rather than to generic-name "
         "distribution",
         "Assuming a paper note satisfies a requirement directed at the computerized system"],
    ),
    _rule(
        "MA-RX-TELEPHONE-RECEIPT", 3, "Dispensing requirements", "Receipt of a telephoned prescription",
        "Who may take a new prescription over the telephone",
        "A pharmacy intern, or a CERTIFIED pharmacy technician WHO HAS THE APPROVAL OF THE "
        "PHARMACIST ON DUTY, may receive NEW prescriptions over the telephone from a prescriber or "
        "an authorized agent. Both limbs matter for the technician: certification and the on-duty "
        "pharmacist's approval.",
        "Tests a delegation that is available but conditioned, against the two common errors of "
        "assuming no one but a pharmacist may take the call and assuming any technician may.",
        [_b("247 CMR 9.04(8)")],
        ["Assuming only a pharmacist may receive a new telephoned prescription",
         "Allowing a non-certified technician to take the call",
         "Overlooking that the on-duty pharmacist's approval is a separate condition"],
        related=["MA-TECH-SCOPE"],
    ),
    _rule(
        "MA-RX-DATE-COUNTING", 3, "Dispensing requirements", "Counting the validity period",
        "The day after the prescription was written is day one",
        "In order to determine whether a prescription is WITHIN DATE, a pharmacist shall count the "
        "DAY AFTER the prescription was written as DAY ONE. The issue date itself is not counted, so "
        "a period measured in days runs from the following day.",
        "Tests a counting convention that decides borderline cases and that candidates almost always "
        "get wrong by starting the count on the issue date.",
        [_b("247 CMR 9.04(10)")],
        ["Counting the date of issue as day one",
         "Applying a different convention to different schedules, when the rule is general",
         "Confusing the counting convention with the length of the validity period itself"],
        related=["MA-CII-VALIDITY-30D"],
    ),
    _rule(
        "MA-RX-OFFSITE-PROCESSING", 3, "Dispensing requirements", "Processing outside the premises",
        "Medication processed off site may be dispensed only on one of two conditions",
        "A pharmacy MAY NOT DISPENSE any medication that was processed OUTSIDE ITS LICENSED PHARMACY "
        "PREMISES unless that process was VERIFIED BY A MASSACHUSETTS LICENSED PHARMACIST or was "
        "PERFORMED IN A PHARMACY LICENSED BY THE BOARD. The two cures are alternatives and neither "
        "is satisfied by the dispensing pharmacy's own after-the-fact inspection of the product.",
        "Tests the boundary of central fill and off-premises processing, and that the cure attaches "
        "to the PROCESS rather than to the finished product.",
        [_b("247 CMR 9.04(11)")],
        ["Treating a visual check of the finished product as verification of the process",
         "Assuming any licensed pharmacy anywhere satisfies the second limb, when it must be "
         "licensed by the Board",
         "Assuming an out-of-state pharmacist's verification suffices"],
    ),
    _rule(
        "MA-RX-CUSTOMER-IDENTIFIER", 3, "Dispensing requirements", "Positive identification",
        "Customer Identifier on a Schedule II through V dispensing, and the hardship route",
        "A licensee shall require a CUSTOMER IDENTIFIER, being the identification number on a valid "
        "government issued identification obtained by inspecting the identification of the ultimate "
        "user or their agent, on dispensing a controlled substance in Schedules II through V or an "
        "additional drug under 105 CMR 700.012(A)(1). A licensee may dispense WITHOUT one only if it "
        "has reason to believe that refusing would cause SERIOUS HARDSHIP to the ultimate user or "
        "agent AND DOCUMENTS THE REASON, AND the recipient PRINTS name and address on the reverse of "
        "the prescription or in a prescription log AND SIGNS it. The Commissioner may waive or modify "
        "the requirement for refills, deliveries or other specified activities.",
        "Tests a three-part cure where candidates typically remember only the hardship belief.",
        [_b("247 CMR 9.04(14)")],
        ["Treating a hardship belief alone as sufficient without documentation and signature",
         "Assuming a familiar regular patient is outside the requirement",
         "Assuming the identifier requirement reaches Schedule VI generally, when it reaches "
         "Schedules II through V and designated additional drugs"],
        exceptions=["Documented serious hardship with the recipient's printed name, address and "
                    "signature", "Commissioner waiver or modification for refills, deliveries or "
                    "other specified activities"],
    ),
    _rule(
        "MA-RX-LARGE-PRINT-DIRECTIONS", 3, "Dispensing requirements", "Accessible label directions",
        "Ten characters per inch on request for an elderly or visually impaired person",
        "UPON THE REQUEST of an elderly person, as defined in M.G.L. c. 19A, s. 14, or of a person "
        "who is VISUALLY IMPAIRED, the directions on the label affixed by the pharmacist to a "
        "container of a prescription drug shall be TYPED IN A PRINT SIZE ALLOWING NO MORE THAN TEN "
        "CHARACTERS PER INCH. The duty is triggered by the request, and the standard is expressed as "
        "a maximum character density rather than a point size.",
        "Tests a request-triggered accessibility duty with a specific measurable standard, which no "
        "other bank question reaches.",
        [_s("M.G.L. c. 94C, s. 21, second paragraph", GL21)],
        ["Treating the duty as automatic for anyone who appears elderly",
         "Reading the standard as a minimum rather than a maximum character density",
         "Assuming it reaches the whole label rather than the directions"],
        numeric=[{"fact": "Maximum print density for directions on request", "value": 10,
                  "unit": "characters per inch", "conditions": "elderly or visually impaired person, "
                                                              "upon request"}],
        related=["MA-CS-LABEL"],
    ),
    _rule(
        "MA-CII-PHARMACIST-ENDORSEMENT", 3, "Controlled prescriptions", "Schedule II endorsement and filing",
        "The filling pharmacist endorses a Schedule II prescription and it is filed separately",
        "The pharmacist filling a written or electronic prescription for a controlled substance in "
        "Schedule II SHALL ENDORSE HIS OWN SIGNATURE ON THE FACE THEREOF. A written or electronic "
        "Schedule II prescription SHALL NOT BE REFILLED, and written Schedule II prescriptions SHALL "
        "BE KEPT IN A SEPARATE FILE.",
        "Tests a personal endorsement duty and a filing duty that sit beside the better-known "
        "no-refill rule, and that candidates commonly attribute to the prescriber.",
        [_s("M.G.L. c. 94C, s. 23(b) and (c)", GL23)],
        ["Assuming the signature required is the prescriber's rather than the filling pharmacist's",
         "Assuming initials on the label discharge the endorsement duty",
         "Overlooking the separate-file requirement for written Schedule II prescriptions"],
        related=["MA-CII-VALIDITY-30D"],
    ),
    # ================= AREA 4 — facility, security and licensure =================
    _rule(
        "MA-CS-PERSONNEL-SCREENING", 4, "Controlled substance security", "Personnel screening",
        "Pre-employment screening and an absolute bar on employing certain persons",
        "All applicants and registrants shall SCREEN BEFORE EMPLOYING new employees who may work in "
        "or around areas where controlled substances are handled. The screening is made SOLELY to "
        "determine whether the prospective employee is a responsible person who can be trusted to "
        "work in and around controlled substances, and documentation of it shall be made available "
        "to the Commissioner ON REQUEST. NO REGISTRANT SHALL KNOWINGLY EMPLOY any agent or employee "
        "who has had an application for registration DENIED for violation of any law or regulation, "
        "or has had their registration REVOKED for violation of any law or regulation, AT ANY TIME.",
        "Tests a procedural duty and an absolute status bar in one provision, where the bar has no "
        "look-back limit at all.",
        [_d("105 CMR 700.005(B)")],
        ["Assuming an old denial or revocation eventually ceases to matter",
         "Treating the screening as a general background check rather than one directed at "
         "trustworthiness around controlled substances",
         "Assuming the documentation must be filed rather than made available on request"],
        exceptions=[],
        related=["MA-CS-SECURITY"],
    ),
    _rule(
        "MA-CLOSURE-DUTIES-BY-TYPE", 4, "Pharmacy licensure", "Closure duties by pharmacy type",
        "Closure duties vary with the type of pharmacy",
        "A NON-RESIDENT pharmacy closing gives the Board certified written notice at least 14 days "
        "ahead with a SHORTER set of particulars, and the post-closure submission of original "
        "licences and the controlled-substance attestation at 247 CMR 6.13(6) DOES NOT APPLY to "
        "non-resident pharmacies. A sterile compounding, complex non-sterile compounding, "
        "institutional sterile compounding or non-resident compounding pharmacy must ADDITIONALLY "
        "notify the Board, at least 14 days ahead, of the IDENTITY OF A BOARD-LICENSED PHARMACY "
        "SUITABLE AND AVAILABLE TO PROVIDE CONTINUITY OF CARE to its patients. 247 CMR 6.13(3) and "
        "6.13(4) are NOT REQUIRED for institutional sterile compounding pharmacies.",
        "Tests that a single closure regime carries three type-specific variations, which a "
        "candidate applying one uniform checklist will miss.",
        [_b("247 CMR 6.13(2), (3) and (7)", CMR6)],
        ["Applying the resident post-closure submission to a non-resident pharmacy",
         "Overlooking the continuity-of-care identification for compounding pharmacies",
         "Applying the patient-notice duty to an institutional sterile compounding pharmacy"],
        related=["MA-PHARMACY-CLOSURE-NOTICE", "MA-PHARMACY-CLOSURE-CS"],
    ),
    _rule(
        "MA-PHARMACY-RELOCATION", 4, "Pharmacy licensure", "Relocation",
        "Relocation needs prior Board approval and a ninety-day application",
        "A pharmacy licensed by the Board shall APPLY TO THE BOARD FOR APPROVAL TO RELOCATE to a new "
        "address PRIOR TO RELOCATING and MAY NOT RELOCATE UNTIL IT RECEIVES APPROVAL. The "
        "application is submitted AT LEAST 90 DAYS before the desired date of relocation, unless "
        "otherwise approved by the Board, with the appropriate fee and blueprints or equivalent "
        "architectural drawings depicting the pharmacy layout.",
        "Tests a long lead time and a prohibition on acting before approval, against the assumption "
        "that notification is enough.",
        [_b("247 CMR 6.16", CMR6)],
        ["Treating relocation as a notification rather than an approval",
         "Assuming a shorter notice period comparable to the 14-day closure notice",
         "Assuming the move may begin while the application is pending"],
        numeric=[{"fact": "Minimum lead time for a relocation application", "value": 90,
                  "unit": "days", "conditions": "before the desired relocation date, unless the "
                                                "Board approves otherwise"}],
    ),
    _rule(
        "MA-PHARMACY-REMODEL-APPROVAL", 4, "Pharmacy licensure", "Remodeling and configuration",
        "No construction may commence before the Board approves",
        "A Drug Store pharmacy, sterile compounding pharmacy, complex non-sterile compounding "
        "pharmacy, institutional sterile compounding pharmacy and non-resident sterile compounding "
        "pharmacy shall apply to the Board for approval to remodel or to change the CONFIGURATION or "
        "SQUARE FOOTAGE, and MAY NOT COMMENCE ANY CONSTRUCTION WORK OR REMODELING until it receives "
        "approval. The supporting submission includes blueprints or equivalent architectural "
        "drawings depicting the pharmacy layout, the PRESCRIPTION AREA and the COUNSELING AREA, and, "
        "for a Massachusetts pharmacy, a WRITTEN PLAN TO MAINTAIN SECURITY OF CONTROLLED SUBSTANCES "
        "DURING ANY TRANSPORTATION.",
        "Tests a prohibition on starting work and a submission list whose distinctive members are "
        "the counseling area and the transport security plan.",
        [_b("247 CMR 6.15(1) and (3)", CMR6)],
        ["Beginning work and seeking approval afterwards",
         "Omitting the counseling area from the drawings",
         "Overlooking the controlled substance transport security plan"],
        related=["MA-PHARMACY-RELOCATION"],
    ),
    _rule(
        "MA-ENGINEERING-CONTROL-APPROVAL", 4, "Compounding", "Secondary engineering controls",
        "Approval before touching a secondary engineering control",
        "A sterile compounding pharmacy, non-resident sterile compounding pharmacy and institutional "
        "sterile compounding pharmacy shall apply for Board approval PRIOR TO MOVING, ADDING, "
        "MODIFYING, REMOVING OR REPLACING ANY SECONDARY ENGINEERING CONTROL, and may not do so until "
        "approval is received. Its submission adds CERTIFIED blueprints depicting compounding areas "
        "and the location and ISO CLASSIFICATION of each primary and secondary engineering control "
        "and the placement of containment hoods, a CONTAINMENT STRATEGY, an ENVIRONMENTAL MONITORING "
        "PLAN, a plan to RE-CERTIFY primary and secondary engineering controls and containment hoods, "
        "and a CONTINUITY OF CARE PLAN, each as applicable.",
        "Tests that an engineering-control change is a separately approved event with a heavier "
        "submission than an ordinary remodel.",
        [_b("247 CMR 6.15(2) and (4)", CMR6)],
        ["Treating a like-for-like replacement as outside the approval requirement",
         "Submitting ordinary layout drawings rather than certified blueprints with ISO "
         "classification",
         "Assuming a Drug Store pharmacy is subject to the same submission"],
        related=["MA-PHARMACY-REMODEL-APPROVAL"],
    ),
    _rule(
        "MA-MOR-CHANGE-INVENTORY", 4, "Pharmacy licensure", "Change of Manager of Record",
        "The inventory attestation that must accompany a change of Manager of Record",
        "A change of Manager of Record application shall include an ATTESTATION confirming the "
        "pharmacy performed an inventory of all controlled substances in Schedules II through V AND "
        "Schedule VI substances required to be reported to the prescription monitoring program, and "
        "filed the inventory report with the pharmacy's controlled substance records. The attestation "
        "shall be SIGNED BY THE OUTGOING MANAGER OF RECORD AND THE PROPOSED INCOMING MANAGER OF "
        "RECORD. Where the outgoing Manager is unavailable due to DEATH, SERIOUS ILLNESS OR "
        "TERMINATION, a staff pharmacist may be authorized to sign PROVIDED the Board is notified at "
        "the time of application of the reason. The application also carries the ORIGINAL Drug Store "
        "Pharmacy licence and the required fees, and the Board may require the proposed Manager to "
        "appear before it.",
        "Tests a dual-signature attestation with a narrow substitution route, and the inclusion of "
        "reportable Schedule VI in the inventory.",
        [_b("247 CMR 6.10(1) and (2)", CMR6)],
        ["Assuming only the incoming Manager of Record signs",
         "Omitting reportable Schedule VI substances from the inventory",
         "Using the staff-pharmacist substitution for an outgoing Manager who is merely unwilling"],
        exceptions=["A staff pharmacist may sign where the outgoing Manager of Record is unavailable "
                    "due to death, serious illness or termination, on notice to the Board of the reason"],
        related=["MA-MOR-TEMP-ABSENCE"],
    ),
    _rule(
        "MA-PHARMACY-NAME-CHANGE", 4, "Pharmacy licensure", "Notification of a name change",
        "Fourteen days to notify the Board of a change of operating name",
        "A licensee shall NOTIFY THE BOARD, WITHIN 14 DAYS, IN WRITING, of any change in the NAME "
        "UNDER WHICH THE PHARMACY OPERATES, accompanied by APPROPRIATE AUTHORIZING DOCUMENTATION. "
        "The clock runs from the change and the notice must carry the supporting documentation.",
        "Tests a short reporting clock on a change candidates treat as cosmetic, and the "
        "documentation that must accompany it.",
        [_b("247 CMR 6.12", CMR6)],
        ["Treating a trading-name change as outside the requirement",
         "Reporting at the next renewal rather than within 14 days",
         "Sending a bare notice without the authorizing documentation"],
        numeric=[{"fact": "Deadline to notify the Board of a pharmacy name change", "value": 14,
                  "unit": "days", "conditions": "in writing, with authorizing documentation"}],
    ),
]

"""Canonical rule records required by tranche B3-F, MA-Q-0391 through MA-Q-0406.

B3-F exists because the B3-S3 legacy salvage returned nothing usable: CLAUDE-FRESH-B3S3-V2 failed
all eight of its questions on realism, leaving a measured Area-3 deficit of six against the Issue #91
minimum of 87. See audits/controller/BATCH3-AREA3-TOPUP-DETERMINATION.json.

Every rule below was read verbatim from the current official publication on 2026-08-20:

  * 247 CMR 9.00 Professional Practice Standards, official PDF
    (sha256 9e1f9d1d2813f761ee7d275c83e220f371382a2e81e0f485f2b7aaabcddce22a).
  * 105 CMR 700.000, official PDF
    (sha256 78c4d84206d280f7aaee0d95bd9c07229366205dfd65fd177ac7847d861a2bcd).
  * M.G.L. c. 94C ss. 18, 18D and 21, read on malegislature.gov.
  * 21 CFR 208.24 and 208.26, read through the eCFR API.

Seven of the ten sections drawn on here -- 247 CMR 9.05, 9.07, 9.08, 9.11, 9.12, 9.22 and the
M.G.L. c. 94C s. 18(d3/4) pathway limits -- were cited by no rule in the bank before this tranche.
They are ordinary dispensing decisions rather than another pass over refill arithmetic, which is what
the S2 realism failures were made of.

Five further propositions reuse rules that already exist: MA-RX-TRANSFER, MA-CS-II-III-PAMPHLET,
MA-COMPOUND-LABEL-CONTACT, MA-CII-OPIOID-ANTAGONIST-OFFER and FED-PSE-QUANTITY. No rule is duplicated.
"""

from __future__ import annotations

CMR9 = "https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"
CMR700 = "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c"
GL18 = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"
CFR208_24 = "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-208/section-208.24"
CFR208_26 = "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-208/section-208.26"

VERIFIED = "2026-08-20"
BORP = "Massachusetts Board of Registration in Pharmacy regulations"
DPH = "Massachusetts Department of Public Health regulations"

NOTES = (
    "Read verbatim in the current official publication on 2026-08-20 during Batch 3 tranche B3-F "
    "under Issue #91. A fresh independent legal and full-bank realism audit is still required "
    "before release."
)


def _rule(rule_id, area, topic, subtopic, title, summary, relevance, authority, confusions,
          numeric=(), exceptions=(), related=(), jurisdiction="MA"):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": jurisdiction,
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
        "verification_notes": NOTES,
    }


def _b(section):
    return {"type": "PROMULGATED_REGULATION", "name": BORP, "section": section, "url": CMR9}


def _d(section):
    return {"type": "PROMULGATED_REGULATION", "name": DPH, "section": section, "url": CMR700}


RULES = [
    _rule(
        "MA-INTERCHANGE-MEDICAL-EMERGENCY", 3, "Dispensing", "Substitution in a medical emergency",
        "Medical-emergency deviation from the substitution instruction",
        "In a MEDICAL EMERGENCY a pharmacist may fill a prescription marked 'no substitution' by "
        "dispensing a less expensive interchangeable drug product allowed by the Massachusetts List "
        "of Interchangeable Drugs IF THE PARTICULAR BRAND IS NOT IN STOCK; and may fill a "
        "prescription NOT marked 'no substitution' by dispensing the brand name product as written "
        "if no less expensive interchangeable product is in stock. In either instance the pharmacist "
        "MUST RECORD THE DATE, HOUR AND NATURE OF THE MEDICAL EMERGENCY on the back of the "
        "prescription or in the computerized pharmacy system, AND the person purchasing the drug "
        "product MUST INDICATE ACCEPTANCE of this deviation IN WRITING.",
        "Candidates who know only the general no-substitution rule miss that a medical emergency "
        "opens a narrow two-way deviation, and that the deviation carries a recording duty and a "
        "written acceptance by the purchaser rather than the pharmacist's judgment alone.",
        [_b("247 CMR 9.05(1)")],
        ["Treating a 'no substitution' direction as absolute even in a medical emergency.",
         "Recording the emergency but omitting the purchaser's written acceptance, or the reverse.",
         "Assuming the deviation runs only toward the cheaper product; it also permits dispensing "
         "the brand as written when no interchangeable product is in stock."],
        exceptions=["The deviation is available only in a medical emergency and only where the "
                    "product actually needed is not in stock."],
        related=["MA-INTERCHANGE"],
    ),
    _rule(
        "MA-REUSABLE-DOSAGE-PLANNER", 3, "Dispensing", "Reusable daily dosage planners",
        "Conditions for dispensing into a reusable daily dosage planner",
        "At the patient's or the patient's agent's REQUEST a pharmacy MAY dispense medications in a "
        "reusable daily dosage planner provided that: the pharmacy MAY NOT PLACE ANY MEDICATION IN "
        "THE PLANNER THAT WAS PREVIOUSLY DISPENSED BY A DIFFERENT PHARMACY; the pharmacy designates "
        "a space allowing orderly placement of equipment, materials and medications and preventing "
        "cross-contamination; the pharmacy maintains policies and procedures covering cleaning, "
        "labeling, dispensing and proper hand hygiene; and the pharmacy cleans and stores planners "
        "so as to prevent contamination.",
        "A common counter request. The decisive limb is provenance: a planner may not be filled with "
        "another pharmacy's product, however willing the patient is.",
        [_b("247 CMR 9.07")],
        ["Treating the planner service as a courtesy the pharmacy may run on its own initiative "
         "rather than on the patient's or agent's request.",
         "Accepting medication the patient brings from another pharmacy for placement in the planner.",
         "Assuming ordinary labeling duties fall away because the container is a planner."],
        related=["MA-COMPLIANCE-PACKAGING"],
    ),
    _rule(
        "MA-COMPLIANCE-PACKAGING-STANDARDS", 3, "Dispensing", "Compliance packaging conditions",
        "Regulatory conditions on compliance packaging",
        "A pharmacy or pharmacist may use compliance packaging, including oral-liquid-single-dose, "
        "single-drug-single-dose and multi-drug-single-dose packaging, provided the pharmacy "
        "designates a space preventing cross-contamination, maintains policies and procedures for "
        "each type used covering cleaning, labeling, dispensing, hand hygiene, quarantine and "
        "reverse distribution, THE PACKAGING DOES NOT CONFLICT WITH THE USP-DI MONOGRAPH OR "
        "FDA-APPROVED LABELING, and THE MEDICATIONS ARE COMPATIBLE with the packaging components and "
        "with each other.",
        "Separates the Board's controlled-substance policy question from the regulation's own "
        "conditions. Product labeling and compatibility govern whatever the patient prefers.",
        [_b("247 CMR 9.08(1)")],
        ["Reading the Schedule II/III maintenance-medication policy as the whole of the compliance "
         "packaging rule.",
         "Overlooking that FDA-approved labeling or a USP-DI monograph can forbid repackaging "
         "outright, whatever the pharmacy's procedures say."],
        related=["MA-COMPLIANCE-PACKAGING", "MA-REUSABLE-DOSAGE-PLANNER"],
    ),
    _rule(
        "MA-PHARMACY-PROCESSING-AUTOMATION", 3, "Dispensing", "Pharmacy processing automation",
        "Verification and recall conditions on pharmacy processing automation",
        "A pharmacy may use Pharmacy Processing Automation to count, fill vials or compliance "
        "packaging, and label, provided the automation USES A TECHNOLOGICAL VERIFICATION -- such as "
        "bar code verification, electronic verification, weight verification, radio frequency "
        "identification, or a similar process -- to ensure the correct medication is dispensed; and "
        "provided that IF LOT NUMBERS ARE COMINGLED IN A SINGLE CELL the pharmacy maintains a policy "
        "and procedure to QUARANTINE ALL COMINGLED LOT NUMBERS in the event a single lot is recalled. "
        "The pharmacy shall also maintain policies covering operation and maintenance, security, "
        "controlled substance accountability, quality assurance, and stocking and return activities.",
        "The recall limb is the one candidates miss: comingling is permitted, but only against a "
        "standing policy to quarantine the whole cell when any one lot is recalled.",
        [_b("247 CMR 9.11")],
        ["Assuming a pharmacist's visual check substitutes for the required technological verification.",
         "Assuming comingled lots are forbidden outright rather than conditioned on a quarantine policy.",
         "Treating the automation as relieving the pharmacist of final dispensing process validation."],
        related=["MA-AUTOMATED-DISPENSING-DEVICE-CONDITIONS"],
    ),
    _rule(
        "MA-AUTOMATED-DISPENSING-DEVICE-CONDITIONS", 3, "Dispensing", "Automated dispensing devices",
        "Conditions on a pharmacy's use of an automated dispensing device for controlled substances",
        "A pharmacy may use an automated dispensing device for CONTROLLED SUBSTANCES provided that "
        "the device IS LOCATED IN A LICENSED HEALTH CARE FACILITY; DISPENSING IS PURSUANT TO A VALID "
        "PATIENT-SPECIFIC PRESCRIPTION OR ORDER; utilization accords with all laws, regulations and "
        "policies; and the pharmacy maintains device policies and procedures covering location, "
        "operation and maintenance, security, controlled substances accountability, quality "
        "assurance, stocking and return activities, and patient confidentiality.",
        "Two hard gates sit in front of every other consideration: where the cabinet stands, and "
        "whether the dispensing traces to a patient-specific order.",
        [_b("247 CMR 9.12")],
        ["Treating an automated cabinet in a retail or non-licensed setting as merely a security question.",
         "Allowing stock removal against a floor-stock or anticipatory list rather than a "
         "patient-specific prescription or order."],
        related=["MA-ADD-CORE", "MA-PHARMACY-PROCESSING-AUTOMATION"],
    ),
    _rule(
        "MA-REFRIGERATED-FROZEN-STORAGE", 3, "Dispensing", "Refrigerated and frozen storage",
        "Equipment and monitoring standards for refrigerated and frozen medications",
        "A pharmacy shall maintain policies and procedures ensuring proper refrigeration equipment is "
        "available, of adequate size, and used to maintain proper refrigerator and freezer "
        "temperatures, including A PROTOCOL TO RESPOND TO ANY OUT OF RANGE TEMPERATURE AND AN "
        "ASSESSMENT OF THE INTEGRITY OF THE MEDICATION. A pharmacy shall use a combination "
        "refrigerator/freezer, a standalone refrigerator, or a standalone freezer; FREEZER UNITS "
        "SHALL BE FROST-FREE WITH AN AUTOMATIC DEFROST CYCLE unless otherwise approved by the Board; "
        "and A PHARMACY MAY NOT USE AN APPLIANCE THAT CONTAINS A FREEZER COMPARTMENT WITHIN THE "
        "REFRIGERATOR SPACE, SUCH AS A DORM-STYLE REFRIGERATOR.",
        "A concrete equipment prohibition that is easy to state and easy to violate, paired with the "
        "duty to assess product integrity rather than merely record the excursion.",
        [_b("247 CMR 9.22")],
        ["Treating a dorm-style unit as acceptable because its measured temperatures are in range.",
         "Recording an out-of-range temperature without the required integrity assessment.",
         "Assuming the Board's approval route removes the frost-free requirement without being sought."],
        exceptions=["A freezer unit that is not frost-free with an automatic defrost cycle may be "
                    "used only if otherwise approved by the Board."],
        related=["FED-ADULTERATED-MISBRANDED"],
    ),
    _rule(
        "MA-CII-PARTIAL-FILL-PATHWAY-LIMITS", 3, "Controlled substances",
        "Which partial-fill deadline applies",
        "The five-day initial limit reaches only the out-of-state pathways",
        "Under M.G.L. c. 94C, s. 18(d3/4) a pharmacist filling a Schedule II prescription SHALL, if "
        "requested by the patient, dispense a lesser quantity; ONLY THE SAME PHARMACY that dispensed "
        "the lesser quantity may dispense the remaining portion; a notation of the partial fill and "
        "quantity goes in the patient record, accessible to the prescriber on request; and the "
        "remaining portion MUST BE FILLED NOT LATER THAN 30 DAYS AFTER THE PRESCRIPTION ISSUE DATE. "
        "The separate FIVE-DAY limit on the INITIAL partial dispensing applies only to a prescription "
        "FILLED PURSUANT TO SUBSECTION (d) OR (d1/2) -- respectively a nonnarcotic Schedule II "
        "prescription issued by an out-of-state practitioner, and a narcotic Schedule II prescription "
        "issued by a practitioner registered in Maine or a state contiguous with the commonwealth.",
        "The statute states two deadlines with different reach. Reading the five-day limit as general "
        "would wrongly condemn an ordinary in-state patient-requested partial fill made after day five.",
        [{"type": "STATUTE", "name": "Massachusetts General Laws",
          "section": "M.G.L. c. 94C, s. 18(d3/4), read with s. 18(d) and s. 18(d1/2)", "url": GL18}],
        ["Applying the five-day initial limit to an ordinary in-state Schedule II partial fill.",
         "Forgetting that the remainder may be dispensed only by the pharmacy that made the initial "
         "partial fill.",
         "Counting the 30 days from the partial dispensing rather than from the issue date."],
        numeric=[{"fact": "Initial partial dispensing limit on the out-of-state pathways",
                  "value": 5, "unit": "days after the prescription issue date",
                  "conditions": "only where the prescription is filled pursuant to s. 18(d) or (d1/2)"},
                 {"fact": "Remaining portion deadline", "value": 30,
                  "unit": "days after the prescription issue date",
                  "conditions": "for a patient-requested partial fill under s. 18(d3/4)"}],
        related=["MA-CII-LESSER-QUANTITY", "MA-CII-REMAINDER-30D", "FED-CII-PARTIAL-PATIENT"],
    ),
    _rule(
        "FED-MEDGUIDE-PRESCRIBER-DIRECTION", 3, "Patient information",
        "Prescriber direction against a Medication Guide",
        "A patient's request overrides a prescriber's direction to withhold a Medication Guide",
        "If the licensed practitioner who prescribes a drug product subject to 21 CFR Part 208 "
        "determines that it is NOT IN A PARTICULAR PATIENT'S BEST INTEREST to receive a Medication "
        "Guide because of significant concerns about its effect, the practitioner MAY DIRECT that the "
        "Medication Guide not be provided to that patient. HOWEVER, the authorized dispenser SHALL "
        "PROVIDE A MEDICATION GUIDE TO ANY PATIENT WHO REQUESTS INFORMATION when the drug product is "
        "dispensed, REGARDLESS OF ANY SUCH DIRECTION by the licensed practitioner.",
        "A genuine conflict between a prescriber instruction and a patient request, resolved on the "
        "face of the regulation in the patient's favour.",
        [{"type": "FEDERAL_REGULATION", "name": "FDA Medication Guide exemptions and deferrals",
          "section": "21 CFR 208.26(b)", "url": CFR208_26}],
        ["Treating the prescriber's direction as binding on the pharmacist without exception.",
         "Reading the patient-request override as requiring a formal or written request.",
         "Assuming the override lets the dispenser ignore the direction even where the patient asks "
         "for nothing."],
        exceptions=["The practitioner's direction stands unless the patient requests information at "
                    "the time the product is dispensed."],
        related=["FED-MEDGUIDE", "FED-MEDGUIDE-RECIPIENT"],
        jurisdiction="FEDERAL",
    ),
    _rule(
        "FED-MEDGUIDE-RECIPIENT", 3, "Patient information", "Who receives the Medication Guide",
        "The Medication Guide goes to the patient or the patient's agent",
        "Each authorized dispenser of a prescription drug product for which a Medication Guide is "
        "required shall, WHEN THE PRODUCT IS DISPENSED TO A PATIENT OR TO A PATIENT'S AGENT, PROVIDE "
        "A MEDICATION GUIDE DIRECTLY TO EACH PATIENT OR TO THE PATIENT'S AGENT, unless an exemption "
        "applies under 21 CFR 208.26. The container or package label must itself instruct the "
        "authorized dispenser to provide a Medication Guide and state how it is provided.",
        "Delivery to an agent is expressly contemplated, so a pharmacy may not defer the duty until "
        "the patient appears in person.",
        [{"type": "FEDERAL_REGULATION", "name": "FDA Medication Guide distribution and dispensing",
          "section": "21 CFR 208.24(d) and (e)", "url": CFR208_24}],
        ["Holding the Medication Guide back because a friend or family member is collecting.",
         "Treating the duty as satisfied by making guides available in the waiting area rather than "
         "providing one directly.",
         "Confusing the dispenser's duty under (e) with the manufacturer's supply duty under (b)."],
        related=["FED-MEDGUIDE", "FED-MEDGUIDE-PRESCRIBER-DIRECTION"],
        jurisdiction="FEDERAL",
    ),
    _rule(
        "MA-PMP-INPATIENT-EXCLUSION", 3, "Prescription monitoring", "Scope of the reporting duty",
        "PMP reporting does not reach an inpatient medication order",
        "105 CMR 700.012 SHALL NOT APPLY to the dispensing PURSUANT TO A MEDICATION ORDER of a "
        "controlled substance TO AN INPATIENT IN A HOSPITAL. The reporting duty otherwise reaches "
        "every pharmacy registered with the Commissioner that dispenses a controlled substance "
        "pursuant to a prescription in Schedules II through V, or a controlled substance classified "
        "as an additional drug, and any out-of-state pharmacy delivering such a substance to a person "
        "in Massachusetts.",
        "Two facts must coincide for the exclusion: a medication order rather than a prescription, "
        "and an inpatient in a hospital. A discharge prescription is neither.",
        [_d("105 CMR 700.012(A)(1) and (A)(2)")],
        ["Extending the exclusion to a discharge prescription written for the same patient.",
         "Assuming an out-of-state pharmacy delivering into Massachusetts is outside the duty.",
         "Reading the exclusion as covering any hospital dispensing rather than inpatient "
         "medication orders."],
        exceptions=["Dispensing pursuant to a medication order to an inpatient in a hospital."],
        related=["MA-PMP-REPORTING"],
    ),
    _rule(
        "MA-PMP-ADDITIONAL-DRUG-DESIGNATION", 3, "Prescription monitoring",
        "Designation of an additional drug",
        "How a Schedule VI drug becomes reportable as an additional drug",
        "The Commissioner MAY DETERMINE that a drug is an 'additional drug' for the purposes of "
        "105 CMR 700.012 because it carries a BONA FIDE POTENTIAL FOR ABUSE, based on factors "
        "including a risk of addiction alone or with a Schedule II through IV drug, known "
        "recreational use, known regular diversion for misuse, or a known contribution to overdose or "
        "regular presence in the bloodstream of persons who have overdosed. UPON MAKING SUCH A "
        "DETERMINATION THE COMMISSIONER SHALL NOTIFY ALL DISPENSERS THAT THEY MUST BEGIN TO REPORT "
        "the dispensing of that additional drug pursuant to prescription as directed in "
        "105 CMR 700.012(A).",
        "The duty to report an additional drug arrives by the Commissioner's determination and "
        "notification, not by the drug's schedule and not by the pharmacy's own assessment.",
        [_d("105 CMR 700.012(C)(8)")],
        ["Assuming a Schedule VI drug is reportable only if it is rescheduled.",
         "Expecting the pharmacy to decide for itself whether a drug carries a potential for abuse.",
         "Overlooking that the reporting duty, once triggered, runs through 700.012(A) like any other."],
        related=["MA-PMP-REPORTING", "MA-PMP-INPATIENT-EXCLUSION"],
    ),
]

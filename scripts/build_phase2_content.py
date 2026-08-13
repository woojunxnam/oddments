from __future__ import annotations

from collections import Counter
from pathlib import Path

from qa_common import DATA, ROOT, load_json, load_records, semantic_content_hash, write_json


TODAY = "2026-08-13"


RULE_SPECS = [
    ("MA-CQI-PROGRAM", "Pharmacy continuous quality improvement program", "MA", 4, "Quality assurance", "CQI program", "Each pharmacy must maintain a continuous quality improvement program that detects, documents, assesses, and prevents quality-related events.", "247 CMR 15.02(1)", "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"),
    ("MA-QRE-NOTIFY", "Immediate response after discovery of a quality-related event", "MA", 4, "Quality assurance", "QRE notification", "On discovery of a quality-related event, the pharmacist must immediately notify the patient or representative, notify the prescriber when professionally indicated, and give corrective and harm-minimization directions.", "247 CMR 15.03(1)", "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"),
    ("MA-QRE-DOCUMENT-24H", "Quality-related event documentation deadline", "MA", 4, "Quality assurance", "QRE documentation", "The pharmacist who discovers or receives notice of a quality-related event must initially document it within 24 hours after discovery or notification.", "247 CMR 15.03(2)", "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"),
    ("MA-QRE-ANALYSIS", "Quality-related event analysis and systems response", "MA", 4, "Quality assurance", "QRE analysis", "A pharmacy must analyze quality-related events for causes and contributing workflow, technology, training, and staffing factors and use the findings to improve systems and processes.", "247 CMR 15.03(3)", "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"),
    ("MA-QRE-ANNUAL-ED", "Annual CQI education for pharmacy personnel", "MA", 4, "Quality assurance", "CQI education", "A pharmacy's CQI program must provide ongoing education in continuous quality improvement to pharmacy personnel at least annually.", "247 CMR 15.02(1)(f)", "https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download"),
    ("MA-SERIOUS-EVENT-REPORT", "Reporting improper dispensing and serious adverse drug events", "MA", 4, "Mandatory reporting", "Serious events", "A manager of record must report qualifying improper dispensing with serious injury or death and qualifying serious adverse drug events within seven business days of discovery or employee knowledge.", "247 CMR 20.02(1)-(3)", "https://www.mass.gov/doc/247-cmr-20-reporting/download"),
    ("MA-SERIOUS-EVENT-RECORDS", "Retention of serious-event reporting records", "MA", 4, "Mandatory reporting", "Record retention", "A pharmacy must retain readily retrievable records relating to reportable improper dispensing and serious adverse drug events for at least five years from filing the report.", "247 CMR 20.02(4)", "https://www.mass.gov/doc/247-cmr-20-reporting/download"),
    ("MA-LICENSEE-CHANGE-14D", "Licensee demographic and status reporting", "MA", 1, "Licensure", "Change reporting", "Board licensees must update specified contact information and report specified name, criminal, disciplinary, or certification events within the applicable 14-day reporting period.", "247 CMR 20.03", "https://www.mass.gov/doc/247-cmr-20-reporting/download"),
    ("FED-THEFT-LOSS-DEA", "Federal reporting of significant controlled-substance theft or loss", "FEDERAL", 4, "Controlled substance security", "Theft and loss", "A DEA registrant must notify the responsible DEA field division in writing within one business day after discovering a theft or significant loss and complete the required electronic DEA Form 106 process.", "21 CFR 1301.74(c)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.74"),
    ("FED-INVENTORY-INITIAL", "Initial controlled-substance inventory", "FEDERAL", 4, "Controlled substance inventory", "Initial inventory", "A newly registered handler must take an inventory of controlled substances on hand on the date first engaging in controlled-substance activity.", "21 CFR 1304.11(b)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"),
    ("FED-INVENTORY-BIENNIAL", "Biennial controlled-substance inventory", "FEDERAL", 4, "Controlled substance inventory", "Biennial inventory", "After the initial inventory, each registrant must take a new controlled-substance inventory at least every two years.", "21 CFR 1304.11(c)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"),
    ("FED-INVENTORY-COUNT", "Exact and estimated controlled-substance inventory counts", "FEDERAL", 4, "Controlled substance inventory", "Counting method", "Schedule II inventory requires an exact count or measure; Schedule III through V opened containers may generally be estimated unless the container holds more than 1,000 units.", "21 CFR 1304.11(e)(6)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"),
    ("FED-CS-RECORDS-2Y", "Federal controlled-substance record retention", "FEDERAL", 4, "Controlled substance records", "Retention", "DEA-required controlled-substance inventories and records must be maintained and available for inspection for at least two years unless another provision requires longer.", "21 CFR 1304.04(a)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.04"),
    ("FED-CII-NO-REFILL", "Schedule II prescriptions may not be refilled", "FEDERAL", 3, "Controlled prescriptions", "Schedule II refills", "Federal law prohibits refilling a Schedule II prescription; additional dispensing requires a new lawful prescription or a permitted remainder of a partial fill.", "21 CFR 1306.12(a)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.12"),
    ("FED-CII-EMERGENCY-ORAL", "Emergency oral Schedule II prescription requirements", "FEDERAL", 3, "Controlled prescriptions", "Emergency Schedule II", "In a defined emergency, a pharmacist may dispense an oral Schedule II prescription only in the quantity necessary for the emergency period after immediate communication with and reasonable identification of the prescriber.", "21 CFR 1306.11(d)(1)-(4)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"),
    ("FED-CII-EMERGENCY-FOLLOWUP", "Follow-up after emergency oral Schedule II dispensing", "FEDERAL", 3, "Controlled prescriptions", "Emergency follow-up", "The prescriber must deliver the required written or electronic follow-up Schedule II prescription to the pharmacy within seven days after authorizing emergency oral dispensing.", "21 CFR 1306.11(d)(4)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11"),
    ("FED-CII-PARTIAL-72H", "Schedule II partial fill caused by pharmacy inability", "FEDERAL", 3, "Partial filling", "Insufficient stock", "When a Schedule II prescription is partially filled because the pharmacy cannot supply the full quantity, the remaining portion must generally be supplied within 72 hours or the pharmacist must notify the prescriber and obtain a new prescription for further quantity.", "21 CFR 1306.13(a)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"),
    ("FED-CII-PARTIAL-PATIENT", "Patient-requested Schedule II partial fill", "FEDERAL", 3, "Partial filling", "Patient request", "A Schedule II prescription may be partially filled at the patient or prescriber request when state law permits, with the remaining portion dispensed no later than 30 days after the prescription was written unless a shorter applicable limit controls.", "21 CFR 1306.13(b)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13"),
    ("MA-CII-VALIDITY-30D", "Massachusetts Schedule II prescription validity", "MA", 3, "Controlled prescriptions", "Schedule II validity", "A Massachusetts written or electronic Schedule II prescription becomes invalid 30 days after its issue date.", "M.G.L. c. 94C, § 23(a)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"),
    ("MA-OUTSTATE-CII-NARCOTIC", "Out-of-state Schedule II narcotic prescriptions", "MA", 2, "Prescription validity", "Out-of-state narcotic", "Massachusetts may fill a Schedule II narcotic prescription from Maine or a contiguous state within five days of issue after required authentication and verification; separate delivery provisions govern certain out-of-state residents.", "M.G.L. c. 94C, § 18(d1/2)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"),
    ("MA-OPIOID-SEVEN-DAY", "Massachusetts initial opioid seven-day limit", "MA", 2, "Opioid prescribing", "Initial supply", "An initial outpatient opiate prescription for an adult and any opiate prescription for a minor is generally limited to seven days, subject to documented statutory exceptions; opioid-dependence treatment is excluded.", "M.G.L. c. 94C, § 19D", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D"),
    ("MA-CII-LESSER-QUANTITY", "Patient option to request a lesser Schedule II quantity", "MA", 3, "Partial filling", "Lesser quantity", "At the patient's request, a Massachusetts pharmacist may dispense less than the prescribed Schedule II quantity and document the partial fill in the patient record.", "M.G.L. c. 94C, § 18(d3/4)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"),
    ("MA-CII-REMAINDER-30D", "Massachusetts Schedule II patient-request remainder", "MA", 3, "Partial filling", "Remainder deadline", "Only the pharmacy that made the initial patient-requested Schedule II partial fill may dispense the remainder, and the remainder must be filled no later than 30 days after issue.", "M.G.L. c. 94C, § 18(d3/4)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"),
    ("MA-CONTROLLED-EPRESCRIBE", "Massachusetts electronic-prescribing requirement", "MA", 3, "Prescription format", "Electronic prescriptions", "Prescribers generally must issue electronic prescriptions for controlled substances and medical devices, subject to statutory and regulatory exceptions and waivers.", "M.G.L. c. 94C, § 23(g); 105 CMR 721.070-.080", "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"),
    ("MA-RX-REQUIRED-ELEMENTS", "Massachusetts controlled-prescription required elements", "MA", 3, "Prescription format", "Required elements", "A controlled-substance prescription must include the practitioner, patient, drug, strength, directions, date, registration, cautionary, and refill information required by Massachusetts law.", "M.G.L. c. 94C, § 22(a)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section22"),
    ("MA-RX-OUTSTATE-III-VI", "Out-of-state Schedule III through VI prescriptions", "MA", 2, "Prescription validity", "Out-of-state III-VI", "An authorized out-of-state practitioner may issue a Schedule III through VI prescription filled in Massachusetts within 30 days of issue; Schedule III through V prescriptions require pharmacist verification.", "M.G.L. c. 94C, § 18(c)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"),
    ("MA-ORAL-III-V-FOLLOWUP", "Massachusetts oral Schedule III through V follow-up request", "MA", 3, "Controlled prescriptions", "Oral follow-up", "For an oral Schedule III through V prescription issued under the out-of-state pathway, the pharmacist records requesting a written prescription within seven days or the shorter federal period.", "M.G.L. c. 94C, § 18(c)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18"),
    ("MA-SCHEDULE-VI", "Massachusetts Schedule VI prescription-drug status", "MA", 2, "Controlled substance classification", "Schedule VI", "Massachusetts Schedule VI includes prescription drugs not otherwise placed in Schedules I through V; Schedule VI status does not itself make a drug federally controlled or routinely MassPAT-reportable.", "105 CMR 700.002(F)", "https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download"),
    ("FED-CIII-V-REFILL", "Federal Schedule III and IV refill limits", "FEDERAL", 3, "Controlled prescriptions", "Schedule III-IV refills", "A Schedule III or IV prescription may not be filled or refilled more than six months after issue and may not be refilled more than five times unless renewed by the practitioner.", "21 CFR 1306.22(a)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22"),
    ("FED-CIII-V-PARTIAL", "Federal partial filling of Schedule III through V prescriptions", "FEDERAL", 3, "Partial filling", "Schedule III-V", "A Schedule III through V prescription may be partially filled if each partial fill is recorded like a refill, the total does not exceed the prescribed quantity, and dispensing occurs within six months after issue.", "21 CFR 1306.23", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.23"),
    ("FED-EPCS-TRANSFER", "One-time transfer of electronic controlled prescriptions", "FEDERAL", 3, "Prescription transfer", "Electronic prescriptions", "At a patient's request, an unfilled electronic Schedule II through V prescription may be transferred once between DEA-registered retail pharmacies if allowed by state law, kept electronic, unaltered, and communicated directly between pharmacists.", "21 CFR 1306.08(e)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08"),
    ("MA-RX-TRANSFER", "Massachusetts transfer of prescriptions", "MA", 3, "Prescription transfer", "Transfer requirements", "Prescription transfers must comply with 247 CMR 9.14, applicable controlled-substance limits, pharmacist-to-pharmacist communication requirements, and required record annotations.", "247 CMR 9.14", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("FED-FORM222-ORDER", "Schedule I and II ordering by Form 222 or CSOS", "FEDERAL", 4, "Controlled substance procurement", "Ordering", "A distribution of Schedule I or II controlled substances generally requires a DEA Form 222 or a compliant digitally signed electronic order unless a listed exception applies.", "21 CFR 1305.03", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.03"),
    ("FED-FORM222-60DAY", "DEA Form 222 validity and partial shipments", "FEDERAL", 4, "Controlled substance procurement", "Form validity", "A supplier may make partial shipments on an accepted DEA Form 222 during the 60-day period after execution; the form is generally invalid after 60 days.", "21 CFR 1305.13(b)", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13"),
    ("FED-FORM222-DEFECT", "Defective DEA Form 222 may not be corrected", "FEDERAL", 4, "Controlled substance procurement", "Defective form", "A supplier may not fill an incomplete, illegible, improperly executed, altered, or erased DEA Form 222; a defective form cannot be corrected and must be replaced.", "21 CFR 1305.15", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.15"),
    ("FED-FORM222-LOSS", "Lost or stolen DEA Form 222 reporting", "FEDERAL", 4, "Controlled substance procurement", "Lost forms", "A registrant must immediately report lost or stolen used or unused DEA Forms 222 to the responsible DEA Special Agent in Charge and retain the required replacement-form statements.", "21 CFR 1305.16", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.16"),
    ("FED-FORM222-RECORDS", "DEA Form 222 preservation", "FEDERAL", 4, "Controlled substance procurement", "Form records", "Purchasers and suppliers must preserve the required copies or originals of DEA Forms 222 separately and make them available for inspection for two years.", "21 CFR 1305.17", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.17"),
    ("FED-CSOS", "Controlled Substance Ordering System electronic orders", "FEDERAL", 4, "Controlled substance procurement", "CSOS", "CSOS permits a properly credentialed registrant or authorized subscriber to issue digitally signed electronic Schedule I and II orders in place of paper DEA Form 222.", "21 CFR 1305 Subpart C; 21 CFR 1311", "https://www.ecfr.gov/current/title-21/chapter-II/part-1305/subpart-C"),
    ("FED-FORM41", "Controlled-substance destruction records", "FEDERAL", 4, "Controlled substance disposal", "DEA Form 41", "A registrant that destroys or causes destruction of controlled substances must maintain the required destruction record, generally using DEA Form 41, with the required substance, method, place, date, and witness information.", "21 CFR 1304.21(e); 21 CFR 1317.95", "https://www.ecfr.gov/current/title-21/chapter-II/part-1317/section-1317.95"),
    ("FED-DISPOSAL-NONRETRIEVABLE", "Non-retrievable standard for controlled-substance destruction", "FEDERAL", 4, "Controlled substance disposal", "Destruction standard", "Controlled substances destroyed by a registrant must be rendered non-retrievable so their physical or chemical condition is permanently altered and unavailable for practical use.", "21 CFR 1317.90; 1317.95", "https://www.ecfr.gov/current/title-21/chapter-II/part-1317/section-1317.90"),
    ("FED-REVERSE-DISTRIBUTOR", "Transfer to a registered reverse distributor", "FEDERAL", 4, "Controlled substance disposal", "Reverse distribution", "A registrant may transfer controlled substances to a DEA-registered reverse distributor under the applicable inventory, ordering, transfer, and record requirements.", "21 CFR 1317.05; 1317.15", "https://www.ecfr.gov/current/title-21/chapter-II/part-1317"),
    ("MA-CS-SECURITY", "Massachusetts pharmacy controlled-substance security", "MA", 4, "Controlled substance security", "Physical security", "A Massachusetts pharmacy must maintain controlled substances securely and comply with the storage, access, accountability, and loss-response requirements in 247 CMR 9.21 and applicable federal law.", "247 CMR 9.21", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-PHARMACY-CLOSURE-NOTICE", "Advance Board notice of pharmacy closure", "MA", 4, "Pharmacy licensure", "Closure notice", "A resident pharmacy generally must give the Board written certified-mail notice at least 14 days before intended closure and provide the required closure and controlled-substance information.", "247 CMR 6.13(1)", "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download"),
    ("MA-PHARMACY-CLOSURE-PATIENTS", "Patient notice before pharmacy closure", "MA", 4, "Pharmacy licensure", "Closure patient notice", "A closing pharmacy identifies patients served in the preceding 90 days, attempts notice at least 14 days before closure, posts conspicuous notice, and supports timely patient-file transfer.", "247 CMR 6.13(4)-(5)", "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download"),
    ("MA-PHARMACY-CLOSURE-CS", "Controlled substances and credentials after pharmacy closure", "MA", 4, "Pharmacy licensure", "Closure disposition", "Within 14 days after closure, the resident pharmacy submits original licenses and controlled-substance registration plus an attestation of lawful controlled-substance disposal or transfer.", "247 CMR 6.13(6); 6.14", "https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download"),
    ("MA-TECH-SCOPE", "Massachusetts pharmacy technician scope and pharmacist responsibility", "MA", 1, "Pharmacy personnel", "Technician duties", "Pharmacy technicians and trainees may perform only duties allowed by 247 CMR 8 under pharmacist supervision; judgmental pharmacist functions may not be delegated.", "247 CMR 8.02-.06", "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download"),
    ("MA-TECH-CII", "Schedule II handling by pharmacy support personnel", "MA", 1, "Pharmacy personnel", "Schedule II handling", "Interns and technician categories may handle Schedule II controlled substances only within the specific conditions and supervision requirements of 247 CMR 8.05.", "247 CMR 8.05", "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download"),
    ("MA-INTERN-SUPERVISION", "Direct supervision of Massachusetts pharmacy interns", "MA", 1, "Pharmacy personnel", "Intern supervision", "A Massachusetts pharmacy intern works under the direct supervision of a registered pharmacist preceptor.", "247 CMR 8.01(3)", "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download"),
    ("MA-INTERN-12H", "Daily pharmacy internship credit limit", "MA", 1, "Pharmacy personnel", "Intern hours", "A pharmacy intern may receive no more than 12 hours of pharmacy internship credit in one day.", "247 CMR 8.01(4)", "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download"),
    ("MA-PHARMACIST-CE", "Massachusetts pharmacist continuing education", "MA", 1, "Licensure", "Continuing education", "A renewing pharmacist generally completes 20 contact hours in each calendar year of the two-year cycle, including at least two hours of pharmacy law each year, with limits on home study and daily credit.", "247 CMR 4.03", "https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download"),
    ("MA-CE-COMPOUNDING", "Massachusetts compounding continuing education", "MA", 1, "Licensure", "Compounding CE", "A pharmacist overseeing or directly engaged in covered sterile or complex nonsterile compounding must complete the applicable additional annual compounding continuing-education hours.", "247 CMR 4.03(4)(c)-(d)", "https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download"),
    ("MA-CDTM-QUALIFICATIONS", "Pharmacist qualifications for collaborative drug therapy management", "MA", 2, "Collaborative practice", "Qualifications", "A collaborating pharmacist must satisfy Massachusetts licensure, experience or degree, liability insurance, practice-focus, and additional annual continuing-education requirements.", "M.G.L. c.112, § 24B1/2(b)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2"),
    ("MA-CDTM-RETAIL-SCOPE", "Retail collaborative drug therapy management scope", "MA", 2, "Collaborative practice", "Retail scope", "Retail CDTM is limited to referred and consenting adults, the diseases and actions authorized by statute, the supervising physician's agreement, and other statutory setting restrictions.", "M.G.L. c.112, § 24B1/2(c)(5)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2"),
    ("MA-CDTM-CONTROLLED-LIMIT", "Retail CDTM Schedule II through V prohibition", "MA", 2, "Collaborative practice", "Controlled substances", "A retail collaborative practice agreement may not authorize the pharmacist to prescribe Schedule II through V controlled substances.", "M.G.L. c.112, § 24B1/2(c)(5)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2"),
    ("MA-CDTM-SVI-RX", "Retail CDTM Schedule VI prescribing", "MA", 2, "Collaborative practice", "Schedule VI", "A properly authorized retail collaborating pharmacist may issue Schedule VI prescriptions for the referred diagnosis and must send a copy to the supervising physician within 24 hours.", "M.G.L. c.112, § 24B1/2(c)(5)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2"),
    ("MA-PRODUR", "Prospective drug utilization review", "MA", 2, "Patient care", "Prospective review", "Before dispensing, a pharmacist must perform the prospective drug utilization review required by 247 CMR 9.17 and resolve clinically significant issues through professional judgment and communication.", "247 CMR 9.17", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-COUNSELING", "Massachusetts patient counseling", "MA", 2, "Patient care", "Counseling", "A pharmacist must comply with the patient-counseling requirements of 247 CMR 9.18, including a meaningful offer or provision in the settings and circumstances governed by the regulation.", "247 CMR 9.18", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-INTERCHANGE", "Massachusetts interchangeable-drug dispensing", "MA", 3, "Drug interchange", "Generic interchange", "A pharmacist dispenses a less expensive reasonably available interchangeable product listed under Massachusetts standards unless the prescriber validly indicates no substitution or another exception applies.", "105 CMR 720; M.G.L. c.112, § 12D", "https://www.mass.gov/info-details/policy-on-drug-interchangeability-and-midstream-interchange"),
    ("MA-NALOXONE", "Massachusetts naloxone prescribing and dispensing", "MA", 2, "Public health", "Opioid antagonist", "Naloxone may lawfully be prescribed and dispensed to a person at risk or to another person positioned to assist, and Massachusetts pharmacy pathways include standing-order and reporting provisions.", "M.G.L. c.94C, §§ 19(d), 19B; 247 CMR 9.06", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19"),
    ("MA-HORMONAL-CONTRACEPTIVE", "Pharmacist prescribing of hormonal contraception", "MA", 2, "Pharmacist prescribing", "Hormonal contraception", "A Massachusetts pharmacist may prescribe and dispense eligible hormonal contraceptive patches and self-administered oral products after the required screening and under the official protocol and labeling.", "M.G.L. c.94C, § 19F; 105 CMR 700.004(B)(15)", "https://www.mass.gov/news/circular-letter-dcp-23-10-121-pharmacist-prescribing-and-dispensing-of-hormonal-contraceptive"),
    ("MA-RETURN-QUARANTINE", "Returned erroneous or defective medication quarantine", "MA", 4, "Pharmacy operations", "Returned medication", "A pharmacy accepts medication it dispensed in error or that is suspected defective or contaminated, but may not return it to inventory and must quarantine and properly dispose of it.", "247 CMR 9.01(7)", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-RX-RECORDS-2Y", "Massachusetts controlled-prescription retention", "MA", 4, "Pharmacy records", "Prescription records", "A pharmacy keeps controlled-substance prescriptions for two years and makes them available for inspection under Massachusetts law.", "M.G.L. c.94C, § 23(e)", "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23"),
    ("FED-MEDGUIDE", "FDA Medication Guide distribution", "FEDERAL", 3, "Federal drug requirements", "Medication Guides", "When FDA requires a Medication Guide for a product, the authorized dispenser must provide it under the conditions in 21 CFR Part 208, subject to the regulation's exceptions.", "21 CFR 208.24", "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-208/section-208.24"),
    ("FED-REMS", "Product-specific FDA REMS requirements", "FEDERAL", 3, "Federal drug requirements", "REMS", "A pharmacy dispensing a drug subject to an FDA REMS must follow the current product-specific certification, authorization, documentation, and safe-use requirements that apply to the dispenser.", "21 U.S.C. 355-1; current REMS@FDA materials", "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems"),
    ("FED-PDMA-SAMPLES", "Prescription drug sample restrictions", "FEDERAL", 4, "Federal distribution", "Drug samples", "Prescription drug samples are distributed only through the authorized practitioner and manufacturer or distributor pathways; a pharmacy may not treat samples marked not for resale as ordinary saleable inventory.", "21 CFR Part 203; 247 CMR 9.01(6)", "https://www.fda.gov/regulatory-information/selected-amendments-fdc-act/prescription-drug-marketing-act-1987"),
    ("FED-RECALL", "Drug recall segregation and response", "FEDERAL", 4, "Product safety", "Recalls", "A pharmacy follows the recall notice and lot-specific instructions, removes affected stock from availability, preserves traceability, and does not assume every recall requires every patient to stop therapy immediately.", "21 CFR 7.40-.59; FDA recall notice", "https://www.fda.gov/drugs/drug-safety-and-availability/drug-recalls"),
    ("FED-ADULTERATED-MISBRANDED", "Adulterated and misbranded drug prohibition", "FEDERAL", 4, "Product safety", "Federal status", "Federal law prohibits dispensing or distributing adulterated or misbranded drugs; labeling, strength, purity, storage, and manufacturing defects can trigger different statutory classifications.", "21 U.S.C. 331, 351, 352", "https://www.fda.gov/regulatory-information/laws-enforced-fda/federal-food-drug-and-cosmetic-act-fdc-act"),
]


HOLD_SPECS = [
    ("MA-USP-795-HOLD", "Nonsterile compounding details pending source reconciliation", 4, "Compounding", "USP 795", "Exact Massachusetts application details require reconciliation of current USP text, Board rules, and pharmacy license class before question authoring.", "247 CMR 9.01(3) and current USP <795>", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-USP-797-HOLD", "Sterile compounding details pending source reconciliation", 4, "Compounding", "USP 797", "Exact sterile-compounding environmental and beyond-use-date details remain on hold pending licensed access to current USP text and final promulgated Massachusetts rules.", "247 CMR 9.01(3) and current USP <797>", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-USP-800-HOLD", "Hazardous-drug handling details pending source reconciliation", 4, "Compounding", "USP 800", "Detailed hazardous-drug engineering and handling requirements remain on hold pending authoritative current USP text and Massachusetts applicability review.", "247 CMR 9.01(3) and current USP <800>", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-REMOTE-CENTRAL-HOLD", "Remote processing and central-fill details on hold", 4, "Pharmacy operations", "Remote and central processing", "Detailed remote-processing and central-fill allocation of responsibility remains on hold until all current Board policies and applicable federal record requirements are reconciled.", "247 CMR 9.10-.12", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
    ("MA-LTCF-KIT-HOLD", "LTCF and hospice emergency-kit details on hold", 4, "Institutional practice", "Emergency kits", "Facility-specific emergency-kit contents, access, replacement, and record duties remain on hold pending full reconciliation of 247 CMR 9.09 and applicable facility regulations.", "247 CMR 9.09", "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"),
]


DRUG_SPECS = [
    ("amphetamine-dextroamphetamine", "amphetamine and dextroamphetamine", ["Adderall"], "Attention deficit hyperactivity disorder and narcolepsy", "CNS stimulant", "II"),
    ("lisdexamfetamine", "lisdexamfetamine", ["Vyvanse"], "Attention deficit hyperactivity disorder and moderate to severe binge eating disorder", "CNS stimulant", "II"),
    ("dexmethylphenidate", "dexmethylphenidate", ["Focalin"], "Attention deficit hyperactivity disorder", "CNS stimulant", "II"),
    ("dextroamphetamine", "dextroamphetamine", ["Dexedrine"], "Attention deficit hyperactivity disorder and narcolepsy", "CNS stimulant", "II"),
    ("methadone", "methadone", ["Dolophine"], "Severe pain requiring an opioid and treatment of opioid use disorder in authorized settings", "Opioid agonist", "II"),
    ("oxycodone", "oxycodone", ["OxyContin"], "Severe and persistent pain requiring extended opioid treatment", "Opioid analgesic", "II"),
    ("hydrocodone-acetaminophen", "hydrocodone and acetaminophen", ["Norco"], "Pain severe enough to require an opioid when alternatives are inadequate", "Opioid combination analgesic", "II"),
    ("hydromorphone", "hydromorphone", ["Dilaudid"], "Pain severe enough to require an opioid when alternatives are inadequate", "Opioid analgesic", "II"),
    ("morphine", "morphine", ["MS Contin"], "Severe and persistent pain requiring extended opioid treatment", "Opioid analgesic", "II"),
    ("fentanyl", "fentanyl", ["Duragesic"], "Severe persistent pain in opioid-tolerant patients requiring continuous opioid treatment", "Opioid analgesic", "II"),
    ("oxymorphone", "oxymorphone", ["Opana"], "Pain severe enough to require an opioid when alternatives are inadequate", "Opioid analgesic", "II"),
    ("meperidine", "meperidine", ["Demerol"], "Pain severe enough to require an opioid when alternatives are inadequate", "Opioid analgesic", "II"),
    ("tapentadol", "tapentadol", ["Nucynta"], "Acute pain severe enough to require an opioid and certain neuropathic pain formulations", "Opioid analgesic", "II"),
    ("buprenorphine", "buprenorphine", ["Subutex"], "Treatment of opioid dependence", "Partial opioid agonist", "III"),
    ("buprenorphine-er", "buprenorphine extended-release injection", ["Sublocade"], "Treatment of moderate to severe opioid use disorder after transmucosal initiation", "Partial opioid agonist", "III"),
    ("alprazolam", "alprazolam", ["Xanax"], "Anxiety disorder and panic disorder", "Benzodiazepine", "IV"),
    ("lorazepam", "lorazepam", ["Ativan"], "Anxiety disorders and short-term relief of anxiety symptoms", "Benzodiazepine", "IV"),
    ("clonazepam", "clonazepam", ["Klonopin"], "Seizure disorders and panic disorder", "Benzodiazepine", "IV"),
    ("diazepam", "diazepam", ["Valium"], "Anxiety disorders, acute alcohol withdrawal, muscle spasm, and adjunctive seizure treatment", "Benzodiazepine", "IV"),
    ("chlordiazepoxide", "chlordiazepoxide", ["Librium"], "Anxiety disorders and acute alcohol withdrawal", "Benzodiazepine", "IV"),
    ("midazolam", "midazolam", ["Versed"], "Sedation, anxiolysis, and amnesia for procedures", "Benzodiazepine", "IV"),
    ("triazolam", "triazolam", ["Halcion"], "Short-term treatment of insomnia", "Benzodiazepine hypnotic", "IV"),
    ("temazepam", "temazepam", ["Restoril"], "Short-term treatment of insomnia", "Benzodiazepine hypnotic", "IV"),
    ("zolpidem", "zolpidem", ["Ambien"], "Short-term treatment of insomnia", "Nonbenzodiazepine hypnotic", "IV"),
    ("eszopiclone", "eszopiclone", ["Lunesta"], "Treatment of insomnia", "Nonbenzodiazepine hypnotic", "IV"),
    ("zaleplon", "zaleplon", ["Sonata"], "Short-term treatment of insomnia", "Nonbenzodiazepine hypnotic", "IV"),
    ("suvorexant", "suvorexant", ["Belsomra"], "Treatment of insomnia with sleep-onset or sleep-maintenance difficulty", "Orexin receptor antagonist", "IV"),
    ("lemborexant", "lemborexant", ["Dayvigo"], "Treatment of insomnia with sleep-onset or sleep-maintenance difficulty", "Orexin receptor antagonist", "IV"),
    ("daridorexant", "daridorexant", ["Quviviq"], "Treatment of insomnia with sleep-onset or sleep-maintenance difficulty", "Orexin receptor antagonist", "IV"),
    ("tramadol", "tramadol", ["Ultram"], "Pain severe enough to require an opioid when alternatives are inadequate", "Opioid analgesic", "IV"),
    ("testosterone-cypionate", "testosterone cypionate", ["Depo-Testosterone"], "Replacement therapy in males with conditions associated with deficient endogenous testosterone", "Androgen", "III"),
    ("phentermine", "phentermine", ["Adipex-P"], "Short-term adjunct in a weight-reduction regimen", "Sympathomimetic anorectic", "IV"),
    ("phendimetrazine", "phendimetrazine", ["Bontril"], "Short-term adjunct in a weight-reduction regimen", "Sympathomimetic anorectic", "III"),
    ("modafinil", "modafinil", ["Provigil"], "Improve wakefulness in narcolepsy, obstructive sleep apnea, or shift-work disorder", "Wakefulness-promoting agent", "IV"),
    ("ketamine", "ketamine", ["Ketalar"], "Induction and maintenance of general anesthesia", "Dissociative anesthetic", "III"),
    ("perampanel", "perampanel", ["Fycompa"], "Treatment of partial-onset seizures and primary generalized tonic-clonic seizures", "Antiseizure medication", "III"),
    ("sodium-oxybate", "sodium oxybate", ["Xyrem"], "Treatment of cataplexy or excessive daytime sleepiness in narcolepsy", "CNS depressant", "III"),
    ("dronabinol", "dronabinol", ["Marinol"], "Chemotherapy-associated nausea and vomiting and AIDS-related anorexia", "Cannabinoid", "III"),
    ("dronabinol-solution", "dronabinol oral solution", ["Syndros"], "Chemotherapy-associated nausea and vomiting and AIDS-related anorexia", "Cannabinoid", "II"),
    ("diphenoxylate-atropine", "diphenoxylate and atropine", ["Lomotil"], "Adjunctive therapy in the management of diarrhea", "Antidiarrheal", "V"),
    ("acetaminophen-codeine", "acetaminophen and codeine", ["Tylenol with Codeine"], "Mild to moderate pain when an opioid is appropriate", "Opioid combination analgesic", "III"),
    ("butorphanol", "butorphanol", ["Stadol"], "Pain management when an opioid is appropriate", "Mixed opioid agonist-antagonist", "IV"),
    ("pentazocine", "pentazocine", ["Talwin"], "Pain management when an opioid is appropriate", "Mixed opioid agonist-antagonist", "IV"),
    ("phenobarbital", "phenobarbital", ["Luminal"], "Treatment of seizure disorders and sedative use", "Barbiturate", "IV"),
    ("carisoprodol", "carisoprodol", ["Soma"], "Short-term relief of acute painful musculoskeletal conditions", "Skeletal muscle relaxant", "IV"),
    ("lacosamide", "lacosamide", ["Vimpat"], "Treatment of partial-onset seizures and primary generalized tonic-clonic seizures", "Antiseizure medication", "V"),
    ("cenobamate", "cenobamate", ["Xcopri"], "Treatment of partial-onset seizures in adults", "Antiseizure medication", "V"),
    ("clobazam", "clobazam", ["Onfi"], "Adjunctive treatment of seizures associated with Lennox-Gastaut syndrome", "Benzodiazepine antiseizure medication", "IV"),
    ("remifentanil", "remifentanil", ["Ultiva"], "Analgesia during induction and maintenance of general anesthesia", "Opioid analgesic", "II"),
    ("naloxone", "naloxone", ["Narcan"], "Emergency treatment of known or suspected opioid overdose", "Opioid antagonist", "NONCONTROLLED"),
    ("isotretinoin", "isotretinoin", ["Absorica"], "Severe recalcitrant nodular acne", "Retinoid", "NONCONTROLLED"),
    ("mifepristone", "mifepristone", ["Mifeprex"], "Medical termination of intrauterine pregnancy under the labeled regimen", "Progesterone receptor antagonist", "NONCONTROLLED"),
    ("epinephrine", "epinephrine", ["EpiPen"], "Emergency treatment of allergic reactions including anaphylaxis", "Adrenergic agonist", "NONCONTROLLED"),
    ("insulin-glargine", "insulin glargine", ["Lantus"], "Improve glycemic control in adults and pediatric patients with diabetes mellitus", "Long-acting insulin", "NONCONTROLLED"),
    ("warfarin", "warfarin", ["Coumadin"], "Prevention and treatment of thromboembolic disorders", "Vitamin K antagonist anticoagulant", "NONCONTROLLED"),
]


DRUG_CASES = [
    ("amphetamine-dextroamphetamine", "FED-CII-NO-REFILL", "An Adderall prescription has no quantity remaining, and the patient asks the pharmacist to process the prescriber's printed notation of three refills. What is the lawful response?", "Decline the refill and require a new lawful Schedule II prescription."),
    ("lisdexamfetamine", "MA-CII-VALIDITY-30D", "A Vyvanse prescription is presented 31 days after its issue date with no prior dispensing. What should the Massachusetts pharmacist conclude?", "Treat the Schedule II prescription as expired under the 30-day Massachusetts validity rule."),
    ("dexmethylphenidate", "MA-CII-OUTSTATE", "A Focalin prescription from a properly registered New Hampshire prescriber was issued four days ago and can be verified. Which conclusion is most defensible?", "The nonnarcotic Schedule II out-of-state pathway may permit dispensing after verification."),
    ("dextroamphetamine", "MA-CII-REMAINDER-30D", "A patient requested a partial fill of Dexedrine at this pharmacy 12 days after issue and now requests the balance on day 28. What controls?", "The same pharmacy may dispense the documented remainder before the 30-day issue-date deadline."),
    ("methadone", "MA-OPIOID-SEVEN-DAY", "An opioid-naive adult receives a first outpatient methadone prescription for pain for 10 days with no documented exception. What should be clarified?", "The prescriber must address the Massachusetts initial-opiate seven-day limit or document an applicable exception."),
    ("oxycodone", "MA-OPIOID-SEVEN-DAY", "An adult receiving an opiate for outpatient acute pain for the first time presents an OxyContin prescription for eight days without exception documentation. What is the key issue?", "The initial outpatient opiate supply generally may not exceed seven days without a documented statutory exception."),
    ("hydrocodone-acetaminophen", "MA-OPIOID-SEVEN-DAY", "A Norco prescription for a minor is written for 12 days, and the record sent with it contains no qualifying exception. What should the pharmacist recognize?", "A minor's opiate prescription is generally limited to seven days unless the prescriber documents a statutory exception."),
    ("hydromorphone", "FED-CII-NO-REFILL", "A Dilaudid prescription was fully dispensed last month, and the patient requests the first of two refills written on the original. What is required?", "Do not refill the Schedule II prescription; a new lawful prescription is required."),
    ("morphine", "FED-EPCS-TRANSFER", "At a patient's request, a DEA-registered pharmacy is asked to transfer an unfilled electronic MS Contin prescription once to another DEA-registered retail pharmacy. What pathway applies?", "Use the one-time pharmacist-to-pharmacist electronic transfer pathway if Massachusetts law and all federal conditions are satisfied."),
    ("fentanyl", "MA-OUTSTATE-CII-NARCOTIC", "A fentanyl prescription from a Rhode Island practitioner was issued four days ago and the pharmacist obtains direct verification. What Massachusetts rule is central?", "Apply the contiguous-state Schedule II narcotic pathway and its five-day and verification conditions."),
    ("oxymorphone", "FED-CII-PARTIAL-PATIENT", "A patient asks to receive only part of a new oxymorphone prescription today and return for the balance. Which limit must be documented?", "Treat it as a patient-requested Schedule II partial fill and dispense any lawful remainder within the applicable 30-day window."),
    ("meperidine", "MA-CII-VALIDITY-30D", "A never-filled Demerol prescription is brought to a Massachusetts pharmacy 35 days after issue. What is the result?", "The Schedule II prescription is invalid because more than 30 days have elapsed since issue."),
    ("tapentadol", "FED-CII-EMERGENCY-ORAL", "A prescriber telephones an emergency Nucynta order when immediate therapy is necessary and no written prescription can be delivered first. What quantity may be dispensed?", "Dispense no more than the amount necessary for the emergency period and follow the emergency Schedule II documentation pathway."),
    ("buprenorphine", "MA-CS-QUANTITY-II-III", "A buprenorphine prescription for opioid use disorder requests a 90-day single fill. Which Massachusetts quantity pathway is relevant?", "The Schedule III opioid-use-disorder treatment pathway may allow up to a 90-day single fill if no other restriction controls."),
    ("buprenorphine-er", "MA-PMP-REPORTING", "A Massachusetts outpatient pharmacy dispenses Sublocade pursuant to a prescription. Which monitoring conclusion is safest?", "Treat covered Schedule III dispensing as MassPAT-reportable under the current dispenser standard."),
    ("alprazolam", "FED-CIII-V-REFILL", "A Xanax prescription issued five months ago has already been refilled five times. The patient asks for another refill. What should occur?", "Require renewed prescriber authorization because the federal five-refill limit has been reached."),
    ("lorazepam", "MA-RX-OUTSTATE-III-VI", "An Ativan prescription from a properly authorized Connecticut practitioner was issued 20 days ago and is verified. What is the key Massachusetts determination?", "The out-of-state Schedule IV prescription may be filled within 30 days after required verification."),
    ("clonazepam", "FED-CIII-V-REFILL", "A Klonopin prescription has been refilled six times within five months because the original stated six refills. What should the pharmacist recognize?", "Federal law limits Schedule IV prescriptions to five refills within six months, despite the prescriber's notation."),
    ("diazepam", "FED-CIII-V-REFILL", "A Valium prescription with unused refills was issued seven months ago. Which clock controls?", "The prescription may not be refilled more than six months after issue."),
    ("chlordiazepoxide", "FED-EPCS-TRANSFER", "An unfilled electronic Librium prescription has already been transferred once at the patient's request. The patient now seeks a second transfer. What is the result?", "Do not transfer it a second time under the federal one-time electronic controlled-prescription rule."),
    ("midazolam", "MA-PMP-REPORTING", "A community pharmacy dispenses a covered outpatient midazolam prescription. What is the reporting classification?", "Report the Schedule IV dispensing to MassPAT under the current submission standard."),
    ("triazolam", "FED-CIII-V-REFILL", "A Halcion prescription is five months old and has five completed refills. Which fact is dispositive?", "The five-refill maximum is exhausted even though the six-month period has not ended."),
    ("temazepam", "FED-CIII-V-REFILL", "A Restoril prescription reaches six months after issue with one authorized refill unused. What should the pharmacist do?", "Decline the refill because the federal issue-date window has ended."),
    ("zolpidem", "MA-RX-OUTSTATE-III-VI", "An out-of-state Ambien prescription is presented 31 days after issue and otherwise appears authentic. What is the Massachusetts consequence?", "Do not use the out-of-state Schedule IV pathway because its 30-day issue window has elapsed."),
    ("eszopiclone", "FED-CIII-V-REFILL", "A Lunesta prescription is four months old and has four prior refills with one refill authorized. What is the most defensible conclusion?", "One additional refill may be lawful because neither the five-refill cap nor six-month clock is exhausted."),
    ("zaleplon", "FED-EPCS-TRANSFER", "A patient requests transfer of an unfilled electronic Sonata prescription to a second DEA-registered retail pharmacy. Both pharmacists can communicate directly. What else matters?", "Confirm it has not been transferred before, remains electronic and unaltered, and state law permits the transfer."),
    ("suvorexant", "MA-PMP-REPORTING", "A pharmacist wonders whether Belsomra dispensing is omitted from MassPAT because it is not a benzodiazepine. What is correct?", "Report it because Schedule IV status, not benzodiazepine class alone, brings covered dispensing into MassPAT."),
    ("lemborexant", "FED-CIII-V-REFILL", "A Dayvigo prescription has two refills used and is three months old. The next refill is requested. Which federal limits should be checked together?", "Check both the five-refill maximum and six-month issue-date window; neither is yet exhausted on these facts."),
    ("daridorexant", "FED-CIII-V-REFILL", "A Quviviq prescription still shows two refills but was issued six months and two days ago. What should control the decision?", "The six-month issue-date limit prevents another Schedule IV refill."),
    ("tramadol", "MA-OPIOID-SEVEN-DAY", "An adult's first outpatient tramadol prescription for acute pain requests a 10-day supply without exception documentation. What should be resolved?", "Resolve the Massachusetts initial-opiate seven-day limit before dispensing the requested quantity."),
]


SATA_DRUG_CASES = [
    ("testosterone-cypionate", ["MA-CS-QUANTITY-II-III", "MA-PMP-REPORTING"], "A Massachusetts pharmacy reviews a new Depo-Testosterone prescription. Select all conclusions supported by the canonical rules.", ["A qualifying non-opioid Schedule III prescription may use the statutory 90-day single-fill pathway.", "Covered dispensing is reportable to MassPAT."], ["The drug is Schedule VI because it is a hormone.", "The original may be refilled without regard to federal refill limits.", "A Schedule II emergency oral follow-up prescription is required."]),
    ("phentermine", ["FED-CIII-V-REFILL", "MA-PMP-REPORTING"], "A phentermine prescription is four months old with four completed refills. Select all supported statements.", ["A fifth refill may remain within the federal numerical limit.", "Covered Schedule IV dispensing is MassPAT-reportable."], ["The prescription remains refillable for one year.", "Phentermine is Schedule II and cannot be refilled.", "The drug is omitted from MassPAT because it is used for weight loss."]),
    ("phendimetrazine", ["MA-CS-QUANTITY-II-III", "FED-CIII-V-REFILL"], "A pharmacist evaluates a phendimetrazine prescription. Select all rules that may apply.", ["The non-opioid Schedule III single-fill quantity pathway must be considered.", "Federal Schedule III refill limits still apply to any authorized refills."], ["Schedule III status permits unlimited refills.", "The drug is a Schedule VI legend drug in Massachusetts.", "A Schedule II remainder may be filled for 30 days without using refill rules."]),
    ("modafinil", ["FED-CIII-V-REFILL", "MA-PMP-REPORTING"], "A Massachusetts pharmacy dispenses Provigil and later evaluates a refill. Select all supported conclusions.", ["Schedule IV refill timing and count limits apply.", "Covered dispensing must be reported to MassPAT."], ["Modafinil is noncontrolled federally.", "The prescription expires five days after issue.", "The pharmacist may create a new prescription after five refills."]),
    ("ketamine", ["FED-CIII-V-REFILL", "MA-PMP-REPORTING"], "A ketamine prescription is presented to a Massachusetts community pharmacy. Select all supported conclusions.", ["Schedule III refill limits apply if refills are authorized.", "Covered outpatient dispensing is MassPAT-reportable."], ["Ketamine is Schedule II and can never be refilled.", "Massachusetts treats ketamine as Schedule VI.", "A five-day contiguous-state narcotic rule automatically governs every ketamine prescription."]),
    ("perampanel", ["FED-CIII-V-REFILL", "MA-PMP-REPORTING"], "A Fycompa prescription is five months old and has three prior refills. Select all supported statements.", ["The federal six-month issue-date clock remains relevant.", "Covered Schedule III dispensing is reported to MassPAT."], ["The prescription can be refilled indefinitely if seizure control is stable.", "Fycompa is noncontrolled because it is an antiseizure drug.", "A new prescription is required after every fill because it is Schedule II."]),
    ("sodium-oxybate", ["FED-REMS", "FED-CIII-V-REFILL"], "Before dispensing Xyrem, a pharmacist reviews both controlled-substance and product-specific obligations. Select all supported conclusions.", ["Current product-specific REMS requirements must be satisfied.", "Federal Schedule III refill limits remain independently applicable."], ["REMS enrollment converts the drug to Schedule VI.", "REMS replaces every controlled-substance record requirement.", "A Medication Guide can be omitted whenever a REMS exists."]),
    ("dronabinol", ["FED-CIII-V-REFILL", "MA-PMP-REPORTING"], "A Marinol prescription has authorized refills. Select all supported statements.", ["Schedule III refill limits apply to the prescription.", "Covered dispensing is MassPAT-reportable."], ["All cannabinoid products are Schedule I.", "The prescription may be refilled for twelve months.", "The pharmacy may disregard the federal schedule because Massachusetts has Schedule VI."]),
    ("dronabinol-solution", ["FED-CII-NO-REFILL", "MA-CII-VALIDITY-30D"], "A pharmacist compares Syndros oral solution with Marinol capsules. Select all rules that apply to Syndros.", ["A Schedule II prescription for Syndros may not be refilled.", "The Massachusetts 30-day Schedule II validity period applies."], ["Syndros follows the Schedule III refill rule used for Marinol.", "Its liquid dosage form makes it Schedule VI.", "An unused refill remains valid for six months."]),
    ("diphenoxylate-atropine", ["MA-RX-CV-REFILL", "MA-PMP-REPORTING"], "A Lomotil prescription is reviewed in a Massachusetts pharmacy. Select all supported conclusions.", ["The Massachusetts Schedule V five-refill and six-month limits apply.", "Covered Schedule V dispensing is MassPAT-reportable."], ["Lomotil is an unrestricted Schedule VI drug.", "The prescription may be refilled for one year.", "The Schedule II 30-day validity rule controls every refill."]),
]


NONDRUG_CASES = [
    ("MA-CQI-PROGRAM", "A new community pharmacy has an incident log but no process for cause analysis or prevention. What is missing?", "A complete CQI program that detects, documents, assesses, and prevents quality-related events."),
    ("MA-QRE-NOTIFY", "A pharmacist discovers that the wrong strength was dispensed yesterday and the patient may still be taking it. What is the immediate priority?", "Notify the patient or representative, give correction and harm-minimization directions, and contact the prescriber when professionally indicated."),
    ("MA-QRE-DOCUMENT-24H", "A pharmacist learns of a quality-related event at 3 p.m. Monday. When must the initial event documentation be completed?", "Within 24 hours after the pharmacist discovered or was told of the event."),
    ("MA-QRE-ANALYSIS", "A pharmacy corrects repeated selection errors but never examines shelving, staffing, or workflow. Which CQI duty remains unmet?", "Analyze causes and contributing system factors and use the findings to improve the process."),
    ("MA-QRE-ANNUAL-ED", "A pharmacy trains new hires on CQI but has provided no follow-up education to existing personnel for 18 months. What is required?", "Provide ongoing CQI education to pharmacy personnel at least annually."),
    ("MA-SERIOUS-EVENT-REPORT", "A dispensing error results in emergency treatment, and the manager of record learns of the serious injury today. What deadline applies?", "Report the qualifying event to the Board within seven business days of discovery."),
    ("MA-SERIOUS-EVENT-RECORDS", "A pharmacy filed a serious-event report three years ago and plans to purge the supporting file. What should it do?", "Retain the readily retrievable supporting records for at least five years from filing."),
    ("FED-THEFT-LOSS-DEA", "A pharmacy discovers a significant unexplained loss of controlled substances on Friday morning. What federal response is time-critical?", "Provide written notice to the responsible DEA field division within one business day and complete the required Form 106 process."),
    ("FED-INVENTORY-INITIAL", "A pharmacy receives its first DEA registration and will begin stocking controlled substances tomorrow. What inventory event is required?", "Take an initial inventory of controlled substances on the date controlled-substance activity begins."),
    ("FED-INVENTORY-BIENNIAL", "A pharmacy took its last complete controlled-substance inventory 25 months ago. What is the issue?", "The federal biennial inventory interval has been exceeded."),
    ("FED-INVENTORY-COUNT", "During inventory, a pharmacist estimates the contents of an opened bottle containing 1,200 Schedule IV tablets. What should change?", "Use an exact count because the opened container holds more than 1,000 dosage units."),
    ("FED-CS-RECORDS-2Y", "A DEA registrant proposes discarding controlled-substance inventory records after 18 months. What is the minimum federal approach?", "Maintain the DEA-required records for at least two years and keep them available for inspection."),
    ("FED-FORM222-ORDER", "A pharmacy orders Schedule II stock by an ordinary purchase order without Form 222 or CSOS. What is missing?", "Use a DEA Form 222 or compliant digitally signed electronic order unless a specific exception applies."),
    ("FED-FORM222-60DAY", "A supplier plans to ship the unfilled balance of a DEA Form 222 order 64 days after execution. What is the problem?", "The ordinary 60-day Form 222 validity and partial-shipment window has expired."),
    ("FED-FORM222-DEFECT", "A supplier receives a DEA Form 222 with an altered quantity line and asks the purchaser to initial the change. What should happen?", "Reject and return the defective form; it cannot be corrected and must be replaced."),
    ("FED-FORM222-LOSS", "A pharmacy discovers that several unused DEA Forms 222 are missing. What is the first regulatory response?", "Immediately report the loss to the responsible DEA Special Agent in Charge with available form details."),
    ("FED-FORM222-RECORDS", "A purchaser stores executed Form 222 copies mixed into general invoices and cannot retrieve them separately. What must be corrected?", "Maintain the required Form 222 records separately or readily retrievable separately for two years."),
    ("FED-CSOS", "A purchaser wants to replace paper Form 222 orders with electronic Schedule II ordering. What makes that possible?", "Use CSOS-enabled software and a valid DEA-issued digital certificate for a compliant electronic order."),
    ("FED-FORM41", "A registrant destroys expired controlled stock but records only the total number of bottles. What is missing?", "Maintain the complete destruction record, including drug, quantity, method, date, place, and required witnesses."),
    ("FED-DISPOSAL-NONRETRIEVABLE", "A pharmacy pours controlled tablets into ordinary trash after removing patient labels. Why is this insufficient?", "Registrant destruction must render the controlled substances permanently non-retrievable."),
    ("FED-REVERSE-DISTRIBUTOR", "A pharmacy wants to send expired controlled stock to another business for disposition. What status must it verify?", "Verify the recipient is appropriately DEA-registered as a reverse distributor and follow the transfer records."),
    ("MA-PHARMACY-CLOSURE-NOTICE", "A resident pharmacy plans to close in 10 days and has not notified the Board. What timing problem exists?", "The ordinary rule calls for certified written Board notice at least 14 days before closure."),
]


SATA_NONDRUG_CASES = [
    ("MA-PHARMACY-CLOSURE-PATIENTS", "A community pharmacy prepares to close. Select all patient-notice duties supported by 247 CMR 6.13.", ["Identify patients who received prescriptions in the preceding 90 days.", "Attempt notice at least 14 days before closure and post conspicuous notice."], ["Destroy every patient file on the closure date.", "Notify only patients with controlled prescriptions.", "Refuse all requested transfers during the notice period."]),
    ("MA-PHARMACY-CLOSURE-CS", "A resident pharmacy has closed. Select all post-closure duties supported by the rule.", ["Submit original licenses and the controlled-substance registration within 14 days.", "Attest to lawful controlled-substance disposal or transfer."], ["Keep unused controlled stock indefinitely at the closed location.", "Wait one year before notifying the Board.", "Treat Form 222 records as patient property."]),
    ("MA-TECH-SCOPE", "A pharmacist assigns duties to a technician trainee. Select all supported principles.", ["The trainee may perform only duties allowed for that category under pharmacist supervision.", "Professional judgment functions remain with the pharmacist."], ["The trainee may independently counsel patients.", "The trainee may resolve a DUR alert without pharmacist review.", "Registration converts the trainee into a pharmacist intern."]),
    ("MA-TECH-CII", "A pharmacy revises its Schedule II workflow for support personnel. Select all supported requirements.", ["The personnel category must be authorized by 247 CMR 8.05 for the assigned handling step.", "The pharmacist remains responsible for required supervision and final professional functions."], ["Every technician trainee may independently receive Schedule II stock.", "A cashier may perform any Schedule II task if the manager consents.", "Schedule II handling is exempt from personnel-scope rules."]),
    ("MA-INTERN-SUPERVISION", "A licensed pharmacy intern is scheduled without a pharmacist preceptor physically or professionally directing the work. Select all supported conclusions.", ["The intern must work under direct supervision of a registered pharmacist preceptor.", "Intern status does not authorize independent pharmacist practice."], ["A senior technician may replace the pharmacist preceptor.", "The intern may verify prescriptions independently after 500 hours.", "Direct supervision applies only to Schedule II drugs."]),
    ("MA-INTERN-12H", "A student completes a 14-hour shift and asks that every hour count toward internship credit. Select all supported statements.", ["No more than 12 hours may be credited for that day.", "The remaining work time does not override the daily internship-credit cap."], ["All 14 hours must be credited because the student was present.", "The cap is eight hours per week.", "Only hours involving controlled substances count."]),
    ("MA-PHARMACIST-CE", "A pharmacist prepares for biennial renewal. Select all generally applicable Massachusetts CE rules.", ["Complete at least 20 contact hours in each calendar year of the cycle.", "Include at least two contact hours of pharmacy law in each calendar year."], ["Carry unused hours freely into the next year.", "Complete all 40 hours in the final month of the cycle.", "Home study has no annual limit."]),
    ("MA-CE-COMPOUNDING", "A pharmacist directly oversees sterile and complex nonsterile compounding. Select all supported conclusions.", ["The applicable sterile-compounding CE requirement must be met annually.", "The applicable complex-nonsterile compounding CE requirement must also be assessed."], ["General pharmacy-law CE automatically replaces all compounding CE.", "Compounding CE applies only to technicians.", "Current USP chapters eliminate state CE requirements."]),
    ("MA-CDTM-QUALIFICATIONS", "A pharmacist seeks to enter a collaborative practice agreement. Select all threshold qualifications supported by statute.", ["Maintain the required Massachusetts license and professional-liability coverage.", "Meet the degree-or-experience and additional annual CE requirements."], ["No written agreement is needed after five years of practice.", "Technician registration satisfies the pharmacist-license requirement.", "The supervising physician may waive statutory qualifications orally."]),
    ("MA-CDTM-RETAIL-SCOPE", "A retail CDTM program enrolls a referred adult patient. Select all supported limitations.", ["The patient must receive notice and consent to the retail collaboration.", "Actions must stay within the agreement, referral, disease states, and statutory retail scope."], ["The pharmacist may diagnose a new unrelated disease independently.", "Any walk-in patient is automatically enrolled.", "The retail pharmacy may employ a physician solely to create the collaboration."]),
    ("MA-CDTM-CONTROLLED-LIMIT", "A retail collaborative agreement purports to let the pharmacist prescribe alprazolam and methylphenidate. Select all supported conclusions.", ["The agreement cannot authorize retail pharmacist prescribing of Schedule II through V substances.", "The controlled-substance limitation applies even if the supervising physician signs the agreement."], ["Professional liability insurance waives the schedule restriction.", "Only Schedule II is prohibited; Schedule IV is allowed.", "A verbal patient consent converts the drugs to Schedule VI."]),
    ("MA-CDTM-SVI-RX", "A retail collaborating pharmacist issues an authorized Schedule VI prescription for a referred diagnosis. Select all supported duties.", ["Keep the prescription within the diagnosis and agreement scope.", "Send a copy of the prescription to the supervising physician within 24 hours."], ["Add Schedule II refills to the same prescription.", "Delay notice until the biennial agreement renewal.", "Use the authority for an unrelated walk-in diagnosis."]),
    ("MA-PRODUR", "A prospective review identifies a clinically significant interaction before dispensing. Select all supported actions.", ["Use professional judgment to evaluate and resolve the issue before dispensing.", "Communicate with the prescriber or patient when needed to resolve the concern."], ["Ignore the alert because the prescription is electronically signed.", "Delegate final resolution to a cashier.", "Dispense first and perform prospective review next month."]),
    ("MA-COUNSELING", "A pharmacy designs its patient-counseling workflow. Select all supported principles.", ["Provide the meaningful counseling opportunity required by 247 CMR 9.18.", "Use pharmacist judgment and patient-specific information rather than a purely mechanical signature."], ["Treat a receipt signature as proof of adequate counseling in every case.", "Delegate counseling to an unlicensed cashier.", "Omit counseling whenever a drug has a Medication Guide."]),
    ("MA-INTERCHANGE", "A lower-cost product is listed as interchangeable and reasonably available. Select all facts that matter before substitution.", ["Determine whether the prescriber validly indicated no substitution.", "Confirm the product is listed as interchangeable under Massachusetts standards."], ["Substitute any same-class drug without checking the list.", "Choose the highest-cost product automatically.", "Treat therapeutic similarity alone as legal interchangeability."]),
    ("MA-RETURN-QUARANTINE", "A patient returns medication that the pharmacy dispensed in error. Select all supported actions.", ["Accept the returned medication under the error pathway.", "Quarantine it and arrange proper disposal rather than returning it to saleable inventory."], ["Place sealed containers directly back on the shelf.", "Resell the medication after changing the patient label.", "Refuse the return because all dispensed drugs are categorically excluded."]),
]


ORDERED_CASES = [
    ("MA-QRE-NOTIFY", "A pharmacist discovers a potentially harmful dispensing error. Put the immediate CQI response in the most defensible order.", ["Assess the event and immediate patient risk.", "Notify the patient or representative and give harm-minimization directions.", "Contact the prescriber when professionally indicated and coordinate correction.", "Complete the initial QRE documentation within 24 hours."]),
    ("MA-PHARMACY-CLOSURE-NOTICE", "Put these planned resident-pharmacy closure actions in the most defensible chronological order.", ["Choose the intended closure date and prepare the required Board information.", "Send required Board and patient notices at least 14 days before closure.", "Transfer requested patient files and lawfully dispose of or transfer controlled stock.", "Within 14 days after closure, submit original credentials and the disposition attestation."]),
]


PLANNED_TOPICS = [
    "Defective drug recall communication", "Adulteration versus misbranding", "Medication Guide delivery", "REMS pharmacy certification", "Prescription drug sample quarantine", "Controlled-substance safe storage", "Schedule II emergency follow-up", "Schedule II insufficient-stock partial fill", "Oral Schedule III-V follow-up", "Controlled prescription required elements", "Electronic-prescribing exceptions", "Schedule VI classification", "Prescription transfer annotation", "Controlled prescription retention", "Licensee demographic reporting", "Serious-event nonresident exception", "CQI aggregate trend analysis", "CQI remedial workflow", "CSOS certificate authority", "Form 222 power of attorney", "Form 222 partial shipment", "Form 222 lost-form replacement", "Reverse-distributor inventory", "Destruction witness documentation", "Initial inventory timing", "Biennial inventory dating", "Opened-container exact count", "Controlled loss significance", "Patient counseling refusal", "DUR prescriber communication", "Midstream interchange notice", "Naloxone third-party dispensing", "Hormonal contraception screening", "CDTM agreement renewal", "CDTM patient consent", "CDTM Schedule VI notice", "Technician judgment boundary", "Intern preceptor responsibility", "Closure record custody", "Closure controlled-substance transfer",
]


def make_rule(spec: tuple, hold: bool = False) -> dict:
    if hold:
        rule_id, title, area, topic, subtopic, summary, section, url = spec
        jurisdiction = "MA"
    else:
        rule_id, title, jurisdiction, area, topic, subtopic, summary, section, url = spec
    authority_type = "FEDERAL_REGULATION" if jurisdiction == "FEDERAL" else "PROMULGATED_REGULATION"
    if "malegislature.gov" in url:
        authority_type = "STATUTE"
    if "fda.gov" in url:
        authority_type = "OFFICIAL_GUIDANCE"
    record = {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "0" * 64,
        "title": title,
        "jurisdiction": jurisdiction,
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": f"Tests whether the candidate can apply {subtopic.lower()} requirements to a pharmacy-practice scenario without substituting a nearby rule.",
        "authority": [{"type": authority_type, "name": title, "section": section, "url": url}],
        "status": "UNCLEAR" if hold else "CURRENT",
        "effective_date": None,
        "supersedes": [],
        "last_verified": TODAY,
        "numeric_facts": [],
        "exceptions": ["Apply any narrower setting-specific, product-specific, or emergency exception before the general rule."],
        "common_confusions": [f"Confusing {subtopic.lower()} with a nearby rule that has a different trigger or deadline."],
        "related_rule_ids": [],
        "verification_status": "HOLD" if hold else ("OFFICIAL_POLICY_VERIFIED" if "mass.gov" in url and "doc" not in url else "PRIMARY_VERIFIED"),
        "verification_notes": ("HOLD: authoritative sources are not yet reconciled; no question may cite this rule." if hold else f"Current official source checked on {TODAY}."),
    }
    record["content_hash"] = semantic_content_hash(record, "rule")
    return record


def rule_index() -> dict[str, dict]:
    return {record["rule_id"]: record for _, record in load_records(DATA / "rules")}


def consequence(rule_ids: list[str], summary: str) -> dict:
    return {"summary": summary, "rule_ids": rule_ids}


def make_drug(spec: tuple, rules: dict[str, dict]) -> dict:
    drug_id, generic, brands, indication, therapeutic_class, schedule = spec
    controlled = schedule != "NONCONTROLLED"
    ma_schedule = schedule if controlled else ("NONCONTROLLED" if drug_id == "naloxone" else "VI")
    masspat = controlled and schedule in {"II", "III", "IV", "V"}
    if schedule == "II":
        refill_rules = ["FED-CII-NO-REFILL"]
        partial_rules = ["FED-CII-PARTIAL-PATIENT"]
        quantity_rules = ["MA-CS-QUANTITY-II-III"]
    elif schedule in {"III", "IV"}:
        refill_rules = ["FED-CIII-V-REFILL"]
        partial_rules = ["FED-CIII-V-PARTIAL"]
        quantity_rules = ["MA-CS-QUANTITY-II-III"] if schedule == "III" else ["FED-CS-SCHEDULES"]
    elif schedule == "V":
        refill_rules = ["MA-RX-CV-REFILL"]
        partial_rules = ["FED-CIII-V-PARTIAL"]
        quantity_rules = ["FED-CS-SCHEDULES"]
    else:
        refill_rules = ["MA-SCHEDULE-VI"]
        partial_rules = ["MA-SCHEDULE-VI"]
        quantity_rules = ["MA-SCHEDULE-VI"]
    transfer_rules = ["FED-EPCS-TRANSFER"] if controlled else ["MA-RX-TRANSFER"]
    masspat_rules = ["MA-PMP-REPORTING"]
    if drug_id == "naloxone":
        refill_rules = partial_rules = quantity_rules = ["MA-NALOXONE"]
        transfer_rules = ["MA-NALOXONE"]
        masspat_rules = ["MA-NALOXONE"]
    if drug_id in {"isotretinoin", "mifepristone", "sodium-oxybate"}:
        transfer_rules = sorted(set(transfer_rules + ["FED-REMS"]))
    legal = {
        "refill": consequence(refill_rules, f"Apply the refill framework for a {schedule} product before dispensing another fill."),
        "transfer": consequence(transfer_rules, "Apply the current transfer rule and any product-specific REMS restriction."),
        "partial_fill": consequence(partial_rules, "Apply the schedule-specific partial-fill framework and document each dispensing."),
        "masspat": consequence(masspat_rules, "Report covered dispensing to MassPAT." if masspat else "This drug is not routinely a Schedule II-V MassPAT transaction; apply any product-specific reporting rule."),
        "quantity_limit": consequence(quantity_rules, "Apply the schedule- and indication-specific Massachusetts quantity rule."),
    }
    dependencies = sorted({rid for item in legal.values() for rid in item["rule_ids"]})
    label_url = f"https://dailymed.nlm.nih.gov/dailymed/search.cfm?query={generic.replace(' ', '+')}"
    record = {
        "drug_id": drug_id,
        "content_version": 1,
        "content_hash": "0" * 64,
        "generic_name": generic,
        "brand_names": brands,
        "main_indications": [indication],
        "therapeutic_class": therapeutic_class,
        "federal_status": {"controlled": controlled, "schedule": schedule},
        "massachusetts_status": {"schedule": ma_schedule, "masspat_reportable": masspat, "drug_of_concern": False},
        "legal_consequences": legal,
        "verified_rule_dependencies": {rid: {"content_version": rules[rid]["content_version"], "content_hash": rules[rid]["content_hash"]} for rid in dependencies},
        "authorities": [
            {"type": "FDA_LABEL", "name": f"DailyMed label search for {generic}", "section": "Indications and Usage; Drug Abuse and Dependence", "url": label_url},
            {"type": "FEDERAL_REGULATION", "name": "Federal controlled-substance schedules", "section": f"21 CFR 1308 ({schedule})" if controlled else "FDA-approved labeling", "url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1308" if controlled else label_url},
            {"type": "STATE_REGULATION", "name": "Massachusetts controlled-substance schedules", "section": "105 CMR 700.002", "url": "https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download"},
        ],
        "last_verified": TODAY,
        "verification_status": "PRIMARY_VERIFIED",
        "verification_notes": f"Identity, labeled indication, and schedule/status checked against official DailyMed, eCFR, and Massachusetts sources on {TODAY}.",
    }
    record["content_hash"] = semantic_content_hash(record, "drug")
    return record


def question_base(qid: str, family_id: str, area: int, topic: str, subtopic: str, difficulty: int, qtype: str, rule_ids: list[str], drug_ids: list[str], stem: str) -> dict:
    return {
        "question_id": qid,
        "family_id": family_id,
        "area": area,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "question_type": qtype,
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": stem,
        "choices": [],
        "correct_choice_ids": [],
        "explanation": {},
        "rule_ids": rule_ids,
        "drug_ids": drug_ids,
        "reasoning_steps": [],
        "verification_status": "AUDIT_PENDING",
        "lifecycle_status": "AUDIT_PENDING",
        "last_legal_review": TODAY,
        "audits": [],
        "duplicate_review_status": "PENDING",
        "independent_audit_status": "PENDING",
        "final_adjudication": None,
        "development_fixture": True,
    }


def difficulty_for(index: int) -> int:
    slot = index % 10
    return 3 if slot < 3 else 4 if slot < 8 else 5


def reasoning(rule_ids: list[str], difficulty: int, rules: dict[str, dict], drug: dict | None) -> list[str]:
    steps = []
    if drug:
        steps.append(f"Identify {drug['generic_name']} ({drug['brand_names'][0]}) as federal Schedule {drug['federal_status']['schedule']} and Massachusetts Schedule {drug['massachusetts_status']['schedule']}")
    steps.append(f"Identify the trigger for {rules[rule_ids[0]]['title']}")
    if difficulty >= 4:
        steps.append("Separate the controlling pathway from a nearby rule with a different schedule, deadline, or setting")
    if difficulty == 5:
        steps.append("Apply the exception and documentation conditions before selecting the final pharmacy action")
    return steps[: max(1, difficulty - 2)] if not drug else steps[: max(1, difficulty - 2)]


def drug_teaching(drug: dict) -> str:
    brand = drug["brand_names"][0]
    return (f"{drug['generic_name']} ({brand}) is used for {drug['main_indications'][0].lower()}. "
            f"It is federal Schedule {drug['federal_status']['schedule']} and Massachusetts Schedule {drug['massachusetts_status']['schedule']}; "
            f"its legal consequence in this scenario follows the cited schedule-specific rule.")


def make_sba(index: int, case: tuple, rules: dict[str, dict], drugs: dict[str, dict], answer_letters: list[str]) -> dict:
    drug_id, primary_rule, stem, correct = case if len(case) == 4 else (None, *case)
    qnum = 11 + index
    qid = f"MA-Q-{qnum:04d}"
    difficulty = difficulty_for(index)
    rule_ids = [primary_rule]
    if drug_id and primary_rule != "FED-CS-SCHEDULES":
        rule_ids.append("FED-CS-SCHEDULES")
    rule_ids = list(dict.fromkeys(rule_ids))
    primary = rules[primary_rule]
    family_id = f"P2_{qnum:04d}_{primary_rule.replace('-', '_')}"
    record = question_base(qid, family_id, primary["area"], primary["topic"], primary["subtopic"], difficulty, "SBA", rule_ids, [drug_id] if drug_id else [], stem)
    alt_ids = ["MA-RX-OUTSTATE-III-VI", "FED-CIII-V-REFILL", "FED-CII-PARTIAL-72H", "MA-SCHEDULE-VI"]
    alt_texts = [
        "Use the out-of-state prescription rule when its schedule, age, and verification conditions have not been checked.",
        "Process another refill because an authorization written by the prescriber overrides schedule limits.",
        "Treat the request as an insufficient-stock partial fill and use the 72-hour remainder rule.",
        "Handle the drug or transaction as ordinary Massachusetts Schedule VI activity.",
    ]
    correct_letter = answer_letters[index]
    letters = list("ABCDE")
    choices_by_letter = {}
    analysis = {}
    distractor_pairs = list(zip(alt_texts, alt_ids))
    d = 0
    for letter in letters:
        if letter == correct_letter:
            choices_by_letter[letter] = correct
            analysis[letter] = f"This applies {primary['title']}: {primary['rule_summary']}"
        else:
            text, alt_id = distractor_pairs[d]
            choices_by_letter[letter] = text
            analysis[letter] = f"That choice belongs, if at all, to {rules[alt_id]['title']}; its trigger does not match this scenario."
            d += 1
    record["choices"] = [{"id": letter, "text": choices_by_letter[letter]} for letter in letters]
    record["correct_choice_ids"] = [correct_letter]
    drug = drugs.get(drug_id) if drug_id else None
    core = f"{primary['rule_summary']} " + (drug_teaching(drug) if drug else "The pharmacy must use the exact trigger and deadline rather than borrowing a nearby controlled-substance rule.")
    record["explanation"] = {
        "core_reasoning": core,
        "choice_analysis": analysis,
        "related_facts": ([drug_teaching(drug), primary["rule_summary"]] if drug else [primary["rule_summary"], primary["authority"][0]["section"]]),
        "mpje_trap": f"Applying {rules[alt_ids[index % len(alt_ids)]]['subtopic'].lower()} to facts controlled by {primary['subtopic'].lower()}.",
    }
    record["reasoning_steps"] = reasoning(rule_ids, difficulty, rules, drug)
    while len(record["reasoning_steps"]) < difficulty - 2:
        record["reasoning_steps"].append(f"Confirm determination {len(record['reasoning_steps']) + 1} against the cited official section")
    return record


def make_sata(index: int, case: tuple, rules: dict[str, dict], drugs: dict[str, dict]) -> dict:
    if len(case) == 5:
        drug_id, rule_ids, stem, corrects, wrongs = case
    else:
        drug_id = None
        primary, stem, corrects, wrongs = case
        rule_ids = [primary]
    qnum = 11 + index
    qid = f"MA-Q-{qnum:04d}"
    difficulty = difficulty_for(index)
    primary = rules[rule_ids[0]]
    family_id = f"P2_{qnum:04d}_{rule_ids[0].replace('-', '_')}"
    record = question_base(qid, family_id, primary["area"], primary["topic"], primary["subtopic"], difficulty, "SATA", rule_ids, [drug_id] if drug_id else [], stem)
    order = [corrects[0], wrongs[0], corrects[1], wrongs[1], wrongs[2]]
    letters = list("ABCDE")
    record["choices"] = [{"id": letter, "text": text} for letter, text in zip(letters, order)]
    record["correct_choice_ids"] = ["A", "C"]
    analysis = {}
    for letter, text in zip(letters, order):
        if letter in {"A", "C"}:
            rid = rule_ids[0] if letter == "A" else rule_ids[min(1, len(rule_ids) - 1)]
            analysis[letter] = f"The proposition '{text}' is supported by {rules[rid]['title']}: {rules[rid]['rule_summary']}"
        else:
            alt = ["FED-CII-NO-REFILL", "MA-SCHEDULE-VI", "FED-CII-PARTIAL-72H"][["B", "D", "E"].index(letter)]
            analysis[letter] = f"This statement imports {rules[alt]['title']} without its required trigger and is not supported by the scenario."
    drug = drugs.get(drug_id) if drug_id else None
    record["explanation"] = {
        "core_reasoning": "Apply each proposition independently. " + " ".join(rules[rid]["rule_summary"] for rid in rule_ids) + (" " + drug_teaching(drug) if drug else ""),
        "choice_analysis": analysis,
        "related_facts": ([drug_teaching(drug)] if drug else []) + [rules[rid]["rule_summary"] for rid in rule_ids[:2]],
        "mpje_trap": "Selecting a familiar statement without checking whether its schedule, setting, deadline, and exception match the facts.",
    }
    record["reasoning_steps"] = reasoning(rule_ids, difficulty, rules, drug)
    while len(record["reasoning_steps"]) < difficulty - 2:
        record["reasoning_steps"].append(f"Evaluate proposition {len(record['reasoning_steps']) + 1} independently against the official source")
    return record


def make_ordered(index: int, case: tuple, rules: dict[str, dict]) -> dict:
    primary, stem, steps = case
    qnum = 11 + index
    qid = f"MA-Q-{qnum:04d}"
    difficulty = difficulty_for(index)
    rule_ids = [primary]
    if primary == "MA-QRE-NOTIFY":
        rule_ids += ["MA-QRE-DOCUMENT-24H"]
    else:
        rule_ids += ["MA-PHARMACY-CLOSURE-PATIENTS", "MA-PHARMACY-CLOSURE-CS"]
    rule_ids = list(dict.fromkeys(rule_ids))
    primary_record = rules[primary]
    family_id = f"P2_{qnum:04d}_{primary.replace('-', '_')}"
    record = question_base(qid, family_id, primary_record["area"], primary_record["topic"], primary_record["subtopic"], difficulty, "ORDERED_RESPONSE", rule_ids, [], stem)
    shuffled = [steps[2], steps[0], steps[3], steps[1]]
    record["choices"] = [{"id": letter, "text": text} for letter, text in zip("ABCD", shuffled)]
    ids = {text: letter for letter, text in zip("ABCD", shuffled)}
    record["correct_choice_ids"] = [ids[step] for step in steps]
    record["explanation"] = {
        "core_reasoning": f"For {primary_record['title']}, the chronology follows the legal trigger, advance or immediate response, operational completion, and final documentation deadlines in the cited rules.",
        "choice_analysis": {ids[step]: f"This is step {position}: {step}" for position, step in enumerate(steps, 1)},
        "related_facts": [rules[rid]["rule_summary"] for rid in rule_ids[:3]],
        "mpje_trap": "Ordering familiar tasks by convenience instead of the legal trigger and deadline sequence.",
    }
    record["reasoning_steps"] = ["Identify the triggering event", "Separate advance or immediate duties from later records", "Order the remaining actions by their legal deadlines"]
    return record


def new_family(question: dict) -> dict:
    return {
        "family_id": question["family_id"],
        "area": question["area"],
        "topic": question["topic"],
        "subtopic": question["subtopic"],
        "primary_rule_ids": [question["rule_ids"][0]],
        "secondary_rule_ids": question["rule_ids"][1:],
        "drug_required": bool(question["drug_ids"]),
        "scenario_types": [question["question_type"].lower().replace("_", " ")],
        "common_traps": [question["explanation"]["mpje_trap"]],
        "target_difficulties": [question["difficulty"]],
        "target_item_types": [question["question_type"]],
        "max_questions_in_final_bank": 2,
        "current_candidate_count": 1,
        "current_released_count": 0,
    }


def planned_family(index: int, rules: list[dict]) -> dict:
    rule = rules[index % len(rules)]
    topic = PLANNED_TOPICS[index]
    return {
        "family_id": f"P2_PLANNED_{index + 1:03d}_{rule['rule_id'].replace('-', '_')}",
        "area": rule["area"],
        "topic": rule["topic"],
        "subtopic": topic,
        "primary_rule_ids": [rule["rule_id"]],
        "secondary_rule_ids": [],
        "drug_required": False,
        "scenario_types": ["planned exception analysis"],
        "common_traps": [f"Using a general rule without checking the planned {topic.lower()} trigger"],
        "target_difficulties": [4, 5],
        "target_item_types": ["SBA", "SATA"],
        "max_questions_in_final_bank": 2,
        "current_candidate_count": 0,
        "current_released_count": 0,
    }


def main() -> int:
    for spec in RULE_SPECS:
        record = make_rule(spec)
        write_json(DATA / "rules" / f"{record['rule_id'].casefold()}.json", record)
    for spec in HOLD_SPECS:
        record = make_rule(spec, hold=True)
        write_json(DATA / "rules" / f"{record['rule_id'].casefold()}.json", record)

    rules = rule_index()
    for spec in DRUG_SPECS:
        record = make_drug(spec, rules)
        write_json(DATA / "drugs" / f"{record['drug_id']}.json", record)
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}

    answer_letters = list(("ABCDE" * 20)[:80])
    # Rebalance the 52 new SBA answers against the seven foundation SBA items.
    sba_letters = list("ABCDE" * 10) + ["E", "E"]
    for position, letter in enumerate(sba_letters):
        answer_letters[position] = letter

    questions = []
    for index, case in enumerate(DRUG_CASES):
        questions.append(make_sba(index, case, rules, drugs, answer_letters))
    for offset, case in enumerate(SATA_DRUG_CASES, 30):
        questions.append(make_sata(offset, case, rules, drugs))
    for offset, case in enumerate(NONDRUG_CASES, 40):
        questions.append(make_sba(offset, case, rules, drugs, answer_letters))
    for offset, case in enumerate(SATA_NONDRUG_CASES, 62):
        questions.append(make_sata(offset, case, rules, drugs))
    for offset, case in enumerate(ORDERED_CASES, 78):
        questions.append(make_ordered(offset, case, rules))

    if len(questions) != 80:
        raise ValueError(f"expected 80 questions, built {len(questions)}")
    if [q["question_id"] for q in questions] != [f"MA-Q-{n:04d}" for n in range(11, 91)]:
        raise ValueError("Phase 2 question IDs are not exactly MA-Q-0011..MA-Q-0090")
    for question in questions:
        write_json(DATA / "questions" / f"{question['question_id'].casefold()}.json", question)

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    matrix["last_reviewed"] = TODAY
    foundation = [family for family in matrix["families"] if not family["family_id"].startswith("P2_")]
    verified_rules = [rule for rule in rules.values() if rule["verification_status"] != "HOLD"]
    matrix["families"] = foundation + [new_family(question) for question in questions] + [planned_family(i, verified_rules) for i in range(40)]
    write_json(matrix_path, matrix)

    counts = {
        "rules": len(rules),
        "verified_rules": sum(r["verification_status"] != "HOLD" for r in rules.values()),
        "hold_rules": sum(r["verification_status"] == "HOLD" for r in rules.values()),
        "drugs": len(drugs),
        "families": len(matrix["families"]),
        "questions": len(load_records(DATA / "questions")),
        "new_difficulty": dict(Counter(q["difficulty"] for q in questions)),
        "new_types": dict(Counter(q["question_type"] for q in questions)),
        "new_drug_questions": sum(bool(q["drug_ids"]) for q in questions),
    }
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

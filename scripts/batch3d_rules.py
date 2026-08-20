"""Canonical rule records required by Batch 3 tranche B3-D.

Every rule below was read verbatim from the current official publication on 2026-08-20:

  * 105 CMR 700.000, recovered in full from the official PDF at
    https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download
    (sha256 78c4d84206d280f7aaee0d95bd9c07229366205dfd65fd177ac7847d861a2bcd).
  * Circular Letter DCP 26-03-124, Pharmacist Administration of Medications, 11 March 2026,
    recovered in full from the official PDF at
    https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download
    (sha256 162bd31fdab634dfb3fd7e3c3514095feae21df8018a2203256f719d2772a4d1). That circular
    states on its face that it replaces DCP 23-04-118 dated 21 April 2023.
  * 247 CMR 16.00, recovered in full from the official PDF
    (sha256 d98c03bcad5f440fcb52da41c5febe7f7c4cbf85db7237051bc6f75cc52506d8).
  * 243 CMR 2.12, recovered in full from the official PDF.
  * M.G.L. c. 94C ss. 1, 9, 18B, 19A, 19B, 19E and 19F, and M.G.L. c. 112 s. 24B1/2, read on
    malegislature.gov.

Nothing here is authored from a section heading, a summary, or a secondary source.

These rules cite only CURRENT authority. The older pharmacist-administration rules in the registry
that still cite Circular DCP 19-2-105 are the subject of a separate, independent authority review
and are deliberately not referenced here.
"""

from __future__ import annotations

CMR700 = "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c"
CMR16 = "https://www.mass.gov/regulations/247-CMR-1600-collaborative-drug-therapy-management"
CMR243 = "https://www.mass.gov/regulations/243-CMR-200-licensing-and-the-practice-of-medicine"
DCP = "https://www.mass.gov/news/pharmacist-administration-of-medications"
GL = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section"
GL112 = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B%201~2"

VERIFIED = "2026-08-20"
DPH = "Massachusetts Department of Public Health regulations"
MED = "Massachusetts Board of Registration in Medicine regulations"
BORP = "Massachusetts Board of Registration in Pharmacy regulations"


def _rule(rule_id, topic, subtopic, title, summary, relevance, authority,
          confusions, numeric=(), exceptions=(), related=(), status="CURRENT",
          verification_status="PRIMARY_VERIFIED"):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": "MA",
        "area": 2,
        "topic": topic,
        "subtopic": subtopic,
        "rule_summary": summary,
        "exam_relevance": relevance,
        "authority": list(authority),
        "status": status,
        "effective_date": None,
        "supersedes": [],
        "last_verified": VERIFIED,
        "numeric_facts": list(numeric),
        "exceptions": list(exceptions),
        "common_confusions": list(confusions),
        "related_rule_ids": list(related),
        "verification_status": verification_status,
        "verification_notes": (
            "Read verbatim in the current official publication on 2026-08-20 during Batch 3 tranche "
            "B3-D authoring under Issue #91. A fresh independent legal and full-bank realism audit "
            "is still required before release."
        ),
    }


def _dph(section):
    return {"type": "PROMULGATED_REGULATION", "name": DPH, "section": section, "url": CMR700}


def _dcp(section):
    return {"type": "OFFICIAL_GUIDANCE",
            "name": "Circular Letter DCP 26-03-124, Pharmacist Administration of Medications, 11 March 2026",
            "section": section, "url": DCP}


def _stat(section, url):
    return {"type": "STATUTE", "name": "Massachusetts General Laws", "section": section, "url": url}


RULES = [
    # ---------------- pharmacist administration, current authority chain ----------------
    _rule(
        "MA-ADMINISTER-STATUTORY-ROUTES", "Pharmacist administration", "Statutory routes",
        "Three statutory routes to pharmacist administration, gated differently",
        "M.G.L. c. 94C, s. 1 defines Administer to include direct application of a controlled "
        "substance by a REGISTERED PHARMACIST acting in accordance with: (i) regulations promulgated "
        "by the department, in consultation with the board of registration in pharmacy and the "
        "department of mental health, governing pharmacist administration of medications for "
        "treatment of mental health and substance use disorder AND at the direction of a prescribing "
        "practitioner; (ii) A PRESCRIPTION for testosterone for gender-affirming care; or (iii) A "
        "PRESCRIPTION for the treatment and prevention of sexually transmitted infections or for the "
        "prevention of HIV. Route (i) is gated on regulations plus practitioner direction; routes "
        "(ii) and (iii) are gated on a prescription.",
        "Tests that the statute contains three separate pharmacist routes with materially different "
        "preconditions, so a condition drawn from one route does not carry to the others.",
        [_stat("M.G.L. c. 94C, s. 1, definition of Administer, clause (c)", GL + "1")],
        ["Treating the mental health and substance use disorder conditions as governing every "
         "pharmacist administration route",
         "Assuming a regulation gate applies to the testosterone and sexually transmitted infection routes",
         "Confusing clause (c), which reaches a registered pharmacist, with clause (b), which reaches "
         "a nurse at the direction of a practitioner"],
    ),
    _rule(
        "MA-ADMIN-ELIGIBLE-MEDICATIONS", "Pharmacist administration", "Eligible medications",
        "The closed list of medications a pharmacist or intern may administer",
        "Under 105 CMR 700.004(B)(9) and current Department guidance, the generic medications listed "
        "in Circular DCP 26-03-124 are THE ONLY medications eligible to be administered by a "
        "pharmacist or pharmacy intern: long-acting injectable antipsychotics (aripiprazole, "
        "aripiprazole lauroxil, fluphenazine decanoate, haloperidol decanoate, paliperidone "
        "palmitate, risperidone, risperidone ER); long-acting injectables for substance use disorders "
        "(buprenorphine, naltrexone); testosterone, all salts, for gender-affirming care; HIV "
        "prevention medications (cabotegravir, lenacapavir or other medications to prevent HIV); and "
        "sexually transmitted infection medications (ceftriaxone by intramuscular injection, "
        "doxycycline or other medications to treat chlamydia). There is no requirement that a "
        "pharmacist or intern administer any of them.",
        "Tests that the list is closed rather than illustrative, and that eligibility is a separate "
        "question from whether the pharmacist must act.",
        [_dph("105 CMR 700.004(B)(9)(d)1."),
         _dcp("Medications Eligible for Pharmacist or Pharmacy Intern Administration")],
        ["Treating the list as examples of a broader category of injectables",
         "Assuming a listed medication must be administered on request",
         "Assuming a brand not named is outside the list, when the list is by generic name"],
        exceptions=["Administration remains voluntary for the pharmacist or intern"],
    ),
    _rule(
        "MA-ADMIN-ROUTE-AND-DOSING", "Pharmacist administration", "Route and dosing",
        "Subcutaneous or intramuscular only, in single doses",
        "A pharmacist or pharmacy intern may ONLY administer an eligible medication BY SUBCUTANEOUS "
        "OR INTRAMUSCULAR INJECTION, in accordance with manufacturer approved labeling and any risk "
        "evaluation and mitigation strategy requirements for the specific medication. The conditions "
        "on dispensing by administration include that administration is NOT INTRAVENOUS and that the "
        "medication is available in single-dose packaging and PRESCRIBED IN SINGLE DOSES, with or "
        "without refills.",
        "Tests the route limit and the separate single-dose condition, which candidates commonly "
        "merge into one idea about injections.",
        [_dcp("Administration and Dosing, with conditions (c) and (d) of Dispensing by Administration"),
         _dph("105 CMR 700.004(B)(9)(d)6.")],
        ["Treating any injection as permitted because the pharmacist is trained to inject",
         "Assuming refills are prohibited, when single-dose prescribing may carry refills",
         "Overlooking the manufacturer labeling and risk evaluation and mitigation strategy limits"],
        exceptions=["A prescription in single doses may carry refills"],
        related=["MA-ADMIN-ELIGIBLE-MEDICATIONS"],
    ),
    _rule(
        "MA-ADMIN-OTP-ORDER-ONLY", "Pharmacist administration", "Opioid treatment programs",
        "Addiction-treatment administration by order in a registered opioid treatment program",
        "105 CMR 700.004(B)(9)(e) authorises a pharmacist to administer controlled substances in an "
        "Opioid Treatment Program PURSUANT TO AN ORDER and in accordance with Department guidance. "
        "Circular DCP 26-03-124 states that a pharmacist may administer medications for addiction "
        "treatment, INCLUDING METHADONE, pursuant to an order, ONLY in a registered opioid treatment "
        "program. The instrument is an order rather than a prescription, and the setting is closed.",
        "Tests a route whose setting and whose instrument both differ from the ordinary "
        "administration pathway.",
        [_dph("105 CMR 700.004(B)(9)(e)"),
         _dcp("Note following the conditions for Dispensing by Administration")],
        ["Assuming a valid prescription opens this route in a community pharmacy",
         "Assuming buprenorphine and methadone travel the same pathway in every setting",
         "Overlooking that the programme must be a registered opioid treatment program"],
        related=["MA-ADMIN-ELIGIBLE-MEDICATIONS"],
    ),
    _rule(
        "MA-ADMIN-PRESCRIPTION-NOTATION", "Pharmacist administration", "Prescriber communication",
        "The administration notation on a prescription, and what its absence requires",
        "Circular DCP 26-03-124 provides that prescribers SHOULD make clear that they intend eligible "
        "medications to be administered by a pharmacist or pharmacy intern by including an "
        "administration notation on the prescription. A pharmacist or pharmacy intern receiving a "
        "prescription for eligible medications WITHOUT the notation is ENCOURAGED to contact the "
        "prescriber if, in their professional judgment, it appears the medication is intended to be "
        "administered rather than dispensed to the patient. Pharmacists and interns are strongly "
        "encouraged to send administration records to prescribers as soon after administration as "
        "practical.",
        "Tests the difference between guidance that is encouraged and a condition that is required, "
        "on a document candidates expect to be mandatory.",
        [_dcp("Pharmacist-Prescriber Communication")],
        ["Treating the missing notation as invalidating the prescription",
         "Treating contact with the prescriber as a precondition to administering",
         "Assuming the notation is required by regulation rather than encouraged by guidance"],
        related=["MA-ADMIN-ROUTE-AND-DOSING"],
    ),
    # ---------------- 105 CMR 700.003(F) emergency vaccine ----------------
    _rule(
        "MA-EMERGENCY-VACCINE-GATE", "Public health", "Emergency vaccine authority",
        "Commissioner order plus practitioner instrument before emergency vaccine administration",
        "Notwithstanding any other Department regulation, a health care professional duly licensed or "
        "certified by the Department, or a student duly enrolled in an approved programme acting "
        "within its policies, may possess and administer any vaccine designated by the Commissioner "
        "for prevention of a pandemic, novel or other vaccine-preventable disease, PROVIDED the "
        "Commissioner determines that there are or will be insufficient health care professionals "
        "available for timely administration AND issues an order authorizing it. Administration must "
        "accord with the Commissioner's order AND with the order or prescription of a duly registered "
        "practitioner authorized to issue one for a vaccine. A student may act only if authorised and "
        "supervised by a licensed and qualified health care professional.",
        "Tests a double gate: the practitioner instrument alone does not open the pathway, and the "
        "Commissioner order alone does not either.",
        [_dph("105 CMR 700.003(F) and (F)(1)")],
        ["Treating a practitioner standing prescription as sufficient without a Commissioner order",
         "Treating the Commissioner order as removing the need for a practitioner instrument",
         "Overlooking the supervision condition attaching to students"],
        exceptions=["A student must be authorised and supervised by a licensed and qualified professional"],
    ),
    _rule(
        "MA-EMERGENCY-VACCINE-PROTOCOLS", "Public health", "Emergency vaccine protocols",
        "Written protocol subjects required before administering under the emergency authority",
        "In accordance with the Commissioner's order, a person administering vaccine shall receive "
        "proper training and supervision in administration of the vaccine, and shall comply with "
        "written protocols to ensure proper STORAGE, HANDLING AND RETURN of vaccine, RECORDKEEPING "
        "regarding administration, RESPONSE TO ADVERSE EVENTS, and safe and appropriate "
        "administration of vaccine.",
        "Tests the required protocol subjects, whose distinctive member is return of vaccine, a "
        "subject the ordinary administration pathway does not name.",
        [_dph("105 CMR 700.003(F)(2)")],
        ["Assuming training records alone satisfy the paragraph",
         "Omitting return of vaccine from the protocol subjects",
         "Treating an adverse-event plan as covering the storage and handling subjects"],
        related=["MA-EMERGENCY-VACCINE-GATE"],
    ),
    # ---------------- 105 CMR 700.003(G) pharmacist prescribing ----------------
    _rule(
        "MA-CDTM-PRESCRIBING-POWERS", "Collaborative practice", "Prescribing powers",
        "Issue, modify or discontinue, each as authorised in the agreement",
        "A pharmacist may ISSUE, MODIFY OR DISCONTINUE a prescription or medication order AS "
        "AUTHORIZED IN a collaborative practice agreement meeting the requirements of 247 CMR 16.00, "
        "243 CMR 2.12 and M.G.L. c. 112, s. 24B1/2. The power is three-fold and each of the three "
        "acts must be authorised by the agreement itself, so an agreement that authorises one does "
        "not by implication authorise the others.",
        "Tests that discontinuation is as much a regulated act as issuance, and that authority is "
        "read act by act out of the agreement.",
        [_dph("105 CMR 700.003(G), opening words")],
        ["Assuming authority to modify carries authority to discontinue",
         "Treating stopping a therapy as a clinical decision outside the prescribing power",
         "Overlooking that the agreement must satisfy all three named instruments"],
    ),
    _rule(
        "MA-CDTM-PRESCRIBING-REGISTRATION", "Collaborative practice", "Prescribing registration",
        "Department registration for the purpose of prescribing",
        "The pharmacist registers with the Department, in accordance with 105 CMR 700.004, and with "
        "the DEA IF APPLICABLE in accordance with 21 CFR 1300, FOR THE PURPOSE OF PRESCRIBING under "
        "105 CMR 700.000. The purpose of the registration is part of the requirement, so a "
        "registration obtained for dispensing does not carry prescribing authority, and the federal "
        "limb bites only where it is applicable.",
        "Tests a precondition that turns on the purpose of an instrument the pharmacist may already "
        "hold for another purpose.",
        [_dph("105 CMR 700.003(G)(2)")],
        ["Treating an existing controlled substance registration as sufficient whatever its purpose",
         "Assuming DEA registration is always required",
         "Confusing this with the 247 CMR 16.02(1)(f) requirement to maintain a registration during "
         "the term of the agreement"],
        exceptions=["The DEA limb applies only if applicable"],
        related=["MA-CDTM-PRESCRIPTIVE-CONDITIONS"],
    ),
    _rule(
        "MA-CDTM-IMMEDIATE-TREATMENT-SUPPLY", "Collaborative practice", "Supply for immediate treatment",
        "Procurement channel for immediate-treatment stock turns on the schedule",
        "The pharmacist may dispense a controlled substance for immediate treatment in accordance with "
        "M.G.L. c. 94C, s. 9, PROVIDED the pharmacist is authorized by 105 CMR 700.003(G) to prescribe "
        "that substance. The pharmacist may order from a drug wholesaler, manufacturer, laboratory or "
        "distributor, for purposes of dispensing for immediate treatment, those controlled substances "
        "IN SCHEDULE VI which the pharmacist is authorized to prescribe. For Schedules II through V "
        "dispensed for immediate treatment, the pharmacist may obtain such controlled substances ONLY "
        "as supplied by the supervising physician or obtained through a prescription or medication "
        "order for the patient.",
        "Tests that the schedule decides the lawful procurement channel, and that ordinary wholesaler "
        "purchasing is closed for Schedules II through V in this pathway.",
        [_dph("105 CMR 700.003(G)(5) and (G)(6)")],
        ["Assuming a pharmacy that may buy a product for dispensing may buy it for this purpose",
         "Overlooking the precondition that the pharmacist must be authorised to prescribe it",
         "Treating the supervising physician's supply route as available for Schedule VI only"],
        related=["MA-CDTM-PRESCRIBING-POWERS"],
    ),
    _rule(
        "MA-PHARMACIST-PRESCRIBER-ID", "Collaborative practice", "Identification on transmission",
        "What a prescribing pharmacist must tell the dispensing pharmacist",
        "The pharmacist may issue a prescription in accordance with M.G.L. c. 94C, s. 20, PROVIDED "
        "that the prescribing pharmacist CLEARLY IDENTIFIES THEIR NAME AND PROFESSIONAL DESIGNATION "
        "to the dispensing pharmacist and provides their REGISTRATION NUMBER, WORK ADDRESS, PHONE "
        "NUMBER, AND THE NAME OF THE SUPERVISING PHYSICIAN.",
        "Tests five particulars a pharmacist prescriber must supply that an ordinary practitioner "
        "prescription does not require, the distinctive one being the supervising physician's name.",
        [_dph("105 CMR 700.003(G)(7)")],
        ["Treating a pharmacist prescription as identical in form to a practitioner prescription",
         "Omitting the supervising physician's name because the pharmacist holds the authority",
         "Assuming a callback number substitutes for the work address"],
        related=["MA-CDTM-PRESCRIBING-POWERS"],
    ),
    _rule(
        "MA-CDTM-FACILITY-ORDER", "Collaborative practice", "Prescribing in a health facility",
        "The instrument for prescribing to a patient in a licensed health facility",
        "The pharmacist may prescribe a controlled substance for a patient IN A LICENSED HEALTH "
        "FACILITY, including a hospital, long term care facility, ambulatory care clinic or hospice, "
        "THROUGH THE USE OF A WRITTEN MEDICATION ORDER ENTERED ON THE PATIENT'S MEDICAL RECORD "
        "MAINTAINED AT THE FACILITY, provided that such a written order meets all applicable "
        "provisions of 105 CMR 700.000.",
        "Tests which instrument the regulation authorises inside a facility and where it must live, "
        "against the habit of writing an outpatient-style prescription.",
        [_dph("105 CMR 700.003(G)(8)")],
        ["Using an outpatient prescription form for a facility inpatient",
         "Entering the order on a record the pharmacy keeps rather than the facility's record",
         "Assuming the paragraph reaches any setting where the pharmacist happens to be working"],
        related=["MA-CDTM-PRESCRIBING-POWERS"],
    ),
    # ---------------- M.G.L. c. 94C s. 9 ----------------
    _rule(
        "MA-S9-PHARMACIST-AUTHORITY", "Pharmacist administration", "Possession and administration",
        "The pharmacist appears on the section 9 practitioner list only as limited",
        "M.G.L. c. 94C, s. 9(a) allows the listed practitioners, and A PHARMACIST AS LIMITED BY s. "
        "7(g) AND M.G.L. c. 112, s. 24B1/2, when registered under s. 7 and acting in good faith in "
        "the course of a professional practice for the alleviation of pain and suffering or for the "
        "treatment or alleviation of disease, to POSSESS controlled substances as may reasonably be "
        "required for the purpose of patient treatment and to ADMINISTER controlled substances, or to "
        "cause the same to be administered under his direction by a nurse.",
        "Tests that the same sentence authorises a physician outright and a pharmacist only through "
        "two further instruments, and that it carries a possession limb as well as an administration "
        "limb.",
        [_stat("M.G.L. c. 94C, s. 9(a), first paragraph", GL + "9")],
        ["Reading the pharmacist into the list on the same footing as a physician",
         "Overlooking the possession limb and the quantity it is measured by",
         "Assuming the section is the whole of a pharmacist's administration authority"],
        related=["MA-ADMINISTER-STATUTORY-ROUTES"],
    ),
    # ---------------- M.G.L. c. 94C s. 18B ----------------
    _rule(
        "MA-NON-OPIATE-DIRECTIVE", "Opioid safety", "Voluntary non-opiate directive",
        "The standard an outpatient pharmacist is held to on a non-opiate directive",
        "A voluntary non-opiate directive form indicates to all practitioners that an individual "
        "shall not be administered or offered a prescription or medication order for an opiate, and "
        "may be revoked by written or oral means. A written prescription presented at, or "
        "electronically transmitted to, an OUTPATIENT PHARMACY is PRESUMED VALID for the purposes of "
        "the section, and a pharmacist in an outpatient setting SHALL NOT be held in violation for "
        "dispensing a controlled substance in contradiction to a directive EXCEPT UPON EVIDENCE THAT "
        "THE PHARMACIST ACTED KNOWINGLY against it. A board of professional licensure may act against "
        "a licensed health care provider who RECKLESSLY OR NEGLIGENTLY fails to comply.",
        "Tests a two-standard structure in one section: knowledge for the outpatient pharmacist, "
        "recklessness or negligence for health care providers generally.",
        [_stat("M.G.L. c. 94C, s. 18B(a), (c) and (e)", GL + "18B")],
        ["Applying the reckless or negligent standard to the outpatient pharmacist",
         "Treating the presented prescription as suspect rather than presumed valid",
         "Assuming a directive can only be revoked in writing"],
        exceptions=["The protection is lost where the pharmacist acted knowingly against the directive"],
    ),
    # ---------------- M.G.L. c. 94C ss. 19A, 19B, 19E reporting ----------------
    _rule(
        "MA-STANDING-ORDER-REPORTING", "Public health", "Standing-order reporting",
        "Reporting cadence and confidentiality across the standing-order regimes",
        "A pharmacist dispensing emergency contraception under the statewide standing order shall "
        "ANNUALLY provide the department with the number of times it is dispensed. A pharmacist who "
        "dispenses an opioid antagonist shall ANNUALLY report the number of doses dispensed. A "
        "pharmacist who dispenses a COVID-19 control measure shall report to the department UPON "
        "REQUEST on the doses, tests or devices dispensed. In each regime the reports shall not "
        "identify any individual patient, shall be confidential, and shall not constitute public "
        "records as defined in clause Twenty-sixth of section 7 of chapter 4.",
        "Tests that two regimes report annually while a third reports only on request, and that the "
        "public-records exclusion is common to all three.",
        [_stat("M.G.L. c. 94C, s. 19B(d)", GL + "19B"),
         _stat("M.G.L. c. 94C, s. 19A(e)", GL + "19A"),
         _stat("M.G.L. c. 94C, s. 19E(d)", GL + "19E")],
        ["Assuming a single reporting cadence governs every statewide standing order",
         "Treating the reports as public records available on request",
         "Assuming patient identifiers are required for the department to use the data"],
        related=["MA-STANDING-ORDER-TRAINING-CONTRAST"],
    ),
    # ---------------- M.G.L. c. 94C s. 19F contraception ----------------
    _rule(
        "MA-CONTRACEPTION-POST-PRESCRIBING", "Pharmacist prescribing", "Post-prescribing duties",
        "What the pharmacist owes after prescribing hormonal contraception",
        "The rules adopted under M.G.L. c. 94C, s. 19F(b) shall require a pharmacist to REFER the "
        "patient to the patient's primary care practitioner or reproductive health care practitioner, "
        "if applicable, upon prescribing and dispensing, or advise the patient to consult with such a "
        "practitioner; to PROVIDE THE PATIENT WITH A WRITTEN RECORD of the hormonal contraceptive "
        "patch or self-administered oral hormonal contraceptive prescribed and dispensed; and to "
        "DISPENSE AS SOON AS PRACTICABLE after the pharmacist issues the prescription.",
        "Tests three duties that attach after the prescribing decision, including a timing duty "
        "candidates rarely expect.",
        [_stat("M.G.L. c. 94C, s. 19F(c)(i)(C), (D) and (E)", GL + "19F")],
        ["Treating the referral as satisfied by a general suggestion to see a doctor sometime",
         "Omitting the written record because the prescription itself is a document",
         "Assuming the pharmacist may issue today and supply at the patient's convenience"],
    ),
    _rule(
        "MA-CONTRACEPTION-NO-APPOINTMENT", "Pharmacist prescribing", "Access conditions",
        "A pharmacist may not require an appointment for contraception prescribing",
        "The rules adopted under M.G.L. c. 94C, s. 19F(b) shall PROHIBIT a pharmacist from REQUIRING "
        "A PATIENT TO SCHEDULE AN APPOINTMENT with the pharmacist for the prescribing or dispensing "
        "of a hormonal contraceptive patch or self-administered oral hormonal contraceptive.",
        "Tests an access protection that runs against ordinary pharmacy workflow management.",
        [_stat("M.G.L. c. 94C, s. 19F(c)(ii)(A)", GL + "19F")],
        ["Treating an appointment requirement as a reasonable workflow measure",
         "Confusing a required appointment with an offered one",
         "Assuming the prohibition also bars asking the patient to wait"],
        related=["MA-CONTRACEPTION-POST-PRESCRIBING"],
    ),
    # ---------------- M.G.L. c. 112 s. 24B1/2(c) settings ----------------
    _rule(
        "MA-CDTM-SETTING-APPROVAL", "Collaborative practice", "Settings and approvals",
        "Which body approves collaborative practice in each non-retail setting",
        "Collaborative drug therapy management is allowed in hospitals licensed under M.G.L. c. 111, "
        "s. 51, SUBJECT TO APPROVAL BY THE MEDICAL STAFF EXECUTIVE COMMITTEE or designee; long-term "
        "care facilities licensed under s. 71, subject to approval by the FACILITY'S MEDICAL DIRECTOR "
        "or designee; inpatient or outpatient hospice settings licensed under s. 57D, subject to "
        "approval by the HOSPICE'S MEDICAL DIRECTOR or designee; and ambulatory care clinics licensed "
        "under s. 51, WITH ON-SITE SUPERVISION by the attending physician and a collaborating "
        "pharmacist, subject to approval by the clinic's medical staff executive committee or "
        "designee, or medical director or designee.",
        "Tests a setting-by-setting approval matrix and the on-site supervision condition unique to "
        "ambulatory care clinics.",
        [_stat("M.G.L. c. 112, s. 24B1/2(c)(1) through (4)", GL112)],
        ["Applying a single approval body across all four settings",
         "Overlooking the on-site supervision condition in the ambulatory care clinic setting",
         "Assuming hospitals and ambulatory care clinics differ because they sit under different "
         "licensing sections, when both are licensed under M.G.L. c. 111, s. 51"],
    ),
    _rule(
        "MA-CDTM-RETAIL-AGE-EXTENSION", "Collaborative practice", "Retail age and extension",
        "The retail age floor and the thirty-day extension power",
        "In the retail drug business setting collaborative practice is limited to PATIENTS 18 YEARS "
        "OF AGE OR OLDER; to AN EXTENSION BY 30 DAYS of current drug therapy prescribed by the "
        "supervising physician; and to administration of vaccines or the modification of dosages of "
        "medications prescribed by the supervising physician for the named disease states and "
        "co-morbidities identified by the supervising physician for the individual patient along with "
        "the primary diagnosis.",
        "Tests the retail age floor and the shape of the extension power, which extends existing "
        "therapy rather than initiating new therapy.",
        [_stat("M.G.L. c. 112, s. 24B1/2(c)(5)", GL112)],
        ["Treating the extension power as a power to initiate therapy",
         "Extending a therapy the supervising physician did not prescribe",
         "Assuming the age floor is a guideline rather than a statutory limit"],
        numeric=[{"fact": "Retail collaborative practice minimum patient age", "value": 18,
                  "unit": "years", "conditions": "retail drug business setting"},
                 {"fact": "Maximum extension of current drug therapy in the retail setting", "value": 30,
                  "unit": "days", "conditions": "therapy prescribed by the supervising physician"}],
        related=["MA-CDTM-RETAIL-SCOPE"],
    ),
    _rule(
        "MA-CDTM-VACCINE-ADMINISTRATION", "Collaborative practice", "Vaccine administration route",
        "Vaccine administration as an authority derived from the agreement",
        "Among the restrictions applying to community pharmacies in retail drug business settings "
        "operating under a current collaborative practice agreement, 247 CMR 16.03(5)(b) provides "
        "that PHARMACISTS, AS AUTHORIZED PURSUANT TO A COLLABORATIVE PRACTICE AGREEMENT, MAY "
        "ADMINISTER VACCINES. The authority is derived from the agreement rather than from the Drug "
        "Control Program medication pathway or from an emergency Commissioner order.",
        "Tests which of the several Massachusetts administration routes a given set of facts engages.",
        [{"type": "PROMULGATED_REGULATION", "name": BORP, "section": "247 CMR 16.03(5)(b)", "url": CMR16}],
        ["Conflating the collaborative vaccine route with the eligible-medication administration pathway",
         "Assuming an emergency Commissioner order is needed for routine vaccination",
         "Overlooking that the retail restrictions in 247 CMR 16.03(5) apply alongside it"],
        related=["MA-CDTM-RETAIL-AGE-EXTENSION", "MA-EMERGENCY-VACCINE-GATE"],
    ),
    # ---------------- 243 CMR 2.12(3) physician eligibility ----------------
    _rule(
        "MA-SUPERVISING-PHYSICIAN-ELIGIBILITY", "Collaborative practice", "Physician eligibility",
        "When the supervising physician's status ends the pharmacist's authority",
        "A physician is INELIGIBLE to participate in collaborative drug therapy management if he or "
        "she is in a Voluntary Agreement Not to Practice Medicine with the Board, or has had a "
        "licence to practise medicine temporarily suspended or revoked. A physician SHALL BE DEEMED "
        "INELIGIBLE if he or she has VOLUNTARILY SURRENDERED or has had SUSPENDED, REVOKED OR "
        "RESTRICTED a controlled substances licence, permit or registration, EITHER STATE OR FEDERAL. "
        "Where the Board acts against a physician it MAY require the physician to notify each "
        "authorized pharmacist with whom the physician is in an agreement.",
        "Tests that a controlled substances registration event alone ends the collaboration even with "
        "the medical licence intact, and that notice to the pharmacist is discretionary.",
        [{"type": "PROMULGATED_REGULATION", "name": MED,
          "section": "243 CMR 2.12(3)(d) and (e)", "url": CMR243}],
        ["Assuming an unrestricted medical licence keeps the collaboration alive",
         "Assuming the pharmacist will always be notified before the authority lapses",
         "Overlooking that a federal registration event counts equally with a state one"],
        related=["MA-CDTM-DISCIPLINE-NOTICE"],
    ),
]

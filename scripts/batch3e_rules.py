"""Canonical rule records required by Batch 3 top-up tranche B3-E.

Every rule below was read verbatim from the current official publication on 2026-08-20:

  * 247 CMR 6.00 Licensure of Pharmacies, official PDF
    https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download
    (sha256 8d1def57328d628a0c2e5a3a7adac28afa2d361585c09550b571f92eafa919f1).
  * 247 CMR 7.00 Wholesale Druggists, 247 CMR 11.00 Registration under the Controlled Substances
    Act, 247 CMR 13.00 Nuclear Pharmacies and 247 CMR 21.00 Registration of Outsourcing Facilities,
    each recovered in full from its official PDF.
  * 105 CMR 700.000, official PDF
    (sha256 78c4d84206d280f7aaee0d95bd9c07229366205dfd65fd177ac7847d861a2bcd).

Four of these chapters were cited by no rule anywhere in the bank before this tranche. See
audits/controller/AREA4-TOPUP-CENSUS.json for the novelty probe and the source survey.

Where the PDF extraction lost a sub-paragraph, no rule rests on the missing text.
"""

from __future__ import annotations

CMR6 = "https://www.mass.gov/regulations/247-CMR-600-licensure-of-pharmacies"
CMR7 = "https://www.mass.gov/regulations/247-CMR-700-wholesale-druggists"
CMR11 = "https://www.mass.gov/regulations/247-CMR-1100-registration-under-the-controlled-substances-act-mgl-c94c"
CMR13 = "https://www.mass.gov/regulations/247-CMR-1300-registration-requirements-and-minimal-professional-standards-for-nuclear-pharmacies"
CMR21 = "https://www.mass.gov/regulations/247-CMR-2100-registration-of-outsourcing-facilities"
CMR700 = "https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c"

VERIFIED = "2026-08-20"
BORP = "Massachusetts Board of Registration in Pharmacy regulations"
DPH = "Massachusetts Department of Public Health regulations"


def _rule(rule_id, topic, subtopic, title, summary, relevance, authority,
          confusions, numeric=(), exceptions=(), related=()):
    return {
        "rule_id": rule_id,
        "content_version": 1,
        "content_hash": "",
        "title": title,
        "jurisdiction": "MA",
        "area": 4,
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
            "Read verbatim in the current official publication on 2026-08-20 during Batch 3 tranche "
            "B3-E authoring under Issue #91. A fresh independent legal and full-bank realism audit "
            "is still required before release."
        ),
    }


def _b(section, url):
    return {"type": "PROMULGATED_REGULATION", "name": BORP, "section": section, "url": url}


RULES = [
    _rule(
        "MA-PHARMACY-SUITABILITY", "Pharmacy licensure", "Suitability of applicant and interest holder",
        "Board discretion to find an applicant, licensee or interest holder unsuitable",
        "In its discretion the Board may determine an applicant or licensee is not suitable to establish "
        "or maintain a pharmacy and that issuing a licence would not be in the interest of public health, "
        "safety and welfare. The eleven listed factors reach an APPLICANT, LICENSEE OR INTEREST HOLDER "
        "and cover conduct presenting an immediate or serious threat to public health and safety; "
        "impeding Board or Department enforcement; assuming ownership to circumvent 247 CMR 2.00; prior "
        "discipline, denial or revocation, or a consent agreement resolving a complaint, at any "
        "pharmacy, health care facility or other FDA- or DEA-registered entity the person owned, "
        "operated or held an interest in; operating such an entity so as to create an immediate or "
        "serious threat; failure to demonstrate competence or experience to operate a pharmacy; "
        "obtaining or attempting to obtain a licence by fraud or misrepresentation; HOLDING PRESCRIPTIVE "
        "PRIVILEGES; and prior discipline or a consent agreement on a professional licence.",
        "Tests that suitability reaches beyond the applicant to interest holders and beyond pharmacies "
        "to other regulated entities, and that one listed factor is a status rather than misconduct.",
        [_b("247 CMR 6.03", CMR6)],
        ["Reading the factors as reaching only the named applicant",
         "Assuming every factor describes misconduct, when holding prescriptive privileges is a status",
         "Assuming only Massachusetts pharmacy history counts, when FDA- and DEA-registered entities do"],
    ),
    _rule(
        "MA-PHARMACY-OWNERSHIP-TRANSFER", "Pharmacy licensure", "Transfer of ownership",
        "Both sides of an ownership transfer owe a fourteen-day duty",
        "At least 14 days before the transfer of ownership of a licensed pharmacy the LICENSEE shall "
        "notify the Board of the proposed transfer, and the outgoing licensee shall comply with the "
        "notification and closing provisions and with the controlled substance distribution provisions. "
        "At least 14 days before the transfer the PROPOSED NEW LICENSEE shall submit an application to "
        "operate a pharmacy, supported by a complete application, a controlled substance inventory "
        "report required by 247 CMR 6.14, an official bill of sale, and any additional information the "
        "Board requires. The Board may find the proposed new licensee or any proposed new interest "
        "holder unsuitable on the 247 CMR 6.03 factors.",
        "Tests that the fourteen-day clock runs against both parties independently and that the incoming "
        "licensee's application is judged on the same suitability factors.",
        [_b("247 CMR 6.11", CMR6)],
        ["Treating the buyer's application as discharging the seller's notice duty",
         "Assuming the buyer inherits the seller's licence rather than applying for one",
         "Overlooking that the inventory report and the bill of sale are application components"],
        numeric=[{"fact": "Minimum notice before a transfer of ownership", "value": 14, "unit": "days",
                  "conditions": "owed separately by the outgoing licensee and the proposed new licensee"}],
        related=["MA-PHARMACY-SUITABILITY"],
    ),
    _rule(
        "MA-CS-TRANSFER-BETWEEN-PHARMACIES", "Controlled substance procurement", "Transfer on closure or sale",
        "Procedure for moving controlled substance stock between licensed pharmacies",
        "A licensee, Manager of Record or agent intending to transfer Schedules II through VI from one "
        "Board-licensed pharmacy to another shall notify the Board IN WRITING BY CERTIFIED MAIL at least "
        "14 days before the transfer, unless otherwise authorized, giving the named particulars of both "
        "pharmacies. No sooner than 14 days after notification the transfer may proceed provided that on "
        "the transfer date the transferor takes a complete inventory of all Schedule II through V "
        "substances and all Schedule VI substances reportable to the prescription monitoring program; "
        "both Managers of Record sign the inventory report, with a staff pharmacist permitted to sign in "
        "place of an unavailable transferor Manager on notice to the Board of the reason; both "
        "pharmacies keep a readily retrievable copy for at least two years; both file an attestation "
        "with the Board within TEN DAYS; the transferee receives the substances and records on the "
        "transfer date and keeps the records at least two years; and the transferor MAY NOT POSSESS any "
        "controlled substances after the transfer date.",
        "Tests a multi-step procedure with three different clocks and a closing prohibition candidates "
        "routinely miss.",
        [_b("247 CMR 6.14", CMR6)],
        ["Confusing the 14-day notice with the 10-day attestation",
         "Assuming the transferor may retain a small residual stock after the transfer date",
         "Assuming only Schedules II through V are inventoried, when reportable Schedule VI is included"],
        numeric=[{"fact": "Notice to the Board before transferring controlled substances", "value": 14,
                  "unit": "days", "conditions": "in writing by certified mail, unless otherwise authorized"},
                 {"fact": "Attestation to the Board confirming the inventory", "value": 10, "unit": "days",
                  "conditions": "after the transfer, filed by both pharmacies"},
                 {"fact": "Retention of the controlled substance inventory report", "value": 2,
                  "unit": "years", "conditions": "by both pharmacies, readily retrievable"}],
        exceptions=["A staff pharmacist may sign where the transferor Manager of Record is unavailable "
                    "due to death, serious illness or termination, on notice to the Board"],
        related=["MA-PHARMACY-OWNERSHIP-TRANSFER"],
    ),
    _rule(
        "MA-PROVISIONAL-PHARMACY-LICENCE", "Facility licensure", "Provisional licences",
        "A provisional pharmacy licence lasts at most one year and cannot be extended",
        "In its discretion the Board may issue a provisional licence in lieu of a sterile compounding, "
        "complex non-sterile compounding, institutional sterile compounding, non-resident Drug Store, "
        "non-resident sterile compounding or non-resident complex non-sterile compounding pharmacy "
        "licence, provided the applicant submitted a COMPLETE application and demonstrated substantial "
        "compliance with Massachusetts pharmacy law together with the potential to achieve FULL "
        "compliance within the provisional period. The provisional licence ends on the earliest of "
        "conversion by the Board, surrender, suspension or revocation, or ONE YEAR from issue. The Board "
        "may convert it once it determines the pharmacy is in full compliance. A provisional licence MAY "
        "NOT BE RENEWED OR EXTENDED.",
        "Tests a hard outer limit with no extension mechanism, against the assumption that a regulator "
        "will always allow more time.",
        [_b("247 CMR 6.17", CMR6)],
        ["Assuming a provisional licence can be renewed while compliance work continues",
         "Treating substantial compliance at application as equivalent to full compliance",
         "Assuming the one-year period restarts on a change of Manager of Record"],
        numeric=[{"fact": "Maximum life of a provisional pharmacy licence", "value": 1, "unit": "year",
                  "conditions": "from issue; not renewable or extendable"}],
    ),
    _rule(
        "MA-WHOLESALE-CHANGE-AND-QUALIFICATION", "Wholesale distribution", "Licence maintenance",
        "Thirty-day change reporting and the wholesale licensing factors",
        "Changes in any of the information a wholesale distributor reported to the Board shall be "
        "submitted to the Board IN WRITING WITHIN 30 DAYS after the change. In issuing, renewing or "
        "revoking a licence to engage in the wholesale distribution of prescription drugs the Board "
        "shall consider at a minimum: convictions under any federal, state or local law relating to drug "
        "samples or to wholesale or retail drug distribution or distribution of controlled substances; "
        "any felony convictions; past experience in manufacture or distribution; furnishing false or "
        "fraudulent material in any application; suspension, revocation or other sanction of any licence "
        "or registration for manufacture or distribution of drugs; compliance with prior licensing "
        "requirements; compliance with record maintenance and availability requirements; failure to "
        "provide adequate control over distribution, diversion, theft or loss of drugs; compliance with "
        "247 CMR 7.00; and any other relevant factor. The Board reserves the right to deny a licence "
        "where granting it would not be in the public interest.",
        "Tests a reporting clock distinct from the pharmacy regime and a factor list that reaches "
        "convictions unrelated to drugs.",
        [_b("247 CMR 7.02(6), (7) and (8)", CMR7)],
        ["Applying the pharmacy notification clock to a wholesale distributor",
         "Assuming only drug-related convictions count, when any felony conviction is listed",
         "Assuming the listed factors are exhaustive"],
        numeric=[{"fact": "Reporting a change in wholesale licence information", "value": 30, "unit": "days",
                  "conditions": "in writing to the Board after the change"}],
    ),
    _rule(
        "MA-CS-REGISTRATION-TERM", "Controlled substance registration", "Separate registration and term",
        "One registration per place of business, with terms that differ by registrant type",
        "A SEPARATE controlled substance registration is required at EACH PRINCIPAL PLACE OF BUSINESS "
        "where the licensee or registrant manufactures, distributes or dispenses controlled substances. "
        "The term differs by registrant: a registration issued to a PHARMACY is valid for two years "
        "beginning January 1st of each EVEN-NUMBERED year; a registration issued to an OUTSOURCING "
        "FACILITY is valid for two years beginning January 1st of each even-numbered year; and a "
        "registration issued to a WHOLESALE DRUGGIST is valid for ONE year beginning DECEMBER 1st of "
        "each year.",
        "Tests that the registration term is not uniform, and that the wholesale term differs from the "
        "others in both length and start date.",
        [_b("247 CMR 11.05 and 11.06", CMR11)],
        ["Assuming a single biennial cycle governs every registrant",
         "Assuming one registration covers several locations under one owner",
         "Assuming the wholesale cycle also starts on January 1st"],
        numeric=[{"fact": "Pharmacy controlled substance registration term", "value": 2, "unit": "years",
                  "conditions": "beginning January 1st of each even-numbered year"},
                 {"fact": "Wholesale druggist controlled substance registration term", "value": 1,
                  "unit": "year", "conditions": "beginning December 1st of each year"}],
    ),
    _rule(
        "MA-NUCLEAR-PHARMACY-SERVICE", "Nuclear pharmacy", "Radiopharmaceutical service",
        "What radiopharmaceutical service comprises, and the permit for a nuclear pharmacy",
        "Radiopharmaceutical service means the counting, dispensing, labeling and delivery of "
        "radiopharmaceuticals; participating in radiopharmaceutical SELECTION and UTILIZATION REVIEWS; "
        "properly and safely storing and distributing radiopharmaceuticals; maintaining "
        "radiopharmaceutical QUALITY ASSURANCE; ADVISING on therapeutic values, hazards and use; and the "
        "acts, services, operations or transactions necessary to conduct, operate, manage and control "
        "radiopharmaceutical services within a nuclear pharmacy. Radiopharmaceutical quality assurance "
        "means performing appropriate chemical, biological and physical tests and interpreting the data "
        "to determine suitability for use in humans or animals, including internal test assessment, "
        "authentication of product history and maintenance of proper records. An initial permit to "
        "establish a nuclear pharmacy is applied for on a Board form with the required fee.",
        "Tests that the defined service reaches clinical and advisory activity rather than handling "
        "alone, and that quality assurance carries a specified content.",
        [_b("247 CMR 13.02 and 13.03", CMR13)],
        ["Reading radiopharmaceutical service as storage, preparation and delivery only",
         "Assuming quality assurance means only testing, when authentication of product history and "
         "record maintenance are inside the definition",
         "Assuming a nuclear pharmacy operates under an ordinary Drug Store pharmacy licence"],
    ),
    _rule(
        "MA-PROVISIONAL-OUTSOURCING-LIMITS", "Facility licensure", "Outsourcing facility registration",
        "A provisional outsourcing registration permits compounding but not supply",
        "An outsourcing facility registration is NON-TRANSFERRABLE. A NON-RESIDENT outsourcing facility "
        "is NOT ELIGIBLE for a provisional registration. Where an applicant was not inspected by the FDA "
        "in the two years immediately preceding the application the Board may issue a provisional "
        "outsourcing registration if the application is otherwise complete. An entity holding a "
        "provisional outsourcing facility registration MAY COMPOUND sterile drug preparations but MAY "
        "NOT DISTRIBUTE OR DISPENSE a sterile drug preparation within or outside the Commonwealth until "
        "it has been inspected by the FDA and has received a Massachusetts outsourcing facility "
        "registration. The provisional registration ends on the earliest of conversion, surrender, "
        "suspension or revocation, or expiry on December 31st of the first odd-numbered year following "
        "issue. The Board may convert it on proof of an FDA inspection under section 503B, provided the "
        "results are not grounds for denial under M.G.L. c. 112, s. 36E(e).",
        "Tests a registration that authorises production but withholds supply, which candidates "
        "routinely collapse into a single permission.",
        [_b("247 CMR 21.02(6) and 21.03", CMR21)],
        ["Assuming a provisional registration permits shipping what it permits compounding",
         "Assuming a non-resident facility may hold a provisional registration",
         "Assuming an outsourcing facility registration passes with a sale of the business"],
    ),
    _rule(
        "MA-THEFT-LOSS-TAMPERING-REPORT", "Mandatory reporting", "Theft, loss or tampering",
        "Twenty-four hour report of theft, loss or suspected tampering",
        "A registrant shall report the THEFT, LOSS OR SUSPECTED TAMPERING of any controlled substances "
        "to the DRUG CONTROL PROGRAM within the Department WITHIN 24 HOURS OF DISCOVERY of such theft, "
        "loss or suspected tampering, by completing and submitting the form provided or approved by the "
        "Drug Control Program for that purpose.",
        "Tests a short clock that runs from discovery rather than from the event, a recipient that is "
        "the Drug Control Program rather than the Board, and a trigger that includes mere suspicion of "
        "tampering.",
        [{"type": "PROMULGATED_REGULATION", "name": DPH, "section": "105 CMR 700.008", "url": CMR700}],
        ["Running the clock from the date of the loss rather than from its discovery",
         "Reporting to the Board of Registration in Pharmacy instead of the Drug Control Program",
         "Waiting for confirmation before reporting, when suspected tampering is itself the trigger"],
        numeric=[{"fact": "Deadline to report theft, loss or suspected tampering", "value": 24,
                  "unit": "hours", "conditions": "from discovery, to the Drug Control Program on its form"}],
    ),
]

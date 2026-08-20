"""Batch 3 top-up tranche B3-E — 9 Area-4 questions, MA-Q-0361 through MA-Q-0369.

Sized to the measured Area-4 deficit rather than to the thirty identifiers the original plan
reserved. Area 4 stands at 61 released against a minimum of 75, and the only unreleased Area-4
candidates are the five S2 questions, so at least nine must be newly authored whatever the salvage
outcome. Nine is authored; nothing beyond the measured need.

One question per family, each family new and capped at 2 so a later top-up has somewhere to go.
Every proposition was established in audits/controller/AREA4-TOPUP-CENSUS.json before authoring,
and each returned zero hits on a whole-bank novelty probe.

Structural targets, against the Phase-2 pool after B3-D (216 SBA, 134 SATA, chi-square 0.6547):
  * 6 SBA / 3 SATA.
  * SBA keys A x2 / E x2 / C x1 / D x1, favouring the two positions the released pool will be
    lightest in once B3-C and B3-D are admitted.
  * SATA correct-counts 2-correct x2 / 4-correct x1, no three-correct item.
"""

from __future__ import annotations


def q(qid, family, topic, subtopic, difficulty, qtype, stem, choices, correct,
      core, analysis, rules, steps, facts, trap):
    return {
        "question_id": qid,
        "family_id": family,
        "area": 4,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "question_type": qtype,
        "provenance": "GEN",
        "source_signal_ids": [],
        "stem": stem,
        "choices": [{"id": cid, "text": text} for cid, text in choices],
        "correct_choice_ids": list(correct),
        "explanation": {
            "core_reasoning": core,
            "choice_analysis": analysis,
            "related_facts": list(facts),
            "mpje_trap": trap,
        },
        "rule_ids": list(rules),
        "drug_ids": [],
        "reasoning_steps": list(steps),
    }


QUESTIONS = [
    q("MA-Q-0361", "B3E_PHARMACY_SUITABILITY_FACTORS", "Pharmacy licensure", "Suitability", 4, "SATA",
      "A company applying for a Massachusetts pharmacy licence has a minority investor whose previous "
      "out-of-state pharmacy entered a consent agreement resolving a complaint, and whose separate "
      "professional licence was once suspended. The applicant company itself has a clean record. Which "
      "statements about the Board's suitability review are correct? Select all that apply.",
      [("A", "The factors reach an interest holder as well as the applicant itself."),
       ("B", "A consent agreement resolving a complaint is among the listed factors."),
       ("C", "Only conduct at a Massachusetts pharmacy may be weighed by the Board."),
       ("D", "Prior discipline on a separate professional licence is a listed factor."),
       ("E", "The Board may conclude that licensing would not serve public health and safety.")],
      ["A", "B", "D", "E"],
      "247 CMR 6.03 lets the Board find an applicant unsuitable and lists eleven factors, each framed "
      "as reaching an APPLICANT, LICENSEE OR INTEREST HOLDER. The listed factors include a consent "
      "agreement resolving a complaint against a pharmacy or other FDA- or DEA-registered entity, and "
      "prior discipline, suspension, denial or revocation of a professional licence or registration.",
      {"A": "Correct: interest holders are named in every factor.",
       "B": "Correct: consent agreements are expressly listed.",
       "C": "The factors reach any pharmacy, health care facility or FDA- or DEA-registered entity.",
       "D": "Correct: professional licence discipline is expressly listed.",
       "E": "Correct: that is the standard the section states."},
      ["MA-PHARMACY-SUITABILITY"],
      ["Identify who the factors reach, not just what they describe",
       "Match the investor's history to the listed factors",
       "Note that the geographic limit the applicant assumes is not in the section"],
      ["Holding prescriptive privileges is itself one of the eleven listed factors"],
      "Candidates read suitability as being about the named applicant's own Massachusetts record."),

    q("MA-Q-0362", "B3E_OWNERSHIP_TRANSFER_DUAL_DUTIES", "Pharmacy licensure", "Transfer of ownership", 4, "SBA",
      "A Massachusetts pharmacy is being sold. Twenty days before the closing date the buyer submits a "
      "complete licence application with the controlled substance inventory report and the bill of sale. "
      "The seller files nothing, on the basis that the buyer's application tells the Board everything it "
      "needs. Is the seller's position sound?",
      [("A", "No, because the outgoing licensee owes the Board its own notice of the transfer."),
       ("B", "No, because the seller must instead surrender the licence to the Board first."),
       ("C", "Yes, because the buyer's application was filed more than 14 days ahead."),
       ("D", "Yes, because the inventory report identifies both pharmacies to the Board."),
       ("E", "Yes, provided the seller countersigns the buyer's licence application.")],
      ["A"],
      "247 CMR 6.11 imposes two separate 14-day duties. At least 14 days before the transfer the "
      "LICENSEE shall notify the Board of the proposed transfer and comply with the closing and "
      "controlled substance distribution provisions; at least 14 days before the transfer the PROPOSED "
      "NEW LICENSEE shall submit its application. One filing does not answer the other duty.",
      {"A": "Correct: the outgoing licensee's notice is a distinct obligation.",
       "B": "Surrender is not what the section requires in place of notice.",
       "C": "Timeliness of the buyer's filing does not discharge the seller's.",
       "D": "The inventory report is an application component, not the seller's notice.",
       "E": "A countersignature is not contemplated by the section."},
      ["MA-PHARMACY-OWNERSHIP-TRANSFER"],
      ["Separate the duty on the outgoing licensee from the duty on the incoming one",
       "Check each against the 14-day clock",
       "Note that the seller must also meet the closing and drug-distribution provisions"],
      ["The Board may test the buyer against the 247 CMR 6.03 suitability factors"],
      "Candidates treat a transfer as a single transaction with a single filing."),

    q("MA-Q-0363", "B3E_CS_TRANSFER_ON_CLOSURE", "Controlled substance procurement", "Transfer between pharmacies", 5, "SATA",
      "A closing Massachusetts pharmacy will move its Schedule II through VI stock to a sister pharmacy. "
      "The Manager of Record has given the Board written certified-mail notice with all required "
      "particulars and the transfer is set for day 15. Which statements about what follows are correct? "
      "Select all that apply.",
      [("A", "The transferor may keep a small residual stock to finish outstanding prescriptions."),
       ("B", "An attestation confirming the inventory is filed with the Board within 30 days."),
       ("C", "The inventory covers Schedules II through V and reportable Schedule VI substances."),
       ("D", "Only the transferee's Manager of Record needs to sign the inventory report."),
       ("E", "The transferor may possess no controlled substances after the transfer date.")],
      ["C", "E"],
      "247 CMR 6.14(2) requires the transferor to take a complete inventory on the transfer date of all "
      "Schedule II through V substances and all Schedule VI substances reportable to the prescription "
      "monitoring program, requires BOTH Managers of Record to sign it, requires an attestation with the "
      "Board WITHIN TEN DAYS, and provides that the transferor pharmacy may not possess any controlled "
      "substances after the transfer date.",
      {"A": "The regulation forecloses any possession after the transfer date.",
       "B": "The attestation window is ten days, not thirty.",
       "C": "Correct: reportable Schedule VI is inside the inventory.",
       "D": "Both Managers of Record sign, subject to the unavailability substitution.",
       "E": "Correct: a flat prohibition after the transfer date."},
      ["MA-CS-TRANSFER-BETWEEN-PHARMACIES"],
      ["Separate the 14-day notice clock from the 10-day attestation clock",
       "Read what the inventory must cover",
       "Apply the post-transfer possession prohibition"],
      ["A staff pharmacist may sign where the transferor Manager of Record is unavailable"],
      "Candidates carry the 14-day figure forward and use it for the attestation as well."),

    q("MA-Q-0364", "B3E_PROVISIONAL_PHARMACY_LICENCE", "Facility licensure", "Provisional licences", 4, "SBA",
      "A Massachusetts sterile compounding applicant has held a provisional licence for eleven months. "
      "It has made real progress but will not reach full compliance for another two months, and asks the "
      "Board to extend the provisional licence for that period. What is the position?",
      [("A", "The Board may extend it once, for a period not exceeding six months."),
       ("B", "The Board may extend it where the applicant shows continued substantial compliance."),
       ("C", "The Board must extend it, since full compliance is the stated objective."),
       ("D", "The Board may convert it now and inspect for full compliance afterwards."),
       ("E", "The provisional licence may not be renewed or extended and lapses at one year.")],
      ["E"],
      "247 CMR 6.17 provides that a provisional licence is valid until the earliest of conversion, "
      "surrender, suspension or revocation, or ONE YEAR from issue, and states flatly that a provisional "
      "licence may not be renewed or extended. Conversion requires the Board to have determined the "
      "pharmacy is in FULL compliance, which has not happened here.",
      {"A": "No extension mechanism exists in the section.",
       "B": "Substantial compliance is the entry test, not a ground for extension.",
       "C": "Nothing obliges the Board to extend.",
       "D": "Conversion follows a determination of full compliance, not precedes it.",
       "E": "Correct: no renewal, no extension, one year outer limit."},
      ["MA-PROVISIONAL-PHARMACY-LICENCE"],
      ["Identify the four events that end a provisional licence",
       "Note the absence of any extension mechanism",
       "Check what conversion requires"],
      ["Substantial compliance plus potential to reach full compliance is the entry test"],
      "Candidates assume a regulator that grants a provisional status will also grant more time."),

    q("MA-Q-0365", "B3E_WHOLESALE_CHANGE_AND_QUALIFICATION", "Wholesale distribution", "Licence maintenance", 4, "SBA",
      "A Massachusetts wholesale drug distributor changes its designated responsible person and its "
      "warehouse address. Its compliance officer plans to report both at the next annual renewal, and "
      "adds that a director's old felony conviction for an offence unrelated to drugs cannot matter to "
      "the Board. Which statement is correct?",
      [("A", "Both points are sound; renewal is the natural time to update the record."),
       ("B", "The reporting plan is sound, but the conviction is a listed Board factor."),
       ("C", "The changes go to the Board within 30 days, and any felony conviction is listed."),
       ("D", "The changes go to the Board within 30 days, but the conviction falls outside the list."),
       ("E", "Neither point matters, because the factors govern issuance rather than renewal.")],
      ["C"],
      "247 CMR 7.02(6) requires changes in the reported information to be submitted to the Board in "
      "writing within 30 days after the change. The minimum factors at 247 CMR 7.02(7) include "
      "convictions under laws relating to drug distribution AND, separately, ANY FELONY CONVICTIONS of "
      "the applicant or licensee, and the factors govern issuing, renewing OR revoking.",
      {"A": "The 30-day clock runs from the change, not to the renewal date.",
       "B": "The reporting plan misses the 30-day requirement.",
       "C": "Correct on both points.",
       "D": "Any felony conviction is expressly listed, whether drug-related or not.",
       "E": "The factors reach renewal and revocation as well as issuance."},
      ["MA-WHOLESALE-CHANGE-AND-QUALIFICATION"],
      ["Locate the change-reporting clock for a wholesale licensee",
       "Read the factor list for the drug-related and the general conviction limbs",
       "Note that the factors govern renewal and revocation too"],
      ["The Board may deny a licence where granting it would not serve the public interest"],
      "Candidates apply a pharmacy-style renewal rhythm to a differently regulated wholesale licence."),

    q("MA-Q-0366", "B3E_CS_REGISTRATION_TERM_BY_TYPE", "Controlled substance registration", "Term and scope", 4, "SBA",
      "A Massachusetts company holds a wholesale druggist controlled substance registration and is "
      "opening a second distribution warehouse in another city. Its counsel says the existing "
      "registration covers the new site and runs on the same two-year cycle as the group's pharmacy "
      "registrations. What is the position?",
      [("A", "Counsel is right on both points, since one registrant holds one registration."),
       ("B", "Counsel is right on coverage but wrong on the cycle, which is three years."),
       ("C", "Counsel is wrong on coverage but right that a two-year cycle applies."),
       ("D", "Counsel is wrong on both: a separate registration is needed and the term is one year."),
       ("E", "Counsel is wrong on coverage, and the wholesale registration has no fixed expiry.")],
      ["D"],
      "247 CMR 11.05 requires a SEPARATE controlled substance registration at each principal place of "
      "business where the registrant manufactures, distributes or dispenses. 247 CMR 11.06 sets terms by "
      "registrant type: two years from January 1st of each even-numbered year for a pharmacy and for an "
      "outsourcing facility, but ONE year from DECEMBER 1st of each year for a wholesale druggist.",
      {"A": "Registration attaches to each principal place of business.",
       "B": "Coverage is wrong and no three-year cycle exists.",
       "C": "The two-year cycle belongs to pharmacies and outsourcing facilities.",
       "D": "Correct on both points.",
       "E": "The wholesale registration has a stated annual expiry."},
      ["MA-CS-REGISTRATION-TERM"],
      ["Apply the separate-registration rule to the second warehouse",
       "Identify the registrant type",
       "Read the term stated for that type"],
      ["The pharmacy and outsourcing facility cycles both begin in even-numbered years"],
      "Candidates assume a single registrant holds a single registration on a single cycle."),

    q("MA-Q-0367", "B3E_NUCLEAR_PHARMACY_SERVICE_SCOPE", "Nuclear pharmacy", "Radiopharmaceutical service", 5, "SATA",
      "A Massachusetts nuclear pharmacy is describing its services to a hospital client. Which "
      "activities fall inside the regulatory definition of radiopharmaceutical service? Select all that "
      "apply.",
      [("A", "Counting, dispensing, labeling and delivery of radiopharmaceuticals."),
       ("B", "Operating the imaging equipment on which the product is later used."),
       ("C", "Interpreting the images produced after the product is administered."),
       ("D", "Prescribing the radiopharmaceutical for the individual hospital patient."),
       ("E", "Advising on therapeutic values, hazards and use of radiopharmaceuticals.")],
      ["A", "E"],
      "247 CMR 13.02 defines radiopharmaceutical service as counting, dispensing, labeling and delivery; "
      "participating in radiopharmaceutical selection and utilization reviews; proper and safe storage "
      "and distribution; maintaining radiopharmaceutical quality assurance; advising on therapeutic "
      "values, hazards and use; and the acts necessary to conduct such services within a nuclear "
      "pharmacy. Imaging operation, image interpretation and prescribing are outside it.",
      {"A": "Correct: the four handling verbs open the definition.",
       "B": "Equipment operation is not within the defined service.",
       "C": "Image interpretation is not within the defined service.",
       "D": "Prescribing is not within the defined service.",
       "E": "Correct: the advisory limb is expressly included."},
      ["MA-NUCLEAR-PHARMACY-SERVICE"],
      ["Read the definition to its end rather than stopping at the handling verbs",
       "Test each described activity against the listed limbs",
       "Exclude activities the definition does not name"],
      ["Radiopharmaceutical quality assurance includes authentication of product history"],
      "Candidates treat everything a nuclear pharmacy touches clinically as part of the defined service."),

    q("MA-Q-0368", "B3E_PROVISIONAL_OUTSOURCING_LIMITS", "Facility licensure", "Outsourcing facility registration", 4, "SBA",
      "A Massachusetts entity holds a provisional outsourcing facility registration because it had not "
      "been inspected by the FDA in the two years before its application. It has compounded a batch of "
      "sterile preparations and wants to ship them to a hospital in the Commonwealth while it waits for "
      "the inspection. May it?",
      [("A", "Yes, because the provisional registration authorises it to operate as a facility."),
       ("B", "Yes, because the shipment stays inside the Commonwealth."),
       ("C", "Yes, provided the receiving hospital records the provisional status."),
       ("D", "No, because a provisional holder is barred from compounding until inspected."),
       ("E", "No, because a provisional holder is permitted to compound but not to supply.")],
      ["E"],
      "247 CMR 21.03(3) provides that an entity with a provisional outsourcing facility registration MAY "
      "COMPOUND sterile drug preparations but MAY NOT DISTRIBUTE OR DISPENSE a sterile drug preparation "
      "within or outside the Commonwealth until it has been inspected by the FDA and has received a "
      "Massachusetts outsourcing facility registration. The permission and the prohibition sit in the "
      "same sentence.",
      {"A": "The registration authorises production, not supply.",
       "B": "The prohibition covers supply within and outside the Commonwealth alike.",
       "C": "No recording by the recipient cures the prohibition.",
       "D": "Compounding is expressly permitted.",
       "E": "Correct: compounding yes, distribution or dispensing no."},
      ["MA-PROVISIONAL-OUTSOURCING-LIMITS"],
      ["Read the permission and the prohibition in the same provision",
       "Note that the geographic reach of the prohibition is both ways",
       "Identify the two conditions that lift it"],
      ["A non-resident outsourcing facility cannot hold a provisional registration at all"],
      "Candidates treat a registration that permits production as permitting supply of what is produced."),

    q("MA-Q-0369", "B3E_THEFT_LOSS_TAMPERING_REPORT", "Mandatory reporting", "Theft, loss or tampering", 3, "SBA",
      "On a Monday a Massachusetts pharmacy discovers that a controlled substance package delivered the "
      "previous Wednesday shows signs of having been opened and resealed. Nothing is confirmed missing. "
      "The Manager of Record plans to investigate for a few days and then decide whether to report. What "
      "does the regulation require?",
      [("A", "A report to the Drug Control Program within 24 hours of Monday's discovery."),
       ("B", "A report to the Board of Registration in Pharmacy within 24 hours of Monday."),
       ("C", "A report to the Drug Control Program within 24 hours of the Wednesday delivery."),
       ("D", "No report, because no controlled substance has been confirmed missing."),
       ("E", "A report once the internal investigation establishes that a loss occurred.")],
      ["A"],
      "105 CMR 700.008 requires a registrant to report the theft, loss OR SUSPECTED TAMPERING of any "
      "controlled substances to the DRUG CONTROL PROGRAM within the Department WITHIN 24 HOURS OF "
      "DISCOVERY, on the form the Drug Control Program provides or approves. Suspected tampering is "
      "itself a trigger, and the clock runs from discovery rather than from the underlying event.",
      {"A": "Correct on the recipient and on the clock.",
       "B": "The report goes to the Drug Control Program.",
       "C": "The clock runs from discovery, not from delivery.",
       "D": "Suspected tampering triggers the duty without a confirmed loss.",
       "E": "Waiting for the investigation would breach the 24-hour requirement."},
      ["MA-THEFT-LOSS-TAMPERING-REPORT"],
      ["Identify the trigger, which includes suspected tampering",
       "Fix the start of the clock at discovery",
       "Identify the recipient as the Drug Control Program"],
      ["The report is made on the form the Drug Control Program provides or approves"],
      "Candidates wait for confirmation of an actual loss before starting a clock that has already run."),
]

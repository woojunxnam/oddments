"""Batch 3 tranche B3-D — 33 Area-2 questions, MA-Q-0328 through MA-Q-0360.

Twelve of the twenty-one families carry two questions. Each pair is separated by a stated material
difference in application, recorded slot by slot in BATCH3-CD-AREA2-ALLOCATION.json.

Structural targets, measured against the Phase-2 pool after B3-C (195 SBA, 122 SATA, answer-position
chi-square 0.8718, SATA three-correct share 46.7%):

  * 21 SBA / 12 SATA.
  * SBA keys weighted D x6 / E x5 / A x4 / B x3 / C x3, chosen to level the released pool once
    B3-C and B3-D are both admitted.
  * SATA correct-counts 2-correct x6 / 4-correct x6, no three-correct item, taking the released
    three-correct share down toward 42%.
  * SATA correct positions spread across all five slots in varied correct-sets, every slot well
    under the 25% concentration threshold.

Citation wording is deliberately varied between questions that rest on the same instrument, so no
ten-token explanation phrase recurs across four or more items.
"""

from __future__ import annotations


def q(qid, family, topic, subtopic, difficulty, qtype, stem, choices, correct,
      core, analysis, rules, steps, facts, trap):
    return {
        "question_id": qid,
        "family_id": family,
        "area": 2,
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
    q("MA-Q-0328", "ADMINISTRATION_CURRENT_ELIGIBLE_PRODUCT_LIST", "Pharmacist administration", "Eligible medications", 4, "SATA",
      "A Massachusetts pharmacist is deciding which injections she may give in the pharmacy under the Department's "
      "current administration guidance. Which statements are correct? Select all that apply.",
      [("A", "A long-acting injectable antipsychotic such as paliperidone palmitate is eligible."),
       ("B", "Testosterone for gender-affirming care is eligible, in any of its salts."),
       ("C", "Cabotegravir for prevention of HIV is eligible for administration."),
       ("D", "Any long-acting injectable is eligible, since the list gives examples of the class."),
       ("E", "The pharmacist is not obliged to administer an eligible medication on request.")],
      ["A", "B", "C", "E"],
      "The Department's current circular states that the generic medications it lists are THE ONLY medications "
      "eligible to be administered by a pharmacist or pharmacy intern, and names long-acting injectable "
      "antipsychotics, long-acting injectables for substance use disorders, testosterone in all salts, HIV "
      "prevention medications and sexually transmitted infection medications. It also states there is no "
      "requirement for a pharmacist or intern to administer them.",
      {"A": "Correct: named among the long-acting injectable antipsychotics.",
       "B": "Correct: testosterone, all salts, for gender-affirming care.",
       "C": "Correct: named among the HIV prevention medications.",
       "D": "The list is closed, not illustrative of a wider class.",
       "E": "Correct: administration is voluntary for the pharmacist."},
      ["MA-ADMIN-ELIGIBLE-MEDICATIONS"],
      ["Check whether the medication appears on the closed list",
       "Separate eligibility from any obligation to act",
       "Resist reading the list as examples of a broader category"],
      ["The list is stated by generic name and may cover several brand names"],
      "Candidates generalise from the listed products to the pharmacological class they belong to."),

    q("MA-Q-0329", "ADMINISTRATION_OTP_ORDER_ONLY", "Pharmacist administration", "Opioid treatment programs", 3, "SBA",
      "A patient asks a Massachusetts community pharmacist to administer methadone for addiction treatment. The "
      "patient presents a valid prescription from a practitioner, and the pharmacist has completed injection "
      "training and holds current CPR certification. May the pharmacist administer it there?",
      [("A", "Yes, because the pharmacist holds a valid prescription for the patient."),
       ("B", "Yes, because the pharmacist has completed the required training and certification."),
       ("C", "No, because that administration may occur only in a registered opioid treatment program."),
       ("D", "No, because a pharmacist may never administer any medication for addiction treatment."),
       ("E", "No, unless the prescriber attends the pharmacy at the time of administration.")],
      ["C"],
      "The regulation at 105 CMR 700.004(B)(9)(e) authorises a pharmacist to administer controlled substances in "
      "an Opioid Treatment Program pursuant to an order, and the Department's circular states that a pharmacist may "
      "administer medications for addiction treatment, including methadone, pursuant to an order, ONLY in a "
      "registered opioid treatment program. The setting is closed and the instrument is an order.",
      {"A": "A prescription is not the instrument this pathway uses.",
       "B": "Training and certification do not open a pathway limited by setting.",
       "C": "Correct: the registered programme is the only place, and the instrument is an order.",
       "D": "Buprenorphine and naltrexone injections are eligible in the ordinary pathway.",
       "E": "Prescriber attendance is not the condition in issue."},
      ["MA-ADMIN-OTP-ORDER-ONLY", "MA-ADMIN-ELIGIBLE-MEDICATIONS"],
      ["Identify the medication as one for addiction treatment",
       "Identify the setting the pathway requires",
       "Note that the instrument is an order rather than a prescription"],
      ["Long-acting injectable buprenorphine and naltrexone sit on the eligible list"],
      "Candidates reason from the pharmacist's competence and paperwork instead of from the setting the rule names."),

    q("MA-Q-0330", "ADMINISTRATION_PRESCRIPTION_NOTATION_AND_CONTACT", "Pharmacist administration", "Prescriber communication", 4, "SBA",
      "A prescription for an eligible long-acting injectable arrives at a Massachusetts pharmacy without the "
      "administration notation the Department's guidance asks prescribers to include. In the pharmacist's judgment "
      "the product is plainly intended to be given in the pharmacy rather than handed to the patient. What does the "
      "guidance call for?",
      [("A", "The pharmacist is encouraged to contact the prescriber, and administration stays open."),
       ("B", "The pharmacist must refuse to administer until a corrected prescription arrives."),
       ("C", "The pharmacist must dispense the product to the patient rather than administer it."),
       ("D", "The pharmacist must obtain the prescriber's written confirmation before proceeding."),
       ("E", "The pharmacist must record the omission and report it to the Board within 24 hours.")],
      ["A"],
      "Under the Pharmacist-Prescriber Communication heading of the current circular, prescribers SHOULD include an "
      "administration notation, and a pharmacist receiving a prescription for eligible medications without it is "
      "ENCOURAGED to contact the prescriber where it appears the medication is intended to be administered. The "
      "guidance is hortatory; it does not make the notation a condition of administering.",
      {"A": "Correct: contact is encouraged, and the missing notation is not disqualifying.",
       "B": "The circular does not make the notation a precondition.",
       "C": "Nothing requires the pharmacist to convert the intent into a hand-out dispensing.",
       "D": "Written confirmation is not what the guidance asks for.",
       "E": "No Board report arises from a missing notation."},
      ["MA-ADMIN-PRESCRIPTION-NOTATION"],
      ["Locate the notation guidance and read whether it says shall or should",
       "Read what the receiving pharmacist is told to do when it is absent",
       "Distinguish encouragement from a condition of lawful administration"],
      ["Pharmacists are strongly encouraged to send administration records to prescribers"],
      "Candidates convert guidance a document is expected to carry into a mandatory element of validity."),

    q("MA-Q-0331", "ADMINISTRATION_ROUTE_SC_IM_ONLY", "Pharmacist administration", "Route of administration", 4, "SATA",
      "A Massachusetts pharmacist is asked to give an eligible medication in the pharmacy. Which statements about "
      "the permitted route are correct? Select all that apply.",
      [("A", "An intravenous infusion is permitted where the pharmacist is trained to place a line."),
       ("B", "Any parenteral route is permitted so long as the product label allows it."),
       ("C", "The route is at the pharmacist's professional discretion for an eligible product."),
       ("D", "Administration must accord with manufacturer approved labeling for the product."),
       ("E", "Only subcutaneous or intramuscular injection is permitted.")],
      ["D", "E"],
      "The Administration and Dosing section of the current circular provides that a pharmacist or pharmacy intern "
      "may ONLY administer an eligible medication by subcutaneous or intramuscular injection, in accordance with "
      "manufacturer approved labeling and any risk evaluation and mitigation strategy requirements for the specific "
      "medication. The conditions on dispensing by administration separately state that administration is not "
      "intravenous.",
      {"A": "Administration is expressly not intravenous, whatever the pharmacist's skill.",
       "B": "Only two routes are open, not every parenteral route.",
       "C": "The route is fixed by the guidance rather than left to discretion.",
       "D": "Correct: manufacturer approved labeling governs.",
       "E": "Correct: subcutaneous or intramuscular only."},
      ["MA-ADMIN-ROUTE-AND-DOSING"],
      ["Read the route limitation in the Administration and Dosing section",
       "Read the separate condition that administration is not intravenous",
       "Apply the manufacturer labeling and risk-strategy overlay"],
      ["Ceftriaxone appears on the eligible list specifically as an intramuscular injection"],
      "Candidates treat injection competence as the test and infer that a trained pharmacist may use any route."),

    q("MA-Q-0332", "ADMINISTRATION_ROUTE_SC_IM_ONLY", "Pharmacist administration", "Single-dose condition", 5, "SBA",
      "A Massachusetts prescriber writes for an eligible injectable to be administered in the pharmacy, specifying "
      "a single dose with three refills. The pharmacy manager says the refills make the prescription unusable for "
      "administration because the conditions require single doses. Who is right?",
      [("A", "The manager, because refills convert it into a course of therapy."),
       ("B", "The manager, because each administration needs its own prescription."),
       ("C", "The manager, unless the prescriber confirms the intent in writing."),
       ("D", "The pharmacist, because single-dose prescribing may carry refills."),
       ("E", "The pharmacist, because the single-dose condition governs packaging only.")],
      ["D"],
      "Among the conditions for dispensing by administration, the medication must be available in single-dose "
      "packaging AND prescribed in single doses, WITH OR WITHOUT REFILLS. The condition therefore controls how each "
      "dose is prescribed and packaged, and expressly tolerates refills, so a single dose with three refills "
      "satisfies it.",
      {"A": "The condition contemplates refills in terms.",
       "B": "No rule requires a fresh prescription for each administration.",
       "C": "No prescriber confirmation is required to cure a condition that is already met.",
       "D": "Correct: the words with or without refills answer the point.",
       "E": "The condition reaches both the packaging and the prescribing."},
      ["MA-ADMIN-ROUTE-AND-DOSING"],
      ["Read the single-dose condition in full, including its closing words",
       "Separate the packaging limb from the prescribing limb",
       "Apply the express tolerance of refills"],
      ["Prescribers must reassess the patient and prescription at appropriate intervals"],
      "Candidates read single doses as excluding repetition and stop before the words that permit it."),

    q("MA-Q-0333", "CDTM_FACILITY_MEDICATION_ORDER_INSTRUMENT", "Collaborative practice", "Prescribing in a facility", 4, "SBA",
      "A Massachusetts collaborating pharmacist rounding in a licensed long-term care facility decides to start a "
      "controlled substance for a resident. She writes what looks like an ordinary outpatient prescription and "
      "leaves it at the nurses' station. What does the regulation require instead?",
      [("A", "A prescription transmitted to the facility's contracted dispensing pharmacy."),
       ("B", "A written medication order entered on the facility's own medical record for the resident."),
       ("C", "A countersignature from the supervising physician on the prescription she wrote."),
       ("D", "An oral order to the nurse on duty, confirmed in writing within 24 hours."),
       ("E", "A referral back to the supervising physician, who must issue the order himself.")],
      ["B"],
      "Where the patient is in a licensed health facility, including a hospital, long-term care facility, "
      "ambulatory care clinic or hospice, 105 CMR 700.003(G)(8) authorises the pharmacist to prescribe THROUGH THE "
      "USE OF A WRITTEN MEDICATION ORDER ENTERED ON THE PATIENT'S MEDICAL RECORD MAINTAINED AT THE FACILITY, "
      "provided that order meets all applicable provisions of the regulation.",
      {"A": "The instrument is a medication order on the facility record, not a transmitted prescription.",
       "B": "Correct: a written medication order on the facility's record.",
       "C": "No countersignature is required by the paragraph.",
       "D": "The paragraph specifies a written order, not an oral one.",
       "E": "The pharmacist's own prescribing authority is not displaced."},
      ["MA-CDTM-FACILITY-ORDER"],
      ["Confirm the patient is in a licensed health facility",
       "Identify the instrument the paragraph authorises there",
       "Note where the order must be entered"],
      ["The order must still meet all applicable provisions of 105 CMR 700.000"],
      "Candidates carry the outpatient prescription habit into a setting the regulation treats differently."),

    q("MA-Q-0334", "CDTM_FACILITY_MEDICATION_ORDER_INSTRUMENT", "Collaborative practice", "Facility boundary", 4, "SBA",
      "A Massachusetts collaborating pharmacist provides services on site at an assisted living residence that "
      "holds no health facility licence. She proposes to use a written medication order entered on the residence's "
      "own care record, as she does when working in a licensed hospice. What is the position?",
      [("A", "Permitted, because a written order is more rigorous than a prescription."),
       ("B", "Permitted, because the residence maintains a care record for each resident."),
       ("C", "Permitted, provided the supervising physician approves the residence in the agreement."),
       ("D", "Not permitted, because the medication order route is unavailable outside a facility."),
       ("E", "Not permitted, because a pharmacist may not provide services at a residence at all.")],
      ["D"],
      "The medication order route in 105 CMR 700.003(G)(8) is expressly framed for a patient IN A LICENSED HEALTH "
      "FACILITY, the paragraph listing a hospital, long-term care facility, ambulatory care clinic or hospice. An "
      "unlicensed residence is none of those, so the instrument the paragraph authorises is simply not available "
      "there, whatever record the residence keeps.",
      {"A": "Rigour is not the test; the setting is.",
       "B": "A care record is not a facility medical record for this purpose.",
       "C": "The agreement cannot confer a route the regulation limits by setting.",
       "D": "Correct: the route depends on the facility being licensed.",
       "E": "The pharmacist is not barred from providing services there."},
      ["MA-CDTM-FACILITY-ORDER"],
      ["Test the setting against the list in the paragraph",
       "Note that licensure is what the paragraph turns on",
       "Conclude that the instrument is unavailable rather than merely irregular"],
      ["The listed facilities are licensed under M.G.L. c. 111, ss. 51, 57D and 71"],
      "Candidates transplant an instrument that worked in one setting to a superficially similar one."),

    q("MA-Q-0335", "CDTM_IMMEDIATE_TREATMENT_PROCUREMENT_CHANNEL", "Collaborative practice", "Supply for immediate treatment", 4, "SATA",
      "A Massachusetts collaborating pharmacist plans to hold stock for dispensing for immediate treatment under "
      "her agreement. Which statements about how she may obtain it are correct? Select all that apply.",
      [("A", "Any product she may prescribe may be bought from her usual wholesaler."),
       ("B", "A Schedule IV product may be bought from a wholesaler for this purpose."),
       ("C", "Schedule VI products she is authorised to prescribe may be ordered from a wholesaler."),
       ("D", "Schedule II to V products may be bought from a distributor if properly recorded."),
       ("E", "Schedule II to V products may come from the supervising physician or a patient's order.")],
      ["C", "E"],
      "105 CMR 700.003(G)(6) permits ordering from a drug wholesaler, manufacturer, laboratory or distributor, for "
      "purposes of dispensing for immediate treatment, only those controlled substances IN SCHEDULE VI which the "
      "pharmacist is authorised to prescribe. For Schedules II through V dispensed for immediate treatment, the "
      "pharmacist may obtain the substances ONLY as supplied by the supervising physician or obtained through a "
      "prescription or medication order for the patient.",
      {"A": "The channel turns on the schedule, not on prescribing authority alone.",
       "B": "Wholesaler purchase is closed for Schedules II through V in this pathway.",
       "C": "Correct: Schedule VI may be ordered from those sources.",
       "D": "Record keeping does not open a channel the regulation closes.",
       "E": "Correct: those are the only two routes for Schedules II through V."},
      ["MA-CDTM-IMMEDIATE-TREATMENT-SUPPLY"],
      ["Classify the product by schedule",
       "Apply the wholesaler route to Schedule VI only",
       "Apply the physician-supply or patient-specific route to Schedules II through V"],
      ["The pharmacist must also be authorised under 700.003(G) to prescribe the substance"],
      "Candidates assume that a pharmacy entitled to buy a product for dispensing may buy it for any purpose."),

    q("MA-Q-0336", "CDTM_IMMEDIATE_TREATMENT_PROCUREMENT_CHANNEL", "Collaborative practice", "Precondition on the power", 5, "SBA",
      "A Massachusetts collaborating pharmacist holds a Department registration for the purpose of prescribing and "
      "a valid agreement. She wishes to dispense a Schedule VI product for immediate treatment. That particular "
      "product is not among those her agreement authorises her to prescribe. May she do so?",
      [("A", "Yes, because immediate treatment is a separate power from prescribing."),
       ("B", "Yes, because the product sits in Schedule VI, the least restricted schedule."),
       ("C", "Yes, provided she notifies the supervising physician within 24 hours."),
       ("D", "No, because the power runs only to substances she is authorised to prescribe."),
       ("E", "No, because dispensing for immediate treatment requires a patient-specific order.")],
      ["D"],
      "The immediate-treatment power at 105 CMR 700.003(G)(5) is expressly conditioned: the pharmacist may dispense "
      "a controlled substance for immediate treatment PROVIDED the pharmacist is authorized by 700.003(G) to "
      "prescribe such controlled substance. Prescribing authority for that substance is the gate, and holding a "
      "prescribing-purpose registration does not supply it.",
      {"A": "The two powers are linked by an express proviso.",
       "B": "Schedule alone does not answer the proviso.",
       "C": "Notification does not cure a missing precondition.",
       "D": "Correct: the proviso ties the power to what she may prescribe.",
       "E": "A patient-specific order is the supply route for other schedules, not the gate here."},
      ["MA-CDTM-IMMEDIATE-TREATMENT-SUPPLY"],
      ["Read the proviso attached to the immediate-treatment power",
       "Check whether the agreement authorises prescribing of this substance",
       "Separate registration from agreement authority"],
      ["Schedule VI stock for this purpose may be ordered from a wholesaler"],
      "Candidates treat immediate-treatment dispensing as an emergency power standing on its own."),

    q("MA-Q-0337", "CDTM_ISSUE_MODIFY_DISCONTINUE_POWERS", "Collaborative practice", "Prescribing powers", 4, "SBA",
      "A Massachusetts collaborative practice agreement authorises the pharmacist to modify the dosage of a named "
      "medication for a referred patient. Reviewing the patient, the pharmacist judges the medication should be "
      "stopped altogether. The agreement says nothing about stopping therapy. What may she do?",
      [("A", "She may not discontinue it, because that act must itself be authorised."),
       ("B", "She may discontinue it, because stopping is a lesser step than modifying."),
       ("C", "She may discontinue it, because it is a clinical rather than a prescribing act."),
       ("D", "She may discontinue it once she notes the reason in the patient's record."),
       ("E", "She may discontinue it only where the medication is in Schedule VI.")],
      ["A"],
      "The opening words of 105 CMR 700.003(G) give the pharmacist power to ISSUE, MODIFY OR DISCONTINUE a "
      "prescription or medication order AS AUTHORIZED IN a collaborative practice agreement. Discontinuation is one "
      "of three separately regulated acts, so authority to modify does not by implication carry authority to "
      "discontinue.",
      {"A": "Correct: each of the three acts must be authorised in the agreement.",
       "B": "The regulation treats them as parallel acts, not as degrees of one act.",
       "C": "Discontinuation is expressly a regulated prescribing act.",
       "D": "A record entry does not supply missing authority.",
       "E": "The schedule is not what the opening words turn on."},
      ["MA-CDTM-PRESCRIBING-POWERS"],
      ["Identify the three acts the regulation names",
       "Check which of them this agreement authorises",
       "Treat the unlisted act as unauthorised"],
      ["The agreement must meet 247 CMR 16.00, 243 CMR 2.12 and M.G.L. c. 112, s. 24B1/2"],
      "Candidates rank the acts by clinical seriousness and assume the greater authority includes the lesser."),

    q("MA-Q-0338", "CDTM_PRESCRIBING_PURPOSE_REGISTRATION", "Collaborative practice", "Prescribing registration", 4, "SBA",
      "A Massachusetts pharmacist holds a current Department controlled substance registration that she obtained so "
      "that her pharmacy could dispense. She now has a valid collaborative practice agreement that includes "
      "prescriptive practices, and proposes to issue her first prescription. What does she still need?",
      [("A", "Nothing further; her current registration covers controlled substance activity."),
       ("B", "A separate Board of Registration in Pharmacy licence category for prescribers."),
       ("C", "The supervising physician's registration number recorded in the agreement."),
       ("D", "A DEA registration, which is required for every collaborating pharmacist."),
       ("E", "Department registration for the purpose of prescribing under 105 CMR 700.000.")],
      ["E"],
      "The condition at 105 CMR 700.003(G)(2) is that the pharmacist registers with the Department in accordance "
      "with 105 CMR 700.004, and with the DEA if applicable, FOR THE PURPOSE OF PRESCRIBING. The purpose of the "
      "registration is part of the requirement, so a registration obtained for dispensing does not carry prescribing "
      "authority.",
      {"A": "The purpose for which the registration was obtained is the point.",
       "B": "No separate Board licence category exists for this.",
       "C": "The physician's number is not the requirement in issue.",
       "D": "The federal limb applies only if applicable.",
       "E": "Correct: registration for the purpose of prescribing."},
      ["MA-CDTM-PRESCRIBING-REGISTRATION"],
      ["Read the purpose clause attached to the registration requirement",
       "Compare it with the purpose of the registration she holds",
       "Note that the DEA limb is conditional"],
      ["247 CMR 16.02(1)(f) separately requires the registration to be maintained during the term"],
      "Candidates treat a controlled substance registration as a single undifferentiated permission."),

    q("MA-Q-0339", "CDTM_PRESCRIBING_PURPOSE_REGISTRATION", "Collaborative practice", "Federal registration limb", 5, "SBA",
      "Two Massachusetts collaborating pharmacists each hold Department registration for the purpose of prescribing. "
      "One will prescribe only Schedule VI products under her agreement. The other will prescribe products in "
      "federally controlled schedules. Neither holds a DEA registration. What follows?",
      [("A", "Both are barred, because the regulation requires DEA registration of prescribers."),
       ("B", "Neither is barred, because Department registration is the operative requirement."),
       ("C", "The first may prescribe; the second needs DEA registration because it applies."),
       ("D", "The second may prescribe; the first needs DEA registration for Schedule VI."),
       ("E", "Both may prescribe, provided each notifies the DEA of the agreement's terms.")],
      ["C"],
      "The registration condition names the DEA limb as applying IF APPLICABLE, in accordance with 21 CFR 1300. "
      "Where the substances the pharmacist will prescribe are federally controlled the limb bites; where they are "
      "not, it does not. The conditional wording is doing real work and is not a formality.",
      {"A": "The federal limb is expressly conditional.",
       "B": "The federal limb bites where the substances are federally controlled.",
       "C": "Correct: applicability turns on what will be prescribed.",
       "D": "This reverses the analysis.",
       "E": "Notification is not a substitute for registration where it is required."},
      ["MA-CDTM-PRESCRIBING-REGISTRATION"],
      ["Read the if applicable qualifier on the federal limb",
       "Ask what each pharmacist will actually prescribe",
       "Apply the limb only where the substances are federally controlled"],
      ["Massachusetts Schedule VI has no federal counterpart schedule"],
      "Candidates read a conditional cross-reference as boilerplate and apply it uniformly or not at all."),

    q("MA-Q-0340", "CDTM_RETAIL_AGE_AND_30_DAY_EXTENSION", "Collaborative practice", "Retail limits", 4, "SATA",
      "A Massachusetts pharmacist practising collaboratively in a retail drug business is reviewing what the "
      "statute permits her to do there. Which statements are correct? Select all that apply.",
      [("A", "Patients must be 18 years of age or older in that setting."),
       ("B", "She may initiate new therapy for a referred patient's primary diagnosis."),
       ("C", "She may extend current therapy prescribed by the supervising physician by 30 days."),
       ("D", "She may modify dosages of any medication the patient is currently taking."),
       ("E", "She may administer vaccines under the terms of her agreement.")],
      ["A", "C"],
      "M.G.L. c. 112, s. 24B1/2(c)(5) limits retail collaborative practice to patients 18 years of age or older, to "
      "an extension by 30 days of current drug therapy PRESCRIBED BY THE SUPERVISING PHYSICIAN, and to "
      "administration of vaccines or the modification of dosages of medications prescribed by the supervising "
      "physician for the named disease states. Option E overstates the vaccine limb by dropping the disease-state "
      "and agreement conditions that frame the whole paragraph, and option D drops the requirement that the "
      "supervising physician prescribed the medication.",
      {"A": "Correct: the age floor applies in the retail setting.",
       "B": "The retail power extends existing therapy rather than initiating new therapy.",
       "C": "Correct: a 30 day extension of the physician's current therapy.",
       "D": "Only medications prescribed by the supervising physician for the named conditions.",
       "E": "The vaccine limb is conditioned by the same paragraph and is not free-standing."},
      ["MA-CDTM-RETAIL-AGE-EXTENSION"],
      ["Apply the age floor",
       "Read the extension power as attaching to the physician's own prescription",
       "Read the modification power as limited to the named disease states"],
      ["The agreement must specifically reference each disease state being co-managed"],
      "Candidates read the retail powers as a general clinical mandate rather than a narrow list."),

    q("MA-Q-0341", "CDTM_RETAIL_AGE_AND_30_DAY_EXTENSION", "Collaborative practice", "Extension power", 4, "SBA",
      "A referred patient at a Massachusetts retail pharmacy has run out of a medication her supervising physician "
      "prescribed, and the physician is unreachable. The collaborating pharmacist has never dispensed this patient "
      "a different medication for the same condition. What may the pharmacist do under the retail collaborative "
      "power?",
      [("A", "Initiate an equivalent medication for the same condition for up to 30 days."),
       ("B", "Extend the current therapy the supervising physician prescribed by 30 days."),
       ("C", "Extend the current therapy indefinitely until the physician can be reached."),
       ("D", "Substitute a therapeutically similar agent and notify the physician afterwards."),
       ("E", "Nothing, because the retail setting confers no continuation power at all.")],
      ["B"],
      "The retail limb of the statute confers an extension by 30 days of CURRENT drug therapy PRESCRIBED BY THE "
      "SUPERVISING PHYSICIAN. It is a continuation power over the physician's own therapy, not a power to start "
      "something new, and it is bounded at 30 days.",
      {"A": "Initiating a different medication is outside the retail power.",
       "B": "Correct: a 30 day extension of the existing therapy.",
       "C": "The power is bounded at 30 days.",
       "D": "Substitution is not what the paragraph confers.",
       "E": "The paragraph does confer a continuation power."},
      ["MA-CDTM-RETAIL-AGE-EXTENSION"],
      ["Confirm the therapy was prescribed by the supervising physician",
       "Apply the extension power rather than an initiation power",
       "Observe the 30 day boundary"],
      ["Retail collaborative patients must be 18 years of age or older"],
      "Candidates reach for the clinically sensible answer of an equivalent agent, which the statute does not confer."),

    q("MA-Q-0342", "CDTM_SETTING_APPROVAL_AUTHORITY_MATRIX", "Collaborative practice", "Approval authorities", 4, "SATA",
      "A Massachusetts health system is setting up collaborative drug therapy management across several of its "
      "sites. Which statements about who must approve it are correct? Select all that apply.",
      [("A", "In a licensed hospital, the medical staff executive committee or designee approves."),
       ("B", "A single system-wide approval suffices for every one of the listed settings."),
       ("C", "In a long-term care facility, the facility's medical director or designee approves."),
       ("D", "In a hospice setting, the hospice's medical director or designee approves."),
       ("E", "An ambulatory care clinic additionally requires on-site physician supervision.")],
      ["A", "C", "D", "E"],
      "The settings limb of the statute names a different approving body for each setting: the medical staff "
      "executive committee or designee in a licensed hospital, the medical director or designee in a long-term care "
      "facility, the hospice's medical director or designee in inpatient or outpatient hospice, and the clinic's "
      "medical staff executive committee or medical director or designee for an ambulatory care clinic, which "
      "uniquely also requires on-site supervision by the attending physician and a collaborating pharmacist.",
      {"A": "Correct: hospital approval runs through the medical staff executive committee.",
       "B": "Each setting carries its own approval route.",
       "C": "Correct: the long-term care facility medical director.",
       "D": "Correct: the hospice medical director.",
       "E": "Correct: on-site supervision is unique to the ambulatory care clinic."},
      ["MA-CDTM-SETTING-APPROVAL"],
      ["Take each setting in turn",
       "Match it to the approving body the statute names",
       "Note the extra on-site supervision condition for ambulatory care clinics"],
      ["Hospitals and ambulatory care clinics are both licensed under M.G.L. c. 111, s. 51"],
      "Candidates look for one governance route because the sites belong to one organisation."),

    q("MA-Q-0343", "CDTM_SETTING_APPROVAL_AUTHORITY_MATRIX", "Collaborative practice", "Ambulatory care condition", 4, "SBA",
      "A Massachusetts ambulatory care clinic has obtained approval from its medical staff executive committee for "
      "collaborative drug therapy management. The collaborating pharmacist works remotely from another site, "
      "reviewing records and speaking to patients by telephone. No physician is present with her. Is the "
      "arrangement compliant?",
      [("A", "Yes, because the correct approving body has approved the arrangement."),
       ("B", "Yes, because the statute does not regulate where the pharmacist works."),
       ("C", "Yes, provided the attending physician is reachable during clinic hours."),
       ("D", "No, because the clinic setting requires on-site supervision by the attending physician."),
       ("E", "No, because collaborative practice may not be conducted in an ambulatory care clinic.")],
      ["D"],
      "The ambulatory care clinic limb of the statute carries a condition none of the other listed settings does: "
      "collaborative practice there is permitted WITH ON-SITE SUPERVISION BY THE ATTENDING PHYSICIAN AND A "
      "COLLABORATING PHARMACIST, subject to approval by the clinic's medical staff executive committee or "
      "designee, or medical director or designee. Approval and on-site supervision are cumulative.",
      {"A": "Approval satisfies one condition; on-site supervision is another.",
       "B": "The statute expressly attaches an on-site condition in this setting.",
       "C": "Reachability is not the same as on-site supervision.",
       "D": "Correct: on-site supervision is required in this setting.",
       "E": "Ambulatory care clinics are an authorised setting."},
      ["MA-CDTM-SETTING-APPROVAL"],
      ["Identify the setting as an ambulatory care clinic",
       "Read the on-site supervision condition attached to it",
       "Treat approval and supervision as cumulative"],
      ["No other listed setting carries an on-site supervision condition"],
      "Candidates check the approval box and stop, because approval is the condition every setting shares."),

    q("MA-Q-0344", "CDTM_VACCINE_ADMINISTRATION_ROUTE", "Collaborative practice", "Vaccine authority route", 3, "SBA",
      "A Massachusetts community pharmacist holds a current collaborative practice agreement that authorises her to "
      "administer vaccines. There is no Commissioner order in force for any designated vaccine, and the vaccine she "
      "is asked to give is not on the Department's eligible-medication administration list. May she give it?",
      [("A", "Yes, because the collaborative practice agreement authorises vaccine administration."),
       ("B", "Yes, because vaccines fall outside the controlled substance framework entirely."),
       ("C", "No, because a Commissioner order is needed before any vaccine may be given."),
       ("D", "No, because the vaccine is absent from the eligible-medication list."),
       ("E", "No, because a pharmacist may administer vaccines only in a hospital setting.")],
      ["A"],
      "247 CMR 16.03(5)(b) provides that pharmacists, AS AUTHORIZED PURSUANT TO A COLLABORATIVE PRACTICE AGREEMENT, "
      "may administer vaccines. That is a distinct route from the emergency Commissioner-order pathway and from the "
      "Drug Control Program eligible-medication pathway, and it does not borrow their conditions.",
      {"A": "Correct: the agreement is the source of the authority here.",
       "B": "The route matters even if the framework does not.",
       "C": "The Commissioner order gates a different, emergency pathway.",
       "D": "That list governs the separate medication-administration pathway.",
       "E": "Community pharmacies are expressly within the collaborative setting list."},
      ["MA-CDTM-VACCINE-ADMINISTRATION"],
      ["Identify which of the administration routes the facts engage",
       "Read the collaborative route as free-standing",
       "Refuse to import conditions from the other two routes"],
      ["The retail restrictions in 247 CMR 16.03(5) still apply to the agreement"],
      "Candidates blend three separate administration pathways into a single set of conditions."),

    q("MA-Q-0345", "CONTRACEPTION_NO_APPOINTMENT_CONDITION", "Pharmacist prescribing", "Access conditions", 3, "SBA",
      "A busy Massachusetts pharmacy decides that patients wanting the pharmacist to prescribe a hormonal "
      "contraceptive must book a slot in advance so the pharmacist can plan her day. Walk-ins are told to come back "
      "at a booked time. Is that policy permissible?",
      [("A", "Yes, because appointment scheduling is ordinary workflow management."),
       ("B", "Yes, provided the earliest available slot is within seven days."),
       ("C", "Yes, provided the pharmacy also offers a walk-in service one day a week."),
       ("D", "No, because the patient must instead be referred to a prescriber."),
       ("E", "No, because requiring an appointment for this service is prohibited.")],
      ["E"],
      "The rules adopted under M.G.L. c. 94C, s. 19F(b) must PROHIBIT a pharmacist from requiring a patient to "
      "schedule an appointment with the pharmacist for the prescribing or dispensing of a hormonal contraceptive "
      "patch or self-administered oral hormonal contraceptive. The prohibition is on requiring an appointment, "
      "however reasonable the operational motive.",
      {"A": "The statute removes this particular workflow tool for this service.",
       "B": "No timeliness proviso rescues a requirement to book.",
       "C": "A limited walk-in window does not cure a requirement imposed the rest of the week.",
       "D": "Referral is not the answer; the service is the pharmacist's to provide.",
       "E": "Correct: requiring an appointment is prohibited."},
      ["MA-CONTRACEPTION-NO-APPOINTMENT"],
      ["Identify the service as pharmacist prescribing of hormonal contraception",
       "Read the express prohibition on requiring an appointment",
       "Distinguish requiring an appointment from offering one"],
      ["A pharmacist may still offer an appointment the patient is free to decline"],
      "Candidates weigh the operational reasonableness of the policy instead of applying an express prohibition."),

    q("MA-Q-0346", "CONTRACEPTION_POST_PRESCRIBING_DUTIES", "Pharmacist prescribing", "Post-prescribing duties", 4, "SATA",
      "A Massachusetts pharmacist has just prescribed and dispensed a self-administered oral hormonal contraceptive "
      "after completing the required screening. Which duties attach at that point? Select all that apply.",
      [("A", "Refer the patient to her primary care or reproductive health care practitioner, if applicable."),
       ("B", "Alternatively advise the patient to consult with such a practitioner."),
       ("C", "Provide the patient with a written record of what was prescribed and dispensed."),
       ("D", "Obtain the practitioner's agreement before the supply may be handed over."),
       ("E", "Dispense as soon as practicable after issuing the prescription.")],
      ["A", "B", "C", "E"],
      "Under M.G.L. c. 94C, s. 19F(c)(i), the rules must require the pharmacist to refer the patient to her primary "
      "care or reproductive health care practitioner, if applicable, upon prescribing and dispensing, OR advise her "
      "to consult with such a practitioner; to provide a written record of the product prescribed and dispensed; "
      "and to dispense as soon as practicable after the prescription is issued.",
      {"A": "Correct: referral where a practitioner relationship applies.",
       "B": "Correct: the statute frames advice to consult as the alternative.",
       "C": "Correct: a written record goes to the patient.",
       "D": "No practitioner agreement gates the supply.",
       "E": "Correct: dispensing follows as soon as practicable."},
      ["MA-CONTRACEPTION-POST-PRESCRIBING"],
      ["List the duties that attach on prescribing and dispensing",
       "Note that referral and advice to consult are alternatives",
       "Note the timing duty attaching to the dispensing"],
      ["A self-screening risk assessment tool must be used before prescribing"],
      "Candidates add a prescriber sign-off that the statute deliberately does not require."),

    q("MA-Q-0347", "CONTRACEPTION_POST_PRESCRIBING_DUTIES", "Pharmacist prescribing", "Timing of supply", 4, "SBA",
      "A Massachusetts pharmacist completes the screening and issues a prescription for a hormonal contraceptive "
      "patch on a Friday afternoon. She tells the patient the pharmacy will order the product and asks her to "
      "return the following week to collect it, although an equivalent product is in stock. Is that consistent with "
      "the statute?",
      [("A", "Yes, because the prescribing duty and the dispensing decision are separate."),
       ("B", "Yes, because the patient suffers no clinical detriment from a short wait."),
       ("C", "Yes, provided the pharmacist gives the patient the written record on the Friday."),
       ("D", "No, because the statute requires dispensing as soon as practicable after issuing."),
       ("E", "No, because a pharmacist may not issue a prescription she cannot fill that day.")],
      ["D"],
      "One of the duties the rules must impose under s. 19F(c)(i) is that the pharmacist DISPENSE THE PRODUCT AS "
      "SOON AS PRACTICABLE AFTER THE PHARMACIST ISSUES THE PRESCRIPTION. Asking a patient to return next week for a "
      "product an equivalent of which is on the shelf is not dispensing as soon as practicable.",
      {"A": "The statute ties the two together in time.",
       "B": "The test is practicability, not demonstrated detriment.",
       "C": "The written record is a separate duty and does not answer the timing one.",
       "D": "Correct: the timing duty is breached on these facts.",
       "E": "The statute regulates the timing of supply, not the power to issue."},
      ["MA-CONTRACEPTION-POST-PRESCRIBING"],
      ["Identify the timing duty among the post-prescribing duties",
       "Ask what was practicable on the day",
       "Separate the timing duty from the written-record duty"],
      ["The pharmacist must also refer the patient or advise her to consult a practitioner"],
      "Candidates treat prescribing and dispensing as independent transactions that may be scheduled apart."),

    q("MA-Q-0348", "EMERGENCY_VACCINE_COMMISSIONER_ORDER_GATE", "Public health", "Emergency vaccine gate", 4, "SATA",
      "A Massachusetts pharmacy proposes to run a walk-in clinic for a newly designated vaccine during a public "
      "health event. Which statements about what must be in place are correct? Select all that apply.",
      [("A", "A practitioner standing prescription alone opens this pathway."),
       ("B", "The Commissioner must determine that health care professionals will be insufficient."),
       ("C", "A Commissioner order authorizing the administration removes any need for a prescription."),
       ("D", "Administration must accord with the Commissioner's order as well as a practitioner instrument."),
       ("E", "A designation of the vaccine by the Commissioner is required.")],
      ["B", "E"],
      "105 CMR 700.003(F) permits a duly licensed health care professional to possess and administer a vaccine "
      "DESIGNATED BY THE COMMISSIONER, PROVIDED the Commissioner determines that there are or will be insufficient "
      "health care professionals available for timely administration AND issues an order authorizing it. Option D "
      "misstates the pairing by treating the practitioner instrument as sufficient alongside the order without the "
      "prior determination and designation, which are the conditions the question asks about.",
      {"A": "The practitioner instrument alone does not open the pathway.",
       "B": "Correct: the insufficiency determination is a stated condition.",
       "C": "The order does not displace the practitioner order or prescription.",
       "D": "The statement omits the determination and designation that gate the pathway.",
       "E": "Correct: the vaccine must be one the Commissioner has designated."},
      ["MA-EMERGENCY-VACCINE-GATE"],
      ["List the conditions the regulation attaches to the pathway",
       "Separate the designation and determination from the order",
       "Note that a practitioner instrument is still required on top"],
      ["A student may act only under authorisation and supervision"],
      "Candidates treat the Commissioner order as a single switch that turns the whole pathway on."),

    q("MA-Q-0349", "EMERGENCY_VACCINE_COMMISSIONER_ORDER_GATE", "Public health", "Who may act under the order", 4, "SBA",
      "A Commissioner order authorising administration of a designated vaccine is in force in Massachusetts. A "
      "pharmacy wishes to use a student enrolled in an approved programme for licensure as a health care "
      "professional to help administer doses. What does the regulation require for the student?",
      [("A", "The student may act on the same footing as a licensed professional."),
       ("B", "The student must be authorised and supervised by a licensed qualified professional."),
       ("C", "The student may not administer vaccine under this pathway in any circumstances."),
       ("D", "The student must hold a separate Department certification before assisting."),
       ("E", "The student may act only where the pharmacy notifies the Commissioner first.")],
      ["B"],
      "The pathway at 105 CMR 700.003(F) reaches a student duly enrolled in an approved or accredited programme for "
      "licensure as a health care professional and acting in accordance with that programme's policies, and "
      "700.003(F)(1)(c) requires that a student administering vaccine be AUTHORISED AND SUPERVISED BY A LICENSED AND "
      "QUALIFIED HEALTH CARE PROFESSIONAL.",
      {"A": "The student limb carries its own supervision condition.",
       "B": "Correct: authorisation and supervision are both required.",
       "C": "Students are expressly within the pathway.",
       "D": "No separate certification is contemplated.",
       "E": "No notification requirement attaches to the student limb."},
      ["MA-EMERGENCY-VACCINE-GATE"],
      ["Confirm the student is enrolled in an approved or accredited programme",
       "Apply the authorisation and supervision condition",
       "Note the programme's own policies also govern"],
      ["The Commissioner's order and a practitioner instrument are still required"],
      "Candidates assume a general authorisation covers everyone the pathway names."),

    q("MA-Q-0350", "EMERGENCY_VACCINE_WRITTEN_PROTOCOL_SUBJECTS", "Public health", "Written protocols", 3, "SATA",
      "A Massachusetts pharmacy operating under a Commissioner order holds training records and a written plan for "
      "responding to adverse events. Which further protocol subjects does the regulation require it to cover? "
      "Select all that apply.",
      [("A", "Proper storage of vaccine."),
       ("B", "Handling of vaccine."),
       ("C", "Return of unused vaccine."),
       ("D", "Reimbursement arrangements for administered doses."),
       ("E", "Recordkeeping regarding administration.")],
      ["A", "B", "C", "E"],
      "Under 105 CMR 700.003(F)(2) a person administering vaccine must receive proper training and supervision and "
      "must comply with written protocols to ensure proper STORAGE, HANDLING AND RETURN of vaccine, RECORDKEEPING "
      "regarding administration, RESPONSE TO ADVERSE EVENTS, and safe and appropriate administration. Return of "
      "vaccine is the subject most often missed.",
      {"A": "Correct: storage is named.",
       "B": "Correct: handling is named.",
       "C": "Correct: return of vaccine is named.",
       "D": "Reimbursement is not among the protocol subjects.",
       "E": "Correct: recordkeeping regarding administration is named."},
      ["MA-EMERGENCY-VACCINE-PROTOCOLS"],
      ["List the protocol subjects the paragraph names",
       "Set aside the subjects the pharmacy has already covered",
       "Identify what is still missing"],
      ["Proper training and supervision are required alongside the protocols"],
      "Candidates recall storage and handling as a pair and omit return, which travels with them in the text."),

    q("MA-Q-0351", "NON_OPIATE_DIRECTIVE_PHARMACIST_STANDARD", "Opioid safety", "Voluntary non-opiate directive", 4, "SBA",
      "An electronically transmitted oxycodone prescription reaches a Massachusetts outpatient pharmacy for a "
      "patient whose voluntary non-opiate directive is recorded in the system. The pharmacist on duty never opens "
      "the record, does not know of the directive, and dispenses. What is her position under the statute?",
      [("A", "In violation, because the directive was recorded and available to her."),
       ("B", "In violation, because failing to check the record is at least negligent."),
       ("C", "In violation, because the prescription contradicted a filed directive."),
       ("D", "Not in violation only if the pharmacy has no system for surfacing directives."),
       ("E", "Not in violation, because she is protected unless she acted knowingly against it.")],
      ["E"],
      "M.G.L. c. 94C, s. 18B(c) provides that a prescription presented at or electronically transmitted to an "
      "outpatient pharmacy is presumed valid for the purposes of the section, and that a pharmacist in an outpatient "
      "setting SHALL NOT be held in violation for dispensing in contradiction to a directive EXCEPT UPON EVIDENCE "
      "THAT THE PHARMACIST ACTED KNOWINGLY against it. A pharmacist who did not know is outside the exception.",
      {"A": "Availability of the record is not knowledge.",
       "B": "Negligence is not the standard the subsection applies to this pharmacist.",
       "C": "The contradiction alone does not establish a violation.",
       "D": "The protection does not depend on the pharmacy's systems.",
       "E": "Correct: the exception requires knowing action."},
      ["MA-NON-OPIATE-DIRECTIVE"],
      ["Identify the setting as an outpatient pharmacy",
       "Apply the presumption of validity to the transmitted prescription",
       "Test the facts against the knowingly exception"],
      ["A directive may be revoked in writing or orally"],
      "Candidates apply an ordinary reasonable-pharmacist standard where the statute has specified knowledge."),

    q("MA-Q-0352", "NON_OPIATE_DIRECTIVE_PHARMACIST_STANDARD", "Opioid safety", "Two standards in one section", 5, "SBA",
      "In the same Massachusetts health system, an outpatient pharmacist carelessly dispenses an opiate contrary to "
      "a filed non-opiate directive without knowing of it, and a nurse practitioner carelessly administers one to "
      "the same patient without checking. Neither acted knowingly. How do their positions compare under the section?",
      [("A", "Both are protected, because neither of them acted knowingly against the directive."),
       ("B", "Both are exposed, because carelessness is enough for a licensing board to act."),
       ("C", "The pharmacist is exposed and the practitioner is protected on these facts."),
       ("D", "Both turn on whether the patient suffered harm from the opiate administered."),
       ("E", "The pharmacist is protected and the practitioner is exposed to board action.")],
      ["E"],
      "The section applies two different standards. The outpatient pharmacist is protected under s. 18B(c) unless "
      "she acted knowingly. Separately, s. 18B(e) permits a board of professional licensure to limit, condition or "
      "suspend the licence of, or fine, a licensed health care provider who RECKLESSLY OR NEGLIGENTLY fails to "
      "comply with a directive. The same carelessness therefore lands differently on the two professionals.",
      {"A": "The recklessness or negligence limb reaches the practitioner.",
       "B": "The pharmacist has a specific statutory protection.",
       "C": "This reverses the two standards.",
       "D": "Harm is not an element of either limb.",
       "E": "Correct: knowledge for the outpatient pharmacist, negligence for the provider generally."},
      ["MA-NON-OPIATE-DIRECTIVE"],
      ["Locate the standard applying to an outpatient pharmacist",
       "Locate the separate standard applying to health care providers",
       "Apply each to its own actor"],
      ["Good-faith failure to offer or administer an opiate carries its own protection"],
      "Candidates find one standard in the section and apply it to everyone the section mentions."),

    q("MA-Q-0353", "PHARMACIST_PRESCRIBER_IDENTIFICATION_PARTICULARS", "Collaborative practice", "Identification particulars", 4, "SATA",
      "A Massachusetts collaborating pharmacist is issuing a prescription that another pharmacy will fill. Which "
      "particulars must she supply to the dispensing pharmacist? Select all that apply.",
      [("A", "Her home address, so that she can be reached outside working hours."),
       ("B", "Her date of initial licensure in the Commonwealth."),
       ("C", "Her registration number."),
       ("D", "The name of her supervising physician."),
       ("E", "Confirmation that the patient has consented to collaborative management.")],
      ["C", "D"],
      "105 CMR 700.003(G)(7) permits the pharmacist to issue a prescription provided the prescribing pharmacist "
      "clearly identifies name and professional designation to the dispensing pharmacist and provides registration "
      "number, work address, phone number, and the name of the supervising physician. The work address rather than "
      "a home address is specified, and neither licensure date nor consent confirmation appears.",
      {"A": "The paragraph specifies a work address.",
       "B": "Licensure date is not among the particulars.",
       "C": "Correct: the registration number is required.",
       "D": "Correct: the supervising physician must be named.",
       "E": "Consent is recorded elsewhere and is not part of this transmission."},
      ["MA-PHARMACIST-PRESCRIBER-ID"],
      ["List the particulars the paragraph names",
       "Distinguish the work address from a personal one",
       "Note the supervising physician among them"],
      ["Name and professional designation must also be clearly identified"],
      "Candidates supply the particulars a prescriber would give and miss the one unique to a pharmacist prescriber."),

    q("MA-Q-0354", "PHARMACIST_PRESCRIBER_IDENTIFICATION_PARTICULARS", "Collaborative practice", "Receiving pharmacist decision", 4, "SBA",
      "A Massachusetts pharmacist takes a telephoned prescription from a collaborating pharmacist who gives her "
      "name, professional designation, registration number, work address and a callback number, but does not name "
      "the supervising physician. What should the receiving pharmacist do?",
      [("A", "Fill it, because the caller supplied the identifying particulars that matter."),
       ("B", "Fill it, and record that the supervising physician was not identified."),
       ("C", "Decline to fill it as transmitted until the supervising physician is named."),
       ("D", "Decline to fill it, because a pharmacist may not telephone a prescription at all."),
       ("E", "Fill it, provided she verifies the caller's registration number independently.")],
      ["C"],
      "The proviso in 105 CMR 700.003(G)(7) lists the supervising physician's name among the particulars the "
      "prescribing pharmacist must provide to the dispensing pharmacist. The transmission is incomplete without it, "
      "so it may not be filled as transmitted; the cure is to obtain the missing particular.",
      {"A": "The physician's name is one of the listed particulars.",
       "B": "Recording the gap does not close it.",
       "C": "Correct: the missing particular must be supplied first.",
       "D": "The paragraph contemplates issuing under M.G.L. c. 94C, s. 20.",
       "E": "Verifying one particular does not supply another."},
      ["MA-PHARMACIST-PRESCRIBER-ID"],
      ["Check the transmission against the listed particulars",
       "Identify the missing one",
       "Treat the transmission as incomplete rather than invalid in principle"],
      ["The particulars are supplied to the dispensing pharmacist, not to the patient"],
      "Candidates weigh whether the missing item is important instead of checking it against the list."),

    q("MA-Q-0355", "S9_PHARMACIST_QUALIFIED_PRACTITIONER_AUTHORITY", "Pharmacist administration", "Section 9 authority", 4, "SATA",
      "A Massachusetts pharmacist and a physician working in the same clinic each point to M.G.L. c. 94C, s. 9 as "
      "their authority to hold and give a controlled substance. Which statements are correct? Select all that "
      "apply.",
      [("A", "The section authorises possession of what is reasonably required for patient treatment."),
       ("B", "It authorises administration, or causing administration under direction by a nurse."),
       ("C", "The pharmacist appears in the section on the same footing as the physician."),
       ("D", "The pharmacist appears only as limited by other named provisions."),
       ("E", "Registration under section 7 is required before the section applies at all.")],
      ["A", "B", "D", "E"],
      "Section 9(a) allows the listed practitioners, and a pharmacist AS LIMITED BY s. 7(g) and M.G.L. c. 112, s. "
      "24B1/2, when registered under s. 7 and acting in good faith in the course of a professional practice, to "
      "possess controlled substances as may reasonably be required for patient treatment and to administer them or "
      "cause them to be administered under direction by a nurse.",
      {"A": "Correct: the possession limb is measured by what treatment reasonably requires.",
       "B": "Correct: both administering and causing administration are covered.",
       "C": "The pharmacist alone on the list carries an as-limited qualifier.",
       "D": "Correct: s. 7(g) and c. 112, s. 24B1/2 limit the pharmacist's place on the list.",
       "E": "Correct: the section applies to those registered under s. 7."},
      ["MA-S9-PHARMACIST-AUTHORITY"],
      ["Read the list of practitioners and note the qualifier attached to the pharmacist",
       "Separate the possession limb from the administration limb",
       "Note the registration precondition"],
      ["The good-faith and professional-practice conditions apply to everyone on the list"],
      "Candidates read a long list of professionals as conferring identical authority on each of them."),

    q("MA-Q-0356", "S9_PHARMACIST_QUALIFIED_PRACTITIONER_AUTHORITY", "Pharmacist administration", "Comparing two actors", 5, "SBA",
      "A Massachusetts pharmacist with no collaborative practice agreement, registered under M.G.L. c. 94C, s. 7, "
      "wishes to keep a stock of a controlled substance for patient treatment and to administer it, relying on s. 9 "
      "alone. A physician in the same clinic, registered on the same basis, proposes to do the same. How do their "
      "positions differ?",
      [("A", "They do not differ; both are authorised by the same sentence of section 9."),
       ("B", "They do not differ; both need a collaborative practice agreement to proceed."),
       ("C", "The pharmacist may proceed and the physician needs a further instrument."),
       ("D", "Neither may proceed, because section 9 confers no possession authority at all."),
       ("E", "The physician may proceed; the pharmacist is limited by two further provisions.")],
      ["E"],
      "The same sentence lists a physician without qualification and a pharmacist only AS LIMITED BY subsection (g) "
      "of section 7 and section 24B1/2 of chapter 112. A pharmacist with no collaborative practice agreement "
      "therefore cannot rest on section 9 standing alone, while the physician can.",
      {"A": "The sentence qualifies only one of the two.",
       "B": "The physician is not routed through a collaborative agreement.",
       "C": "This reverses the qualification.",
       "D": "The section does confer a possession authority.",
       "E": "Correct: the pharmacist alone carries the as-limited qualifier."},
      ["MA-S9-PHARMACIST-AUTHORITY"],
      ["Locate the pharmacist within the section 9 list",
       "Read the qualifier attached to that entry",
       "Compare it with the unqualified entry for a physician"],
      ["The qualifier points at M.G.L. c. 94C, s. 7(g) and M.G.L. c. 112, s. 24B1/2"],
      "Candidates see the pharmacist named in the statute and stop reading before the words that limit the entry."),

    q("MA-Q-0357", "STANDING_ORDER_REPORTING_CADENCE_AND_CONFIDENTIALITY", "Public health", "Reporting cadence", 4, "SATA",
      "A Massachusetts pharmacy dispenses emergency contraception, opioid antagonists and COVID-19 control measures "
      "under the respective standing orders. Which statements about its reporting duties are correct? Select all "
      "that apply.",
      [("A", "A single combined annual return satisfies all three regimes."),
       ("B", "Opioid antagonist doses dispensed are reported annually."),
       ("C", "COVID-19 control measures are reported to the department upon request."),
       ("D", "Emergency contraception is reported only when the department opens an inquiry."),
       ("E", "Each report must identify the individual patients supplied.")],
      ["B", "C"],
      "The three regimes report differently. Emergency contraception is reported ANNUALLY, opioid antagonist doses "
      "are reported ANNUALLY, and COVID-19 control measures are reported UPON REQUEST. In each case the reports "
      "shall not identify any individual patient and are confidential.",
      {"A": "The regimes are separate and one of them is request-driven.",
       "B": "Correct: an annual report of doses dispensed.",
       "C": "Correct: reporting on request rather than on a cycle.",
       "D": "Emergency contraception is reported annually.",
       "E": "The reports must not identify any individual patient."},
      ["MA-STANDING-ORDER-REPORTING"],
      ["Take each standing-order regime separately",
       "Identify its reporting trigger",
       "Apply the common prohibition on patient identifiers"],
      ["The department publishes aggregate annual information for opioid antagonists"],
      "Candidates assume parallel public-health regimes carry parallel administrative duties."),

    q("MA-Q-0358", "STANDING_ORDER_REPORTING_CADENCE_AND_CONFIDENTIALITY", "Public health", "Status of the reports", 4, "SBA",
      "A journalist makes a public records request to a Massachusetts department for the reports a named pharmacy "
      "filed about opioid antagonists it dispensed. The pharmacy asks its pharmacist what the statutory position "
      "is. What should the pharmacist say?",
      [("A", "The reports are public records once filed with a state agency."),
       ("B", "The reports are public records with patient identifiers redacted."),
       ("C", "The reports are available only to the prescriber who issued the standing order."),
       ("D", "The reports are confidential and are not public records under the statute."),
       ("E", "The reports may be released once the department publishes its annual summary.")],
      ["D"],
      "Each standing-order reporting provision states that reports shall not identify an individual patient, shall "
      "be confidential, and shall not constitute a public record as defined in clause Twenty-sixth of section 7 of "
      "chapter 4. The department separately publishes an annual report containing aggregate information, which is "
      "not the same thing as releasing the filings.",
      {"A": "Filing with an agency does not make them public records here.",
       "B": "Redaction is not the mechanism; the statute excludes them outright.",
       "C": "Access is not defined by reference to the standing-order issuer.",
       "D": "Correct: confidential and excluded from the public records definition.",
       "E": "The aggregate publication does not open the underlying filings."},
      ["MA-STANDING-ORDER-REPORTING"],
      ["Read the confidentiality sentence attached to the reporting duty",
       "Note the express exclusion from the public records definition",
       "Distinguish the aggregate publication from the filings themselves"],
      ["Reports must not identify any individual patient in the first place"],
      "Candidates assume anything filed with a public agency is presumptively a public record."),

    q("MA-Q-0359", "STATUTORY_ADMINISTRATION_ROUTE_ARCHITECTURE", "Pharmacist administration", "Statutory routes", 5, "SATA",
      "A Massachusetts pharmacist is asked in one shift to administer a long-acting injectable antipsychotic, "
      "testosterone for gender-affirming care, and an antibiotic for a sexually transmitted infection. Which "
      "statements about the statutory basis for each are correct? Select all that apply.",
      [("A", "All three rest on the same statutory clause and share the same conditions."),
       ("B", "The antipsychotic route requires the direction of a prescribing practitioner."),
       ("C", "The antipsychotic route additionally requires departmental regulations."),
       ("D", "The testosterone route rests on a prescription for that purpose."),
       ("E", "The sexually transmitted infection route rests on a prescription for that purpose.")],
      ["B", "C", "D", "E"],
      "Clause (c) of the definition of Administer sets out three pharmacist routes with different gates: (i) "
      "medications for treatment of mental health and substance use disorder, under departmental regulations AND at "
      "the direction of a prescribing practitioner; (ii) a prescription for testosterone for gender-affirming care; "
      "and (iii) a prescription for treatment and prevention of sexually transmitted infections or for prevention "
      "of HIV. Only the first route carries a regulation gate and a direction requirement.",
      {"A": "The three routes are gated differently.",
       "B": "Correct: practitioner direction is part of the first route.",
       "C": "Correct: the first route runs through departmental regulations as well.",
       "D": "Correct: a prescription is the gate for testosterone.",
       "E": "Correct: a prescription is the gate for the infection route."},
      ["MA-ADMINISTER-STATUTORY-ROUTES"],
      ["Split clause (c) into its three sub-clauses",
       "Read the gate attached to each",
       "Resist carrying a condition from one route across to another"],
      ["Clause (b) separately covers a nurse acting at a practitioner's direction"],
      "Candidates find one set of administration conditions and apply it to every medication a pharmacist may give."),

    q("MA-Q-0360", "SUPERVISING_PHYSICIAN_INELIGIBILITY_ENDS_AUTHORITY", "Collaborative practice", "Physician eligibility", 4, "SBA",
      "A Massachusetts collaborating pharmacist learns informally that her supervising physician surrendered his "
      "federal controlled substances registration last month. His medical licence is unrestricted and she has "
      "received no notice from any board. May she continue co-managing patients this afternoon?",
      [("A", "No, because the physician is deemed ineligible on that surrender alone."),
       ("B", "Yes, because his medical licence remains unrestricted."),
       ("C", "Yes, because no board has notified her that anything has changed."),
       ("D", "Yes, because only a state registration event affects the collaboration."),
       ("E", "Yes, provided she confines herself to non-controlled therapies today.")],
      ["A"],
      "243 CMR 2.12(3)(d) deems a physician ineligible to participate in collaborative drug therapy management "
      "where he has voluntarily surrendered, or has had suspended, revoked or restricted, a controlled substances "
      "licence, permit or registration, EITHER STATE OR FEDERAL. The medical licence being intact does not save it, "
      "and notification to the pharmacist is discretionary for the Board, so the absence of notice proves nothing.",
      {"A": "Correct: the surrender alone renders him ineligible.",
       "B": "The regulation makes the registration event sufficient on its own.",
       "C": "Notification is discretionary, so silence is not reassurance.",
       "D": "The regulation names state or federal events alike.",
       "E": "The ineligibility goes to the collaboration itself, not to the drugs involved."},
      ["MA-SUPERVISING-PHYSICIAN-ELIGIBILITY"],
      ["Identify the event as a controlled substances registration surrender",
       "Note that state and federal events count equally",
       "Note that notice to the pharmacist is discretionary"],
      ["Board notification to the pharmacist is permitted rather than required"],
      "Candidates wait for formal notice, which the regulation does not guarantee will ever come."),
]

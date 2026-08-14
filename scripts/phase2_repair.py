from __future__ import annotations

from collections import Counter
import re
from typing import Any


SBA_IDS = [f"MA-Q-{number:04d}" for number in list(range(11, 41)) + list(range(51, 73))]
SATA_IDS = [f"MA-Q-{number:04d}" for number in list(range(41, 51)) + list(range(73, 91))]


STEM_LEADS = [
    "During final verification,",
    "At prescription intake,",
    "While resolving a claim,",
    "During pharmacist consultation,",
    "At same-day pickup,",
    "While documenting the transaction,",
    "During a profile review,",
    "Before releasing the medication,",
    "During an end-of-shift check,",
    "At a Massachusetts pharmacy,",
    "While reviewing the prescription,",
    "During a prescriber call,",
    "Before the next dispensing,",
    "During a controlled-substance review,",
    "While calculating the legal deadline,",
    "While reconciling pharmacy records,",
    "During a transfer request,",
    "Before accepting an exception,",
    "While comparing federal and state law,",
    "During prospective legal review,",
]


# Each wrong answer records the nearby fact pattern that would make it plausible.
# The condition is used to produce an item-specific explanation rather than boilerplate.
SBA_DISTRACTORS: dict[str, list[tuple[str, str]]] = {
    "MA-Q-0011": [
        ("Process the notation under the five-refill, six-month framework.", "the medication were Schedule III or IV rather than Schedule II"),
        ("Treat each printed refill number as a separate future-dated Schedule II prescription.", "the prescriber had issued separate prescriptions meeting the multiple-prescription requirements"),
        ("Dispense the requested amount as the remainder of a partial fill.", "the original prescription had been partially filled with a documented balance"),
        ("Accept a new oral authorization from the office for the refill.", "a defined Schedule II emergency existed and the emergency oral-prescription safeguards were followed"),
    ],
    "MA-Q-0012": [
        ("Dispense because a stimulant prescription remains valid for six months.", "the prescription were Schedule III or IV and still within the federal refill window"),
        ("Call the prescriber and use that confirmation to restart the 30-day clock.", "a new prescription bearing a new lawful issue date were issued"),
        ("Transfer the unfilled prescription so the receiving pharmacy can treat it as new.", "transfer changed neither the original issue date nor Massachusetts validity"),
        ("Apply the one-year Schedule VI transfer period.", "the drug were Massachusetts Schedule VI rather than Schedule II"),
    ],
    "MA-Q-0013": [
        ("Reject it because Massachusetts never accepts an out-of-state Schedule II prescription.", "the out-of-state statutory pathway were unavailable on the stated facts"),
        ("Apply the five-day contiguous-state narcotic rule because all Schedule II drugs are narcotics.", "Focalin were a Schedule II narcotic rather than a nonnarcotic stimulant"),
        ("Use the 30-day out-of-state Schedule III-through-VI window.", "the prescription were for a Schedule III, IV, V, or VI drug"),
        ("Dispense without verification because New Hampshire is contiguous.", "the applicable pathway did not require the pharmacist's verification step"),
    ],
    "MA-Q-0014": [
        ("Use the federal 72-hour remainder deadline.", "the first partial fill resulted from the pharmacy's inability to supply the full quantity"),
        ("Calculate 30 days from the date of the partial dispensing.", "Massachusetts measured this remainder window from the partial-fill date rather than issue date"),
        ("Send the balance to any pharmacy selected by the patient.", "the law did not reserve the remainder to the pharmacy that made the initial partial fill"),
        ("Record the balance as an authorized refill of the Schedule II prescription.", "Schedule II prescriptions could be refilled instead of completed through a lawful remainder"),
    ],
    "MA-Q-0015": [
        ("Treat the prescription as exempt because methadone is always used for opioid dependence.", "the stated indication were opioid-dependence treatment rather than pain"),
        ("Apply only the general 30-day Schedule II opioid quantity ceiling.", "the more restrictive initial-opiate seven-day rule did not apply"),
        ("Allow a 90-day fill because every methadone prescription qualifies for the OUD pathway.", "the prescription actually met the OUD-treatment exception and all other conditions"),
        ("Dispense ten days because the seven-day limit applies only to minors.", "the statute did not also cover an adult's first outpatient opiate prescription"),
    ],
    "MA-Q-0016": [
        ("Dispense the eight-day supply because extended-release opioids are exempt.", "the statute contained a dosage-form exception for extended-release products"),
        ("Use the ordinary 30-day Schedule II opioid quantity limit without further inquiry.", "the initial outpatient opiate limit were not more restrictive"),
        ("Use the 90-day non-opioid Schedule II pathway.", "oxycodone were a non-opioid controlled substance"),
        ("Split the prescription into seven days now and one day as a refill.", "Schedule II refills were permitted and could cure the original quantity defect"),
    ],
    "MA-Q-0017": [
        ("Apply the seven-day restriction only if this is the minor's first opiate prescription.", "the minor provision depended on first use, as the adult provision does"),
        ("Dispense 12 days if a parent signs at pickup.", "parental acknowledgment alone satisfied the prescriber's statutory documentation exception"),
        ("Use the 30-day Schedule II ceiling because it displaces the minor-specific rule.", "the general quantity rule overrode the more restrictive minor provision"),
        ("Accept the written 12-day quantity as the prescriber's implied exception.", "the statute did not require the triggering condition and non-opiate-alternative finding to be documented"),
    ],
    "MA-Q-0018": [
        ("Honor the first refill because the prescription is less than six months old.", "hydromorphone were Schedule III or IV rather than Schedule II"),
        ("Dispense a remainder because the original quantity was fully supplied.", "an unfilled balance from a lawful partial dispensing still existed"),
        ("Telephone the prescriber and add one refill to the original record.", "an oral refill authorization could convert a completed Schedule II prescription"),
        ("Transfer the refill to another pharmacy for a new prescription number.", "a transfer could create a lawful Schedule II refill"),
    ],
    "MA-Q-0019": [
        ("Print the electronic prescription and transfer the paper image by fax.", "federal transfer rules allowed the electronic prescription to be converted out of electronic form"),
        ("Transfer it repeatedly while no quantity has been dispensed.", "the federal pathway permitted more than one transfer"),
        ("Have technicians at both pharmacies complete the transfer without pharmacist communication.", "the rule did not require direct pharmacist-to-pharmacist communication"),
        ("Treat the transaction as a Schedule II refill at the receiving pharmacy.", "transfer of an unfilled electronic prescription created refill authority"),
    ],
    "MA-Q-0020": [
        ("Use the 30-day out-of-state Schedule III-through-VI window.", "fentanyl were in Schedule III through VI rather than Schedule II"),
        ("Fill any state's Schedule II narcotic prescription within five days.", "the Massachusetts pathway were not limited by origin-state and other statutory conditions"),
        ("Skip direct verification because Rhode Island is contiguous.", "contiguity eliminated the statute's verification requirement"),
        ("Treat electronic transmission as resetting the five-day issue period.", "the transmission date rather than the issue date controlled"),
    ],
    "MA-Q-0021": [
        ("Apply the 72-hour remainder rule automatically.", "the pharmacy, rather than the patient, could not supply the full quantity"),
        ("Require a new prescription for every amount left after today's patient-requested partial fill.", "the federal and Massachusetts patient-request pathways did not authorize a documented remainder"),
        ("Measure the remainder deadline from today's partial-fill date.", "the controlling 30-day period ran from partial dispensing instead of prescription issuance"),
        ("Allow the patient to collect the balance from a different pharmacy.", "Massachusetts did not restrict the remainder to the original partially filling pharmacy"),
    ],
    "MA-Q-0022": [
        ("Dispense after confirming that the prescriber still wants the medication supplied.", "prescriber confirmation could extend an expired Schedule II prescription without a new prescription"),
        ("Use the federal six-month refill clock because Demerol is controlled.", "meperidine were Schedule III or IV rather than Schedule II"),
        ("Transfer the prescription before dispensing to restore validity.", "a transfer changed the original issue date"),
        ("Treat 35 days as acceptable when no prior quantity was dispensed.", "Massachusetts validity depended on prior dispensing rather than elapsed time from issue"),
    ],
    "MA-Q-0023": [
        ("Dispense the full quantity written in the later follow-up prescription.", "the initial emergency oral quantity were not limited to the emergency period"),
        ("Limit the emergency supply to exactly 72 hours.", "the 72-hour insufficient-stock remainder rule controlled emergency oral prescribing"),
        ("Decline every oral Schedule II order, even in a defined emergency.", "federal law contained no emergency oral exception"),
        ("Use a seven-day supply cap as the federal emergency quantity standard.", "the federal rule set a fixed seven-day quantity rather than the amount necessary for the emergency"),
    ],
    "MA-Q-0024": [
        ("Apply a 30-day ceiling because no Schedule III opioid can qualify for 90 days.", "the Massachusetts OUD-drug pathway were unavailable"),
        ("Use 90 days merely because every Schedule III drug qualifies.", "the pathway were schedule-based without indication and other conditions"),
        ("Apply the initial-opiate seven-day limit even though the drug is prescribed for OUD.", "the statutory OUD-treatment exclusion did not apply"),
        ("Convert six authorized refills into one 90-day supply.", "federal refill authorization itself determined the Massachusetts single-fill quantity"),
    ],
    "MA-Q-0025": [
        ("Omit the dispensing because MassPAT receives only Schedule II records.", "Massachusetts reporting excluded Schedule III dispensing"),
        ("Treat administration by a health professional as automatically eliminating a pharmacy dispensing report.", "the pharmacy's covered dispensing transaction fell outside the reporting standard"),
        ("Use the product program in place of MassPAT submission.", "a product-specific distribution program displaced state PMP reporting"),
        ("Report only if the prescription later receives a refill.", "MassPAT reporting were triggered by refill status rather than covered dispensing"),
    ],
    "MA-Q-0026": [
        ("Dispense a sixth refill because the prescription is still under six months old.", "the federal rule imposed only a time limit and no five-refill maximum"),
        ("Treat the original notation as a practitioner renewal.", "renewal occurred without a new or renewed practitioner authorization"),
        ("Use Massachusetts Schedule V rules instead of the federal Schedule IV rule.", "alprazolam were Schedule V in Massachusetts"),
        ("Transfer the prescription to obtain five more refills.", "transfer reset the federal refill count"),
    ],
    "MA-Q-0027": [
        ("Reject it after five days under the out-of-state Schedule II narcotic rule.", "lorazepam were a Schedule II narcotic"),
        ("Use the federal six-month clock as the only deadline.", "federal refill timing displaced Massachusetts' 30-day initial-fill condition"),
        ("Accept it without verification because Connecticut licenses the practitioner.", "Massachusetts did not require verification for out-of-state Schedule III-V prescriptions"),
        ("Require a Massachusetts prescriber for every Schedule IV prescription.", "Massachusetts prohibited the statutory out-of-state pathway"),
    ],
    "MA-Q-0028": [
        ("Honor all six refills because they were written on the original.", "practitioner notation could exceed the federal numerical limit"),
        ("Count only refills dispensed in Massachusetts.", "the federal count excluded refills at other pharmacies"),
        ("Allow another refill because five months is less than six months.", "the time limit were the sole federal restriction"),
        ("Convert the sixth refill into a partial fill of the fifth.", "a completed refill could be reopened as a partial dispensing"),
    ],
    "MA-Q-0029": [
        ("Dispense because unused authorized refills survive for one year.", "Schedule IV prescriptions had a one-year refill window"),
        ("Use the date of the last refill to start a new six-month period.", "federal timing ran from last dispensing rather than issue"),
        ("Renew the prescription based solely on the patient's request.", "the pharmacist could supply practitioner renewal authority"),
        ("Transfer it and apply a new issue date at the receiving pharmacy.", "transfer altered the original issue date"),
    ],
    "MA-Q-0030": [
        ("Permit a second transfer because no dose has been dispensed.", "the federal electronic-transfer limit depended only on dispensing status"),
        ("Print and fax it so the next transaction is no longer electronic.", "changing format avoided the one-transfer ceiling"),
        ("Return it to the original pharmacy and treat that return as a refill.", "a completed transfer preserved a freely reusable original prescription"),
        ("Allow another transfer when the patient consents in writing.", "patient consent created a second-transfer exception"),
    ],
    "MA-Q-0031": [
        ("Exclude midazolam because only opioid prescriptions enter MassPAT.", "Massachusetts reporting were limited to opioids"),
        ("Report it only if more than a seven-day supply is dispensed.", "the reporting trigger depended on days supply"),
        ("Classify the drug as Schedule VI because the dosage form is not stated.", "midazolam lost its Schedule IV status when formulation details were absent"),
        ("Wait until month-end to combine the transaction with inventory data.", "the current dispenser submission standard permitted monthly reporting"),
    ],
    "MA-Q-0032": [
        ("Dispense because the six-month period remains open.", "the federal five-refill cap had not also been reached"),
        ("Treat five completed refills as five new prescriptions.", "each refill carried independent refill authority"),
        ("Add a refill after confirming stable therapy with the patient.", "a pharmacist could renew Schedule IV authorization without the practitioner"),
        ("Apply the no-refill rule used for Schedule II drugs.", "triazolam were Schedule II rather than Schedule IV"),
    ],
    "MA-Q-0033": [
        ("Dispense because one authorized refill remains on the profile.", "unused authorization survived after the prescription became more than six months old"),
        ("Measure six months from the most recent refill date.", "21 CFR 1306.22 measured from last dispensing rather than issue"),
        ("Transfer the record and let the receiving pharmacy restart the clock.", "transfer created a new issue date"),
        ("Use the Massachusetts 30-day Schedule II validity rule.", "temazepam were Schedule II rather than Schedule IV"),
    ],
    "MA-Q-0034": [
        ("Fill because federal Schedule IV prescriptions remain refillable for six months.", "the Massachusetts 30-day out-of-state initial-fill condition did not also apply"),
        ("Use the five-day contiguous-state narcotic rule.", "zolpidem were a Schedule II narcotic"),
        ("Accept the prescription after telephone verification on day 31.", "verification extended the statutory 30-day window"),
        ("Change the issue date to the date the pharmacy received it.", "receipt date controlled instead of practitioner issue date"),
    ],
    "MA-Q-0035": [
        ("Decline because four prior refills exhaust the federal limit.", "the numerical ceiling were four rather than five"),
        ("Dispense indefinitely until the prescriber cancels it.", "Schedule IV prescriptions had neither a count nor time ceiling"),
        ("Require a new prescription because every controlled-drug fill is nonrefillable.", "eszopiclone were Schedule II"),
        ("Allow two more refills because the six-month window has two months left.", "time remaining could increase the five-refill maximum"),
    ],
    "MA-Q-0036": [
        ("Transfer any unfilled Sonata prescription even if it began on paper.", "the federal pathway applied to paper and fax prescriptions"),
        ("Permit repeated transfers until the first dispensing.", "the rule allowed more than one transfer"),
        ("Let a technician transmit the record without pharmacist communication.", "the required direct communication could be delegated entirely"),
        ("Ignore Massachusetts transfer restrictions because federal permission preempts every state condition.", "federal permission operated without the state-law prerequisite"),
    ],
    "MA-Q-0037": [
        ("Omit Belsomra because MassPAT covers benzodiazepines only.", "reportability depended on therapeutic class instead of Schedule IV status"),
        ("Report only Schedule II and III medications.", "the Massachusetts program excluded Schedules IV and V"),
        ("Treat suvorexant as Schedule VI because it is an insomnia drug.", "indication displaced its controlled-substance classification"),
        ("Submit only after the prescription reaches its fifth refill.", "refill count rather than dispensing triggered reporting"),
    ],
    "MA-Q-0038": [
        ("Check only whether five refills have been completed.", "21 CFR 1306.22 had no separate six-month limit"),
        ("Check only whether six months have elapsed.", "the rule imposed no numerical maximum"),
        ("Require renewal now because two prior refills exhaust the limit.", "the federal cap were two refills"),
        ("Use a one-year window because Dayvigo is prescribed for sleep.", "indication altered the Schedule IV refill period"),
    ],
    "MA-Q-0039": [
        ("Dispense because the profile still displays two refills.", "unused refills remained valid after the issue-date limit"),
        ("Start a new six-month window from the last dispensing.", "the controlling clock did not run from issue"),
        ("Apply the 30-day Schedule II rule instead.", "daridorexant were Schedule II"),
        ("Extend validity after documenting continued insomnia.", "clinical need allowed a pharmacist to extend federal authorization"),
    ],
    "MA-Q-0040": [
        ("Apply only the five-refill and six-month Schedule IV limits.", "the opiate-specific Massachusetts supply limit did not apply to tramadol"),
        ("Allow ten days because Schedule IV drugs are exempt from the opiate statute.", "schedule placement eliminated tramadol's opiate status"),
        ("Reduce the quantity without contacting the prescriber and discard the balance.", "the pharmacist could unilaterally rewrite the authorized days supply"),
        ("Use the seven-day restriction only for patients younger than 18.", "the statute did not cover an adult's first outpatient opiate prescription"),
    ],
    "MA-Q-0051": [
        ("Keep the incident log alone; documentation is the entire CQI obligation.", "247 CMR 15 required no assessment or prevention component"),
        ("Wait for a serious-injury report before reviewing system causes.", "CQI analysis were triggered only by Board-reportable harm"),
        ("Delegate prevention planning to the software vendor.", "the pharmacy had no responsibility for its own workflow controls"),
        ("Replace CQI with an annual controlled-substance inventory.", "inventory compliance served the same function as quality improvement"),
    ],
    "MA-Q-0052": [
        ("Complete root-cause analysis before contacting anyone.", "the regulation allowed later analysis to precede immediate harm-minimization duties"),
        ("Notify only the prescriber and wait for instructions before contacting the patient.", "the patient-notification duty were conditional on prescriber direction"),
        ("Document within 24 hours but defer corrective directions until then.", "the documentation deadline also delayed immediate protective action"),
        ("Report every QRE to the Board before assisting the patient.", "all QREs were automatically Board-reportable and reporting came first"),
    ],
    "MA-Q-0053": [
        ("Document by the end of the next business day.", "the regulation used a business-day deadline rather than 24 elapsed hours"),
        ("Wait until the monthly CQI meeting.", "initial event documentation could be deferred to aggregate review"),
        ("Start the clock only after the patient confirms harm.", "the trigger were patient harm rather than discovery or notification"),
        ("Use the seven-business-day serious-event reporting deadline.", "initial QRE documentation and Board reporting shared one deadline"),
    ],
    "MA-Q-0054": [
        ("Close each event after correcting the individual prescription.", "CQI imposed no systems-level analysis duty"),
        ("Examine only whether the pharmacist violated a rule.", "the required analysis excluded workflow, staffing, technology, and training contributors"),
        ("Wait for the Board to prescribe a corrective action.", "the pharmacy lacked responsibility to use its findings for improvement"),
        ("Replace cause analysis with annual personnel education.", "education alone satisfied event analysis and systems response"),
    ],
    "MA-Q-0055": [
        ("Train personnel only when they are first hired.", "ongoing CQI education were not required"),
        ("Repeat training every two years with license renewal.", "the regulation used a biennial rather than annual interval"),
        ("Educate pharmacists only, excluding other pharmacy personnel.", "the CQI education duty did not extend across pharmacy personnel"),
        ("Substitute two hours of pharmacist law CE for the pharmacy's CQI program education.", "individual CE automatically met the facility's separate annual duty"),
    ],
    "MA-Q-0056": [
        ("Use 24 hours because that is the initial QRE documentation deadline.", "the question concerned internal QRE documentation rather than Board reporting of serious injury"),
        ("Report within seven calendar days.", "247 CMR 20.02 counted calendar rather than business days"),
        ("Start the clock only after the patient files a complaint.", "discovery or employee knowledge did not trigger reporting"),
        ("Do not report because emergency treatment is not serious injury.", "the regulation excluded emergency treatment from the serious-injury definition"),
    ],
    "MA-Q-0057": [
        ("Purge the file after two years under the general prescription-record rule.", "the special five-year serious-event retention rule did not control"),
        ("Keep only the submitted report and destroy supporting records.", "247 CMR 20.02 required no readily retrievable supporting material"),
        ("Measure five years from the dispensing date rather than filing.", "the retention period began at the medication event"),
        ("Transfer the file to the Board and retain no pharmacy copy.", "submission shifted all retention responsibility away from the pharmacy"),
    ],
    "MA-Q-0058": [
        ("Wait for the inventory investigation to finish before notifying DEA.", "the one-business-day notice clock began only after final loss quantification"),
        ("Give oral notice within 24 hours and omit written notice.", "21 CFR 1301.74(c) accepted oral notice in place of written notice"),
        ("File Form 106 within one business day as the only required step.", "the regulation imposed the same deadline on final Form 106 completion and eliminated separate written notice"),
        ("Notify only the Massachusetts Board because the loss occurred in Massachusetts.", "state notice displaced the registrant's federal DEA duty"),
    ],
    "MA-Q-0059": [
        ("Take the first inventory at the end of the first month.", "federal law allowed a post-opening grace period"),
        ("Wait two years because only biennial inventories are required.", "the initial-inventory trigger did not precede the biennial cycle"),
        ("Inventory only Schedule II stock on the start date.", "the initial inventory excluded other controlled schedules"),
        ("Use the wholesaler's invoice as the pharmacy's initial inventory.", "purchase records alone satisfied the registrant's inventory record"),
    ],
    "MA-Q-0060": [
        ("No problem exists until 30 months have elapsed.", "the federal interval were 30 months rather than two years"),
        ("The annual pharmacy permit renewal resets the inventory clock.", "state licensure renewal replaced the federal inventory date"),
        ("Only Schedule II stock needs a biennial inventory.", "21 CFR 1304.11(c) excluded Schedules III through V"),
        ("A perpetual inventory removes the need for the biennial snapshot.", "ongoing records substituted for the required biennial inventory"),
    ],
    "MA-Q-0061": [
        ("Estimate because exact counts are required only for Schedule II.", "the opened-container exception had no more-than-1,000-unit threshold"),
        ("Estimate after subtracting quantities shown on invoices.", "derived bookkeeping could replace the required physical count"),
        ("Count exactly only if the bottle originally contained 1,000 units or fewer.", "the threshold operated in the opposite direction"),
        ("Move tablets into two smaller containers and estimate each.", "repackaging during inventory could avoid the large-container rule"),
    ],
    "MA-Q-0062": [
        ("Eighteen months is sufficient if records are scanned.", "electronic format shortened the federal retention period"),
        ("Retain only the most recent biennial inventory.", "new inventories allowed destruction of still-required older records"),
        ("Use the five-year Massachusetts serious-event period for all DEA records.", "the special state event-record rule set the federal minimum for every controlled record"),
        ("Send records to DEA after one year and delete the pharmacy copies.", "transmission to DEA ended the registrant's availability obligation"),
    ],
    "MA-Q-0063": [
        ("Use the ordinary purchase order if the supplier also holds a DEA registration.", "registration alone replaced the Schedule II order-form requirement"),
        ("Use Form 106 because Schedule II stock is being acquired.", "the theft/loss form served as an ordering instrument"),
        ("Use Form 41 to document the incoming quantity.", "the destruction form authorized procurement"),
        ("Obtain prescriber signatures on the purchase order.", "individual prescription authority governed wholesale Schedule II ordering"),
    ],
    "MA-Q-0064": [
        ("Ship the balance because 60 business days have not elapsed.", "21 CFR 1305.13 measured business rather than calendar days"),
        ("Extend the form by documenting the supplier's back order.", "a back order created an extension beyond the 60-day period"),
        ("Use the original form indefinitely for any unfilled balance.", "partial-shipment authorization had no expiration"),
        ("Change the execution date after the purchaser agrees.", "the supplier could alter the date to revive the form"),
    ],
    "MA-Q-0065": [
        ("Let the purchaser initial the altered line and fill the form.", "21 CFR 1305.15 permitted correction by agreement"),
        ("Fill only the unaltered items and retain the defective form.", "a supplier could partially validate an altered order form"),
        ("Have the supplier rewrite the quantity on the same form.", "the supplier could cure the purchaser's defective execution"),
        ("Convert the defective paper form into a CSOS order without a new digital signature.", "paper execution could be imported as a compliant electronic order"),
    ],
    "MA-Q-0066": [
        ("Wait to report until a missing form is fraudulently used.", "immediate reporting depended on confirmed diversion"),
        ("Report only to the form supplier.", "supplier notice replaced notice to the responsible DEA official"),
        ("Use DEA Form 106 as the lost-form report.", "the controlled-substance theft/loss form governed missing order forms"),
        ("Void the serial numbers internally and take no external action.", "an internal log alone satisfied 21 CFR 1305.16"),
    ],
    "MA-Q-0067": [
        ("Leave the paper forms with invoices if staff can eventually locate them.", "paper forms qualified for the electronic readily-retrievable treatment"),
        ("Scan the forms after two years and then begin the retention period.", "the two-year clock began at scanning rather than the required transaction date"),
        ("Keep only a list of form numbers instead of the executed copies.", "an index replaced the required Form 222 records"),
        ("Store purchaser copies with Schedule III prescription records.", "controlled-prescription segregation satisfied the separate paper Form 222 requirement"),
    ],
    "MA-Q-0068": [
        ("Email a scanned Form 222 with an ordinary electronic signature.", "an emailed image met CSOS digital-signature and certificate requirements"),
        ("Use the pharmacy's NPI as the CSOS signing credential.", "the NPI replaced a DEA-issued digital certificate"),
        ("Let any employee submit the order through standard purchasing software.", "subscriber authorization and compliant CSOS software were unnecessary"),
        ("Send an unsigned spreadsheet if the supplier confirms receipt.", "supplier confirmation supplied the required digital signature"),
    ],
    "MA-Q-0069": [
        ("Bottle totals alone are enough if the products were expired.", "expiration eliminated drug-level destruction documentation"),
        ("Record only the date and method because inventory lists contain the rest.", "other inventory records automatically supplied every required Form 41 element"),
        ("Use a patient medication-return log for registrant stock.", "ultimate-user collection records governed registrant inventory destruction"),
        ("Document the witnesses only when Schedule II stock is destroyed.", "witness and method requirements excluded other controlled schedules"),
    ],
    "MA-Q-0070": [
        ("Removing patient labels makes the tablets non-retrievable.", "privacy de-identification altered the drug's physical or chemical condition"),
        ("Ordinary trash is acceptable after an employee witnesses disposal.", "witnessing alone met the destruction standard"),
        ("Crushing the tablets without mixing or chemical alteration is always sufficient.", "crushing alone necessarily made recovery and practical use impossible"),
        ("Use the sewer whenever the product appears on an FDA flush list.", "ultimate-user disposal guidance governed registrant destruction methods"),
    ],
    "MA-Q-0071": [
        ("Use any waste hauler that signs a confidentiality agreement.", "privacy contracting replaced DEA reverse-distributor registration"),
        ("Transfer Schedule II stock on an ordinary invoice.", "Schedule II transfer records did not require the applicable ordering documentation"),
        ("Treat the recipient's state pharmacy permit as sufficient federal authority.", "state licensure alone authorized controlled-substance reverse distribution"),
        ("Remove the stock from inventory before the registered recipient accepts it.", "inventory accountability ended before the lawful transfer"),
    ],
    "MA-Q-0072": [
        ("Ten days is enough when the pharmacy posts a sign immediately.", "public posting shortened the Board's advance-notice period"),
        ("Notify the Board within 14 days after closure instead.", "the post-closure credential deadline replaced advance closure notice"),
        ("Use ordinary email rather than the required certified written notice.", "the regulation allowed email as the ordinary notice method"),
        ("Wait until the final prescription is transferred before announcing the date.", "completion of file transfers triggered the advance notice duty"),
    ],
}


SPECIAL_STEMS = {
    "MA-Q-0021": "A patient asks the pharmacist to dispense part of a new prescription for generic oxymorphone tablets today and return later for the balance. Which limit governs the remainder?",
    "MA-Q-0033": "A Restoril prescription issued on January 10 is presented for another refill on July 11; one authorized refill remains. What should the pharmacist do?",
    "MA-Q-0067": "A purchaser files executed paper DEA Form 222 copies among ordinary invoices, where they cannot be maintained as a separate record set. What correction is required?",
    "MA-Q-0089": "After discovering a dispensing error that may still expose the patient to harm, which duties does 247 CMR 15.03 impose? Select all that apply.",
    "MA-Q-0090": "A resident pharmacy is preparing to close. Which timing and transfer statements are supported by 247 CMR 6.13 and 6.14? Select all that apply.",
}


CORRECT_OVERRIDES = {
    "MA-Q-0033": "Decline the refill because the prescription is now more than six months past its issue date.",
    "MA-Q-0067": "Maintain the executed paper Form 222 copies separately from other records for at least two years.",
}


SATA_EXTRA_TRUES: dict[str, list[str]] = {
    "MA-Q-0041": ["Federal Schedule III refill limits remain a separate check when refills are authorized."],
    "MA-Q-0043": ["Phendimetrazine remains a federal and Massachusetts Schedule III drug regardless of its weight-loss indication."],
    "MA-Q-0045": ["Ketamine's anesthetic indication does not remove its federal or Massachusetts Schedule III status."],
    "MA-Q-0047": [
        "Xyrem is Schedule III when it is an FDA-approved sodium oxybate product under the federal scheduling exception.",
        "REMS compliance does not displace ordinary controlled-substance record duties.",
    ],
    "MA-Q-0048": ["The federal six-month issue-date limit applies independently of the number of refills written."],
    "MA-Q-0049": ["Syndros is Schedule II even though dronabinol capsules marketed as Marinol are Schedule III."],
    "MA-Q-0073": ["Requested patient-file transfers must be handled timely so therapy is not delayed."],
    "MA-Q-0074": ["The post-closure submission deadline is 14 days after the pharmacy closes."],
    "MA-Q-0077": ["The pharmacist preceptor remains responsible for the direct-supervision relationship."],
    "MA-Q-0079": [
        "No more than 15 contact hours in a calendar year may ordinarily be satisfied through home study.",
        "Unused annual continuing-education hours do not carry into the next calendar year.",
    ],
    "MA-Q-0080": ["Sterile and complex-nonsterile compounding duties are cumulative when both activities are supervised."],
    "MA-Q-0081": ["The additional annual continuing education must relate to the pharmacist's collaborative practice area."],
    "MA-Q-0082": ["The collaboration must be established through the written agreement and supervising-physician framework required by statute."],
    "MA-Q-0083": ["Schedule VI prescribing may be authorized only within the separate statutory retail CDTM limits."],
    "MA-Q-0084": ["The pharmacist must document the authorized Schedule VI prescription within the patient-specific collaborative workflow."],
    "MA-Q-0087": [
        "The substitute must be reasonably available at a lower retail price.",
        "A valid prescriber direction against substitution prevents automatic interchange.",
    ],
    "MA-Q-0088": [
        "Returned erroneous medication must not be restored to saleable inventory.",
        "The pharmacy remains responsible for proper disposition after quarantine.",
    ],
}


SATA_COUNTS = {
    **{qid: 2 for qid in ["MA-Q-0042", "MA-Q-0044", "MA-Q-0046", "MA-Q-0050", "MA-Q-0075", "MA-Q-0076", "MA-Q-0078", "MA-Q-0085", "MA-Q-0086"]},
    **{qid: 4 for qid in ["MA-Q-0047", "MA-Q-0079", "MA-Q-0087", "MA-Q-0088", "MA-Q-0090"]},
}


KEY_PATTERNS = {
    2: ["AB", "CD", "AE", "BC", "DE", "AC", "BD", "CE", "AD"],
    3: ["ABC", "BCD", "CDE", "ADE", "ABE", "ACD", "BCE", "BDE", "ACE", "ABD", "ABC", "CDE", "BCE", "ADE"],
    4: ["ABCD", "ABCE", "ABDE", "ACDE", "BCDE"],
}


def _sentence_case(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def _rewrite_stem(question: dict[str, Any], index: int) -> str:
    qid = question["question_id"]
    if qid in SPECIAL_STEMS:
        return SPECIAL_STEMS[qid]
    return f"{STEM_LEADS[index % len(STEM_LEADS)]} {_sentence_case(question['stem'])}"


def _drug_check(drug: dict[str, Any]) -> str:
    generic = drug["generic_name"]
    fed = drug["federal_status"]["schedule"]
    ma = drug["massachusetts_status"]["schedule"]
    indication = drug["main_indications"][0].lower()
    if drug["drug_id"] == "oxymorphone":
        return (
            "Generic oxymorphone products are opioid analgesics used for severe pain and remain federal and Massachusetts "
            "Schedule II. OPANA and OPANA ER are discontinued brand products and are not presented here as current brands."
        )
    brands = ", ".join(drug["brand_names"])
    return f"{generic} ({brands}) is used for {indication}; it is federal Schedule {fed} and Massachusetts Schedule {ma}."


def _reasoning_steps(question: dict[str, Any], rules: dict[str, dict], drugs: dict[str, dict]) -> list[str]:
    steps: list[str] = []
    if question["drug_ids"]:
        drug = drugs[question["drug_ids"][0]]
        steps.append(
            f"Classify {drug['generic_name']} under the federal and Massachusetts schedules before selecting a legal pathway"
        )
    primary = rules[question["rule_ids"][0]]
    steps.append(f"Match the scenario's operative facts to {primary['title']}")
    if question["difficulty"] >= 4:
        steps.append(f"Reject nearby rules whose schedule, trigger, deadline, or actor differs from {primary['subtopic']}")
    if question["difficulty"] == 5:
        steps.append("Confirm the exception, documentation, and timing conditions against the cited official authority")
    needed = max(1, question["difficulty"] - 2)
    return steps[: max(needed, 3 if question["difficulty"] == 5 else needed)]


def _repair_sba(question: dict[str, Any], index: int, rules: dict[str, dict], drugs: dict[str, dict]) -> dict[str, Any]:
    qid = question["question_id"]
    primary = rules[question["rule_ids"][0]]
    revised_stem = _rewrite_stem(question, index)
    original_correct = next(
        choice["text"] for choice in question["choices"] if choice["id"] == question["correct_choice_ids"][0]
    )
    correct_text = CORRECT_OVERRIDES.get(qid, original_correct)
    correct_text = correct_text.replace("Opana", "oxymorphone")
    correct_letter = question["correct_choice_ids"][0]
    wrong_specs = SBA_DISTRACTORS[qid]
    wrong_iter = iter(wrong_specs)
    choices = []
    analysis: dict[str, str] = {}
    for letter in "ABCDE":
        if letter == correct_letter:
            text = correct_text
            analysis[letter] = (
                f"'{correct_text}': supported by {primary['subtopic'].lower()}."
            )
        else:
            text, condition = next(wrong_iter)
            analysis[letter] = (
                f"'{text}' would apply only if {condition}; '{revised_stem}' states otherwise."
            )
        choices.append({"id": letter, "text": text})
    correct_choice = next(choice for choice in choices if choice["id"] == correct_letter)
    wrong_choices = [choice for choice in choices if choice["id"] != correct_letter]
    hedge = re.compile(r"\b(?:generally|may|might|typically|ordinarily|unless|if|when|can)\b", re.IGNORECASE)
    if hedge.search(correct_choice["text"]) and not any(hedge.search(choice["text"]) for choice in wrong_choices):
        wrong_choices[0]["text"] = wrong_choices[0]["text"].rstrip(".") + " if its alternate trigger can be documented."
    correct_length = len(re.findall(r"[A-Za-z0-9]+", correct_choice["text"]))
    max_wrong_length = max(len(re.findall(r"[A-Za-z0-9]+", choice["text"])) for choice in wrong_choices)
    if correct_length >= max_wrong_length * 1.5 and correct_length - max_wrong_length >= 4:
        wrong_choices[0]["text"] = (
            wrong_choices[0]["text"].rstrip(".")
            + f" after documenting whether {wrong_specs[0][1]}."
        )
    question["stem"] = revised_stem
    question["choices"] = choices
    related = [primary["rule_summary"], primary["authority"][0]["section"]]
    if question["drug_ids"]:
        related = [_drug_check(drugs[question["drug_ids"][0]]), primary["rule_summary"]]
    question["explanation"] = {
        "core_reasoning": (
            f"'{correct_text}' is the governing result. By contrast, '{wrong_specs[0][0]}' would require that "
            f"{wrong_specs[0][1]}. The decisive cue appears in '{revised_stem}'."
        ),
        "choice_analysis": analysis,
        "related_facts": related[:3],
        "mpje_trap": (
            f"'{wrong_specs[0][0]}' would apply if {wrong_specs[0][1]}. In '{revised_stem}', that predicate is missing."
        ),
    }
    question["reasoning_steps"] = _reasoning_steps(question, rules, drugs)
    return question


def _paraphrase_statement(text: str, index: int) -> str:
    replacements = [
        ("must be", "is required to be"),
        ("must", "is required to"),
        ("may", "can"),
        ("apply", "govern"),
        ("applies", "governs"),
        ("supported", "legally supported"),
        ("conclusions", "determinations"),
        ("within", "inside"),
    ]
    old, new = replacements[index % len(replacements)]
    rewritten = text.replace(old, new, 1)
    if rewritten == text:
        prefixes = [
            "On this record, ",
            "For this scenario, ",
            "Under these facts, ",
            "In this setting, ",
            "At this stage, ",
            "Given the described event, ",
        ]
        rewritten = prefixes[index % len(prefixes)] + _sentence_case(text)
    return rewritten


def _special_sata_pool(qid: str) -> tuple[list[str], list[str]] | None:
    if qid == "MA-Q-0089":
        return (
            [
                "Immediately notify the patient or representative and provide directions intended to correct the error and minimize harm.",
                "Immediately notify the prescriber when professional judgment indicates that prescriber notice is warranted.",
                "Complete the initial quality-related-event documentation within 24 hours after discovery or notification.",
            ],
            [
                "Always finish root-cause analysis before contacting the patient.",
                "Notify the patient before the prescriber because the regulation imposes that strict relative order.",
            ],
        )
    if qid == "MA-Q-0090":
        return (
            [
                "Send the Board's required certified written notice at least 14 days before the intended closure date.",
                "Identify patients served during the preceding 90 days and attempt patient notice at least 14 days before closure.",
                "Handle requested patient-file transfers timely so the closure does not delay therapy.",
                "Within 14 days after closure, submit original credentials and the controlled-substance disposition attestation.",
            ],
            [
                "Delay every patient-file transfer until after all controlled stock has been disposed of.",
            ],
        )
    return None


def _repair_sata(
    question: dict[str, Any],
    index: int,
    rules: dict[str, dict],
    drugs: dict[str, dict],
    pattern_offsets: dict[int, int],
) -> dict[str, Any]:
    qid = question["question_id"]
    special = _special_sata_pool(qid)
    if special:
        true_pool, false_pool = special
    else:
        original_correct = set(question["correct_choice_ids"])
        true_pool = [choice["text"] for choice in question["choices"] if choice["id"] in original_correct]
        false_pool = [choice["text"] for choice in question["choices"] if choice["id"] not in original_correct]
        true_pool.extend(SATA_EXTRA_TRUES.get(qid, []))
    count = SATA_COUNTS.get(qid, 3)
    if len(true_pool) < count:
        raise ValueError(f"{qid}: insufficient true propositions for requested correct count {count}")
    true_pool = [_paraphrase_statement(text, index + offset) for offset, text in enumerate(true_pool[:count])]
    false_needed = 5 - count
    false_pool = [_paraphrase_statement(text, index + count + offset) for offset, text in enumerate(false_pool[:false_needed])]
    if question["drug_ids"]:
        generic = drugs[question["drug_ids"][0]]["generic_name"]

        def add_drug_context(text: str) -> str:
            if generic.casefold() in text.casefold():
                return text
            return f"{text.rstrip('.')} for {generic}."

        true_pool = [add_drug_context(text) for text in true_pool]
        false_pool = [add_drug_context(text) for text in false_pool]
    pattern_list = KEY_PATTERNS[count]
    offset = pattern_offsets[count]
    pattern_offsets[count] += 1
    correct_letters = list(pattern_list[offset % len(pattern_list)])
    true_iter = iter(true_pool)
    false_iter = iter(false_pool)
    choices = []
    analysis: dict[str, str] = {}
    rule_titles = ", ".join(rules[rid]["title"] for rid in question["rule_ids"])
    primary = rules[question["rule_ids"][0]]
    for letter in "ABCDE":
        is_true = letter in correct_letters
        text = next(true_iter if is_true else false_iter)
        choices.append({"id": letter, "text": text})
        if is_true:
            analysis[letter] = f"'{text}': {primary['subtopic']} supports this proposition."
        else:
            analysis[letter] = f"'{text}': {primary['subtopic']} contradicts this proposition."
    question["question_type"] = "SATA"
    question["stem"] = _rewrite_stem(question, index)
    question["choices"] = choices
    question["correct_choice_ids"] = correct_letters
    related = [rules[rid]["rule_summary"] for rid in question["rule_ids"][:2]]
    if question["drug_ids"]:
        related.insert(0, _drug_check(drugs[question["drug_ids"][0]]))
    question["explanation"] = {
        "core_reasoning": (
            f"Assess each proposition in '{question['stem']}' independently. '{true_pool[0]}' satisfies "
            f"{primary['subtopic']}; '{false_pool[0]}' changes its legal premise."
        ),
        "choice_analysis": analysis,
        "related_facts": related[:3],
        "mpje_trap": (
            f"Answer positions prove nothing. Test '{choices[0]['text']}' independently, then analyze the rest."
        ),
    }
    question["reasoning_steps"] = _reasoning_steps(question, rules, drugs)
    return question


def repair_questions(
    questions: list[dict[str, Any]], rules: dict[str, dict], drugs: dict[str, dict]
) -> list[dict[str, Any]]:
    by_id = {question["question_id"]: question for question in questions}
    if set(SBA_IDS + SATA_IDS) != set(by_id):
        raise ValueError("repair scope must be exactly MA-Q-0011..MA-Q-0090")
    pattern_offsets = Counter()
    repaired = []
    for index, qid in enumerate([f"MA-Q-{number:04d}" for number in range(11, 91)]):
        question = by_id[qid]
        if qid in SBA_IDS:
            repaired.append(_repair_sba(question, index, rules, drugs))
        else:
            repaired.append(_repair_sata(question, index, rules, drugs, pattern_offsets))
        repaired[-1]["verification_status"] = "AUDIT_PENDING"
        repaired[-1]["lifecycle_status"] = "AUDIT_PENDING"
        repaired[-1]["audits"] = []
        repaired[-1]["independent_audit_status"] = "PENDING"
        repaired[-1]["final_adjudication"] = None
        repaired[-1]["duplicate_review_status"] = "PENDING"
    counts = Counter(question["question_type"] for question in repaired)
    if counts != Counter({"SBA": 52, "SATA": 28}):
        raise ValueError(f"unexpected repaired item mix: {counts}")
    if any(question["question_type"] == "ORDERED_RESPONSE" for question in repaired):
        raise ValueError("unsupported Phase 2 ordered responses remain")
    return repaired

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SPEC = ROOT / "repair_specs" / "batch2"
TODAY = "2026-08-14"
ZERO = "0" * 64

SPEC_FILES = ["spec_core_a.json", "spec_core_b.json", "spec_drug_a.json", "spec_drug_b.json"]

RULES = {
    "MA-ADD-CORE": ("MA",4,"Automated dispensing devices","ADD use, security, and accountability","Massachusetts pharmacies using automated dispensing devices must follow the current Board/DCP policy governing facility approval, pharmacy ownership of stock, patient-specific authorization, records, packaging, loss accountability, and retail emergency-versus-routine controls.","Automated dispensing device Use","Policy 2019-02","https://www.mass.gov/policy-statement/automated-dispensing-device-use","BOARD_POLICY"),
    "MA-ADD-TECH": ("MA",1,"Technician scope","Technician stocking of automated dispensing devices","Massachusetts Policy 2023-08 creates credential-specific ADD inventory pathways: trainees may handle pharmacist-verified Schedule III-VI stock; licensed non-trainee technicians may handle pharmacist-verified Schedule II-VI stock; a nationally certified licensed technician has a narrow no-prior-verification pathway for sealed non-patient-specific non-PMP Schedule VI stock with electronic validation.","Pharmacy Practice Resources","Policy 2023-08","https://www.mass.gov/lists/pharmacy-practice-resources","BOARD_POLICY"),
    "MA-EPT": ("MA",2,"Expedited partner therapy","Chlamydia EPT prescriptions","Massachusetts pharmacy Policy 2020-08 permits chlamydia EPT partner prescriptions with a named partner or an approved EPT designation in place of partner name and address, directs the corresponding profile/label workflow, and requires referral to another pharmacy when a pharmacist is unable or unwilling to fill.","Pharmacy Practice Resources","Policy 2020-08","https://www.mass.gov/lists/pharmacy-practice-resources","BOARD_POLICY"),
    "MA-PHARM-ADMIN": ("MA",2,"Pharmacist administration","Authorized medication categories","Massachusetts law and current Board guidance authorize pharmacists meeting applicable conditions to administer specified categories of prescribed medications, including testosterone for gender-affirming care and other enumerated categories; the authority is not a general license to administer every prescription injectable.","Pharmacist Administration of Medications","Current guidance","https://www.mass.gov/lists/pharmacy-practice-resources","OFFICIAL_GUIDANCE"),
    "MA-MH-SUD-ADMIN": ("MA",2,"Pharmacist administration","Mental illness and substance use disorder medications","Current Massachusetts guidance permits trained pharmacists and pharmacy interns to administer listed patient-specific prescribed single-dose long-acting mental-health medications and extended-release naltrexone for substance use disorder under prescriber-directed conditions and required documentation/communication safeguards.","Pharmacist Administration of Medications","Mental illness and substance use disorder pathway","https://www.mass.gov/lists/pharmacy-practice-resources","OFFICIAL_GUIDANCE"),
    "MA-LTC-EMERGENCY-KIT": ("MA",4,"Long-term care","Emergency medication kits","Massachusetts long-term-care facilities may maintain approved emergency medication kits with separate Schedule II-V analgesic and sedative/anticonvulsant category limits tied to licensed bed capacity, single-dose tamper-evident packaging, accountability controls, and controlled Schedule VI emergency-stock safeguards.","Long Term Care Facility Emergency Kits","Current circular letter","https://www.mass.gov/lists/pharmacy-practice-resources","OFFICIAL_GUIDANCE"),
    "MA-HOSPICE-ACUTE": ("MA",4,"Hospice pharmacy","Inpatient hospice acute-use medications","Massachusetts inpatient hospices may use pharmacy-owned ADD stock in approved Schedule II-VI categories as a limited acute palliative bridge until the full patient prescription can be filled and delivered, subject to registration, monitoring, reconciliation, packaging, and bed-capacity quantity controls.","Hospice Inpatient Facility Acute Use Medications","Current circular letter","https://www.mass.gov/lists/pharmacy-practice-resources","OFFICIAL_GUIDANCE"),
    "FED-CII-FAX": ("FEDERAL",3,"Controlled prescriptions","Schedule II fax exceptions","Federal law provides specific circumstances in which a faxed Schedule II prescription may serve as the original, including prescriptions for LTCF residents, qualifying Schedule II narcotics for hospice patients, and qualifying Schedule II narcotics compounded for specified direct parenteral or infusion administration.","Electronic Code of Federal Regulations","21 CFR 1306.11","https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11","FEDERAL_REGULATION"),
    "FED-CII-MULTIPLE": ("FEDERAL",3,"Controlled prescriptions","Multiple Schedule II prescriptions","Federal law permits a practitioner, when all conditions are met, to issue multiple separate Schedule II prescriptions on the actual issue date authorizing a total supply of up to 90 days, with appropriate earliest-fill instructions on later prescriptions rather than postdating or refills.","Electronic Code of Federal Regulations","21 CFR 1306.12","https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.12","FEDERAL_REGULATION"),
    "FED-CII-LTC-TERMINAL": ("FEDERAL",3,"Partial filling","LTCF and terminally ill Schedule II partial filling","Federal law permits Schedule II prescriptions for LTCF residents or terminally ill patients to be partially filled under a special documentation framework for up to 60 days from issue unless the prescription is discontinued sooner.","Electronic Code of Federal Regulations","21 CFR 1306.13(c)","https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13","FEDERAL_REGULATION"),
    "FED-CORRESPONDING-RESP": ("FEDERAL",3,"Prescription validity","Corresponding responsibility","A controlled-substance prescription must be issued for a legitimate medical purpose in the usual course of professional practice; the pharmacist who knowingly fills an invalid prescription shares corresponding responsibility and must exercise an independent dispensing judgment when material red flags remain unresolved.","Electronic Code of Federal Regulations","21 CFR 1306.04(a)","https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.04","FEDERAL_REGULATION"),
    "FED-OUD-OTP": ("FEDERAL",3,"Opioid use disorder","Narcotic treatment pathways","Federal law distinguishes ordinary controlled-prescription practice from narcotic maintenance/detoxification treatment: methadone OUD maintenance generally follows the narcotic-treatment-program framework, while a narrow non-OTP emergency provision permits practitioner dispensing one day at a time for no more than three days while referral is arranged and qualifying Schedule III-V narcotic treatment may use a prescription pathway when otherwise lawful.","Electronic Code of Federal Regulations","21 CFR 1306.07","https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.07","FEDERAL_REGULATION"),
    "MA-MCSR-DEA": ("MA",1,"Prescriber authority","Massachusetts and federal registration","Massachusetts practitioners conducting approved Schedule II-V controlled-substance activities generally require both Massachusetts Controlled Substances Registration and corresponding DEA registration, while approved Schedule VI-only activity requires the appropriate Massachusetts registration but not a federal DEA registration solely because of Schedule VI status.","Massachusetts controlled substances registration","MCSR registration requirements","https://www.mass.gov/lists/pharmacy-practice-resources","OFFICIAL_GUIDANCE"),
    "MA-COMPLIANCE-PACKAGING": ("MA",4,"Compliance packaging","Schedule II and III maintenance medications","Current Massachusetts Board policy permits qualifying Schedule II and III maintenance medications to be included in multi-drug single-dose compliance packages; the change does not convert every acute Schedule II or III course into maintenance therapy or waive other packaging requirements.","Pharmacy Practice Resources","Policy 2023-01","https://www.mass.gov/lists/pharmacy-practice-resources","BOARD_POLICY"),
}

DRUGS = {
"testosterone-cypionate":("testosterone cypionate",["Depo-Testosterone"],"Testosterone replacement and gender-affirming care","Androgen",True,"III","III",True,False),
"naltrexone-er":("naltrexone extended-release injection",["Vivitrol"],"Alcohol and opioid use disorder","Opioid antagonist",False,"NONCONTROLLED","VI",False,False),
"aripiprazole-er":("aripiprazole extended-release injection",["Abilify Maintena"],"Schizophrenia and bipolar I maintenance","Atypical antipsychotic",False,"NONCONTROLLED","VI",False,False),
"paliperidone-palmitate":("paliperidone palmitate",["Invega Sustenna"],"Schizophrenia and schizoaffective disorder","Atypical antipsychotic",False,"NONCONTROLLED","VI",False,False),
"insulin-glargine":("insulin glargine",["Lantus"],"Diabetes mellitus","Long-acting insulin",False,"NONCONTROLLED","VI",False,False),
"doxycycline":("doxycycline",["Vibramycin"],"Susceptible bacterial infections","Tetracycline antibiotic",False,"NONCONTROLLED","VI",False,False),
"warfarin":("warfarin",["Coumadin"],"Prevention and treatment of thromboembolism","Vitamin K antagonist",False,"NONCONTROLLED","VI",False,False),
"gabapentin":("gabapentin",["Neurontin"],"Seizures and postherpetic neuralgia","Gabapentinoid",False,"NONCONTROLLED","VI",True,True),
"pregabalin":("pregabalin",["Lyrica"],"Neuropathic pain and seizures","Gabapentinoid",True,"V","V",True,False),
"methylphenidate":("methylphenidate",["Ritalin"],"Attention-deficit/hyperactivity disorder","CNS stimulant",True,"II","II",True,False),
"alprazolam":("alprazolam",["Xanax"],"Anxiety and panic disorder","Benzodiazepine",True,"IV","IV",True,False),
"oxycodone":("oxycodone",["OxyContin"],"Pain","Opioid analgesic",True,"II","II",True,False),
"fentanyl":("fentanyl",["Sublimaze"],"Analgesia and anesthesia","Opioid analgesic",True,"II","II",True,False),
"dexmethylphenidate":("dexmethylphenidate",["Focalin"],"Attention-deficit/hyperactivity disorder","CNS stimulant",True,"II","II",True,False),
"morphine":("morphine",["MS Contin"],"Pain","Opioid analgesic",True,"II","II",True,False),
"lisdexamfetamine":("lisdexamfetamine",["Vyvanse"],"Attention-deficit/hyperactivity disorder and binge-eating disorder","CNS stimulant",True,"II","II",True,False),
"methadone":("methadone",["Methadose"],"Pain and opioid use disorder","Opioid agonist",True,"II","II",True,False),
"buprenorphine":("buprenorphine",["Subutex"],"Opioid use disorder and pain","Partial opioid agonist",True,"III","III",True,False),
"naloxone":("naloxone",["Narcan"],"Opioid overdose reversal","Opioid antagonist",False,"NONCONTROLLED","VI",False,False),
"isotretinoin":("isotretinoin",["Absorica"],"Severe recalcitrant nodular acne","Retinoid",False,"NONCONTROLLED","VI",False,False),
"mifepristone":("mifepristone",["Mifeprex"],"Medication abortion","Progesterone receptor antagonist",False,"NONCONTROLLED","VI",False,False),
"sodium-oxybate":("sodium oxybate",["Xyrem"],"Narcolepsy","CNS depressant",True,"III","III",True,False),
"clozapine":("clozapine",["Clozaril"],"Treatment-resistant schizophrenia","Atypical antipsychotic",False,"NONCONTROLLED","VI",False,False),
"hydromorphone":("hydromorphone",["Dilaudid"],"Pain","Opioid analgesic",True,"II","II",True,False),
"lorazepam":("lorazepam",["Ativan"],"Anxiety disorders","Benzodiazepine",True,"IV","IV",True,False),
}

def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load_specs():
    rows=[]
    for name in SPEC_FILES:
        rows += json.loads((SPEC/name).read_text(encoding="utf-8"))
    overrides={x["id"]:x for x in json.loads((SPEC/"spec_overrides.json").read_text(encoding="utf-8"))}
    rows=[overrides.get(x["id"],x) for x in rows]
    rows.sort(key=lambda x:x["id"])
    return rows

def current_ids(folder: Path, key: str):
    out=set()
    for p in folder.glob("*.json"):
        try: out.add(json.loads(p.read_text(encoding="utf-8"))[key])
        except Exception: pass
    return out

def build_rule(rule_id, meta):
    jur,area,topic,subtopic,summary,name,section,url,atype=meta
    return {"rule_id":rule_id,"content_version":1,"content_hash":ZERO,"title":subtopic.title(),"jurisdiction":jur,"area":area,"topic":topic,"subtopic":subtopic,"rule_summary":summary,"exam_relevance":"Tests a distinct pharmacist decision path using current official authority rather than rote trivia.","authority":[{"type":atype,"name":name,"section":section,"url":url}],"status":"CURRENT","effective_date":None,"supersedes":[],"last_verified":TODAY,"numeric_facts":[],"exceptions":[],"common_confusions":[],"related_rule_ids":[],"verification_status":"OFFICIAL_POLICY_VERIFIED" if jur=="MA" else "PRIMARY_VERIFIED","verification_notes":"Authoring-session current official-source verification on 2026-08-14; requires fresh independent audit before release."}

def build_drug(drug_id, meta):
    generic,brands,indication,tclass,controlled,fsched,msched,pmp,concern=meta
    base_rule="FED-CS-SCHEDULES" if controlled else "MA-SCHEDULE-VI"
    consequence={"summary":"Apply the drug's current schedule/product-specific legal pathway before dispensing.","rule_ids":[base_rule]}
    return {"drug_id":drug_id,"content_version":1,"content_hash":ZERO,"generic_name":generic,"brand_names":brands,"main_indications":[indication],"therapeutic_class":tclass,"federal_status":{"controlled":controlled,"schedule":fsched},"massachusetts_status":{"schedule":msched,"masspat_reportable":pmp,"drug_of_concern":concern},"legal_consequences":{"refill":dict(consequence),"transfer":dict(consequence),"partial_fill":dict(consequence),"masspat":{"summary":"Apply Massachusetts PMP reporting when the drug is reportable.","rule_ids":["MA-PMP-REPORTING"] if pmp else [base_rule]},"quantity_limit":dict(consequence)},"verified_rule_dependencies":{},"authorities":[{"type":"FDA_LABEL","name":f"DailyMed search for {generic}","section":"Indications and Drug Abuse/Dependence when applicable","url":"https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=" + generic.replace(" ","%20")},{"type":"STATE_REGULATION","name":"Massachusetts controlled-substance schedules","section":"105 CMR 700","url":"https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c"}],"last_verified":TODAY,"verification_status":"PRIMARY_VERIFIED","verification_notes":"Identity/status authoring record prepared from official sources for Batch 2; fresh independent audit required before release."}

def build_question(s):
    ids="ABCDE"
    choices=[]; correct=[]; analysis={}
    for i,(text,is_correct,why) in enumerate(s["choices"]):
        cid=ids[i]; choices.append({"id":cid,"text":text}); analysis[cid]=why
        if is_correct: correct.append(cid)
    return {"question_id":s["id"],"family_id":s["family"],"area":s["area"],"topic":s["topic"],"subtopic":s["subtopic"],"difficulty":s["difficulty"],"question_type":s["type"],"provenance":"GEN","source_signal_ids":[],"stem":s["stem"],"choices":choices,"correct_choice_ids":correct,"explanation":{"core_reasoning":s["core"],"choice_analysis":analysis,"related_facts":s["facts"],"mpje_trap":s["trap"]},"rule_ids":s["rules"],"drug_ids":s["drugs"],"reasoning_steps":s["steps"],"verification_status":"AUDIT_PENDING","lifecycle_status":"AUDIT_PENDING","last_legal_review":TODAY,"audits":[],"duplicate_review_status":"PENDING","independent_audit_status":"PENDING","final_adjudication":None,"development_fixture":True}

def validate_specs(rows):
    expected=[f"MA-Q-{i:04d}" for i in range(131,211)]
    assert [x["id"] for x in rows]==expected
    assert len({x["family"] for x in rows})==80
    for s in rows:
        assert len(s["choices"])==5
        n=sum(bool(c[1]) for c in s["choices"])
        assert (s["type"]=="SBA" and n==1) or (s["type"]=="SATA" and 2<=n<=4)
        if s["difficulty"]==5: assert len(s["steps"])>=3
    drug=rows[40:]
    assert sum(x["type"]=="SATA" for x in drug)==30
    assert sum(x["type"]=="SBA" for x in drug)==10
    assert {d:sum(x["difficulty"]==d for x in drug) for d in (3,4,5)}=={3:12,4:20,5:8}

def main():
    rows=load_specs(); validate_specs(rows)
    rule_ids=current_ids(DATA/"rules","rule_id")
    for rid,meta in RULES.items():
        if rid not in rule_ids: dump(DATA/"rules"/(rid.lower()+".json"),build_rule(rid,meta))
    drug_ids=current_ids(DATA/"drugs","drug_id")
    referenced={d for s in rows for d in s["drugs"]}
    missing=sorted(referenced-drug_ids)
    unknown=[d for d in missing if d not in DRUGS]
    assert not unknown, f"missing drug metadata: {unknown}"
    for d in missing: dump(DATA/"drugs"/(d+".json"),build_drug(d,DRUGS[d]))
    for s in rows: dump(DATA/"questions"/(s["id"].lower()+".json"),build_question(s))
    matrix_path=DATA/"exam_style"/"question_family_matrix.json"
    matrix=json.loads(matrix_path.read_text(encoding="utf-8"))
    existing={f["family_id"] for f in matrix["families"]}
    for s in rows:
        if s["family"] in existing: continue
        matrix["families"].append({"family_id":s["family"],"area":s["area"],"topic":s["topic"],"subtopic":s["subtopic"],"primary_rule_ids":s["rules"][:1],"secondary_rule_ids":s["rules"][1:],"drug_required":bool(s["drugs"]),"scenario_types":["practice scenario"],"common_traps":[s["trap"]],"target_difficulties":[s["difficulty"]],"target_item_types":[s["type"]],"max_questions_in_final_bank":3,"current_candidate_count":1,"current_released_count":0})
    matrix["last_reviewed"]=TODAY
    dump(matrix_path,matrix)
    blueprint=[]
    for s in rows:
        blueprint.append({"question_id":s["id"],"part":"CORE" if s["id"]<"MA-Q-0171" else "DRUG_TRIGGERED","question_type":s["type"],"difficulty":s["difficulty"],"topic":s["topic"],"subtopic":s["subtopic"],"intended_decision_path":" -> ".join(s["steps"]),"drug_ids":s["drugs"],"rule_ids":s["rules"],"distinct_from_existing_bank":s["distinct"],"smart_guess_resistance":s["anti_guess"]})
    dump(SPEC/"batch2_blueprint.json",{"base_main_sha":"67626815564062bd7f7bfec5b3667ba0deb03454","generated_on":TODAY,"question_count":80,"questions":blueprint})
    print("Batch 2 canonical source generated: 80 questions")

if __name__=="__main__": main()

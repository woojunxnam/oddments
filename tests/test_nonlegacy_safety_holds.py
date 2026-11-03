"""Current evidence may contain defaults without rewriting archives or release evidence."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_representative_rewrites as builder
import practice_quality
from publish_practice import build_payload, render


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(builder.encoded(value))
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def evidence(tmp_path):
    banks = [json.loads((ROOT / name).read_text()) for name in
             [*builder.ARCHIVES, 'practice_expansion/2026-10-28-representative/questions.json']]
    by_id = {q['question_id']: q for bank in banks for q in bank['questions']}
    previous = {q['question_id'] for q in banks[2]['questions']}
    rewrites = {q['question_id'] for q in banks[3]['questions']}
    baseline = json.loads(builder.ORIGINAL_SELECTION.read_text())
    legacy = set(baseline['recommended_ids']) - previous
    authority = dict(source_id='official', official_url='https://www.mass.gov/example',
                     exact_section='Fixture section 1', law_checked_date='2026-11-03')
    ids = ['MA-REV-0058', 'MA-RW-0001']
    report = dict(schema_version='fixture-author-review/1', source_register={'official': authority}, records=[])
    for qid in ids:
        report['records'].append(dict(question_id=qid, record_sha256=builder.raw_record_hash(by_id[qid]),
            disposition='HOLD', checked_at='2026-11-03',
            reviewer_provenance=dict(author_session='fixture-author-session', independent=False),
            choice_by_choice_findings={c['id']:dict(finding_ko='테스트 근거', authorities=[authority])
                                      for c in by_id[qid]['choices']}))
    source = 'reports/full-corpus-review/fixture-author-review.json'
    sha = write(tmp_path / source, report)
    holds = [dict(question_id=qid, question_record_sha256=builder.raw_record_hash(by_id[qid]),
                  review_source=source, review_source_sha256=sha,
                  reason='테스트 보류 이유 ' + qid, next_action='새 ID로 수정 후 검토') for qid in ids]
    def persist():
        sha = write(tmp_path / source, report)
        for hold in holds:
            hold['review_source_sha256'] = sha
        write(tmp_path / builder.NONLEGACY_HOLDS,
              dict(schema_version='nonlegacy-default-safety-holds/1', holds=holds))
    persist()
    return dict(root=tmp_path, by_id=by_id, previous=previous, rewrites=rewrites, legacy=legacy,
                baseline=baseline, source=source, report=report, holds=holds, persist=persist)


def validate(evidence):
    e=evidence
    return builder.load_safety_holds(e['by_id'],e['previous'],e['rewrites'],e['legacy'],
                                    e['previous']|e['rewrites'],{},e['root'])


def test_only_explicit_current_review_failures_are_accepted(evidence):
    assert validate(evidence) == evidence['holds']
    evidence['report']['records'][0]['disposition'] = 'KEEP'
    evidence['persist']()
    with pytest.raises(ValueError,match='nonKEEP/failure'):
        validate(evidence)


@pytest.mark.parametrize('field,value,message', [
    ('question_id','MA-REV-9999','Unknown nonlegacy'),
    ('question_id','MA-EXP-0003','Original355'),
    ('question_record_sha256','0'*64,'Stale safety hold record'),
    ('review_source_sha256','0'*64,'Stale safety review source'),
    ('review_source','reports/full-corpus-review/../../secret.json','Unsafe nonlegacy'),
    ('review_source','reports/representative-rewrite/default-holds.json','Unsafe nonlegacy'),
    ('reason',' ','reason/next_action'),
    ('next_action','','reason/next_action'),
])
def test_invalid_hold_cannot_remove_a_default(evidence,field,value,message):
    evidence['holds'][0][field]=value
    write(evidence['root']/builder.NONLEGACY_HOLDS,
          dict(schema_version='nonlegacy-default-safety-holds/1',holds=evidence['holds']))
    with pytest.raises(ValueError,match=message):
        validate(evidence)


@pytest.mark.parametrize('mutation,message', [
    ('duplicate_hold','Duplicate nonlegacy'),('duplicate_review','Duplicate safety review'),
    ('wrong_id','matching current record'),('wrong_hash','matching current record'),
    ('unattributed','nonKEEP/failure'),('nonofficial','invalid official authority'),
    ('missing_options','individual option review'),('wrong_source','invalid official authority'),
])
def test_review_must_bind_actual_id_hash_provenance_and_official_sources(evidence,mutation,message):
    e=evidence;r=e['report']['records'][0]
    if mutation=='duplicate_hold':e['holds'].append(copy.deepcopy(e['holds'][0]))
    elif mutation=='duplicate_review':e['report']['records'].append(copy.deepcopy(r))
    elif mutation=='wrong_id':r['question_id']='MA-REV-0001'
    elif mutation=='wrong_hash':r['record_sha256']='0'*64
    elif mutation=='unattributed':r['reviewer_provenance']['independent']=True
    elif mutation=='nonofficial':
        for a in r['choice_by_choice_findings']['A']['authorities']:a['official_url']='https://example.org/unofficial'
    elif mutation=='missing_options':r['choice_by_choice_findings'].pop('A')
    elif mutation=='wrong_source':e['report']['source_register']={}
    e['persist']()
    with pytest.raises(ValueError,match=message):validate(e)


def test_true_independent_failure_can_contain_but_pass_cannot(evidence):
    e=evidence
    authorities=e['report']['records'][0]['choice_by_choice_findings']['A']['authorities']
    e['report'].update(independent_of_authors=True,auditor_instance='fixture-independent-session',
                       canonical_audit=False,canonical_release_credit=0,sources=authorities)
    for r in e['report']['records']:
        r.pop('reviewer_provenance')
        r['legal_review']=dict(verdict='KEEP',existing_answer_correct='YES',authorities=authorities)
        r['realism_review']=dict(verdict='FAIL')
    e['persist']()
    assert len(validate(e))==2
    e['report']['records'][0]['realism_review']['verdict']='PASS'
    e['persist']()
    with pytest.raises(ValueError,match='nonKEEP/failure'):validate(e)


def derived_selection(e):
    baseline_build=builder.build()
    original_loader=builder.load_safety_holds
    def fixture_loader(by_id,previous,rewrites,legacy,defaults,hashes,root=None):
        return original_loader(by_id,previous,rewrites,legacy,defaults,hashes,e['root'])
    with patch.object(builder,'load_safety_holds',side_effect=fixture_loader):
        result=builder.build()
    selection=result[builder.BASE/'selection.json']
    return baseline_build,result,selection


def test_builder_separates_counts_and_preserves_every_raw_question(evidence):
    e=evidence
    before,result,s=derived_selection(e)
    old=before[builder.BASE/'selection.json']
    held={h['question_id'] for h in e['holds']}
    assert set(s['recommended_ids'])==set(old['recommended_ids'])-held
    assert s['stats']['recommended']==old['stats']['recommended']-2
    assert s['stats']['previous_quality']==96
    assert s['stats']['previous_quality_default']==95
    assert s['stats']['previous_quality_safety_held']==1
    assert s['stats']['rewrite_safety_held']==1
    assert s['stats']['rewrite_default']==len(s['new_ids'])-1
    for key in ['legacy_representatives_remaining','held_from_default','baseline_legacy_representatives',
                'newly_authored_replacements','replaced_by_existing_quality','available_total']:
        assert s['stats'][key]==old['stats'][key]
    assert s['holds']==old['holds'] and s['previous_quality_ids']==old['previous_quality_ids']
    assert result[builder.BASE/'questions.json']['questions']==before[builder.BASE/'questions.json']['questions']
    assert builder.validate_nonlegacy_selection(s,e['baseline'],e['by_id'],e['root'])==e['holds']
    tampered=copy.deepcopy(s)
    tampered['recommended_ids'].remove('MA-REV-0001')
    with pytest.raises(ValueError,match='explicit replacement/hold'):
        builder.validate_nonlegacy_selection(tampered,e['baseline'],e['by_id'],e['root'])
    tampered=copy.deepcopy(s)
    tampered['previous_quality_ids'].remove('MA-REV-0058')
    with pytest.raises(ValueError,match='archive preservation'):
        builder.validate_nonlegacy_selection(tampered,e['baseline'],e['by_id'],e['root'])


def test_attach_rechecks_evidence_and_raw_records_instead_of_delivery_metadata(evidence):
    e=evidence
    _,result,s=derived_selection(e)
    for relative in [*builder.ARCHIVES,'practice_expansion/2026-10-27-quality/selection.json',
                     'practice_expansion/2026-10-28-representative/questions.json']:
        target=e['root']/relative;target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(ROOT/relative)
    selection_path='practice_expansion/2026-10-28-representative/selection.json'
    sha=write(e['root']/selection_path,s)
    original=build_payload()
    with patch.object(practice_quality,'ROOT',e['root']):
        data=practice_quality.attach(copy.deepcopy(original),dict(path=selection_path,sha256=sha))
    assert data['questions']==original['questions']
    assert data['representative_revision']['safety_holds']==e['holds']
    assert len(data['quality_selection']['new_ids'])==96
    assert len(data['representative_revision']['previous_quality_ids'])==96
    html=render(data)
    assert '기본 포함 95개·별도 안전 보류 1개' in html
    assert 'QC.chaos(Q,count)' in html and "KEY='oddments.mpje.practice.v1'" in html
    # Execute the actual generated warning function for both previous96 and MA-RW.
    function=next(line for line in html.splitlines() if line.startswith('function revisionNotice('))
    js=r'''
const assert=require('assert/strict');
function el(tag,text){return {tag,text,childNodes:[],append(...nodes){this.childNodes.push(...nodes);},replaceChildren(){this.childNodes=[];}};}
const box=el('div'),$=()=>box,session=null;
const revisionLinks=new Map(),archiveReviewNotices=new Map();
const heldVersions=new Map([['MA-REV-0058',{reason:'exact reason',next_action:'next'}],['MA-RW-0001',{reason:'RW reason',next_action:'next'}]]);
function allText(node){return [node.text||'',...node.childNodes.map(allText)].join(' ');}
'''+function+r'''
revisionNotice({question_id:'MA-REV-0058'});assert.equal(box.hidden,false);assert.match(allText(box),/exact reason/);
revisionNotice({question_id:'MA-RW-0001',revision_of:'MA-EXP-0003'});assert.match(allText(box),/RW reason/);assert.match(allText(box),/이전 문항 보기/);
'''
    run=subprocess.run(['node','-e',js],capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    changed=copy.deepcopy(s);changed['safety_holds']=[]
    sha=write(e['root']/selection_path,changed)
    with patch.object(practice_quality,'ROOT',e['root']),pytest.raises(ValueError,match='differ from source evidence'):
        practice_quality.attach(copy.deepcopy(original),dict(path=selection_path,sha256=sha))


def test_safety_hold_must_have_been_a_default_candidate(evidence):
    e=evidence
    with pytest.raises(ValueError,match='not a default candidate'):
        builder.validate_safety_holds(e['holds'],e['by_id'],e['previous'],e['rewrites'],e['legacy'],
                                     set(),root=e['root'])


def test_nonlegacy_safety_holds_do_not_change_original355_ledger_statuses(evidence):
    import build_representative_audit_ledger as ledger
    e=evidence
    _,_,selection=derived_selection(e)
    old=ledger.build_ledger()
    original_read=ledger.read
    original_loader=builder.load_safety_holds
    def fixture_read(path):
        return selection if path==ledger.SELECTION else original_read(path)
    def fixture_loader(by_id,previous,rewrites,legacy,defaults,hashes,root=None):
        return original_loader(by_id,previous,rewrites,legacy,defaults,hashes,e['root'])
    with patch.object(ledger,'read',side_effect=fixture_read),patch.object(builder,'load_safety_holds',side_effect=fixture_loader):
        updated=ledger.build_ledger()
    assert updated['counts']['implementation_statuses']==old['counts']['implementation_statuses']
    assert updated['counts']['original_representatives']==355
    assert updated['counts']['previous_quality_retained']==96
    assert updated['counts']['previous_quality_default']==95
    assert updated['counts']['previous_quality_safety_held']==1
    assert updated['counts']['rewrite_safety_held']==1
    assert updated['counts']['current_default']==old['counts']['current_default']-2
    assert [r['editorial_triage'] for r in updated['questions']]==[r['editorial_triage'] for r in old['questions']]
    rwrow=next(r for r in updated['questions'] if r['implementation']['replacement_question_id']=='MA-RW-0001')
    assert rwrow['implementation_status']=='REWRITTEN_NEW_ID'
    assert rwrow['implementation']['replacement_is_in_current_default'] is False
    assert rwrow['implementation']['replacement_default_safety_hold']==e['holds'][1]
    text=ledger.render_markdown(updated).decode()
    assert '기본 목록에는 95개를 포함하고 1개는 별도 안전 보류' in text
    assert 'MA-RW-0001 (별도 안전 보류)' in text

"""One immutable memo binding never turns missing legal payloads into evidence."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import independent_public_style_bindings as public_style
from build_full_corpus_review import validate_independent_source_bytes


def sha(raw):return hashlib.sha256(raw).hexdigest()


def write(root,path,value):
    target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())
    return sha(target.read_bytes())


def commit(root):
    subprocess.run(['git','-C',str(root),'add','.'],check=True)
    subprocess.run(['git','-C',str(root),'commit','--allow-empty','-qm','fixture checkpoint'],check=True)


def bindings(report):
    return {r['question_id']:dict(source_path=public_style.REPORT_PATH,
        source_sha256=public_style.REPORT_SHA256)for r in report['records']}


@pytest.fixture
def captured(tmp_path):
    report=json.loads((ROOT/public_style.REPORT_PATH).read_bytes())
    paths=[public_style.REPORT_PATH,public_style.MEMO_PATH]+[
        s['metadata_path']for s in report['sources']if s['source_id']in public_style.PUBLIC_STYLE_URLS]
    for path in paths:
        target=tmp_path/path;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/path,target)
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    for key,value in [('user.name','Fixture'),('user.email','fixture@example.invalid')]:
        subprocess.run(['git','-C',str(tmp_path),'config',key,value],check=True)
    commit(tmp_path)
    return tmp_path,report


def projected(root,report,source_bindings=None):
    return public_style.validation_sources(root,report,
        source_bindings=bindings(report)if source_bindings is None else source_bindings)


def repin_fixture(root,report,monkeypatch,*,metadata_change=None,memo_change=None):
    """Independently exercise deeper guards even after all ancestor SHAs change."""
    if metadata_change:
        source=next(s for s in report['sources']if s['source_id']=='nabpsample')
        metadata=json.loads((root/source['metadata_path']).read_bytes())
        metadata_change(metadata)
        source['metadata_sha256']=write(root,source['metadata_path'],metadata)
    memo=json.loads((root/public_style.MEMO_PATH).read_bytes())
    memo['official_retrieval_metadata']=[copy.deepcopy(s)for s in report['sources']
        if s['source_id']in public_style.PUBLIC_STYLE_URLS]
    if memo_change:memo_change(memo)
    report['public_style_memo_sha256']=write(root,public_style.MEMO_PATH,memo)
    report_sha=write(root,public_style.REPORT_PATH,report)
    monkeypatch.setattr(public_style,'REPORT_SHA256',report_sha)
    commit(root)


def test_exact_report_projects_only_three_memo_bindings_without_changing_inputs(captured):
    root,report=captured;before=copy.deepcopy(report);raw=(root/public_style.REPORT_PATH).read_bytes()
    sources=projected(root,report)
    assert report==before and (root/public_style.REPORT_PATH).read_bytes()==raw
    selected=[s for s in sources if 'public_style_parent_binding'in s]
    assert len(selected)==3
    for source in selected:
        validate_independent_source_bytes(source,root)
        assert 'raw_path'not in source and 'text_path'not in source
        assert source['evidence_path']==public_style.MEMO_PATH
        parent=source['public_style_parent_binding']
        assert parent['source_sha256']==public_style.REPORT_SHA256
        assert parent['raw_payload_verified']is parent['extracted_text_verified']is False
        assert all(parent[k]==0 for k in parent if k.endswith('credit'))
    for old,new in zip(report['sources'],sources):
        if old['source_id']not in public_style.PUBLIC_STYLE_URLS:assert old==new
    sources[0]['source_id']='mutated returned copy'
    assert report==before


@pytest.mark.parametrize('path',[public_style.REPORT_PATH,public_style.MEMO_PATH,
    public_style.EVIDENCE_PREFIX+'sources/nabpsample.meta.json'])
@pytest.mark.parametrize('committed',[False,True])
def test_report_memo_and_metadata_tamper_fail_even_when_committed(captured,path,committed):
    root,report=captured;target=root/path;target.write_bytes(target.read_bytes()+b' ')
    if committed:commit(root)
    with pytest.raises(ValueError):projected(root,report)


@pytest.mark.parametrize('defect',['wrong_report_sha','one_missing_binding','other_report','no_bindings'])
def test_projection_requires_this_reports_validated_consumer_bindings(captured,defect):
    root,report=captured;b=bindings(report)
    if defect=='wrong_report_sha':next(iter(b.values()))['source_sha256']='0'*64
    elif defect=='one_missing_binding':b.pop(next(iter(b)))
    elif defect=='other_report':
        for item in b.values():item['source_path']='reports/full-corpus-review/another-report.json'
    else:b={}
    if defect in {'other_report','no_bindings'}:
        sources=projected(root,report,b)
        assert sources==report['sources']
        for source in sources:
            if source['source_id']in public_style.PUBLIC_STYLE_URLS:
                with pytest.raises(ValueError):validate_independent_source_bytes(source,root)
    else:
        with pytest.raises(ValueError):projected(root,report,b)


def test_in_memory_report_change_and_source_duplication_do_not_match_fixed_head(captured):
    root,report=captured;report['sources'].append(copy.deepcopy(report['sources'][-1]))
    with pytest.raises(ValueError,match='differs'):projected(root,report)


@pytest.mark.parametrize('defect',['external_url','wrong_id','duplicate_report_source',
    'duplicate_memo_source','memo_source_differs','memo_timestamp','review_date',
    'metadata_raw_sha','metadata_text_sha','metadata_url','metadata_timestamp','metadata_missing_field'])
def test_rehashed_ancestors_cannot_bypass_exact_scope_or_metadata_links(captured,monkeypatch,defect):
    root,report=captured;source=next(s for s in report['sources']if s['source_id']=='nabpsample')
    meta=None;memo=None
    if defect=='external_url':source['official_url']=source['final_url']='https://example.invalid/style'
    elif defect=='wrong_id':source['source_id']='other-style'
    elif defect=='duplicate_report_source':report['sources'].append(copy.deepcopy(source))
    elif defect=='duplicate_memo_source':memo=lambda m:m['official_retrieval_metadata'].append(copy.deepcopy(m['official_retrieval_metadata'][0]))
    elif defect=='memo_source_differs':memo=lambda m:m['official_retrieval_metadata'][0].update(retention='changed')
    elif defect=='memo_timestamp':memo=lambda m:m.update(reviewed_at='2026-11-04T00:00:00+00:00')
    elif defect=='review_date':report['reviewed_at']='2026-11-03'
    elif defect=='metadata_missing_field':meta=lambda m:m.pop('retrieved_at')
    else:
        key={'metadata_raw_sha':'raw_sha256','metadata_text_sha':'text_sha256',
             'metadata_url':'official_url','metadata_timestamp':'retrieved_at'}[defect]
        value='0'*64 if key.endswith('sha256')else 'https://example.invalid/'if key=='official_url'else '2026-11-03T00:00:00+00:00'
        meta=lambda m:m.update({key:value})
    repin_fixture(root,report,monkeypatch,metadata_change=meta,memo_change=memo)
    before=copy.deepcopy(report)
    with pytest.raises(ValueError):projected(root,report)
    assert report==before


@pytest.mark.parametrize('key',['public_style_memo_sha256','metadata_sha256'])
def test_wrong_parent_or_metadata_sha_is_rejected(captured,monkeypatch,key):
    root,report=captured
    if key=='public_style_memo_sha256':report[key]='0'*64
    else:next(s for s in report['sources']if s['source_id']=='nabpsample')[key]='0'*64
    report_sha=write(root,public_style.REPORT_PATH,report)
    monkeypatch.setattr(public_style,'REPORT_SHA256',report_sha);commit(root)
    with pytest.raises(ValueError):projected(root,report)


@pytest.mark.parametrize('path',[public_style.REPORT_PATH,public_style.MEMO_PATH,
    public_style.EVIDENCE_PREFIX+'sources/nabpsample.meta.json'])
def test_same_bytes_symlink_is_not_a_committed_input(captured,path):
    root,report=captured;target=root/path;copy_path=root/'same-bytes.json'
    copy_path.write_bytes(target.read_bytes());target.unlink();target.symlink_to(copy_path)
    with pytest.raises(ValueError):projected(root,report)


def test_missing_government_payload_still_fails_the_original_validator(captured,monkeypatch):
    root,report=captured
    government=next(s for s in report['sources']if s['source_id']not in public_style.PUBLIC_STYLE_URLS)
    government['raw_path']=None
    repin_fixture(root,report,monkeypatch)
    source=next(s for s in projected(root,report)if s['source_id']==government['source_id'])
    assert source==government
    with pytest.raises(ValueError,match='Incomplete'):validate_independent_source_bytes(source,root)


def test_head_advance_during_projection_rejects_the_result(captured,monkeypatch):
    root,report=captured;original=public_style.committed;advanced=False
    def advance(*args,**kwargs):
        nonlocal advanced
        raw=original(*args,**kwargs)
        if not advanced:commit(root);advanced=True
        return raw
    monkeypatch.setattr(public_style,'committed',advance)
    with pytest.raises(ValueError,match='HEAD advanced'):projected(root,report)

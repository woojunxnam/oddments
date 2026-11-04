"""Bounded wrapper evolution; native evidence is stubbed only in model fixtures."""
import copy
import json

import pytest

import notes_published15_closure as c
import legacy_independent_metadata as native
from test_notes_published15_closure import put,commit,git


@pytest.fixture
def wrapper(tmp_path,monkeypatch):
    root=tmp_path/'repo';root.mkdir();git(root,'init','-q')
    git(root,'config','user.name','Synthetic wrapper fixture')
    git(root,'config','user.email','fixture@example.invalid')
    previous=dict(question_ids=['SYNTHETIC-1'],question_record_hashes={'SYNTHETIC-1':'q1'},
                  issue_type='AUTHOR_REVIEW_FINDING',reason='Synthetic retained negative',
                  review_source='reports/full-corpus-review/old.json',review_source_sha256='old')
    old_notices=dict(notices=[previous])
    oldraw=c.encoded(old_notices)
    oldbank=dict(edition='UNCHANGED',source_authoring_hashes={c.ARCHIVE_NOTICES:c.sha(oldraw),'other':'constant'},
                 questions=[dict(question_id='SYNTHETIC-1',stem='Unchanged',correct_choice_ids=['A'])],sources={'official':'same'})
    newnotice=dict(question_ids=['SYNTHETIC-1'],question_record_hashes={'SYNTHETIC-1':'q1'},
                   issue_type='INDEPENDENT_REVIEW_FINDING',reason='Synthetic new negative',
                   review_source='reports/full-corpus-review/native.json',review_source_sha256='native',checked_at='2026-11-04',
                   previous_notices=[previous])
    current_notices=dict(notices=[newnotice]);currentbank=copy.deepcopy(oldbank)
    currentbank['source_authoring_hashes'][c.ARCHIVE_NOTICES]=c.sha(c.encoded(current_notices))
    preimages={};files={}
    for p,raw in [(c.REPRESENTATIVE_BANK,c.encoded(oldbank)),(c.ARCHIVE_NOTICES,oldraw)]:
        destination=c.PREIMAGES+'synthetic/'+p;put(root,destination,raw)
        files[p]={'raw_sha256':c.sha(raw)}
        preimages[p]={'path':destination,'raw_sha256':c.sha(raw)}
    put(root,c.REPRESENTATIVE_BANK,currentbank);put(root,c.ARCHIVE_NOTICES,current_notices)
    commit(root,'synthetic exact preserved bank and notice wrapper update')
    def integrated(root,source_bindings):
        source_bindings['SYNTHETIC-1']=dict(source_path='reports/full-corpus-review/native.json',source_sha256='native',record_sha256='q1',reviewed_at='2026-11-04')
    monkeypatch.setattr(native,'integrated_sources',integrated)
    monkeypatch.setattr(c,'verify_representative_outputs',lambda root:None)
    return root,dict(full_source_files=files,retained_preimages=preimages),currentbank,current_notices


def test_exact_native_negative_notice_digest_can_evolve_without_changing_question(wrapper):
    root,closure,_,_=wrapper
    c.validate_archive_notice_wrapper(root,closure)
    assert json.loads(c.old_bytes(root,closure,c.REPRESENTATIVE_BANK))['questions']==json.loads(c.committed(root,c.REPRESENTATIVE_BANK))['questions']


@pytest.mark.parametrize('defect',['question','key','source','metadata','other_hash','stale_notice_hash',
                                  'drop_warning','drop_history','fabricated_report','positive_type','wrong_current_hash','credit','date'])
def test_wrapper_exception_rejects_content_changes_or_unbound_warning_history(wrapper,defect):
    root,closure,bank,notices=wrapper
    if defect=='question':bank['questions'][0]['stem']='Changed question'
    elif defect=='key':bank['questions'][0]['correct_choice_ids']=['B']
    elif defect=='source':bank['sources']['official']='Changed authority'
    elif defect=='metadata':bank['edition']='Changed edition'
    elif defect=='other_hash':bank['source_authoring_hashes']['other']='Changed other input'
    elif defect=='stale_notice_hash':bank['source_authoring_hashes'][c.ARCHIVE_NOTICES]='stale'
    else:
        if defect=='drop_warning':notices['notices']=[]
        elif defect=='drop_history':notices['notices'][0]['previous_notices']=[]
        elif defect=='fabricated_report':notices['notices'][0]['review_source']='reports/full-corpus-review/fabricated.json'
        elif defect=='positive_type':notices['notices'][0]['issue_type']='AUTHOR_REVIEW_FINDING'
        elif defect=='credit':notices['notices'][0]['canonical_release_credit']=1
        elif defect=='date':notices['notices'][0]['checked_at']='2099-01-01'
        else:notices['notices'][0]['question_record_hashes']['SYNTHETIC-1']='another-content'
        bank['source_authoring_hashes'][c.ARCHIVE_NOTICES]=c.sha(c.encoded(notices))
    put(root,c.REPRESENTATIVE_BANK,bank);put(root,c.ARCHIVE_NOTICES,notices)
    commit(root,'synthetic rejected wrapper attack '+defect)
    with pytest.raises(ValueError):c.validate_archive_notice_wrapper(root,closure)


def test_missing_native_integration_cannot_be_replaced_by_a_source_declaration(wrapper,monkeypatch):
    root,closure,_,_=wrapper
    monkeypatch.setattr(native,'integrated_sources',lambda *a,**k:[])
    with pytest.raises(ValueError,match='actual integrated'):c.validate_archive_notice_wrapper(root,closure)


def test_failed_deterministic_builder_is_not_a_wrapper_exception(wrapper,monkeypatch):
    root,closure,_,_=wrapper
    def failure(root):raise ValueError('synthetic deterministic builder rejection')
    monkeypatch.setattr(c,'verify_representative_outputs',failure)
    with pytest.raises(ValueError,match='deterministic'):c.validate_archive_notice_wrapper(root,closure)

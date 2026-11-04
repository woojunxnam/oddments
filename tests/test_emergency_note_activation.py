"""Emergency boundary fixes activate only with exact body/source/audit evidence."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from notes_revision import PATHS, load_notes, apply_study_revision
from notes_emergency_activation import (
    ACTIVATION, CENSUS, REVIEW, REVISION_M, UNIT_IDS, SOURCE_IDS,
    official_url, validate_emergency_note_review, validate_review_contents,
)
from verify_representative_protected import migrated_baseline_bytes, verify

MIGRATION = 'revisions/notes/protected-migration-emergency-kit.json'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def emergency_copy(tmp_path):
    shutil.copytree(ROOT/'revisions', tmp_path/'revisions')
    shutil.copytree(ROOT/'notes', tmp_path/'notes')
    safety='reports/full-corpus-review/canonical-q0012-withdrawal'
    shutil.copytree(ROOT/safety,tmp_path/safety)
    for relative in ['reports/representative-rewrite/protected-baseline.json',
                     'site/generated/preview_allowlist.json']:
        dest=tmp_path/relative;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/relative,dest)
    evidence = 'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103'
    shutil.copytree(ROOT/evidence, tmp_path/evidence)
    paths = {'site/notes/build.json', 'site/notes/complete-notes.md',
             'reports/full-corpus-review/note-wave8-census.json',
             'reports/full-corpus-review/note-wave9-census.json'}
    annotation = ROOT/'revisions/notes/protected-migration-independent-notes-wave2.json'
    if annotation.exists():
        paths.update(json.loads(annotation.read_bytes())['independent_reviews'])
    for activation_path in (ROOT/'revisions/notes').glob('*-activation.json'):
        activation = json.loads(activation_path.read_bytes())
        report = json.loads((ROOT/activation['review_path']).read_bytes())
        paths.update([activation['review_path'], activation['census_path']])
        paths.update(s['evidence_path'] for s in report['sources'])
        if report.get('prior_review'):
            paths.add(report['prior_review']['path'])
    for path in paths:
        destination = tmp_path/path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/path, destination)
    if annotation.exists():
        # These original activation tests exercise the published twelve-guard
        # context. Annotation-specific tests install their own later layers.
        (tmp_path/annotation.relative_to(ROOT)).unlink()
        for source,target in [('complete-notes-pr188.md','complete-notes.md'),
                              ('notes-build-pr188.json','build.json')]:
            shutil.copyfile(tmp_path/'revisions/baselines'/source,tmp_path/'site/notes'/target)
    (tmp_path/'revisions/notes/protected-migration-independent-notes-wave3.json').unlink(missing_ok=True)
    return tmp_path


@pytest.fixture
def annotation_copy(emergency_copy):
    root=emergency_copy
    # Synthetic annotation bytes exercise protection only; these fixtures do not
    # constitute legal audits or pass the independent publication consumer.
    scope={
        'b':['w1-b-10','w1-b-11','w1-b-12','w1-c-1','w1-c-2'],
        'c':['w1-c-3','w1-c-4','w1-c-5','w1-c-6','w1-c-7'],
        'e':['w1-c-8','w4-a-21','w2-a-2','w2-a-3','w2-a-4'],
        'f':['w2-a-5','w2-a-6','w2-a-7','w2-a-8','w2-a-10'],
    }
    bindings={}
    for name,units in scope.items():
        relative=f'reports/full-corpus-review/independent-notes/second-{name}-review.json'
        path=root/relative; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(encoded(dict(stage='independent-notes',canonical_audit=False,
            canonical_release_credit=0,records=[dict(unit_id=uid) for uid in units])))
        bindings[relative]=sha(path.read_bytes())
    raw=(root/'revisions/baselines/complete-notes-pr188.md').read_bytes()+b'\n> synthetic audit annotation\n'
    (root/'site/notes/complete-notes.md').write_bytes(raw)
    metadata=dict(schema_version='notes-protected-annotation-migration/1',
        baseline_commit='b5d1b3e98ca3a7d97252b331a33cf7a4c0ba956b',
        path='site/notes/complete-notes.md',baseline_copy='revisions/baselines/complete-notes-pr188.md',
        baseline_build_copy='revisions/baselines/notes-build-pr188.json',
        baseline_build_sha256='373b22191f5c2f9565b2dc3206d93801a488cfc65eab1e97f7ffa31b8985416f',
        semantic_notes_sha256='e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824',
        previous_migration_path=MIGRATION,
        previous_migration_sha256='b74a101c0319ae9ca7cba366c55125243a2f8f9186e43bf45a7148fe8ea9fa35',
        old_sha256='8d23fa9c5e63deffd33218630a630a61d946cfd25d56bc578b553cbc37a84aaf',
        new_sha256=sha(raw),independent_reviews=bindings)
    path=root/'revisions/notes/protected-migration-independent-notes-wave2.json'
    path.write_bytes(encoded(metadata))
    return root,path,metadata


def test_annotation_decodes_pr188_export_through_all_twelve_original_guards(annotation_copy):
    root,_,_=annotation_copy
    raw=(root/'site/notes/complete-notes.md').read_bytes()
    original=(root/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert migrated_baseline_bytes(root,'site/notes/complete-notes.md',raw)==original


@pytest.mark.parametrize('change,expected',[
    ('scope','expands protected scope'),('parent','Published emergency-kit migration changed'),
    ('snapshot','Published PR188 export changed'),('build','Published PR188 build changed'),
    ('semantics','cannot authorize semantic note changes'),
    ('evidence','annotation review changed'),('units','annotation review unit scope changed'),
    ('extra_report','annotation evidence scope changed'),('output','Stale independent-note annotation export'),
])
def test_annotation_cannot_rebind_published_history_or_expand_scope(annotation_copy,change,expected):
    root,path,metadata=annotation_copy
    if change=='scope': metadata['path']='notes/guide.json'
    elif change=='parent':
        parent=root/MIGRATION; parent.write_bytes(parent.read_bytes()+b' ')
        metadata['previous_migration_sha256']=sha(parent.read_bytes())
    elif change=='snapshot':
        snapshot=root/metadata['baseline_copy']; snapshot.write_bytes(snapshot.read_bytes()+b' ')
        metadata['old_sha256']=sha(snapshot.read_bytes())
    elif change=='build':
        build=root/metadata['baseline_build_copy']; build.write_bytes(build.read_bytes()+b' ')
        metadata['baseline_build_sha256']=sha(build.read_bytes())
    elif change=='semantics':
        build=root/'site/notes/build.json'; data=json.loads(build.read_bytes())
        data['content_sha256']='0'*64; build.write_bytes(encoded(data))
        metadata['semantic_notes_sha256']='0'*64
    elif change in {'evidence','units'}:
        relative=next(iter(metadata['independent_reviews'])); report=root/relative
        data=json.loads(report.read_bytes());data['records'][0]['unit_id']='w6-b-16'
        report.write_bytes(encoded(data))
        if change=='units': metadata['independent_reviews'][relative]=sha(report.read_bytes())
    elif change=='extra_report': metadata['independent_reviews']['notes/guide.json']='0'*64
    elif change=='output':
        output=root/'site/notes/complete-notes.md'; output.write_bytes(output.read_bytes()+b' changed')
    path.write_bytes(encoded(metadata))
    with pytest.raises(ValueError,match=expected):
        migrated_baseline_bytes(root,'site/notes/complete-notes.md',(root/'site/notes/complete-notes.md').read_bytes())


@pytest.fixture
def wave3_copy(emergency_copy):
    root=emergency_copy
    # Only engineering fixtures: these minimal reports are not legal audits and
    # are never written to the real repository or accepted as publication credit.
    parent='revisions/notes/protected-migration-independent-notes-wave2.json'
    shutil.copyfile(ROOT/parent,root/parent)
    for source,target in [('complete-notes-pr189.md','complete-notes.md'),
                          ('notes-build-pr189.json','build.json')]:
        shutil.copyfile(root/'revisions/baselines'/source,root/'site/notes'/target)
    scope={
        'b':['oral-followup','w2-b-1','w2-b-2','w2-b-3','w2-b-4'],
        'e':['w2-b-5','w2-b-6','w2-b-7','w2-b-8','w2-b-9'],
        'g':['w2-b-10','w2-b-11','w2-b-12','w2-b-13','w2-c-1'],
        'f':['w2-c-2','schedule-vi-continuity','w2-c-4','w2-c-5','w2-c-6'],
    }
    bindings={}
    for name,units in scope.items():
        relative=f'reports/full-corpus-review/independent-notes/third-{name}-review.json'
        path=root/relative;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(encoded(dict(stage='independent-notes',canonical_audit=False,
            canonical_release_credit=0,question_audit_credit=0,
            records=[dict(unit_id=uid)for uid in units])))
        bindings[relative]=sha(path.read_bytes())
    raw=(root/'revisions/baselines/complete-notes-pr189.md').read_bytes()+b'\n> synthetic wave3 audit annotation\n'
    (root/'site/notes/complete-notes.md').write_bytes(raw)
    metadata=dict(schema_version='notes-protected-annotation-migration/1',
        baseline_commit='f4ecea13a31b4c8dbdb7ef460b8caee54b571b27',
        path='site/notes/complete-notes.md',baseline_copy='revisions/baselines/complete-notes-pr189.md',
        baseline_build_copy='revisions/baselines/notes-build-pr189.json',
        baseline_build_sha256='d4f24c8c32745d3b4c4d8d411fd3e07dbc94bbcbdad55fe028bccf9479a3ad2e',
        semantic_notes_sha256='e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824',
        previous_migration_path=parent,
        previous_migration_sha256='8573eced55fdd94dd9fa23ede6da19fa7049b93026200a27096cd73d503e3e8b',
        old_sha256='f4ebbad48aaea4575c123533878d59a90fc12a19391e2a3b49e13666f8a93440',
        new_sha256=sha(raw),independent_reviews=bindings,canonical_release_credit=0)
    path=root/'revisions/notes/protected-migration-independent-notes-wave3.json'
    path.write_bytes(encoded(metadata))
    return root,path,metadata


def test_wave3_decodes_pr189_through_all_thirteen_published_guards(wave3_copy):
    root,_,_=wave3_copy
    raw=(root/'site/notes/complete-notes.md').read_bytes()
    original=(root/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert migrated_baseline_bytes(root,'site/notes/complete-notes.md',raw)==original


def test_wave3_pr189_snapshots_and_published_parent_are_pinned():
    for relative,expected in [
        ('revisions/baselines/complete-notes-pr189.md','f4ebbad48aaea4575c123533878d59a90fc12a19391e2a3b49e13666f8a93440'),
        ('revisions/baselines/notes-build-pr189.json','d4f24c8c32745d3b4c4d8d411fd3e07dbc94bbcbdad55fe028bccf9479a3ad2e'),
        ('revisions/notes/protected-migration-independent-notes-wave2.json','8573eced55fdd94dd9fa23ede6da19fa7049b93026200a27096cd73d503e3e8b'),
    ]:
        assert sha((ROOT/relative).read_bytes())==expected


@pytest.mark.parametrize('relative',[
    'notes/guide.json','docs/RELEASE_POLICY.md','data/questions/ma-q-0001.json',
])
def test_wave3_layer_cannot_authorize_changes_to_protected_sources(wave3_copy,relative):
    root,_,_=wave3_copy
    manifest=json.loads((ROOT/'reports/representative-rewrite/protected-baseline.json').read_bytes())
    for row in manifest['files']:
        dest=root/row['path']
        if not dest.exists():
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/row['path'],dest)
    verify(manifest,root)
    source=root/relative;source.write_bytes(source.read_bytes()+b' ')
    with pytest.raises(ValueError):
        verify(manifest,root)


def test_wave3_allows_additional_build_annotations_without_changing_semantics(wave3_copy):
    root,_,_=wave3_copy
    path=root/'site/notes/build.json';data=json.loads(path.read_bytes())
    data['independent_note_review_progress']={'synthetic_engineering_fixture':True}
    data['additional_publication_metadata']={'synthetic':True}
    path.write_bytes(encoded(data))
    assert migrated_baseline_bytes(root,'site/notes/complete-notes.md',
        (root/'site/notes/complete-notes.md').read_bytes())==(root/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()


def test_absent_wave3_keeps_existing_thirteen_guard_behavior(wave3_copy):
    root,path,_=wave3_copy;path.unlink()
    for report in (root/'reports/full-corpus-review/independent-notes').glob('third-*-review.json'):
        report.unlink()
    raw=(root/'revisions/baselines/complete-notes-pr189.md').read_bytes()
    assert migrated_baseline_bytes(root,'site/notes/complete-notes.md',raw)==(root/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()


@pytest.mark.parametrize('change,expected',[
    ('base','Unexpected wave3'),('scope','expands protected scope'),
    ('snapshot_path','expands protected scope'),('build_path','expands protected scope'),
    ('parent','Published wave2'),('parent_path','Published wave2'),('missing_parent','Missing protected file'),
    ('snapshot','Published PR189 export changed'),('build','Published PR189 build changed'),
    ('semantics','cannot authorize semantic note changes'),('edition','cannot authorize semantic note changes'),
    ('provenance','cannot authorize semantic note changes'),('actual_semantics','cannot authorize semantic note changes'),
    ('evidence','annotation review changed'),('units','unit scope or credit changed'),
    ('duplicate_units','unit scope or credit changed'),('extra_unit','unit scope or credit changed'),
    ('missing_unit','unit scope or credit changed'),('missing_report','Missing protected file'),
    ('stage','unit scope or credit changed'),('canonical','unit scope or credit changed'),
    ('credit','unit scope or credit changed'),('question_credit','unit scope or credit changed'),
    ('extra_report','annotation evidence scope changed'),('missing_binding','annotation evidence scope changed'),
    ('output','Stale wave3'),('manifest_credit','cannot create canonical release credit'),
    ('old_guard','Published emergency-kit migration changed'),
])
def test_wave3_rejects_rebound_history_scope_credit_or_tampering(wave3_copy,monkeypatch,change,expected):
    root,path,metadata=wave3_copy
    if change=='base':metadata['baseline_commit']='0'*40
    elif change=='scope':metadata['path']='notes/guide.json'
    elif change=='snapshot_path':metadata['baseline_copy']='notes/guide.json'
    elif change=='build_path':metadata['baseline_build_copy']='notes/guide.json'
    elif change=='parent':
        parent=root/metadata['previous_migration_path'];parent.write_bytes(parent.read_bytes()+b' ')
        metadata['previous_migration_sha256']=sha(parent.read_bytes())
    elif change=='parent_path':metadata['previous_migration_path']=MIGRATION
    elif change=='missing_parent':(root/metadata['previous_migration_path']).unlink()
    elif change=='snapshot':
        snapshot=root/metadata['baseline_copy'];snapshot.write_bytes(snapshot.read_bytes()+b' ')
        metadata['old_sha256']=sha(snapshot.read_bytes())
    elif change=='build':
        build=root/metadata['baseline_build_copy'];build.write_bytes(build.read_bytes()+b' ')
        metadata['baseline_build_sha256']=sha(build.read_bytes())
    elif change in {'semantics','edition','provenance'}:
        build=root/'site/notes/build.json';data=json.loads(build.read_bytes())
        if change=='semantics':data['content_sha256']=metadata['semantic_notes_sha256']='0'*64
        elif change=='edition':data['edition']='synthetic-other-edition'
        else:data['revision_provenance']['sha256']='0'*64
        build.write_bytes(encoded(data))
    elif change=='actual_semantics':
        data=copy.deepcopy(load_notes(root));data['chapters'][0]['units'][0]['body']+=' changed actual body'
        monkeypatch.setattr('notes_revision.load_notes',lambda _root:data)
    elif change in {'evidence','units','duplicate_units','extra_unit','missing_unit','missing_report',
                     'stage','canonical','credit','question_credit'}:
        relative=next(iter(metadata['independent_reviews']));report=root/relative
        if change=='missing_report':report.unlink()
        else:
            data=json.loads(report.read_bytes())
            if change in {'evidence','units'}:data['records'][0]['unit_id']='w6-b-16'
            elif change=='duplicate_units':data['records'][0]=data['records'][1]
            elif change=='extra_unit':data['records'].append(dict(unit_id='w6-b-16'))
            elif change=='missing_unit':data['records'].pop()
            elif change=='stage':data['stage']='author'
            elif change=='canonical':data['canonical_audit']=True
            elif change=='credit':data['canonical_release_credit']=1
            else:data['question_audit_credit']=1
            report.write_bytes(encoded(data))
            if change!='evidence':metadata['independent_reviews'][relative]=sha(report.read_bytes())
    elif change=='extra_report':metadata['independent_reviews']['notes/guide.json']='0'*64
    elif change=='missing_binding':metadata['independent_reviews'].popitem()
    elif change=='output':
        output=root/'site/notes/complete-notes.md';output.write_bytes(output.read_bytes()+b' changed')
    elif change=='manifest_credit':metadata['canonical_release_credit']=1
    elif change=='old_guard':
        parent=root/MIGRATION;parent.write_bytes(parent.read_bytes()+b' ')
    path.write_bytes(encoded(metadata))
    with pytest.raises(ValueError,match=expected):
        migrated_baseline_bytes(root,'site/notes/complete-notes.md',(root/'site/notes/complete-notes.md').read_bytes())


def contents(root):
    return [json.loads((root/path).read_bytes()) for path in [REVISION_M, REVIEW, CENSUS]]


def test_emergency_activation_changes_only_two_bodies_adds_exact_sources_and_preserves_other_notes():
    before = load_notes(revision_id='2026-11-03.refill-cancer.1')
    after = load_notes()
    old = {u['id']:u for c in before['chapters'] for u in c['units']}
    new = {u['id']:u for c in after['chapters'] for u in c['units']}
    assert set(old) == set(new)
    assert {uid for uid in old if old[uid] != new[uid]} == UNIT_IDS
    assert set(after['sources']) - set(before['sources']) == SOURCE_IDS
    assert all(after['sources'][sid] == source for sid,source in before['sources'].items())
    assert '≤50 beds' in new['w4-a-19']['body']
    assert '≤10 beds, 11–20 beds, ≥21 beds' in new['w4-a-20']['body']
    assert 'Max number of units per facility' in new['w4-a-20']['body']
    assert all(new[uid]['independent_content_review']['decision'] == 'KEEP' for uid in UNIT_IDS)
    assert '2026-11-03-packaging-pamphlet-final.json' not in repr(PATHS)
    for a,b in zip(before['chapters'],after['chapters']):
        assert {k:v for k,v in a.items() if k != 'units'} == {k:v for k,v in b.items() if k != 'units'}
    assert json.loads((ROOT/REVISION_M).read_bytes())['status'] == 'AUDIT_PENDING_NOT_APPLIED'
    assert json.loads((ROOT/REVISION_M).read_bytes())['activation'] is False


def test_four_related_cards_retain_full_source_records_without_new_patch_credit():
    for kind,path,field,ids in [
        ('study','notes/study/guide.json','lessons',{'LAW-053','LAW-054'}),
        ('refresh','notes/refresh/guide.json','cards',{'RF-054','RF-056'}),
    ]:
        source = json.loads((ROOT/path).read_bytes())
        revised = apply_study_revision(copy.deepcopy(source), kind)
        assert [r for r in source[field] if r['id'] in ids] == [r for r in revised[field] if r['id'] in ids]
    report = json.loads((ROOT/REVIEW).read_bytes())
    assert report['historical_canonical_four_holds_resolved'] == report['question_audit_credit'] == 0
    assert report['derived_patches'] == []


@pytest.mark.parametrize('url',[
    'https://www.mass.gov.evil.invalid/doc/source', 'https://www.mass.gov@evil.invalid/source',
    'http://www.mass.gov/doc/source', 'https://www.mass.gov:444/doc/source',
])
def test_official_hostname_whitelist_rejects_lookalikes_and_credentials(url):
    assert not official_url(url)


@pytest.mark.parametrize('path', [REVISION_M, REVIEW, CENSUS])
def test_rebinding_changed_candidate_or_audit_hashes_does_not_authorize_activation(emergency_copy,path):
    root = emergency_copy
    value = json.loads((root/path).read_bytes())
    value['unreviewed_change'] = True
    (root/path).write_bytes(encoded(value))
    activation = json.loads((root/ACTIVATION).read_bytes())
    field = {REVISION_M:'revision_sha256', REVIEW:'review_sha256', CENSUS:'census_sha256'}[path]
    activation[field] = sha((root/path).read_bytes())
    (root/ACTIVATION).write_bytes(encoded(activation))
    raw = (root/REVISION_M).read_bytes()
    with pytest.raises(ValueError,match='activation binding changed'):
        validate_emergency_note_review(root,raw,json.loads(raw))


def test_duplicate_keep_cannot_hide_a_failed_atomic_claim(emergency_copy):
    revision,review,census = contents(emergency_copy)
    failed = copy.deepcopy(review['claims'][0]); failed['verdict'] = 'HOLD'
    review['claims'].insert(0,failed)
    with pytest.raises(ValueError,match='atomic claim coverage changed'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_keep_summary_cannot_override_failed_body_or_claim(emergency_copy):
    revision,review,census = contents(emergency_copy)
    review['units'][0]['body_read_completely'] = False
    with pytest.raises(ValueError,match='body lacks current independent evidence'):
        validate_review_contents(emergency_copy,revision,review,census)
    revision,review,census = contents(emergency_copy)
    review['claims'][0]['verdict'] = 'HOLD'
    with pytest.raises(ValueError,match='claim lacks current independent evidence'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_unchanged_patch_summary_cannot_cover_unreviewed_card(emergency_copy):
    revision,review,census = contents(emergency_copy)
    revision['study_lessons']['LAW-054'] = {'core':'Unreviewed changed legal rule'}
    with pytest.raises(ValueError,match='requested derived scope changed'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_source_addition_and_visual_table_inspection_are_exact_requirements(emergency_copy):
    revision,review,census = contents(emergency_copy)
    revision['sources']['src-unreviewed'] = {'id':'src-unreviewed','url':'https://www.mass.gov/doc/unreviewed'}
    with pytest.raises(ValueError,match='revised source scope changed'):
        validate_review_contents(emergency_copy,revision,review,census)
    revision,review,census = contents(emergency_copy)
    review['visual_table_review']['hospice']['actually_viewed_by_auditor'] = False
    with pytest.raises(ValueError,match='visual table evidence missing'):
        validate_review_contents(emergency_copy,revision,review,census)


@pytest.mark.parametrize('relative',[
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/kits-page3.png',
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/hospice.pdf',
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/unchanged-derived-cards-and-summaries.json',
    'notes/study/guide.json',
])
def test_live_primary_visual_and_unchanged_card_bytes_are_bound(emergency_copy,relative):
    path = emergency_copy/relative
    path.write_bytes(path.read_bytes()+b' tampered')
    raw = (emergency_copy/REVISION_M).read_bytes()
    with pytest.raises(ValueError,match='evidence changed'):
        validate_emergency_note_review(emergency_copy,raw,json.loads(raw))


def test_semantic_migration_decodes_j_export_and_j_build_context(emergency_copy):
    path = emergency_copy/'site/notes/complete-notes.md'
    original = (ROOT/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert migrated_baseline_bytes(emergency_copy,'site/notes/complete-notes.md',path.read_bytes()) == original
    (emergency_copy/MIGRATION).unlink()
    # The unchanged 11th migration still rejects M semantics on its own.
    with pytest.raises(ValueError,match='cannot authorize a semantic note edit'):
        migrated_baseline_bytes(emergency_copy,'site/notes/complete-notes.md',path.read_bytes())


@pytest.mark.parametrize('change,expected',[
    ('current_semantic','current semantic build changed'),
    ('scope','expands protected scope'),
    ('historical_build','Historical J census build changed'),
    ('historical_export','Historical J census export changed'),
    ('previous_guard','Previous census annotation migration changed'),
])
def test_semantic_migration_cannot_weaken_old_guards_or_rebind_context(emergency_copy,change,expected):
    root = emergency_copy
    metadata = json.loads((root/MIGRATION).read_bytes())
    if change == 'current_semantic':
        path = root/'site/notes/build.json'; build = json.loads(path.read_bytes())
        build['content_sha256'] = metadata['semantic_notes_sha256'] = '0'*64
        path.write_bytes(encoded(build))
    elif change == 'scope':
        metadata['path'] = 'notes/guide.json'
    elif change == 'historical_build':
        path = root/metadata['baseline_build_copy']; build = json.loads(path.read_bytes())
        build['content_sha256'] = metadata['semantic_notes_sha256']
        path.write_bytes(encoded(build)); metadata['baseline_build_sha256'] = sha(path.read_bytes())
    elif change == 'historical_export':
        path = root/metadata['baseline_copy']; path.write_bytes(path.read_bytes()+b' changed')
        metadata['old_sha256'] = sha(path.read_bytes())
    else:
        path = root/metadata['previous_migration_path']; parent = json.loads(path.read_bytes())
        parent['semantic_notes_sha256'] = metadata['semantic_notes_sha256']
        path.write_bytes(encoded(parent)); metadata['previous_migration_sha256'] = sha(path.read_bytes())
    (root/MIGRATION).write_bytes(encoded(metadata))
    with pytest.raises(ValueError,match=expected):
        migrated_baseline_bytes(root,'site/notes/complete-notes.md',(root/'site/notes/complete-notes.md').read_bytes())

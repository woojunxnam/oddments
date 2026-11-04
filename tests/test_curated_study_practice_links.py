"""LAW-035 navigation regression checks; no new legal or question audit credit."""
import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

import build_exam_study as builder
from curated_study_practice_links import CONFIG_PATH, load_curated_practice_candidates
from notes_revision import apply_study_revision, load_notes

ROOT = Path(__file__).resolve().parents[1]
DIRECT = {f'MA-EXP-{n:04d}' for n in range(713, 717)}
WRONG = {'MA-CASE-1063', 'MA-CASE-0696', 'MA-CASE-1066'}


@pytest.fixture(scope='module')
def actual_inputs():
    notes = load_notes(ROOT)
    units = {u['id']: u for c in notes['chapters'] for u in c['units']}
    lessons = apply_study_revision(json.loads((ROOT/'notes/study/guide.json').read_text()),
                                   'study', ROOT)['lessons']
    config = json.loads((ROOT/'site/practice-expansion/publication.json').read_text())
    paths = ['practice_expansion/2026-10-23/candidates/questions.json'] + [
        b['path'] for b in config['additional_banks']]
    questions = [q for p in paths for q in json.loads((ROOT/p).read_text())['questions']]
    selection = json.loads((ROOT/config['representative_selection']['path']).read_text())
    held = {qid for h in selection['holds'] for qid in
            [h['legacy_question_id'], *h.get('affected_archive_ids', [])]}
    held.update(qid for n in selection.get('archive_review_notices', []) for qid in n['question_ids'])
    return lessons, units, questions, set(selection['recommended_ids']), set(selection['new_ids']), held


def scope(inputs, root=ROOT):
    return load_curated_practice_candidates(root, *inputs[:3])


def links(inputs, curated, excluded=None, item=None):
    lessons, _, questions, recommended, revised, held = inputs
    item = item or next(l for l in lessons if l['id'] == 'LAW-035')
    return builder.study_practice_links(item, questions, recommended, revised,
                                       held if excluded is None else excluded, curated)


@pytest.fixture
def proof_root(tmp_path):
    """Copy only pinned evidence; mutate fixtures, never source notes or banks."""
    config = json.loads((ROOT/CONFIG_PATH).read_text())
    paths = {CONFIG_PATH} | {config['source_review'][k]['path'] for k in
                             ['report', 'derived_findings', 'question_alignment']}
    report = json.loads((ROOT/config['source_review']['report']['path']).read_text())
    paths.update(s['evidence_path'] for s in report['sources']
                 if s['source_id'] in {'mgl94c-19d', 'mgl94c-18b'})
    for path in paths:
        (tmp_path/path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/path, tmp_path/path)
    return tmp_path


def edit_config(root, edit):
    path = root/CONFIG_PATH
    data = json.loads(path.read_text())
    edit(data)
    path.write_text(json.dumps(data, ensure_ascii=False))


def test_actual_seven_day_lesson_links_only_a_directly_read_family(actual_inputs):
    curated = scope(actual_inputs)
    assert curated == {'LAW-035': frozenset(DIRECT)}
    # Actual unrelated PMP questions still share the unit and pass ordinary
    # eligibility, so an empty/fallback bug would expose them again.
    item = next(l for l in actual_inputs[0] if l['id'] == 'LAW-035')
    wrong = [q for q in actual_inputs[2] if q['question_id'] in WRONG]
    assert len(wrong) == 3
    assert all(set(item['note_units']) & {e['unit_id'] for e in q['note_evidence']} for q in wrong)
    result = links(actual_inputs, curated)
    assert len(result) <= 1
    assert {r['id'] for r in result} <= DIRECT
    assert not {r['id'] for r in result} & WRONG
    assert all(r['family'] == 'PMP07' for r in result)


def test_all_direct_candidates_held_never_falls_back_to_available_pmp(actual_inputs):
    curated = scope(actual_inputs)
    assert links(actual_inputs, curated, actual_inputs[5] | DIRECT) == []
    # This also protects an explicit empty allowlist from becoming unrestricted.
    assert links(actual_inputs, {'LAW-035': frozenset()}) == []


def test_excluded_candidate_can_only_be_replaced_with_another_direct_candidate(actual_inputs):
    curated = scope(actual_inputs)
    first = links(actual_inputs, curated)
    if first:
        result = links(actual_inputs, curated, actual_inputs[5] | {first[0]['id']})
        assert len(result) <= 1
        assert {r['id'] for r in result} <= DIRECT - {first[0]['id']}


@pytest.mark.parametrize('curated', [{}, {'LAW-035': None}])
def test_missing_law035_scope_is_an_error_not_a_pmp_fallback(actual_inputs, curated):
    with pytest.raises(ValueError, match='Missing direct practice scope'):
        links(actual_inputs, curated)


@pytest.mark.parametrize('flags', [['source-gap'], ['open'], ['open', 'source-gap']])
def test_curated_support_does_not_bypass_existing_source_gap_or_open_policy(actual_inputs, flags):
    curated = scope(actual_inputs)
    inputs = copy.deepcopy(actual_inputs)
    for q in inputs[2]:
        if q['question_id'] in DIRECT:
            q['inherited_flags'] = flags
            q['primary_source_read_records'] = []
    assert links(inputs, curated) == []


def test_existing_narrow_open_exception_still_requires_selection_review_and_keeps_flag(actual_inputs):
    curated = scope(actual_inputs)
    inputs = copy.deepcopy(actual_inputs)
    qid = 'MA-EXP-0715'
    q = next(q for q in inputs[2] if q['question_id'] == qid)
    q.update(inherited_flags=['open'],
             primary_source_verification='AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_AUDIT',
             primary_source_read_records=[{'access_status': 'READ_OFFICIAL'}])
    restricted = {'LAW-035': frozenset({qid})}
    lessons, units, questions, _, _, held = inputs
    selected = (lessons, units, questions, {qid}, {qid}, held - {qid})
    assert [x['id'] for x in links(selected, restricted)] == [qid]
    assert q['inherited_flags'] == ['open']
    assert links((lessons, units, questions, {qid}, set(), held), restricted) == []
    assert links(selected, restricted, held | {qid}) == []


def test_every_other_lesson_link_is_unchanged_by_the_law035_restriction(actual_inputs):
    curated = scope(actual_inputs)
    for item in actual_inputs[0]:
        if item['id'] != 'LAW-035':
            assert links(actual_inputs, curated, item=item) == links(actual_inputs, {}, item=item)


@pytest.mark.parametrize('source', ['report', 'derived_findings', 'question_alignment'])
def test_changed_b_report_or_entry_or_option_evidence_fails_closed(actual_inputs, proof_root, source):
    config = json.loads((proof_root/CONFIG_PATH).read_text())
    path = proof_root/config['source_review'][source]['path']
    path.write_bytes(path.read_bytes() + b' ')
    with pytest.raises(ValueError, match='stale source'):
        scope(actual_inputs, proof_root)


@pytest.mark.parametrize('source_id', ['mgl94c-19d', 'mgl94c-18b'])
def test_changed_official_raw_payload_fails_closed(actual_inputs, proof_root, source_id):
    config = json.loads((proof_root/CONFIG_PATH).read_text())
    report = json.loads((proof_root/config['source_review']['report']['path']).read_text())
    path = proof_root/next(s['evidence_path'] for s in report['sources'] if s['source_id'] == source_id)
    path.write_bytes(path.read_bytes() + b' ')
    with pytest.raises(ValueError, match='stale source'):
        scope(actual_inputs, proof_root)


def test_stored_body_hash_cannot_mask_changed_effective_note_text(actual_inputs, proof_root):
    inputs = copy.deepcopy(actual_inputs)
    unit = inputs[1]['w2-c-12']
    unit['body'] += '\nChanged seven-day rule.'
    unit['body_sha256'] = hashlib.sha256(unit['body'].encode()).hexdigest()
    with pytest.raises(ValueError, match='changed effective note body'):
        scope(inputs, proof_root)


def test_changed_actual_law035_entry_requires_new_support(actual_inputs, proof_root):
    inputs = copy.deepcopy(actual_inputs)
    next(l for l in inputs[0] if l['id'] == 'LAW-035')['core'] += ' changed'
    with pytest.raises(ValueError, match='changed LAW-035 entry text'):
        scope(inputs, proof_root)


@pytest.mark.parametrize('change', ['stem', 'option', 'key', 'rationale'])
def test_changed_whole_question_record_rejects_old_scope_proof(actual_inputs, proof_root, change):
    inputs = copy.deepcopy(actual_inputs)
    q = next(q for q in inputs[2] if q['question_id'] == 'MA-EXP-0715')
    if change == 'stem': q['stem'] += ' changed'
    if change == 'option': q['choices'][0]['text'] += ' changed'
    if change == 'key': q['correct_choice_ids'] = ['D']
    if change == 'rationale': q['explanation']['core_reasoning'] += ' changed'
    with pytest.raises(ValueError, match='changed question record'):
        scope(inputs, proof_root)


def test_same_unit_wrong_question_cannot_be_added_to_the_curated_source(actual_inputs, proof_root):
    edit_config(proof_root, lambda c: c['lessons']['LAW-035']['candidates'][0].update(
        question_id='MA-CASE-1066'))
    with pytest.raises(ValueError, match='candidate lacks direct review'):
        scope(actual_inputs, proof_root)


@pytest.mark.parametrize('change', ['entry', 'body', 'question', 'proof'])
def test_curated_hash_tampering_fails_closed(actual_inputs, proof_root, change):
    def edit(c):
        entry = c['lessons']['LAW-035']
        if change == 'entry': entry['entry_text_sha256'] = '0'*64
        if change == 'body': entry['note_body_sha256']['w2-c-12'] = '0'*64
        if change == 'question': entry['candidates'][0]['record_sha256'] = '0'*64
        if change == 'proof': entry['candidates'][0]['direct_scope_review_sha256'] = '0'*64
    edit_config(proof_root, edit)
    with pytest.raises(ValueError):
        scope(actual_inputs, proof_root)


def test_config_cannot_expand_to_another_lesson(actual_inputs, proof_root):
    edit_config(proof_root, lambda c: c['lessons'].update({'LAW-036': c['lessons']['LAW-035']}))
    with pytest.raises(ValueError, match='only LAW-035'):
        scope(actual_inputs, proof_root)


def test_law035_family_cap_cannot_be_raised(actual_inputs, proof_root):
    edit_config(proof_root, lambda c: c['lessons']['LAW-035'].update(max_families=2))
    with pytest.raises(ValueError, match='family cap must remain one'):
        scope(actual_inputs, proof_root)


def test_config_cannot_replace_the_reviewed_source_hash(actual_inputs, proof_root):
    edit_config(proof_root, lambda c: c['source_review']['report'].update(sha256='0'*64))
    with pytest.raises(ValueError, match='stale source'):
        scope(actual_inputs, proof_root)


def test_link_building_never_rewrites_original_questions_notes_or_lesson(actual_inputs):
    before = copy.deepcopy(actual_inputs)
    before_config = (ROOT/CONFIG_PATH).read_bytes()
    curated = scope(actual_inputs)
    links(actual_inputs, curated)
    links(actual_inputs, curated, actual_inputs[5] | DIRECT)
    assert actual_inputs == before
    assert (ROOT/CONFIG_PATH).read_bytes() == before_config

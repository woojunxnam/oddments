"""Hash-bound navigation evidence for LAW-035, not a question admission/audit gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CONFIG_PATH = 'config/curated-study-practice-links.v1.json'
LESSON_ID = 'LAW-035'
ENTRY_FIELDS = ('id', 'title', 'core', 'why', 'trap', 'recall', 'note_units')
DIRECT_SCOPE = 'MATCH_WITHIN_19D_18B_CLAIMS_ONLY'


def content_digest(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(',', ':')
    ).encode()).hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError('Curated practice link: ' + message)


def _checked_bytes(root, path, expected):
    target = (root / path).resolve()
    _require(target.is_relative_to(root.resolve()), 'source path outside repository')
    _require(target.is_file(), 'missing source ' + path)
    raw = target.read_bytes()
    _require(hashlib.sha256(raw).hexdigest() == expected, 'stale source ' + path)
    return raw


def _checked_json(root, reference):
    return json.loads(_checked_bytes(root, reference['path'], reference['sha256']))


def load_curated_practice_candidates(root, lessons, units, questions):
    """Return only directly supported IDs; stale proof fails closed, never falls back.

    This restriction precedes no eligibility decision. The caller must still apply
    its unchanged HOLD/notice/source-gap/OPEN rules to every permitted question.
    """
    root = Path(root)
    config = json.loads((root / CONFIG_PATH).read_text())
    _require(config['schema_version'] == 1, 'unknown configuration version')
    _require(config['scope'] == 'LAW-035_DIRECT_PRACTICE_LINK_NAVIGATION_ONLY', 'unknown scope')
    _require(config['question_audit_credit'] == config['canonical_release_credit'] == 0,
             'navigation evidence cannot award audit/release credit')
    _require(set(config['lessons']) == {LESSON_ID}, 'only LAW-035 may be curated here')
    spec = config['lessons'][LESSON_ID]
    _require(spec['max_families'] == 1, 'LAW-035 family cap must remain one')
    source = config['source_review']
    report = _checked_json(root, source['report'])
    findings = _checked_json(root, source['derived_findings'])
    alignment = _checked_json(root, source['question_alignment'])
    _require(report['derived_surface_evidence_path'] == source['derived_findings']['path']
             and report['derived_surface_evidence_sha256'] == source['derived_findings']['sha256'],
             'report/derived source binding differs')
    _require(report['question_alignment']['evidence_path'] == source['question_alignment']['path']
             and report['question_alignment']['evidence_sha256'] == source['question_alignment']['sha256'],
             'report/question alignment binding differs')
    matching = [f for f in findings['findings'] if f['finding_id'] == source['finding_id']]
    _require(len(matching) == 1, 'missing or duplicate source finding')
    finding = matching[0]
    _require(content_digest(finding) == source['finding_sha256'], 'changed source finding')
    _require(finding['kind'] == 'PRACTICE_LINK_SUPPORT_GAP'
             and finding['entry_text']['id'] == LESSON_ID, 'wrong finding scope')
    current = [l for l in lessons if l['id'] == LESSON_ID]
    _require(len(current) == 1, 'missing or duplicate LAW-035 lesson')
    entry = {k: current[0][k] for k in ENTRY_FIELDS}
    reviewed_entry = {k: finding['entry_text'][k] for k in ENTRY_FIELDS}
    _require(content_digest(entry) == spec['entry_text_sha256']
             == content_digest(reviewed_entry), 'changed LAW-035 entry text')
    _require(set(entry['note_units']) == set(spec['note_body_sha256'])
             == {finding['unit_id']}, 'changed lesson note scope')
    for uid, expected in spec['note_body_sha256'].items():
        records = [r for r in report['records'] if r['unit_id'] == uid]
        _require(len(records) == 1, 'missing or duplicate reviewed note')
        _require(uid in units and hashlib.sha256(units[uid]['body'].encode()).hexdigest()
                 == expected == records[0]['binding']['body_sha256'], 'changed effective note body')

    # Retain the actual official payloads behind B's option-by-option scope review.
    authorities = {s['source_id']: s for s in report['sources']
                   if s['source_id'] in {'mgl94c-19d', 'mgl94c-18b'}}
    _require(set(authorities) == {'mgl94c-19d', 'mgl94c-18b'}, 'missing controlling source')
    for s in authorities.values():
        _checked_bytes(root, s['evidence_path'], s['evidence_sha256'])
    direct = {r['question_id']: r for r in finding['verified_direct_replacement_scope']}
    checks = {r['question_id']: r for r in alignment['direct_19d_18b_keychecks']}
    by_id = {q['question_id']: q for q in questions}
    _require(len(by_id) == len(questions), 'duplicate question ID')
    ids = [c['question_id'] for c in spec['candidates']]
    _require(ids and len(ids) == len(set(ids)), 'missing or duplicate curated candidate')
    for c in spec['candidates']:
        qid = c['question_id']
        _require(qid in direct and qid in checks and qid in by_id, 'candidate lacks direct review ' + qid)
        q, check, scope = by_id[qid], checks[qid], direct[qid]
        _require(c['family_id'] == q['family_id'] == check['family_id'] == scope['family_id'] == 'PMP07',
                 'candidate family differs ' + qid)
        _require(c['record_sha256'] == content_digest(q) == check['record_sha256']
                 == scope['record_sha256'], 'changed question record ' + qid)
        _require(content_digest(check) == c['direct_scope_review_sha256'], 'changed direct option proof ' + qid)
        _require(check['status'] == scope['status'] == DIRECT_SCOPE
                 and check['question_audit_credit'] == 0, 'unsupported direct scope ' + qid)
        _require(q['correct_choice_ids'] == check['stored_key'] == check['claim_limited_expected_key']
                 == scope['stored_key'] == scope['claim_limited_expected_key'], 'changed stored key binding ' + qid)
        options = {x['id']: x['text'] for x in q['choices']}
        proof = check['per_choice_findings']
        _require(len(proof) == len(options) and {x['choice_id'] for x in proof} == set(options),
                 'incomplete direct option proof ' + qid)
        for p in proof:
            _require(p['option_text'] == options[p['choice_id']] and p['authorities'], 'changed option proof ' + qid)
            for a in p['authorities']:
                s = authorities.get(a['source_id'])
                _require(s is not None and a['evidence_path'] == s['evidence_path']
                         and a['evidence_sha256'] == s['evidence_sha256']
                         and a['official_url'] == s['official_url'] and bool(a['exact_section']),
                         'option authority binding differs ' + qid)
    return {LESSON_ID: frozenset(ids)}

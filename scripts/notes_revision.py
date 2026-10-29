"""Compose the explicit personnel revision over immutable notes inputs.

Baseline digests remain available to historical questions. Effective body hashes
identify the displayed edition; original inputs are never rewritten.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'revisions/notes/2026-10-29-personnel-ratios.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load_notes(root=ROOT):
    raw = (root / 'notes/guide.json').read_bytes()
    data = json.loads(raw)
    revision_raw = (root / REVISION).read_bytes()
    revision = json.loads(revision_raw)
    if digest(raw) != revision['base_guide_sha256']:
        raise ValueError('Stale notes revision base')
    units = {u['id']: u for c in data['chapters'] for u in c['units']}
    if [u['id'] for u in revision['units']] != ['w1-b-8']:
        raise ValueError('Unexpected personnel revision unit scope')
    for change in revision['units']:
        unit = units[change['id']]
        if digest(unit['body'].encode()) != change['expected_body_sha256']:
            raise ValueError('Stale notes revision body')
        for field in ['body', 'source_review_date', 'flags', 'editor_note']:
            unit[field] = copy.deepcopy(change[field])
        unit['body_sha256'] = digest(unit['body'].encode())
        unit['content_version'] = revision['id']
    if set(revision['chapter_highlights']) != {'personnel'}:
        raise ValueError('Unexpected revision chapter scope')
    for chapter in data['chapters']:
        if chapter['id'] in revision['chapter_highlights']:
            chapter['highlights'] = revision['chapter_highlights'][chapter['id']]
    data['edition'] = revision['id']
    data['revision_provenance'] = dict(
        id=revision['id'], path=REVISION, sha256=digest(revision_raw),
        base_guide_sha256=digest(raw), review_status=revision['review_status'],
        history_policy=revision['history_policy'])
    return data


def apply_study_revision(data, kind, root=ROOT):
    revision = json.loads((root / REVISION).read_text())
    field = {'study': 'lessons', 'refresh': 'cards'}[kind]
    patches = revision[{'study': 'study_lessons', 'refresh': 'refresh_cards'}[kind]]
    if set(patches) != ({'LAW-012'} if kind == 'study' else {'RF-049'}):
        raise ValueError('Unexpected derived revision scope')
    lookup = {x['id']: x for x in data[field]}
    for identifier, patch in patches.items():
        if identifier not in lookup or not set(patch) <= set(lookup[identifier]):
            raise ValueError('Unknown revised learning field')
        lookup[identifier].update(copy.deepcopy(patch))
    data['notes_revision'] = load_notes(root)['revision_provenance']
    return data

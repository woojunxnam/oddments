"""Compose versioned personnel revisions without rewriting protected inputs."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'revisions/notes/2026-10-29-personnel-ratios.json'
REVISION_B = 'revisions/notes/2026-10-29-personnel-supervision-training.json'
REVISION_C = 'revisions/notes/2026-10-30-mor-presence.json'
REVISION_D = 'revisions/notes/2026-10-30-mor-discipline.json'
REVISION_E = 'revisions/notes/2026-10-30-discipline-cdtm.json'
REVISION_F = 'revisions/notes/2026-10-30-cdtm0512.json'
PATHS = [REVISION, REVISION_B, REVISION_C, REVISION_D, REVISION_E, REVISION_F]
IDS = ['2026-10-29.personnel-ratios.1', '2026-10-29.personnel-supervision-training.1', '2026-10-30.mor-presence.1', '2026-10-30.mor-discipline.1', '2026-10-30.discipline-cdtm.1', '2026-10-30.cdtm05-12.1']


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def revisions(root=ROOT):
    result=[]
    for i, path in enumerate(PATHS):
        raw=(root/path).read_bytes()
        value=json.loads(raw)
        if value['id'] != IDS[i]:
            raise ValueError('Unexpected revision ID')
        if i and (value['previous_revision']['path'] != PATHS[i-1] or
                  value['previous_revision']['sha256'] != digest((root/PATHS[i-1]).read_bytes())):
            raise ValueError('Stale parent revision hash')
        result.append((path,raw,value))
    return result


def load_notes(root=ROOT, revision_id=None):
    raw=(root/'notes/guide.json').read_bytes()
    data=json.loads(raw)
    for i,(path,revision_raw,revision) in enumerate(revisions(root)):
        if digest(raw) != revision['base_guide_sha256']:
            raise ValueError('Stale notes revision base')
        new_sources = revision.get('sources', {})
        expected_sources = [set(), set(), set(), set(), {
            'src-cdtm-c112s24bhalf-20261030', 'src-cdtm-naloxone-order-20261030',
        }, set()][i]
        if set(new_sources) != expected_sources or set(new_sources).intersection(data['sources']):
            raise ValueError('Unexpected revision source scope or overwritten source')
        for sid, source in new_sources.items():
            if source['id'] != sid or not source['url'].startswith(('https://www.mass.gov/', 'https://malegislature.gov/')):
                raise ValueError('Unknown revised official source')
            data['sources'][sid] = copy.deepcopy(source)
        units={u['id']:u for c in data['chapters'] for u in c['units']}
        expected=[['w1-b-8'],['w1-b-9','w1-b-10'],['w1-c-7'],['w1-c-4','w1-c-5','w1-c-7','w1-c-13','w6-b-8'],
                  ['w1-c-14','w1-c-15','w4-d-17','w3-d-2','w3-d-3','authority-paths','w6-b-17'],
                  ['w3-d-4','w3-d-5','w3-d-6','w3-d-7','w3-d-8']][i]
        if [u['id'] for u in revision['units']] != expected:
            raise ValueError('Unexpected notes revision unit scope')
        for change in revision['units']:
            unit=units[change['id']]
            if digest(unit['body'].encode()) != change['expected_body_sha256']:
                raise ValueError('Stale notes revision body: '+path+' / '+change['id']+' expected='+change['expected_body_sha256']+' actual='+digest(unit['body'].encode()))
            for field in ['body','source_review_date','flags','editor_note']:
                unit[field]=copy.deepcopy(change[field])
            if 'source_ids' in change:
                if any(sid not in data['sources'] for sid in change['source_ids']):
                    raise ValueError('Unknown revised source')
                unit['source_ids']=copy.deepcopy(change['source_ids'])
            unit['body_sha256']=digest(unit['body'].encode())
            unit['content_version']=revision['id']
        expected_chapters=[{'personnel'},{'personnel'},set(),{'pharmacy-mor','discipline-inspection'}, {'discipline-inspection','cdtm'}, {'cdtm'}][i]
        if set(revision['chapter_highlights']) != expected_chapters:
            raise ValueError('Unexpected revision chapter scope')
        for chapter in data['chapters']:
            if chapter['id'] in revision['chapter_highlights']:
                chapter['highlights']=copy.deepcopy(revision['chapter_highlights'][chapter['id']])
        data['edition']=revision['id']
        data['revision_provenance']=dict(
            id=revision['id'],path=path,sha256=digest(revision_raw),
            base_guide_sha256=digest(raw),review_status=revision['review_status'],
            history_policy=revision['history_policy'])
        if revision_id == revision['id']:
            return data
    if revision_id is not None:
        raise ValueError('Unknown requested notes revision')
    return data


def apply_study_revision(data, kind, root=ROOT):
    field={'study':'lessons','refresh':'cards'}[kind]
    lookup={x['id']:x for x in data[field]}
    for _,_,revision in revisions(root):
        patches=revision[{'study':'study_lessons','refresh':'refresh_cards'}[kind]]
        expected_scopes={'study':[{'LAW-012'},{'LAW-012'},set(),{'LAW-015'}, {'LAW-016','LAW-045','LAW-048'}, set()],
                         'refresh':[{'RF-049'},{'RF-049'},set(),set(), {'RF-011'}, set()]}
        if set(patches) != expected_scopes[kind][IDS.index(revision['id'])]:
            raise ValueError('Unexpected derived revision scope')
        for identifier,patch in patches.items():
            if identifier not in lookup or not set(patch)<=set(lookup[identifier]):
                raise ValueError('Unknown revised learning field')
            lookup[identifier].update(copy.deepcopy(patch))
    data['notes_revision']=load_notes(root)['revision_provenance']
    return data

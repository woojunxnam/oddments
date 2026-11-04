"""Compose versioned personnel revisions without rewriting protected inputs."""
import copy
import hashlib
import json
from pathlib import Path
from notes_emergency_activation import REVISION_M, SOURCE_IDS, official_url, validate_emergency_note_review

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'revisions/notes/2026-10-29-personnel-ratios.json'
REVISION_B = 'revisions/notes/2026-10-29-personnel-supervision-training.json'
REVISION_C = 'revisions/notes/2026-10-30-mor-presence.json'
REVISION_D = 'revisions/notes/2026-10-30-mor-discipline.json'
REVISION_E = 'revisions/notes/2026-10-30-discipline-cdtm.json'
REVISION_F = 'revisions/notes/2026-10-30-cdtm0512.json'
REVISION_G = 'revisions/notes/2026-10-30-cdtm13-vax04.json'
REVISION_H = 'revisions/notes/2026-11-03-counsel-shield-final.json'
REVISION_I = 'revisions/notes/2026-11-03-ce-disclosure-final.json'
REVISION_J = 'revisions/notes/2026-11-03-refill-cancer-final.json'
PATHS = [REVISION, REVISION_B, REVISION_C, REVISION_D, REVISION_E, REVISION_F, REVISION_G, REVISION_H, REVISION_I, REVISION_J, REVISION_M]
IDS = ['2026-10-29.personnel-ratios.1', '2026-10-29.personnel-supervision-training.1', '2026-10-30.mor-presence.1', '2026-10-30.mor-discipline.1', '2026-10-30.discipline-cdtm.1', '2026-10-30.cdtm05-12.1', '2026-10-30.cdtm13-vax04.1', '2026-11-03.counsel-shield-final.1', '2026-11-03.ce-disclosure.1', '2026-11-03.refill-cancer.1', '2026-11-03.emergency-kit.1']


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def record_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode())


def validate_final_note_review(root, revision_raw, revision, revision_path=REVISION_H):
    """Activate only exact independently reviewed final note/card revisions.

    Historical HOLD evidence remains immutable. A summary KEEP cannot replace
    matching current-body, atomic-claim and derived-card evidence.
    """
    if revision_path == REVISION_M:
        return validate_emergency_note_review(root, revision_raw, revision)
    scopes = {
        REVISION_H: ('counsel-shield', 'counsel-shield-final-independent-review-r2.json',
                     'counsel-shield-final-census.json', {'w3-b-1', 'w3-d-23'},
                     {('study_lessons','LAW-041'), ('refresh_cards','RF-034')}),
        REVISION_I: ('ce-disclosure', 'ce-disclosure-final-independent-review.json',
                     'ce-disclosure-final-census.json', {'w1-a-7'}, {('study_lessons','LAW-008')}),
        REVISION_J: ('refill-cancer', 'refill-cancer-final-independent-review.json',
                     'refill-cancer-final-census.json', {'w2-c-1','w2-c-12'}, set()),
    }
    active_revision_path = revision_path
    name, review_name, census_name, expected_units, expected = scopes[revision_path]
    activation = json.loads((root/('revisions/notes/'+name+'-activation.json')).read_bytes())
    review_path = 'reports/full-corpus-review/' + review_name
    census_path = 'reports/full-corpus-review/' + census_name
    if (activation['revision_path'] != active_revision_path or activation['review_path'] != review_path or
            activation['census_path'] != census_path or activation['revision_sha256'] != digest(revision_raw)):
        raise ValueError('Final note activation binding changed')
    review_raw = (root/review_path).read_bytes()
    census_raw = (root/census_path).read_bytes()
    if (digest(review_raw) != activation['review_sha256'] or
            digest(census_raw) != activation['census_sha256']):
        raise ValueError('Final note review or census changed')
    review, census = json.loads(review_raw), json.loads(census_raw)
    if (review['decision'] != 'KEEP' or not review['independent_of_authors'] or
            review['candidate_edited_by_auditor'] or not review['auditor_instance'] or
            review['candidate_sha256'] != digest(revision_raw) or
            review['census_sha256'] != digest(census_raw)):
        raise ValueError('Final note independent KEEP missing or stale')
    if active_revision_path == REVISION_H:
        prior_path = 'reports/full-corpus-review/counsel-shield-final-independent-review.json'
        prior = review['prior_review']
        prior_raw = (root/prior_path).read_bytes()
        prior_review = json.loads(prior_raw)
        if (prior['path'] != prior_path or prior['sha256'] != digest(prior_raw) or
                prior_review['decision'] != 'HOLD' or
                prior_review['candidate_sha256'] == review['candidate_sha256'] or
                prior_review['auditor_instance'] != review['auditor_instance']):
            raise ValueError('Prior note HOLD history changed or was overridden unchanged')
    bodies = {u['id']: digest(u['body'].encode()) for u in revision['units']}
    reviewed = {u['unit_id']: u for u in review['units']}
    if (len(bodies) != len(revision['units']) or len(reviewed) != len(review['units']) or
            set(bodies) != expected_units or set(reviewed) != set(bodies)):
        raise ValueError('Final note review unit scope changed')
    for uid, body_hash in bodies.items():
        unit = reviewed[uid]
        if (unit['verdict'] != 'KEEP' or unit['body_sha256'] != body_hash or
                not unit['body_read_completely'] or not unit['fully_supported_in_current_scope']):
            raise ValueError('Final note body lacks current independent evidence: '+uid)
    claims = {c['claim_id']: c for c in census['claims']}
    results = {c['claim_id']: c for c in review['claims']}
    if (len(results) != len(review['claims']) or len(claims) != len(census['claims']) or
            set(results) != set(claims)):
        raise ValueError('Final note atomic claim coverage changed')
    for cid, claim in claims.items():
        result = results[cid]
        if (result['verdict'] != 'KEEP' or result['claim_record_sha256'] != record_digest(claim) or
                claim['unit_content_sha256'] != bodies[claim['unit_id']] or
                claim['review_status'] != 'AUTHOR_SOURCE_CHECKED' or not result['authorities']):
            raise ValueError('Final note claim lacks current independent evidence: '+cid)
        for authority in result['authorities']:
            if (not authority['official_url'].startswith('https://') or
                    not authority['exact_section'] or not authority['law_checked_date']):
                raise ValueError('Final note authority incomplete')
    patches = {(p['collection'], p['id']): p for p in review['derived_patches']}
    requested = {(collection, identifier) for collection in ('study_lessons','refresh_cards')
                 for identifier in revision[collection]}
    if requested != expected:
        raise ValueError('Final note requested card scope changed')
    if set(patches) != expected or len(patches) != len(review['derived_patches']):
        raise ValueError('Final note card review scope changed')
    for collection, identifier in expected:
        evidence = patches[(collection, identifier)]
        if (evidence['verdict'] != 'KEEP' or not evidence['full_base_card_read'] or
                evidence['patch_sha256'] != record_digest(revision[collection][identifier])):
            raise ValueError('Final note card evidence stale')
    for source in review['sources']:
        path = Path(source['evidence_path'])
        if path.is_absolute() or '..' in path.parts or digest((root/path).read_bytes()) != source['evidence_sha256']:
            raise ValueError('Final note primary evidence changed')
    return dict(path=review_path, sha256=digest(review_raw), auditor_instance=review['auditor_instance'],
                decision='KEEP', scope='SPECIFIED_CURRENT_NOTE_BODIES_AND_CARD_PATCHES_ONLY')


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
        if path in {REVISION_H, REVISION_I, REVISION_J, REVISION_M}:
            validate_final_note_review(root, raw, value, path)
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
        }, set(), set(), {'src-shield-act-20251103'}, set(), set(), SOURCE_IDS][i]
        if set(new_sources) != expected_sources or set(new_sources).intersection(data['sources']):
            raise ValueError('Unexpected revision source scope or overwritten source')
        for sid, source in new_sources.items():
            if source['id'] != sid or not official_url(source['url']):
                raise ValueError('Unknown revised official source')
            data['sources'][sid] = copy.deepcopy(source)
        units={u['id']:u for c in data['chapters'] for u in c['units']}
        expected=[['w1-b-8'],['w1-b-9','w1-b-10'],['w1-c-7'],['w1-c-4','w1-c-5','w1-c-7','w1-c-13','w6-b-8'],
                  ['w1-c-14','w1-c-15','w4-d-17','w3-d-2','w3-d-3','authority-paths','w6-b-17'],
                  ['w3-d-4','w3-d-5','w3-d-6','w3-d-7','w3-d-8'],
                  ['w3-d-9','w3-d-10','w3-c-1','w3-c-2','w3-c-3','w3-c-4'],
                  ['w3-b-1','w3-d-23'], ['w1-a-7'], ['w2-c-1','w2-c-12'], ['w4-a-19','w4-a-20']][i]
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
            if path in {REVISION_H, REVISION_I, REVISION_J, REVISION_M}:
                unit['independent_content_review'] = validate_final_note_review(root, revision_raw, revision, path)
        expected_chapters=[{'personnel'},{'personnel'},set(),{'pharmacy-mor','discipline-inspection'}, {'discipline-inspection','cdtm'}, {'cdtm'}, {'cdtm','vaccination-administration'}, set(), set(), set(), set()][i]
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
    from notes_held_sixteenth import apply_if_bound
    return apply_if_bound(root,data)


def apply_study_revision(data, kind, root=ROOT):
    field={'study':'lessons','refresh':'cards'}[kind]
    lookup={x['id']:x for x in data[field]}
    for _,_,revision in revisions(root):
        patches=revision[{'study':'study_lessons','refresh':'refresh_cards'}[kind]]
        expected_scopes={'study':[{'LAW-012'},{'LAW-012'},set(),{'LAW-015'}, {'LAW-016','LAW-045','LAW-048'}, set(), set(), {'LAW-041'}, {'LAW-008'}, set(), set()],
                         'refresh':[{'RF-049'},{'RF-049'},set(),set(), {'RF-011'}, set(), set(), {'RF-034'}, set(), set(), set()]}
        if set(patches) != expected_scopes[kind][IDS.index(revision['id'])]:
            raise ValueError('Unexpected derived revision scope')
        for identifier,patch in patches.items():
            if identifier not in lookup or not set(patch)<=set(lookup[identifier]):
                raise ValueError('Unknown revised learning field')
            lookup[identifier].update(copy.deepcopy(patch))
    data['notes_revision']=load_notes(root)['revision_provenance']
    return data

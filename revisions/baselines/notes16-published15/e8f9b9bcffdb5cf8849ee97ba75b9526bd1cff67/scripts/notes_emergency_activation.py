"""Exact, source-backed activation of the two emergency stock boundary repairs.

The author candidate and independent review stay immutable. This is a narrow
content gate; it does not resolve the four historical OPEN/HOLD records.
"""
import hashlib
import json
from pathlib import PurePosixPath
from urllib.parse import urlsplit

REVISION_M = 'revisions/notes/2026-11-03-emergency-kit-final.json'
ACTIVATION = 'revisions/notes/emergency-kit-activation.json'
REVIEW = 'reports/full-corpus-review/emergency-kit-final-independent-review.json'
CENSUS = 'reports/full-corpus-review/emergency-kit-final-census.json'
REVISION_SHA256 = 'b891ef1f7b61e70e7967f5628a64109400e28b76d1b7816320d0611325a5e374'
REVIEW_SHA256 = '714cac739db1ac83e8fecd364854178dccd691a8170828b48ab92cafe8e0ab94'
CENSUS_SHA256 = 'c3093bbc0c7c6e29f89cce15d4ce97be02ef71a469295d21cbd43969ea742cb1'
UNIT_IDS = {'w4-a-19', 'w4-a-20'}
SOURCE_IDS = {
    'src-ltcf-kit-visual-20261103', 'src-ltcf-kit-cmr150-20261103',
    'src-ltcf-kit-cmr9-20261103', 'src-ltcf-kit-index-20261103',
    'src-hospice-acute-visual-20261103', 'src-hospice-acute-add-20261103',
    'src-hospice-acute-index-20261103',
}
OFFICIAL_HOSTS = {'www.mass.gov', 'malegislature.gov'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def record_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode())


def read_bound(root, path, sha256):
    pure = PurePosixPath(path)
    require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == path,
            'Emergency note evidence path escapes repository')
    target = root/path
    require(root.resolve() in target.resolve().parents and not target.is_symlink(),
            'Emergency note evidence path escapes repository')
    raw = target.read_bytes()
    require(digest(raw) == sha256, 'Emergency note evidence changed: '+path)
    return raw


def official_url(url):
    parsed = urlsplit(url)
    return (parsed.scheme == 'https' and parsed.hostname in OFFICIAL_HOSTS and
            parsed.username is None and parsed.password is None and parsed.port is None)


def check_evidence(root, value):
    """Verify each explicit path/hash pair, including raw PDFs and page renders."""
    if isinstance(value, dict):
        if 'path' in value and ('raw_sha256' in value or 'sha256' in value):
            read_bound(root, value['path'], value.get('raw_sha256', value.get('sha256')))
        if 'evidence_path' in value:
            read_bound(root, value['evidence_path'], value['evidence_sha256'])
        for child in value.values():
            check_evidence(root, child)
    elif isinstance(value, list):
        for child in value:
            check_evidence(root, child)


def validate_unchanged_derived(root, review):
    binding = review['unchanged_card_review']
    evidence = json.loads(read_bound(root, binding['path'], binding['raw_sha256']))
    cards = evidence['cards']
    require(len(cards) == 4 and {c['id'] for c in cards} == {'LAW-053','LAW-054','RF-054','RF-056'}
            and evidence['derived_patches'] == [], 'Emergency note unchanged card scope changed')
    guides = {}
    for card in cards:
        path = 'notes/study/guide.json' if card['id'].startswith('LAW-') else 'notes/refresh/guide.json'
        require(card['source_file']['path'] == path, 'Emergency note card source changed')
        guide = guides.setdefault(path, json.loads(read_bound(root, path, card['source_file']['raw_sha256'])))
        field, patch_field = ('lessons','study_lessons') if card['id'].startswith('LAW-') else ('cards','refresh_cards')
        actual = next(c for c in guide[field] if c['id'] == card['id'])
        require(actual == card['base_record'] == card['effective_record'] and
                record_digest(actual) == card['base_record_sha256'] == card['effective_record_sha256'] and
                card['read_completely'] is True and card['unchanged'] is True and
                card['patch_needed'] is False and card['boundary_assertions_present'] is False,
                'Emergency note unchanged card evidence stale')
        checks = card['parent_patch_checks']
        expected_paths = [p for p in __import__('notes_revision').PATHS if p != REVISION_M]
        require(len(checks) == len(expected_paths) and
                [c['revision']['path'] for c in checks] == expected_paths,
                'Emergency note card parent scope changed')
        for check in checks:
            parent = check['revision']
            revision = json.loads(read_bound(root, parent['path'], parent['raw_sha256']))
            require(check['target_patch_present'] is False and card['id'] not in revision[patch_field],
                    'Emergency note card has an unreviewed parent patch')
    summaries = evidence['summaries']
    require(len(summaries) == 3 and {s['type'] for s in summaries} ==
            {'chapter-summary-highlights','module-m14','plan-day23'},
            'Emergency note summary review scope changed')
    notes = json.loads((root/'notes/guide.json').read_bytes())
    study = guides['notes/study/guide.json']
    chapter = next(c for c in notes['chapters'] if c['id'] == 'shared-automation')
    actuals = {
        'chapter-summary-highlights': {k:chapter[k] for k in ('id','title','part','summary','highlights')},
        'module-m14': next(m for m in study['modules'] if m['id'] == 'm14'),
        'plan-day23': next(p for p in study['plan'] if p['day'] == 23),
    }
    for summary in summaries:
        require(summary['read_completely'] is True and summary['patch_needed'] is False and
                summary['record'] == actuals[summary['type']], 'Emergency note summary evidence stale')


def validate_review_contents(root, revision, review, census):
    """Validate actual audit fields without inventing J's different report schema."""
    require(review['decision'] == 'KEEP' and review['independent_of_authors'] is True and
            review['candidate_edited_by_auditor'] is False and bool(review['auditor_instance']) and
            review['body_read_completely'] is True and review['atomic_claim_census_complete'] is True and
            review['fully_supported_in_current_scope'] is True,
            'Emergency note independent KEEP missing')
    require(review['candidate'] == {'path':REVISION_M, 'raw_sha256':REVISION_SHA256} and
            review['census'] == {'path':CENSUS, 'raw_sha256':CENSUS_SHA256} and
            census['revision_path'] == REVISION_M and census['revision_sha256'] == REVISION_SHA256,
            'Emergency note candidate/census binding changed')
    units = {u['id']:u for u in revision['units']}
    reviewed = {u['unit_id']:u for u in review['units']}
    enumerated = {u['unit_id']:u for u in census['units']}
    require(len(revision['units']) == len(review['units']) == len(census['units']) == 2 and
            set(units) == set(reviewed) == set(enumerated) == UNIT_IDS,
            'Emergency note review unit scope changed')
    for uid, unit in units.items():
        audit, counted = reviewed[uid], enumerated[uid]
        body_hash = digest(unit['body'].encode())
        require(audit['body_sha256'] == counted['unit_content_sha256'] == body_hash and
                audit['body'] == unit['body'] and audit['candidate_unit_record_sha256'] == record_digest(unit) and
                audit['previous_body_sha256'] == counted['previous_effective_actual_body_sha256'] == unit['expected_body_sha256'] and
                audit['verdict'] == 'KEEP' and audit['body_read_completely'] is True and
                audit['fully_supported_in_current_scope'] is True and audit['census_complete_for_body'] is True and
                audit['atomic_claim_count'] == counted['claim_count'] == 27,
                'Emergency note body lacks current independent evidence: '+uid)
    claims = {c['claim_id']:c for c in census['claims']}
    results = {c['claim_id']:c for c in review['claims']}
    require(len(census['claims']) == len(review['claims']) == len(claims) == len(results) == 54 and
            set(claims) == set(results) and review['claim_count'] == 54 and
            all(sum(c['unit_id'] == uid for c in census['claims']) == 27 for uid in UNIT_IDS) and
            review['claim_verdict_counts'] == {'KEEP':54,'HOLD':0,'SOURCE_BLOCKED':0},
            'Emergency note atomic claim coverage changed')
    for cid, claim in claims.items():
        result = results[cid]
        require(claim['unit_id'] in UNIT_IDS and result['unit_id'] == claim['unit_id'] and
                result['claim_record_sha256'] == record_digest(claim) and
                result['unit_content_sha256'] == claim['unit_content_sha256'] == digest(units[claim['unit_id']]['body'].encode()) and
                claim['review_status'] == 'AUTHOR_SOURCE_CHECKED' and result['verdict'] == 'KEEP' and
                result['claim_read_completely'] is True and result['fully_supported_in_current_scope'] is True and
                bool(result['authorities']), 'Emergency note claim lacks current independent evidence: '+cid)
        for authority in result['authorities']:
            require(authority['source_type'] == 'PUBLIC_OFFICIAL' and official_url(authority['official_url']) and
                    bool(authority['exact_section']) and bool(authority['law_checked_date']),
                    'Emergency note authority incomplete or unofficial')
    require(revision['study_lessons'] == revision['refresh_cards'] == revision['chapter_highlights'] == {} and
            review['derived_patches'] == [], 'Emergency note requested derived scope changed')
    require(len(review['sources']) == 6 and {s['source_id'] for s in review['sources']} ==
            {'kits','hospice','add','150','cmr9','practice-index'} and
            all(s['source_type'] == 'PUBLIC_OFFICIAL' and official_url(s['official_url']) for s in review['sources']),
            'Emergency note primary source scope changed')
    require(set(revision['sources']) == SOURCE_IDS and
            all(s['id'] == sid and official_url(s['url']) for sid,s in revision['sources'].items()) and
            set(units['w4-a-19']['source_ids']) == {sid for sid in SOURCE_IDS if sid.startswith('src-ltcf-')} and
            set(units['w4-a-20']['source_ids']) == {sid for sid in SOURCE_IDS if sid.startswith('src-hospice-')},
            'Emergency note revised source scope changed')
    require(set(review['visual_table_review']) == {'kits','hospice'} and
            all(v['actually_viewed_by_auditor'] is True and v['page'] == 3
                for v in review['visual_table_review'].values()), 'Emergency note visual table evidence missing')
    require(review['historical_canonical_four_holds_resolved'] == 0 and
            review['existing_open_registry_edited'] is False and review['canonical_audit'] is False and
            review['canonical_release_credit'] == review['question_audit_credit'] == 0,
            'Emergency note activation expands audit credit or resolves historical HOLDs')
    check_evidence(root, review)
    validate_unchanged_derived(root, review)


def validate_emergency_note_review(root, revision_raw, revision):
    activation = json.loads((root/ACTIVATION).read_bytes())
    require(activation['revision_path'] == REVISION_M and activation['revision_sha256'] == REVISION_SHA256 and
            activation['review_path'] == REVIEW and activation['review_sha256'] == REVIEW_SHA256 and
            activation['census_path'] == CENSUS and activation['census_sha256'] == CENSUS_SHA256,
            'Emergency note activation binding changed')
    require(digest(revision_raw) == REVISION_SHA256 and json.loads(revision_raw) == revision,
            'Emergency note candidate changed')
    review = json.loads(read_bound(root, REVIEW, REVIEW_SHA256))
    census = json.loads(read_bound(root, CENSUS, CENSUS_SHA256))
    validate_review_contents(root, revision, review, census)
    return dict(path=REVIEW, sha256=REVIEW_SHA256, auditor_instance=review['auditor_instance'],
                decision='KEEP', scope='EXACT_TWO_CURRENT_NOTE_BODIES_54_CLAIMS_ZERO_DERIVED_PATCHES_ONLY')

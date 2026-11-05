"""Read-only canonical successor infrastructure, with no admission capability.

Existing protection/release validators remain authoritative and unchanged. Boundary
inspection is not a native schema/audit/source validation, an approval, or a replay.
All file seals must be recomputed by the caller from its trusted immutable inputs.
No approval or activation enrollment is accepted by this infrastructure version.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from datetime import date
import hashlib
import json
from pathlib import PurePosixPath
import re
import unicodedata


MODE = 'INFRASTRUCTURE_INACTIVE'
ACTIVATION_PATH = 'revisions/canonical/active-admission.json'
PUBLISHED_NOTE16_SHA256 = '4cf793e0293887a0e20dc5951cc694b596274954d872e20ced15601902f3fcf9'
FAMILY = 'data/exam_style/question_family_matrix.json'
ALLOWED_ADDITION = re.compile(r'^data/(questions|audits|rules|drugs)/[a-zA-Z0-9_-]+\.json$')
QID = re.compile(r'^MA-Q-\d{4}$')
FAMILY_FIELDS = {'family_id','area','topic','subtopic','primary_rule_ids','secondary_rule_ids',
    'drug_required','scenario_types','common_traps','target_difficulties','target_item_types',
    'max_questions_in_final_bank','current_candidate_count','current_released_count'}


class BoundaryViolation(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise BoundaryViolation(message)


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON property: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Seal:
    sha256: str
    size: int

    def __post_init__(self):
        require(bool(re.fullmatch('[a-f0-9]{64}', self.sha256)) and type(self.size) is int and self.size >= 0,
            'Invalid actual file seal')

    @classmethod
    def of(cls, raw):
        return cls(digest(raw), len(raw))


@dataclass(frozen=True)
class Proposal:
    additions: dict[str, Seal]
    family_before: Seal
    family_after: Seal
    status: str = 'NOT_APPROVED_PROPOSAL'


def safe_path(path):
    require(isinstance(path, str), 'Relative path must be text')
    parsed = PurePosixPath(path)
    require(not parsed.is_absolute() and str(parsed) == path
        and '..' not in parsed.parts and '\\' not in path and '\0' not in path and '\n' not in path,
        'Unsafe path')


def read_current_preimages(root, paths):
    """Read exact regular files; symlinks in any path component are rejected."""
    from pathlib import Path
    root = Path(root).resolve()
    result = {}
    require(len(paths)==len(set(paths)), 'Duplicate file preimage path')
    for relative in paths:
        safe_path(relative)
        path = root
        for part in PurePosixPath(relative).parts:
            path = path / part
            require(not path.is_symlink(), 'Symlink in source preimage path: '+relative)
        require(path.is_file(), 'Missing regular source preimage: '+relative)
        result[relative] = path.read_bytes()
    return result


def read_committed_preimages(root, commit, paths):
    """Read real Git blobs without checkout, object writes or baseline enrollment.

    The caller must obtain ``commit`` and ``paths`` from a separately trusted
    immutable manifest. This reader does not approve the selected commit/scope.
    """
    import subprocess
    require(isinstance(commit,str) and bool(re.fullmatch('[0-9a-f]{40}',commit)),
        'An exact immutable commit is required')
    paths = list(paths)
    require(bool(paths) and len(paths)==len(set(paths)), 'Empty or duplicate committed preimage inventory')
    for path in paths:safe_path(path)
    object_type = subprocess.check_output(['git','cat-file','-t',commit],cwd=root).strip()
    require(object_type==b'commit', 'Source anchor is not a Git commit')
    response = subprocess.run(['git','cat-file','--batch'],cwd=root,
        input=''.join(commit+':'+path+'\n' for path in paths).encode(),capture_output=True,check=True).stdout
    cursor = 0;result = {}
    for path in paths:
        end = response.find(b'\n',cursor)
        require(end>=cursor, 'Truncated Git blob header')
        fields = response[cursor:end].split();cursor=end+1
        require(len(fields)==3 and fields[1]==b'blob', 'Committed preimage is not a blob: '+path)
        size=int(fields[2]);raw=response[cursor:cursor+size];cursor+=size
        require(len(raw)==size and response[cursor:cursor+1]==b'\n', 'Truncated Git preimage')
        cursor+=1
        blob=hashlib.sha1(b'blob '+str(size).encode()+b'\0'+raw).hexdigest().encode()
        require(blob==fields[0], 'Git blob preimage hash mismatch')
        result[path]=raw
    require(cursor==len(response), 'Extra Git preimage response')
    return result


def verify_exact_file_boundary(base, candidate, proposal):
    require(proposal.status == 'NOT_APPROVED_PROPOSAL', 'Boundary inspection cannot accept an approval claim')
    require(bool(proposal.additions), 'No exact proposed additions exist')
    for path, seal in proposal.additions.items():
        safe_path(path)
        require(bool(ALLOWED_ADDITION.fullmatch(path)), 'Addition outside four bounded registry directories: ' + path)
        require(path not in base, 'Existing file cannot be reclassified as an addition: ' + path)
        require(isinstance(seal, Seal), 'Missing exact added-file seal')
    require(set(candidate) == set(base) | set(proposal.additions), 'Missing or unlisted added file')
    require(base.get(FAMILY) == proposal.family_before, 'Family preimage does not match actual base')
    for path, old in base.items():
        require(candidate[path] == (proposal.family_after if path == FAMILY else old),
            'Original protected/source-bound file changed: ' + path)
    for path, expected in proposal.additions.items():
        require(candidate[path] == expected, 'Added file differs from exact proposed bytes: ' + path)
    return {'scope': 'EXACT_FILE_BOUNDARY_ONLY', 'original_files':len(base),
        'added_files':len(proposal.additions), 'activation': MODE, 'approval_credit':0}


def verify_preservation_anchor(base, frozen_anchor):
    require(frozen_anchor is not None and set(base) == set(frozen_anchor), 'Frozen preservation inventory missing, expanded or omitted')
    require(all(base[path] == expected for path,expected in frozen_anchor.items()), 'Base seals were re-enrolled instead of preserved')


def content_identity(question):
    """Detect exact semantic-body re-identification, even with renamed IDs/families."""
    text = lambda value: ' '.join(unicodedata.normalize('NFC', value).casefold().split())
    choices = {choice['id']: text(choice['text']) for choice in question['choices']}
    value = {'stem':text(question['stem']), 'type':question['question_type'],
        'choices':sorted(choices.values()),
        'correct_text':sorted(choices[key] for key in question['correct_choice_ids'])}
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True).encode())


def verify_added_questions(base_questions, added_raw):
    known = {content_identity(question) for question in base_questions.values()}
    added = {}
    for path, raw in added_raw.items():
        if not path.startswith('data/questions/'):
            continue
        question = strict_json(raw); uid = question.get('question_id', '')
        require(bool(QID.fullmatch(uid)) and path == 'data/questions/' + uid.lower() + '.json',
            'Question ID/path mismatch')
        require(uid not in base_questions and uid not in added, 'Old or duplicate question ID')
        identity = content_identity(question)
        require(identity not in known, 'Question body reidentified or duplicated; old negative cannot be renamed')
        known.add(identity); added[uid] = question
    require(30 <= len(added) <= 40, 'Ordinary INITIAL admission needs 30–40 actual canonical questions')
    return added


def released(question):
    return question.get('verification_status') == question.get('lifecycle_status') == 'RELEASED'


def verify_family_append(before, after, old_questions, added_questions):
    require(set(before) == set(after) == {'matrix_id','profile_id','last_reviewed','families'}, 'Family top-level shape drift')
    require(before['matrix_id'] == after['matrix_id'] and before['profile_id'] == after['profile_id'], 'Family matrix/profile identity changed')
    try:
        parsed_date = date.fromisoformat(after['last_reviewed'])
    except (ValueError,TypeError):
        raise BoundaryViolation('Invalid family review date')
    require(parsed_date.isoformat()==after['last_reviewed'] and after['last_reviewed'] >= before['last_reviewed'], 'Family review date moved backwards')
    old_rows = before['families']; rows = after['families']
    require(len(rows) >= len(old_rows), 'Existing family removed')
    require([row['family_id'] for row in rows[:len(old_rows)]] == [row['family_id'] for row in old_rows], 'Existing family order/identity changed')
    ids = [row['family_id'] for row in rows]
    require(len(ids) == len(set(ids)), 'Duplicate family ID')
    all_questions = {**old_questions, **added_questions}
    candidates = Counter(q['family_id'] for q in all_questions.values())
    releases = Counter(q['family_id'] for q in all_questions.values() if released(q))
    require(set(candidates) <= set(ids), 'Question family missing from matrix')
    for old, new in zip(old_rows, rows):
        require(set(new) == set(old), 'Old family fields changed')
        require({key:value for key,value in old.items() if key not in {'current_candidate_count','current_released_count'}} ==
            {key:value for key,value in new.items() if key not in {'current_candidate_count','current_released_count'}},
            'Old family meaning/cap/rules changed')
    new_ids = {row['family_id'] for row in rows[len(old_rows):]}
    require(new_ids <= {q['family_id'] for q in added_questions.values()}, 'Unrelated orphan new family')
    for row in rows:
        require(set(row) == FAMILY_FIELDS, 'Family schema fields changed')
        require(type(row['current_candidate_count']) is int and type(row['current_released_count']) is int,
            'Family counts must be actual integer counts, not flags')
        require(row['current_candidate_count'] == candidates.get(row['family_id'],0)
            and row['current_released_count'] == releases.get(row['family_id'],0), 'Family counts are not exact registry counts')
        require(type(row['max_questions_in_final_bank']) is int and row['max_questions_in_final_bank'] >= 1
            and row['current_released_count'] <= row['max_questions_in_final_bank'], 'Family release cap exceeded')
    require({uid for uid,q in old_questions.items() if released(q)} <= {uid for uid,q in all_questions.items() if released(q)}, 'Old released membership removed')
    return {'old_family_rows':len(old_rows), 'appended_family_rows':len(rows)-len(old_rows),
        'activation': MODE, 'canonical_release_credit':0}


def verify_proposal(base_seals, candidate_seals, proposal, old_questions, old_family, new_family_raw, added_raw,
        frozen_anchor=None, original_question_raw=None, original_family_raw=None):
    verify_preservation_anchor(base_seals, frozen_anchor)
    require(original_question_raw is not None and original_family_raw is not None,
        'Original semantic objects must be tied to actual sealed preimage bytes')
    expected_paths = {path for path in base_seals if path.startswith('data/questions/') and path.endswith('.json')}
    require(set(original_question_raw)==expected_paths, 'Original question preimage inventory omitted or expanded')
    parsed_originals = {}
    for path, raw in original_question_raw.items():
        require(Seal.of(raw)==base_seals[path], 'Original semantic preimage differs from frozen seal')
        value = strict_json(raw)
        require(value['question_id'] not in parsed_originals, 'Duplicate original semantic ID')
        parsed_originals[value['question_id']] = value
    require(parsed_originals==old_questions, 'Original semantic questions do not match sealed source bytes')
    require(Seal.of(original_family_raw)==base_seals[FAMILY] and strict_json(original_family_raw)==old_family,
        'Original semantic family does not match its sealed source bytes')
    proof = verify_exact_file_boundary(base_seals, candidate_seals, proposal)
    require(Seal.of(new_family_raw) == proposal.family_after, 'Family semantic input not bound to its actual bytes')
    require(set(added_raw) == set(proposal.additions), 'Added semantic documents missing or extra')
    for path, raw in added_raw.items():
        require(Seal.of(raw) == proposal.additions[path], 'Semantic input does not match file seal')
    added = verify_added_questions(old_questions, added_raw)
    family = verify_family_append(old_family, strict_json(new_family_raw), old_questions, added)
    return {**proof, 'family':family, 'new_question_ids':sorted(added), 'native_audit_credit':0}


def legacy_seal_projection_only(*args, **kwargs):
    """A boundary-checked projection, never an executed filesystem replay."""
    proof = verify_proposal(*args, **kwargs)
    return {'legacy_base_seals':dict(args[0]), 'current_boundary_proof':proof,
        'legacy_validator_execution_credit':0, 'activation':MODE}


def note_source_context_only(parent_raw, old_bindings, current_bindings, before_outputs,
        after_outputs, before_claim_ledger, after_claim_ledger, admission_sources, expected_admission_sources,
        *, trusted_output_seals=None):
    require(digest(parent_raw)==PUBLISHED_NOTE16_SHA256, 'Published16 parent bytes are not the approved immutable manifest')
    parent = strict_json(parent_raw)
    require(trusted_output_seals is not None and bool(trusted_output_seals), 'Immutable trusted output preimages are required')
    require(set(before_outputs)==set(trusted_output_seals), 'Output inventory differs from trusted immutable preimages')
    require(all(isinstance(seal,Seal) and before_outputs[path]==seal.sha256
        for path,seal in trusted_output_seals.items()), 'Output SHA differs from trusted immutable preimages')
    required_outputs = {'site/notes/complete-notes.md','site/notes/build.json','site/notes/content.js'}
    require(required_outputs <= set(before_outputs), 'Published16 output inventory omitted')
    require(before_outputs['site/notes/complete-notes.md']==parent['new_markdown_sha256']
        and before_outputs['site/notes/build.json']==parent['new_build_sha256'], 'Published16 output preimage differs from approved manifest')
    require(before_claim_ledger==parent['source_bindings']['reports/full-corpus-review/notes-unit-ledger.jsonl'], 'Published16 claim-ledger preimage changed')
    for path,seal in {**before_outputs,**admission_sources}.items():
        safe_path(path)
        require(isinstance(seal,str) and bool(re.fullmatch('[a-f0-9]{64}',seal)), 'Invalid source/output SHA-256')
    require(parent.get('purpose')=='SIXTEENTH_EXACT_HELD_N1_NOT_LEGAL_PASS', 'Wrong published16 parent')
    require(parent.get('canonical_release_credit')==parent.get('question_audit_credit')==0
        and parent.get('public_unit_legal_status')=='LEGAL_HOLD', 'Parent note credit/HOLD changed')
    require(old_bindings==current_bindings==parent['source_bindings'], 'Old source-binding missing or rewritten')
    require(before_outputs==after_outputs and before_claim_ledger==after_claim_ledger,
        'Source-only context cannot modify any note output or claim-review body')
    require(set(admission_sources).isdisjoint(old_bindings), 'New source context cannot replace an old bound source')
    require(admission_sources==expected_admission_sources and bool(admission_sources), 'Admission source binding missing or expanded')
    return {'purpose':'PROPOSED_SOURCE_ONLY_CONTEXT_NOT_NOTE_CONTENT_MIGRATION',
        'parent_manifest_sha256':digest(parent_raw),'note_body_delta':0,
        'parent_note_outputs':before_outputs,'claim_ledger':before_claim_ledger,
        'exact_new_admission_sources':admission_sources,'activation':MODE,
        'native_audit_credit':0,'note_legal_PASS_credit':0}


def require_acyclic_hash_dependencies(graph):
    visiting=set();done=set()
    def visit(node):
        require(node in graph, 'Unknown hash dependency')
        require(node not in visiting, 'Self/mutual hash reference cycle')
        if node in done:return
        visiting.add(node)
        for dependency in graph[node]:visit(dependency)
        visiting.remove(node);done.add(node)
    for node in graph:visit(node)
    return True


def inactive_status(root):
    """Fail closed if any enrollment is presented; this version supports none.

    A missing enrollment means INACTIVE, not approved. Existing validators do not
    dispatch through this module and continue rejecting canonical source changes.
    """
    from pathlib import Path
    root = Path(root)
    target = root / ACTIVATION_PATH
    require(not target.exists() and not target.is_symlink(),
        'Canonical successor enrollment is unsupported; native admission remains blocked')
    return {'status':MODE, 'activation_allowed':False, 'canonical_admission_credit':0,
        'legal_audit_credit':0, 'realism_audit_credit':0, 'canonical_RELEASED_credit':0,
        'legacy_replay_credit':0}


def activation_assessment(**_untrusted_claims):
    """No keyword, manifest status or caller-supplied receipt can enable release."""
    return {'status':MODE, 'activation_allowed':False,
        'blockers':['NO_ENROLLED_SUCCESSOR_SUPPORTED','NATIVE_GATES_AND_TRUSTED_BASE_REPLAY_REQUIRED'],
        'canonical_admission_credit':0, 'legal_audit_credit':0,
        'realism_audit_credit':0, 'canonical_RELEASED_credit':0, 'legacy_replay_credit':0}


def main():
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(inactive_status(args.root),sort_keys=True))


if __name__ == '__main__':
    main()

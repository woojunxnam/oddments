"""One-off exact-scope generation for Unit3B when local execution is unavailable."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE='580368073eba947d1484694fef078b413f24c85f'
ALLOWED=[
'practice_expansion/2026-10-28-representative/questions.json',
'practice_expansion/2026-10-28-representative/selection.json',
'reports/representative-rewrite/pattern-metrics.json',
'reports/representative-rewrite/audit-ledger.json',
'reports/representative-rewrite/audit-ledger.md',
'reports/representative-rewrite/near-candidates.json',
'site/practice-expansion/publication.json',
'site/practice-expansion/quality-review.html',
'site/notes/content.js','site/notes/book.html','site/notes/complete-notes.md','site/notes/build.json',
'site/notes/study-data.js','site/notes/study-build.json','site/notes/study.html',
'site/notes/refresh-data.js','site/notes/refresh-build.json',
'revisions/baselines/complete-notes-unit3a.md',
'revisions/notes/protected-migration-unit3b.json',
'reports/full-corpus-review/question-ledger.jsonl','reports/full-corpus-review/notes-unit-ledger.jsonl',
'reports/full-corpus-review/notes-claim-ledger.jsonl','reports/full-corpus-review/coverage-matrix.json',
'reports/full-corpus-review/canonical-inventory.json','reports/full-corpus-review/progress.json',
'reports/full-corpus-review/pattern-comparison.json','reports/full-corpus-review/unit3b-preservation.json',
]


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def record_hash(q):
    return hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def run(script,*args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)


def write(path,data):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def main():
    target='practice_expansion/2026-10-28-representative/questions.json'
    before=json.loads((ROOT/target).read_text())
    old={q['question_id']:record_hash(q) for q in before['questions']}
    if len(old)!=59:raise ValueError('Materialization requires exactly deployed prior59')
    prior_migration='revisions/notes/protected-migration.json'
    first=json.loads((ROOT/prior_migration).read_text())
    prior_export=(ROOT/'site/notes/complete-notes.md').read_bytes()
    if hashlib.sha256(prior_export).hexdigest()!=first['files'][0]['new_sha256']:
        raise ValueError('Prior published export differs from Unit3A migration')
    # Check immutable original bytes before making the one allowed generated migration.
    run('verify_representative_protected.py')
    baseline_copy='revisions/baselines/complete-notes-unit3a.md'
    dest=ROOT/baseline_copy;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() and dest.read_bytes()!=prior_export:raise ValueError('Refuse baseline overwrite')
    dest.write_bytes(prior_export)
    run('build_representative_rewrites.py')
    after=json.loads((ROOT/target).read_text())
    by={q['question_id']:q for q in after['questions']}
    if len(by)!=62 or any(qid not in by or record_hash(by[qid])!=expected for qid,expected in old.items()):
        raise ValueError('A previous59 question object changed or new count differs')
    p=ROOT/'site/practice-expansion/publication.json'
    config=json.loads(p.read_text())
    config.update(edition='2026-10-29.practice7-unit3b',published_total=2334,
        authorization='Owner requested continued full corpus and integrated-notes review; Unit3B applies narrow source-verified replacements while preserving archive/history and canonical audit policy.')
    addition=config['additional_banks'][-1]
    addition.update(sha256=digest(target),question_count=62,title='대표 재작성62문항')
    config['representative_selection']['sha256']=digest(config['representative_selection']['path'])
    write('site/practice-expansion/publication.json',config)
    run('build_ultimate_notes.py')
    revision='revisions/notes/2026-10-29-personnel-supervision-training.json'
    migration=dict(schema_version='notes-protected-migration/1',baseline_commit=BASE,
        authorization='Owner 2026-10-29 request covers continued notes review; exact same generated export only.',
        previous_migration_path=prior_migration,previous_migration_sha256=digest(prior_migration),
        revision_path=revision,revision_sha256=digest(revision),
        files=[dict(path='site/notes/complete-notes.md',baseline_copy=baseline_copy,
                    old_sha256=hashlib.sha256(prior_export).hexdigest(),
                    new_sha256=digest('site/notes/complete-notes.md'),
                    reason='Versioned revisions of w1-b-9/w1-b-10; original and Unit3A exports retained.')])
    write('revisions/notes/protected-migration-unit3b.json',migration)
    run('build_representative_audit_ledger.py')
    run('audit_representative_similarity.py')
    run('build_exam_study.py')
    run('build_refresh.py')
    run('build_full_corpus_review.py')
    run('build_quality_status.py')
    run('verify_representative_protected.py')
    write('reports/full-corpus-review/unit3b-preservation.json',dict(
        source_base=BASE,previous_questions=59,unchanged_previous_objects=59,
        previous_question_record_hashes=old,new_question_ids=sorted(set(by)-set(old)),
        original_guide_sha256=digest('notes/guide.json'),canonical_audit_status_changed=False,
        fresh_independent_audit_created=False,local_exec='UNAVAILABLE_REMOTE_GENERATION',
        tests='Not certified by generation; see exact worker/PR CI head outcomes.'))
    changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    unexpected=set(changed+untracked)-set(ALLOWED)
    if unexpected:raise ValueError('Unexpected materialized path(s): '+repr(sorted(unexpected)))
    print('UNIT3B_SUMMARY '+json.dumps(json.loads((ROOT/'reports/full-corpus-review/progress.json').read_text()),ensure_ascii=False))
    # Targeted selection is data for manual follow-up, not automatically reviewed.
    plus=json.loads((ROOT/'practice_expansion/2026-10-26-plus/questions.json').read_text())
    targets=[q for q in plus['questions'] if q['question_id'] in {'MA-CASE-0109','MA-CASE-0812','MA-CASE-0814'}]
    print('UNIT3B_FOLLOWUP_READ_ONLY '+json.dumps(targets,ensure_ascii=False,separators=(',',':')))
    subprocess.run(['git','add','--',*ALLOWED],cwd=ROOT,check=True)


if __name__=='__main__':
    main()

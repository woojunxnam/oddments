#!/usr/bin/env python3
"""Verify protected source bytes against a baseline anchored to real main blobs.

Normal invocation is read-only and never refreshes expected hashes. Initialization
requires an explicit GitHub main-tree snapshot and first checks each local file's
Git blob SHA-1 against that snapshot. CI then checks both SHA-256 and Git blob
SHA-1, as well as missing or added source files in the protected scope.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports/representative-rewrite'
MANIFEST = REPORTS / 'protected-baseline.json'
SUMMARY = REPORTS / 'protected-baseline.md'
BASE_COMMIT = 'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'
REPOSITORY = 'woojunxnam/oddments'
PREFIXES = (
    'data/', 'audits/', 'notes/', 'schemas/',
    'practice_expansion/2026-10-23/',
    'practice_expansion/2026-10-26-plus/',
    'practice_expansion/2026-10-27-quality/',
)
EXACT_FILES = (
    'docs/RELEASE_POLICY.md', 'docs/AUDIT_WORKFLOW.md',
    'docs/QUESTION_AUTHORING_STANDARD.md', 'docs/SOURCE_USE_POLICY.md',
    'site/notes/complete-notes.md',
)
IGNORED_CACHE_DIRECTORIES = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha1(raw):
    header = b'blob ' + str(len(raw)).encode('ascii') + b'\0'
    return hashlib.sha1(header + raw).hexdigest()


def in_scope(path):
    return path in EXACT_FILES or path.startswith(PREFIXES)


def ignored_cache(path):
    pure = PurePosixPath(path)
    return bool(set(pure.parts) & IGNORED_CACHE_DIRECTORIES) or pure.suffix in {'.pyc', '.pyo'}


def safe_file(root, relative):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative,
            'Invalid protected relative path: ' + relative)
    path = root / relative
    require(root.resolve() in path.resolve().parents, 'Protected path escapes repository: ' + relative)
    require(not path.is_symlink(), 'Protected file replaced with a symlink: ' + relative)
    require(path.is_file(), 'Missing protected file: ' + relative)
    return path


def inventory(root=ROOT):
    paths = set(EXACT_FILES)
    for prefix in PREFIXES:
        directory = root / prefix
        require(directory.is_dir() and not directory.is_symlink(), 'Missing or symlinked protected directory: ' + prefix)
        for path in directory.rglob('*'):
            if path.is_file() or path.is_symlink():
                relative = path.relative_to(root).as_posix()
                if not ignored_cache(relative):
                    paths.add(relative)
    return paths


def render_summary(manifest):
    groups = manifest['counts']['by_top_level_directory']
    lines = [
        '# 대표 문항 재작성: 원본 보호 기준', '',
        f"Repository: `{manifest['repository']}` · 기준 main commit: `{manifest['baseline_commit']}`", '',
        '이 기준은 현재 파일의 SHA-256을 단순 등록한 것이 아닙니다. 초기 생성 시 실제 main의 GitHub tree/blob 기록과 각 보호 파일의 Git blob SHA-1을 먼저 대조했고, 일치한 바이트의 SHA-256만 저장했습니다.', '',
        f"보호 파일 **{manifest['counts']['files']:,}개**, 총 **{manifest['counts']['bytes']:,} bytes**. 완전한 파일별 경로·Git blob SHA-1·SHA-256은 [protected-baseline.json](protected-baseline.json)에 있습니다.", '',
        '## 범위', '', '| 최상위 디렉터리 | 보호 파일 수 |', '|---|---:|',
    ]
    lines.extend(f'| {name} | {count} |' for name, count in groups.items())
    lines += ['', '보호하는 디렉터리:', '']
    lines.extend('- `' + prefix + '`' for prefix in PREFIXES)
    lines += ['', '추가 보호 파일:', '']
    lines.extend('- `' + path + '`' for path in EXACT_FILES)
    lines += ['', '## 확인 방식과 한계', '',
              '- 일반 실행은 파일별 SHA-256·Git blob SHA-1·크기와 보호 범위의 파일 집합을 확인합니다. 보호 원본의 변경·삭제·새 source 파일 추가는 실패합니다.',
              '- Python/test cache는 source inventory에서 제외합니다. 이 제외는 JSON·법규·문항 source 파일을 제외하지 않습니다.',
              '- 허용된 파생 산출물 `site/notes/study-data.js`, `site/notes/study-build.json`은 보호 범위에 넣지 않습니다. 새 대표 재작성 collection과 새 보고서·개발 스크립트도 이 기존 원본 기준의 대상이 아닙니다.',
              '- 검증 실행은 baseline을 자동으로 갱신하지 않습니다. 명시적인 초기 생성도 동일한 기준이 이미 있으면 바이트가 같은 경우에만 허용됩니다.',
              '- 이 기준은 원본 보존 증거입니다. 문항의 법규 정확성, 독립 감사 완료 또는 브라우저의 학습 기록 동작을 판정하지 않습니다.', '',
              '## 재현 명령', '', '```sh', 'python scripts/verify_representative_protected.py', '```', '',
              f"초기 GitHub tree snapshot SHA-256: `{manifest['baseline_source']['tree_snapshot_sha256']}`", '',
              '초기 snapshot은 CI에서 다시 필요하지 않습니다. CI는 저장된 기준의 각 원본 Git blob과 SHA-256을 확인합니다.', '']
    return '\n'.join(lines).encode('utf-8')


def make_baseline(main_tree, root=ROOT):
    raw_tree = main_tree.read_bytes()
    tree = json.loads(raw_tree)
    require(tree.get('sha') == BASE_COMMIT, 'Tree snapshot does not identify the required baseline main commit.')
    require(not tree.get('truncated', False), 'Truncated main-tree snapshot is not a baseline.')
    entries = tree['tree']
    require(len({entry['path'] for entry in entries}) == len(entries), 'Duplicate paths in the main-tree snapshot.')
    require(all(entry.get('type') in {'blob', 'tree'} for entry in entries if in_scope(entry['path'])),
            'Unsupported object in a protected main-tree directory.')
    selected = [entry for entry in entries if in_scope(entry['path']) and entry.get('type') == 'blob']
    require(selected, 'No protected source files in the main-tree snapshot.')
    require(set(EXACT_FILES) <= {entry['path'] for entry in selected}, 'A required protected policy/note is absent from main.')
    expected_paths = {entry['path'] for entry in selected}
    actual_paths = inventory(root)
    require(actual_paths == expected_paths,
            'Protected inventory differs from main; missing=' + repr(sorted(expected_paths - actual_paths)) +
            '; added=' + repr(sorted(actual_paths - expected_paths)))
    records = []
    for entry in sorted(selected, key=lambda x: x['path']):
        path = entry['path']
        require(entry.get('type') == 'blob' and entry.get('mode') in {'100644', '100755'},
                'Unsupported protected Git object: ' + path)
        blob = entry['sha']
        require(re.fullmatch(r'[0-9a-f]{40}', blob), 'Invalid main blob SHA-1: ' + path)
        raw = safe_file(root, path).read_bytes()
        require(git_blob_sha1(raw) == blob, 'Current protected bytes differ from actual main blob: ' + path)
        if 'size' in entry:
            require(len(raw) == entry['size'], 'Main blob size mismatch: ' + path)
        records.append(dict(path=path, bytes=len(raw), sha256=sha256(raw), git_blob_sha1=blob,
                            git_mode=entry['mode'],
                            official_blob_url=f'https://api.github.com/repos/{REPOSITORY}/git/blobs/{blob}',
                            verified_against_main_blob=True))
    return dict(
        schema_version='representative-protected-baseline/1', repository=REPOSITORY,
        baseline_commit=BASE_COMMIT,
        baseline_source=dict(
            description='Actual GitHub main tree/blob records recovered for the identified commit; each protected local file matched its recorded Git blob SHA-1 before SHA-256 enrollment.',
            tree_snapshot_sha256=sha256(raw_tree), tree_response_sha=tree['sha'],
            tree_record_count=len(entries), all_enrolled_files_matched_main_blob=True,
            tree_snapshot_required_for_regular_ci=False,
        ),
        protected_prefixes=list(PREFIXES), protected_exact_files=list(EXACT_FILES),
        excluded_generated_files=['site/notes/study-data.js', 'site/notes/study-build.json'],
        ignored_cache_directories=sorted(IGNORED_CACHE_DIRECTORIES),
        ignored_cache_suffixes=['.pyc', '.pyo'],
        counts=dict(files=len(records), bytes=sum(row['bytes'] for row in records),
                    by_top_level_directory=dict(sorted(collections.Counter(row['path'].split('/')[0] for row in records).items()))),
        canonical_release_status_changed=False,
        independent_legal_audit_created=False,
        files=records,
    )


def migrated_baseline_bytes(root, relative, current):
    if relative=='site/notes/complete-notes.md'and (root/'revisions/notes/protected-migration-held-n1.json').exists():
        from notes_held_sixteenth import decode
        return decode(root,relative,current)
    if relative in ('data/questions/ma-q-0012.json','data/exam_style/question_family_matrix.json',
                    'data/study_guide/sections/sg-cii-lifecycle.json'):
        from canonical_q0012_withdrawal import decode
        return decode(root,relative,current)
    # Only this exact generated export can migrate; immutable inputs remain strict.
    effective_build = None
    fifteenth_path=root/'revisions/notes/protected-migration-after190.json'
    if fifteenth_path.exists() and relative=='site/notes/complete-notes.md':
        from notes_after190_annotation import decode
        current=decode(root,relative,current)
    fourteenth_path=root/'revisions/notes/protected-migration-independent-notes-wave3.json'
    if fourteenth_path.exists() and relative=='site/notes/complete-notes.md':
        metadata=json.loads(fourteenth_path.read_bytes())
        require(metadata['schema_version']=='notes-protected-annotation-migration/1' and
                metadata['baseline_commit']=='f4ecea13a31b4c8dbdb7ef460b8caee54b571b27',
                'Unexpected wave3 independent-note annotation migration base')
        require(metadata['path']==relative and
                metadata['baseline_copy']=='revisions/baselines/complete-notes-pr189.md' and
                metadata['baseline_build_copy']=='revisions/baselines/notes-build-pr189.json',
                'Wave3 independent-note annotation migration expands protected scope')
        require(metadata.get('canonical_release_credit')==0,
                'Wave3 annotation cannot create canonical release credit')
        require(metadata['previous_migration_path']=='revisions/notes/protected-migration-independent-notes-wave2.json' and
                metadata['previous_migration_sha256']=='8573eced55fdd94dd9fa23ede6da19fa7049b93026200a27096cd73d503e3e8b' and
                sha256(safe_file(root,metadata['previous_migration_path']).read_bytes())==metadata['previous_migration_sha256'],
                'Published wave2 independent-note annotation migration changed')
        historical_build=safe_file(root,metadata['baseline_build_copy']).read_bytes()
        require(metadata['baseline_build_sha256']=='d4f24c8c32745d3b4c4d8d411fd3e07dbc94bbcbdad55fe028bccf9479a3ad2e' and
                sha256(historical_build)==metadata['baseline_build_sha256'],
                'Published PR189 build changed')
        previous_build=json.loads(historical_build)
        current_build=json.loads(safe_file(root,'site/notes/build.json').read_bytes())
        from notes_revision import load_notes
        semantic_sha256=sha256(json.dumps(load_notes(root),ensure_ascii=False,sort_keys=True).encode())
        require(metadata['semantic_notes_sha256']==semantic_sha256==
                previous_build['content_sha256']==current_build['content_sha256']==
                'e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824' and
                previous_build['revision_provenance']==current_build['revision_provenance'] and
                previous_build['edition']==current_build['edition']=='2026-11-03.emergency-kit.1',
                'Wave3 independent-note annotation cannot authorize semantic note changes')
        scope={
            'third-b-review.json':{'oral-followup','w2-b-1','w2-b-2','w2-b-3','w2-b-4'},
            'third-e-review.json':{'w2-b-5','w2-b-6','w2-b-7','w2-b-8','w2-b-9'},
            'third-g-review.json':{'w2-b-10','w2-b-11','w2-b-12','w2-b-13','w2-c-1'},
            'third-f-review.json':{'w2-c-2','schedule-vi-continuity','w2-c-4','w2-c-5','w2-c-6'},
        }
        review_scope={'reports/full-corpus-review/independent-notes/'+name:ids for name,ids in scope.items()}
        require(set(metadata['independent_reviews'])==set(review_scope),
                'Wave3 independent-note annotation evidence scope changed')
        for path,expected_units in review_scope.items():
            report_raw=safe_file(root,path).read_bytes()
            require(sha256(report_raw)==metadata['independent_reviews'][path],
                    'Wave3 independent-note annotation review changed')
            report=json.loads(report_raw)
            require(report.get('stage')=='independent-notes' and
                    report.get('canonical_audit') is False and report.get('canonical_release_credit')==0 and
                    report.get('question_audit_credit')==0 and
                    len(report['records'])==len(expected_units) and
                    {r['unit_id'] for r in report['records']}==expected_units,
                    'Wave3 independent-note annotation review unit scope or credit changed')
        require(sha256(current)==metadata['new_sha256'], 'Stale wave3 independent-note annotation export')
        current=safe_file(root,metadata['baseline_copy']).read_bytes()
        require(metadata['old_sha256']=='f4ebbad48aaea4575c123533878d59a90fc12a19391e2a3b49e13666f8a93440' and
                sha256(current)==metadata['old_sha256'], 'Published PR189 export changed')
        # Decode only this new annotation layer. All thirteen published guards
        # below still evaluate their original manifest and historical bytes.
    thirteenth_path=root/'revisions/notes/protected-migration-independent-notes-wave2.json'
    if thirteenth_path.exists() and relative=='site/notes/complete-notes.md':
        metadata=json.loads(thirteenth_path.read_bytes())
        require(metadata['schema_version']=='notes-protected-annotation-migration/1' and
                metadata['baseline_commit']=='b5d1b3e98ca3a7d97252b331a33cf7a4c0ba956b',
                'Unexpected independent-note annotation migration base')
        require(metadata['path']==relative and
                metadata['baseline_copy']=='revisions/baselines/complete-notes-pr188.md' and
                metadata['baseline_build_copy']=='revisions/baselines/notes-build-pr188.json',
                'Independent-note annotation migration expands protected scope')
        require(metadata['previous_migration_path']=='revisions/notes/protected-migration-emergency-kit.json' and
                metadata['previous_migration_sha256']=='b74a101c0319ae9ca7cba366c55125243a2f8f9186e43bf45a7148fe8ea9fa35' and
                sha256(safe_file(root,metadata['previous_migration_path']).read_bytes())==metadata['previous_migration_sha256'],
                'Published emergency-kit migration changed')
        historical_build=safe_file(root,metadata['baseline_build_copy']).read_bytes()
        require(metadata['baseline_build_sha256']=='373b22191f5c2f9565b2dc3206d93801a488cfc65eab1e97f7ffa31b8985416f' and
                sha256(historical_build)==metadata['baseline_build_sha256'],
                'Published PR188 build changed')
        previous_build=json.loads(historical_build)
        current_build=json.loads(safe_file(root,'site/notes/build.json').read_bytes())
        from notes_revision import load_notes
        semantic_sha256=sha256(json.dumps(load_notes(root),ensure_ascii=False,sort_keys=True).encode())
        require(metadata['semantic_notes_sha256']==semantic_sha256==
                previous_build['content_sha256']==current_build['content_sha256']==
                'e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824' and
                previous_build['revision_provenance']==current_build['revision_provenance'] and
                previous_build['edition']==current_build['edition']=='2026-11-03.emergency-kit.1',
                'Independent-note annotation cannot authorize semantic note changes')
        scope={
            'second-b-review.json':{'w1-b-10','w1-b-11','w1-b-12','w1-c-1','w1-c-2'},
            'second-c-review.json':{'w1-c-3','w1-c-4','w1-c-5','w1-c-6','w1-c-7'},
            'second-e-review.json':{'w1-c-8','w4-a-21','w2-a-2','w2-a-3','w2-a-4'},
            'second-f-review.json':{'w2-a-5','w2-a-6','w2-a-7','w2-a-8','w2-a-10'},
        }
        review_scope={'reports/full-corpus-review/independent-notes/'+name:ids for name,ids in scope.items()}
        require(set(metadata['independent_reviews'])==set(review_scope),
                'Independent-note annotation evidence scope changed')
        for path,expected_units in review_scope.items():
            report_raw=safe_file(root,path).read_bytes()
            require(sha256(report_raw)==metadata['independent_reviews'][path],
                    'Independent-note annotation review changed')
            report=json.loads(report_raw)
            require(report.get('stage')=='independent-notes' and
                    report.get('canonical_audit') is False and report.get('canonical_release_credit')==0 and
                    len(report['records'])==len(expected_units) and
                    {r['unit_id'] for r in report['records']}==expected_units,
                    'Independent-note annotation review unit scope changed')
        require(sha256(current)==metadata['new_sha256'], 'Stale independent-note annotation export')
        current=safe_file(root,metadata['baseline_copy']).read_bytes()
        require(metadata['old_sha256']=='8d23fa9c5e63deffd33218630a630a61d946cfd25d56bc578b553cbc37a84aaf' and
                sha256(current)==metadata['old_sha256'], 'Published PR188 export changed')
        # Feed the original PR188 export into the unchanged twelve older guards.
        # The current semantic build remains M in both contexts.
    twelfth_path=root/'revisions/notes/protected-migration-emergency-kit.json'
    if twelfth_path.exists() and relative=='site/notes/complete-notes.md':
        from notes_emergency_activation import (REVISION_M, ACTIVATION, REVIEW, CENSUS,
            REVISION_SHA256, REVIEW_SHA256, CENSUS_SHA256, validate_emergency_note_review)
        from notes_revision import load_notes
        twelfth=json.loads(twelfth_path.read_bytes())
        require(twelfth['schema_version']=='notes-protected-semantic-migration/1' and
                twelfth['baseline_commit']=='0e1c03302b38401ed53085af4ee402abfd0b46ec',
                'Unexpected emergency-kit migration base')
        require(twelfth['path']==relative and
                twelfth['baseline_copy']=='revisions/baselines/complete-notes-census-wave8-9.md' and
                twelfth['baseline_build_copy']=='revisions/baselines/notes-build-census-wave8-9.json',
                'Emergency-kit migration expands protected scope')
        require(twelfth['revision_path']==REVISION_M and twelfth['revision_sha256']==REVISION_SHA256 and
                twelfth['activation_path']==ACTIVATION and twelfth['review_path']==REVIEW and
                twelfth['review_sha256']==REVIEW_SHA256 and twelfth['census_path']==CENSUS and
                twelfth['census_sha256']==CENSUS_SHA256,
                'Emergency-kit migration review scope changed')
        revision_raw=safe_file(root,REVISION_M).read_bytes()
        require(sha256(revision_raw)==REVISION_SHA256 and
                sha256(safe_file(root,ACTIVATION).read_bytes())==twelfth['activation_sha256'] and
                sha256(safe_file(root,REVIEW).read_bytes())==REVIEW_SHA256 and
                sha256(safe_file(root,CENSUS).read_bytes())==CENSUS_SHA256,
                'Emergency-kit activation or independent evidence changed')
        validate_emergency_note_review(root,revision_raw,json.loads(revision_raw))
        require(twelfth['previous_migration_path']=='revisions/notes/protected-migration-census-wave8-9.json' and
                twelfth['previous_migration_sha256']=='9ccb67705c0a371e683fe5d1a5f129a6b59a7581e93e06c8eddfaa4cae72a933' and
                sha256(safe_file(root,twelfth['previous_migration_path']).read_bytes())==twelfth['previous_migration_sha256'],
                'Previous census annotation migration changed')
        current_build=json.loads(safe_file(root,'site/notes/build.json').read_bytes())
        semantic_sha256=sha256(json.dumps(load_notes(root),ensure_ascii=False,sort_keys=True).encode())
        require(current_build['edition']=='2026-11-03.emergency-kit.1' and
                current_build['content_sha256']==twelfth['semantic_notes_sha256']==semantic_sha256 and
                current_build['revision_provenance']['path']==REVISION_M and
                current_build['revision_provenance']['sha256']==REVISION_SHA256,
                'Emergency-kit current semantic build changed')
        require(sha256(current)==twelfth['new_sha256'], 'Stale emergency-kit export')
        current=safe_file(root,twelfth['baseline_copy']).read_bytes()
        require(twelfth['old_sha256']=='23b17eb365f0f58b3a59f7755151ca11335c569e3260b0b2ac628dc8e9435c41' and
                sha256(current)==twelfth['old_sha256'], 'Historical J census export changed')
        historical_build=safe_file(root,twelfth['baseline_build_copy']).read_bytes()
        require(twelfth['baseline_build_sha256']=='39bfac671f059d494fca5b01caae69796318ca6a7b19957ae1be447946907d8d' and
                sha256(historical_build)==twelfth['baseline_build_sha256'],
                'Historical J census build changed')
        effective_build=json.loads(historical_build)
        require(effective_build['edition']=='2026-11-03.refill-cancer.1' and
                effective_build['content_sha256']==twelfth['previous_semantic_notes_sha256']==
                '8138f0556bcaba8f157eed04bc8a6754bc9e3a0f0f53b9dd35a6e06f38e1bb1b',
                'Emergency-kit migration historical semantic context changed')
    metadata_path=root/'revisions/notes/protected-migration-census-wave8-9.json'
    if metadata_path.exists() and relative=='site/notes/complete-notes.md':
        metadata=json.loads(metadata_path.read_bytes())
        require(metadata['baseline_commit']=='2a7873ea9a0061d70f970969996106ad9f76a60f',
                'Unexpected census annotation migration base')
        require(metadata['path']==relative and metadata['baseline_copy']=='revisions/baselines/complete-notes-refill-cancer.md',
                'Census annotation migration expands protected scope')
        require(metadata['revision_path']=='revisions/notes/2026-11-03-refill-cancer-final.json' and
                metadata['previous_migration_path']=='revisions/notes/protected-migration-refill-cancer.json',
                'Census annotation revision or parent changed')
        require(sha256(safe_file(root,metadata['revision_path']).read_bytes())==metadata['revision_sha256'] and
                sha256(safe_file(root,metadata['previous_migration_path']).read_bytes())==metadata['previous_migration_sha256'],
                'Census annotation source or previous migration changed')
        require(metadata['baseline_build_copy']=='revisions/baselines/notes-build-refill-cancer.json' and
                sha256(safe_file(root,metadata['baseline_build_copy']).read_bytes())==metadata['baseline_build_sha256'],
                'Census annotation baseline build changed')
        require(json.loads(safe_file(root,metadata['baseline_build_copy']).read_bytes())['content_sha256']==metadata['semantic_notes_sha256'] and
                (effective_build if effective_build is not None else
                 json.loads(safe_file(root,'site/notes/build.json').read_bytes()))['content_sha256']==metadata['semantic_notes_sha256'],
                'Census metadata cannot authorize a semantic note edit')
        require(set(metadata['census_sources'])=={'reports/full-corpus-review/note-wave8-census.json',
                                                 'reports/full-corpus-review/note-wave9-census.json'},
                'Census annotation evidence scope changed')
        for path,digest in metadata['census_sources'].items():
            require(sha256(safe_file(root,path).read_bytes())==digest, 'Census annotation evidence changed')
        require(sha256(current)==metadata['new_sha256'], 'Stale census annotation export')
        current=safe_file(root,metadata['baseline_copy']).read_bytes()
        require(sha256(current)==metadata['old_sha256'], 'Previous refill/cancer export changed')
    tenth_path=root/'revisions/notes/protected-migration-refill-cancer.json'
    if tenth_path.exists() and relative=='site/notes/complete-notes.md':
        tenth=json.loads(tenth_path.read_bytes())
        require(tenth['baseline_commit']=='c46e0f85fcedd0de468215f90b1112104da9997e',
                'Unexpected refill/cancer migration base')
        require(tenth['path']==relative and tenth['baseline_copy']=='revisions/baselines/complete-notes-ce-disclosure.md',
                'Refill/cancer migration expands protected scope')
        require(tenth['revision_path']=='revisions/notes/2026-11-03-refill-cancer-final.json',
                'Unexpected refill/cancer revision')
        require(tenth['previous_migration_path']=='revisions/notes/protected-migration-ce-disclosure.json',
                'Unexpected refill/cancer migration parent')
        require(sha256(safe_file(root,tenth['revision_path']).read_bytes())==tenth['revision_sha256'],
                'Stale refill/cancer overlay source')
        require(sha256(safe_file(root,tenth['previous_migration_path']).read_bytes())==tenth['previous_migration_sha256'],
                'Previous CE disclosure migration changed')
        require(sha256(current)==tenth['new_sha256'], 'Stale refill/cancer export')
        current=safe_file(root,tenth['baseline_copy']).read_bytes()
        require(sha256(current)==tenth['old_sha256'], 'Previous CE disclosure export changed')
    ninth_path=root/'revisions/notes/protected-migration-ce-disclosure.json'
    if ninth_path.exists() and relative=='site/notes/complete-notes.md':
        ninth=json.loads(ninth_path.read_bytes())
        require(ninth['baseline_commit']=='3f93165e18af53d8a9dfcfe654805ba61164e303',
                'Unexpected CE disclosure migration base')
        require(ninth['path']==relative and ninth['baseline_copy']=='revisions/baselines/complete-notes-counsel-shield.md',
                'CE disclosure migration expands protected scope')
        require(ninth['revision_path']=='revisions/notes/2026-11-03-ce-disclosure-final.json',
                'Unexpected CE disclosure revision')
        require(ninth['previous_migration_path']=='revisions/notes/protected-migration-counsel-shield.json',
                'Unexpected CE disclosure migration parent')
        require(sha256(safe_file(root,ninth['revision_path']).read_bytes())==ninth['revision_sha256'],
                'Stale CE disclosure overlay source')
        require(sha256(safe_file(root,ninth['previous_migration_path']).read_bytes())==ninth['previous_migration_sha256'],
                'Previous counsel/Shield migration changed')
        require(sha256(current)==ninth['new_sha256'], 'Stale CE disclosure export')
        current=safe_file(root,ninth['baseline_copy']).read_bytes()
        require(sha256(current)==ninth['old_sha256'], 'Previous counsel/Shield export changed')
    eighth_path=root/'revisions/notes/protected-migration-counsel-shield.json'
    if eighth_path.exists() and relative=='site/notes/complete-notes.md':
        eighth=json.loads(eighth_path.read_bytes())
        require(eighth['baseline_commit']=='3f93165e18af53d8a9dfcfe654805ba61164e303',
                'Unexpected counsel/Shield migration base')
        require(eighth['path']==relative and eighth['baseline_copy']=='revisions/baselines/complete-notes-cdtm13-vax04.md',
                'Counsel/Shield migration expands protected scope')
        require(eighth['revision_path']=='revisions/notes/2026-11-03-counsel-shield-final.json',
                'Unexpected counsel/Shield revision')
        require(eighth['previous_migration_path']=='revisions/notes/protected-migration-cdtm13-vax04.json',
                'Unexpected counsel/Shield migration parent')
        require(sha256(safe_file(root,eighth['revision_path']).read_bytes())==eighth['revision_sha256'],
                'Stale counsel/Shield overlay source')
        require(sha256(safe_file(root,eighth['previous_migration_path']).read_bytes())==eighth['previous_migration_sha256'],
                'Previous CDTM13/VAX04 migration changed')
        require(sha256(current)==eighth['new_sha256'], 'Stale counsel/Shield export')
        current=safe_file(root,eighth['baseline_copy']).read_bytes()
        require(sha256(current)==eighth['old_sha256'], 'Previous published CDTM13/VAX04 export changed')
    seventh_path=root/'revisions/notes/protected-migration-cdtm13-vax04.json'
    if seventh_path.exists() and relative=='site/notes/complete-notes.md':
        seventh=json.loads(seventh_path.read_bytes())
        require(seventh['baseline_commit']=='8e3c4dd1e7ec7315e6831dc1e95f8daf0cbd78f6',
                'Unexpected CDTM13/VAX04 migration base')
        require(seventh['path']==relative and seventh['baseline_copy']=='revisions/baselines/complete-notes-cdtm0512.md',
                'CDTM13/VAX04 migration expands protected scope')
        require(seventh['revision_path']=='revisions/notes/2026-10-30-cdtm13-vax04.json',
                'Unexpected CDTM13/VAX04 revision')
        require(seventh['previous_migration_path']=='revisions/notes/protected-migration-cdtm0512.json',
                'Unexpected CDTM13/VAX04 parent')
        require(sha256(safe_file(root,seventh['revision_path']).read_bytes())==seventh['revision_sha256'],
                'Stale CDTM13/VAX04 overlay source')
        require(sha256(safe_file(root,seventh['previous_migration_path']).read_bytes())==seventh['previous_migration_sha256'],
                'Previous CDTM05/VAX migration changed')
        require(sha256(current)==seventh['new_sha256'],
                'Stale CDTM13/VAX04 export')
        current=safe_file(root,seventh['baseline_copy']).read_bytes()
        require(sha256(current)==seventh['old_sha256'],
                'Previous published CDTM05-12 notes export changed')
    sixth_path=root/'revisions/notes/protected-migration-cdtm0512.json'
    if sixth_path.exists() and relative=='site/notes/complete-notes.md':
        sixth=json.loads(sixth_path.read_bytes())
        require(sixth['baseline_commit']=='6e47fc7efbf4bef1c2f337ace55ca7d111631d21',
                'Unexpected CDTM05-12 migration base')
        require(sixth['path']==relative and sixth['baseline_copy']=='revisions/baselines/complete-notes-discipline-cdtm.md',
                'CDTM05-12 migration expands scope')
        require(sixth['revision_path']=='revisions/notes/2026-10-30-cdtm0512.json',
                'Unexpected CDTM05-12 revision')
        require(sixth['previous_migration_path']=='revisions/notes/protected-migration-discipline-cdtm.json',
                'Unexpected CDTM05-12 parent')
        require(sha256(safe_file(root,sixth['revision_path']).read_bytes())==sixth['revision_sha256'],
                'Stale CDTM05-12 notes overlay')
        require(sha256(safe_file(root,sixth['previous_migration_path']).read_bytes())==sixth['previous_migration_sha256'],
                'Previous CDTM migration manifest mutated')
        require(sha256(current)==sixth['new_sha256'],'Stale CDTM05-12 generated export')
        current=safe_file(root,sixth['baseline_copy']).read_bytes()
        require(sha256(current)==sixth['old_sha256'],'Prior CDTM export baseline changed')
    fifth_path=root/'revisions/notes/protected-migration-discipline-cdtm.json'
    if fifth_path.exists() and relative=='site/notes/complete-notes.md':
        fifth=json.loads(fifth_path.read_bytes())
        require(fifth['baseline_commit']=='c4a05c8bf48ecc333e331b3c267607af6590ac40', 'Unexpected discipline CDTM migration base')
        require(fifth['path']==relative and fifth['baseline_copy']=='revisions/baselines/complete-notes-mor-discipline.md', 'Discipline CDTM migration expands scope')
        require(fifth['revision_path']=='revisions/notes/2026-10-30-discipline-cdtm.json', 'Unexpected discipline CDTM revision')
        require(fifth['previous_migration_path']=='revisions/notes/protected-migration-mor-discipline.json', 'Unexpected discipline CDTM parent migration')
        require(sha256(safe_file(root,fifth['previous_migration_path']).read_bytes())==fifth['previous_migration_sha256'], 'Prior MOR discipline migration changed')
        require(sha256(safe_file(root,fifth['revision_path']).read_bytes())==fifth['revision_sha256'], 'Stale discipline CDTM revision')
        require(sha256(current)==fifth['new_sha256'], 'Stale discipline CDTM export')
        current=safe_file(root,fifth['baseline_copy']).read_bytes()
        require(sha256(current)==fifth['old_sha256'], 'Prior MOR discipline baseline changed')
    fourth_path=root/'revisions/notes/protected-migration-mor-discipline.json'
    if fourth_path.exists() and relative=='site/notes/complete-notes.md':
        fourth=json.loads(fourth_path.read_bytes())
        require(fourth['path']==relative and fourth['baseline_copy']=='revisions/baselines/complete-notes-mor-presence.md', 'MOR discipline migration expands scope')
        require(fourth['revision_path']=='revisions/notes/2026-10-30-mor-discipline.json', 'Unexpected MOR discipline revision')
        require(fourth['previous_migration_path']=='revisions/notes/protected-migration-mor.json', 'Unexpected MOR discipline parent migration')
        require(sha256(safe_file(root,fourth['previous_migration_path']).read_bytes())==fourth['previous_migration_sha256'], 'Prior MOR migration changed')
        require(sha256(safe_file(root,fourth['revision_path']).read_bytes())==fourth['revision_sha256'], 'Stale MOR discipline revision')
        require(sha256(current)==fourth['new_sha256'], 'Stale MOR discipline export')
        current=safe_file(root,fourth['baseline_copy']).read_bytes()
        require(sha256(current)==fourth['old_sha256'], 'Prior MOR presence baseline changed')
    third_path=root/'revisions/notes/protected-migration-mor.json'
    if third_path.exists() and relative=='site/notes/complete-notes.md':
        third=json.loads(third_path.read_bytes())
        require(third['path']==relative and third['baseline_copy']=='revisions/baselines/complete-notes-unit3b.md', 'MOR migration expands scope')
        require(third['revision_path']=='revisions/notes/2026-10-30-mor-presence.json', 'Unexpected MOR revision')
        require(sha256(safe_file(root,third['revision_path']).read_bytes())==third['revision_sha256'], 'Stale MOR revision')
        require(sha256(current)==third['new_sha256'], 'Stale MOR export')
        current=safe_file(root,third['baseline_copy']).read_bytes()
        require(sha256(current)==third['old_sha256'], 'Prior MOR baseline changed')
    migration_path = root / 'revisions/notes/protected-migration.json'
    if not migration_path.exists() or relative != 'site/notes/complete-notes.md':
        return current
    migration = json.loads(migration_path.read_bytes())
    require(migration['schema_version'] == 'notes-protected-migration/1', 'Unknown migration schema')
    require(migration['baseline_commit'] == '9f3fed116792b33c65cad35da77a8d68aab58c06', 'Unexpected migration base')
    require([x['path'] for x in migration['files']] == ['site/notes/complete-notes.md'], 'Migration expands protected scope')
    require(migration['revision_path'] == 'revisions/notes/2026-10-29-personnel-ratios.json', 'Unexpected revision source')
    revision = safe_file(root, migration['revision_path']).read_bytes()
    require(sha256(revision) == migration['revision_sha256'], 'Stale migration revision hash')
    row = migration['files'][0]
    require(row['baseline_copy'] == 'revisions/baselines/complete-notes-2026-10-23.1.md', 'Unexpected baseline copy')
    baseline = safe_file(root, row['baseline_copy']).read_bytes()
    require(sha256(baseline) == row['old_sha256'], 'Archived notes baseline changed')
    followup_path=root/'revisions/notes/protected-migration-unit3b.json'
    if followup_path.exists():
        followup=json.loads(followup_path.read_bytes())
        require(followup['schema_version']=='notes-protected-migration/1', 'Unknown followup migration schema')
        require(followup['baseline_commit']=='580368073eba947d1484694fef078b413f24c85f', 'Unexpected followup baseline')
        require(followup['previous_migration_path']=='revisions/notes/protected-migration.json', 'Unexpected previous migration path')
        require(followup['previous_migration_sha256']==sha256(migration_path.read_bytes()), 'Prior migration changed')
        require(followup['revision_path']=='revisions/notes/2026-10-29-personnel-supervision-training.json', 'Unexpected followup source')
        require(sha256(safe_file(root,followup['revision_path']).read_bytes())==followup['revision_sha256'], 'Stale followup revision hash')
        require([x['path'] for x in followup['files']]==['site/notes/complete-notes.md'], 'Followup migration expands protected scope')
        new_row=followup['files'][0]
        require(new_row['baseline_copy']=='revisions/baselines/complete-notes-unit3a.md', 'Unexpected followup baseline copy')
        previous=safe_file(root,new_row['baseline_copy']).read_bytes()
        require(sha256(previous)==row['new_sha256']==new_row['old_sha256'], 'Prior rendered notes baseline changed')
        require(sha256(current)==new_row['new_sha256'], 'Generated notes migration hash changed')
    else:
        require(sha256(current) == row['new_sha256'], 'Generated notes migration hash changed')
    return baseline


def verify(manifest, root=ROOT):
    require(manifest['schema_version'] == 'representative-protected-baseline/1', 'Unexpected protection schema.')
    require(manifest['repository'] == REPOSITORY and manifest['baseline_commit'] == BASE_COMMIT,
            'Unexpected protection repository or baseline commit.')
    require(manifest['protected_prefixes'] == list(PREFIXES) and manifest['protected_exact_files'] == list(EXACT_FILES),
            'Protection scope changed; do not silently weaken the baseline.')
    require(manifest['baseline_source']['all_enrolled_files_matched_main_blob'] is True,
            'Baseline was not anchored to main blob records.')
    records = manifest['files']
    paths = [row['path'] for row in records]
    require(len(paths) == len(set(paths)) and paths == sorted(paths), 'Invalid protected file inventory.')
    require(all(in_scope(path) and not ignored_cache(path) for path in paths), 'Manifest includes a file outside protected scope.')
    expected_paths, actual_paths = set(paths), inventory(root)
    require(expected_paths == actual_paths,
            'Protected inventory changed; missing=' + repr(sorted(expected_paths - actual_paths)) +
            '; added=' + repr(sorted(actual_paths - expected_paths)))
    total_bytes = 0
    for row in records:
        raw = safe_file(root, row['path']).read_bytes()
        raw = migrated_baseline_bytes(root, row['path'], raw)
        require(len(raw) == row['bytes'], 'Protected source size changed: ' + row['path'])
        require(sha256(raw) == row['sha256'], 'Protected source SHA-256 changed: ' + row['path'])
        require(git_blob_sha1(raw) == row['git_blob_sha1'], 'Protected source differs from main Git blob: ' + row['path'])
        require(row['verified_against_main_blob'] is True, 'Unverified baseline entry: ' + row['path'])
        total_bytes += len(raw)
    require(manifest['counts']['files'] == len(records) and manifest['counts']['bytes'] == total_bytes,
            'Protected baseline summary counts are inconsistent.')
    return dict(files=len(records), bytes=total_bytes, baseline_commit=BASE_COMMIT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Explicit alias for the default read-only verification.')
    parser.add_argument('--initialize-from-main-tree', type=Path,
                        help='Create the initial baseline only after every current byte matches the supplied actual main blob record.')
    args = parser.parse_args()
    require(not (args.check and args.initialize_from_main_tree), 'Use verification or explicit initialization, not both.')
    if args.initialize_from_main_tree:
        manifest = make_baseline(args.initialize_from_main_tree)
        outputs = {MANIFEST: encoded(manifest), SUMMARY: render_summary(manifest)}
        for path, payload in outputs.items():
            if path.exists():
                require(path.read_bytes() == payload, 'Refusing to overwrite an established protection baseline: ' + str(path))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
    else:
        require(MANIFEST.is_file(), 'Protection baseline is missing; initialization requires the actual main-tree records.')
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    result = verify(manifest)
    require(SUMMARY.is_file() and SUMMARY.read_bytes() == render_summary(manifest), 'Protection summary drift.')
    print(f"Verified {result['files']:,} protected files ({result['bytes']:,} bytes) against main {BASE_COMMIT}; immutable baseline retained; only the exact manifest-bound generated notes export may migrate. Audit status unchanged.")


if __name__ == '__main__':
    main()

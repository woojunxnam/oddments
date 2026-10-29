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
    # Only this exact generated export can migrate; immutable inputs remain strict.
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

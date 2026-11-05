#!/usr/bin/env python3
"""Capture actual premerge API evidence after all candidate QA, without merging.

No API request occurs on import, syntax checking, --help, or missing CLI inputs.
The controller must invoke this only after actual QA on the final candidate.
All writes use a new external directory; no repository or CI is changed.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

REPOSITORY = 'woojunxnam/oddments'
API_ROOT = 'https://api.github.com/repos/' + REPOSITORY + '/'
VALIDATOR_PATH = Path(__file__).resolve().with_name('final306_public_verifier.py')
VALIDATOR_APPROVED_SHA256 = 'a0e0b737a97289ecd41273c47f7ca02740feb3053087d89023e0432aec184c6d'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def full_sha(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{40}', value):
        raise argparse.ArgumentTypeError('Require an actual full40 lowercase commit/tree SHA')
    return value


def positive(value):
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError('Require an actual positive PR number')
    if result <= 0:
        raise argparse.ArgumentTypeError('Require an actual positive PR number')
    return result


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument('--candidate-sha', required=True, type=full_sha)
    result.add_argument('--pr-number', required=True, type=positive)
    result.add_argument('--output-new-dir', required=True, type=Path,
                        help='New nonexisting external evidence directory, outside every Git checkout')
    return result


def clean_api_environment(environ):
    """Inherit normal gh authentication without printing or serializing environment."""
    require(environ.get('GH_HOST', 'github.com') in {'', 'github.com'},
            'Alternate GH_HOST is forbidden')
    require(not environ.get('GH_HTTP_UNIX_SOCKET'), 'Alternate API socket is forbidden')
    for key in ('GH_INSECURE', 'GITHUB_INSECURE', 'GIT_SSL_NO_VERIFY'):
        require(environ.get(key, '').lower() in {'', '0', 'false', 'no'},
                'Insecure TLS environment is forbidden')
    result = {key: value for key, value in environ.items()
              if key not in {'GH_DEBUG', 'DEBUG', 'GIT_TRACE', 'GIT_TRACE_CURL',
                             'GIT_CURL_VERBOSE', 'GIT_TRACE_PACKET', 'GH_HTTP_UNIX_SOCKET'}}
    result.update(GH_HOST='github.com', GH_PROMPT_DISABLED='1', NO_COLOR='1',
                  CLICOLOR='0', PYTHONDONTWRITEBYTECODE='1')
    return result


def parse_http_response(raw):
    pieces = re.split(rb'\r?\n\r?\n', raw, maxsplit=1)
    require(len(pieces) == 2, 'Actual API output did not contain HTTP headers and JSON body')
    headers, body = pieces
    match = re.match(rb'^HTTP/\S+\s+([0-9]{3})(?:\s|$)', headers)
    require(match is not None, 'Actual HTTP status line missing')
    status = int(match.group(1))
    require(status == 200, 'Actual API status was not 200: ' + str(status))
    payload = json.loads(body)
    require(isinstance(payload, dict), 'Actual API response must be a JSON object')
    return status, body, payload


def pull_binding(pull, candidate, number):
    require(pull.get('number') == number and pull.get('state') == 'open'
            and pull.get('merged') is False, 'Actual PR is not open and unmerged')
    require(pull.get('head', {}).get('sha') == candidate,
            'Actual PR head differs from candidate')
    base = pull.get('base', {})
    require(base.get('ref') == 'main'
            and base.get('repo', {}).get('full_name') == REPOSITORY,
            'Actual PR base must be the official repository main')
    return {'pull_number': number, 'candidate_sha': candidate, 'base_ref': 'main',
            'base_repository': REPOSITORY, 'base_sha': full_sha(base.get('sha')),
            'state': 'open', 'merged': False}


def commit_binding(commit, expected_sha=None):
    commit_sha = full_sha(commit.get('sha'))
    if expected_sha is not None:
        require(commit_sha == expected_sha, 'Actual commit SHA changed')
    return {'sha': commit_sha,
            'tree': full_sha(commit.get('commit', {}).get('tree', {}).get('sha'))}


def initial_bindings(candidate, number, pull, main, candidate_commit, merge_ref, merge_commit):
    pr = pull_binding(pull, candidate, number)
    base = commit_binding(main, pr['base_sha'])
    current = commit_binding(candidate_commit, candidate)
    ref_sha = full_sha(merge_ref.get('object', {}).get('sha'))
    require(merge_ref.get('ref') == 'refs/pull/' + str(number) + '/merge'
            and merge_ref.get('object', {}).get('type') == 'commit',
            'Actual PR merge ref identity changed')
    merged = commit_binding(merge_commit, ref_sha)
    require(current['tree'] == merged['tree'],
            'Actual PR merge-ref tree differs from tested candidate tree')
    parents = [full_sha(parent.get('sha')) for parent in merge_commit.get('parents', [])]
    require(len(parents) == 2 and len(set(parents)) == 2
            and set(parents) == {candidate, base['sha']},
            'Actual merge-ref must have exactly the candidate and current base parents')
    return {'pull': pr, 'main': base, 'candidate': current,
            'merge_ref_sha': ref_sha, 'merge_ref_tree': merged['tree'],
            'merge_ref_parent_sha256': sha(json.dumps(parents, separators=(',', ':')).encode())}


def stability_bindings(initial, candidate, number, final_pull, final_main):
    final_pr = pull_binding(final_pull, candidate, number)
    final_base = commit_binding(final_main, initial['main']['sha'])
    require(final_pr == initial['pull'], 'PR head/base/state moved during capture')
    require(final_base == initial['main'], 'Official main commit/tree moved during capture')
    return {'head_base_state_unchanged': True, 'main_sha_tree_unchanged': True,
            'final_pull_binding': final_pr, 'final_main_binding': final_base}


def compatibility_reader():
    raw = VALIDATOR_PATH.read_bytes()
    require(sha(raw) == VALIDATOR_APPROVED_SHA256,
            'Approved public verifier source changed; require a new static review')
    namespace = {'__name__': 'premerge_capture_compatibility_reader',
                 '__file__': str(VALIDATOR_PATH)}
    exec(compile(raw, str(VALIDATOR_PATH), 'exec'), namespace)
    reader = namespace.get('load_premerge_proof')
    require(callable(reader), 'Approved actual premerge proof reader is unavailable')
    return reader


class Capture:
    def __init__(self, arguments):
        self.arguments = arguments
        self.output = arguments.output_new_dir.resolve()
        self.created = False
        self.requests = []
        self.started_at = now()
        self.tick = time.monotonic()
        self.source_sha256 = sha(Path(__file__).read_bytes())
        self.environment = clean_api_environment(os.environ)
        self.reader = compatibility_reader()
        require(not self.output.exists(), 'Output already exists; preserve prior evidence')
        require(not any((parent / '.git').exists() for parent in self.output.parents),
                'Evidence directory must be outside every Git checkout')

    def write(self, relative, raw):
        target = self.output / relative
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with target.open('xb') as handle:
            handle.write(raw)

    def json(self, relative, value):
        self.write(relative, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

    def get(self, key, endpoint):
        require(endpoint.startswith('repos/' + REPOSITORY + '/') and '?' not in endpoint
                and '#' not in endpoint, 'Exact official API endpoint required')
        prefix = 'api/' + str(len(self.requests) + 1).zfill(2) + '-' + key
        command = ['gh', 'api', '--hostname', 'github.com', '--include', '--method', 'GET', endpoint]
        started = now()
        tick = time.monotonic()
        try:
            process = subprocess.run(command, capture_output=True, env=self.environment,
                                     timeout=60, check=False)
            stdout, stderr, exit_code = process.stdout, process.stderr, process.returncode
        except subprocess.TimeoutExpired as error:
            stdout, stderr, exit_code = error.stdout or b'', error.stderr or b'', None
        retrieved = now()
        self.write(prefix + '.http.raw', stdout)
        pieces = re.split(rb'\r?\n\r?\n', stdout, maxsplit=1)
        status_match = re.match(rb'^HTTP/\S+\s+([0-9]{3})(?:\s|$)', stdout)
        body = pieces[1] if len(pieces) == 2 else None
        if body is not None:
            self.write(prefix + '.response.raw.json', body)
        # Never persist request-debug or environment/credential strings from stderr.
        receipt = {'key': key, 'started_at_utc': started, 'retrieved_at_utc': retrieved,
                   'wall_seconds': time.monotonic() - tick, 'command': command,
                   'official_url': 'https://api.github.com/' + endpoint,
                   'actual_exit_code': exit_code,
                   'actual_http_status': int(status_match.group(1)) if status_match else None,
                   'raw_body_path': prefix + '.response.raw.json' if body is not None else None,
                   'raw_body_sha256': sha(body) if body is not None else None,
                   'raw_http_path': prefix + '.http.raw',
                   'raw_http_sha256': sha(stdout), 'stderr_bytes': len(stderr),
                   'stderr_sha256': sha(stderr), 'stderr_content_persisted': False,
                   'credentials_or_environment_logged': False,
                   'tls_verification_basis': 'Official gh HTTPS default verification; no insecure flag or alternate host/socket'}
        self.requests.append(receipt)
        self.json(prefix + '.receipt.json', receipt)
        require(exit_code == 0, 'Actual gh GET failed or timed out: ' + key)
        status, body, payload = parse_http_response(stdout)
        binding = {'path': prefix + '.response.raw.json', 'raw_sha256': sha(body),
                   'official_url': receipt['official_url'], 'http_status': status,
                   'tls_verified': True, 'retrieved_at_utc': retrieved}
        return payload, binding

    def run(self):
        self.output.mkdir(parents=True, exist_ok=False, mode=0o700)
        self.created = True
        self.write('executed-capture-source.py', Path(__file__).read_bytes())
        self.json('inputs.json', {'started_at_utc': self.started_at,
                  'candidate_sha': self.arguments.candidate_sha,
                  'pull_number': self.arguments.pr_number,
                  'repository': REPOSITORY, 'capture_helper_sha256': self.source_sha256,
                  'compatible_public_verifier_sha256': VALIDATOR_APPROVED_SHA256,
                  'status': 'CAPTURE_IN_PROGRESS_NOT_PASS', 'QA_or_merge_credit': 0})
        candidate = self.arguments.candidate_sha
        number = self.arguments.pr_number
        endpoint = 'repos/' + REPOSITORY + '/'
        pull, bp = self.get('pull', endpoint + 'pulls/' + str(number))
        pull_binding(pull, candidate, number)
        main, bm = self.get('main_commit', endpoint + 'commits/main')
        candidate_commit, bc = self.get('candidate_commit', endpoint + 'commits/' + candidate)
        merge_ref, br = self.get('merge_ref', endpoint + 'git/ref/pull/' + str(number) + '/merge')
        ref_sha = full_sha(merge_ref.get('object', {}).get('sha'))
        merge_commit, bmc = self.get('merge_ref_commit', endpoint + 'commits/' + ref_sha)
        bindings = initial_bindings(candidate, number, pull, main, candidate_commit, merge_ref, merge_commit)
        final_pull, bfp = self.get('stability_final_pull', endpoint + 'pulls/' + str(number))
        final_main, bfm = self.get('stability_final_main', endpoint + 'commits/main')
        stability = stability_bindings(bindings, candidate, number, final_pull, final_main)
        self.json('stability-receipt.json', {'observed_at_utc': now(), **stability,
                  'final_pull_response': bfp, 'final_main_response': bfm,
                  'initial_bindings': bindings, 'no_QA_or_merge_credit': True})
        require(sha(Path(__file__).read_bytes()) == self.source_sha256
                and sha(VALIDATOR_PATH.read_bytes()) == VALIDATOR_APPROVED_SHA256,
                'Capture or compatibility source changed during capture')
        proof = {'schema_version': 1, 'purpose': 'ACTUAL_PREMERGE_HEAD_BASE_AND_TREE_PROOF',
                 'repository': REPOSITORY, 'pull_number': number,
                 'candidate_sha': candidate, 'candidate_tree': bindings['candidate']['tree'],
                 'base_sha': bindings['main']['sha'], 'merge_ref_sha': bindings['merge_ref_sha'],
                 'merge_ref_tree': bindings['merge_ref_tree'], 'observed_at_utc': now(),
                 'pull': bp, 'main_commit': bm, 'candidate_commit': bc,
                 'merge_ref': br, 'merge_ref_commit': bmc}
        self.json('premerge-proof.json', proof)
        compatible = self.reader(self.output / 'premerge-proof.json', candidate,
                                 proof['candidate_tree'], number)
        require(compatible.get('actual_raw_values_recomputed') is True,
                'Approved public verifier did not revalidate captured proof')
        self.json('capture-receipt.json', {'started_at_utc': self.started_at,
                  'completed_at_utc': now(), 'wall_seconds': time.monotonic() - self.tick,
                  'status': 'ACTUAL_PREMERGE_SOURCE_PROOF_CAPTURED_AND_SCHEMA_VALIDATED',
                  'actual_GET_count': len(self.requests), 'requests': self.requests,
                  'proof_path': 'premerge-proof.json', 'proof_raw_sha256': compatible['raw_sha256'],
                  'source_head_tree_stability_verified': True,
                  'public_verifier_compatibility_verified': True,
                  'actual_candidate_QA_verified_by_this_helper': False,
                  'merged_or_deployed_by_this_helper': False,
                  'QA_or_legal_or_canonical_release_credit': 0})
        self.manifest()
        return compatible['raw_sha256']

    def manifest(self):
        self.json('artifact-sha256.json', {p.relative_to(self.output).as_posix(): sha(p.read_bytes())
                  for p in sorted(self.output.rglob('*')) if p.is_file()
                  and p.name != 'artifact-sha256.json'})


def main(argv=None):
    arguments = parser().parse_args(argv)
    capture = None
    try:
        capture = Capture(arguments)
        digest = capture.run()
        print(json.dumps({'status': 'PREMERGE_SOURCE_PROOF_CAPTURED_NOT_QA_OR_MERGE',
                          'proof': str(capture.output / 'premerge-proof.json'),
                          'proof_raw_sha256': digest, 'QA_or_merge_credit': 0}))
        return 0
    except Exception as error:
        if capture is not None and capture.created:
            capture.json('failure.json', {'observed_at_utc': now(), 'status': 'FAILED_NO_PASS',
                         'error_type': type(error).__name__, 'error': str(error),
                         'requests_completed': len(capture.requests),
                         'no_QA_merge_or_release_credit': True})
            capture.manifest()
        print('PREMERGE CAPTURE FAILED: ' + type(error).__name__ + ': ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

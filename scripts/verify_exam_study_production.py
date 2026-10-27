#!/usr/bin/env python3
"""Verify the deployed exam-study bytes, links and preserved published practice count."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    'notes/study-build.json', 'notes/study-data.js', 'notes/study.js',
    'notes/study.css', 'notes/study.html', 'notes/index.html', 'notes/notes.js',
    'notes/refresh.js', 'assets/learning-tools.js',
]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='https://woojunxnam.github.io/oddments/')
    parser.add_argument('--attempts', type=int, default=12)
    args = parser.parse_args()
    base = args.base_url.rstrip('/') + '/'
    suffix = '?exam-study=' + os.environ.get('EXPECTED_SHA', os.environ.get('GITHUB_SHA', 'verify'))
    def get(path: str) -> bytes:
        request = urllib.request.Request(base + path + suffix, headers={'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    for attempt in range(args.attempts):
        try:
            for path in ASSETS:
                assert hashlib.sha256(get(path)).digest() == hashlib.sha256((ROOT/'site'/path).read_bytes()).digest(), path
            main = get('').decode('utf-8')
            assert 'exam-study-entry' in main and 'notes/#study' in main
            assert 'notes/#refresh' in main and 'practice-expansion/?bank=plus' in main
            for path in ['', 'notes/', 'notes/book.html', 'notes/study.html', 'practice-expansion/', 'practice-expansion/research.html']:
                assert get(path).decode('utf-8').count('assets/learning-tools.js') == 1, path
            practice = json.loads(get('practice-expansion/build.json'))
            assert practice['published_question_count'] == 2176
            manifest = json.loads(get('notes/study-build.json'))
            assert manifest['stats']['concepts'] == 64 and manifest['stats']['modules'] == 16
            print('Production exam-study assets match the merged source byte-for-byte.')
            print('Six published pages retain shared navigation; practice remains 2,176 questions.')
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
            return
        except Exception as exc:
            if attempt + 1 == args.attempts:
                raise
            print(f'Attempt {attempt + 1}: deployment not synchronized: {exc}', flush=True)
            time.sleep(5)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify a single authorized generated Markdown export migration for CDTM13–16/VAX01–04.

Do not alter earlier protected inputs or previous revision/migration manifests.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from notes_revision import ROOT

OUT=ROOT/'revisions/notes/protected-migration-cdtm13-vax04.json'
BASE=ROOT/'revisions/baselines/complete-notes-cdtm0512.md'
EXPORTED=ROOT/'site/notes/complete-notes.md'
PREVIOUS=ROOT/'revisions/notes/protected-migration-cdtm0512.json'
REVISION=ROOT/'revisions/notes/2026-10-30-cdtm13-vax04.json'
def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def make()->str:
    prior=json.loads(PREVIOUS.read_text())
    assert prior['new_sha256']==sha(BASE),'The preceding generated export was not frozen correctly'
    assert prior['path']=='site/notes/complete-notes.md'
    assert sha(EXPORTED)!=sha(BASE),'Expected a changed CDTM export'
    return json.dumps(dict(
        baseline_commit='8e3c4dd1e7ec7315e6831dc1e95f8daf0cbd78f6',
        path='site/notes/complete-notes.md',
        baseline_copy='revisions/baselines/complete-notes-cdtm0512.md',
        revision_path='revisions/notes/2026-10-30-cdtm13-vax04.json',
        revision_sha256=sha(REVISION),
        previous_migration_path='revisions/notes/protected-migration-cdtm0512.json',
        previous_migration_sha256=sha(PREVIOUS),
        old_sha256=sha(BASE),new_sha256=sha(EXPORTED),
        authorization='Owner explicitly requested CDTM13-16/VAX01-04 integrated note improvement, protected original notes, all previous revisions, and existing reader history. Only this exact generated Markdown export is migrated.',
    ),ensure_ascii=False,indent=2)+'\n'

def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true')
    opt=p.parse_args()
    data=make()
    if opt.check:
        if not OUT.exists() or OUT.read_text()!=data:raise SystemExit('Stale CDTM migration manifest')
    else:OUT.write_text(data)
    print('CDTM13–16/VAX01–04 protected export: previous source and generated current bytes checked')

if __name__=='__main__':main()

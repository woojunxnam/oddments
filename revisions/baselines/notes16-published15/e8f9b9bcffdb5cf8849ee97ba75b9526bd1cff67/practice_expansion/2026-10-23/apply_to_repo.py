#!/usr/bin/env python3
"""Add this review package to a local repository, without publishing or changing its bank.

Dry run is the default. Use --apply to copy into practice_expansion/2026-10-23/.
Never commits, pushes, changes RELEASED flags, edits existing site/data, or executes hooks.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEST=Path('practice_expansion/2026-10-23')
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def apply(repo:Path,write:bool=False)->dict:
    repo=repo.resolve(strict=True)
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    guide=repo/'notes/guide.json'
    if not guide.is_file():raise ValueError('Target lacks notes/guide.json; select the oddments repository root.')
    if sha(guide)!=manifest['input_guide_sha256']:
        raise ValueError('Integrated notes changed. Rebase and review the question evidence; no files were copied.')
    parent=repo/'practice_expansion';target=repo/DEST
    if parent.is_symlink() or target.is_symlink():raise ValueError('Refusing a symlink destination.')
    if target.exists():raise ValueError(f'Destination already exists; refusing overwrite: {target}')
    entries=[]
    for name,expected in manifest['files'].items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe manifest path')
        source=ROOT/rel
        if source.is_symlink() or not source.is_file() or not source.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f'Invalid package file: {name}')
        if sha(source)!=expected:raise ValueError(f'Package checksum mismatch: {name}')
        entries.append((rel,source))
    if write:
        # Validate the entire input before creating anything. A partial write is removed on failure.
        target.mkdir(parents=True,exist_ok=False)
        try:
            for rel,source in entries:
                out=target/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,out)
            shutil.copyfile(ROOT/'MANIFEST.json',target/'MANIFEST.json')
        except Exception:
            shutil.rmtree(target)
            raise
    return {'action':'COPIED_DRAFT_PACKAGE' if write else 'DRY_RUN_NO_WRITES',
            'destination':str(target),'files':len(entries)+1,
            'existing_bank_modified':False,'website_modified':False,
            'questions_released':0,'commit_created':False,'pushed':False}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,type=Path,help='Local oddments repository root')
    p.add_argument('--apply',action='store_true',help='Actually copy the segregated draft package')
    a=p.parse_args()
    try:print(json.dumps(apply(a.repo,a.apply),ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,json.JSONDecodeError) as e:print('ERROR: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())

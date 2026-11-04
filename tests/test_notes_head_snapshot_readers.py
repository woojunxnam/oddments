"""Tree-index reuse still checks fresh native reader bytes and every bound SHA."""
import os
import subprocess

import pytest

from test_note_review_queue import repo, CENSUS
from test_notes_census_reassessment import remediation, register, switch_ledger
import note_review_queue as q
import notes_census_reassessment as census
import notes_independent_metadata as metadata
import notes_published15_closure as closure


@pytest.mark.parametrize('reader', [census.disk_reader, lambda root: lambda path, sha: closure.committed(root,path,sha)])
def test_snapshot_readers_recheck_disk_bytes_even_with_preserved_mtime(repo, reader):
    root,_,_=repo;read=reader(root);target=root/CENSUS;raw=target.read_bytes()
    before=target.stat()
    with closure.head_snapshot(root):
        assert read(CENSUS,q.raw_sha(raw))==raw
        altered=raw.replace(b'legal claim',b'other claim')
        assert len(altered)==len(raw) and altered!=raw
        target.write_bytes(altered)
        os.utime(target,ns=(before.st_atime_ns,before.st_mtime_ns))
        # Even a caller supplying the altered bytes' SHA cannot bypass HEAD.
        with pytest.raises(ValueError):read(CENSUS,q.raw_sha(altered))
        target.write_bytes(raw)
        assert read(CENSUS,q.raw_sha(raw))==raw


def test_nested_disk_reader_keeps_sha_check_before_head_check(repo, monkeypatch):
    root,_,_=repo
    def unexpected(*args):raise AssertionError('SHA mismatch must fail first')
    with closure.head_snapshot(root):
        monkeypatch.setattr(census,'head_bytes_match',unexpected)
        with pytest.raises(ValueError,match='changed reassessment snapshot'):
            census.disk_reader(root)(CENSUS,'0'*64)


@pytest.mark.parametrize('reader', [census.disk_reader, lambda root: lambda path, sha: closure.committed(root,path,sha)])
def test_snapshot_readers_reject_wrong_sha_for_exact_head_bytes(repo, reader):
    root,_,_=repo
    with closure.head_snapshot(root):
        with pytest.raises(ValueError):reader(root)(CENSUS,'0'*64)


@pytest.mark.parametrize('reader', [census.disk_reader, lambda root: lambda path, sha: closure.committed(root,path,sha)])
def test_snapshot_readers_reject_symlink_with_identical_target_bytes(repo, reader):
    root,_,_=repo;target=root/CENSUS;raw=target.read_bytes();copy=root/'copy.json'
    copy.write_bytes(raw)
    with closure.head_snapshot(root):
        target.unlink();target.symlink_to(copy)
        with pytest.raises(ValueError):reader(root)(CENSUS,q.raw_sha(raw))


def test_nested_reader_rejects_head_advance_at_outer_boundary(repo):
    root,_,_=repo;raw=(root/CENSUS).read_bytes()
    with pytest.raises(ValueError,match='HEAD advanced'):
        with closure.head_snapshot(root):
            with closure.head_snapshot(root):
                assert census.disk_reader(root)(CENSUS,q.raw_sha(raw))==raw
                q.git(root,'commit','--allow-empty','-qm','advance during validation')


def test_nested_readers_reuse_one_tree_index_without_git_show(repo, monkeypatch):
    root,_,_=repo;raw=(root/CENSUS).read_bytes();calls=[]
    original=subprocess.check_output
    def counted(command,*args,**kwargs):
        calls.append(command[3:])
        return original(command,*args,**kwargs)
    monkeypatch.setattr(subprocess,'check_output',counted)
    with closure.head_snapshot(root):
        with closure.head_snapshot(root):
            for _ in range(10):
                assert census.disk_reader(root)(CENSUS,q.raw_sha(raw))==raw
                assert closure.committed(root,CENSUS,q.raw_sha(raw))==raw
    assert [call[0] for call in calls].count('ls-tree')==1
    assert [call[0] for call in calls].count('rev-parse')==2
    assert not any(call[0]=='show' for call in calls)


def test_reader_outside_snapshot_still_checks_actual_head(repo):
    root,_,_=repo;target=root/CENSUS;raw=target.read_bytes();read=census.disk_reader(root)
    assert read(CENSUS,q.raw_sha(raw))==raw
    target.write_bytes(raw+b' ')
    with pytest.raises(ValueError):read(CENSUS,q.raw_sha(raw+b' '))


def test_tree_index_cannot_be_reused_for_another_repository(repo,tmp_path):
    root,_,_=repo;other=tmp_path/'other'
    subprocess.run(['git','clone','-q',str(root),str(other)],check=True)
    raw=(other/CENSUS).read_bytes();(other/CENSUS).write_bytes(raw+b' ')
    with closure.head_snapshot(root):
        with pytest.raises(ValueError):census.disk_reader(other)(CENSUS,q.raw_sha(raw+b' '))


def test_metadata_snapshot_preserves_result_and_all_source_bindings(remediation,monkeypatch):
    root,notes,_,_,_,_=remediation;register(remediation);switch_ledger(remediation)
    def git_bytes(root,relative,raw):return q.git(root,'show','HEAD:'+relative,binary=True)==raw
    before={}
    with monkeypatch.context()as patch:
        patch.setattr(census,'head_bytes_match',git_bytes)
        patch.setattr(metadata,'head_bytes_match',git_bytes)
        expected=metadata.load_metadata(root,notes,source_bindings=before)
    after={};calls=[];original=subprocess.check_output
    def counted(command,*args,**kwargs):
        calls.append(command[3:])
        return original(command,*args,**kwargs)
    monkeypatch.setattr(subprocess,'check_output',counted)
    assert metadata.load_metadata(root,notes,source_bindings=after)==expected
    assert after==before and after
    assert [call[0]for call in calls].count('ls-tree')==1
    assert not any(call[0]=='show'for call in calls)


def test_metadata_snapshot_rejects_head_advance(repo,monkeypatch):
    root,notes,_=repo;original=q.inventory
    def advance(*args,**kwargs):
        result=original(*args,**kwargs)
        q.git(root,'commit','--allow-empty','-qm','advance during metadata')
        return result
    monkeypatch.setattr(q,'inventory',advance)
    with pytest.raises(ValueError,match='HEAD advanced'):metadata.load_metadata(root,notes)

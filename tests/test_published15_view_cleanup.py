"""Synthetic context lifecycle only; these fixtures assert no publication proof."""
import json
from pathlib import Path
import subprocess
import sys
import stat

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=r'''
import contextlib,hashlib,json,sys,tempfile,types
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import published15_test_view as helper
base=Path(sys.argv[2]);count=int(sys.argv[3])
closure={'path':'synthetic-closure.json','raw_sha256':'0'*64}
raw=json.dumps({'closure':closure}).encode()
def sha(value):return hashlib.sha256(value).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
@contextlib.contextmanager
def fixed_view(root,binding):
    assert binding==closure
    directory=tempfile.TemporaryDirectory(prefix='synthetic-view-cleanup-')
    view=Path(directory.name)
    try:yield view,{}
    finally:
        # This must run before TemporaryDirectory's atexit finalizer removes it.
        view.chmod(0o755)
        with (base/'closed.txt').open('a')as stream:stream.write(root.name+'\n')
        directory.cleanup()
sys.modules['notes_held_sixteenth']=types.SimpleNamespace(MANIFEST='manifest.json',
    APPROVED_MIGRATIONS={('manifest.json',sha(raw)):{'closure':closure}})
sys.modules['notes_published15_closure']=types.SimpleNamespace(
    committed=lambda root,path:(root/path).read_bytes(),sha=sha,require=require,fixed_view=fixed_view)
views=[]
for index in range(count):
    root=base/str(index);root.mkdir();(root/'manifest.json').write_bytes(raw)
    view=helper.published15_root(root)
    assert helper.published15_root(root)==view
    views.append(str(view))
assert len(helper._VIEWS)==count
(base/'views.json').write_text(json.dumps(views))
'''


def run_case(helper_directory,tmp_path,count):
    return subprocess.run([sys.executable,'-c',SCRIPT,str(helper_directory),str(tmp_path),str(count)],
                          capture_output=True,text=True)


@pytest.mark.parametrize('count',[1,2])
def test_cached_views_close_before_temporary_directory_finalizers(tmp_path,count):
    result=run_case(ROOT/'tests',tmp_path,count)
    assert result.returncode==0 and result.stderr==''
    assert (tmp_path/'closed.txt').read_text().splitlines()==[str(i)for i in reversed(range(count))]
    assert all(not Path(path).exists()for path in json.loads((tmp_path/'views.json').read_text()))


def test_regression_control_reproduces_old_atexit_order_failure(tmp_path):
    before=tmp_path/'old-helper';before.mkdir()
    raw=(ROOT/'tests/published15_test_view.py').read_text()
    registration='        atexit.unregister(close)\n        atexit.register(close)\n'
    assert registration in raw
    (before/'published15_test_view.py').write_text(raw.replace(registration,'',1))
    output=tmp_path/'output';output.mkdir()
    result=run_case(before,output,1)
    assert 'FileNotFoundError'in result.stderr
    assert not (output/'closed.txt').exists()


def test_readonly_published_copy_is_mutable_without_touching_source(tmp_path):
    from published15_test_view import mutable_copytree
    source=tmp_path/'verified-view';nested=source/'nested';nested.mkdir(parents=True)
    original=nested/'evidence.json';original.write_bytes(b'EXACT HISTORICAL FIXTURE BYTES\n')
    original.chmod(0o444);nested.chmod(0o555);source.chmod(0o555)
    try:
        destination=mutable_copytree(source,tmp_path/'mutation-copy')
        copied=destination/'nested/evidence.json'
        assert copied.read_bytes()==original.read_bytes()
        assert copied.stat().st_ino!=original.stat().st_ino
        copied.write_bytes(b'INTENTIONAL TEST TAMPER\n')
        copied.unlink()
        (destination/'nested/new-case.json').write_bytes(b'new fixture')
        assert original.read_bytes()==b'EXACT HISTORICAL FIXTURE BYTES\n'
        assert stat.S_IMODE(original.stat().st_mode)==0o444
        assert stat.S_IMODE(nested.stat().st_mode)==0o555
        assert stat.S_IMODE(source.stat().st_mode)==0o555
    finally:
        source.chmod(0o755);nested.chmod(0o755);original.chmod(0o644)

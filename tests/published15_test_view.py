"""Historical guard tests use the same approved frozen15 input view as runtime."""
import atexit
import json
import shutil
import stat

_VIEWS={}


def mutable_copytree(source,destination):
    """Independent mutation fixtures copy bytes, then relax only their own mode.

    The verified published view stays read-only. copytree never hard-links the
    source, so later fixture edits cannot change historical or live evidence.
    """
    result=shutil.copytree(source,destination)
    for item in [result,*result.rglob('*')]:
        mode=item.stat().st_mode|stat.S_IWUSR
        if item.is_dir():mode|=stat.S_IXUSR
        item.chmod(mode)
    return result


def published15_root(root):
    import notes_held_sixteenth as held
    import notes_published15_closure as old
    if not (root/held.MANIFEST).exists():return root
    raw=old.committed(root,held.MANIFEST);metadata=json.loads(raw)
    approval=held.APPROVED_MIGRATIONS.get((held.MANIFEST,old.sha(raw)))
    old.require(approval is not None and metadata['closure']==approval['closure'],
                'Historical tests require the actual approved16/published15 closure, not a fallback candidate')
    key=str(root.resolve())
    if key not in _VIEWS:
        context=old.fixed_view(root,metadata['closure']);view,_=context.__enter__();_VIEWS[key]=(context,view)
        # TemporaryDirectory registers its weakref finalizer during entry.
        # Run our generator exits first so their permission restoration still
        # sees the views, then let TemporaryDirectory finish normal cleanup.
        atexit.unregister(close)
        atexit.register(close)
    return _VIEWS[key][1]


def release(root):
    item=_VIEWS.pop(str(root.resolve()),None)
    if item:item[0].__exit__(None,None,None)


def close():
    for key in reversed(list(_VIEWS)):
        context,_=_VIEWS.pop(key);context.__exit__(None,None,None)


atexit.register(close)

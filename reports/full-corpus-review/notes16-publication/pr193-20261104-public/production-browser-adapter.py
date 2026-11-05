"""Origin-only in-memory adapter for unchanged notes/refresh browser assertions.

The original CLIs do not accept --base-url. This removes only loopback server
selection; no browser assertion or actual-navigation/storage test is removed.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path('/workspace/mpje-pr193-public')
OUT=ROOT/'reports/full-corpus-review/notes16-publication/pr193-20261104-public'
ORIGIN='https://woojunxnam.github.io/oddments/'
name=sys.argv[1]
assert name in {'verify_notes_browser.py','verify_refresh_browser.py'}
path=ROOT/'scripts'/name;raw=path.read_bytes();source=raw.decode()
if name=='verify_notes_browser.py':
    before="""    if not args.inline_preview:
        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/'
    else:base=''"""
else:
    before="""    if not a.inline_preview:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(a.site)))
        threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    else:base='https://refresh-preview.invalid/'"""
after='    base='+repr(ORIGIN)
assert source.count(before)==1 and '--inline-preview'not in sys.argv
adapted=source.replace(before,after)
sha=lambda data:hashlib.sha256(data).hexdigest()
record=dict(observed_at_utc=datetime.now(timezone.utc).isoformat(),source_path='scripts/'+name,
            source_sha256=sha(raw),adapted_sha256=sha(adapted.encode()),origin=ORIGIN,
            removed_server_selection=before,replacement=after,assertions_changed=False,
            isolated_headless_context=True,real_user_browser_profile_used=False,
            limitation='Chromium headless viewport checks, not physical iOS/Android/Safari.')
(OUT/(name+'.origin-adapter.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
sys.path.insert(0,str(ROOT/'scripts'));sys.argv=[str(path),*sys.argv[2:]]
exec(compile(adapted,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})

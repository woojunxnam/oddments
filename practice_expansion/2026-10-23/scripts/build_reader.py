#!/usr/bin/env python3
"""Generate the standalone, offline draft-review screen; no remote runtime assets."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'candidates/questions.json').read_text())
# Escape all '<' inside the embedded JSON to prevent premature script-tag closure.
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
t=(ROOT/'review/reader.template.html').read_text()
assert t.count('__PAYLOAD__')==1
(ROOT/'review/practice-lab.html').write_text(t.replace('__PAYLOAD__',payload),encoding='utf-8')
print('Built review/practice-lab.html')

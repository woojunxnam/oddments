import json,hashlib
from pathlib import Path
root=Path('/workspace/independent-wave14-d');p=root/'reports/full-corpus-review/independent-phase14-d-review.json';r=json.load(open(p));idx=json.load(open('/tmp/phase14-d-claims-index.json'))
def exact(i,sid,default):
 if sid=='247-13':
  return '247 CMR '+('13.05(12)(e)' if i in [48,55] else '13.05(5)' if i in [50,54] else '13.05(6)(d)' if i in [51,53] else '13.02 Qualified nuclear pharmacist;13.03;13.05(1)-(3);13.06')
 if sid=='247-15':
  return '247 CMR '+('15.03(3)(a)1-3,(b)' if i in [63,64,67] else '15.02(1)(f)' if i in [65,69] else '15.02(1)(b)-(e);15.04(1)' if i in [66,68] else '15.04(2)' if i in [70,76] else '15.03(2)(a)' if i in [71,72,74] else '15.03(1)-(2)' if i in [73,75,86,91] else '15.02(1);15.03(3)')
 if sid=='247-20':
  return '247 CMR '+('20.02(1)' if i in [85,90] else '20.02(3)' if i in [86,91] else '20.02(5);20.07(3)' if i==87 else '20.02(4)' if i in [88,89] else '20.02(2);20.06(2)-(3)' if i in [59,61] else '20.06(2)-(3)')
 if sid=='policy-definitions':
  return 'Board Policy2025-02 II.'+('F' if i in [56,60] else 'G final paragraph' if i in [79,83] else 'G' if i in [77,84] else 'I' if i in [78,80,81,82] else 'F,G,I')
 if sid=='gov-dscsa':
  return '21 U.S.C.360eee-1 '+('(d)(1)(A)(ii)' if i in [19,26] else '(d)(2),(3)' if i in [20,23] else '(d)(1)(A)(iii)' if i in [22,24] else '(d)(4)(A)(i)-(iii)' if i in [27,29,32] else '(d)(4)(B)(ii)' if i in [30,31] else '(d)(1)(A),(d)(2)')
 if sid=='ecfr7-20261102':
  return '21 CFR '+('7.3(h)' if i in [34,40] else '7.3(k)' if i in [35,38] else '7.3(g),(j),(k)' if i==36 else '7.3(g),(j)' if i in [37,39] else '7.3(m)(3);7.49(b)' if i in [41,46] else '7.3(m)(1)' if i in [42,47] else '7.42(a)(2);7.49(b)')
 if sid=='mgl39d':return 'M.G.L.c.112 §39D(b)' if i in [85,90] else 'M.G.L.c.112 §39D(c),(e)' if i in [36,59,61] else 'M.G.L.c.112 §39D(e)'
 if sid=='ecfr310-20261102':return '21 CFR310.305(b), Adverse drug experience' if i==57 else '21 CFR310.305(b), Serious/Unexpected adverse drug experience;(c)(1)-(2)'
 if sid=='fda-smallletter':return 'FDA letter2026-08-06 p.2 eligibility and footnotes14-16' if i in [15,18] else 'FDA letter2026-08-06 pp.1-3, enumerated exemptions and reservation of other §582 requirements'
 if sid=='fda-notify':return 'Notify FDA of Illegitimate Products: Notifying FDA / Form FDA3911' if i in [28,33] else 'Notify FDA of Illegitimate Products: Notify FDA within24Hours;Terminating a Notification'
 return default
for row in r['records']:
 for f in row['legal_review']['per_choice_findings']:
  i=idx[f['option_text']]
  for a in f['authorities']:a['exact_section']=exact(i,a['source_id'],a['exact_section'])
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
target=root/'reports/full-corpus-review/phase14-d-evidence/method/phase14-d-tighten.py';target.write_bytes(Path('/tmp/phase14-d-tighten.py').read_bytes())
print(hashlib.sha256(p.read_bytes()).hexdigest())

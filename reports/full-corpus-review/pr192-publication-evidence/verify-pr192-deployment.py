import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,sys,urllib.request
merge,pages=sys.argv[1:3]
root=pathlib.Path('/tmp/mpje-pr192-final-site')
files=['index.html','practice-expansion/index.html','practice-expansion/build.json','practice-expansion/quality-review.html','notes/build.json','notes/content.js','notes/notes.js','notes/book.html','notes/complete-notes.md','notes/study-data.js','notes/refresh-data.js','generated/questions.json','generated/study_guide.json','generated/preview_allowlist.json']
def check(relative):
 expected=(root/relative).read_bytes();url='https://woojunxnam.github.io/oddments/'+relative+'?mission_sha='+merge
 req=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'MPJE-release-byte-verifier'})
 with urllib.request.urlopen(req,timeout=45) as response:actual=response.read();http=response.status
 match=actual==expected
 return {'path':relative,'url':url,'http_status':http,'expected_sha256':hashlib.sha256(expected).hexdigest(),'actual_sha256':hashlib.sha256(actual).hexdigest(),'bytes':len(actual),'result':'PASS' if match and http==200 else 'FAIL'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(check,files))
report={'pr':192,'review_head':'4c6380f14b516e6486c8ce8e8fdfcf75eb9ce7aa','merge_commit':merge,'pages_run':int(pages),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_assets':assets,'verified_public_assets':sum(a['result']=='PASS' for a in assets),'current_public_canonical_questions':397,'current_public_canonical_guides':40,'source_practice_questions':2349,'default_practice_questions':202,'new_canonical_audit_credit':0,'status':'PASS' if all(a['result']=='PASS' for a in assets) else 'FAIL'}
pathlib.Path('/tmp/pr192-deployment.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'verified':report['verified_public_assets'],'expected':len(files)}))
raise SystemExit(report['status']!='PASS')

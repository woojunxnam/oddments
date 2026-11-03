# MPJE waves11–12 / census8–9 / 독립 큐 체크포인트

기준은 PR186 candidate2a7873ea9a0061d70f970969996106ad9f76a60f이다. PR186은16exact-head CI성공(배포전production4skip별도)후merge870f1505cd49d0f861e9ebdb60fb18659a6d9eec로병합했고 Pages41679764054성공 및공개10파일byte일치를확인했다. pr186-deployment.json과PR186최종본문에해시를보존했다. 이번후속판배포증거로승계하지않는다.

## 통합 범위

Author wave11 EXP0572–0731, wave12 EXP0732–0891 각160개,총320문항/1280선지를각작업branch에서원문·모든보기·한국어설명·현재공식primary로대조했다. ExactID/hash/workercommit/evidenceSHA와실제claim/token/순차integration은작업별resultmanifest와author work-queue에있다. 원래질문객체·키·사용자history는변경하지않았다.

특정 actualdefect는 pseudoephedrine SALE01 EXP0785–0788의same-regulated-seller 사실누락이다. Seller3.6g/calendar-day와개인9g/30day를혼동해산술만으로단일키를확정하지않는다. 해당key는HOLD. All-correctSATA의문항별편집결함은법적키오류와구분했다. 기본대표15개추가보류385→370,총held78,보관2346/경고496개다. 단순숫자·반복만으로다른문항을일괄실패처리하지않았다.

Census8/9 신규40본문의340+297개주장을완전히원자열거했다. NOTE9는실제question32개의원stem/보기를읽고문항SHA로직접관련성을묶었으며상속태그를verifiedlink로격상하지않았다. Directpractice가없는주제는gap이다. FDA/USPpublicFAQ·주규정·policy·incorporation관계를구분하고미확인fulltechnical/label/child-resistant/IVscope/consent는차단한다.

K packaging/pamphlet후보는전체2unitHOLD/미적용이다. 서로다른reviewer가50claims중40개지원·10SOURCE_BLOCKED를분리했고corrections_verdictKEEP_WITH_UNIT_SOURCE_HOLDS를whole-bodyKEEP으로보지않는다. 같은실제reviewer_instance/nonblind노출을공개했다. K를독립검증완료단원이나실질본문수정에더하지않는다. 현재적용본문은여전히J이며5개단원의bounded별도검토/31개versionededit다.

새Markdownmigration은reviewannotation만갱신한다. 이전Jexport/build를보존하고semanticnotesSHA가같을때만허용하며,정확한complete-notes.md한경로·Jrawrevision·직전migration·두census증거를고정했다. Sourcehold가검색150결과한도때문에검사에서누락되지않도록chapter별필터로확인한다. Canonicalreleasegate/보호원문은변경없다.

Citationerrata의추가대상은EXP0425-C/0427-D/0428-D 3개문항/6개인용필드뿐이다. §21 large-print를첫문단이라부른오기를retainedclause의고유시작문구로정정했다. EXP0426-B는실제오기없음을전수필드검색으로확인해제외했다. 원보고서SHA불변,각원문hash와oldvalue및nestedpointer/공식원문SHA에묶었다. 기존wave6정정4개도유지하며legaltruth/key/검토credit는변경0이다.

## 독립 감사 실행 준비

Controller에--stage independent-legacy를추가했다. reports/full-corpus-review/independent-legacy-work-queue.json은authorqueue와별도purpose/jobnamespace다. Author기존jobID·lease·event이력은그대로다. 독립배정은checked_at가있고독립assessment없는실제원장집합에서정한다. 제출과Git증거에actor/session/auditor/currentrecordhash/canonicalcredit0을강제하고,독립원장에반영안된integratedjob은다음plan을막는다. 문자열alias만으로실제독립성을증명할수없어,운영상다른저자/실제freshreviewer를배정해야한다. 작성자자기검증금지와canonicalrelease별도기준을유지했다.

초기독립4×40은QUEUED이고실제감사credit는아직0이다. 첫배정은CASE0109와0162–0200,다음0201–0240/0241–0280/0281–0320이다. 범위추정으로0109를빼지않는다. Freshreviewer가실제시작할때claim하고자기actor/session과manifest를맞춘다.

## 분리 지표

- 작성자2085/2346=88.87%,미검토261개.
- 독립legacy키평가233/2346=9.93%(읽음240중미평가7제외);새canonical감사/RELEASED승격0.
- 새질문실질재작성·출판0/1800=0%;draft·안전보류와구분. 실질적용노트5개는별도.
- Authorcompleteatomiccensus172/306=56.21%,미완료134절. 현재4138atoms=3617sourcechecked+521SOURCE_BLOCKED,부분clause수0. Whole306독립완전성/법규PASS아님.
- 이전PR186공개10/10일치100%;이후속판Pages/publicorigin은PENDING이다.

419localpytestPASS,보호1781PASS,독립큐43개및citation2개회귀PASS,노트realHTTP20검사/74개개정판·원래attempt/bookmark·shuffle·320px·backup/import·20/120·Chaos10PASS. 첫localfullrun은418PASS/1FAIL:missing-review회귀가바로citationerrata를전제로하는문항을제거해올바른bindingguard가막았으며,실제errata영향없음이확인된0426을누락하는회귀로바꿨다. Missingreview를family로상속시키거나citation으로대체하지않는다. Source/QA수정후419전체재실행PASS다. 현재exacthead GitHubfullvalidator/pytest/regeneration/Pages는별도확인후에만merge한다.

## 미통합 진행과 재개

Wave13원문160개의결과가도착했지만현재2085에는미포함이다. Authorqueue의그다음배정은source원장통합후에만선택한다. NOTE10/11의완료authorcensus/evidence도미래통합자료로보존하되현재172에는미포함이다. NOTE12/13은동시비중복예약이며완료전credit0이다. Emergency-kit≤50 visual문제는후속versioned후보의별도검토대상이다. 이W4OPEN-03 narrative는기존legacyclaim-HOLD4개와다른ID(NOTE-WAVE11-W4-A-19-013)이며그4개를해소했다고세지않는다.

재개시remote최신branch와두queue/각assignment/result/sourceSHA를읽고실제lease를회복한다. 원보고서·부정감사·HOLD를보존하고currenthash의독립최종증거없이RELEASED로올리지않는다. 사용자추가승인이나보호자료업로드를이단계의전제조건으로두지않는다.

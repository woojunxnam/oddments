import json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
E=Path(__file__).resolve().parent;P=Path('/tmp/phase13-c-private-official-copyright');P.mkdir(exist_ok=True)
memos={
'src-b2350e40af92':'''공식 MA DCP가 현행 reporting page에서 연결하는 PMP Data Submission Guide v5.2 (May 2023)를 실제 읽었다. 법적 위임 원문은 105 CMR700.012(A)이고 안내서의 제품/기술 필드는 그 집행 절차다. §1–2: II–V 및 gabapentin, MA 수령인에게 보내는 비거주 약국도 보고한다. 조제준비와 실제 판매/배송일은 구별한다. 미조제기간에는 waiver가 없으면 zero report가 필요하다. §4.4 zero filing, §5–6 record acceptance와 file upload를 구별하며 fatal record를 수정해 다시 제출해야 한다. Appendix B pp67–69: 실제 수령 customer와 patient는 다를 수 있고, 유효한 정부발급ID를 매번 확인한다. SSN은 customer ID로 쓰지 않는다. Serious hardship 사유를 기록하고 이름·주소·서명 및 cust signed rx 필드를 사용한다. 배송에 customer ID 수집 예외가 있으나 내부 추적을 유지하고 DSP17은 환자 실제 인도일이다. Appendix E: no-dispensing waiver의 조건을 지켜야 한다. Appendix F pp81–82: fatal unaccepted record는 new로, 기존 accepted data는 revise/void를 구별한다. 이 메모는 직접 작성한 사실검토이며 안내서의 화면·예제·문장 원문을 재배포하지 않는다. 표기된 오래된 XDEA field는 현행 법적 의무의 증거로 채택하지 않았다.''',
'nabp-sample':'''NABP 공개 MPJE Sample Questions 1쪽을 직접 읽었다. 보호된 Pre-MPJE가 아닌 공개 format 안내다. 단일 선택, 복수 선택, 순서 배열 형식을 설명하고 sample이 시험 content-area를 대표한다고 주장하지 않는다. 이 감사는 형식 확인만 사용하며 샘플 문항의 문구나 정답을 복제하지 않는다. 원문 PDF와 추출문은 저작권 보호를 위해 로컬 private 임시 경로에 두고 SHA만 공개한다.''',
'nabp-format':'''NABP 공개 Take the MPJE 페이지의 형식 안내를 직접 읽었다. 120 selected-response 문항, 적응형, 2.5시간이라는 현재 안내를 확인했다. 이 내용은 법률권위가 아니라 공개 시험형식 확인이다. 문항 텍스트를 복제하지 않았다.''',
'nabp-competency':'''NABP 공개 competency 페이지를 직접 읽었다. 현재 outline과 2027-03-01 이후 새 content outline을 구별하는 공지를 확인했다. licensure/personnel, practice, dispensing, operations 및 permitted/mandated product selection 같은 공개 학습범위만 검토에 사용했다. 보호된 시험문제는 읽지 않았다.'''}
for sid,memo in memos.items():
 mp=E/(sid+'.meta.json');m=json.loads(mp.read_text())
 for field in ['raw_path','text_path']:
  old=Path(m[field]);new=P/old.name;shutil.move(str(old),new);m[field]=str(new)
 memo_path=E/(sid+'.memo.txt');memo_path.write_text(memo+'\n');m.update(public_raw_redistribution=False,public_evidence_mode='original authored factual memo; restricted raw retained privately, SHA only',memo_path=str(memo_path),memo_sha256=hashlib.sha256(memo_path.read_bytes()).hexdigest(),read_at=datetime.now(timezone.utc).isoformat(),document_identity_confirmed=True)
 mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

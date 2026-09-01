# Generated Site Data

이 directory의 파일은 canonical JSON registry에서 생성된 tracked deterministic output입니다. `python scripts/generate_artifacts.py --write`로 재생성하고 hand edit하지 마십시오. `validate_all.py`와 CI가 drift를 검사합니다.

Tracked `questions.json`은 GitHub Pages용 production artifact이므로 `verification_status`와 `lifecycle_status`가 모두 `RELEASED`인 문항만 포함합니다. 개발 fixture가 필요하면 별도 출력 경로에 `python scripts/build_site_data.py --include-fixtures --output <path>`를 명시적으로 실행하십시오.

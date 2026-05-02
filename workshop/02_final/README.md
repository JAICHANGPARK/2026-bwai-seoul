# Workshop Final

핸즈온 최종 완성본입니다. 모든 시나리오가 등록되어 있으며, 시작 코드에서 막혔을 때 비교용 참고 코드로 사용할 수 있습니다.

## 실행

```bash
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

주요 완성 흐름:

```bash
bash run.sh --scenario resume --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획자" --hires 2

bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
bash run.sh --scenario publication_offer_email
bash run.sh --scenario contract_negotiation
bash run.sh --scenario contract_draft
bash run.sh --scenario story_revision
bash run.sh --scenario marketing_copy --tasks 10
```

Windows PowerShell에서는 `bash run.sh` 대신 `.\run.ps1`을 사용합니다.

단편소설 출간 실습은 `심사/선정 -> 출간 의향 확인 -> 계약 조건 협의 -> 계약서 초안 작성 -> 개정 작업 -> 마케팅 문구` 순서입니다. 오퍼/계약/개정 단계는 선정 결과에서 작품 수를 자동 추론하고, 마케팅 단계는 기본 10개 agent가 선정작을 순환 배정받아 여러 문구 변형을 만듭니다. 계약서 초안은 워크샵용 산출물이며, 실제 법적 계약서로 사용하지 않습니다.

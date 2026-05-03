# Workshop Final

핸즈온 최종 완성본입니다. 모든 시나리오가 등록되어 있으며, 시작 코드에서 막혔을 때 비교용 참고 코드로 사용할 수 있습니다.

## 실행

```bash
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

`code` 기본 10개 agent에는 Dart가 포함됩니다.

Windows PowerShell:

```powershell
uv sync
Invoke-RestMethod http://127.0.0.1:1234/v1/models
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

`Invoke-RestMethod`가 실패하면 LM Studio Local Server가 켜져 있는지, 포트가 `1234`인지 먼저 확인하세요.

Ollama를 쓰는 경우에는 모든 실행 명령에 `--port 11434 --model "gemma4:e2b"`를 붙입니다. 모델명이 다르면 `ollama list`에 표시된 이름을 사용합니다.

## 최종 실행 순서

**0. 기본 실행**

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

**1. 편집자 채용**

```bash
bash run.sh --scenario resume --topic "도서 출판사 소설 기획편집자" --tasks 10
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획편집자" --tasks 10
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획편집자" --hires 2
```

**2. 마케터 채용**

```bash
bash run.sh --scenario marketer_resume --topic "도서 출판사 북 마케터" --tasks 10
bash run.sh --scenario marketer_interview_review --topic "도서 출판사 북 마케터" --tasks 10
bash run.sh --scenario marketer_hiring_decision --topic "도서 출판사 북 마케터" --hires 2
```

**3. 선택 확장: 실제 멀티턴 면접**

```bash
bash run.sh --scenario interview_dialogue --topic "도서 출판사 소설 기획편집자" --tasks 3
bash run.sh --scenario hiring_decision_from_dialogue --topic "도서 출판사 소설 기획편집자" --hires 2
```

`interview_dialogue`는 후보자 1명마다 질문/답변을 여러 번 생성하므로 처음에는 `--tasks 3`으로 확인하는 편이 좋습니다.

**4. 선택 확장: 장편 소설 기획**

```bash
bash run.sh --scenario novel_writing --topic "도시 미스터리 장편소설 기획" --tasks 10
```

**5. 단편소설 출판 흐름**

```bash
bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
bash run.sh --scenario publication_offer_email
bash run.sh --scenario contract_negotiation
bash run.sh --scenario contract_draft
bash run.sh --scenario story_revision
bash run.sh --scenario marketing_copy --tasks 10
```

Windows PowerShell에서는 `bash run.sh` 대신 `.\run.ps1`을 사용합니다.

초반 채용 실습에서는 소설 기획편집자와 북 마케터를 함께 채용합니다. `interview_dialogue`는 이력서를 바탕으로 질문과 답변을 번갈아 생성하는 실제 멀티턴 면접으로 실행됩니다. 단편소설 출간 실습은 `심사/선정 -> 출간 의향 확인 -> 계약 조건 협의 -> 계약서 초안 작성 -> 개정 작업 -> 마케팅 문구` 순서입니다. 심사/오퍼/계약/개정 단계는 채용된 편집자 결정 결과를 함께 참고하고, 오퍼/계약/개정 단계는 선정 결과에서 작품 수를 자동 추론합니다. 마케팅 단계는 기본 10개 agent가 선정작을 순환 배정받아 여러 문구 변형을 만들며, 채용된 마케터 결정 결과도 함께 참고합니다. 계약서 초안은 워크샵용 산출물이며, 실제 법적 계약서로 사용하지 않습니다.

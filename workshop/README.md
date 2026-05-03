## 폴더 구조

먼저 [03_labs/README.md](03_labs/README.md)를 열고, [01_starter](01_starter) 폴더에서 단계별로 실습하면 됩니다. 막히면 [02_final](02_final)을 참고 코드로 확인하세요.

- `01_starter/`: 시작 코드입니다. `translate`, `code`를 바로 실행 가능하고, 핸즈온 중 `demo/scenarios.py`에 시나리오를 하나씩 추가합니다.
- `02_final/`: 최종 완성본입니다. 모든 시나리오가 등록되어 있습니다.
- `03_labs/`: `01_starter`에서 `02_final`까지 단계별로 구현하는 실습 문서입니다.

## 준비물

- **macOS + Terminal** 또는 **Windows + PowerShell**
- 코드 수정을 위한 **Visual Studio Code 또는 Google Antigravity**: 자세한 설치 방법은 [코드 편집기 설치 가이드](../docs/17-code-editor-setup.md)를 참고하세요.
- Python 패키지 관리를 위한 **[uv](https://github.com/astral-sh/uv)**
- **LM Studio** 또는 **Ollama** 로컬 OpenAI 호환 서버
- Intel Mac 사용자는 LM Studio 대신 **Ollama**를 사용합니다. 자세한 준비는 [Intel Mac 사용자 사전 준비 가이드](../docs/18-intel-mac-prep.md)를 참고하세요.

> [!NOTE]
> 실행 스크립트의 기본 포트는 `1234`입니다. LM Studio의 일반적인 로컬 서버 포트와 맞습니다.
> Ollama는 OpenAI 호환 API 포트가 `11434`입니다. Ollama 사용자는 `--port 11434 --model "모델명"`을 붙여 실행합니다.

## 빠른 시작

**1. 의존성 설치**

시작 코드는 `workshop/01_starter` 폴더에서 실행합니다.

```bash
cd 01_starter
uv sync
```

**2. 로컬 OpenAI 호환 서버 실행**

대부분의 환경에서는 LM Studio가 가장 간단합니다.

1. LM Studio에서 Gemma 4 모델을 다운로드합니다.
2. OpenAI 호환 로컬 서버를 켭니다.
3. 서버 주소를 `http://127.0.0.1:1234`로 유지합니다.

Ollama를 쓰는 경우:

```bash
ollama pull gemma4:e2b
curl http://127.0.0.1:11434/v1/models
```

Ollama 앱이 서버를 자동 실행하지 않는 환경에서는 별도 터미널에서 `ollama serve`를 먼저 실행합니다. `address already in use`가 나오면 이미 서버가 켜진 상태입니다.

**3. macOS에서 데모 실행**

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

이 명령은 macOS Terminal 창을 여러 개 엽니다. 위쪽에는 대시보드가 열리고, 아래쪽에는 오케스트레이터와 여러 전문 에이전트 창이 배치됩니다.

Ollama 포트 `11434`를 쓰는 경우에는 모델명을 함께 지정하고 작은 task 수로 시작하세요.

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 3 --port 11434 --model "gemma4:e2b"
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 3 --port 11434 --model "gemma4:e2b"
```

**4. Windows PowerShell에서 데모 실행**

스크립트 실행 정책 때문에 막히면 현재 PowerShell 창에서만 임시로 허용합니다.

```powershell
cd .\01_starter
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

그 다음 실행합니다.

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

이 명령은 별도의 PowerShell 창들을 엽니다. 하나는 대시보드, 하나는 오케스트레이터, 나머지는 각 Gemma 4 인스턴스 역할을 하는 전문 에이전트입니다.

## reasoning 옵션

기본값은 `--reasoning off`입니다. Gemma 4 모델의 thinking/reasoning을 켜서 비교하고 싶을 때만 `--reasoning on`을 붙입니다.

macOS:

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10 --reasoning on
```

Windows PowerShell:

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10 --reasoning on
```

`--reasoning on`은 모델이 지원하는 경우 thinking/reasoning을 요청합니다. 이 경우 답변 품질이나 복잡한 판단은 좋아질 수 있지만, 생성 시간이 길어지고 토큰 사용량이 늘어 처리량이 낮아질 수 있습니다. 형식이 엄격한 JSON/Markdown 시나리오에서는 reasoning 출력이 서버 설정에 따라 본문에 섞이면 결과 파싱이 불안정해질 수 있으므로 기본값은 `off`로 둡니다.

## Windows 노트북 사용자 가이드

Windows에서는 `bash run.sh` 대신 PowerShell용 `run.ps1`을 사용합니다. WSL2는 필요하지 않습니다.

**1. 로컬 모델 서버 준비**

가장 간단한 경로는 LM Studio입니다.

1. LM Studio에서 Gemma 4 모델을 다운로드합니다.
2. OpenAI 호환 로컬 서버를 켭니다.
3. 서버 주소가 `http://127.0.0.1:1234`인지 확인합니다.

PowerShell에서 서버가 켜져 있는지 확인하려면:

```powershell
Invoke-RestMethod http://127.0.0.1:1234/v1/models
```

**2. uv 설치 확인**

PowerShell에서 확인합니다.

```powershell
uv --version
```

`uv`가 없다면 [uv 설치 가이드](../docs/16-uv-setup.md)의 Windows PowerShell 섹션을 먼저 따라가면 됩니다.

**3. 워크샵 의존성 설치**

PowerShell에서 이 저장소의 `workshop/01_starter` 폴더로 이동한 뒤 실행합니다.

```powershell
cd .\workshop\01_starter
uv sync
```

**4. 데모 실행**

처음 실행할 때 스크립트 실행 정책 때문에 막히면 현재 PowerShell 창에서만 임시 허용합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

LM Studio 기본 포트 `1234`를 쓰는 경우:

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 5
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 5
```

Ollama 포트 `11434`를 쓰는 경우:

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 3 --port 11434 --model "gemma4:e2b"
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 3 --port 11434 --model "gemma4:e2b"
```

실행하면 PowerShell 창이 여러 개 열립니다.

- `Dashboard`: 전체 처리량과 에이전트 상태
- `Orchestrator`: 작업을 나누고 결과를 모으는 프로세스
- 나머지 창들: 각 Gemma 4 인스턴스 역할을 하는 전문 에이전트

노트북 성능이 낮거나 창이 너무 많이 열리면 `--tasks 3` 또는 `--tasks 5`부터 시작하세요.

**Windows 문제 해결**

- `.venv not found`가 나오면 실행 중인 폴더(`workshop/01_starter` 또는 `workshop/02_final`)에서 `uv sync`를 먼저 실행합니다.
- `Connection refused` 또는 API 연결 오류가 나오면 LM Studio 로컬 서버가 켜져 있는지, 포트가 `1234`인지 확인합니다. 최신 `run.ps1`은 서버나 모델을 확인하지 못하면 agent 창 10개를 띄우기 전에 멈춥니다.
- 모델 이름 오류가 나오면 `Invoke-RestMethod http://127.0.0.1:1234/v1/models`로 모델 ID를 확인한 뒤 `.\run.ps1 ... --model "모델ID"`를 붙입니다. `run.ps1`은 기본값일 때 가능한 경우 첫 모델 ID를 자동으로 사용합니다.
- PowerShell 창이 여러 개 뜬 뒤 모든 agent가 같은 `[ERROR]`를 보이면 한 창의 에러 첫 줄을 확인합니다. 서버 옵션 호환 문제는 코드가 자동으로 최소 요청으로 재시도하고, 모델/포트 문제는 `--port` 또는 `--model`을 명시해야 합니다.
- Ollama 사용자는 `Invoke-RestMethod http://127.0.0.1:11434/v1/models`로 서버를 확인하고, `ollama list`에 보이는 모델명을 `--model`에 그대로 넣습니다.
- 한글이나 이모지가 깨지면 Windows Terminal 또는 최신 PowerShell을 사용합니다. `run.ps1`은 실행 창에서 UTF-8 출력을 자동으로 설정합니다.
- LM Studio 로그에 `GET /metrics` 오류가 반복되면 최신 코드에서는 기본적으로 발생하지 않아야 합니다. 대시보드는 agent가 쓰는 로컬 metrics 파일을 사용하고, 서버 `/metrics` 폴링은 꺼져 있습니다.

## Ollama 사용자 가이드

Ollama는 기본 API 포트가 `11434`입니다. 이 워크샵 코드는 OpenAI 호환 `chat/completions` API를 사용하므로 Ollama의 OpenAI 호환 주소인 `http://127.0.0.1:11434/v1`에 연결합니다.

핵심 규칙:

- LM Studio: `--port` 생략 가능. 기본값 `1234`
- Ollama: `--port 11434` 필요
- Ollama: `--model`에 `ollama list`에 표시되는 모델명 지정

macOS:

```bash
ollama pull gemma4:e2b
curl http://127.0.0.1:11434/v1/models

cd workshop/01_starter
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 5 --port 11434 --model "gemma4:e2b"
```

Windows PowerShell:

```powershell
ollama pull gemma4:e2b
Invoke-RestMethod http://127.0.0.1:11434/v1/models

cd .\workshop\01_starter
uv sync
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 5 --port 11434 --model "gemma4:e2b"
```

노트북 성능이 낮으면 처음에는 `--tasks 3` 또는 `--tasks 5`로 시작합니다. 모델명이 다르면 `gemma4:e2b` 대신 `ollama list`에 표시된 이름을 사용합니다. Ollama의 OpenAI 호환 API는 [공식 문서](https://docs.ollama.com/openai) 기준으로 `http://localhost:11434/v1/` 형식을 사용합니다.

## 주요 시나리오 흐름

단계별로 시나리오를 추가하면서 진행하는 핸즈온 운영안은 [03_labs/README.md](03_labs/README.md)를 참고하세요.

핸즈온에서는 먼저 LM Studio 앱에서 user message만으로 이력서 1개를 직접 생성해보고, 이어서 system instruction을 사용해 시나리오 코드 초안을 생성해봅니다. 이후 같은 프롬프트를 코드의 멀티 에이전트 시나리오로 확장하고, 이력서/면접/채용 결정 흐름을 단계적으로 추가합니다.

### 시나리오 이름표

`--scenario` 뒤에 넣는 영어 이름은 아래 의미로 사용합니다.

| 실행 이름 | 한국어 의미 | 주 입력 및 산출물 |
| --- | --- | --- |
| `translate` | 기본 번역 그리드 | `--topic` 문장을 여러 언어로 번역 |
| `code` | 기본 코드 갤러리 | `--topic` 문제를 Python, JavaScript, Dart 등 여러 언어 코드로 생성하고 `code_outputs/`에 저장 |
| `resume` | 소설 기획편집자 이력서 생성 | `--topic` 직무 기준으로 `resumes/` 생성 |
| `interview_review` | 이력서 기반 면접 평가 | `resumes/`를 읽어 `interview_reviews/` 생성 |
| `hiring_decision` | 편집자 최종 채용 결정 | `interview_reviews/`를 읽어 `hiring_decisions/` 생성 |
| `interview_dialogue` | 이력서 기반 실제 멀티턴 면접 실행 | `resumes/`를 읽어 질문/답변 턴을 번갈아 실행하고 `interview_dialogues/` 생성 |
| `hiring_decision_from_dialogue` | 면접 대화록 기반 채용 결정 | `interview_dialogues/`를 읽어 `hiring_decisions_from_dialogue/` 생성 |
| `marketer_resume` | 북 마케터 이력서 생성 | `--topic` 직무 기준으로 `marketer_resumes/` 생성 |
| `marketer_interview_review` | 마케터 이력서 기반 면접 평가 | `marketer_resumes/`를 읽어 `marketer_interview_reviews/` 생성 |
| `marketer_hiring_decision` | 마케터 최종 채용 결정 | `marketer_interview_reviews/`를 읽어 `marketer_hiring_decisions/` 생성 |
| `novel_writing` | 장편 소설 기획 패키지 생성 | `--topic` 기준으로 `novel_outputs/` 생성 |
| `short_story_writing` | 단편소설 투고작 생성 | `--topic` 기준으로 `short_stories/` 생성 |
| `story_review_selection` | 단편소설 심사 및 선정 | `short_stories/`와 `hiring_decisions/`를 읽어 `story_selections/` 생성 |
| `publication_offer_email` | 선정작 출간 의향 확인 메일 | `story_selections/`, `short_stories/`, `hiring_decisions/`를 읽어 `publication_offer_emails/` 생성 |
| `contract_negotiation` | 계약 조건 협의 메모 | `publication_offer_emails/`와 선정작 맥락을 읽어 `contract_negotiations/` 생성 |
| `contract_draft` | 출간 계약서 초안 작성 | `contract_negotiations/`와 선정작 맥락을 읽어 `contract_drafts/` 생성 |
| `story_revision` | 선정작 개정 원고 작성 | `story_selections/`, `short_stories/`, `contract_drafts/`를 읽어 `revised_stories/` 생성 |
| `marketing_copy` | 출간 마케팅 문구 생성 | `revised_stories/`, `contract_drafts/`, `marketer_hiring_decisions/`를 읽어 `marketing_copy/` 생성 |
| `publication_contract` | 이전 이름 호환용 별칭 | 현재는 `contract_draft`와 같은 시나리오로 실행 |

**0. 기본 실행**

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

**1. 이력서 생성 및 면접 평가 흐름**

```bash
bash run.sh --scenario resume --topic "도서 출판사 소설 기획편집자" --tasks 10
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획편집자" --tasks 10
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획편집자" --hires 2

bash run.sh --scenario marketer_resume --topic "도서 출판사 북 마케터" --tasks 10
bash run.sh --scenario marketer_interview_review --topic "도서 출판사 북 마케터" --tasks 10
bash run.sh --scenario marketer_hiring_decision --topic "도서 출판사 북 마케터" --hires 2
```

`resume`은 가상의 소설 기획편집자 이력서를 `resumes/`에 저장합니다. `interview_review`는 저장된 이력서를 읽어 면접관 평가를 `interview_reviews/`에 저장하고, `hiring_decision`은 평가 결과를 모아 최종 채용 결정을 `hiring_decisions/`에 저장합니다. 같은 방식으로 `marketer_resume`, `marketer_interview_review`, `marketer_hiring_decision`은 북 마케터 채용 결과를 `marketer_hiring_decisions/`에 저장합니다.

면접 대화 시뮬레이션까지 확장하려면 아래 흐름을 추가로 실행합니다.

```bash
bash run.sh --scenario interview_dialogue --topic "도서 출판사 소설 기획편집자" --tasks 3
bash run.sh --scenario hiring_decision_from_dialogue --topic "도서 출판사 소설 기획편집자" --hires 2
```

`interview_dialogue`는 이력서를 바탕으로 질문과 답변을 번갈아 생성하는 실제 멀티턴 면접 결과를 `interview_dialogues/`에 저장하고, `hiring_decision_from_dialogue`는 그 면접 결과를 근거로 채용 결정을 생성합니다. 후보자 1명마다 여러 번 호출되므로 처음에는 `--tasks 3`으로 확인하는 편이 좋습니다.

**2. 단편소설 공모 흐름**

```bash
bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
bash run.sh --scenario publication_offer_email
bash run.sh --scenario contract_negotiation
bash run.sh --scenario contract_draft
bash run.sh --scenario story_revision
bash run.sh --scenario marketing_copy --tasks 10
```

단편소설 흐름은 실제 출판사 업무에 가깝게 `심사/선정 -> 출간 의향 확인 -> 계약 조건 협의 -> 계약서 초안 작성 -> 개정 작업 -> 마케팅 문구` 순서로 구성했습니다. `story_review_selection`, `publication_offer_email`, `contract_negotiation`, `contract_draft`, `story_revision`은 초반에 생성한 `hiring_decisions/`를 함께 읽어 채용된 편집팀의 관점을 반영합니다. 오퍼/계약/개정 단계는 선정작 수를 자동으로 추론하므로 `--select 3 --tasks 3`를 반복해서 넣지 않아도 됩니다. `marketing_copy`는 선정작 수와 1:1로 묶지 않고, 기본 10개 agent가 선정작과 채용된 마케터 팀의 관점을 순환 배정받아 온라인 서점, SNS, 보도자료 등 여러 문구 변형을 생성합니다.

`story_revision`은 `story_review_selection`의 선정 보고서, `short_story_writing`의 원본 단편 원고, `contract_draft`의 출간 조건 맥락, 편집자 최종 채용 결정 맥락을 함께 읽고 개정 원고를 `revised_stories/`에 저장합니다. 선정 보고서의 `선정작` 섹션에서 작품 파일명을 먼저 추출하고 중복을 제거한 뒤 agent별로 하나씩 배정하므로, 같은 작품이 여러 번 개정되지 않습니다. `marketing_copy`는 개정 원고, 계약서 초안, 마케터 최종 채용 결정 맥락을 바탕으로 온라인 서점, SNS, 뉴스레터, 보도자료용 문구를 생성합니다.

## 새 시나리오 추가

핸즈온에서는 `01_starter/demo/scenarios.py`를 수정합니다. 전체 단계별 코드는 [03_labs/README.md](03_labs/README.md)에 정리되어 있습니다.

```python
def make_my_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"Agent {i+1}",
            "emoji": "🎯",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": "주어진 주제를 X 스타일로 처리하세요: {topic}",
        }
        for i in range(n)
    ]

MY_PLAN = {
    "system": '각 agent별 "name"과 "instruction"을 가진 JSON 배열만 출력하세요.',
    "user": '주제: "{topic}". Agent 목록: {agent_list}.',
}

MY_SYSTEM = "당신은 ... 입니다. 반드시 ... 형식으로만 출력하세요."

def my_card(agent, result, task=None):
    return f"<div>{result}</div>"

SCENARIOS["my_scenario"] = {
    "make_agents": make_my_agents,
    "plan": MY_PLAN,
    "system_prompt": MY_SYSTEM,
    "render_card": my_card,
    "title": "My Scenario",
    "default_n": 10,
    "direct_plan": True,
}
```

macOS에서는 이렇게 실행합니다.

```bash
bash run.sh --scenario my_scenario --topic "내 주제"
```

Windows PowerShell에서는 이렇게 실행합니다.

```powershell
.\run.ps1 --scenario my_scenario --topic "내 주제"
```

## 참고

본 워크숍 코드는 [google-gemma/cookbook](https://github.com/google-gemma/cookbook) 리포지토리 코드를 참고, 활용하였습니다.

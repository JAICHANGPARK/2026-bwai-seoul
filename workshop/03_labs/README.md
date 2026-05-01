# BWAI Seoul Workshop Hands-on Guide

이 문서는 `workshop/01_starter`에서 시작해 시나리오를 하나씩 추가하고, `workshop/02_final`의 최종 완성본까지 도달하는 진행안을 정리합니다.

## 진행 방식

핸즈온의 핵심 흐름은 아래와 같습니다.

```text
LM Studio 앱에서 이력서 1개 직접 생성
-> LM Studio 앱에서 system instruction으로 시나리오 코드 초안 생성
-> 기본 translate 실행
-> 새 시나리오 코드 추가
-> 실행
-> Markdown 산출물 확인
-> 다음 시나리오가 이전 산출물을 입력으로 사용
```

참석자는 [01_starter](../01_starter) 폴더에서 실습합니다. `01_starter`는 `translate` 시나리오만 바로 실행 가능하며, `orchestrator.py`, `specialist.py`, `dashboard.py`, `utils.py`, `run.sh`, `run.ps1`은 완성본과 동일하게 유지합니다. 실습에서는 주로 `01_starter/demo/scenarios.py`를 편집합니다.

macOS:

```bash
cd 01_starter
uv sync
```

Windows PowerShell:

```powershell
cd .\01_starter
uv sync
```

강사용 정답 코드는 [02_final](../02_final) 폴더에 있습니다.

이하 실행 명령은 별도 언급이 없으면 모두 `workshop/01_starter` 폴더 안에서 실행합니다.

## Starter 기준

`01_starter/demo/scenarios.py`에는 아래 요소가 이미 들어 있다고 가정합니다.

- `_COLORS`, `_LANG_NAMES`, `_LANG_EMOJIS`
- `make_translate_agents`
- `TRANSLATE_SYSTEM`
- `TRANSLATE_PLAN`
- `translate_card`
- Markdown 렌더링 helper와 각 Markdown용 card renderer
  - `resume_card`
  - `interview_review_card`
  - `interview_dialogue_card`
  - `hiring_decision_card`
  - `short_story_card`
  - `story_review_selection_card`
  - `story_revision_card`
  - `publication_offer_email_card`
  - `contract_negotiation_card`
  - `publication_contract_card`
  - `marketing_copy_card`
- `SCENARIOS`에는 처음에는 `translate`만 등록

처음 registry는 아래처럼 둡니다.

```python
SCENARIOS = {
    "translate": {
        "make_agents": make_translate_agents,
        "plan": TRANSLATE_PLAN,
        "system_prompt": TRANSLATE_SYSTEM,
        "render_card": translate_card,
        "title": "Translation Grid",
        "default_n": 10,
    },
}
```

## Step 0. LM Studio 앱에서 이력서 1개 직접 생성

목표는 코드로 들어가기 전에 "좋은 프롬프트 하나가 어떤 구조화된 결과를 만드는지"를 먼저 확인하는 것입니다. 이 단계에서는 `run.sh`나 `run.ps1`을 쓰지 않고, LM Studio 앱의 채팅 화면에서 직접 프롬프트를 실행합니다.

LM Studio 앱에서 Gemma 4 모델을 선택한 뒤 아래 프롬프트를 그대로 입력합니다.

```text
당신은 출판/콘텐츠 업계 전문 이력서 작성자입니다.

도서 출판사에서 일할 "소설 기획자, 편집자" 포지션에 지원하는 가상의 한국인 후보자 이력서 1개를 작성하세요.

조건:
- 출력은 한국어 Markdown만 사용합니다.
- 설명이나 코드블록은 쓰지 않습니다.
- 실제 개인정보, 실제 전화번호, 실제 이메일, 실제 회사의 비공개 정보는 쓰지 않습니다.
- 이름, 회사, 프로젝트, 성과 지표는 모두 허구로 만듭니다.
- 일반 IT 기획자가 아니라 소설/문학/출판 기획 직무에 맞게 작성합니다.
- 후보자의 경력, 담당 장르, 출판사 유형, 프로젝트, 성과, 사용 도구가 구체적으로 드러나야 합니다.

반드시 아래 구조를 따르세요.

# [가상의 한국인 이름] - 도서 출판사 소설 기획자 이력서
## 프로필
## 핵심 역량
## 경력
## 주요 기획 프로젝트
## 성과 지표
## 사용 도구
## 학력 및 자격
## 포트폴리오 요약
```

확인할 것:

- 결과가 Markdown 구조를 지키는지
- 직무가 "소설 기획자"에 맞게 구체화되는지
- 실제 개인정보가 들어가지 않는지
- 같은 프롬프트를 다시 실행하면 다른 후보자가 나오는지

이 프롬프트는 이후 Step 3의 `RESUME_SYSTEM`과 `make_resume_agents()`로 나누어 들어갑니다. 즉, 앱에서 직접 입력한 단일 프롬프트를 코드에서는 여러 agent가 병렬로 실행하도록 바꾸는 것이 핵심입니다.

## Step 1. LM Studio 앱에서 system instruction으로 시나리오 코드 초안 생성

목표는 콘텐츠 생성 프롬프트와 코드 생성 프롬프트의 차이를 비교하는 것입니다. 이력서 1개를 만드는 Step 0은 user message만으로 충분하지만, `scenarios.py`에 붙여 넣을 코드 초안을 만들 때는 system instruction으로 역할과 출력 형식을 고정하는 편이 안정적입니다.

LM Studio 앱에서 system instruction 영역이 있다면 아래 내용을 넣습니다.

```text
당신은 Python 워크샵용 코드 생성 도우미입니다.
사용자는 multi-agent demo의 scenarios.py에 추가할 새 시나리오 코드를 요청합니다.

규칙:
- Python 코드만 출력합니다.
- 설명, 마크다운 코드블록, 불필요한 주석은 출력하지 않습니다.
- 아래 구성요소를 반드시 포함합니다.
  1. make_xxx_agents(n) 함수
  2. XXX_SYSTEM 문자열
  3. XXX_PLAN 딕셔너리
  4. SCENARIOS["xxx"] 등록 코드
- 기존 helper인 _COLORS와 resume_card는 이미 있다고 가정합니다.
- 출력 코드는 demo/scenarios.py에 그대로 붙여 넣을 수 있어야 합니다.
- 결과 Markdown 파일을 저장해야 하는 시나리오에는 save_markdown, markdown_dir를 포함합니다.
```

그 다음 user message input에는 아래 요청을 넣습니다.

```text
이력서 생성 시나리오를 만들어주세요.

요구사항:
- 시나리오 이름: resume
- agent 수 기본값: 10
- 각 agent는 도서 출판사 소설 기획자/편집자 지원자 이력서 1개를 생성합니다.
- 결과는 한국어 Markdown입니다.
- 저장 폴더는 resumes 입니다.
- 카드 렌더러는 resume_card를 사용합니다.
- 파일명 예시는 01_resume_01.md 입니다.
- 실제 개인정보, 실제 전화번호, 실제 이메일, 실제 회사의 비공개 정보는 만들지 않습니다.
- 이름, 회사, 프로젝트, 성과 지표는 모두 허구로 만듭니다.
- 일반 IT 기획자가 아니라 소설/문학/출판 기획 직무에 맞게 작성합니다.
- direct_plan: True를 사용합니다.
```

확인할 것:

- Python 코드만 출력되는지
- `make_resume_agents`, `RESUME_SYSTEM`, `RESUME_PLAN`, `SCENARIOS["resume"]`가 모두 포함되는지
- `save_markdown: True`, `markdown_dir: "resumes"`가 들어 있는지
- 기존 코드와 이름이 충돌하지 않는지

이 단계의 결과는 그대로 쓰기보다 코드 구조를 이해하기 위한 초안으로 봅니다. 실제 핸즈온에서는 다음 단계의 제공 코드를 기준으로 붙여 넣습니다.

## Step 2. 기본 translate 실행

목표는 참가자가 서버, 실행 스크립트, dashboard, orchestrator, specialist 구조를 먼저 눈으로 확인하는 것입니다.

macOS:

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

Windows PowerShell:

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

확인할 것:

- dashboard에 agent 상태와 throughput이 표시되는지
- orchestrator가 작업을 생성하고 specialist들이 응답하는지
- `demo/website_build/index.html`이 생성되는지

## 시나리오 추가 패턴

새 시나리오를 추가할 때는 보통 네 가지를 추가합니다.

```text
1. make_xxx_agents() - agent 목록과 direct_instruction 정의
2. XXX_SYSTEM - specialist에게 공통으로 들어가는 system prompt
3. XXX_PLAN - direct_plan이 아닐 때 쓰는 planning prompt. 실습에서는 구조 설명용으로 유지
4. SCENARIOS["xxx"] - scenario registry 등록
```

이 핸즈온에서는 대부분 `direct_plan: True`를 사용합니다. 그래서 LLM에게 작업 분해를 다시 맡기지 않고, `make_xxx_agents()`가 만든 `direct_instruction`을 그대로 각 agent에게 전달합니다.

## Step 3. 이력서 생성 시나리오 추가

목표는 "agent 여러 개가 서로 다른 Markdown 산출물을 생성하고 폴더에 저장하는 구조"를 이해하는 것입니다.

`demo/scenarios.py`에 agent factory를 추가합니다.

```python
def make_resume_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"resume_{i+1:02d}",
            "emoji": "📄",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Create one complete Korean Markdown resume for a fictional "
                "book publishing company fiction planner. Topic: {topic}. "
                f"This is resume #{i+1}; make the candidate profile, career path, "
                "publisher types, fiction genres, projects, achievements, and tools "
                "clearly different from the other resumes. Output Markdown only."
            ),
            "filename": f"{i+1:02d}_resume_{i+1:02d}.md",
        }
        for i in range(n)
    ]
```

system prompt를 추가합니다.

```python
RESUME_SYSTEM = """
You are a senior Korean resume writer for publishing and content industry roles.
Create one realistic but fully fictional resume for a book publishing company fiction planner.

Output ONLY Markdown.
Do not include explanations or markdown fences.
Do not use real personal data, real phone numbers, real emails, or real company-confidential facts.
Use fictional names, fictional employers, fictional projects, and fictional metrics.
Make the resume specific to fiction/book publishing planning, not a generic IT product planner.

Required structure:
# [Fictional Korean Name] - 도서 출판사 소설 기획자 이력서
## 프로필
## 핵심 역량
## 경력
## 주요 기획 프로젝트
## 성과 지표
## 사용 도구
## 학력 및 자격
## 포트폴리오 요약
""".strip()
```

plan prompt를 추가합니다.

```python
RESUME_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} different fictional Korean Markdown resumes for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each instruction should ask for one complete resume for a book publishing "
        "company fiction planner, with differentiated seniority, genre focus, "
        "publisher type, projects, and achievements."
    ),
}
```

`SCENARIOS`에 등록합니다.

```python
"resume": {
    "make_agents": make_resume_agents,
    "plan": RESUME_PLAN,
    "system_prompt": RESUME_SYSTEM,
    "render_card": resume_card,
    "title": "Publishing Fiction Planner Resumes",
    "default_n": 10,
    "direct_plan": True,
    "save_markdown": True,
    "markdown_dir": "resumes",
},
```

실행합니다.

```bash
bash run.sh --scenario resume --topic "도서 출판사 소설 기획자" --tasks 10
```

확인할 것:

- `demo/website_build/resumes/`에 Markdown 이력서가 저장되는지
- `demo/website_build/resume.html` 또는 `index.html`에서 결과를 볼 수 있는지

## Step 4. 이력서 기반 면접 리뷰 시나리오 추가

목표는 "이전 시나리오의 Markdown 산출물을 다음 시나리오가 입력으로 읽는 구조"를 이해하는 것입니다.

agent factory를 추가합니다.

```python
def make_interview_review_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"interview_{i+1:02d}",
            "emoji": "🧑‍⚖️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Review the following resume as a senior interviewer for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Write one structured Korean Markdown interview review. "
                "Evaluate only evidence visible in the resume. If evidence is weak, say what must be verified in the interview."
            ),
            "filename": f"{i+1:02d}_interview_review_{i+1:02d}.md",
        }
        for i in range(n)
    ]
```

system prompt를 추가합니다.

```python
INTERVIEW_REVIEW_SYSTEM = """
You are a senior interviewer and hiring committee reviewer for Korean book publishing companies.
You are reviewing candidates for fiction planning, novel acquisition, IP development, and editorial planning roles.

Output ONLY Markdown.
Do not include explanations outside the review.
Do not invent facts not present in the resume.
When a claim needs verification, state the interview question that would verify it.
Use a realistic, strict interviewer tone.
For treatment negotiation, make fictional but plausible recommendations based only on resume seniority and role fit.

Required structure:
# [Candidate or Source File] - 면접관 리뷰
## 한줄 평가
## 직무 적합도
## 강점 근거
## 우려점 및 검증 리스크
## 면접 질문 7개
## 꼬리 질문
## 처우협의 포인트
## 예상 연봉/직급 제안
## 평가 루브릭
## 채용 추천
""".strip()
```

plan prompt를 추가합니다.

```python
INTERVIEW_REVIEW_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} interviewer review tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reviews one generated resume from the resumes folder."
    ),
}
```

`SCENARIOS`에 등록합니다.

```python
"interview_review": {
    "make_agents": make_interview_review_agents,
    "plan": INTERVIEW_REVIEW_PLAN,
    "system_prompt": INTERVIEW_REVIEW_SYSTEM,
    "render_card": interview_review_card,
    "title": "Interview Reviews",
    "default_n": 10,
    "direct_plan": True,
    "input_markdown_dir": "resumes",
    "save_markdown": True,
    "markdown_dir": "interview_reviews",
    "preserve_build_dirs": ["resumes"],
},
```

실행합니다.

```bash
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획자" --tasks 10
```

핵심 설명:

- `input_markdown_dir: "resumes"`가 이전 단계 산출물을 읽습니다.
- `{source_filename}`에는 현재 agent가 읽는 파일명이 들어갑니다.
- `{resume_text}`에는 해당 Markdown 파일 내용이 들어갑니다.

## Step 5. 최종 채용 결정 시나리오 추가

목표는 "여러 Markdown 파일을 하나로 모아 aggregate input으로 처리하는 구조"를 이해하는 것입니다.

agent factory를 추가합니다.

```python
def make_hiring_decision_agents(n: int = 1) -> list[dict]:
    return [
        {
            "name": f"hiring_committee_{i+1:02d}",
            "emoji": "🏁",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "You are the final hiring committee for {topic}.\n"
                "Select exactly {hire_count} candidates from the interview reviews below.\n"
                "Input source: {source_filename}\n\n"
                "<interview_reviews>\n{resume_text}\n</interview_reviews>\n\n"
                "Write a final Korean Markdown hiring decision. Include treatment negotiation guidance for selected candidates."
            ),
            "filename": f"{i+1:02d}_hiring_decision.md",
        }
        for i in range(n)
    ]
```

system prompt를 추가합니다.

```python
HIRING_DECISION_SYSTEM = """
You are a final hiring committee for a Korean book publishing company.
You must choose a fixed number of candidates from the provided interview reviews.

Output ONLY Markdown.
Select exactly the requested number of hires.
Use only the evidence in the interview reviews.
When scores are close, explain the tie-breaker.
Include treatment negotiation guidance, but keep it fictional and scenario-based.

Required structure:
# 최종 채용 의사결정
## 선발 인원
## 최종 합격자
## 예비 합격자
## 탈락자 요약
## 비교 평가표
## 처우협의 전략
## 오퍼 리스크
## 최종 결론
""".strip()
```

plan prompt를 추가합니다.

```python
HIRING_DECISION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create final hiring committee decision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads all interview reviews and selects the required number of hires."
    ),
}
```

`SCENARIOS`에 등록합니다.

```python
"hiring_decision": {
    "make_agents": make_hiring_decision_agents,
    "plan": HIRING_DECISION_PLAN,
    "system_prompt": HIRING_DECISION_SYSTEM,
    "render_card": hiring_decision_card,
    "title": "Hiring Decision",
    "default_n": 1,
    "direct_plan": True,
    "input_markdown_dir": "interview_reviews",
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "hiring_decisions",
    "preserve_build_dirs": ["resumes", "interview_reviews"],
},
```

실행합니다.

```bash
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획자" --hires 2
```

핵심 설명:

- `aggregate_input_markdown: True`가 `interview_reviews/` 안의 모든 Markdown 파일을 하나의 입력으로 합칩니다.
- `--hires 2`는 `{hire_count}`로 전달됩니다.

## Step 6. 면접 대화 시뮬레이션 확장

목표는 같은 `resumes/` 입력을 다른 방식으로 활용하는 파생 시나리오를 추가하는 것입니다.

agent factory를 추가합니다.

```python
def make_interview_dialogue_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"interview_dialogue_{i+1:02d}",
            "emoji": "🗣️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Simulate a realistic Korean job interview dialogue for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Write a multi-turn Markdown transcript between a senior interviewer and the candidate. "
                "Include evidence-based questions, follow-up questions, candidate answers, interviewer notes, "
                "and a compensation negotiation section. The candidate may elaborate plausible context only when "
                "it is consistent with the resume; mark anything that needs verification."
            ),
            "filename": f"{i+1:02d}_interview_dialogue_{i+1:02d}.md",
        }
        for i in range(n)
    ]
```

system prompt를 추가합니다.

```python
INTERVIEW_DIALOGUE_SYSTEM = """
You are a senior Korean publishing-company interviewer and a realistic fictional candidate simulator.
You are conducting interviews for fiction planning, novel acquisition, IP development, and editorial planning roles.

Output ONLY Markdown.
Do not include explanations outside the transcript.
Use the resume as the factual base.
The candidate may give plausible elaborations only if they are consistent with the resume.
Do not invent new major achievements, employers, awards, or confidential facts not supported by the resume.
When a candidate answer needs verification, add an interviewer note.
Include a short compensation negotiation conversation near the end.

Required structure:
# [Candidate or Source File] - 면접 대화록
## 면접 설정
## 핵심 검증 포인트
## 질의응답 대화
### Q1. [질문 제목]
**면접관:**
**지원자:**
**면접관 꼬리질문:**
**지원자 추가 답변:**
**면접관 메모:**
## 처우협의 대화
## 면접관 최종 평가
## 추가 검증 필요 사항
## 채용 추천
""".strip()
```

plan prompt와 registry를 추가합니다.

```python
INTERVIEW_DIALOGUE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} interview dialogue simulation tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads one generated resume and writes a multi-turn interviewer-candidate Q&A transcript."
    ),
}
```

```python
"interview_dialogue": {
    "make_agents": make_interview_dialogue_agents,
    "plan": INTERVIEW_DIALOGUE_PLAN,
    "system_prompt": INTERVIEW_DIALOGUE_SYSTEM,
    "render_card": interview_dialogue_card,
    "title": "Interview Dialogues",
    "default_n": 10,
    "direct_plan": True,
    "input_markdown_dir": "resumes",
    "save_markdown": True,
    "markdown_dir": "interview_dialogues",
    "preserve_build_dirs": ["resumes"],
},
```

실행합니다.

```bash
bash run.sh --scenario interview_dialogue --topic "도서 출판사 소설 기획자" --tasks 10
```

대화록 기반 최종 채용 결정은 `hiring_decision`과 같은 구조를 사용하되 입력 폴더만 바꿉니다.

```python
def make_hiring_decision_from_dialogue_agents(n: int = 1) -> list[dict]:
    return [
        {
            "name": f"hiring_committee_dialogue_{i+1:02d}",
            "emoji": "🏁",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "You are the final hiring committee for {topic}.\n"
                "Select exactly {hire_count} candidates from the interview dialogue transcripts below.\n"
                "Input source: {source_filename}\n\n"
                "<interview_dialogues>\n{resume_text}\n</interview_dialogues>\n\n"
                "Write a final Korean Markdown hiring decision. Use the Q&A evidence, interviewer notes, "
                "role fit, risk signals, and compensation negotiation responses."
            ),
            "filename": f"{i+1:02d}_hiring_decision_from_dialogue.md",
        }
        for i in range(n)
    ]
```

```python
HIRING_DECISION_FROM_DIALOGUE_SYSTEM = """
You are a final hiring committee for a Korean book publishing company.
You must choose a fixed number of candidates from interview dialogue transcripts.

Output ONLY Markdown.
Select exactly the requested number of hires.
Use only evidence from the Q&A transcripts, interviewer notes, and compensation negotiation sections.
When a candidate answer is plausible but weakly verified, treat it as a risk.
When scores are close, explain the tie-breaker.
Include treatment negotiation guidance, but keep it fictional and scenario-based.

Required structure:
# 최종 채용 의사결정 - 면접 대화 기반
## 선발 인원
## 최종 합격자
## 예비 합격자
## 탈락자 요약
## 질의응답 근거 비교표
## 처우협의 전략
## 오퍼 리스크
## 최종 결론
""".strip()
```

```python
HIRING_DECISION_FROM_DIALOGUE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create final hiring committee decision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads all interview dialogue transcripts and selects the required number of hires."
    ),
}
```

```python
"hiring_decision_from_dialogue": {
    "make_agents": make_hiring_decision_from_dialogue_agents,
    "plan": HIRING_DECISION_FROM_DIALOGUE_PLAN,
    "system_prompt": HIRING_DECISION_FROM_DIALOGUE_SYSTEM,
    "render_card": hiring_decision_card,
    "title": "Hiring Decision From Dialogue",
    "default_n": 1,
    "direct_plan": True,
    "input_markdown_dir": "interview_dialogues",
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "hiring_decisions_from_dialogue",
    "preserve_build_dirs": ["resumes", "interview_dialogues"],
},
```

실행합니다.

```bash
bash run.sh --scenario hiring_decision_from_dialogue --topic "도서 출판사 소설 기획자" --hires 2
```

## Step 7. 단편소설 생성 시나리오 추가

목표는 채용 파이프라인과 다른 도메인으로 같은 멀티 에이전트 패턴을 확장하는 것입니다.

agent factory를 추가합니다.

```python
def make_short_story_writing_agents(n: int = 10) -> list[dict]:
    genres = [
        ("literary", "문학성이 강한 현실 단편"),
        ("mystery", "도시 미스터리 단편"),
        ("romance", "잔잔한 로맨스 단편"),
        ("sf", "근미래 SF 단편"),
        ("fantasy", "현대 판타지 단편"),
        ("thriller", "심리 스릴러 단편"),
        ("historical", "근현대사 배경 단편"),
        ("young_adult", "청소년/성장 단편"),
        ("horror", "서늘한 호러 단편"),
        ("humor", "블랙코미디 단편"),
    ]
    agents = []
    for i in range(n):
        slug, genre = genres[i % len(genres)]
        agents.append({
            "name": f"short_story_{i+1:02d}_{slug}",
            "emoji": "🖋️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are fiction writer #{i+1}. Write one complete Korean short story for this call: {{topic}}.\n"
                f"Assigned lane: {genre}.\n"
                "Output a polished Markdown manuscript with title, author pen name, short logline, and the full story. "
                "The story must have a complete beginning, development, turn, and ending. "
                "Use fictional pen names and do not copy existing works."
            ),
            "filename": f"{i+1:02d}_short_story_{slug}.md",
        })
    return agents
```

system prompt, plan, registry를 추가합니다.

```python
SHORT_STORY_WRITING_SYSTEM = """
You are a professional Korean short-story writer.
Write original, complete, publishable short fiction.

Output ONLY Markdown.
Do not include explanations outside the manuscript.
Do not copy existing works, real living authors' style, or copyrighted characters.
Use fictional author names and fictional story content.

Required structure:
# [작품 제목]
## 작가명
## 로그라인
## 원고
""".strip()
```

```python
SHORT_STORY_WRITING_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} short-story writing tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task should produce one complete, distinct short story."
    ),
}
```

```python
"short_story_writing": {
    "make_agents": make_short_story_writing_agents,
    "plan": SHORT_STORY_WRITING_PLAN,
    "system_prompt": SHORT_STORY_WRITING_SYSTEM,
    "render_card": short_story_card,
    "title": "Short Story Submissions",
    "default_n": 10,
    "direct_plan": True,
    "save_markdown": True,
    "markdown_dir": "short_stories",
    "preserve_build_dirs": ["resumes", "interview_reviews", "hiring_decisions"],
},
```

실행합니다.

```bash
bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
```

## Step 8. 단편소설 심사 및 선정 시나리오 추가

목표는 여러 원고를 한 번에 읽고, 서로 다른 편집자 관점으로 선정 보고서를 만드는 것입니다.

agent factory를 추가합니다.

```python
def make_story_review_selection_agents(n: int = 3) -> list[dict]:
    perspectives = [
        ("editorial", "문학성과 완성도 중심 편집자"),
        ("market", "독자성, 판매 가능성, 포지셔닝 중심 편집자"),
        ("series", "작가 성장성, IP 확장성, 출간 리스크 중심 편집자"),
    ]
    agents = []
    for i in range(n):
        slug, perspective = perspectives[i % len(perspectives)]
        agents.append({
            "name": f"story_editor_{i+1:02d}_{slug}",
            "emoji": "📚",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are editor #{i+1}, a {perspective}.\n"
                "Review all submitted short stories for the publication theme: {topic}.\n"
                "Select exactly {select_count} stories for publication consideration.\n"
                "Input source: {source_filename}\n\n"
                "<short_stories>\n{resume_text}\n</short_stories>\n\n"
                "Write a Korean Markdown editorial review and selection report."
            ),
            "filename": f"{i+1:02d}_story_selection_{slug}.md",
        })
    return agents
```

system prompt, plan, registry를 추가합니다.

```python
STORY_REVIEW_SELECTION_SYSTEM = """
You are a senior Korean publishing editor reviewing short-story submissions.
You must review all submitted stories and select a fixed number for publication consideration.

Output ONLY Markdown.
Select exactly the requested number of stories.
Use only the submitted story texts as evidence.
Be clear about editorial strengths, market fit, revision needs, and publication risk.

Required structure:
# 단편소설 심사 및 선정 보고서
## 심사 기준
## 전체 후보작 요약
## 선정작
## 예비 선정작
## 탈락작 주요 사유
## 작품별 편집 메모
## 출간 가능성 및 리스크
## 최종 추천
""".strip()
```

```python
STORY_REVIEW_SELECTION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} editorial review tasks for short stories about "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reviews all short stories and selects the requested number."
    ),
}
```

```python
"story_review_selection": {
    "make_agents": make_story_review_selection_agents,
    "plan": STORY_REVIEW_SELECTION_PLAN,
    "system_prompt": STORY_REVIEW_SELECTION_SYSTEM,
    "render_card": story_review_selection_card,
    "title": "Short Story Review Selection",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "short_stories",
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "story_selections",
    "preserve_build_dirs": ["short_stories"],
},
```

실행합니다.

```bash
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
```

핵심 설명:

- `--select 3`은 `{select_count}`로 전달됩니다.
- 이 단계까지는 `--topic`이 심사 기준에 직접 들어가므로 넣는 것이 좋습니다.

## Step 9. 출간 의향 확인 메일 시나리오 추가

실제 출판사 흐름에서는 선정 직후 바로 개정 원고를 쓰기보다, 먼저 저자에게 출간 의향을 확인하고 계약 협의를 시작합니다.

```text
story_selections/에서 선정 보고서 읽기
-> 선정작별 출간 의향 확인 메일 작성
-> publication_offer_emails/에 저장
```

핵심 agent factory입니다.

```python
def make_publication_offer_email_agents(n: int = 3) -> list[dict]:
    return [
        {
            "name": f"offer_email_{i+1:02d}",
            "emoji": "✉️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are an acquisitions editor writing publication offer email #{i+1}.\n"
                "Use the story selection results below. Draft an initial publication-intent email for selected story slot #{slot}.\n"
                "If that slot does not exist, write a brief internal note saying there is no selected story for this slot.\n"
                "Input source: {source_filename}\n\n"
                "<selection_results>\n{resume_text}\n</selection_results>\n\n"
                "Output one Korean Markdown email draft only, including subject, recipient placeholder, opening, selected-work rationale, intent-to-publish note, contract-discussion agenda, schedule, and closing."
            ),
            "filename": f"{i+1:02d}_publication_offer_email.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]
```

registry는 이전 단계의 선정 보고서만 읽도록 둡니다.

```python
"publication_offer_email": {
    "make_agents": make_publication_offer_email_agents,
    "plan": PUBLICATION_OFFER_EMAIL_PLAN,
    "system_prompt": PUBLICATION_OFFER_EMAIL_SYSTEM,
    "render_card": publication_offer_email_card,
    "title": "Publication Offer Emails",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "story_selections",
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "publication_offer_emails",
    "preserve_build_dirs": ["short_stories", "story_selections"],
},
```

실행합니다.

```bash
bash run.sh --scenario publication_offer_email --select 3 --tasks 3
```

## Step 10. 계약 조건 협의 시나리오 추가

목표는 출간 제안 이후의 조건 협의 메모를 만드는 것입니다. 이 산출물은 실습용 문서이며 법적 조언이나 실제 계약서가 아닙니다.

```python
def make_contract_negotiation_agents(n: int = 3) -> list[dict]:
    return [
        {
            "name": f"contract_negotiation_{i+1:02d}",
            "emoji": "🤝",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing rights editor preparing contract negotiation memo #{i+1}.\n"
                "Use the publication offer emails and selection reports below. Prepare negotiation notes for selected story slot #{slot}.\n"
                "This is a fictional workshop artifact, not legal advice and not a binding contract.\n"
                "Input source: {source_filename}\n\n"
                "<offer_and_selection_materials>\n{resume_text}\n</offer_and_selection_materials>\n\n"
                "Output one Korean Markdown negotiation memo only, covering proposed rights scope, manuscript delivery, revision expectations, schedule, compensation placeholders, risk points, author questions, publisher concessions, and next actions."
            ),
            "filename": f"{i+1:02d}_contract_negotiation.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]
```

```python
CONTRACT_NEGOTIATION_SYSTEM = """
You are a Korean publishing rights editor preparing a contract-term negotiation memo.

Output ONLY Markdown.
This is a fictional workshop artifact, not legal advice and not a binding contract.
Use placeholders for money, dates, addresses, personal information, and legal entity details.
Keep the memo close to a real publishing workflow: rights scope, compensation, manuscript delivery, revision, approval, schedule, and unresolved negotiation points.

Required structure:
# 계약 조건 협의 메모
## 협의 대상 작품
## 출간 제안 요약
## 주요 계약 조건 초안
## 쟁점 및 협상 포인트
## 작가에게 확인할 질문
## 출판사 내부 검토 사항
## 다음 액션
## 비고
""".strip()
```

```python
"contract_negotiation": {
    "make_agents": make_contract_negotiation_agents,
    "plan": CONTRACT_NEGOTIATION_PLAN,
    "system_prompt": CONTRACT_NEGOTIATION_SYSTEM,
    "render_card": contract_negotiation_card,
    "title": "Contract Negotiation Memos",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "publication_offer_emails",
    "auxiliary_input_markdown_dirs": ["story_selections"],
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "contract_negotiations",
    "preserve_build_dirs": ["short_stories", "story_selections", "publication_offer_emails"],
},
```

실행합니다.

```bash
bash run.sh --scenario contract_negotiation --select 3 --tasks 3
```

## Step 11. 출간 계약 패키지 초안 시나리오 추가

목표는 협의 메모를 바탕으로 편집팀이 법무 검토 전에 정리할 계약 패키지 초안을 만드는 것입니다.

```python
def make_publication_contract_agents(n: int = 3) -> list[dict]:
    return [
        {
            "name": f"publication_contract_{i+1:02d}",
            "emoji": "📑",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing operations editor preparing contract package #{i+1}.\n"
                "Use the negotiation memo and publication offer materials below. Prepare a non-binding contract package summary for selected story slot #{slot}.\n"
                "This is a fictional workshop artifact, not legal advice, not a substitute for lawyer review, and not a binding legal contract.\n"
                "Input source: {source_filename}\n\n"
                "<negotiation_and_offer_materials>\n{resume_text}\n</negotiation_and_offer_materials>\n\n"
                "Output one Korean Markdown contract package only, including term sheet, clauses-to-review checklist, required author materials, internal approval checklist, signature workflow, and open legal-review items."
            ),
            "filename": f"{i+1:02d}_publication_contract.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]
```

```python
PUBLICATION_CONTRACT_SYSTEM = """
You are a Korean publishing operations editor preparing a non-binding contract package summary.

Output ONLY Markdown.
This is a fictional workshop artifact, not legal advice, not a substitute for lawyer review, and not a binding legal contract.
Do not invent real personal information, real bank details, real registration numbers, or real legal entity data.
Focus on what an editorial team would prepare before formal contract review and signing.

Required structure:
# 출간 계약 패키지 초안
## 계약 대상 작품
## 조건 합의 요약
## 계약 주요 조항 체크리스트
## 작가 제출 필요 자료
## 출판사 내부 승인 체크리스트
## 서명 및 보관 절차
## 법무 검토 필요 항목
## 다음 액션
""".strip()
```

```python
"publication_contract": {
    "make_agents": make_publication_contract_agents,
    "plan": PUBLICATION_CONTRACT_PLAN,
    "system_prompt": PUBLICATION_CONTRACT_SYSTEM,
    "render_card": publication_contract_card,
    "title": "Publication Contract Packages",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "contract_negotiations",
    "auxiliary_input_markdown_dirs": ["publication_offer_emails"],
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "publication_contracts",
    "preserve_build_dirs": ["short_stories", "story_selections", "publication_offer_emails", "contract_negotiations"],
},
```

실행합니다.

```bash
bash run.sh --scenario publication_contract --select 3 --tasks 3
```

## Step 12. 선정작 개정 시나리오 추가

계약 조건까지 정리한 뒤 선정작을 개정합니다. 이 단계는 완성본의 `orchestrator.py`에 들어 있는 선정작 중복 제거 로직을 사용합니다.

```text
story_selections/에서 선정 보고서 읽기
+ short_stories/에서 원본 원고 읽기
+ publication_contracts/에서 출간 조건 맥락 읽기
-> 선정작 파일명을 추출하고 중복 제거
-> agent별로 개정 대상 원고를 하나씩 배정
```

registry는 계약 패키지까지 보존하고 참고 입력으로 추가합니다.

```python
"story_revision": {
    "make_agents": make_story_revision_agents,
    "plan": STORY_REVISION_PLAN,
    "system_prompt": STORY_REVISION_SYSTEM,
    "render_card": story_revision_card,
    "title": "Short Story Revisions",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "story_selections",
    "auxiliary_input_markdown_dirs": ["short_stories", "publication_contracts"],
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "revised_stories",
    "preserve_build_dirs": [
        "short_stories",
        "story_selections",
        "publication_offer_emails",
        "contract_negotiations",
        "publication_contracts",
    ],
},
```

실행합니다.

```bash
bash run.sh --scenario story_revision --select 3 --tasks 3
```

## Step 13. 출간 마케팅 문구 시나리오 추가

마지막 단계에서는 개정 원고와 출간 조건 맥락을 바탕으로 온라인 서점, SNS, 뉴스레터, 보도자료용 문구를 생성합니다.

```python
def make_marketing_copy_agents(n: int = 3) -> list[dict]:
    channels = [
        ("bookstore", "online bookstore detail page and search snippets"),
        ("social", "short social media launch posts"),
        ("press", "press release and newsletter copy"),
    ]
    agents = []
    for i in range(n):
        slug, channel = channels[i % len(channels)]
        agents.append({
            "name": f"marketing_copy_{i+1:02d}_{slug}",
            "emoji": "📣",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing marketer writing launch copy package #{i+1} for {channel}.\n"
                "Use the revised stories, contract package summaries, and selection notes below.\n"
                "Write copy for selected story slot #{slot}. If the slot cannot be identified, write a brief internal note.\n"
                "Input source: {source_filename}\n\n"
                "<publication_materials>\n{resume_text}\n</publication_materials>\n\n"
                "Output one Korean Markdown marketing copy package only, including positioning, target readers, one-line hook, short synopsis, bookstore copy, SNS posts, newsletter blurb, press headline, and caution notes."
            ),
            "filename": f"{i+1:02d}_marketing_copy_{slug}.md",
            "slot": str(i + 1),
        })
    return agents
```

```python
MARKETING_COPY_SYSTEM = """
You are a Korean publishing marketer creating launch copy for selected and revised short stories.

Output ONLY Markdown.
Use the revised manuscript and editorial context as evidence.
Do not claim awards, bestseller status, media quotes, or author facts that are not present in the source material.
Write commercially useful copy that can support bookstore detail pages, SNS, newsletter, and press outreach.

Required structure:
# 출간 마케팅 문구 패키지
## 작품 포지셔닝
## 타깃 독자
## 한 줄 훅
## 짧은 소개문
## 온라인 서점 문구
## SNS 문구
## 뉴스레터 문구
## 보도자료 헤드라인
## 사용 시 주의사항
""".strip()
```

```python
"marketing_copy": {
    "make_agents": make_marketing_copy_agents,
    "plan": MARKETING_COPY_PLAN,
    "system_prompt": MARKETING_COPY_SYSTEM,
    "render_card": marketing_copy_card,
    "title": "Publication Marketing Copy",
    "default_n": 3,
    "direct_plan": True,
    "input_markdown_dir": "revised_stories",
    "auxiliary_input_markdown_dirs": ["publication_contracts", "story_selections"],
    "aggregate_input_markdown": True,
    "save_markdown": True,
    "markdown_dir": "marketing_copy",
    "preserve_build_dirs": [
        "short_stories",
        "story_selections",
        "publication_offer_emails",
        "contract_negotiations",
        "publication_contracts",
        "revised_stories",
    ],
},
```

실행합니다.

```bash
bash run.sh --scenario marketing_copy --select 3 --tasks 3
```

## 최종 실행 순서

핸즈온을 끝까지 진행한 뒤에는 아래 순서로 전체 파이프라인을 다시 실행할 수 있습니다.

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10

bash run.sh --scenario resume --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획자" --hires 2

bash run.sh --scenario interview_dialogue --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario hiring_decision_from_dialogue --topic "도서 출판사 소설 기획자" --hires 2

bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
bash run.sh --scenario publication_offer_email --select 3 --tasks 3
bash run.sh --scenario contract_negotiation --select 3 --tasks 3
bash run.sh --scenario publication_contract --select 3 --tasks 3
bash run.sh --scenario story_revision --select 3 --tasks 3
bash run.sh --scenario marketing_copy --select 3 --tasks 3
```

## 진행자가 강조할 포인트

- `make_agents()`는 병렬 작업자 목록을 만든다.
- `direct_instruction`은 각 agent에게 들어가는 실제 작업 지시다.
- `system_prompt`는 해당 시나리오 전체의 공통 역할과 출력 형식을 잡는다.
- `save_markdown: True`는 결과를 다음 시나리오가 읽을 수 있게 파일로 저장한다.
- `input_markdown_dir`는 이전 단계의 산출물 폴더를 읽는다.
- `aggregate_input_markdown: True`는 여러 파일을 하나의 입력으로 합친다.
- `auxiliary_input_markdown_dirs`는 주 입력 외의 참고 폴더를 추가로 읽는다.
- `preserve_build_dirs`는 다음 실행에서 이전 단계 산출물을 지우지 않도록 보존한다.

## 문제 해결

- `Unknown scenario`가 나오면 `SCENARIOS`에 해당 이름이 등록되어 있는지 확인합니다.
- `NO_INPUT_FILE_FOUND.md`가 나오면 이전 단계 시나리오를 먼저 실행했는지 확인합니다.
- 결과가 이전 단계와 맞지 않으면 `input_markdown_dir`와 `markdown_dir` 이름이 서로 맞물리는지 확인합니다.
- Windows에서는 `bash run.sh` 대신 `.\run.ps1`을 사용합니다.
- 노트북 성능이 부족하면 `--tasks 3` 또는 `--tasks 5`로 줄입니다.

# Hermes Agent란 무엇인가

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `Hermes Agent`가 정확히 어떤 도구인지 먼저 이해하고 싶은 참가자
- `Codex`, `Claude Code`, `OpenCode` 같은 코딩 에이전트와 무엇이 다른지 감을 잡고 싶은 참가자
- 왜 이번 핸즈온에서 `Hermes`를 기본 경로가 아니라 선택형 고급 경로로 두는지 알고 싶은 참가자

## 먼저 한 줄 정의

`Hermes Agent`는 Nous Research가 만든 **자율형 AI agent runtime** 입니다.

단순 채팅 앱이나 IDE 안에 묶인 코딩 보조 도구라기보다:

- 도구를 호출하고
- 기억을 쌓고
- skills를 재사용하고
- 여러 플랫폼에서 동작하고
- 필요하면 subagent로 작업을 나누는

**장기 실행형 agent framework** 에 가깝습니다.

## 공식 문서가 설명하는 Hermes의 핵심

Hermes 공식 문서 기준으로 핵심 포인트는 아래입니다.

- self-improving agent
- built-in learning loop
- persistent memory
- skills system
- context files
- scheduled tasks
- subagent delegation
- messaging gateway
- provider-agnostic model routing

즉, 모델 하나에 얇게 붙는 채팅 UI가 아니라, **기억 + 도구 + 자동화 + 실행 환경**까지 포함한 agent 시스템으로 이해하면 됩니다.

## Hermes는 무엇을 할 수 있나요?

Hermes Features Overview 기준으로 주요 기능은 아래와 같습니다.

### 1. Tools / Toolsets

- 터미널 실행
- 파일 읽기/쓰기
- 웹 검색/추출
- 브라우저 자동화
- 이미지/음성 관련 도구

즉, 모델이 답만 하는 것이 아니라 **실제로 작업을 수행**할 수 있습니다.

### 2. Skills System

- 필요한 지식을 on-demand로 로드
- 토큰 낭비를 줄이기 위한 progressive disclosure
- 재사용 가능한 플레이북 축적

핸즈온 관점에서는 이 부분이 특히 중요합니다.

### 3. Persistent Memory

- `MEMORY.md`
- `USER.md`

같은 형태로 세션 간 기억을 이어 갑니다.

### 4. Context Files

- `.hermes.md`
- `AGENTS.md`
- `CLAUDE.md`
- `SOUL.md`

같은 파일을 읽어 프로젝트 규칙과 정체성을 반영합니다.

### 5. Delegation / Automation

- `delegate_task`로 child agent 생성
- `cron` 기반 자동화
- 여러 플랫폼으로 결과 전달

즉 Hermes는 “한 번 답하는 도구”보다 “계속 일하는 agent”에 더 가깝습니다.

## 다른 도구와 무엇이 다른가요?

짧게 비교하면:

- `LM Studio`: 로컬 모델 실행/관리 GUI
- `Ollama`: 로컬 모델 실행 CLI/API
- `llama.cpp`: GGUF 실행 엔진 및 로컬 서버
- `OpenCode`: 코딩 중심 에이전트
- `Hermes`: 코딩도 할 수 있지만, 더 넓게는 **에이전트 운영체제**에 가까움

즉:

- `LM Studio`, `Ollama`, `llama.cpp`는 주로 **추론 서버**
- `Hermes`는 그 위에 붙는 **agent layer**

라고 보면 됩니다.

## 이번 핸즈온에서 Hermes를 어떻게 보나요?

이번 문서 묶음에서는 `Hermes`를 **선택형 고급 경로**로 봅니다.

이유:

- Windows에서는 WSL2가 필요합니다.
- 설치와 설정 면적이 기본 경로보다 넓습니다.
- 참가자 전원에게 강제하기엔 운영 리스크가 있습니다.

반대로 강점도 분명합니다.

- role-based agent workflow를 구성하기 좋음
- skills 실습 주제로 적합함
- 로컬 OpenAI-compatible endpoint와 연결 가능
- `Gemma 4 + llama.cpp` 또는 `Gemma 4 + LM Studio` 위에 agent layer를 얹을 수 있음

## 이번 핸즈온에서 Hermes를 어떤 그림으로 이해하면 되나요?

가장 쉬운 그림은 이렇습니다.

```text
Gemma 4
  -> local inference server
     (LM Studio / Ollama / llama.cpp)
        -> Hermes Agent
           -> tools, skills, memory, delegation
```

즉 `Gemma 4`는 두뇌이고, `Hermes`는 실행기이자 오케스트레이터입니다.

## 왜 기본 경로가 아니고 고급 경로인가요?

- 기본 참가자는 `LM Studio`만으로도 충분히 세션을 따라올 수 있습니다.
- `Hermes`는 설치뿐 아니라 모델 endpoint 연결까지 이해해야 합니다.
- Windows 참가자는 WSL2까지 준비해야 합니다.
- 핸즈온 60분 안에 모두에게 같은 수준의 안정성을 기대하기 어렵습니다.

그래서 문서 흐름상으로도:

1. 모델과 실행 환경 이해
2. 기본 설치 경로 준비
3. 그 다음 고급 경로로 `Hermes` 확장

순서가 자연스럽습니다.

## 누구에게 특히 잘 맞나요?

- 에이전트 워크플로에 관심 있는 참가자
- `skills`를 직접 만들어 보고 싶은 참가자
- role-based workflow를 구성해 보고 싶은 참가자
- 로컬 모델 위에 agent system을 얹어 보고 싶은 참가자

## 다음에 무엇을 보면 되나요?

- 실제 설치는 [Hermes Agent 설치 가이드](./13-hermes-agent-setup.md)
- 로컬 서버는 [llama.cpp 설치 가이드](./07-llamacpp-setup.md)
- 코드 에이전트 기대치는 [Gemma 4 벤치마크와 코딩 에이전트 기대치](./09-gemma4-benchmarks-and-agent-expectations.md)

## 공식 참고 링크

- [Hermes Docs Home](https://hermes-agent.nousresearch.com/docs/)
- [Features Overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview)
- [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart/)

## 문서 작성 메모

- 이 문서는 `2026-04-21` 기준 Hermes 공식 문서를 바탕으로 정리했습니다.
- 이번 행사 기준으로는 `Hermes = 선택형 고급 경로`라는 운영 관점을 반영했습니다.

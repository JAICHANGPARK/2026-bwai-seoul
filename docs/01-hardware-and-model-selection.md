# 하드웨어 / 운영체제 / 모델 선택 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서에서 다루는 내용

- 어떤 도구를 기본으로 설치할지
- 운영체제별 권장 경로
- 8GB, 16GB, 32GB, 36GB 메모리별 권장 모델
- 행사 전에 어떤 모델을 미리 받아야 하는지

추가 참고:

- 코딩 에이전트 기대치와 모델별 벤치마크는 [Gemma 4 벤치마크와 코딩 에이전트 기대치](./09-gemma4-benchmarks-and-agent-expectations.md) 문서를 확인해 주세요.
- 메모리로 어떤 모델을 골라야 하는지는 [메모리 기준으로 Gemma 4 모델 고르는 방법](./03-memory-based-model-selection.md) 문서를 확인해 주세요.
- OpenCode를 개발자 에이전트처럼 연결해 보고 싶다면 [OpenCode 설치 및 LM Studio 연동 가이드](./10-opencode-lmstudio-developer-agent.md) 문서를 확인해 주세요.
- Hermes Agent가 정확히 어떤 도구인지 먼저 이해하고 싶다면 [Hermes Agent란 무엇인가](./12-hermes-agent-overview.md) 문서를 확인해 주세요.

## Ollama와 LM Studio 비교

| 항목 | Ollama | LM Studio |
| --- | --- | --- |
| 추천 대상 | 개발자, CLI/API 선호 사용자 | 개발자, 비개발자 모두 / GUI 선호 사용자 |
| 설치 방식 | 앱 + CLI 중심 | 데스크톱 앱 중심 |
| 모델 받기 | `ollama pull` 또는 `ollama run` | Discover 탭에서 검색/다운로드 |
| 사용 방식 | 터미널, 로컬 API, 자동화에 강함 | 채팅 UI, 모델 관리 UI, 로컬 서버에 강함 |
| 오프라인 사용 | 모델 다운로드 후 로컬 실행 | 모델 다운로드 후 완전 오프라인 사용 가능 |
| macOS 지원 | Apple Silicon 지원, Intel Mac은 CPU 전용 | Apple Silicon만 지원, Intel Mac 미지원 |
| Windows 지원 | 네이티브 앱, NVIDIA/AMD GPU 지원 | x64/ARM 지원, 16GB+ RAM 권장 |
| ChromeOS | Linux 개발 환경에서 best-effort | 공식 권장 경로 아님 |
| 행사 권장도 | 보조 또는 고급/CLI 경로 | 기본 권장 |

## 운영체제별 빠른 추천

| 운영체제 | 가장 권장 | 대안 | 비고 |
| --- | --- | --- | --- |
| Windows | LM Studio | Ollama | 하나만 설치한다면 LM Studio를 권장합니다. |
| macOS Apple Silicon | LM Studio | Ollama | LM Studio는 Apple Silicon 전용이며, GGUF를 기본으로 쓰고 필요하면 MLX도 활용할 수 있습니다. |
| macOS Intel | Ollama | 없음에 가까움 | LM Studio 데스크톱 앱은 Intel Mac 미지원입니다. |
| Linux (Ubuntu) | LM Studio | Ollama | GUI 설치가 가능하면 LM Studio를 우선 권장합니다. |
| ChromeOS | Ollama | 가능하면 다른 노트북 준비 | Linux 개발 환경은 GPU 가속 미지원입니다. |

## 메모리별 권장 모델

아래 권장은 행사 당일 안정적인 진행을 기준으로 잡았습니다.  
공식 모델 페이지의 최소 메모리는 더 낮을 수 있지만, 실제로는 운영체제와 브라우저가 메모리를 함께 사용하므로 여유를 두는 편이 안전합니다.

| 노트북 메모리 | 행사 권장 모델 | 권장 도구 | 안내 |
| --- | --- | --- | --- |
| 8GB | `gemma4:e2b` / `google/gemma-4-e2b` | `best-effort` | 8GB는 공식 권장 사양보다 낮아 LM Studio/Ollama 어느 쪽도 무난한 기본 조합으로 보기 어렵습니다. E2B만 시도하고, 가능하면 16GB 이상 노트북을 권장합니다. 실제로는 속도가 많이 느리거나 시스템이 일시적으로 멈춘 것처럼 보일 수 있습니다. |
| 16GB | `gemma4:e4b` / `google/gemma-4-e4b` | LM Studio 우선 | 가장 무난한 참가 사양입니다. 실패 시 E2B로 낮추면 됩니다. |
| 32GB | `gemma4:e4b`, `gemma4:26b` / `google/gemma-4-26b-a4b` | LM Studio 우선 | 속도와 안정성을 우선하면 E4B, 더 큰 모델을 원하면 26B A4B를 선택하세요. |
| 36GB | `gemma4:26b`, `gemma4:31b` / `google/gemma-4-31b` | LM Studio 우선 | 31B도 가능하지만, 반응 속도는 26B A4B가 더 나을 수 있습니다. |

8GB 추가 메모:

- Windows와 macOS에서 LM Studio 공식 권장 메모리는 16GB 이상입니다.
- 따라서 8GB는 "무난한 기본 조합"이 아니라, 작은 모델(E2B) 기준의 `best-effort` 준비로 이해하는 편이 안전합니다.
- 8GB Apple Silicon Mac도 E2B/E4B 실행 중 속도가 크게 떨어지거나 시스템이 멈춘 것처럼 보일 수 있으므로, 안정적인 실습 장비로 보기 어렵습니다.
- 8GB 장비로 참석하는 경우에는 작은 컨텍스트, 브라우저 탭 최소화, 다른 앱 종료를 전제로 안내하는 편이 좋습니다.

## 공식 최소 메모리 참고

LM Studio 모델 페이지 기준:

- `google/gemma-4-e2b`: 최소 시스템 메모리 4GB
- `google/gemma-4-e4b`: 최소 시스템 메모리 6GB
- `google/gemma-4-26b-a4b`: 최소 시스템 메모리 17GB
- `google/gemma-4-31b`: 최소 시스템 메모리 19GB

행사 운영 기준 권장은 위 최소치보다 보수적으로 잡는 것을 추천합니다.

## 어떤 모델을 미리 받아두면 좋을까?

행사 표준 권장안은 아래와 같습니다.

중요:

- 이번 핸즈온은 **채팅 / 질의응답 / 에이전트 흐름**이 중심이므로, 가능하면 **instruction-tuned (`-it`) 또는 chat-ready 모델**을 받는 편이 맞습니다.
- Hugging Face나 `llama.cpp` 예시에서는 보통 `gemma-4-...-it` 처럼 보입니다.
- Ollama는 `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b` 같은 런타임 태그를 쓰므로, 사용자가 별도로 `-it` 접미사를 고를 필요는 없습니다.
- LM Studio는 모델 목록 이름이 `google/gemma-4-e4b`처럼 더 짧게 보일 수 있으므로, **채팅/실습용 instruction-tuned 또는 chat-ready 항목인지** 설명을 함께 확인하는 편이 안전합니다.

- 8GB: `E2B`만 미리 다운로드
- 8GB는 현장 안정성이 낮으므로, 가능하면 16GB 이상 장비로 변경
- 16GB: `E4B` 다운로드, 불안하면 `E2B`도 함께 준비
- 32GB: `E4B` 또는 `26B A4B`
- 36GB: `26B A4B` 또는 `31B`

중요:

- 행사 당일에 모델 다운로드를 시작하지 마세요.
- 모델 파일이 커서 네트워크 상황이 좋지 않으면 실습 시간 대부분을 다운로드에 쓰게 될 수 있습니다.
- 최소한 설치, 모델 다운로드, 1회 실행 테스트까지 끝낸 상태로 참석해 주세요.

## 권장 준비 시나리오

### 가장 안전한 시나리오

- Windows/macOS/Linux 사용자: LM Studio 설치 + **chat-ready / instruction-tuned** `google/gemma-4-e2b` 또는 `google/gemma-4-e4b` 다운로드
- 추가로 CLI/API 실습도 원하면 Ollama까지 설치
- 공통 필수 조건: 행사 전 모델 다운로드와 실행 테스트까지 완료

### 행사 운영 관점의 권장안

- 8GB: 가능하면 다른 장비 권장. 꼭 가져오면 **E2B only, best-effort**
- 16GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-e4b`
- 32GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-e4b` 또는 `google/gemma-4-26b-a4b`
- 36GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-26b-a4b` 또는 `google/gemma-4-31b`
- ChromeOS: Ollama + `gemma4:e2b`

### 가장 비추천하는 조합

- 8GB Chromebook + 큰 모델
- Intel Mac + LM Studio
- 행사 당일 현장에서 처음 모델 다운로드

## Ollama 태그 관련 주의

- 2026-04-20 기준 Ollama 라이브러리 페이지에서 `gemma4:latest`는 9.6GB, 128K 컨텍스트의 E4B 계열로 표시됩니다.
- 다만 `latest` 태그는 향후 변경될 수 있으므로, 행사 준비용으로는 반드시 `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b`처럼 명시적 태그를 사용하는 것을 권장합니다.
- 도구별 배포 포맷이 달라 다운로드 크기와 표시 용량은 서로 다를 수 있습니다.

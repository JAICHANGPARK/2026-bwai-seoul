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
- Gemini CLI에서 Gemma 4 preview 모델 선택이나 Gemma 라우팅 실험 기능을 미리 확인해 보고 싶다면 [Gemini CLI Gemma 4 Preview 및 Gemma 라우팅 사전 준비 가이드](./15-gemini-cli-gemma-routing-prep.md) 문서를 확인해 주세요.

## Ollama와 LM Studio 비교

| 항목 | Ollama | LM Studio |
| --- | --- | --- |
| 사용하기 좋은 경우 | 개발자, CLI/API 선호 | 개발자, 비개발자 모두 / GUI 선호 |
| 설치 방식 | 앱 + CLI 중심 | 데스크톱 앱 중심 |
| 모델 받기 | `ollama pull` 또는 `ollama run` | Discover 탭에서 검색/다운로드 |
| 사용 방식 | 터미널, 로컬 API, 자동화에 강함 | 채팅 UI, 모델 관리 UI, 로컬 서버에 강함 |
| 오프라인 사용 | 모델 다운로드 후 로컬 실행 | 모델 다운로드 후 완전 오프라인 사용 가능 |
| macOS 지원 | Apple Silicon 지원, Intel Mac은 CPU 전용 | Apple Silicon만 지원, Intel Mac 미지원 |
| Windows 지원 | 네이티브 앱, NVIDIA/AMD GPU 지원 | x64/ARM 지원, 16GB+ RAM 권장 |
| ChromeOS | Linux 개발 환경에서 가능하지만 느릴 수 있음 | 공식 권장 경로 아님 |
| 행사 권장도 | 보조 또는 고급/CLI 경로 | 기본 권장 |

## 운영체제별 빠른 추천

| 운영체제 | 가장 권장 | 대안 | 비고 |
| --- | --- | --- | --- |
| Windows | LM Studio | Ollama | 하나만 설치한다면 LM Studio를 권장합니다. |
| macOS Apple Silicon | LM Studio | Ollama | LM Studio는 Apple Silicon 전용이며, GGUF를 기본으로 쓰고 필요하면 MLX도 활용할 수 있습니다. |
| macOS Intel | Ollama | 없음에 가까움 | LM Studio 데스크톱 앱은 Intel Mac 미지원입니다. |
| Linux (Ubuntu) | LM Studio | Ollama | GUI 설치가 가능하면 LM Studio를 우선 권장합니다. |
| ChromeOS | Ollama | 가능하면 다른 노트북 준비 | Linux 개발 환경에서는 로컬 LLM용 전용 GPU/VRAM 가속을 기대하기 어렵습니다. |

## 메모리별 권장 모델

아래 권장은 행사 당일 안정적인 진행을 기준으로 잡았습니다.
모델 페이지의 표시 크기나 최소 메모리는 더 낮게 보일 수 있지만, 실제로는 운영체제와 브라우저도 메모리를 함께 사용하므로 여유가 필요합니다.

| 노트북 메모리 | 행사 권장 모델 | 권장 도구 | 안내 |
| --- | --- | --- | --- |
| 8GB | `gemma4:e2b` / `google/gemma-4-e2b` | E2B만 시도 | 8GB는 공식 권장 사양보다 낮아 LM Studio/Ollama 어느 쪽도 무난한 기본 조합으로 보기 어렵습니다. E2B만 시도하고, 가능하면 16GB 이상 노트북을 권장합니다. 실제로는 속도가 많이 느리거나 시스템이 일시적으로 멈춘 것처럼 보일 수 있습니다. |
| 16GB | `gemma4:e4b` / `google/gemma-4-e4b` | LM Studio 우선 | 가장 무난한 참가 사양입니다. 실패 시 E2B로 낮추면 됩니다. |
| 32GB | `gemma4:e4b`, `gemma4:26b` / `google/gemma-4-26b-a4b` | LM Studio 우선 | 속도와 안정성을 우선하면 E4B, 더 큰 모델을 원하면 26B A4B를 선택하세요. |
| 36GB | `gemma4:26b`, `gemma4:31b` / `google/gemma-4-31b` | LM Studio 우선 | 31B도 가능하지만, 반응 속도는 26B A4B가 더 나을 수 있습니다. |

## `A4B`는 무슨 뜻인가요?

`26B A4B`에서 `26B`는 모델 전체 파라미터 규모를 뜻하고, `A4B`는 **답을 만들 때 실제로 계산에 참여하는 부분이 약 4B 규모**라는 뜻입니다.

이 방식은 `MoE(Mixture-of-Experts)` 구조라고 부릅니다. 모델 안에 여러 "전문가" 부분이 있고, 답을 만들 때마다 필요한 일부 전문가만 골라 계산하는 방식입니다. 공식 모델 카드 기준으로는 총 파라미터가 `25.2B`, 실제 계산에 참여하는 파라미터가 `3.8B`입니다.

그래서 `26B A4B`는 `31B`처럼 모든 주요 계산 블록을 함께 쓰는 모델보다 더 빠르게 느껴질 수 있습니다. 다만 모델 파일은 전체 26B 규모를 메모리에 올려야 하므로, **4B 모델처럼 가볍게 실행된다는 뜻은 아닙니다.** 32GB 이상 장비에서 권장하는 이유가 이 점 때문입니다.

8GB 추가 메모:

- Windows와 macOS에서 LM Studio 공식 권장 메모리는 16GB 이상입니다.
- 따라서 8GB는 "무난한 기본 조합"이 아니라, 작은 모델(E2B)만 시도하는 최소 준비로 이해해 주세요.
- 8GB Apple Silicon Mac도 E2B/E4B 실행 중 속도가 크게 떨어지거나 시스템이 멈춘 것처럼 보일 수 있으므로, 안정적인 실습 장비로 보기 어렵습니다.
- 8GB 장비로 참석하는 경우에는 작은 컨텍스트, 브라우저 탭 최소화, 다른 앱 종료를 전제로 준비해 주세요.

## 로컬 모델 크기 참고

LM Studio Gemma 4 모델 페이지 기준 표시 크기:

- `google/gemma-4-e2b`: 4.20GB
- `google/gemma-4-e4b`: 5.90GB
- `google/gemma-4-26b-a4b`: 17.00GB
- `google/gemma-4-31b`: 19.00GB

Ollama Gemma 4 태그 페이지 기준으로는 기본 태그가 `gemma4:e2b` 7.2GB, `gemma4:e4b` 9.6GB, `gemma4:26b` 18GB, `gemma4:31b` 20GB로 표시됩니다.

이번 핸즈온 권장은 위 표시 크기보다 여유 있게 잡았습니다. 모델 크기 외에도 실행 도구, 긴 대화 컨텍스트, 브라우저, 운영체제가 메모리를 함께 사용합니다.

## 어떤 모델을 미리 받아두면 좋을까?

행사 전에 미리 받아 둘 모델은 아래처럼 고르면 됩니다.

중요:

- 이번 핸즈온은 **채팅 / 질의응답 / 에이전트 흐름**이 중심이므로, 가능하면 **instruction-tuned (`-it`) 또는 chat-ready 모델**을 받으세요.
- Hugging Face나 `llama.cpp` 예시에서는 보통 `gemma-4-...-it` 처럼 보입니다.
- Ollama는 `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b` 같은 런타임 태그를 쓰므로, 사용자가 별도로 `-it` 접미사를 고를 필요는 없습니다.
- LM Studio는 모델 목록 이름이 `google/gemma-4-e4b`처럼 더 짧게 보일 수 있으므로, **채팅/실습용 instruction-tuned 또는 chat-ready 항목인지** 설명을 함께 확인해 주세요.

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

### 메모리별 추천

- 8GB: 가능하면 다른 장비 권장. 꼭 가져오면 **E2B만 시도, 속도 저하 감안**
- 16GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-e4b`
- 32GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-e4b` 또는 `google/gemma-4-26b-a4b`
- 36GB: LM Studio + **chat-ready / instruction-tuned** `google/gemma-4-26b-a4b` 또는 `google/gemma-4-31b`
- ChromeOS: Ollama + `gemma4:e2b`

### 가장 비추천하는 조합

- 8GB Chromebook + 큰 모델
- Intel Mac + LM Studio
- 행사 당일 현장에서 처음 모델 다운로드

### Gemini CLI Gemma 기능은 별도 선택 경로

Gemini CLI의 Gemma 기능은 현재 두 가지로 나눠서 봐야 합니다.

- `v0.41.0-preview.0` 이상 preview: `experimental.gemma`를 켜면 Gemma 4 모델 선택을 실험적으로 확인할 수 있습니다.
- `gemini gemma` / `gemini gemma setup`: LiteRT-LM으로 Gemma 3 기반 `gemma3-1b-gpu-custom`을 내려받아 로컬 라우팅 판단에 씁니다.

즉, preview에서 Gemma 4 모델을 선택할 수 있어도 `gemini gemma setup`이 Gemma 4 모델을 로컬로 내려받는다는 뜻은 아닙니다.
또한 `/model` 목록에 Gemma 4가 보여도 실제 호출 권한은 계정, API 키, 조직의 Preview Release Channel 설정에 따라 막힐 수 있습니다.

따라서 행사 기본 준비는 여전히 아래 중 하나를 먼저 끝내세요.

- LM Studio에서 Gemma 4 모델 다운로드 및 채팅 1회 성공
- Ollama에서 `gemma4:e2b` 또는 `gemma4:e4b` 실행 성공

Gemini CLI를 이미 쓰고 있거나 CLI 실험 기능까지 확인하고 싶은 경우에만 [Gemini CLI Gemma 4 Preview 및 Gemma 라우팅 사전 준비 가이드](./15-gemini-cli-gemma-routing-prep.md)를 추가로 보면 됩니다.

## Ollama 태그 관련 주의

- 2026-04-27 기준 Ollama Gemma 4 태그 페이지에는 29개 태그가 표시됩니다.
- `gemma4:latest`는 현재 9.6GB, 128K 컨텍스트의 E4B 계열로 표시됩니다.
- `latest`는 향후 바뀔 수 있으므로, 사전 준비용으로는 `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b`처럼 명시적 태그를 사용하세요.
- `*-cloud`, `*-mlx-*`, `*-mxfp8`, `*-nvfp4`, `*-q8_0` 같은 변형 태그는 목적을 알고 선택할 때만 사용하세요.
- 도구별 배포 포맷이 달라 다운로드 크기와 표시 용량은 서로 다를 수 있습니다.

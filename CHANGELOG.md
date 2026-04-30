# CHANGELOG

Build with AI Seoul 2026 세션 **Build Your Own AI Office with Gemma 4** 사전 준비 문서의 주요 변경 이력입니다.

## 2026-05-01

### 추가

- `docs/17-faq.md`를 추가해 자주 헷갈리는 질문을 한곳에서 확인할 수 있도록 정리했습니다.
- `docs/15-gemini-cli-gemma-routing-prep.md`를 추가해 Gemini CLI preview, Gemma 4 모델 선택, Gemma 로컬 라우팅 준비 흐름을 별도 문서로 분리했습니다.
- Gemini CLI가 무엇인지, 로컬 Gemma 라우팅이 무엇인지, `gemini gemma setup`이 실제로 어떤 모델을 내려받는지 설명을 보강했습니다.
- Gemma 4 preview 모델은 목록에서 선택 가능해도 계정/API 키/조직 설정에 따라 실제 호출이 막힐 수 있다는 주의사항을 추가했습니다.
- `docs/14-gemma4-architecture-deep-dive.md`에 Dense, MoE, expert routing, RoPE, Dual RoPE, hybrid attention, GQA, shared KV cache 설명을 확장했습니다.
- `docs/04-gguf-mlx-llamacpp-explainer.md`에 FP32, BF16, FP16, 4-bit, NVFP4, GPU 세대별 숫자 타입 지원 차이를 설명하는 섹션을 추가했습니다.
- `instruction-tuned` 모델과 `base/pretrained` 모델의 차이를 개념 문서와 FAQ에 추가했습니다.

### 변경

- 문서 순서를 조정해 Gemini CLI 사전 준비 문서를 15번, 트러블슈팅과 최종 체크 문서를 16번, FAQ를 17번으로 정리했습니다.
- `README.md`와 `gemma4-local-setup-guide.md`의 문서 목록을 최신 17개 문서 구성에 맞게 갱신했습니다.
- 모델 선택 안내를 `instruction-tuned / chat-ready` 계열 기준으로 명확히 바꿨습니다.
- Hugging Face 공식 Gemma 4 모델 예시로 `google/gemma-4-E2B-it`, `google/gemma-4-E4B-it`, `google/gemma-4-26B-A4B-it`, `google/gemma-4-31B-it`를 안내했습니다.
- `base`나 `pretrained`로 표시된 모델은 모델 연구나 파인튜닝 출발점에는 의미가 있지만, 이번 핸즈온 기본 준비용으로는 권장하지 않는다고 정리했습니다.
- `B` 표기를 GB가 아니라 billion parameters, 즉 10억 개 단위의 파라미터 수로 설명하도록 보강했습니다.
- `26B A4B`가 4B 모델처럼 가볍다는 뜻이 아니라, 전체 26B 규모 모델을 메모리에 올리되 추론 시 약 4B 규모가 활성화되는 MoE 구조라는 점을 명확히 했습니다.
- “파라미터 수 나누기 4” 같은 표현 대신 “모델 추론에 필요한 메모리 계산 방법”으로 설명 방식을 바꿨습니다.
- 추론 메모리를 `모델 가중치 + KV cache + 입력/출력 처리 메모리 + 실행 도구 오버헤드`로 나눠 설명했습니다.
- NVFP4를 단순 양자화 이름이 아니라 `4-bit floating point data type + block scaling + NVIDIA 하드웨어/런타임 지원`으로 설명했습니다.
- NVIDIA `Gemma-4-31B-IT-NVFP4` 모델은 24GB GPU에서 항상 안정적으로 된다는 뜻이 아니라, 짧은 context와 특정 런타임 조건이 붙은 고급 실험 경로로 안내했습니다.
- 한국어 문장을 핸즈온을 준비하는 사람이 직접 읽는 문서 톤에 맞게 다듬었습니다.

### 수정

- `Gemini CLI Gemma` 안내에서 `gemini gemma setup`이 Gemma 4 로컬 채팅 모델 설치가 아니라 Gemma 3 기반 로컬 모델 라우터 설정이라는 점을 바로잡았습니다.
- Gemini CLI preview에서 Gemma 4 모델을 선택할 수 있어도 실제 메시지 전송 시 “access 없음” 오류가 날 수 있다는 점을 추가했습니다.
- `latest` 태그처럼 나중에 바뀔 수 있는 모델 태그는 사전 준비 기본값으로 쓰지 않도록 안내했습니다.
- LM Studio에서 모델 이름이 짧게 보일 수 있으므로 모델 카드나 설명에서 `chat-ready`, `instruction-tuned`, `instruct` 계열인지 확인하도록 수정했습니다.
- `참가자`, `참석자`, `기본 경로`처럼 독자 입장에서 어색하게 보일 수 있는 표현을 줄이고, 직접 안내하는 문장으로 정리했습니다.
- `output/pdf/gemma4-hands-on-prep-guide.pdf`를 최신 문서 기준으로 다시 생성했습니다.

## 2026-04-30

### 추가

- Gemma 4 로컬 실행 사전 준비를 위한 기본 문서 세트를 구성했습니다.
- 운영체제별 준비 문서, 메모리 기준 모델 선택 문서, LM Studio/Ollama/llama.cpp/MLX 설치 문서를 추가했습니다.
- OpenCode, Hermes Agent, Pi 경량 코딩 에이전트 관련 안내 문서를 추가했습니다.
- Gemma 4 벤치마크와 코딩 에이전트 기대치를 정리했습니다.
- 전체 안내 문서 `gemma4-local-setup-guide.md`와 PDF 생성 스크립트를 마련했습니다.

### 변경

- 8GB, 16GB, 32GB, 36GB 장비별 권장 모델을 정리했습니다.
- 처음 준비하는 경우 LM Studio를 기본 경로로 안내하되, ChromeOS와 Intel Mac은 Ollama 중심으로 보도록 정리했습니다.
- 현장 네트워크에 의존하지 않도록 모델 다운로드와 1회 실행 테스트를 행사 전에 끝내도록 강조했습니다.

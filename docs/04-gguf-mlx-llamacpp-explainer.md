# GGUF, MLX, llama.cpp 개념 설명

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `GGUF`, `MLX`, `llama.cpp`가 무엇인지 헷갈리는 참가자
- LM Studio에서 왜 어떤 모델은 `GGUF`, 어떤 모델은 `MLX`로 보이는지 알고 싶은 참가자
- Apple Silicon Mac과 Windows/Linux에서 어떤 실행 경로가 다른지 이해하고 싶은 참가자

## 먼저 아주 짧게 정리

- `GGUF`: **모델 파일 포맷**
- `llama.cpp`: **로컬 LLM 실행 엔진 / 런타임**
- `MLX`: **Apple Silicon용 머신러닝 프레임워크**

즉:

- `GGUF`는 **파일**
- `llama.cpp`는 그 파일을 **실행하는 쪽**
- `MLX`는 Apple Silicon에서 모델을 실행하는 **다른 경로**

## 가장 중요한 오해 하나

`GGUF`, `MLX`, `llama.cpp`는 같은 종류의 단어가 아닙니다.

- `GGUF`는 파일 포맷입니다.
- `llama.cpp`는 추론 엔진입니다.
- `MLX`는 Apple의 프레임워크이자 그 위에서 돌아가는 실행 생태계입니다.

예를 들면:

- 같은 Gemma 4 모델도 `GGUF` 버전이 있을 수 있고
- Apple Silicon에서는 `MLX` 버전이 따로 있을 수 있습니다.

즉, **같은 모델이 여러 실행 포맷/런타임으로 제공될 수 있다**고 이해하면 됩니다.

## GGUF란?

GGUF 공식 문서 기준:

- GGUF는 **GGML 및 GGML 기반 실행기에서 추론용 모델을 저장하는 파일 포맷**입니다.
- 빠른 로딩, `mmap` 친화성, 단일 파일 배포, 메타데이터 포함을 목표로 설계되었습니다.
- 보통 모델은 처음에 PyTorch 같은 프레임워크에서 학습되고, 이후 로컬 추론용으로 GGUF로 변환되어 배포됩니다.

쉽게 말하면:

- Hugging Face 원본 체크포인트를
- 로컬 PC에서 다루기 쉬운 형태로 바꾼
- **로컬 실행용 파일 포맷**

이라고 보면 됩니다.

참가자 관점에서 중요한 점:

- Windows/Linux에서 로컬 LLM을 돌릴 때 가장 흔히 보는 포맷 중 하나가 `GGUF`입니다.
- LM Studio, Ollama, llama.cpp 같은 도구와 함께 자주 등장합니다.
- `Q4`, `Q5`, `Q8` 같은 양자화 표기가 붙은 GGUF 모델을 많이 보게 됩니다.

## llama.cpp란?

llama.cpp 공식 README 기준:

- llama.cpp는 **C/C++ 기반 LLM inference 엔진**입니다.
- 최소한의 설정으로 다양한 하드웨어에서 로컬/클라우드 추론을 할 수 있도록 만드는 것이 목표입니다.
- Apple Silicon, x86, NVIDIA GPU, AMD GPU 등 여러 백엔드를 지원합니다.
- OpenAI 호환 API 서버(`llama-server`)도 제공할 수 있습니다.

이름 때문에 오해하기 쉬운데:

- `llama.cpp`는 **Llama 모델만 실행하는 도구가 아닙니다.**
- 실제로 Gemma, Qwen, Mistral 등 `llama.cpp` 호환 모델도 많이 실행합니다.

참가자 관점에서 쉽게 말하면:

- `GGUF 파일을 실제로 돌려주는 대표적인 실행 엔진`

입니다.

정리하면:

- LM Studio는 문서상 **GGUF 모델을 `llama.cpp`로 실행**

라고 이해하면 큰 흐름을 잡는 데 도움이 됩니다.

## MLX란?

Apple MLX 공식 README 기준:

- MLX는 **Apple Silicon용 머신러닝 프레임워크**입니다.
- CPU와 GPU를 아우르는 **unified memory** 구조를 활용합니다.
- Python, C++, C, Swift API를 제공합니다.

LLM 관점에서 더 직접적인 것은 `mlx-lm` 입니다.

Apple `mlx-lm` 공식 README 기준:

- `mlx-lm`은 **Apple Silicon에서 LLM을 실행하고 fine-tuning 하는 패키지**입니다.
- Hugging Face 모델을 불러오고
- 양자화하고
- MLX 형식으로 변환하고
- LoRA/QLoRA fine-tuning도 할 수 있습니다.

즉, 참가자 관점에서는:

- `MLX`는 Apple Silicon 전용 경로
- `MLX 모델`은 Apple Silicon에서 잘 맞는 실행 방식

으로 이해하면 됩니다.

## GGUF와 MLX는 어떻게 다른가요?

| 항목 | GGUF | MLX |
| --- | --- | --- |
| 성격 | 로컬 추론용 모델 파일 포맷 | Apple Silicon용 프레임워크/실행 생태계 |
| 대표 실행 경로 | `llama.cpp`, LM Studio, Ollama | MLX, `mlx-lm`, LM Studio(Apple Silicon) |
| 운영체제 | macOS, Windows, Linux 전반 | 사실상 Apple Silicon 중심 |
| 참가자 관점 | 가장 흔한 범용 로컬 포맷 | Mac Apple Silicon에서만 고려할 선택지 |

핵심:

- `GGUF`는 더 범용적입니다.
- `MLX`는 Apple Silicon에 특화된 선택지입니다.

## LM Studio에서는 왜 둘 다 보이나요?

LM Studio 공식 문서 기준:

- LM Studio는 macOS, Windows, Linux에서 **`llama.cpp` 기반 GGUF 모델 실행**을 지원합니다.
- Apple Silicon Mac에서는 **Apple의 MLX 실행 경로**도 지원합니다.

그래서 LM Studio에서:

- Windows/Linux에서는 주로 `GGUF`
- Apple Silicon Mac에서는 `GGUF`와 `MLX` 둘 다

보일 수 있습니다.

## 참가자 입장에서는 무엇을 선택하면 되나요?

이번 핸즈온에서는:

- **Windows/Linux**: `GGUF` 중심으로 생각하면 됩니다.
- **Apple Silicon Mac**: `GGUF 기본`, `MLX는 옵션`

즉:

- 개념이 헷갈리면 그냥 **GGUF를 기본 선택지**로 보면 됩니다.
- Apple Silicon 사용자만 필요할 때 `MLX`를 추가로 이해하면 충분합니다.

## 왜 GGUF가 행사 기본 설명에 더 자주 나오나요?

이유는 단순합니다.

- 참가자 환경이 macOS만 있는 것이 아니고
- Windows/Linux/ChromeOS까지 같이 봐야 하며
- LM Studio, Ollama, llama.cpp 같은 로컬 도구에서 범용적으로 이해하기 쉬운 축이 `GGUF`이기 때문입니다.

그래서 이번 핸즈온에서는:

- `GGUF`를 기본 개념
- `MLX`를 Apple Silicon 추가 옵션

으로 이해하면 됩니다.

## llama.cpp는 행사에서 왜 알아두면 좋나요?

참가자가 꼭 직접 설치할 필요는 없지만, 아래를 이해하는 데 도움이 됩니다.

- 왜 GGUF 모델이 여러 로컬 도구에서 공통으로 보이는지
- 왜 `Q4`, `Q5`, `Q8` 같은 양자화 모델이 자주 나오는지
- 왜 OpenAI 호환 로컬 서버를 만들 수 있는지

즉, llama.cpp는 로컬 LLM 생태계에서 **기초 엔진 역할**을 하는 경우가 많습니다.

## 한 줄 정리

- `GGUF`: 범용 로컬 모델 파일
- `llama.cpp`: 그 파일을 돌려주는 대표 엔진
- `MLX`: Apple Silicon에서 쓰는 별도 최적화 경로

## 이번 핸즈온 기준 추천 해석

- 개념이 어렵다면 `GGUF 기본`으로 이해해도 충분합니다.
- Apple Silicon Mac 사용자만 `MLX는 선택 사항`으로 추가 이해하면 됩니다.
- `llama.cpp`는 참가자가 직접 만지는 도구가 아니더라도, LM Studio/GGUF를 이해하는 배경지식으로 알면 좋습니다.

## 같이 보면 좋은 문서

- [LM Studio 설치 가이드](./05-lm-studio-setup.md)
- [Apple Silicon + MLX 안내](./08-apple-silicon-mlx.md)
- [메모리 기준으로 Gemma 4 모델 고르는 방법](./03-memory-based-model-selection.md)

## 참고 링크

- [GGUF spec (ggml)](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
- [llama.cpp README](https://github.com/ggml-org/llama.cpp)
- [Apple MLX README](https://github.com/ml-explore/mlx)
- [Apple MLX LM README](https://github.com/ml-explore/mlx-lm)
- [LM Studio Docs](https://lmstudio.ai/docs)

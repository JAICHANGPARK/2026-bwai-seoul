# GGUF, MLX, llama.cpp 개념 설명

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `GGUF`, `MLX`, `llama.cpp`가 무엇인지 헷갈리는 분
- LM Studio에서 왜 어떤 모델은 `GGUF`, 어떤 모델은 `MLX`로 보이는지 알고 싶은 분
- Apple Silicon Mac과 Windows/Linux에서 실행 방식이 어떻게 다른지 이해하고 싶은 분

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

## instruction-tuned와 base 모델은 무엇이 다른가요?

모델을 받을 때 `-it`, `instruct`, `instruction-tuned`, `chat-ready`, `base`, `pretrained` 같은 표현을 보게 됩니다.  
이것은 `GGUF`, `MLX`, `Q4`, `NVFP4`처럼 파일 포맷이나 숫자 저장 방식을 말하는 것이 아니라, **모델이 어떤 방식으로 훈련되어 어떤 행동을 하도록 준비되었는지**를 말합니다.

Gemma 4 공식 Hugging Face 컬렉션도 같은 크기에서 두 계열을 나눠 제공합니다.

| 계열 | 예시 | 성격 |
| --- | --- | --- |
| base / pre-trained | `google/gemma-4-26B-A4B` | 원본에 가까운 사전학습 모델 |
| instruction-tuned | `google/gemma-4-26B-A4B-it` | 채팅과 지시 수행에 맞게 추가 학습된 모델 |

`base` 또는 `pretrained` 모델은 대량의 텍스트, 코드, 이미지 같은 데이터를 보고 다음 토큰을 예측하도록 학습한 모델입니다.  
이 단계에서 모델은 언어와 지식, 코드 패턴, 시각 정보를 폭넓게 배웁니다. 하지만 "질문에 답하기", "요청을 단계적으로 수행하기", "대화 형식을 지키기" 같은 행동을 안정적으로 하도록 별도 조정된 상태는 아닙니다.

그래서 base 모델에 바로 질문을 던지면 답을 하기도 하지만, 질문을 이어 쓰는 식으로 반응하거나, 출력 형식이 흔들리거나, 대화형 앱에서 기대하는 역할 구분을 잘 따르지 못할 수 있습니다. base 모델은 주로 모델 연구, 자체 instruction tuning, 도메인 fine-tuning, 평가 실험을 시작할 때 쓰는 출발점에 가깝습니다.

`instruction-tuned` 모델은 base 모델을 바탕으로 사람이 쓴 지시문과 기대 답변 형식에 더 맞도록 추가 훈련한 모델입니다. Google의 Gemma 실행 문서도 처음 시작할 때는 instruction-tuned(IT) 모델을 추천합니다. IT 모델은 별도 추가 학습 없이도 자연어 요청에 답하기 좋고, 채팅 UI나 로컬 에이전트 흐름에 바로 연결하기 쉽습니다.

차이를 실습 관점에서 보면 아래와 같습니다.

| 구분 | base / pre-trained | instruction-tuned / chat-ready |
| --- | --- | --- |
| 주된 목적 | 모델 연구, 파인튜닝 출발점 | 바로 채팅, 질의응답, 지시 수행 |
| 프롬프트 반응 | 텍스트를 이어 쓰는 성격이 강함 | 요청에 대한 답변을 만들도록 조정됨 |
| 대화 형식 | 직접 템플릿을 맞추거나 추가 튜닝이 필요할 수 있음 | 도구가 제공하는 chat template과 잘 맞음 |
| 이번 핸즈온 적합도 | 기본 준비용으로는 비추천 | 기본 준비용으로 추천 |

중요한 점은 **instruction-tuned 여부와 양자화 여부는 서로 다른 축**이라는 것입니다.

예를 들어 아래 표현들은 서로 다른 질문에 답합니다.

- `google/gemma-4-26B-A4B-it`: 26B A4B의 instruction-tuned 모델인가?
- `Q4`, `Q5`, `Q8`, `NVFP4`: 숫자를 어떤 크기와 정밀도로 저장했는가?
- `GGUF`, `MLX`, `Safetensors`: 어떤 파일 포맷이나 실행 생태계로 배포되는가?

즉, 같은 instruction-tuned 모델도 GGUF로 변환될 수 있고, 4-bit로 양자화될 수 있습니다. 반대로 base 모델도 GGUF나 양자화 파일로 배포될 수 있습니다.  
이번 핸즈온에서는 먼저 **instruction-tuned / chat-ready 계열인지** 확인하고, 그다음에 내 장비에 맞는 크기와 양자화 방식을 고르면 됩니다.

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

실습에서 중요한 점:

- Windows/Linux에서 로컬 LLM을 돌릴 때 가장 흔히 보는 포맷 중 하나가 `GGUF`입니다.
- LM Studio, Ollama, llama.cpp 같은 도구와 함께 자주 등장합니다.
- `Q4`, `Q5`, `Q8` 같은 양자화 표기가 붙은 GGUF 모델을 많이 보게 됩니다.

## FP32, BF16, FP16, 4-bit는 무엇인가요?

LLM 모델은 아주 많은 숫자로 이루어져 있습니다.  
이 숫자 하나하나를 어떤 형식으로 저장하고 계산할지에 따라 모델 크기와 실행 속도가 달라집니다.

자주 보는 표기는 아래처럼 이해하면 됩니다.

| 표기 | 의미 | 파라미터 1개당 대략 크기 | 느낌 |
| --- | --- | --- | --- |
| `FP32` | 32-bit floating point | 4 bytes | 정확하지만 너무 큼 |
| `BF16` | bfloat16 | 2 bytes | LLM 원본 가중치에서 자주 쓰임 |
| `FP16` | 16-bit floating point | 2 bytes | GPU 추론에서 흔함 |
| `INT8` / `Q8` | 8-bit 양자화 | 1 byte 안팎 | 원본보다 작고 비교적 안정적 |
| `INT4` / `Q4` | 4-bit 양자화 | 0.5 byte 안팎 | 훨씬 작지만 품질/지원 차이 있음 |

Gemma 4를 FP32가 기본이라고 생각하면 메모리를 너무 크게 잡게 됩니다.  
공식 Transformers 설정은 BF16 계열로 보는 것이 맞고, LM Studio/Ollama에서 받는 로컬 모델은 보통 여기서 한 번 더 줄인 양자화 모델입니다.

예를 들어 31B 모델을 단순 계산하면:

```text
FP32: 31B x 4 bytes ≈ 124GB
BF16: 31B x 2 bytes ≈ 62GB
4-bit: 31B x 0.5 bytes ≈ 15.5GB + 오버헤드
```

즉, `31B`라는 이름만 보고 31GB라고 생각하면 안 됩니다.  
모델 이름의 `B`는 파라미터 수이고, 실제 파일 크기는 숫자 형식과 양자화 방식에 따라 달라집니다.

## BF16은 왜 많이 쓰나요?

`BF16`은 `bfloat16`의 줄임말입니다.  
FP32보다 메모리는 절반만 쓰면서, 숫자를 표현할 수 있는 범위는 FP32와 비슷하게 유지하는 16-bit 형식입니다.

FP16과 BF16은 둘 다 16-bit지만 성격이 다릅니다.

- `FP16`: 소수점 정밀도는 조금 더 좋지만, 표현 가능한 숫자 범위가 좁습니다.
- `BF16`: 소수점 정밀도는 낮지만, FP32와 비슷한 넓은 숫자 범위를 가집니다.

LLM에서는 계산 중 숫자가 매우 커지거나 작아질 수 있습니다.  
그래서 BF16은 FP32보다 훨씬 가볍고, FP16보다 안정적인 경우가 많습니다.

## 모델 추론에 필요한 메모리는 어떻게 계산하나요?

모델 추론에 필요한 메모리는 한 숫자로 딱 떨어지지 않습니다.  
대략 아래 항목을 더해서 생각하면 됩니다.

```text
추론 메모리 ≈ 모델 가중치 + KV cache + 입력/출력 처리 메모리 + 실행 도구 오버헤드
```

이 중에서 가장 큰 부분은 보통 **모델 가중치**입니다.  
가중치 메모리는 아래처럼 계산합니다.

```text
가중치 메모리 ≈ 파라미터 수 x 파라미터 1개당 저장 크기
```

예를 들어 26B 모델은 파라미터가 약 260억 개입니다.

```text
BF16: 26B x 2 bytes ≈ 52GB
4-bit: 26B x 0.5 bytes ≈ 13GB
```

BF16 기준 약 52GB였던 가중치가 4-bit에서는 약 13GB로 줄어듭니다.  
이 차이는 **파라미터 수가 줄어서가 아니라, 파라미터 하나를 저장하는 크기가 줄어서** 생깁니다.

```text
2 bytes -> 0.5 byte
가중치 메모리 약 1/4
```

하지만 실제 추론 메모리는 가중치 계산보다 더 듭니다.

- 양자화 메타데이터
- 일부 비양자화 레이어
- KV cache
- 긴 컨텍스트
- 이미지 입력
- 실행 도구와 GPU/CPU 오버헤드

이 붙기 때문입니다. 그래서 26B 4-bit 모델이 이론상 13GB 근처로 보이더라도, 실제 LM Studio/Ollama 표시 크기는 17~18GB처럼 보일 수 있습니다.

## NVIDIA GPU마다 지원 타입이 다른 이유

NVIDIA GPU마다 `FP16`, `BF16`, `INT8`, `FP8`, `FP4` 같은 지원이 다른 이유는 GPU 세대마다 Tensor Core가 처리할 수 있는 숫자 형식이 다르기 때문입니다.

중요한 구분:

```text
모델을 4-bit로 저장할 수 있음
≠
GPU가 4-bit를 전용 회로로 바로 빠르게 계산할 수 있음
```

많은 경우 4-bit 가중치를 읽은 뒤 실제 행렬 곱은 FP16/BF16으로 풀어서 계산합니다.  
그래서 같은 모델이라도 GPU 세대, CUDA, 드라이버, 실행 도구에 따라 속도와 지원 여부가 달라질 수 있습니다.

실습에서는 아래 정도만 기억하면 충분합니다.

- 최신 GPU일수록 더 다양한 저정밀 타입을 빠르게 처리할 가능성이 큽니다.
- 모델 파일의 `Q4`, `Q5`, `Q8` 표기는 저장 방식에 가깝습니다.
- 실제 계산이 어떤 타입으로 도는지는 실행 엔진과 하드웨어 지원에 따라 달라집니다.
- 타입 지원이 애매하면 작은 모델이나 더 보수적인 양자화 모델을 고르는 편이 안전합니다.

## NVFP4는 무엇인가요?

`NVFP4`는 NVIDIA가 Blackwell 세대 GPU를 중심으로 밀고 있는 **4-bit floating point 데이터 타입**입니다.  
NVIDIA 기술 블로그도 NVFP4를 low-precision inference를 위한 data type으로 설명하고, Hugging Face의 `Gemma-4-31B-IT-NVFP4` 모델 카드도 weights와 activations를 NVFP4 data type으로 양자화했다고 설명합니다.

다만 NVFP4를 "그냥 4-bit 숫자 하나"로만 이해하면 부족합니다.  
NVFP4는 **4-bit 값 + scale 정보 + 하드웨어 가속 방식**이 함께 묶인 micro-scaled FP4 데이터 타입에 가깝습니다.

즉, NVFP4는 아래 세 가지 성격을 같이 가집니다.

- 데이터 타입: 숫자를 4-bit floating point로 표현하는 방식
- 양자화 포맷: 원래 BF16/FP16 값을 NVFP4 값과 scale로 줄여 저장하는 방식
- 실행 경로: Blackwell Tensor Core가 이 형식을 빠르게 처리하도록 설계된 하드웨어 지원 방식

그래서 문서나 모델 카드에서 NVFP4를 볼 때는:

```text
NVFP4 = 4-bit floating point data type + block scaling + NVIDIA 하드웨어/런타임 지원
```

으로 이해하는 것이 가장 안전합니다.

일반적인 4-bit 양자화와 비슷하게 모델을 작게 만들지만, 단순히 숫자를 4-bit로 자르는 방식은 아닙니다.

NVFP4의 핵심은 **작은 블록마다 scale을 따로 두는 것**입니다.

- 4-bit 값 자체는 `1 sign bit + 2 exponent bits + 1 mantissa bit` 구조입니다.
- 값 16개마다 FP8(E4M3) scale을 공유합니다.
- tensor 전체에는 추가 FP32 scale을 한 번 더 적용합니다.

즉:

```text
원래 값 ≈ 4-bit 값 x 16개 단위 FP8 scale x tensor 단위 FP32 scale
```

이렇게 하면 4-bit처럼 작게 저장하면서도, 각 블록의 값 범위에 더 잘 맞출 수 있습니다. NVIDIA 기술 블로그 기준으로 NVFP4는 FP16 대비 약 3.5배, FP8 대비 약 1.8배 메모리 절감 효과를 목표로 합니다.

## Gemma 4 31B NVFP4는 왜 주목받나요?

NVIDIA는 `Gemma-4-31B-IT-NVFP4` 모델을 Hugging Face에 공개했습니다.  
공식 모델 카드 기준으로 이 모델은 Google의 Gemma 4 31B instruction-tuned 모델을 NVIDIA Model Optimizer로 NVFP4 양자화한 버전입니다.

주요 포인트:

- 31B dense 모델을 NVFP4로 줄인 버전
- weights와 activations가 NVFP4 data type으로 양자화된 버전
- 256K context window 명시
- text, image, video 입력 지원
- vLLM 런타임 기준
- NVIDIA Blackwell 호환성을 명시
- calibration에는 `cnn_dailymail` 데이터셋 사용
- 평가표에서 BF16 원본 대비 여러 벤치마크 손실이 0.5%p 미만으로 표시됨

Hugging Face 파일 정보에 `BF16`, `F8_E4M3`, `U8` 같은 tensor type이 함께 보일 수 있습니다.  
이것은 NVFP4가 4-bit 값만 단독으로 있는 구조가 아니라, FP8 scale이나 packing된 저장 표현을 함께 쓰는 구조이기 때문입니다. 모델 이름에 NVFP4가 붙어도 내부 파일에는 scale, metadata, 일부 보조 tensor가 같이 들어갈 수 있습니다.

다만 이 모델을 행사 기본 준비로 보기는 어렵습니다.

- 공식 모델 카드의 예시 serve 명령은 `--tensor-parallel-size 8`입니다.
- 모델 카드의 test hardware는 H100으로 표시되어 있습니다.
- Blackwell에서 가장 잘 맞도록 설계된 경로입니다.
- 24GB GPU에서 짧은 context로 가능하다는 이야기는 조건부로 봐야 합니다.
- 256K full context까지 한 장의 24GB GPU에서 안정적으로 된다는 뜻은 아닙니다.

따라서 실습 문서에서는 이렇게 이해하면 됩니다.

- **개념적으로:** NVFP4는 4-bit 양자화의 최신 고성능 경로 중 하나입니다.
- **실습 준비로:** LM Studio/Ollama의 E2B/E4B 또는 26B A4B 준비가 우선입니다.
- **고급 실험으로:** Blackwell/Hopper급 NVIDIA GPU, vLLM, Linux 환경이 있으면 별도 실험 항목으로 볼 수 있습니다.

## llama.cpp란?

llama.cpp 공식 README 기준:

- llama.cpp는 **C/C++ 기반 LLM inference 엔진**입니다.
- 최소한의 설정으로 다양한 하드웨어에서 로컬/클라우드 추론을 할 수 있도록 만드는 것이 목표입니다.
- Apple Silicon, x86, NVIDIA GPU, AMD GPU 등 여러 백엔드를 지원합니다.
- OpenAI 호환 API 서버(`llama-server`)도 제공할 수 있습니다.

이름 때문에 오해하기 쉬운데:

- `llama.cpp`는 **Llama 모델만 실행하는 도구가 아닙니다.**
- 실제로 Gemma, Qwen, Mistral 등 `llama.cpp` 호환 모델도 많이 실행합니다.

쉽게 말하면:

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

즉, 실습에서는:

- `MLX`는 Apple Silicon 전용 경로
- `MLX 모델`은 Apple Silicon에서 잘 맞는 실행 방식

으로 이해하면 됩니다.

## GGUF와 MLX는 어떻게 다른가요?

| 항목 | GGUF | MLX |
| --- | --- | --- |
| 성격 | 로컬 추론용 모델 파일 포맷 | Apple Silicon용 프레임워크/실행 생태계 |
| 대표 실행 경로 | `llama.cpp`, LM Studio, Ollama | MLX, `mlx-lm`, LM Studio(Apple Silicon) |
| 운영체제 | macOS, Windows, Linux 전반 | 사실상 Apple Silicon 중심 |
| 실습 기준 | 가장 흔한 범용 로컬 포맷 | Mac Apple Silicon에서만 고려할 선택지 |

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

## 무엇을 선택하면 되나요?

이번 핸즈온에서는:

- **Windows/Linux**: `GGUF` 중심으로 생각하면 됩니다.
- **Apple Silicon Mac**: `GGUF 기본`, `MLX는 옵션`

즉:

- 개념이 헷갈리면 그냥 **GGUF를 기본 선택지**로 보면 됩니다.
- Apple Silicon 사용자만 필요할 때 `MLX`를 추가로 이해하면 충분합니다.

## 왜 GGUF가 행사 기본 설명에 더 자주 나오나요?

이유는 단순합니다.

- 실습 환경이 macOS만 있는 것이 아니고
- Windows/Linux/ChromeOS까지 같이 봐야 하며
- LM Studio, Ollama, llama.cpp 같은 로컬 도구에서 범용적으로 이해하기 쉬운 축이 `GGUF`이기 때문입니다.

그래서 이번 핸즈온에서는:

- `GGUF`를 기본 개념
- `MLX`를 Apple Silicon 추가 옵션

으로 이해하면 됩니다.

## llama.cpp는 행사에서 왜 알아두면 좋나요?

꼭 직접 설치할 필요는 없지만, 아래를 이해하는 데 도움이 됩니다.

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
- `llama.cpp`는 직접 만지는 도구가 아니더라도, LM Studio/GGUF를 이해하는 배경지식으로 알면 좋습니다.

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
- [Google AI for Developers: Run Gemma](https://ai.google.dev/gemma/docs/run)
- [Google Gemma 4 Hugging Face collection](https://huggingface.co/collections/google/gemma-4)
- [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it)
- [NVIDIA Gemma-4-31B-IT-NVFP4](https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4)
- [NVIDIA Technical Blog: Introducing NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)

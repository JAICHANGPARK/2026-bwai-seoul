# 자주 묻는 질문

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 준비 범위

### 하나만 설치한다면 무엇을 설치하면 되나요?

대부분의 Windows, macOS Apple Silicon, Linux 사용자는 **LM Studio**를 먼저 설치하면 됩니다.

예외:

- ChromeOS 사용자는 Ollama를 우선 권장합니다.
- Intel Mac 사용자는 LM Studio 데스크톱 앱 대신 Ollama를 사용하세요.
- CLI/API 사용에 익숙하고 자동화까지 해 보고 싶다면 Ollama도 함께 설치하면 좋습니다.

### Intel Mac에서는 LM Studio를 쓸 수 없나요?

행사 준비 기준으로는 **쓰지 않는 것**으로 안내합니다.

공식 LM Studio 시스템 요구사항은 Mac에서 Apple Silicon을 요구하고, Intel Mac은 현재 지원 대상이 아니라고 안내합니다. Intel Mac을 쓰고 있다면 [Intel Mac 사용자 사전 준비 가이드](./18-intel-mac-prep.md)를 먼저 보고, Ollama로 `gemma4:e2b`를 준비하세요.

워크샵 코드 실행 시에는 LM Studio 기본 포트 `1234`가 아니라 Ollama 포트와 모델명을 명시합니다.

```bash
bash run.sh --scenario translate --topic "short test" --tasks 3 --port 11434 --model gemma4:e2b
```

### Ollama와 LM Studio를 둘 다 설치해야 하나요?

둘 다 설치하면 좋지만 필수는 아닙니다.

- 처음 준비하는 경우: LM Studio 하나로 충분합니다.
- 개발자이거나 터미널 사용에 익숙한 경우: Ollama도 함께 설치하면 좋습니다.
- ChromeOS: Ollama 위주로 준비하세요.

행사 당일에는 설치보다 **이미 다운로드한 모델을 바로 실행할 수 있는 상태**가 더 중요합니다.

### Hermes Agent, OpenCode, llama.cpp도 꼭 준비해야 하나요?

아닙니다. 세 도구는 선택 사항입니다.

- 기본 실습: LM Studio 또는 Ollama만 준비해도 됩니다.
- 코딩 에이전트 흐름을 더 실험해 보고 싶은 경우: OpenCode, Hermes Agent를 추가로 보면 됩니다.
- 로컬 서버나 GGUF 실행을 직접 다뤄 보고 싶은 경우: llama.cpp를 보면 됩니다.

터미널, WSL2, 빌드 도구에 익숙하지 않다면 행사 전에는 LM Studio 준비에 집중하는 편이 안전합니다.

### Gemini CLI Gemma 기능도 필수인가요?

필수는 아닙니다.

Gemini CLI의 Gemma 기능은 기본 로컬 실행 준비와 별도 선택 경로입니다. preview에서 Gemma 4 모델 선택을 확인할 수 있지만, 계정/API 키/조직 설정에 따라 실제 호출 권한이 없을 수 있습니다.

또한 `gemini gemma setup`은 현재 Gemma 3 기반 로컬 라우팅 설정으로 이해해야 하며, Gemma 4 모델을 로컬로 내려받는 흐름과는 구분해 주세요.

## 모델 선택

### 내 노트북 메모리를 모르겠으면 어떻게 하나요?

운영체제 설정에서 메모리를 먼저 확인하세요.

- Windows: `설정 > 시스템 > 정보`
- macOS: `Apple 메뉴 > 이 Mac에 관하여`
- ChromeOS: `설정 > About ChromeOS` 또는 기기 사양 페이지
- Linux: 터미널에서 `free -h`

모르겠거나 애매하면 더 작은 모델을 선택하세요. 행사 준비에서는 큰 모델을 억지로 실행하는 것보다 작은 모델을 안정적으로 실행하는 것이 낫습니다.

### 8GB 노트북으로도 참여할 수 있나요?

가능은 하지만 권장 사양으로 보기는 어렵습니다.

- 가능하면 16GB 이상 노트북을 준비하세요.
- 8GB 장비라면 `E2B`만 미리 다운로드하세요.
- 브라우저 탭과 다른 앱을 최대한 닫고 테스트하세요.
- 응답이 매우 느리거나 시스템이 멈춘 것처럼 보일 수 있습니다.

8GB 장비로 사용하는 경우에는 행사 전에 반드시 1회 실행 테스트를 끝내야 합니다.

### 16GB 노트북이면 어떤 모델을 받으면 되나요?

`E4B`를 권장합니다.

- LM Studio: `google/gemma-4-e4b` 계열의 chat-ready / instruction-tuned 항목
- Ollama: `gemma4:e4b`

불안하면 `E2B`도 함께 받아 두면 좋습니다. 현장에서 문제가 생기면 작은 모델로 바로 바꿀 수 있습니다.

### instruction-tuned 모델을 받아야 하나요?

네. 이번 핸즈온 기본 준비는 **instruction-tuned / chat-ready 모델**을 기준으로 보세요.

Hugging Face의 Gemma 4 공식 컬렉션을 보면 같은 크기에서도 두 계열이 따로 있습니다.

| 계열 | 예시 | 이번 핸즈온 기준 |
| --- | --- | --- |
| base / pre-trained | `google/gemma-4-26B-A4B` | 기본 준비용으로 비추천 |
| instruction-tuned | `google/gemma-4-26B-A4B-it` | 기본 준비용으로 추천 |

`base`나 `pretrained`로 표시된 모델은 원본에 가까운 사전학습 모델입니다.  
대량의 텍스트, 코드, 이미지 같은 데이터를 보고 다음 토큰을 예측하도록 학습한 모델이라 언어와 패턴은 잘 배웠지만, 바로 대화하고 지시를 따르도록 조정된 모델은 아닙니다.

그래서 base 모델은 모델 연구, 자체 파인튜닝, instruction tuning 실험을 시작할 때 의미가 있습니다. 반면 이번 핸즈온처럼 채팅, 질의응답, 지시 수행, 로컬 에이전트 흐름을 바로 실습할 때는 답변 형식이나 지시 수행이 흔들릴 수 있습니다.

`instruction-tuned` 모델은 base 모델을 바탕으로 사람이 쓰는 요청과 기대 답변 형식에 맞게 추가 훈련된 모델입니다. Google의 Gemma 실행 문서도 처음 시작할 때는 IT 모델을 추천합니다. 별도 추가 학습 없이 자연어 요청에 응답하기 좋고, LM Studio나 Ollama 같은 채팅 도구에 연결하기 쉽습니다.

모델을 직접 고를 때는 아래 표현을 확인하세요.

- `-it`
- `instruct`
- `instruction-tuned`
- `chat-ready`

Gemma 4에서는 예를 들어 아래 이름을 기준으로 보면 됩니다.

- `google/gemma-4-E2B-it`
- `google/gemma-4-E4B-it`
- `google/gemma-4-26B-A4B-it`
- `google/gemma-4-31B-it`

LM Studio에서는 모델 이름이 짧게 보일 수 있으므로 모델 설명이나 모델 카드까지 확인하세요.  
Ollama의 `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b` 같은 기본 런타임 태그는 별도로 `-it`를 붙이지 않아도 됩니다.

헷갈리기 쉬운 점이 하나 더 있습니다. `-it` 여부는 모델의 **훈련 목적과 동작 방식**이고, `Q4`, `Q5`, `Q8`, `NVFP4`는 모델 숫자를 **얼마나 작게 저장했는지**에 관한 표기입니다. 즉 instruction-tuned 모델도 4-bit로 양자화될 수 있고, base 모델도 4-bit로 배포될 수 있습니다.

### 32GB 이상이면 무조건 큰 모델을 받는 게 좋나요?

아닙니다.

- 안정성과 속도 우선: `E4B`
- 더 큰 모델을 실험하고 싶음: `26B A4B`
- 36GB 이상이고 큰 모델을 시도하고 싶음: `26B A4B` 또는 `31B`

핸즈온에서는 모델 크기보다 실행 안정성과 응답 속도가 더 중요할 수 있습니다.

### `B`는 GB와 같은 뜻인가요?

아닙니다.

`B`는 `Billion`, 즉 10억 개를 뜻합니다. `26B`는 파일 크기가 26GB라는 뜻이 아니라, 모델 내부 파라미터가 대략 260억 개 규모라는 뜻입니다.

실제 다운로드 크기와 실행 중 메모리 사용량은 양자화 방식, 실행 도구, 컨텍스트 길이에 따라 달라집니다.

### 사용자가 받는 모델은 보통 양자화된 모델인가요?

네. LM Studio나 Ollama에서 일반 사용자가 받는 로컬 실행용 모델은 보통 원본 BF16 가중치 그대로가 아니라 **4-bit, 5-bit, 8-bit 등으로 양자화된 배포본**입니다.

그래서 모델 이름의 `26B`, `31B`는 파라미터 규모를 뜻하고, 다운로드 크기는 그 파라미터를 어떤 숫자 형식으로 저장했는지에 따라 달라집니다. 다만 양자화되어도 KV cache, 긴 컨텍스트, 이미지 입력, 실행 도구 오버헤드는 별도로 메모리를 사용합니다.

### `26B A4B`는 4B 모델처럼 가볍게 실행되나요?

아닙니다.

`A4B`는 답을 만들 때 실제 계산에 참여하는 부분이 약 4B 규모라는 뜻입니다. 하지만 전체 모델 파일은 26B 규모로 메모리에 올라가야 하므로, 4B 모델처럼 가볍게 실행된다는 뜻은 아닙니다.

그래서 `26B A4B`는 32GB 이상 장비에서 권장합니다.

### Gemma 4는 FP32가 기본인가요?

아닙니다.

Gemma 4를 FP32 기준으로 생각하면 필요한 메모리를 너무 크게 잡게 됩니다. 공식 Transformers 설정은 BF16 계열로 보는 것이 맞고, LM Studio/Ollama에서 받는 로컬 모델은 보통 4-bit, 5-bit, 8-bit처럼 더 작게 양자화된 버전입니다.

쉽게 계산하면:

```text
FP32: 파라미터 1개 = 4 bytes
BF16/FP16: 파라미터 1개 = 2 bytes
4-bit: 파라미터 1개 = 약 0.5 bytes
```

그래서 `31B` 모델도 FP32로 보면 가중치만 약 124GB지만, BF16이면 약 62GB, 4-bit 양자화면 그보다 훨씬 작아집니다.

### BF16은 무엇인가요?

`BF16`은 `bfloat16`의 줄임말입니다.  
모델 안의 숫자를 16-bit로 저장하는 형식입니다.

FP32와 비교하면 메모리를 절반만 씁니다.

```text
FP32: 4 bytes
BF16: 2 bytes
```

FP16과 BF16은 둘 다 16-bit지만, BF16은 FP32와 비슷한 넓은 숫자 범위를 유지합니다. 그래서 LLM에서는 FP32보다 가볍고 FP16보다 안정적인 경우가 많아 원본 가중치 형식으로 자주 쓰입니다.

### 모델 추론에 필요한 메모리는 어떻게 계산하나요?

대략 아래 항목을 더해서 생각하면 됩니다.

```text
추론 메모리 ≈ 모델 가중치 + KV cache + 입력/출력 처리 메모리 + 실행 도구 오버헤드
```

가장 큰 부분은 보통 모델 가중치입니다.  
가중치 메모리는 아래처럼 계산합니다.

```text
가중치 메모리 ≈ 파라미터 수 x 파라미터 1개당 저장 크기
```

예를 들어 26B 모델을 단순 계산하면:

```text
BF16: 26B x 2 bytes ≈ 52GB
4-bit: 26B x 0.5 bytes ≈ 13GB
```

이 차이는 파라미터 수가 줄어서가 아니라, 파라미터 하나를 저장하는 크기가 줄어서 생깁니다.

하지만 실제 실행에는 KV cache, 컨텍스트, 실행 도구 오버헤드가 추가됩니다. 그래서 4-bit 가중치 계산값보다 실제 필요한 메모리가 더 커질 수 있습니다.

### NVIDIA GPU마다 지원하는 타입이 다른 이유는 무엇인가요?

GPU 세대마다 Tensor Core가 처리할 수 있는 숫자 형식이 다르기 때문입니다.

예를 들어 어떤 GPU는 FP16은 잘 처리하지만 BF16은 약하거나, 최신 GPU는 FP8/FP4 같은 더 작은 타입을 더 잘 처리할 수 있습니다.

중요한 점은 아래입니다.

```text
모델 파일이 4-bit로 저장되어 있음
≠
GPU가 4-bit 전용 회로로 바로 계산함
```

실제로는 4-bit 가중치를 읽은 뒤 FP16/BF16으로 풀어서 계산하는 경우도 많습니다. 그래서 같은 모델이라도 GPU 세대, 드라이버, CUDA, 실행 도구에 따라 속도와 지원 여부가 달라질 수 있습니다.

### NVFP4는 무엇인가요?

`NVFP4`는 NVIDIA의 4-bit floating point 데이터 타입입니다.  
NVIDIA 기술 블로그는 NVFP4를 low-precision inference를 위한 data type으로 설명하고, `Gemma-4-31B-IT-NVFP4` 모델 카드도 weights와 activations가 NVFP4 data type으로 양자화되었다고 설명합니다.

다만 NVFP4는 4-bit 값만 쓰는 단순한 숫자 형식은 아닙니다.  
작은 값 묶음마다 scale을 붙여 원래 숫자 범위를 더 잘 복원하는 micro-scaled FP4 데이터 타입으로 이해하면 됩니다.

NVIDIA 설명 기준으로는:

- 4-bit 값은 `1 sign bit + 2 exponent bits + 1 mantissa bit` 구조
- 값 16개마다 FP8 scale 사용
- tensor 전체에는 FP32 scale을 한 번 더 적용
- scale overhead까지 포함하면 약 4.5 bits/value에 가까움

그래서 일반적인 4-bit 양자화보다 정확도를 더 잘 보존하면서 메모리를 크게 줄이는 것을 목표로 합니다.

정리하면:

```text
NVFP4 = 4-bit floating point data type + block scaling + NVIDIA 하드웨어/런타임 지원
```

입니다.

### Gemma 4 31B NVFP4는 24GB GPU에서 무조건 되나요?

무조건 된다고 보면 안 됩니다.

NVIDIA의 `Gemma-4-31B-IT-NVFP4` 모델은 31B dense 모델을 NVFP4로 줄인 고급 실험 경로입니다. 짧은 context의 everyday inference에서는 24GB GPU에서 가능하다는 사례가 있지만, 공식 모델 카드 기준으로는 vLLM, NVIDIA GPU, Linux, tensor parallel 설정 같은 조건이 붙습니다.

특히 256K full context, 이미지/비디오 입력, 큰 batch를 쓰면 KV cache와 activation 메모리가 커져 24GB를 넘길 수 있습니다.

이번 핸즈온 기준으로는:

- 기본 준비: LM Studio/Ollama에서 E2B/E4B 우선
- 고사양 실험: 26B A4B 또는 31B
- NVFP4: NVIDIA GPU와 vLLM에 익숙한 경우의 별도 고급 실험

으로 보는 것이 안전합니다.

### LM Studio에서 모델 이름에 `-it`가 안 보이면 잘못 받은 건가요?

반드시 그렇지는 않습니다.

LM Studio에서는 모델 이름이 `google/gemma-4-e4b`처럼 짧게 보일 수 있습니다. 이 경우 모델 설명이나 모델 카드에서 **chat-ready**, **instruction-tuned**, **instruct** 계열인지 확인하세요.

이번 핸즈온은 채팅과 실습 흐름이 중심이므로 base 모델보다는 instruction-tuned/chat-ready 모델을 권장합니다.

### Ollama에서 `gemma4:latest`를 받아도 되나요?

사전 준비용으로는 명시적 태그를 권장합니다.

- 8GB: `gemma4:e2b`
- 16GB: `gemma4:e4b`
- 32GB 이상: `gemma4:26b`
- 36GB 이상: `gemma4:26b` 또는 `gemma4:31b`

`latest`는 나중에 가리키는 모델이 바뀔 수 있으므로, 행사 준비 문서에서는 명시적 태그를 기준으로 안내합니다.

## 설치와 실행

### 행사 당일에 모델을 다운로드해도 되나요?

권장하지 않습니다.

모델 파일은 수 GB에서 20GB 안팎까지 커질 수 있습니다. 현장 네트워크 상황에 따라 다운로드만 오래 걸릴 수 있고, 60분 핸즈온 시간이 모델 다운로드로 끝날 수 있습니다.

행사 전에 아래 세 가지를 끝내 주세요.

- 도구 설치 완료
- 모델 다운로드 완료
- 최소 1회 실행 테스트 완료

### 디스크 공간은 얼마나 필요하나요?

최소 20GB, 가능하면 40GB 이상 여유 공간을 권장합니다.

여러 모델을 함께 받거나 LM Studio와 Ollama를 둘 다 쓰면 모델 파일이 각각 저장될 수 있습니다. 설치 전에 불필요한 대용량 파일을 정리해 두면 좋습니다.

### 모델을 한 번 다운로드하면 오프라인에서도 쓸 수 있나요?

대체로 가능합니다.

- LM Studio는 모델 다운로드 후 완전 오프라인 사용이 가능합니다.
- Ollama도 모델을 미리 받은 뒤에는 로컬 실행이 가능합니다.

다만 설치, 모델 검색, 최초 다운로드, 일부 런타임 업데이트는 인터넷이 필요할 수 있으므로 행사 전에 완료해 주세요.

### 준비가 끝났는지 어떻게 확인하나요?

아래 중 하나 이상이 성공하면 기본 준비는 된 상태로 봅니다.

- LM Studio: 앱 실행, 모델 다운로드, Chat 화면에서 응답 1회 성공
- Ollama: `ollama --version`, `ollama run gemma4:e2b` 또는 `ollama run gemma4:e4b` 성공
- llama.cpp: `llama-cli --version`, `llama-server --version` 확인
- Hermes Agent: `hermes version`, `hermes doctor` 확인
- Gemini CLI Gemma 4 preview: `gemini --version`, `/model`에서 모델 선택 가능 여부 확인

더 자세한 기준은 [트러블슈팅 / 최종 체크 / 참고 링크](./19-troubleshooting-and-final-check.md)를 확인해 주세요.

### Windows에서는 PowerShell과 WSL2 중 무엇을 써야 하나요?

기본 설치 확인은 PowerShell 기준으로 보면 됩니다.

- Ollama: PowerShell
- LM Studio CLI: PowerShell
- Gemini CLI: PowerShell 또는 사용 중인 터미널
- OpenCode: WSL 경로 권장
- Hermes Agent: WSL2 Ubuntu 셸 기준

Windows에서 모든 명령을 한 터미널에서 처리하려고 하면 헷갈릴 수 있습니다. 문서의 해당 도구 섹션에서 PowerShell인지 WSL2인지 먼저 확인하세요.

### ChromeOS에서도 같은 방식으로 따라가면 되나요?

ChromeOS는 예외가 많습니다.

- Linux 개발 환경을 켜야 합니다.
- 학교/회사 정책으로 Linux 사용이 막혀 있을 수 있습니다.
- 로컬 LLM용 전용 GPU/VRAM 가속을 기대하기 어렵습니다.
- LM Studio보다는 Ollama와 `E2B`를 권장합니다.

가능하면 Windows 또는 macOS 노트북을 함께 준비하는 편이 안전합니다.

### 모델 실행 중 노트북이 멈춘 것처럼 보이면 어떻게 하나요?

먼저 몇 분 정도 기다려 보세요. 작은 장비에서는 모델을 메모리에 올리는 동안 응답이 늦을 수 있습니다.

계속 문제가 있으면 아래 순서로 처리하세요.

1. 브라우저 탭과 다른 앱을 닫습니다.
2. 더 작은 모델로 바꿉니다.
3. 컨텍스트 길이와 동시 실행 작업을 줄입니다.
4. 가능하면 전원 어댑터를 연결합니다.
5. 그래도 어렵다면 16GB 이상 장비를 준비합니다.

### 현장에서 문제가 생기면 어떤 문서를 먼저 보면 되나요?

먼저 [트러블슈팅 / 최종 체크 / 참고 링크](./19-troubleshooting-and-final-check.md)를 보세요.

가장 빠른 복구 방법은 보통 아래 순서입니다.

1. 큰 모델 대신 `E2B` 또는 `E4B`로 낮추기
2. LM Studio 또는 Ollama 중 이미 성공한 도구로 돌아가기
3. 브라우저 탭과 무거운 앱 닫기
4. 다운로드가 안 된 모델은 현장에서 새로 받지 않기

## 기대치

### 로컬 Gemma 4가 클라우드 최신 모델만큼 빠르고 똑똑한가요?

항상 그렇지는 않습니다.

로컬 모델의 장점은 내 장비에서 직접 실행하고, 네트워크 의존성을 줄이며, 로컬 에이전트 흐름을 실험할 수 있다는 점입니다. 반면 최신 대형 클라우드 모델보다 느리거나, 긴 복잡한 작업에서 품질 차이가 날 수 있습니다.

이번 핸즈온에서는 로컬 모델을 직접 준비하고 실행하는 감각을 익히는 것을 우선합니다.

### 코딩 에이전트에 연결하면 바로 실무 수준으로 쓸 수 있나요?

작은 로컬 모델은 간단한 코드 설명, 짧은 수정, 로컬 도구 호출 실험에는 유용할 수 있습니다. 하지만 큰 코드베이스를 오래 분석하거나 복잡한 리팩터링을 안정적으로 맡기는 수준을 기대하면 무리가 있습니다.

코딩 에이전트 실험은 [Gemma 4 벤치마크와 코딩 에이전트 기대치](./09-gemma4-benchmarks-and-agent-expectations.md)를 먼저 보고 기대치를 맞추는 것을 권장합니다.

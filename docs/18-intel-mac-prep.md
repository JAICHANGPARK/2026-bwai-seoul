# Intel Mac 사용자 사전 준비 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 먼저 결론

Intel Mac 사용자는 이번 핸즈온을 **Ollama + 작은 Gemma 4 모델** 기준으로 준비하세요.

- LM Studio 데스크톱 앱은 공식 시스템 요구사항 기준으로 **Apple Silicon Mac만 지원**하며, Intel Mac은 지원 대상이 아닙니다.
- Ollama는 macOS에서 Intel Mac을 지원하지만, Intel Mac에서는 **CPU 전용**으로 동작합니다.
- 따라서 Intel Mac에서는 `gemma4:e2b`를 먼저 준비하고, 16GB 이상 장비에서 이미 `E2B`가 안정적으로 되는 경우에만 `gemma4:e4b`를 추가로 시도하세요.
- 모델 실행이 많이 느릴 수 있으므로 행사 전에 반드시 1회 실행 테스트를 끝내야 합니다.

## 내 Mac이 Intel인지 확인

가장 쉬운 방법:

1. Apple 메뉴를 엽니다.
2. `이 Mac에 관하여`를 선택합니다.
3. `Processor` 또는 `프로세서` 항목에 Intel CPU가 보이면 Intel Mac입니다.
4. `Chip` 항목에 M1/M2/M3/M4가 보이면 Apple Silicon Mac입니다. 이 경우 [Apple Silicon + MLX 안내](./08-apple-silicon-mlx.md)를 보면 됩니다.

터미널에서 확인하려면:

```bash
uname -m
sw_vers -productVersion
```

결과 해석:

- `x86_64`: Intel Mac
- `arm64`: Apple Silicon Mac

Ollama의 최신 macOS 문서는 macOS 14 Sonoma 이상을 요구합니다. Intel Mac이 macOS 14 이상으로 업데이트되지 않는 오래된 장비라면 행사 당일 기본 실습 장비로 쓰기 어렵습니다. 가능하면 다른 노트북을 준비하세요.

## Intel Mac 권장 준비 흐름

### 1. Ollama 설치

1. 공식 다운로드 페이지로 이동합니다: [Ollama macOS 다운로드](https://ollama.com/download)
2. `ollama.dmg`를 열고 Ollama 앱을 `Applications` 폴더로 옮깁니다.
3. Ollama 앱을 한 번 실행합니다.
4. 터미널을 새로 열고 설치를 확인합니다.

```bash
ollama --version
```

### 2. E2B 모델 먼저 다운로드

Intel Mac에서는 큰 모델보다 작은 모델을 안정적으로 실행하는 것이 중요합니다.

```bash
ollama pull gemma4:e2b
```

다운로드가 끝나면 바로 실행 테스트를 합니다.

```bash
ollama run gemma4:e2b
```

아래처럼 짧게 물어보세요.

```text
Build with AI Seoul 핸즈온 테스트입니다. 한 문장으로 자기소개해 주세요.
```

### 3. E4B는 선택 사항

16GB 이상 Intel Mac이고 `E2B`가 큰 문제 없이 동작하면 `E4B`를 추가로 받아볼 수 있습니다.

```bash
ollama pull gemma4:e4b
ollama run gemma4:e4b
```

다만 Intel Mac에서는 CPU 전용이라 `E4B`도 답변이 많이 느릴 수 있습니다. 행사 기본 준비는 `E2B` 성공을 기준으로 잡으세요.

### 4. 로컬 API 서버 확인

Ollama 앱이 실행 중이면 로컬 API는 보통 `http://127.0.0.1:11434`에서 동작합니다.

```bash
curl http://127.0.0.1:11434/v1/models
```

연결이 안 되면 Ollama 앱을 다시 실행하거나 아래 명령을 별도 터미널에서 실행합니다.

```bash
ollama serve
```

## 워크샵 코드 실행 시 차이

워크샵 실행 스크립트의 기본 포트는 LM Studio에 맞춘 `1234`입니다. Intel Mac에서 Ollama를 쓰는 경우에는 `--port 11434`와 `--model gemma4:e2b`를 같이 넘기세요.

```bash
cd workshop/01_starter
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 3 --port 11434 --model gemma4:e2b
```

성능이 낮으면 `--tasks 3`처럼 작은 값으로 시작하세요. 여러 Terminal 창이 동시에 모델을 호출하므로 Intel Mac에서는 `--tasks 10`이 버거울 수 있습니다.

## LM Studio 앱 실습 부분은 어떻게 따라가나요?

핸즈온 문서에는 LM Studio 앱 채팅 화면에서 프롬프트를 직접 넣어보는 단계가 있습니다. Intel Mac 사용자는 같은 프롬프트를 Ollama 터미널 세션에 붙여 넣어 확인하면 됩니다.

```bash
ollama run gemma4:e2b
```

그 다음 문서의 프롬프트를 그대로 붙여 넣습니다.

차이점:

- LM Studio의 `Chat` 화면 대신 터미널 대화창을 사용합니다.
- LM Studio 서버 포트 `1234` 대신 Ollama 포트 `11434`를 사용합니다.
- 모델 이름은 `google/gemma-4-e2b`가 아니라 `gemma4:e2b`입니다.

## Intel Mac에서 기대치를 낮춰야 하는 부분

- 응답 생성이 Apple Silicon Mac이나 GPU가 있는 Windows 노트북보다 많이 느릴 수 있습니다.
- 여러 agent를 동시에 실행하면 CPU와 메모리를 많이 써서 시스템이 멈춘 것처럼 보일 수 있습니다.
- 큰 모델(`26B`, `31B`)은 행사 준비용으로 권장하지 않습니다.
- 브라우저 탭, 영상 회의 앱, 무거운 개발 도구를 최대한 닫고 테스트하세요.
- 전원 어댑터를 연결한 상태로 실행하세요.

## 준비 완료 기준

아래가 되면 Intel Mac 기준 기본 준비는 된 상태로 봅니다.

```bash
ollama --version
ollama run gemma4:e2b
curl http://127.0.0.1:11434/v1/models
```

그리고 가능하면 워크샵 폴더에서 아래 명령도 행사 전에 한 번 실행해 보세요.

```bash
cd workshop/01_starter
uv sync
bash run.sh --scenario translate --topic "short test" --tasks 3 --port 11434 --model gemma4:e2b
```

## 그래도 어렵다면

아래 중 하나에 해당하면 Intel Mac을 기본 실습 장비로 쓰지 않는 편이 안전합니다.

- macOS 14 이상으로 업데이트할 수 없음
- 메모리가 8GB이고 `gemma4:e2b`도 매우 느리거나 자주 실패함
- 행사 전 `ollama run gemma4:e2b` 테스트를 성공하지 못함
- 워크샵 코드 실행 시 `--tasks 3`에서도 계속 실패함

이 경우 가능하면 Windows 노트북, Apple Silicon Mac, 또는 16GB 이상 장비를 준비하세요.

## 관련 문서

- [Ollama 설치 가이드](./06-ollama-setup.md)
- [하드웨어 / 운영체제 / 모델 선택 가이드](./01-hardware-and-model-selection.md)
- [트러블슈팅 / 최종 체크 / 참고 링크](./19-troubleshooting-and-final-check.md)
- [LM Studio System Requirements](https://lmstudio.ai/docs/app/system-requirements)
- [Ollama macOS 문서](https://docs.ollama.com/macos)

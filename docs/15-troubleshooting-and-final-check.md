# 트러블슈팅 / 최종 체크 / 참고 링크

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 문제 발생 시 바로 해볼 것

### Ollama

- `ollama --version`이 안 되면 앱 또는 설치 상태를 다시 확인
- 모델 로드 실패 시 더 작은 모델로 변경
  - `gemma4:e4b` -> `gemma4:e2b`
- 메모리 부족 시 브라우저 탭과 다른 앱 종료
- 너무 느리면 큰 모델 대신 E2B/E4B 사용

### LM Studio

- 앱이 켜지지만 모델이 안 돌면 런타임 상태 확인
  - `Cmd/Ctrl + Shift + R`
- 모델 로드 실패 시 더 작은 모델 선택
- 8GB 환경이면 `google/gemma-4-e2b`만 사용
- 8GB Mac/노트북에서 시스템이 멈춘 것처럼 보이면, 잠시 기다린 뒤 앱을 종료하고 브라우저 탭과 다른 앱을 먼저 줄인 다음 다시 시도
- Intel Mac이면 LM Studio 대신 Ollama 사용

### llama.cpp

- `llama-cli --version` 또는 `llama-server --version`이 안 되면 PATH 또는 설치 상태를 다시 확인
- 모델 경로 오류가 나면 `.gguf` 절대 경로를 다시 확인
- 모델이 너무 느리거나 메모리 부족이면 더 작은 모델이나 더 작은 quant 사용
- macOS / Linux 서버 확인은 `curl http://127.0.0.1:8080/v1/models`로 먼저 점검
- Windows PowerShell 서버 확인은 `Invoke-RestMethod http://127.0.0.1:8080/v1/models`가 더 안전함

### Hermes Agent

- `hermes version`이 안 되면 셸을 다시 열거나 `source ~/.zshrc` / `source ~/.bashrc` 실행
- `hermes doctor`에서 누락 의존성이 보이면 먼저 그 결과를 기준으로 수정
- Windows 사용자는 네이티브가 아니라 WSL2 안에서 실행해야 함
- Windows에서 `hermes`가 안 잡히면 먼저 PowerShell에서 `wsl --status`, `wsl -l -v`를 확인하고, WSL2 Ubuntu 셸 안에서 다시 점검
- 로컬 모델 연결 실패 시 `hermes model`에서 base URL과 model ID를 다시 확인

### ChromeOS

- Linux 개발 환경이 꺼져 있지 않은지 확인
- 학교/회사 정책으로 Linux가 막혀 있지 않은지 확인
- GPU 가속이 없으므로 성능 기대치를 낮추고 작은 모델만 사용

## 행사 전 최종 확인

아래 중 하나 이상이 되면 준비 완료입니다.

### LM Studio 준비 완료 기준

- 앱 실행 성공
- `google/gemma-4-e2b` 또는 `google/gemma-4-e4b` 계열의 **chat-ready / instruction-tuned 항목** 다운로드 완료
- Chat 화면에서 한 번 답변 생성 성공
- Windows에서 CLI까지 확인하고 싶다면 PowerShell에서 아래처럼 확인할 수 있습니다.

```powershell
lms --help
```

## 8GB 장비 참가자 사전 안내 문구 예시

아래처럼 강하게 안내하는 편이 안전합니다.

> 8GB 메모리 노트북은 작은 모델(E2B)에서도 속도가 많이 느리거나 시스템이 일시적으로 멈춘 것처럼 보일 수 있습니다.  
> 가능하면 16GB 이상 메모리 장비를 권장합니다.  
> 8GB 장비로 참석하는 경우에는 `E2B`만 미리 다운로드하고, 다른 앱을 종료한 상태에서 행사 전에 반드시 1회 실행 테스트를 완료해 주세요.

### Ollama 준비 완료 기준

macOS / Linux:

```bash
ollama --version
ollama run gemma4:e2b
```

Windows PowerShell:

```powershell
ollama --version
ollama run gemma4:e2b
```

### llama.cpp 준비 완료 기준

macOS / Linux:

```bash
llama-cli --version
llama-server --version
```

Windows PowerShell:

```powershell
llama-cli --version
llama-server --version
```

그리고 아래 중 하나 이상:

- `llama-cli`로 1회 응답 생성 성공
- `llama-server` 실행 성공
- macOS / Linux: `curl http://127.0.0.1:8080/v1/models`
- Windows PowerShell: `Invoke-RestMethod http://127.0.0.1:8080/v1/models`

### Hermes 준비 완료 기준

macOS / Linux / WSL2:

```bash
hermes version
hermes doctor
```

간단한 실행 확인:

```bash
hermes chat -q "Hello"
```

로컬 모델을 붙여 볼 참가자는 `hermes model`에서 local endpoint 등록까지 확인하면 더 안전합니다.

Windows 사용자는 위 명령을 PowerShell이 아니라 **WSL2 Ubuntu 셸 안에서** 실행해야 합니다.

## 공식 참고 링크

### Gemma 4

- [Gemma 4 출시 블로그 - Google Developers Blog](https://developers.googleblog.com/bring-state-of-the-art-agentic-skills-to-the-edge-with-gemma-4/)

### Ollama

- [Ollama Quickstart](https://docs.ollama.com/quickstart)
- [Ollama macOS](https://docs.ollama.com/macos)
- [Ollama Windows](https://docs.ollama.com/windows)
- [Ollama Linux](https://docs.ollama.com/linux)
- [Ollama Gemma 4 Library](https://ollama.com/library/gemma4)
- [Ollama Context Length](https://docs.ollama.com/context-length)

### LM Studio

- [LM Studio Download](https://lmstudio.ai/download)
- [LM Studio Docs](https://lmstudio.ai/docs/app)
- [LM Studio System Requirements](https://www.lmstudio.ai/docs/app/system-requirements)
- [LM Studio Get Started](https://lmstudio.ai/docs/app/basics)
- [LM Studio Download an LLM](https://lmstudio.ai/docs/app/basics/download-model)
- [LM Studio CLI](https://lmstudio.ai/docs/cli)
- [LM Studio Offline Operation](https://lmstudio.ai/docs/app/offline)
- [LM Studio Gemma 4 Models](https://lmstudio.ai/models/gemma-4)
- [LM Studio MLX Engine Blog](https://lmstudio.ai/blog/unified-mlx-engine)

### llama.cpp

- [llama.cpp README](https://github.com/ggml-org/llama.cpp)
- [llama.cpp Install Guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md)
- [llama.cpp Build Guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)

### Hermes Agent

- [Hermes Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)
- [Hermes Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart/)
- [Hermes FAQ](https://hermes-agent.nousresearch.com/docs/reference/faq/)
- [Hermes Docs Home](https://hermes-agent.nousresearch.com/docs/)

### Apple MLX / Community MLX

- [Apple MLX GitHub](https://github.com/ml-explore/mlx)
- [Apple MLX LM GitHub](https://github.com/ml-explore/mlx-lm)
- [MLX LoRA / QLoRA Guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Hugging Face MLX Community](https://huggingface.co/mlx-community)

### ChromeOS

- [Set up Linux on your Chromebook](https://support.google.com/chromebook/answer/9145439?hl=ko)

## 문서 작성 메모

- 이 가이드는 2026-04-21 기준 공식 문서와 모델 페이지를 바탕으로 정리했습니다.
- ChromeOS 관련 설명은 공식 지원 범위를 우선으로 정리했으며, 행사 안정성을 위해 보수적으로 안내했습니다.

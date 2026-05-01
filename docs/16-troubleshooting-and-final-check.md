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

### Gemini CLI Gemma 4 preview / Gemma 라우팅

- Gemma 4 모델 선택을 확인하려면 `gemini --version`으로 `v0.41.0-preview.0` 이상 preview인지 확인
- `~/.gemini/settings.json` 또는 `/settings`에서 `experimental.gemma`가 켜져 있는지 확인
- 프로젝트의 `.gemini/settings.json`이 사용자 설정을 덮어쓸 수 있으므로, 현재 프로젝트 설정도 확인
- `/model` 목록에 Gemma 4가 보여도 실제 호출 권한이 있다는 뜻은 아님
- `gemini --model gemma-4-26b-a4b-it`가 `You don't have access` 또는 `Preview Release Channel` 관련 메시지로 실패하면 계정/API 키/조직 관리자 설정에서 preview 모델 호출이 막힌 상태로 봄
- `gemini gemma` 명령이 없으면 `gemini --version`으로 v0.40.0 이상인지 확인
- `/gemma`에서 준비되지 않았다고 나오면 `/settings`에서 Gemma experimental 항목을 켠 뒤 Gemini CLI를 재시작
- `gemini gemma setup`에서 `gemma3-1b-gpu-custom`을 받는 것은 현재 정상 동작으로 보고, Gemma 4 모델 선택 기능과 구분
- 다운로드가 오래 걸리면 행사장 네트워크에서 진행하지 말고 행사 전에 미리 완료
- macOS에서 LiteRT-LM 실행이 막히면 Privacy & Security에서 허용하거나 공식 문서의 quarantine 해제 안내 확인

### ChromeOS

- Linux 개발 환경이 꺼져 있지 않은지 확인
- 학교/회사 정책으로 Linux가 막혀 있지 않은지 확인
- 로컬 LLM용 전용 GPU/VRAM 가속을 기대하기 어려우므로 성능 기대치를 낮추고 작은 모델만 사용

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

## 8GB 장비 주의사항

8GB 메모리 노트북은 작은 모델(E2B)에서도 속도가 많이 느리거나 시스템이 일시적으로 멈춘 것처럼 보일 수 있습니다.

- 가능하면 16GB 이상 메모리 장비를 권장합니다.
- 8GB 장비로 참석하는 경우에는 `E2B`만 미리 다운로드하세요.
- 다른 앱을 종료한 상태에서 행사 전에 반드시 1회 실행 테스트를 완료해 주세요.

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

그 다음 `hermes` 또는 `hermes --tui`를 실행해 짧은 질문이 응답되는지 확인하세요.

로컬 모델을 붙여 볼 경우에는 `hermes model`에서 로컬 서버 주소 등록까지 확인하세요.

Windows 사용자는 위 명령을 PowerShell이 아니라 **WSL2 Ubuntu 셸 안에서** 실행해야 합니다.

### Gemini CLI Gemma 4 preview 준비 완료 기준

macOS / Linux / Windows:

```bash
gemini --version
gemini --model gemma-4-26b-a4b-it
```

Gemini CLI 세션 안에서:

```text
/model
```

아래가 확인되면 Gemma 4 preview 준비 완료입니다.

- Gemini CLI 버전이 `v0.41.0-preview.0` 이상 preview
- `experimental.gemma` 설정 활성화
- 사용자 설정과 프로젝트 설정 중 어디에서 설정이 적용되는지 확인
- `/model`에서 Gemma 4 모델 선택 가능 여부 확인
- `gemma-4-26b-a4b-it` 또는 `gemma-4-31b-it`로 짧은 일반 질문 응답 성공

목록에만 보이고 `You don't have access` 또는 `Preview Release Channel` 관련 오류가 나오면 Gemma 4 preview 호출 준비는 미완료입니다.

### Gemini CLI Gemma 라우팅 준비 완료 기준

macOS / Linux / Windows:

```bash
gemini --version
gemini gemma setup
gemini gemma status
```

Gemini CLI 세션 안에서:

```text
/gemma
```

아래가 확인되면 준비 완료입니다.

- Gemini CLI 버전이 `v0.40.0` 이상
- `experimental.gemma` 설정 활성화
- `gemma3-1b-gpu-custom` 다운로드 완료
- `gemini gemma status` 상태 확인 성공
- `/gemma` 상태 확인 성공
- 짧은 일반 질문에 Gemini CLI가 응답

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
- [Hermes CLI Commands Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands/)
- [Hermes FAQ](https://hermes-agent.nousresearch.com/docs/reference/faq/)
- [Hermes Docs Home](https://hermes-agent.nousresearch.com/docs/)

### uv

- [uv Installation](https://docs.astral.sh/uv/getting-started/installation/)
- [uv First steps](https://docs.astral.sh/uv/getting-started/first-steps/)
- [uv Tools Guide](https://docs.astral.sh/uv/guides/tools/)

### Gemini CLI

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI v0.41.0-preview.0 release](https://github.com/google-gemini/gemini-cli/releases/tag/v0.41.0-preview.0)
- [Gemma 4 support PR #25604](https://github.com/google-gemini/gemini-cli/pull/25604)
- [Gemini CLI v0.40.0 discussion](https://github.com/google-gemini/gemini-cli/discussions/26216)
- [Gemini CLI settings reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md)
- [Gemini CLI model selection reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md)
- [Gemini CLI CLI reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md)
- [Gemini CLI Model Routing](https://geminicli.com/docs/cli/model-routing/)
- [Gemini CLI `gemini gemma` setup](https://geminicli.com/docs/core/gemma-setup/)
- [Gemini CLI Manual Local Model Routing](https://geminicli.com/docs/core/local-model-routing/)
- [Gemma Terms of Use](https://ai.google.dev/gemma/terms)

### Apple MLX / Community MLX

- [Apple MLX GitHub](https://github.com/ml-explore/mlx)
- [Apple MLX LM GitHub](https://github.com/ml-explore/mlx-lm)
- [MLX LoRA / QLoRA Guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Hugging Face MLX Community](https://huggingface.co/mlx-community)

### ChromeOS

- [Set up Linux on your Chromebook](https://support.google.com/chromebook/answer/9145439?hl=ko)

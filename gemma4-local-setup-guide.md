# Build Your Own AI Office with Gemma 4

Build with AI Seoul 2026 with Google DeepMind  
사전 준비 전체 안내 문서  
기준 확인일: 2026-05-02

## 행사 정보

- 세션명: **Build Your Own AI Office with Gemma 4**
- 진행자: **박제창**
- 트랙: **Hands-On A**
- 진행 시간: **13:30 ~ 14:30 (60분)**

## 이 문서는 전체 안내 문서입니다

사전 준비 문서 길이가 길어져서, 필요한 항목만 바로 볼 수 있도록 문서를 섹션별로 나눴습니다.  
아래 링크에서 필요한 문서만 열어 보시면 됩니다.

## 매우 중요한 안내

> **행사 당일에 처음 모델을 다운로드하지 않도록 강하게 권장합니다.**
>
> Gemma 4 모델 파일은 작아도 수 GB 수준이며, 모델에 따라 대략 **4GB~20GB 내외**까지 커질 수 있습니다.  
> 현장 인터넷 상황에 따라 다운로드만 오래 걸릴 수 있고, **핸즈온 60분 동안 모델만 받다가 세션이 끝날 수 있습니다.**
>
> **특히 8GB 메모리 노트북은 작은 모델(E2B)에서도 속도가 많이 느리거나, 경우에 따라 시스템이 일시적으로 멈춘 것처럼 보일 수 있습니다.**
> 가능하면 **16GB 이상 메모리 노트북**으로 참석해 주세요.
>
> **반드시 행사 전에**
> - 도구 설치 완료
> - 사용할 모델 다운로드 완료
> - 최소 1회 실행 테스트 완료

## Windows 사용자 준비

- 이 문서의 명령 예시는 운영체제에 따라 `bash` 또는 `PowerShell`로 구분되어 있습니다.
- **Windows 사용자는 기본적으로 PowerShell 기준으로 따라오시는 것을 권장합니다.**
- `ollama`, `lms`, `pi` 같은 명령은 PowerShell에서 실행하세요.
- 다만 `OpenCode`는 Windows에서 공식적으로 **WSL 경로를 권장**하므로, 이 부분은 PowerShell/CMD가 아니라 **WSL 터미널 기준**으로 보시면 됩니다.
- `Hermes Agent`도 Windows 네이티브가 아니라 **WSL2 기준**으로 봐야 합니다.

## 먼저 결론

- 가능하면 **Ollama와 LM Studio를 둘 다 설치**해 주세요.
- 하나만 설치한다면 **LM Studio를 먼저 설치하세요**.
- `Hermes Agent`와 `llama.cpp`는 필수가 아닙니다. 터미널 사용에 익숙한 경우에만 추가로 준비하세요.
- `uv`는 로컬 LLM 실행 도구가 아니라 Python 기반 도구와 실행 환경을 관리하는 보조 도구입니다. `Hermes Agent` 설치 중 문제가 날 때만 별도로 확인해도 됩니다.
- 핸즈온에서 `workshop/01_starter` 코드를 수정하므로 `Visual Studio Code` 또는 `Google Antigravity` 중 하나를 준비하세요.
- `Gemini CLI Gemma`도 필수 준비 항목은 아닙니다. preview에서는 Gemma 4 모델 선택이 가능하지만, `gemini gemma setup`은 Gemma 3 기반 로컬 라우팅 설정으로 이해해 주세요.
- **ChromeOS 사용자는 예외적으로 Ollama를 우선 권장**합니다.
- 이번 세션은 **개발자, 비개발자 모두 참여 가능한 세션**이므로, 처음 준비한다면 **GUI로 따라가기 쉬운 LM Studio**부터 설치하면 됩니다.
- 이번 핸즈온은 채팅, 실습, 에이전트 흐름이 중심이므로 **instruction-tuned(chat-ready) 계열을 기준으로 준비하세요.** `base`나 `pretrained`로 표시된 모델은 기본 준비용으로 권장하지 않습니다.
- 모델 다운로드까지 반드시 행사 전에 끝내고 와야 합니다.

## 빠른 선택

- Windows/macOS/Linux에서 하나만 설치: **LM Studio**
- ChromeOS: **Ollama**
- 8GB 노트북: **E2B만 시도, 속도 저하 감안**
- 16GB 노트북: **E4B**
- 32GB 노트북: **E4B 또는 26B A4B**
- 36GB 노트북: **26B A4B 또는 31B**

모델 이름에 붙은 `B`는 `Billion`, 즉 **10억 개**를 뜻합니다.  
`26B`는 대략 260억 개 파라미터를 가진 모델, `31B`는 대략 310억 개 파라미터를 가진 모델이라는 뜻입니다.

여기서 파라미터는 모델이 학습하면서 갖게 된 숫자 값입니다.  
사람에게 비유하면 "기억과 계산 방식이 저장된 내부 숫자"에 가깝습니다. 숫자가 많을수록 더 복잡한 패턴을 담을 수 있지만, 보통 더 많은 메모리와 계산이 필요합니다.

주의할 점은 `B`가 `GB`가 아니라는 것입니다.  
`26B`는 파일 크기가 26GB라는 뜻이 아닙니다. 실제 다운로드 크기와 실행 중 메모리 사용량은 양자화 방식, 실행 도구, 컨텍스트 길이에 따라 달라집니다.

일반 사용자가 LM Studio나 Ollama에서 받는 로컬 실행용 모델은 보통 원본 BF16 가중치 그대로가 아니라 **4-bit, 5-bit, 8-bit 등으로 양자화된 배포본**입니다. 그래서 `26B`, `31B`라는 이름과 다운로드 크기가 1:1로 대응하지 않습니다.

모델을 직접 고를 때는 `-it`, `instruct`, `instruction-tuned`, `chat-ready` 같은 설명이 붙은 항목을 우선하세요.  
`base`나 `pretrained`로 표시된 모델은 모델을 연구하거나 파인튜닝을 시작할 때는 의미가 있지만, 이번 핸즈온처럼 바로 대화하고 지시를 수행하는 흐름에는 덜 적합합니다.

`26B A4B`는 26B 규모 모델이지만, 답을 만들 때는 내부의 여러 "전문가" 부분 중 필요한 일부만 사용합니다. 이 방식을 `MoE`라고 부르며, `A4B`는 그때 실제로 계산되는 부분이 약 4B 규모라는 뜻입니다. 다만 전체 26B 규모의 모델 파일은 메모리에 올라가야 하므로, 4B 모델처럼 가볍게 실행된다는 뜻은 아닙니다.

## 문서 목록

1. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
2. [Windows 빠른 준비 가이드](./docs/02-windows-guide.md)
3. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)
4. [GGUF, MLX, llama.cpp 개념 설명](./docs/04-gguf-mlx-llamacpp-explainer.md)
5. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)
6. [Ollama 설치 가이드](./docs/06-ollama-setup.md)
7. [llama.cpp 설치 가이드](./docs/07-llamacpp-setup.md)
8. [Apple Silicon + MLX 안내](./docs/08-apple-silicon-mlx.md)
9. [Gemma 4 벤치마크와 코딩 에이전트 기대치](./docs/09-gemma4-benchmarks-and-agent-expectations.md)
10. [OpenCode 설치 및 LM Studio 연동 가이드](./docs/10-opencode-lmstudio-developer-agent.md)
11. [Pi 경량 코딩 에이전트 대안과 이번 핸즈온 선택 이유](./docs/11-pi-and-tool-selection-notes.md)
12. [Hermes Agent란 무엇인가](./docs/12-hermes-agent-overview.md)
13. [Hermes Agent 설치 가이드](./docs/13-hermes-agent-setup.md)
14. [Gemma 4 아키텍처 상세 정리](./docs/14-gemma4-architecture-deep-dive.md)
15. [Gemini CLI Gemma 4 Preview 및 Gemma 라우팅 사전 준비 가이드](./docs/15-gemini-cli-gemma-routing-prep.md)
16. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)
17. [자주 묻는 질문](./docs/17-faq.md)
18. [uv 설치 가이드](./docs/18-uv-setup.md)
19. [코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity](./docs/19-code-editor-setup.md)

## 어떤 문서를 먼저 보면 되나요?

### 처음 준비하는 경우

1. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
2. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)
3. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)
4. [코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity](./docs/19-code-editor-setup.md)
5. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### Windows를 쓰는 경우

1. [Windows 빠른 준비 가이드](./docs/02-windows-guide.md)
2. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
3. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)
4. [코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity](./docs/19-code-editor-setup.md)
5. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### ChromeOS를 쓰는 경우

1. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
2. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)
3. [Ollama 설치 가이드](./docs/06-ollama-setup.md)
4. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### Apple Silicon Mac을 쓰는 경우

1. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
2. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)
3. [GGUF, MLX, llama.cpp 개념 설명](./docs/04-gguf-mlx-llamacpp-explainer.md)
4. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)
5. [Apple Silicon + MLX 안내](./docs/08-apple-silicon-mlx.md)
6. [코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity](./docs/19-code-editor-setup.md)
7. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### 핸즈온 코드를 직접 수정해야 하는 경우

1. [코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity](./docs/19-code-editor-setup.md)
2. [uv 설치 가이드](./docs/18-uv-setup.md)
3. [workshop/03_labs/README.md](./workshop/03_labs/README.md)

### 코딩 에이전트 경험이 있는 경우

1. [Gemma 4 벤치마크와 코딩 에이전트 기대치](./docs/09-gemma4-benchmarks-and-agent-expectations.md)
2. [OpenCode 설치 및 LM Studio 연동 가이드](./docs/10-opencode-lmstudio-developer-agent.md)
3. [Pi 경량 코딩 에이전트 대안과 이번 핸즈온 선택 이유](./docs/11-pi-and-tool-selection-notes.md)
4. [Hermes Agent란 무엇인가](./docs/12-hermes-agent-overview.md)
5. [llama.cpp 설치 가이드](./docs/07-llamacpp-setup.md)
6. [Hermes Agent 설치 가이드](./docs/13-hermes-agent-setup.md)
7. [uv 설치 가이드](./docs/18-uv-setup.md) (Hermes 설치 중 오류가 날 때)
8. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
9. [Gemma 4 아키텍처 상세 정리](./docs/14-gemma4-architecture-deep-dive.md)
10. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)

### Gemini CLI에서 Gemma 4 preview 또는 Gemma 라우팅을 확인해 보고 싶은 경우

1. [Gemini CLI Gemma 4 Preview 및 Gemma 라우팅 사전 준비 가이드](./docs/15-gemini-cli-gemma-routing-prep.md)
2. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### 자주 묻는 질문부터 보고 싶은 경우

1. [자주 묻는 질문](./docs/17-faq.md)
2. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
3. [LM Studio 설치 가이드](./docs/05-lm-studio-setup.md)

### Hermes를 먼저 이해하고 싶은 경우

1. [Hermes Agent란 무엇인가](./docs/12-hermes-agent-overview.md)
2. [Hermes Agent 설치 가이드](./docs/13-hermes-agent-setup.md)
3. [uv 설치 가이드](./docs/18-uv-setup.md) (Hermes 설치 중 오류가 날 때)
4. [llama.cpp 설치 가이드](./docs/07-llamacpp-setup.md)
5. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### CLI 기반 로컬 서버를 직접 띄워 보고 싶은 경우

1. [llama.cpp 설치 가이드](./docs/07-llamacpp-setup.md)
2. [GGUF, MLX, llama.cpp 개념 설명](./docs/04-gguf-mlx-llamacpp-explainer.md)
3. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)
4. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/16-troubleshooting-and-final-check.md)

### 모델 구조가 궁금한 경우

1. [Gemma 4 아키텍처 상세 정리](./docs/14-gemma4-architecture-deep-dive.md)
2. [GGUF, MLX, llama.cpp 개념 설명](./docs/04-gguf-mlx-llamacpp-explainer.md)
3. [메모리 기준으로 Gemma 4 모델 고르는 방법](./docs/03-memory-based-model-selection.md)

## 참가 전 체크리스트

- 운영체제 업데이트 완료
- 관리자 권한 또는 설치 권한 확인
- 여유 디스크 공간 최소 20GB, 가능하면 40GB 이상
- 안정적인 인터넷 연결
- 실습 당일 전원 어댑터 지참
- 행사 전에 모델 다운로드 완료
- 행사 전 테스트 완료
  - 코드 편집기: VS Code `code --version` 또는 Antigravity 앱 실행 + `workshop/01_starter` 폴더 열기
  - Ollama: `ollama --version`, `ollama run gemma4:e2b`
  - LM Studio: 앱 실행, 모델 다운로드, 채팅 1회 성공
  - llama.cpp: `llama-cli --version`, `llama-server --version`
  - uv: `uv --version`, `uvx --version` (Hermes 등 Python 기반 CLI 도구를 직접 준비하는 경우)
  - Hermes: `hermes version`, `hermes doctor`
  - Gemini CLI Gemma 4 preview: `gemini --version`, `/settings`에서 `experimental.gemma` 확인, `gemini --model gemma-4-26b-a4b-it`, 세션 안에서 `/model`
  - Gemini CLI Gemma 라우팅: `gemini gemma setup`, `gemini gemma status`, 세션 안에서 `/gemma`

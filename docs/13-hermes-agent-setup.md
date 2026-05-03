# Hermes Agent 설치 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

`Hermes`가 어떤 도구인지 먼저 이해하고 싶다면 [Hermes Agent란 무엇인가](./12-hermes-agent-overview.md) 문서를 먼저 확인해 주세요.

## 이 문서는 누구를 위한 문서인가요?

- `Hermes Agent`를 이번 핸즈온에서 추가로 써 보고 싶은 분
- `Gemma 4 + llama.cpp` 또는 다른 OpenAI 호환 로컬 서버에 `Hermes`를 연결해 보고 싶은 분
- `CEO / CPO / PM / QA / Developer` 같은 역할 기반 AI office 데모를 직접 구성해 보고 싶은 분

## 먼저 결론

- `Hermes Agent`는 이번 세션에서 필수 준비 항목이 아닙니다.
- macOS, Linux, WSL2에서는 설치가 비교적 단순합니다.
- **Windows 네이티브는 공식 미지원**이며, Windows 사용자는 **WSL2 안에서 설치**해야 합니다.
- 라이브 데모나 고급 실습에는 좋지만, 처음 준비할 때 기본으로 두기에는 설치와 연결 과정이 복잡합니다.

## 사전 안내

- 행사 전에 반드시 설치를 끝내고 오세요.
- 행사 전에 최소 1회 `hermes` 실행 테스트를 해 두세요.
- `Hermes`만 설치된 상태로는 로컬 모델 추론이 되지 않습니다.
- 로컬 모델을 쓰려면 `Ollama`, `LM Studio`, `llama.cpp`, `vLLM` 같은 **별도 inference server**가 필요합니다.

## 공식 지원 범위

### macOS / Linux / WSL2

공식 one-line installer를 사용할 수 있습니다.

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

설치가 끝나면 셸을 다시 읽습니다.

```bash
source ~/.zshrc
```

또는 `bash` 사용자라면:

```bash
source ~/.bashrc
```

### Windows

Windows 네이티브는 공식 미지원입니다.  
먼저 `WSL2`를 설치한 뒤, **WSL 터미널 안에서** 위 설치 명령을 실행해야 합니다.

Windows 사용자는 `Hermes = WSL2 전용 선택 경로`로 이해하면 됩니다.

PowerShell 관리자 권한에서 먼저 할 일:

```powershell
wsl --install -d Ubuntu
```

설치가 멈추거나 Store 경로가 불안정하면:

```powershell
wsl --install --web-download -d Ubuntu
```

설치 후 상태 확인:

```powershell
wsl --status
wsl --list --verbose
```

Ubuntu 실행:

```powershell
wsl -d Ubuntu
```

## 설치 전에 확인할 것

- `git --version`
- 관리자 권한 또는 설치 권한
- 안정적인 인터넷
- 여유 디스크 공간
- macOS / Linux / WSL2 셸 사용 가능 여부

`Hermes` 설치 스크립트는 공식 문서 기준으로 아래를 자동 처리합니다.

- `uv`
- Python 3.11
- Node.js
- `ripgrep`
- `ffmpeg`
- `hermes` 명령 연결
- setup wizard 실행

자동 설치가 실패하거나 `uv`만 미리 준비하고 싶다면 [uv 설치 가이드](./16-uv-setup.md)를 먼저 확인하세요.

## 설치 순서

### 1. Windows 사용자는 먼저 WSL2 준비

PowerShell 관리자 권한:

```powershell
wsl --install -d Ubuntu
```

설치 확인:

```powershell
wsl --status
wsl --list --verbose
```

Ubuntu 셸 열기:

```powershell
wsl -d Ubuntu
```

이후 명령은 **WSL 터미널 안에서** 실행합니다.

macOS / Linux 사용자는 이 단계를 건너뛰고 바로 다음 단계로 가면 됩니다.

### 2. 설치 실행

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 3. 셸 재로드

```bash
source ~/.zshrc
```

또는:

```bash
source ~/.bashrc
```

### 4. 설정 마법사 또는 모델 설정

처음 설치 후 setup wizard가 열리면 기본 모델 공급자를 설정할 수 있습니다.

나중에 다시 바꾸려면:

```bash
hermes model
```

### 5. 설치 확인

```bash
hermes version
hermes doctor
```

## 로컬 모델과 연결하는 법

이번 핸즈온에서는 `Hermes`가 직접 모델을 돌리는 것이 아니라, 별도 로컬 서버에 붙는 구조로 이해하면 됩니다.

중요:

- Hermes Agent는 다단계 tool-calling 작업을 위해 **최소 64K 토큰 컨텍스트**를 요구합니다.
- 로컬 모델 서버의 컨텍스트가 이보다 작으면 Hermes가 시작 단계에서 거부하거나, 작업 중 불안정하게 동작할 수 있습니다.
- 컨텍스트를 키우면 메모리 사용량도 함께 늘어나므로, 8GB/16GB 장비에서는 Hermes 경로를 무리하게 권장하지 않습니다.

도구별 확인 예시:

- `llama.cpp`: `llama-server ... --ctx-size 65536`
- `Ollama`: 필요 시 `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`처럼 64K 이상으로 서버를 띄운 뒤 연결
- `LM Studio`: 서버를 켜기 전에 모델 설정에서 context length를 64K 이상으로 설정할 수 있는지 확인

따라서 Hermes와 연결할 로컬 서버는 아래 두 가지를 먼저 확인해야 합니다.

1. `/v1/models`에서 실제 model ID가 보이는지
2. 해당 서버/모델이 64K 이상 컨텍스트로 실행 중인지

예를 들어 `llama.cpp`의 `llama-server`를 `127.0.0.1:8080/v1`에 띄웠다면:

```bash
hermes model
```

입력 예시:

- Base URL: `http://127.0.0.1:8080/v1`
- API key: `none`
- Model name: `/v1/models`에서 보이는 모델 ID
- Context length: `64000` 또는 `65536` 이상

즉 구조는 아래와 같습니다.

```text
Hermes Agent -> OpenAI 호환 로컬 서버 -> Gemma 4
```

## Windows에서 권하는 방식

Windows에서 `Hermes`를 꼭 쓰고 싶다면 아래 방식으로 준비하세요.

1. Windows에서 `LM Studio` 또는 `llama.cpp` 서버 실행
2. WSL2 안에서 `Hermes` 실행
3. `Hermes`가 로컬 서버 주소에 연결

이 방식은 WSL 안에서 대용량 모델을 다시 내려받고 빌드하는 부담을 줄여 줍니다.

Windows PowerShell에서 WSL 진입 예시:

```powershell
wsl -d Ubuntu
```

그 다음 WSL 안에서:

```bash
hermes version
hermes doctor
```

## 행사 전 최종 확인

아래가 되면 준비 완료입니다.

### Hermes 준비 완료 기준

macOS / Linux / WSL2:

```bash
hermes version
hermes doctor
```

그 다음 `hermes` 또는 `hermes --tui`를 실행해 짧은 질문이 응답되는지 확인하세요.

Windows 사용자는 위 명령을 **PowerShell이 아니라 WSL2 Ubuntu 셸 안에서** 실행하면 됩니다.

로컬 모델 연결까지 확인하려면:

```bash
hermes model
```

에서 로컬 서버 주소를 등록한 뒤, 간단한 질문이 한 번 응답되면 충분합니다.

## 이런 경우에 해 보세요

- 라이브 데모
- 로컬 에이전트, skills, delegation, AI office 워크플로를 직접 구성해 보고 싶은 경우

## 이런 경우에는 나중에 해도 됩니다

- 당일 처음 WSL2를 설치해야 하는 경우
- 60분 안에 GUI 중심으로만 간단한 체험을 원하는 경우
- 에이전트보다 기본 로컬 추론만 빨리 체험하고 싶은 경우

## 공식 참고 링크

- [Hermes Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)
- [Hermes Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart/)
- [Hermes CLI Commands Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands/)
- [Hermes FAQ](https://hermes-agent.nousresearch.com/docs/reference/faq/)
- [Hermes Docs Home](https://hermes-agent.nousresearch.com/docs/)

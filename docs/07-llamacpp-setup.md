# llama.cpp 설치 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `GGUF + llama.cpp`로 Gemma 4를 로컬에서 돌려 보고 싶은 분
- `llama-server`를 띄워 `Hermes`, `OpenCode`, `Pi` 같은 에이전트와 연결하고 싶은 분
- `LM Studio` 대신 CLI 기반 local server 방식을 선호하는 분

## 먼저 결론

- `llama.cpp`는 이번 세션의 **고급 / 선택형 경로**입니다.
- 가장 쉬운 설치 경로는 **pre-built package 설치**입니다.
- 공식 문서 기준으로:
  - macOS / Linux: `brew install llama.cpp`
  - Windows: `winget install llama.cpp`
- 이번 핸즈온에서는 **소스 빌드보다 pre-built 설치**를 우선 권장합니다.

## 왜 llama.cpp를 쓰나요?

- `GGUF` 모델을 직접 로컬에서 돌릴 수 있습니다.
- `llama-server`로 **OpenAI 호환 API 서버**를 띄울 수 있습니다.
- `Hermes` 같은 에이전트가 로컬 서버 주소에 붙기 쉽습니다.

## 권장 설치 방법

### macOS / Linux

```bash
brew install llama.cpp
```

설치 확인:

```bash
llama-cli --version
llama-server --version
```

### Windows

PowerShell:

```powershell
winget install llama.cpp
```

설치 확인:

```powershell
llama-cli --version
llama-server --version
```

모델 파일 경로에 공백이 있다면 큰따옴표로 감싸 주세요.

## 다른 설치 방법

공식 문서에는 아래도 있습니다.

- pre-built binaries 다운로드
- Docker
- 소스 빌드

이번 핸즈온에서는 일단 **패키지 매니저 설치**를 우선 사용하세요.

## 소스 빌드는 언제 필요한가요?

- GPU backend를 직접 선택해 빌드해야 할 때
- 최신 기능이 패키지보다 먼저 필요할 때
- 배포 패키지 대신 특정 빌드 옵션을 직접 제어하고 싶을 때

공식 CPU build 기본 예시는 아래입니다.

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

이번 사전 준비 가이드에서는 소스 빌드를 기본 설치 방법으로 권장하지 않습니다.

## 가장 간단한 실행 예시

### 로컬 GGUF 파일 사용

```bash
llama-cli -m /path/to/model.gguf
```

Windows PowerShell:

```powershell
llama-cli -m "C:\path\to\model.gguf"
```

### Hugging Face에서 바로 다운로드해서 실행

```bash
llama-cli -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M
```

Windows PowerShell:

```powershell
llama-cli -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M
```

### OpenAI 호환 API 서버 실행

```bash
llama-server -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M
```

Windows PowerShell:

```powershell
llama-server -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M
```

또는 이미 내려받은 GGUF 파일이 있다면:

```bash
llama-server -m /path/to/model.gguf --host 127.0.0.1 --port 8080
```

Windows PowerShell:

```powershell
llama-server -m "C:\path\to\model.gguf" --host 127.0.0.1 --port 8080
```

기본 Web UI는 보통 아래에서 열 수 있습니다.

```text
http://localhost:8080
```

chat completions endpoint는 아래입니다.

```text
http://localhost:8080/v1/chat/completions
```

## Gemma 4와 함께 쓸 때

이번 핸즈온에서는 `Gemma 4 GGUF`를 `llama.cpp`로 띄우고, 필요하면 그 위에 `Hermes` 같은 에이전트를 연결하는 구성이 가능합니다.

예시:

```bash
llama-server -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M
```

또는:

```bash
llama-server -m /absolute/path/to/gemma-4-E4B-it-Q4_K_M.gguf --host 127.0.0.1 --port 8080
```

## 행사 전 최종 확인

아래가 되면 준비 완료입니다.

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

1. `llama-cli`로 한 번 답변 생성 성공
2. `llama-server` 실행 성공
3. `curl http://127.0.0.1:8080/v1/models` 확인 성공

예시:

```bash
curl http://127.0.0.1:8080/v1/models
```

Windows PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/v1/models
```

## 주의할 점

- `llama.cpp`만 설치해도 모델 파일은 자동으로 준비되지 않습니다.
- 대용량 모델은 다운로드 시간이 길 수 있으므로 행사 전에 미리 받아 두세요.
- `GGUF` 경로를 직접 관리해야 할 수 있습니다.
- Windows에서는 `llama.cpp` 자체는 설치 가능하지만, 그 위에 `Hermes`를 붙일 때는 `Hermes`가 WSL2 안에서 돌아가야 한다는 점을 별도로 이해해야 합니다.

## 이런 경우에 해 보세요

- CLI에 익숙한 경우
- LM Studio보다 더 직접적인 local server 구성을 원하는 경우
- `Hermes + Gemma 4`를 직접 묶어 보고 싶은 경우

## 공식 참고 링크

- [llama.cpp README](https://github.com/ggml-org/llama.cpp)
- [llama.cpp Install Guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md)
- [llama.cpp Build Guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)

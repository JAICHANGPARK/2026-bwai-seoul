# Pi 경량 코딩 에이전트 대안과 이번 핸즈온 선택 이유

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `opencode`보다 더 가벼운 터미널 코딩 에이전트를 찾는 분
- Gemma 4 local LLM을 붙일 수 있는 다른 코딩 에이전트 방식을 알고 싶은 분
- 왜 이번 핸즈온에서 `gemini-cli`, `Antigravity`를 code agent로 사용하지 않았는지 궁금한 분

## 먼저 결론

- `pi`는 **좋은 경량 대안**입니다.
- 이유는 `pi`가 스스로를 **minimal terminal coding harness** 로 설명하고, `~/.pi/agent/models.json` 을 통해 **LM Studio / Ollama / vLLM 같은 로컬 OpenAI 호환 서버**를 붙일 수 있다고 공식 문서에 적고 있기 때문입니다.
- 이번 핸즈온은 **Gemma 4를 각자 노트북에 미리 내려받아 두고, 네트워크가 없거나 매우 불안정해도 로컬에서 실행 가능한 흐름**을 중요하게 봅니다.
- 반대로 `gemini-cli`와 `Antigravity`는 이번 핸즈온 기준 **Gemma 4 local LLM + LM Studio 기반의 오프라인 code agent 경로가 명확하지 않습니다.**

짧게 정리하면:

- `opencode`: 기능이 더 많고, 역할 분리와 에이전트 구성이 쉬움
- `pi`: 더 가볍고 단순한 경량 대안
- `gemini-cli`: 공식 문서 기준 Gemini 중심 도구
- `Antigravity`: 공식 공개 자료 기준 hosted model 중심 도구에 가까우며, 로컬 Gemma 4 + LM Studio 기반 오프라인 경로가 명확하지 않음

## `pi`는 왜 대안으로 적절한가요?

Pi 공식 README 기준:

- `pi`는 **minimal terminal coding harness** 입니다.
- 기본 도구는 `read`, `write`, `edit`, `bash` 로 비교적 단순합니다.
- `sub agents`와 `plan mode` 같은 기능은 기본 내장보다 확장/패키지 방식에 가깝습니다.
- `~/.pi/agent/models.json` 으로 **custom providers & models** 를 추가할 수 있고, 문서에서 **Ollama, LM Studio, vLLM** 같은 로컬 모델 서버를 명시적으로 언급합니다.

즉, 이번 핸즈온에서는:

- `opencode`보다 설정 면적이 작고
- 로컬 OpenAI 호환 서버 연결이 가능하며
- “개발자 에이전트 최소 버전”을 보여주기 좋습니다.

## `opencode`와 `pi`는 어떻게 나눠 쓰나요?

| 도구 | 추천 상황 | 특징 |
| --- | --- | --- |
| `opencode` | 역할 분리, 에이전트 구성, 데모 확장성이 중요할 때 | 기능이 더 많고, 에이전트/권한/프롬프트 구성이 풍부함 |
| `pi` | 더 가볍고 단순한 CLI 코딩 에이전트를 원할 때 | 최소 도구 구성, 빠른 시작, 커스텀 모델 연결 가능 |

권장 사용:

- 라이브 데모 메인 경로: `opencode`
- 가벼운 대안 소개: `pi`

## `pi` 설치 가이드

공식 Quick Start 기준:

macOS / Linux:

```bash
npm install -g @mariozechner/pi-coding-agent
```

Windows PowerShell:

```powershell
npm install -g @mariozechner/pi-coding-agent
```

설치 확인:

macOS / Linux:

```bash
pi --version
```

Windows PowerShell:

```powershell
pi --version
```

Windows 메모:

- `pi` 자체는 PowerShell에서도 설치와 실행이 가능합니다.
- 다만 이번 핸즈온의 code agent 메인 경로는 `OpenCode`이고, OpenCode는 Windows에서 **WSL 권장**입니다.
- Windows에서는 `pi = PowerShell 가능`, `OpenCode = WSL 권장`으로 구분하면 됩니다.

Ollama를 함께 쓰는 경우에는 `ollama launch pi --config`로 Pi의 Ollama provider 설정을 자동 생성할 수도 있습니다. 이 문서에서는 LM Studio 연결을 직접 확인하기 위해 `models.json` 수동 설정을 기준으로 설명합니다.

## LM Studio와 `pi` 연결하기

### 1. LM Studio 서버 준비

먼저 LM Studio에서 Gemma 4 모델을 다운로드하고, `Developer` 탭에서 서버를 시작합니다.

핸즈온 기준으로는 **instruction-tuned / chat-ready 모델**을 선택합니다.
Hugging Face나 `llama.cpp` 예시에서는 보통 `...-it` 접미사가 보이지만, LM Studio에서는 이름이 더 짧게 보일 수 있습니다.

기본 엔드포인트:

```text
http://127.0.0.1:1234/v1
```

모델 확인:

macOS / Linux:

```bash
curl http://127.0.0.1:1234/v1/models
```

Windows PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:1234/v1/models
```

### 2. `~/.pi/agent/models.json` 설정

Pi 공식 문서 기준으로, local model provider는 `models.json` 으로 추가합니다.

Pi 모델 문서 기준으로 `openai-completions` 가 **most compatible** 한 기본 선택입니다.

예시:

```json
{
  "providers": {
    "lmstudio": {
      "baseUrl": "http://127.0.0.1:1234/v1",
      "api": "openai-completions",
      "authHeader": false,
      "apiKey": "lm-studio",
      "models": [
        { "id": "google/gemma-4-e4b", "name": "Gemma 4 E4B (LM Studio)" },
        { "id": "google/gemma-4-26b-a4b", "name": "Gemma 4 26B A4B (LM Studio)" },
        { "id": "google/gemma-4-31b", "name": "Gemma 4 31B (LM Studio)" }
      ]
    }
  }
}
```

중요:

- 여기서 `id` 는 LM Studio 서버가 실제로 노출하는 모델 ID와 맞아야 합니다.
- 먼저 `curl http://127.0.0.1:1234/v1/models` 또는 PowerShell의 `Invoke-RestMethod http://127.0.0.1:1234/v1/models` 로 확인한 뒤 맞추세요.
- 예시처럼 `authHeader: false` 로 두면 LM Studio에 불필요한 Bearer 인증 헤더를 보내지 않게 됩니다.
- 만약 로컬 서버가 OpenAI 호환 필드를 일부만 지원한다면, Pi 모델 문서의 `compat` 설정으로 추가 조정할 수 있습니다.

### 3. 실행

실행 후 `/model` 로 모델을 고르거나, provider/model 형식으로 선택합니다.

예시:

macOS / Linux:

```bash
pi --model lmstudio/google/gemma-4-e4b
```

Windows PowerShell:

```powershell
pi --model lmstudio/google/gemma-4-e4b
```

또는 interactive 모드에서:

```text
/model
```

## `pi`에서 Gemma 4를 쓸 때 추천

- 8GB: 비권장
- 16GB: `E4B`로 가벼운 코드 보조만 권장
- 32GB: `26B A4B` 권장
- 36GB+: `31B` 또는 `26B A4B`

`pi`도 결국 코딩 에이전트이므로, 작은 모델의 한계는 `opencode`와 비슷하게 존재합니다.

## 왜 `gemini-cli`를 기본 code agent로 쓰지 않나요?

`gemini-cli`는 좋은 터미널 AI 에이전트이지만, 이번 핸즈온의 기본 code agent로는 쓰지 않습니다.

이번 핸즈온의 기준은 아래입니다.

- 각자 노트북에서 Gemma 4를 미리 다운로드
- LM Studio, Ollama, llama.cpp 같은 로컬 실행 경로 사용
- 현장 인터넷이 불안정해도 기본 실습 진행 가능

`gemini-cli`는 공식 문서상 Gemini, Google 계정, Gemini API key, Vertex AI 중심의 사용 흐름이 먼저 나옵니다.
로컬 Gemma 4를 LM Studio 또는 Ollama의 OpenAI 호환 로컬 API 주소로 붙이는 방식은 이번 사전 준비의 기본 방식으로 잡기 어렵습니다.

따라서 이번 핸즈온에서는:

- 기본 고급 code agent: `OpenCode`
- 더 가벼운 대안: `pi`
- Gemini 중심 워크플로: 별도 실험 항목

로 구분합니다.

## 왜 `Antigravity`를 기본 code agent로 쓰지 않나요?

`Antigravity`도 이번 핸즈온의 기본 code agent로는 쓰지 않습니다.

이유는 단순합니다.

- 공개 공식 자료는 personal Gmail account와 preview 사용 흐름을 전제로 설명합니다.
- 설치, 에이전트 사용, rules/workflows, 보안 설정은 확인할 수 있지만, LM Studio나 localhost의 OpenAI 호환 로컬 API 주소에 로컬 Gemma 4를 연결하는 안정적인 기본 방식은 확인하기 어렵습니다.
- 따라서 이번 핸즈온의 핵심 조건인 **로컬 Gemma 4 + 사전 다운로드 + 오프라인 가능 실습**과는 맞지 않습니다.

Antigravity는 hosted model 중심 agent IDE를 써 보고 싶은 별도 실험 주제로 보면 됩니다.
이번 사전 준비에서는 로컬 실행이 쉬운 `OpenCode`, 그리고 더 가벼운 `pi`를 우선합니다.

## 참고 링크

- [Pi coding agent README](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)
- [Pi custom models docs](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/models.md)
- [Ollama Pi integration](https://docs.ollama.com/integrations/pi)
- [OpenCode 설치 및 LM Studio 연동 가이드](./10-opencode-lmstudio-developer-agent.md)
- [Gemini CLI README](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI `/model` docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md)
- [Gemini CLI issue: local/offline models](https://github.com/google-gemini/gemini-cli/issues/5938)
- [Gemini CLI discussion: OpenAI-compatible local model support](https://github.com/google-gemini/gemini-cli/discussions/24166)
- [Google Antigravity Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity)

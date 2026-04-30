# OpenCode 설치 및 LM Studio 연동 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- Gemma 4를 `개발자 에이전트`로 활용해 보고 싶은 분
- PM이 만든 PRD를 바탕으로 코드 구현 흐름을 실습해 보고 싶은 분
- LM Studio에 내려받은 로컬 Gemma 4 모델을 `opencode`와 연결하고 싶은 분

## 먼저 결론

- `opencode + LM Studio + Gemma 4` 조합은 **조건부로 적절합니다.**
- 이유는 `opencode`가 공식적으로 **로컬 모델 + LM Studio의 OpenAI 호환 로컬 API 주소** 구성을 지원하고, 에이전트별 **프롬프트 / 모델 / 권한 / 단계 수**를 설정할 수 있기 때문입니다.
- 다만 이 조합은 모두가 따라야 하는 기본 준비가 아니라, `개발자 에이전트`를 시연하거나 직접 실습해 보고 싶을 때의 추가 준비입니다.

왜 이렇게 보나요?

- OpenCode 공식 문서는 로컬 모델과 LM Studio 구성을 지원합니다.
- 하지만 OpenCode 공식 문서도 **코드 생성 + 툴 콜링을 모두 잘하는 모델은 많지 않다**고 설명합니다.
- 실제로는 `Gemma 4 E2B/E4B` 같은 소형 모델에서 코딩 에이전트 체감이 약하거나, 툴 사용 흐름이 흔들릴 수 있습니다.
- 커뮤니티 이슈에서도 Gemma 4와 로컬 OpenAI 호환 서버 조합에서 도구 호출(tool calling) 실패나 루프 현상이 보고되어 있어, **100% 안정성을 전제로 한 데모**로 잡는 것은 권장하지 않습니다.

권장:

- 발표자 데모: `26B A4B` 또는 `31B` 권장
- 32GB 이상: 추가 실습으로 고려 가능
- 16GB: `E4B`로 가벼운 코딩 보조 정도만 권장
- 8GB: `opencode` 기반 개발자 에이전트 실습은 비권장

## 어떤 방식이 가장 안정적인가요?

PRD를 한 번에 길게 넣고 곧바로 전체 구현을 시키기보다, 아래처럼 **2단계**로 나누면 더 안정적입니다.

1. `PM/Plan 단계`
   - PRD를 읽고 요구사항, 범위, 제약, 구현 순서를 짧은 체크리스트로 정리
2. `Developer 단계`
   - 정리된 체크리스트를 바탕으로 코드 탐색, 수정, 테스트 수행

이 방식이 좋은 이유:

- 작은 모델일수록 긴 문서와 다단계 작업을 한 번에 처리할 때 흔들리기 쉽습니다.
- 먼저 범위를 좁히면 도구 호출(tool calling)과 코드 수정 정확도가 상대적으로 나아질 수 있습니다.
- 발표 흐름도 더 명확합니다.

즉, 이번 핸즈온에서는

- `PM 역할`: PRD 정리와 구현 체크리스트 작성
- `Developer 역할`: 체크리스트 기반 구현

처럼 나누는 구성이 더 적절합니다.

## 모델 선택 권장

`opencode` 같은 코딩 에이전트 흐름에서는 일반 채팅보다 모델 요구치가 더 높습니다.

| 환경 | 권장 모델 | 안내 |
| --- | --- | --- |
| 8GB | 비권장 | `opencode` 기반 개발자 에이전트 실습은 권장하지 않습니다. |
| 16GB | `E4B` | 코드 읽기, 간단한 수정, 초안 생성 정도만 권장합니다. |
| 32GB | `26B A4B` 우선 | 가장 현실적인 로컬 개발자 에이전트 실습 구간입니다. |
| 36GB+ | `31B` 또는 `26B A4B` | 품질 우선이면 31B, 반응성 우선이면 26B A4B를 고려하세요. |

짧게 정리하면:

- `E2B`: 개발자 에이전트용으로는 비추천
- `E4B`: 가벼운 보조 수준
- `26B A4B`: 가장 현실적인 선택
- `31B`: 가능하면 가장 좋은 선택

## OpenCode 설치

이 가이드는 **CLI/TUI 기준**으로 설명합니다.
OpenCode Desktop 앱도 있지만, 개발자 에이전트 실습은 보통 터미널 기반 흐름이 더 단순합니다.

### macOS / Linux

가장 간단한 방법:

```bash
brew install anomalyco/tap/opencode
```

또는 설치 스크립트:

```bash
curl -fsSL https://opencode.ai/install | bash
```

설치 확인:

```bash
opencode --version
```

### Windows

OpenCode 공식 문서는 **Windows에서는 WSL 사용을 권장**합니다.

즉, 이 가이드의 OpenCode 설치와 실행 예시는 **PowerShell/CMD가 아니라 WSL 터미널 기준**입니다.

권장 순서:

1. PowerShell 관리자 권한으로 WSL 설치

```powershell
wsl --install -d Ubuntu
```

설치가 멈추면:

```powershell
wsl --install --web-download -d Ubuntu
```

2. PowerShell에서 Ubuntu 실행

```powershell
wsl -d Ubuntu
```

3. WSL 터미널에서 OpenCode 설치

```bash
curl -fsSL https://opencode.ai/install | bash
```

설치 확인:

```bash
opencode --version
```

WSL 사용 시 프로젝트가 Windows 파일에 있다면 예시는 아래와 같습니다.

```bash
cd /mnt/c/Users/YourName/project
opencode
```

## LM Studio와 연결하기

### 1. LM Studio에서 Gemma 4 모델 준비

먼저 LM Studio에서 아래 중 하나를 다운로드하고 테스트합니다.

- `google/gemma-4-e4b` 계열의 **instruction-tuned / chat-ready** 모델
- `google/gemma-4-26b-a4b` 계열의 **instruction-tuned / chat-ready** 모델
- `google/gemma-4-31b` 계열의 **instruction-tuned / chat-ready** 모델

가능하면 행사 전 아래까지 확인해 두세요.

- 모델 다운로드 완료
- Chat 탭에서 1회 답변 생성 성공
- Hugging Face나 `llama.cpp` 예시에서는 보통 `...-it` 접미사가 보이지만, LM Studio에서는 모델 ID가 더 짧게 정리되어 보일 수 있습니다.

### 2. LM Studio 로컬 서버 시작

방법 1. GUI

- LM Studio `Developer` 탭으로 이동
- `Start server`를 켭니다

방법 2. CLI

macOS / Linux / WSL:

```bash
lms server start
```

Windows에서 WSL을 쓰지 않고 LM Studio CLI만 확인할 때는 PowerShell에서 아래처럼 실행할 수 있습니다.

```powershell
lms server start
```

기본 엔드포인트는 아래입니다.

```text
http://127.0.0.1:1234/v1
```

### 3. 모델 목록 확인

아래 명령으로 LM Studio 서버가 보는 모델 목록을 확인합니다.

macOS / Linux / WSL:

```bash
curl http://127.0.0.1:1234/v1/models
```

Windows PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:1234/v1/models
```

여기서 보이는 **실제 모델 identifier** 를 확인해 두는 것이 안전합니다.  
문서 예시에서는 `google/gemma-4-e4b` 같은 ID를 사용하지만, 실제 환경에서는 내려받은 모델 항목에 따라 표시 문자열이 다를 수 있습니다.  
중요한 것은 이름 자체보다 **instruction-tuned / chat-ready 모델을 선택했는지** 입니다.

## `opencode.json` 예시

프로젝트 루트에 `opencode.json` 파일을 두는 방식을 권장합니다.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "lmstudio/google/gemma-4-e4b",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://127.0.0.1:1234/v1"
      },
      "models": {
        "google/gemma-4-e4b": {
          "name": "Gemma 4 E4B (local)"
        },
        "google/gemma-4-26b-a4b": {
          "name": "Gemma 4 26B A4B (local)"
        },
        "google/gemma-4-31b": {
          "name": "Gemma 4 31B (local)"
        }
      }
    }
  },
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "pnpm *": "allow",
      "bun *": "allow"
    },
    "edit": "ask"
  }
}
```

중요:

- `model` 값 형식은 `provider/model-id` 입니다.
- 위 예시에서 provider는 `lmstudio`, model-id는 `google/gemma-4-e4b` 입니다.
- 실제 모델 ID가 다르면 `curl http://127.0.0.1:1234/v1/models` 또는 PowerShell의 `Invoke-RestMethod http://127.0.0.1:1234/v1/models` 결과에 맞춰 수정하세요.
- Hugging Face나 `llama.cpp` 예시에서는 `gemma-4-26b-a4b-it` 같은 ID가 더 직접적으로 보일 수 있습니다.

## 개발자 에이전트 페르소나 예시

OpenCode는 에이전트별로 프롬프트와 권한을 설정할 수 있습니다.  
즉, `PM`, `Developer`, `Reviewer` 같은 역할을 분리하는 구성이 가능합니다.

행사에서는 다음처럼 단순하게 구성합니다.

- `plan` 또는 PM 역할: PRD 해석, 범위 정리
- `developer` 역할: 코드 구현

예시 `opencode.json` 확장:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "lmstudio/google/gemma-4-e4b",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://127.0.0.1:1234/v1"
      },
      "models": {
        "google/gemma-4-e4b": {
          "name": "Gemma 4 E4B (local)"
        },
        "google/gemma-4-26b-a4b": {
          "name": "Gemma 4 26B A4B (local)"
        }
      }
    }
  },
  "agent": {
    "developer": {
      "mode": "primary",
      "model": "lmstudio/google/gemma-4-26b-a4b",
      "prompt": "{file:./prompts/developer-agent.txt}",
      "steps": 6,
      "permission": {
        "bash": {
          "*": "ask",
          "git *": "allow",
          "npm *": "allow",
          "pnpm *": "allow",
          "bun *": "allow"
        },
        "edit": "ask"
      }
    }
  }
}
```

권장 모델 치환:

- 16GB 전후: `developer.model`도 `lmstudio/google/gemma-4-e4b`로 두세요.
- 32GB 이상: `lmstudio/google/gemma-4-26b-a4b` 권장
- 36GB 이상: 필요하면 `lmstudio/google/gemma-4-31b` 고려

예시 `prompts/developer-agent.txt`:

```text
You are the Developer employee in this AI Office.

Your input is a PRD or a short implementation checklist created by the PM.

Your job:
1. Summarize the task briefly.
2. Inspect the codebase before changing anything.
3. Propose a small implementation plan.
4. Make the smallest reasonable code change.
5. Report assumptions, risks, and test results clearly.

Rules:
- Do not make unrelated changes.
- Prefer small diffs.
- If the PRD is too broad, ask to narrow the scope.
- If tool use fails or becomes unstable, fall back to a text plan instead of hallucinating success.
```

## 실제 사용 순서 예시

1. 프로젝트 폴더에서 `opencode` 실행
2. 필요하면 `/models` 로 `lmstudio/google/gemma-4-e4b` 또는 `lmstudio/google/gemma-4-26b-a4b` 선택
3. `plan` 또는 PM 역할로 PRD를 짧은 구현 체크리스트로 정리
4. `developer` 에이전트로 전환
5. 체크리스트를 넣고 구현 요청

예시 흐름:

```text
이 PRD를 읽고 이번 세션에서 구현할 최소 범위를 5개 이하 체크리스트로 정리해 줘.
```

그 다음:

```text
이 체크리스트를 기준으로 현재 코드베이스를 확인하고, 가장 작은 단위부터 구현해 줘.
```

## OpenCode 실습 주의사항

- `opencode`는 이번 행사에서 필수 준비 항목이 아닙니다.
- `E2B`, `E4B`는 일반 채팅보다 코딩 에이전트 체감이 약할 수 있습니다.
- 특히 작은 로컬 모델은 도구 호출(tool calling), 긴 PRD 처리, 다단계 수정 흐름에서 흔들릴 수 있습니다.
- 짧은 PRD, 좁은 구현 범위, 작은 단계, `ask` 기반 권한 설정을 권장합니다.
- 가능하면 `26B A4B` 또는 `31B` 모델에서 실습하는 것이 좋습니다.

## 참고 링크

- [OpenCode Intro](https://opencode.ai/docs/)
- [OpenCode Providers](https://opencode.ai/docs/providers)
- [OpenCode Models](https://opencode.ai/docs/models)
- [OpenCode Agents](https://opencode.ai/docs/agents)
- [OpenCode Permissions](https://opencode.ai/docs/permissions)
- [OpenCode Windows (WSL)](https://opencode.ai/docs/windows-wsl/)
- [OpenCode GitHub](https://github.com/anomalyco/opencode)
- [LM Studio local server](https://lmstudio.ai/docs/developer/core/server)
- [LM Studio OpenAI 호환 endpoint 문서](https://lmstudio.ai/docs/developer/openai-compat)
- [LM Studio List Models](https://lmstudio.ai/docs/developer/openai-compat/models)
- [OpenCode issue: Gemma 4 e4b tool calling fails via Ollama](https://github.com/anomalyco/opencode/issues/20995)
- [OpenCode issue: Gemma 4 26B / 31B interaction issues](https://github.com/anomalyco/opencode/issues/21034)

더 가벼운 대안은 [Pi 경량 코딩 에이전트 대안과 이번 핸즈온 선택 이유](./11-pi-and-tool-selection-notes.md) 문서를 확인해 주세요.

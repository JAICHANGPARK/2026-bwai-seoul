# Gemini CLI Gemma 4 Preview 및 Gemma 라우팅 사전 준비 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

기준 확인일: 2026-05-01

## 이 문서는 누구를 위한 문서인가요?

- 이미 `Gemini CLI`를 쓰고 있거나, 행사 전에 추가로 설치해 보고 싶은 분
- Gemini CLI preview에서 `Gemma 4` 모델 선택을 확인해 보고 싶은 분
- Gemma 4 모델이 선택은 되지만 실제 응답에서 막힐 수 있다는 점을 미리 알고 싶은 분
- `gemini gemma setup`이 실제로 무엇을 내려받는지 헷갈리는 분
- `LM Studio`나 `Ollama` 기본 준비와 별개로, Gemini CLI의 Gemma 실험 기능을 미리 확인하고 싶은 분

## Gemini CLI란 무엇인가요?

Gemini CLI는 Google의 Gemini 모델을 터미널에서 직접 사용할 수 있게 해 주는 오픈소스 AI 에이전트입니다.  
단순히 질문과 답변만 주고받는 채팅 앱이 아니라, 개발자가 터미널 안에서 자연어로 작업을 요청하고, 필요하면 파일 읽기/수정, 셸 명령 실행, 웹 검색/가져오기 같은 도구를 함께 사용할 수 있게 만든 CLI 도구입니다.

공식 문서 기준으로 Gemini CLI는 아래처럼 구성됩니다.

- 사용자는 터미널에서 `gemini` 명령으로 대화형 세션을 시작합니다.
- CLI 프런트엔드는 로컬의 core 프로세스와 통신합니다.
- core는 Gemini API와 모델 호출, 파일 시스템 도구, 셸 도구, 웹 도구 등을 관리합니다.
- `/model`, `/settings`, `/gemma` 같은 슬래시 명령으로 세션 중 설정과 상태를 바꿀 수 있습니다.

이번 행사 준비 관점에서 중요한 점:

- Gemini CLI는 `LM Studio`나 `Ollama`처럼 Gemma 4 모델 파일을 내려받아 로컬 채팅 앱으로 실행하는 기본 준비 방식이 아닙니다.
- Gemini CLI의 일반 대화와 도구 사용은 Gemini 계정/API 키/조직 설정의 영향을 받습니다.
- preview에서 Gemma 4 모델을 선택할 수 있어도, 실제 호출 권한은 별도로 필요합니다.
- `gemini gemma setup`은 Gemma 4 로컬 실행이 아니라, Gemma 3 기반 로컬 라우터를 준비하는 경로입니다.

따라서 Gemini CLI는 이번 세션에서 **개발자용 추가 실험 항목**으로 보는 것이 가장 안전합니다.

## 먼저 결론

Gemini CLI의 Gemma 관련 기능은 현재 두 갈래로 나눠서 이해해야 합니다.

| 구분 | 필요한 버전/명령 | 확인되는 모델 | 의미 |
| --- | --- | --- | --- |
| Gemma 4 모델 선택 | `@google/gemini-cli@preview` + `experimental.gemma` | `gemma-4-26b-a4b-it`, `gemma-4-31b-it` | Gemini CLI에서 Gemma 4 모델을 실험적으로 선택하는 경로 |
| 로컬 Gemma 라우터 | `gemini gemma` 또는 `gemini gemma setup` | `gemma3-1b-gpu-custom` | LiteRT-LM으로 로컬 라우팅 판단용 Gemma 3 모델을 준비하는 경로 |
| Gemma 4 로컬 실행 | `LM Studio`, `Ollama`, `llama.cpp` | Gemma 4 E2B/E4B/26B/31B | 이번 행사 기본 로컬 실행 경로 |

중요:

- `v0.41.0-preview.0`에는 Gemma 4 모델 지원이 실험 기능으로 들어왔습니다.
- 하지만 `gemini gemma setup`에서 내려받는 모델은 여전히 `gemma3-1b-gpu-custom`으로 보입니다.
- 따라서 `Gemma 4 모델 선택 지원`과 `Gemma 3 로컬 라우터 설치`는 같은 기능이 아닙니다.
- Gemini CLI preview에서 Gemma 4 모델을 선택할 수 있어도, 그것이 Gemma 4를 LiteRT-LM으로 로컬 다운로드해 실행한다는 뜻은 아닙니다.
- `/model` 목록에서 Gemma 4를 고를 수 있고 선택 상태로 보이더라도, 실제 메시지를 보내면 권한 오류로 응답이 막힐 수 있습니다.
- 행사 기본 사전 준비는 여전히 `LM Studio` 또는 `Ollama`입니다.

## 선택 가능과 응답 가능은 다릅니다

현재 Gemini CLI preview에서는 `/model` 목록에 `gemma-4-26b-a4b-it`, `gemma-4-31b-it` 같은 Gemma 4 모델이 보이고, 선택까지는 정상적으로 되는 경우가 있습니다.

하지만 이것만으로 실제 실행 권한이 확인된 것은 아닙니다.  
모델을 선택한 뒤 첫 메시지를 보냈을 때 아래처럼 접근 권한 오류가 날 수 있습니다.

```text
It seems like you don't have access to gemma-4-26b-a4b-it.
Your admin might have disabled the access. Contact them to enable the Preview Release Channel.
```

이 경우는 "모델 선택 UI 확인"까지만 성공한 상태입니다.  
Gemma 4 preview를 실제로 쓸 수 있다고 보려면, 모델을 선택한 뒤 짧은 메시지까지 응답에 성공해야 합니다.

행사 준비 관점에서는 이 상태를 실패로 오래 붙잡지 마세요.  
Gemini CLI preview 권한 문제는 현장에서 바로 해결하기 어려울 수 있으므로, Gemma 4 로컬 실행은 `LM Studio` 또는 `Ollama`로 먼저 준비하는 편이 안전합니다.

## 공식 문서 기준으로 알아둘 점

Gemini CLI 공식 문서의 `Model routing`, `gemini gemma`, `Manual Local Model Routing` 문서를 함께 보면 구조가 조금 더 분명해집니다.

### 1. Gemini CLI에는 기본 모델 라우팅이 있습니다

Gemini CLI는 선택한 모델이 쿼터, 서버 오류 같은 이유로 실패할 때 다른 모델로 전환할 수 있는 모델 라우팅 기능을 갖고 있습니다. 이 기능은 기본으로 켜져 있으며, 모델 상태는 `ModelAvailabilityService`가 확인합니다.

흐름은 보통 아래처럼 이해하면 됩니다.

1. 현재 선택한 모델 호출이 실패합니다.
2. 정책에 따라 fallback 모델로 바꿀지 물어볼 수 있습니다.
3. 전환을 승인하거나, 정책상 조용히 전환해도 되는 경우에는 현재 턴 또는 남은 세션에서 fallback 모델을 사용합니다.

다만 prompt completion, classification 같은 내부 보조 호출은 현재 선택한 대화 모델을 바꾸지 않고 조용히 대체 호출 흐름을 탈 수 있습니다. 공식 문서에는 `gemini-2.5-flash-lite`에서 실패하면 `gemini-2.5-flash`, `gemini-2.5-pro`로 넘어갈 수 있다고 설명되어 있습니다.

### 2. Local Model Routing은 "Gemma 4 로컬 채팅"이 아닙니다

공식 `gemini gemma` 문서에서 말하는 Local Model Routing은 로컬 Gemma 모델이 **요청을 분류하고 라우팅 결정을 돕는 기능**입니다. 예를 들어 단순한 파일 읽기 요청은 Flash 쪽으로, 복잡한 설계 논의는 Pro 쪽으로 보내는 식입니다.

여기서 로컬로 받는 모델은 현재 공식 문서 기준 `Gemma 3 1B` 계열인 `gemma3-1b-gpu-custom`입니다.  
즉, `gemini gemma setup`은 Gemma 4 모델 파일을 받아서 로컬 채팅을 하는 명령이 아니라, **라우팅 판단용 로컬 분류기**를 준비하는 명령입니다.

### 3. 자동 설정은 `gemini gemma setup`이 담당합니다

공식 문서 기준 `gemini gemma setup`은 아래 작업을 한 번에 처리합니다.

- LiteRT-LM 런타임 다운로드
- `gemma3-1b-gpu-custom` 모델 다운로드
- Gemma 약관 동의 확인
- Gemini CLI 설정 반영
- 로컬 LiteRT 서버 시작

설정이 끝나면 평소처럼 Gemini CLI를 쓰면 되고, 라우팅은 요청마다 자동으로 일어납니다. 로컬 LiteRT 서버가 내려가면 CLI는 오류로 멈추기보다 클라우드 분류기로 조용히 되돌아갈 수 있습니다.

## 행사 준비에서 어떻게 봐야 하나요?

Gemini CLI Gemma 기능은 흥미롭지만, 모두가 설치할 필요는 없습니다.

해 보면 좋은 경우:

- 개발자이거나 터미널 사용에 익숙한 경우
- CLI 도구 설치와 설정 변경이 부담스럽지 않은 경우
- Gemini CLI를 이미 쓰고 있는 경우
- preview 버전의 불안정성을 감안할 수 있는 경우
- Gemini CLI에서 Gemma 4 모델 선택 UI/명령을 확인해 보고 싶은 경우

먼저 하지 않아도 되는 경우:

- 설치를 최소화하고 싶은 경우
- GUI 중심으로 실습하고 싶은 경우
- 8GB 장비에서 기본 Gemma 4 실행 준비도 아직 끝나지 않은 경우
- "Gemini CLI preview만 설치하면 Gemma 4가 완전히 로컬 실행된다"는 기대가 있는 경우

8GB 장비에서도 Gemini CLI 설치 자체는 가능할 수 있지만, 행사 준비 우선순위는 `LM Studio` 또는 `Ollama`에서 작은 Gemma 4 모델을 먼저 실행해 보는 것입니다.

## 사전 요구사항

- Node.js 20 이상
- 안정적인 인터넷 연결
- 디스크 여유 공간 최소 2GB 이상
- 터미널 사용 가능 환경
- Gemini CLI 로그인 또는 API 키 설정
- Gemma Terms of Use 확인 및 동의

Gemini CLI 자체는 메인 대화에 Gemini 계정 또는 API 인증을 사용합니다.  
로컬 Gemma 라우터를 설정해도 Gemini CLI의 일반 대화가 모두 오프라인으로 바뀌는 것은 아닙니다.

## 설치 버전 선택

### Gemma 4 모델 선택을 확인하려면 preview 설치

Gemini CLI에서 Gemma 4 모델 선택을 확인하려면 preview 버전을 설치합니다.

```bash
npm install -g @google/gemini-cli@preview
```

설치 확인:

```bash
gemini --version
```

이 문서는 `v0.41.0-preview.0` 이상 preview를 기준으로 합니다.

### 안정성을 우선하면 latest/stable 사용

행사 기본 실습에는 Gemini CLI가 필수가 아닙니다.  
Gemini CLI를 꼭 써야 하는 것이 아니라면 `LM Studio` 또는 `Ollama` 준비를 먼저 끝내세요.

Gemini CLI를 안정 경로로만 쓰고 싶다면 일반 설치를 사용할 수 있습니다.

```bash
npm install -g @google/gemini-cli@latest
```

다만 Gemma 4 모델 선택 실험 기능은 preview 기준으로 보는 것이 안전합니다.

## Gemini CLI 사전 설정

Gemma 4 preview 모델 선택을 확인하려면 설치뿐 아니라 Gemini CLI 설정도 미리 확인해야 합니다.

설정 파일 위치:

- 사용자 설정: `~/.gemini/settings.json`
- 프로젝트 설정: `your-project/.gemini/settings.json`

중요:

- 프로젝트 설정은 사용자 설정을 덮어씁니다.
- 개인 설정은 가능하면 `~/.gemini/settings.json`에 두세요.
- 프로젝트의 `.gemini/settings.json`에 실험 기능을 커밋하면 다른 사람의 환경에도 영향을 줄 수 있으므로 권장하지 않습니다.

Gemini CLI 세션 안에서 설정을 여는 방법:

```bash
gemini
```

세션 안에서:

```text
/settings
```

`Gemma Models` 또는 Gemma 관련 experimental 항목을 켭니다.

직접 설정 파일을 수정해야 한다면 `~/.gemini/settings.json`에 아래 값을 병합합니다.

```json
{
  "experimental": {
    "gemma": true
  }
}
```

이미 `settings.json`이 있다면 파일 전체를 덮어쓰지 말고, 기존 설정 안에 `experimental.gemma`만 추가하세요.  
설정 변경 후에는 Gemini CLI를 다시 시작하는 것이 안전합니다.

Gemma 4 모델을 기본 모델로 고정하고 싶다면 아래처럼 `model.name`을 추가할 수 있습니다.

```json
{
  "experimental": {
    "gemma": true
  },
  "model": {
    "name": "gemma-4-26b-a4b-it"
  }
}
```

다만 호출 권한이 없는 계정에서 기본 모델을 Gemma 4로 고정하면 Gemini CLI 시작 후 계속 오류를 만날 수 있습니다.  
처음에는 `/model`에서 직접 선택하거나 `gemini --model gemma-4-26b-a4b-it`로 테스트한 뒤, 실제 호출이 성공할 때만 기본 모델로 저장하세요.

로컬 Gemma 라우터 관련 설정은 `gemini gemma` 또는 `gemini gemma setup`이 처리하는 것을 우선 권장합니다. 수동 설정이 필요할 때만 `experimental.gemmaModelRouter`를 직접 편집하세요.

## 모델 선택 우선순위

Gemini CLI에서 어떤 대화 모델을 쓸지는 공식 문서 기준 아래 순서로 결정됩니다.

1. 실행할 때 넘긴 `--model` 플래그
2. `GEMINI_MODEL` 환경 변수
3. `settings.json`의 `model.name`
4. `settings.json`에서 켠 로컬 Gemma 라우터
5. 기본값 `auto`

실습에서 헷갈리기 쉬운 부분은 4번입니다.  
로컬 Gemma 라우터를 켰다고 해서 대화 모델이 `gemma3-1b-gpu-custom`으로 바뀌는 것은 아닙니다. `gemma3-1b-gpu-custom`은 "이번 요청을 어떤 hosted Gemini 모델로 보낼지" 판단하는 데 쓰입니다.

따라서 Gemma 4 preview 모델을 명시적으로 테스트하려면 아래처럼 직접 모델을 지정하는 편이 가장 분명합니다.

```bash
gemini --model gemma-4-26b-a4b-it
```

기존 문서나 CLI 출력에서 `-m` 축약형을 쓰는 경우도 있지만, 처음 확인할 때는 공식 문서에서 설명하는 `--model` 형태가 더 읽기 쉽습니다.

## Gemma 4 모델 선택 확인

preview 설치와 `experimental.gemma` 설정이 끝났다면 Gemma 4 모델을 직접 지정해 볼 수 있습니다.

```bash
gemini --model gemma-4-26b-a4b-it
```

또는:

```bash
gemini --model gemma-4-31b-it
```

Gemini CLI 세션 안에서는 `/model` 명령으로 선택 가능한 모델 목록을 확인해 보세요.

```text
/model
```

주의:

- 계정, API 키, 지역, preview 접근 권한에 따라 모델 호출이 실패할 수 있습니다.
- `/model` 목록에 Gemma 4가 보여도 실제 호출 권한이 있다는 뜻은 아닙니다.
- 이 경로는 `gemini gemma setup`으로 Gemma 4 모델 파일을 로컬에 내려받는 방식이 아닙니다.
- 현재 확인되는 Gemini CLI 내장 Gemma 4 모델 ID는 `gemma-4-26b-a4b-it`, `gemma-4-31b-it`입니다.
- E2B/E4B까지 CLI 모델 선택에 표시되는지는 실제 `/model` 목록을 기준으로 확인하세요.

실제 호출 권한이 없으면 아래와 비슷한 메시지가 나올 수 있습니다.

```text
It seems like you don't have access to gemma-4-26b-a4b-it.
Your admin might have disabled the access. Contact them to enable the Preview Release Channel.
```

이 경우 Gemini CLI Gemma 4 preview는 **모델 목록 확인까지만 성공**한 상태입니다.  
행사 준비 완료 기준으로는 `LM Studio` 또는 `Ollama`에서 Gemma 4 로컬 실행을 먼저 완료하세요.

## 로컬 Gemma 라우터 설정

Gemini CLI의 로컬 라우터도 확인하고 싶다면 아래 명령을 실행합니다.

```bash
gemini gemma
```

버전에 따라 setup 하위 명령을 안내하면 아래처럼 실행합니다.

```bash
gemini gemma setup
```

실행 중에는 LiteRT-LM 런타임과 `gemma3-1b-gpu-custom` 모델 다운로드를 안내합니다.  
실행 화면에는 모델 다운로드 크기가 약 1GB로 안내될 수 있습니다.

진행 중 확인할 것:

- Gemma Terms of Use 링크를 열어 확인
- 약관 동의 여부 선택
- LiteRT-LM 런타임 다운로드
- `gemma3-1b-gpu-custom` 모델 다운로드
- 설정 완료 메시지 확인

이 단계는 행사장 네트워크에서 처음 실행하지 않는 것이 좋습니다.

공식 문서 기준으로 함께 알아둘 명령은 아래와 같습니다.

| 명령 | 하는 일 |
| --- | --- |
| `gemini gemma setup` | LiteRT-LM, 모델, 설정, 서버 시작까지 한 번에 처리 |
| `gemini gemma status` | 설치 상태와 서버 실행 상태 확인 |
| `gemini gemma start` | LiteRT 서버 시작 |
| `gemini gemma stop` | LiteRT 서버 중지 |
| `gemini gemma logs` | 라우팅 요청 로그 확인 |
| `/gemma` | Gemini CLI 세션 안에서 Gemma 라우터 상태 확인 |

포트나 다운로드 방식을 조정해야 할 때는 setup 플래그를 쓸 수 있습니다.

```bash
gemini gemma setup --port 8080
gemini gemma setup --no-start
gemini gemma setup --force
gemini gemma setup --skip-model
```

처음 준비한다면 플래그 없이 `gemini gemma setup`만 실행하는 쪽이 가장 단순합니다.

## 상태 확인

자동 설정 후에는 먼저 상태를 확인합니다.

```bash
gemini gemma status
```

조금 더 확실히 보려면 터미널을 두 개 열어 확인할 수 있습니다.

```bash
gemini gemma logs
```

다른 터미널에서 Gemini CLI를 평소처럼 실행합니다.

```bash
gemini
```

세션 안에서:

```text
/gemma
```

여기서 Gemma 라우터가 설정되어 있는지 확인합니다.

추가로 짧은 질문을 한 번 보내 Gemini CLI 일반 응답도 확인하세요.

```text
간단히 자기소개를 한 문장으로 해줘.
```

## 완료 기준

### Gemma 4 preview 모델 선택 완료 기준

- `gemini --version`이 `v0.41.0-preview.0` 이상 preview로 표시됨
- `experimental.gemma` 설정을 켰음
- 사용자 설정 또는 프로젝트 설정 중 어디에서 설정이 적용되는지 확인함
- Gemini CLI 세션에서 `/model` 목록을 확인함
- `gemini --model gemma-4-26b-a4b-it` 또는 `gemini --model gemma-4-31b-it`로 짧은 질문에 응답 성공

모델 목록에는 보이지만 `You don't have access` 또는 `Preview Release Channel` 관련 오류가 나오면 Gemma 4 preview **호출 준비는 미완료**로 보세요.

### 로컬 Gemma 라우터 완료 기준

- `gemini gemma setup`이 끝남
- `gemma3-1b-gpu-custom` 다운로드가 끝남
- `gemini gemma status`에서 설치와 서버 상태를 확인함
- Gemini CLI 세션에서 `/gemma` 상태 확인이 됨
- 짧은 일반 질문에 Gemini CLI가 응답함

## 수동 설정이 필요한 경우

자동 설정이 실패하거나, LiteRT-LM 런타임을 직접 띄워야 하는 경우에는 공식 Local Model Routing 문서의 수동 설정을 확인하세요.

수동 설정은 아래 구조를 직접 준비하는 방식입니다.

- LiteRT-LM 런타임을 운영체제에 맞게 다운로드
- `gemma3-1b-gpu-custom` 모델을 pull
- LiteRT-LM을 예를 들어 `9379` 포트로 실행
- `settings.json`에 로컬 classifier 주소와 모델명을 설정

수동 설정의 핵심 설정은 아래와 같습니다.

```json
{
  "experimental": {
    "gemmaModelRouter": {
      "enabled": true,
      "classifier": {
        "host": "http://localhost:9379",
        "model": "gemma3-1b-gpu-custom"
      }
    }
  }
}
```

자동 설정을 사용했다면 이 값을 직접 만들 필요가 없을 수 있습니다.  
설정 변경 후에는 Gemini CLI를 다시 시작해야 반영됩니다.

문서와 실제 CLI 동작은 버전에 따라 빠르게 바뀔 수 있으므로, 우선 `gemini gemma setup` 명령을 기준으로 따라가세요.

## 자주 생기는 오해

### preview를 설치하면 Gemma 4를 쓸 수 있나요?

Gemini CLI의 모델 선택 경로에서는 가능해진 것으로 보입니다.  
다만 `experimental.gemma`를 켜야 하고, 실제 호출은 계정/키/preview 접근 권한의 영향을 받을 수 있습니다.

### `gemini gemma setup`이 Gemma 3를 받는 게 이상한가요?

아닙니다. 현재 `gemini gemma setup` 준비 흐름에서 확인되는 로컬 모델은 `gemma3-1b-gpu-custom`입니다.  
이 모델은 Gemma 4 채팅 모델이 아니라, 라우팅 판단을 위한 로컬 모델로 이해해야 합니다.

### Gemini CLI preview가 Gemma 4를 완전히 오프라인으로 실행하나요?

아닙니다. preview의 Gemma 4 모델 지원은 CLI 모델 선택/호출 경로의 실험 기능으로 봐야 합니다.  
Gemma 4를 로컬 파일로 내려받아 오프라인 실행하려면 이 저장소의 `LM Studio`, `Ollama`, `llama.cpp` 문서를 보세요.

### 기존 기본 준비 문서 대신 이것만 하면 되나요?

아닙니다. 이 문서는 선택형 추가 준비입니다.  
행사 기본 실습 준비는 `LM Studio` 또는 `Ollama`에서 Gemma 4 모델을 미리 내려받고 1회 실행해 보는 것입니다.

### 설정 파일을 프로젝트에 커밋해야 하나요?

개인 설정이면 `~/.gemini/settings.json`에 두세요.  
개인 환경 설정을 프로젝트 `.gemini/settings.json`으로 커밋하는 것은 권장하지 않습니다.

## 트러블슈팅

### Gemma 4 모델이 목록에 안 보일 때

- `gemini --version`이 preview인지 확인합니다.
- `v0.41.0-preview.0` 미만이면 preview로 업데이트합니다.
- `/settings`에서 Gemma experimental 항목을 켰는지 확인합니다.
- Gemini CLI를 완전히 종료한 뒤 다시 실행합니다.

```bash
npm install -g @google/gemini-cli@preview
```

### `gemini --model gemma-4-26b-a4b-it`가 실패할 때

- `/model` 목록에 보여도 실제 호출 권한은 별도로 필요합니다.
- `It seems like you don't have access to ...` 메시지가 나오면 현재 계정 또는 조직 설정에서 해당 preview 모델 호출이 막힌 상태로 봅니다.
- `Your admin might have disabled the access. Contact them to enable the Preview Release Channel.` 메시지가 나오면 조직/관리자 계정에서 Preview Release Channel 허용이 필요할 수 있습니다.
- 개인 계정이나 별도 API 키로 다시 로그인/설정해 볼 수 있지만, 행사장에서 이 문제를 해결하려고 시간을 쓰지 않는 것을 권장합니다.
- preview 기능이므로 일시적으로 동작이 바뀔 수 있음을 감안합니다.
- 행사 실습 준비가 목적이면 `LM Studio` 또는 `Ollama`의 Gemma 4 로컬 실행을 우선하세요.

### `gemini gemma` 명령이 없다고 나올 때

- `gemini --version`으로 버전을 확인합니다.
- `v0.40.0` 미만이면 Gemini CLI를 업데이트합니다.

```bash
npm install -g @google/gemini-cli@latest
```

### `/gemma`에서 준비되지 않았다고 나올 때

- `/settings`에서 Gemma experimental 항목을 켰는지 확인합니다.
- Gemini CLI를 완전히 종료한 뒤 다시 실행합니다.
- `gemini gemma`를 다시 실행합니다.

### `gemini gemma setup`에서 Gemma 3 모델을 받는다고 나올 때

현재 정상 동작으로 보세요.  
이 명령은 Gemma 4 모델 선택 기능이 아니라, LiteRT-LM 기반 로컬 라우팅 설정 경로입니다.

### 다운로드가 오래 걸릴 때

- 모델과 런타임을 행사 전에 미리 받으세요.
- 회사/학교 네트워크에서 GitHub 또는 Google 다운로드가 막혀 있으면 개인 네트워크에서 준비하세요.
- 디스크 여유 공간을 확인하세요.

### macOS에서 LiteRT-LM 실행이 막힐 때

macOS 보안 설정 때문에 다운로드한 바이너리 실행이 막힐 수 있습니다.

- `System Settings -> Privacy & Security`에서 허용
- 또는 공식 문서의 quarantine 해제 안내 확인

### Windows에서 실행이 막힐 때

- PowerShell을 새로 열어 다시 실행합니다.
- 보안 프로그램이나 방화벽이 로컬 런타임 실행을 막는지 확인합니다.
- 관리자 권한이 필요한 환경이면 설치 권한을 먼저 확인합니다.

## 참고 링크

- [Gemini CLI v0.41.0-preview.0 release](https://github.com/google-gemini/gemini-cli/releases/tag/v0.41.0-preview.0)
- [Gemma 4 support PR #25604](https://github.com/google-gemini/gemini-cli/pull/25604)
- [Gemini CLI v0.40.0 GitHub discussion #26216](https://github.com/google-gemini/gemini-cli/discussions/26216)
- [Gemini CLI README](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI settings reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md)
- [Gemini CLI model selection reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md)
- [Gemini CLI CLI reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md)
- [Gemini CLI Model Routing](https://geminicli.com/docs/cli/model-routing/)
- [Gemini CLI `gemini gemma` setup](https://geminicli.com/docs/core/gemma-setup/)
- [Gemini CLI Manual Local Model Routing](https://geminicli.com/docs/core/local-model-routing/)
- [Gemma Terms of Use](https://ai.google.dev/gemma/terms)
- [Gemma Prohibited Use Policy](https://ai.google.dev/gemma/prohibited_use_policy)

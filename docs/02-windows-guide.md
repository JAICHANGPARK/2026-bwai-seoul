# Windows 참가자 빠른 준비 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- Windows 노트북으로 이번 핸즈온에 참가하는 분
- Apple Silicon Mac이 아니라 일반적인 `Windows x64` 또는 `Windows ARM` 장비를 쓰는 분
- 어떤 도구를 설치해야 할지 빠르게 결정하고 싶은 분

## 먼저 결론

- Windows 참가자의 **기본 권장 경로는 LM Studio**입니다.
- CLI/API도 같이 써 보고 싶으면 **Ollama**를 추가로 설치하면 됩니다.
- `llama.cpp`는 **고급 / 선택형 경로**입니다.
- `Hermes Agent`는 Windows 네이티브가 아니라 **WSL2 안에서만 공식 지원**이므로, 모든 참가자에게 기본으로 권하지 않습니다.

즉 가장 현실적인 준비 순서는 아래입니다.

1. **기본 참가자**: `LM Studio`
2. **CLI까지 써 보고 싶은 참가자**: `LM Studio + Ollama`
3. **고급 참가자**: `LM Studio 또는 llama.cpp + WSL2 안의 Hermes`

## 어떤 도구를 설치하면 되나요?

### 경로 A: 가장 쉬운 기본 경로

설치:

- `LM Studio`

이 경로가 적합한 사람:

- GUI가 편한 분
- 로컬 모델을 한 번 실행해 보는 것이 우선인 분
- 핸즈온 현장에서 가장 안정적인 경로를 원하는 분

### 경로 B: 기본 + CLI/API 경로

설치:

- `LM Studio`
- `Ollama`

이 경로가 적합한 사람:

- GUI와 터미널 둘 다 써 보고 싶은 분
- 나중에 로컬 API를 붙여 보고 싶은 분
- 발표 도중 CLI 예시도 따라가 보고 싶은 분

### 경로 C: 고급 에이전트 경로

설치:

- `LM Studio` 또는 `llama.cpp`
- `WSL2`
- `Hermes Agent`는 WSL2 안에 설치

이 경로가 적합한 사람:

- `Hermes + Gemma 4` AI office 데모를 직접 해 보고 싶은 분
- 로컬 OpenAI-compatible endpoint에 에이전트를 연결해 보고 싶은 분

## 추천 조합

| 목표 | 추천 조합 | 비고 |
| --- | --- | --- |
| 가장 쉬운 참가 | `LM Studio` | 기본 권장 |
| GUI + CLI 둘 다 | `LM Studio + Ollama` | 가장 무난한 확장 경로 |
| 직접 서버 띄우기 | `llama.cpp` | 고급 경로 |
| Hermes까지 실습 | `LM Studio 또는 llama.cpp + WSL2 + Hermes` | 선택형 고급 경로 |

## 메모리 기준 추천

| 메모리 | 추천 모델 | 권장 도구 |
| --- | --- | --- |
| 8GB | `E2B`만 best-effort | LM Studio 우선 |
| 16GB | `E4B` | LM Studio 우선, 필요하면 Ollama 추가 |
| 32GB | `E4B` 또는 `26B A4B` | LM Studio, Ollama, llama.cpp 선택 가능 |
| 36GB+ | `26B A4B` 또는 `31B` | 고급 경로도 현실적 |

중요:

- 8GB Windows 노트북은 가능한 경우 다른 장비를 권장합니다.
- 16GB가 가장 무난한 최소 기준에 가깝습니다.
- 발표자 데모용으로는 32GB 이상이 훨씬 여유롭습니다.

## Windows 참가자가 가장 먼저 해야 할 일

### 1. 기본 경로부터 끝내기

먼저 아래 중 **하나 이상**을 반드시 끝내세요.

- `LM Studio` 설치 + Gemma 4 실행 성공
- `Ollama` 설치 + `ollama run gemma4:e2b` 성공
- `llama.cpp` 설치 + `llama-server` 실행 성공

### 2. 모델도 미리 받아 두기

행사 당일에 모델을 처음 다운로드하지 않는 것이 중요합니다.

권장:

- 8GB: `E2B`
- 16GB: `E4B`
- 32GB+: `E4B` 또는 `26B A4B`

### 3. Hermes는 나중에

Windows 참가자는 `Hermes`를 가장 먼저 설치하기보다:

1. 모델이 실제로 한 번 도는지 먼저 확인
2. 그다음 필요하면 WSL2 + Hermes로 확장

이 순서가 훨씬 안전합니다.

## WSL2는 꼭 필요한가요?

- `LM Studio`: 필요 없음
- `Ollama`: 필요 없음
- `llama.cpp`: 필요 없음
- `Hermes Agent`: **필요함**

즉 Windows 참가자에게 WSL2는 **Hermes를 쓸 때만 필수**라고 이해하면 됩니다.

WSL2 설치는 PowerShell 관리자 권한으로 아래처럼 시작하면 됩니다.

```powershell
wsl --install -d Ubuntu
```

설치가 멈추면:

```powershell
wsl --install --web-download -d Ubuntu
```

설치 후 상태 확인:

```powershell
wsl --status
wsl --list --verbose
```

## Windows + Hermes 권장 아키텍처

Windows에서 `Hermes`까지 하고 싶다면 가장 안전한 조합은 아래입니다.

```text
Windows native:
  LM Studio or llama.cpp server

WSL2:
  Hermes Agent
```

즉:

1. Windows에서 모델 서버 실행
2. WSL2 안에서 Hermes 실행
3. Hermes가 `http://127.0.0.1:PORT/v1` 또는 host endpoint에 연결

이 방식이 좋은 이유:

- WSL2 안에서 대용량 모델을 다시 받지 않아도 됨
- Windows GPU/GUI 앱 활용이 쉬움
- Hermes는 공식 지원 방식인 WSL2 안에서 돌릴 수 있음

## 설치 우선순위

### 기본 참가자

1. [LM Studio 설치 가이드](./05-lm-studio-setup.md)
2. [트러블슈팅 / 최종 체크 / 참고 링크](./15-troubleshooting-and-final-check.md)

### CLI도 해 보고 싶은 참가자

1. [LM Studio 설치 가이드](./05-lm-studio-setup.md)
2. [Ollama 설치 가이드](./06-ollama-setup.md)
3. [트러블슈팅 / 최종 체크 / 참고 링크](./15-troubleshooting-and-final-check.md)

### Hermes까지 해 보고 싶은 참가자

1. [LM Studio 설치 가이드](./05-lm-studio-setup.md) 또는 [llama.cpp 설치 가이드](./07-llamacpp-setup.md)
2. PowerShell 관리자 권한으로 WSL2 준비

```powershell
wsl --install -d Ubuntu
```

3. Ubuntu 실행

```powershell
wsl -d Ubuntu
```

4. [Hermes Agent란 무엇인가](./12-hermes-agent-overview.md)
5. [Hermes Agent 설치 가이드](./13-hermes-agent-setup.md)

## 절대 행사 당일에 처음 하면 안 되는 것

- WSL2 첫 설치
- 큰 모델 첫 다운로드
- `Hermes + WSL2 + local server`를 한 번도 테스트하지 않은 상태로 참석
- 8GB 노트북에서 큰 모델을 현장에서 바로 시도

## 행사 전 최종 체크리스트

아래 중 자신이 선택한 경로에 맞는 항목만 확인하면 됩니다.

### LM Studio 경로

- 앱 설치 완료
- Gemma 4 다운로드 완료
- Chat 탭에서 1회 응답 생성 성공

### Ollama 경로

- `ollama --version`
- `ollama pull gemma4:e2b` 또는 `ollama pull gemma4:e4b`
- `ollama run gemma4:e2b` 또는 `ollama run gemma4:e4b`

### llama.cpp 경로

- `llama-cli --version`
- `llama-server --version`
- `llama-server` 또는 `llama-cli`로 1회 실행 성공
- 필요하면 `Invoke-RestMethod http://127.0.0.1:8080/v1/models` 확인

### Hermes 경로

- WSL2 설치 완료
- PowerShell에서 `wsl --status` 확인
- WSL2 터미널에서 `hermes version`
- `hermes doctor`
- local endpoint 연결 1회 성공

## 권장 한 줄 요약

- 대부분의 Windows 참가자: **LM Studio만 준비해도 충분**
- 조금 더 해 보고 싶으면: **Ollama 추가**
- AI office / agents까지 직접 하려면: **WSL2 + Hermes는 선택형 고급 경로**

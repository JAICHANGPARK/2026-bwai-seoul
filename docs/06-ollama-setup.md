# Ollama 설치 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 언제 보면 되나요?

- LM Studio 외에 CLI/API 방식도 함께 준비하고 싶을 때
- ChromeOS를 쓸 때
- Intel Mac처럼 LM Studio 데스크톱 앱이 맞지 않는 환경일 때

## Windows

이런 환경에 맞습니다:

- Windows 10 22H2 이상
- NVIDIA 또는 AMD GPU가 있으면 더 좋음

설치 순서:

1. 공식 다운로드 페이지로 이동합니다.  
   [Ollama Windows 다운로드](https://ollama.com/download/windows)
2. 가장 쉬운 방법은 설치 프로그램(`OllamaSetup.exe`)을 사용하는 것입니다.
3. 설치 후 PowerShell 또는 명령 프롬프트를 열고 아래 명령으로 확인합니다.

```powershell
ollama --version
```

4. 메모리에 맞는 Gemma 4 모델을 미리 받습니다.

```powershell
ollama pull gemma4:e2b
```

또는

```powershell
ollama pull gemma4:e4b
```

5. 실행 테스트:

```powershell
ollama run gemma4:e2b
```

권장 메모:

- Ollama Windows 설치는 공식 문서 기준 관리자 권한이 필수는 아닙니다.
- 모델은 기본적으로 사용자 홈 디렉터리 아래에 저장됩니다.
- 설치 후 Ollama는 백그라운드에서 실행되고, 로컬 API는 기본적으로 `http://localhost:11434`에서 동작합니다.
- Windows에서는 **명령 프롬프트(CMD)** 도 가능하지만, 이 가이드는 **PowerShell 기준**입니다.
- Ollama는 `gemma4:e2b`, `gemma4:e4b` 같은 런타임 태그를 사용하므로, 사용자가 따로 `-it` 접미사를 고르지 않아도 됩니다. 핸즈온에서는 이 태그들을 chat-ready 실행 경로로 이해하면 됩니다.

## Gemma 4 태그 선택

2026-04-27 기준 Ollama Gemma 4 태그 페이지에는 29개 태그가 표시됩니다.

사전 준비에서는 목적이 명확한 로컬 기본 태그를 사용하세요.

- 8GB: `gemma4:e2b`
- 16GB: `gemma4:e4b`, 버거우면 `gemma4:e2b`
- 32GB 이상: `gemma4:26b`
- 36GB 이상: `gemma4:26b` 또는 `gemma4:31b`

주의:

- `gemma4:latest`는 현재 E4B 계열로 표시되지만, 나중에 바뀔 수 있습니다.
- `*-cloud` 태그는 로컬에 모델을 받아 두는 경로가 아니므로, 사전 준비 기본값으로 쓰지 마세요.
- `*-mlx-*`, `*-mxfp8`, `*-nvfp4`, `*-q8_0` 같은 변형 태그는 정밀도와 실행 목적을 알고 선택할 때만 사용하세요.

## macOS

이런 환경에 맞습니다:

- macOS 14 Sonoma 이상
- Apple Silicon 권장
- Intel Mac도 가능하지만 CPU 전용

설치 순서:

1. 공식 다운로드 페이지로 이동합니다.  
   [Ollama macOS 다운로드](https://ollama.com/download)
2. `ollama.dmg`를 열고 Ollama 앱을 `Applications` 폴더로 옮깁니다.
3. 앱을 처음 실행합니다.
4. 터미널에서 설치 확인:

```bash
ollama --version
```

5. 메모리에 맞는 모델을 미리 받습니다.

```bash
ollama pull gemma4:e2b
```

또는

```bash
ollama pull gemma4:e4b
```

6. 실행 테스트:

```bash
ollama run gemma4:e2b
```

권장 메모:

- 첫 실행 시 CLI 경로 연결을 요청하면 허용하세요.
- Apple Silicon에서는 CPU/GPU를 함께 활용하기 쉽고, 행사 진행에도 유리합니다.

## Linux (Ubuntu 등)

이런 환경에 맞습니다:

- 일반 Linux 노트북 또는 데스크톱
- NVIDIA/AMD GPU가 있으면 더 유리
- ARM64 장치도 가능하지만 행사 안정성 기준으로는 x64가 더 무난

설치 순서:

1. 터미널을 엽니다.
2. Ollama를 설치합니다.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

3. 설치 확인:

```bash
ollama -v
```

4. 모델 다운로드:

```bash
ollama pull gemma4:e2b
```

또는

```bash
ollama pull gemma4:e4b
```

5. 실행 테스트:

```bash
ollama run gemma4:e2b
```

추가 메모:

- AMD GPU가 있으면 ROCm 패키지를 별도로 설치할 수 있습니다.
- ARM64 장치에서는 ARM64용 패키지를 써야 합니다.
- 서버처럼 계속 띄워둘 경우 `ollama serve`와 systemd 서비스 설정도 가능합니다.

## ChromeOS

ChromeOS는 Ollama만 권장합니다. 다만 이 경로는 안정성이 낮을 수 있으며, Windows/macOS보다 느릴 수 있습니다.

중요 제한:

- Chromebook에서 Linux 개발 환경이 켜져 있어야 합니다.
- 회사/학교 지급 기기에서는 Linux 사용이 막혀 있을 수 있습니다.
- ChromeOS Linux 환경에서는 Ollama/Gemma 4 같은 로컬 LLM 실행에서 전용 GPU/VRAM 기반 compute 가속을 기대하기 어렵습니다.
- 따라서 ChromeOS에서는 E2B 위주로 준비하는 것을 권장합니다.

설치 순서:

1. ChromeOS에서 Linux 개발 환경을 켭니다.  
   경로: `설정 > About ChromeOS > Developers > Linux development environment > Set up`
2. Linux 터미널이 열리면 패키지를 업데이트합니다.

```bash
sudo apt-get update && sudo apt-get dist-upgrade
```

3. Ollama를 설치합니다.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

4. 설치 확인:

```bash
ollama -v
```

5. 모델 다운로드:

```bash
ollama pull gemma4:e2b
```

6. 실행 테스트:

```bash
ollama run gemma4:e2b
```

ChromeOS 권장 메모:

- 8GB Chromebook: 가능하면 다른 기기를 권장, 꼭 써야 한다면 `E2B`만 시도
- 16GB 이상 Chromebook: `E2B` 권장, `E4B`는 속도가 매우 느릴 수 있음

# LM Studio 설치 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 먼저 알아둘 점

- 이번 세션은 개발자, 비개발자 모두 참여 가능한 세션이므로, 하나만 설치한다면 LM Studio를 기본 권장합니다.
- LM Studio는 macOS Apple Silicon, Windows, Linux를 지원합니다.
- macOS는 Apple Silicon만 지원하며, Intel Mac은 지원 대상이 아닙니다.
- macOS 앱은 공식 문서 기준 macOS 14.0 이상을 권장 기준으로 봅니다.
- Windows는 x64와 ARM을 지원합니다.
- Linux는 Ubuntu 20.04+ AppImage가 공식 기준입니다.
- 모델 다운로드 후에는 완전 오프라인 사용이 가능합니다.
- Apple Silicon Mac에서는 GGUF를 기본으로 사용해도 되고, 필요하면 MLX 모델도 선택할 수 있습니다.
- 이번 핸즈온은 채팅/실습/에이전트 흐름이 중심이므로 **instruction-tuned(chat-ready) 모델**을 선택하세요.
- `base`나 `pretrained`로 표시된 모델은 기본 준비용으로 받지 않는 편이 안전합니다.
- LM Studio에서는 모델 이름이 `...-it` 로 그대로 보일 수도 있고, `google/gemma-4-e4b`처럼 더 짧게 보일 수도 있으므로 **설명이나 모델 카드에서 chat-ready / instruct 계열인지** 함께 확인해 주세요.

## Intel Mac은 이 문서를 따라가지 마세요

Intel Mac에서는 LM Studio 데스크톱 앱을 행사 준비 경로로 쓰지 않습니다.

- 공식 LM Studio 시스템 요구사항은 Mac에서 Apple Silicon을 요구합니다.
- Intel Mac 사용자는 [Intel Mac 사용자 사전 준비 가이드](./18-intel-mac-prep.md)를 먼저 보세요.
- 기본 준비는 [Ollama 설치 가이드](./06-ollama-setup.md)의 macOS 섹션을 따라 `gemma4:e2b`를 받는 방식입니다.

## Windows

이런 환경에 맞습니다:

- Windows x64 또는 ARM
- RAM 16GB 이상 권장

설치 순서:

1. 공식 다운로드 페이지로 이동합니다.  
   [LM Studio 다운로드](https://lmstudio.ai/download)
2. Windows용 설치 파일을 받아 실행합니다.
3. 앱을 한 번 실행합니다.
4. 필요 시 런타임을 설치하거나 업데이트합니다.  
   단축키: `Ctrl + Shift + R`
5. `Discover` 탭에서 `gemma 4`를 검색합니다.
6. 아래 중 하나를 다운로드합니다.
   - `google/gemma-4-e2b` 계열의 chat-ready / instruction-tuned 항목
   - `google/gemma-4-e4b` 계열의 chat-ready / instruction-tuned 항목
7. `Chat` 탭으로 이동해 모델을 메모리에 로드합니다.
8. 테스트 프롬프트를 입력합니다.

예시 프롬프트:

```text
안녕하세요. Build with AI Seoul 2026 핸즈온 테스트입니다. 한 줄로 자기소개해 주세요.
```

선택 사항:

- 터미널에서 `lms --help`를 실행해 CLI까지 확인할 수 있습니다.
- 단, `lms`는 LM Studio를 최소 1회 실행한 뒤 사용하는 것이 안전합니다.
- Windows에서는 **PowerShell 기준**으로 아래처럼 확인하면 됩니다.

```powershell
lms --help
```

## macOS

이런 환경에 맞습니다:

- Apple Silicon (M1/M2/M3/M4)
- macOS 14.0 이상

설치 순서:

1. 공식 다운로드 페이지로 이동합니다.  
   [LM Studio 다운로드](https://lmstudio.ai/download)
2. macOS용 앱을 설치합니다.
3. 앱을 실행합니다.
4. 필요 시 런타임을 설치하거나 업데이트합니다.  
   단축키: `Cmd + Shift + R`
5. `Discover` 탭에서 `gemma 4`를 검색합니다.
6. 아래 중 하나를 다운로드합니다.
   - `google/gemma-4-e2b` 계열의 chat-ready / instruction-tuned 항목
   - `google/gemma-4-e4b` 계열의 chat-ready / instruction-tuned 항목
7. `Chat` 탭에서 모델을 로드하고 테스트합니다.

권장 메모:

- LM Studio 공식 문서는 macOS에서 16GB+ RAM 권장입니다.
- LM Studio 앱은 Apple Silicon Mac 기준으로 준비하세요. Intel Mac은 지원 대상이 아닙니다.
- 행사 준비 기준으로는 최신 macOS를 권장합니다.
- 8GB Mac도 가능할 수 있지만, 작은 모델과 작은 컨텍스트만 권장합니다.
- Apple Silicon에서도 GGUF 기반 fine-tuned 모델을 사용하는 것은 대체로 가능하지만, 양자화 방식, 채팅 템플릿, 멀티모달 지원 여부에 따라 모델별 확인이 필요합니다.
- MLX는 선택 사항이며, 행사 준비 기준으로는 GGUF만 사용해도 충분합니다.
- `GGUF`, `MLX`, `llama.cpp` 개념이 헷갈리면 [GGUF, MLX, llama.cpp 개념 설명](./04-gguf-mlx-llamacpp-explainer.md) 문서를 먼저 확인해 주세요.
- Apple Silicon 사용자는 필요하면 [Apple Silicon + MLX 안내](./08-apple-silicon-mlx.md)도 함께 확인해 주세요.
- LM Studio를 `opencode` 같은 코딩 에이전트 도구와 연결해 보고 싶다면 [OpenCode 설치 및 LM Studio 연동 가이드](./10-opencode-lmstudio-developer-agent.md)도 함께 확인해 주세요.
- Windows 사용자는 LM Studio CLI 예시를 볼 때 `bash` 대신 **PowerShell**로 따라오시면 됩니다.

## Linux (Ubuntu)

이런 환경에 맞습니다:

- Ubuntu 20.04 이상
- x64 또는 ARM64

설치 순서:

1. 공식 다운로드 페이지로 이동합니다.  
   [LM Studio 다운로드](https://lmstudio.ai/download)
2. Linux용 AppImage를 다운로드합니다.
3. 터미널에서 실행 권한을 부여합니다.

```bash
chmod +x LM-Studio-*.AppImage
```

4. AppImage를 실행합니다.

```bash
./LM-Studio-*.AppImage
```

5. 앱이 실행되면 `Discover` 탭에서 `gemma 4`를 검색합니다.
6. `google/gemma-4-e2b` 또는 `google/gemma-4-e4b` 계열의 **chat-ready / instruction-tuned 항목**을 다운로드합니다.
7. `Chat` 탭에서 모델을 로드하고 테스트합니다.

참고:

- 공식 문서는 Linux 배포 형식을 AppImage로 안내합니다.
- 위 AppImage 실행 절차는 그 배포 형식에 맞춘 일반적인 설치 흐름입니다.
- Ubuntu 22.04보다 최신 버전은 공식 문서상 충분히 테스트되지 않았다고 안내되어 있습니다.

## ChromeOS

ChromeOS에서는 LM Studio를 권장하지 않습니다.

이유:

- LM Studio Linux 공식 지원 기준은 Ubuntu 20.04+ AppImage입니다.
- ChromeOS Linux 개발 환경은 Debian 기반입니다.
- ChromeOS Linux 환경에서는 로컬 LLM 실행에 필요한 전용 GPU/VRAM 기반 compute 가속을 기대하기 어렵습니다.

즉, ChromeOS에서 LM Studio는 공식 권장 경로 밖이며, 행사 당일 설치 이슈가 생길 가능성이 있습니다.

ChromeOS를 쓰는 경우:

1. Ollama로 준비
2. 가능하면 Windows 또는 macOS 노트북 추가 준비

# 2026 Build with AI Seoul - Gemma 4 Hands-On Prep

Build with AI Seoul 2026 세션 **"Build Your Own AI Office with Gemma 4"**를 위한 사전 준비 문서 저장소입니다.

- 세션명: `Build Your Own AI Office with Gemma 4`
- 진행자: `박제창`
- 트랙: `Hands-On A`
- 진행 시간: `13:30 ~ 14:30 (60분)`
- 기준 확인일: `2026-04-27`

이 저장소는 행사 참가자가 자신의 운영체제와 장비 사양에 맞춰 **로컬 Gemma 4 실행 환경을 미리 준비**할 수 있도록 문서를 정리한 허브입니다. 기본 경로는 `LM Studio` 중심이며, 필요에 따라 `Ollama`, `llama.cpp`, `OpenCode`, `Hermes Agent`, `MLX`까지 다룹니다.

## 빠른 시작

가장 먼저 아래 허브 문서를 여세요.

- [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)

상황별 추천 읽기 순서는 다음과 같습니다.

| 대상 | 먼저 볼 문서 |
| --- | --- |
| 대부분의 참가자 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [05](./docs/05-lm-studio-setup.md) -> [15](./docs/15-troubleshooting-and-final-check.md) |
| Windows 참가자 | [02](./docs/02-windows-guide.md) -> [01](./docs/01-hardware-and-model-selection.md) -> [05](./docs/05-lm-studio-setup.md) -> [15](./docs/15-troubleshooting-and-final-check.md) |
| ChromeOS 참가자 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [06](./docs/06-ollama-setup.md) -> [15](./docs/15-troubleshooting-and-final-check.md) |
| Apple Silicon Mac 사용자 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [04](./docs/04-gguf-mlx-llamacpp-explainer.md) -> [05](./docs/05-lm-studio-setup.md) -> [08](./docs/08-apple-silicon-mlx.md) |
| 코딩 에이전트까지 써볼 참가자 | [09](./docs/09-gemma4-benchmarks-and-agent-expectations.md) -> [10](./docs/10-opencode-lmstudio-developer-agent.md) -> [11](./docs/11-pi-and-tool-selection-notes.md) -> [12](./docs/12-hermes-agent-overview.md) -> [13](./docs/13-hermes-agent-setup.md) |

## 핵심 권장안

- 행사 당일에 처음 모델을 다운로드하지 않는 것을 강하게 권장합니다.
- 가능하면 `16GB 이상` 메모리 장비를 준비하세요.
- 하나만 설치한다면 기본 권장 도구는 `LM Studio`입니다.
- `8GB` 장비는 `E2B`만 준비하고, 실행 속도가 매우 느릴 수 있음을 감안해 주세요.
- `Hermes Agent`와 `llama.cpp`는 선택형 고급 경로입니다.

메모리 기준의 빠른 추천:

| 메모리 | 권장 모델 |
| --- | --- |
| 8GB | `E2B` |
| 16GB | `E4B` |
| 32GB | `E4B` 또는 `26B A4B` |
| 36GB | `26B A4B` 또는 `31B` |

`26B A4B`는 26B 규모 모델이지만, 답을 만들 때는 내부의 여러 "전문가" 부분 중 필요한 일부만 사용합니다. 이 방식을 `MoE`라고 부르며, `A4B`는 그때 실제로 계산되는 부분이 약 4B 규모라는 뜻입니다. 단, 전체 모델 파일은 메모리에 올라가므로 4B 모델처럼 가볍지는 않습니다.

## 문서 구성

### 허브 문서

- [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md): 전체 안내 허브 문서

### 세부 문서

1. [하드웨어 / 운영체제 / 모델 선택 가이드](./docs/01-hardware-and-model-selection.md)
2. [Windows 참가자 빠른 준비 가이드](./docs/02-windows-guide.md)
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
15. [트러블슈팅 / 최종 체크 / 참고 링크](./docs/15-troubleshooting-and-final-check.md)

## 저장소 구조

```text
.
├── gemma4-local-setup-guide.md
├── docs/
├── scripts/
│   └── generate_hands_on_prep_pdf.py
├── output/
│   └── pdf/
│       └── gemma4-hands-on-prep-guide.pdf
└── tmp/
    └── pdfs/
```

- `docs/`: 세션 준비용 원본 마크다운 문서
- `gemma4-local-setup-guide.md`: 참가자에게 먼저 보여줄 허브 문서
- `scripts/generate_hands_on_prep_pdf.py`: `docs/01-15`를 하나의 PDF로 묶는 스크립트
- `output/pdf/`: 생성된 PDF 산출물
- `tmp/pdfs/`: PDF 미리보기 contact sheet 이미지

## PDF 생성

저장소에는 이미 생성된 PDF가 포함되어 있습니다.

- [output/pdf/gemma4-hands-on-prep-guide.pdf](./output/pdf/gemma4-hands-on-prep-guide.pdf)

문서를 수정한 뒤 PDF를 다시 만들려면 아래처럼 실행하면 됩니다.

```bash
python3 -m pip install reportlab pymupdf pillow
python3 scripts/generate_hands_on_prep_pdf.py
```

출력 결과:

- PDF: `output/pdf/gemma4-hands-on-prep-guide.pdf`
- 미리보기 이미지: `tmp/pdfs/gemma4-hands-on-prep-contact-*.png`

참고:

- `reportlab`은 PDF 생성에 필요합니다.
- `pymupdf`, `pillow`는 페이지 수 계산 및 contact sheet 생성에 사용됩니다.
- macOS에서는 로컬 `Pretendard` 폰트가 있으면 우선 사용하고, 없으면 기본 대체 폰트로 동작합니다.

## 준비 기준

- 모델과 도구는 **행사 당일 안정적으로 실행할 수 있는 조합**을 우선합니다.
- 운영체제별 차이와 Windows의 `PowerShell` / `WSL2` 구분을 확인해 주세요.
- `OpenCode`, `Hermes Agent`, `llama.cpp`는 기본 경로가 아니라 선택형 고급 경로입니다.

## 라이선스

[MIT License](./LICENSE)

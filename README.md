# 2026 Build with AI Seoul

Build with AI Seoul 2026 세션 **Build Your Own AI Office with Gemma 4**를 위한 사전 준비 문서와 핸즈온 실습 코드 저장소입니다.

- 세션명: `Build Your Own AI Office with Gemma 4`
- 진행자: `박제창`
- 트랙: `Hands-On A`
- 진행 시간: `13:30 ~ 14:30 (60분)`
- 기준 확인일: `2026-05-01`

이 저장소에는 행사 전에 자신의 운영체제와 장비 사양에 맞춰 **로컬 Gemma 4 실행 환경을 미리 준비**할 수 있도록 필요한 문서와, 당일 실습에서 사용할 `workshop/` 코드가 들어 있습니다. 처음 준비한다면 `LM Studio`를 기준으로 따라오면 되고, 핸즈온 실습은 [workshop/03_labs/README.md](./workshop/03_labs/README.md)를 보면서 [workshop/01_starter](./workshop/01_starter)에서 진행하면 됩니다.

## 빠른 시작

행사 전 준비는 아래 문서부터 보세요.

- [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)

행사 당일 핸즈온은 아래 순서로 보면 됩니다.

1. [workshop/03_labs/README.md](./workshop/03_labs/README.md)를 엽니다.
2. [workshop/01_starter](./workshop/01_starter) 폴더에서 실습합니다.
3. 막히면 [workshop/02_final](./workshop/02_final)을 정답 코드로 참고합니다.

본인 상황에 맞게 아래 순서로 보면 됩니다.

| 내 상황 | 먼저 볼 문서 |
| --- | --- |
| 처음 준비하는 경우 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [05](./docs/05-lm-studio-setup.md) -> [16](./docs/16-troubleshooting-and-final-check.md) |
| Windows를 쓰는 경우 | [02](./docs/02-windows-guide.md) -> [01](./docs/01-hardware-and-model-selection.md) -> [05](./docs/05-lm-studio-setup.md) -> [16](./docs/16-troubleshooting-and-final-check.md) |
| ChromeOS를 쓰는 경우 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [06](./docs/06-ollama-setup.md) -> [16](./docs/16-troubleshooting-and-final-check.md) |
| Apple Silicon Mac을 쓰는 경우 | [01](./docs/01-hardware-and-model-selection.md) -> [03](./docs/03-memory-based-model-selection.md) -> [04](./docs/04-gguf-mlx-llamacpp-explainer.md) -> [05](./docs/05-lm-studio-setup.md) -> [08](./docs/08-apple-silicon-mlx.md) |
| 코딩 에이전트까지 해 보고 싶은 경우 | [09](./docs/09-gemma4-benchmarks-and-agent-expectations.md) -> [10](./docs/10-opencode-lmstudio-developer-agent.md) -> [11](./docs/11-pi-and-tool-selection-notes.md) -> [12](./docs/12-hermes-agent-overview.md) -> [13](./docs/13-hermes-agent-setup.md) -> [18](./docs/18-uv-setup.md) (필요 시) |
| Gemini CLI에서 Gemma 4 preview / Gemma 라우팅을 확인해 보고 싶은 경우 | [15](./docs/15-gemini-cli-gemma-routing-prep.md) |
| 자주 묻는 질문을 먼저 보고 싶은 경우 | [17](./docs/17-faq.md) |
| `uv` 또는 `uvx`를 미리 설치하고 싶은 경우 | [18](./docs/18-uv-setup.md) |

## 먼저 기억할 것

- 행사 당일에 처음 모델을 받기 시작하면 시간이 부족할 수 있습니다. 미리 받아 주세요.
- 가능하면 `16GB 이상` 메모리 장비를 준비하세요.
- 하나만 설치한다면 `LM Studio`를 설치하세요.
- `8GB` 장비는 `E2B`만 준비하세요. 실행 속도는 많이 느릴 수 있습니다.
- 모델은 **instruction-tuned / chat-ready** 계열을 받으세요. `base`나 `pretrained`로 표시된 모델은 이번 기본 준비용으로 권장하지 않습니다.
- `Hermes Agent`와 `llama.cpp`는 필수가 아닙니다. 터미널 사용에 익숙한 분만 추가로 준비하세요.
- `uv`는 로컬 LLM 실행 도구가 아니라 Python 기반 도구와 실행 환경을 관리하는 보조 도구입니다. `Hermes Agent` 설치 중 문제가 날 때만 별도로 확인해도 됩니다.
- `Gemini CLI Gemma`도 필수 준비 항목은 아닙니다. preview에서는 Gemma 4 모델을 선택할 수 있지만, `gemini gemma setup`은 Gemma 3 기반 로컬 라우팅 설정으로 봐야 합니다.

메모리별 모델 추천:

| 메모리 | 권장 모델 |
| --- | --- |
| 8GB | `E2B` |
| 16GB | `E4B` |
| 32GB | `E4B` 또는 `26B A4B` |
| 36GB | `26B A4B` 또는 `31B` |

모델 이름의 `B`는 `Billion`, 즉 **10억 개**를 뜻합니다.  
`26B`는 대략 260억 개 파라미터를 가진 모델이라는 뜻이고, `31B`는 대략 310억 개 파라미터를 가진 모델이라는 뜻입니다. 여기서 파라미터는 모델이 학습하면서 갖게 된 숫자 값이라고 보면 됩니다.

중요한 점은 `B`가 `GB`가 아니라는 것입니다.  
`26B`는 "파일 크기가 26GB"라는 뜻이 아니라 "모델 안에 학습된 숫자가 약 260억 개"라는 뜻입니다. 실제 다운로드 크기와 메모리 사용량은 양자화 방식, 실행 도구, 컨텍스트 길이에 따라 달라집니다.

일반 사용자가 LM Studio나 Ollama에서 받는 로컬 실행용 모델은 보통 원본 BF16 가중치 그대로가 아니라 **4-bit, 5-bit, 8-bit 등으로 양자화된 배포본**입니다. 그래서 `26B`, `31B`라는 이름과 다운로드 크기가 1:1로 대응하지 않습니다.

이번 핸즈온은 채팅, 질의응답, 로컬 에이전트 흐름이 중심입니다.  
따라서 모델을 직접 고를 때는 `-it`, `instruct`, `instruction-tuned`, `chat-ready` 같은 설명이 붙은 항목을 우선하세요. `base`나 `pretrained`로 표시된 모델은 기본 준비용으로 받지 않는 편이 안전합니다.

`26B A4B`는 26B 규모 모델이지만, 답을 만들 때는 내부의 여러 "전문가" 부분 중 필요한 일부만 사용합니다. 이 방식을 `MoE`라고 부르며, `A4B`는 그때 실제로 계산되는 부분이 약 4B 규모라는 뜻입니다. 단, 전체 모델 파일은 메모리에 올라가므로 4B 모델처럼 가볍지는 않습니다.

## 문서 구성

### 핸즈온 실습 코드

- [workshop/README.md](./workshop/README.md): 워크샵 코드 폴더 안내
- [workshop/03_labs/README.md](./workshop/03_labs/README.md): 단계별 핸즈온 문서
- [workshop/01_starter](./workshop/01_starter): 직접 수정하며 시작하는 코드
- [workshop/02_final](./workshop/02_final): 전체 시나리오가 포함된 최종 완성 코드

### 전체 안내 문서

- [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md): 가장 먼저 볼 전체 안내 문서

### 세부 문서

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

## 저장소 구조

```text
.
├── gemma4-local-setup-guide.md
├── docs/
├── workshop/
│   ├── 01_starter/
│   ├── 02_final/
│   └── 03_labs/
├── scripts/
│   └── generate_hands_on_prep_pdf.py
├── output/
│   └── pdf/
│       └── gemma4-hands-on-prep-guide.pdf
└── tmp/
    └── pdfs/
```

- `docs/`: 세션 준비용 원본 마크다운 문서
- `workshop/`: 당일 핸즈온 실습 코드와 단계별 문서
- `workshop/01_starter/`: 시작 코드
- `workshop/02_final/`: 최종 완성 코드
- `workshop/03_labs/`: 단계별 실습 문서
- `gemma4-local-setup-guide.md`: 가장 먼저 볼 전체 안내 문서
- `scripts/generate_hands_on_prep_pdf.py`: `docs/01-18`을 하나의 PDF로 묶는 스크립트
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
- `OpenCode`, `Hermes Agent`, `llama.cpp`는 필수가 아니며, 익숙한 분만 추가로 준비하면 됩니다.

## 라이선스

[MIT License](./LICENSE)

# Gemma 4 아키텍처 상세 정리

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- Gemma 4의 구조를 조금 더 깊게 이해하고 싶은 분
- `E2B`, `E4B`, `26B A4B`, `31B`가 왜 다른지 알고 싶은 분
- 설치 가이드보다 모델 자체의 설계 차이가 궁금한 분

## 먼저 알아둘 점

- **정확한 모델별 수치**는 Google 공식 모델 카드 기준으로 정리했습니다.
- Hugging Face의 [Gemma 4 blog](https://huggingface.co/blog/gemma4) 와 Maarten Grootendorst의 [A Visual Guide to Gemma 4](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4) 는 이해를 돕는 **설명 자료**로 함께 참고했습니다.
- 따라서 아래 문서에서는:
  - `모델 크기, 레이어 수, 컨텍스트, modality` 같은 항목은 **공식 모델 카드 기준**
  - `왜 이런 구조가 나왔는지`에 대한 해설은 **블로그/설명 자료를 참고한 해석**
  
  으로 이해하면 됩니다.

## 먼저 용어부터 보기

모델 구조 용어는 세부 구현보다 아래 정도만 이해하면 충분합니다.

- `Dense`: 모델의 주요 계산 블록을 대부분 함께 쓰는 일반적인 구조입니다. 구조가 단순하지만, 큰 모델일수록 계산과 메모리 부담이 커집니다.
- `MoE`: "여러 전문가 중 필요한 일부만 골라 쓰는 구조"입니다. 모델 안에 여러 전문가 블록(expert)이 있고, 답을 만들 때마다 그중 일부만 계산합니다.
- `active parameters`: 답을 만들 때 그 순간 실제 계산에 참여하는 파라미터입니다.
- `effective parameters`: 작은 모델의 체감 계산 규모를 설명하기 위한 표기입니다.
- `PLE`: E2B/E4B가 작은 모델 효율을 높이기 위해 쓰는 보조 장치입니다. 세부 구조보다 "작은 모델을 더 효율적으로 쓰기 위한 장치"로 이해하면 됩니다.

## 한눈에 보는 구조 차이

| 모델 | 구조 | 핵심 포인트 |
| --- | --- | --- |
| `E2B` | Dense + PLE | 작은 온디바이스용, audio 지원, 128K context |
| `E4B` | Dense + PLE | 작은 온디바이스용, audio 지원, 128K context |
| `26B A4B` | MoE | 총 26B지만 답을 만들 때는 약 4B 규모만 계산, 속도/성능 균형형 |
| `31B` | Dense | 가장 단순하고 강한 상위 모델, 품질 우선 |

핵심:

- 작은 모델(`E2B`, `E4B`)은 **PLE** 로 효율을 높인 구조입니다.
- `26B A4B`는 여러 전문가 중 일부만 골라 쓰는 **MoE** 구조입니다.
- `31B`는 모든 주요 계산 블록을 함께 쓰는 상위 모델입니다.

## Gemma 4 전체가 공통으로 갖는 구조

공식 모델 카드와 Hugging Face 기술 블로그 기준으로, Gemma 4 전반에는 아래 같은 공통 특성이 있습니다.

### 1. Hybrid Attention

Gemma 4는 **local sliding-window attention** 과 **global full attention** 을 섞어 씁니다.

- local layer는 계산량과 메모리를 줄이는 역할
- global layer는 긴 문맥과 전체 구조를 다시 보는 역할
- 마지막 레이어는 global attention 이 되도록 설계되었습니다

이 구조 덕분에:

- 긴 컨텍스트를 지원하면서도
- 무조건 모든 레이어가 full attention 인 모델보다
- 더 효율적으로 동작합니다.

### 2. Long Context용 RoPE 설계

RoPE는 문장 안에서 각 토큰이 어느 위치에 있는지 모델이 이해하도록 돕는 방식입니다.

Hugging Face 설명 자료 기준으로 Gemma 4는:

- sliding layer에는 표준 RoPE
- global layer에는 긴 문맥에 맞춘 **Proportional / low-frequency-pruned RoPE**

를 사용합니다.

실습에서는:

- “128K / 256K 문맥을 그냥 억지로 늘린 게 아니라”
- 긴 문맥을 버티기 위한 attention + positional encoding 조합이 들어갔다

정도로 이해하면 충분합니다.

### 3. Shared KV Cache

KV cache는 모델이 이미 읽은 문맥을 다시 계산하지 않도록 저장해 두는 내부 메모리입니다.

Hugging Face blog 기준으로 Gemma 4는 **shared KV cache** 를 사용합니다.

- 마지막 일부 레이어가 자기만의 key/value projection을 다시 만들지 않고
- 앞쪽 레이어의 KV 상태를 재사용합니다

의미:

- 긴 문맥에서 메모리와 계산량 절감
- 온디바이스/로컬 추론에 유리

### 4. Vision Encoder

Gemma 4는 전 모델이 image 입력을 지원합니다.

핵심 특징:

- **가변 aspect ratio**
- **가변 resolution**
- **고정된 soft token budget** 으로 이미지 정보를 요약

Hugging Face blog 기준 대표 token budget:

- `70`
- `140`
- `280`
- `560`
- `1120`

즉, 같은 이미지 모델이라도:

- 더 적은 시각 토큰으로 빠르게 볼 수도 있고
- 더 많은 시각 토큰으로 자세히 볼 수도 있습니다.

### 5. Audio Encoder

audio 는 **E2B / E4B** 에만 있습니다.

Hugging Face blog 기준:

- USM-style conformer 기반 audio encoder
- Gemma-3n 계열과 유사한 audio 처리 경로

즉:

- 작은 모델은 text + image + audio
- 큰 모델은 text + image

로 이해하면 됩니다.

## 모델별 공식 구조 요약

Google 공식 Gemma 4 모델 카드 기준:

### Dense 모델

Dense 모델은 답을 만들 때 모델의 주요 계산 블록을 대부분 함께 쓰는 구조입니다.

| 항목 | `E2B` | `E4B` | `31B` |
| --- | --- | --- | --- |
| 총 파라미터 | 2.3B effective (5.1B with embeddings) | 4.5B effective (8B with embeddings) | 30.7B |
| 레이어 수 | 35 | 42 | 60 |
| sliding window | 512 | 512 | 1024 |
| 컨텍스트 | 128K | 128K | 256K |
| vocab | 262K | 262K | 262K |
| modality | Text, Image, Audio | Text, Image, Audio | Text, Image |
| vision encoder | ~150M | ~150M | ~550M |
| audio encoder | ~300M | ~300M | 없음 |

### MoE 모델

| 항목 | `26B A4B` |
| --- | --- |
| 총 파라미터 | 25.2B |
| 실제 계산 참여 파라미터 | 3.8B |
| 레이어 수 | 30 |
| sliding window | 1024 |
| 컨텍스트 | 256K |
| vocab | 262K |
| 전문가 블록 구성 | 128개 중 8개 선택 + 공통 전문가 블록 1개 |
| modality | Text, Image |
| vision encoder | ~550M |

## `A4B`는 무슨 뜻인가요?

`26B A4B`는 **전체 규모는 26B급이지만, 답을 만들 때 실제로 계산에 참여하는 부분은 약 4B 규모인 모델**이라는 뜻입니다.

- `26B`: 모델 전체가 가진 총 파라미터 규모입니다. 공식 카드 기준 실제 수치는 `25.2B`입니다.
- `A`: active, 즉 실제 계산에 참여한다는 뜻입니다.
- `4B`: 답을 만들 때 계산에 참여하는 파라미터 규모입니다. 공식 카드 기준 실제 수치는 `3.8B`입니다.

이 차이는 `26B A4B`가 **MoE(Mixture-of-Experts)** 구조이기 때문에 생깁니다. 모델 안에는 여러 전문가 블록이 있고, 답을 만들 때마다 그중 일부만 골라 계산합니다. 공식 카드 기준으로는 전체 `128개` 전문가 블록 중 `8개`와 `1개` 공통 전문가 블록을 사용합니다.

실습에서 가장 중요한 해석은 아래입니다.

- 속도: 답을 만들 때 약 4B 규모만 계산하므로 31B보다 빠르게 느껴질 수 있습니다.
- 품질: 전체 모델 규모는 26B급이라 E2B/E4B보다 더 좋은 코딩과 에이전트 체감을 기대할 수 있습니다.
- 메모리: 전체 26B 규모의 가중치를 메모리에 올려야 하므로, 4B 모델처럼 가볍게 실행되는 것은 아닙니다.

## E2B / E4B는 왜 “effective” 인가요?

공식 모델 카드와 Hugging Face blog 기준으로, 작은 모델에는 **Per-Layer Embeddings (PLE)** 가 들어갑니다.

이 구조 때문에:

- 총 embedding 테이블 크기는 꽤 크지만
- 실제 추론에서 답을 만들 때 무겁게 계산되는 파라미터는 더 적습니다

그래서 공식 카드도:

- `E2B = 2.3B effective (5.1B with embeddings)`
- `E4B = 4.5B effective (8B with embeddings)`

처럼 표기합니다.

직관적으로는:

- “모델 본체는 더 작게 유지하면서”
- “레이어별 추가 조건 신호를 embedding lookup 방식으로 넣어”
- 온디바이스 효율을 높인 구조

라고 이해하면 됩니다.

Hugging Face blog 해설 기준으로 PLE는:

- 각 token에 대해 레이어마다 작은 보조 벡터를 공급하고
- 각 레이어가 자기 시점에 필요한 token-specific 정보를 더 잘 받게 해줍니다

즉, 작은 모델에서 **깊이를 무작정 늘리지 않고 효율을 높이는 장치**라고 볼 수 있습니다.

## 26B A4B는 왜 빠를 수 있나요?

`26B A4B`는 위에서 설명한 MoE 구조를 사용합니다.

의미:

- 모델 전체는 26B급으로 크지만
- 매 토큰마다 전체를 다 활성화하지 않고
- 일부 전문가 블록만 선택적으로 계산합니다

그래서:

- 31B보다 더 가볍게 느껴질 수 있고
- 로컬 환경에서는 속도/품질 균형이 좋을 수 있습니다

다만 중요한 점:

- 메모리에는 전체 파라미터가 올라가야 하므로
- “4B 모델처럼 가볍게 메모리만 쓰는 것”은 아닙니다

즉:

- **속도 관점에서는 4B active의 장점**
- **메모리 관점에서는 26B total의 부담**

을 동시에 갖습니다.

## 31B는 왜 따로 의미가 있나요?

31B는 Gemma 4 계열의 상위 모델입니다.

장점:

- 구조가 비교적 단순하고 해석이 쉬움
- 최고 수준의 일반 성능
- coding / reasoning / long-context 품질이 가장 좋음

공식 카드와 Hugging Face 설명을 같이 보면:

- 31B는 “특별한 트릭”보다
- Gemma 4 공통 구조를 더 큰 규모로 밀어붙인 상위 모델

로 이해하면 됩니다.

이번 핸즈온에서는:

- 가능한 하드웨어가 있으면 가장 품질이 좋음
- 다만 일반 노트북에서는 부담이 큼

## Vision 쪽에서 Gemma 4가 중요한 이유

Gemma 4는 text-only 모델이 아니라 **multimodal 모델**입니다.

특히 image 쪽에서 중요한 점:

- 정사각형으로 무조건 찌그러뜨리지 않고
- 원본 aspect ratio를 더 잘 보존하려고 하고
- token budget을 선택해 속도/메모리/품질을 조절할 수 있습니다

그래서:

- OCR
- 문서 읽기
- UI 이해
- 화면 인식

같은 시나리오에서 활용도가 높습니다.

## 핸즈온 관점에서 이 구조 차이가 왜 중요할까요?

### E2B / E4B

- 로컬 노트북 친화적
- audio 지원
- 하지만 코딩 에이전트나 복잡한 계획에는 한계가 더 빨리 드러날 수 있음

### 26B A4B

- 로컬에서 코딩/에이전트 체감을 노리기 좋은 균형형
- 속도와 품질의 절충안으로 보기 좋음

### 31B

- 가장 좋은 품질
- 발표자 데모나 고사양 환경에 적합

## 한 줄 해석

- `E2B/E4B`: 작은 온디바이스 모델 + PLE
- `26B A4B`: 빠른 상위 MoE
- `31B`: 가장 강한 상위 모델

## 같이 보면 좋은 문서

- [하드웨어 / 운영체제 / 모델 선택 가이드](./01-hardware-and-model-selection.md)
- [메모리 기준으로 Gemma 4 모델 고르는 방법](./03-memory-based-model-selection.md)
- [Gemma 4 벤치마크와 코딩 에이전트 기대치](./09-gemma4-benchmarks-and-agent-expectations.md)

## 참고 링크

- [Google Gemma 4 E2B model card](https://huggingface.co/google/gemma-4-E2B)
- [Google Gemma 4 26B A4B model card](https://huggingface.co/google/gemma-4-26B-A4B)
- [Google Gemma 4 31B model card](https://huggingface.co/google/gemma-4-31B)
- [Gemma 4 documentation](https://ai.google.dev/gemma/docs)
- [Hugging Face blog: Gemma 4](https://huggingface.co/blog/gemma4)
- [A Visual Guide to Gemma 4](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4)

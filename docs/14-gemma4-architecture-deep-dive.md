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

모델 구조 용어는 아래 흐름으로 이해하면 됩니다.  
세부 구현 수식보다 "어떤 계산을 언제 아끼는가"에 초점을 두면 훨씬 읽기 쉽습니다.

- `Dense`: 모델의 주요 계산 블록을 대부분 함께 쓰는 일반적인 구조입니다. 구조가 단순하지만, 큰 모델일수록 계산과 메모리 부담이 커집니다.
- `MoE`: "여러 전문가 중 필요한 일부만 골라 쓰는 구조"입니다. 모델 안에 여러 전문가 블록(expert)이 있고, 답을 만들 때마다 그중 일부만 계산합니다.
- `B`: Billion의 줄임말입니다. `26B`는 대략 260억 개 파라미터를 뜻합니다. `B`는 파일 크기 단위인 `GB`가 아닙니다.
- `active parameters`: 답을 만들 때 그 순간 실제 계산에 참여하는 파라미터입니다.
- `effective parameters`: 작은 모델의 체감 계산 규모를 설명하기 위한 표기입니다.
- `RoPE`: token 위치 정보를 attention 계산 안에 넣는 방식입니다. 긴 문맥에서 "이 token이 앞쪽에 있었는지, 가까운지, 먼지"를 다루는 데 중요합니다.
- `PLE`: E2B/E4B가 작은 모델 효율을 높이기 위해 쓰는 보조 장치입니다. 세부 구조보다 "작은 모델을 더 효율적으로 쓰기 위한 장치"로 이해하면 됩니다.

## 모델 이름의 `B`는 무엇인가요?

`B`는 `Billion`의 줄임말입니다.  
한국어로는 10억입니다.

- `E2B`: 약 20억 개 규모
- `E4B`: 약 40억 개 규모
- `26B`: 약 260억 개 규모
- `31B`: 약 310억 개 규모

여기서 말하는 것은 모델 파일 크기가 아니라 `파라미터 수`입니다.  
파라미터는 모델이 학습하면서 조정한 숫자 값입니다. 모델은 이 숫자들을 사용해서 "다음에 어떤 token이 올 가능성이 높은지"를 계산합니다.

쉽게 말하면:

- `B`는 모델 안에 들어 있는 학습된 숫자의 규모
- `GB`는 파일 크기나 메모리 용량
- `26B`는 26GB 파일이라는 뜻이 아님

보통 파라미터가 많을수록 더 복잡한 패턴을 담을 수 있습니다.  
그래서 큰 모델은 reasoning, coding, 긴 문맥 이해에서 더 좋은 결과를 낼 가능성이 큽니다.

하지만 그만큼:

- 모델 파일이 커지고
- 메모리를 더 많이 쓰고
- 한 token을 만들 때 계산도 더 무거워질 수 있습니다

그래서 로컬 실습에서는 "큰 모델이 무조건 좋다"보다 "내 노트북에서 안정적으로 돌아가는 모델"을 고르는 것이 더 중요합니다.

## Dense는 무엇인가요?

Transformer decoder block은 크게 보면 attention과 feed-forward network(FFN)로 이루어집니다.  
`Dense` 모델에서는 각 layer의 FFN이 하나의 큰 블록이고, 모든 token이 그 블록을 통과합니다.

쉽게 말하면:

- 모든 token이 같은 계산 경로를 지나갑니다.
- 구조가 단순하고 예측하기 쉽습니다.
- 모델이 커질수록 품질은 좋아질 수 있지만, 매번 계산해야 하는 양도 같이 커집니다.

Gemma 4에서는 `31B`가 대표적인 상위 dense 모델입니다.  
`E2B`, `E4B`도 dense 계열이지만, 작은 장비에서 더 잘 돌도록 `PLE` 같은 효율화 장치가 붙어 있습니다.

Dense 모델을 고를 때의 직관:

- **장점:** 구조가 단순하고 안정적입니다.
- **단점:** 큰 모델은 매 token마다 큰 FFN을 계속 계산해야 합니다.
- **실습 해석:** 31B는 품질이 좋지만, 일반 노트북에서는 메모리와 속도 부담이 큽니다.

## MoE는 무엇인가요?

`MoE`는 `Mixture of Experts`의 줄임말입니다.  
Dense 모델처럼 하나의 큰 FFN만 두는 대신, 여러 개의 작은 FFN expert를 두고 token마다 일부 expert만 골라 계산합니다.

중요한 점은 MoE가 모델 전체를 아무렇게나 켰다 껐다 하는 구조가 아니라는 것입니다.  
주로 FFN 부분을 여러 expert로 나누고, attention 등 나머지 구조는 계속 함께 동작합니다.

Gemma 4 `26B A4B`는 MoE 구조입니다.

- 전체 파라미터: 약 26B
- 실제 계산 참여 파라미터: 약 4B
- expert 수: 128개
- 한 번에 선택되는 expert: 8개
- 공통 expert: 항상 켜지는 shared expert 1개

그래서 `26B A4B`는 이름 그대로:

- 메모리에는 26B급 모델을 올려야 하지만
- 매 token 계산에서는 약 4B 규모만 활성화하는 구조

라고 보면 됩니다.

## MoE는 expert를 어떻게 고르나요?

MoE layer 안에는 `router`가 있습니다.  
router는 token embedding을 보고 어떤 expert를 쓸지 점수를 매깁니다.

개념적으로는 아래 순서입니다.

1. token embedding이 MoE layer에 들어옵니다.
2. router가 각 expert에 대한 점수 또는 확률을 계산합니다.
3. 점수가 높은 expert 일부를 고릅니다.
4. 선택된 expert들이 token을 처리합니다.
5. expert별 결과를 router 점수로 가중해서 합칩니다.
6. shared expert 결과도 함께 더해집니다.

이 선택은 **token 단위**로 일어납니다.  
같은 문장 안에서도 token마다 선택되는 expert가 달라질 수 있고, layer마다 선택도 달라질 수 있습니다.

몇 가지 오해를 피해야 합니다.

- 사람이 "이번에는 3번 expert를 써줘"처럼 직접 고르는 구조가 아닙니다.
- expert가 반드시 "코딩 담당", "한국어 담당"처럼 사람이 읽기 좋은 역할로 나뉜다고 보장되지는 않습니다.
- 라우터는 학습 과정에서 좋은 결과가 나오도록 expert 선택 방식을 같이 배웁니다.
- MoE라고 해서 메모리까지 4B 모델처럼 줄어드는 것은 아닙니다. 선택되지 않은 expert도 가중치로는 메모리에 올라가야 합니다.

실습에서 중요한 해석은 단순합니다.

- **속도:** 매번 전체 26B를 계산하지 않으므로 유리합니다.
- **품질:** 전체 모델 용량은 크기 때문에 작은 dense 모델보다 더 좋은 답을 기대할 수 있습니다.
- **메모리:** 전체 expert 가중치를 들고 있어야 하므로 26B급 부담이 남습니다.

## RoPE는 무엇인가요?

`RoPE`는 `Rotary Positional Embedding`의 줄임말입니다.  
Transformer는 token 순서를 그냥 문자열처럼 읽지 않습니다. attention 계산에서 "이 token이 몇 번째 위치에 있었는지"를 알 수 있어야 합니다.

RoPE는 위치 번호를 별도 값으로 붙이는 대신, query/key 벡터 일부를 위치에 따라 회전시키는 방식입니다.  
그래서 attention이 두 token의 내용뿐 아니라 위치 관계도 같이 보게 됩니다.

쉽게 말하면:

- 가까운 token끼리는 가까운 위치 관계로 보이고
- 멀리 떨어진 token은 다른 회전 패턴을 갖고
- 모델은 이 패턴을 통해 상대적인 거리와 순서를 파악합니다

긴 context 모델에서 RoPE가 중요한 이유는, 위치 정보가 흔들리면 긴 문서 뒤쪽의 token을 제대로 다루기 어렵기 때문입니다.  
128K, 256K context를 지원하려면 attention 구조뿐 아니라 position encoding도 긴 문맥에 맞게 설계되어야 합니다.

## Dual RoPE는 무엇인가요?

Hugging Face Gemma 4 블로그 기준으로 Gemma 4는 `Dual RoPE` 구성을 사용합니다.

- sliding-window layer: 표준 RoPE
- global full-context layer: pruned RoPE, 또는 low-frequency-pruned RoPE

이렇게 나누는 이유는 layer마다 하는 일이 다르기 때문입니다.

`sliding-window layer`는 가까운 주변 token을 자세히 봅니다.  
여기서는 표준 RoPE처럼 위치 차이를 비교적 촘촘하게 다루는 방식이 잘 맞습니다.

`global layer`는 긴 문맥 전체를 넓게 봅니다.  
긴 거리에서는 너무 빠르게 변하는 고주파 위치 성분이 오히려 불안정해질 수 있습니다. 그래서 global layer에서는 긴 context에 더 맞게 일부 위치 성분을 줄인 RoPE를 씁니다.

정리하면:

- 표준 RoPE는 가까운 문맥을 정확히 보는 데 유리합니다.
- pruned RoPE는 긴 문맥을 더 안정적으로 보는 데 유리합니다.
- Gemma 4는 local/global attention 구조에 맞춰 RoPE도 다르게 씁니다.

이 구조가 있어서 `128K`, `256K` 같은 긴 context를 그냥 숫자만 늘린 것이 아니라, attention과 position encoding을 함께 조정한 설계로 볼 수 있습니다.

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
- E2B/E4B의 sliding window는 512 token
- 26B A4B/31B의 sliding window는 1024 token

이 구조 덕분에:

- 긴 컨텍스트를 지원하면서도
- 무조건 모든 레이어가 full attention 인 모델보다
- 더 효율적으로 동작합니다.

조금 더 풀어 말하면, local layer는 가까운 token만 봅니다. 그래서 빠르고 가볍습니다.  
하지만 local layer만 계속 쌓으면 앞쪽 정보가 여러 layer를 거쳐 간접적으로 전달되어야 하므로, 긴 문서 전체 구조를 놓칠 수 있습니다.

그래서 중간중간 global layer를 넣습니다.  
global layer는 전체 문맥을 다시 직접 보면서 local layer가 놓칠 수 있는 큰 흐름을 잡아 줍니다.

### 2. Long Context용 RoPE 설계

RoPE는 문장 안에서 각 토큰이 어느 위치에 있는지 모델이 이해하도록 돕는 방식입니다.

Hugging Face Gemma 4 블로그 기준으로 Gemma 4는:

- sliding layer에는 표준 RoPE
- global layer에는 긴 문맥에 맞춘 **pruned RoPE / low-frequency-pruned RoPE**

를 사용합니다.

Maarten Grootendorst 설명 자료 기준으로는 global attention layer에서 `p=0.25`인 p-RoPE를 사용합니다.  
즉 모든 벡터 차원에 위치 회전을 넣는 대신 일부 차원에만 RoPE를 적용해, 긴 context에서 위치 정보가 과하게 흔들리지 않도록 하는 방식입니다.

실습에서는:

- “128K / 256K 문맥을 그냥 억지로 늘린 게 아니라”
- 긴 문맥을 버티기 위한 attention + positional encoding 조합이 들어갔다

정도로 이해하면 충분합니다.

### 3. Global attention 효율화

Global attention은 전체 context를 보기 때문에 비용이 큽니다.  
Gemma 4는 이 부분을 줄이기 위해 몇 가지 장치를 같이 씁니다.

- `GQA`: 여러 query head가 key/value head를 공유해 KV cache 부담을 줄입니다.
- `K=V`: 설명 자료 기준으로 global attention layer에서 key와 value를 같게 두어 cache 부담을 더 줄입니다.
- `p-RoPE`: global layer에서 긴 context를 더 안정적으로 다루기 위해 위치 회전 적용 범위를 줄입니다.

이 조합은 모두 같은 방향을 봅니다.

- 긴 context를 지원해야 함
- global attention 품질은 유지해야 함
- 하지만 로컬/온디바이스 실행을 위해 메모리와 계산량은 줄여야 함

### 4. Shared KV Cache

KV cache는 모델이 이미 읽은 문맥을 다시 계산하지 않도록 저장해 두는 내부 메모리입니다.

Hugging Face blog 기준으로 Gemma 4는 **shared KV cache** 를 사용합니다.

- 마지막 일부 레이어가 자기만의 key/value projection을 다시 만들지 않고
- 앞쪽 레이어의 KV 상태를 재사용합니다

의미:

- 긴 문맥에서 메모리와 계산량 절감
- 온디바이스/로컬 추론에 유리

### 5. Vision Encoder

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

### 6. Audio Encoder

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

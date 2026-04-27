# Apple Silicon + MLX 안내

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- Apple Silicon Mac(M1/M2/M3/M4) 사용자
- LM Studio에서 GGUF 말고 MLX 경로도 이해하고 싶은 참가자
- MLX 기반 파생 모델이나 fine-tuned 모델이 있는지 궁금한 참가자

## MLX란?

- MLX는 Apple Silicon용 머신러닝 프레임워크입니다.
- Apple의 `mlx-lm` 프로젝트는 Apple Silicon에서 LLM 실행뿐 아니라 fine-tuning(LoRA/QLoRA 포함)도 지원합니다.
- LM Studio 공식 문서도 Apple Silicon Mac에서 Apple의 MLX를 지원한다고 안내합니다.
- `GGUF`, `MLX`, `llama.cpp` 차이를 먼저 보고 싶다면 [GGUF, MLX, llama.cpp 개념 설명](./04-gguf-mlx-llamacpp-explainer.md) 문서를 함께 확인해 주세요.

## 행사 준비에서 MLX는 어떻게 보면 되나요?

- Apple Silicon 사용자는 LM Studio에서 GGUF뿐 아니라 MLX 모델도 선택할 수 있습니다.
- Gemma 4도 LM Studio 모델 페이지 기준 GGUF와 MLX로 제공됩니다.
- 다만 이번 핸즈온 참가 준비 관점에서는 MLX 자체가 필수는 아닙니다.
- Apple Silicon에서도 GGUF 기반 fine-tuned 모델을 대체로 사용할 수 있지만, 양자화 방식, 채팅 템플릿, 멀티모달 지원 여부에 따라 모델별 호환성과 품질 확인이 필요합니다.
- 즉, macOS 사용자는 `GGUF 기본 + 필요하면 MLX 추가 고려` 정도로 이해하면 됩니다.
- 가장 중요한 것은 행사 전에 사용할 모델을 미리 다운로드하고 실행 확인을 끝내는 것입니다.

## MLX 기반 Gemma 4 모델 예시

Hugging Face에는 아래와 같은 MLX 형식 Gemma 4 모델이 올라와 있습니다.

- `mlx-community/gemma-4-e2b-it-8bit`
- `mlx-community/gemma-4-e4b-it-8bit`

이 모델들은 Hugging Face 카드 기준으로 각각 원본 Google Gemma 4 체크포인트를 MLX 형식으로 변환한 모델입니다.

## MLX 기반 fine-tuned 모델도 있나요?

있습니다.

- Apple의 `mlx-lm`은 Gemma 계열을 포함한 여러 모델 패밀리에 대해 LoRA/QLoRA fine-tuning을 지원합니다.
- Hugging Face에는 MLX 기반 파생 모델이나 fine-tuned 모델도 존재합니다.
- 예를 들어 `emanubiz/gemma4-E4B-opus-finetuned` 같은 모델은 `mlx-community/gemma-4-e4b-it-4bit`를 바탕으로 LoRA fine-tuning 한 사례입니다.

즉, Apple Silicon 환경에서는 MLX로 실행 가능한 Gemma 파생 모델이나 fine-tuned 모델을 활용할 수 있습니다.

## `mlx-community` 관련 주의

- `mlx-community`는 공식 Google 배포처가 아니라 Hugging Face 커뮤니티 업로드/변환 흐름을 사용하는 조직입니다.
- 따라서 `mlx-community` 계열 모델은 공식 Google 원본이나 Ollama, LM Studio 허브의 기본 항목과 비교해 업데이트나 패치 반영 시점이 늦을 수 있습니다.
- 커뮤니티 모델은 변환 방식, 채팅 템플릿, 툴 호출, 멀티모달 동작이 제각각일 수 있습니다.

권장:

- 행사 당일에는 공식 Gemma 4 기본 모델(E2B/E4B) 사용을 우선 권장합니다.
- MLX 파생 모델, 커뮤니티 변환 모델, 개인 fine-tuned 모델은 추가 실험용으로만 권장합니다.

## Apple Silicon 사용자 권장안

- 하나만 설치한다면 LM Studio
- 메모리 8GB면 E2B만 시도, 속도 저하 감안
- 메모리 16GB면 E4B
- 행사 준비는 공식 기본 모델 우선
- GGUF로 준비해도 충분함
- GGUF fine-tuned 모델은 대체로 가능하지만, 모델별 호환성과 품질 확인 필요
- MLX는 선택 사항

8GB Apple Silicon Mac 추가 안내:

- 8GB 장비는 E2B에서도 속도가 많이 느리거나 시스템이 잠깐 멈춘 것처럼 보일 수 있습니다.
- E4B는 실행되더라도 행사 당일 안정성이 떨어질 수 있습니다.
- 가능하면 16GB 이상 메모리 장비를 권장합니다.
- 8GB 장비로 참석하는 경우에는 작은 모델, 짧은 컨텍스트, 최소한의 앱 실행을 전제로 준비해 주세요.

## 참고 문서

- [LM Studio MLX Engine Blog](https://lmstudio.ai/blog/unified-mlx-engine)
- [Apple MLX GitHub](https://github.com/ml-explore/mlx)
- [Apple MLX LM GitHub](https://github.com/ml-explore/mlx-lm)
- [MLX LoRA / QLoRA Guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Hugging Face MLX Community](https://huggingface.co/mlx-community)

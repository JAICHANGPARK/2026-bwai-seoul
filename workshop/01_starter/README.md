# Workshop Starter

시작 코드입니다. `translate`, `code` 시나리오가 등록되어 있고, 핸즈온을 진행하면서 `demo/scenarios.py`에 시나리오를 하나씩 추가합니다.

## 실행

```bash
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

Windows PowerShell:

```powershell
uv sync
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 10
```

Ollama를 쓰는 경우에는 포트와 모델명을 지정합니다.

```bash
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 3 --port 11434 --model "gemma4:e2b"
bash run.sh --scenario code --topic "Implement binary search for a sorted array" --tasks 3 --port 11434 --model "gemma4:e2b"
```

Windows PowerShell:

```powershell
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 3 --port 11434 --model "gemma4:e2b"
.\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 3 --port 11434 --model "gemma4:e2b"
```

단계별 추가 코드는 [03_labs/README.md](../03_labs/README.md)를 참고하세요.
`code` 기본 10개 agent에는 Dart가 포함됩니다.

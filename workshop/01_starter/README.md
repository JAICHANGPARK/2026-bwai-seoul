# Workshop Starter

시작 코드입니다. `translate` 시나리오만 등록되어 있고, 핸즈온을 진행하면서 `demo/scenarios.py`에 시나리오를 하나씩 추가합니다.

## 실행

```bash
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

Windows PowerShell:

```powershell
uv sync
.\run.ps1 --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

단계별 추가 코드는 [03_labs/README.md](../03_labs/README.md)를 참고하세요.

# uv 설치 가이드

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

## 이 문서는 누구를 위한 문서인가요?

- `Hermes Agent` 설치 중 `uv` 관련 오류가 난 분
- Python 기반 CLI 도구를 `uv` 또는 `uvx`로 실행해 보고 싶은 분
- 행사 전에 터미널 개발 환경을 미리 정리해 두고 싶은 분

## 먼저 결론

- `uv`는 Python 패키지와 실행 환경을 빠르게 관리하는 도구입니다.
- `uv` 자체가 Gemma 4 모델을 실행하는 도구는 아닙니다.
- 이번 핸즈온에서 `LM Studio` 또는 `Ollama`만 쓴다면 `uv`를 따로 설치하지 않아도 됩니다.
- `Hermes Agent` 공식 설치 스크립트는 `uv`를 자동으로 준비합니다.
- 다만 자동 설치가 실패하거나, `uvx`로 Python 기반 도구를 실행하고 싶다면 아래 절차로 미리 설치해 두면 됩니다.

공식 문서:

- [uv Installation](https://docs.astral.sh/uv/getting-started/installation/)

## 설치 확인

이미 설치되어 있는지 먼저 확인합니다.

```bash
uv --version
uvx --version
```

둘 중 하나가 `command not found`로 나오면 아래 운영체제별 설치 방법을 따라가세요.

## macOS / Linux / WSL2

가장 단순한 공식 standalone installer 방식입니다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`curl`이 없는 환경에서는 `wget`을 사용할 수 있습니다.

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

설치 후 터미널을 새로 열거나 셸 설정을 다시 읽습니다.

```bash
source ~/.zshrc
```

`bash` 사용자라면:

```bash
source ~/.bashrc
```

다시 확인합니다.

```bash
uv --version
uvx --version
```

그래도 명령을 찾지 못하면 `~/.local/bin`이 `PATH`에 들어 있는지 확인합니다.

```bash
echo $PATH
```

임시로 현재 터미널에만 추가하려면:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## macOS Homebrew

Homebrew를 쓰고 있다면 아래 방식도 가능합니다.

```bash
brew install uv
```

확인:

```bash
uv --version
uvx --version
```

## Windows PowerShell

PowerShell에서 공식 installer를 실행합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 후 PowerShell을 새로 열고 확인합니다.

```powershell
uv --version
uvx --version
```

회사 또는 학교 장비처럼 보안 정책이 엄격한 환경에서는 인터넷에서 받은 스크립트 실행이 막힐 수 있습니다. 이런 경우에는 관리자 권한, 실행 정책, 보안 솔루션 정책을 먼저 확인해야 합니다.

## Windows 패키지 매니저

`winget`을 쓰는 경우:

```powershell
winget install --id=astral-sh.uv -e
```

`Scoop`을 쓰는 경우:

```powershell
scoop install main/uv
```

확인:

```powershell
uv --version
uvx --version
```

## pipx 또는 pip로 설치

Python 환경이 이미 준비되어 있다면 `pipx`로 격리 설치할 수 있습니다.

```bash
pipx install uv
```

`pip`로도 설치할 수는 있습니다.

```bash
pip install uv
```

다만 행사 준비용으로 처음 설치한다면 standalone installer, Homebrew, winget 같은 운영체제별 설치 경로가 더 단순합니다.

## 업그레이드

standalone installer로 설치했다면:

```bash
uv self update
```

Homebrew로 설치했다면:

```bash
brew upgrade uv
```

winget으로 설치했다면:

```powershell
winget upgrade --id=astral-sh.uv -e
```

pipx로 설치했다면:

```bash
pipx upgrade uv
```

## 자동완성 설정

필수는 아니지만 터미널에서 `uv` 명령을 자주 쓸 계획이면 자동완성을 켤 수 있습니다.

`zsh`:

```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

`bash`:

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
source ~/.bashrc
```

PowerShell:

```powershell
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
Add-Content -Path $PROFILE -Value '(& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

설정 후 새 터미널을 열어 확인하세요.

## Hermes Agent와의 관계

`Hermes Agent` 설치 스크립트는 공식 문서 기준으로 `uv`, Python 3.11, Node.js, `ripgrep`, `ffmpeg` 등을 자동으로 준비합니다.

따라서 보통은:

1. [Hermes Agent 설치 가이드](./13-hermes-agent-setup.md)를 먼저 따라갑니다.
2. 설치 중 `uv` 관련 오류가 나면 이 문서로 돌아와 `uv`를 수동 설치합니다.
3. 이후 다시 `Hermes Agent` 설치 명령을 실행합니다.

## 행사 전 확인

`uv`를 직접 설치했다면 행사 전에 아래까지만 확인하면 충분합니다.

```bash
uv --version
uvx --version
```

`Hermes Agent`까지 준비하는 경우에는 이어서 아래도 확인합니다.

```bash
hermes version
hermes doctor
```

## 자주 헷갈리는 점

### `uv`를 설치하면 Python도 자동으로 설치되나요?

`uv`는 Python 버전 관리 기능을 제공하지만, 설치 방식과 명령에 따라 실제 Python 다운로드 여부는 달라집니다. 단순히 `uv`만 설치했다고 해서 모든 프로젝트용 Python 환경이 자동으로 준비되는 것은 아닙니다.

### `uvx`는 무엇인가요?

`uvx`는 Python 기반 command-line tool을 별도 프로젝트에 설치하지 않고 바로 실행할 때 쓰는 명령입니다. Node.js 생태계의 `npx`와 비슷하게 이해하면 됩니다.

### `uv`가 Gemma 4 모델을 다운로드하나요?

아닙니다. Gemma 4 모델 다운로드는 `LM Studio`, `Ollama`, `llama.cpp` 같은 모델 실행 도구에서 처리합니다. `uv`는 Python 도구와 실행 환경을 관리하는 역할입니다.


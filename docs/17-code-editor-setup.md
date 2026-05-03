# 코드 편집기 설치 가이드: Visual Studio Code / Google Antigravity

[메인 안내로 돌아가기](../gemma4-local-setup-guide.md)

기준 확인일: 2026-05-02

## 이 문서는 누구를 위한 문서인가요?

- 핸즈온에서 `workshop/01_starter` 코드를 직접 수정해야 하는 분
- Python 파일과 Markdown 산출물을 편하게 열어 보고 싶은 분
- `Visual Studio Code` 또는 `Google Antigravity` 중 어떤 편집기를 준비할지 고르고 싶은 분

## 먼저 결론

- 이번 핸즈온에서는 `workshop/01_starter/demo/scenarios.py`를 직접 수정합니다.
- 코드 편집기는 **Visual Studio Code 또는 Google Antigravity 중 하나만 준비해도 됩니다.**
- 처음 준비한다면 **Visual Studio Code**를 권장합니다.
- AI agent 기반 코드 수정까지 실험해 보고 싶다면 **Google Antigravity**를 선택할 수 있습니다.
- Google Antigravity는 preview 성격의 도구이며, 공식 codelab 기준 개인 Gmail 계정과 Chrome 브라우저가 필요합니다.

선택 기준:

| 상황 | 권장 편집기 |
| --- | --- |
| 처음 코드를 수정해 보는 경우 | Visual Studio Code |
| 설치와 사용 흐름을 안정적으로 가져가고 싶은 경우 | Visual Studio Code |
| VS Code에 이미 익숙한 경우 | Visual Studio Code |
| agent가 계획, 코드 수정, 브라우저 검증까지 하는 흐름을 보고 싶은 경우 | Google Antigravity |
| 개인 Gmail 계정 사용이 어렵거나 회사/학교 계정만 있는 경우 | Visual Studio Code |

## 공통 준비

핸즈온 코드는 아래 위치에서 시작합니다.

```text
workshop/01_starter
```

실습에서 주로 수정하는 파일은 아래입니다.

```text
workshop/01_starter/demo/scenarios.py
```

터미널에서 저장소 루트에 있다면 아래처럼 열면 됩니다.

```bash
cd workshop/01_starter
```

또는 편집기에서 `workshop/01_starter` 폴더를 직접 열어도 됩니다.

## Visual Studio Code 설치

공식 문서:

- [Visual Studio Code Download](https://code.visualstudio.com/Download)
- [VS Code setup overview](https://code.visualstudio.com/docs/setup/setup-overview)
- [VS Code on Windows](https://code.visualstudio.com/docs/setup/windows)
- [VS Code on macOS](https://code.visualstudio.com/docs/setup/mac)
- [VS Code on Linux](https://code.visualstudio.com/docs/setup/linux)
- [VS Code command line](https://code.visualstudio.com/docs/configure/command-line)

### Windows

가장 쉬운 방법은 공식 설치 프로그램을 사용하는 것입니다.

1. [VS Code Download](https://code.visualstudio.com/Download)에 접속합니다.
2. Windows용 installer를 다운로드합니다.
3. `VSCodeUserSetup-{version}.exe`를 실행합니다.
4. 설치가 끝나면 PowerShell 또는 명령 프롬프트를 새로 엽니다.
5. 아래 명령으로 확인합니다.

```powershell
code --version
```

설치 프로그램은 보통 `code` 명령을 `PATH`에 추가합니다. 설치 직후 `code` 명령이 안 되면 PowerShell을 완전히 닫았다가 다시 여세요.

### macOS

1. [VS Code Download](https://code.visualstudio.com/Download)에 접속합니다.
2. macOS용 `.dmg` 파일을 다운로드합니다.
3. `.dmg`를 열고 `Visual Studio Code.app`을 `Applications` 폴더로 옮깁니다.
4. `Applications` 폴더에서 VS Code를 실행합니다.

터미널에서 `code .`로 열고 싶다면 VS Code 안에서 아래 작업을 한 번 해 주세요.

1. VS Code 실행
2. `Cmd + Shift + P`
3. `Shell Command: Install 'code' command in PATH` 실행
4. 터미널을 새로 열기

확인:

```bash
code --version
```

Homebrew를 쓰는 경우에는 아래 방식도 가능합니다.

```bash
brew install --cask visual-studio-code
```

### Linux

Ubuntu/Debian 계열에서는 공식 `.deb` 패키지를 받아 설치하는 방식이 가장 단순합니다.

1. [VS Code Download](https://code.visualstudio.com/Download)에 접속합니다.
2. Linux용 `.deb` 패키지를 다운로드합니다.
3. 다운로드한 파일이 있는 폴더에서 아래처럼 설치합니다.

```bash
sudo apt install ./<file>.deb
```

설치 확인:

```bash
code --version
```

Linux 배포판마다 패키지 형식과 업데이트 방식이 다를 수 있으므로, Fedora/RHEL 계열이나 다른 배포판은 공식 Linux 설치 문서를 확인하세요.

## VS Code에서 핸즈온 코드 열기

저장소 루트에서:

```bash
code workshop/01_starter
```

Windows PowerShell에서도 같은 방식으로 열 수 있습니다.

```powershell
code .\workshop\01_starter
```

VS Code가 열리면 아래 파일을 확인합니다.

```text
demo/scenarios.py
```

권장 확장:

- `Python`
- `Markdown Preview Mermaid Support` 또는 Markdown preview 관련 확장
- `GitHub Copilot`은 선택 사항입니다.

확장 설치가 부담스럽다면 Python 확장만 설치해도 이번 핸즈온 진행에는 충분합니다.

## Google Antigravity 설치

공식 문서와 codelab:

- [Google Antigravity](https://antigravity.google/)
- [Google Antigravity Download](https://antigravity.google/download)
- [Getting Started with Google Antigravity - Google Codelabs](https://codelabs.developers.google.com/getting-started-google-antigravity)
- [Google Antigravity Docs](https://antigravity.google/docs)

### 먼저 알아둘 점

- Google Antigravity는 agent-first 개발 환경입니다.
- VS Code 기반 편집 경험과 별도 Agent Manager 흐름을 함께 제공합니다.
- 공식 codelab 기준 현재 preview로 제공되며, 개인 Gmail 계정으로 시작할 수 있습니다.
- Chrome 브라우저가 필요합니다.
- 회사 또는 학교 Google Workspace 계정은 preview 정책에 따라 제한될 수 있으므로, 행사 전 개인 Gmail 계정으로 로그인이 되는지 확인하세요.

### 설치 순서

1. [Google Antigravity Download](https://antigravity.google/download)에 접속합니다.
2. 본인 운영체제에 맞는 설치 파일을 다운로드합니다.
3. 설치 파일을 실행합니다.
4. 앱을 실행하고 초기 설정을 진행합니다.
5. 개인 Gmail 계정으로 로그인합니다.
6. 설정 중 `Command Line` 또는 `agy` command-line tool 설치 옵션이 보이면 켜 둡니다.
7. agent 설정은 처음에는 `Review-driven development`에 가까운 안전한 설정을 권장합니다.

운영체제별 설치 파일 이름과 세부 UI는 preview 기간에 바뀔 수 있습니다. 행사 전에는 반드시 공식 다운로드 페이지에서 최신 안내를 확인하세요.

### Antigravity에서 핸즈온 코드 열기

앱에서 직접 여는 방식:

1. Antigravity 실행
2. `Open Folder` 선택
3. 저장소의 `workshop/01_starter` 폴더 선택
4. `demo/scenarios.py` 열기

`agy` 명령을 설치했다면 아래 방식도 사용할 수 있습니다.

```bash
cd workshop/01_starter
agy .
```

`agy` 명령이 안 되면 앱에서 `Open Folder`를 사용하면 됩니다. CLI 옵션이 궁금하면 아래처럼 확인하세요.

```bash
agy --help
```

## 행사 전 확인

Visual Studio Code를 선택했다면:

```bash
code --version
code workshop/01_starter
```

Google Antigravity를 선택했다면:

- 앱 실행 성공
- 개인 Gmail 계정 로그인 성공
- `workshop/01_starter` 폴더 열기 성공
- `demo/scenarios.py` 파일 열기 성공
- 가능하면 `Review-driven development` 방식으로 agent 권한 설정

## 어떤 편집기를 준비해야 하나요?

처음 준비한다면 VS Code가 더 안정적입니다. 설치가 쉽고, 운영체제별 문서가 잘 정리되어 있으며, 핸즈온에서 필요한 직접 코드 수정 흐름에 충분합니다.

Antigravity는 agent 기반 개발 흐름을 보여 주기에 좋지만, preview 정책, 계정 로그인, 브라우저 extension, agent 권한 설정 같은 준비 요소가 더 많습니다. 이미 VS Code가 준비되어 있다면 Antigravity는 선택 실험 경로로 보면 됩니다.

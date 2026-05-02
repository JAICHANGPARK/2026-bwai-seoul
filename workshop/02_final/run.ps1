# run.ps1 - Launch the multi-agent demo with PowerShell windows.
#
# Usage:
#   .\run.ps1 --scenario <name> [--topic <text>] [--port <port>] [--tasks <n>] [--model <name>] [--hires <n>] [--select <n>] [--reasoning on|off]
#
# Examples:
#   .\run.ps1 --scenario translate --topic "Hello world"
#   .\run.ps1 --scenario code --topic "Implement binary search for a sorted array" --tasks 10
#   .\run.ps1 --scenario resume --topic "도서 출판사 소설 기획자" --tasks 10
#   .\run.ps1 --scenario marketer_resume --topic "도서 출판사 북 마케터" --tasks 10
#   .\run.ps1 --scenario marketer_interview_review --topic "도서 출판사 북 마케터" --tasks 10
#   .\run.ps1 --scenario marketer_hiring_decision --topic "도서 출판사 북 마케터" --hires 2
#   .\run.ps1 --scenario publication_offer_email --topic "문예지 신인상 투고용 도시 미스터리 단편"
#   .\run.ps1 --scenario contract_negotiation --topic "문예지 신인상 투고용 도시 미스터리 단편"
#   .\run.ps1 --scenario contract_draft --topic "문예지 신인상 투고용 도시 미스터리 단편"
#   .\run.ps1 --scenario story_revision --topic "문예지 신인상 투고용 도시 미스터리 단편"
#   .\run.ps1 --scenario marketing_copy --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10

$ErrorActionPreference = "Stop"

$Port = "1234"
$Scenario = "translate"
$Topic = "Gemma is Google DeepMind most capable open AI model"
$Tasks = ""
$Model = "default"
$Hires = "2"
$Select = "3"
$Reasoning = "off"

# The Windows launcher mirrors run.sh but uses PowerShell windows instead of
# macOS Terminal + AppleScript. Keep this file dependency-free so participants
# can run it after installing only uv and LM Studio.
function Show-Usage {
    Write-Host "Usage: .\run.ps1 --scenario <name> [--topic <text>] [--port <port>] [--tasks <n>] [--model <name>] [--hires <n>] [--select <n>] [--reasoning on|off]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  --scenario   Scenario name (translate, code, resume, interview_review, hiring_decision, marketer_resume, marketer_interview_review, marketer_hiring_decision, interview_dialogue, hiring_decision_from_dialogue, novel_writing, short_story_writing, story_review_selection, publication_offer_email, contract_negotiation, contract_draft, story_revision, marketing_copy)  [default: translate]"
    Write-Host "  --topic      Topic or text; optional when scenario reads prior Markdown outputs"
    Write-Host "  --port       OpenAI-compatible server port        [default: 1234]"
    Write-Host "  --tasks      Number of LLMs to use                [default: scenario default or selected-story count]"
    Write-Host "  --model      OpenAI-compatible model name         [default: default]"
    Write-Host "  --hires      Number of hires for hiring_decision  [default: 2]"
    Write-Host "  --select     Number of stories to select in story_review_selection [default: 3]"
    Write-Host "  --reasoning  Enable model thinking/reasoning      [default: off]"
}

function Read-Value {
    param(
        [string[]]$Values,
        [int]$Index,
        [string]$Name
    )

    if (($Index + 1) -ge $Values.Count) {
        throw "Missing value for $Name"
    }
    return $Values[$Index + 1]
}

# Manual argument parsing keeps the script compatible with Windows PowerShell
# and PowerShell 7 without requiring advanced parameter binding.
for ($i = 0; $i -lt $args.Count; $i++) {
    switch ($args[$i]) {
        "--port" {
            $Port = Read-Value -Values $args -Index $i -Name "--port"
            $i++
            continue
        }
        "--scenario" {
            $Scenario = Read-Value -Values $args -Index $i -Name "--scenario"
            $i++
            continue
        }
        "--topic" {
            $Topic = Read-Value -Values $args -Index $i -Name "--topic"
            $i++
            continue
        }
        "--tasks" {
            $Tasks = Read-Value -Values $args -Index $i -Name "--tasks"
            $i++
            continue
        }
        "--model" {
            $Model = Read-Value -Values $args -Index $i -Name "--model"
            $i++
            continue
        }
        "--hires" {
            $Hires = Read-Value -Values $args -Index $i -Name "--hires"
            $i++
            continue
        }
        "--select" {
            $Select = Read-Value -Values $args -Index $i -Name "--select"
            $i++
            continue
        }
        "--reasoning" {
            $Reasoning = Read-Value -Values $args -Index $i -Name "--reasoning"
            $i++
            continue
        }
        "--help" {
            Show-Usage
            exit 0
        }
        default {
            throw "Unknown argument: $($args[$i]). Use --help for usage."
        }
    }
}

function Quote-PowerShellString {
    # Child windows are launched with generated PowerShell code. Single-quote
    # escaping prevents paths/topics containing spaces or quotes from breaking it.
    param([string]$Value)
    return "'" + ($Value -replace "'", "''") + "'"
}

function New-PowerShellArrayLiteral {
    param([string[]]$Values)
    return "@(" + (($Values | ForEach-Object { Quote-PowerShellString $_ }) -join ", ") + ")"
}

function Resolve-Python {
    param([string]$Root)

    # uv creates different virtualenv executable paths depending on OS/shell.
    # Check Windows first, then Unix-style paths for users running PowerShell Core.
    $candidates = @(
        (Join-Path $Root ".venv\Scripts\python.exe"),
        (Join-Path $Root ".venv\bin\python.exe"),
        (Join-Path $Root ".venv\bin\python")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    throw ".venv not found at $Root\.venv - run 'uv sync' first"
}

function Resolve-PowerShellExe {
    $candidates = @("pwsh.exe", "powershell.exe")

    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    throw "Could not find pwsh.exe or powershell.exe"
}

function Resolve-ModelName {
    param(
        [string]$Model,
        [string]$ServerUrl
    )

    if ($Model -ne "default") {
        return $Model
    }

    try {
        # LM Studio exposes /v1/models. When the user leaves --model as default,
        # use the first loaded model ID so participants do not have to type it.
        $models = Invoke-RestMethod -Uri "$ServerUrl/v1/models" -TimeoutSec 2
        $firstModel = @($models.data)[0]
        if ($firstModel -and $firstModel.id) {
            return [string]$firstModel.id
        }
    }
    catch {
        return $Model
    }

    return $Model
}

function New-EncodedChildCommand {
    param(
        [string]$Title,
        [string]$Python,
        [string]$DemoDir,
        [string]$Model,
        [string[]]$Arguments
    )

    # Start-Process quoting gets fragile with Korean text and nested arguments.
    # Encode the whole child script as UTF-16LE Base64, which is what
    # powershell.exe/pwsh.exe expects for -EncodedCommand.
    $argumentLiteral = New-PowerShellArrayLiteral $Arguments
    $lines = @(
        '$ErrorActionPreference = "Stop"',
        # Force UTF-8 so Korean Markdown and emoji render correctly in child windows.
        'if (Get-Command chcp.com -ErrorAction SilentlyContinue) { chcp.com 65001 | Out-Null }',
        '$utf8 = New-Object System.Text.UTF8Encoding $false',
        '[Console]::InputEncoding = $utf8',
        '[Console]::OutputEncoding = $utf8',
        '$env:PYTHONIOENCODING = "utf-8"',
        '$env:PYTHONUTF8 = "1"',
        '$env:LLM_MODEL = ' + (Quote-PowerShellString $Model),
        '$Host.UI.RawUI.WindowTitle = ' + (Quote-PowerShellString $Title),
        'Set-Location -LiteralPath ' + (Quote-PowerShellString $DemoDir),
        '$argList = ' + $argumentLiteral,
        '& ' + (Quote-PowerShellString $Python) + ' @argList',
        '$exitCode = $LASTEXITCODE',
        'if ($null -eq $exitCode) { $exitCode = 0 }',
        'if ($exitCode -ne 0) { Write-Host ""; Read-Host "Process failed. Press Enter to close" | Out-Null }',
        'exit $exitCode'
    )
    $script = $lines -join "`n"
    return [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
}

function Start-DemoWindow {
    param(
        [string]$PowerShellExe,
        [string]$Title,
        [string]$Python,
        [string]$DemoDir,
        [string]$Model,
        [string[]]$Arguments
    )

    # Every process gets its own window: one dashboard, one orchestrator, and one
    # specialist per agent. This mirrors the visual layout of the macOS launcher.
    $encodedCommand = New-EncodedChildCommand `
        -Title $Title `
        -Python $Python `
        -DemoDir $DemoDir `
        -Model $Model `
        -Arguments $Arguments

    Start-Process -FilePath $PowerShellExe -ArgumentList @("-EncodedCommand", $encodedCommand) | Out-Null
    Start-Sleep -Milliseconds 150
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DemoDir = Join-Path $ScriptDir "demo"
$Python = Resolve-Python $ScriptDir
$PowerShellExe = Resolve-PowerShellExe
$ApiUrl = "http://127.0.0.1:$Port/v1/chat/completions"
$ServerUrl = "http://127.0.0.1:$Port"
$Model = Resolve-ModelName -Model $Model -ServerUrl $ServerUrl

if ($Reasoning -ne "on" -and $Reasoning -ne "off") {
    throw "--reasoning must be 'on' or 'off'"
}

$utf8 = New-Object System.Text.UTF8Encoding $false
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:WORKSHOP_DEMO_DIR = $DemoDir
$env:WORKSHOP_SCENARIO = $Scenario
$env:WORKSHOP_TASKS = $Tasks

$loadAgentsScript = @'
import os
import sys

sys.path.insert(0, os.environ["WORKSHOP_DEMO_DIR"])
from scenarios import get_scenario

tasks = os.environ.get("WORKSHOP_TASKS") or None
n_agents = int(tasks) if tasks else None
scenario = get_scenario(os.environ["WORKSHOP_SCENARIO"], n_agents=n_agents)

for agent in scenario["agents"]:
    print(f"{agent['name']}|{agent['emoji']}|{agent['color']}")
'@

# Ask scenarios.py for agent metadata before opening windows. This keeps the
# launcher generic; new scenarios only need to be registered in demo/scenarios.py.
$agentData = & $Python -c $loadAgentsScript
if ($LASTEXITCODE -ne 0 -or -not $agentData) {
    throw "Failed to load scenario '$Scenario'"
}

$agents = @()
foreach ($line in $agentData) {
    if (-not $line.Trim()) {
        continue
    }

    $parts = $line -split "\|", 3
    if ($parts.Count -ne 3) {
        throw "Invalid agent data: $line"
    }

    $agents += [pscustomobject]@{
        Name = $parts[0]
        Emoji = $parts[1]
        Color = $parts[2]
    }
}

$dashboardArgs = @(
    # dashboard.py reads metrics JSON files and renders status/throughput.
    "dashboard.py",
    "--server-url", $ServerUrl,
    "--scenario", $Scenario,
    "--topic", $Topic
)
if ($Tasks) {
    $dashboardArgs += @("--tasks", $Tasks)
}

$orchestratorArgs = @(
    # orchestrator.py creates task JSON files, collects result JSON files, and
    # assembles the generated HTML/Markdown outputs.
    "orchestrator.py",
    "--scenario", $Scenario,
    "--api-url", $ApiUrl,
    "--topic", $Topic,
    "--reasoning", $Reasoning
)
if ($Tasks) {
    $orchestratorArgs += @("--tasks", $Tasks)
}
if ($Hires) {
    $orchestratorArgs += @("--hires", $Hires)
}
if ($Select) {
    $orchestratorArgs += @("--select", $Select)
}

Start-DemoWindow `
    -PowerShellExe $PowerShellExe `
    -Title "Dashboard" `
    -Python $Python `
    -DemoDir $DemoDir `
    -Model $Model `
    -Arguments $dashboardArgs

Start-DemoWindow `
    -PowerShellExe $PowerShellExe `
    -Title "Orchestrator" `
    -Python $Python `
    -DemoDir $DemoDir `
    -Model $Model `
    -Arguments $orchestratorArgs

foreach ($agent in $agents) {
    $specialistArgs = @(
        # specialist.py waits for task_<name>.json, calls LM Studio, and writes
        # result_<name>.json for the orchestrator to collect.
        "specialist.py",
        "--name", $agent.Name,
        "--emoji", $agent.Emoji,
        "--color", $agent.Color,
        "--api-url", $ApiUrl,
        "--reasoning", $Reasoning
    )

    Start-DemoWindow `
        -PowerShellExe $PowerShellExe `
        -Title $agent.Name `
        -Python $Python `
        -DemoDir $DemoDir `
        -Model $Model `
        -Arguments $specialistArgs
}

Write-Host "Launched: $Scenario ($($agents.Count) agents + orchestrator + dashboard)"

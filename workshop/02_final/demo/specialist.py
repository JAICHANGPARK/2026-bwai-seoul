"""
specialist.py — Specialist agent for the multi-agent demo.

Polls for a task file, calls the LLM, streams the response, writes the result.

Usage:
    python specialist.py --name french --emoji "🇫🇷" --color "1;34" \
        --api-url http://127.0.0.1:8080/v1/chat/completions
"""

import argparse
import json
import os
import time

from utils import COMMS_DIR, RESET, DIM, stream_llm

POLL_INTERVAL = 0.5


def wait_for_task(name: str) -> dict:
    """Poll until the orchestrator writes task_{name}.json.

    각 specialist 프로세스는 자기 이름과 같은 task 파일만 기다립니다. 파일이
    나타나면 읽고 바로 삭제해서 같은 작업이 두 번 실행되지 않게 합니다.
    JSONDecodeError를 무시하는 이유는 orchestrator가 파일을 쓰는 아주 짧은
    순간에 specialist가 먼저 읽을 수 있기 때문입니다.
    """
    task_path = os.path.join(COMMS_DIR, f"task_{name}.json")
    while True:
        if os.path.exists(task_path):
            time.sleep(0.1)
            try:
                with open(task_path, "r") as f:
                    task = json.load(f)
                os.remove(task_path)
                return task
            except (json.JSONDecodeError, IOError):
                pass
        time.sleep(POLL_INTERVAL)


def main():
    parser = argparse.ArgumentParser()
    # run.sh/run.ps1이 각 specialist 창을 열 때 아래 인자들을 넘깁니다.
    # name은 task/result 파일명에 쓰이는 agent id이고, emoji/color는 터미널 UI용입니다.
    parser.add_argument("--name", required=True)
    parser.add_argument("--emoji", default="🤖")
    parser.add_argument("--color", default="1;37")
    parser.add_argument("--api-url", default="http://127.0.0.1:8080/v1/chat/completions")
    parser.add_argument("--reasoning", choices=["on", "off"], default="off",
                        help="Enable or disable model thinking/reasoning controls")
    args = parser.parse_args()

    color = args.color
    name = args.name
    display = name.upper().replace("_", " ")

    # Header: 여러 터미널 창이 동시에 열리므로, 각 창이 어떤 agent인지
    # 바로 식별할 수 있게 색상과 emoji를 크게 보여줍니다.
    print(f"\033[{color}m{'━' * 45}{RESET}")
    print(f"\033[{color}m  {args.emoji}  {display}{RESET}")
    print(f"\033[{color}m{'━' * 45}{RESET}")
    print(f"{DIM}  Waiting for task...{RESET}\n")

    # Wait -> Execute -> Report
    # 1. orchestrator가 task JSON 파일을 만들 때까지 대기
    # 2. system prompt와 user instruction을 OpenAI message 형태로 조립
    # 3. stream_llm으로 LM Studio에 요청하고 결과를 result JSON으로 저장
    task = wait_for_task(name)
    instruction = task.get("instruction", "")
    system_prompt = task.get("system_prompt", "")

    print(f"\033[{color}m📋 {instruction[:60]}...{RESET}\n")
    print(f"\033[{color}m{'─' * 45}{RESET}\n")

    messages = []
    if system_prompt:
        # system_prompt는 시나리오 전체에 공통으로 적용되는 역할/출력 규칙입니다.
        # 예: "Markdown만 출력", "실제 개인정보 금지", "심사 보고서 형식 유지".
        messages.append({"role": "system", "content": system_prompt})
    # instruction은 agent별 개별 작업입니다. 예: "3번 이력서를 면접관 관점으로 평가".
    messages.append({"role": "user", "content": instruction})

    result = stream_llm(args.api_url, messages, agent_name=name, color=color, reasoning=args.reasoning)

    # Write result: orchestrator.collect()가 result_{name}.json 파일들을 모아서
    # HTML/Markdown 산출물을 만듭니다.
    result_path = os.path.join(COMMS_DIR, f"result_{name}.json")
    with open(result_path, "w") as f:
        json.dump({"task_id": task.get("task_id", ""), "result": result}, f)

    print(f"\n\n\033[{color}m{'─' * 45}{RESET}")
    print(f"\033[{color}m  ✅ {args.emoji}  {display} — Done!{RESET}")
    print(f"\033[{color}m{'─' * 45}{RESET}")

    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()

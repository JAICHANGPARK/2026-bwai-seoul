"""
utils.py — Shared utilities for the multi-agent demo.

Contains the LLM streaming logic, metrics writer, and shared constants
used by both the orchestrator and specialist agents.
"""

import json
import os
import sys
import time

from openai import OpenAI

# ─── Shared Paths ───────────────────────────────────────────
#
# 이 데모는 별도의 메시지 브로커나 DB를 쓰지 않고, 같은 폴더 안의 JSON 파일로
# orchestrator와 specialist agent들이 통신합니다. 구조가 단순해서 핸즈온에서
# "작업 배정 -> 결과 수집" 흐름을 파일 시스템만으로 눈으로 확인할 수 있습니다.

COMMS_DIR = os.path.join(os.path.dirname(__file__), ".agent_comms")
BUILD_DIR = os.path.join(os.path.dirname(__file__), "website_build")

# ─── ANSI Colors ────────────────────────────────────────────

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
WHITE = "\033[1;37m"


# ─── Metrics ────────────────────────────────────────────────

def write_metrics(name: str, status: str, tokens: int, elapsed: float, tps: float = None):
    """Write metrics to .agent_comms/metrics_{name}.json atomically.

    dashboard.py는 이 JSON 파일들을 주기적으로 읽어 agent별 상태와 tokens/sec를
    표시합니다. 임시 파일에 먼저 쓰고 os.replace로 교체하는 이유는 dashboard가
    파일을 읽는 순간에 JSON이 반쯤 쓰인 상태가 되는 것을 피하기 위해서입니다.
    """
    if tps is None:
        tps = tokens / elapsed if elapsed > 0 else 0.0
    metrics = {
        "name": name,
        "status": status,
        "tokens": tokens,
        "elapsed_s": round(elapsed, 2),
        "tps": round(tps, 1),
    }
    path = os.path.join(COMMS_DIR, f"metrics_{name}.json")
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(metrics, f)
    os.replace(tmp, path)


# ─── LLM Streaming ─────────────────────────────────────────

def stream_llm(
    api_url: str,
    messages: list[dict],
    agent_name: str,
    color: str = "1;37",
    max_tokens: int = 4000,
    reasoning: str = "off",
) -> str:
    """Stream an LLM response, update metrics, and print tokens in color.

    Args:
        api_url:    Full chat completions URL (e.g. http://…/v1/chat/completions).
        messages:   OpenAI-style messages list.
        agent_name: Name used for metrics files.
        color:      ANSI color code for terminal output.
        max_tokens: Maximum tokens to generate.
        reasoning:  "on" requests model thinking/reasoning when supported.

    Returns:
        The full response text (content only, excluding reasoning tokens).
    """
    base_url = api_url.rsplit("/chat/completions", 1)[0]
    # OpenAI SDK는 base_url만 주면 LM Studio의 OpenAI-compatible endpoint에도
    # 그대로 붙을 수 있습니다. LM Studio는 실제 API key를 검증하지 않으므로
    # dummy key를 사용합니다.
    client = OpenAI(base_url=base_url, api_key="sk-no-key")
    reasoning = (reasoning or "off").lower()
    requested_model = os.environ.get("LLM_MODEL", "default")

    def detect_model_id():
        """Return the first model exposed by /v1/models, when available."""
        try:
            models = client.models.list()
            data = getattr(models, "data", None) or []
            if not data:
                return None
            first = data[0]
            if isinstance(first, dict):
                return first.get("id")
            return getattr(first, "id", None)
        except Exception:
            return None

    model_name = requested_model
    if requested_model == "default":
        # LM Studio/Ollama servers usually expose the loaded model at /v1/models.
        # Resolving it here keeps run.sh and run.ps1 behavior consistent.
        detected_model = detect_model_id()
        if detected_model:
            model_name = detected_model

    full = ""
    chunk_count = 0
    server_tokens = None  # Will be set from usage if available
    start_t = time.time()

    def create_response(use_reasoning_controls: bool, include_stream_usage: bool):
        # 모든 specialist와 orchestrator planning 호출이 이 request builder를 탑니다.
        # 모델 이름은 run.sh/run.ps1이 환경변수 LLM_MODEL로 넘겨주며, LM Studio에서
        # 모델 ID를 자동 감지하지 못하는 경우 --model로 직접 지정할 수 있습니다.
        request = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        }
        if include_stream_usage:
            # 최신 OpenAI-compatible 서버는 usage 포함 스트리밍을 지원하지만,
            # 일부 LM Studio/Ollama 버전은 이 필드를 거절할 수 있어 아래에서
            # minimal request로 한 번 더 재시도합니다.
            request["stream_options"] = {"include_usage": True}
        if use_reasoning_controls:
            # Gemma 계열 서버/런타임마다 thinking 옵션 이름이 조금 다를 수 있어
            # 흔히 쓰이는 camelCase와 snake_case를 함께 보냅니다. 서버가 모르는
            # 옵션을 거절하면 아래 except 블록에서 한 번 더 plain request로 재시도합니다.
            enable_thinking = reasoning == "on"
            request["extra_body"] = {
                "enableThinking": enable_thinking,
                "enable_thinking": enable_thinking,
            }
            if enable_thinking:
                request["reasoning_effort"] = "medium"
        return client.chat.completions.create(**request)

    # 기본값 off에서는 thinking 제어 필드를 아예 보내지 않습니다. 일부 LM Studio
    # 버전은 알 수 없는 extra_body를 요청 오류로 처리하기 때문입니다.
    use_reasoning_controls = reasoning == "on"
    last_poll_t = start_t
    poll_interval = 0.3
    chunks_since_poll = 0

    def consume_response(response):
        nonlocal full, chunk_count, server_tokens, last_poll_t, chunks_since_poll

        for chunk in response:
            # Final chunk with usage stats (no choices)
            if hasattr(chunk, "usage") and chunk.usage:
                server_tokens = chunk.usage.completion_tokens
                continue

            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            # Handle reasoning tokens (thinking models)
            rc = getattr(delta, "reasoning_content", None) or getattr(delta, "reasoning", None)
            if rc:
                # reasoning/thinking 토큰은 터미널에서는 흐리게 보여주되 최종 결과
                # Markdown/HTML에는 섞지 않습니다. 결과물 파싱 안정성을 위한 분리입니다.
                sys.stdout.write(f"\033[2;37m{rc}\033[0m")
                sys.stdout.flush()

            c = delta.content or ""
            if c:
                full += c
                sys.stdout.write(f"\033[{color}m{c}\033[0m")
                sys.stdout.flush()

            if rc or c:
                chunks_since_poll += 1
                chunk_count += 1

                now = time.time()
                if (now - last_poll_t) >= poll_interval:
                    # 토큰이 들어올 때마다 파일을 쓰면 디스크 I/O가 많아지므로
                    # 짧은 interval로 묶어서 dashboard에 충분히 부드럽게 갱신합니다.
                    tps = chunks_since_poll / (now - last_poll_t)
                    tokens = server_tokens if server_tokens is not None else chunk_count
                    write_metrics(agent_name, "running", tokens, now - start_t, tps)
                    chunks_since_poll = 0
                    last_poll_t = now

    try:
        write_metrics(agent_name, "running", 0, 0.0, 0.0)
        attempts = [(use_reasoning_controls, True, None)]
        if use_reasoning_controls:
            attempts.append((
                False,
                True,
                "\n\033[33m[reasoning controls unsupported; retrying without them]\033[0m\n",
            ))
        attempts.append((
            False,
            False,
            "\n\033[33m[retrying with a minimal OpenAI-compatible request]\033[0m\n",
        ))

        last_error = None
        for attempt_reasoning, include_stream_usage, retry_message in attempts:
            if retry_message:
                sys.stdout.write(retry_message)
                sys.stdout.flush()
            try:
                consume_response(create_response(attempt_reasoning, include_stream_usage))
                last_error = None
                break
            except Exception as e:
                last_error = e
                # If streaming already started, do not repeat the request and risk
                # duplicated output or duplicated side effects in downstream prompts.
                if full or chunk_count:
                    break

        if last_error is not None:
            sys.stdout.write(f"\n\033[31m[ERROR] {last_error}\033[0m\n")

    except Exception as e:
        sys.stdout.write(f"\n\033[31m[ERROR] {e}\033[0m\n")

    total_elapsed = time.time() - start_t
    # Use server-reported token count if available, otherwise fall back to chunk count
    final_tokens = server_tokens if server_tokens is not None else chunk_count
    final_tps = final_tokens / total_elapsed if total_elapsed > 0 else 0.0
    write_metrics(agent_name, "done", final_tokens, total_elapsed, final_tps)

    return full

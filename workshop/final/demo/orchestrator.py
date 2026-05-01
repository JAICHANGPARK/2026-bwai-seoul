"""
orchestrator.py — Orchestrator for the multi-agent demo.

Uses the LLM to decompose a topic into per-agent tasks, dispatches them
via JSON files, collects results, and assembles a visual HTML page.

Usage:
    python orchestrator.py --scenario translate --topic "Gemma is an open AI model"
    python orchestrator.py --scenario svg_art --topic "Technology and AI"
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time

from scenarios import get_scenario
from utils import (
    COMMS_DIR, BUILD_DIR, RESET, DIM, BOLD, CYAN, GREEN, YELLOW, WHITE,
    stream_llm, write_metrics,
)

POLL_INTERVAL = 0.5


def slugify(value: str) -> str:
    """Create a filesystem-safe slug for generated build artifacts."""
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower())
    return slug.strip("_") or "scenario"


def open_in_browser(path: str):
    """Open a generated HTML file with the platform default browser."""
    try:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)
        else:
            subprocess.run(["xdg-open", path], check=True)
        print(f"  {GREEN}🌍 Opened in browser!{RESET}")
    except Exception:
        pass


def write_website_index(current_run_id: str = None, current_scenario_slug: str = None) -> str:
    """Write a stable index page that links to generated outputs."""
    os.makedirs(BUILD_DIR, exist_ok=True)
    index_path = os.path.join(BUILD_DIR, "index.html")

    def rel(path: str) -> str:
        return os.path.relpath(path, BUILD_DIR).replace(os.sep, "/")

    scenario_pages = []
    for filename in sorted(os.listdir(BUILD_DIR)):
        path = os.path.join(BUILD_DIR, filename)
        if not os.path.isfile(path):
            continue
        if not filename.endswith(".html") or filename in {"index.html", "latest.html"}:
            continue
        slug = filename[:-5]
        scenario_pages.append({
            "slug": slug,
            "href": filename,
            "mtime": os.path.getmtime(path),
            "current": slug == current_scenario_slug,
        })

    scenario_pages.sort(key=lambda item: item["mtime"], reverse=True)

    archived_runs = []
    runs_dir = os.path.join(BUILD_DIR, "runs")
    if os.path.isdir(runs_dir):
        for run_id in sorted(os.listdir(runs_dir), reverse=True):
            run_index = os.path.join(runs_dir, run_id, "index.html")
            if os.path.isfile(run_index):
                archived_runs.append({
                    "run_id": run_id,
                    "href": rel(run_index),
                    "current": run_id == current_run_id,
                })

    markdown_dirs = []
    for dirname in sorted(os.listdir(BUILD_DIR)):
        path = os.path.join(BUILD_DIR, dirname)
        if not os.path.isdir(path) or dirname == "runs":
            continue
        md_files = sorted(name for name in os.listdir(path) if name.endswith(".md"))
        if md_files:
            dir_index_path = os.path.join(path, "index.html")
            file_links = "\n".join(
                f'<li><a href="{html.escape(name)}">{html.escape(name)}</a></li>'
                for name in md_files
            )
            dir_title = html.escape(dirname)
            with open(dir_index_path, "w", encoding="utf-8") as f:
                f.write(f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{dir_title}</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #172033; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 40px 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    a {{ color: #1646a0; font-weight: 700; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    ul {{ list-style: none; padding: 0; display: grid; gap: 10px; }}
    li {{ background: #fff; border: 1px solid #dce3ee; border-radius: 8px; padding: 12px 14px; }}
    .back {{ display: inline-block; margin-bottom: 24px; color: #5d687a; }}
  </style>
</head>
<body>
  <main>
    <a class="back" href="../index.html">← 결과 홈</a>
    <h1>{dir_title}</h1>
    <p>{len(md_files)} Markdown files</p>
    <ul>{file_links}</ul>
  </main>
</body>
</html>
""")
            markdown_dirs.append({
                "name": dirname,
                "href": f"{dirname}/index.html",
                "count": len(md_files),
            })

    def page_link(item):
        marker = '<span class="badge">latest</span>' if item["current"] else ""
        label = html.escape(item["slug"].replace("_", " "))
        href = html.escape(item["href"])
        return f'<li><a href="{href}">{label}</a>{marker}</li>'

    def run_link(item):
        marker = '<span class="badge">new</span>' if item["current"] else ""
        href = html.escape(item["href"])
        run_id = html.escape(item["run_id"])
        return f'<li><a href="{href}">{run_id}</a>{marker}</li>'

    def markdown_item(item):
        name = html.escape(item["name"])
        href = html.escape(item["href"])
        return f'<li><a href="{href}">{name}</a><span class="muted">{item["count"]} markdown files</span></li>'

    scenario_html = "\n".join(page_link(item) for item in scenario_pages) or "<li class=\"empty\">아직 생성된 시나리오 페이지가 없습니다.</li>"
    run_html = "\n".join(run_link(item) for item in archived_runs[:40]) or "<li class=\"empty\">아직 archive run이 없습니다.</li>"
    markdown_html = "\n".join(markdown_item(item) for item in markdown_dirs) or "<li class=\"empty\">아직 저장된 Markdown 결과가 없습니다.</li>"

    latest_link = ""
    latest_path = os.path.join(BUILD_DIR, "latest.html")
    if os.path.isfile(latest_path):
        latest_link = '<a class="primary" href="latest.html">최근 실행 결과 열기</a>'

    generated = time.strftime("%Y-%m-%d %H:%M:%S")
    index_html = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gemma 4 Workshop Results</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #172033; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    h2 {{ margin: 0 0 16px; font-size: 18px; }}
    p {{ margin: 0; color: #5d687a; }}
    .top {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 28px; }}
    .primary {{ display: inline-block; padding: 10px 14px; border-radius: 6px; background: #1d4ed8; color: #fff; text-decoration: none; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    section {{ background: #fff; border: 1px solid #dce3ee; border-radius: 8px; padding: 18px; }}
    ul {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }}
    li {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding-bottom: 10px; border-bottom: 1px solid #edf1f7; }}
    li:last-child {{ border-bottom: 0; padding-bottom: 0; }}
    a {{ color: #1646a0; font-weight: 700; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .badge {{ flex: 0 0 auto; border-radius: 999px; padding: 3px 8px; background: #dbeafe; color: #1d4ed8; font-size: 11px; font-weight: 800; text-transform: uppercase; }}
    .muted, .empty {{ color: #778294; font-size: 13px; }}
    @media (max-width: 860px) {{ .grid {{ grid-template-columns: 1fr; }} .top {{ align-items: flex-start; flex-direction: column; }} }}
  </style>
</head>
<body>
  <main>
    <div class="top">
      <div>
        <h1>Gemma 4 Workshop Results</h1>
        <p>생성된 시나리오 결과, Markdown 산출물, 실행 archive를 한 곳에서 엽니다. Updated {html.escape(generated)}</p>
      </div>
      {latest_link}
    </div>
    <div class="grid">
      <section>
        <h2>시나리오별 최신 HTML</h2>
        <ul>{scenario_html}</ul>
      </section>
      <section>
        <h2>Markdown 산출물 폴더</h2>
        <ul>{markdown_html}</ul>
      </section>
      <section>
        <h2>최근 Archive Runs</h2>
        <ul>{run_html}</ul>
      </section>
    </div>
  </main>
</body>
</html>
"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    return index_path


def load_markdown_files(input_dir: str) -> list[dict]:
    """Load Markdown files from a generated output directory."""
    if not input_dir:
        return []

    source_dir = os.path.join(BUILD_DIR, input_dir)
    if not os.path.isdir(source_dir):
        return []

    docs = []
    for filename in sorted(os.listdir(source_dir)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(source_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            docs.append({
                "filename": filename,
                "path": path,
                "input_dir": input_dir,
                "text": f.read().strip(),
            })
    return docs


def load_input_markdown_files(scenario: dict) -> list[dict]:
    """Load source Markdown files for scenarios that review prior outputs."""
    return load_markdown_files(scenario.get("input_markdown_dir"))


_SHORT_STORY_REF_RE = re.compile(
    r"(?:short_stories/)?(?P<stem>\d{2}_short_story_[A-Za-z0-9_-]+)(?:\.md)?"
)


def extract_selected_section(text: str) -> str:
    """Return the Markdown body under the main selected-stories heading."""
    lines = text.splitlines()
    selected_lines = []
    in_section = False
    selected_level = 0

    for line in lines:
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip().strip("#").strip()
            normalized_title = re.sub(r"[*_`]", "", title)

            if in_section and level <= selected_level:
                break
            if normalized_title == "선정작" or normalized_title.startswith("선정작 "):
                in_section = True
                selected_level = level
                continue

        if in_section:
            selected_lines.append(line)

    return "\n".join(selected_lines).strip()


def extract_short_story_refs(text: str) -> list[str]:
    """Extract short-story file stems while preserving first-seen order."""
    refs = []
    seen = set()
    for match in _SHORT_STORY_REF_RE.finditer(text):
        stem = match.group("stem")
        if stem not in seen:
            refs.append(stem)
            seen.add(stem)
    return refs


def rank_selected_short_stories(
    selection_docs: list[dict],
    story_docs: list[dict],
    limit: int,
) -> list[dict]:
    """Rank unique selected story manuscripts from reviewer reports."""
    available_stories = {
        os.path.splitext(doc["filename"])[0]: doc
        for doc in story_docs
    }
    candidates = {}
    first_seen = 0

    for doc in selection_docs:
        section = extract_selected_section(doc["text"])
        refs = extract_short_story_refs(section or doc["text"])
        for rank, stem in enumerate(refs, start=1):
            if stem not in available_stories:
                continue
            if stem not in candidates:
                first_seen += 1
                candidates[stem] = {
                    "stem": stem,
                    "filename": available_stories[stem]["filename"],
                    "votes": 0,
                    "score": 0,
                    "best_rank": rank,
                    "first_seen": first_seen,
                }
            candidates[stem]["votes"] += 1
            candidates[stem]["score"] += max(1, limit - rank + 1)
            candidates[stem]["best_rank"] = min(candidates[stem]["best_rank"], rank)

    ranked = sorted(
        candidates.values(),
        key=lambda item: (
            -item["votes"],
            -item["score"],
            item["best_rank"],
            item["first_seen"],
            item["stem"],
        ),
    )
    return ranked[:limit]


def assign_story_revision_targets(
    agents: list[dict],
    source_docs: list[dict],
    story_docs: list[dict],
    limit: int,
) -> list[dict]:
    """Attach one unique selected short story to each revision agent."""
    assignments = rank_selected_short_stories(source_docs, story_docs, limit)
    assigned_agents = []

    for i, agent in enumerate(agents):
        assigned = dict(agent)
        if i < len(assignments):
            story = assignments[i]
            assigned["selected_story_id"] = story["stem"]
            assigned["selected_story_filename"] = story["filename"]
            assigned["selected_story_votes"] = story["votes"]
            assigned["selected_story_rank"] = i + 1
            assigned["filename"] = f"{i+1:02d}_revised_{story['stem']}.md"
        else:
            assigned["selected_story_id"] = "NO_SELECTED_STORY_FOUND"
            assigned["selected_story_filename"] = "NO_SELECTED_STORY_FOUND.md"
            assigned["selected_story_votes"] = 0
            assigned["selected_story_rank"] = i + 1
        assigned_agents.append(assigned)

    return assigned_agents


def build_direct_tasks(scenario: dict, topic: str) -> list[dict]:
    """Build one task per agent without asking the LLM to plan."""
    agents = scenario["agents"]
    source_docs = load_input_markdown_files(scenario)
    auxiliary_docs = {
        input_dir: load_markdown_files(input_dir)
        for input_dir in scenario.get("auxiliary_input_markdown_dirs", [])
    }

    if scenario.get("name") == "story_revision":
        agents = assign_story_revision_targets(
            agents,
            source_docs,
            auxiliary_docs.get("short_stories", []),
            scenario.get("select_count", len(agents)),
        )
        scenario["agents"] = agents

    aggregate_source = None
    if scenario.get("aggregate_input_markdown"):
        aggregate_docs = list(source_docs)
        for input_dir in scenario.get("auxiliary_input_markdown_dirs", []):
            aggregate_docs.extend(auxiliary_docs.get(input_dir, []))

        if aggregate_docs:
            combined = []
            for doc in aggregate_docs:
                combined.append(f"## {doc['input_dir']}/{doc['filename']}\n\n{doc['text']}")
            source_dirs = [scenario.get("input_markdown_dir", "inputs")]
            source_dirs.extend(scenario.get("auxiliary_input_markdown_dirs", []))
            aggregate_source = {
                "filename": f"{len(aggregate_docs)} files from {', '.join(source_dirs)}",
                "text": "\n\n---\n\n".join(combined),
            }
        else:
            aggregate_source = {
                "filename": "NO_INPUT_FILE_FOUND.md",
                "text": (
                    "No source Markdown files were found. Write a short Markdown error report "
                    "explaining which prior scenario must be run first."
                ),
            }
    tasks = []

    for i, agent in enumerate(agents):
        source = aggregate_source or (source_docs[i] if i < len(source_docs) else {
            "filename": "NO_INPUT_FILE_FOUND.md",
            "text": (
                "No source Markdown file was found. Write a short Markdown error report "
                "explaining which prior scenario must be run first."
            ),
        })
        instruction = agent.get("direct_instruction", "Work on: {topic}")
        instruction = (
            instruction
            .replace("{topic}", topic)
            .replace("{hire_count}", str(scenario.get("hire_count", 2)))
            .replace("{select_count}", str(scenario.get("select_count", 3)))
            .replace("{slot}", str(agent.get("slot", i + 1)))
            .replace("{selected_story_id}", str(agent.get("selected_story_id", "")))
            .replace("{selected_story_filename}", str(agent.get("selected_story_filename", "")))
            .replace("{selected_story_rank}", str(agent.get("selected_story_rank", i + 1)))
            .replace("{selected_story_votes}", str(agent.get("selected_story_votes", 0)))
            .replace("{source_filename}", source["filename"])
            .replace("{resume_text}", source["text"])
        )
        tasks.append({
            "name": agent["name"],
            "instruction": instruction,
            "filename": agent.get("filename", f"{agent['name']}.md"),
            "source_filename": source["filename"],
            "selected_story_filename": agent.get("selected_story_filename"),
        })

    write_metrics("orchestrator", "done", 0, 0.0, 0.0)
    return tasks


def clean_generated_dirs(scenario: dict):
    """Clean transient state and only the current scenario output folder."""
    os.makedirs(COMMS_DIR, exist_ok=True)
    for name in os.listdir(COMMS_DIR):
        path = os.path.join(COMMS_DIR, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    os.makedirs(BUILD_DIR, exist_ok=True)
    output_dir = scenario.get("markdown_dir") if scenario.get("save_markdown") else None
    if output_dir:
        path = os.path.join(BUILD_DIR, output_dir)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)


# ─── Step 1: Plan ───────────────────────────────────────────

def plan_tasks(api_url: str, scenario: dict, topic: str, reasoning: str = "off") -> list[dict]:
    """Use the LLM to generate specific instructions per agent."""
    agents = scenario["agents"]
    plan = scenario["plan"]

    print(f"\n{CYAN}{'━' * 60}{RESET}")
    print(f"{CYAN}  🧠 STEP 1: PLANNING{RESET}")
    print(f"{CYAN}{'━' * 60}{RESET}\n")

    if scenario.get("direct_plan"):
        tasks = build_direct_tasks(scenario, topic)
        print(f"{GREEN}✅ Direct plan: {len(tasks)} tasks{RESET}\n")
        for task in tasks:
            agent = next((a for a in agents if a["name"] == task["name"]), None)
            emoji = agent["emoji"] if agent else "❓"
            instr = task.get("instruction", "")[:50]
            source = task.get("selected_story_filename") or task.get("source_filename")
            source_note = f" from {source}" if source else ""
            print(f"  {emoji}  {BOLD}{task['name']}{RESET}{DIM}{source_note}: {instr}...{RESET}")
        print()
        return tasks

    agent_list = ", ".join(a["name"] for a in agents)
    user_prompt = plan["user"].replace("{topic}", topic).replace("{agent_list}", agent_list)

    print(f"{DIM}Generating agent instructions...{RESET}\n")
    plan_tokens = max(1024, len(agents) * 200)

    messages = [
        {"role": "system", "content": plan["system"]},
        {"role": "user", "content": user_prompt},
    ]
    raw = stream_llm(api_url, messages, agent_name="orchestrator",
                     color="1;36", max_tokens=plan_tokens, reasoning=reasoning)
    print("\n")

    # Extract JSON array (skip any reasoning preamble)
    start_idx = raw.find('[')
    end_idx = raw.rfind(']')

    if start_idx != -1 and end_idx != -1:
        json_str = raw[start_idx:end_idx + 1]
    else:
        json_str = raw

    try:
        tasks = json.loads(json_str)
        print(f"{GREEN}✅ Plan: {len(tasks)} tasks{RESET}\n")
        for t in tasks:
            name = t.get("name", "?")
            agent = next((a for a in agents if a["name"] == name), None)
            emoji = agent["emoji"] if agent else "❓"
            instr = t.get("instruction", "")[:50]
            print(f"  {emoji}  {BOLD}{name}{RESET} {DIM}{instr}...{RESET}")
        print()
        return tasks
    except json.JSONDecodeError:
        print(f"{YELLOW}⚠️  Parse failed — using fallback{RESET}\n")
        return [{"name": a["name"], "instruction": f"Work on: {topic}"} for a in agents]


# ─── Step 2: Dispatch ───────────────────────────────────────

def dispatch(tasks: list[dict], agents: list[dict], system_prompt: str = ""):
    """Write task files so specialist agents can pick them up."""
    print(f"{CYAN}{'━' * 60}{RESET}")
    print(f"{CYAN}  🚀 STEP 2: DISPATCHING{RESET}")
    print(f"{CYAN}{'━' * 60}{RESET}\n")

    task_id = f"task_{int(time.time())}"

    for task in tasks:
        name = task["name"]
        path = os.path.join(COMMS_DIR, f"task_{name}.json")
        with open(path, "w") as f:
            json.dump({
                "task_id": task_id,
                "instruction": task["instruction"],
                "system_prompt": system_prompt,
            }, f)

        agent = next((a for a in agents if a["name"] == name), None)
        emoji = agent["emoji"] if agent else "📦"
        print(f"  {emoji}  {name}")

    print(f"\n{GREEN}✅ {len(tasks)} tasks dispatched!{RESET}\n")


# ─── Step 3: Collect ────────────────────────────────────────

def collect(tasks: list[dict], agents: list[dict]) -> dict[str, str]:
    """Wait for all agents to write their result files."""
    print(f"{YELLOW}⏳ Waiting for agents...{RESET}\n")

    results = {}
    pending = {t["name"] for t in tasks}

    while pending:
        for name in list(pending):
            path = os.path.join(COMMS_DIR, f"result_{name}.json")
            if os.path.exists(path):
                time.sleep(0.1)
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                    os.remove(path)
                    results[name] = data.get("result", "")
                    pending.remove(name)
                    done = len(tasks) - len(pending)
                    print(f"  {GREEN}✅{RESET}  Agent {done}/{len(tasks)} done")
                except (json.JSONDecodeError, IOError):
                    pass
        if pending:
            time.sleep(POLL_INTERVAL)

    print(f"\n{GREEN}🎉 All agents finished!{RESET}\n")
    return results


# ─── Step 4: Assemble ───────────────────────────────────────

def assemble(scenario: dict, topic: str, results: dict, tasks: list = None):
    """Build the final HTML page from all agent results."""
    print(f"{CYAN}{'━' * 60}{RESET}")
    print(f"{CYAN}  🔧 STEP 3: ASSEMBLING{RESET}")
    print(f"{CYAN}{'━' * 60}{RESET}\n")

    from scenarios import build_page
    page_html = build_page(topic, scenario, results, tasks=tasks)

    os.makedirs(BUILD_DIR, exist_ok=True)
    scenario_slug = scenario.get("slug") or slugify(scenario.get("name", scenario.get("title", "scenario")))
    run_id = scenario.get("run_id") or f"{time.strftime('%Y%m%d-%H%M%S')}_{scenario_slug}"
    run_dir = os.path.join(BUILD_DIR, "runs", run_id)
    os.makedirs(run_dir, exist_ok=True)

    latest_path = os.path.join(BUILD_DIR, "latest.html")
    scenario_path = os.path.join(BUILD_DIR, f"{scenario_slug}.html")
    archive_path = os.path.join(run_dir, "index.html")

    for path in [latest_path, scenario_path, archive_path]:
        with open(path, "w", encoding="utf-8") as f:
            f.write(page_html)

    index_path = write_website_index(current_run_id=run_id, current_scenario_slug=scenario_slug)

    print(f"  {GREEN}✅ Assembled latest:{RESET} latest.html")
    print(f"  {GREEN}✅ Assembled scenario:{RESET} {scenario_slug}.html")
    print(f"  {GREEN}✅ Archived run:{RESET} runs/{run_id}/index.html")
    print(f"  {GREEN}✅ Updated result index:{RESET} index.html")

    open_in_browser(index_path)

    return index_path

def save_markdown_files(scenario: dict, results: dict, tasks: list = None):
    """Save each result as a Markdown file for scenarios that request it."""
    if not scenario.get("save_markdown"):
        return []

    out_dir = os.path.join(BUILD_DIR, scenario.get("markdown_dir", "markdown"))
    run_id = scenario.get("run_id")
    archive_dir = None
    if run_id:
        archive_dir = os.path.join(BUILD_DIR, "runs", run_id, scenario.get("markdown_dir", "markdown"))
        os.makedirs(archive_dir, exist_ok=True)

    os.makedirs(out_dir, exist_ok=True)

    task_map = {t.get("name"): t for t in tasks or []}
    saved_paths = []

    for idx, (name, content) in enumerate(results.items(), start=1):
        task = task_map.get(name, {})
        filename = task.get("filename") or f"{idx:02d}_{name}.md"
        filename = filename.replace("/", "_").replace("\\", "_")

        if not filename.endswith(".md"):
            filename += ".md"

        body = content.strip() + "\n"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        saved_paths.append(path)

        if archive_dir:
            archive_path = os.path.join(archive_dir, filename)
            with open(archive_path, "w", encoding="utf-8") as f:
                f.write(body)

    print(f"  {GREEN}✅ Saved Markdown files:{RESET} {out_dir}")
    if archive_dir:
        print(f"  {GREEN}✅ Archived Markdown files:{RESET} {archive_dir}")
    print(f"  {DIM}{len(saved_paths)} files written{RESET}\n")
    return saved_paths

# ─── Main ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="translate")
    parser.add_argument("--topic", default="Gemma is Google's most capable open AI model")
    parser.add_argument("--tasks", type=int, default=None,
                        help="Number of tasks/LLMs (default: scenario default)")
    parser.add_argument("--hires", type=int, default=2,
                        help="Number of candidates to hire for hiring_decision scenarios")
    parser.add_argument("--select", type=int, default=3,
                        help="Number of stories to select for story_review_selection scenarios")
    parser.add_argument("--api-url", default="http://127.0.0.1:8080/v1/chat/completions")
    parser.add_argument("--reasoning", choices=["on", "off"], default="off",
                        help="Enable or disable model thinking/reasoning controls")
    args = parser.parse_args()

    scenario = get_scenario(args.scenario, n_agents=args.tasks)
    scenario["name"] = args.scenario
    scenario["slug"] = slugify(args.scenario)
    scenario["run_id"] = f"{time.strftime('%Y%m%d-%H%M%S')}_{scenario['slug']}"
    scenario["hire_count"] = args.hires
    scenario["select_count"] = args.select
    agents = scenario["agents"]

    print(f"\n{CYAN}{'━' * 60}{RESET}")
    print(f"{CYAN}  🏗️  MULTI-AGENT ORCHESTRATOR{RESET}")
    print(f"{CYAN}{'━' * 60}{RESET}")
    print(f"\n{WHITE}  Scenario:{RESET} {args.scenario}")
    print(f"{WHITE}  Topic:{RESET} {args.topic}")
    print(f"{DIM}  {len(agents)} agents{RESET}\n")

    clean_generated_dirs(scenario)

    tasks = plan_tasks(args.api_url, scenario, args.topic, reasoning=args.reasoning)
    dispatch(tasks, agents, system_prompt=scenario.get("system_prompt", ""))
    results = collect(tasks, agents)
    save_markdown_files(scenario, results, tasks)
    assemble(scenario, args.topic, results, tasks=tasks)
    print(f"\n{CYAN}{'━' * 60}{RESET}")
    print(f"{CYAN}  ✅ COMPLETE{RESET}")
    print(f"{CYAN}{'━' * 60}{RESET}\n")

    input("Press Enter to close...")


if __name__ == "__main__":
    main()

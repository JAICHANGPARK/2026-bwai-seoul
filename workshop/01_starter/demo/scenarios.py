"""
Starter scenario definitions for the hands-on workshop.

01_starter intentionally contains only the translate scenario. During the
hands-on, participants add resume/interview/story scenarios to this file and
compare their result with 02_final/demo/scenarios.py.
"""

import html
import re
from pathlib import Path


_COLORS = [
    "1;35", "1;36", "1;33", "1;32", "1;34", "0;36", "0;35", "0;33", "0;32", "0;34",
    "1;31", "0;31", "1;37", "0;37", "1;35", "1;36", "1;33", "1;32", "1;34", "0;36",
]

# Agent metadata is deliberately simple dictionaries. run.sh/run.ps1 read this
# list before launching terminal windows, and orchestrator.py uses the same list
# to create per-agent tasks. Keeping the structure plain makes the workshop easy
# to inspect without learning a framework first.
_LANG_EMOJIS = [
    "🇫🇷", "🇪🇸", "🇩🇪", "🇯🇵", "🇨🇳", "🇰🇷", "🇸🇦", "🇮🇳", "🇧🇷", "🇷🇺",
    "🇮🇹", "🇹🇷", "🇻🇳", "🇹🇭", "🇳🇱", "🇵🇱", "🇸🇪", "🇬🇷", "🇮🇩", "🇺🇦",
]

_LANG_NAMES = [
    "french", "spanish", "german", "japanese", "chinese", "korean",
    "arabic", "hindi", "portuguese", "russian", "italian", "turkish",
    "vietnamese", "thai", "dutch", "polish", "swedish", "greek",
    "indonesian", "ukrainian",
]

_CODE_LANGS = [
    "python", "javascript", "dart", "typescript", "rust", "go", "java",
    "kotlin", "swift", "c", "ruby", "php", "scala", "haskell",
    "elixir", "lua", "perl", "r", "julia", "zig",
]

_CODE_EMOJIS = [
    "🐍", "📜", "🎯", "🔷", "🦀", "🐹", "☕",
    "🟣", "🍎", "⚙️", "💎", "🐘", "🔴", "λ",
    "💧", "🌙", "🐪", "📊", "🔮", "⚡",
]

_CODE_EXTENSIONS = {
    "python": "py",
    "javascript": "js",
    "rust": "rs",
    "go": "go",
    "c": "c",
    "java": "java",
    "ruby": "rb",
    "swift": "swift",
    "kotlin": "kt",
    "typescript": "ts",
    "php": "php",
    "scala": "scala",
    "haskell": "hs",
    "elixir": "ex",
    "lua": "lua",
    "perl": "pl",
    "r": "R",
    "julia": "jl",
    "dart": "dart",
    "zig": "zig",
}

_BUILD_DIR = Path(__file__).resolve().parent / "website_build"
_SHORT_STORY_REF_RE = re.compile(
    r"(?:short_stories/)?(?P<stem>\d{2}_short_story_[A-Za-z0-9_-]+)(?:\.md)?"
)


def _extract_selected_section(text: str) -> str:
    """Return only the body under the Markdown heading named 선정작."""
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


def _infer_selected_story_count(default: int) -> int:
    """Infer selected-story count from story_selections/*.md for later labs."""
    selection_dir = _BUILD_DIR / "story_selections"
    story_dir = _BUILD_DIR / "short_stories"
    if not selection_dir.is_dir():
        return default

    known_stems = set()
    if story_dir.is_dir():
        for path in story_dir.glob("*.md"):
            match = _SHORT_STORY_REF_RE.search(path.name)
            if match:
                known_stems.add(match.group("stem"))

    selected_stems = []
    seen = set()
    for path in sorted(selection_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        selected_section = _extract_selected_section(text)
        for match in _SHORT_STORY_REF_RE.finditer(selected_section or text):
            stem = match.group("stem")
            if known_stems and stem not in known_stems:
                continue
            if stem not in seen:
                selected_stems.append(stem)
                seen.add(stem)

    return len(selected_stems) or default


def make_translate_agents(n: int = 10) -> list[dict]:
    """Create one translation agent per target language.

    The important field is direct_instruction. orchestrator.py replaces {topic}
    with the CLI --topic value and sends the resulting instruction to the
    specialist process for this agent.
    """
    return [
        {
            "name": _LANG_NAMES[i % len(_LANG_NAMES)],
            "emoji": _LANG_EMOJIS[i % len(_LANG_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": f"Translate this into {_LANG_NAMES[i % len(_LANG_NAMES)]}: {{topic}}",
        }
        for i in range(n)
    ]


def make_code_agents(n: int = 10) -> list[dict]:
    """Create one code-writing agent per programming language."""
    agents = []
    for i in range(n):
        language = _CODE_LANGS[i % len(_CODE_LANGS)]
        extension = _CODE_EXTENSIONS.get(language, "txt")
        agents.append({
            "name": language,
            "emoji": _CODE_EMOJIS[i % len(_CODE_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"Write a solution for {{topic}} in {language}. "
                "Output ONLY code."
            ),
            "filename": f"{i+1:02d}_{language}.{extension}",
        })
    return agents


TRANSLATE_SYSTEM = (
    # System prompt = scenario-wide behavior contract.
    # It applies to every translation specialist and keeps outputs clean enough
    # for the HTML renderer to display without post-processing.
    "You are a precise translator. Output only the translated text, "
    "without commentary or markdown fences."
)

CODE_SYSTEM = (
    "You are a programmer. Output ONLY the code. "
    "No explanations, no markdown fences, no language labels. Raw code only."
)

TRANSLATE_PLAN = {
    # PLAN is kept in starter so participants can see the general architecture.
    # In many later scenarios we set direct_plan=True, so this planning prompt is
    # not called. It remains useful when you want the orchestrator LLM to create
    # agent-specific instructions dynamically.
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name" and "instruction". '
        "Use agent names exactly as provided. Output ONLY valid JSON."
    ),
    "user": (
        'Translate this into {n_agents} languages: "{topic}"\n'
        "Agents: {agent_list}\n"
        "Create one instruction per agent."
    ),
}

CODE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name" and "instruction". '
        "Keep each instruction to ONE sentence. Output ONLY valid JSON."
    ),
    "user": (
        'Task: "{topic}". Agents (each is a programming language): {agent_list}\n'
        'Each instruction: "Write [specific solution] in [language]". One sentence. That is all.'
    ),
}


# TODO Step 3~13:
# Paste scenario implementation snippets from workshop/03_labs/README.md here.
#
# Put these blocks in this section, above the card renderer functions and above
# SCENARIOS:
# - def make_xxx_agents(...): ...
# - XXX_SYSTEM = ...
# - XXX_PLAN = ...
# - Any extra renderer needed by the lab, for example novel_writing_card.
#
# Step 0~2 do not require pasting scenario code because translate and code are
# already included. Starting from Step 3, add each scenario's implementation
# block here in order:
# Step 3 resume
# Step 4 interview_review
# Step 5 hiring_decision
# Hiring extension marketer_resume, marketer_interview_review, marketer_hiring_decision
# Step 6 interview_dialogue and hiring_decision_from_dialogue
# Optional novel_writing
# Step 7 short_story_writing
# Step 8 story_review_selection
# Step 9 publication_offer_email
# Step 10 contract_negotiation
# Step 11 contract_draft
# Step 12 story_revision
# Step 13 marketing_copy
#
# Do NOT paste SCENARIOS["xxx"] registry entries here. Those go inside the
# SCENARIOS dict below.


def translate_card(agent, result, task=None):
    """Render one translation result inside a card on the generated HTML page."""
    name = agent["name"]
    emoji = agent["emoji"]
    text = result.strip().strip("`").strip()
    return (
        f'<div class="flex items-center gap-2 mb-3">\n'
        f'    <span class="text-xl">{emoji}</span>\n'
        f'    <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">{name}</span>\n'
        f'</div>\n'
        f'<div class="text-sm text-gray-700 leading-relaxed">{html.escape(text)}</div>'
    )


def code_card(agent, result, task=None):
    """Render one generated code snippet with syntax highlighting hooks."""
    name = agent["name"]
    emoji = agent.get("emoji", "💻")
    code = result.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)
    escaped = html.escape(code)
    lang_class = f"language-{name}" if name in _CODE_LANGS else ""
    return (
        f'<div class="flex items-center gap-2 px-1 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <span class="text-lg">{emoji}</span>\n'
        f'    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</span>\n'
        f'</div>\n'
        f'<pre class="m-0 text-xs leading-relaxed overflow-auto"><code class="{lang_class}" '
        f'style="padding: 0; background: transparent;">{escaped}</code></pre>'
    )


def strip_markdown_fence(text):
    """Remove ``` fences when a model wraps Markdown despite being asked not to."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def render_markdown(text):
    """Render simple generated Markdown into static HTML cards.

    This is intentionally a tiny renderer, not a full Markdown implementation.
    It supports only the structures generated in the workshop prompts: headings,
    bullet/numbered lists, bold text, inline code, and paragraphs. The limited
    scope keeps the dependency footprint small and makes the output predictable.
    """
    def inline(value):
        # Escape HTML first so model output cannot inject arbitrary tags, then
        # restore a small subset of Markdown inline formatting.
        escaped = html.escape(value)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        return escaped

    html_lines = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            close_lists()
            continue

        if line.startswith("# "):
            close_lists()
            html_lines.append(
                f'<h2 class="text-base font-bold text-gray-900 mb-3">{inline(line[2:])}</h2>'
            )
        elif line.startswith("## "):
            close_lists()
            html_lines.append(
                f'<h3 class="text-sm font-semibold text-gray-800 mt-5 mb-2">{inline(line[3:])}</h3>'
            )
        elif line.startswith("### "):
            close_lists()
            html_lines.append(
                f'<h4 class="text-xs font-semibold text-gray-700 mt-4 mb-2">{inline(line[4:])}</h4>'
            )
        elif line.startswith("- "):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append('<ul class="list-disc pl-5 space-y-1 text-xs leading-relaxed text-gray-700">')
                in_ul = True
            html_lines.append(f"<li>{inline(line[2:])}</li>")
        elif re.match(r"^\d+\.\s+", line):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append('<ol class="list-decimal pl-5 space-y-1 text-xs leading-relaxed text-gray-700">')
                in_ol = True
            html_lines.append(f"<li>{inline(re.sub(r'^\d+\.\s+', '', line))}</li>")
        else:
            close_lists()
            html_lines.append(
                f'<p class="text-xs leading-relaxed text-gray-700 mb-2">{inline(line)}</p>'
            )

    close_lists()
    return "\n".join(html_lines)


def markdown_card(agent, result, task=None, max_height="680px"):
    """Shared card renderer for Markdown-heavy scenarios.

    Later hands-on steps reuse this function through small wrappers such as
    resume_card and interview_review_card. The wrappers differ only by max
    height, which keeps scenario code focused on prompts rather than HTML.
    """
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    source_html = ""
    if source:
        source_html = f'<div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>'

    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        {source_html}\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[{max_height}] overflow-auto pr-1">{rendered}</div>'
    )


def resume_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="520px")


def interview_review_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="620px")


def interview_dialogue_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="720px")


def hiring_decision_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def short_story_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="760px")


def story_review_selection_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def story_revision_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="760px")


def publication_offer_email_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def contract_negotiation_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def contract_draft_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def publication_contract_card(agent, result, task=None):
    return contract_draft_card(agent, result, task)


def marketing_copy_card(agent, result, task=None):
    return markdown_card(agent, result, task, max_height="680px")


def build_page(topic, scenario, results, tasks=None):
    """Build the full HTML page from all agent results."""
    agents = scenario["agents"]
    title = scenario["title"]
    render_card = scenario["render_card"]
    extra_head = scenario.get("extra_head", "")
    extra_body = scenario.get("extra_body", "")

    task_map = {}
    if tasks:
        for task in tasks:
            task_map[task.get("name", "")] = task

    cards_html = []
    for agent in agents:
        result = results.get(agent["name"], "")
        task = task_map.get(agent["name"])
        inner = render_card(agent, result, task)
        cards_html.append(
            f'            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 '
            f'hover:shadow-md transition-all">\n'
            f'{inner}\n'
            f'            </div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
        svg {{ width: 100%; height: 100%; }}
    </style>
{extra_head}
</head>
<body class="bg-white text-gray-900 min-h-screen">
    <div class="mx-auto px-8 py-16" style="max-width: 1920px;">
        <h1 class="text-4xl font-bold text-center mb-2 text-gray-900">
            {html.escape(title)}
        </h1>
        <p class="text-center text-gray-500 text-base mb-12">{html.escape(topic)}</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
{chr(10).join(cards_html)}
        </div>
        <p class="text-center text-gray-400 text-xs mt-12 tracking-wide uppercase">
            Generated by {len(agents)} concurrent Gemma 4 instances
        </p>
    </div>
{extra_body}
</body>
</html>"""


SCENARIOS = {
    # Registry entry contract:
    # - make_agents: returns agent metadata
    # - plan: optional planning prompts
    # - system_prompt: common specialist system message
    # - render_card: HTML renderer for each result
    # - default_n: used when --tasks is omitted
    "translate": {
        "make_agents": make_translate_agents,
        "plan": TRANSLATE_PLAN,
        "system_prompt": TRANSLATE_SYSTEM,
        "render_card": translate_card,
        "title": "Translation Grid",
        "default_n": 10,
    },
    "code": {
        "make_agents": make_code_agents,
        "plan": CODE_PLAN,
        "system_prompt": CODE_SYSTEM,
        "render_card": code_card,
        "title": "Code Gallery",
        "extra_head": (
            '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">\n'
            '    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>'
        ),
        "extra_body": "    <script>hljs.highlightAll();</script>",
        "default_n": 10,
        "save_markdown": True,
        "markdown_dir": "code_outputs",
        "raw_output_files": True,
    },

    # TODO Step 3~13:
    # Paste each registry entry from workshop/03_labs/README.md here, inside
    # this dict, after the translate entry.
    #
    # Step 0~2 do not add registry entries because translate and code are
    # already registered. Starting from Step 3, add entries in the same order
    # as the lab guide:
    # resume, interview_review, hiring_decision,
    # marketer_resume, marketer_interview_review, marketer_hiring_decision,
    # interview_dialogue, hiring_decision_from_dialogue, optional novel_writing,
    # short_story_writing, story_review_selection, publication_offer_email,
    # contract_negotiation, contract_draft, story_revision, marketing_copy.
    #
    # Example shape:
    # "resume": {
    #     "make_agents": make_resume_agents,
    #     "plan": RESUME_PLAN,
    #     "system_prompt": RESUME_SYSTEM,
    #     "render_card": resume_card,
    #     "title": "Publishing Fiction Planner Resumes",
    #     "default_n": 10,
    #     "direct_plan": True,
    #     "save_markdown": True,
    #     "markdown_dir": "resumes",
    # },
    #
    # Keep the comma after each scenario entry.
}


def get_scenario(name: str, n_agents: int = None) -> dict:
    """Get a scenario by name and generate its agents.

    run.sh/run.ps1 call this function to know how many specialist windows to
    open. orchestrator.py calls it again to get the same scenario definition for
    planning, dispatch, and final rendering.
    """
    if name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise KeyError(f"Unknown scenario '{name}'. Available: {available}")
    scenario = dict(SCENARIOS[name])
    if n_agents is not None:
        n = n_agents
    elif scenario.get("default_n_from_selected_stories"):
        n = _infer_selected_story_count(scenario["default_n"])
    else:
        n = scenario["default_n"]
    scenario["agents"] = scenario["make_agents"](n)
    scenario["plan"] = {
        k: v.replace("{n_agents}", str(n)) if isinstance(v, str) else v
        for k, v in scenario["plan"].items()
    }
    return scenario

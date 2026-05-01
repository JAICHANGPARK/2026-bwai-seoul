"""
Starter scenario definitions for the hands-on workshop.

Copy this file to demo/scenarios.py when you want participants to start
from the minimal translate scenario and add new scenarios step by step.
"""

import html
import re


_COLORS = [
    "1;35", "1;36", "1;33", "1;32", "1;34", "0;36", "0;35", "0;33", "0;32", "0;34",
    "1;31", "0;31", "1;37", "0;37", "1;35", "1;36", "1;33", "1;32", "1;34", "0;36",
]

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


def make_translate_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": _LANG_NAMES[i % len(_LANG_NAMES)],
            "emoji": _LANG_EMOJIS[i % len(_LANG_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": f"Translate this into {_LANG_NAMES[i % len(_LANG_NAMES)]}: {{topic}}",
        }
        for i in range(n)
    ]


TRANSLATE_SYSTEM = (
    "You are a precise translator. Output only the translated text, "
    "without commentary or markdown fences."
)

TRANSLATE_PLAN = {
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


def translate_card(agent, result, task=None):
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


def strip_markdown_fence(text):
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def render_markdown(text):
    """Render simple generated Markdown into static HTML cards."""
    def inline(value):
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


SCENARIOS = {
    "translate": {
        "make_agents": make_translate_agents,
        "plan": TRANSLATE_PLAN,
        "system_prompt": TRANSLATE_SYSTEM,
        "render_card": translate_card,
        "title": "Translation Grid",
        "default_n": 10,
    },
}


def get_scenario(name: str, n_agents: int = None) -> dict:
    """Get a scenario by name. Generates agents dynamically."""
    if name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise KeyError(f"Unknown scenario '{name}'. Available: {available}")
    scenario = dict(SCENARIOS[name])
    n = n_agents or scenario["default_n"]
    scenario["agents"] = scenario["make_agents"](n)
    scenario["plan"] = {
        k: v.replace("{n_agents}", str(n)) if isinstance(v, str) else v
        for k, v in scenario["plan"].items()
    }
    return scenario

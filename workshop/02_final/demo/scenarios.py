"""
scenarios.py — Scenario definitions for the multi-agent demo.

Each scenario defines:
  - make_agents(n):   Returns a list of agent dicts
  - plan:             System + user prompts for orchestrator planning
  - system_prompt:    System prompt for specialist agents
  - render_card:      Function(agent, result) → inner HTML for one card
  - title:            Page title
  - default_n:        Default number of agents


─── Adding a New Scenario ──────────────────────────────────

1. Create a make_xxx_agents(n) function returning agent dicts
2. Define XXX_SYSTEM prompt for specialists
3. Define XXX_PLAN with "system" and "user" prompts
   (use {n_agents}, {topic}, {agent_list} placeholders)
4. Create xxx_card(agent, result) → inner HTML for one card
5. Register in SCENARIOS dict with title and render_card

Then run:  bash run.sh --scenario my_scenario --topic "My Topic"

핸즈온에서 가장 중요한 파일입니다. 새 workflow를 만들 때는 보통 아래 세
영역을 같이 추가합니다.

1. Agent factory: agent 이름, 색상, 파일명, 개별 direct_instruction 정의
2. System prompt: 모든 specialist에게 공통으로 들어가는 역할/출력 규칙
3. Scenario registry: orchestrator가 읽는 실행 설정
"""

import html
import re
from pathlib import Path


# ─── Palettes ───────────────────────────────────────────────

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

_SVG_STYLES = [
    "minimalist", "cyberpunk", "watercolor", "pixel art",
    "abstract", "geometric", "neon", "vintage",
    "pop art", "isometric", "steampunk", "monochrome",
    "low poly", "surreal", "line art", "flat design",
    "3D render", "anime", "cubism", "synthwave",
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
    """Infer selected-story count from story_selections/*.md for downstream stages."""
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






# ─── Agent Factories ───────────────────────────────────────
#
# Agent factory는 "몇 명의 specialist를 띄울지"와 "각 specialist가 어떤 일을
# 맡을지"를 정합니다. 각 dict의 핵심 필드는 아래와 같습니다.
#
# - name: task/result/metrics 파일명에 들어가는 고유 agent id
# - emoji/color: 터미널과 dashboard 표시용 metadata
# - direct_instruction: specialist에게 들어갈 user message template
# - filename: save_markdown=True일 때 저장될 Markdown 파일명

def make_translate_agents(n: int = 10) -> list[dict]:
    """Create one translation agent per language."""
    return [
        {
            "name": _LANG_NAMES[i % len(_LANG_NAMES)],
            "emoji": _LANG_EMOJIS[i % len(_LANG_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"Translate the following text into {_LANG_NAMES[i % len(_LANG_NAMES)]}. "
                "Output only the translated sentence. Preserve proper nouns such as model names "
                "and organization names, but translate all ordinary words.\n\nText: {topic}"
            ),
        }
        for i in range(n)
    ]


def make_svg_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"Agent {i+1}",
            "emoji": "🎨",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"Draw a simple SVG of a {{topic}}. "
                f"Use a {_SVG_STYLES[i % len(_SVG_STYLES)]} style. "
                f"Output SVG only and start with <svg"
            ),
        }
        for i in range(n)
    ]


def make_code_agents(n: int = 10) -> list[dict]:
    agents = []
    for i in range(n):
        language = _CODE_LANGS[i % len(_CODE_LANGS)]
        extension = _CODE_EXTENSIONS.get(language, "txt")
        agents.append({
            "name": language,
            "emoji": _CODE_EMOJIS[i % len(_CODE_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": f"Write a solution for {{topic}} in {language}. Output ONLY code.",
            "filename": f"{i+1:02d}_{language}.{extension}",
        })
    return agents


def make_ascii_agents(n: int = 10) -> list[dict]:
    return [
        {
            "name": f"Agent {i+1}",
            "emoji": "👾",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"Create ASCII art of {{topic}}. "
                f"Output ASCII art only."
            ),
        }
        for i in range(n)
    ]


def make_resume_agents(n: int = 10) -> list[dict]:
    """Create independent resume-writing agents.

    Step 0에서 LM Studio 앱에 직접 넣었던 이력서 프롬프트를 여러 agent용으로
    확장한 형태입니다. 각 agent가 같은 직무를 다루되 i 값을 이용해 서로 다른
    후보자 프로필을 만들도록 지시합니다.
    """
    return [
        {
            "name": f"resume_{i+1:02d}",
            "emoji": "📄",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Create one complete Korean Markdown resume for a fictional "
                "book publishing company fiction planning editor. Topic: {topic}. "
                f"This is resume #{i+1}; make the candidate profile, career path, "
                "publisher types, fiction genres, projects, achievements, and tools "
                "clearly different from the other resumes. Output Markdown only."
            ),
            "filename": f"{i+1:02d}_resume_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_interview_review_agents(n: int = 10) -> list[dict]:
    """Create agents that review one resume each.

    {source_filename}과 {resume_text}는 orchestrator.build_direct_tasks()가
    resumes/ 폴더의 Markdown 파일을 읽어서 채워 넣습니다.
    """
    return [
        {
            "name": f"interview_{i+1:02d}",
            "emoji": "🧑‍⚖️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Review the following resume as a senior interviewer for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Write one structured Korean Markdown interview review. "
                "Evaluate only evidence visible in the resume. If evidence is weak, say what must be verified in the interview."
            ),
            "filename": f"{i+1:02d}_interview_review_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_interview_dialogue_agents(n: int = 10) -> list[dict]:
    """Create agents that run real multi-turn interviews from resumes."""
    return [
        {
            "name": f"interview_dialogue_{i+1:02d}",
            "emoji": "🗣️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Run a realistic Korean multi-turn job interview for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Use this resume as the factual base. The execution engine will alternate interviewer question turns "
                "and candidate answer turns, then write a final interviewer evaluation. Ask evidence-based questions, "
                "use follow-up questions, and verify concerns raised by the resume."
            ),
            "filename": f"{i+1:02d}_interview_dialogue_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_hiring_decision_agents(n: int = 1) -> list[dict]:
    """Create final committee agents that read all interview reviews."""
    return [
        {
            "name": f"hiring_committee_{i+1:02d}",
            "emoji": "🏁",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "You are the final hiring committee for {topic}.\n"
                "Select exactly {hire_count} candidates from the interview reviews below.\n"
                "Input source: {source_filename}\n\n"
                "<interview_reviews>\n{resume_text}\n</interview_reviews>\n\n"
                "Write a final Korean Markdown hiring decision. Include treatment negotiation guidance for selected candidates."
            ),
            "filename": f"{i+1:02d}_hiring_decision.md",
        }
        for i in range(n)
    ]


def make_hiring_decision_from_dialogue_agents(n: int = 1) -> list[dict]:
    """Create final committee agents that judge from dialogue transcripts."""
    return [
        {
            "name": f"hiring_committee_dialogue_{i+1:02d}",
            "emoji": "🏁",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "You are the final hiring committee for {topic}.\n"
                "Select exactly {hire_count} candidates from the interview dialogue transcripts below.\n"
                "Input source: {source_filename}\n\n"
                "<interview_dialogues>\n{resume_text}\n</interview_dialogues>\n\n"
                "Write a final Korean Markdown hiring decision. Use the Q&A evidence, interviewer notes, "
                "role fit, risk signals, and compensation negotiation responses."
            ),
            "filename": f"{i+1:02d}_hiring_decision_from_dialogue.md",
        }
        for i in range(n)
    ]


def make_marketer_resume_agents(n: int = 10) -> list[dict]:
    """Create independent resume-writing agents for publishing marketers."""
    return [
        {
            "name": f"marketer_resume_{i+1:02d}",
            "emoji": "📈",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Create one complete Korean Markdown resume for a fictional "
                "book publishing company marketer. Topic: {topic}. "
                f"This is marketer resume #{i+1}; make the candidate's channel focus, "
                "campaign history, reader/community strategy, launch performance, "
                "analytics tools, and collaboration style clearly different from the other resumes. "
                "Output Markdown only."
            ),
            "filename": f"{i+1:02d}_marketer_resume_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_marketer_interview_review_agents(n: int = 10) -> list[dict]:
    """Create agents that review one marketer resume each."""
    return [
        {
            "name": f"marketer_interview_{i+1:02d}",
            "emoji": "🧑‍💼",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Review the following marketer resume as a senior publishing marketing lead for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Write one structured Korean Markdown interview review. "
                "Evaluate evidence about book launch strategy, target readers, paid/owned/earned channels, "
                "copywriting, campaign analytics, author collaboration, and sales coordination. "
                "If evidence is weak, say what must be verified in the interview."
            ),
            "filename": f"{i+1:02d}_marketer_interview_review_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_marketer_hiring_decision_agents(n: int = 1) -> list[dict]:
    """Create final committee agents for publishing marketer hiring."""
    return [
        {
            "name": f"marketer_hiring_committee_{i+1:02d}",
            "emoji": "🏁",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "You are the final hiring committee for {topic}.\n"
                "Select exactly {hire_count} marketers from the interview reviews below.\n"
                "Input source: {source_filename}\n\n"
                "<marketer_interview_reviews>\n{resume_text}\n</marketer_interview_reviews>\n\n"
                "Write a final Korean Markdown marketer hiring decision. "
                "Prioritize candidates who can create launch positioning, bookstore copy, SNS/newsletter campaigns, "
                "press angles, reader targeting, and measurable campaign plans for fiction publishing."
            ),
            "filename": f"{i+1:02d}_marketer_hiring_decision.md",
        }
        for i in range(n)
    ]


def make_novel_writing_agents(n: int = 10) -> list[dict]:
    roles = [
        ("concept", "소설 기획서와 핵심 독자 타깃을 작성"),
        ("world", "세계관, 배경, 출판 포지셔닝을 설계"),
        ("characters", "주요 인물과 관계도를 설계"),
        ("plot", "3막 구조와 회차별/장별 플롯을 작성"),
        ("chapter_01", "1장 원고를 실제 소설 문체로 작성"),
        ("chapter_02", "2장 원고를 실제 소설 문체로 작성"),
        ("chapter_03", "3장 원고를 실제 소설 문체로 작성"),
        ("editorial", "편집자 관점의 수정 방향과 리스크를 작성"),
        ("copy", "책 소개, 띠지 문구, 온라인 서점 상세 카피를 작성"),
        ("series", "후속권/시리즈 확장안과 IP 전개안을 작성"),
    ]
    agents = []
    for i in range(n):
        slug, role = roles[i % len(roles)]
        agents.append({
            "name": f"novel_{i+1:02d}_{slug}",
            "emoji": "✍️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"Topic: {{topic}}\n"
                f"Role: {role}.\n"
                "Create a polished Korean Markdown document. "
                "If writing prose, write in a publishable fiction style with scene, dialogue, sensory detail, and narrative tension. "
                "Do not summarize instead of writing the requested material."
            ),
            "filename": f"{i+1:02d}_{slug}.md",
        })
    return agents


def make_short_story_writing_agents(n: int = 10) -> list[dict]:
    """Create short-story writer agents with different genre lanes."""
    genres = [
        ("literary", "문학성이 강한 현실 단편"),
        ("mystery", "도시 미스터리 단편"),
        ("romance", "잔잔한 로맨스 단편"),
        ("sf", "근미래 SF 단편"),
        ("fantasy", "현대 판타지 단편"),
        ("thriller", "심리 스릴러 단편"),
        ("historical", "근현대사 배경 단편"),
        ("young_adult", "청소년/성장 단편"),
        ("horror", "서늘한 호러 단편"),
        ("humor", "블랙코미디 단편"),
    ]
    agents = []
    for i in range(n):
        slug, genre = genres[i % len(genres)]
        agents.append({
            "name": f"short_story_{i+1:02d}_{slug}",
            "emoji": "🖋️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are fiction writer #{i+1}. Write one complete Korean short story for this call: {{topic}}.\n"
                f"Assigned lane: {genre}.\n"
                "Output a polished Markdown manuscript with title, author pen name, short logline, and the full story. "
                "The story must have a complete beginning, development, turn, and ending. "
                "Use fictional pen names and do not copy existing works."
            ),
            "filename": f"{i+1:02d}_short_story_{slug}.md",
        })
    return agents


def make_story_review_selection_agents(n: int = 3) -> list[dict]:
    """Create editorial review agents with different evaluation perspectives."""
    perspectives = [
        ("editorial", "문학성과 완성도 중심 편집자"),
        ("market", "독자성, 판매 가능성, 포지셔닝 중심 편집자"),
        ("series", "작가 성장성, IP 확장성, 출간 리스크 중심 편집자"),
    ]
    agents = []
    for i in range(n):
        slug, perspective = perspectives[i % len(perspectives)]
        agents.append({
            "name": f"story_editor_{i+1:02d}_{slug}",
            "emoji": "📚",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are editor #{i+1}, a {perspective}.\n"
                "Review all submitted short stories for the publication theme: {topic} as part of the hired editorial team.\n"
                "Use the editor hiring decision below as editorial-board context when it is available.\n"
                "Select exactly {select_count} stories for publication consideration.\n"
                "When listing selected stories, include each exact source Markdown filename.\n"
                "Input source: {source_filename}\n\n"
                "<short_stories_and_editorial_team_context>\n{resume_text}\n</short_stories_and_editorial_team_context>\n\n"
                "Write a Korean Markdown editorial review and selection report."
            ),
            "filename": f"{i+1:02d}_story_selection_{slug}.md",
        })
    return agents


def make_story_revision_agents(n: int = 3) -> list[dict]:
    """Create revision agents for selected stories.

    selected_story_* placeholders are filled by orchestrator.py after it parses
    story_selections/*.md. This avoids multiple agents revising the same story.
    """
    return [
        {
            "name": f"story_revision_{i+1:02d}",
            "emoji": "✍️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean fiction editor rewriting selected short story assignment #{i+1}.\n"
                "Use the editorial selection reports, original short-story manuscripts, contract draft context, and editor hiring decision below.\n"
                "Assigned selected story: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Revise only the assigned story above. Do not choose or rewrite any other story, "
                "even if other selected stories appear in the review reports.\n"
                "Locate the matching original manuscript and revise the story based on the review notes, "
                "editorial strengths, hired editor team context, risks, and requested changes that apply to this assigned story.\n"
                "Input source: {source_filename}\n\n"
                "<review_results_original_stories_contract_and_editor_context>\n{resume_text}\n</review_results_original_stories_contract_and_editor_context>\n\n"
                "Output one revised Korean Markdown manuscript only. "
                "If the assigned story or matching source story cannot be identified, "
                "write a short Korean Markdown internal note explaining what is missing."
            ),
            "filename": f"{i+1:02d}_revised_story.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]


def make_publication_offer_email_agents(n: int = 3) -> list[dict]:
    """Create agents that draft initial publication-intent emails."""
    return [
        {
            "name": f"offer_email_{i+1:02d}",
            "emoji": "✉️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are an acquisitions editor writing publication offer email #{i+1}.\n"
                "Use the story selection results, original manuscripts, and editor hiring decision below.\n"
                "Assigned selected story: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Draft an initial publication-intent email for the assigned selected story only, using the hired editorial team's rationale as context.\n"
                "If the assigned story does not exist, write a brief internal note saying there is no selected story for this task.\n"
                "Input source: {source_filename}\n\n"
                "<selection_results_original_stories_and_editor_context>\n{resume_text}\n</selection_results_original_stories_and_editor_context>\n\n"
                "Output one Korean Markdown email draft only, including subject, recipient placeholder, opening, selected-work rationale, intent-to-publish note, contract-discussion agenda, schedule, and closing."
            ),
            "filename": f"{i+1:02d}_publication_offer_email.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]


def make_contract_negotiation_agents(n: int = 3) -> list[dict]:
    """Create agents that simulate contract-term negotiation notes."""
    return [
        {
            "name": f"contract_negotiation_{i+1:02d}",
            "emoji": "🤝",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing rights editor preparing contract negotiation memo #{i+1}.\n"
                "Use the publication offer emails, selection reports, original manuscripts, and editor hiring decision below.\n"
                "Assigned selected story: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Prepare negotiation notes for the assigned selected story only, reflecting the hired editorial team's priorities.\n"
                "This is a fictional workshop artifact, not legal advice and not a binding contract.\n"
                "Input source: {source_filename}\n\n"
                "<offer_selection_story_and_editor_context>\n{resume_text}\n</offer_selection_story_and_editor_context>\n\n"
                "Output one Korean Markdown negotiation memo only, covering proposed rights scope, manuscript delivery, revision expectations, schedule, compensation placeholders, risk points, author questions, publisher concessions, and next actions."
            ),
            "filename": f"{i+1:02d}_contract_negotiation.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]


def make_contract_draft_agents(n: int = 3) -> list[dict]:
    """Create agents that draft non-binding publication contract drafts."""
    return [
        {
            "name": f"contract_draft_{i+1:02d}",
            "emoji": "📑",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing operations editor preparing publication contract draft #{i+1}.\n"
                "Use the negotiation memo, publication offer, selection materials, and editor hiring decision below.\n"
                "Assigned selected story: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Prepare a non-binding publication contract draft for the assigned selected story only, keeping the hired editorial team's publication priorities visible.\n"
                "This is a fictional workshop artifact, not legal advice, not a substitute for lawyer review, and not a binding legal contract.\n"
                "Input source: {source_filename}\n\n"
                "<negotiation_offer_selection_and_editor_context>\n{resume_text}\n</negotiation_offer_selection_and_editor_context>\n\n"
                "Output one Korean Markdown contract draft only, including draft clauses, term sheet, required author materials, internal approval notes, signature workflow, and open legal-review items."
            ),
            "filename": f"{i+1:02d}_contract_draft.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]


def make_marketing_copy_agents(n: int = 10) -> list[dict]:
    """Create agents that write launch marketing copy for revised stories."""
    channels = [
        ("bookstore", "online bookstore detail page and search snippets"),
        ("social", "short social media launch posts"),
        ("press", "press release and newsletter copy"),
    ]
    agents = []
    for i in range(n):
        slug, channel = channels[i % len(channels)]
        agents.append({
            "name": f"marketing_copy_{i+1:02d}_{slug}",
            "emoji": "📣",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean publishing marketer writing launch copy package #{i+1} for {channel}.\n"
                "Use the revised stories, contract drafts, selection notes, and marketer hiring decisions below.\n"
                "Assigned revised/selected story material: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Write copy for the assigned story only, using the hired marketer team's strengths as the marketing lens. "
                "If the assigned story cannot be identified, write a brief internal note.\n"
                "Input source: {source_filename}\n\n"
                "<publication_materials>\n{resume_text}\n</publication_materials>\n\n"
                "Output one Korean Markdown marketing copy package only, including positioning, target readers, one-line hook, short synopsis, bookstore copy, SNS posts, newsletter blurb, press headline, and caution notes."
            ),
            "filename": f"{i+1:02d}_marketing_copy_{slug}.md",
            "slot": str(i + 1),
            "variant_slug": slug,
        })
    return agents





# ─── System Prompts ─────────────────────────────────────────
#
# System prompt는 specialist에게 공통으로 들어가는 "역할과 출력 규칙"입니다.
# direct_instruction이 개별 작업이라면, *_SYSTEM은 전체 시나리오의 품질 기준입니다.
# 예: Markdown만 출력, 실제 개인정보 금지, 구조화된 섹션 유지.

TRANSLATE_SYSTEM = (
    "You are a translator. Output ONLY the translated text. "
    "No explanations, no preamble, no original text, no quotes. Preserve proper "
    "nouns, but translate all ordinary words into the requested target language."
)

SVG_SYSTEM = (
    "You are an SVG artist. Output ONLY a raw <svg> tag with viewBox='0 0 120 120'. "
    "Use vibrant colors. No explanations, no markdown, no text before or after the SVG."
)

CODE_SYSTEM = (
    "You are a programmer. Output ONLY the code. "
    "No explanations, no markdown fences, no language labels. Raw code only."
)

ASCII_SYSTEM = (
    "You are an ASCII artist. Output ONLY raw ASCII art. "
    "No explanations, no markdown fences, no text before or after the art."
)

RESUME_SYSTEM = """
You are a senior Korean resume writer for publishing and content industry roles.
Create one realistic but fully fictional resume for a book publishing company fiction planning editor.

Output ONLY Markdown.
Do not include explanations or markdown fences.
Do not use real personal data, real phone numbers, real emails, or real company-confidential facts.
Use fictional names, fictional employers, fictional projects, and fictional metrics.
Make the resume specific to fiction acquisition, editorial planning, manuscript development, and book publishing, not a generic IT product planner.

Required structure:
# [Fictional Korean Name] - 도서 출판사 소설 기획편집자 이력서
## 프로필
## 핵심 역량
## 경력
## 주요 기획 프로젝트
## 성과 지표
## 사용 도구
## 학력 및 자격
## 포트폴리오 요약
""".strip()

INTERVIEW_REVIEW_SYSTEM = """
You are a senior interviewer and hiring committee reviewer for Korean book publishing companies.
You are reviewing candidates for fiction planning editor roles: manuscript editing, novel acquisition, IP development, and editorial planning.

Output ONLY Markdown.
Do not include explanations outside the review.
Do not invent facts not present in the resume.
When a claim needs verification, state the interview question that would verify it.
Use a realistic, strict interviewer tone.
For treatment negotiation, make fictional but plausible recommendations based only on resume seniority and role fit.

Required structure:
# [Candidate or Source File] - 면접관 리뷰
## 한줄 평가
## 직무 적합도
## 강점 근거
## 우려점 및 검증 리스크
## 면접 질문 7개
## 꼬리 질문
## 처우협의 포인트
## 예상 연봉/직급 제안
## 평가 루브릭
## 채용 추천
""".strip()


INTERVIEW_DIALOGUE_SYSTEM = """
You are a senior Korean publishing-company interviewer evaluating fiction planning editor candidates.
You are conducting a real multi-turn interview: one interviewer question, one candidate answer, repeated across turns.

Output ONLY Markdown.
Do not include explanations outside the transcript.
Use the resume as the factual base.
The candidate may give plausible elaborations only if they are consistent with the resume.
Do not invent new major achievements, employers, awards, or confidential facts not supported by the resume.
When a candidate answer needs verification, add an interviewer note.
Include a short compensation negotiation conversation near the end.

Required structure:
# [Candidate or Source File] - 면접 대화록
## 면접 설정
## 질의응답 대화
### Turn 1
**면접관:**
**지원자:**
## 면접관 최종 평가
""".strip()


HIRING_DECISION_SYSTEM = """
You are a final hiring committee for a Korean book publishing company.
You must choose a fixed number of candidates from the provided interview reviews.

Output ONLY Markdown.
Select exactly the requested number of hires.
Use only the evidence in the interview reviews.
When scores are close, explain the tie-breaker.
Include treatment negotiation guidance, but keep it fictional and scenario-based.

Required structure:
# 최종 채용 의사결정
## 선발 인원
## 최종 합격자
## 예비 합격자
## 탈락자 요약
## 비교 평가표
## 처우협의 전략
## 오퍼 리스크
## 최종 결론
""".strip()


HIRING_DECISION_FROM_DIALOGUE_SYSTEM = """
You are a final hiring committee for a Korean book publishing company.
You must choose a fixed number of candidates from interview dialogue transcripts.

Output ONLY Markdown.
Select exactly the requested number of hires.
Use only evidence from the Q&A transcripts, interviewer notes, and compensation negotiation sections.
When a candidate answer is plausible but weakly verified, treat it as a risk.
When scores are close, explain the tie-breaker.
Include treatment negotiation guidance, but keep it fictional and scenario-based.

Required structure:
# 최종 채용 의사결정 - 면접 대화 기반
## 선발 인원
## 최종 합격자
## 예비 합격자
## 탈락자 요약
## 질의응답 근거 비교표
## 처우협의 전략
## 오퍼 리스크
## 최종 결론
""".strip()

MARKETER_RESUME_SYSTEM = """
You are a senior Korean resume writer for publishing and media marketing roles.
Create one realistic but fully fictional resume for a book publishing company marketer.

Output ONLY Markdown.
Do not include explanations or markdown fences.
Do not use real personal data, real phone numbers, real emails, or real company-confidential facts.
Use fictional names, fictional employers, fictional campaigns, and fictional metrics.
Make the resume specific to book publishing marketing, fiction launches, reader communities, and sales-channel coordination.

Required structure:
# [Fictional Korean Name] - 도서 출판사 북 마케터 이력서
## 프로필
## 핵심 역량
## 경력
## 주요 마케팅 캠페인
## 성과 지표
## 사용 도구
## 학력 및 자격
## 포트폴리오 요약
""".strip()

MARKETER_INTERVIEW_REVIEW_SYSTEM = """
You are a senior publishing marketing lead and hiring committee reviewer.
You are reviewing candidates for book marketing, fiction launch campaigns, reader targeting, channel strategy, and sales enablement roles.

Output ONLY Markdown.
Do not include explanations outside the review.
Do not invent facts not present in the resume.
When a claim needs verification, state the interview question that would verify it.
Use a realistic, strict marketing lead tone.
For treatment negotiation, make fictional but plausible recommendations based only on resume seniority and role fit.

Required structure:
# [Candidate or Source File] - 북 마케터 면접 리뷰
## 한줄 평가
## 직무 적합도
## 강점 근거
## 우려점 및 검증 리스크
## 면접 질문 7개
## 캠페인 과제 제안
## 처우협의 포인트
## 예상 연봉/직급 제안
## 평가 루브릭
## 채용 추천
""".strip()

MARKETER_HIRING_DECISION_SYSTEM = """
You are a final hiring committee for a Korean book publishing company.
You must choose a fixed number of book marketers from the provided interview reviews.

Output ONLY Markdown.
Select exactly the requested number of hires.
Use only the evidence in the marketer interview reviews.
When scores are close, explain the tie-breaker.
Prefer candidates who can support fiction launch positioning, bookstore detail pages, SNS/newsletter campaigns, press angles, reader acquisition, and measurable marketing plans.
Include treatment negotiation guidance, but keep it fictional and scenario-based.

Required structure:
# 북 마케터 최종 채용 의사결정
## 선발 인원
## 최종 합격자
## 예비 합격자
## 탈락자 요약
## 비교 평가표
## 캠페인 역량 비교
## 처우협의 전략
## 오퍼 리스크
## 최종 결론
""".strip()

NOVEL_WRITING_SYSTEM = """
You are a professional Korean fiction writer and publishing editor.
Create polished Markdown for a publishable novel development package.

Output ONLY Markdown.
Do not include explanations outside the requested document.
When asked to write prose, write actual fiction scenes, not a summary.
Keep the style literary but commercially readable for Korean book publishing.
""".strip()


SHORT_STORY_WRITING_SYSTEM = """
You are a professional Korean short-story writer.
Write original, complete, publishable short fiction.

Output ONLY Markdown.
Do not include explanations outside the manuscript.
Do not copy existing works, real living authors' style, or copyrighted characters.
Use fictional author names and fictional story content.

Required structure:
# [작품 제목]
## 작가명
## 로그라인
## 원고
""".strip()

STORY_REVIEW_SELECTION_SYSTEM = """
You are a senior Korean publishing editor reviewing short-story submissions.
You must review all submitted stories and select a fixed number for publication consideration.

Output ONLY Markdown.
Select exactly the requested number of stories.
Use only the submitted story texts as evidence for story quality.
Use the final editor hiring decision as editorial-board context when it is available.
For every selected story, include the exact source Markdown filename from the input.
Be clear about editorial strengths, market fit, revision needs, and publication risk.

Required structure:
# 단편소설 심사 및 선정 보고서
## 심사 기준
## 전체 후보작 요약
## 선정작
## 예비 선정작
## 탈락작 주요 사유
## 작품별 편집 메모
## 출간 가능성 및 리스크
## 최종 추천
""".strip()

STORY_REVISION_SYSTEM = """
You are a senior Korean fiction editor and revision writer.
You revise selected short stories using editorial review reports, original manuscripts, agreed publication context, and hired editorial-team context.

Output ONLY Markdown.
Revise the actual story text, not just a summary or plan.
Preserve the core premise and authorial identity of the original manuscript unless the review explicitly requires a change.
Apply concrete editorial feedback about structure, characterization, pacing, scene clarity, tone, market fit, and ending.
Use the final editor hiring decision as editorial-team context when it is available.
Use contract draft context only as publication constraints; do not write legal terms into the manuscript.
Do not copy existing works, real living authors' style, or copyrighted characters.
If the selected story or original manuscript cannot be identified, output a short internal note instead.

Required structure:
# [개정 작품 제목]
## 개정 대상
## 반영한 리뷰 요약
## 개정 방향
## 작가명
## 로그라인
## 개정 원고
## 변경 메모
""".strip()

PUBLICATION_OFFER_EMAIL_SYSTEM = """
You are a Korean publishing editor drafting professional publication offer emails to selected short-story authors.

Output ONLY Markdown.
Draft email text only. Do not claim the email was actually sent.
Keep terms fictional and use placeholders for personal/contact details.
Use the final editor hiring decision as editorial-team context when it is available.
Make the offer warm, specific to the selected work, and clear that contract terms still need discussion.

Required structure:
# 출간 제안 안내 메일
## 제목
## 수신자
## 본문
## 계약 협의 안내
## 후속 일정
## 내부 메모
""".strip()


CONTRACT_NEGOTIATION_SYSTEM = """
You are a Korean publishing rights editor preparing a contract-term negotiation memo.

Output ONLY Markdown.
This is a fictional workshop artifact, not legal advice and not a binding contract.
Use placeholders for money, dates, addresses, personal information, and legal entity details.
Use the final editor hiring decision as editorial-team context when it is available.
Keep the memo close to a real publishing workflow: rights scope, compensation, manuscript delivery, revision, approval, schedule, and unresolved negotiation points.

Required structure:
# 계약 조건 협의 메모
## 협의 대상 작품
## 출간 제안 요약
## 주요 계약 조건 초안
## 쟁점 및 협상 포인트
## 작가에게 확인할 질문
## 출판사 내부 검토 사항
## 다음 액션
## 비고
""".strip()


CONTRACT_DRAFT_SYSTEM = """
You are a Korean publishing operations editor preparing a non-binding publication contract draft.

Output ONLY Markdown.
This is a fictional workshop artifact, not legal advice, not a substitute for lawyer review, and not a binding legal contract.
Do not invent real personal information, real bank details, real registration numbers, or real legal entity data.
Use the final editor hiring decision as editorial-team context when it is available.
Focus on a readable contract draft that an editorial team can pass to legal review before signing.

Required structure:
# 출간 계약서 초안
## 계약 대상 작품
## 조건 합의 요약
## 계약 주요 조항 초안
## 특약 및 검토 필요 조항
## 작가 제출 필요 자료
## 출판사 내부 승인 메모
## 서명 및 보관 절차
## 법무 검토 필요 항목
## 다음 액션
""".strip()


MARKETING_COPY_SYSTEM = """
You are a Korean publishing marketer creating launch copy for selected and revised short stories.

Output ONLY Markdown.
Use the revised manuscript and editorial context as evidence.
Use the hired marketer decision as marketing team context when it is available.
Do not claim awards, bestseller status, media quotes, or author facts that are not present in the source material.
Write commercially useful copy that can support bookstore detail pages, SNS, newsletter, and press outreach.

Required structure:
# 출간 마케팅 문구 패키지
## 작품 포지셔닝
## 타깃 독자
## 한 줄 훅
## 짧은 소개문
## 온라인 서점 문구
## SNS 문구
## 뉴스레터 문구
## 보도자료 헤드라인
## 사용 시 주의사항
""".strip()





# ─── Planning Prompts ───────────────────────────────────────
#
# 이 데모의 완성 시나리오들은 대부분 direct_plan=True를 사용하므로 runtime에서는
# PLAN을 호출하지 않습니다. 그래도 남겨두는 이유는 다음과 같습니다.
# - direct_plan=False로 바꾸면 orchestrator LLM이 agent별 작업 JSON을 생성할 수 있음
# - system instruction / user message 분리 예시를 보여줄 수 있음
# - 사용자가 LM Studio에서 "시나리오 코드 생성" 프롬프트를 만들 때 참고 가능

TRANSLATE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name" and "instruction". '
        "Keep each instruction to ONE sentence. Output ONLY valid JSON."
    ),
    "user": (
        'Translate this into {n_agents} languages: "{topic}"\n'
        "Agents: {agent_list}\n"
        'Each instruction: "Translate into [language]: [text]". That is all.'
    ),
}

SVG_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", "instruction", and "label". '
        'The "label" is a short 2-4 word title for the SVG (e.g. "A Cat"). '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Theme: "{topic}". Agents: {agent_list}\n'
        'Each instruction: "Draw a simple SVG of [specific thing].". '
        "One sentence max. Do NOT mention size or format."
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

ASCII_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", "instruction", and "label". '
        'The "label" is a one word description of the ASCII art (e.g. "Cat"). '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Theme: "{topic}". Agents (each is an ASCII artist): {agent_list}\n'
        'Each instruction: "Create realistic and small ASCII (max 20x60 characters) art of [specific aspect of the theme - one word description only]". '
        "One sentence. That is all. "
    ),
}

RESUME_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} different fictional Korean Markdown resumes for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each instruction should ask for one complete resume for a book publishing "
        "company fiction planning editor, with differentiated seniority, genre focus, "
        "publisher type, projects, and achievements."
    ),
}

INTERVIEW_REVIEW_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} interviewer review tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reviews one generated resume from the resumes folder."
    ),
}


INTERVIEW_DIALOGUE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} interview dialogue simulation tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads one generated resume and runs a real multi-turn interviewer-candidate Q&A."
    ),
}


HIRING_DECISION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create final hiring committee decision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads all interview reviews and selects the required number of hires."
    ),
}


HIRING_DECISION_FROM_DIALOGUE_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create final hiring committee decision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads all interview dialogue transcripts and selects the required number of hires."
    ),
}

MARKETER_RESUME_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} different fictional Korean Markdown resumes for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each instruction should ask for one complete resume for a book publishing marketer, "
        "with differentiated seniority, channel focus, campaign type, reader segment, tools, and achievements."
    ),
}


MARKETER_INTERVIEW_REVIEW_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} marketer interview review tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reviews one generated marketer resume from the marketer_resumes folder."
    ),
}


MARKETER_HIRING_DECISION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create final marketer hiring committee decision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reads all marketer interview reviews and selects the required number of hires."
    ),
}

NOVEL_WRITING_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} novel writing tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Tasks should divide planning, prose writing, editorial review, and publishing copy."
    ),
}


SHORT_STORY_WRITING_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} short-story writing tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task should produce one complete, distinct short story."
    ),
}

STORY_REVIEW_SELECTION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} editorial review tasks for short stories about "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task reviews all short stories and selects the requested number."
    ),
}

STORY_REVISION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} short-story revision tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task uses editorial selection reports and original short stories to revise one selected manuscript."
    ),
}

PUBLICATION_OFFER_EMAIL_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} publication offer email drafting tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task drafts one offer email from selected story reports."
    ),
}


CONTRACT_NEGOTIATION_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} contract negotiation memo tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task prepares one fictional, non-binding publishing contract negotiation memo."
    ),
}


CONTRACT_DRAFT_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} publication contract draft tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task prepares one fictional, non-binding publication contract draft."
    ),
}


MARKETING_COPY_PLAN = {
    "system": (
        'Output a JSON array with {n_agents} objects. Each has "name", '
        '"instruction", and "filename". Use agent names exactly as provided. '
        "Output ONLY valid JSON."
    ),
    "user": (
        'Create {n_agents} marketing copy package tasks for "{topic}".\n'
        "Agents: {agent_list}\n"
        "Each task writes launch copy for one selected and revised short story."
    ),
}





# ─── Card Renderers ─────────────────────────────────────────
#
# specialist 결과는 Markdown/string이고, build_page()는 render_card 함수를 호출해
# 각 결과를 HTML card 내부로 변환합니다. 시나리오를 추가할 때 새 renderer가
# 꼭 필요한 것은 아니며, Markdown 중심 결과라면 render_markdown 기반 card를
# 재사용하는 편이 가장 단순합니다.
# Each render_card(agent, result) returns ONLY the inner HTML.
# The card wrapper (div, border, hover, padding) is handled by build_page().

def translate_card(agent, result, task=None):
    name = agent["name"]
    emoji = agent["emoji"]
    text = result.strip().strip("`").strip()
    return (
        f'<div class="flex items-center gap-2 mb-3">\n'
        f'    <span class="text-xl">{emoji}</span>\n'
        f'    <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">{name}</span>\n'
        f'</div>\n'
        f'<div class="text-sm text-gray-700 leading-relaxed">{text}</div>'
    )


def svg_card(agent, result, task=None):
    name = agent["name"]
    label = task.get("label", name.title()) if task else name.title()
    svg = result
    if "<svg" in svg:
        start = svg.index("<svg")
        end = svg.index("</svg>") + 6 if "</svg>" in svg else len(svg)
        svg = svg[start:end]
    else:
        svg = '<div class="text-sm text-gray-400 p-4 text-center">Failed to generate SVG</div>'
    return (
        f'<div class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">{name}</div>\n'
        f'<div class="w-full aspect-square flex items-center justify-center p-2">{svg}</div>\n'
        f'<div class="text-sm font-semibold text-gray-500 mt-3 pt-3 border-t border-gray-200 w-full text-center">{label}</div>'
    )


def code_card(agent, result, task=None):
    name = agent["name"]
    emoji = agent.get("emoji", "💻")
    code = result.strip()
    # Strip markdown fences if present
    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)
    escaped = html.escape(code)
    lang_class = f'language-{name}' if name in _CODE_LANGS else ''
    return (
        f'<div class="flex items-center gap-2 px-1 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <span class="text-lg">{emoji}</span>\n'
        f'    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</span>\n'
        f'</div>\n'
        f'<pre class="m-0 text-xs leading-relaxed overflow-auto"><code class="{lang_class}" style="padding: 0; background: transparent;">{escaped}</code></pre>'
    )


def ascii_card(agent, result, task=None):
    name = agent["name"]
    label = task.get("label", name.title()) if task else name.title()
    art = result
    if art.startswith("```"):
        lines = art.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        art = "\n".join(lines)
    art = art.strip("\n")
    escaped = html.escape(art)
    return (
        f'<div class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">{name}</div>\n'
        f'<div class="w-full bg-gray-900 rounded-lg p-4 flex items-center justify-center min-h-[180px] overflow-auto">\n'
        f'    <pre class="text-base font-mono text-green-400 leading-tight" style="text-shadow: 0 0 5px rgba(74, 222, 128, 0.5);">{escaped}</pre>\n'
        f'</div>\n'
        f'<div class="text-sm font-semibold text-gray-500 mt-3 pt-3 border-t border-gray-200 w-full text-center">{label}</div>'
    )


def strip_markdown_fence(text):
    """Remove code fences if a model wraps Markdown despite the prompt."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def render_markdown(text):
    """Render the simple Markdown emitted by agents into static HTML.

    전체 Markdown parser를 쓰지 않고, 워크샵 산출물에 필요한 subset만 지원합니다.
    이렇게 하면 의존성이 줄고 모델 출력이 약간 흔들려도 화면이 안정적으로 나옵니다.
    """
    def inline(value):
        # HTML escape를 먼저 적용해 모델 출력이 임의 HTML을 주입하지 못하게 한 뒤,
        # 굵게/inline code 정도만 다시 살립니다.
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


def resume_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    resume_html = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-center justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</span>\n'
        f'    <span class="text-xs text-gray-400">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[520px] overflow-auto pr-1">{resume_html}</div>'
    )


def interview_review_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    review_html = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[620px] overflow-auto pr-1">{review_html}</div>'
    )


def interview_dialogue_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[720px] overflow-auto pr-1">{rendered}</div>'
    )


def hiring_decision_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[680px] overflow-auto pr-1">{rendered}</div>'
    )


def novel_writing_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-center justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</span>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[680px] overflow-auto pr-1">{rendered}</div>'
    )


def short_story_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-center justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</span>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[760px] overflow-auto pr-1">{rendered}</div>'
    )


def story_review_selection_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[680px] overflow-auto pr-1">{rendered}</div>'
    )


def story_revision_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[760px] overflow-auto pr-1">{rendered}</div>'
    )


def publication_offer_email_card(agent, result, task=None):
    name = agent["name"]
    filename = task.get("filename", f"{name}.md") if task else f"{name}.md"
    source = task.get("source_filename", "") if task else ""
    rendered = render_markdown(strip_markdown_fence(result))
    return (
        f'<div class="flex items-start justify-between gap-3 pb-3 mb-3 border-b border-gray-200">\n'
        f'    <div>\n'
        f'        <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{name}</div>\n'
        f'        <div class="text-xs text-gray-400 mt-1">source: {html.escape(source)}</div>\n'
        f'    </div>\n'
        f'    <span class="text-xs text-gray-400 text-right">{filename}</span>\n'
        f'</div>\n'
        f'<div class="max-h-[680px] overflow-auto pr-1">{rendered}</div>'
    )


def contract_negotiation_card(agent, result, task=None):
    """Render contract negotiation memos with the same Markdown card shell."""
    return publication_offer_email_card(agent, result, task)


def contract_draft_card(agent, result, task=None):
    """Render contract drafts with the same Markdown card shell."""
    return publication_offer_email_card(agent, result, task)


def publication_contract_card(agent, result, task=None):
    """Backward-compatible renderer name for older lab snippets."""
    return contract_draft_card(agent, result, task)


def marketing_copy_card(agent, result, task=None):
    """Render marketing copy packages with the same Markdown card shell."""
    return publication_offer_email_card(agent, result, task)





# ─── Page Builder ───────────────────────────────────────────

def build_page(topic, scenario, results, tasks=None):
    """Build the full HTML page. Wraps each card automatically."""
    agents = scenario["agents"]
    title = scenario["title"]
    render_card = scenario["render_card"]
    extra_head = scenario.get("extra_head", "")
    extra_body = scenario.get("extra_body", "")

    cols = min((len(agents) + 1) // 2, 5)

    # Build a lookup from agent name → task dict
    task_map = {}
    if tasks:
        for t in tasks:
            task_map[t.get("name", "")] = t

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
    <title>{title}</title>
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
            {title}
        </h1>
        <p class="text-center text-gray-500 text-base mb-12">{topic}</p>
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


# ─── Scenario Registry ──────────────────────────────────────
#
# orchestrator.py는 이 SCENARIOS dict만 보고 실행 방식을 결정합니다.
#
# 주요 필드:
# - direct_plan: True이면 make_agents의 direct_instruction을 그대로 사용
# - save_markdown: True이면 결과를 markdown_dir에 저장해 다음 단계 입력으로 사용
# - input_markdown_dir: 이전 단계 산출물 폴더를 1:1 또는 aggregate로 읽음
# - aggregate_input_markdown: 여러 Markdown 파일을 하나의 큰 입력으로 합침
# - auxiliary_input_markdown_dirs: 주 입력 외에 참고할 추가 산출물 폴더
# - preserve_build_dirs: 현재 실행에서 지우지 말아야 할 이전 산출물 폴더

SCENARIOS = {
    "translate": {
        "make_agents": make_translate_agents,
        "plan": TRANSLATE_PLAN,
        "system_prompt": TRANSLATE_SYSTEM,
        "render_card": translate_card,
        "title": "Translation Grid",
        "default_n": 10,
        "direct_plan": True,
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
        "direct_plan": True,
        "save_markdown": True,
        "markdown_dir": "code_outputs",
        "raw_output_files": True,
    },
    "resume": {
        "make_agents": make_resume_agents,
        "plan": RESUME_PLAN,
        "system_prompt": RESUME_SYSTEM,
        "render_card": resume_card,
        "title": "Publishing Fiction Planning Editor Resumes",
        "default_n": 10,
        "direct_plan": True,
        "save_markdown": True,
        "markdown_dir": "resumes",
    },
    "interview_review": {
        "make_agents": make_interview_review_agents,
        "plan": INTERVIEW_REVIEW_PLAN,
        "system_prompt": INTERVIEW_REVIEW_SYSTEM,
        "render_card": interview_review_card,
        "title": "Interview Reviews",
        "default_n": 10,
        "direct_plan": True,
        "input_markdown_dir": "resumes",
        "save_markdown": True,
        "markdown_dir": "interview_reviews",
        "preserve_build_dirs": ["resumes"],
    },
    "interview_dialogue": {
        "make_agents": make_interview_dialogue_agents,
        "plan": INTERVIEW_DIALOGUE_PLAN,
        "system_prompt": INTERVIEW_DIALOGUE_SYSTEM,
        "render_card": interview_dialogue_card,
        "title": "Interview Dialogues",
        "default_n": 10,
        "direct_plan": True,
        "execution_mode": "interview_multiturn",
        "interview_turns": 4,
        "input_markdown_dir": "resumes",
        "save_markdown": True,
        "markdown_dir": "interview_dialogues",
        "preserve_build_dirs": ["resumes"],
    },
    "hiring_decision": {
        "make_agents": make_hiring_decision_agents,
        "plan": HIRING_DECISION_PLAN,
        "system_prompt": HIRING_DECISION_SYSTEM,
        "render_card": hiring_decision_card,
        "title": "Hiring Decision",
        "default_n": 1,
        "direct_plan": True,
        "input_markdown_dir": "interview_reviews",
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "hiring_decisions",
        "preserve_build_dirs": ["resumes", "interview_reviews"],
    },
    "hiring_decision_from_dialogue": {
        "make_agents": make_hiring_decision_from_dialogue_agents,
        "plan": HIRING_DECISION_FROM_DIALOGUE_PLAN,
        "system_prompt": HIRING_DECISION_FROM_DIALOGUE_SYSTEM,
        "render_card": hiring_decision_card,
        "title": "Hiring Decision From Dialogue",
        "default_n": 1,
        "direct_plan": True,
        "input_markdown_dir": "interview_dialogues",
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "hiring_decisions_from_dialogue",
        "preserve_build_dirs": ["resumes", "interview_dialogues"],
    },
    "marketer_resume": {
        "make_agents": make_marketer_resume_agents,
        "plan": MARKETER_RESUME_PLAN,
        "system_prompt": MARKETER_RESUME_SYSTEM,
        "render_card": resume_card,
        "title": "Publishing Marketer Resumes",
        "default_n": 10,
        "direct_plan": True,
        "save_markdown": True,
        "markdown_dir": "marketer_resumes",
        "preserve_build_dirs": ["resumes", "interview_reviews", "hiring_decisions"],
    },
    "marketer_interview_review": {
        "make_agents": make_marketer_interview_review_agents,
        "plan": MARKETER_INTERVIEW_REVIEW_PLAN,
        "system_prompt": MARKETER_INTERVIEW_REVIEW_SYSTEM,
        "render_card": interview_review_card,
        "title": "Publishing Marketer Interview Reviews",
        "default_n": 10,
        "direct_plan": True,
        "input_markdown_dir": "marketer_resumes",
        "save_markdown": True,
        "markdown_dir": "marketer_interview_reviews",
        "preserve_build_dirs": ["resumes", "interview_reviews", "hiring_decisions", "marketer_resumes"],
    },
    "marketer_hiring_decision": {
        "make_agents": make_marketer_hiring_decision_agents,
        "plan": MARKETER_HIRING_DECISION_PLAN,
        "system_prompt": MARKETER_HIRING_DECISION_SYSTEM,
        "render_card": hiring_decision_card,
        "title": "Publishing Marketer Hiring Decision",
        "default_n": 1,
        "direct_plan": True,
        "input_markdown_dir": "marketer_interview_reviews",
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "marketer_hiring_decisions",
        "preserve_build_dirs": [
            "resumes",
            "interview_reviews",
            "hiring_decisions",
            "marketer_resumes",
            "marketer_interview_reviews",
        ],
    },
    "novel_writing": {
        "make_agents": make_novel_writing_agents,
        "plan": NOVEL_WRITING_PLAN,
        "system_prompt": NOVEL_WRITING_SYSTEM,
        "render_card": novel_writing_card,
        "title": "Novel Writing Studio",
        "default_n": 10,
        "direct_plan": True,
        "save_markdown": True,
        "markdown_dir": "novel_outputs",
        "preserve_build_dirs": ["resumes", "interview_reviews", "hiring_decisions"],
    },
    "short_story_writing": {
        "make_agents": make_short_story_writing_agents,
        "plan": SHORT_STORY_WRITING_PLAN,
        "system_prompt": SHORT_STORY_WRITING_SYSTEM,
        "render_card": short_story_card,
        "title": "Short Story Submissions",
        "default_n": 10,
        "direct_plan": True,
        "save_markdown": True,
        "markdown_dir": "short_stories",
        "preserve_build_dirs": ["resumes", "interview_reviews", "hiring_decisions", "novel_outputs"],
    },
    "story_review_selection": {
        "make_agents": make_story_review_selection_agents,
        "plan": STORY_REVIEW_SELECTION_PLAN,
        "system_prompt": STORY_REVIEW_SELECTION_SYSTEM,
        "render_card": story_review_selection_card,
        "title": "Short Story Review Selection",
        "default_n": 3,
        "direct_plan": True,
        "input_markdown_dir": "short_stories",
        "auxiliary_input_markdown_dirs": ["hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "story_selections",
        "preserve_build_dirs": ["hiring_decisions", "short_stories"],
    },
    "publication_offer_email": {
        "make_agents": make_publication_offer_email_agents,
        "plan": PUBLICATION_OFFER_EMAIL_PLAN,
        "system_prompt": PUBLICATION_OFFER_EMAIL_SYSTEM,
        "render_card": publication_offer_email_card,
        "title": "Publication Offer Emails",
        "default_n": 3,
        "default_n_from_selected_stories": True,
        "selected_story_targeting": "unique",
        "selected_story_selection_dir": "story_selections",
        "selected_story_story_dir": "short_stories",
        "direct_plan": True,
        "input_markdown_dir": "story_selections",
        "auxiliary_input_markdown_dirs": ["short_stories", "hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "publication_offer_emails",
        "preserve_build_dirs": ["hiring_decisions", "short_stories", "story_selections"],
    },
    "contract_negotiation": {
        "make_agents": make_contract_negotiation_agents,
        "plan": CONTRACT_NEGOTIATION_PLAN,
        "system_prompt": CONTRACT_NEGOTIATION_SYSTEM,
        "render_card": contract_negotiation_card,
        "title": "Contract Negotiation Memos",
        "default_n": 3,
        "default_n_from_selected_stories": True,
        "selected_story_targeting": "unique",
        "selected_story_selection_dir": "story_selections",
        "selected_story_story_dir": "short_stories",
        "direct_plan": True,
        "input_markdown_dir": "publication_offer_emails",
        "auxiliary_input_markdown_dirs": ["story_selections", "short_stories", "hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "contract_negotiations",
        "preserve_build_dirs": ["hiring_decisions", "short_stories", "story_selections", "publication_offer_emails"],
    },
    "contract_draft": {
        "make_agents": make_contract_draft_agents,
        "plan": CONTRACT_DRAFT_PLAN,
        "system_prompt": CONTRACT_DRAFT_SYSTEM,
        "render_card": contract_draft_card,
        "title": "Contract Draft Writing",
        "default_n": 3,
        "default_n_from_selected_stories": True,
        "selected_story_targeting": "unique",
        "selected_story_selection_dir": "story_selections",
        "selected_story_story_dir": "short_stories",
        "direct_plan": True,
        "input_markdown_dir": "contract_negotiations",
        "auxiliary_input_markdown_dirs": ["publication_offer_emails", "story_selections", "hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "contract_drafts",
        "preserve_build_dirs": ["hiring_decisions", "short_stories", "story_selections", "publication_offer_emails", "contract_negotiations"],
    },
    "story_revision": {
        "make_agents": make_story_revision_agents,
        "plan": STORY_REVISION_PLAN,
        "system_prompt": STORY_REVISION_SYSTEM,
        "render_card": story_revision_card,
        "title": "Short Story Revisions",
        "default_n": 3,
        "default_n_from_selected_stories": True,
        "selected_story_targeting": "unique",
        "selected_story_selection_dir": "story_selections",
        "selected_story_story_dir": "short_stories",
        "selected_story_filename_mode": "revision",
        "direct_plan": True,
        "input_markdown_dir": "story_selections",
        "auxiliary_input_markdown_dirs": ["short_stories", "contract_drafts", "hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "revised_stories",
        "preserve_build_dirs": [
            "hiring_decisions",
            "short_stories",
            "story_selections",
            "publication_offer_emails",
            "contract_negotiations",
            "contract_drafts",
        ],
    },
    "marketing_copy": {
        "make_agents": make_marketing_copy_agents,
        "plan": MARKETING_COPY_PLAN,
        "system_prompt": MARKETING_COPY_SYSTEM,
        "render_card": marketing_copy_card,
        "title": "Publication Marketing Copy",
        "default_n": 10,
        "selected_story_targeting": "cycle",
        "selected_story_selection_dir": "story_selections",
        "selected_story_story_dir": "revised_stories",
        "selected_story_filename_mode": "marketing",
        "direct_plan": True,
        "input_markdown_dir": "revised_stories",
        "auxiliary_input_markdown_dirs": ["contract_drafts", "story_selections", "marketer_hiring_decisions"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "marketing_copy",
        "preserve_build_dirs": [
            "short_stories",
            "story_selections",
            "publication_offer_emails",
            "contract_negotiations",
            "contract_drafts",
            "revised_stories",
            "marketer_hiring_decisions",
        ],
    },

}


SCENARIO_ALIASES = {
    # Older workshop drafts used publication_contract. Keep it working while the
    # participant-facing name moves to the clearer contract_draft.
    "publication_contract": "contract_draft",
}


def get_scenario(name: str, n_agents: int = None) -> dict:
    """Get a scenario by name and generate its agents.

    run.sh/run.ps1은 이 함수를 호출해 agent 목록을 알아낸 뒤 창을 띄우고,
    orchestrator.py는 같은 함수를 호출해 task 생성과 HTML rendering에 사용합니다.
    """
    name = SCENARIO_ALIASES.get(name, name)
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

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
"""

import html
import re


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
    "python", "javascript", "rust", "go", "c", "java", "ruby", "swift",
    "kotlin", "typescript", "php", "scala", "haskell", "elixir",
    "lua", "perl", "r", "julia", "dart", "zig",
]

_CODE_EMOJIS = [
    "🐍", "📜", "🦀", "🐹", "⚙️", "☕", "💎", "🍎",
    "🟣", "🔷", "🐘", "🔴", "λ", "💧",
    "🌙", "🐪", "📊", "🔮", "🎯", "⚡",
]






# ─── Agent Factories ───────────────────────────────────────

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
    return [
        {
            "name": _CODE_LANGS[i % len(_CODE_LANGS)],
            "emoji": _CODE_EMOJIS[i % len(_CODE_EMOJIS)],
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": f"Write a solution for {{topic}} in {_CODE_LANGS[i % len(_CODE_LANGS)]}. Output ONLY code.",
        }
        for i in range(n)
    ]


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
    return [
        {
            "name": f"resume_{i+1:02d}",
            "emoji": "📄",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Create one complete Korean Markdown resume for a fictional "
                "book publishing company fiction planner. Topic: {topic}. "
                f"This is resume #{i+1}; make the candidate profile, career path, "
                "publisher types, fiction genres, projects, achievements, and tools "
                "clearly different from the other resumes. Output Markdown only."
            ),
            "filename": f"{i+1:02d}_resume_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_interview_review_agents(n: int = 10) -> list[dict]:
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
    return [
        {
            "name": f"interview_dialogue_{i+1:02d}",
            "emoji": "🗣️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                "Simulate a realistic Korean job interview dialogue for {topic}.\n"
                "Source resume file: {source_filename}\n\n"
                "<resume>\n{resume_text}\n</resume>\n\n"
                "Write a multi-turn Markdown transcript between a senior interviewer and the candidate. "
                "Include evidence-based questions, follow-up questions, candidate answers, interviewer notes, "
                "and a compensation negotiation section. The candidate may elaborate plausible context only when "
                "it is consistent with the resume; mark anything that needs verification."
            ),
            "filename": f"{i+1:02d}_interview_dialogue_{i+1:02d}.md",
        }
        for i in range(n)
    ]


def make_hiring_decision_agents(n: int = 1) -> list[dict]:
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
                "Review all submitted short stories for the publication theme: {topic}.\n"
                "Select exactly {select_count} stories for publication consideration.\n"
                "Input source: {source_filename}\n\n"
                "<short_stories>\n{resume_text}\n</short_stories>\n\n"
                "Write a Korean Markdown editorial review and selection report."
            ),
            "filename": f"{i+1:02d}_story_selection_{slug}.md",
        })
    return agents


def make_story_revision_agents(n: int = 3) -> list[dict]:
    return [
        {
            "name": f"story_revision_{i+1:02d}",
            "emoji": "✍️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are a Korean fiction editor rewriting selected short story assignment #{i+1}.\n"
                "Use the editorial selection reports and original short-story manuscripts below.\n"
                "Assigned selected story: {selected_story_filename}\n"
                "Selection rank: {selected_story_rank}; selected-list mentions: {selected_story_votes}\n"
                "Revise only the assigned story above. Do not choose or rewrite any other story, "
                "even if other selected stories appear in the review reports.\n"
                "Locate the matching original manuscript and revise the story based on the review notes, "
                "editorial strengths, risks, and requested changes that apply to this assigned story.\n"
                "Input source: {source_filename}\n\n"
                "<review_results_and_original_stories>\n{resume_text}\n</review_results_and_original_stories>\n\n"
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
    return [
        {
            "name": f"offer_email_{i+1:02d}",
            "emoji": "✉️",
            "color": _COLORS[i % len(_COLORS)],
            "direct_instruction": (
                f"You are an acquisitions editor writing publication offer email #{i+1}.\n"
                "Use the story selection results and any revised stories below. Draft an offer email for selected story slot #{slot}.\n"
                "If that slot does not exist, write a brief internal note saying there is no selected story for this slot.\n"
                "Input source: {source_filename}\n\n"
                "<selection_results_and_revised_stories>\n{resume_text}\n</selection_results_and_revised_stories>\n\n"
                "Output one Korean Markdown email draft only, including subject, recipient placeholder, opening, offer details, revision request, schedule, treatment/royalty discussion placeholder, and closing."
            ),
            "filename": f"{i+1:02d}_publication_offer_email.md",
            "slot": str(i + 1),
        }
        for i in range(n)
    ]





# ─── System Prompts ─────────────────────────────────────────

TRANSLATE_SYSTEM = (
    "You are a translator. Output ONLY the translated text. "
    "No explanations, no preamble, no original text, no quotes."
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
Create one realistic but fully fictional resume for a book publishing company fiction planner.

Output ONLY Markdown.
Do not include explanations or markdown fences.
Do not use real personal data, real phone numbers, real emails, or real company-confidential facts.
Use fictional names, fictional employers, fictional projects, and fictional metrics.
Make the resume specific to fiction/book publishing planning, not a generic IT product planner.

Required structure:
# [Fictional Korean Name] - 도서 출판사 소설 기획자 이력서
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
You are reviewing candidates for fiction planning, novel acquisition, IP development, and editorial planning roles.

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
You are a senior Korean publishing-company interviewer and a realistic fictional candidate simulator.
You are conducting interviews for fiction planning, novel acquisition, IP development, and editorial planning roles.

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
## 핵심 검증 포인트
## 질의응답 대화
### Q1. [질문 제목]
**면접관:**
**지원자:**
**면접관 꼬리질문:**
**지원자 추가 답변:**
**면접관 메모:**
## 처우협의 대화
## 면접관 최종 평가
## 추가 검증 필요 사항
## 채용 추천
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
Use only the submitted story texts as evidence.
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
You revise selected short stories using editorial review reports and original manuscripts.

Output ONLY Markdown.
Revise the actual story text, not just a summary or plan.
Preserve the core premise and authorial identity of the original manuscript unless the review explicitly requires a change.
Apply concrete editorial feedback about structure, characterization, pacing, scene clarity, tone, market fit, and ending.
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
Make the offer warm, specific to the selected work, and clear about next steps.

Required structure:
# 출간 제안 안내 메일
## 제목
## 수신자
## 본문
## 후속 일정
## 내부 메모
""".strip()





# ─── Planning Prompts ───────────────────────────────────────

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
        "company fiction planner, with differentiated seniority, genre focus, "
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
        "Each task reads one generated resume and writes a multi-turn interviewer-candidate Q&A transcript."
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





# ─── Card Renderers ─────────────────────────────────────────
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
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def render_markdown(text):
    """Render the simple Markdown emitted by resume agents into static HTML."""
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

SCENARIOS = {
    "translate": {
        "make_agents": make_translate_agents,
        "plan": TRANSLATE_PLAN,
        "system_prompt": TRANSLATE_SYSTEM,
        "render_card": translate_card,
        "title": "Translation Grid",
        "default_n": 10,
    },
    "resume": {
        "make_agents": make_resume_agents,
        "plan": RESUME_PLAN,
        "system_prompt": RESUME_SYSTEM,
        "render_card": resume_card,
        "title": "Publishing Fiction Planner Resumes",
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
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "story_selections",
        "preserve_build_dirs": ["short_stories"],
    },
    "story_revision": {
        "make_agents": make_story_revision_agents,
        "plan": STORY_REVISION_PLAN,
        "system_prompt": STORY_REVISION_SYSTEM,
        "render_card": story_revision_card,
        "title": "Short Story Revisions",
        "default_n": 3,
        "direct_plan": True,
        "input_markdown_dir": "story_selections",
        "auxiliary_input_markdown_dirs": ["short_stories"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "revised_stories",
        "preserve_build_dirs": ["short_stories", "story_selections"],
    },
    "publication_offer_email": {
        "make_agents": make_publication_offer_email_agents,
        "plan": PUBLICATION_OFFER_EMAIL_PLAN,
        "system_prompt": PUBLICATION_OFFER_EMAIL_SYSTEM,
        "render_card": publication_offer_email_card,
        "title": "Publication Offer Emails",
        "default_n": 3,
        "direct_plan": True,
        "input_markdown_dir": "story_selections",
        "auxiliary_input_markdown_dirs": ["revised_stories"],
        "aggregate_input_markdown": True,
        "save_markdown": True,
        "markdown_dir": "publication_offer_emails",
        "preserve_build_dirs": ["short_stories", "story_selections", "revised_stories"],
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

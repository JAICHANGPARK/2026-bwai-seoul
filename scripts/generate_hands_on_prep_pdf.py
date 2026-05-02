#!/usr/bin/env python3
"""Generate a full single-file PDF for the Gemma 4 hands-on prep documents."""

from __future__ import annotations

import math
import re
import textwrap
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

try:
    import fitz  # PyMuPDF
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover - optional for rendering checks only.
    fitz = None
    Image = None
    ImageDraw = None
    ImageFont = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional for page count fallback only.
    PdfReader = None


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output" / "pdf"
TMP_DIR = ROOT / "tmp" / "pdfs"
PDF_PATH = OUTPUT_DIR / "gemma4-hands-on-prep-guide.pdf"
CONTACT_PREFIX = TMP_DIR / "gemma4-hands-on-prep-contact"

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 16 * mm
RIGHT_MARGIN = 16 * mm
TOP_MARGIN = 18 * mm
BOTTOM_MARGIN = 18 * mm
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

ACCENT = colors.HexColor("#0F766E")
ACCENT_DARK = colors.HexColor("#0B3C49")
INK = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#475569")
SOFT_BG = colors.HexColor("#F4F7FB")
WARM = colors.HexColor("#F59E0B")
ALERT_BG = colors.HexColor("#FFF7ED")
CODE_BG = colors.HexColor("#F8FAFC")
RULE = colors.HexColor("#CBD5E1")

SESSION_NAME = "Build Your Own AI Office with Gemma 4"
EVENT_NAME = "Build with AI Seoul 2026"
TRACK = "Hands-On A"
PRESENTER = "박제창"
DURATION = "13:30 ~ 14:30 (60분)"
CHECK_DATE = "2026-05-02"

DOC_FILES = [
    ROOT / "docs/01-hardware-and-model-selection.md",
    ROOT / "docs/02-windows-guide.md",
    ROOT / "docs/03-memory-based-model-selection.md",
    ROOT / "docs/04-gguf-mlx-llamacpp-explainer.md",
    ROOT / "docs/05-lm-studio-setup.md",
    ROOT / "docs/06-ollama-setup.md",
    ROOT / "docs/07-llamacpp-setup.md",
    ROOT / "docs/08-apple-silicon-mlx.md",
    ROOT / "docs/09-gemma4-benchmarks-and-agent-expectations.md",
    ROOT / "docs/10-opencode-lmstudio-developer-agent.md",
    ROOT / "docs/11-pi-and-tool-selection-notes.md",
    ROOT / "docs/12-hermes-agent-overview.md",
    ROOT / "docs/13-hermes-agent-setup.md",
    ROOT / "docs/14-gemma4-architecture-deep-dive.md",
    ROOT / "docs/15-gemini-cli-gemma-routing-prep.md",
    ROOT / "docs/16-troubleshooting-and-final-check.md",
    ROOT / "docs/17-faq.md",
    ROOT / "docs/18-uv-setup.md",
    ROOT / "docs/19-code-editor-setup.md",
]


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)


def register_fonts() -> dict[str, str]:
    home = Path.home()
    font_pairs = [
        (
            home / "Library/Fonts/Pretendard-Regular.otf",
            home / "Library/Fonts/Pretendard-Bold.otf",
        ),
        (
            home / "Library/Fonts/PretendardVariable.ttf",
            home / "Library/Fonts/PretendardVariable.ttf",
        ),
        (
            Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        ),
    ]
    for regular_path, bold_path in font_pairs:
        if not regular_path.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont("GuideSans", str(regular_path)))
            if bold_path.exists():
                pdfmetrics.registerFont(TTFont("GuideSans-Bold", str(bold_path)))
            else:
                pdfmetrics.registerFont(TTFont("GuideSans-Bold", str(regular_path)))
            pdfmetrics.registerFontFamily(
                "GuideSans",
                normal="GuideSans",
                bold="GuideSans-Bold",
                italic="GuideSans",
                boldItalic="GuideSans-Bold",
            )
            return {
                "sans": "GuideSans",
                "bold": "GuideSans-Bold",
                "mono": "Courier",
                "source": regular_path.name,
            }
        except Exception:
            continue

    pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
    pdfmetrics.registerFontFamily(
        "GuideSans",
        normal="HYGothic-Medium",
        bold="HYGothic-Medium",
        italic="HYGothic-Medium",
        boldItalic="HYGothic-Medium",
    )
    return {
        "sans": "HYGothic-Medium",
        "bold": "HYGothic-Medium",
        "mono": "Courier",
        "source": "HYGothic-Medium",
    }


def build_styles(fonts: dict[str, str]) -> StyleSheet1:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName=fonts["sans"],
            fontSize=10.2,
            leading=14.4,
            textColor=INK,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["Body"],
            fontSize=8.8,
            leading=12.2,
            textColor=MUTED,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Heading1"],
            fontName=fonts["bold"],
            fontSize=19,
            leading=24,
            textColor=ACCENT_DARK,
            spaceBefore=4,
            spaceAfter=9,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName=fonts["bold"],
            fontSize=14,
            leading=18,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subsection",
            parent=styles["Heading3"],
            fontName=fonts["bold"],
            fontSize=11.5,
            leading=15,
            textColor=ACCENT_DARK,
            spaceBefore=5,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MinorHeading",
            parent=styles["Heading4"],
            fontName=fonts["bold"],
            fontSize=10.4,
            leading=14,
            textColor=INK,
            spaceBefore=4,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocKicker",
            parent=styles["BodySmall"],
            fontName=fonts["bold"],
            fontSize=8.8,
            leading=11.5,
            textColor=ACCENT,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocSource",
            parent=styles["BodySmall"],
            fontSize=8.3,
            leading=11.2,
            textColor=MUTED,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName=fonts["bold"],
            fontSize=27,
            leading=33,
            alignment=TA_LEFT,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Heading2"],
            fontName=fonts["sans"],
            fontSize=15,
            leading=19,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#DDEFF0"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMeta",
            parent=styles["Body"],
            fontName=fonts["sans"],
            fontSize=10.2,
            leading=14,
            textColor=colors.HexColor("#D5E8EA"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideBullet",
            parent=styles["Body"],
            leftIndent=12,
            firstLineIndent=0,
            bulletIndent=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["Body"],
            fontSize=8.9,
            leading=12,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["TableCell"],
            fontName=fonts["bold"],
            textColor=colors.white,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeLabel",
            parent=styles["BodySmall"],
            fontName=fonts["bold"],
            textColor=ACCENT_DARK,
        )
    )
    return styles


def rich(text: str) -> str:
    def inline_code(match: re.Match[str]) -> str:
        content = match.group(1)
        if content.isascii():
            return f'<font name="Courier">{content}</font>'
        return f"<b>{content}</b>"

    text = escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#0F766E">\1</link>',
        text,
    )
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", inline_code, text)
    return text.replace("\n", "<br/>")


def p(text: str, styles: StyleSheet1, style: str = "Body") -> Paragraph:
    return Paragraph(rich(text), styles[style])


def bullets(items: Iterable[str], styles: StyleSheet1, ordered: bool = False) -> ListFlowable:
    return ListFlowable(
        [
            ListItem(Paragraph(rich(item), styles["GuideBullet"]), leftIndent=6)
            for item in items
        ],
        bulletType="1" if ordered else "bullet",
        start="1" if ordered else "-",
        leftIndent=10,
        bulletFontName=styles["Body"].fontName,
        bulletFontSize=10,
        bulletColor=ACCENT_DARK,
    )


def wrap_code_text(code: str, ascii_only: bool) -> str:
    width = 92 if ascii_only else 54
    wrapped_lines: list[str] = []
    for raw_line in code.strip("\n").splitlines():
        if not raw_line.strip():
            wrapped_lines.append("")
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        prefix = " " * indent
        content = raw_line[indent:]
        chunks = textwrap.wrap(
            content,
            width=max(12, width - indent),
            break_long_words=False,
            break_on_hyphens=False,
        )
        if not chunks:
            wrapped_lines.append(prefix)
            continue
        for chunk in chunks:
            wrapped_lines.append(prefix + chunk)
    return "\n".join(wrapped_lines)


def code_block(label: str, code: str, styles: StyleSheet1) -> KeepTogether:
    ascii_only = code.isascii()
    display_label = (label or "code").strip().lower()
    header = Paragraph(
        rich(display_label),
        ParagraphStyle(
            "CodeBlockHeader",
            parent=styles["CodeLabel"],
            fontName=styles["CodeLabel"].fontName,
            fontSize=8.3,
            leading=10,
            textColor=colors.white,
        ),
    )
    body = Preformatted(
        wrap_code_text(code, ascii_only),
        ParagraphStyle(
            "CodeBlockBody",
            fontName="Courier" if ascii_only else styles["Body"].fontName,
            fontSize=8.2,
            leading=10.6,
            textColor=INK,
            leftIndent=0,
            rightIndent=0,
        ),
    )
    table = Table([[header], [body]], colWidths=[CONTENT_WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT_DARK),
                ("BACKGROUND", (0, 1), (-1, 1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.7, RULE),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#164E63")),
                ("LEFTPADDING", (0, 0), (-1, 0), 8),
                ("RIGHTPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 5),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                ("LEFTPADDING", (0, 1), (-1, 1), 9),
                ("RIGHTPADDING", (0, 1), (-1, 1), 9),
                ("TOPPADDING", (0, 1), (-1, 1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 3 * mm)])


def info_box(title: str, body: list[str], styles: StyleSheet1, warm: bool = False) -> Table:
    bg = ALERT_BG if warm else SOFT_BG
    accent = WARM if warm else ACCENT
    content = [Paragraph(rich(f"**{title}**"), styles["Subsection"])]
    for item in body:
        content.append(Paragraph(rich(item), styles["Body"]))
    table = Table([[content]], colWidths=[CONTENT_WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def cover_info_table(rows: list[list[str]], styles: StyleSheet1) -> Table:
    data = [
        [
            Paragraph(rich(f"**{label}**"), styles["CoverMeta"]),
            Paragraph(rich(value), styles["CoverMeta"]),
        ]
        for label, value in rows
    ]
    table = Table(data, colWidths=[28 * mm, CONTENT_WIDTH - 28 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0B3C49")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#2DD4BF")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#185A68")),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def data_table(rows: list[list[str]], styles: StyleSheet1) -> Table:
    column_count = max(len(row) for row in rows)
    normalized = [row + [""] * (column_count - len(row)) for row in rows]
    widths = [CONTENT_WIDTH / column_count] * column_count
    data = [
        [Paragraph(rich(cell), styles["TableHeader"]) for cell in normalized[0]],
        *[
            [Paragraph(rich(cell), styles["TableCell"]) for cell in row]
            for row in normalized[1:]
        ],
    ]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT_BG]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def cover_background(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0F172A"))
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#0F766E"))
    canvas.rect(0, PAGE_HEIGHT - 42 * mm, PAGE_WIDTH, 42 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#134E4A"))
    canvas.circle(PAGE_WIDTH - 18 * mm, PAGE_HEIGHT - 18 * mm, 20 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#EAB308"))
    canvas.circle(PAGE_WIDTH - 42 * mm, PAGE_HEIGHT - 50 * mm, 8 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#0B3C49"))
    canvas.rect(LEFT_MARGIN, 28 * mm, CONTENT_WIDTH, 34 * mm, stroke=0, fill=1)
    canvas.restoreState()


def later_pages(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(
        LEFT_MARGIN,
        PAGE_HEIGHT - 12 * mm,
        PAGE_WIDTH - RIGHT_MARGIN,
        PAGE_HEIGHT - 12 * mm,
    )
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(ACCENT_DARK)
    canvas.drawString(LEFT_MARGIN, PAGE_HEIGHT - 8.5 * mm, "Gemma 4 Hands-On Prep Guide")
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(
        PAGE_WIDTH - RIGHT_MARGIN,
        8 * mm,
        f"{EVENT_NAME}  |  Page {doc.page}",
    )
    canvas.restoreState()


def extract_doc_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.name


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells if cell)


def parse_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown(path: Path, styles: StyleSheet1) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    flowables: list = []
    paragraph_lines: list[str] = []
    first_h1_seen = False
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if not paragraph_lines:
            return
        text = " ".join(line.strip() for line in paragraph_lines if line.strip())
        if text:
            flowables.append(p(text, styles))
        paragraph_lines = []

    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        if stripped == "":
            flush_paragraph()
            i += 1
            continue

        if stripped in {"---", "***", "___"}:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("[메인 안내로 돌아가기]("):
            flush_paragraph()
            i += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            if level == 1:
                if first_h1_seen:
                    flowables.append(Spacer(1, 3 * mm))
                    flowables.append(Paragraph(rich(text), styles["DocTitle"]))
                else:
                    flowables.append(Paragraph(rich(text), styles["DocTitle"]))
                    first_h1_seen = True
            elif level == 2:
                flowables.append(Paragraph(rich(text), styles["Section"]))
            elif level == 3:
                flowables.append(Paragraph(rich(text), styles["Subsection"]))
            else:
                flowables.append(Paragraph(rich(text), styles["MinorHeading"]))
            i += 1
            continue

        fence_match = re.match(r"^(```|~~~)\s*(.*)$", stripped)
        if fence_match:
            flush_paragraph()
            fence = fence_match.group(1)
            label = fence_match.group(2).strip() or "Code"
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(fence):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            flowables.append(code_block(label, "\n".join(code_lines), styles))
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            flush_paragraph()
            table_rows = [parse_table_row(lines[i])]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(parse_table_row(lines[i]))
                i += 1
            if len(table_rows) > 1:
                flowables.append(data_table(table_rows, styles))
                flowables.append(Spacer(1, 2 * mm))
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].lstrip())
                i += 1
            flowables.append(info_box("중요 메모", quote_lines, styles, warm=True))
            flowables.append(Spacer(1, 2 * mm))
            continue

        unordered_match = re.match(r"^\s*[-*+]\s+(.*)$", line)
        ordered_match = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if unordered_match or ordered_match:
            flush_paragraph()
            ordered = bool(ordered_match)
            items: list[str] = []
            while i < len(lines):
                current = lines[i].rstrip("\n")
                current_stripped = current.strip()
                if not current_stripped:
                    break
                current_unordered = re.match(r"^\s*[-*+]\s+(.*)$", current)
                current_ordered = re.match(r"^\s*\d+\.\s+(.*)$", current)
                if current_unordered or current_ordered:
                    if ordered != bool(current_ordered):
                        break
                    item_text = (current_ordered or current_unordered).group(1).strip()
                    items.append(item_text)
                    i += 1
                    while i < len(lines):
                        continuation = lines[i].rstrip("\n")
                        continuation_stripped = continuation.strip()
                        if not continuation_stripped:
                            break
                        if re.match(r"^\s*[-*+]\s+(.*)$", continuation) or re.match(
                            r"^\s*\d+\.\s+(.*)$", continuation
                        ):
                            break
                        if continuation.startswith(" ") or continuation.startswith("\t"):
                            items[-1] += " " + continuation_stripped
                            i += 1
                            continue
                        break
                else:
                    break
            flowables.append(bullets(items, styles, ordered=ordered))
            flowables.append(Spacer(1, 1 * mm))
            continue

        paragraph_lines.append(line)
        i += 1

    flush_paragraph()
    return flowables


def document_section(index: int, path: Path, styles: StyleSheet1) -> list:
    story: list = []
    if index > 1:
        story.append(PageBreak())
    story.append(Paragraph(f"문서 {index:02d}", styles["DocKicker"]))
    story.append(Paragraph(path.relative_to(ROOT).as_posix(), styles["DocSource"]))
    story.extend(parse_markdown(path, styles))
    return story


def prep_summary_page(styles: StyleSheet1) -> list:
    return [
        Paragraph("한장 요약: 행사 전 준비", styles["DocTitle"]),
        p(
            "행사 당일에는 설치와 모델 다운로드를 시작하지 않는 것을 기준으로 준비합니다. "
            "아래 항목 중 본인 환경에 맞는 경로를 선택하고, 모델 다운로드와 1회 실행 테스트까지 끝내 주세요.",
            styles,
        ),
        info_box(
            "가장 중요한 기준",
            [
                "하나만 설치한다면 **LM Studio**를 우선 권장합니다. ChromeOS 또는 Intel Mac은 **Ollama**를 우선 고려하세요.",
                "8GB 장비는 **E2B only, best-effort**입니다. 가능하면 16GB 이상 장비로 참석해 주세요.",
            ],
            styles,
            warm=True,
        ),
        Spacer(1, 3 * mm),
        Paragraph("설치해야 하는 소프트웨어와 LLM", styles["Section"]),
        data_table(
            [
                ["내 상황", "설치 소프트웨어", "미리 받을 LLM", "완료 기준"],
                [
                    "처음 준비하는 경우",
                    "LM Studio",
                    "Gemma 4 E4B 권장, 8GB는 E2B",
                    "앱 실행, 모델 다운로드, Chat 1회 성공",
                ],
                [
                    "CLI/API도 필요한 경우",
                    "LM Studio + Ollama",
                    "`gemma4:e2b` 또는 `gemma4:e4b`",
                    "`ollama run` 1회 성공",
                ],
                [
                    "ChromeOS / Intel Mac",
                    "Ollama",
                    "`gemma4:e2b` 우선",
                    "Linux 환경 또는 터미널에서 1회 실행",
                ],
                [
                    "고급 에이전트 실습",
                    "LM Studio 또는 llama.cpp + OpenCode/Hermes",
                    "32GB+는 26B A4B, 36GB+는 31B 가능",
                    "local endpoint와 에이전트 연결 확인",
                ],
                [
                    "Gemini CLI Gemma 실험 기능 확인",
                    "Gemini CLI",
                    "Preview는 Gemma 4 모델 선택, setup은 Gemma 3 라우터",
                    "`gemini --model gemma-4-26b-a4b-it`, `gemini gemma setup`",
                ],
            ],
            styles,
        ),
        Spacer(1, 3 * mm),
        Paragraph("메모리별 LLM 선택", styles["Section"]),
        data_table(
            [
                ["노트북 메모리", "권장 LLM", "권장 도구", "준비 메모"],
                ["8GB", "Gemma 4 E2B만", "LM Studio 또는 Ollama", "속도 저하 가능, 다른 앱 종료"],
                ["16GB", "Gemma 4 E4B", "LM Studio 우선", "가장 무난한 참가 사양"],
                ["32GB", "E4B 또는 26B A4B", "LM Studio, 필요 시 llama.cpp", "에이전트 실습은 26B A4B 권장"],
                ["36GB+", "26B A4B 또는 31B", "LM Studio 또는 llama.cpp", "품질 우선은 31B, 반응성 우선은 26B A4B"],
            ],
            styles,
        ),
        Spacer(1, 3 * mm),
        Paragraph("공통 최종 체크리스트", styles["Section"]),
        bullets(
            [
                "설치 권한 또는 관리자 권한 확인",
                "디스크 여유 공간 최소 20GB, 가능하면 40GB 이상 확보",
                "선택한 소프트웨어 설치 완료",
                "사용할 Gemma 4 모델 다운로드 완료",
                "행사 전 최소 1회 응답 생성 테스트 완료",
                "실습 당일 전원 어댑터 지참",
            ],
            styles,
        ),
        PageBreak(),
    ]


def build_story(styles: StyleSheet1) -> list:
    story: list = []

    story.extend(
        [
            Spacer(1, 56 * mm),
            Paragraph("핸즈온 사전 준비 가이드", styles["CoverTitle"]),
            Paragraph(SESSION_NAME, styles["CoverSubtitle"]),
            Spacer(1, 10 * mm),
            cover_info_table(
                [
                    ["세션명", SESSION_NAME],
                    ["진행자", PRESENTER],
                    ["행사", EVENT_NAME],
                    ["트랙", TRACK],
                    ["진행 시간", DURATION],
                    ["수록 범위", "docs/01-19 전체 문서 원문"],
                    ["기준 확인일", CHECK_DATE],
                ],
                styles,
            ),
            Spacer(1, 14 * mm),
            Paragraph(
                "이 PDF는 저장소의 01-19번 사전 준비 문서를 순서대로 하나의 배포본으로 묶은 버전입니다.",
                styles["CoverMeta"],
            ),
            Spacer(1, 2 * mm),
            Paragraph(
                "표지 다음 페이지부터 각 문서의 본문을 전체 수록합니다.",
                styles["CoverMeta"],
            ),
            PageBreak(),
        ]
    )

    story.extend(prep_summary_page(styles))

    story.append(Paragraph("수록 문서", styles["DocTitle"]))
    story.append(
        p(
            "아래 문서를 순서대로 모두 포함했습니다. 각 문서는 다음 페이지부터 원문 내용을 전체 수록합니다.",
            styles,
        )
    )
    story.append(
        bullets(
            [f"{idx:02d}. {extract_doc_title(path)}" for idx, path in enumerate(DOC_FILES, start=1)],
            styles,
            ordered=False,
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        info_box(
            "편집 방침",
            [
                "세션명과 진행자명은 표지에 반영했습니다.",
                "기존 요약 위주의 본문은 제거하고, 각 마크다운 문서의 전체 내용을 넣도록 생성 방식을 바꿨습니다.",
                "문서 내부의 상대 링크는 PDF 안에서는 링크 라벨 텍스트로 정리해 표시합니다.",
            ],
            styles,
        )
    )

    for index, path in enumerate(DOC_FILES, start=1):
        story.extend(document_section(index, path, styles))

    return story


def build_pdf(styles: StyleSheet1) -> int:
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Gemma 4 Hands-On Prep Guide",
        author="OpenAI Codex",
        subject="Build with AI Seoul 2026 hands-on prep guide",
    )
    story = build_story(styles)
    doc.build(story, onFirstPage=cover_background, onLaterPages=later_pages)
    if fitz is not None:
        return fitz.open(PDF_PATH).page_count
    if PdfReader is not None:
        return len(PdfReader(PDF_PATH).pages)
    return 0


def _fit_text(draw, text: str, width: int, font_path: str | None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if ImageFont is None:
        raise RuntimeError("Pillow is not available")
    if font_path:
        for size in range(24, 11, -1):
            try:
                font = ImageFont.truetype(font_path, size=size)
            except Exception:
                continue
            box = draw.textbbox((0, 0), text, font=font)
            if (box[2] - box[0]) <= width:
                return font
    return ImageFont.load_default()


def render_contact_sheets() -> list[Path]:
    if fitz is None or Image is None or ImageDraw is None:
        return []

    doc = fitz.open(PDF_PATH)
    if doc.page_count == 0:
        return []

    font_path = None
    for candidate in [
        Path.home() / "Library/Fonts/PretendardVariable.ttf",
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    ]:
        if candidate.exists():
            font_path = str(candidate)
            break

    contact_paths: list[Path] = []
    per_sheet = 6
    columns = 3
    rows = 2
    thumb_w = 500
    thumb_h = 710
    gap = 28
    margin = 44
    sheet_w = columns * thumb_w + (columns - 1) * gap + margin * 2
    sheet_h = rows * thumb_h + (rows - 1) * gap + margin * 2 + 80

    for sheet_index in range(math.ceil(doc.page_count / per_sheet)):
        sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
        draw = ImageDraw.Draw(sheet)
        title = f"Gemma 4 prep guide review sheet {sheet_index + 1}"
        title_font = _fit_text(draw, title, sheet_w - margin * 2, font_path)
        draw.text((margin, 18), title, fill=(15, 23, 42), font=title_font)

        for slot in range(per_sheet):
            page_index = sheet_index * per_sheet + slot
            if page_index >= doc.page_count:
                break
            page = doc.load_page(page_index)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.thumbnail((thumb_w, thumb_h))

            row = slot // columns
            col = slot % columns
            x = margin + col * (thumb_w + gap)
            y = margin + 48 + row * (thumb_h + gap)

            draw.rounded_rectangle(
                [x - 4, y - 24, x + thumb_w + 4, y + thumb_h + 10],
                radius=12,
                outline=(203, 213, 225),
                width=2,
                fill=(248, 250, 252),
            )
            label = f"Page {page_index + 1}"
            label_font = _fit_text(draw, label, thumb_w, font_path)
            draw.text((x, y - 20), label, fill=(15, 118, 110), font=label_font)
            paste_x = x + (thumb_w - img.width) // 2
            paste_y = y + (thumb_h - img.height) // 2
            sheet.paste(img, (paste_x, paste_y))

        output_path = Path(f"{CONTACT_PREFIX}-{sheet_index + 1}.png")
        sheet.save(output_path, format="PNG")
        contact_paths.append(output_path)

    return contact_paths


def main() -> None:
    ensure_dirs()
    fonts = register_fonts()
    styles = build_styles(fonts)
    page_count = build_pdf(styles)
    contacts = render_contact_sheets()

    print(f"PDF generated: {PDF_PATH}")
    print(f"Pages: {page_count}")
    print(f"Font source: {fonts['source']}")
    if contacts:
        for path in contacts:
            print(f"Contact sheet: {path}")
    else:
        print("Contact sheets were not generated.")


if __name__ == "__main__":
    main()

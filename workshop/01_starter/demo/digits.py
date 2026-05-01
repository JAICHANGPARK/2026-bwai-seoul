"""
digits.py — ASCII art font for the real-time throughput dashboard.
"""

# ─────────────────────────────────────────────────────────────
# Font: "Shaded" blocks (7 lines tall, 10 chars wide per glyph)
# ─────────────────────────────────────────────────────────────

GLYPHS = {
    "0": [
        " ░██████ ",
        "░██   ░██",
        "░██   ░██",
        "░██   ░██",
        "░██   ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    "1": [
        "  ░██  ",
        "░████  ",
        "  ░██  ",
        "  ░██  ",
        "  ░██  ",
        "  ░██  ",
        "░██████",
    ],
    "2": [
        " ░██████ ",
        "░██   ░██",
        "      ░██",
        "  ░█████ ",
        " ░██     ",
        "░██      ",
        "░████████",
    ],
    "3": [
        " ░██████ ",
        "░██   ░██",
        "      ░██",
        "  ░█████ ",
        "      ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    "4": [
        "   ░████ ",
        "  ░██ ██ ",
        " ░██  ██ ",
        "░██   ██ ",
        "░█████████",
        "     ░██ ",
        "     ░██ ",
    ],
    "5": [
        "░████████",
        "░██      ",
        "░███████ ",
        "      ░██",
        "░██   ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    "6": [
        " ░██████ ",
        "░██   ░██",
        "░██      ",
        "░███████ ",
        "░██   ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    "7": [
        "░█████████",
        "░██    ░██",
        "      ░██ ",
        "     ░██  ",
        "    ░██   ",
        "    ░██   ",
        "    ░██   ",
    ],
    "8": [
        " ░██████ ",
        "░██   ░██",
        "░██   ░██",
        " ░██████ ",
        "░██   ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    "9": [
        " ░██████ ",
        "░██   ░██",
        "░██   ░██",
        " ░███████",
        "      ░██",
        "░██   ░██",
        " ░██████ ",
    ],
    ".": [
        "         ",
        "         ",
        "         ",
        "         ",
        "         ",
        "         ",
        " ░████   ",
    ],
}

# Pad every row to exactly 10 characters to prevent alignment jitter.
# dashboard.py는 tokens/sec 숫자를 매초 다시 그립니다. glyph마다 폭이 다르면
# 숫자가 바뀔 때 UI가 좌우로 흔들리므로, 모든 줄을 같은 폭으로 맞춥니다.
GLYPHS = {k: [r.ljust(10) for r in v] for k, v in GLYPHS.items()}

_HEIGHT = 7


def render_big_number(number_str: str) -> str:
    """Render a number string as shaded block characters.

    입력은 이미 포맷된 문자열입니다. 예: "12.3". 정의되지 않은 문자는 같은
    폭의 공백 glyph로 처리해서 dashboard layout이 깨지지 않게 합니다.
    """
    lines = [""] * _HEIGHT
    for ch in number_str:
        glyph = GLYPHS.get(ch)
        if glyph is None:
            # Unknown character fallback. 폭을 유지하는 것이 숫자 자체보다 중요합니다.
            width = len(GLYPHS["0"][0])
            glyph = [" " * width] * _HEIGHT
        for i in range(_HEIGHT):
            lines[i] += glyph[i]
    return "\n".join(lines)

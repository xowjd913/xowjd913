"""Render the static slate cards (section titles, featured work, AI workflow) into assets/."""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
FONT = "'Segoe UI',Ubuntu,sans-serif"
# Two-tone palette for the profile slate theme: slate blue and soft teal only.
NEON = ["#7ea6e0", "#9bc4b4"]
W = 830
DEFS = """<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e2432"/><stop offset="1" stop-color="#171c28"/></linearGradient>
<filter id="g" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>"""

FEATURED = [
    ("Mascoz", "Windows", "Unity 6 · VRM · MediaPipe"),
    ("Mascoz Launcher & Publisher", "Windows", "Flutter · Dart"),
    ("Toema Prototype", "Windows", "Unity · UniTask · Addressables"),
    ("XGEN", "Windows · WebGL · Android", "Unity · Zenject · OpenCV"),
    ("Healthverse", "Android · iOS", "Unity · Agora · Cinemachine"),
    ("Narang", "Android", "Unity · AR Foundation · UGS"),
    ("Noisy Smart Kit", "WebGL · Windows", "Unity · Zenject · UniRx"),
    ("Omniverse Extensions", "Windows", "Python · Omniverse"),
]
AI = [
    ("HUMAN IN THE LOOP", ["I verify every change and merge it myself.", "Agents never force-push to the base branch."]),
    ("COST-AWARE MODELS", ["Sonnet by default, Opus only when judgment is", "needed. Work is gated by remaining usage limits."]),
    ("INDEPENDENT REVIEW", ["Every PR goes through a separate reviewer agent", "before I test it myself."]),
    ("SHARED RULES", ["One private rules repo keeps model choice, PR", "format and review scope consistent everywhere."]),
]


def write(name, height, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}">{DEFS}{body}</svg>\n'
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


def title(name, text, color):
    write(name, 44, f"""<style>.t{{font:800 18px {FONT};letter-spacing:3px}}</style>
<rect x="0" y="12" width="4" height="22" rx="2" fill="{color}" filter="url(#g)"/>
<text x="16" y="30" class="t" fill="{color}" filter="url(#g)">{escape(text)}</text>
<line x1="16" y1="40" x2="{W}" y2="40" stroke="{color}" stroke-opacity=".35"/>""")


def grid(name, items, card_h, draw, top=0, pre="", css=""):
    cols, gap = 2, 14
    card_w = (W - gap) / cols
    rows = (len(items) + 1) // cols
    height = top + rows * card_h + (rows - 1) * gap + 2
    body = ""
    for i, item in enumerate(items):
        x, y = 1 + (i % cols) * (card_w + gap), 1 + top + (i // cols) * (card_h + gap)
        color = NEON[(i % cols + i // cols) % 2]
        body += f'<rect x="{x:.1f}" y="{y}" width="{card_w - 2:.1f}" height="{card_h}" rx="10" fill="url(#bg)" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>'
        body += f'<rect x="{x + 14:.1f}" y="{y + 16}" width="3" height="{card_h - 32}" rx="1.5" fill="{color}" filter="url(#g)"/>'
        body += draw(x + 30, y, color, item)
    write(name, height, f"""<style>.n{{font:700 17px {FONT}}}.p{{font:600 12px {FONT};fill:#dde3ee}}.s{{font:400 12px {FONT};fill:#97a3b8}}.h{{font:800 14px {FONT};letter-spacing:2px}}.d{{font:400 12.5px {FONT};fill:#dde3ee}}{css}</style>{pre}{body}""")


def featured(x, y, color, item):
    name, platform, stack = map(escape, item)
    return (f'<text x="{x:.1f}" y="{y + 32}" class="n" fill="{color}" filter="url(#g)">{name}</text>'
            f'<text x="{x:.1f}" y="{y + 54}" class="p">{platform}</text>'
            f'<text x="{x:.1f}" y="{y + 72}" class="s">{stack}</text>')


def workflow(x, y, color, item):
    head, lines = item
    out = f'<text x="{x:.1f}" y="{y + 32}" class="h" fill="{color}" filter="url(#g)">{escape(head)}</text>'
    for j, line in enumerate(lines):
        out += f'<text x="{x:.1f}" y="{y + 56 + j * 18}" class="d">{escape(line)}</text>'
    return out


FLOW_CSS = (f".f{{font:800 13px {FONT};letter-spacing:1.5px}}.m{{font:400 11px {FONT};fill:#97a3b8}}"
            ".l{fill:none;stroke:#97a3b8;stroke-width:1.5}")


FLOW_H = 190
LEADERS = 3


def flow():
    """Top strip: YOU -> PO -> several LEADERs, each with its own WORKER + REVIEWER."""
    out = ('<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           '<path d="M0 1 L9 5 L0 9 z" fill="#97a3b8"/></marker>'
           f'<rect x="1" y="1" width="{W - 2}" height="{FLOW_H - 2}" rx="10" fill="url(#bg)" stroke="{NEON[0]}" stroke-opacity=".35" stroke-width="1.5"/>')

    def box(x, y, w, h, color):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#171c28" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>'

    def label(c, y, name, sub, color):
        return (f'<text x="{c}" y="{y + 19}" text-anchor="middle" class="f" fill="{color}" filter="url(#g)">{name}</text>'
                f'<text x="{c}" y="{y + 35}" text-anchor="middle" class="m">{escape(sub)}</text>')

    pitch, top, bh = 56, 15, 48
    mid = top + (LEADERS - 1) * pitch / 2 + bh / 2  # vertical centre of the leader column
    my = int(mid - bh / 2)
    for x, w, name, sub, color in [(24, 110, "YOU", "request & verify", NEON[1]),
                                   (164, 154, "PO", "plans & manages leaders", NEON[0])]:
        out += box(x, my, w, bh, color) + label(x + w // 2, my, name, sub, color)
    out += f'<path class="l" d="M138 {mid:.0f} H160" marker-end="url(#a)"/>'
    bus = 336
    ys = [top + i * pitch for i in range(LEADERS)]
    out += f'<path class="l" d="M318 {mid:.0f} H{bus} M{bus} {ys[0] + bh // 2} V{ys[-1] + bh // 2}"/>'
    for i, y in enumerate(ys):
        c = y + bh // 2
        out += f'<path class="l" d="M{bus} {c} H352" marker-end="url(#a)"/>'
        out += box(356, y, 130, bh, NEON[1]) + label(421, y, f"LEADER {i + 1}", "splits into issues", NEON[1])
        out += f'<path class="l" d="M490 {c} H510 M510 {y + 11} V{y + 37}"/>'
        for dy, name, sub, color in [(0, "WORKER", "implements", NEON[0]), (26, "REVIEWER", "reviews PRs", NEON[1])]:
            out += f'<path class="l" d="M510 {y + dy + 11} H532" marker-end="url(#a)"/>'
            out += box(536, y + dy, 276, 22, color)
            out += f'<text x="552" y="{y + dy + 15}" class="f" fill="{color}" filter="url(#g)">{name}</text>'
            out += f'<text x="660" y="{y + dy + 15}" class="m">{sub}</text>'
    return out


os.makedirs(OUT, exist_ok=True)
title("title-featured.svg", "FEATURED WORK", NEON[0])
title("title-ai.svg", "HOW I BUILD WITH AI", NEON[1])
grid("featured.svg", FEATURED, 88, featured)
grid("ai.svg", AI, 92, workflow, top=FLOW_H + 14, pre=flow(), css=FLOW_CSS)
print("neon assets written")

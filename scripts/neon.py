"""Render the static neon cards (section titles, featured work, AI workflow) into assets/."""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
FONT = "'Segoe UI',Ubuntu,sans-serif"
# Two-tone palette matching the agent office theme: cyan and neon yellow only.
NEON = ["#00f0ff", "#fcee0a"]
W = 830
DEFS = """<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0a24"/><stop offset="1" stop-color="#07060f"/></linearGradient>
<filter id="g" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>"""

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
    ("AGENT TEAM", ["A lead agent splits work into issues and runs", "developer–reviewer agent pairs in parallel worktrees"]),
    ("INDEPENDENT REVIEW", ["Every feature PR goes through a separate reviewer", "agent before a human tests and merges"]),
    ("AGENT OFFICE", ["A pixel-art office that shows what each agent", "is doing in real time"]),
    ("SHARED RULES", ["One rule repository keeps model choice, PR format", "and review scope consistent across projects"]),
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


def grid(name, items, card_h, draw):
    cols, gap = 2, 14
    card_w = (W - gap) / cols
    rows = (len(items) + 1) // cols
    height = rows * card_h + (rows - 1) * gap + 2
    body = ""
    for i, item in enumerate(items):
        x, y = 1 + (i % cols) * (card_w + gap), 1 + (i // cols) * (card_h + gap)
        color = NEON[(i % cols + i // cols) % 2]
        body += f'<rect x="{x:.1f}" y="{y}" width="{card_w - 2:.1f}" height="{card_h}" rx="10" fill="url(#bg)" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>'
        body += f'<rect x="{x + 14:.1f}" y="{y + 16}" width="3" height="{card_h - 32}" rx="1.5" fill="{color}" filter="url(#g)"/>'
        body += draw(x + 30, y, color, item)
    write(name, height, f"""<style>.n{{font:700 17px {FONT}}}.p{{font:600 12px {FONT};fill:#cfd8ff}}.s{{font:400 12px {FONT};fill:#8f9cc8}}.h{{font:800 14px {FONT};letter-spacing:2px}}.d{{font:400 12.5px {FONT};fill:#cfd8ff}}</style>{body}""")


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


os.makedirs(OUT, exist_ok=True)
title("title-featured.svg", "FEATURED WORK", NEON[0])
title("title-ai.svg", "HOW I BUILD WITH AI", NEON[1])
grid("featured.svg", FEATURED, 88, featured)
grid("ai.svg", AI, 92, workflow)
print("neon assets written")

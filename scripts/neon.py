"""Render the static neon cards (section titles, featured work, AI workflow) into assets/."""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
FONT = "'Segoe UI',Ubuntu,sans-serif"
# Two-tone palette for the profile cyberpunk theme: cyan and neon yellow only.
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
    write(name, height, f"""<style>.n{{font:700 17px {FONT}}}.p{{font:600 12px {FONT};fill:#cfd8ff}}.s{{font:400 12px {FONT};fill:#8f9cc8}}.h{{font:800 14px {FONT};letter-spacing:2px}}.d{{font:400 12.5px {FONT};fill:#cfd8ff}}{css}</style>{pre}{body}""")


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


FLOW_CSS = (f".f{{font:800 13px {FONT};letter-spacing:1.5px}}.m{{font:400 11px {FONT};fill:#8f9cc8}}"
            ".l{fill:none;stroke:#8f9cc8;stroke-width:1.5}")


def flow():
    """Top strip: YOU -> PO -> LEADER -> WORKER + REVIEWER."""
    out = ('<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           '<path d="M0 1 L9 5 L0 9 z" fill="#8f9cc8"/></marker>'
           f'<rect x="1" y="1" width="{W - 2}" height="76" rx="10" fill="url(#bg)" stroke="{NEON[0]}" stroke-opacity=".35" stroke-width="1.5"/>')

    def box(x, y, w, h, color):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#07060f" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>'

    for x, w, name, sub, color in [(24, 120, "YOU", "request & verify", NEON[1]),
                                   (194, 120, "PO", "plans & triages", NEON[0]),
                                   (364, 140, "LEADER", "splits into issues", NEON[1])]:
        c = x + w // 2
        out += box(x, 17, w, 44, color)
        out += f'<text x="{c}" y="36" text-anchor="middle" class="f" fill="{color}" filter="url(#g)">{name}</text>'
        out += f'<text x="{c}" y="52" text-anchor="middle" class="m">{escape(sub)}</text>'
    out += ('<path class="l" d="M148 39 H190" marker-end="url(#a)"/><path class="l" d="M318 39 H360" marker-end="url(#a)"/>'
            '<path class="l" d="M508 39 H548 M548 23 V55"/>'
            '<path class="l" d="M548 23 H600" marker-end="url(#a)"/><path class="l" d="M548 55 H600" marker-end="url(#a)"/>')
    for y, name, sub, color in [(9, "WORKER", "implements", NEON[0]), (41, "REVIEWER", "reviews PRs", NEON[1])]:
        out += box(604, y, 210, 28, color)
        out += f'<text x="620" y="{y + 18}" class="f" fill="{color}" filter="url(#g)">{name}</text>'
        out += f'<text x="722" y="{y + 18}" class="m">{sub}</text>'
    return out


os.makedirs(OUT, exist_ok=True)
title("title-featured.svg", "FEATURED WORK", NEON[0])
title("title-ai.svg", "HOW I BUILD WITH AI", NEON[1])
grid("featured.svg", FEATURED, 88, featured)
grid("ai.svg", AI, 92, workflow, top=90, pre=flow(), css=FLOW_CSS)
print("neon assets written")

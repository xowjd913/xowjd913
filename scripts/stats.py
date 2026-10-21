"""Render stats.svg from the GitHub GraphQL API, counting private work the token can see."""
import json, os, sys, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ["GH_TOKEN"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "stats.svg"


def query(q):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]


viewer = query("""{viewer{login createdAt pullRequests{totalCount}
  repositories(ownerAffiliations:OWNER){totalCount}}}""")["viewer"]
first_year = int(viewer["createdAt"][:4])
this_year = datetime.now(timezone.utc).year
years = " ".join(
    f'y{y}: contributionsCollection(from:"{y}-01-01T00:00:00Z", to:"{y}-12-31T23:59:59Z")'
    "{contributionCalendar{totalContributions}}"
    for y in range(first_year, this_year + 1)
)
per_year = {
    int(k[1:]): v["contributionCalendar"]["totalContributions"]
    for k, v in query(f'{{user(login:"{viewer["login"]}"){{{years}}}}}')["user"].items()
}
active = [y for y, n in per_year.items() if n]
total = sum(per_year.values())

sizes, colors, cursor = {}, {}, None
while True:
    after = f', after:"{cursor}"' if cursor else ""
    page = query(f"""{{viewer{{repositories(first:100, isFork:false,
      ownerAffiliations:[OWNER, ORGANIZATION_MEMBER]{after}){{
      pageInfo{{hasNextPage endCursor}}
      nodes{{languages(first:20){{edges{{size node{{name color}}}}}}}}}}}}}}""")["viewer"]["repositories"]
    for repo in page["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]
            colors[name] = edge["node"]["color"] or "#8b949e"
    if not page["pageInfo"]["hasNextPage"]:
        break
    cursor = page["pageInfo"]["endCursor"]

all_bytes = sum(sizes.values()) or 1
top = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
langs = [(n, s * 100 / all_bytes, colors[n]) for n, s in top]
rest = 100 - sum(p for _, p, _ in langs)
if rest > 0.05:
    langs.append(("Other", rest, "#8b949e"))

W, x = 495, 25.0
bar = ""
for _, pct, color in langs:
    w = (W - 50) * pct / 100
    bar += f'<rect x="{x:.1f}" y="118" width="{w:.1f}" height="8" fill="{color}"/>'
    x += w
legend = ""
for i, (name, pct, color) in enumerate(langs[:5]):
    cx, cy = 25 + (i % 3) * 150, 148 + (i // 3) * 20
    legend += f'<circle cx="{cx + 5}" cy="{cy}" r="5" fill="{color}"/><text x="{cx + 15}" y="{cy + 4}" class="l">{name} {pct:.1f}%</text>'
stats = [
    (f"{total:,}", "Contributions", f"{min(active)} – {max(active)}" if active else "-"),
    (f'{viewer["pullRequests"]["totalCount"]:,}', "Pull Requests", "authored"),
    (f'{viewer["repositories"]["totalCount"]:,}', "Repositories", "incl. private"),
]
cells = ""
for i, (value, title, sub) in enumerate(stats):
    cx = 25 + i * 150
    cells += f'<text x="{cx}" y="62" class="v">{value}</text><text x="{cx}" y="82" class="t">{title}</text><text x="{cx}" y="98" class="s">{sub}</text>'

font = "'Segoe UI',Ubuntu,sans-serif"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="195" viewBox="0 0 {W} 195">
<style>.h{{font:600 15px {font};fill:#58a6ff}}.v{{font:700 24px {font};fill:#e6edf3}}.t{{font:500 12px {font};fill:#c9d1d9}}.s{{font:400 11px {font};fill:#8b949e}}.l{{font:400 11px {font};fill:#c9d1d9}}</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="194" rx="6" fill="#0d1117" stroke="#30363d"/>
<text x="25" y="30" class="h">GitHub Activity · including private work</text>
{cells}<clipPath id="r"><rect x="25" y="118" width="{W - 50}" height="8" rx="4"/></clipPath><g clip-path="url(#r)">{bar}</g>{legend}
</svg>
"""
with open(OUT, "w") as f:
    f.write(svg)
print(f"{OUT}: {total} contributions, {len(sizes)} languages")

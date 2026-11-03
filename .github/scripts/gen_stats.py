"""Gera assets/stats.svg — estatísticas do GitHub no estilo neofetch.

Corre todos os dias pelo workflow .github/workflows/stats.yml.
Sem GITHUB_TOKEN (ex.: localmente) mostra só o que a API pública dá.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape

USER = os.environ.get("GH_USER", "NicolasKCost")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "stats.svg")

FONT = "Consolas, 'SFMono-Regular', 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New', monospace"
GREEN, CYAN, WHITE, GREY = "#00ff9c", "#56d4ff", "#e6edf3", "#7d8590"
LANG_COLORS = {"PHP": "#4F5D95", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#663399",
               "Python": "#3572A5", "Shell": "#89e051", "TypeScript": "#3178c6", "Hack": "#878787"}


def get(url, data=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def contribuicoes():
    if not TOKEN:
        return None
    q = """query($u:String!){ user(login:$u){ contributionsCollection{
      totalCommitContributions totalPullRequestContributions
      contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } } } } }"""
    body = json.dumps({"query": q, "variables": {"u": USER}}).encode()
    try:
        c = get("https://api.github.com/graphql", body)["data"]["user"]["contributionsCollection"]
    except Exception as ex:  # o card continua a sair, só sem estes números
        print("graphql falhou:", ex)
        return None
    dias = [d["contributionCount"] for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    seq = 0
    # o dia de hoje pode ainda não ter contribuições: não parte a sequência
    for i, n in enumerate(reversed(dias)):
        if n > 0:
            seq += 1
        elif i > 0:
            break
    return {"total": c["contributionCalendar"]["totalContributions"],
            "commits": c["totalCommitContributions"],
            "prs": c["totalPullRequestContributions"], "seq": seq}


def main():
    u = get(f"https://api.github.com/users/{USER}")
    repos = [r for r in get(f"https://api.github.com/users/{USER}/repos?per_page=100") if not r["fork"]]
    estrelas = sum(r["stargazers_count"] for r in repos)
    langs = {}
    for r in repos:
        if r["name"] == USER:
            continue
        for k, v in get(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    c = contribuicoes()
    desde = u["created_at"][:4]

    info = [
        ("SO", "Lisboa, Portugal (x86_64)"),
        ("Cargo", "Desenvolvedor Web Júnior"),
        ("Shell", "php · javascript · mysql"),
        ("Repos", f"{u['public_repos']} públicos · {estrelas} estrelas"),
        ("Seguidores", str(u["followers"])),
        ("Contribuições", f"{c['total']} no último ano" if c else "—"),
        ("Commits", f"{c['commits']} no último ano" if c else "—"),
        ("Sequência", f"{c['seq']} dia(s) seguidos" if c else "—"),
        ("No GitHub desde", desde),
    ]

    # "NK" em pixel art (rects, para não depender da fonte de quem vê)
    glifos = {"N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
              "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"]}
    px, lx0, ly0 = 22, 40, 92
    pix = []
    for gi, g in enumerate("NK"):
        for r, linha in enumerate(glifos[g]):
            for col, b in enumerate(linha):
                if b == "1":
                    d = 0.05 * (r + col + gi * 5)
                    pix.append(f'<rect class="px" style="animation-delay:{d:.2f}s" x="{lx0 + (gi*6 + col)*px}" y="{ly0 + r*px}" width="{px-3}" height="{px-3}" rx="2" fill="{GREEN}"/>')

    W, x0, y0, lh = 900, 330, 92, 23
    rows = [f'<text x="{x0}" y="{y0}" font-size="16" font-weight="bold"><tspan fill="{GREEN}">nicolas</tspan><tspan fill="{WHITE}">@</tspan><tspan fill="{GREEN}">github</tspan></text>',
            f'<text x="{x0}" y="{y0+14}" font-size="14" fill="{GREY}">──────────────────</text>']
    y = y0 + 38
    for i, (k, v) in enumerate(info):
        rows.append(f'<text class="fade" style="animation-delay:{0.8+i*0.12:.2f}s" x="{x0}" y="{y}" font-size="14.5">'
                    f'<tspan fill="{CYAN}">{escape(k)}</tspan><tspan fill="{WHITE}">: {escape(v)}</tspan></text>')
        y += lh
    y += 8
    rows.append(f'<text class="fade" style="animation-delay:2s" x="{x0}" y="{y}" font-size="14.5" fill="{CYAN}">Linguagens</text>')
    bx, bw = x0 + 110, 420
    acc = 0
    bars, legend = [], []
    for i, (k, v) in enumerate(top):
        w = bw * v / total
        bars.append(f'<rect x="{bx+acc:.1f}" y="{y-12}" width="{w:.1f}" height="12" fill="{LANG_COLORS.get(k, "#8b949e")}"/>')
        legend.append((k, 100 * v / total))
        acc += w
    rows.append(f'<g class="grow" style="animation-delay:2.1s"><clipPath id="lb"><rect x="{bx}" y="{y-12}" width="{bw}" height="12" rx="6"/></clipPath><g clip-path="url(#lb)">{"".join(bars)}</g></g>')
    y += 22
    lx = x0
    for i, (k, pct) in enumerate(legend):
        rows.append(f'<g class="fade" style="animation-delay:{2.4+i*0.1:.2f}s"><circle cx="{lx+5}" cy="{y-4}" r="5" fill="{LANG_COLORS.get(k, "#8b949e")}"/>'
                    f'<text x="{lx+15}" y="{y}" font-size="12.5" fill="{GREY}">{escape(k)} {pct:.0f}%</text></g>')
        lx += len(k) * 7.5 + 62
    y += 26
    pal = ["#0a0e14", "#ff5f56", "#27c93f", "#ffbd2e", "#56d4ff", "#c678dd", "#00ff9c", "#e6edf3"]
    rows.append('<g class="fade" style="animation-delay:3s">' + "".join(
        f'<rect x="{x0+i*28}" y="{y-14}" width="28" height="16" fill="{c}"/>' for i, c in enumerate(pal)) + "</g>")
    H = y + 40
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <style>
    text {{ font-family: {FONT}; }}
    .fade {{ opacity: 0; animation: fade .5s ease-out forwards; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    .grow {{ transform: scaleX(0); transform-box: fill-box; transform-origin: left; animation: grow 1s cubic-bezier(.2,.8,.2,1) forwards; }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    .logo {{ animation: flick 4s infinite; }}
    @keyframes flick {{ 0%,92%,100% {{ opacity: 1; }} 93% {{ opacity: .4; }} 94% {{ opacity: 1; }} 96% {{ opacity: .6; }} }}
    .px {{ opacity: 0; animation: fade .3s ease-out forwards; }}
    .blink {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>
  <defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#0a0e14" stroke="#1f3b2d" stroke-width="2"/>
  <path d="M1 11 a10 10 0 0 1 10 -10 H{W-11} a10 10 0 0 1 10 10 V34 H1 Z" fill="#161b22"/>
  <circle cx="20" cy="17.5" r="6" fill="#ff5f56"/><circle cx="40" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="60" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{W/2}" y="22" text-anchor="middle" font-size="13" fill="{GREY}">~/stats — neofetch</text>
  <text x="24" y="62" font-size="15"><tspan fill="{GREEN}">nicolas@lisboa:~$ </tspan><tspan fill="{WHITE}"> neofetch --github</tspan></text>
  <g class="logo" filter="url(#glow)">{"".join(pix)}</g>
  <text x="{lx0 + 5.5*px}" y="{ly0 + 7*px + 30}" text-anchor="middle" font-size="14" fill="{GREY}">&lt;/&gt; código · café</text>
  {"".join(rows)}
  <text x="{W-24}" y="{H-14}" text-anchor="end" font-size="11" fill="#4b5563">atualizado {agora}</text>
  <rect class="blink" x="24" y="{H-28}" width="9" height="16" fill="{GREEN}"/>
</svg>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("ok stats.svg", "(com contribuições)" if c else "(sem token: sem contribuições)")


if __name__ == "__main__":
    main()

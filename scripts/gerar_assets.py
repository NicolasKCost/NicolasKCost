"""Gera os SVGs animados do README (estética terminal/hacker).

Uso: python scripts/gerar_assets.py   (escreve em assets/)
O card de estatísticas é gerado à parte por .github/scripts/gen_stats.py.
"""
import os
import random
from html import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(7)

FONT = "Consolas, 'SFMono-Regular', 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New', monospace"
BG, PANEL, BAR, BORDER = "#0a0e14", "#0d1117", "#161b22", "#1f3b2d"
GREEN, GREEN_DIM, CYAN, YELLOW, RED, WHITE, GREY = (
    "#00ff9c", "#1f8a5b", "#56d4ff", "#e3b341", "#ff5f56", "#e6edf3", "#7d8590")


def e(s):
    return escape(s, quote=True)


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("ok", name)


def base_style(extra=""):
    return f"""<style>
    text {{ font-family: {FONT}; }}
    .fade {{ opacity: 0; animation: fade .5s ease-out forwards; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    .blink {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .pulse {{ animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(.75); }} }}
    {extra}
  </style>"""


def window(w, h, title):
    """Moldura de terminal com barra de título e os três botões."""
    return f"""<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 11 a10 10 0 0 1 10 -10 H{w-11} a10 10 0 0 1 10 10 V34 H1 Z" fill="{BAR}"/>
  <line x1="1" y1="34" x2="{w-1}" y2="34" stroke="{BORDER}"/>
  <circle cx="20" cy="17.5" r="6" fill="#ff5f56"/><circle cx="40" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="60" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{w/2}" y="22" text-anchor="middle" font-size="13" fill="{GREY}">{e(title)}</text>"""


def scanlines(w, h):
    return f"""<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity=".035"/></pattern></defs>
  <rect x="2" y="35" width="{w-4}" height="{h-37}" fill="url(#scan)" pointer-events="none"/>"""


def prompt(x, y, cmd, delay=0.0, size=15, cw=None):
    """Linha de prompt que se escreve sozinha (largura fixada com textLength)."""
    cw = cw or size * 0.6
    user = "nicolas@lisboa:~$"
    n = len(cmd)
    w = n * cw
    dur = max(0.4, n * 0.045)
    return f"""<g>
    <text x="{x}" y="{y}" font-size="{size}" fill="{GREEN}" class="fade" style="animation-delay:{delay}s" textLength="{len(user)*cw}" lengthAdjust="spacingAndGlyphs">{e(user)}</text>
    <text x="{x+(len(user)+1)*cw}" y="{y}" font-size="{size}" fill="{WHITE}" textLength="{w}" lengthAdjust="spacingAndGlyphs"
      style="clip-path: inset(0 100% 0 0); animation: typeonce {dur}s steps({n}) {delay+0.3}s forwards">{e(cmd)}</text>
  </g>"""


TYPE_ONCE = "@keyframes typeonce { to { clip-path: inset(0 0 0 0); } }"


# ---------------------------------------------------------------- banner
def banner():
    W, H = 900, 300
    cols = []
    chars = "01ABCDEF0123456789<>/{}$#=+*"
    for i, x in enumerate(range(14, W, 26)):
        n = random.randint(10, 18)
        s = "".join(random.choice(chars) for _ in range(n))
        dur = random.uniform(5, 11)
        delay = -random.uniform(0, dur)
        op = random.choice([.18, .25, .35, .5])
        tsp = "".join(f'<tspan x="{x}" dy="17">{e(c)}</tspan>' for c in s)
        cols.append(
            f'<text font-size="14" fill="{GREEN}" opacity="{op}" class="rain" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s" y="-{n*17}">{tsp}</text>')
    rain = "\n    ".join(cols)
    name = "NICOLAS KAIKY COSTA"
    extra = TYPE_ONCE + """
    .rain { animation: rain linear infinite; }
    @keyframes rain { from { transform: translateY(0); } to { transform: translateY(620px); } }
    .g1 { animation: g1 3.5s infinite steps(1); }
    .g2 { animation: g2 3.5s infinite steps(1); }
    @keyframes g1 { 0%,88%,100% { transform: none; opacity: 0; } 89% { transform: translate(-4px,-2px); opacity: .9; clip-path: inset(10% 0 55% 0); } 91% { transform: translate(5px,1px); opacity: .9; clip-path: inset(60% 0 10% 0); } 93% { transform: translate(-2px,0); opacity: .9; clip-path: inset(35% 0 40% 0); } 95% { opacity: 0; } }
    @keyframes g2 { 0%,88%,100% { transform: none; opacity: 0; } 89% { transform: translate(4px,2px); opacity: .9; clip-path: inset(50% 0 20% 0); } 91% { transform: translate(-5px,-1px); opacity: .9; clip-path: inset(5% 0 70% 0); } 93% { transform: translate(3px,0); opacity: .9; clip-path: inset(70% 0 5% 0); } 95% { opacity: 0; } }
    .shake { animation: shake 3.5s infinite steps(1); }
    @keyframes shake { 0%,88%,96%,100% { transform: none; } 90% { transform: translateX(2px); } 92% { transform: translateX(-2px); } }"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(extra)}
  <defs>
    <clipPath id="body"><rect x="2" y="35" width="{W-4}" height="{H-37}" rx="8"/></clipPath>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <radialGradient id="vig" cx="50%" cy="55%" r="60%"><stop offset="0" stop-color="{BG}" stop-opacity=".92"/><stop offset=".7" stop-color="{BG}" stop-opacity=".55"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
  </defs>
  {window(W, H, "nicolas@lisboa: ~/perfil — bash")}
  <g clip-path="url(#body)">
    {rain}
    <rect x="0" y="35" width="{W}" height="{H}" fill="url(#vig)"/>
  </g>
  {prompt(30, 70, "./apresentar.sh --modo=hacker", 0.2)}
  <g text-anchor="middle" font-size="50" font-weight="bold" style="letter-spacing:3px">
    <g class="fade" style="animation-delay:1.8s">
      <text class="shake" x="{W/2}" y="160" fill="{WHITE}" filter="url(#glow)">{name}</text>
      <text class="g1" x="{W/2}" y="160" fill="#ff0055">{name}</text>
      <text class="g2" x="{W/2}" y="160" fill="#00e5ff">{name}</text>
    </g>
  </g>
  <text class="fade" style="animation-delay:2.3s" x="{W/2}" y="204" text-anchor="middle" font-size="19" fill="{GREEN}">&lt; Desenvolvedor Web Júnior /&gt;</text>
  <g class="fade" style="animation-delay:2.7s" font-size="14" fill="{GREY}">
    <circle class="pulse" cx="{W/2-215}" cy="245" r="5" fill="{GREEN}"/>
    <text x="{W/2-202}" y="250">online</text>
    <text x="{W/2-140}" y="250">·  PHP · JavaScript · MySQL · APIs REST  ·  Lisboa</text>
  </g>
  {scanlines(W, H)}
</svg>"""
    write("banner.svg", svg)


# ---------------------------------------------------------------- typing (loop)
def typing():
    W, H = 900, 56
    lines = [
        "Desenvolvedor Web Júnior em Lisboa",
        "PHP · JavaScript · MySQL · APIs REST",
        "4 projetos web em produção, do zero ao servidor",
        "Helpdesk + 8 anos de design → agora código",
        "Disponível de imediato",
    ]
    slot = 4.0
    total = slot * len(lines)
    size, cw = 18, 10.8
    x0 = 52
    parts, css = [], [f".cur {{ animation: blink .8s step-end infinite; }}"]
    for i, t in enumerate(lines):
        n = len(t)
        a = 100 * slot / total  # % que cada linha ocupa
        typ = a * 0.35
        css.append(
            f"@keyframes t{i} {{ 0% {{ clip-path: inset(0 100% 0 0); opacity: 1; }} {typ:.2f}% {{ clip-path: inset(0 0 0 0); }} "
            f"{a*0.92:.2f}% {{ clip-path: inset(0 0 0 0); opacity: 1; }} {a:.2f}%,100% {{ opacity: 0; }} }}")
        css.append(
            f"@keyframes c{i} {{ 0% {{ transform: translateX(0); opacity: 1; }} {typ:.2f}% {{ transform: translateX({n*cw}px); }} "
            f"{a*0.92:.2f}% {{ transform: translateX({n*cw}px); opacity: 1; }} {a:.2f}%,100% {{ opacity: 0; transform: translateX({n*cw}px); }} }}")
        timing = f"{total}s infinite {i*slot}s"
        parts.append(
            f'<text x="{x0}" y="35" font-size="{size}" fill="{GREEN}" textLength="{n*cw}" lengthAdjust="spacingAndGlyphs" '
            f'style="opacity:0; animation: t{i} {timing}; animation-timing-function: steps({n})">{e(t)}</text>')
        parts.append(
            f'<g style="opacity:0; animation: c{i} {timing}; animation-timing-function: steps({n})"><rect class="cur" x="{x0+2}" y="20" width="10" height="20" fill="{GREEN}"/></g>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(" ".join(css))}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <text x="24" y="35" font-size="{size}" fill="{CYAN}">❯</text>
  {"\n  ".join(parts)}
</svg>"""
    write("typing.svg", svg)


# ---------------------------------------------------------------- perfil.json (estilo VS Code)
def perfil():
    K, S, N, P, C, B = "#9cdcfe", "#ce9178", "#b5cea8", "#d4d4d4", "#6a9955", "#569cd6"
    L = [
        [("// whoami --verbose", C)],
        [("{", P)],
        [("  \"nome\"", K), (": ", P), ("\"Nicolas Kaiky Costa\"", S), (",", P)],
        [("  \"cargo\"", K), (": ", P), ("\"Desenvolvedor Web Júnior\"", S), (",", P)],
        [("  \"local\"", K), (": ", P), ("\"Lisboa, Portugal\"", S), (",", P)],
        [("  \"stack\"", K), (": [", P), ("\"PHP\"", S), (", ", P), ("\"JavaScript\"", S), (", ", P), ("\"MySQL\"", S), (", ", P), ("\"APIs REST\"", S), ("],", P)],
        [("  \"ferramentas\"", K), (": [", P), ("\"Git\"", S), (", ", P), ("\"Linux/SSH\"", S), (", ", P), ("\"WordPress\"", S), (", ", P), ("\"Claude Code\"", S), ("],", P)],
        [("  \"experiencia\"", K), (": {", P)],
        [("    \"suporte\"", K), (": ", P), ("\"helpdesk e técnico de informática e sistemas\"", S), (",", P)],
        [("    \"design\"", K), (": ", P), ("\"8+ anos em design gráfico e digital\"", S), (",", P)],
        [("    \"dev\"", K), (": ", P), ("\"aplicações web da base de dados ao servidor\"", S)],
        [("  },", P)],
        [("  \"projetos_em_producao\"", K), (": ", P), ("4", N), (",", P)],
        [("  \"disponivel\"", K), (": ", P), ("true", B), (",", P)],
        [("  \"proxima_missao\"", K), (": ", P), ("\"primeira vaga como dev em Lisboa\"", S)],
        [("}", P)],
    ]
    W = 900
    top = 92
    lh = 21
    H = top + len(L) * lh + 46
    rows = []
    for i, segs in enumerate(L):
        y = top + i * lh
        tsp = "".join(f'<tspan fill="{c}">{e(t)}</tspan>' for t, c in segs)
        rows.append(
            f'<g class="fade" style="animation-delay:{0.25 + i*0.11:.2f}s">'
            f'<text x="88" y="{y}" font-size="13" fill="#4b5563" text-anchor="end">{i+1}</text>'
            f'<text x="104" y="{y}" font-size="14.5" xml:space="preserve">{tsp}</text></g>')
    last = top + (len(L) - 1) * lh
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style()}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#1e1e1e" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 11 a10 10 0 0 1 10 -10 H{W-11} a10 10 0 0 1 10 10 V34 H1 Z" fill="#181818"/>
  <circle cx="20" cy="17.5" r="6" fill="#ff5f56"/><circle cx="40" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="60" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{W/2}" y="22" text-anchor="middle" font-size="13" fill="{GREY}">perfil.json — nicolas — Visual Studio Code</text>
  <rect x="2" y="34" width="44" height="{H-58}" fill="#181818"/>
  <g fill="none" stroke="#6e7681" stroke-width="1.6">
    <rect x="15" y="50" width="16" height="19" rx="2"/><path d="M19 57 h8 M19 62 h8"/>
    <circle cx="22" cy="92" r="6"/><path d="M26.5 96.5 l5 5"/>
    <circle cx="18" cy="122" r="3"/><circle cx="28" cy="132" r="3"/><circle cx="18" cy="140" r="3"/><path d="M18 125 v12 M18 131 q0 -6 7 -1"/>
  </g>
  <rect x="2" y="46" width="2" height="26" fill="{GREEN}"/>
  <rect x="46" y="34" width="160" height="32" fill="#1e1e1e"/>
  <rect x="46" y="34" width="160" height="2" fill="{GREEN}"/>
  <rect x="206" y="34" width="{W-208}" height="32" fill="#181818"/>
  <text x="60" y="55" font-size="13" fill="#e5c07b">{{}}</text>
  <text x="84" y="55" font-size="13" fill="{WHITE}">perfil.json</text>
  <text x="186" y="55" font-size="13" fill="{GREY}">×</text>
  {"\n  ".join(rows)}
  <g class="fade" style="animation-delay:{0.25 + len(L)*0.11:.2f}s"><rect class="blink" x="{104 + 1*8.7:.0f}" y="{last-14}" width="2" height="18" fill="{WHITE}"/></g>
  <path d="M1 {H-24} H{W-1} V{H-11} a10 10 0 0 1 -10 10 H11 a10 10 0 0 1 -10 -10 Z" fill="#0e7a4d"/>
  <g font-size="12" fill="#ffffff">
    <text x="16" y="{H-8}">⎇ main</text>
    <text x="90" y="{H-8}">✓ 0 problemas</text>
    <text x="{W-400}" y="{H-8}">Ln {len(L)}, Col 2</text>
    <text x="{W-310}" y="{H-8}">UTF-8</text>
    <text x="{W-255}" y="{H-8}">JSON</text>
    <text x="{W-16}" y="{H-8}" text-anchor="end">● a compilar ideias</text>
  </g>
</svg>"""
    write("perfil.svg", svg)


# ---------------------------------------------------------------- stack (apt install)
def stack():
    pkgs = [
        ("php", "back-end, APIs e integrações"),
        ("javascript", "front-end e interatividade"),
        ("mysql", "modelação e consultas SQL"),
        ("html-css", "interfaces responsivas"),
        ("api-rest", "Gemini · Groq · Stripe · Google · Telegram"),
        ("wordpress", "plugins à medida"),
        ("linux-ssh", "servidores, deploy e cron"),
        ("git", "versionamento e GitHub"),
    ]
    W = 900
    top = 110
    lh = 28
    H = top + len(pkgs) * lh + 80
    rows = []
    for i, (name, desc) in enumerate(pkgs):
        y = top + i * lh
        d = 1.6 + i * 0.45
        rows.append(f"""<g class="fade" style="animation-delay:{d:.2f}s">
    <text x="30" y="{y}" font-size="15" fill="{CYAN}">{e(name)}</text>
    <rect x="160" y="{y-12}" width="220" height="14" rx="2" fill="#132019" stroke="{BORDER}"/>
    <rect class="grow" style="animation-delay:{d+0.1:.2f}s" x="162" y="{y-10}" width="216" height="10" rx="1" fill="url(#bar)"/>
    <text class="fade" style="animation-delay:{d+0.55:.2f}s" x="396" y="{y}" font-size="14" fill="{GREEN}">✓</text>
    <text class="fade" style="animation-delay:{d+0.55:.2f}s" x="420" y="{y}" font-size="14" fill="{GREY}">{e(desc)}</text>
  </g>""")
    end = 1.6 + len(pkgs) * 0.45 + 0.6
    yl = top + len(pkgs) * lh + 14
    extra = TYPE_ONCE + """
    .grow { transform: scaleX(0); transform-box: fill-box; transform-origin: left; animation: grow .5s cubic-bezier(.2,.8,.2,1) forwards; }
    @keyframes grow { to { transform: scaleX(1); } }"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(extra)}
  <defs><linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#0b6b43"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>
  {window(W, H, "~/stack — instalação de competências")}
  {prompt(30, 64, "sudo apt install nicolas-stack", 0.2)}
  <text class="fade" style="animation-delay:1.3s" x="30" y="88" font-size="14" fill="{GREY}">A ler listas de pacotes... Pronto</text>
  {"\n  ".join(rows)}
  <text class="fade" style="animation-delay:{end:.2f}s" x="30" y="{yl}" font-size="14" fill="{WHITE}">{len(pkgs)} pacotes instalados, 0 erros. <tspan fill="{GREEN}">Pronto para produção.</tspan></text>
  <g class="fade" style="animation-delay:{end+0.4:.2f}s">
    <text x="30" y="{yl+30}" font-size="15" fill="{GREEN}">nicolas@lisboa:~$</text>
    <rect class="blink" x="182" y="{yl+17}" width="9" height="17" fill="{GREEN}"/>
  </g>
  {scanlines(W, H)}
</svg>"""
    write("stack.svg", svg)


# ---------------------------------------------------------------- projetos
def projetos_header():
    W, H = 900, 70
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(TYPE_ONCE)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  {prompt(24, 30, "ls -la ~/projetos --em-producao", 0.1)}
  <text class="fade" style="animation-delay:1.8s" x="24" y="54" font-size="14" fill="{GREY}">total 4  ·  <tspan fill="{GREEN}">todos online</tspan>  ·  clica num cartão para abrir o repositório</text>
</svg>"""
    write("projetos.svg", svg)


def card(fname, title, status, desc, tags, url, delay):
    W, H = 440, 200
    tag_svg, x = [], 20
    for t in tags:
        w = len(t) * 7.2 + 16
        if x + w > W - 20:
            break
        tag_svg.append(
            f'<rect x="{x}" y="128" width="{w}" height="22" rx="4" fill="#0f2a1e" stroke="{GREEN_DIM}"/>'
            f'<text x="{x+8}" y="143" font-size="12" fill="{GREEN}" textLength="{len(t)*7.2}" lengthAdjust="spacingAndGlyphs">{e(t)}</text>')
        x += w + 6
    desc_svg = "".join(f'<text x="20" y="{84 + i*20}" font-size="13.5" fill="#c9d1d9">{e(l)}</text>' for i, l in enumerate(desc))
    extra = """
    .card { animation: border 3s ease-in-out infinite; }
    @keyframes border { 0%,100% { stroke: #1f3b2d; } 50% { stroke: #1f8a5b; } }
    .sweep { animation: sweep 4s linear infinite; }
    @keyframes sweep { from { transform: translateX(-120px); } to { transform: translateX(560px); } }"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(extra)}
  <defs>
    <linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".9"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
    <clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10"/></clipPath>
  </defs>
  <g class="fade" style="animation-delay:{delay}s">
  <rect class="card" x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <g clip-path="url(#c)"><rect class="sweep" style="animation-delay:{delay}s" x="0" y="1" width="120" height="2" fill="url(#sw)"/></g>
  <path d="M20 30 h10 l4 4 h14 v16 h-28 z" fill="none" stroke="{YELLOW}" stroke-width="1.8"/>
  <text x="58" y="48" font-size="19" font-weight="bold" fill="{WHITE}">{e(title)}</text>
  <circle class="pulse" cx="{W-82}" cy="42" r="5" fill="{GREEN}"/>
  <text x="{W-70}" y="47" font-size="13" fill="{GREEN}">{e(status)}</text>
  {desc_svg}
  {"".join(tag_svg)}
  <text x="20" y="181" font-size="13" fill="{CYAN}">→ {e(url)}</text>
  </g>
</svg>"""
    write(fname, svg)


# ---------------------------------------------------------------- jornada (git log --graph)
def jornada():
    commits = [
        # (hash, ano, tipo, mensagem, destaque)
        ("???????", "em breve", "feat", "primeira vaga como dev em Lisboa", "next"),
        ("4f9c2ad", "2026", "feat", "Um CV por Vaga, MovAI-Fit e Zágora em produção", "head"),
        ("b71e0c3", "2020", "perf", "automatiza o envio de ~850 boletos", ""),
        ("9a3d5f1", "2017", "feat", "técnico de informática e sistemas na ASSC Saúde", ""),
        ("e28b6c4", "2015", "feat", "helpdesk (Contax) e aulas de informática (Cinética)", ""),
        ("1c0ffee", "2011", "init", "design gráfico em gráficas e comunicação visual", ""),
    ]
    W = 900
    top = 100
    lh = 44
    H = top + len(commits) * lh + 10
    gx = 44
    rows = []
    for i, (h, ano, tipo, msg, kind) in enumerate(commits):
        y = top + i * lh
        d = 1.4 + i * 0.35
        if kind == "next":
            dot = f'<circle class="blink" cx="{gx}" cy="{y-5}" r="7" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="3 3"/>'
            hc, mc = GREY, GREY
        else:
            dot = f'<circle cx="{gx}" cy="{y-5}" r="7" fill="{BG}" stroke="{GREEN}" stroke-width="2.5"/><circle cx="{gx}" cy="{y-5}" r="3" fill="{GREEN}"/>'
            hc, mc = YELLOW, WHITE
        ref = ""
        if kind == "head":
            ref = f'<tspan fill="{YELLOW}">(</tspan><tspan fill="{CYAN}">HEAD -&gt; </tspan><tspan fill="{GREEN}">main</tspan><tspan fill="{YELLOW}">) </tspan>'
        rows.append(f"""<g class="fade" style="animation-delay:{d:.2f}s">{dot}
    <text x="{gx+24}" y="{y}" font-size="14.5" xml:space="preserve"><tspan fill="{hc}">{h}</tspan>  {ref}<tspan fill="{CYAN}">[{ano}]</tspan>  <tspan fill="{GREEN}">{tipo}:</tspan> <tspan fill="{mc}">{e(msg)}</tspan></text></g>""")
    line_len = (len(commits) - 1) * lh
    extra = TYPE_ONCE + f"""
    .draw {{ stroke-dasharray: {line_len}; stroke-dashoffset: {line_len}; animation: draw 2.2s ease-out 1.3s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(extra)}
  {window(W, H, "~/carreira — git log")}
  {prompt(24, 64, "git log --graph --oneline carreira", 0.2)}
  <line x1="{gx}" y1="{top-5}" x2="{gx}" y2="{top-5+line_len}" stroke="#123524" stroke-width="3"/>
  <line class="draw" x1="{gx}" y1="{top-5+line_len}" x2="{gx}" y2="{top-5}" stroke="{GREEN_DIM}" stroke-width="3"/>
  {"\n  ".join(rows)}
  {scanlines(W, H)}
</svg>"""
    write("jornada.svg", svg)


# ---------------------------------------------------------------- snake header, contacto, botões, rodapé
def snake_header():
    W, H = 900, 48
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(TYPE_ONCE)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  {prompt(24, 30, "./snake --comer=contribuicoes", 0.1)}
</svg>"""
    write("snake-header.svg", svg)


def contacto():
    W, H = 900, 150
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(TYPE_ONCE)}
  {window(W, H, "~/contacto — ssh")}
  {prompt(30, 66, "ssh visitante@nicolas", 0.2)}
  <text class="fade" style="animation-delay:1.5s" x="30" y="92" font-size="14" fill="{GREY}">A estabelecer ligação segura... <tspan fill="{GREEN}">[ OK ]</tspan></text>
  <text class="fade" style="animation-delay:2.1s" x="30" y="116" font-size="14" fill="{WHITE}">Ligação aberta. Tens uma vaga, projeto ou ideia? Escolhe um canal:</text>
  <g class="fade" style="animation-delay:2.6s"><rect class="blink" x="30" y="126" width="9" height="16" fill="{GREEN}"/></g>
  {scanlines(W, H)}
</svg>"""
    write("contacto.svg", svg)


def botao(fname, label):
    W, H = 220, 52
    extra = """
    .b { animation: glow 2.4s ease-in-out infinite; }
    @keyframes glow { 0%,100% { stroke: #1f8a5b; } 50% { stroke: #00ff9c; } }"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(extra)}
  <rect class="b" x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="8" fill="{BG}" stroke-width="2"/>
  <text x="{W/2}" y="32" text-anchor="middle" font-size="16" fill="{GREEN}"><tspan fill="{GREY}">[</tspan> {e(label)} <tspan fill="{GREY}">]</tspan></text>
</svg>"""
    write(fname, svg)


def rodape():
    W, H = 900, 90
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {base_style(TYPE_ONCE)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  {prompt(24, 32, "exit", 0.3)}
  <text class="fade" style="animation-delay:1s" x="24" y="56" font-size="14" fill="{GREY}">logout · obrigado pela visita <tspan fill="{GREEN}">:)</tspan></text>
  <text class="fade" style="animation-delay:1.5s" x="24" y="76" font-size="13" fill="#4b5563">[processo terminado com código 0] <tspan class="blink" fill="{GREEN}">█</tspan></text>
</svg>"""
    write("rodape.svg", svg)


if __name__ == "__main__":
    banner()
    typing()
    perfil()
    stack()
    projetos_header()
    card("proj-cvporvaga.svg", "Um CV por Vaga", "online",
         ["SaaS que adapta o CV a cada vaga com IA,", "sem inventar dados, e envia a candidatura."],
         ["PHP", "JavaScript", "MySQL", "Gemini", "OAuth", "Stripe"], "umcvporvaga.pt", 0.1)
    card("proj-movaifit.svg", "MovAI-Fit", "online",
         ["PWA de treino com planos gerados por IA", "e área para personal trainers."],
         ["PHP", "JavaScript", "Groq API", "PWA"], "movaifit.me", 0.3)
    card("proj-boletos.svg", "Portal de Boletos", "em uso",
         ["Plugin WordPress para uma clínica: importa PDFs,", "envia por e-mail e tem área do cliente."],
         ["PHP", "WordPress", "Composer"], "plugin para cliente", 0.5)
    card("proj-zagora.svg", "Zágora", "online",
         ["Bot de finanças pessoais no Telegram com IA", "e testes automáticos."],
         ["PHP", "MySQL", "Telegram API", "IA"], "zagora.space", 0.7)
    jornada()
    snake_header()
    contacto()
    botao("btn-linkedin.svg", "linkedin")
    botao("btn-site.svg", "umcvporvaga.pt")
    rodape()

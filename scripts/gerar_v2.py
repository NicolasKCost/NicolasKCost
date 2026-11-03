"""Versão 2 do README: mais animação (tudo em loop) e partes clicáveis.

Uso: python scripts/gerar_v2.py   (escreve em assets/v2/)
Reaproveita as peças da versão 1 (scripts/gerar_assets.py).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gerar_assets as v1  # noqa: E402
from gerar_assets import (BG, BORDER, CYAN, GREEN, GREEN_DIM, GREY, TYPE_ONCE, WHITE, YELLOW,  # noqa: E402
                          base_style, e, prompt, scanlines, window)

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "v2")
os.makedirs(OUT, exist_ok=True)
random.seed(42)


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("ok v2/" + name)


def svg_open(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'


# ---------------------------------------------------------------- hero: boot -> desencriptar nome (loop)
def hero():
    W, H, T = 900, 340, 16.0
    pc = lambda s: f"{100 * s / T:.3f}%"  # segundos -> % do ciclo
    boot = [
        ("OK", "A montar /dev/cafe"),
        ("OK", "A carregar módulo php.ko"),
        ("OK", "A carregar módulo javascript.ko"),
        ("OK", "A ligar ao mysql na porta 3306"),
        ("OK", "A iniciar servidor web (nginx)"),
        ("OK", "A verificar 4 projetos em produção"),
        ("..", "A procurar vaga de dev em Lisboa"),
    ]
    css = []
    rows = []
    for i, (st, txt) in enumerate(boot):
        a = 0.2 + i * 0.28
        css.append(f"@keyframes b{i} {{ 0%,{pc(a)} {{ opacity: 0; }} {pc(a+0.05)},{pc(3.1)} {{ opacity: 1; }} {pc(3.4)},100% {{ opacity: 0; }} }}")
        cor = GREEN if st == "OK" else YELLOW
        rows.append(f'<text x="34" y="{78 + i*24}" font-size="15" style="animation: b{i} {T}s infinite" xml:space="preserve">'
                    f'<tspan fill="{GREY}">[</tspan><tspan fill="{cor}"> {st} </tspan><tspan fill="{GREY}">]</tspan>  <tspan fill="{WHITE}">{e(txt)}</tspan></text>')
    # barra de arranque
    css.append(f"@keyframes boot {{ 0% {{ transform: scaleX(0); opacity: 1; }} {pc(2.9)} {{ transform: scaleX(1); opacity: 1; }} {pc(3.4)},100% {{ transform: scaleX(1); opacity: 0; }} }}")
    css.append(f"@keyframes bootf {{ 0%,{pc(2.9)} {{ opacity: 1; }} {pc(3.4)},100% {{ opacity: 0; }} }}")
    # nome a desencriptar: cada letra passa por caracteres aleatórios
    name = "NICOLAS KAIKY COSTA"
    cw, size = 31.0, 50
    x0 = W / 2 - len(name) * cw / 2
    lixo = "#$%&@!?<>/\\{}[]01ABCDEFXZ"
    letras = []
    start = 3.5
    for i, ch in enumerate(name):
        if ch == " ":
            continue
        x = x0 + i * cw
        fim = start + 0.35 + i * 0.07
        n = 6
        for k in range(n):
            a, b = start + (fim - start) * k / n, start + (fim - start) * (k + 1) / n
            g = random.choice(lixo)
            nm = f"s{i}_{k}"
            css.append(f"@keyframes {nm} {{ 0%,{pc(a)} {{ opacity: 0; }} {pc(a+0.02)},{pc(b)} {{ opacity: 1; }} {pc(b+0.02)},100% {{ opacity: 0; }} }}")
            letras.append(f'<text x="{x}" y="175" font-size="{size}" font-weight="bold" fill="{GREEN}" text-anchor="middle" style="opacity:0;animation:{nm} {T}s infinite">{e(g)}</text>')
        nm = f"r{i}"
        css.append(f"@keyframes {nm} {{ 0%,{pc(fim)} {{ opacity: 0; }} {pc(fim+0.02)},{pc(T-0.6)} {{ opacity: 1; }} {pc(T-0.3)},100% {{ opacity: 0; }} }}")
        letras.append(f'<text x="{x}" y="175" font-size="{size}" font-weight="bold" fill="{WHITE}" filter="url(#glow)" text-anchor="middle" style="opacity:0;animation:{nm} {T}s infinite">{e(ch)}</text>')
    nome_ok = start + 0.35 + len(name) * 0.07
    css.append(f"@keyframes sub {{ 0%,{pc(nome_ok+0.2)} {{ opacity: 0; transform: translateY(6px); }} {pc(nome_ok+0.6)},{pc(T-0.6)} {{ opacity: 1; transform: none; }} {pc(T-0.3)},100% {{ opacity: 0; }} }}")
    css.append(f"@keyframes ok {{ 0%,{pc(nome_ok)} {{ opacity: 0; transform: scale(1.4); }} {pc(nome_ok+0.25)} {{ opacity: 1; transform: scale(1); }} {pc(nome_ok+1.6)} {{ opacity: 1; }} {pc(nome_ok+2)},100% {{ opacity: 0; }} }}")
    css.append(f"@keyframes glitch {{ 0%,{pc(nome_ok+3)},{pc(nome_ok+3.25)},{pc(nome_ok+6)},{pc(nome_ok+6.2)},100% {{ opacity: 0; transform: none; }} "
               f"{pc(nome_ok+3.05)} {{ opacity: .9; transform: translate(-5px,-2px); clip-path: inset(10% 0 55% 0); }} "
               f"{pc(nome_ok+3.15)} {{ opacity: .9; transform: translate(5px,2px); clip-path: inset(60% 0 8% 0); }} "
               f"{pc(nome_ok+6.1)} {{ opacity: .9; transform: translate(4px,-1px); clip-path: inset(30% 0 40% 0); }} }}")
    # chuva de fundo (mesma técnica da v1)
    cols = []
    for x in range(14, W, 22):
        nch = random.randint(10, 18)
        s = "".join(random.choice("01ABCDEF<>/{}$#") for _ in range(nch))
        dur = random.uniform(4, 10)
        tsp = "".join(f'<tspan x="{x}" dy="17">{e(c)}</tspan>' for c in s)
        cols.append(f'<text font-size="14" fill="{GREEN}" opacity="{random.choice([.12, .2, .3, .45])}" class="rain" '
                    f'style="animation-duration:{dur:.2f}s;animation-delay:-{random.uniform(0, dur):.2f}s" y="-{nch*17}">{tsp}</text>')
    css.append(".rain { animation: rain linear infinite; } @keyframes rain { to { transform: translateY(660px); } }")
    css.append(f".sub {{ opacity: 0; animation: sub {T}s infinite; }} .ok {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: ok {T}s infinite; }}")
    css.append(f".gl {{ opacity: 0; animation: glitch {T}s infinite steps(1); }}")
    css.append(".sweep { animation: sweep 5s linear infinite; } @keyframes sweep { from { transform: translateY(-60px); } to { transform: translateY(360px); } }")
    final = "".join(f'<text x="{x0 + i*cw}" y="175" font-size="{size}" font-weight="bold" text-anchor="middle">{e(c)}</text>' for i, c in enumerate(name) if c != " ")
    svg = f"""{svg_open(W, H)}
  {base_style(" ".join(css))}
  <defs>
    <clipPath id="body"><rect x="2" y="35" width="{W-4}" height="{H-37}" rx="8"/></clipPath>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <radialGradient id="vig" cx="50%" cy="55%" r="60%"><stop offset="0" stop-color="{BG}" stop-opacity=".9"/><stop offset=".7" stop-color="{BG}" stop-opacity=".5"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
    <linearGradient id="sw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".12"/></linearGradient>
  </defs>
  {window(W, H, "NicolasOS v2.0 — tty1")}
  <g clip-path="url(#body)">
    {"".join(cols)}
    <rect x="0" y="35" width="{W}" height="{H}" fill="url(#vig)"/>
    <rect class="sweep" x="0" y="0" width="{W}" height="60" fill="url(#sw)"/>
  </g>
  {"".join(rows)}
  <g style="animation: bootf {T}s infinite">
    <rect x="34" y="262" width="400" height="10" rx="2" fill="#132019" stroke="{BORDER}"/>
    <rect x="35" y="263" width="398" height="8" fill="{GREEN}" style="transform-box: fill-box; transform-origin: left; animation: boot {T}s infinite"/>
    <text x="448" y="272" font-size="13" fill="{GREY}">a arrancar...</text>
  </g>
  {"".join(letras)}
  <g class="gl" fill="#ff0055">{final}</g>
  <g class="gl" fill="#00e5ff" style="animation-delay:.05s">{final}</g>
  <g class="ok"><rect x="{W/2-110}" y="64" width="220" height="30" rx="4" fill="#0f2a1e" stroke="{GREEN}"/>
    <text x="{W/2}" y="85" text-anchor="middle" font-size="15" font-weight="bold" fill="{GREEN}">ACESSO CONCEDIDO</text></g>
  <g class="sub">
    <text x="{W/2}" y="222" text-anchor="middle" font-size="20" fill="{GREEN}">&lt; Desenvolvedor Web Júnior /&gt;</text>
    <circle class="pulse" cx="{W/2-215}" cy="262" r="5" fill="{GREEN}"/>
    <text x="{W/2-202}" y="267" font-size="14" fill="{GREY}">online  ·  PHP · JavaScript · MySQL · APIs REST  ·  Lisboa</text>
    <text x="{W/2}" y="310" text-anchor="middle" font-size="12" fill="#4b5563">↓ desliza para explorar o sistema ↓</text>
  </g>
  {scanlines(W, H)}
</svg>"""
    write("hero.svg", svg)


# ---------------------------------------------------------------- menu (cada botão é um link para uma secção)
def botao_menu(fname, num, label):
    W, H = 168, 44
    extra = f""".b {{ animation: glow 2.4s ease-in-out infinite; animation-delay: {num*0.3}s; }}
    @keyframes glow {{ 0%,100% {{ stroke: #1f8a5b; fill: {BG}; }} 50% {{ stroke: #00ff9c; fill: #0f2a1e; }} }}"""
    svg = f"""{svg_open(W, H)}
  {base_style(extra)}
  <rect class="b" x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="6" stroke-width="2"/>
  <text x="14" y="27" font-size="14" fill="{GREY}">{num:02d}</text>
  <text x="40" y="27" font-size="15" fill="{GREEN}">./{e(label)}</text>
</svg>"""
    write(fname, svg)


# ---------------------------------------------------------------- VS Code a escrever código PHP (loop)
def codigo():
    K, S, F, V, C, P, T_ = "#c586c0", "#ce9178", "#dcdcaa", "#9cdcfe", "#6a9955", "#d4d4d4", "#4ec9b0"
    L = [
        [("<?php", K)],
        [("// Um CV por Vaga — a parte mais importante", C)],
        [("function ", K), ("adaptarCV", F), ("(", P), ("array ", T_), ("$cv", V), (", ", P), ("string ", T_), ("$vaga", V), ("): ", P), ("array", T_)],
        [("{", P)],
        [("    $requisitos", V), (" = ", P), ("extrairRequisitos", F), ("(", P), ("$vaga", V), (");", P)],
        [("    $prompt", V), (" = ", P), ("montarPrompt", F), ("(", P), ("$cv", V), (", ", P), ("$requisitos", V), (");", P)],
        [("    $resposta", V), (" = ", P), ("Gemini", T_), ("::", P), ("gerar", F), ("(", P), ("$prompt", V), (");", P)],
        [("", P)],
        [("    // regra de ouro: nunca inventar dados", C)],
        [("    return ", K), ("validarSemInventar", F), ("(", P), ("$cv", V), (", ", P), ("$resposta", V), (");", P)],
        [("}", P)],
    ]
    W, top, lh, cw, size = 900, 92, 22, 8.7, 14.5
    por_letra = 0.03
    escrita = sum(max(1, len("".join(s for s, _ in segs))) * por_letra + 0.15 for segs in L)
    T = round(0.4 + escrita + 0.3 + 6, 1)  # escrever + terminal + ~4s parado no fim
    pc = lambda s: f"{100 * s / T:.3f}%"
    css, rows = [], []
    t = 0.4
    for i, segs in enumerate(L):
        txt = "".join(s for s, _ in segs)
        n = max(1, len(txt))
        dur = n * por_letra
        y = top + i * lh
        css.append(f"@keyframes l{i} {{ 0%,{pc(t)} {{ clip-path: inset(0 100% 0 0); }} {pc(t+dur)},{pc(T-0.8)} {{ clip-path: inset(0 0 0 0); opacity: 1; }} {pc(T-0.4)},100% {{ clip-path: inset(0 0 0 0); opacity: 0; }} }}")
        css.append(f"@keyframes k{i} {{ 0%,{pc(t)} {{ opacity: 0; transform: translateX(0); }} {pc(t+0.02)} {{ opacity: 1; transform: translateX(0); }} "
                   f"{pc(t+dur)} {{ opacity: 1; transform: translateX({len(txt)*cw}px); }} {pc(t+dur+0.02)},100% {{ opacity: 0; transform: translateX({len(txt)*cw}px); }} }}")
        tsp = "".join(f'<tspan fill="{c}">{e(s)}</tspan>' for s, c in segs)
        rows.append(f'<text x="88" y="{y}" font-size="13" fill="#4b5563" text-anchor="end">{i+1}</text>')
        if txt:
            rows.append(f'<text x="104" y="{y}" font-size="{size}" xml:space="preserve" textLength="{len(txt)*cw}" lengthAdjust="spacingAndGlyphs" '
                        f'style="clip-path: inset(0 100% 0 0); animation: l{i} {T}s infinite steps({n * 3})">{tsp}</text>')
            rows.append(f'<rect x="104" y="{y-14}" width="2" height="18" fill="{WHITE}" style="opacity:0; animation: k{i} {T}s infinite steps({n * 3})"/>')
        t += dur + 0.15
    # painel do terminal por baixo
    ty = top + len(L) * lh + 22
    tt = t + 0.3
    css.append(f"@keyframes term {{ 0%,{pc(tt)} {{ opacity: 0; }} {pc(tt+0.2)},{pc(T-0.8)} {{ opacity: 1; }} {pc(T-0.4)},100% {{ opacity: 0; }} }}")
    css.append(f"@keyframes term2 {{ 0%,{pc(tt+0.9)} {{ opacity: 0; }} {pc(tt+1.1)},{pc(T-0.8)} {{ opacity: 1; }} {pc(T-0.4)},100% {{ opacity: 0; }} }}")
    css.append(f"@keyframes term3 {{ 0%,{pc(tt+1.6)} {{ opacity: 0; }} {pc(tt+1.8)},{pc(T-0.8)} {{ opacity: 1; }} {pc(T-0.4)},100% {{ opacity: 0; }} }}")
    H = ty + 104
    svg = f"""{svg_open(W, H)}
  {base_style(" ".join(css))}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="#1e1e1e" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 11 a10 10 0 0 1 10 -10 H{W-11} a10 10 0 0 1 10 10 V34 H1 Z" fill="#181818"/>
  <circle cx="20" cy="17.5" r="6" fill="#ff5f56"/><circle cx="40" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="60" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{W/2}" y="22" text-anchor="middle" font-size="13" fill="{GREY}">adaptarCV.php — um-cv-por-vaga — Visual Studio Code</text>
  <rect x="2" y="34" width="{W-4}" height="32" fill="#181818"/>
  <rect x="46" y="34" width="170" height="32" fill="#1e1e1e"/><rect x="46" y="34" width="170" height="2" fill="{GREEN}"/>
  <text x="60" y="55" font-size="13" fill="#a074c4">php</text>
  <text x="90" y="55" font-size="13" fill="{WHITE}">adaptarCV.php</text>
  <circle cx="200" cy="50" r="4" fill="{WHITE}" class="pulse"/>
  <rect x="2" y="66" width="44" height="{H-68}" fill="#181818"/>
  {"".join(rows)}
  <line x1="46" y1="{ty-18}" x2="{W-2}" y2="{ty-18}" stroke="#2b2b2b"/>
  <text x="62" y="{ty}" font-size="12" fill="{WHITE}">TERMINAL</text><rect x="62" y="{ty+4}" width="62" height="1.5" fill="{GREEN}"/>
  <text x="140" y="{ty}" font-size="12" fill="{GREY}">PROBLEMAS   SAÍDA</text>
  <g font-size="14">
    <text x="62" y="{ty+28}" style="opacity:0; animation: term {T}s infinite"><tspan fill="{GREEN}">nicolas@lisboa:~$</tspan><tspan fill="{WHITE}"> php -l adaptarCV.php</tspan></text>
    <text x="62" y="{ty+50}" fill="{GREY}" style="opacity:0; animation: term2 {T}s infinite">No syntax errors detected in adaptarCV.php</text>
    <text x="62" y="{ty+72}" style="opacity:0; animation: term3 {T}s infinite"><tspan fill="{GREEN}">✓ </tspan><tspan fill="{WHITE}">deploy feito → </tspan><tspan fill="{CYAN}">umcvporvaga.pt</tspan></text>
  </g>
</svg>"""
    write("codigo.svg", svg)


# ---------------------------------------------------------------- htop com medidores sempre a mexer (loop)
def htop():
    W = 900
    cores = [("php", .92), ("javascript", .85), ("mysql", .78), ("html/css", .8), ("apis rest", .75),
             ("wordpress", .6), ("linux/ssh", .65), ("git", .8)]
    css = [".m { transform-box: fill-box; transform-origin: left; animation: m ease-in-out infinite alternate; }"]
    rows = []
    for i, (nome, base) in enumerate(cores):
        col, lin = i % 2, i // 2
        x, y = 30 + col * 430, 78 + lin * 26
        lo, hi = base - .07, min(1, base + .03)  # oscilação pequena, só para parecer vivo
        css.append(f"@keyframes v{i} {{ 0% {{ transform: scaleX({lo}); }} 35% {{ transform: scaleX({hi}); }} 60% {{ transform: scaleX({(lo+hi)/2:.2f}); }} 100% {{ transform: scaleX({hi-.03:.2f}); }} }}")
        dur = random.uniform(5, 8)
        n = 34
        rows.append(f"""<text x="{x}" y="{y}" font-size="14" fill="{CYAN}">{i+1}</text>
    <text x="{x+18}" y="{y}" font-size="14" fill="{WHITE}">{e(nome)}</text>
    <text x="{x+120}" y="{y}" font-size="14" fill="{GREY}">[</text>
    <g clip-path="url(#m{i})"><text x="{x+132}" y="{y}" font-size="14" fill="url(#hg)" textLength="{n*7.6}" lengthAdjust="spacingAndGlyphs">{"|"*n}</text></g>
    <clipPath id="m{i}"><rect class="m" style="animation-name:v{i};animation-duration:{dur:.2f}s" x="{x+132}" y="{y-14}" width="{n*7.6}" height="18"/></clipPath>
    <text x="{x+132+n*7.6+4}" y="{y}" font-size="14" fill="{GREY}">]</text>""")
    # gráfico de atividade a deslizar
    gy, gh, gw = 210, 70, 840
    pts = []
    for k in range(0, 2 * gw + 1, 12):
        v = .5 + .3 * math.sin(k / 37) + .15 * math.sin(k / 11) + random.uniform(-.06, .06)
        pts.append(f"{30 + k},{gy + gh - v * gh:.1f}")
    linha = " ".join(pts)
    css.append(f".graf {{ animation: graf 12s linear infinite; }} @keyframes graf {{ to {{ transform: translateX(-{gw}px); }} }}")
    procs = [
        ("1337", "nicolas", "procura_vaga_dev", "R", GREEN),
        ("2048", "nicolas", "um-cv-por-vaga", "S", WHITE),
        ("2049", "nicolas", "movai-fit", "S", WHITE),
        ("2050", "nicolas", "zagora-bot", "S", WHITE),
        ("4096", "nicolas", "aprender --sempre", "R", GREEN),
    ]
    py = gy + gh + 46
    prow = [f'<rect x="20" y="{py-17}" width="{W-40}" height="22" fill="#0e7a4d"/>'
            f'<text x="30" y="{py}" font-size="13.5" fill="#ffffff" xml:space="preserve">  PID USER      S  CPU%  COMANDO</text>']
    css.append(".cpu { animation: blink 1.3s step-end infinite; }")
    for i, (pid, u, cmd, st, cor) in enumerate(procs):
        y = py + 24 + i * 22
        cpu = f"{random.uniform(30, 99):.1f}" if st == "R" else f"{random.uniform(0.1, 3):.1f}"
        alt = f"{random.uniform(30, 99):.1f}" if st == "R" else cpu
        prow.append(f'<text x="30" y="{y}" font-size="13.5" fill="{cor}" xml:space="preserve">{pid:>5} {u:<9} {st}  '
                    f'<tspan class="cpu">{cpu:>5}</tspan>  {e(cmd)}</text>'
                    f'<text x="30" y="{y}" font-size="13.5" fill="{cor}" xml:space="preserve" class="cpu" style="animation-delay:.65s;opacity:0"></text>')
    H = py + 24 + len(procs) * 22 + 40
    svg = f"""{svg_open(W, H)}
  {base_style(" ".join(css))}
  <defs>
    <linearGradient id="hg" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".7" stop-color="{YELLOW}"/><stop offset="1" stop-color="#ff5f56"/></linearGradient>
    <linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".35"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
    <clipPath id="gc"><rect x="30" y="{gy}" width="{gw}" height="{gh}"/></clipPath>
  </defs>
  {window(W, H, "htop — competências em tempo real")}
  {"".join(rows)}
  <text x="30" y="{gy-10}" font-size="13" fill="{GREY}">atividade (commits · deploys · café)</text>
  <rect x="30" y="{gy}" width="{gw}" height="{gh}" fill="#0b1510" stroke="{BORDER}"/>
  <g stroke="#123524">{"".join(f'<line x1="30" y1="{gy + k*gh/4}" x2="{30+gw}" y2="{gy + k*gh/4}"/>' for k in range(1, 4))}</g>
  <g clip-path="url(#gc)"><g class="graf">
    <polygon points="30,{gy+gh} {linha} {30+2*gw},{gy+gh}" fill="url(#ga)"/>
    <polyline points="{linha}" fill="none" stroke="{GREEN}" stroke-width="2"/>
  </g></g>
  {"".join(prow)}
  <text x="30" y="{H-16}" font-size="13" fill="{GREY}" xml:space="preserve">Tarefas: <tspan fill="{WHITE}">5</tspan>, <tspan fill="{GREEN}">2 a correr</tspan>   Carga: <tspan fill="{WHITE}">alta</tspan>   Uptime: <tspan fill="{WHITE}">desde 2011 a resolver problemas</tspan></text>
  {scanlines(W, H)}
</svg>"""
    write("htop.svg", svg)


# ---------------------------------------------------------------- globo a rodar com Lisboa marcada (loop)
def globo():
    W, H = 900, 300
    cx, cy, r = 190, 165, 105
    css = [".rot { animation: rot 8s linear infinite; }",
           ".ping { transform-box: fill-box; transform-origin: center; animation: ping 2s ease-out infinite; }",
           "@keyframes ping { from { transform: scale(.3); opacity: 1; } to { transform: scale(3); opacity: 0; } }",
           ".radar { transform-origin: 190px 165px; animation: radar 4s linear infinite; } @keyframes radar { to { transform: rotate(360deg); } }"]
    # meridianos: elipses cujo rx varia para simular rotação
    mer = []
    for k in range(6):
        nm = f"mr{k}"
        steps = []
        for s in range(0, 101, 5):
            ang = (s / 100) * math.pi + k * math.pi / 6
            steps.append(f"{s}% {{ rx: {abs(math.cos(ang)) * r:.1f}px; }}")
        css.append(f"@keyframes {nm} {{ {' '.join(steps)} }}")
        mer.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{GREEN_DIM}" stroke-width="1.2" style="animation: {nm} 9s linear infinite"/>')
    par = "".join(f'<ellipse cx="{cx}" cy="{cy + r*math.sin(a)}" rx="{r*math.cos(a):.1f}" ry="{r*math.cos(a)*0.18:.1f}" fill="none" stroke="{GREEN_DIM}" stroke-width="1"/>'
                  for a in [-1.0, -0.5, 0, 0.5, 1.0])
    lx, ly = cx - 18, cy - 48  # Lisboa (38.7N), aproximado
    info = [
        ("ALVO", "Nicolas Kaiky Costa"),
        ("LOCAL", "Lisboa, Portugal"),
        ("COORD", "38.72° N · 9.14° W"),
        ("FUSO", "WET (UTC+0)"),
        ("MODO", "presencial · híbrido · remoto"),
        ("ESTADO", "disponível de imediato"),
    ]
    rows = []
    for i, (k, v) in enumerate(info):
        rows.append(f'<g class="fade" style="animation-delay:{0.6 + i*0.25:.2f}s"><text x="380" y="{92 + i*30}" font-size="15" xml:space="preserve">'
                    f'<tspan fill="{CYAN}">{k:<7}</tspan><tspan fill="{GREY}">: </tspan><tspan fill="{GREEN if k == "ESTADO" else WHITE}">{e(v)}</tspan></text></g>')
    svg = f"""{svg_open(W, H)}
  {base_style(" ".join(css))}
  <defs>
    <radialGradient id="gl" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#0f3d2a"/><stop offset="1" stop-color="{BG}"/></radialGradient>
    <linearGradient id="rd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".45"/></linearGradient>
    <clipPath id="gcp"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  </defs>
  {window(W, H, "geoloc --alvo nicolas")}
  <circle cx="{cx}" cy="{cy}" r="{r+16}" fill="none" stroke="{BORDER}" stroke-dasharray="2 6"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gl)" stroke="{GREEN}" stroke-width="1.5"/>
  <g clip-path="url(#gcp)">{par}{"".join(mer)}
    <path class="radar" d="M{cx} {cy} L{cx+r} {cy} A{r} {r} 0 0 0 {cx + r*math.cos(-0.6):.1f} {cy + r*math.sin(-0.6):.1f} Z" fill="url(#rd)"/>
  </g>
  <circle class="ping" cx="{lx}" cy="{ly}" r="6" fill="none" stroke="{GREEN}" stroke-width="2"/>
  <circle cx="{lx}" cy="{ly}" r="4" fill="{GREEN}"/>
  <line x1="{lx}" y1="{ly}" x2="{lx-60}" y2="{ly-40}" stroke="{GREEN}" stroke-width="1"/>
  <text x="{lx-62}" y="{ly-46}" font-size="12" fill="{GREEN}" text-anchor="end">LISBOA</text>
  {"".join(rows)}
  <g class="fade" style="animation-delay:2.4s"><text x="380" y="{H-22}" font-size="13" fill="{GREY}">sinal localizado <tspan fill="{GREEN}">✓</tspan>  a transmitir <tspan class="blink" fill="{GREEN}">█</tspan></text></g>
  {scanlines(W, H)}
</svg>"""
    write("globo.svg", svg)


# ---------------------------------------------------------------- cartões de projeto (com scan e barra de uptime)
def card(fname, title, desc, tags, url, seed):
    W, H = 900, 144
    random.seed(seed)
    tag_svg, x = [], 20
    for t in tags:
        w = len(t) * 7.2 + 16
        tag_svg.append(f'<rect x="{x}" y="90" width="{w}" height="22" rx="4" fill="#0f2a1e" stroke="{GREEN_DIM}"/>'
                       f'<text x="{x+8}" y="105" font-size="12" fill="{GREEN}" textLength="{len(t)*7.2}" lengthAdjust="spacingAndGlyphs">{e(t)}</text>')
        x += w + 6
    barras = "".join(
        f'<rect x="{W/2 - 60 + k*10}" y="{H-30}" width="7" height="10" rx="1" fill="{GREEN}" opacity="{random.choice([.5, .7, .9, 1])}"/>' for k in range(24))
    desc_svg = f'<text x="20" y="76" font-size="14" fill="#c9d1d9">{e(" ".join(desc))}</text>'
    extra = """
    .card { animation: border 3s ease-in-out infinite; }
    @keyframes border { 0%,100% { stroke: #1f3b2d; } 50% { stroke: #00ff9c; } }
    .scan { animation: scan 3.5s ease-in-out infinite; }
    @keyframes scan { 0% { transform: translateY(0); opacity: 0; } 10% { opacity: .8; } 90% { opacity: .8; } 100% { transform: translateY(150px); opacity: 0; } }
    .up { animation: up 1.5s steps(1) infinite; } @keyframes up { 50% { opacity: .35; } }"""
    svg = f"""{svg_open(W, H)}
  {base_style(extra)}
  <defs><linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".25"/></linearGradient>
    <clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10"/></clipPath></defs>
  <rect class="card" x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <g clip-path="url(#c)"><rect class="scan" x="0" y="-30" width="{W}" height="30" fill="url(#sc)"/></g>
  <path d="M20 30 h10 l4 4 h14 v16 h-28 z" fill="none" stroke="{YELLOW}" stroke-width="1.8"/>
  <text x="58" y="48" font-size="19" font-weight="bold" fill="{WHITE}">{e(title)}</text>
  <circle class="pulse" cx="{W-82}" cy="42" r="5" fill="{GREEN}"/>
  <text x="{W-70}" y="47" font-size="13" fill="{GREEN}">online</text>
  {desc_svg}
  {"".join(tag_svg)}
  <text x="20" y="{H-20}" font-size="13" fill="{CYAN}">→ {e(url)}</text>
  <text x="{W-20}" y="{H-20}" font-size="13" fill="{GREEN}" text-anchor="end">▸ clica para ver detalhes</text>
  <g class="up">{barras}</g>
  <text x="{W/2 - 70}" y="{H-21}" font-size="11" fill="{GREY}" text-anchor="end">uptime</text>
</svg>"""
    write(fname, svg)


# ---------------------------------------------------------------- snake que come o percurso (loop)
def snake_percurso():
    comidas = [  # (texto no placar, rótulo curto, cor) por ordem cronológica
        ("design gráfico (gráficas)", "design", YELLOW),
        ("aulas de informática", "aulas", YELLOW),
        ("helpdesk (Contax)", "helpdesk", YELLOW),
        ("técnico de sistemas (ASSC)", "sistemas", YELLOW),
        ("automação de ~850 boletos", "automação", YELLOW),
        ("PHP", "PHP", CYAN),
        ("JavaScript", "JS", CYAN),
        ("MySQL", "MySQL", CYAN),
        ("APIs REST + IA", "APIs + IA", CYAN),
        ("deploy umcvporvaga.pt", "deploy", GREEN),
        ("deploy movaifit.me", "deploy", GREEN),
        ("deploy zagora.space", "deploy", GREEN),
    ]
    cols, rows, passo, lado, gx, gy = 30, 17, 16, 13, 24, 56
    caminho = []
    for c in range(cols):
        for r in (range(rows) if c % 2 == 0 else range(rows - 1, -1, -1)):
            caminho.append((gx + c * passo, gy + r * passo))
    dt = 0.03
    fim_cobra = len(caminho) * dt
    T = round(fim_cobra + 5, 1)
    pc = lambda s: f"{100 * s / T:.3f}%"
    idx = [14 + j * 40 for j in range(len(comidas))]
    tempos = [i * dt for i in idx]
    css, cels, comida_svg, pops, log = [], [], [], [], []
    for (x, y) in caminho:
        cels.append(f'<rect x="{x}" y="{y}" width="{lado}" height="{lado}" rx="3" fill="#161b22"/>')
    lx, ly, llh = 540, 92, 15
    for j, ((txt, curto, cor), i, t) in enumerate(zip(comidas, idx, tempos)):
        x, y = caminho[i]
        css.append(f"@keyframes f{j} {{ 0%,{pc(t)} {{ opacity: 1; }} {pc(t+0.05)},99% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}")
        comida_svg.append(f'<g style="animation: f{j} {T}s infinite"><rect class="pulse" x="{x}" y="{y}" width="{lado}" height="{lado}" rx="3" fill="{cor}"/></g>')
        css.append(f"@keyframes p{j} {{ 0%,{pc(t)} {{ opacity: 0; transform: translateY(0); }} {pc(t+0.1)} {{ opacity: 1; }} {pc(t+1.2)},100% {{ opacity: 0; transform: translateY(-22px); }} }}")
        px = min(max(x + lado / 2, gx + 30), gx + cols * passo - 40)
        pops.append(f'<text x="{px}" y="{y - 4}" text-anchor="middle" font-size="12" font-weight="bold" fill="{cor}" style="opacity:0; animation: p{j} {T}s infinite">+1 {e(curto)}</text>')
        css.append(f"@keyframes l{j} {{ 0%,{pc(t)} {{ opacity: 0; }} {pc(t+0.15)},{pc(T-0.5)} {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
        log.append(f'<text x="{lx}" y="{ly + j * llh}" font-size="12.5" style="opacity:0; animation: l{j} {T}s infinite" xml:space="preserve">'
                   f'<tspan fill="{GREY}">[{j+1:02d}]</tspan> <tspan fill="{cor}">+1</tspan> <tspan fill="{WHITE}">{e(txt)}</tspan></text>')
    # cobra: cresce um segmento por cada coisa que come
    base = 3
    seg = []
    for k in range(base + len(comidas)):
        atraso = k * dt
        mov = f"animation: cobra {T}s linear infinite; animation-delay: -{T - atraso:.3f}s" if k else f"animation: cobra {T}s linear infinite"
        corpo = f'<rect width="{lado}" height="{lado}" rx="{4 if k == 0 else 3}" fill="{GREEN}" opacity="{max(.35, 1 - k*0.045):.2f}" style="{mov}"/>'
        if k >= base:
            t = tempos[k - base]
            css.append(f"@keyframes g{k} {{ 0%,{pc(t)} {{ opacity: 0; }} {pc(t+0.02)},{pc(fim_cobra + 0.6)} {{ opacity: 1; }} {pc(fim_cobra + 0.7)},100% {{ opacity: 0; }} }}")
            corpo = f'<g style="opacity:0; animation: g{k} {T}s infinite">{corpo}</g>'
        seg.append(corpo)
    quadros = [f"{pc(i*dt)} {{ transform: translate({x}px,{y}px); }}" for i, (x, y) in enumerate(caminho)]
    ux, uy = caminho[-1]
    quadros.append(f"{pc(fim_cobra)},100% {{ transform: translate({ux}px,{uy - 90}px); }}")  # sai por cima
    css.append("@keyframes cobra { " + " ".join(quadros) + " }")
    # barra de XP sobe a cada comida
    xp = ["0% { transform: scaleX(0); }"] + [f"{pc(t)} {{ transform: scaleX({j/len(comidas):.3f}); }} {pc(t+0.02)} {{ transform: scaleX({(j+1)/len(comidas):.3f}); }}" for j, t in enumerate(tempos)]
    xp.append(f"{pc(T-0.5)} {{ transform: scaleX(1); }} 100% {{ transform: scaleX(0); }}")
    css.append("@keyframes xp { " + " ".join(xp) + " }")
    fim = tempos[-1] + 0.6
    css.append(f"@keyframes fim {{ 0%,{pc(fim)} {{ opacity: 0; }} {pc(fim+0.3)},{pc(T-0.5)} {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
    W = 900
    yb = ly + len(comidas) * llh + 10
    H = max(gy + rows * passo + 18, yb + 58)
    svg = f"""{svg_open(W, H)}
  {base_style(TYPE_ONCE + " " + " ".join(css))}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  {prompt(24, 34, "./snake --comer=percurso", 0.1)}
  {"".join(cels)}
  {"".join(comida_svg)}
  <g>{"".join(reversed(seg))}</g>
  {"".join(pops)}
  <line x1="{lx-16}" y1="52" x2="{lx-16}" y2="{H-18}" stroke="{BORDER}"/>
  <text x="{lx}" y="70" font-size="13" fill="{CYAN}">~/xp.log</text>
  {"".join(log)}
  <text x="{lx}" y="{yb + 4}" font-size="12" fill="{GREY}">XP</text>
  <rect x="{lx+26}" y="{yb - 6}" width="300" height="10" rx="2" fill="#132019" stroke="{BORDER}"/>
  <rect x="{lx+27}" y="{yb - 5}" width="298" height="8" fill="url(#xpg)" style="transform-box: fill-box; transform-origin: left; animation: xp {T}s infinite"/>
  <defs><linearGradient id="xpg" x1="0" x2="1"><stop offset="0" stop-color="#0b6b43"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>
  <g style="opacity:0; animation: fim {T}s infinite" font-size="12.5">
    <text x="{lx}" y="{yb + 24}" fill="{WHITE}">nível atual: <tspan fill="{GREEN}">Desenvolvedor Web Júnior</tspan></text>
    <text x="{lx}" y="{yb + 40}" fill="{WHITE}">próximo nível: <tspan fill="{YELLOW}">a tua equipa?</tspan> <tspan class="blink" fill="{GREEN}">█</tspan></text>
  </g>
</svg>"""
    write("snake.svg", svg)


# ---------------------------------------------------------------- ficheiro secreto (cabeçalho do <details>)
def secreto():
    W, H = 900, 64
    lixo = "".join(random.choice("0123456789abcdef") for _ in range(56))
    extra = """.scr { animation: scr .12s steps(1) infinite; } @keyframes scr { 50% { transform: translateX(3px); opacity: .6; } }
    .lock { animation: lock 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; } @keyframes lock { 50% { transform: rotate(-8deg); } }"""
    svg = f"""{svg_open(W, H)}
  {base_style(extra)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="#5c1a2a" stroke-width="2" stroke-dasharray="6 4"/>
  <g class="lock" fill="none" stroke="#ff5f56" stroke-width="2"><rect x="24" y="28" width="20" height="16" rx="2"/><path d="M28 28 v-5 a6 6 0 0 1 12 0 v5"/></g>
  <text x="60" y="30" font-size="15" fill="#ff5f56">segredo.enc  ·  ACESSO RESTRITO</text>
  <text class="scr" x="60" y="50" font-size="12" fill="{GREY}">{lixo}</text>
  <text x="{W-24}" y="40" font-size="14" fill="{GREEN}" text-anchor="end">▸ clica para desencriptar</text>
</svg>"""
    write("secreto.svg", svg)


if __name__ == "__main__":
    hero()
    for i, (f, lbl) in enumerate([("menu-sobre.svg", "sobre"), ("menu-codigo.svg", "codigo"), ("menu-projetos.svg", "projetos"),
                                  ("menu-carreira.svg", "carreira"), ("menu-contacto.svg", "contacto")], 1):
        botao_menu(f, i, lbl)
    codigo()
    htop()
    globo()
    card("proj-cvporvaga.svg", "Um CV por Vaga",
         ["SaaS que adapta o CV a cada vaga com IA,", "sem inventar dados, e envia a candidatura."],
         ["PHP", "JavaScript", "MySQL", "Gemini", "OAuth", "Stripe"], "umcvporvaga.pt", 1)
    card("proj-movaifit.svg", "MovAI-Fit",
         ["PWA de treino com planos gerados por IA", "e área para personal trainers."],
         ["PHP", "JavaScript", "Groq API", "PWA"], "movaifit.me", 2)
    card("proj-boletos.svg", "Portal de Boletos",
         ["Plugin WordPress para uma clínica: importa PDFs,", "envia por e-mail e tem área do cliente."],
         ["PHP", "WordPress", "Composer"], "plugin para cliente", 3)
    card("proj-zagora.svg", "Zágora",
         ["Bot de finanças pessoais no Telegram com IA", "e testes automáticos."],
         ["PHP", "MySQL", "Telegram API", "IA"], "zagora.space", 4)
    secreto()
    snake_percurso()

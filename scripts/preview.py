"""Gera páginas locais para ver os READMEs como no GitHub (modo escuro). Não vão para o GitHub."""
import re

CSS = ("body{background:#0d1117;color:#e6edf3;font-family:-apple-system,Segoe UI,sans-serif;max-width:900px;margin:20px auto;padding:0 16px;line-height:1.5}"
       "img{max-width:100%}a{color:#4493f8}blockquote{border-left:4px solid #30363d;color:#8b949e;margin:16px 0;padding:0 1em}"
       "details{margin:6px 0}summary{cursor:pointer}pre{background:#161b22;padding:12px;border-radius:6px;overflow:auto}"
       ".add{color:#3fb950}")


def md(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"```diff\n(.*?)```", lambda m: "<pre>" + "".join(f'<span class="add">{l}</span>\n' for l in m.group(1).splitlines()) + "</pre>", s, flags=re.S)
    s = re.sub(r"^> (.*)$", r"<blockquote>\1</blockquote>", s, flags=re.M)
    s = re.sub(r"\*\*\[(.+?)\]\((.+?)\)\*\*", r'<b><a href="\2">\1</a></b>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s


for src, out in [("README.md", "preview.html")]:
    with open(src, encoding="utf-8") as f:
        html = md(f.read())
    with open(out, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><meta charset="utf-8"><title>{src}</title><style>{CSS}</style>{html}')

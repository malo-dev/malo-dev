"""
Génère les images du README GitHub (versions claire et sombre).
Modifie les sections PROFILE, PROJECTS et STACK, puis lance :  python generate.py
"""
import random, os, base64
from xml.sax.saxutils import escape

# ---------- À MODIFIER ----------
PROFILE = {
    "name": "Leader Mushio",
    "role": "R&D Engineer  ·  AI, Web, Mobile, Security",
    "place": "Spain  ·  Remote",
    "langs": "TypeScript, Python, Vue",
}

PROJECTS = [
    {"slug": "DataForge-Pro", "title": "DataForge Pro", "shot": "dataforge.png",
     "desc": "A JSON workbench in the browser: edit, validate, generate schemas, test API calls.",
     "stack": "Vue  ·  TypeScript  ·  Node.js"},
    {"slug": "admin-bim", "title": "BIM Next Console", "shot": "bim.png",
     "desc": "Admin console for a banking network: accounts, treasury flows, partner governance.",
     "stack": "Vue  ·  TypeScript  ·  Node.js"},
    {"slug": "leaderportfolio", "title": "Portfolio", "shot": "portfolio.png",
     "desc": "Personal site covering my AI, web, mobile and cybersecurity work.",
     "stack": "TypeScript  ·  React  ·  Vercel"},
]

STACK = [
    ("Daily",       ["TypeScript", "Python", "PHP", "React", "Next.js", "Node.js", "NestJS", "Laravel", "PostgreSQL", "MySQL", "Docker"]),
    ("Comfortable", ["Vue", "Express", "Flask", "Prisma", "MongoDB", "Firebase", "Tailwind", "Linux"]),
    ("Exploring",   ["PyTorch", "Hugging Face", "Cloud architecture", "App security"]),
]
# --------------------------------

THEMES = {
    "dark":  dict(bg="#0F1626", surface="#141D31", line="#26324B", text="#E8EBF0",
                  muted="#8F9AAE", accent="#D9AB4E", accent2="#3D5A8C", accent3="#22304D"),
    "light": dict(bg="#FFFFFF", surface="#F7F8FA", line="#E1E5EC", text="#17202E",
                  muted="#5A6477", accent="#A7781E", accent2="#2E4A7B", accent3="#DCE3EE"),
}
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"


def kuba(x0, y0, cols, rows, cell, seed, t, density=1.0):
    """Motif géométrique inspiré des tissus Kuba (RDC)."""
    rnd = random.Random(seed)
    fills = [t["accent"], t["accent2"], t["accent3"]]
    out = []
    for r in range(rows):
        for c in range(cols):
            x, y, s = x0 + c * cell, y0 + r * cell, cell
            if rnd.random() > density:
                continue
            m = rnd.choice([0, 0, 1, 1, 2, 3, 4, 5, 6])
            f = rnd.choice(fills)
            g = s * 0.12
            if m == 0:
                out.append(f'<path d="M{x} {y} L{x+s} {y+s} L{x} {y+s} Z" fill="{f}"/>')
            elif m == 1:
                out.append(f'<path d="M{x} {y} L{x+s} {y} L{x+s} {y+s} Z" fill="{f}"/>')
            elif m == 2:
                h = s / 2
                out.append(f'<path d="M{x+h} {y+g} L{x+s-g} {y+h} L{x+h} {y+s-g} L{x+g} {y+h} Z" fill="{f}"/>')
                if rnd.random() < .5:
                    q = s * .3
                    out.append(f'<path d="M{x+h} {y+h-q/2} L{x+h+q/2} {y+h} L{x+h} {y+h+q/2} L{x+h-q/2} {y+h} Z" fill="{t["bg"]}"/>')
            elif m == 3:
                for i in range(3):
                    yy = y + g + i * (s - 2 * g) / 3
                    out.append(f'<rect x="{x+g}" y="{yy:.1f}" width="{s-2*g}" height="{(s-2*g)/6:.1f}" fill="{f}"/>')
            elif m == 4:
                out.append(f'<path d="M{x} {y+s*.65} L{x+s/2} {y+s*.25} L{x+s} {y+s*.65} L{x+s} {y+s*.9} '
                           f'L{x+s/2} {y+s*.5} L{x} {y+s*.9} Z" fill="{f}"/>')
            elif m == 5:
                out.append(f'<rect x="{x+g*1.5}" y="{y+g*1.5}" width="{s-3*g}" height="{s-3*g}" fill="none" '
                           f'stroke="{f}" stroke-width="{g*.9:.1f}"/>')
            # m == 6 : vide, laisse respirer le motif
    return "\n".join(out)


def svg(w, h, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{escape(FONT)}">\n{body}\n</svg>\n')


def header(t):
    w, h = 1200, 320
    cell = 40
    band = kuba(720, 0, 12, 8, cell, 7, t, density=.92)
    p = PROFILE
    body = f'''
<clipPath id="r"><rect width="{w}" height="{h}" rx="18"/></clipPath>
<g clip-path="url(#r)">
  <rect width="{w}" height="{h}" fill="{t["bg"]}"/>
  {band}
  <rect x="716" y="0" width="4" height="{h}" fill="{t["accent"]}"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{t["line"]}"/>
<text x="64" y="132" font-size="58" font-weight="700" fill="{t["text"]}" letter-spacing="-1">{escape(p["name"])}</text>
<text x="66" y="180" font-size="24" fill="{t["text"]}">{escape(p["role"])}</text>
<rect x="66" y="210" width="44" height="3" fill="{t["accent"]}"/>
<text x="66" y="250" font-size="17" fill="{t["muted"]}">{escape(p["place"])}</text>
<text x="66" y="276" font-size="17" fill="{t["muted"]}">{escape(p["langs"])}</text>
'''
    return svg(w, h, body, t)


def divider(t):
    w, h, s = 1200, 20, 20
    out = []
    for i in range(w // s):
        x = i * s
        f = t["accent"] if i % 6 in (0, 1) else t["line"]
        if i % 2 == 0:
            out.append(f'<path d="M{x} {h} L{x+s/2} 0 L{x+s} {h} Z" fill="{f}"/>')
    return svg(w, h, "\n".join(out), t)


def card(p, i, t):
    w, h = 1200, 228
    shot = ""
    path = os.path.join("assets", "screens", p["shot"])
    if os.path.exists(path):
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        shot = (f'<image x="24" y="24" width="288" height="180" preserveAspectRatio="xMidYMin slice" '
                f'href="data:image/png;base64,{b64}"/>')
    else:
        shot = kuba(24, 24, 9, 5, 32, 100 + i * 17, t, density=1)
    body = f'''
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>
<clipPath id="c"><rect x="24" y="24" width="288" height="180" rx="10"/></clipPath>
<g clip-path="url(#c)"><rect x="24" y="24" width="288" height="180" fill="{t["bg"]}"/>{shot}</g>
<rect x="24.5" y="24.5" width="287" height="179" rx="10" fill="none" stroke="{t["line"]}"/>
<text x="344" y="76" font-size="30" font-weight="700" fill="{t["text"]}">{escape(p["title"])}</text>
<text x="344" y="118" font-size="19" fill="{t["muted"]}">{escape(p["desc"])}</text>
<text x="344" y="162" font-size="16" font-weight="600" fill="{t["accent"]}">{escape(p["stack"])}</text>
<text x="{w-48}" y="120" font-size="28" fill="{t["muted"]}" text-anchor="end">↗</text>
'''
    return svg(w, h, body, t)


def stack(t):
    w = 1200
    out, y = [], 40
    lx, px0, maxx = 40, 220, w - 40
    for label, items in STACK:
        x = px0
        out.append(f'<text x="{lx}" y="{y+26}" font-size="17" font-weight="600" fill="{t["text"]}">{escape(label)}</text>')
        for it in items:
            pw = int(len(it) * 9.6 + 36)
            if x + pw > maxx:
                x, y = px0, y + 54
            strong = label == "Daily"
            out.append(f'<rect x="{x}" y="{y}" width="{pw}" height="40" rx="20" '
                       f'fill="{t["surface"] if not strong else t["bg"]}" stroke="{t["accent"] if strong else t["line"]}"/>')
            out.append(f'<text x="{x+pw/2}" y="{y+26}" font-size="16" text-anchor="middle" '
                       f'fill="{t["text"] if strong else t["muted"]}">{escape(it)}</text>')
            x += pw + 10
        y += 54
        if label != STACK[-1][0]:
            out.append(f'<line x1="{lx}" x2="{maxx}" y1="{y+4}" y2="{y+4}" stroke="{t["line"]}"/>')
            y += 24
    h = y + 24
    body = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/>\n' + "\n".join(out)
    return svg(w, h, body, t)


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    for name, t in THEMES.items():
        open(f"assets/header-{name}.svg", "w", encoding="utf-8").write(header(t))
        open(f"assets/divider-{name}.svg", "w", encoding="utf-8").write(divider(t))
        open(f"assets/stack-{name}.svg", "w", encoding="utf-8").write(stack(t))
        for i, p in enumerate(PROJECTS):
            open(f"assets/project-{i+1}-{name}.svg", "w", encoding="utf-8").write(card(p, i, t))
    print("Images générées dans ./assets")

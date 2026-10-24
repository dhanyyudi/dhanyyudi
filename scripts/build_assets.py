"""Builds the README artwork in assets/ for both GitHub themes.

Run from the repository root:  python3 scripts/build_assets.py
Palette follows the Graphite terrain tokens used on dhanypedia.com.
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg="#141414", surface="#1e1f1c", fg="#f2f0e9", muted="#aaa99f",
                 accent="#b9c4b2", line="#383a33", ink="#f2f0e9", ink_op=0.11),
    "light": dict(bg="#f1f0e9", surface="#e5e5db", fg="#20231d", muted="#606357",
                  accent="#4d6246", line="#cccec1", ink="#20231d", ink_op=0.14),
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def blob(cx, cy, r, seed, n=96, squash=1.35):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + 0.16 * math.sin(3 * t + seed) + 0.09 * math.sin(5 * t + seed * 1.7) + 0.05 * math.cos(7 * t + seed * 0.6)
        out.append((cx + r * squash * k * math.cos(t), cy + r * k * math.sin(t)))
    return "M" + pts(out).replace(" ", " L") + "Z"


def contours(c, summits, step=14):
    paths = []
    for cx, cy, rings, seed in summits:
        for i in range(1, rings + 1):
            major = i % 5 == 0
            paths.append(
                f'<path d="{blob(cx, cy, step * i + i * i * 0.9, seed + i * 0.08)}" fill="none" '
                f'stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * (1.7 if major else 1):.3f}" '
                f'stroke-width="{1.2 if major else 0.8}"/>')
    return "\n".join(paths)


def write(name, theme, body):
    (OUT / f"{name}-{theme}.svg").write_text(body)


# ---------------------------------------------------------------- header

def header(theme, c):
    W, H = 1280, 300
    route = "M760,236 C820,214 846,170 902,160 S1000,182 1046,132 S1120,72 1196,88"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Dhany Yudi Prasetyo, Geospatial and GIS Engineer">
<style>
  .route {{ stroke-dasharray: 490; stroke-dashoffset: 490; animation: draw 3.2s cubic-bezier(.2,0,0,1) .4s forwards; }}
  .end {{ opacity: 0; animation: show .5s ease-out 3.4s forwards; }}
  .pulse {{ transform-origin: 1196px 88px; animation: pulse 2.8s ease-out 3.6s infinite; opacity: 0; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes show {{ to {{ opacity: 1; }} }}
  @keyframes pulse {{ 0% {{ transform: scale(.4); opacity: .6; }} 100% {{ transform: scale(2.6); opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .route {{ animation: none; stroke-dashoffset: 0; }} .end {{ animation: none; opacity: 1; }} .pulse {{ display: none; }}
  }}
</style>
<defs>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0.36" stop-color="{c["bg"]}" stop-opacity="1"/>
    <stop offset="0.6" stop-color="{c["bg"]}" stop-opacity="0"/>
  </linearGradient>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  {contours(c, [(1050, 140, 11, 0.4), (820, 290, 7, 2.1)])}
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <path class="route" d="{route}" fill="none" stroke="{c["accent"]}" stroke-width="2" stroke-linecap="round"/>
  <circle cx="760" cy="236" r="4" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>
  <circle class="pulse" cx="1196" cy="88" r="8" fill="none" stroke="{c["accent"]}" stroke-width="1.5"/>
  <g class="end">
    <circle cx="1196" cy="88" r="5" fill="{c["accent"]}"/>
    <text x="1180" y="66" text-anchor="end" fill="{c["muted"]}" font-family="{MONO}" font-size="11" letter-spacing="0.5">ETA 14 MIN · 6.2 KM</text>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{c["line"]}"/>
</g>
<g font-family="{SANS}">
  <text x="64" y="104" fill="{c["muted"]}" font-size="17" letter-spacing="2">DHANY YUDI PRASETYO</text>
  <text x="62" y="182" fill="{c["fg"]}" font-size="62" letter-spacing="-2.4">Geospatial <tspan fill="{c["accent"]}">&amp;</tspan> GIS Engineer</text>
</g>
<text x="64" y="236" fill="{c["muted"]}" fill-opacity="0.75" font-family="{MONO}" font-size="12" letter-spacing="0.5">06°12′S  106°49′E  ·  JAKARTA  ·  EPSG:4326</text>
</svg>
'''


# ---------------------------------------------------------------- numbers

STATS = [
    ("14", "vehicle classes in", "production OSRM profiles"),
    ("5", "Asian markets", "routed and maintained"),
    ("131.69 km", "toll corridor", "mapped with UAV LiDAR"),
    ("18", "published projects", "on dhanypedia.com"),
]


def numbers(theme, c):
    W, H = 1280, 150
    col = W / len(STATS)
    cells = []
    for i, (big, a, b) in enumerate(STATS):
        x = 32 + i * col
        rule = f'<line x1="{i * col:.0f}" y1="32" x2="{i * col:.0f}" y2="{H - 32}" stroke="{c["line"]}"/>' if i else ""
        cells.append(f'''{rule}
  <text x="{x:.0f}" y="70" fill="{c["fg"]}" font-family="{SANS}" font-size="40" letter-spacing="-1.4">{big}</text>
  <text x="{x:.0f}" y="100" fill="{c["muted"]}" font-family="{SANS}" font-size="15">{a}</text>
  <text x="{x:.0f}" y="120" fill="{c["muted"]}" font-family="{SANS}" font-size="15">{b}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="14 vehicle classes in production OSRM profiles, 5 Asian markets, 131.69 km toll corridor mapped with UAV LiDAR, 18 published projects">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>
  {"".join(cells)}
</svg>
'''


# ---------------------------------------------------------------- project cards

CW, CH = 640, 340
ART = (40, 32, CW - 40, 176)  # x0, y0, x1, y1 of the illustration band


def mesh(seed, cols=9, rows=4, jitter=0.32):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = ART
    dx, dy = (x1 - x0) / cols, (y1 - y0) / rows
    return [[(x0 + i * dx + (rnd.uniform(-jitter, jitter) * dx if 0 < i < cols else 0),
              y0 + j * dy + (rnd.uniform(-jitter, jitter) * dy if 0 < j < rows else 0))
             for i in range(cols + 1)] for j in range(rows + 1)]


def art_regions(c):
    g = mesh(3)
    faint = f'stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 2.2:.2f}"'
    cells = []
    for j in range(len(g) - 1):
        for i in range(len(g[0]) - 1):
            quad = [g[j][i], g[j][i + 1], g[j + 1][i + 1], g[j + 1][i]]
            hot = (i, j) in {(5, 1), (6, 1), (5, 2)}
            fill = f'fill="{c["accent"]}" fill-opacity="0.22"' if hot else 'fill="none"'
            cells.append(f'<polygon points="{pts(quad)}" {fill} {faint} stroke-width="1"/>')
    cx, cy = g[2][6]
    cells.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{c["accent"]}"/>')
    cells.append(f'<text x="{cx + 10:.1f}" y="{cy - 8:.1f}" fill="{c["muted"]}" font-family="{MONO}" font-size="11">32.73</text>')
    return "\n".join(cells)


def art_roads(c):
    g = mesh(11, cols=12, rows=5, jitter=0.22)
    out = []
    for j, row in enumerate(g[1:-1], 1):
        w, op = (2.4, 0.9) if j == 2 else (1, c["ink_op"] * 2.6)
        col = c["accent"] if j == 2 else c["ink"]
        out.append(f'<polyline points="{pts(row)}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="{w}"/>')
    for i in range(1, len(g[0]) - 1):
        colpts = [r[i] for r in g]
        w, op = (1.8, c["ink_op"] * 5) if i in (4, 9) else (0.8, c["ink_op"] * 2)
        out.append(f'<polyline points="{pts(colpts)}" fill="none" stroke="{c["ink"]}" stroke-opacity="{op:.2f}" stroke-width="{w}"/>')
    return "\n".join(out)


def art_route(c):
    g = mesh(7, cols=10, rows=4, jitter=0.3)
    out = []
    for j in range(len(g)):
        for i in range(len(g[0])):
            x, y = g[j][i]
            if i + 1 < len(g[0]):
                out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{g[j][i + 1][0]:.1f}" y2="{g[j][i + 1][1]:.1f}" stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 1.8:.2f}"/>')
            if j + 1 < len(g):
                out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{g[j + 1][i][0]:.1f}" y2="{g[j + 1][i][1]:.1f}" stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 1.8:.2f}"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="{c["ink"]}" fill-opacity="{c["ink_op"] * 3:.2f}"/>')
    path = [g[3][1], g[2][1], g[2][2], g[2][3], g[1][3], g[1][4], g[1][5], g[2][5], g[2][6], g[2][7], g[1][7], g[1][8], g[1][9]]
    out.append(f'<polyline points="{pts(path)}" fill="none" stroke="{c["accent"]}" stroke-width="2.4" stroke-linejoin="round"/>')
    (sx, sy), (ex, ey) = path[0], path[-1]
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" fill="{c["surface"]}" stroke="{c["accent"]}" stroke-width="2"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{c["accent"]}"/>')
    return "\n".join(out)


def art_seismic(c):
    x0, y0, x1, y1 = ART
    cx, cy = 420, 104
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["accent"]}" stroke-opacity="{0.9 - r / 110:.2f}" stroke-width="1.2"/>'
           for r in (10, 26, 46, 70, 98)]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{c["accent"]}"/>')
    wave = []
    for k in range(0, 300):
        x = x0 + k
        amp = 30 * math.exp(-((k - 150) / 40) ** 2)
        wave.append((x, 104 + amp * math.sin(k * 0.55)))
    out.append(f'<polyline points="{pts(wave)}" fill="none" stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 5:.2f}" stroke-width="1.2"/>')
    out.append(f'<line x1="{x0}" y1="104" x2="{x0 + 300}" y2="104" stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 1.6:.2f}"/>')
    out.append(f'<text x="{cx + 14}" y="{cy - 10}" fill="{c["muted"]}" font-family="{MONO}" font-size="11">M 5.3</text>')
    return "\n".join(out)


def art_elevation(c):
    x0, y0, x1, y1 = ART
    prof = []
    for k in range(0, x1 - x0 + 1, 4):
        t = k / (x1 - x0)
        h = 0.55 * math.sin(t * 3.1) + 0.25 * math.sin(t * 9 + 1) + 0.08 * math.sin(t * 31)
        prof.append((x0 + k, y1 - 20 - (h + 0.4) * 90))
    area = prof + [(x1, y1), (x0, y1)]
    out = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["ink"]}" stroke-opacity="{c["ink_op"] * 1.2:.2f}" stroke-dasharray="2 4"/>'
           for y in (y0 + 20, y0 + 60, y0 + 100)]
    out.append(f'<polygon points="{pts(area)}" fill="{c["accent"]}" fill-opacity="0.14"/>')
    out.append(f'<polyline points="{pts(prof)}" fill="none" stroke="{c["accent"]}" stroke-width="2"/>')
    peak = min(prof, key=lambda p: p[1])
    out.append(f'<circle cx="{peak[0]:.1f}" cy="{peak[1]:.1f}" r="4" fill="{c["accent"]}"/>')
    out.append(f'<text x="{peak[0] + 10:.1f}" y="{peak[1] - 6:.1f}" fill="{c["muted"]}" font-family="{MONO}" font-size="11">+412 m</text>')
    return "\n".join(out)


def art_trees(c):
    rnd = random.Random(5)
    x0, y0, x1, y1 = ART
    out = []
    for j in range(5):
        for i in range(19):
            x = x0 + 14 + i * 29 + rnd.uniform(-5, 5) + (j % 2) * 14
            y = y0 + 16 + j * 28 + rnd.uniform(-4, 4)
            if x > x1 - 8:
                continue
            r = rnd.uniform(5, 8)
            hit = rnd.random() < 0.18
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c["ink"]}" fill-opacity="{c["ink_op"] * 2.2:.2f}"/>')
            if hit:
                b = r + 4
                out.append(f'<rect x="{x - b:.1f}" y="{y - b:.1f}" width="{2 * b:.1f}" height="{2 * b:.1f}" fill="none" stroke="{c["accent"]}" stroke-width="1.4"/>')
    out.append(f'<text x="{x1}" y="{y1 + 4}" text-anchor="end" fill="{c["muted"]}" font-family="{MONO}" font-size="11">conf 0.87</text>')
    return "\n".join(out)


PROJECTS = [
    ("wilayah-id", "SPATIAL API", "Indonesian admin boundaries,", "region codes and postal codes", art_regions),
    ("osmroad", "ROAD DATA", "Open .osm.pbf road extracts in", "the browser, export GeoParquet", art_roads),
    ("valhalla-route-id", "ROUTING", "Valhalla routing tuned for", "Indonesian roads", art_route),
    ("bmkg-api", "OPEN DATA", "BMKG weather and earthquake", "feeds as JSON, with an MCP server", art_seismic),
    ("ridetopo", "CYCLING", "Round-trip bike routes with", "elevation profiles and GPX export", art_elevation),
    ("qgis-tree-counter", "GEOAI · QGIS", "Count trees in aerial imagery", "with YOLO, right inside QGIS", art_trees),
]


def card(c, name, label, d1, d2, art):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{name}: {d1} {d2}">
<defs>
  <linearGradient id="fx"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.14" stop-color="#fff"/><stop offset="0.86" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="fy" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.18" stop-color="#fff"/><stop offset="0.82" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="mx" maskUnits="userSpaceOnUse"><rect x="{ART[0] - 8}" y="0" width="{ART[2] - ART[0] + 16}" height="{CH}" fill="url(#fx)"/></mask>
  <mask id="my" maskUnits="userSpaceOnUse"><rect x="0" y="{ART[1] - 12}" width="{CW}" height="{ART[3] - ART[1] + 24}" fill="url(#fy)"/></mask>
</defs>
<rect x="0.5" y="0.5" width="{CW - 1}" height="{CH - 1}" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>
<g mask="url(#mx)"><g mask="url(#my)">
{art(c)}
</g></g>
<line x1="40" y1="200" x2="{CW - 40}" y2="200" stroke="{c["line"]}"/>
<text x="40" y="232" fill="{c["accent"]}" font-family="{MONO}" font-size="12" letter-spacing="1.2">{label}</text>
<text x="40" y="268" fill="{c["fg"]}" font-family="{SANS}" font-size="28" letter-spacing="-0.8">{name}</text>
<text x="40" y="298" fill="{c["muted"]}" font-family="{SANS}" font-size="16">{d1}</text>
<text x="40" y="320" fill="{c["muted"]}" font-family="{SANS}" font-size="16">{d2}</text>
<text x="{CW - 40}" y="268" text-anchor="end" fill="{c["muted"]}" font-family="{SANS}" font-size="20">↗</text>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "cards").mkdir(exist_ok=True)
    for theme, c in THEMES.items():
        write("header", theme, header(theme, c))
        write("numbers", theme, numbers(theme, c))
        for name, label, d1, d2, art in PROJECTS:
            (OUT / "cards" / f"{name}-{theme}.svg").write_text(card(c, name, label, d1, d2, art))
    print("wrote", len(list(OUT.glob("*.svg"))) + len(list((OUT / "cards").glob("*.svg"))), "svg files")

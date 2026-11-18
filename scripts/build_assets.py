#!/usr/bin/env python3
"""Generate the self-hosted SVG assets used by the profile README.

Everything the README shows (banner and project cards) is rendered here,
in a dark and a light variant, so the profile never depends on third-party
card services. Standard library only:  python3 scripts/build_assets.py
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BRAND = "#36BCF7"

THEMES = {
    "dark": {
        "bg_from": "#0D1117",
        "bg_to": "#0A1C27",
        "border": "#30363D",
        "title": "#F0F6FC",
        "text": "#C9D1D9",
        "muted": "#8B949E",
        "accent_text": BRAND,
        "grid": "#1F2A33",
        "pill_bg": "#0F2A38",
        "card_bg": "#0D1117",
    },
    "light": {
        "bg_from": "#FFFFFF",
        "bg_to": "#E8F6FD",
        "border": "#D0D7DE",
        "title": "#0D1117",
        "text": "#24292F",
        "muted": "#57606A",
        "accent_text": "#0A6C9C",
        "grid": "#D8EEF8",
        "pill_bg": "#E1F3FC",
        "card_bg": "#FFFFFF",
    },
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

TYPED_LINES = [
    "building context engines for coding agents",
    "shipping open banking APIs at Tink (Visa)",
    "evaluating ML models like production code",
]

# Only projects with verifiable quality signals (README, tests, CI, licence).
# Tags state facts a reviewer can check in the repo, not adjectives.
PROJECTS = [
    {
        "slug": "swarmtrader",
        "title": "swarmtrader",
        "repo": "dalonsogomez-ai/swarmtrader",
        "wide": True,
        "kicker": "FLAGSHIP",
        "description": "Multi-agent equity research you can audit: walk-forward "
        "evaluation, out-of-sample probability calibration and statistical "
        "controls for backtest overfitting. When the evidence is not there, "
        "it abstains instead of pretending.",
        "tags": ["Python", "Multi-agent", "Calibration", "CI + 277 tests", "MIT"],
    },
    {
        "slug": "braid-kg",
        "title": "braid-kg",
        "repo": "dalonsogomez/braid-kg",
        "description": "MCP-first persistent memory, knowledge graph and RAG "
        "for coding agents such as Claude Code, Codex and Cursor.",
        "tags": ["MCP", "Knowledge graph", "RAG", "CI + tests"],
    },
    {
        "slug": "vp-class-diagram-agent",
        "title": "vp-class-diagram-agent",
        "repo": "dalonsogomez/vp-class-diagram-agent-afg",
        "description": "Local MCP server and Visual Paradigm plugin that "
        "generates editable UML class-diagram projects.",
        "tags": ["MCP", "Python", "CI + tests", "MIT"],
    },
]

# Hand-placed knowledge-graph motif for the banner (x, y, radius).
NODES = [
    (930, 150, 13),  # hub
    (820, 78, 7), (1040, 70, 8), (1110, 160, 7), (1050, 238, 8),
    (900, 250, 7), (800, 190, 6), (990, 108, 5), (1000, 196, 5),
    (870, 120, 5), (1135, 92, 4), (760, 120, 4),
]
EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
    (1, 9), (9, 6), (2, 10), (7, 2), (8, 4), (3, 8), (1, 11), (11, 6),
]


def _defs_background(t: dict, gid: str) -> str:
    return f"""
    <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{t['bg_from']}"/>
      <stop offset="100%" stop-color="{t['bg_to']}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BRAND}"/>
      <stop offset="100%" stop-color="#7C6CF2"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t['grid']}"/>
    </pattern>"""


def _typing_block(t: dict, x: int, y: int) -> tuple[str, str]:
    """Return (css, svg) for a looping, char-by-char typing effect."""
    size = 19
    char_w = size * 0.6
    window = 100 / len(TYPED_LINES)
    css, svg = [], []
    for i, line in enumerate(TYPED_LINES):
        n = len(line)
        width = round(n * char_w, 1)
        a = round(i * window, 3)
        b = round(a + window * 0.40, 3)  # typed
        c = round(a + window * 0.85, 3)  # hold
        d = round(a + window * 0.95, 3)  # erased
        css.append(f"""
      @keyframes type{i} {{ 0%,{a}% {{transform:scaleX(0)}} {b}%,{c}% {{transform:scaleX(1)}} {d}%,100% {{transform:scaleX(0)}} }}
      @keyframes caret{i} {{ 0%,{a}% {{transform:translateX(0)}} {b}%,{c}% {{transform:translateX({width}px)}} {d}%,100% {{transform:translateX(0)}} }}
      @keyframes show{i} {{ 0%,{a}% {{opacity:0}} {a + 0.01}%,{d}% {{opacity:1}} {d + 0.01}%,100% {{opacity:0}} }}
      .clip{i} {{ transform-box:fill-box; transform-origin:0 0; animation:type{i} 13.5s steps({n},end) infinite; }}
      .caret{i} {{ animation:caret{i} 13.5s steps({n},end) infinite; }}
      .line{i} {{ animation:show{i} 13.5s linear infinite; }}""")
        svg.append(f"""
    <clipPath id="clip{i}"><rect class="clip{i}" x="{x}" y="{y - size}" width="{width}" height="{size + 8}"/></clipPath>
    <g class="line{i}">
      <text x="{x}" y="{y}" textLength="{width}" lengthAdjust="spacingAndGlyphs" clip-path="url(#clip{i})"
            font-family="{MONO}" font-size="{size}" fill="{t['accent_text']}">{escape(line)}</text>
      <g class="caret{i}"><rect class="blink" x="{x + 2}" y="{y - size + 2}" width="10" height="{size + 2}" rx="1.5" fill="{BRAND}"/></g>
    </g>""")
    css.append("""
      @keyframes blink { 50% {opacity:0} }
      .blink { animation: blink 1s step-end infinite; }
      @media (prefers-reduced-motion: reduce) {
        .clip0, .caret0, .line0, .blink, .flow, .halo { animation: none !important; }
        .line1, .line2 { display: none; }
      }""")
    return "".join(css), "".join(svg)


def build_banner(theme: str) -> str:
    t = THEMES[theme]
    typing_css, typing_svg = _typing_block(t, x=92, y=238)

    edges = []
    for k, (i, j) in enumerate(EDGES):
        x1, y1, _ = NODES[i]
        x2, y2, _ = NODES[j]
        edges.append(
            f'<line class="flow" style="animation-delay:-{k * 0.37:.2f}s" '
            f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
        )
    nodes = []
    for k, (x, y, r) in enumerate(NODES):
        halo = (
            f'<circle class="halo" style="animation-delay:-{k * 0.53:.2f}s" '
            f'cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{BRAND}" stroke-width="1.5"/>'
        )
        fill = "url(#accent)" if k == 0 else BRAND
        opacity = 1 if r >= 7 else 0.75
        nodes.append(f'{halo}<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{opacity}"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img" aria-labelledby="title desc">
  <title id="title">Daniel Alonso Gómez</title>
  <desc id="desc">Senior Software Engineer working on AI agents and ML systems, based in Madrid.</desc>
  <defs>{_defs_background(t, "bg")}
    <style>
      .flow {{ stroke:{BRAND}; stroke-opacity:.45; stroke-width:1.4; stroke-dasharray:4 7; animation: flow 2.6s linear infinite; }}
      @keyframes flow {{ to {{ stroke-dashoffset:-22; }} }}
      .halo {{ transform-box:fill-box; transform-origin:center; animation: halo 3.2s ease-out infinite; }}
      @keyframes halo {{ 0% {{ transform:scale(1); opacity:.7; }} 100% {{ transform:scale(2.6); opacity:0; }} }}{typing_css}
    </style>
  </defs>
  <rect x="1" y="1" width="1198" height="298" rx="18" fill="url(#bg)" stroke="{t['border']}"/>
  <rect x="1" y="1" width="1198" height="298" rx="18" fill="url(#dots)" opacity=".7"/>
  <rect x="64" y="56" width="4" height="190" rx="2" fill="url(#accent)"/>

  <text x="92" y="76" font-family="{MONO}" font-size="16" fill="{t['muted']}">~/dalonsogomez <tspan fill="{t['accent_text']}">$</tspan> whoami</text>
  <text x="90" y="138" font-family="{SANS}" font-size="54" font-weight="700" fill="{t['title']}" letter-spacing="-0.5">Daniel Alonso Gómez</text>
  <text x="92" y="182" font-family="{SANS}" font-size="23" fill="{t['text']}">Senior Software Engineer  ·  AI agents &amp; ML systems</text>
  <text x="92" y="238" font-family="{MONO}" font-size="19" fill="{t['muted']}" text-anchor="end" dx="-6">&gt;</text>{typing_svg}
  <text x="92" y="274" font-family="{SANS}" font-size="15" fill="{t['muted']}">Madrid, Spain  ·  Python · TypeScript · MCP  ·  open to good conversations</text>

  <g>{''.join(edges)}</g>
  <g>{''.join(nodes)}</g>
</svg>
"""


def _pill(x: float, y: float, label: str, t: dict) -> tuple[str, float]:
    w = len(label) * 7.1 + 22
    svg = (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{t["pill_bg"]}" '
        f'stroke="{BRAND}" stroke-opacity=".35"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + 16.5}" text-anchor="middle" font-family="{SANS}" '
        f'font-size="12.5" fill="{t["accent_text"]}">{escape(label)}</text>'
    )
    return svg, w


def build_card(project: dict, theme: str) -> str:
    t = THEMES[theme]
    # Wide cards render at 100% and normal ones at 49%, so 1060 vs 520 keeps
    # the same on-screen scale for text in both.
    width = 1060 if project.get("wide") else 520
    lines = textwrap.wrap(project["description"], width=124 if project.get("wide") else 60)[:3]
    desc = "".join(
        f'<text x="32" y="{82 + i * 21}" font-family="{SANS}" font-size="15" fill="{t["text"]}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    pills, x = [], 32.0
    for tag in project["tags"]:
        svg, w = _pill(x, 150, tag, t)
        pills.append(svg)
        x += w + 8
    kicker = ""
    if project.get("kicker"):
        kw = len(project["kicker"]) * 7.6 + 20
        kx = 54 + len(project["title"]) * 11.4 + 14
        kicker = (
            f'<rect x="{kx:.1f}" y="33" width="{kw:.1f}" height="22" rx="11" fill="url(#accent)"/>'
            f'<text x="{kx + kw / 2:.1f}" y="48.5" text-anchor="middle" font-family="{MONO}" '
            f'font-size="11.5" font-weight="700" letter-spacing="1" fill="#FFFFFF">{escape(project["kicker"])}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 194" width="{width}" height="194" role="img" aria-labelledby="title desc">
  <title id="title">{escape(project['title'])}</title>
  <desc id="desc">{escape(project['description'])}</desc>
  <defs>{_defs_background(t, "bg")}</defs>
  <rect x="1" y="1" width="{width - 2}" height="192" rx="14" fill="url(#bg)" stroke="{t['border']}"/>
  <rect x="1" y="24" width="4" height="146" rx="2" fill="url(#accent)"/>
  <circle cx="38" cy="44" r="6" fill="none" stroke="{BRAND}" stroke-width="2"/>
  <circle cx="38" cy="44" r="2.2" fill="{BRAND}"/>
  <text x="54" y="50" font-family="{MONO}" font-size="19" font-weight="700" fill="{t['title']}">{escape(project['title'])}</text>
  {kicker}
  <text x="{width - 32}" y="50" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t['muted']}">{escape(project['repo'] if project.get('wide') else project['repo'].split('/')[0])}</text>
  {desc}
  {''.join(pills)}
</svg>
"""


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    written = []
    for theme in THEMES:
        path = ASSETS / f"banner-{theme}.svg"
        path.write_text(build_banner(theme), encoding="utf-8")
        written.append(path)
        for project in PROJECTS:
            path = ASSETS / f"card-{project['slug']}-{theme}.svg"
            path.write_text(build_card(project, theme), encoding="utf-8")
            written.append(path)
    for path in written:
        print(path.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()

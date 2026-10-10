#!/usr/bin/env python3
"""
Generate a neofetch-style SVG info card.
Prints system/profile information in a clean terminal window aesthetic.
Can be rendered statically or with staggered fade/slide SMIL animations.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 880
PAD = 24
TITLEBAR_H = 30
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
MUTED = "#7d8590"
INK = "#e6edf3"
BLUE = "#58a6ff"
GREEN = "#3fb950"
YELLOW = "#d29922"
PURPLE = "#bc8cff"
CYAN = "#39c5cf"

info_items = [
    ("OS", "Arch Linux x86_64", BLUE),
    ("Host", "GitHub @Pritampy", CYAN),
    ("Kernel", "Fullstack & AI Engineer", GREEN),
    ("Uptime", "Coding since 2021", YELLOW),
    ("Languages", "Python, Java, C++, JavaScript, SQL", PURPLE),
    ("Frameworks", "Django, React, Flask, PyTorch, Docker", BLUE),
    ("Databases", "PostgreSQL, MongoDB, MySQL", CYAN),
    ("Algorithms", "1000+ DSA questions solved on LeetCode", GREEN),
    ("Focus", "Scalable Systems · Machine Learning · Web Dev", YELLOW),
    ("Contact", "pritamsingh07102001@gmail.com", INK),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>'
    '.row{opacity:0;animation:fadeIn 0.5s ease-out forwards;}'
    '@keyframes fadeIn{0%{opacity:0;transform:translateX(-10px)}100%{opacity:1;transform:translateX(0)}}'
    '@media (prefers-reduced-motion: reduce){.row{opacity:1!important;transform:none!important;animation:none!important}}'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">pritam@github: ~$ neofetch</text>')

# Title section
parts.append(f'<text class="row" style="animation-delay:0.1s" x="{PAD+20}" y="80" fill="{GREEN}" font-size="28" font-weight="700">pritam<tspan fill="{MUTED}">@</tspan><tspan fill="{BLUE}">github</tspan></text>')
parts.append(f'<line class="row" style="animation-delay:0.15s" x1="{PAD+20}" y1="96" x2="{W-PAD-20}" y2="96" stroke="{FRAME}" stroke-dasharray="4,4"/>')

# Key-value rows
y = 145
for idx, (k, v, color) in enumerate(info_items):
    delay = 0.2 + idx * 0.12
    safe_k = html.escape(k)
    safe_v = html.escape(v)
    parts.append(f'<g class="row" style="animation-delay:{delay:.2f}s">')
    parts.append(f'<text x="{PAD+20}" y="{y}" fill="{color}" font-weight="600" font-size="20">{safe_k:12}</text>')
    parts.append(f'<text x="{PAD+200}" y="{y}" fill="{INK}" font-size="19">{safe_v}</text>')
    parts.append('</g>')
    y += 56

# Palette circles at bottom
palette_colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#39c5cf", "#58a6ff", "#bc8cff", "#e6edf3"]
py = H - 50
for ci, pc in enumerate(palette_colors):
    parts.append(f'<circle class="row" style="animation-delay:1.5s" cx="{PAD+30 + ci*32}" cy="{py}" r="10" fill="{pc}"/>')

parts.append('</svg>')
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")

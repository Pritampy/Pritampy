#!/usr/bin/env python3
"""
Generate a neofetch-style SVG info card.
Prints system/profile information in a clean terminal window aesthetic.
Uses rock-solid SVG formatting (default opacity 1 with SMIL animations).
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "stack-card.svg")

W, H = 840, 520  # compact height for cleaner aesthetic
PAD = 24
TITLEBAR_H = 34
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
    ("Role", "Fullstack &amp; AI Engineer", GREEN),
    ("Uptime", "Coding since 2021", YELLOW),
    ("Languages", "Python, Java, C++, JavaScript, SQL", PURPLE),
    ("Frameworks", "Django, React, Flask, PyTorch, Docker", BLUE),
    ("Databases", "PostgreSQL, MongoDB, MySQL", CYAN),
    ("Algorithms", "1000+ DSA questions solved on LeetCode", GREEN),
    ("Focus", "Scalable Systems · Machine Learning · Web Dev", YELLOW),
    ("Contact", "pritamsingh07102001@gmail.com", INK),
]

parts = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">\n',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>\n',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>\n',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>\n',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>\n',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*18}" cy="{TITLEBAR_H/2}" r="5.5" fill="{dot}"/>\n')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">pritam@github: ~$ neofetch</text>\n')

# Title section
parts.append(f'<text x="{PAD+20}" y="74" fill="{GREEN}" font-size="24" font-weight="700">pritam<tspan fill="{MUTED}">@</tspan><tspan fill="{BLUE}">github</tspan></text>\n')
parts.append(f'<line x1="{PAD+20}" y1="88" x2="{W-PAD-20}" y2="88" stroke="{FRAME}" stroke-dasharray="4,4"/>\n')

# Key-value rows
y = 126
for idx, (k, v, color) in enumerate(info_items):
    delay = 0.1 + idx * 0.08
    safe_k = html.escape(k) if '&' not in k else k
    safe_v = html.escape(v) if '&' not in v else v
    parts.append(f'<g opacity="1">\n')
    parts.append(f'  <text x="{PAD+20}" y="{y}" fill="{color}" font-weight="600" font-size="18">{safe_k}</text>\n')
    parts.append(f'  <text x="{PAD+180}" y="{y}" fill="{INK}" font-size="17">{safe_v}</text>\n')
    parts.append('</g>\n')
    y += 34

# Palette circles at bottom
palette_colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#39c5cf", "#58a6ff", "#bc8cff", "#e6edf3"]
py = H - 28
for ci, pc in enumerate(palette_colors):
    parts.append(f'<circle cx="{PAD+30 + ci*28}" cy="{py}" r="8" fill="{pc}"/>\n')

parts.append('</svg>\n')
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

# also write info-card.svg
with open(os.path.join(HERE, "..", "info-card.svg"), "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Wrote {OUT} ({W}x{H}) and info-card.svg")

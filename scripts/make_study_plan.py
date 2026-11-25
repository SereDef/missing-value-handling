"""Draws images/study-plan.svg for divider 3 ("Missing data designs (offence)"):
a clipboard holding a planned-missingness design grid (some cells deliberately
empty), with a pencil and a ruler, in the flat layered style of tree.png
(no outlines, 3-5 tones per material, grey cast shadow).

Run: python3 scripts/make_study_plan.py
"""
W, H = 1240, 500
out = []
def add(s): out.append(s)

BROWNS = ["#4E2A0C", "#7A4511", "#9A5A16", "#C27E28", "#DDA43F"]
STEEL = ["#4F5560", "#6E7682", "#97A0AB", "#C3CAD2", "#E6EAEE"]
LAV = ["#4D4D95", "#6666BC", "#8F8DD0", "#C3C2E4", "#E5E4F4"]     # section 3 blues
YEL = ["#B07A14", "#E0A21E", "#FFD26D", "#FFE9A8"]
MINT = ["#1F7A62", "#47C5A3", "#B5E8DA"]
CORAL = ["#C93B42", "#E0484F", "#F0676C", "#FFBFAF"]
GREENS = ["#2B8A1D", "#46A41B", "#6CC11A"]

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

# shadows on the ground
add('<ellipse cx="620" cy="478" rx="360" ry="16" fill="#8C8C8C" opacity="0.35"/>')
add('<ellipse cx="630" cy="476" rx="260" ry="10" fill="#6F6F6F" opacity="0.35"/>')

# --- clipboard board (wood) -----------------------------------------------------
add(f'<rect x="420" y="40" width="400" height="440" rx="22" fill="{BROWNS[2]}"/>')
add(f'<rect x="420" y="40" width="22" height="440" rx="11" fill="{BROWNS[3]}"/>')
add(f'<rect x="798" y="40" width="22" height="440" rx="11" fill="{BROWNS[1]}"/>')
for x, y, w in [(470, 455, 120), (640, 462, 140), (700, 60, 90)]:
    add(f'<path d="M{x} {y} C {x + w*0.3} {y - 3}, {x + w*0.7} {y + 3}, {x + w} {y}" stroke="{BROWNS[4]}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>')

# --- paper ----------------------------------------------------------------------
add('<rect x="450" y="78" width="340" height="380" rx="6" fill="#FFFFFF"/>')
add('<rect x="450" y="78" width="340" height="380" rx="6" fill="#000000" opacity="0.03"/>')
add('<path d="M790 380 L790 458 L712 458 Z" fill="#EDEDED"/>')       # curled corner shade
add(f'<path d="M712 458 L790 380 L770 446 Z" fill="{STEEL[3]}"/>')

# title lines
add(f'<rect x="478" y="132" width="180" height="12" rx="6" fill="{LAV[0]}"/>')
add(f'<rect x="478" y="152" width="120" height="8" rx="4" fill="{LAV[3]}"/>')

# planned-missingness grid: rows = groups, columns = waves; empty cells are missing by design
cols, rows = 5, 4
gx, gy, cw, ch, gap = 482, 182, 54, 48, 8
plan = ["11100", "01110", "00111", "10011"]
for r in range(rows):
    for c in range(cols):
        x = gx + c * (cw + gap); y = gy + r * (ch + gap)
        if plan[r][c] == "1":
            add(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="9" fill="{LAV[2]}"/>')
            add(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch*0.38:.0f}" rx="9" fill="{LAV[3]}"/>')
            add(f'<path d="M{x+15} {y+26} l9 9 l17 -17" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            add(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="9" fill="none" stroke="{LAV[3]}" stroke-width="3" stroke-dasharray="6 5"/>')

# --- metal clip on top -----------------------------------------------------------
add(f'<rect x="545" y="22" width="150" height="62" rx="14" fill="{STEEL[1]}"/>')
add(f'<rect x="545" y="22" width="150" height="20" rx="10" fill="{STEEL[3]}"/>')
add(f'<rect x="585" y="8" width="70" height="36" rx="16" fill="none" stroke="{STEEL[2]}" stroke-width="10"/>')
add(f'<rect x="560" y="66" width="120" height="8" rx="4" fill="{STEEL[0]}"/>')

# --- ruler (yellow), leaning on the left -------------------------------------------
add('<g transform="rotate(-14 360 330)">')
add(f'<rect x="300" y="140" width="70" height="330" rx="8" fill="{YEL[1]}"/>')
add(f'<rect x="300" y="140" width="22" height="330" rx="8" fill="{YEL[2]}"/>')
add(f'<rect x="356" y="140" width="14" height="330" rx="6" fill="{YEL[0]}"/>')
for i in range(15):
    y = 158 + i * 21
    w = 26 if i % 5 == 0 else 15
    add(f'<rect x="{370 - w}" y="{y}" width="{w}" height="3" rx="1.5" fill="{YEL[0]}"/>')
add('</g>')

# --- pencil, lying across the bottom right ---------------------------------------
add('<g transform="rotate(-28 930 380)">')
add(f'<rect x="830" y="364" width="210" height="34" rx="4" fill="{YEL[1]}"/>')
add(f'<rect x="830" y="364" width="210" height="11" rx="4" fill="{YEL[2]}"/>')
add(f'<rect x="830" y="388" width="210" height="10" rx="4" fill="{YEL[0]}"/>')
add(f'<rect x="1040" y="364" width="26" height="34" fill="{STEEL[2]}"/><rect x="1040" y="364" width="26" height="10" fill="{STEEL[3]}"/>')
add(f'<rect x="1066" y="364" width="30" height="34" rx="10" fill="{CORAL[2]}"/><rect x="1066" y="364" width="30" height="11" rx="5" fill="{CORAL[3]}"/>')
add(f'<path d="M830 364 L782 381 L830 398 Z" fill="#F3D3A8"/>')
add(f'<path d="M800 375 L782 381 L800 387 Z" fill="{LAV[0]}"/>')
add('</g>')

# --- small plant pot on the far left, tree-style leaves, for balance -------------
add(f'<path d="M180 470 L200 400 L280 400 L300 470 Z" fill="{CORAL[1]}"/>')
add(f'<path d="M180 470 L200 400 L222 400 L206 470 Z" fill="{CORAL[2]}"/>')
add(f'<rect x="194" y="392" width="92" height="16" rx="5" fill="{CORAL[0]}"/>')
for cx, cy, r, col in [(240, 340, 52, GREENS[0]), (215, 320, 34, GREENS[1]), (262, 312, 36, GREENS[1]), (238, 296, 30, GREENS[2]), (250, 330, 22, GREENS[2])]:
    pts = []
    import math
    for i in range(36):
        a = math.pi * 2 * i / 36
        k = 1.0 if i % 2 == 0 else 0.86
        pts.append(f"{cx + r * k * math.cos(a):.1f} {cy + r * 0.85 * k * math.sin(a):.1f}")
    add(f'<path d="M{" L".join(pts)} Z" fill="{col}"/>')

add('</svg>')
open('images/study-plan.svg', 'w').write("\n".join(out))
print("wrote images/study-plan.svg")

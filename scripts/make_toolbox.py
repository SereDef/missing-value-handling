"""Draws images/toolbox.svg: an open wooden toolbox full of tools, in the flat,
layered style of images/tree.png (no outlines, 3-5 tones per material, a grey
cast shadow on the ground). Used on divider 2 ("Missing data handling").

Run: python3 scripts/make_toolbox.py
"""
import math

W, H = 1240, 500
out = []
def add(s): out.append(s)

BROWNS = ["#4E2A0C", "#7A4511", "#9A5A16", "#C27E28", "#DDA43F"]     # tree trunk tones
GREENS = ["#17480F", "#2B8A1D", "#46A41B", "#6CC11A", "#8EDB23"]
STEEL = ["#4F5560", "#6E7682", "#97A0AB", "#C3CAD2", "#E6EAEE"]
RED = ["#9E2A30", "#C93B42", "#E0484F", "#F0676C"]
YEL = ["#B07A14", "#E0A21E", "#FFD26D"]
TEAL = ["#1F7A62", "#2FA586", "#47C5A3"]

def poly(pts, fill, extra=""):
    add(f'<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f' Z" fill="{fill}" {extra}/>')

def rot(pts, cx, cy, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]

def g_open(cx, cy, deg):
    add(f'<g transform="rotate({deg} {cx} {cy})">')
def g_close():
    add('</g>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

# ---------------------------------------------------------------- ground + shadows
add(f'<ellipse cx="640" cy="468" rx="430" ry="26" fill="#8C8C8C" opacity="0.35"/>')
add(f'<ellipse cx="650" cy="466" rx="330" ry="17" fill="#6F6F6F" opacity="0.35"/>')
# little grass tufts either side, like the base of the tree
for x0, s in [(240, 1.0), (300, 0.7), (1010, 0.9), (1060, 0.65), (180, 0.55)]:
    pts = [(x0, 470)]
    for k in range(6):
        pts += [(x0 + k * 9 * s, 470 - 34 * s * (0.6 + 0.4 * ((k * 7) % 3) / 2)), (x0 + (k * 9 + 4) * s, 462)]
    pts.append((x0 + 54 * s, 470))
    poly(pts, GREENS[2]); poly([(x, y + 6) for x, y in pts], GREENS[3], 'opacity="0.8"')

# ---------------------------------------------------------------- tools (behind the front panel)
# screwdriver (yellow handle)
g_open(470, 250, -18)
add(f'<rect x="462" y="90" width="12" height="150" rx="3" fill="{STEEL[2]}"/>')
add(f'<rect x="462" y="90" width="5" height="150" fill="{STEEL[3]}"/>')
add(f'<path d="M462 90 L468 70 L474 90 Z" fill="{STEEL[1]}"/>')
add(f'<rect x="452" y="220" width="32" height="90" rx="12" fill="{YEL[1]}"/>')
add(f'<rect x="452" y="220" width="12" height="90" rx="6" fill="{YEL[2]}"/>')
add(f'<rect x="476" y="224" width="6" height="82" rx="3" fill="{YEL[0]}"/>')
g_close()
# hammer (wooden handle, steel head)
g_open(560, 260, 10)
add(f'<rect x="548" y="120" width="24" height="200" rx="8" fill="{BROWNS[3]}"/>')
add(f'<rect x="548" y="120" width="9" height="200" rx="4" fill="{BROWNS[4]}"/>')
add(f'<rect x="565" y="120" width="7" height="200" rx="3" fill="{BROWNS[2]}"/>')
add(f'<path d="M500 92 L600 92 L604 100 L612 100 C 628 104, 640 116, 646 130 L 606 126 L 600 132 L 500 132 Z" fill="{STEEL[1]}"/>')
add(f'<path d="M500 92 L600 92 L600 104 L500 104 Z" fill="{STEEL[3]}"/>')
add(f'<rect x="494" y="88" width="16" height="48" rx="4" fill="{STEEL[0]}"/>')
g_close()
# spanner / wrench
g_open(700, 250, 22)
add(f'<rect x="686" y="110" width="26" height="190" rx="10" fill="{STEEL[2]}"/>')
add(f'<rect x="686" y="110" width="9" height="190" rx="4" fill="{STEEL[3]}"/>')
add(f'<path d="M672 86 C 672 60, 726 60, 726 86 C 726 110, 714 118, 712 124 L 686 124 C 684 118, 672 110, 672 86 Z" fill="{STEEL[1]}"/>')
add(f'<path d="M688 64 L 710 64 L 708 92 L 690 92 Z" fill="#FFFFFF" opacity="0"/>')
add(f'<rect x="690" y="56" width="18" height="36" rx="4" fill="#FBFBFB"/>')     # open jaw
g_close()
# pliers (red grips)
g_open(800, 250, 30)
add(f'<path d="M788 300 L 796 170 L 806 170 L 802 300 Z" fill="{RED[1]}"/>')
add(f'<path d="M818 300 L 810 170 L 820 170 L 832 300 Z" fill="{RED[2]}"/>')
add(f'<path d="M790 300 L 796 200 L 800 200 L 796 300 Z" fill="{RED[3]}"/>')
add(f'<path d="M794 172 L 800 110 L 806 106 L 812 172 Z" fill="{STEEL[1]}"/>')
add(f'<path d="M808 172 L 812 104 L 820 108 L 822 172 Z" fill="{STEEL[2]}"/>')
add(f'<circle cx="808" cy="172" r="9" fill="{STEEL[0]}"/><circle cx="806" cy="170" r="3" fill="{STEEL[3]}"/>')
g_close()
# paintbrush-like measuring tape body (teal) poking out on the left
add(f'<rect x="395" y="215" width="70" height="60" rx="16" fill="{TEAL[1]}" transform="rotate(-10 430 245)"/>')
add(f'<circle cx="428" cy="245" r="15" fill="{TEAL[0]}" transform="rotate(-10 430 245)"/>')
add(f'<rect x="395" y="215" width="70" height="16" rx="8" fill="{TEAL[2]}" transform="rotate(-10 430 245)"/>')

# ---------------------------------------------------------------- toolbox
# back wall, inside shadow
poly([(350, 250), (930, 250), (930, 290), (350, 290)], BROWNS[0])
# end panels (taller, carry the handle)
for x in (330, 900):
    poly([(x, 450), (x, 200), (x + 25, 170), (x + 50, 200), (x + 50, 450)], BROWNS[2])
    poly([(x, 450), (x, 200), (x + 14, 183), (x + 14, 450)], BROWNS[3])
    poly([(x + 38, 450), (x + 38, 190), (x + 50, 200), (x + 50, 450)], BROWNS[1])
# handle (round wooden bar)
add(f'<rect x="352" y="182" width="576" height="20" rx="10" fill="{BROWNS[3]}"/>')
add(f'<rect x="352" y="182" width="576" height="7" rx="3.5" fill="{BROWNS[4]}"/>')
add(f'<rect x="352" y="196" width="576" height="6" rx="3" fill="{BROWNS[1]}"/>')
# front panel with planks and grain streaks
poly([(345, 290), (935, 290), (935, 452), (345, 452)], BROWNS[2])
for y0, tone in [(290, 3), (344, 2), (398, 3)]:
    poly([(345, y0), (935, y0), (935, y0 + 52), (345, y0 + 52)], BROWNS[tone])
    add(f'<rect x="345" y="{y0 + 50}" width="590" height="4" fill="{BROWNS[1]}"/>')
for i, (x, y, w) in enumerate([(380, 305, 120), (560, 318, 160), (760, 300, 110), (420, 360, 180),
                                (680, 372, 140), (390, 414, 130), (600, 428, 170), (820, 410, 90)]):
    add(f'<path d="M{x} {y} C {x + w*0.3} {y - 4}, {x + w*0.6} {y + 4}, {x + w} {y}" fill="none" '
        f'stroke="{BROWNS[1] if i % 2 else BROWNS[4]}" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
# light rim along the top edge
poly([(345, 286), (935, 286), (935, 296), (345, 296)], BROWNS[4])
# metal corner brackets
for x in (345, 905):
    for y in (296, 420):
        add(f'<rect x="{x}" y="{y}" width="30" height="30" rx="4" fill="{STEEL[2]}"/>')
        add(f'<rect x="{x}" y="{y}" width="30" height="9" rx="3" fill="{STEEL[3]}"/>')
        add(f'<circle cx="{x + 15}" cy="{y + 18}" r="3.5" fill="{STEEL[0]}"/>')

# ---------------------------------------------------------------- loose tools on the ground
# a second spanner lying in front, right
add(f'<g transform="rotate(-8 1020 440)">'
    f'<rect x="960" y="432" width="120" height="16" rx="8" fill="{STEEL[2]}"/>'
    f'<rect x="960" y="432" width="120" height="6" rx="3" fill="{STEEL[3]}"/>'
    f'<circle cx="1088" cy="440" r="18" fill="{STEEL[1]}"/><circle cx="1088" cy="440" r="8" fill="#FBFBFB"/>'
    f'</g>')
# a few screws and a nut, left
for x, y in [(250, 452), (275, 458), (296, 448)]:
    add(f'<rect x="{x}" y="{y}" width="14" height="5" rx="2" fill="{STEEL[1]}"/><rect x="{x - 4}" y="{y - 3}" width="6" height="11" rx="2" fill="{STEEL[2]}"/>')
add(f'<path d="M220 450 l8 -5 l9 0 l8 5 l0 8 l-8 5 l-9 0 l-8 -5 Z" fill="{STEEL[2]}"/><circle cx="232" cy="454" r="4" fill="#FBFBFB"/>')

add('</svg>')
open('images/toolbox.svg', 'w').write("\n".join(out))
print("wrote images/toolbox.svg")

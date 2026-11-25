"""Draws images/pothole-road.svg: a cartoon road full of potholes, in the flat,
layered style of images/tree.png (no outlines, 4-5 tones per material, frilly
foliage edges, bark streaks, grey cast shadows). Run: python3 scripts/make_pothole_road.py
"""
import math, random

random.seed(11)
W, H = 1240, 500
out = []
def add(s): out.append(s)

GREENS = ["#17480F", "#2B8A1D", "#46A41B", "#6CC11A", "#8EDB23"]   # dark -> light, from tree.png
BROWNS = ["#4E2A0C", "#7A4511", "#9A5A16", "#C27E28", "#DDA43F"]
GREYS = ["#4F4F4F", "#6C6C6C", "#868686", "#9B9B9B", "#B3B3B3"]

def poly(pts, fill, extra=""):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    add(f'<path d="{d}" fill="{fill}" {extra}/>')

def frilly(cx, cy, rx, ry, fill, spikes=None, depth=0.22, seed=None):
    """Blob with an irregular leafy edge (like the tree's foliage clumps):
    a few soft lobes plus small jagged teeth of random depth."""
    rnd = random.Random(seed)
    n = spikes or max(24, int((rx + ry) / 2.2))
    p1, p2 = rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)
    pts = []
    for i in range(n * 2):
        a = math.pi * 2 * (i + rnd.uniform(-0.3, 0.3)) / (n * 2)
        lobe = 1 + 0.12 * math.sin(3 * a + p1) + 0.07 * math.sin(5 * a + p2)
        tooth = 1.0 if i % 2 == 0 else 1 - depth * rnd.uniform(0.2, 1.0)
        k = lobe * tooth
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    poly(pts, fill)

def foliage(cx, cy, r, seed):
    """A clump of tree-style foliage: dark base, mid layers, light highlights."""
    rnd = random.Random(seed)
    frilly(cx, cy + r * 0.15, r * 1.05, r * 0.8, GREENS[0], depth=0.12, seed=rnd.random())
    for tone, k, dy in [(1, 0.9, 0.05), (2, 0.78, -0.05), (3, 0.6, -0.15), (4, 0.38, -0.25)]:
        for j in range(3 if tone < 4 else 2):
            ox = rnd.uniform(-0.45, 0.45) * r * (1.1 - k)
            oy = rnd.uniform(-0.2, 0.2) * r * (1.1 - k)
            frilly(cx + ox - r * 0.12 * (tone - 1) / 3, cy + r * dy + oy,
                   r * k * rnd.uniform(0.55, 0.85), r * k * rnd.uniform(0.4, 0.6),
                   GREENS[tone], depth=0.14, seed=rnd.random())

def small_tree(x, base, h, seed):
    rnd = random.Random(seed)
    tw = h * 0.09
    add(f'<ellipse cx="{x + tw*1.5:.1f}" cy="{base:.1f}" rx="{h*0.32:.1f}" ry="{h*0.05:.1f}" fill="#7F7F7F" opacity="0.45"/>')
    poly([(x - tw, base), (x - tw * 0.5, base - h * 0.55), (x + tw * 0.5, base - h * 0.55), (x + tw, base)], BROWNS[1])
    poly([(x - tw * 0.1, base), (x + tw * 0.1, base - h * 0.5), (x + tw * 0.5, base - h * 0.5), (x + tw * 0.9, base)], BROWNS[3])
    poly([(x - tw * 0.6, base), (x - tw * 0.45, base - h * 0.45), (x - tw * 0.25, base - h * 0.45), (x - tw * 0.3, base)], BROWNS[0])
    foliage(x, base - h * 0.72, h * 0.36, rnd.random())

# ---------------------------------------------------------------- landscape
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
# soft cartoon clouds
def cloud(x, y, sc):
    add(f'<g transform="translate({x} {y}) scale({sc})">'
        '<ellipse cx="0" cy="10" rx="70" ry="18" fill="#E4EEF5"/>'
        '<circle cx="-30" cy="0" r="24" fill="#F4F8FB"/><circle cx="8" cy="-12" r="32" fill="#FFFFFF"/>'
        '<circle cx="42" cy="2" r="22" fill="#F4F8FB"/><ellipse cx="0" cy="12" rx="62" ry="12" fill="#FFFFFF"/>'
        '</g>')
cloud(330, 70, 1.0); cloud(930, 55, 0.8); cloud(610, 110, 0.55); cloud(1150, 120, 0.5)
# far hills
add(f'<path d="M0 235 C 150 185 330 170 520 196 C 700 220 860 155 1040 160 C 1130 163 1200 182 1240 196 L1240 500 L0 500 Z" fill="{GREENS[2]}"/>')
add(f'<path d="M0 262 C 160 222 340 210 560 240 C 720 260 900 205 1240 232 L1240 500 L0 500 Z" fill="{GREENS[3]}"/>')
# distant tree line (small frilly clumps along the horizon)
for x in range(20, 1240, 46):
    y = 205 - 25 * math.sin(x / 210) + random.uniform(-6, 6)
    if 600 < x < 760:  # leave the road's vanishing point clear
        continue
    frilly(x, y, 30, 18, GREENS[1], seed=x)
    frilly(x - 6, y - 5, 20, 11, GREENS[2], seed=x + 1)
# nearer meadows
add(f'<path d="M0 330 C 170 290 330 300 470 332 L 420 500 L0 500 Z" fill="{GREENS[3]}"/>')
add(f'<path d="M1240 300 C 1110 286 990 300 880 342 L 990 500 L1240 500 Z" fill="{GREENS[3]}"/>')
add(f'<path d="M0 405 C 120 378 260 392 380 428 L 360 500 L0 500 Z" fill="{GREENS[4]}"/>')
add(f'<path d="M1240 395 C 1130 378 1040 392 960 428 L 1010 500 L1240 500 Z" fill="{GREENS[4]}"/>')
# small trees in the middle distance
for x, base, h, s in [(150, 262, 95, 1), (300, 250, 70, 2), (980, 236, 85, 3), (1110, 248, 105, 4), (870, 228, 55, 5)]:
    small_tree(x, base, h, s)

# meadow flowers
for i in range(90):
    x = random.uniform(0, 1240); y = random.uniform(300, 495)
    if 330 < x < 1080 and y > 250:   # keep them off the road area
        continue
    c = random.choice(["#FFFFFF", "#FFD26D", "#FFBFAF", "#F7F3C8"])
    r = random.uniform(4, 7) * (0.6 + (y - 300) / 400)
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.35:.1f}" fill="#E8A53A"/>')

# ---------------------------------------------------------------- road geometry
def centre(t):
    """t = 0 at the bottom edge, 1 at the horizon."""
    x = 700 + 150 * math.sin(t * math.pi * 1.6) * (1 - t) ** 0.8
    y = 500 - 330 * (1 - (1 - t) ** 1.25)
    return x, y
def width(t):
    return 600 * (1 - t) ** 1.7 + 20
def point(t, s):     # s in [-1, 1] across the road; cross-sections are horizontal
    x, y = centre(t)
    return x + s * width(t) / 2, y

ts = [i / 120 for i in range(0, 119)]
def band(s0, s1, fill):
    left = [point(t, s0) for t in ts]
    right = [point(t, s1) for t in reversed(ts)]
    poly(left + right, fill)

# dirt verges, then asphalt from dark edges to a light centre band
add('<g>')
band(-1.18, 1.18, BROWNS[2]); band(-1.12, 1.12, BROWNS[3])
band(-1.04, 1.04, GREYS[0]); band(-0.98, 0.98, GREYS[2]); band(-0.55, 0.75, GREYS[3])
band(-0.1, 0.45, GREYS[4])
add('</g>')
# asphalt texture: short streaks along the road
for i in range(110):
    t = random.random() ** 1.4 * 0.93
    s = random.uniform(-0.9, 0.9)
    x, y = point(t, s)
    w = width(t) / 640
    col = random.choice([GREYS[1], GREYS[1], GREYS[4], "#C4C4C4"])
    add(f'<path d="M{x:.1f} {y:.1f} l{18*w*random.uniform(0.5,1.5):.1f} {random.uniform(-1,1)*2*w:.1f}" stroke="{col}" stroke-width="{max(0.6,3*w):.1f}" stroke-linecap="round" opacity="0.7"/>')
# grass tufts on the verges
for i in range(70):
    t = random.random() ** 1.2 * 0.9
    side = random.choice([-1.2, 1.2])
    x, y = point(t, side)
    s = max(0.25, width(t) / 640) * 26
    pts = [(x - s * 0.5, y)]
    for k in range(5):
        pts += [(x - s * 0.4 + k * s * 0.2, y - s * random.uniform(0.6, 1.1)), (x - s * 0.3 + k * s * 0.2, y - s * 0.2)]
    pts.append((x + s * 0.5, y))
    poly(pts, random.choice(GREENS[1:4]))
# edge lines (white, dashed) and double centre line
def line_along(s, width_px, dash=None, fill="#FFFFFF"):
    segs = []
    step = 2
    for i in range(0, len(ts) - step, step):
        if dash and (i // dash) % 2:
            continue
        a, b = point(ts[i], s), point(ts[i + step], s)
        w = max(0.8, width_px * width(ts[i]) / 640)
        segs.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{fill}" stroke-width="{w:.1f}" stroke-linecap="round"/>')
    add("".join(segs))
line_along(-0.04, 9); line_along(0.04, 9)

# ---------------------------------------------------------------- potholes
def pothole(t, s, size, seed):
    rnd = random.Random(seed)
    x, y = point(t, s)
    w = width(t) / 640
    rx, ry = 70 * w * size, 17 * w * size
    # cracks radiating out
    for k in range(3):
        a = rnd.uniform(0, math.pi * 2)
        px, py = x + rx * 1.05 * math.cos(a), y + ry * 1.05 * math.sin(a)
        qx, qy = px + rx * 0.3 * math.cos(a + rnd.uniform(-0.4, 0.4)), py + ry * 0.4 * math.sin(a)
        add(f'<polyline points="{px:.1f},{py:.1f} {(px+qx)/2+rnd.uniform(-3,3)*w:.1f},{(py+qy)/2:.1f} {qx:.1f},{qy:.1f}" fill="none" stroke="{GREYS[0]}" stroke-width="{max(0.8,3*w):.1f}" stroke-linecap="round"/>')
    frilly(x, y, rx * 1.12, ry * 1.25, "#A79A8A", depth=0.08, seed=rnd.random())   # broken rim
    frilly(x, y, rx, ry * 1.08, "#6B5A48", depth=0.1, seed=rnd.random())
    frilly(x + rx * 0.05, y + ry * 0.12, rx * 0.84, ry * 0.85, "#3B2C20", depth=0.12, seed=rnd.random())
    frilly(x + rx * 0.1, y + ry * 0.2, rx * 0.55, ry * 0.5, "#21170F", depth=0.12, seed=rnd.random())
    # a little puddle glint, as in the tree's highlights
    add(f'<ellipse cx="{x - rx*0.25:.1f}" cy="{y + ry*0.25:.1f}" rx="{rx*0.18:.1f}" ry="{ry*0.14:.1f}" fill="#7FA9C9" opacity="0.8"/>')
    # loose chunks of asphalt
    for k in range(3):
        cx = x + rnd.uniform(-1.3, 1.3) * rx
        cy = y + rnd.uniform(0.9, 1.6) * ry
        r = rnd.uniform(3, 7) * w * size
        frilly(cx, cy, r, r * 0.6, GREYS[1], spikes=5, depth=0.3, seed=rnd.random())

# spread along the whole road, alternating lanes, so there is no clean line
holes = [(0.05, -0.5, 1.1), (0.2, 0.45, 0.95), (0.34, -0.35, 1.0),
         (0.55, 0.4, 1.0), (0.7, -0.3, 1.1), (0.82, 0.25, 1.2)]
car_t = 0.47
for t, s, size in sorted(holes, key=lambda h: -h[0]):   # far ones first
    if t < car_t:
        continue
    pothole(t, s, size, int(t * 1000))

# ---------------------------------------------------------------- car
cx, cy = point(car_t, -0.05)
sc = width(car_t) / 640 * 1.9
add(f'<g transform="translate({cx:.1f} {cy - 22*sc:.1f}) rotate(-9) scale({sc:.2f})">')
add('''
  <ellipse cx="4" cy="36" rx="50" ry="8" fill="#3F3F3F" opacity="0.45"/>
  <rect x="-40" y="22" width="13" height="16" rx="3" fill="#232323"/>
  <rect x="27" y="22" width="13" height="16" rx="3" fill="#232323"/>
  <path d="M-42 6 C -42 -2 -37 -6 -29 -8 L 29 -8 C 37 -6 42 -2 42 6 L 42 26 C 42 30 39 33 35 33 L -35 33 C -39 33 -42 30 -42 26 Z" fill="#E0484F"/>
  <path d="M-42 6 C -42 -2 -37 -6 -29 -8 L -10 -8 L -18 33 L -35 33 C -39 33 -42 30 -42 26 Z" fill="#F0676C"/>
  <path d="M-42 19 L 42 19 L 42 26 C 42 30 39 33 35 33 L -35 33 C -39 33 -42 30 -42 26 Z" fill="#B3333A"/>
  <path d="M-27 -8 L -21 -28 C -19 -32 -16 -34 -11 -34 L 11 -34 C 16 -34 19 -32 21 -28 L 27 -8 Z" fill="#C93B42"/>
  <path d="M-22 -9 L -17 -26 C -16 -29 -14 -30 -11 -30 L 11 -30 C 14 -30 16 -29 17 -26 L 22 -9 Z" fill="#BFE3F2"/>
  <path d="M-15 -26 L -4 -26 L -15 -10 L -20 -10 Z" fill="#FFFFFF" opacity="0.75"/>
  <path d="M2 -26 L 7 -26 L -3 -10 L -8 -10 Z" fill="#FFFFFF" opacity="0.5"/>
  <rect x="-48" y="-6" width="8" height="6" rx="2" fill="#B3333A"/>
  <rect x="40" y="-6" width="8" height="6" rx="2" fill="#B3333A"/>
  <ellipse cx="-30" cy="9" rx="8" ry="5.5" fill="#FFE9A8"/>
  <ellipse cx="-31" cy="8" rx="3.5" ry="2.5" fill="#FFFFFF"/>
  <ellipse cx="30" cy="9" rx="8" ry="5.5" fill="#FFE08A"/>
  <rect x="-16" y="5" width="32" height="10" rx="3" fill="#7E2328"/>
  <line x1="-12" y1="8" x2="12" y2="8" stroke="#5A171B" stroke-width="1.4"/>
  <line x1="-12" y1="11.5" x2="12" y2="11.5" stroke="#5A171B" stroke-width="1.4"/>
  <rect x="-11" y="22" width="22" height="7" rx="1.5" fill="#F4F4F4"/>
''')
add('</g>')
for t, s, size in sorted(holes, key=lambda h: -h[0]):   # near ones in front of the car
    if t >= car_t:
        continue
    pothole(t, s, size, int(t * 1000))

# ---------------------------------------------------------------- foreground bushes
for cx_, cy_, r, s in [(40, 345, 85, 21), (150, 380, 70, 22), (1200, 335, 90, 23), (1090, 372, 66, 24), (30, 480, 60, 25), (1215, 478, 64, 26)]:
    add(f'<ellipse cx="{cx_+10}" cy="{cy_+r*0.75:.0f}" rx="{r*1.1:.0f}" ry="{r*0.18:.0f}" fill="#7F7F7F" opacity="0.4"/>')
    foliage(cx_, cy_, r, s)

add('</svg>')
open('images/pothole-road.svg', 'w').write("\n".join(out))
print(len(out), 'elements')

"""Collider / selection example for the "Experimental data" slide.

Simulates attractiveness and pleasantness with NO true relationship, then
removes everyone above or below an oblique line (attractiveness + pleasantness
too high, or too low): being very attractive OR very pleasant is enough to
leave the sample at the top, and the same at the bottom. It then
saves each step as its own SVG layer so the slide can build them up as
fragments. All layers share one viewBox and stack exactly.

Run: python3 scripts/make_scatter.py   (writes images/sec1/scatter-*.svg)
"""
import math, random

random.seed(2024)
N = 200
N_DROP = 50         # removed: the 25 highest and the 25 lowest x + y

def draw():   # standard normal, redrawn if it would fall outside the plotted range
    while True:
        v = random.gauss(0, 1)
        if abs(v) < 2.7:
            return v
xs = [draw() for _ in range(N)]
ys = [draw() for _ in range(N)]
# remove the small chance correlation, so the full-sample line is exactly flat
mx, my = sum(xs) / N, sum(ys) / N
b0 = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
xs = [x - mx for x in xs]
ys = [y - my - b0 * x for x, y in zip(xs, ys)]
order = sorted(range(N), key=lambda i: xs[i] + ys[i])
cut = set(order[:N_DROP // 2] + order[-N_DROP // 2:])
excluded = [i in cut for i in range(N)]
kept = [(x, y) for (x, y), e in zip(zip(xs, ys), excluded) if not e]
dropped = [(x, y) for (x, y), e in zip(zip(xs, ys), excluded) if e]

def ols(pts):
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    b = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    r = b * math.sqrt(sum((x - mx) ** 2 for x, _ in pts) / sum((y - my) ** 2 for _, y in pts))
    return my - b * mx, b, r

a_sel, b_sel, r_sel = ols(kept)
a_all, b_all, r_all = ols(list(zip(xs, ys)))

# --- drawing ------------------------------------------------------------------
W, H = 640, 460
X0, Y0, X1, Y1 = 70, 20, 620, 380            # axes box
LIM = 3.0
def sx(v): return X0 + 15 + (v + LIM) / (2 * LIM) * (X1 - X0 - 30)
def sy(v): return Y1 - 15 - (v + LIM) / (2 * LIM) * (Y1 - Y0 - 30)

INK, DOT, RED, PINK = "#4D4D95", "#8F8DD0", "#C0393B", "#F28A8E"
FONT = 'font-family="Avenir Next, Nunito Sans, sans-serif"'

def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" {FONT}>\n'
            + body + '\n</svg>\n')

def axes(xlab="Attractiveness", ylab="Pleasantness"):
    return (f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{X1-10} {Y1-6} L{X1} {Y1} L{X1-10} {Y1+6}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="{X0}" y1="{Y1}" x2="{X0}" y2="{Y0}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{X0-6} {Y0+10} L{X0} {Y0} L{X0+6} {Y0+10}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{(X0+X1)/2}" y="{Y1+42}" text-anchor="middle" font-size="22" fill="{INK}">{xlab}</text>'
            f'<text transform="translate({X0-22} {(Y0+Y1)/2}) rotate(-90)" text-anchor="middle" font-size="22" fill="{INK}">{ylab}</text>')

def dots(pts, colour):
    return "".join(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.2" fill="none" stroke="{colour}" stroke-width="1.7"/>'
                   for x, y in pts)

def line(a, b, colour, extra=""):
    lo, hi = -LIM * 0.95, LIM * 0.95
    return (f'<line x1="{sx(lo):.1f}" y1="{sy(a + b*lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(a + b*hi):.1f}" '
            f'stroke="{colour}" stroke-width="3.5" stroke-linecap="round" {extra}/>')

def cut_region(c, above, wx=1.0, wy=1.0):
    """Shade the corner of the plot beyond the oblique line wx*x + wy*y = c
    (the people who are cut out), with the line itself dashed."""
    L = LIM * 0.97
    f = lambda p: wx * p[0] + wy * p[1]
    box = [(-L, -L), (L, -L), (L, L), (-L, L)]
    inside = (lambda p: f(p) >= c) if above else (lambda p: f(p) <= c)
    poly = []
    for i, p in enumerate(box):                       # clip the square by the half-plane
        q = box[(i + 1) % 4]
        if inside(p):
            poly.append(p)
        if inside(p) != inside(q):
            t = (c - f(p)) / (f(q) - f(p))
            poly.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    d = "M" + " L".join(f"{sx(x):.1f} {sy(y):.1f}" for x, y in poly) + " Z"
    ends = [pt for pt in poly if abs(f(pt) - c) < 1e-9]
    (x1, y1), (x2, y2) = ends[0], ends[-1]
    return (f'<path d="{d}" fill="{PINK}" opacity="0.3"/>'
            f'<line x1="{sx(x1):.1f}" y1="{sy(y1):.1f}" x2="{sx(x2):.1f}" y2="{sy(y2):.1f}" '
            f'stroke="{RED}" stroke-width="2" stroke-dasharray="7 6" opacity="0.7"/>')

# The shaded corners are drawn a bit further out than the real cut-off, so they
# stay narrow: SHADE = how far into the removed group the dashed line sits
# (0 = right at the edge of the kept people, 1 = at the most extreme person).
SHADE = 0.6
low_sums = sorted(x + y for x, y in dropped if x + y < 0)            # most extreme first
high_sums = sorted((x + y for x, y in dropped if x + y > 0), reverse=True)
c_low = low_sums[int((1 - SHADE) * (len(low_sums) - 1))]
c_high = high_sums[int((1 - SHADE) * (len(high_sums) - 1))]

out = "images/sec1/"
open(out + "scatter-1-selected.svg", "w").write(svg(axes() + dots(kept, DOT)))
open(out + "scatter-2-fit.svg", "w").write(svg(line(a_sel, b_sel, INK)))
open(out + "scatter-3-low.svg", "w").write(svg(cut_region(c_low, above=False)))
open(out + "scatter-4-high.svg", "w").write(svg(cut_region(c_high, above=True)))
open(out + "scatter-5-excluded.svg", "w").write(svg(dots(dropped, RED) + line(a_all, b_all, RED)))

print(f"kept {len(kept)}, excluded {len(dropped)}")
print(f"r among the people you see: {r_sel:+.2f}   r in everyone: {r_all:+.2f}")


# =============================================================================
# Second example: QC exclusion for head motion in brain data
# =============================================================================
# A real NEGATIVE association between attention problems and functional
# connectivity. Head motion goes up with attention problems, and high-motion
# scans also tend to show lower (long-range) connectivity, so the scans that
# fail QC sit in the high-attention-problems / low-connectivity corner. Losing
# that corner flattens the association in the scans that pass. Motion is
# noisy, so the cut is fuzzy rather than a sharp line.
random.seed(31)
N_B = 200
QC_FAIL = 50            # 25% of scans excluded, not unusual in paediatric samples

def brain_sample():
    xs = [draw() for _ in range(N_B)]
    ys = [-0.5 * x + math.sqrt(1 - 0.25) * draw() for x in xs]
    motion = [0.6 * x - 0.6 * y + random.gauss(0, 0.15) for x, y in zip(xs, ys)]
    worst = set(sorted(range(N_B), key=lambda i: motion[i])[-QC_FAIL:])
    keep = [(xs[i], ys[i]) for i in range(N_B) if i not in worst]
    drop = [(xs[i], ys[i]) for i in range(N_B) if i in worst]
    return xs, ys, keep, drop

# pick the draw whose QC-passed slope is closest to flat (the point of the slide)
best = None
for attempt in range(400):
    bx, by, bkeep, bdrop = brain_sample()
    if max(map(abs, bx + by)) > 2.85:
        continue
    _, slope, _ = ols(bkeep)
    if best is None or abs(slope) < abs(best[0]):
        best = (slope, bx, by, bkeep, bdrop)
_, bx, by, bkeep, bdrop = best
a_k, b_k, r_k = ols(bkeep)
a_a, b_a, r_a = ols(list(zip(bx, by)))
# dashed line further out than where failures start, so the shaded corner stays narrow
fail = sorted((x - y for x, y in bdrop), reverse=True)
c_qc = fail[int((1 - SHADE) * (len(fail) - 1))]

XL, YL = "Attention problems", "Functional connectivity"
open(out + "brain-1-selected.svg", "w").write(svg(axes(XL, YL) + dots(bkeep, DOT)))
open(out + "brain-2-fit.svg", "w").write(svg(line(a_k, b_k, INK)))
open(out + "brain-3-motion.svg", "w").write(svg(cut_region(c_qc, above=True, wx=1.0, wy=-1.0)))
open(out + "brain-4-excluded.svg", "w").write(svg(dots(bdrop, RED) + line(a_a, b_a, RED)))
print(f"brain: passed QC {len(bkeep)}, failed {len(bdrop)}")
print(f"r in scans that pass QC: {r_k:+.2f} (slope {b_k:+.2f})   r in everyone: {r_a:+.2f} (slope {b_a:+.2f})")

"""Custom-cut 9U rack: 2020 extrusion cut to exact length + 20 mm metal 3-way corner cubes.
Writes concept STLs and a dimensioned drawing page. X width (centred), Y depth front->rear, Z up, mm.
Concept only: cube size, fit, stiffness and strength UNKNOWN until parts are in hand."""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "custom")
os.makedirs(OUT, exist_ok=True)

# ---- one set of numbers drives the model, the drawings and the cut list
U = 44.45
E = 20.0                          # 2020 profile and corner cube size (cube size assumed = 20, check the parts)
INSIDE = 208.0                    # inside width between posts (current rack / app limit)
MOUNT = 240.0                     # front-to-rear distance between hole-strip mounting faces (OptiPlex sleeve)
T = 8.0                           # printed hole-strip thickness (M6 x 5 x 8 insert, 6 deep + 2 mm floor)
PLATE = 4.0                       # faceplate / rear plate thickness
HOLE_X = 118.2625                 # four-corner faceplate holes, ±X
HOLE_Z = 15.902                   # ±Z about each U centre (Lab Rax spacing; EIA would be 15.875)

POST_L = 400.0                    # 9U = 400.05; the 0.05 is not worth a custom length
WIDTH_L = INSIDE                  # 208
DEPTH_L = MOUNT - 2 * T - 2 * E   # 184
PX0, PX1 = INSIDE / 2, INSIDE / 2 + E          # post X 104..124
FY0 = 0.0                                      # front post outer face
RY1 = MOUNT - 2 * T                            # rear post outer face (224)
FY1, RY0 = FY0 + E, RY1 - E                    # 20, 204
STRIP_F, STRIP_R = (FY0 - T, FY0), (RY1, RY1 + T)
FACE_F, FACE_R = STRIP_F[0], STRIP_R[1]        # mounting faces: -8 and 232 (240 apart)
Z0, Z1 = E, E + POST_L                         # posts sit on the bottom cubes
H = Z1 + E                                     # 440

assert abs(FACE_R - FACE_F - MOUNT) < 1e-9 and DEPTH_L == RY0 - FY1 and abs(HOLE_X - PX0) < E

def box(x0, x1, y0, y1, z0, z1):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    i = lambda a, b, c: v[a * 4 + b * 2 + c]
    q = [(i(0,0,0), i(0,1,0), i(1,1,0), i(1,0,0)), (i(0,0,1), i(1,0,1), i(1,1,1), i(0,1,1)),
         (i(0,0,0), i(1,0,0), i(1,0,1), i(0,0,1)), (i(0,1,0), i(0,1,1), i(1,1,1), i(1,1,0)),
         (i(0,0,0), i(0,0,1), i(0,1,1), i(0,1,0)), (i(1,0,0), i(1,1,0), i(1,1,1), i(1,0,1))]
    return [t for a, b, c, d in q for t in ((a, b, c), (a, c, d))]

def write(name, tris):
    with open(os.path.join(OUT, name + ".stl"), "w", encoding="utf-8") as f:
        f.write(f"solid {name}\n")
        for t in tris:
            f.write(" facet normal 0 0 0\n  outer loop\n" + "".join("   vertex %.3f %.3f %.3f\n" % p for p in t) + "  endloop\n endfacet\n")
        f.write(f"endsolid {name}\n")
    return os.path.join(OUT, name + ".stl")

sides = [(PX0, PX1), (-PX1, -PX0)]
ends = [(FY0, FY1), (RY0, RY1)]
levels = [(0.0, E), (Z1, H)]
parts = {
    "posts_2020x400": [t for x in sides for y in ends for t in box(*x, *y, Z0, Z1)],
    "width_members_2020x208": [t for y in ends for z in levels for t in box(-PX0, PX0, *y, *z)],
    "depth_rails_2020x184": [t for x in sides for z in levels for t in box(*x, FY1, RY0, *z)],
    "corner_cubes_20mm": [t for x in sides for y in ends for z in levels for t in box(*x, *y, *z)],
    "printed_3U_hole_strips": [t for x in sides for s in (STRIP_F, STRIP_R) for k in range(3)
                               for t in box(*x, *s, Z0 + k * 3 * U + 0.2, Z0 + (k + 1) * 3 * U - 0.2)],
}
GEAR = [(1, 2, (180, 200, 80), True), (3, 1, (200, 120, 30), False), (6, 2, (190, 170, 78), False), (9, 1, (170, 140, 32), False)]
plates, gear = [], []
for s, n, (w, d, h), rear in GEAR:
    zb = Z0 + (s - 1) * U
    plates += box(-126, 126, FACE_F - PLATE, FACE_F, zb + 0.025, zb + n * U - 0.025)
    if rear:
        plates += box(-126, 126, FACE_R, FACE_R + PLATE, zb + 0.025, zb + n * U - 0.025)
    gear += box(-w / 2 - 4, w / 2 + 4, FACE_F, FACE_F + d + 2, zb + 1, zb + 3) + box(-w / 2, w / 2, FACE_F + 1, FACE_F + d, zb + 3, zb + 3 + h)
parts["faceplates_example"] = plates
parts["example_gear"] = gear
files = [write(k, v) for k, v in parts.items()]

# ---- drawings (SVG, mm units)
def dim(x1, y1, x2, y2, label, off, cls="dim"):
    """Dimension between two points along a horizontal or vertical line, offset perpendicular by off."""
    if abs(y1 - y2) < 1e-9:   # horizontal
        y = y1 + off
        return (f'<line class="ext" x1="{x1}" y1="{y1}" x2="{x1}" y2="{y + (4 if off > 0 else -4)}"/>'
                f'<line class="ext" x1="{x2}" y1="{y2}" x2="{x2}" y2="{y + (4 if off > 0 else -4)}"/>'
                f'<line class="{cls}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-start="url(#a)" marker-end="url(#a)"/>'
                f'<text class="dt" x="{(x1 + x2) / 2}" y="{y - 3}" text-anchor="middle">{label}</text>')
    x = x1 + off
    return (f'<line class="ext" x1="{x1}" y1="{y1}" x2="{x + (4 if off > 0 else -4)}" y2="{y1}"/>'
            f'<line class="ext" x1="{x2}" y1="{y2}" x2="{x + (4 if off > 0 else -4)}" y2="{y2}"/>'
            f'<line class="{cls}" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" marker-start="url(#a)" marker-end="url(#a)"/>'
            f'<text class="dt" x="{x - 4}" y="{(y1 + y2) / 2}" text-anchor="middle" transform="rotate(-90 {x - 4} {(y1 + y2) / 2})">{label}</text>')

def rect(x0, y0, x1, y1, cls):
    return f'<rect class="{cls}" x="{min(x0, x1)}" y="{min(y0, y1)}" width="{abs(x1 - x0)}" height="{abs(y1 - y0)}"/>'

def svg(vb, body, title):
    x, y, w, h = vb
    return (f'<figure><figcaption>{title}</figcaption><div class="scroll"><svg viewBox="{x} {y} {w} {h}" role="img" aria-label="{title}">'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            '<path d="M0 2 L10 5 L0 8 z" class="arrow"/></marker></defs>' + body + '</svg></div></figure>')

f = lambda v: f"{v:g}"
# front view: X right, Z up (svg y = -Z)
fv = []
for x0, x1 in sides:
    fv.append(rect(x0, -Z0, x1, -Z1, "alu"))
    for z0, z1 in levels:
        fv.append(rect(x0, -z0, x1, -z1, "cube"))
for z0, z1 in levels:
    fv.append(rect(-PX0, -z0, PX0, -z1, "alu"))
fv.append(rect(-126, -Z0, 126, -(Z0 + 2 * U), "plate"))
for zc in (Z0 + U / 2 - HOLE_Z, Z0 + U / 2 + HOLE_Z):
    for xs in (-HOLE_X, HOLE_X):
        fv.append(f'<circle class="hole" cx="{xs}" cy="{-zc}" r="3.2"/>')
for k in range(10):
    fv.append(f'<line class="tick" x1="{PX1 + 2}" y1="{-(Z0 + k * U)}" x2="{PX1 + 8}" y2="{-(Z0 + k * U)}"/>')
fv += [dim(-PX0, -H, PX0, -H, f"inside {f(INSIDE)}", -14), dim(-PX1, -H, PX1, -H, f"frame {f(2 * PX1)}", -32),
       dim(-126, 0, 126, 0, "faceplate 252", 16), dim(-HOLE_X, 0, HOLE_X, 0, f"holes {2 * HOLE_X:.2f}", 34),
       dim(-PX1, 0, -PX1, -H, f"overall {f(H)}", -18), dim(-PX1, -Z0, -PX1, -Z1, f"post {f(POST_L)} (9U)", -40),
       dim(PX1, 0, PX1, -Z0, "20", 22)]
front = svg((-185, -H - 50, 370, H + 100), "".join(fv), "Front view (one 2U faceplate shown at U1–U2)")

# side view: Y right (front on the left), Z up
sv = []
for y0, y1 in ends:
    sv.append(rect(y0, -Z0, y1, -Z1, "alu"))
    for z0, z1 in levels:
        sv.append(rect(y0, -z0, y1, -z1, "cube"))
for z0, z1 in levels:
    sv.append(rect(FY1, -z0, RY0, -z1, "alu"))
for s in (STRIP_F, STRIP_R):
    sv.append(rect(s[0], -Z0, s[1], -Z1, "print"))
sv.append(rect(FACE_F - PLATE, -Z0, FACE_F, -(Z0 + 2 * U), "plate"))
sv.append(rect(FACE_R, -Z0, FACE_R + PLATE, -(Z0 + 2 * U), "plate"))
sv += [dim(FY1, -H, RY0, -H, f"depth rail {f(DEPTH_L)}", -14), dim(FY0, -H, RY1, -H, f"frame {f(RY1 - FY0)}", -32),
       dim(FACE_F, 0, FACE_R, 0, f"mounting faces {f(MOUNT)}", 16),
       dim(FACE_F - PLATE, 0, FACE_R + PLATE, 0, f"with plates {f(MOUNT + 2 * PLATE)}", 34),
       dim(RY1, -Z1, RY1, -Z0, f"post {f(POST_L)}", 22), dim(FACE_F - PLATE, 0, FACE_F - PLATE, -H, f"overall {f(H)}", -16)]
side = svg((FACE_F - PLATE - 45, -H - 50, MOUNT + 2 * PLATE + 100, H + 100), "".join(sv), "Side view (front on the left)")

# top view: X right, Y down (front at the top)
tv = []
for x0, x1 in sides:
    for y0, y1 in ends:
        tv.append(rect(x0, y0, x1, y1, "cube"))
    tv.append(rect(x0, FY1, x1, RY0, "alu"))
    for s in (STRIP_F, STRIP_R):
        tv.append(rect(x0, s[0], x1, s[1], "print"))
for y0, y1 in ends:
    tv.append(rect(-PX0, y0, PX0, y1, "alu"))
tv.append(rect(-126, FACE_F - PLATE, 126, FACE_F, "plate"))
tv += [dim(-PX0, FACE_F - PLATE, PX0, FACE_F - PLATE, f"width member {f(WIDTH_L)}", -14),
       dim(-126, FACE_F - PLATE, 126, FACE_F - PLATE, "faceplate 252", -32),
       dim(PX1, FY1, PX1, RY0, f"rail {f(DEPTH_L)}", 18), dim(PX1, FACE_F, PX1, FACE_R, f"{f(MOUNT)}", 40),
       dim(-PX1, FY0, -PX1, RY1, f"frame {f(RY1 - FY0)}", -18)]
top = svg((-185, FACE_F - PLATE - 50, 370, MOUNT + 2 * PLATE + 75), "".join(tv), "Top view (front at the top)")

rows = [("2020 extrusion, posts", 4, f"{f(POST_L)} mm", "both ends tapped for the cube screws"),
        ("2020 extrusion, width members", 4, f"{f(WIDTH_L)} mm", "both ends tapped; sets the 208 mm inside width"),
        ("2020 extrusion, depth rails", 4, f"{f(DEPTH_L)} mm", "both ends tapped; sets the 240 mm mounting depth"),
        ("3-way corner cubes, 2020", 8, "20 mm", "screws usually included; check thread and size"),
        ("M6 x 5 x 8 heat-set inserts", "72 + spares", "", "in the printed strips, 2 per U per post"),
        ("M5 countersunk screws + roll-in T-nuts", "~40", "10–12 mm", "hole strips to posts"),
        ("Printed 3U hole strips", 12, f"{3 * U:.2f} x 20 x {f(T)} mm", "printed, not ordered")]
table = "".join(f"<tr><td>{a}</td><td class=n>{b}</td><td class=n>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows)

html = f"""<title>Custom 9U Rack Drawings</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* layout: drafting sheet, three orthographic views stacked, cut list after */
:root {{ --paper:#f6f8f9; --ink:#1d2a33; --muted:#5d6c76; --line:#c9d3d9; --alu:#9fb0bb; --cube:#4e6270; --print:#d9822b; --plate:#7aa6c2;
  --sans:"IBM Plex Sans", system-ui, sans-serif; --mono:"IBM Plex Mono", ui-monospace, monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --paper:#12181d; --ink:#dfe7ec; --muted:#93a3ad; --line:#2c3a43; --alu:#5d707c; --cube:#a9bccb; --print:#e39645; --plate:#4f7f9e; color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --paper:#12181d; --ink:#dfe7ec; --muted:#93a3ad; --line:#2c3a43; --alu:#5d707c; --cube:#a9bccb; --print:#e39645; --plate:#4f7f9e; color-scheme:dark; }}
body {{ background:var(--paper); color:var(--ink); font:15px/1.5 var(--sans); padding-block:24px 48px;
  padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); }}
main {{ max-width:900px; margin:0 auto; display:grid; gap:28px; }}
h1 {{ font-size:1.6rem; margin:0; text-wrap:balance; }} h2 {{ font-size:1.1rem; margin:0 0 8px; }}
.sub {{ color:var(--muted); margin:4px 0 0; max-width:65ch; }}
.views {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:20px; }}
figure {{ margin:0; border:1px solid var(--line); border-radius:6px; padding:12px; min-width:0; }}
figcaption {{ font:500 12px var(--mono); letter-spacing:.04em; text-transform:uppercase; color:var(--muted); margin-bottom:8px; }}
.scroll {{ overflow-x:auto; }} svg {{ width:100%; height:auto; min-width:240px; display:block; }}
.alu {{ fill:var(--alu); stroke:var(--ink); stroke-width:.4; }} .cube {{ fill:var(--cube); stroke:var(--ink); stroke-width:.4; }}
.print {{ fill:var(--print); stroke:var(--ink); stroke-width:.4; }} .plate {{ fill:var(--plate); fill-opacity:.55; stroke:var(--ink); stroke-width:.4; }}
.hole {{ fill:var(--paper); stroke:var(--ink); stroke-width:.5; }} .tick {{ stroke:var(--muted); stroke-width:.6; }}
.dim {{ stroke:var(--ink); stroke-width:.5; fill:none; }} .ext {{ stroke:var(--muted); stroke-width:.3; }} .arrow {{ fill:var(--ink); }}
.dt {{ font:500 7.5px var(--mono); fill:var(--ink); }}
.legend {{ display:flex; flex-wrap:wrap; gap:8px 18px; font-size:13px; color:var(--muted); }}
.legend span::before {{ content:""; display:inline-block; width:12px; height:12px; border-radius:2px; margin-right:6px; vertical-align:-2px; background:var(--c); }}
.tbl {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; min-width:520px; font-size:14px; }}
th, td {{ text-align:left; padding:7px 10px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ font:500 12px var(--mono); text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }}
td.n {{ font-family:var(--mono); font-variant-numeric:tabular-nums; white-space:nowrap; }}
ul {{ margin:0; padding-left:20px; max-width:70ch; }} li + li {{ margin-top:4px; }}
</style>
<main>
<header><h1>Custom 9U Rack</h1>
<p class="sub">2020 aluminium cut to exact length, joined by 20 mm metal 3-way corner cubes. Same inside dimensions as the current rack, so existing faceplates, trays and sleeves fit. All sizes in mm.</p></header>
<div class="legend"><span style="--c:var(--alu)">2020 extrusion</span><span style="--c:var(--cube)">corner cube</span><span style="--c:var(--print)">printed hole strip</span><span style="--c:var(--plate)">faceplate / rear plate</span></div>
<section class="views">{front}{side}</section>
<section class="views">{top}</section>
<section><h2>Cut list and parts</h2><div class="tbl"><table><thead><tr><th>Part</th><th>Qty</th><th>Size</th><th>Note</th></tr></thead><tbody>{table}</tbody></table></div></section>
<section><h2>Checks and assumptions</h2><ul>
<li>Inside width {f(INSIDE)} = width member length (cubes sit on the post line). Frame width {f(2 * PX1)}; faceplates {f(252)} overhang 2 mm a side.</li>
<li>Mounting depth: rail {f(DEPTH_L)} + two posts {f(2 * E)} + two strips {f(2 * T)} = {f(DEPTH_L + 2 * E + 2 * T)}. A different strip thickness changes the rail length: rail = 240 &minus; 40 &minus; 2 &times; strip.</li>
<li>Height: cube {f(E)} + post {f(POST_L)} + cube {f(E)} = {f(H)}. 9U is 400.05; the 0.05 mm is not worth cutting for.</li>
<li>Hole line &plusmn;{HOLE_X} falls on the post face ({f(PX0)}–{f(PX1)}), {PX1 - HOLE_X:.2f} mm from its outer edge.</li>
<li>Assumed, not yet checked: corner cubes are exactly 20 mm and flush with the profile; the cube screw thread (the listing says M6, 2020 ends usually take M5); strip thickness {f(T)} mm.</li>
<li>Order tolerance &plusmn;0.2 mm, square ends. Fit, stiffness and strength UNKNOWN until built.</li>
</ul></section>
</main>"""
with open(os.path.join(OUT, "Custom_Rack_Drawings.html"), "w", encoding="utf-8") as fh:
    fh.write(html)
print(f"post {POST_L} width {WIDTH_L} depth {DEPTH_L} frame {2*PX1}x{RY1-FY0}x{H} mount {FACE_R-FACE_F}")
print("\n".join(files))

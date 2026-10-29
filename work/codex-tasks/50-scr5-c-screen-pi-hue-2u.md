# Task 50 — SCR5-C: 2U screen + Pi 4 + Hue + keystone unit (U4–U3)

Brian, 2026-10-29. New revision **SCR5-C**, an *option* beside SCR5-B (SCR5-B, SCR5-A, HP4-M6-A/B stay immutable; nothing in `outputs/Final_3MF/` changes). One 2U unit at U4–U3 holds everything that was in U5 plus the screen, so the DSI ribbon becomes short and **U5 is freed**.

## Brian's decisions (2026-10-29)
- Seen from the front: **screen on the left**, **Pi 4 lower right**, **Hue Bridge + keystone top right**.
- Hue sits flat on an **upper-right shelf that extends left behind the screen** (Hue ~88 × 88 does not fit the ~70 mm right zone). The keystone goes on the faceplate top right.
- Pi lies flat with its **USB/Ethernet end facing the faceplate**, openings in the plate lower right (same port openings as HP4, translated, never mirrored).
- **Loaded tray with M6 tray joints**: faceplate + floor tray joined with the rack M6 heat-set inserts and M6 × 8 button heads, exactly like HP4-M6-B (`m6_tray_joint_add/cut`, `jzx`). Normal four-corner rack holes, 44.4 mm/U standard (plate 252 × 88.8 × 4, R2.5, slots X ±118.2625, Z 6.323/38.127/50.773/82.577).

## Sources (read-only)
- Screen pocket, lip, rounded window, M2.5 plate bosses and rear clamp frame: `outputs/Screen_5in_SCR5-B_2026-10-29/` (`src/SCR5-B.scad`, `SCR5-B_parameters.json`). Keep the whole screen-retention design unchanged, only translated in X.
- Pi board/standoffs/port openings, Hue cradle import, golden keystone (`ks_tight=0.2`), M6 joints: `outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad`. The Hue cradle stays imported in place from `C:/Users/brian/Downloads/Swanky Rottis.stl`; never copy it into the repo.
- Screen dimensions: `work/screen-5in/Dimensions.md`.

## Starting layout (parameters; adjust only if a check fails, and report why)
Coordinates as SCR5-B: X negative = left from front, plate rear Y=0, Y+ into rack, Z up from U3 slot bottom. Rack inner opening ±104 (everything behind the plate stays inside, 2 mm side clearance).
- `screen_cx` = -33 (pocket outer about X -101.75..35.75). Lip, window R4, bosses, frame all move with it.
- Pi zone X ≈ 38..102: Pi rotated so the 56 mm width runs along X, 85 mm along Y, USB/Ethernet end toward the plate (`front_gap` as HP4). Board on the floor tray, standoffs/inserts as HP4. Port openings in the plate lower right, from HP4's openings translated.
- Hue shelf deck above the Pi: clear the Pi's tallest part (~20 mm + standoff) by ≥ 3 mm, Hue top ≤ 86 mm. Deck spans from the right zone leftward **behind the screen** (deck starts behind the clamp-frame screw heads/tool envelope, SCR5-B Y 26.5 + tool clearance). Hue cradle sits on the deck; supports go down to the floor tray, not onto the screen frame.
- Keystone (golden, unmirrored) top right of the plate, about X 92, upper U; must clear the Pi openings, rack slots (2 mm) and plate outline.
- DSI ribbon: screen connector (left top of screen, ~X screen_cx-52) to the Pi DSI connector. Route behind the screen across to the Pi; add cable guides/notches if needed. Report the route length with the same allowances as task 48/49 (insertion 16, slack 15, bends 10). Target ≤ 160 mm with the stock cable; if not, say so.
- Pi power (USB-C) and HDMI side must stay reachable or routable to the rear; report what is blocked.
- Engrave `SCR5-C` on the rear (tray or frame), not the front.

## Parts / outputs
`outputs/Screen_Pi_Hue_SCR5-C_2026-10-29/`: `SCR5-C_faceplate.stl`, `SCR5-C_tray.stl` (floor + Hue shelf; split only if not printable, explain), `SCR5-C_frame.stl` (screen clamp frame), one plain-tag 3MF with each part as a separate object side by side (12 mm gap, each min Z=0, sensible print orientation), parameterized `src/SCR5-C.scad`, `SCR5-C_parameters.json`, Python 3.10 stdlib `src/SCR5-C_build.py` with `--final` and `--check-only`, `checks/`, README with BOM (M6 inserts/M6×8 count, M2.5 inserts/screws, Pi screws) and assembly order. Explicit OpenSCAD.exe build only.

## Acceptance checks (all must PASS, else stop and report)
1. Every STL one closed, consistently wound shell, positive volume, no degenerate faces.
2. Plate 252 × 88.8 × 4, eight slot boundaries identical to SCR5-B.
3. Screen retention geometry identical to SCR5-B after the X translation (compare pocket, lip, window, bosses, frame vertices with a pure offset).
4. Assembly: no unintended intersections between tray, shelf, frame, screws (head + tool envelope), screen envelope (12.6 deep), Pi envelope (board + ports, standoff), Hue envelope and keystone collar. Screen still slides in from the rear with the frame removed; the frame can be removed with the shelf in place (state the tool path).
5. Everything behind the plate inside X ±102; tray depth ≤ HP4's 123.4 unless needed (report).
6. M6 joint modules byte-identical to HP4-M6-B; keystone geometry unchanged and not mirrored; Pi openings and cradle not mirrored.
7. 3MF: literal `<vertex>`/`<triangle>` tags, no `ns0`, all objects named `SCR5-C …`, exact geometry roundtrip.
8. SCR5-A/B, HP4-M6-A/B, Final_3MF, app, `data/normal-use` hashes unchanged.

## Don't
No printing, no Final_3MF copy, no app/library/rack-document changes, no data/normal-use, no mirroring, no subagents. Physical fit, shelf strength, ribbon reach, heat and access stay UNKNOWN. Write `50-scr5-c-screen-pi-hue-2u-REPORT.md` next to this spec, update HANDOFF.md, commit only task-owned files and push to private main.

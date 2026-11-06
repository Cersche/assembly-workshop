# Task 53: rack top fan parts, release prep + joint test coupon (no release)

**Brian (2026-11-05): use the stock source values in `docs/devices/lab-rax-top.md` for the joint; no measurements needed.** E is measured (about 35). Printer bed J is UNKNOWN: assume 256 x 256 and report the margin. Draft 3 is the go (Brian 2026-11-05).

## Goal
Turn the draft `work/rack-top-fan/rack_top_fan.scad` (option B, Brian 2026-11-05) into parts ready for `tools/release_part.py`, plus one small joint test coupon. Do not release, print or create an outputs/ folder: Claude releases when Brian says he is printing.

## Read first
AGENTS.md; `.claude/skills/new-part/SKILL.md`; `lib/README.md`; `docs/devices/lab-rax-top.md`; `docs/devices/fan-200mm.md`; `work/rack-cooling/Decisions.md` (last section); the draft SCAD.

## Work (all in `work/rack-top-fan/rack_top_fan.scad`)
**Draft 3 (2026-11-05) has no panel: the parts are edge_front, edge_rear, rail (print 2; rail_left is the same shape mirrored) and grille. Skip every panel item in this list; the coupon has the grille seat instead of the panel recess. Add `rail_print` (lying on its outer face) and tag `TSR-A`. Add a second coupon `rail_coupon`: the rail's front end only, Y 35..75 (tongue pocket, cross-hole, groove, one M6 insert), tag `TSR-T1`, so the edge coupon and the rail coupon test the joint together.**
1. Update the joint values (plug, tongue, cross-holes, panel recess) from the card's measured column. Keep every value marked measured exactly; keep `fit=0.3` and the 0.5 fan fit unless the card says otherwise.
2. Add `part=="keepout"`: `ws_head_keepout()` for every M3 countersunk head (panel to edges, grille to posts), and room for an M6 x 8 button head at any cross-hole Brian says takes a screw.
3. Add `part=="cuts"`: each grille opening and the panel's cable hole as separate solids (check-only), so `--cuts` can count them.
4. Add print parts in their print orientation, named `edge_front_print`, `edge_rear_print`, `panel_print`, `grille_print`: edges lying on their back (inner face Y 35 down) so the plugs and tongues print upright; panel and grille flat. If the printer bed (row J) is smaller than an edge's footprint, place the edge diagonally and report the margin.
5. Add parameter `tag` and engrave it 0.6 deep where it touches nothing that fits: edges on the inner face (Y 35) mid-length, panel underside near a corner, grille underside. Defaults: `TFE-A` front edge, `TRE-A` rear edge, `TFP-A` panel, `TFG-A` grille.
6. Add `part=="coupon"`: one end of the front edge only, X 101..141.12 (plug, tongue, cross-holes, panel recess, one M3 insert), tag `TFE-T1` on the inner face. This is the first print to try the joint on the real post and rail.
7. Render every part with the snapshot: `D:\Tools\OpenSCAD-snapshot\OpenSCAD-2026.11.01-x86-64\openscad.exe --backend=manifold` (library path `lib`). Each must be one body with no warnings. 
8. Dry-run checks into a scratch folder outside outputs/ (e.g. `%TEMP%`): `python tools/release_part.py work/rack-top-fan/rack_top_fan.scad --id TFE-T1 --part coupon:TFE-T1 --keepout keepout -o <scratch>` and the same for the four print parts with `--cuts cuts=<N>` on the grille. Report each FAIL/WARN as is; don't work around one.
9. Clash check in the assembly frame against the stock top meshes, as in the draft session: build them from `outputs/Mechanical_Design_App/rack-references/component_*.json` with the poses in `rack-references/rack-scene.js` (9 slots). Expected: edges clear the posts and rails; new rails clear the posts and the stock handles raised 15 (Z +15); edges, rails, grille and fan dummy don't overlap each other.

## Don't touch
Any other part, `lib/workshop.scad`, the app, outputs/, data/normal-use/, the creator's meshes. Never write a creator mesh into the repo; viewer pages that embed them stay uncommitted. No printing, no 3MF in outputs/Final_3MF.

## Report
`work/codex-tasks/53-rack-top-fan-prep-REPORT.md`: values changed (old → new, source), part list with bounding boxes and body counts, release dry-run output (FAIL/WARN), clash volumes, anything still UNKNOWN.

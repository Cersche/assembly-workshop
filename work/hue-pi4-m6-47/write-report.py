from pathlib import Path
import json,hashlib,subprocess
R=Path('D:/Projects/assembly-workshop');O=R/'outputs/Hue_Pi4_M6-B_2026-10-28';W=R/'work/hue-pi4-m6-47';a=json.loads((O/'checks/acceptance.json').read_text(encoding='utf-8'));c=a['clearance'];v=json.loads((W/'final-verification.json').read_text(encoding='utf-8'))
readme='''# HP4-M6-B - Hue + Pi 4 bracket, Pi left / Hue right

Test-print ID **HP4-M6-B**; 0.6 mm engraving on the rear plate at X=34.5, Z=8 and floor at X=34.5, Y=119. **Not printed. Fit, strength and DSI ribbon reach UNKNOWN.**

| File | Purpose |
| --- | --- |
| `HP4-M6-B_Hue_Pi4_M6_set.3mf` | Two named objects side by side, both minimum Z=0 |
| `HP4-M6-B_tray.stl`, `HP4-M6-B_faceplate.stl` | Assembly-coordinate parts, one closed shell each |
| `src/HP4-M6-B.scad` | Patch of immutable HP4-M6-A; no generator rebuild |
| `src/HP4-M6-B_build.py` | Python 3.10 standard library; OpenSCAD.exe; topology/contact checks; pack via tools/plate_layout_stl.py |
| `checks/acceptance.json`, `checks/clearance.json` | Numeric acceptance and clearance evidence; logs/probes alongside |

**Bracket BOM:** 3 x rack M6 heat-set insert + 3 x M6 x 8 button-head screw.

**Pi board mounting (unchanged, pending Brian):** four device insert mounts, 3.2 mm pilots, 6 mm standoffs, Pi holes 2.7 mm. Pi insert specification and board screws remain pending Brian; they are separate from the bracket BOM.

Changes from A are translations only: Pi -148 mm (X -102..-46, rotation 270 and Y unchanged); openings X -93/-75/-56.3; Hue cradle +69 mm to X=34.5; golden keystone +185 mm to X=92.5; ties X=-42.5/-19.5; joints X=-29.5/11/57; floor X=-102..82.5, depth 123.4 unchanged; new IDs at X=34.5. The 33.1 mm lane now lies at X=-46..-12.9. No mirroring of devices, openings, cradle or keystone.

The swap puts the Pi on the connector side of the planned upright, centred Waveshare 5-inch DSI screen in U4-U3 beneath the U5 bracket. **Routing and 160 mm cable reach are not validated.** No ribbon slot or other feature was added.

Preserved: complete A M6 joint geometry, 20 mm tabs plus inherited 4 mm low coves, 14 mm bosses, 7.6 mm bores, 6.6 mm screw clearance, 11.5 x 3.5 counterbores, jzx=[24], screw Z=32.225, tongues/slots; four corner rack slots only; nominal 252 x 44.4 x 4 plate; Pi mounts and openings' dimensions/heights; cradle cut/Z; golden geometry and ks_tight=0.2.

Digital checks: tray 7,256 triangles / 10,884 edges; faceplate 5,232 triangles / 7,848 edges. Each has one shell, zero bad edges and zero inconsistent winding edges. Contact intersection: 760 triangles all exactly Y=0, zero volume. Rear X=-102..102.4 lies inside +/-104. 3MF literal plain vertex/triangle tags: tray 3,620/7,256; faceplate 2,602/5,232; no ns0 prefixes. One collinear tray triangle and two collinear plate triangles remain, as in A; no mesh repair or rounding.

Clearances are documented in `checks/clearance.json` and `../../work/codex-tasks/47-hue-pi4-m6-b-REPORT.md`. Full-joint guaranteed minimum gaps to the checked device/port/cradle/tie/keystone envelopes are 6.5 / 8.4 / 8.4 mm. The lane tab is 6.5 mm from the Pi edge. Low coves extend closer in XY below the board; the rendered full joint still clears the Pi box by 6.5 mm. Cradle right inset 0.5 mm; keystone rear-to-floor gap 0.1 mm; tray ID-to-cradle guaranteed gap 1.246 mm.

Rebuild with `py -3.10 src/HP4-M6-B_build.py` from this folder. The builder requires passing `checks/clearance.json` before rendering/packing. Evidence scripts in `../../work/hue-pi4-m6-47/` regenerate probes and check clearances (`probe-clearance.py`, `check-clearance.py`, then `check-joint-coves.py`; the last uses `checks/lane-joint.scad/.stl`). Keep this evidence with the source. Reassess clearances if source or cradle changes. No automatic build.

The cradle remains imported directly from `C:/Users/brian/Downloads/Swanky Rottis.stl`, never copied. Creator/imported geometry stays local/private; no redistribution outside the authorized private repository. No Final_3MF copy.

UNKNOWN: printed fit/strength, load capacity, insert OD/length, retention, insertion bulging, usable thread engagement, Pi mounting hardware, cable bend room, DSI ribbon reach and slicer behaviour. Digital closure does not establish physical approval. No printing, physical testing, commit or push performed.
'''
(O/'README.md').write_text(readme,encoding='utf-8')
report='''# Task 47 - HP4-M6-B Hue + Pi 4 bracket

Completed 2026-10-29 in `D:/Projects/assembly-workshop`. First command: `git pull`, already up to date. Python 3.10.11 standard library and `C:/Program Files/OpenSCAD/openscad.exe`; no .com launcher. AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md and task 47 read. No printing, commit or push.

## Changes and source preservation

Patched `outputs/Hue_Pi4_M6_2026-10-28/src/HP4-M6-A.scad` into `outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad`. Only the spec table's 11 literal replacements plus HP4-M6-A -> HP4-M6-B ID/comment renaming were made. Reversing exactly these changes recovers A's complete normalized source text, including every M6 module, boss, pilot, counterbore, tongue/slot and jzx=[24]. Full diff: `work/hue-pi4-m6-47/source.diff`.

Pi translates -148 mm to footprint X=-102..-46; openings -93/-75/-56.3. Hue translates +69 mm to cradle X=34.5; ghost follows. Keystone translates +185 mm to 92.5, without mirroring. Floor -102..82.5, ties -42.5/-19.5, joints -29.5/11/57; IDs move to X=34.5 with B text. Depth 123.4, Pi rotation 270, Y=-12, Pi holes/pilots/standoffs, port sizes/Z/radii, cradle cut/Z and all other features remain A. No new slots or openings. One pre-existing `mirror()` remains only in the unused rear-bracket helper; zero new mirror calls and none applied to the swapped items.

The DSI reason is to put the Pi on the left of the U5 tray, above the left-edge connector of the planned upright, centred U4-U3 screen. Reach is UNKNOWN; this work does not validate the 160 mm ribbon or add a floor slot.

## Part and package acceptance

| Check | Result |
| --- | --- |
| OpenSCAD.exe part renders | PASS; exit 0 for both, Simple=yes, no empty/invalid-geometry warnings; 35 inherited assignment-override notices each |
'''
for part in ['tray','faceplate']:
 d=a[part];report+=f"| {part} exact mesh | PASS; {d['triangles']:,} triangles, {d['vertices']:,} vertices, {d['edges']:,} edges; {d['bad_edges']} bad edges, {d['inconsistent_edges']} inconsistent winding edges, {d['shells']} shell; signed volume {d['signed_volume_mm3']:.8f} mm3 |\n"
report+='''| Degenerate triangles | Explicitly counted: tray 1, faceplate 2, same counts as A; collinear ASCII facets; exact edge closure still passes, no repair/welding/rounding |
| Faceplate intersect tray | PASS; contact only, 0 volume; 760 triangles, all 2,280 exported vertex occurrences exactly Y=0; no relief added |
| Behind-plate X | PASS; tray -102..82.5, faceplate -36.5..102.4, combined -102..102.4 within -104..104; margins 2.0 left / 1.6 right |
| Source scope | PASS; complete reverse-patch recovery; full diff saved; joint geometry and all unlisted source retained |
| 3MF layout | PASS; 2 separate named objects, 2 build items, both min Z=0; faceplate maximum print Y=-10, tray minimum Y=0: 10 mm separation |
| 3MF plain XML tags | PASS; tray 3,620 plain `<vertex ` and 7,256 plain `<triangle ` tags; faceplate 2,602 / 5,232; totals 6,222 / 12,488; 0 `ns0:` prefixes; per-object counts match STL |
| Bracket BOM | 3 rack M6 inserts + 3 M6 x 8 button heads; Pi board mounting unchanged and pending Brian |

Contact probe alone has expected non-manifold warnings from its zero-thickness Y=0 surfaces. These do not occur in either actual part render. Exact assembly bounds: tray X=-102..82.5, Y=0..123.4, Z=8.225..42.225; faceplate X=-126..126, Y=-4.07999..8, Z=0.0249939..44.425 (OpenSCAD serialization of nominal 0.025 lower edge). Packed tray bounds X=-102..82.5, Y=0..123.4, Z=0..34; packed plate X=-126..126, Y=-54.400006..-10, Z=0..12.07999.

## Clearance checks 1-5

All dimensions below are mm. Positive bounding-box separation proves clearance conservatively; it is a lower bound, not a claim of the exact closest point on the imported cradle. Pi/port distances use the rendered full joint triangles against their conservative boxes, including every inherited cove. Box separation and triangle vertex/edge distance calculations use Python standard library, no geometry library or coordinate rounding. Rounded openings lie inside the tested boxes.

1. **Golden keystone:** full X=82..103, rear (Y>0) X=82.6..102.4, rear depth max Y=6.31999. Floor edge X=82.5 gives 0.1 separation, matching A's rear gap (-82.6 against floor -82.5). Nominal full-block X overlap is 0.5 in both A and B; the outer front flange is in the plate plane, not a new rear-floor clash. Keystone-to-cradle guaranteed Y gap 16.38001; right joint full-cove envelope ends X=71, leaving 11.6 (nominal tab ends X=67, leaving 15.6). Geometry only translated; golden asymmetry preserved.

2. **Pi openings and plate webs:** conservative horizontal webs to the right edge of the left rack slots (-118.2625+5=-113.2625) and to the straight left plate edge (-126):

| Port centre X | Rack-slot web | Left edge web | Bottom web | Top web |
| --- | --- | --- | --- | --- |
'''
for d in c['pi_opening_webs']:
 report+=f"| {d['port_x']:g} | {d['left_rack_slot_horizontal_web_mm']:.4f} | {d['left_plate_edge_web_mm']:.4f} | {d['bottom_web_mm']:.3f} | {d['top_web_mm']:.3f} |\n"
report+='''
3. **M6 joints:** tabs remain centre +/-10, bosses radius 7, foot ends Y=14.3. Cov es extend a further 4 mm at the floor (included below). Guaranteed minimum distances to the checked envelopes:

| Joint X | Pi box | Pi opening boxes | Cradle | Tie slots | Keystone rear | Smallest guaranteed |
| --- | --- | --- | --- | --- | --- | --- |
'''.replace('Cov es','Coves')
for d in c['joints']:
 g=d['gap_lower_bounds_mm'];report+=f"| {d['x']:g} | {g['pi_footprint']:.5f} | {g['pi_openings']:.5f} | {g['cradle_posts']:.5f} | {g['tie_slots']:.5f} | {g['keystone_rear']:.5f} | {d['smallest_guaranteed_gap_mm']:.5f} |\n"
report+='''
Lane tab X=-39.5..-19.5 clears Pi edge -46 by **6.5 >= 5**. The inherited low coves reach X=-43.5..-15.5 (2.5 projected X gap), but their top is Z=15.215, below Pi bottom Z=17.225. A full rendered joint-to-Pi-box distance check, including these curved coves, returns **6.5**, so the 5 mm condition passes without altering A's geometry. The lane width remains 33.1.

4. **Imported cradle after cut:** rendered bounds X=-13..82, Y=22.7..117.7, Z=11.18..38.88. Right edge 82 is 0.5 inside tray edge 82.5; left inset 89; rear inset 5.7. Tie slot nearest right edge is -16.5, giving 3.5 X gap to cradle -13. Cradle front Y=22.7 vs full joint feet Y=14.3 gives 8.4 Y gap. Pi-to-cradle X gap is 33.0 to the imported mesh, versus the table's 33.1 nominal lane/device boundary; no dimension changed to hide this 0.1 difference.

5. **IDs:** actual text-cut bounds (font rendered locally) and conservative separations:

| ID | X bounds | Y bounds | Z bounds |
| --- | --- | --- | --- |
| Plate | 22.0606..47.1525 | -0.6..0.01 | 7.94577..11.8789 |
| Tray | 22.0606..47.1525 | 118.946..122.879 | 10.625..11.235 |

| ID | Bosses | Pi openings | Rack slots | Cradle | Tie slots | Keystone rear | Tongue/slots |
| --- | --- | --- | --- | --- | --- | --- | --- |
'''
for name in ['plate-id','tray-id']:
 d=c['ids'][name]['gap_lower_bounds_mm'];report+='| '+name+' | '+' | '.join(f'{d[k]:.5f}' for k in ['bosses','pi_openings','rack_slots','cradle_posts','tie_slots','keystone_rear','tongue_slots'])+' |\n'
report+='''
Tray text stays 0.521 inside the rear floor edge and at least 1.246 from cradle. The whole plate-ID AABB and a tab AABB overlap slightly; that preliminary screen is inconclusive, not a geometry failure. Exact OpenSCAD intersection of the actual plate-ID text with all M6 tray additions is empty (exit 1, normal empty-object result), so no fix or relocation was made. Every required clearance passes.

## Preservation, evidence and limits

Protected before/after SHA-256 manifests are `work/hue-pi4-m6-47/protected-before.json` and `protected-after.json`: **376 files, 0 changed, 0 missing, 0 added** in the selected protected paths. Includes A, older Hue folders, Final_3MF, other bracket baselines/deliveries, generator sources, tools, data/normal-use and original Downloads cradle. Protected git status unchanged; pre-existing unrelated untracked files preserved. Active data was only hashed, never used for tests. No cradle STL copied, no generator/tools/other-bracket edits, no Final_3MF copy, no app/server or desktop-control session.

`checks/acceptance.json` and logs retain mesh counts/contact/3MF evidence; `clearance.json`, probe SCAD/STLs and logs retain clearance evidence. `work/hue-pi4-m6-47/` holds full source diff, independent verification scripts/results, preservation manifests/status and three local viewer pages (assembled, print layout and diagnostic probes). Viewer pages are preview-only and not committed. SendUserFile is unavailable in this Codex tool set; the assembled page is opened in Codex and local links supplied instead. Viewer files are kept with task evidence as requested.

No geometry deviations from the table. Full-cove checks supplement the nominal-tab screen. One collinear tray facet and two plate facets remain consistent with A; slicer behaviour is untested. Fit, strength, load, retention, insert OD/length, insertion bulging, usable thread engagement, Pi hardware, cable bend room and DSI ribbon reach remain **UNKNOWN**. No printing, physical testing, uploads, publishing, release, commit or push.
'''
(R/'work/codex-tasks/47-hue-pi4-m6-b-REPORT.md').write_text(report,encoding='utf-8')
p=R/'HANDOFF.md';s=p.read_text(encoding='utf-8');marker='## 2026-10-29 Task 47 - HP4-M6-B digital checks complete\n\n'
assert marker not in s
entry=marker+'Built the specified translated swap in `outputs/Hue_Pi4_M6-B_2026-10-28/`; HP4-M6-A and its M6 geometry preserved. Pi left, Hue/keystone right, no mirroring or extra features. Tray 7,256 / plate 5,232 triangles, each one closed shell; contact only at Y=0, 0 volume; all five clearance checks pass (full lane joint to Pi 6.5 mm); rear X=-102..102.4. Two-object 3MF has plain vertex/triangle tags, both min Z=0. 376 protected file hashes unchanged. Report: [task 47](work/codex-tasks/47-hue-pi4-m6-b-REPORT.md); local viewers/evidence in `work/hue-pi4-m6-47/`. Next: Brian/Claude review; no Final_3MF copy, printing, commit or push authorized/performed. Fit, strength and DSI ribbon reach UNKNOWN.\n\n'
pos=s.index('## ');s=s[:pos]+entry+s[pos:];p.write_text(s,encoding='utf-8')
print('README, task report and handoff written')

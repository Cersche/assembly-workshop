# Task 40 — 9U rack: switch/keystone alignment, Pi + Hue USB slot (parts A, B); screen plate and cooling briefs (C, D, blocked)

Status: SPEC (Claude, 2026-10-22). Source plan: [work/rack-plan/Rack_Plan_9U.html](../rack-plan/Rack_Plan_9U.html). U numbers count from the BOTTOM (U1 = bottom); stored slot numbers count from the top (`U = slots - slot + 1`, 9 slots → U8 = slot 2, U7 = slot 3, U6 = slot 4). Brian's answers (2026-10-22): the HDD connects by USB-SATA adapter; one 80 mm exhaust fan (U1–U2 rear) for now.

Everything here is PROPOSED — UNVALIDATED. Fit, airflow, cable bend space and strength stay UNKNOWN. Use only NEW disposable data, never data/normal-use. No printing, no pushes, no auto-builds. Every new test print gets a unique ID modeled into the part (AGENTS.md).

## Part A — U8 switch faceplate lined up with the U7 keystone panel
Goal: U7 is a 10-keystone panel (3 USB, 4 Ethernet, 3 blank; keystones evenly spaced, reference layout in the task-38 faceplate-only slot). U8 is the TP-Link TL-SG108E. The four Ethernet keystones sit at positions 4–7 of 10. The switch's ports 2–5 should line up under them, so the 15 cm jumpers go straight up. Plan option 2 = keep keystones evenly spaced, offset the switch ~15 mm to the right (standing in front).
1. Measure the switch RJ45 pitch, first-port offset from the case edge and case size from `C:\Users\brian\Downloads\TP-Link TL-SG108.stp` (read in place, never copy; the SG108 and SG108E share the case but say so and flag it UNKNOWN). Use `mesh_study.py` / the existing wizard import (Y is up). If the STEP cannot give port centres, stop and list the exact caliper measurements Brian should take (port centre-to-centre, case width, edge to first port) instead of guessing.
2. Compute the keystone X positions of the 10-keystone panel and the switch port X positions for `dev_off_x` = 0 and find the offset that minimises the worst error over ports 2–5 vs keystones 4–7. Report the per-port misalignment in mm for that offset and for +15 mm. If the pitches differ so ports cannot all line up, report the best offset and the residual, and offer the alternative of non-even keystone spacing for the four Ethernet ones (do not apply it).
3. Build the U8 item with the existing generic path (sleeve mount, `tray_follow`, 44.4 mm plate). Ports face out. NO uplink keystone this time (all 8 ports are used). Make it a saved example only if Brian confirms; otherwise leave it as a spec + disposable-data render.
4. Add a check script or test that prints the alignment table so it can be re-run.
Acceptance: existing Python + JS checks pass; other library items byte-identical; U8 render (`assembly`, `tray`, `faceplate`) closed; alignment table in the report.

## Part B — U6 Pi 4 + Hue tray: front USB slot, hidden HDMI exit
Item: the saved library item "Philips Hue Bridge + Raspberry Pi 4 (keystone)" (`eq-de5e30c93309`; Hue 88 × 88 × 26 clips, Pi rotated 90° at dev_off_x +46, keystone at −100). Read its spec from `data/normal-use/equipment-library.json` (READ ONLY; copy into disposable data).
1. The Pi's USB and Ethernet face the front. Add a small slot (opt-in key, absent = byte-identical sources) in the faceplate BELOW the Pi's USB stack so a down-angled USB-A to micro-USB cable (~30 cm) can leave towards the screen below. State the slot size you chose and why (cable plug dimensions: take a typical right-angle USB-A plug ≈ 17 × 8 mm and say it is an assumption).
2. The micro-HDMI port is on the Pi's side: add a side/rear exit path so a right-angle micro-HDMI cable leaves hidden behind the plates (opt-in key; propose a notch in the tray wall or a cable window in the floor; report which and why).
3. Do not move the Pi, the Hue, the keystone or the existing openings. Report per-feature distances to rack slots and joints.
Acceptance: as in Part A, plus renders of the changed item (closed meshes) and a screenshot of the Place on tray preview on disposable data.

## Part C — U5–U3 3U screen plate (BLOCKED until Brian measures the Hosyond 7" 1024 × 600 HDMI touch screen)
No code yet. Measurements needed from Brian: outside size, visible-area size and its offset from the edges, ear hole positions and diameters, thickness, which micro-USB port is touch, connector positions. Intended design: 3U plate (3 × 44.4 mm = 133.2 mm) with a window for the visible area and ears with holes, back left open for airflow, cables to the Pi in U6 above. Write the spec when the numbers arrive.

## Part D — Cooling (BLOCKED until Brian sends a photo of the OptiPlex 7010's back and right-side vents)
No code yet. The OptiPlex sleeve, orientation, mounting and rear bracket are SETTLED (memory `optiplex-sleeve-settled`); do not change them. Planned, to be specced after the photo:
- an opt-in opening in the right side of the OptiPlex tray behind the PC (Y ≈ 195–228 mm) lined up with the PC's exhaust;
- a right side panel with an 80 mm 5 V PWM exhaust fan at U1–U2 rear (fan spacing 71.5 mm for NF-A8);
- optional second exhaust at U8–U9 and optional filtered bottom intake at the FRONT, never under the rear floor opening;
- vented side panels (right), mostly solid left; wall-mounted rack with small rear clearance;
- fan speed from Pi GPIO PWM plus DS18B20 sensors in Home Assistant.
First research step for Codex when unblocked: report how Lab Rax side panels attach (rack-reference meshes) before designing anything.

## Do not
Touch data/normal-use, old revisions, the OptiPlex sleeve, keystone defaults, golden keystone geometry, or Print in color; print; push; regenerate historical evidence; mark anything fit-verified. Parts C and D stay specs only.

Report: `work/codex-tasks/40-nine-u-faceplates-REPORT.md` (files changed, test results, before/after hashes of untouched items, alignment table, every UNKNOWN).

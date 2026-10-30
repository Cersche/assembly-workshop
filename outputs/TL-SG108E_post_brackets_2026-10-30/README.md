# SG8-PB-A — post brackets for the printed TL-SG108E SG8-M6-D tray (2026-10-30)

Test-print ID **SG8-PB-A** is engraved on the rear face of each post pad. **Not printed. Fit and strength UNKNOWN.**

Hangs the already printed **SG8-M6-D tray** from the back of the front rack posts, so the tray no longer hangs on the faceplate bosses (those bosses sat on the tray's sleeve lip and pushed it ~2 mm low). Use with the printed **SG8-M6-B faceplate after cutting its two round screw bosses off flush** (each boss: Ø12, 8 mm deep, on the plate back above the switch window); each bracket's screw block takes a boss's place.

| File | What |
|---|---|
| `SG8-PB-A_post_brackets.3mf` | Left + right bracket, separate objects, assembly orientation (print standing; supports under the screw blocks) |
| `SG8-PB-A_left.stl`, `SG8-PB-A_right.stl` | Separate parts (closed, 0 open edges) |
| `src/SG8-PB-A.scad` | Source (`-D part="left"` / `"right"`); `src/pack_3mf.py` packs the 3MF |

**Where it mounts:** each U of the Lab Rax post has three Ø7.6 holes in its front flange (Z −15.9 / 0 / +15.9 about the U centre, X ±118.26); the faceplate uses the outer two. The bracket pad bolts to the **middle hole from behind** (pad on the flange's rear face, Y 6.2–12), with an M6 x 8 button head in an 11.5 counterbore (2.5 mm under the head, ~5.5 mm into the post hole). Measured from the creator's 1U post mesh (local only, not redistributed).

**Tray joint:** each bracket has a block in front of the tray upright (Y 0.3–8.0, Z 35.15–44.2, 0.3 above the sleeve lip). The existing M6 x 8 goes in from behind through the upright as before and threads **straight into a 5.0 mm pilot** in the block (~5.2 mm engagement). There is no room for an M6 insert there: anything wider than ~6.5 mm hits the sleeve lip. The right bracket is a frame around the plate's keystone block (low beam Z 0.6–6.6, column X 72.4–77.6, top beam Z 41–44.2).

**BOM:** 2 × M6 x 8 button head (post pads) + the tray's 2 existing M6 x 8. **Needs an M6 insert in each post's middle hole** (UNKNOWN whether yours have one).

**Checks (OpenSCAD intersections, digital only):** no overlap with the D tray, the B faceplate with its bosses removed, or either placed 1U post (after trimming the pad to |X| 125 and leaving 0.2 mm to the flange). Keystone jack body and cables behind the plate were not modelled.

UNKNOWN: insert in the middle post hole, M6 thread strength in the plastic pilot, bracket stiffness, physical fit.

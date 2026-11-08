---
name: new-part
description: Design, draft and release a new or revised 3D printed part for the rack (bracket, tray, faceplate, test coupon). Use for any work on a part design, including drafts that aren't ready to print.
---

# New part

Prints are slow and real, so a dropped feature or a tightened clearance costs Brian a print. Show and ask as if the part were in hand.

## Before modelling
1. If an earlier version exists, read its README and `docs/Fit_Findings.md`. List every feature Brian asked for and keep them all. If one can't stay, ask in chat first.
2. Keep every clearance from the version that printed well. Never tighten one without Brian's OK. A fit report about one feature applies to that feature only.
3. Measure first. Each device gets one card, `docs/devices/<device>.md`, holding overall size, corners, end and edge shapes, slopes, feet, screw heads, ports and anything else the part touches. Mark each value measured by Brian, from a source file or UNKNOWN. Before a new device's first print, send one interactive 3D measurement page (`tools/mesh_viewer.py --measure`, see PROJECT.md) showing where and how to measure, with the expected values, and ask for everything the fit depends on in one go. If Brian prints with a value still UNKNOWN, name it in chat first. Source models and STEP files are not measurements.
4. Look at the actual post mesh, and consider the rear posts as mounting points. Default pattern: post rails (`outputs/Chunky_Revisions/README.md`). Brian's rack has 4U posts with no side holes mid-post.

## Draft
Explore freely until Brian says he's printing it. A draft is one working SCAD file and a viewer page: no new ID, 3MF, outputs folder, README, handoff entry or per-change commit. Put several small changes into one viewer update instead of one each. Render with the pinned snapshot (`--backend=manifold`), then send and publish the page with `tools/mesh_viewer.py`. Commit working files once at the end of the session so nothing stays on one machine.

## Modelling
- `include <workshop.scad>` for the plate, slots, golden keystone, insert bores and hidden M6 joint. Don't redraw these. Use `include <BOSL2/std.scad>` for fillets and rounded shapes. See `lib/README.md`.
- Name parts with a SCAD variable: `part="tray";` and `if(part=="tray")...`.
- Every screw joint in a print gets a heat-set insert, with bores modeled in: M3 by default, M6 for weight-bearing joints and brackets, M2/M2.5 only where a device forces it. No self-tapping and no drilling. Ask before adding a new screw type.
- Leave real room around screw heads, tool paths and other non-fit features; don't design them down to the last fraction of a mm (Brian, 2026-11-05). Minimum 1 mm around a screw head, unprinted as a rule. Keep a head's recess completely open: the proven 11.5 M6 recess stays that size, and nothing may intrude into it. Add a `part=="keepout"` with `ws_m6_head_keepout()` or `ws_head_keepout()` for every screw head and pass `--keepout keepout` to the release script. Tell Brian about any tight spot. This doesn't loosen proven fit clearances, which stay as printed.
- Use a new unique ID for each revision, and model it on the part where it doesn't affect a tested feature. Test prints and coupons always need one.
- Never edit an already printed revision. Make a new one.

## Release
Only when Brian says he's printing it, or asks for a print file. If he does, the current draft becomes the next revision.
1. Run this, adding `--against device.stl` whenever a device mesh exists, `--posts <U>:<right|left|both>` for anything near the rack posts (places the real posts by U; never place them by hand), and `--cuts cuts=<N>` when the part has several windows, vents or slots (a check-only `part=="cuts"` holding each opening as a solid; merged openings fail):
   `python tools/release_part.py <part>.scad --id <ID> --part <name>[:<ID on part>] -o outputs/<Name>_<ID>_<YYYY-MM-DD>`
2. Fix every FAIL. Read every WARN and tell Brian about any you keep. Don't work around a failed check.
3. Confirm bores in the viewer: the hole scan can miss bores open on one side. The script checks the ID is on the mesh, but not that it is legible.
4. Send the viewer page with SendUserFile (display "render") and publish the same file as an Artifact. Send the 3MF too.
5. Write the folder's README: what changed, which fit values were kept or changed and why, and what's UNKNOWN.
6. End the delivery message with the fit report to send back: ID on the part; fits or not; where tight or loose, and by how much if measured; walls and infill. Add any part-specific items, such as a screw or lights.

## After
- If the part has a section in `work/workbench/Workflow_Log.md`, add a short row whenever a step starts or ends or something gets in the way.
- Add Brian's printed results to `docs/Fit_Findings.md`, and new device measurements to the device's card. If a report leaves out the ID, ask once before logging it. Printing needs his direction, and fit and strength stay UNKNOWN until a print shows otherwise, for that specimen only.
- Update `HANDOFF.md`, commit only this part's files, push, then send the Gene photo.

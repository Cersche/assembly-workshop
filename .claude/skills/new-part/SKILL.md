---
name: new-part
description: Design and release a new or revised 3D printed part for the rack (bracket, tray, faceplate, test coupon). Use for any work that creates a new part revision.
---

# New part

Prints are slow and real, so a dropped feature or a tightened clearance costs Brian a print. Show and ask as if the part were in hand.

## Before modelling
1. If an earlier version exists, read its README and `docs/Fit_Findings.md`. List every feature Brian asked for and keep them all. If one can't stay, ask in chat first.
2. Keep every clearance from the version that printed well. Never tighten one without Brian's OK. A fit report about one feature applies to that feature only.
3. Measure the real device. Any measurement request comes with a diagram showing where and how to measure, and the expected value. Keep unmeasured dimensions marked UNKNOWN.
4. Look at the actual post mesh, and consider the rear posts as mounting points. Default pattern: post rails (`outputs/Chunky_Revisions/README.md`). Brian's rack has 4U posts with no side holes mid-post.

## Modelling
- `include <workshop.scad>` for the plate, slots, golden keystone, insert bores and hidden M6 joint. Don't redraw these. Use `include <BOSL2/std.scad>` for fillets and rounded shapes. See `lib/README.md`.
- Name parts with a SCAD variable: `part="tray";` and `if(part=="tray")...`.
- Every screw joint in a print gets a heat-set insert, with bores modeled in: M3 by default, M6 for weight-bearing joints and brackets, M2/M2.5 only where a device forces it. No self-tapping and no drilling. Ask before adding a new screw type.
- Leave real room around screw heads, tool paths and other non-fit features; don't design them down to the last fraction of a mm (Brian, 2026-11-05). Minimum 1 mm around a screw head, unprinted as a rule. Keep a head's recess completely open: the proven 11.5 M6 recess stays that size, and nothing may intrude into it. Add a `part=="keepout"` with `ws_m6_head_keepout()` or `ws_head_keepout()` for every screw head and pass `--keepout keepout` to the release script. Tell Brian about any tight spot. This doesn't loosen proven fit clearances, which stay as printed.
- Use a new unique ID for each revision, and model it on the part where it doesn't affect a tested feature. Test prints and coupons always need one.
- Never edit an already printed revision. Make a new one.

## Release
1. Run this, adding `--against device.stl` whenever a device mesh exists:
   `python tools/release_part.py <part>.scad --id <ID> --part <name>[:<ID on part>] -o outputs/<Name>_<ID>_<YYYY-MM-DD>`
2. Fix every FAIL. Read every WARN and tell Brian about any you keep. Don't work around a failed check.
3. Confirm IDs and bores in the viewer: the script only finds the ID in the source, and its hole scan can miss bores open on one side.
4. Send the viewer page with SendUserFile (display "render") and publish the same file as an Artifact. Send the 3MF too.
5. Write the folder's README: what changed, which fit values were kept or changed and why, and what's UNKNOWN.

## After
- Add Brian's printed results to `docs/Fit_Findings.md`. Printing needs his direction, and fit and strength stay UNKNOWN until a print shows otherwise, for that specimen only.
- Update `HANDOFF.md`, commit only this part's files, push, then send the Gene photo.

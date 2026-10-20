# Cable management Step 1 (views + guides): implementation notes

2026-10-19. Prepared from reading only; no app code changed yet. Proposal and Brian's decisions: [Proposal.html](Proposal.html).

## Brian's decisions (2026-10-19)
- Cable guide mesh: local preview only, like the creator parts. Never redistributed, and not part of PRINT THE RACK / `/api/rack-stl`.
- Ports (Step 2): Pi 4 preset plus a wizard Ports step, then fine-tuning by clicking on the device mesh.
- Start with Step 1: views and guides.

## Source asset (untrusted download, read only)
- `C:\Users\brian\Downloads\Frame+Cable+Holder.3mf`: "Lab Rax Cable Guide" by mklements, Bambu Studio 2.7, **MakerWorld Exclusive License**. One object, `3D/Objects/object_1.model`, 352 vertices / 708 triangles, identity component transform.
- Local mesh bounds: x ±14, y ±14, z ±22 mm. Mounting plate is y = -14 … -11.6 (2.4 mm), 28 wide (x) × 44 tall (z). Two Ø6.4 holes at x = 0, z = ±15.9 (31.8 mm apart). Cable loops project toward +y.
- Creator text: 1U, 2 × M6 × 10 mm screws into the existing post holes, intended mainly for the rear posts. Fit, capacity, retention and strength are UNKNOWN.

## Placement math (visual pose, fit UNKNOWN)
- Scene axes (rack-scene.js): X is width, Y is depth (front face of the front posts at y = 0, rear face of the rear posts at y = 240), Z is up. Posts are 30 × 35 at x = ±125.98. Faceplate hole column is at |x| = 118.26 (faceplate_mounting.json).
- Slot n middle z = (slots − n) × 44.45 + 22.225. The guide holes (±15.9) line up with the outer faceplate hole pair around the U middle.
- Rear posts (RL, RR): R = I, t = [±118.26, 254, z_mid], so the plate sits on y = 240 and the loops point backwards.
- Front posts (FL, FR): R = RZ (180° about Z), t = [±118.26, −14, z_mid]. Use rotations only, never mirroring (mirroring flips the normals).
- Where a 1U support extension takes that U on that side (post_levels), whether holes exist there is UNKNOWN. Allow the guide and show a note.

## Planned changes
1. Convert the guide to `rack-references/cable_guide.json` (`{vertices, triangles}`, like component_*.json) with a one-off script in work/cable-management/. Add its SHA-256 to `asset-manifest.json`. Record the license and provenance in a sidecar. Keep it out of `RACK_PART_SOURCES` and rack_stl.
2. `rack_workspace.validate`: optional `cabling.guides[]` = `{id ≤80 unique, kind:'labrax-cable-guide', post:'FL'|'FR'|'RL'|'RR', slot:int 1..slots}`. Allow at most one guide per post/slot, and drop guides past the slot count with an error. Unknown keys are currently stripped silently, so this must be added or Save loses guides. Add tests in test_rack_workspace.py.
3. Renderer: push guide objects (`kind:'guide'`, `guide:id`) from `rack.cabling.guides` in `objects()`. `pick()` should return `{guide:id}` before slot. Add a "Cables" view mode that hides side, top and bottom panels and ghosts the frame (alpha blend pass, or a dimmed color plus depth-write off for frame parts).
4. workspace.js: a Rear view button (yaw = π, orthographic), Rear post labels on automatically in Rear view, the Cables mode toggle, and a Guides section in the Setup tab (add at post + slot; select, move up/down, change post, remove; ellipsis/right-click). Changes go through `markChanged()` → explicit Save only.
5. Tests: Node scene test for the guide pose (plate on post face, inside the post's x span ±15 of the hole column), Python schema tests, run_checks.ps1, disposable-8767 browser check. Never test on data/normal-use.

## Progress (2026-10-19)
- Done: `rack-references/cable_guide.json` created (exact copy of 352 vertices / 708 triangles; provenance in [Guide_Provenance.json](Guide_Provenance.json)). It is **not yet in asset-manifest.json**, so the app cannot serve it until that entry is added.
- Done: `rack_workspace._cabling` validates `cabling.guides`. New test `test_cable_guides_round_trip_and_reject_invalid` passes, and test_rack_workspace passes 9/9. The studio Save (`assembly_records.save_workspace`) uses the same validator.
- UI must remove guides above a reduced slot count before Save, or Save fails with "inside the rack slots".
- Waiting: renderer, workspace UI and manifest work start once the faceplate-images session finishes.

## Coordination
On 2026-10-19 at 08:24, "Show faceplate images on wizard-made equipment" (local_d2c9cec0) was running in this folder and had just edited rack-studio.js and asset-manifest.json. Do not edit those files, workspace.js or the asset manifest while it runs. Re-read them fresh before starting.

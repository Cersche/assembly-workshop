# Assembly Workshop — handoff notes

Read this first if you are a fresh assistant session. Owner is not an engineer; explain plainly, keep turns efficient.

## Setup
- App: `outputs\Mechanical_Design_App\app.py`, already running at http://127.0.0.1:8765/ — do not start another server.
- Do NOT edit `outputs\Mechanical_Design_App\rack-references\` (hash-locked; edits cause HTTP 409).
- Node is not installed; verify JS by loading the page in a browser (add `?v=N` to bust cache).
- Work directly on the current git branch (owner doesn't want branch management).

## Done (2026-10-18) — all in `workspace.js`, verified in browser
- Rack settings dialog (`#rackDialog`) now has a live 3D frame preview (`#rackPreviewCanvas`), drawn by `drawRackPreview()` with its own `previewRenderer` (disposed on dialog close). Passes `{slots, placements: []}` to avoid the placements TypeError. `drawRack()` untouched.
- Post chips are draggable; dropping onto the preview adds that many U. All slot changes go through `setSlots(n)` (clamps 1–14).
- Bill of materials (`#rackBom`, `renderBom()`): splits height into 5U segments + remainder, assumes 4 posts, 3 holes per U per post; bolts = inserts = slots × 3 × 4.

## Lab Rax logo missing (found 2026-10-18)
- Not caused by the dialog work. No JS anywhere in the project loads `rack-references/rack-logo-faces.json` (logo data, dated 16:41). The live `rack-studio.js` (15:34, hash matches the manifest) has no logo code, so the logo-painting version was overwritten/reverted at some point.
- FIXED with owner's OK: `rack-studio.js` now has `logoMeshes()`. The Renderer fetches rack-logo-faces.json itself and splits `beam_top_front` into `-body` + `-logo` (lime `#a6e22e`, or `appearance.logo_color`). Manifest hash updated to 905eb376…a1ee. Verified in browser.

## U-labels (2026-10-18)
- Front left (X=-133) and right (X=+133) always shown. Rear posts only when the "Rear U labels" toolbar button (`showRearLabels`) is on; rear Y is estimated from scene bounds, text runs along -X.
- In `drawRack()` (workspace.js), U01… are drawn "printed" on the left post face: 2D canvas text transformed by the projected post axes, centred at X=-133, Y=-3.2, Z=z+38.1 (top post hole of each U, EIA spacing; 36.902 was the faceplate slot and looked low on U02+), 5 mm bold, dark ink, alphabetic baseline offset +1.75 to centre caps on the hole. Hidden when the post face points away (screen-space cross-product test). They're small at default zoom; scroll to zoom in. Tweak `at` / font there.

## Support extension (2026-10-18)
- `LabRaxScene.load` skips the `extension` mesh and `frame()` never places it. workspace.js now fetches `component_2_1.json` after load and `rackFrame()` adds one per side (X=±125.98, Y=120, R=I / RY) at every post-segment joint Z. Both drawRack and the dialog preview use `rackFrame()`. Extension mesh bounds: 30 × 240 × 84 mm. Owner confirmed it sits in the post pockets.
- Movable: `rack.post_levels = {left:[...], right:[...]}` (bottom-up U sizes, each 1–5, sum = slots). `rackFrame(slots,panels,rack)` rebuilds posts/side panels per side from it; `moveExtension(side,j,±1)` shifts a joint; Inspector (no slot selected) shows ▲/▼ per side via `appendExtensionControls`. Kept when the rack height is unchanged in the settings dialog.
- `rack_workspace.py` now validates and keeps `post_levels`. Server restarted 2026-10-18 (now PID 44824, started hidden via Start-Process); save round-trip tested in a temp folder.
- While restarting, found and fixed a pre-existing indentation error in `assembly_records.py` (line 33, `piece_colors`) that would have stopped the server from starting at all.

## Extension takes 1U of height (2026-10-18, supersedes the joint model above)
- Stack rule: sum(posts) + (posts−1) × 1U extension = slots. e.g. 9U = 3U post (bottom) + 1U ext + 5U post. `defaultLevels()` uses the fewest posts, fills from the top down to 5U, so the short post ends up at the bottom. Extension drawn centred in its own U (z+U/2); posts above shift up 1U. Python validation matches this. Dialog BOM lists extensions (2 per joint). Server restarted (PID 32964).

## Appearance redesign — built 2026-10-18 (workspace.js)
- `renderRackPaint()`: theme chips (`rackThemes`), Whole rack color, a PARTS list of `paintGroups` that are in the build (swatch + "custom"/"rack color"), and one color editor for the selected group with "Use whole-rack color" / "Use default lime". Group colors write every key in the group to `appearance.components`; logo → `appearance.logo_color`. Styles are injected as a `<style>` (`.paint-*`).
- Click-to-paint: on the Appearance tab with the layout locked, clicking the 3D view calls `pickRackPart()` (a ray-pick copied from LabRaxStudio.pick, using `sceneRenderer.pickState`). A near-tie on the beam goes to the logo. Clicking between the letters selects Beams.
- 3D highlight: drawRack sets `part.selected` on the scene parts in the current `paintGroup` (only on the Appearance tab with the layout locked). The renderer spreads the part's fields into its objects, so it gets the blue uSelected tint. Picking the logo highlights the whole top front beam. showInspector now redraws.
- Still to do: "recent colors".

## Rack colors gated + filtered (2026-10-18)
- `rack.layout_locked` (bool, saved; validated in rack_workspace.py). Setup tab (no slot selected) has "Lock in post layout" / "Unlock". While unlocked, Appearance → Rack colors shows only a notice; extension ▲/▼ disabled while locked. Changing rack height in the dialog drops the lock.
- Component override list is built from `rackFrame(rack.slots,true,rack).parts` so it only lists parts in the build (incl. "Support extensions"; 'extension' added to RACK_COMPONENTS in assembly_records.py). Server restarted (PID 23296).

## Rack toolbar cleanup (2026-10-18)
- Toolbar reads: "5U rack · 208 × 240 mm" | VIEW [3D][Front] (segmented, `setViewButtons`; orbiting from Front switches back to 3D) | SHOW [Side panels][Back labels] (dot toggles) | [Shadows] (= studioQuality). Same element IDs as before, so the existing handlers still work. Styles `.tb-*` are in the injected `<style>` in workspace.js.
- rack-reference.js: its button is now "Parts catalog" in the viewport heading. It used to insertBefore resetRackView, which broke once that button moved into a group. Heading badge now reads "Rack preview" / "Pi 4 assembly".

## Original CAD sources
- `work/rack-geometry-recovery/sources/`: `Lab+Rax+1-5U+Posts+&+Panels.3mf`, `5U+Lab+Rax+X2D.3mf`, `1U+Support+Extension.3mf`
- Pi4 tray/faceplate: `outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/` (.scad, .stl)

## Next feature area: more equipment + STL generation (investigated 2026-10-18, nothing built yet)
- Equipment today is hard-wired to the Pi 4. `#pi4Card` is static HTML in workspace.js (line ~19). `startWizard()` (~303) needs an empty selected slot; `newAssembly()` (~126) always names it "Raspberry Pi 4" and deep-copies `legacyTemplate` (the legacy Pi4 project).
- Geometry: `pi4_baseline.scad` (60 lines, parametric: plate_w=252, plate_h=42, tray 112×82, tray_z=7, two M3 joint bosses at x=±40, `part` = tray/faceplate/assembly). `design_revision()` in app.py (~374) only swaps ONE value (`insert_pilot=4.2;`) and rejects any other input change. It also requires a screw+insert selection and `pi_validation.validate()` to not fail.
- STL export: POST `/api/build` → `mesh_revision.build()` runs OpenSCAD.exe twice (`-D part="tray"` / `"faceplate"`), checks the meshes are closed, and saves them under `revisions/<sha256>/` (immutable cache). `/api/build-bundle` returns a zip. `/api/design` returns only the .scad. Rack frame parts are never in the STL output (they're only preview meshes from rack-references).
- AGENTS.md says "Pi4 remains the only manufacturing geometry adapter", so a new equipment adapter is a scope change that needs the owner's explicit go-ahead. Proposed plan (awaiting owner's choice): (A) a generic "tray from dimensions" template (`generic_tray.scad`, device W×D×H, optional mounting holes, faceplate cut-outs) as a second adapter beside Pi4; (B) STL file import used for preview + auto-filling A's dimensions (STEP needs non-stdlib libs, so not planned); (C) rack-part STLs by converting the existing frame meshes, later.

## Owner direction — hardware import wizard (2026-10-18, supersedes "Pi4 only adapter")
- Build a wizard to import hardware (SCAD or similar model file) → auto-find mounting positions → owner confirms → ask for port connections → generate tray + faceplate → STL.
- Faceplate default template = the current Pi4 faceplate (pi4_baseline.scad faceplate) for all devices until the owner says otherwise.
- At any point in faceplate creation, offer "add keystone(s)".
- Offer several bonding/mounting options for hardware→tray and tray→faceplate.
- Owner answers: file types = STL, SCAD, STEP and dimensions-only (all of them). Device→tray options = heat-set inserts + screws, printed standoffs/pegs, snap-fit clips, strap/zip-tie slots. Tray→faceplate = current screw joint, snap-fit tabs, single printed piece (no glue). Keystone = standard 14.5 × 16 mm snap-in opening.
- Phased plan: P1 a generic parametric `equipment_tray.scad` (default faceplate taken from pi4_baseline, plus keystones and all the mount/joint options) and a dimensions-only wizard → STL through the existing mesh_revision pipeline. P2 STL import (find round holes on the bottom face for you to confirm). P3 SCAD import (render to STL via OpenSCAD, then same as P2). P4 STEP (needs an external converter, so ask first). Ports become rectangle/round cut-outs on the faceplate. The Pi 4 path stays untouched. 
- P1 BUILT 2026-10-18:
  - `equipment_tray.scad`: generic template. The faceplate is copied from pi4_baseline and has one pair of rack slots per U. It supports keystones (14.5×16), port cut-outs `[x,z,w,h,r]`, device mounts (inserts/pegs/clips/straps), joints (screw/snap/single → `part="combined"`), and `u` 1–5. The wizard appends override assignments at the end of the file; OpenSCAD's last assignment wins.
  - `equipment.py`: `clean()` validates the spec, `build()` renders with OpenSCAD, checks the meshes with mesh_revision.read_mesh, caches in `data/equipment-revisions/<sha>/` and returns a zip (STL + .scad + revision.json).
  - app.py: POST `/api/equipment-build`, and serves `/equipment-wizard.js`. index.html loads it last.
  - `equipment-wizard.js`: a "+ New equipment from dimensions" card under the Pi 4 card opens a 5-step dialog (Device, Mounting, Ports, Faceplate joint, Generate). It has a live 2D faceplate preview and an "Add keystone" bar on every step. It downloads the zip.
  - Verified: all 4 mount/joint combos render closed meshes; the browser POST returned a 200 zip. Server restarted (PID 36832, started from the app folder).
  - LIBRARY + SLOTS (2026-10-18): POST `/api/equipment-library` → `equipment.save_item()` builds the meshes and writes `data/equipment-library.json` items `{id:'eq-<12hex>', name, span=u, spec, build, parts}`. GET is the same path; GET `/api/equipment-mesh/<build>/<part>.stl`. The wizard's Generate step has "Save to equipment library". A "MY EQUIPMENT" list (`#ewLibrary`) under the new-equipment card: select an empty slot, click an item → `window.placeLibraryEquipment(item)` (in workspace.js) pushes a placement `{equipment:item.id, geometry:'equipment-library', span}` with a normal assembly record named after the item. An Edit chip reopens the wizard and re-saves with the same id. rack_workspace.py accepts `eq-xxxxxxxxxxxx` equipment. Tree/inspector labels use `assembly.name`.
  - 3D: equipment-wizard.js wraps `LabRaxStudio.Renderer.prototype.objects` (rack-studio.js stays untouched/hash-locked). For eq- placements it replaces the generic studio-* meshes with the parsed ASCII STL parts at z=(slots-(slot+span-1))×44.45.
  - Verified on a throwaway server (port 8799, temp data, since deleted): save to library → place in slot 3 → Save → reload keeps "Slot 3 · Switch" with the custom mesh drawn. The live server was restarted (PID 41356).
  - GAPS FIXED (2026-10-18):
    - Delete chip per library item. POST `/api/equipment-library-delete` refuses while a saved rack placement uses the id; meshes stay cached.
    - The list reloads when the Equipment section opens and on window focus.
    - `openAssembly()` in workspace.js hands eq- placements to `window.openCustomEquipment` (the wizard pre-filled, titled "Edit equipment"), so they never open the Pi4 hardware editor. The inspector button reads "Edit equipment" and isn't disabled before the first Save. Saving updates the item everywhere it's placed; changing u doesn't resize placed slots (noted in the dialog).
    - Verified on a throwaway server (deleted afterwards). Live server restarted (PID 41240).
  - P2 STL IMPORT BUILT (2026-10-18, all in equipment-wizard.js, browser-only, file never uploaded):
    - Device step has a file input. `parseStlBuffer` reads binary or ASCII STL. Orientation chips (Z/Y/X up) and "Turn 90°" go through `transformed()`. `applyImport()` sets W/D/H from the bounding box and auto-picks u.
    - `findHoles()`: on faces with |nz|>0.99, grouped by Z plane, it takes boundary edges, walks them into loops, and keeps round loops (r 0.6–4.5 mm, ±10%), deduplicated.
    - Mounting step lists the candidates as checkboxes on a top-view SVG (`#ewTop`, front at the bottom). "Use ticked holes" fills `spec.holes` and sets hole_d to the median.
    - Verified: a test board (85×56, 4 × Ø2.7 holes plus a chip) gave exactly 4 holes at the right coordinates and 85×56×16.6 mm. Units are assumed mm. Holes that are only drawn as features in a solid box, or non-circular slots, won't be found.
  - PORT SUGGESTIONS (2026-10-18): `findPorts()` rasterises triangles within 6 mm of the model's front (min Y) onto a 0.5 mm X–Z grid. It clears near-full-width rows (the PCB) and turns each connected blob into a box, skipping blobs under 2.5 mm or covering the whole front.
    - `portOnPlate()` converts to faceplate coordinates: x = cx − dev_w/2; z = 10 (tray floor top) + standoff (0 for straps) + cz; +1 mm clearance per side; r = 1.
    - The Ports step shows checkboxes plus dashed outlines on the faceplate preview, and "Use ticked ports" adds them.
    - Verified: a test board with 13×14 and 15×6 front connectors gave 2 ports within the 0.5 mm grid. Limits: recessed ports in a solid box front aren't detectable (the whole front reads as one blob → skipped); touching connectors merge into one opening.
  - P3 SCAD IMPORT (2026-10-18): the wizard file input accepts .scad. POST `/api/scad-to-stl` {source} → `equipment.scad_to_stl()` renders in a temp folder with `--export-format asciistl` (2 MB limit, 180 s timeout, nothing stored), then the same STL hole/port finder runs. include/use of other files isn't supported (only the text is uploaded), and the error says so. Verified on a throwaway server: test board → 85×58×15.6, 4 holes, 1 port; a broken file shows a readable error. Live server restarted (PID 39428).
  - WIZARD 3D PREVIEW (2026-10-18): Generate step → "Show 3D preview". POST `/api/equipment-preview` → `equipment.preview()` (uses the shared `render()`, cached by source hash) returns {id, parts}. The wizard fetches the STLs and draws them in `#ewView` with a small canvas painter (`show3D`/`draw3D`: drag to orbit, wheel to zoom). The device ghost is the imported model (or a box) placed at x=−W/2, y=12, z=10+standoff. Nothing is saved. Verified on a throwaway server. Live server restarted (PID 38972).
  - P4 STEP (2026-10-18, not built): STEP needs a CAD kernel; Python stdlib can't read it. Options given to the owner: (1, recommended) install FreeCAD (free), and the app calls `FreeCADCmd.exe` to convert STEP→STL, the same way it calls OpenSCAD; (2) pip install cadquery/OCP, which breaks the stdlib-only rule; (3) online converters, ruled out (uploads); (4) for now, use the manufacturer's STL. BUILT: FreeCAD 1.1 was already installed (`C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe`; `equipment.freecad()` finds the newest `C:\Program Files\FreeCAD*`).
    - POST `/api/step-to-stl` {source: STEP text} → `equipment.step_to_stl()` runs a small FreeCAD script (Part.read → MeshPart.meshFromShape, 0.1 mm deflection), with paths passed via env vars, a 300 s timeout and a 60 MB limit. It returns a binary STL; nothing is stored.
    - The wizard accepts .step/.stp, and the same hole/port finder runs. Verified: a FreeCAD-made test board STEP → 4 holes, 1 port.
    - Found and killed a stale duplicate app.py (old PID 39428) that had survived a restart. Live server now PID 36992. After a restart, list `python.exe` processes running app.py to make sure there's only one.
  - Note: Stop-Process + restart once left the old PID listening; check the StartTime after a restart. The placement's assembly record still carries copied Pi4 pins internally (unused for eq- items).
  - Earlier note, now outdated: wizard items weren't saved as library equipment and can't be placed in rack slots yet; there's no 3D preview of the generated parts. Snap tabs, clips and keystone retention on the 3 mm plate are untested geometry (UNKNOWN).

## Printed Pi4 specimen vs the wizard (checked 2026-10-18)
- The printed specimen ("Fitment is fantastic") = Clearance v2 tray + faceplate with a 4 mm insert pilot (outputs/Phase7_Physical_Observations/2026-10-18/Recovered_Test_File_Provenance.json).
- `pi4_baseline.scad` is hash-identical to `outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/pi4_assembly.scad`, so the source wasn't damaged. The wizard's `equipment_tray.scad` copies that faceplate (outline, 3 mm thickness, rack slot capsules) and its screw joint (tongues, bosses, ears), so 1U + screw-joint wizard parts share the printed geometry.
- CHANGED per owner (2026-10-18): the wizard faceplate default is now **4 mm thick** (`plate_t=4`) with **8 mm rounded corners** (`plate_r=8`), and `joint_pilot` is 4.0 (matching the print). The 1U Pi4 printed part was 3 mm with square corners, so the plate itself now differs from the printed specimen; the slots and joint positions are unchanged.
  - The plate is built from 2D layers (`plate2d`/`plate_layer`). With keystones, the front 2 mm (`ks_front`) carries the 14.5×16 opening and the rear 2 mm is pocketed 18.5×22, so jacks latch on a 2 mm wall (retention UNKNOWN).
  - clean() rejects keystones within 16 mm of the screw-joint bosses.
  - OpenSCAD 2021 sometimes emits zero-area slivers with pockets. render() retries with `nudge` = 0.011/0.023/0.037/0.051 mm on the corner radius and pocket size, stores the nudged .scad per part, and records `nudge_mm` in revision.json.
  - Library items saved earlier keep their old 3 mm builds until re-saved via Edit → Save.
  - Live server restarted (PID 44776). It wasn't running when I went to restart it. Snap tabs, single piece, pegs, clips, straps, keystones and multi-U slot spacing are new and unprinted (UNKNOWN).

## 4 HOLES PER U — owner rule (2026-10-18, "nuke from orbit")
- Every faceplate U gets 4 rack holes: x=±118.2625, z = U centre ±15.902 (5.098/36.902 on 1U), from faceplate_mounting.json (the user-supplied 1U blank plate). `equipment_tray.scad` `plate2d()` now does this; the old single centred pair (+1.9722) is gone from the wizard template.
- The Pi4 legacy export already applied this via faceplate_mounting.apply_default. The four-corner matter is now explicitly raised by Brian and settled as the default.
- Consequence: those holes sit 1.6 mm from the plate's top/bottom edge, so the corner radius is limited to 2.5 mm (8 mm would cut into the holes). Told the owner.
- The wizard SVG preview draws 4 holes per U.

## Rear-post support (2026-10-18)
- `rear_support` (wizard step 4 checkbox): the tray becomes 240 mm (rack_depth) long, its front joint features are mirrored to the rear (`to_rear()`), and a new part `rear_bracket` is added (a plain plate with the same 4-hole slots, mirrored to sit on the back posts at y 240–244). Not allowed with the single-piece joint; device depth ≤ 200. Assumption: rear posts' back face at y=240 (frame depth), fit UNKNOWN.

## Test coupons replace the kit (2026-10-18)
- Brian: too much material; only the keystone and snaps. `outputs/Physical_Test_Coupons_2026-10-18/`: a keystone + corner-holes faceplate end (48×4×42) and a snap arm strip + tray corner. Made with the new `coupon=[x0,x1,ymax]` template parameter (intersection slice; empty parts are skipped). README has the checks.
- The old 7-piece kit (with 2-hole 1U plates) was moved to `outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/`, not deleted.

## Physical test kit (2026-10-18) — SUPERSEDED, see above
- `outputs/Physical_Test_Kit_2026-10-18/`: 7 STLs (A: inserts + screw joint + 2 keystones, tray + plate; B: pegs + snap joint; C: clips + single piece; D: straps tray only; E: 2U plate only), each with its `__source.scad`, plus manifest.json (sha256, nudge) and README.md (print list, hardware, 9-point checklist). All use Pi4 dimensions/holes. Made with throwaway data via scratchpad make_kit.py; the library is untouched.
- Next: when Brian reports results, record them per piece (specimen-specific) and tune the template.

## Rack frame STL export (2026-10-18, owner request; supersedes "no rack-frame STL adapter")
- Inspector, with the rack selected and no slot: "PRINT THE RACK" → "Include side panels" checkbox + "Download rack frame STLs" (`appendRackStlExport`/`downloadRackStl` in workspace.js). It counts parts from `rackFrame(...)` with `RACK_PART_SOURCES` (a copy of rack-scene.js `sources`). Extension count = joints on the left + right.
- POST `/api/rack-stl` → new `rack_stl.py`: reads `rack-references/component_<ref>_<id>.json` (read-only; nothing locked was edited) and writes binary STLs named "<count>x <part>.stl" plus parts-list.txt with a personal-use notice (designer mklements, BY-NC-SA metadata). All frame rotations are proper rotations, so no mirrored copies are needed.
- Verified on the live server (read-only): the default 5U rack gave 10 part files with sensible counts (4× 5U post, 2 handles, 4 feet…). One test zip was downloaded through the browser pane.
- Not done: part orientation for printing is left to the slicer; no print-settings guidance (fit/strength UNKNOWN).

## Open questions / ideas
- Is 4 posts correct? (`POSTS` constant in workspace.js)
- BOM segment split is automatic (largest-first), not the exact chips clicked.

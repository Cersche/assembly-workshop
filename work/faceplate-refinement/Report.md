# Faceplate painting & artwork refinement — 2026-10-19

Brian asked to accept more image formats, especially vectors, reconcile the artwork scope conflict, and fix the reviewed bugs. Originals before editing are in `originals/` (workspace.js, faceplate_color.py, test_faceplate_color.py, assembly_records.py, test_assembly_records.py, app.py, run_checks.ps1, js-tests/run.js, check_python.py, AGENTS.md, PROJECT.md, HANDOFF.md). js-tests/run.js was backed up but not changed.

## Changes
- **Formats** (workspace.js `artworkSource`/`loadArtwork`): PNG, JPEG, WebP, GIF (first frame), BMP, AVIF and **SVG**. SVG is parsed locally, sized from width/height or viewBox, and drawn through `<img>`, so scripts and external resources never run or load. Vectors are rendered at the target size, not upscaled. Everything is still stored as one local PNG.
- **Sharper previews:** stored PNG is up to 1024 px / 1.4 MB (was 512 px / 512 KB), with step-down 1024→768→512→256 until it fits (assembly_records.py `ARTWORK_MAX_*`). Older 512 px images stay valid. Decoded images are cached by sha256 in faceplate_color.py.
- **Print in color settings:** `setFil` reads live settings, so a Style change is no longer reverted by a later color pick (reproduced before the fix: Bug_Style_Reverts.jpg). Untouched colors are stored as `null` (automatic) instead of being frozen. Each row has "auto". Out-of-order preview responses are ignored. Moving or resizing the image, or changing the faceplate color, refreshes an open preview.
- **Export cache:** the identity now includes base and body colors (`faceplate-color-v2`, `export_identity`). Before, a color-only change returned a cached zip whose README and revision.json named the old colors. Old v1 cache folders are untouched.
- **Base color:** index 0 is always the faceplate (or an explicit base filament). An opaque image no longer turns its most common color into the whole faceplate. Giving a color the base filament merges it into the faceplate.
- **Wizard-made equipment:** the Appearance tab shows only tray/faceplate colors. There is no Pi reference color, image chooser, "View faceplate front" or Print in color, because the rack view draws no images on those faceplates (equipment-wizard.js:327 `art:null`). A saved image can still be removed. The export button verifies the open assembly; the server rejects a mismatched `assembly` and non-Pi4 placements.
- **Polish:** a "Choose/Replace image…" button replaces the native "No file chosen" input. The whole-rack color refreshes the selected part's field. "Reset all rack colors" needs a second click within 4 s. Removing or replacing an image clears its stale color preview.
- **Scope reconciled** (Brian, this chat): AGENTS.md has a new "Faceplate artwork and Print in color" section, with matching lines in PROJECT.md and HANDOFF.md. Pi4 Print in color is the only artwork-to-STL path. All other STLs never contain artwork.

## Verification
- `run_checks.ps1`: 46 Python (was 38: +1 assembly_records, +7 faceplate color now included; OpenSCAD export test excluded) + 11 JS, all pass.
- Manually ran `test_export_is_watertight_and_conserves_volume` once (synthetic image, temp folder): pass.
- Disposable server 8767 on the scratch data copy, never data/normal-use:
  - SVG → 1024×256 PNG.
  - Style stays raised after a color pick; auto colors persist as `null` after Save.
  - The slider refreshes the preview.
  - Wizard-equipment panel checked.
  - The server guard rejects a mismatched assembly (400, before any render).
  - Two-step reset checked.
- No export zip was produced in the browser. Screenshots: 1–4_*.jpg.
- The browser console's other 400s are the fixture's fake equipment meshes (`0000…`) in the disposable data, not from this change.

## Not done / limits
- The normal server (8765, PID 41408) still runs the old Python. The JS loads on refresh, but SVG/1024 px uploads and the new export need a restart via start.bat (Brian's call; save drafts first).
- PDF/EPS/AI are not accepted (no stdlib renderer); export them to SVG.
- Images on wizard-made faceplates are not implemented.
- Printed color results, fit and strength remain UNKNOWN.
- Narrow and phone widths were not visually checked.


# Faceplate image on wizard-made equipment — 2026-10-19 (side session)

Requested by the coordinating session: show the slot Appearance faceplate image on wizard-made equipment (`eq-…`) in the Lab Rax rack view, sized to the real faceplate front, including multi-U. Preview only. **No Print in color for wizard equipment** (AGENTS.md "Faceplate artwork and Print in color"). Originals before editing are in `originals-wizard/`: equipment-wizard.js, workspace.js, rack-references/rack-studio.js, rack-references/asset-manifest.json and js-tests/run.js.

## How the Pi4 projection works
The fragment shader in rack-studio.js paints the image on front-facing faces only (`vWorld.y < -2.99`, `|n.y| > .95`). It maps world X and `Z - uBaseZ` into `uArtRect = [cx, cz, w, h]`. `uBaseZ` is the object's translation Z, which is the bottom of its slot. `artworkRect` fixed the window at 216 × 34 mm, centred 21 mm above the base. That is the Pi4 1U plate (42 mm tall) less 18 mm at each side, clear of the rack holes, and 4 mm at the top and bottom.

## Changes
- **rack-studio.js:** `artworkRect(art, aspect, win)` takes an optional window `{w, h, z}`. The default is the Pi4 window, so Pi4 output is unchanged. The new `artworkWindow(plateW, plateH, bottom)` keeps the same margins: `w = plateW − 36`, `h = plateH − 8`, `z = bottom + plateH/2`. The renderer passes `o.artWindow`. Both functions are exported.
- **equipment-wizard.js:**
  - `patchRenderer` measures the wizard faceplate mesh's own front face: the bounding box of the lowest-Y vertices, i.e. the y = −4 face from equipment_tray.scad. This gives the real width, height and U span (252 × 42 for 1U, 252 × 86.45 for 2U). It is cached per mesh.
  - The faceplate part now gets `art: appearance.artwork` and `artWindow`. The tray and rear bracket get no image.
  - The base Z is unchanged (bottom of the lowest slot the placement spans).
- **Pre-existing bug fixed (needed for this):**
  - Every wizard part was pushed with key `studio-plate`/`studio-tray`. The renderer caches GPU buffers by key, so wizard plates drew the already-uploaded Pi4 plate.
  - Effect: a 2U wizard faceplate appeared as a 1U Pi4 plate (screenshot 8_Bug_Before_2U_Drawn_As_1U.jpg).
  - Each part is now keyed `studio-eq-<build>-<part>`. Nothing else matched on those keys.
- **asset-manifest.json:** the rack-studio.js sha256 was updated for this intentional edit. Only that line changed. Without it, the server answers 409 and the rack view shows "LabRaxStudio is not defined". The manifest is read on every request, so running servers pick up the change on refresh.
- **workspace.js renderAppearance:**
  - `eq-` slots now get the image chooser, Fit & center, Center, the horizontal/vertical/size sliders and Remove image.
  - Still Pi4-only: "View faceplate front", the Pi reference color and Print in color (`renderFilament` stays behind `isPi`).
  - The help text says the image is rack-view only and Print in color is Pi4-only.
- **js-tests/run.js:** new test `LabRaxStudio.artworkWindow generalizes the Pi4 window…`. It checks that:
  - a 252 × 42 plate gives exactly the Pi4 window and identical rects;
  - for 1/2/3/5U plates and every corner placement, size and aspect, the rect stays inside the plate width and inside the 4 mm top/bottom margins;
  - a 2U window allows a taller image than 1U.

## Verification
- `run_checks.ps1` after the final edits: 46 Python + 12 JS, all pass. RESULT: all checks passed.
- **Server:** the sibling session's disposable-8767 server was already running on the shared scratch data. To avoid writing into it, I used my own copy of that disposable data, never data/normal-use. It runs under a new launch.json entry, `disposable-wizard-art-8769`.
- **Test items:** I built two disposable wizard items through the app's own `/api/equipment-library` route (local OpenSCAD render): "Art test 1U switch" (u=1) and "Art test 2U amp" (u=2). The first 1U attempt failed once with a Windows `Access is denied` while renaming the render folder; the retry succeeded. The retry is untested as a fix, and this behaviour is not from this change.
- **Placement:** Pi4 in slots 1–2, 2U in slots 3–4, 1U in slot 5. Saved in the disposable copy.
- **Images:** loaded through the real hidden file input, using generated PNGs passed in by DataTransfer.
- **Observed results:**
  - The 1U image is centred on the 1U wizard plate.
  - The 2U image is centred across the full 2U plate.
  - Fit & center fills the 2U window height.
  - The horizontal slider moves it.
  - After Save and a page reload, both images are still shown in Front and 3D views.
  - The Pi4 image on slot 1 is unchanged.
  - The final page load had no failed resources.
- **Screenshots:** 5_Wizard_1U_2U_Image_Front.jpg, 6_Wizard_1U_2U_Image_3D.jpg, 7_Wizard_2U_Image_Controls.jpg, and 8_Bug_Before_2U_Drawn_As_1U.jpg (the bug before the key fix). The 2U test PNG's text ("AMP 2U") overflows its own canvas. That is the test image, not clipping in the renderer.

## Not done / limits
- No Print in color, relief or engraving for wizard equipment. Wizard STLs still never contain artwork.
- The selection outline in the shader is still the fixed 1U rectangle (`uSelected` block, 121.5 × 17.75 around 22.225 mm). On a selected 2U wizard plate it rings only the lower U. This is pre-existing and was left alone.
- Port and keystone openings are not masked: the image is painted on the plate's front faces only, so holes show through, but the window is not reduced around them.
- The narrow/phone layout was not checked. The normal 8765 server was not touched. It serves the new JS on refresh; no Python changed.
- Printed result, fit and strength remain UNKNOWN.

## Follow-up — selection outline, openings, widths (Brian, 2026-10-19)

Brian asked for three things: the blue selection outline should always match the U height being worked with; the image should no longer be cut by keystone and port openings; and the layout should be checked at other widths. Originals before this pass are in `originals-wizard-2/`: equipment-wizard.js, workspace.js, workspace.css, rack-studio.js, asset-manifest.json and run.js.

### Changes
- **Selection outline** (rack-studio.js shader):
  - The fixed 1U rectangle is replaced by the uniforms `uSelRect` (centre x, centre z above base, half width, half height) and `uSelRadius`.
  - Pi4 keeps exactly its old outline (`PI4_SELECTION = [0, 22.225, 125.5, 21.75, 4]`), which is the plate's own rounded outline.
  - Wizard faceplates use `selectionRect` from their measured front face, with r = 2.5 (`plate_r`). The outline therefore wraps 1U, 2U … 5U plates exactly.
  - Only the front faceplate is highlighted now; the rear bracket was previously flagged too.
- **Image clear of openings:**
  - equipment-wizard.js lists each keystone (14.5 × 16 mm at mid-height, as equipment_tray.scad cuts it) and each port (x, z, w, h from the spec) in plate coordinates.
  - `artworkRect` passes them to the new `clearWindow`. That function finds the clear rectangles inside the image window, keeping a 2 mm gap from every opening. It picks the one where an image of this aspect can be drawn largest, so a wide logo and a square badge may end up in different gaps.
  - Position and size sliders then work inside that area.
  - With no openings in the window, the window is unchanged.
  - The Pi4 path is untouched. The help text says the image uses the largest area clear of openings.
- **Widths:** at phone width, scrolled inspector content showed through an 11 px gap between the sticky "INSPECTOR" heading (29 px tall) and the sticky tab bar (top: 40 px). workspace.css now gives the tab bar a background-colored `box-shadow: 0 -12px 0`, which covers the gap without changing layout.
- **asset-manifest.json:** the rack-studio.js sha256 was updated again. The final hash was checked against the file.
- **js-tests/run.js:** two new tests.
  - Openings: in three plate layouts (keystone row with ports, 2U, and a full-width slot), for every placement and aspect, the image never comes within 2 mm of an opening and stays inside the margins. An empty openings list, or one outside the window, changes nothing.
  - `selectionRect`: the Pi4 constant, and centre and half-height for 1/2/3/5U.

### Verification
- `run_checks.ps1`: 47 Python (one is a new test from another session) + 14 JS, all pass.
- Checked on my disposable copy (`disposable-wizard-art-8769`), never data/normal-use.
  - I built a 1U test item with keystones at X −15/+10/+70, a USB port at −90 and a power port at −70, and pointed slot 5 at it by editing the disposable rack file.
  - Fit & center put the 4:1 test image in the 41.5 mm gap between the +10 and +70 keystones, which is what the numbers predict.
  - The 1U outline is tight on slot 5. The 2U outline wraps U03–U04 fully. The Pi4 outline on slot 1 is unchanged.
- Widths: at 1440, tablet 768 and phone 375 the page width equals the viewport (no horizontal scroll), and nothing in the Appearance panel overflows. The rack, the outline and the image look correct at each width.
- Screenshots:
  - 9_Image_Clear_Of_Keystones_1U_Outline.jpg (4× crop of the rendered canvas)
  - 10_2U_Selection_Outline.jpg
  - 11_Tablet_768.jpg
  - 12_Phone_375_2U_Selected.jpg
- One misclick opened the 2U item's Edit equipment dialog. It was closed without saving, and the item is unchanged.

### Limits
- Openings are rectangles. The rounded corners of ports and the keystone outline are treated as their bounding boxes plus 2 mm.
- If openings leave no clear area inside the window, the full window is used, and the openings show through the image.
- Printed result, fit and strength remain UNKNOWN.
### Physical testing — deferred (Brian, 2026-10-19)
Brian chose to save physical testing for later. **This work still needs physical testing.** Nothing here was printed or fitted. Before any physical approval, printed tests need to cover:
- the wizard faceplates and trays (1U and 2U+);
- plates with keystone and port openings;
- the Pi4 Print in color result.
Until Brian directs that test, fit, strength, retention and printed color stay UNKNOWN. The rack-view image placement and selection outline are visual previews only.
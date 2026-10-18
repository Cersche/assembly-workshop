# Rack-first GUI restoration — 2026-10-18

Brian authorized returning to the recovered GUI and rack-first workflow: configure the rack, select a slot, then create an assembly there. Browser acceptance was separately approved and used disposable data.

## Recovered context

The original ChatGPT chat **Create Claude App Prompt**, `6ad39502-fa44-83e8-a1ce-5a357df4d02e`, began October 17 at 08:32 Pacific. Older pages became available after the initial bounded/partial reads. User-authored choices are saved in Recovered_GUI_Decisions.json with their turn IDs. Assistant replies still use content-reference placeholders, so their detailed claims are not recovered evidence.

The intended product is a rack-context design tool for equipment brackets, faceplates and trays in Lab Rax enclosures. Pi4 is the first supported geometry adapter, not the whole product. Confirmed GUI choices include dark professional styling, a CAD viewport, three panels, Equipment Library / Assembly Explorer tabs, contextual Properties, guided creation, a startup dashboard and searchable shortcut reference. Historical choices were design specifications; they do not prove those features were implemented. Later constraints take precedence: no printer integration, no automatic builds, mounting tabled, niche research parked, Phase7 closed with limitations.

The original uploaded HTML files (`index.html` / `lab-rax-assembler-code-only.html`) and generated rack-frame implementation have not been recovered. This change rebuilds the core workspace around the existing current app; it is not a wholesale restoration of that old implementation.

## Implemented

- Dark three-panel studio with Rack / Assemble / Review / Prepare navigation and contextual property controls.
- Dashboard, multiple named rack layouts, explicit settings dialog, 1–48 logical slots, optional user-supplied width/depth/pitch. Missing dimensions remain null/UNKNOWN. Unknown-dimension views use an explicitly labeled normalized schematic.
- Orbitable rack schematic, slot selection through Explorer or the viewport, and logical occupancy display. Posts, rails and allocation shelves are illustration primitives; none enter STL generation.
- Equipment Library Pi4 picture card, selected-slot creation wizard, explicit allocation confirmation, overlap/bounds protection and inspection of existing Pi4 baseline geometry. Reserving slots does not resize meshes or establish installed fit.
- Existing hardware library/import/filter controls, shared Pi4 pins and dimension controls, reviews and generation/export handlers retained by moving their actual DOM elements. No hardware schema migration, packs or new pins.
- Explicit Save layout and Ctrl/Cmd+S for rack layouts. `rack-workspace.json` lives beside the selected library, independent of `library.sqlite3` and `revisions/`. Atomic replacement, generation checks against stale writers and immutable prior JSON recovery files under `rack-history/`.
- Searchable centered Keyboard Shortcuts dialog; keyboard focus styles. Existing per-pixel mesh depth testing retained and canvas colors aligned with the dark theme.

## Boundaries and missing features

Rack creation currently means layout planning and space allocation. There is no rack-frame STL generator, certified Lab Rax post/rail profile, rack-wide collision/clearance calculation or arbitrary equipment adapter. Frame profiles and usable depth remain unverified. Entering dimensions is not manufacturer verification.

Pi4 slot entries currently reference the same existing hardware project; independent per-slot hardware pins/design revisions are not implemented. Manufacturing exports still use the documented Pi4 assembly coordinates and contain no rack-frame or slot-position geometry. Existing legacy cache downloads remain blocked without their integrity manifest. Nothing was regenerated to bypass that rule.

The larger original specification also describes drag-and-drop, direct manipulation, independent equipment instances, synchronized revision comparison and other capabilities not implemented here. Do not mark the entire historical specification complete or import its old printer requirements into current scope.

## Preservation and verification

- Source safety copy: before-app/ (includes the app before this restoration; not a release package).
- Protected normal-use/Beta0.8 database and cache hashes: protected-data-hashes.json. All matched after acceptance. Baseline SCAD, assembly, Pi reference and mounting module matched the safety copy.
- 7 new rack document tests PASS; 12 existing app tests PASS, excluding the tabled mounting-specific test. Catalog/frontend handler, viewer behavior, pixel occlusion and JavaScript syntax checks PASS.
- HTTP_Checks.json: GUI assets and APIs, rack save/reload, stale-write rejection, token enforcement, unchanged hardware state; all in new temporary data.
- Browser on disposable acceptance-data: create five-slot rack; select slot2; confirm Pi4 allocation; save/reload; reject overlap and shrinking past an occupied slot; equipment-card workflow; assembly view; Review/Prepare navigation; searchable shortcuts. No browser console errors. No renderer, geometry export or import buttons clicked.
- Screenshots: Rack_Workspace.png (disposable test rack), Normal_Use_Dashboard.png (actual normal-use app).
- Verification.json records the checks and remaining limitations. The browser test server was stopped and its test tab closed. A previously running launcher process held port8765; identified normal-use processes were restarted to activate the updated routes.

Normal app remains at http://127.0.0.1:8765 using `data/normal-use` with `--existing-library`. Its new dashboard was verified read-only. No rack document was initialized there by acceptance; the first real rack remains Brian's choice. Library, pins and cache remain unchanged.

## Next development

Recover and inspect the original HTML application and creator rack component sources, including rights/provenance, before claiming the old rack generator is restored. Use recovered source or a separately verified component adapter for exact rack geometry. Keep current layout planning distinct from physical/export support. Continue the existing STL-only scope; no new numbered phase or mounting work is implied.

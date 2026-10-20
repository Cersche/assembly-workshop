# Assembly Workshop — persistent development guidance

Read AGENTS.md, PROJECT.md and HANDOFF.md first. HANDOFF.md contains current Phase7 status; outputs/Phase7_Closeout/Closeout_Report.md consolidates digital acceptance and Brian's reported specimen fit. Historical planning remains in docs/phase7-readiness. Inspect only relevant referenced files; do not scan the whole repository by default.

- Preserve all outputs/, work/, user data, immutable hardware revisions, build caches, project pins and the historical mechanical baseline. Most assets are untracked: a Git clone/commit alone is not a backup. Never git clean, reset or replace these assets as routine setup.
- Four-corner mounting is SETTLED by Brian (2026-10-18): every faceplate U gets four rack holes, two per side; corner radius is limited to 2.5 mm as a consequence. Fit/strength of the four-hole design remains UNKNOWN; no physical testing without Brian's direction.
- Phase 6 is closed WITH LIMITATIONS. Phase 7 is CLOSED WITH LIMITATIONS at Brian's explicit direction. Digital acceptance passed and Brian confirms qualitative fit of the earlier supplied specimen. Physical test fitting is LATE Phase 7 and requires Brian's direction. No printing, purchases, uploads, release packaging, publishing, deployments or pushes without explicit authorization. This organization task authorizes none of those.
- Ask before a fresh desktop-control session; read applicable computer-use instructions first. No subagents unless authorized.
- Keep unsupported dimensions, usable depth, generic wall guidance, process settings, loads, fit and strength UNKNOWN. Digital screening, mesh closure and supplier metadata do not establish physical approval.
- Preserve M3 x 0.5 adapter limits and mechanical baseline. Catalog breadth is not geometry support. Conditional manufacturer guidance is not generic FDM wall guidance. Nominal after-knurl OD is not a certified maximum.
- Draft does not save; explicit import does not repin. Preserve immutable old revisions. Failed checks block proposed export; UNKNOWNs remain visible. Source disagreement and project source policy remain distinct.
- Use new disposable data for acceptance, never active user data. Do not regenerate historical evidence or run old geometry scripts blindly. No automatic builds. Supplier/Pi assets with unresolved rights stay local and are not redistributed.
- Python 3.10 standard library; use UTF-8 explicitly. Existing checks and commands are in PROJECT.md/HANDOFF.md. OpenSCAD.exe is the documented renderer; the .com launcher was reported broken.
- Continue authorized reversible work without repeated confirmation. Ask for missing decisions only when they are needed. Report what was actually verified, keep progress and handoffs concise, and distinguish observations from assumptions.
- Do not add credentials or secrets to instructions, documentation or version control.

## STL delivery scope — Brian, 2026-10-18

The app delivers STL files. Do not require or build integration for the end user's printer, slicer, filament profiles or machine setup. Printer/material identification is not an app-readiness or Phase 7 software-completion gate. Prioritize supported geometry, exact source/mesh matching, traceable hardware, export integrity and explicit validation limits. Any later optional physical validation applies only to its documented specimens/material/process; it does not certify arbitrary printers or materials. Do not ask for printer details to continue software development. Unsupported printed fit and strength remain UNKNOWN. Physical fitting remains late Phase 7 and requires Brian's direction; printing is not authorized.

## Confirmed specimen and parked research — 2026-10-18

Brian confirms positive physical fit of the earlier supplied tray/faceplate specimen (Clearance v2: two-hole, 3 mm, square-corner plate; it does not transfer to the current four-hole/4 mm design); preserve that report/photos/provenance without repeatedly asking him to identify already recovered files. This is specimen-specific qualitative evidence, not general strength/installation approval or a physical test of the later digital build. Remaining niche insert research is parked at Brian's direction; do not resume by default. Phase7 is closed with limitations; do not silently mark every physical UNKNOWN passed. Further printing/testing remains separately authorized.


## Recovered rack-first purpose and GUI — 2026-10-18

Assembly Workshop is intended to design equipment assemblies in a Lab Rax rack context. Brian confirmed configure rack → select slot → create the assembly. Preserve the recovered dark three-panel GUI direction and decisions at work/gui-restoration/Recovered_GUI_Decisions.json. Later scope restrictions still supersede historical specifications. Brian subsequently requested the main rack look like the supplied enclosure: the viewport now instances actual source meshes using recovered visual placements. Do not substitute generic box posts for that mesh preview. Each saved slot allocation now has independent assembly hardware pins/inputs/revisions; the legacy project is preserved and copied once for new assemblies. Appearance and local image assets are preview-only. Preserve rack-history/ and artwork/ with the rack document. See work/gui-restoration/Restoration_Report.md and work/rack-scene/Report.md for implemented versus missing capabilities; do not confuse historical planning, recreated GUI and recovered implementation. Rack layout data/history and unsaved user drafts must be preserved alongside library.sqlite3 and revisions/.

## Confirmed scope expansion — Brian, 2026-10-18

These supersede the earlier "Pi4 only adapter" and "no rack-frame STL adapter" restrictions. Physical fit, strength and retention of everything below remain UNKNOWN.

- **Support extension rule:** each 1U support extension occupies its own 1U between stacked posts (post U + extension U = rack height); joints are movable.
- **Equipment wizard:** generic `equipment_tray.scad` plus the dimensions/STL/SCAD/STEP (local FreeCAD) import wizard is a second manufacturing adapter beside Pi4. Leave the Pi4 path untouched. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing are unprinted.
- **Rack-frame STL export:** "PRINT THE RACK" / `/api/rack-stl` is in scope. Creator parts stay local (BY-NC-SA, personal use) and are never redistributed. Do not run exports during housekeeping.
- **Data location (C4) SETTLED by Brian:** `data/normal-use/` is the official user data. Always start the app via `outputs/Mechanical_Design_App/start.bat` (or the same `--existing-library --data …\data\normal-use` arguments); never run bare `python app.py`, which falls back to the app-local folder. `outputs/Mechanical_Design_App/data/` is a preserved historical copy (older 1-allocation rack, 8:59 PM wizard cache); do not delete or merge it. See docs/housekeeping/Data_Locations.md.

## Selected hybrid GUI — Brian, 2026-10-18

Brian chose1C/2C/3A/4A/5A/6A/7A/8A: hybrid with collapsible inspector; collapsible Racks & slots, Equipment and Hardware library on the left (2C confirmed FINAL by Brian 2026-10-19); click selects, ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic Save; color presets plus custom picker; local artwork fit/center, size/position/remove; navigation first. These choices supersede the earlier unchosen concepts. Implemented pass and acceptance: work/gui-refinement/Report.md. Drafts remain unsaved until Save; checks/exports do not silently save them. Artwork remains preview-only. Brian reviewed the left grouping on 2026-10-19 and made it final (see work/equipment-list/Report.md and work/hardware-section/Report.md); do not rearrange it without his direction.

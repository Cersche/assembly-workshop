# Assembly Workshop — agent guidance

Read HANDOFF.md (current status) and ROADMAP.md (Now / Next / Later, the only plan) first. PROJECT.md has the commands, checks and tool usage. Read other files only as the task needs them; don't scan the whole repository. For any part design work, use the /new-part skill (`.claude/skills/new-part/SKILL.md`).

Cloud sessions and other machines can't see Brian's global CLAUDE.md or the PC's memory folder, so every rule this project depends on is stated or pointed to here.

## Working rules

- **Sessions:** start with `git pull` and HANDOFF.md. End by updating HANDOFF.md, committing and pushing to `main`, so the next account or device can pick up. Pushing is pre-approved (Brian, 2026-10-22). Never force-push; if a push is rejected, pull and merge first. One editing session at a time.
- **Brian decides:** printing, physical testing, purchases, uploads, publishing, release packaging and deployments need his direction. Brian does the printing; a part becomes a print file only when he says he is printing it. Ask before a fresh desktop-control session. No subagents unless he asks.
- **Repo stays private:** https://github.com/Cersche/assembly-workshop holds the whole project, including outputs/, data/normal-use/, archives and licensed third-party parts. Never make it public, fork it publicly or add collaborators without Brian's direction.
- **Preserve:** outputs/, work/, user data (data/normal-use/ with library.sqlite3, revisions/, rack-history/, artwork/ and unsaved drafts), build caches, project pins and the historical mechanical baseline. Never git clean, reset or replace them as routine setup. Printed or saved revisions are immutable: make a new revision instead. Don't regenerate historical evidence or run old geometry scripts blindly. No automatic builds.
- **Data:** `data/normal-use/` is the official user data. Start the app only via `outputs/Mechanical_Design_App/start.bat` (or the same `--existing-library --data …\data\normal-use` arguments); bare `python app.py` falls back to the app-local folder. `outputs/Mechanical_Design_App/data/` is a preserved historical copy: don't delete or merge it (docs/housekeeping/Data_Locations.md). Use new disposable data for acceptance; never test on data/normal-use in any environment.
- **UNKNOWN stays UNKNOWN:** unsupported dimensions, usable depth, generic wall guidance, process settings, loads, fit and strength. Digital checks, mesh closure and supplier metadata are not physical approval. A fit report covers the reported specimen and feature only (docs/Fit_Findings.md); never mark a physical UNKNOWN passed on your own.
- **Reporting:** say what was actually verified and separate observations from assumptions. Continue authorized reversible work without repeated confirmation; ask only for decisions you need.
- **No phase language:** the numbered-phase plan is retired (Brian, 2026-10-19). No phase numbers or "closed with limitations" wording in new docs. Old phase-named folders and files are preserved history; don't rename or delete them, and don't read their milestone claims as status.
- **Environment:** Python 3.10 standard library, UTF-8 stated explicitly. Cloud sessions run Linux without OpenSCAD/FreeCAD and can't show the rack GUI: renders, STL exports and GUI checks happen on the PC.
- No credentials or secrets in instructions, docs or version control.

## Settled standards (Brian)

Fit results apply to the printed specimens on Brian's rack; strength is UNKNOWN throughout.

- **Four-corner mounting (2026-10-18):** every faceplate U gets four rack holes, two per side, so the corner radius is limited to 2.5 mm. Faceplates only ever get those corner holes; the posts' empty middle holes may only be used by a tie-in from behind (2026-10-28).
- **44.4 mm faceplate (2026-10-20, coupons FP44-A..D):** 44.4 mm per 1U, width 252, thickness 4, 2.5 mm corners, slots at ±118.2625, ±15.902 about each U centre. The plate is centred in its slot; Z=0 is the slot bottom.
- **Fasteners (2026-10-31; same table as global CLAUDE.md, keep the two in step):** no self-tapping screws into prints and no drilling printed parts: every screw joint gets a heat-set insert with its bore modeled in. M3 is the default, M6 for weight-bearing joints, M2/M2.5 only where a device forces it. Inserts (thread x length x OD): M6 x 5 x 8 → 7.6 bore, ≥ 6 deep; M3 x 3 x 5 → 4.2 bore, 4 deep, boss ≥ 9 OD; M2.5 x 4 x 3.5 → 3.2 bore, 5 deep. Screws: M3 countersunk, M2.5 socket head, and M6 x 10 button head for every new design (Brian, 2026-11-11; it replaces M6 x 8, which stays on already printed revisions). Make each M6 bore deep enough for the 10 mm screw. Ask before adding a screw type.
- **M6 bracket hardware (2026-10-28):** bracket redesigns use the rack posts' M6 inserts and M6 button heads (M6 x 10 for new designs) instead of M3 (one-item BOM; M3 lacked rigidity). One bracket per fresh session; the printed baseline is listed in HANDOFF.md. The app's M3 x 0.5 adapter limits still apply to everything else.
- **Keystone (2026-10-19):** the golden keystone, `ks_style="golden"`, `ks_tight=0.2`, opening 14.8 x 16.4, is the permanent default. Don't change it or propose new keystone coupons unless Brian asks. Retention over time is UNKNOWN.
- **OptiPlex orientation (2026-10-20):** imported with X up and rotated 90° once, so the power button is at the faceplate and the ports face the rear posts. Brian asked to be stopped if he tries to change this: remind him first.
- **Own printed rack (2026-11-09):** Brian's own rounded printed rack (posts plus corner brackets, flush bezel, Lab Rax U standards, depth 240, M6 x 10 button heads) replaces both the Lab Rax frame plan and the 2020 extrusion plan. Draft, unprinted: see HANDOFF.md.
- **Test print IDs (2026-10-19):** every test print or coupon carries a unique ID modeled into the part, away from the feature under test, and the same ID in its folder, file names and README.
- **OpenSCAD (2026-11-05):** new parts render with the pinned snapshot `D:\Tools\OpenSCAD-snapshot\OpenSCAD-2026.11.01-x86-64\openscad.exe --backend=manifold` (PC only; don't auto-update it). Existing revisions, the app and its scripts stay on `C:\Program Files\OpenSCAD\openscad.exe` (2021.01), because text outlines differ between versions; use OpenSCAD.exe, not the broken .com launcher.

## Showing parts and asking for measurements

- **3D viewer (2026-10-27):** whenever work produces, changes or examines STL/3MF files, build one page for the job with `python tools/mesh_viewer.py <files...> -o work/mesh-viewer/<name>.html -t "<title>"`, send it with SendUserFile (display "render") and publish it as a private Artifact, without being asked. Brian pastes back "3D viewer notes" (mm in the file's own frame, part names as in the file). Preview only. Don't commit generated pages unless asked.
- **Measurements (2026-11-08):** every measurement request is an interactive page: `tools/mesh_viewer.py ... --measure spec.json`, sent the same way. Never ask in words alone. Usage: PROJECT.md.

## The app

- **Purpose:** design equipment assemblies in a rack: configure rack → select slot → create the assembly. It delivers STL files only. Don't build or require printer, slicer, filament or machine integration, and don't ask for printer details; printer or material identification is not a readiness gate. Priorities: supported geometry, exact source/mesh matching, traceable hardware, export integrity and explicit validation limits.
- **Rack view:** the viewport instances the actual source meshes at the recovered placements; don't substitute generic box posts. Each saved slot has its own hardware pins, inputs and revisions.
- **GUI (final, Brian 2026-10-19):** dark three-panel hybrid with a collapsible inspector; collapsible Racks & slots, Equipment and Hardware library on the left; click selects, ellipsis/right-click for actions; Setup/Hardware/Appearance tabs; one explicit atomic Save. Don't rearrange the left grouping without his direction. Decisions: work/gui-restoration/Recovered_GUI_Decisions.json, work/gui-refinement/Report.md.
- **Saving:** a draft does not save and an explicit import does not repin. Checks and exports never silently save drafts. Failed checks block a proposed export, and UNKNOWNs stay visible. Source disagreement and project source policy are separate things.
- **Hardware catalog:** catalog breadth is not geometry support. Conditional manufacturer guidance is not generic FDM wall guidance. Nominal after-knurl OD is not a certified maximum. Niche insert research is parked; don't resume it by default.
- **Equipment wizard:** generic `equipment_tray.scad` plus the dimensions/STL/SCAD/STEP (local FreeCAD) import wizard is the manufacturing path. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing are unprinted. No Pi wording, defaults or Pi-specific fields: the Pi 4 is one saved library example only.
- **Support extensions:** each 1U support extension occupies its own 1U between stacked posts (post U + extension U = rack height); joints are movable.
- **PRINT THE RACK** (`/api/rack-stl`) is in scope.
- **Cable planner (2026-10-19):** front/rear views, selectable ports and keystones, cable guides, cables entering and leaving, suggestions, wiring diagram (work/cable-management/Proposal.html, Report.md). Guide and cable fit, capacity and strength are UNKNOWN; cable lengths are planning estimates.
- **Print in color (2026-10-19, extended 2026-10-21):** the opt-in export (`faceplate_color.py`, `/api/faceplate-colors/preview|export`) is the only artwork-to-STL path. It rebuilds a wizard-made faceplate (`equipment_tray.scad`, 4 mm, front face Y=-4, 44.4 mm per U, four-corner slots, 1U–5U, including a one-piece "combined" part) from the slot's saved library item and tray settings, and turns the saved image into one STL per filament color (inlay 0.6 mm by default, or raised). The image lands where the rack view draws it: `faceplate_color.clear_window` ports `rack-studio.js clearWindow` and `faceplate_color.openings` matches `equipment-wizard.js openings`; keep them in step. Color stays 2 mm clear of ports, windows, keystone blocks and rack slots and 1 mm inside the plate outline. Export uses the saved rack document only; preview may use draft settings and writes nothing. PROPOSED — UNVALIDATED: printed color result, fit and strength UNKNOWN. Normal tray, faceplate, rack and wizard STLs never contain color or artwork; relief or engraving there needs Brian's explicit direction. Images may be PNG, JPEG, WebP, GIF, BMP, AVIF or SVG, converted locally to one PNG of at most 1024 px / 1.4 MB.

## Third-party meshes and licences

Lab Rax creator parts (BY-NC-SA), the golden keystone source (BY-NC-SA), the Lab Rax Cable Guide (mklements, MakerWorld Exclusive License) and supplier assets are for Brian's personal use: credited, never redistributed, never in anything shared or public. Inside the private repo and private Artifacts they may be used freely (Brian, 2026-11-03 and 2026-11-06: "stop worrying about licenses"). The cable guide is a preview mesh only and never goes into PRINT THE RACK or rack STLs. Before any public release Brian will contact the creators, and conflicting licensed files will be removed.

## History (not current rules)

- Earlier specimen: Brian confirmed qualitative fit of the Clearance v2 tray/faceplate (two-hole, 3 mm, square corners). It does not transfer to the four-hole 4 mm design. Keep its report, photos and provenance; don't ask him to re-identify recovered files.
- Raspberry Pi 4: an early fit-test item, deep-cleaned out of the app on 2026-10-19 (work/codex-tasks/21-pi4-deep-clean-REPORT.md). Retired build files are in docs/archive/pi4-retired-20261019/; outputs/Lab_Rax_Pi4_* and pi_reference.json stay untouched.
- 42 mm plates, M3 bracket joints, the Lab Rax frame plan and the 2020 extrusion rack plan are superseded by the standards above.
- GUI recovery reports: work/gui-restoration/Restoration_Report.md, work/rack-scene/Report.md, work/equipment-list/Report.md, work/hardware-section/Report.md, work/faceplate-refinement/Report.md.

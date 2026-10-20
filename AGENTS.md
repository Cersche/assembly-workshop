# Assembly Workshop — persistent development guidance

Read AGENTS.md, PROJECT.md, HANDOFF.md and ROADMAP.md first. HANDOFF.md has current status; ROADMAP.md (Now / Next / Later) is the only plan. The old numbered-phase plan is retired (Brian, 2026-10-19): do not use phase numbers or "closed with limitations" milestone language in new docs, reports or handoffs. Folders and files with old phase names (e.g. outputs/Phase7_*, docs/phase7-readiness, catalog-packs/phase6-*) are preserved history only; their milestone claims are not current status. Inspect only relevant referenced files; do not scan the whole repository by default.

- Preserve all outputs/, work/, user data, immutable hardware revisions, build caches, project pins and the historical mechanical baseline. Most assets are untracked: a Git clone/commit alone is not a backup. Never git clean, reset or replace these assets as routine setup.
- Four-corner mounting is SETTLED by Brian (2026-10-18): every faceplate U gets four rack holes, two per side; corner radius is limited to 2.5 mm as a consequence. Fit/strength of the four-hole design remains UNKNOWN; no physical testing without Brian's direction.
- Digital checks pass and Brian confirms qualitative fit of the earlier supplied specimen. Physical test fitting is a ROADMAP "Next" item and requires Brian's direction. No printing, purchases, uploads, release packaging, publishing, deployments or pushes without explicit authorization. This organization task authorizes none of those.
- Ask before a fresh desktop-control session; read applicable computer-use instructions first. No subagents unless authorized.
- Keep unsupported dimensions, usable depth, generic wall guidance, process settings, loads, fit and strength UNKNOWN. Digital screening, mesh closure and supplier metadata do not establish physical approval.
- Preserve M3 x 0.5 adapter limits and mechanical baseline. Catalog breadth is not geometry support. Conditional manufacturer guidance is not generic FDM wall guidance. Nominal after-knurl OD is not a certified maximum.
- Draft does not save; explicit import does not repin. Preserve immutable old revisions. Failed checks block proposed export; UNKNOWNs remain visible. Source disagreement and project source policy remain distinct.
- Use new disposable data for acceptance, never active user data. Do not regenerate historical evidence or run old geometry scripts blindly. No automatic builds. Supplier/Pi assets with unresolved rights stay local and are not redistributed.
- Python 3.10 standard library; use UTF-8 explicitly. Existing checks and commands are in PROJECT.md/HANDOFF.md. OpenSCAD.exe is the documented renderer; the .com launcher was reported broken.
- Continue authorized reversible work without repeated confirmation. Ask for missing decisions only when they are needed. Report what was actually verified, keep progress and handoffs concise, and distinguish observations from assumptions.
- Do not add credentials or secrets to instructions, documentation or version control.

## STL delivery scope — Brian, 2026-10-18

The app delivers STL files. Do not require or build integration for the end user's printer, slicer, filament profiles or machine setup. Printer/material identification is not an app-readiness or software-completion gate. Prioritize supported geometry, exact source/mesh matching, traceable hardware, export integrity and explicit validation limits. Any later optional physical validation applies only to its documented specimens/material/process; it does not certify arbitrary printers or materials. Do not ask for printer details to continue software development. Unsupported printed fit and strength remain UNKNOWN. Physical fitting requires Brian's direction; printing is not authorized.

## Confirmed specimen and parked research — 2026-10-18

Brian confirms positive physical fit of the earlier supplied tray/faceplate specimen (Clearance v2: two-hole, 3 mm, square-corner plate; it does not transfer to the current four-hole/4 mm design); preserve that report/photos/provenance without repeatedly asking him to identify already recovered files. This is specimen-specific qualitative evidence, not general strength/installation approval or a physical test of the later digital build. Remaining niche insert research is parked at Brian's direction; do not resume by default. Do not silently mark any physical UNKNOWN passed. Further printing/testing remains separately authorized.


## Recovered rack-first purpose and GUI — 2026-10-18

Assembly Workshop is intended to design equipment assemblies in a Lab Rax rack context. Brian confirmed configure rack → select slot → create the assembly. Preserve the recovered dark three-panel GUI direction and decisions at work/gui-restoration/Recovered_GUI_Decisions.json. Later scope restrictions still supersede historical specifications. Brian subsequently requested the main rack look like the supplied enclosure: the viewport now instances actual source meshes using recovered visual placements. Do not substitute generic box posts for that mesh preview. Each saved slot allocation now has independent assembly hardware pins/inputs/revisions; the legacy project is preserved and copied once for new assemblies. Appearance colors and local image assets are previews; the only artwork-to-STL path is the opt-in Print in color export below. Preserve rack-history/ and artwork/ with the rack document. See work/gui-restoration/Restoration_Report.md and work/rack-scene/Report.md for implemented versus missing capabilities; do not confuse historical planning, recreated GUI and recovered implementation. Rack layout data/history and unsaved user drafts must be preserved alongside library.sqlite3 and revisions/.

## Raspberry Pi 4 is history — Brian, 2026-10-19

The Pi 4 was only an early fit-test item; later fit tests of other parts also went fine, so nothing in the design depends on it. Brian directed a deep clean (all levels): no Pi wording, defaults or Pi-specific code/data fields in the app; the Pi survives only as one saved example in the equipment library, built by the generic wizard / equipment_tray.scad path; legacy saved Pi slots are migrated on load (old document kept in rack-history/). Retired Pi-only build files are archived in docs/archive/pi4-retired-20261019/ (moved, not deleted). The printed specimen evidence (outputs/Lab_Rax_Pi4_*) and pi_reference.json stay untouched as history. Done by Codex task 21 and reviewed by Claude 2026-10-19 (work/codex-tasks/21-pi4-deep-clean-REPORT.md). Print in color stays unavailable for generic faceplates (its code depends on the old plate geometry); extending it needs Brian's direction. Older sections below/above that mention the Pi4 path or Pi4-only Print in color describe the pre-cleanup state.

## Confirmed scope expansion — Brian, 2026-10-18

These supersede the earlier "Pi4 only adapter" and "no rack-frame STL adapter" restrictions. Physical fit, strength and retention of everything below remain UNKNOWN.

- **Support extension rule:** each 1U support extension occupies its own 1U between stacked posts (post U + extension U = rack height); joints are movable.
- **Equipment wizard:** generic `equipment_tray.scad` plus the dimensions/STL/SCAD/STEP (local FreeCAD) import wizard is a second manufacturing adapter beside Pi4. Leave the Pi4 path untouched. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing are unprinted.
- **Rack-frame STL export:** "PRINT THE RACK" / `/api/rack-stl` is in scope. Creator parts stay local (BY-NC-SA, personal use) and are never redistributed. Do not run exports during housekeeping.
- **Data location (C4) SETTLED by Brian:** `data/normal-use/` is the official user data. Always start the app via `outputs/Mechanical_Design_App/start.bat` (or the same `--existing-library --data …\data\normal-use` arguments); never run bare `python app.py`, which falls back to the app-local folder. `outputs/Mechanical_Design_App/data/` is a preserved historical copy (older 1-allocation rack, 8:59 PM wizard cache); do not delete or merge it. See docs/housekeeping/Data_Locations.md.

## Cable management — Brian, 2026-10-19

A cabling planner is in scope: front/rear views, selectable ports/keystones, cable guides, cables entering/leaving the cabinet, suggestions, wiring diagram ([proposal](work/cable-management/Proposal.html)). The default guide (Lab Rax Cable Guide, mklements, MakerWorld Exclusive License) is a local preview mesh only: never redistributed, never in PRINT THE RACK / rack STLs. Ports come from a Pi 4 preset plus a wizard Ports step, then mesh-click fine-tuning. Guide/cable fit, capacity and strength remain UNKNOWN; cable lengths are planning estimates. Step 1 status: work/cable-management/Report.md.

## Selected hybrid GUI — Brian, 2026-10-18

Brian chose1C/2C/3A/4A/5A/6A/7A/8A: hybrid with collapsible inspector; collapsible Racks & slots, Equipment and Hardware library on the left (2C confirmed FINAL by Brian 2026-10-19); click selects, ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic Save; color presets plus custom picker; local artwork fit/center, size/position/remove; navigation first. These choices supersede the earlier unchosen concepts. Implemented pass and acceptance: work/gui-refinement/Report.md. Drafts remain unsaved until Save; checks/exports do not silently save them. Artwork in the viewers is preview-only (see "Faceplate artwork and Print in color" below). Brian reviewed the left grouping on 2026-10-19 and made it final (see work/equipment-list/Report.md and work/hardware-section/Report.md); do not rearrange it without his direction.

## Faceplate artwork and Print in color — Brian, 2026-10-19

Brian resolved the artwork scope conflict: the existing opt-in "Print in color" export (`faceplate_color.py`, `/api/faceplate-colors/preview|export`) is in scope. It turns the saved faceplate image into one STL per filament color for the **Raspberry Pi 4 faceplate only**, uses saved settings only, and is PROPOSED — UNVALIDATED (printed color result, fit and strength UNKNOWN). Everything else stays preview-only: the normal tray/faceplate STLs, rack STLs and wizard-made equipment STLs never contain color or artwork. Faceplate images may be PNG, JPEG, WebP, GIF, BMP, AVIF or SVG (vector), converted locally to one PNG of at most 1024 px / 1.4 MB. Wizard-made faceplates do not show or export images yet. Extending image-to-STL beyond this (other adapters, relief/engraving in the normal STL) still needs Brian's explicit direction. See work/faceplate-refinement/Report.md.
## Test print IDs — Brian, 2026-10-19

Every new test print or test coupon gets a unique identifier modeled into the part itself (embossed or engraved text, placed where it doesn't affect the feature under test). Use the same ID in its folder, file names and README so a printed piece can always be matched to its files. Existing coupons keep their files unchanged.

## Cloud repo and account switching — Brian, 2026-10-20

The whole project, including outputs/, data/normal-use/, archives and licensed third-party parts, is in the PRIVATE GitHub repo https://github.com/Cersche/assembly-workshop (branch `main`). This replaces the earlier "assets stay local" rule for this private repo only. Brian uses two Claude accounts on four devices (PC, laptop, iPad, iPhone), one session at a time. Both accounts may push.

- **Start of every session:** `git pull` (cloud sessions start from GitHub automatically). Read HANDOFF.md.
- **End of every session:** update HANDOFF.md, commit and push to `main` so the next account or device picks up from there. Never leave work only on one machine.
- **One at a time:** don't run two sessions that edit at once. If a push is rejected, pull and merge first; never force-push.
- **Keep the repo private.** Never make it public, fork it publicly or add collaborators without Brian's direction. Before any public release, Brian will contact the Lab Rax creator (MakerWorld) and licensed files that conflict will be removed. Redistribution limits still apply to everything outside this repo.
- **Cloud limits:** cloud sessions run Linux without the PC's OpenSCAD/FreeCAD and can't show the rack GUI. Renders, STL exports and GUI checks still happen on the PC. Never test on data/normal-use in any environment.
- No secrets or credentials in the repo. Python caches are ignored by .gitignore.

# Assembly Workshop — project entry point

Updated 2026-10-18. Current operational state is in HANDOFF.md; persistent boundaries are in AGENTS.md. Previous versions of both guides are preserved in outputs/Session_Handoff_20261018/.

## Product

A local rack-context design app for Lab Rax equipment: configure a rack, select a slot, then design its equipment/tray/faceplate/bracket assembly. STL files are the deliverable. The Pi4 assembly is the first supported geometry adapter. Printer/slicer integration is outside scope.

The original ChatGPT discussion included a dark professional three-panel workspace, equipment cards and assembly tree, contextual Properties and guided creation. User decisions were recovered and preserved at work/gui-restoration/Recovered_GUI_Decisions.json. This is evidence of choices, not proof all historical features are implemented. Later scope restrictions prevail.

## Paths

- Canonical project root: `C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop`.
- Runnable app: `outputs/Mechanical_Design_App/`, entry app.py and start.bat.
- Normal data: `data/normal-use/` (library.sqlite3, revisions/, plus rack-workspace.json/rack-history/ after explicit rack saves).
- Preserved original data: `outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/`. All beta revisions and historical outputs/work remain intact.
- Data-location/setup evidence: `outputs/Normal_Use_Location_Review/`.
- GUI recovery/source safety copy/acceptance: `work/gui-restoration/`.
- Current handoff/prompt/final preservation records: `outputs/Session_Handoff_20261018/`.
- Phase7 closed-with-limitations acceptance and specimen provenance: `outputs/Phase7_Closeout/`, `outputs/Phase7_Digital_Acceptance/`, `outputs/Phase7_Physical_Observations/`.
- Project membership last verified earlier: Assembly Workshop, ID23bbc12a-5bb0-42a8-8c3f-a060bf2d0ea0. Not rechecked/changed during this handoff.

## Working features

Python3.10 standard library, SQLite, HTML/JavaScript/canvas, loopback HTTP; no pip/npm runtime installation needed. Local OpenSCAD is used only for explicitly requested supported mesh generation.

Current GUI: dark dashboard and three-panel studio; Rack/Assemble/Review/Prepare; named rack-layout settings, orbitable schematic, slot selection/occupancy and guided Pi4 allocation; existing hardware imports/filtering, immutable catalog revisions, saved pins, joint inputs/checks, viewer and matching STL/source integrity safeguards. Rack saves are separate JSON documents with atomic writes, stale-save detection and prior-version recovery files. No normal-use rack was created by acceptance.

Current sourced catalog packs plus starter represent34 identities/38 revisions; normal-use library contains its preserved6 revisions because packs are explicit imports. Catalog breadth does not imply geometry support.

## Important limits

Rack layouts are schematic planning, not rack-frame manufacturing geometry. Original HTML and the three supplied creator rack sources are now recovered under `work/rack-geometry-recovery/`; no manufacturing rack-frame STL writer was located. The rack builder's new **Lab Rax references** viewer shows unchanged creator photos and21 individual components at full source coordinates, with observed bounds/provenance and Brian's attributed M6 note. It does not apply dimensions or assembled transforms to layouts. See its Recovery_Report.md for the supported geometry route and actual verification. Arbitrary equipment/CAD manipulation and independent per-slot hardware projects are not implemented. Pi4 placements share the existing hardware project. Manufacturing exports contain supported Pi4 geometry at its documented coordinates, not the rack or slot transforms.

Legacy build cache remains intact but downloads require integrity manifests; no automatic regeneration. Unsupported dimensions, usable depth, wall/process/load/strength/installation claims stay UNKNOWN. Phase7 is closed with limitations; the reported physical fit applies only to the earlier documented specimen. Four-corner mounting and niche insert research stay parked. Supplier/Pi reference rights remain unresolved; keep their assets local.

## Running and testing

Use `outputs/Mechanical_Design_App/start.bat`. It resolves `data/normal-use` and passes `--existing-library`, skipping automatic starter imports and rejecting a missing database. Direct invocation without this flag retains older default initialization behavior. Do not initialize an empty replacement for user data.

Open the running app at `http://127.0.0.1:8765/`; opening index.html directly cannot load its APIs. A direct-file guard now explains this. After Brian's screenshot, the inactive server was started with the existing library and all studio/reference/API GET checks passed; see `work/startup-repair/Verification.json` and the latest HANDOFF startup note.

Normal-use server was left running on http://127.0.0.1:8765 with the new dashboard. Do not start a duplicate. A fresh desktop/browser session requires permission. See HANDOFF.md for exact commands and last verification. Use only NEW disposable data for acceptance. No automatic builds; older scripts may render or package, so inspect relevant scripts first.

## Preservation

Most source/assets are untracked. Neither a Git commit nor a clone contains a full app backup. Preserve all outputs/, work/, user data, immutable revisions/caches and project pins. Do not clean/reset/replace them. The current complete working-file safety copy and per-file hash manifest are recorded in outputs/Session_Handoff_20261018/Preservation_Report.json when completed. The older Phase7 preservation remains at its recorded location. Local safety copies are not releases or off-machine backups.

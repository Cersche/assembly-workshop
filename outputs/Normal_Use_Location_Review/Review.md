# Normal-use location review — 2026-10-18

Current app code remains `outputs/Mechanical_Design_App/` under the canonical project root. Handoff commit verified: `0906668`.

Correction to earlier handoff: Beta0.7 and Beta0.8 libraries EXIST inside the nested `Mechanical_Design_App/data/` directory of each version. Earlier absence checks missed that nesting. The current app default library remains absent.

Eight historical beta databases were inspected using SQLite mode=ro without importing or launching the app. All database SHA-256 hashes matched before/after inspection. See Inventory.json for paths, pins, inputs and revision-file inventory. No data, pins, hardware records or meshes were changed.

Strongest local candidate: `outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/`. It contains six hardware revisions, one saved project, pinned Accu M3x8 r1 / McMaster 94459A140 r1, pilot 4 mm, and one cached revision directory. Beta0.7 has the same pin IDs and inputs but no revision directory. Earlier versions retain distinct historical state. This evidence identifies a candidate; it does not establish Brian's intended active library or certify compatibility with the current app.

Recommended decision: confirm Beta0.8 as the source library before preparing a separate normal-use copy of its entire data directory, preserving the historical original. Do not launch the current app against it yet: startup invokes Store initialization and load_starter(), which can write to the selected database. Do not use current start.bat yet: its default would initialize an empty current-app data directory.

Pending Brian: whether Beta0.8 is the intended library, or another existing directory should be used. No normal-use directory selected, copied, migrated or initialized; no launcher changed. Process ownership could not be inspected because CIM access was unavailable; no current server/port ownership claim is made. No desktop control, rendering, packaging or push occurred. Phase7 stays closed with limitations.


## Normal-use setup completed — 2026-10-18

Brian selected Beta0.8 as the source and authorized a separate normal-use copy. Current app: `outputs/Mechanical_Design_App/`. Normal-use data: `data/normal-use/`. Original `outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/` remains untouched. The full six-file copy retains all database rows, saved pins and cached revision files with identical SHA-256 hashes.

Launch using `outputs/Mechanical_Design_App/start.bat`; it resolves the normal-use directory relative to the launcher and passes `--existing-library`. This mode requires the existing database and skips automatic starter imports. Optional packs are not imported. Direct app.py invocation without that flag retains historical default behavior; use the configured launcher for normal use.

Compatibility checks PASS: SQLite integrity; current Store initialization/state; localhost GET /, /api/state and /api/project; complete source/copy hash equality after checks; missing-library guard exits without creating a directory. Test server stopped. No desktop control or rendering occurred. One legacy cache remains preserved and is correctly blocked from download for lacking an integrity manifest; regenerating it requires separate direction. This is a retained export limitation, not data loss. No packs imported or builds regenerated. See outputs/Normal_Use_Location_Review/Setup.json and verify_setup.py. Phase7 remains CLOSED WITH LIMITATIONS.

# Retired equipment-specific build path — 2026-10-19

Local preservation only. These files are history, not startup/build instructions. Nothing here certifies generic fit or strength. Do not redistribute reference/supplier/creator assets.

| File | Why archived |
| --- | --- |
| pi4_baseline.scad | Retired dedicated tray/faceplate source; new geometry uses equipment_tray.scad. |
| pi_validation.py | Dedicated board-reference, pinned-axis and baseline surface checks. |
| test_pi_validation.py | Tests only that retired reference/geometry path. |
| assembly.json | Historical two-part baseline viewer meshes; active equipment uses library/slot meshes or explicit box sketches. |
| joint_validation.json | Historical solid-regression evidence for the dedicated build. |
| workspace.js.bak | Old equipment-specific GUI backup; not active source. |
| app_legacy.py.txt | Extracted dedicated design adapter and retired HTTP implementation; complete original app.py is in the task's byte-for-byte checkpoint. |
| mesh_revision_legacy.py.txt | Retired dedicated build/cache/bundle implementation; shared mesh checks remain active. |
| test_app_before_cleanup.py.txt | Original mixed test module, preserving old baseline/adapter/HTTP tests removed from the active module. |
| test_mesh_integrity.py.txt | Original mixed tests, preserving retired builder/cache tests; generic closure and triangulation regressions remain active. |
| test_faceplate_color.py.txt | Original color tests, preserving its retired baseline-only export test; reduction/settings tests remain active. |

The first six files above were copied byte-for-byte, verified with SHA-256, then removed only from their original app paths. moves-sha256.json records those hashes. Extracted text sections use LF; complete originals of existing app/test source are preserved under ../codex/2026-10-19/task21/outputs/Mechanical_Design_App/.

Printed specimen folders and zips remain unchanged in outputs/Lab_Rax_Pi4_*. The local pi_reference.json and its provenance/rights manifest remain in the app directory, unused by the active viewer. User data, immutable revisions/caches, catalog-packs/ and rack-references/ were not modified. The active generic renderer sources are separate root files; the protected reference directory and its existing manifest remain intact.

The one bundled saved example is equipment-examples.json, using the generic equipment_tray.scad path. Library reads expose that record without startup builds or writing user data. The original rack document is archived before a migrated draft is returned; explicit Save is still required.

The historical color slicing adapter depends on a fixed 3 mm faceplate front and 216 × 34 mm window. Generic faceplates have a 4 mm front, variable heights and openings. Its API is gated as unavailable for current faceplates; saved artwork/settings remain preserved. No generic artwork-to-STL expansion was attempted.

# Assembly Workshop — current handoff (2026-10-18)

Read AGENTS.md and PROJECT.md, then only referenced relevant files. Canonical project home: C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop. The earlier generated folder was successfully renamed; previous copy and all assets retained.

## Goal and status

Local Python-standard-library/SQLite + HTML/JavaScript mechanical design app. Traceable hardware, constrained Pi4 M3 joint proposals, viewer and matching STLs. Printer/slicer integration is OUT OF SCOPE. Phases1–6 closed with limitations. Phase7 CLOSED WITH LIMITATIONS at Brian's explicit direction. Digital points2–6 accepted; Brian confirms positive qualitative physical fit for the earlier supplied printed tray/faceplate. All seven milestones complete within their stated scopes. See outputs/Phase7_Closeout/Closeout_Report.md.

## Current evidence

- App: outputs/Mechanical_Design_App/. Digital acceptance: outputs/Phase7_Digital_Acceptance/Report.md (46PythonPASS; one mounting-specific test deferred; JS behavior/syntax and9localhost endpointsPASS). New pi4-mesh-v2-triangulation1 cache uses strict mesh checks, bounded exact-collinear export retriangulation and per-artifact integrity manifests. Old caches stay untouched; legacy downloads lacking manifests require explicit new generation.
- Physical: outputs/Phase7_Physical_Observations/2026-10-18/. Brian: “Fitment is fantastic”;3photos, recovered prior chat/file provenance, User_Confirmation.json. Earlier replacement build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. Do not claim the later digital build was physically tested. No precise photo/ruler measurements inferred.
- Hardware:7packs+starter,34identities/38revisions.14/14screw and12/14insert families; M4.5/M7 inserts awaiting_source. Phase6 closeout: app catalog-packs/phase6-closeout.md. Full prior evidence remains at C:/Users/brian/Documents/Codex/2026-10-18/continue-assembly-workshop-from-c-users-2/outputs/Phase6_Closeout/.
- McMaster94459A140 drawing reference evidence: outputs/Phase7_Hardware_Evidence/94459A140_Drawing_Review.json. Brian parked further niche insert research. Keep missing tolerances/usable-depth/wall and installation claims UNKNOWN; do not infer dimensions or revise pins.
- Protected pi4_baseline.scad, assembly.json, pi_reference.json and mounting files unchanged. Rechecked evidence/photo/earlier-STL/protected hashes in outputs/Phase7_Closeout/Evidence_Check.json. Prior handoff saved there as before_HANDOFF.md.

## Next steps

1. Phase7 is closed; do not reopen it or start a new numbered phase by default. Read outputs/Phase7_Closeout/Next_Chat_Prompt.md. Establish the intended normal-use app/data directory next; current/Beta0.8/Beta0.7 default database paths were absent on read-only inspection.
2. Preserve existing user data and pins; do not mistake disposable acceptance data for the user's library. Do not create a new default database as a substitute for locating existing work.
3. Fresh desktop sessions require Brian's permission. Any later workflow review, release preparation or further physical work is separately scoped. No print/purchase/release package/publish/deploy/push authorized.

## Decisions and limitations

Preserve all outputs/,work/,user data,immutable hardware revisions/cache and project pins. Most app/evidence assets are untracked; Git alone is not a backup. Draft does not save; explicit imports do not repin; failures block proposed export; UNKNOWNs remain explicit. M3x0.5 adapter/pilot3–4.2/fixed stack3.3,pocket8,boss9 retained. Four-corner mounting matter remains TABLED until Brian raises it; supplied-photo/file identification is not reopening it. Strength/retention/torque, installation approval, Pi-board/rack/cable/tool access and whole-Pi containment/global clearance remain UNKNOWN or unestablished. Supplier/Pi reference rights unresolved; no redistribution. Exact supplier/project source policy stays distinct from manufacturer corrections. No subagents unless authorized.

## Run/check

From canonical project root, Python C:/Program Files/Python310/python.exe; Node C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe. App command: `& 'C:/Program Files/Python310/python.exe' outputs/Mechanical_Design_App/app.py --port 8767 --data work/NEW-disposable-folder` (the data directory must be NEW for acceptance). Ctrl+C stops it. Normal default launcher uses app-relative data/ and port8765; intended active data location is not yet established. No running acceptance server remains from digital tests.

Routine Python discovery includes the tabled mounting-specific test; for current acceptance scope use work/phase7-digital/accept.py filtering and inspect its fresh-data behavior before running. It renders and uses disposable data, so don't rerun by default. Existing Node tests: app test_catalog_workflow.cjs, test_phase7_workflow.cjs; work/test_viewer_v08.cjs; JS syntax checks and work/extract_frontend.py. OpenSCAD.exe C:/Program Files/OpenSCAD/openscad.exe (not broken .com launcher). User-authorized rendering only. No automatic builds or historical evidence regeneration.

## Final preservation and next-chat preparation

See outputs/Phase7_Closeout/Preservation_Report.json for the complete local safety copy and manifest. App/assets/work remain largely untracked: the handoff commit is not an app backup. Prepared next-chat prompt: outputs/Phase7_Closeout/Next_Chat_Prompt.md. No release packaging, printing, desktop control, publishing, deployment or push occurred during closeout. Static app roadmap/README now reflect Phase7 closed with limitations; final targeted checks recorded beside the closeout.

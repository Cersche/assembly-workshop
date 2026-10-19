# Static code map — outputs/Mechanical_Design_App only

2026-10-18. Files read as text; Python AST parsed without imports/execution. No tests or routes invoked. One line per source file, including tests and nested reference JS; data/ and __pycache__/ are not source maps. JSON assets are listed separately. Nested before-app/ source/assets and fixture directories are historical safety/test material, not active entry points; they are listed because they reside inside the requested app directory. Documentation references describe provenance, not a claim every function was accepted.

## Source files

| Source path relative to app | Purpose | Feature documentation |
| --- | --- | --- |
| app.py | Loopback HTTP handlers, immutable hardware Store, joint rules and Pi4 design proposals. | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| assembly_records.py | Independent slot hardware snapshots, appearance/artwork validation and atomic studio Save. | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| catalog.js | Hardware catalog filtering, replacement/import and selection UI. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| catalog_evidence.py | Offline source evidence/completeness audit without promoting verification. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| catalog_packs.py | Manifest-checked optional hardware catalog inventory/loading. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| equipment-wizard.js | Dimensions/STL/SCAD/STEP wizard, candidate detection, library placement and preview. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| equipment.py | Spec validation, local OpenSCAD/FreeCAD conversion, generic mesh cache, library and bundles. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| equipment_tray.scad | Generic equipment tray/faceplate geometry with mounting/joint/port/keystone/rear/coupon variants. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| faceplate_mounting.py | Applies supplied faceplate mounting definition to Pi4 proposed source. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| index.html | Page/legacy hardware interface and script bootstrapping; token/CSS response template. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| mesh_revision.py | Pi4 render identity/cache, mesh screening, artifact integrity and bundle checks. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| pi4_baseline.scad | Immutable historical Pi4 tray/faceplate mechanical baseline. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| pi_validation.py | Bounded Pi4 reference, dimensional/access evidence and screening limits. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack-reference.js | Parts catalog/source reference viewer integration. | work/rack-scene/Report.md; work/rack-geometry-recovery/Recovery_Report.md |
| rack-references/assembly-studio.js | Adapter from actual inspection mesh data to shared studio renderer. | work/render-studio/Report.md; work/assemble-studio/Report.md; work/rack-branding/Report.md |
| rack-references/before-app/app.py | Loopback HTTP handlers, immutable hardware Store, joint rules and Pi4 design proposals. | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| rack-references/before-app/assembly_records.py | Independent slot hardware snapshots, appearance/artwork validation and atomic studio Save. | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| rack-references/before-app/rack-studio.js | Shared WebGL source/inspection renderer, materials, picking, logo and effects. | work/render-studio/Report.md; work/assemble-studio/Report.md; work/rack-branding/Report.md |
| rack-references/before-app/workspace.js | Rack dashboard/slots/inspector, source scene, post/extension/paint actions and rack STL controls. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:11–46; work/gui-refinement/Report.md; work/workflow-audit/Report.md |
| rack-references/extract_logo.py | Recover original painted face IDs, without changing any source geometry. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack-references/preview_server.py | Fresh local appearance fixture; no active data or mesh builds. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack-references/rack-layout.js | Logical slot move/resize/release/undo helpers. | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| rack-references/rack-scene.js | Locked supplied component mapping and rigid source scene placements. | work/rack-scene/Report.md; work/rack-geometry-recovery/Recovery_Report.md |
| rack-references/rack-studio.js | Shared WebGL source/inspection renderer, materials, picking, logo and effects. | work/render-studio/Report.md; work/assemble-studio/Report.md; work/rack-branding/Report.md |
| rack-references/register_assets.py | Local source module register_assets.py; see static declarations and linked feature provenance. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack-references/test_branding.cjs | Regression checks for branding; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack-references/test_branding.py | Regression checks for branding; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| rack_references.py | Integrity-checked local source/reference asset delivery. | work/rack-scene/Report.md; work/rack-geometry-recovery/Recovery_Report.md |
| rack_stl.py | Local binary STL ZIP and counts from supplied rack component meshes. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:123–127; HANDOFF current C2/C3 |
| rack_workspace.py | Rack JSON schema, stack/slot validation, atomic saves, generations and history. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:11–46; work/gui-refinement/Report.md; work/workflow-audit/Report.md |
| start.bat | Launcher selecting data/normal-use and existing-library mode. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_app.py | Regression checks for app; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_assembly_records.py | Regression checks for assembly records; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_catalog_batch6.py | Regression checks for catalog batch6; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_catalog_evidence.py | Regression checks for catalog evidence; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_catalog_phase6.py | Regression checks for catalog phase6; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_catalog_workflow.cjs | Regression checks for catalog workflow; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_catalog_workflow.py | Regression checks for catalog workflow; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_installation_evidence.py | Regression checks for installation evidence; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_mesh_integrity.py | Regression checks for mesh integrity; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_pem_resolution.py | Regression checks for pem resolution; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_phase7_workflow.cjs | Regression checks for phase7 workflow; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_pi_validation.py | Regression checks for pi validation; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_rack_references.py | Regression checks for rack references; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_rack_workspace.py | Regression checks for rack workspace; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| test_studio_save.py | Regression checks for studio save; not run in housekeeping. | outputs/Phase7_Closeout/Closeout_Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:48–55; work/gui-refinement/Report.md (as applicable) |
| viewer.js | Actual assembly inspection, source/proposal selection, appearance and renderer controls. | work/render-studio/Report.md; work/assemble-studio/Report.md; work/rack-branding/Report.md |
| workspace.css | Canonical hybrid workspace styling, embedded by root HTTP response. | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| workspace.js | Rack dashboard/slots/inspector, source scene, post/extension/paint actions and rack STL controls. | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:11–46; work/gui-refinement/Report.md; work/workflow-audit/Report.md |

workspace.js.bak is a preserved older safety copy, not the active source. JSON/SCAD baselines and protected source meshes do not imply physical approval.

## JSON source/configuration assets (data/cache excluded)

| Asset | Purpose |
| --- | --- |
| assembly.json | Baseline assembly inspection meshes |
| catalog-packs/phase6-batch1-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch1.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch2-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch2.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch3-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch3.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch4-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch4.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch5-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch5.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch6-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch6.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch7-manifest.json | Catalog hardware source records/manifest |
| catalog-packs/phase6-batch7.json | Catalog hardware source records/manifest |
| catalog-packs/source-gaps.json | Catalog hardware source records/manifest |
| faceplate_mounting.json | Supplied 1U faceplate mounting definition |
| joint_validation.json | Bounded joint evidence/rules |
| pi_reference.json | Detailed Pi reference geometry |
| pi_reference_manifest.json | Pi reference provenance/integrity |
| rack-references/asset-manifest.json | Reference asset SHA-256 delivery manifest |
| rack-references/before-app/asset-manifest.json | Reference asset SHA-256 delivery manifest |
| rack-references/Browser_Reloads.json | Local reference/configuration/provenance asset |
| rack-references/catalog.json | Local reference/configuration/provenance asset |
| rack-references/component_0_1.json | Exact supplied component coordinates/indices |
| rack-references/component_0_14.json | Exact supplied component coordinates/indices |
| rack-references/component_0_17.json | Exact supplied component coordinates/indices |
| rack-references/component_0_22.json | Exact supplied component coordinates/indices |
| rack-references/component_0_24.json | Exact supplied component coordinates/indices |
| rack-references/component_0_29.json | Exact supplied component coordinates/indices |
| rack-references/component_0_31.json | Exact supplied component coordinates/indices |
| rack-references/component_0_36.json | Exact supplied component coordinates/indices |
| rack-references/component_0_6.json | Exact supplied component coordinates/indices |
| rack-references/component_0_9.json | Exact supplied component coordinates/indices |
| rack-references/component_1_1.json | Exact supplied component coordinates/indices |
| rack-references/component_1_11.json | Exact supplied component coordinates/indices |
| rack-references/component_1_13.json | Exact supplied component coordinates/indices |
| rack-references/component_1_15.json | Exact supplied component coordinates/indices |
| rack-references/component_1_18.json | Exact supplied component coordinates/indices |
| rack-references/component_1_20.json | Exact supplied component coordinates/indices |
| rack-references/component_1_23.json | Exact supplied component coordinates/indices |
| rack-references/component_1_25.json | Exact supplied component coordinates/indices |
| rack-references/component_1_28.json | Exact supplied component coordinates/indices |
| rack-references/component_1_6.json | Exact supplied component coordinates/indices |
| rack-references/component_2_1.json | Exact supplied component coordinates/indices |
| rack-references/fixture-0li3pv2o/rack-history/4d274e74-5d5c-46fb-82a0-023f1b2cc9ea.json | Local reference/configuration/provenance asset |
| rack-references/fixture-0li3pv2o/rack-history/814b0610-fa71-440f-aa73-d43a9c9f20f2.json | Local reference/configuration/provenance asset |
| rack-references/fixture-0li3pv2o/rack-history/c81445d0-8988-41ee-a511-8eb8eb9314c1.json | Local reference/configuration/provenance asset |
| rack-references/fixture-0li3pv2o/rack-history/cf29af92-ab4f-452b-bcbf-58c7fe3d8da2.json | Local reference/configuration/provenance asset |
| rack-references/fixture-0li3pv2o/rack-workspace.json | Local reference/configuration/provenance asset |
| rack-references/rack-logo-faces.json | Source-painted wordmark triangle provenance |
| starter-hardware.json | Starter immutable hardware records |

## HTTP route dispatch in app.py

GET enters Handler.do_GET (normalizes URL path) → get_request; POST enters Handler.do_POST with host/token/body-size gates. Unmatched paths return 404; these are branch dispatch routes, not a framework router. Prefix routes retain suffix conditions shown. Methods other than GET/POST have no authored handler. The common POST size gate is 2 MB even where deeper converters advertise larger limits; static observation only.

| Method | Path / pattern | Handler / action | Dispatch file:line | Feature documentation |
| --- | --- | --- | --- | --- |
| GET | / | Handler.get_request → index.html + canonical workspace.css + session token | app.py:663 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /api/state | selected_store().state() | app.py:673 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| GET | /api/workspace-capabilities | Handler.get_request → fixed version/capability JSON | app.py:677 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| GET | /api/artwork/<sha256>.png | assembly_records.artwork | app.py:680 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| GET | /api/rack-workspace | rack_workspace.read | app.py:683 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| GET | /rack-references/<asset> (prefix; manifest checked) | rack_references.asset(self.path) | app.py:689 | work/rack-geometry-recovery/Recovery_Report.md; work/rack-scene/Report.md |
| GET | /api/equipment-library | equipment.library | app.py:698 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| GET | /api/equipment-mesh/<build>/<part>.stl | equipment.mesh_file | app.py:701 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| GET | /workspace.js | static file/HTML/CSS response | app.py:705 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /workspace.css | static file/HTML/CSS response | app.py:705 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /rack-reference.js | static file/HTML/CSS response | app.py:705 | work/rack-geometry-recovery/Recovery_Report.md; work/rack-scene/Report.md |
| GET | /equipment-wizard.js | static file/HTML/CSS response | app.py:705 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| GET | /api/catalog-packs | catalog_packs.inventory | app.py:710 | outputs/Phase7_Closeout/Closeout_Report.md; outputs/Mechanical_Design_App/hardware-records.md |
| GET | /catalog.js | static file/HTML/CSS response | app.py:713 | outputs/Phase7_Closeout/Closeout_Report.md; outputs/Mechanical_Design_App/hardware-records.md |
| GET | /api/project | selected_store().project() | app.py:716 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| GET | /api/geometry | joint_geometry(selected_store().project()) | app.py:720 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /api/pi-reference | pi_validation.reference | app.py:724 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /api/assembly-checks | pi_validation.validate | app.py:736 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /api/assembly | Handler.get_request → assembly.json | app.py:740 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /viewer.js | static file/HTML/CSS response | app.py:744 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| GET | /api/bom | selected_store().project() → CSV rows | app.py:748 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| POST | /api/studio-save | assembly_records.save_workspace | app.py:785 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| POST | /api/rack-workspace | rack_workspace.save | app.py:788 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| POST | /api/artwork | assembly_records.save_artwork | app.py:794 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| POST | /api/import | store.import_parts(payload) → store.state() | app.py:797 | outputs/Phase7_Closeout/Closeout_Report.md; outputs/Mechanical_Design_App/hardware-records.md |
| POST | /api/save | selected_store().save(payload) | app.py:803 | work/assembly-instances/Report.md; work/gui-refinement/Report.md |
| POST | /api/preview | joint_geometry(selected_store().draft(payload)) | app.py:807 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| POST | /api/design | design_revision → in-memory SCAD/revision ZIP | app.py:811 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| POST | /api/build | assembly_records.fingerprint, mesh_revision.build | app.py:828 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| POST | /api/equipment-library | equipment.save_item | app.py:837 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/equipment-library-delete | rack_workspace.read, equipment.delete_item | app.py:840 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/equipment-preview | equipment.preview | app.py:846 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/rack-stl | rack_stl.export | app.py:849 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:123–127; HANDOFF current C2/C3 |
| POST | /api/step-to-stl | equipment.step_to_stl | app.py:852 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/scad-to-stl | equipment.scad_to_stl | app.py:855 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/equipment-build | equipment.build | app.py:858 | docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:57–113; HANDOFF current C2/C3 |
| POST | /api/build-bundle | mesh_revision.bundle, assembly_records.fingerprint | app.py:861 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |
| POST | /api/check | evaluate(selected_store().project() selections/inputs) | app.py:873 | work/startup-reliability/Report.md; work/gui-style-delivery/Report.md; docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:51–94 |

## Important boundaries and utility declarations

- app.py Store owns hardware revisions/projects; selected_store binds independent assembly context. Existing-library mode avoids starter initialization; data defaults and launcher differ (Data_Locations.md).
- Pi4 design_revision and mesh_revision handle the legacy adapter; equipment.py is a separate generic pipeline. Presence does not imply equal validation coverage.
- rack_stl consumes supplied local component meshes. Creator parts never leave local personal-use scope under Brian's direction.
- No source hashes/manifests/geometry were refreshed here. App tests listed above were read only.

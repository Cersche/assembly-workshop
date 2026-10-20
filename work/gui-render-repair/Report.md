# Hybrid GUI / renderer integration repair — 2026-10-18

Brian reported the normal app GUI broken after the rendering integration. The original normal tab visibly lacked the workspace styling and contained an older workspace shell rather than his selected hybrid. The rendering pass had integrated against that older script and failed to verify the documented hybrid contract. Renderer acceptance on disposable data did not establish that the selected normal GUI had been preserved.

## Repair

- Preserved the pre-repair app sources in `before-app/`; fingerprinted all 14 normal-use data files before work.
- Reconstructed the selected hybrid in `stage/` from `work/gui-refinement/before-app/`, the preserved GUI transformation scripts and controller resources. The reconstructed pre-render index.html and viewer.js match their recorded final GUI hashes exactly. The workspace reconstruction also restores the later tested save-race/input-error corrections. No historical geometry/build scripts were executed.
- Reintegrated the current renderer block into that hybrid shell, retaining independent per-slot assemblies, the capability handshake, guarded combined Save, pending-draft protection, context actions, appearance swatches/artwork and collapsible inspector/left groups.
- Preserved top-down Slot 01 indexing and corrected the recovered older sidebar hint. Appearance edits now redraw the rack scene immediately. Unset tray/faceplate preview colors match the recovered inspector defaults; explicitly saved colors retain their values.
- Loaded the unchanged hybrid stylesheet through a new versioned URL. Read-only HTTP diagnostics returned 200/text-css for both existing CSS URLs and both servers, so a permanent backend route failure was not established. The original tab's initial missing styling was observed directly; its exact earlier loading failure is not proven. The refreshed page now has the expected computed grid layout.
- No backend restart was required. app.py, assembly_records.py, workspace.css and viewer.js match the recorded final hybrid source hashes. The original rack-scene.js hash lock remains intact. The changed authored rack-studio.js entry was explicitly rehashed after aligning default colors.

## Actual acceptance

- All 37 targeted Python checks PASS using new temporary data.
- Preserved Save controller and appearance-startup JavaScript harnesses PASS. Existing Phase7 frontend harness PASS.
- Renderer geometry/camera suite PASS (256 comparisons); three renderer asset-integrity/route tests PASS.
- Disposable browser: Setup/Hardware/Appearance tabs, explicit color Save, inspector collapse/restore, slot ellipsis menu and opening the independently saved hardware editor PASS. No warning/error console entries observed. Only disposable data was saved.
- Normal server inspected in a fresh read-only tab: selected hybrid and renderer both visible, My Lab Rax / five slots / one allocation retained.
- Before refreshing Brian's original tab, checked twice that layout was saved, hardware dirty text was empty and Save was disabled. Reloaded that same tab; waited for source meshes to render. Normal_DOM_Checks.json confirms grid columns, all three inspector tabs, one visible Save, no duplicate element IDs and active source-mesh preview. No warning/error console entries observed. Screenshot: `Normal_GUI_Repaired.jpg`.
- Rechecked all 14 normal-use data file hashes: unchanged. No normal-use Save, imports, builds, exports or physical actions occurred. Existing user record and hardware pins were preserved.

The reconstruction scripts are one-shot recovery records, not startup commands. Do not run them against later sources as routine setup. The renderer report remains valid for its rendering tests; this report supersedes its earlier GUI-preservation claim and documents the additional restoration.

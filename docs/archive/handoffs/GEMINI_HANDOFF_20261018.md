# Continue Lab Rax Assembler / Assembly Workshop

Work in `C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop`. Read AGENTS.md, PROJECT.md, then the latest sections at the top of HANDOFF.md. Inspect relevant references only. Continue the existing implementation; do not reconstruct the GUI or repeat historical recovery/acceptance by default.

## Current build

- Python3.10 standard library local app: `outputs/Mechanical_Design_App/`, `http://127.0.0.1:8765/`. Last main PID29100; verify before starting/restarting anything. Do not duplicate the listener.
- **Data discrepancy:** current main process explicitly uses `outputs/Mechanical_Design_App/data`, while `start.bat` targets `data/normal-use`. Both contain preserved user data. Do not switch, merge or overwrite them without Brian's decision. Last verification: all16 files across both folders unchanged. Preserve unsaved browser drafts before refresh/restart.
- Last main browser view: Rack, My Lab Rax,5 slots/1 Pi4 allocation, Slot1 selected, Appearance tab with Rack colors open. Save disabled at last check. Disposable8770/8771 servers stopped;8767 is a separate disposable renderer server, not user data.

## Completed work

1. Restored Brian's chosen dark hybrid three-panel GUI: collapsible Racks & slots / Equipment / Hardware, collapsible inspector, Setup/Hardware/Appearance tabs, slot context actions and one explicit atomic Save. Independent slot assemblies retain separate hardware pins/inputs/revisions. Appearance and artwork are preview-only; drafts never silently save.
2. Rack viewport instances actual supplied source meshes using recovered visual placements. Shared WebGL studio engine adds depth testing, perspective/orthographic cameras, lighting/materials, shadows, ambient occlusion, artwork and picking. Faceplate selection has cyan rim/tint synchronized with inspector/slot context.
3. Assemble uses the same engine for its **actual loaded inspection meshes**, optional detailed Pi and nominal hardware envelopes. Retains selection, artwork, visibility, Top/Full assembly/joint focus/Zoom, orthographic front view and software fallback. Never substitute rack procedural equipment previews for inspection meshes.
4. Fixed recurring missing GUI styling: root HTTP response embeds canonical `workspace.css` directly. No duplicate CSS source. Separate CSS route remains available.
5. Fixed reproduced startup script-load failures: `WorkshopHTTPServer` uses connection backlog64 instead of default5. Cancelled response writes no longer trigger second error responses/misleading integrity errors. Controlled burst:9/24 old versus24/24 patched;72 parallel HTTP requests and20 consecutive browser reloads passed.
6. Restored independent color for original **Lab Rax wordmark on upper front beam** using448 painted triangles recovered from supplied5U3MF object23. Exact source vertices/indices matched; new `rack-logo-faces.json` records original face IDs/provenance. Appearance → Rack colors → Lab Rax logo has presets/custom picker; defaults lime. No source/manufacturing mesh edits.
7. Added saved `post_labels` toggle: Appearance → Show U labels on rack posts. U1–U48 are depth-tested surface markings on both front posts, top-down, with automatic contrast. Logo color and toggle survive explicit Save/reload. Shared Assemble WebGL and five further reloads passed. **Current labels can be occluded by occupied faceplates; Brian now requests relocation.**

## Next request — NOT implemented

Brian wants to build/edit the rack “like Legos”: individually labeled/selectable/editable posts and other source components, a universal component labeling system, and optional per-instance colors. Default pieces should share one color, with arbitrary individual overrides allowed. Current UI only supports whole-rack and component-**type** colors, not individual pieces or a component/stack editor. Design stable instance identities and persistence without losing existing layouts or hardware data. Keep rack editing a source-component layout preview; no implied manufacturing/physical certification.

Also move U labels to the **outer sides of the faceplate area**, so they remain visible when slots are occupied; retain visibility toggle and top-down numbering. Previous labels sit between front-post holes. Inspect actual geometry before choosing new positions.

The last turn only read relevant files and announced intent; no component-editor or label-relocation edits were made. Brian then requested this handoff.

## Key files/evidence

- `workspace.js`: GUI, rack controls/integration; `viewer.js`: Assemble controls/integration.
- `rack-references/rack-studio.js`: shared renderer; `assembly-studio.js`: exact inspection-mesh adapter; `rack-scene.js`: locked source mapping/poses; `rack-layout.js`: allocation helpers; `asset-manifest.json`: integrity enforcement.
- Backend: `app.py`, `rack_workspace.py`, `assembly_records.py`. Saved appearance currently validates whole-rack/type colors, `logo_color` and Boolean `post_labels`.
- Reports/tests/screenshots: `work/assemble-studio/`, `work/gui-render-repair/`, `work/gui-style-delivery/`, `work/startup-reliability/`, `work/rack-branding/`. Read their Report.md files for actual verification and limits. One-shot integration/reconstruction/extraction scripts are evidence, not startup commands.
- Original `rack-scene.js` SHA256 MUST remain `414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2`. Protected asset edits require matching manifest hashes; preserve HTTP409 rejection on mismatch.
- Supplied creator photo: `rack-references/reference_1.webp`; original rack3MF/HTML sources: `work/rack-geometry-recovery/sources/`. Keep unresolved-rights assets local.

## Boundaries

Preserve all outputs/, work/, both data folders, rack history/artwork, immutable revisions, pins and caches. Most assets are untracked; Git is not a backup. Never clean/reset/restore older shells wholesale. Use fresh disposable data for acceptance. Ask before fresh desktop-control sessions; no subagents unless authorized.

Phase7 is CLOSED WITH LIMITATIONS; Pi4 is the only manufacturing adapter. Rack preview is not a rack-frame STL adapter. Brian confirms specimen-specific perfect faceplate/post-hole fit; general fit, strength, loads and installation remain UNKNOWN. Four-corner mounting is TABLED; niche insert research is parked. No printer details needed. No automatic mesh builds, printing, purchases, remote uploads, release packaging, publishing, deployment or pushes without explicit authorization. Keep M3x0.5 adapter/mechanical baseline intact.

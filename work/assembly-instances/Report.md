# Independent assemblies, appearance and GUI alternatives — 2026-10-18

Brian requested closing the independent per-slot hardware gap, rack/equipment/component colors, custom faceplate images and two streamlined GUI options. Brian explicitly chose **preview first; STL artwork later**. No whole-interface redesign has been selected yet.

## Implemented and activated

- Each Pi4 allocation now owns a stable assembly ID, saved hardware snapshot, inputs and revision. New allocations copy the legacy project's pins once. Subsequent saves edit only the selected instance. Legacy SQLite pins and immutable part revisions remain intact. Save layout before opening a new instance's editor; allocation confirmation alone remains a draft.
- Rack workspace v2 persists assembly records and appearance beside the library. V1 documents are normalized only in memory on read, with deterministic instance IDs; the next explicit layout save creates v2 and preserves the previous file in rack-history. The server rejects stale generations/revisions, old clients overwriting v2, generic layout saves changing hardware snapshots, and wrong/older instance mesh bundles. Saved releases can be undone with their latest historical hardware snapshot.
- Project state, preview, checks, BOM/project exports and existing generation handlers carry the selected assembly identity. Appearance is excluded from hardware/mesh identity. No generation or manufacturing export was exercised. The existing supported adapter and tabled mechanical baseline were not changed.
- Whole-rack color plus overrides by source component type (all matching instances, not individual physical post IDs). Equipment color applies to the optional detailed Pi reference. Tray and faceplate colors apply to the inspection meshes. All are visual-only and saved with **Save layout**.
- Local PNG/JPEG/WebP chooser prepares a bounded PNG preview stored by content hash in `data/artwork/`. Image position and size are saved in the assembly appearance. Verified local image delivery and depth-tested texturing apply artwork only to actual planar faceplate front triangles; holes remain open. **View faceplate front** provides a readable front view. STL files contain no color or artwork. This is not a decal/engraving CAD adapter.
- Slot ellipsis and right-click share the same actions: create/open, allocation edit, appearance and release. Keyboard context menu, menu navigation and Escape are supported. Unsaved hardware drafts block switching assemblies; asynchronous responses cannot replace another slot's state.
- A capability handshake blocks writes from the updated frontend against an older backend. Updated server PID19424 runs `--existing-library` on8765. Opened a clean normal-use tab read-only; five slots, zero allocations. Its underlying v1 document was not migrated or saved. An older slot5 wizard mentioned in the last handoff was not accessible in this browser session; no older tab was reloaded, saved or cancelled.

## GUI options for Brian's decision

The inline `rack-studio-options.html` contains two interactive concepts, using a screenshot of the actual supplied-mesh rack preview:

- **Focused studio**: compact slot tree, ellipsis/context actions, one contextual inspector with Appearance/Details, equipment and hardware workflows on demand. Recommended starting point.
- **Canvas-first**: narrow slot rail, more canvas space, selection dock with appearance controls, hardware/allocation task sheets.

These are proposed layouts, not recovered historical screenshots or an applied redesign. Local mock interactions do not change app data. Both preserve the dark rack-first product direction. Refine after Brian chooses a direction or a combination.

## Verification and preservation

- 31 Python checks PASS: 7 rack documents, 3 exact-source reference/integrity tests, 10 independent-assembly tests, 11 existing app checks. Tests involving tabled mounting/source generation were excluded. All data were freshly disposable.
- Node suites PASS: actual catalog and Phase7 handlers; actual scoped context, stale response and concurrent-draft saves; per-pixel artwork coverage/occlusion; viewer controls/depth; rigid source scene; all21 reference selections; allocation/release/undo and serialized saves. Updated old test fixtures only where the DOM/document shape changed.
- Browser on disposable8767: two independently saved instances; changing slot1 pins/pilot left slot2 unchanged; draft switch guard; colors/image save and reload; readable faceplate image; rack/post override colors; equipment reference color; right-click and ellipsis menus. No console warnings/errors observed. Screenshots: Faceplate_Preview.png, Equipment_Color.png, Rack_Colors_Full.png.
- Normal-use seven files all match `Protected_Data_Before.json`, including real saved rack. SQLite integrity `ok`. Baseline SCAD, assembly, Pi reference and mounting module match the previous safety copy. `Verification.json` records the results. Before-app/before-guides safety copies and the new files remain local. Git is not a backup.

## Limits that remain

Pi4 is still the only manufacturing geometry adapter. There is no installed equipment placement/clearance engine, verified rack interface, explicit rack stack editor or rack-frame STL generator. Component transforms are recovered visual poses, not physical certification. M6 insert specification, fit, usable depth, loads, strength and installation remain UNKNOWN. The earlier positive fit remains specimen-specific. Phase7 remains CLOSED WITH LIMITATIONS; mounting and niche research remain parked. No builds, printing, purchases, remote uploads, release packaging, publishing or pushes occurred.

Preserve `rack-workspace.json`, `rack-history/` and the new `artwork/` directory together with the SQLite library and immutable mesh cache. Artwork assets are append-only; removal from a current draft does not purge historical images. History/recovery UI and image-on-STL work remain future work.

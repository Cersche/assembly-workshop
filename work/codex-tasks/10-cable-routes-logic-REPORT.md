# Task 10 — cable routes logic report

Completed 2026-10-19. **No API name or return-shape deviations.** Final checks PASS: 71 Python + 94 JavaScript tests, including 18 new routing tests.

**Behavioral limit:** detecting a moved guide on a manual route uses an in-memory position baseline established by an earlier `upkeep` call on the same rack object. A freshly loaded/replaced rack object has no previous positions in the specified schema; its first call cannot identify an earlier movement. Removed guide/exit references are detected on the first call. This limitation requires no schema or API changes and is not a physical-validation claim.

## API as built

`LabRaxCables` is an IIFE export and `module.exports` under Node. It uses no DOM, fetch, window lookup or external runtime imports. Context port/library data comes only from the caller. Non-upkeep helpers leave inputs unchanged; upkeep mutates the draft and keeps its movement baseline privately in a WeakMap.

| API | Return |
| --- | --- |
| EXIT_POSITIONS, ENDPOINT_KINDS | value-to-plain-label maps |
| TYPE_STYLE | port type to `{color, diameter_mm}`; existing port colours and specified nominal diameters |
| cableColor(cable) | override or type colour |
| endAnchor(rack, end, ctx) | port `[x,y,z]`, otherwise null |
| endFace(rack, end, ctx) | front, rear or null; outside endpoint counts as rear |
| autoRoute(rack, cable, ctx) | `{guides:[ids], exit:id|null}` |
| path(rack, cable, ctx) | ordered anchor arrays |
| estimate(rack, cable, ctx) | `{route_mm, length_m, to_exit, complete}` |
| linkedCable(rack, cable, ctx) | paired keystone cable id or null |
| portInUse(rack, allocation, port, exceptCableId) | cable id or null |
| nextNumber(rack) | lowest unused C-number |
| guideLoad(rack) | guide id to cable count |
| crowded(rack) | guide ids above the configured setting |
| upkeep(rack, ctx) | the rack's cable array after mutation |
| warnings(rack, cable, ctx) | plain warning strings |

## Routing choices and limits

Uses the specified scene coordinates and directional 8 mm port offsets. Anchor Z selects the containing U, clamped to rack bounds. Front posts require both port faces to be front; otherwise rear posts are used. Mean known port X chooses left/right. Guide order follows from-to slots. Existing valid exit selections are retained. For a new selection, each exit is scored against the last guide of its candidate route, or the known port anchor when there is no guide; this resolves the exit-slot/guide-interval dependency without iterative oscillation. Equal-distance ties keep list order. Without known port positions, deterministic right-post/list-order fallback applies.

`path` follows the contract literally: from port, stored ordered guides, exit, to port. It uses stored routes when present (including manual routes); upkeep recomputes automatic routes after edits. For endpoint-as-from cables, the exit still occupies the contract's specified position before the to port. Lengths sum straight segments, add loops per connected port, and round up to 0.1 m with floating-point boundary noise suppressed. Rendered sag/display diameters are not physical cable measurements. `complete` means neither end is null, as specified; warnings separately cover missing exits and UNKNOWN faces.

Manual guide order survives upkeep; removed references are dropped, moved observed guides remain and set route_changed, and user acknowledgement is preserved on later unchanged calls. Automatic routes follow equipment movement. Missing equipment, ports or outside endpoints disconnect the affected end while retaining the cable. Keystone links use the existing passThrough pair on the same allocation. No new persisted fields are introduced.

## Tests and commands

18 Node tests cover exact exports and global isolation, actual Pi preset and generic wizard anchors, all four pointing offsets, UNKNOWN faces, front/rear and left/right route selection, reversed order, multi-U anchors, exit selection/intervals, all exit coordinates, manual paths, loop fallback/zero/rounding, keystone links, occupancy/numbering, crowding, moved/removed guides, equipment movement/removal, port/endpoint deletion, idempotence, acknowledgement, warnings and nonmutation of read-only helpers.

Commands actually run:
- Targeted read-only `rg` of port and front-end call sites. A lookup of app-root rack-studio.js reported that path absent; no replacement or edits were made.
- `Copy-Item` archived run_checks.ps1 before its registration-only edit. Python stdin scripts normalized LF and calculated hashes.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1`: first task 10 run passed 70 Python and 93/94 JS; one new test caught a negative-zero empty length. Fixed it to return positive zero.
- The next run passed 70 Python + 94 JS. After final schema review, the final run passed **71 Python + 94 JS**, no skipped tests, and printed `RESULT: all checks passed`. A `Select-String` filter summarized counts and result.

No browser acceptance was performed. Front-end integration beyond the unchanged API and existing automated checks is not claimed. The caller must supply the equipment library before upkeep (the existing page hook already guards library readiness). The movement-baseline limitation above remains visible for UI review. No additional user decision is needed for these two task implementations.

Existing changed files were copied byte-for-byte before editing to `docs/archive/codex/2026-10-19/cable-tasks-09-10/`. Edited and new source, test, queue and report files use UTF-8/LF; archive copies preserve original bytes (including original line endings).

Nothing in `data/normal-use` or other user data was read or written. Tests use newly created temporary data or in-memory fixtures. No server was started/restarted, no desktop session was opened, and no builds, exports, printing, installs, commits or pushes were performed. Physical fit, strength and guide capacity remain UNKNOWN. No prohibited front-end file or asset manifest was edited.

## File hashes

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| outputs/Mechanical_Design_App/cable-routes.js | new | 429185d2da44e4435308f520c872714f88e38a3347373c153b98a6e7f315a626 |
| outputs/Mechanical_Design_App/js-tests/cable-routes.js | new | 0a6b71f6f5261dd5b4d5b1c0d503db1121e5eb0b5d8864e4b317f18cb5d40753 |
| outputs/Mechanical_Design_App/run_checks.ps1 | cf869ad11747e50ea4235630bd8d1da98fe7e3ea8b7f282c29001a7a68f80e7f | 5817ba6d84eac7152b983971f4ba874d91a5faf2fea8fb337eb8236ced7dabf7 |
| work/codex-tasks/README.md | e79474eaf84c82407ed58518a28e3496210c21a5939df33dba07f65a83f9e3c1 | 62b4f51339156ff738216fbb78569c4707c286175e827891a9a7abba234295bd |

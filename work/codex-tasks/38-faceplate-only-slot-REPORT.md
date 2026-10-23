# Task 38 — Faceplate-only slots

2026-10-22. Implementation and automated/digital acceptance complete; **browser acceptance and screenshots pending permission**. PROPOSED — UNVALIDATED: printed fit, strength and retention remain UNKNOWN.

## Review state and scope

Worked in `D:\Projects\assembly-workshop`; `git pull` was the first command and returned “Already up to date.” Read AGENTS.md, HANDOFF.md, PROJECT.md, ROADMAP.md, task queue README and task 38. No subagents. No user data used. Port 8765 was not stopped, restarted or used for testing. No commits or pushes were performed by this Codex session.

Brian explicitly approved `cable-ports.js` for the keystone-port integration in this chat. The task specification was also updated externally to include it. During this session another actor created commit **0241508** (“Task 38: allow cable-ports.js for keystone port pairs”), which included the initial edits to equipment.py, equipment_tray.scad and faceplate_color.py as well as the scope change. Therefore **review that commit plus the working tree**, not just `git diff`. This session did not create or undo that commit. Before hashes below are the original byte-for-byte snapshots taken before this session edited the files, not hashes of the now-current HEAD.

## Implemented

- Empty-slot ellipsis/right-click actions and Setup offer **Faceplate only**. Setup provides Blank, Keystones and Custom openings, 1U–5U, count per row, rows, individual X/Z nudges and editable rectangular/rounded openings.
- A reserved built-in equipment identity (`eq-000000000038`) avoids creating a fictitious device or writing the equipment library. Each allocation stores its own `tray.faceplate` settings and independent assembly identity. Existing rack schema, explicit atomic Save, history and immutable equipment-revision caches remain in use. Missing panel settings on ordinary items retain existing behavior.
- Apply changes only the draft. Explicit render/export does not save it. Height edits go through the panel editor so reservation and plate height stay together. Saved thin-wall warnings remain visible; Appearance omits the nonexistent tray color and Review handles panels separately from equipment envelopes.
- Engine uses the existing template, `joint="none"`, `part="faceplate"`, and emits **only faceplate.stl**. The bundled SCAD also defaults to faceplate. No tray/rear bracket/combined mesh. PRINT THE RACK was not changed.
- Golden keystones accept scalar X, `[X]` or `[X,Z]` in SCAD. Existing generated tray sources restore the exact original numeric-loop text; their source identities remain unchanged. The golden geometry table, tightness, plate dimensions and rack slots are unchanged.
- Rack view uses the plate-only sketch until an explicit exact render exists, then uses that mesh. Python/JS artwork keep-outs use each keystone's Z plus the existing 1.75 mm golden-block offset. Cables get stable reciprocal front/rear keystone pairs at each row's opening centre.
- Invalid overlap/rack-slot/outline clearance blocks export. Outline checks include the rounded corners. Web under 2 mm warns **“thin wall, fit/strength UNKNOWN”**; negative web fails. At most 10 per row and at most one row per U.

## Spacing decision

Largest equal pitch across the reference centre span ±96.75 mm, capped at **48 mm**. This keeps sparse groups usable without pushing a pair to opposite rack edges. Ten per row gives exactly 21.5 mm pitch and 0.5 mm web. One gives X=0. Five gives X=-96,-48,0,48,96. Rows default to one per U, at `(row + 0.5) × 44.45` mm; this is the existing rack pitch. The plate gap remains 0.05 mm (1U actual plate height 44.4 mm). For fewer rows than U, rows occupy the lowest U centres. Manual nudges are retained until count/rows/height changes regenerate spacing.

## Commands and checks actually run

1. `git pull` → already up to date. Read-only Git status/diff/log checks; final `git diff --check` reported no whitespace errors.
2. `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` **before edits** → all checks passed: 177 Python (1 skipped) and existing JS suite. The first sandboxed attempt stalled on D: permissions; it was interrupted and retried with approved elevation. Its disposable scratch folder `work/gui-refinement/checks-t9iv5v35/` is preserved, not user data. Baseline console output was observed but not separately persisted.
3. `python -B -m unittest discover -s outputs/Mechanical_Design_App -p test_allocation_tray.py -v` → 13 passed at that point (7 existing + 6 panel tests).
4. `node --test-reporter=spec outputs/Mechanical_Design_App/js-tests/faceplate-slot.js` → 3 passed. Registered in js-tests/run.js. Python panel cases are registered through test_allocation_tray.py; no renders in run_checks.
5. Full post-edit run initially exposed the single-row static assertion and LF-normalized manifest hashes/line-ending mismatch. Fixed the assertion and restored each original newline convention. The raw first post-edit output is [checks-after.txt](38-faceplate-only-slot-evidence/checks-after.txt).
6. **Final** `run_checks.ps1`, after the standalone-SCAD part-default fix → **183 Python tests, 1 skipped; 234 JS tests passed; RESULT: all checks passed**. [Full output](38-faceplate-only-slot-evidence/checks-final.txt).
7. PowerShell here-string Python acceptance scripts called `equipment.clean_faceplate`, `render`, `build`, `mesh_revision.read_mesh` and ZIP inspection on a newly created `%TEMP%/aw-task38-*` folder. Final renders verified after the part-default fix. [Results](38-faceplate-only-slot-evidence/render-results.json).
8. Started `python -B outputs/Mechanical_Design_App/app.py --data <new temporary folder> --port 8843`, after checking the port was free. This explicitly seeded only new disposable starter data. HTTP requests exercised placement-check, equipment-preview, equipment-build and faceplate-colors/preview. All returned HTTP 200; both exported ZIPs contained only faceplate.stl. [HTTP results](38-faceplate-only-slot-evidence/http-results.json). This HTTP pass preceded the last part-default/rounded-corner refinement; final direct render and full automated tests cover those refinements. The disposable server was then stopped through its own tool session; no live server was touched.

## Digital acceptance evidence

| Case | Closed mesh volume (mm³) | Result |
| --- | ---: | --- |
| Blank 1U | 43,783.5346219 | One faceplate STL; 4 through-holes; no keystones; nudge 0 |
| Blank 3U | 131,494.7410831 | One faceplate STL; 12 through-holes; no keystones; nudge 0 |
| Reference 10-keystone 1U | 45,023.2954663 | Exact reference bounds and volume; relative error 0%; nudge 0 |
| 2U, two rows of five | 88,878.9021618 | Z=22.225/66.675; no thin-web warning; one faceplate; nudge 0 |

Blank-hole counts were checked by Euler genus of the closed connected meshes (4 and 12); source retains the four-slot loop per U. All meshes passed the existing strict closure/winding/degeneracy checks. The reference file was read only, never regenerated or modified.

Legacy regression: archived-before and current generated SCAD are byte-identical, including a tray with rear support. An actual old tray spec was rendered with both implementations in separate disposable caches: **triangle coordinates are exactly identical**, as are bounds and volumes (tray 26,027.3836195 mm³; faceplate 45,099.5147559 mm³). Raw STL bytes differ only in facet ordering between independent OpenSCAD runs; no geometric tolerance was used for the triangle comparison. Source bytes and source hash inputs are identical. Existing old-document round-trip tests pass; a new two-panel rack round-trips through save/read with independent assembly IDs and no equipment-library write.

Print in color: synthetic image on blank 2U preview is exportable (108 × 27 mm at the tested scale). On the crowded ten-keystone plate the same image is reduced to 2.4 × 0.6 mm and correctly becomes non-exportable (“Only the base color remains”); keep-clear rules were not weakened. Color openings and port-pair row positions are tested.

## Screenshots / remaining acceptance

**No screenshots captured.** A fresh browser-control session has not been started. Permission was requested separately from the scope question; only the cable-ports.js scope reply has arrived. AGENTS.md says: “Ask before a fresh desktop-control session; read applicable computer-use instructions first.” The computer-use SKILL.md, guidance and confirmations were read. Required remaining browser checks: create blank 2U, create ten-keystone 1U, capture thin-wall warning, rack view, Save/reload, Cables rows and Print in color preview, on disposable data only. These are not claimed passed by API or unit tests.

## Open questions / review notes

- Approve the pending disposable-server browser-control request to finish screenshots and visual acceptance, or have Claude perform them. Layout appearance and actual click flow remain unverified.
- Confirm whether 48 mm pitch cap and lower-U placement when fewer rows are requested suit the intended workflow; both are explicit implementation choices.
- Ten tightly packed keystones can leave insufficient area for printable artwork; the current color-preview refusal is intentional under existing keep-clear/minimum-feature rules.
- Review commit 0241508 alongside the working tree because it absorbed initial changes while this session was active. No rollback, commit or push was done here.
- Printed fit, retention and strength remain UNKNOWN. No printing or physical test occurred.

## Files and SHA-256

Byte hashes (not the LF-normalized browser asset digests). Originals are under `docs/archive/codex/2026-10-22/task38/`. Machine-readable list: [files-sha256.json](38-faceplate-only-slot-evidence/files-sha256.json). Paths below are relative to outputs/Mechanical_Design_App/.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `equipment.py` | `bfca6d83c5f503c4e6f8b2bda1068571be092add989ae6ecdb7426eac066d6aa` | `55100bddf7d7a73b6c43ce461f87d4e264292724fc1846914b0334503f99562d` |
| `equipment_tray.scad` | `487e8457ae6f7d6a2021ad2e0a2e8239963be16e0b61ad75e893aa42d2580f10` | `19706d0d016d3d10ac64a7ae85ea7f9f61ac0266de0bc5aaeda156892a5bf9f3` |
| `port-openings.js` | `c0c05da6c416c795084d62037433f2960957b9ab3d951d93b5233fa19de2cbdc` | `66b5451c9917dd57f05829d5fcf433bce5eff2932f3bd7f906784c06a1da7265` |
| `equipment-wizard.js` | `926dbf8f89488afa7afee2216d04bed2528086e88e6a9a0c83cea1948fd7e435` | `5013df477212ca52297b4cdce9b7fd8f9a1e8c4ce0a8584f0a1d9b7e5afa95c4` |
| `tray-placement.js` | `ba61ac468cf13147b88220079fae1d009c02a6bc08802289fe26f9ad81f3d34f` | `e3c0c17284e853793bb7de2399de0b593ea714c353fa7a552be33bab8a3cc8e2` |
| `workspace.js` | `68ec9f5f3e087d7c5773811eb47684dc5bf8c3677ccda56b2366067fe8ad7582` | `a081c7547c4025ff43ab2c2cae742a92b3542649c42eee45f09b9558226f2225` |
| `faceplate_color.py` | `50202871880b8a9716e695726ad9476eb030defaacce43a39b275e4369c30d7d` | `b3f1be400576b4afc4769cd868480d6a2522bdddc805d7eed78b6d2089daac92` |
| `app.py` | `6101ac2437b25004b54b880c35158e859a2a3daac930c28ed7b3e4f985c698a1` | `738a8d576b16477e73ce2e5ae5cf218622afd367e013f33342d836e7dd773075` |
| `asset-manifest.json` | `6a042acacf068c82a143be72127edd9bc964c887b507c91643e88459e6bd67e9` | `b91c4667ba60fe999fdb9cddc7548a371428e596b20270b0b69b4d1b4df374b3` |
| `js-tests/run.js` | `148bfa6461185bdc3f4261138ef89714b434df73215f4b0c1f696468c7c310f2` | `157999f74a72df38e58020797f955b217b21b453ebbbf12e43075c24a4fb4330` |
| `test_allocation_tray.py` | `9b07285b733098c6bf22ab654de1317f28cc8125663653a47c8b0d5a32a93a41` | `0b872be2f8a14191d81a42dedb615ca04b7a64adc260b5ba30f302f0fe100f47` |
| `cable-ports.js` | `757f88a0c1d54ce01752eb181f28336262f7508bd8fc773f2191db45827c2782` | `74d17f28260f1356b86b9fba8568719d63770d2b9d84a64a9a1fa80dd925fec5` |
| `test_keystone_mesh.py` | `89889dba05aa7ab86488af47f57f7a5f935bf3c28f3c10bfd8b20b90ad3ae46d` | `c70033ca30f19d3f2fa4096f2c203a76b32506e56b992b8ffc3039adc53afff1` |
| `test_faceplate_slot.py` | `NEW` | `ae7dc23593761d57f0e1a0240aea20d1ea492f7915a71860aafd3f5c7523f446` |
| `js-tests/faceplate-slot.js` | `NEW` | `efc47f5285ffee2d2f3cc2d4d6ed5d188621b8ee7790d43f772d026264100095` |

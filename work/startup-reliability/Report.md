# Startup reliability repair — 2026-10-18

## Cause and comparison

The disposable diagnostic page caught resource-load failures for workspace.js, rack-reference.js and viewer.js when #studio was absent. Earlier scripts loaded. The failed script requests never reached the HTTP handler log; this was delivery failure, not a GUI reconstruction or a thrown workspace exception.

Python3.10 ThreadingHTTPServer inherits a five-connection listen backlog. Startup and reload issue bursts of scripts, APIs and source-mesh requests. With the original queue, the browser failed on reload2. Changing only the diagnostic server queue to64 gave10 consecutive successful reloads with all8 scripts loaded. An independent controlled24-connection burst before accepting requests connected9/24 with the original server versus24/24 with the new server. These observations support backlog saturation as the cause of the reproduced failure; they do not promise immunity to arbitrary network/browser failure.

## Change

app.py now defines WorkshopHTTPServer with request_queue_size64, used by the real main entry point. No client script bundling, retries, external dependencies or renderer changes. The canonical embedded stylesheet repair remains.

Response writes now quietly end when reload/navigation closes the connection (broken pipe/reset/abort), rather than trying to write another HTTP error after the original headers or misreporting an integrity failure. Actual manifest mismatches still follow the existing409 path. All renderer assets and the locked original rack-scene.js were untouched.

## Verification

- New test_startup.py:3 tests PASS. Controlled backlog comparison;72 parallel startup HTTP requests with200/no-store and correct document CSS;6 cancelled-response cases covering headers/body and three connection exceptions, with no second response.
- Final browser fixture uses the production WorkshopHTTPServer class and fresh temporary data.20 consecutive reloads PASS:all8 scripts report loaded, hybrid grid present, no captured startup errors. Browser_Checks.json records before/after observations.
- Actual source-mesh renderer finished at115654 triangles in the empty disposable rack. Appearance/Setup navigation and inspector collapse/restore PASS; one disabled Save, no duplicate IDs. Verified_Startup.png records this.
- Existing focused CSS regression tests PASS again, including20 root deliveries, live CSS reread and missing-CSS error behavior. Data/locked-asset check PASS after activation:all16 files across data/normal-use and outputs/Mechanical_Design_App/data retain their pre-repair hashes.
- Active user tab checked before reload:Saved locally, Save disabled, empty hardware dirty status, no open dialog, wizard hidden. Restarted only verified PID26616; new main listener PID20944. Kept --existing-library and the already active outputs/Mechanical_Design_App/data folder (NOT a data migration to data/normal-use). Startup log:6 revisions,0 starter imports. Reloaded same tab and restored its selected Slot1. Rack source renderer138494 triangles, dark hybrid visible, no warning/error browser logs. Normal_Startup_Verified.png records the result.

The separate8767 listener was untouched; disposable8770 tab closed and test server stopped. No normal data save, manufacturing geometry generation/export, physical work, uploads, publishing or pushes. Source backups and diagnostics remain local in this folder. Phase7 and all physical/manufacturing limitations are unchanged. This supersedes the unresolved startup finding in the preceding persistence test report.

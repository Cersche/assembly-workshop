# Task 55 — Workshop Bench five features

2026-11-08. Implemented in `D:\Projects\assembly-workshop` on main. Initial `git pull` reported `Already up to date.` No commit or push. Existing unrelated changes were preserved. No HANDOFF/PROJECT/ROADMAP changes, original viewer/3MF changes, geometry work or acceptance server against the real root. Port 8720 was not contacted or stopped.

**All five features are implemented and the final browser acceptance passes at 1280 and 375 pixels.** The final Python suite passes three consecutive runs. Cancel and Discard were tested using Brian's explicitly authorized in-memory `window.confirm` overrides, not real native-dialog clicks. The report below identifies that distinction and preserves the earlier tool limitation as history.

## Files and feature-order checks

| Feature | Files changed (relative to tools/bench/) | Suite before starting the next feature |
| --- | --- | --- |
| 1. Solo part | bench.py, static/viewer-bridge.js, static/bench.js, static/bench.css, test_bench.py | 173 tests, OK |
| 2. Open 3D in new tab | static/bench.js, test_bench.py | 174 tests, OK |
| 3. Edit job details | bench.py, static/bench.js, test_bench.py | 181 tests, OK |
| 4. Quick status | static/bench.js, test_bench.py | 182 tests, OK |
| 5. Print queue | bench.py, static/index.html, static/bench.js, test_bench.py | 185 tests, OK |

README.md documents Use, HTTP fields, queue, served-only bridge and the operator harness. Other additions under tools/bench/ are task55-* operator evidence plus task55-browser-acceptance.cjs. Nothing imports or serves the harness/logs. The existing task-54 acceptance.py was not changed or run as a whole; its copy_metadata helper prepared the disposable metadata root.

Final browser verification surfaced a favicon 404. A self-contained data-SVG favicon was added to static/index.html; it uses the existing CSP, adds no route/file/dependency, and removes that unexpected console error. Final review also corrected multi-path textarea newlines and rejects sparse part-name arrays. These final source changes are included in the three final Python runs and both complete browser runs.

## Implementation and tests

The installation bridge is inserted exactly once into the served response before the last closing body tag (case insensitive), or at EOF. The disk page is untouched and there is no bridge route. Viewer CSP is byte-for-byte the original policy. The bridge reads part labels, accepts only its parent, changes the existing checkboxes, fires change and clicks reset to re-frame visible parts. The parent checks the current iframe window and the exact two-key payload, at most 200 string names of at most 200 characters, rejects sparse holes, and escapes displayed names. Unknown solo names do nothing. Standalone hash soloing works without a Referer.

Detail PATCH shares title/prefix/path validation with create, permits own prefixes while rejecting other-job duplicates/overlap, rejects ID/unknown fields and empty changes, validates exact workflow section titles (including continued-only sections), updates the date and invalidates the scan cache. The following state request rescans. Only projects.json and its backup change. Independent dirty forms survive another form's successful save. Quick buttons send status only, and notes/details edits disable them with the requested hint. The original dropdown and Save remain.

Queue is computed read-only during scanning: printing/report-due only, updated ascending then ID for ties, newest released ID or null, and printing overdue strictly after three days. Its view selection is remembered when localStorage is available.

Python 3.10.4 on Windows; server source also passed Python-3.10 syntax parsing. Final `git diff --check -- tools/bench` passes. The application remains standard-library Python and plain HTML/CSS/JS with no new dependencies, network-client, subprocess/git/render/release functionality or write targets. Write/backup/rollback/hash/append-only machinery and the viewer CSP were not altered.

Added unittest coverage includes bridge order/exactly-once/disk unchanged/exact CSP/EOF/standalone/path safety; editing every field, own-prefix acceptance, duplicates/overlaps, file constraints, fixed ID, workflow titles, staleness and write boundaries; status-only preservation; fixed-date queue order/status/days/overdue/latest-null/ties and HTTP state queue. Existing tests remain passing.

Final command, three runs in a row:

```text
python -m unittest tools/bench/test_bench.py -v
```

- Run 1: 185 tests in 6.593s, OK.
- Run 2: 185 tests in 6.099s, OK.
- Run 3: 185 tests in 6.106s, OK.

Full outputs for these final runs and each sequential feature suite follow later in this report.

## Temporary acceptance and browser method

```text
python -B tools/bench/bench.py --root C:\Users\brian\AppData\Local\Temp\bench55-rgkt7o4_ --port 8875
node work/codex-tasks/55-evidence/task55-browser-acceptance.cjs
```

Metadata copy contains real docs/catalog/workflow and output text/listings, with empty 3MF placeholders rather than original 3MF bytes. Most viewer names are simple fixtures; TF-D.html and TF-D_second.html in the temp root copy the real four-part TF-D page as task 55 requires. Linked sources were copied locally for path validation and never executed. Fake jobs exercise every status, overdue/no-release queue cases, and empty queue. All mutations, stale-file simulation and fit-report appends targeted the disposable root. The browser harness restores the temporary catalog after each complete run (and in its finally cleanup).

Initial in-app-browser checks exercised desktop solo/new-tab/edit/status/queue paths but stalled on a native unsaved-edit prompt. The tool's getJsDialog returned undefined, and recovery attempts could not resume input. Brian then explicitly authorized `window.confirm = () => false` / `true` plus a dismissing native-dialog handler. The in-app browser's evaluation API rejects assignments (`Cannot add property confirm, object is not extensible`), so the requested overrides were run using the already installed Playwright runtime and Chrome in a separate headless browser with fresh contexts and no user profile. No packages were installed. This is an operator-only test dependency, not an application dependency.

At **each** viewport, 1280 x 900 and 375 x 900, the final harness verified:

1. Real TF-D viewer: All parts initially checked; TF-D_grille solo gives [false,false,false,true], pressed state and encoded link; All parts restores [true,true,true,true]. Screenshots show the resulting framing. Changing chooser resets solo and link; changing revision resets/hides part controls for a no-list fixture; missing viewer hides the new-tab link.
2. Clicking Open 3D in new tab opens the expected #solo URL and leaves only the named part checked in the standalone sandboxed viewer; separate screenshot at each width.
3. Details: ID fixed, title/prefixes/cards/sources/workflow saved; two-card/two-source prefill contains actual newlines and re-saves correctly. Dirty details and notes disable quick status. Saving details preserves independent unsaved notes and does not persist them. Cancel notes restores saved text. Stale details returns 409, rescans, keeps the typed title, and succeeds only on explicit retry.
4. Every table status action (idea, measuring, draft, printing, report-due, done, parked) saves the expected status and preserves notes. Write fit report selects the newest release without status mutation; no-release case leaves an empty revision with its explanation. Status-only 409 leaves status unchanged; a deliberate retry succeeds.
5. Queue: rendered IDs/order match /api/state.queue; overdue printing and no-release text appear; clicking a row opens the job; a clean reload remembers Print queue. Clearing all disposable printing/report-due statuses gives the exact empty message.
6. DOM innerWidth and document scrollWidth equal the requested 1280 or 375 at every saved screenshot; no horizontal page overflow. No unexpected console errors or script exceptions at either width.

### Confirm-path disclosure

At each width, details Cancel and Discard and notes Cancel and Discard were tested through an in-memory override installed before page scripts. It counted calls and returned the chosen false/true value. Cancel preserved the current job and typed text; Discard navigated and dropped the unsaved draft. **None of those paths were tested by clicking a real native browser confirmation.** Each page also had `page.on('dialog', d => d.dismiss())` as backup; it was never needed (zero native dialogs). Clean reloads avoided native beforeunload prompts. Browser/tab-close warning appearance itself was not re-tested.

The two deliberately induced stale saves per width naturally produce Chromium HTTP-resource console messages for status 409. They are recorded as expected negative-test evidence (exactly two per viewport). All other console errors and page exceptions fail the harness; there were none. The earlier favicon 404 was fixed, not suppressed. The first harness draft also needed a narrower heading selector because device-card markdown contains headings; that was a harness selector fix, not an app failure.

## Screenshots

Final Playwright captures are PNGs at exactly 1280 x 900 or 375 x 900. Each has a matching DOM width/overflow assertion:

- `work/codex-tasks/55-screens/1280-solo.png`
- `work/codex-tasks/55-screens/1280-standalone.png`
- `work/codex-tasks/55-screens/1280-all-parts.png`
- `work/codex-tasks/55-screens/1280-details.png`
- `work/codex-tasks/55-screens/1280-stale-details.png`
- `work/codex-tasks/55-screens/1280-fit-report.png`
- `work/codex-tasks/55-screens/1280-queue.png`
- `work/codex-tasks/55-screens/1280-empty-queue.png`
- `work/codex-tasks/55-screens/375-solo.png`
- `work/codex-tasks/55-screens/375-standalone.png`
- `work/codex-tasks/55-screens/375-all-parts.png`
- `work/codex-tasks/55-screens/375-details.png`
- `work/codex-tasks/55-screens/375-stale-details.png`
- `work/codex-tasks/55-screens/375-fit-report.png`
- `work/codex-tasks/55-screens/375-queue.png`
- `work/codex-tasks/55-screens/375-empty-queue.png`

Earlier retained JPEGs 1280-layout.jpg, 375-layout.jpg and standalone-solo.jpg are historical captures from the initial in-app attempt; the standalone bitmap is 447 x 932 and does not claim a 1280 viewport. Several other initial temporary screenshots were lost on tool reset. The sixteen PNGs above supersede that incomplete evidence and were visually inspected for desktop queue, mobile details and mobile solo layout.

## What remains unverified and decisions to review

The requested feature click-through is now complete at both widths. Native warning appearance/dismissal is not re-certified: the authorized confirm overrides tested application Cancel/Discard behavior, and the backup handler saw no native dialogs. Private/incognito/storage-denied behavior was not separately exercised; all localStorage calls retain try/catch. Full keyboard-only interaction and light mode were not re-tested in task 55. Physical fit/strength remain UNKNOWN; no geometry work was authorized or performed.

Routine choices for Claude's review: workflow section cap 300 characters; queue ties by ID; queue ignores search/status filters and disables them while showing the complete queue; no-release Write fit report leaves revision blank with an explanation; successful saves preserve other dirty forms. These require no new user decision before review. No commit/push occurred.

Both the original and resumed acceptance status snapshots match within their before/after pairs, and all four specified hashes match the original baseline. The resumed status has two additional operator-evidence paths prepared before its baseline (browser harness/results); these are authorized additions under tools/bench, not acceptance writes to user data. Full resumed snapshots and browser output are included below. Equality of git status means path/status equality, not source-byte identity; implementation edits are intentional.

## Resumed complete browser output

```json
[
  {
    "label": "1280 solo",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 all-parts",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 details",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 confirm Cancel/Discard",
    "value": {
      "calls": 2,
      "method": "window.confirm override; no native click"
    }
  },
  {
    "label": "1280 stale-details",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 quick idea",
    "value": "draft"
  },
  {
    "label": "1280 quick measuring",
    "value": "draft"
  },
  {
    "label": "1280 quick draft",
    "value": "printing"
  },
  {
    "label": "1280 quick printing",
    "value": "report-due"
  },
  {
    "label": "1280 fit-report",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 quick report-due",
    "value": "done"
  },
  {
    "label": "1280 quick done",
    "value": "draft"
  },
  {
    "label": "1280 quick parked",
    "value": "draft"
  },
  {
    "label": "1280 queue",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 queue remembers view",
    "value": true
  },
  {
    "label": "1280 empty-queue",
    "value": {
      "width": 1280,
      "documentWidth": 1280
    }
  },
  {
    "label": "1280 deliberately expected HTTP 409 logs",
    "value": [
      "Failed to load resource: the server responded with a status of 409 (Conflict)",
      "Failed to load resource: the server responded with a status of 409 (Conflict)"
    ]
  },
  {
    "label": "1280 browser errors",
    "value": []
  },
  {
    "label": "1280 native fallback dialogs",
    "value": []
  },
  {
    "label": "375 solo",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 all-parts",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 details",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 confirm Cancel/Discard",
    "value": {
      "calls": 2,
      "method": "window.confirm override; no native click"
    }
  },
  {
    "label": "375 stale-details",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 quick idea",
    "value": "draft"
  },
  {
    "label": "375 quick measuring",
    "value": "draft"
  },
  {
    "label": "375 quick draft",
    "value": "printing"
  },
  {
    "label": "375 quick printing",
    "value": "report-due"
  },
  {
    "label": "375 fit-report",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 quick report-due",
    "value": "done"
  },
  {
    "label": "375 quick done",
    "value": "draft"
  },
  {
    "label": "375 quick parked",
    "value": "draft"
  },
  {
    "label": "375 queue",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 queue remembers view",
    "value": true
  },
  {
    "label": "375 empty-queue",
    "value": {
      "width": 375,
      "documentWidth": 375
    }
  },
  {
    "label": "375 deliberately expected HTTP 409 logs",
    "value": [
      "Failed to load resource: the server responded with a status of 409 (Conflict)",
      "Failed to load resource: the server responded with a status of 409 (Conflict)"
    ]
  },
  {
    "label": "375 browser errors",
    "value": []
  },
  {
    "label": "375 native fallback dialogs",
    "value": []
  },
  {
    "label": "RESULT",
    "value": "PASS"
  }
]
```

## Resumed git status --short — Before

```text
 M IDEAS.md
 M docs/devices/bridgelink-2way-splitter.md
 M outputs/Final_3MF/CM6A_CM1000_M6_bracket_set.3mf
 M tools/bench/README.md
 M tools/bench/bench.py
 M tools/bench/static/bench.css
 M tools/bench/static/bench.js
 M tools/bench/static/index.html
 M tools/bench/test_bench.py
 M work/equipment-models/power_strip/power_strip.scad
 M work/equipment-models/power_strip/power_strip.stl
 M work/moca-rack-tray/MRT.scad
 M work/screen-5in/Dimensions.md
?? outputs/Final_3MF/CHS-A_chess_clock_switch_set.3mf
?? outputs/Final_3MF/SCR5-J4_screen_pi_hue_3port_set.3mf
?? outputs/Final_3MF/WMB-A_flat_wire_bracket.3mf
?? outputs/Screen_Pi_Hue_SCR5-J3_2026-11-03/
?? outputs/Screen_Pi_Hue_SCR5-J4_2026-11-03/
?? rwm1.scad
?? tools/bench/static/viewer-bridge.js
?? work/codex-tasks/55-evidence/task55-after.json
?? work/codex-tasks/55-evidence/task55-before.json
?? work/codex-tasks/55-evidence/task55-browser-acceptance.cjs
?? work/codex-tasks/55-evidence/task55-browser-results.json
?? work/codex-tasks/55-evidence/task55-feature1-tests.txt
?? work/codex-tasks/55-evidence/task55-feature2-tests.txt
?? work/codex-tasks/55-evidence/task55-feature3-tests.txt
?? work/codex-tasks/55-evidence/task55-feature4-tests.txt
?? work/codex-tasks/55-evidence/task55-feature5-tests.txt
?? work/codex-tasks/55-evidence/task55-resumed-browser.json
?? work/codex-tasks/55-evidence/task55-run-1.txt
?? work/codex-tasks/55-evidence/task55-run-2.txt
?? work/codex-tasks/55-evidence/task55-run-3.txt
?? work/codex-tasks/55-evidence/task55-temp-root.txt
?? work/chess-clock-switch/
?? work/cm1000-diffuser/parts/
?? work/codex-tasks/55-bench-five-features-REPORT.md
?? work/codex-tasks/55-screens/
?? work/fan-junction-box/concept_stl/
?? work/fan-junction-box/draft_stl/
?? work/fan-junction-box/draft_stl_B/
?? work/gene-success/dishes.png
?? work/mesh-viewer/CBL-A-E_rear_lane_set.html
?? work/mesh-viewer/CBL-A_rear_lane.html
?? work/mesh-viewer/CHS-A_chess_clock_assembled.html
?? work/mesh-viewer/CM1000_1U_Mount_on_modem.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.png
?? work/mesh-viewer/CM1000_icon_stroke_check.png
?? work/mesh-viewer/CM1000_modem_as_understood.html
?? work/mesh-viewer/CM1000_modem_understood_v2.html
?? work/mesh-viewer/CM1000_underside_measure.png
?? work/mesh-viewer/CM1P-A_one_piece_bracket.html
?? work/mesh-viewer/CM1P-B_skeleton_rails.html
?? work/mesh-viewer/CM1P-C_fitment_draft.html
?? work/mesh-viewer/CM1P-D_fitment_draft.html
?? work/mesh-viewer/CM1P-E_clearance.png
?? work/mesh-viewer/CM1P-E_one_piece_bracket.html
?? work/mesh-viewer/CM1P-F_changes.png
?? work/mesh-viewer/CM1P-F_one_piece_bracket.html
?? work/mesh-viewer/CM1P-G_one_piece_bracket.html
?? work/mesh-viewer/CM1P-H_one_piece_bracket.html
?? work/mesh-viewer/CM1P-I_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_front_slope.png
?? work/mesh-viewer/CM1P-J_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_with_modem_see_through.html
?? work/mesh-viewer/CM1P-K_V_section.png
?? work/mesh-viewer/CM1P-K_front_section.png
?? work/mesh-viewer/CM1P-K_print_part.html
?? work/mesh-viewer/CM1P-K_tip_width_measure.png
?? work/mesh-viewer/CM1P-K_with_modem_see_through.html
?? work/mesh-viewer/CM1P-L_screw_at_80.png
?? work/mesh-viewer/CM1P-L_slot_move.png
?? work/mesh-viewer/CM1P-L_with_modem_see_through.html
?? work/mesh-viewer/CM1P-M_slot.png
?? work/mesh-viewer/CM1P-M_with_modem_see_through.html
?? work/mesh-viewer/CM1P-N_with_modem_see_through.html
?? work/mesh-viewer/CM1P-O_pipe_vs_earlier.png
?? work/mesh-viewer/CM1P-O_seated_section.png
?? work/mesh-viewer/CM1P-O_with_modem_see_through.html
?? work/mesh-viewer/CM1P-P_and_modem.html
?? work/mesh-viewer/CM1P-P_icon_options.png
?? work/mesh-viewer/CM1P-P_light_distance.png
?? work/mesh-viewer/CM1P-P_lip_vs_top_edge.png
?? work/mesh-viewer/CM1P-P_logos_now.png
?? work/mesh-viewer/CM1P-P_print_part.html
?? work/mesh-viewer/CM1P-P_vs_forward_2.5_preview.html
?? work/mesh-viewer/CM1P-P_with_modem_see_through.html
?? work/mesh-viewer/CM1P-Q_with_modem.html
?? work/mesh-viewer/CM1P-T1_test_slice.html
?? work/mesh-viewer/CM1P-T2_test_slice.html
?? work/mesh-viewer/CM1P-T3_test_slice.html
?? work/mesh-viewer/CM1P-T4_test_slice.html
?? work/mesh-viewer/CM1P-T5_holes.png
?? work/mesh-viewer/CM1P-T5_on_modem.html
?? work/mesh-viewer/CM1P-T5_print_parts.html
?? work/mesh-viewer/CM1P-T6_on_modem.html
?? work/mesh-viewer/CM1P-T7_on_modem.html
?? work/mesh-viewer/CM1P-T8_look.png
?? work/mesh-viewer/CM1P-T8_look_cups.png
?? work/mesh-viewer/CM1P-T8_on_modem.html
?? work/mesh-viewer/CM1P-T8_print.html
?? work/mesh-viewer/CM1P-diffuser_option_A.png
?? work/mesh-viewer/CM1P-diffuser_option_B.png
?? work/mesh-viewer/CM1P-diffuser_option_C.png
?? work/mesh-viewer/CM1P-diffuser_options.html
?? work/mesh-viewer/CM6A_CM1000_M6.html
?? work/mesh-viewer/CM6A_fitment_review.html
?? work/mesh-viewer/CM6A_review.html
?? work/mesh-viewer/CM6A_vs_CM6B_rev2.html
?? work/mesh-viewer/CM6B_rev3.html
?? work/mesh-viewer/CM6C_assembled.html
?? work/mesh-viewer/CM6C_print_set.html
?? work/mesh-viewer/CRN-A_proposal.html
?? work/mesh-viewer/CRN-B_proposal.html
?? work/mesh-viewer/CRN-C_proposal.html
?? work/mesh-viewer/CRN-D_concept.html
?? work/mesh-viewer/CRN-E_concept.html
?? work/mesh-viewer/CSB-A.html
?? work/mesh-viewer/CSB-B.html
?? work/mesh-viewer/CSB-B_draft_tool_window.html
?? work/mesh-viewer/CSB-B_draft_zip_ties.html
?? work/mesh-viewer/CSB-C.html
?? work/mesh-viewer/CSB-C_draft.html
?? work/mesh-viewer/Cable_Span_concept.html
?? work/mesh-viewer/Cable_Span_styles.html
?? work/mesh-viewer/ER6-A_vs_source.html
?? work/mesh-viewer/ER6-B_with_router.html
?? work/mesh-viewer/ER6-C_with_router.html
?? work/mesh-viewer/ER6-D_with_router.html
?? work/mesh-viewer/ER6-E_with_router.html
?? work/mesh-viewer/ER6-F_with_router.html
?? work/mesh-viewer/ER6-G_with_router.html
?? work/mesh-viewer/ER6-H_with_router.html
?? work/mesh-viewer/HDT-M6-A_mockup.html
?? work/mesh-viewer/HP4-M6-A.html
?? work/mesh-viewer/HP4-M6-A_assembled.html
?? work/mesh-viewer/HP4-M6-A_baseline.html
?? work/mesh-viewer/HP4-M6-A_print-layout.html
?? work/mesh-viewer/HP4-M6-B.html
?? work/mesh-viewer/JB_draft1_junction_box.html
?? work/mesh-viewer/JB_draft2_box_closeup.html
?? work/mesh-viewer/JB_optionB_closeup.html
?? work/mesh-viewer/JB_optionB_in_rack.html
?? work/mesh-viewer/JB_placement_concept.html
?? work/mesh-viewer/Library_plate_and_SG8_tray.html
?? work/mesh-viewer/M6_generator_HDT.html
?? work/mesh-viewer/MRT-A_moca_tray_mockup.html
?? work/mesh-viewer/MRT-B_moca_tray_braces.html
?? work/mesh-viewer/MRT-B_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-C_moca_tray.html
?? work/mesh-viewer/MRT-C_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-D_moca_tray.html
?? work/mesh-viewer/MRT-D_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-E_tray_plate_and_test_prints.html
?? work/mesh-viewer/MRT-F.html
?? work/mesh-viewer/MRT-F_covers_and_jig.html
?? work/mesh-viewer/MRT-F_release_test.3mf
?? work/mesh-viewer/MRT-F_release_test.html
?? work/mesh-viewer/MRT-G.html
?? work/mesh-viewer/MRT-H.html
?? work/mesh-viewer/MRT-H_T5-T7_print_set.html
?? work/mesh-viewer/MRT-H_draft1_walls_keystones.html
?? work/mesh-viewer/MRT-H_draft2_ramps.html
?? work/mesh-viewer/MRT-I_draft1.html
?? work/mesh-viewer/MRT-T4.html
?? work/mesh-viewer/MRT-T4_fit_report.html
?? work/mesh-viewer/MRT-T5-T7_coax_jigs.html
?? work/mesh-viewer/MRT-T5.html
?? work/mesh-viewer/MRT_splitter_coax_review.html
?? work/mesh-viewer/MoCA_RX1_concept.html
?? work/mesh-viewer/MoCA_RX2_bones.html
?? work/mesh-viewer/MoCA_RX3_bones.html
?? work/mesh-viewer/MoCA_RX4-C_tabs.html
?? work/mesh-viewer/MoCA_RX4_bones.html
?? work/mesh-viewer/MoCA_sleeve_rev3.html
?? work/mesh-viewer/MoCA_wall_cleat_seated.html
?? work/mesh-viewer/MoCA_wall_cleat_set.html
?? work/mesh-viewer/OPX-A_concept.html
?? work/mesh-viewer/OPX-A_print_set.html
?? work/mesh-viewer/OPX-B_assembled.html
?? work/mesh-viewer/OPX-C_assembled.html
?? work/mesh-viewer/OPX-D_assembled.html
?? work/mesh-viewer/OPX-D_concept.html
?? work/mesh-viewer/OPX-D_print_set.html
?? work/mesh-viewer/OPX-E_assembled.html
?? work/mesh-viewer/OPX-E_rails_print.html
?? work/mesh-viewer/OPX-F_assembled.html
?? work/mesh-viewer/OPX-F_rails_print.html
?? work/mesh-viewer/OPX-G_assembled.html
?? work/mesh-viewer/OPX-G_channels_print.html
?? work/mesh-viewer/OpenSCAD_old_vs_snapshot.html
?? work/mesh-viewer/OptiPlex_reference_brackets.html
?? work/mesh-viewer/PHX-A_post_hex_concept.html
?? work/mesh-viewer/PHX-B_post_hex_chamfer.html
?? work/mesh-viewer/PHX-C_blank_assembled.html
?? work/mesh-viewer/PSB-A_assembled.html
?? work/mesh-viewer/PSB-A_print_set.html
?? work/mesh-viewer/Power_strip_as_understood.html
?? work/mesh-viewer/RW_rack_wall_mount_print.html
?? work/mesh-viewer/RW_rack_wall_mount_seated.html
?? work/mesh-viewer/RX4-A_print_set.html
?? work/mesh-viewer/RX4-B_print_set.html
?? work/mesh-viewer/RX4-C_print_set.html
?? work/mesh-viewer/RX5-A_print_set.html
?? work/mesh-viewer/RX5-B_assembled.html
?? work/mesh-viewer/RX5-B_print_set.html
?? work/mesh-viewer/RX5_rear_ports_issue.html
?? work/mesh-viewer/RX5_rear_ports_rev2.html
?? work/mesh-viewer/Rack_B_mock_wiring.html
?? work/mesh-viewer/Rack_custom_9U.html
?? work/mesh-viewer/Rack_frame_9U_concept.html
?? work/mesh-viewer/Rack_frame_A_vs_B.html
?? work/mesh-viewer/Rack_order_B.html
?? work/mesh-viewer/Rack_top_fan_TF-B_full_rack.html
?? work/mesh-viewer/Rack_top_fan_draft4_assembled.html
?? work/mesh-viewer/Rack_top_fan_draft4_full_rack_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_draft_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_task53_print_parts.html
?? work/mesh-viewer/SCR5-AP_1_fronts.png
?? work/mesh-viewer/SCR5-AP_2_overview.png
?? work/mesh-viewer/SCR5-AP_3_pi_on_screen.png
?? work/mesh-viewer/SCR5-AP_4_side_cut.png
?? work/mesh-viewer/SCR5-AP_5_joints.png
?? work/mesh-viewer/SCR5-AP_C_top_row.png
?? work/mesh-viewer/SCR5-AP_D_bottom_row.png
?? work/mesh-viewer/SCR5-AP_layout_A.html
?? work/mesh-viewer/SCR5-AP_layout_B.html
?? work/mesh-viewer/SCR5-AP_layout_C.html
?? work/mesh-viewer/SCR5-AP_layout_D.html
?? work/mesh-viewer/SCR5-A_review.html
?? work/mesh-viewer/SCR5-B_review.html
?? work/mesh-viewer/SCR5-C_assembled.html
?? work/mesh-viewer/SCR5-D_assembled.html
?? work/mesh-viewer/SCR5-E_app_placeholder_check.html
?? work/mesh-viewer/SCR5-E_assembled.html
?? work/mesh-viewer/SCR5-E_on_posts.html
?? work/mesh-viewer/SCR5-F_on_posts.html
?? work/mesh-viewer/SCR5-G_review.html
?? work/mesh-viewer/SCR5-H10_assembled.html
?? work/mesh-viewer/SCR5-H10_low_joint.png
?? work/mesh-viewer/SCR5-H11_assembled.html
?? work/mesh-viewer/SCR5-H11_rails_and_fan_mount.png
?? work/mesh-viewer/SCR5-H7.html
?? work/mesh-viewer/SCR5-H8.html
?? work/mesh-viewer/SCR5-H8_assembled.html
?? work/mesh-viewer/SCR5-H8_sag_section.png
?? work/mesh-viewer/SCR5-H9_assembled.html
?? work/mesh-viewer/SCR5-H9_tray.png
?? work/mesh-viewer/SCR5-H_review.html
?? work/mesh-viewer/SCR5-J1_assembled.html
?? work/mesh-viewer/SCR5-J1_hue_cradle.png
?? work/mesh-viewer/SCR5-J1_no_cradle.html
?? work/mesh-viewer/SCR5-J1_views.png
?? work/mesh-viewer/SCR5-J2_assembled.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.png
?? work/mesh-viewer/SCR5-J2_bevel_options.png
?? work/mesh-viewer/SCR5-J2_cutout_as_built.html
?? work/mesh-viewer/SCR5-J2_cutout_as_built.png
?? work/mesh-viewer/SCR5-J2_print_set.html
?? work/mesh-viewer/SCR5-J2_views.png
?? work/mesh-viewer/SCR5-J3_front_frame.html
?? work/mesh-viewer/SCR5-J3_views.png
?? work/mesh-viewer/SCR5-J3_views2.png
?? work/mesh-viewer/SCR5-J4_front.png
?? work/mesh-viewer/SCR5-J4_front_frame.html
?? work/mesh-viewer/SCR5-J4_print_set.html
?? work/mesh-viewer/SCR5-J4_views.png
?? work/mesh-viewer/SCR5-J5_tray_vs_J4.html
?? work/mesh-viewer/SCR5-WP-A_coupon.html
?? work/mesh-viewer/SCR5-swap_3d_C.png
?? work/mesh-viewer/SCR5-swap_3d_H11.png
?? work/mesh-viewer/SCR5-swap_3d_N.png
?? work/mesh-viewer/SCR5-swap_3d_N2.png
?? work/mesh-viewer/SCR5-swap_3d_S1.png
?? work/mesh-viewer/SCR5-swap_3d_S2.png
?? work/mesh-viewer/SCR5-swap_3d_S3.png
?? work/mesh-viewer/SCR5-swap_S3.html
?? work/mesh-viewer/SCR5-swap_S3.png
?? work/mesh-viewer/SCR5-swap_no_keystone.html
?? work/mesh-viewer/SCR5-swap_no_keystone.png
?? work/mesh-viewer/SCR5-swap_options.html
?? work/mesh-viewer/SCR5-swap_plate_fronts.png
?? work/mesh-viewer/SCR5-swap_side_cuts.png
?? work/mesh-viewer/SCR5_border_measure.png
?? work/mesh-viewer/SCR5_frame_rounded_draft.html
?? work/mesh-viewer/SCR5_frame_rounded_draft.png
?? work/mesh-viewer/SG8-C1_coupon.html
?? work/mesh-viewer/SG8-C1_coupon_assembled.html
?? work/mesh-viewer/SG8-C2_boss.html
?? work/mesh-viewer/SG8-M6-A_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_screws_fastened.html
?? work/mesh-viewer/SG8-M6-C_tray.html
?? work/mesh-viewer/SG8-M6-D.html
?? work/mesh-viewer/SG8-M6-E_faceplate_on_D_tray.html
?? work/mesh-viewer/SG8-M6-F_on_posts_LOCAL-ONLY.html
?? work/mesh-viewer/SG8-M6-F_post_cheeks.html
?? work/mesh-viewer/SG8-PB-A_post_brackets.html
?? work/mesh-viewer/SG8_B-plate_on_D-tray.html
?? work/mesh-viewer/TF-A.html
?? work/mesh-viewer/TF-B.html
?? work/mesh-viewer/TF-C.html
?? work/mesh-viewer/TF-D.html
?? work/mesh-viewer/TF-D_draft1.html
?? work/mesh-viewer/WMB-A_vs_original.html
?? work/mesh-viewer/faceplate_baseline_vs_CM6B.html
?? work/mesh-viewer/optiplex_rear_R_vs_O.html
?? work/mesh-viewer/printed_brackets_review_2026-10-28.html
?? work/mesh-viewer/task46-reference-regression.html
?? work/rack-finish/Rack_Finish_3D.html
?? work/rack-plan/Rack_B_Wiring_2026-11-04.png
?? work/rack-plan/Rack_Order_Options_2026-11-04.png
?? work/rack-post-hex/
?? work/rack-top-fan/draft_D/
?? work/scr5-access/png/
?? work/scr5-access/stl/
?? work/scr5-swap/stl/
?? work/wire-bracket/
```

## Resumed git status --short — After

```text
 M IDEAS.md
 M docs/devices/bridgelink-2way-splitter.md
 M outputs/Final_3MF/CM6A_CM1000_M6_bracket_set.3mf
 M tools/bench/README.md
 M tools/bench/bench.py
 M tools/bench/static/bench.css
 M tools/bench/static/bench.js
 M tools/bench/static/index.html
 M tools/bench/test_bench.py
 M work/equipment-models/power_strip/power_strip.scad
 M work/equipment-models/power_strip/power_strip.stl
 M work/moca-rack-tray/MRT.scad
 M work/screen-5in/Dimensions.md
?? outputs/Final_3MF/CHS-A_chess_clock_switch_set.3mf
?? outputs/Final_3MF/SCR5-J4_screen_pi_hue_3port_set.3mf
?? outputs/Final_3MF/WMB-A_flat_wire_bracket.3mf
?? outputs/Screen_Pi_Hue_SCR5-J3_2026-11-03/
?? outputs/Screen_Pi_Hue_SCR5-J4_2026-11-03/
?? rwm1.scad
?? tools/bench/static/viewer-bridge.js
?? work/codex-tasks/55-evidence/task55-after.json
?? work/codex-tasks/55-evidence/task55-before.json
?? work/codex-tasks/55-evidence/task55-browser-acceptance.cjs
?? work/codex-tasks/55-evidence/task55-browser-results.json
?? work/codex-tasks/55-evidence/task55-feature1-tests.txt
?? work/codex-tasks/55-evidence/task55-feature2-tests.txt
?? work/codex-tasks/55-evidence/task55-feature3-tests.txt
?? work/codex-tasks/55-evidence/task55-feature4-tests.txt
?? work/codex-tasks/55-evidence/task55-feature5-tests.txt
?? work/codex-tasks/55-evidence/task55-resumed-browser.json
?? work/codex-tasks/55-evidence/task55-run-1.txt
?? work/codex-tasks/55-evidence/task55-run-2.txt
?? work/codex-tasks/55-evidence/task55-run-3.txt
?? work/codex-tasks/55-evidence/task55-temp-root.txt
?? work/chess-clock-switch/
?? work/cm1000-diffuser/parts/
?? work/codex-tasks/55-bench-five-features-REPORT.md
?? work/codex-tasks/55-screens/
?? work/fan-junction-box/concept_stl/
?? work/fan-junction-box/draft_stl/
?? work/fan-junction-box/draft_stl_B/
?? work/gene-success/dishes.png
?? work/mesh-viewer/CBL-A-E_rear_lane_set.html
?? work/mesh-viewer/CBL-A_rear_lane.html
?? work/mesh-viewer/CHS-A_chess_clock_assembled.html
?? work/mesh-viewer/CM1000_1U_Mount_on_modem.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.png
?? work/mesh-viewer/CM1000_icon_stroke_check.png
?? work/mesh-viewer/CM1000_modem_as_understood.html
?? work/mesh-viewer/CM1000_modem_understood_v2.html
?? work/mesh-viewer/CM1000_underside_measure.png
?? work/mesh-viewer/CM1P-A_one_piece_bracket.html
?? work/mesh-viewer/CM1P-B_skeleton_rails.html
?? work/mesh-viewer/CM1P-C_fitment_draft.html
?? work/mesh-viewer/CM1P-D_fitment_draft.html
?? work/mesh-viewer/CM1P-E_clearance.png
?? work/mesh-viewer/CM1P-E_one_piece_bracket.html
?? work/mesh-viewer/CM1P-F_changes.png
?? work/mesh-viewer/CM1P-F_one_piece_bracket.html
?? work/mesh-viewer/CM1P-G_one_piece_bracket.html
?? work/mesh-viewer/CM1P-H_one_piece_bracket.html
?? work/mesh-viewer/CM1P-I_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_front_slope.png
?? work/mesh-viewer/CM1P-J_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_with_modem_see_through.html
?? work/mesh-viewer/CM1P-K_V_section.png
?? work/mesh-viewer/CM1P-K_front_section.png
?? work/mesh-viewer/CM1P-K_print_part.html
?? work/mesh-viewer/CM1P-K_tip_width_measure.png
?? work/mesh-viewer/CM1P-K_with_modem_see_through.html
?? work/mesh-viewer/CM1P-L_screw_at_80.png
?? work/mesh-viewer/CM1P-L_slot_move.png
?? work/mesh-viewer/CM1P-L_with_modem_see_through.html
?? work/mesh-viewer/CM1P-M_slot.png
?? work/mesh-viewer/CM1P-M_with_modem_see_through.html
?? work/mesh-viewer/CM1P-N_with_modem_see_through.html
?? work/mesh-viewer/CM1P-O_pipe_vs_earlier.png
?? work/mesh-viewer/CM1P-O_seated_section.png
?? work/mesh-viewer/CM1P-O_with_modem_see_through.html
?? work/mesh-viewer/CM1P-P_and_modem.html
?? work/mesh-viewer/CM1P-P_icon_options.png
?? work/mesh-viewer/CM1P-P_light_distance.png
?? work/mesh-viewer/CM1P-P_lip_vs_top_edge.png
?? work/mesh-viewer/CM1P-P_logos_now.png
?? work/mesh-viewer/CM1P-P_print_part.html
?? work/mesh-viewer/CM1P-P_vs_forward_2.5_preview.html
?? work/mesh-viewer/CM1P-P_with_modem_see_through.html
?? work/mesh-viewer/CM1P-Q_with_modem.html
?? work/mesh-viewer/CM1P-T1_test_slice.html
?? work/mesh-viewer/CM1P-T2_test_slice.html
?? work/mesh-viewer/CM1P-T3_test_slice.html
?? work/mesh-viewer/CM1P-T4_test_slice.html
?? work/mesh-viewer/CM1P-T5_holes.png
?? work/mesh-viewer/CM1P-T5_on_modem.html
?? work/mesh-viewer/CM1P-T5_print_parts.html
?? work/mesh-viewer/CM1P-T6_on_modem.html
?? work/mesh-viewer/CM1P-T7_on_modem.html
?? work/mesh-viewer/CM1P-T8_look.png
?? work/mesh-viewer/CM1P-T8_look_cups.png
?? work/mesh-viewer/CM1P-T8_on_modem.html
?? work/mesh-viewer/CM1P-T8_print.html
?? work/mesh-viewer/CM1P-diffuser_option_A.png
?? work/mesh-viewer/CM1P-diffuser_option_B.png
?? work/mesh-viewer/CM1P-diffuser_option_C.png
?? work/mesh-viewer/CM1P-diffuser_options.html
?? work/mesh-viewer/CM6A_CM1000_M6.html
?? work/mesh-viewer/CM6A_fitment_review.html
?? work/mesh-viewer/CM6A_review.html
?? work/mesh-viewer/CM6A_vs_CM6B_rev2.html
?? work/mesh-viewer/CM6B_rev3.html
?? work/mesh-viewer/CM6C_assembled.html
?? work/mesh-viewer/CM6C_print_set.html
?? work/mesh-viewer/CRN-A_proposal.html
?? work/mesh-viewer/CRN-B_proposal.html
?? work/mesh-viewer/CRN-C_proposal.html
?? work/mesh-viewer/CRN-D_concept.html
?? work/mesh-viewer/CRN-E_concept.html
?? work/mesh-viewer/CSB-A.html
?? work/mesh-viewer/CSB-B.html
?? work/mesh-viewer/CSB-B_draft_tool_window.html
?? work/mesh-viewer/CSB-B_draft_zip_ties.html
?? work/mesh-viewer/CSB-C.html
?? work/mesh-viewer/CSB-C_draft.html
?? work/mesh-viewer/Cable_Span_concept.html
?? work/mesh-viewer/Cable_Span_styles.html
?? work/mesh-viewer/ER6-A_vs_source.html
?? work/mesh-viewer/ER6-B_with_router.html
?? work/mesh-viewer/ER6-C_with_router.html
?? work/mesh-viewer/ER6-D_with_router.html
?? work/mesh-viewer/ER6-E_with_router.html
?? work/mesh-viewer/ER6-F_with_router.html
?? work/mesh-viewer/ER6-G_with_router.html
?? work/mesh-viewer/ER6-H_with_router.html
?? work/mesh-viewer/HDT-M6-A_mockup.html
?? work/mesh-viewer/HP4-M6-A.html
?? work/mesh-viewer/HP4-M6-A_assembled.html
?? work/mesh-viewer/HP4-M6-A_baseline.html
?? work/mesh-viewer/HP4-M6-A_print-layout.html
?? work/mesh-viewer/HP4-M6-B.html
?? work/mesh-viewer/JB_draft1_junction_box.html
?? work/mesh-viewer/JB_draft2_box_closeup.html
?? work/mesh-viewer/JB_optionB_closeup.html
?? work/mesh-viewer/JB_optionB_in_rack.html
?? work/mesh-viewer/JB_placement_concept.html
?? work/mesh-viewer/Library_plate_and_SG8_tray.html
?? work/mesh-viewer/M6_generator_HDT.html
?? work/mesh-viewer/MRT-A_moca_tray_mockup.html
?? work/mesh-viewer/MRT-B_moca_tray_braces.html
?? work/mesh-viewer/MRT-B_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-C_moca_tray.html
?? work/mesh-viewer/MRT-C_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-D_moca_tray.html
?? work/mesh-viewer/MRT-D_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-E_tray_plate_and_test_prints.html
?? work/mesh-viewer/MRT-F.html
?? work/mesh-viewer/MRT-F_covers_and_jig.html
?? work/mesh-viewer/MRT-F_release_test.3mf
?? work/mesh-viewer/MRT-F_release_test.html
?? work/mesh-viewer/MRT-G.html
?? work/mesh-viewer/MRT-H.html
?? work/mesh-viewer/MRT-H_T5-T7_print_set.html
?? work/mesh-viewer/MRT-H_draft1_walls_keystones.html
?? work/mesh-viewer/MRT-H_draft2_ramps.html
?? work/mesh-viewer/MRT-I_draft1.html
?? work/mesh-viewer/MRT-T4.html
?? work/mesh-viewer/MRT-T4_fit_report.html
?? work/mesh-viewer/MRT-T5-T7_coax_jigs.html
?? work/mesh-viewer/MRT-T5.html
?? work/mesh-viewer/MRT_splitter_coax_review.html
?? work/mesh-viewer/MoCA_RX1_concept.html
?? work/mesh-viewer/MoCA_RX2_bones.html
?? work/mesh-viewer/MoCA_RX3_bones.html
?? work/mesh-viewer/MoCA_RX4-C_tabs.html
?? work/mesh-viewer/MoCA_RX4_bones.html
?? work/mesh-viewer/MoCA_sleeve_rev3.html
?? work/mesh-viewer/MoCA_wall_cleat_seated.html
?? work/mesh-viewer/MoCA_wall_cleat_set.html
?? work/mesh-viewer/OPX-A_concept.html
?? work/mesh-viewer/OPX-A_print_set.html
?? work/mesh-viewer/OPX-B_assembled.html
?? work/mesh-viewer/OPX-C_assembled.html
?? work/mesh-viewer/OPX-D_assembled.html
?? work/mesh-viewer/OPX-D_concept.html
?? work/mesh-viewer/OPX-D_print_set.html
?? work/mesh-viewer/OPX-E_assembled.html
?? work/mesh-viewer/OPX-E_rails_print.html
?? work/mesh-viewer/OPX-F_assembled.html
?? work/mesh-viewer/OPX-F_rails_print.html
?? work/mesh-viewer/OPX-G_assembled.html
?? work/mesh-viewer/OPX-G_channels_print.html
?? work/mesh-viewer/OpenSCAD_old_vs_snapshot.html
?? work/mesh-viewer/OptiPlex_reference_brackets.html
?? work/mesh-viewer/PHX-A_post_hex_concept.html
?? work/mesh-viewer/PHX-B_post_hex_chamfer.html
?? work/mesh-viewer/PHX-C_blank_assembled.html
?? work/mesh-viewer/PSB-A_assembled.html
?? work/mesh-viewer/PSB-A_print_set.html
?? work/mesh-viewer/Power_strip_as_understood.html
?? work/mesh-viewer/RW_rack_wall_mount_print.html
?? work/mesh-viewer/RW_rack_wall_mount_seated.html
?? work/mesh-viewer/RX4-A_print_set.html
?? work/mesh-viewer/RX4-B_print_set.html
?? work/mesh-viewer/RX4-C_print_set.html
?? work/mesh-viewer/RX5-A_print_set.html
?? work/mesh-viewer/RX5-B_assembled.html
?? work/mesh-viewer/RX5-B_print_set.html
?? work/mesh-viewer/RX5_rear_ports_issue.html
?? work/mesh-viewer/RX5_rear_ports_rev2.html
?? work/mesh-viewer/Rack_B_mock_wiring.html
?? work/mesh-viewer/Rack_custom_9U.html
?? work/mesh-viewer/Rack_frame_9U_concept.html
?? work/mesh-viewer/Rack_frame_A_vs_B.html
?? work/mesh-viewer/Rack_order_B.html
?? work/mesh-viewer/Rack_top_fan_TF-B_full_rack.html
?? work/mesh-viewer/Rack_top_fan_draft4_assembled.html
?? work/mesh-viewer/Rack_top_fan_draft4_full_rack_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_draft_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_task53_print_parts.html
?? work/mesh-viewer/SCR5-AP_1_fronts.png
?? work/mesh-viewer/SCR5-AP_2_overview.png
?? work/mesh-viewer/SCR5-AP_3_pi_on_screen.png
?? work/mesh-viewer/SCR5-AP_4_side_cut.png
?? work/mesh-viewer/SCR5-AP_5_joints.png
?? work/mesh-viewer/SCR5-AP_C_top_row.png
?? work/mesh-viewer/SCR5-AP_D_bottom_row.png
?? work/mesh-viewer/SCR5-AP_layout_A.html
?? work/mesh-viewer/SCR5-AP_layout_B.html
?? work/mesh-viewer/SCR5-AP_layout_C.html
?? work/mesh-viewer/SCR5-AP_layout_D.html
?? work/mesh-viewer/SCR5-A_review.html
?? work/mesh-viewer/SCR5-B_review.html
?? work/mesh-viewer/SCR5-C_assembled.html
?? work/mesh-viewer/SCR5-D_assembled.html
?? work/mesh-viewer/SCR5-E_app_placeholder_check.html
?? work/mesh-viewer/SCR5-E_assembled.html
?? work/mesh-viewer/SCR5-E_on_posts.html
?? work/mesh-viewer/SCR5-F_on_posts.html
?? work/mesh-viewer/SCR5-G_review.html
?? work/mesh-viewer/SCR5-H10_assembled.html
?? work/mesh-viewer/SCR5-H10_low_joint.png
?? work/mesh-viewer/SCR5-H11_assembled.html
?? work/mesh-viewer/SCR5-H11_rails_and_fan_mount.png
?? work/mesh-viewer/SCR5-H7.html
?? work/mesh-viewer/SCR5-H8.html
?? work/mesh-viewer/SCR5-H8_assembled.html
?? work/mesh-viewer/SCR5-H8_sag_section.png
?? work/mesh-viewer/SCR5-H9_assembled.html
?? work/mesh-viewer/SCR5-H9_tray.png
?? work/mesh-viewer/SCR5-H_review.html
?? work/mesh-viewer/SCR5-J1_assembled.html
?? work/mesh-viewer/SCR5-J1_hue_cradle.png
?? work/mesh-viewer/SCR5-J1_no_cradle.html
?? work/mesh-viewer/SCR5-J1_views.png
?? work/mesh-viewer/SCR5-J2_assembled.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.png
?? work/mesh-viewer/SCR5-J2_bevel_options.png
?? work/mesh-viewer/SCR5-J2_cutout_as_built.html
?? work/mesh-viewer/SCR5-J2_cutout_as_built.png
?? work/mesh-viewer/SCR5-J2_print_set.html
?? work/mesh-viewer/SCR5-J2_views.png
?? work/mesh-viewer/SCR5-J3_front_frame.html
?? work/mesh-viewer/SCR5-J3_views.png
?? work/mesh-viewer/SCR5-J3_views2.png
?? work/mesh-viewer/SCR5-J4_front.png
?? work/mesh-viewer/SCR5-J4_front_frame.html
?? work/mesh-viewer/SCR5-J4_print_set.html
?? work/mesh-viewer/SCR5-J4_views.png
?? work/mesh-viewer/SCR5-J5_tray_vs_J4.html
?? work/mesh-viewer/SCR5-WP-A_coupon.html
?? work/mesh-viewer/SCR5-swap_3d_C.png
?? work/mesh-viewer/SCR5-swap_3d_H11.png
?? work/mesh-viewer/SCR5-swap_3d_N.png
?? work/mesh-viewer/SCR5-swap_3d_N2.png
?? work/mesh-viewer/SCR5-swap_3d_S1.png
?? work/mesh-viewer/SCR5-swap_3d_S2.png
?? work/mesh-viewer/SCR5-swap_3d_S3.png
?? work/mesh-viewer/SCR5-swap_S3.html
?? work/mesh-viewer/SCR5-swap_S3.png
?? work/mesh-viewer/SCR5-swap_no_keystone.html
?? work/mesh-viewer/SCR5-swap_no_keystone.png
?? work/mesh-viewer/SCR5-swap_options.html
?? work/mesh-viewer/SCR5-swap_plate_fronts.png
?? work/mesh-viewer/SCR5-swap_side_cuts.png
?? work/mesh-viewer/SCR5_border_measure.png
?? work/mesh-viewer/SCR5_frame_rounded_draft.html
?? work/mesh-viewer/SCR5_frame_rounded_draft.png
?? work/mesh-viewer/SG8-C1_coupon.html
?? work/mesh-viewer/SG8-C1_coupon_assembled.html
?? work/mesh-viewer/SG8-C2_boss.html
?? work/mesh-viewer/SG8-M6-A_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_screws_fastened.html
?? work/mesh-viewer/SG8-M6-C_tray.html
?? work/mesh-viewer/SG8-M6-D.html
?? work/mesh-viewer/SG8-M6-E_faceplate_on_D_tray.html
?? work/mesh-viewer/SG8-M6-F_on_posts_LOCAL-ONLY.html
?? work/mesh-viewer/SG8-M6-F_post_cheeks.html
?? work/mesh-viewer/SG8-PB-A_post_brackets.html
?? work/mesh-viewer/SG8_B-plate_on_D-tray.html
?? work/mesh-viewer/TF-A.html
?? work/mesh-viewer/TF-B.html
?? work/mesh-viewer/TF-C.html
?? work/mesh-viewer/TF-D.html
?? work/mesh-viewer/TF-D_draft1.html
?? work/mesh-viewer/WMB-A_vs_original.html
?? work/mesh-viewer/faceplate_baseline_vs_CM6B.html
?? work/mesh-viewer/optiplex_rear_R_vs_O.html
?? work/mesh-viewer/printed_brackets_review_2026-10-28.html
?? work/mesh-viewer/task46-reference-regression.html
?? work/rack-finish/Rack_Finish_3D.html
?? work/rack-plan/Rack_B_Wiring_2026-11-04.png
?? work/rack-plan/Rack_Order_Options_2026-11-04.png
?? work/rack-post-hex/
?? work/rack-top-fan/draft_D/
?? work/scr5-access/png/
?? work/scr5-access/stl/
?? work/scr5-swap/stl/
?? work/wire-bracket/
```

## Resumed protected hashes

| File | Before | After |
| --- | --- | --- |
| `work/bench/projects.json` | `9e2579cc9c6e7eb7a824770b16797eea5af80613d5b2faa309c0aa04143f6cb7` | `9e2579cc9c6e7eb7a824770b16797eea5af80613d5b2faa309c0aa04143f6cb7` |
| `docs/Fit_Findings.md` | `ee1012c5f3d4a12cb3990a5b207a86766e2ebfb082060de52186823a06f4eb93` | `ee1012c5f3d4a12cb3990a5b207a86766e2ebfb082060de52186823a06f4eb93` |
| `work/workbench/Workflow_Log.md` | `57ddd2cf37d366e09c2040d08436b3c197497bf4595d78b60db2585cbb026018` | `57ddd2cf37d366e09c2040d08436b3c197497bf4595d78b60db2585cbb026018` |
| `work/mesh-viewer/TF-D.html` | `aeab6a8373b77e51f0c0a68ff47e96db1d3064918c3a214a173e1e957f8ff818` | `aeab6a8373b77e51f0c0a68ff47e96db1d3064918c3a214a173e1e957f8ff818` |

Cleanup: stopped only the Python process naming the disposable root and port 8875; closed the isolated Playwright browser/contexts. Original in-app viewport override had been reset. Temporary root retained for review; 8720 untouched.

## Protected SHA-256 before and after

The full `git status --short` path/status output matches exactly before and after acceptance (318 lines), including pre-existing unrelated changes and the already-created task evidence paths. Source changes are intentional implementation edits, not acceptance writes; equality of status output does not prove source-byte identity. The four specified protected file hashes match exactly. Both snapshots are stored in work/codex-tasks/55-evidence/task55-before.json and task55-after.json.

| File | Before | After |
| --- | --- | --- |
| `work/bench/projects.json` | `9e2579cc9c6e7eb7a824770b16797eea5af80613d5b2faa309c0aa04143f6cb7` | `9e2579cc9c6e7eb7a824770b16797eea5af80613d5b2faa309c0aa04143f6cb7` |
| `docs/Fit_Findings.md` | `ee1012c5f3d4a12cb3990a5b207a86766e2ebfb082060de52186823a06f4eb93` | `ee1012c5f3d4a12cb3990a5b207a86766e2ebfb082060de52186823a06f4eb93` |
| `work/workbench/Workflow_Log.md` | `57ddd2cf37d366e09c2040d08436b3c197497bf4595d78b60db2585cbb026018` | `57ddd2cf37d366e09c2040d08436b3c197497bf4595d78b60db2585cbb026018` |
| `work/mesh-viewer/TF-D.html` | `aeab6a8373b77e51f0c0a68ff47e96db1d3064918c3a214a173e1e957f8ff818` | `aeab6a8373b77e51f0c0a68ff47e96db1d3064918c3a214a173e1e957f8ff818` |

## Temporary HTTP acceptance output

```text
/api/health: 200
/api/state: 200
/api/projects: 200
/api/projects/csb: 200
/api/projects/mrt: 200
/api/projects/fan: 200
/api/projects/opx: 200
/api/projects/scr5: 200
/api/projects/er6: 200
/api/projects/cm1000: 200
/api/projects/psb: 200
/api/projects/rx5: 200
/api/projects/chs: 200
/api/projects/wmb: 200
/api/projects/sg8: 200
/api/projects/hdt: 200
/api/projects/phx: 200
/api/projects/rw: 200
/api/projects/moca-wall: 200
/api/projects/cbl: 200
/api/projects/hp4: 200
/api/projects/crn: 200
/api/projects/frame: 200
/api/projects/bottom: 200
/api/projects/accept-idea: 200
/api/projects/accept-measuring: 200
/api/projects/accept-draft: 200
/api/projects/accept-printing: 200
/api/projects/accept-report-due: 200
/api/projects/accept-done: 200
/api/projects/accept-parked: 200
Real TF-D response: bridge once, sandbox/connect CSP retained, disk bytes unchanged.
Viewer path safety: all four blocked.
Desktop quick buttons persisted: {"accept-idea": "draft", "accept-measuring": "draft", "accept-draft": "printing", "accept-printing": "report-due", "accept-report-due": "done", "accept-done": "draft", "accept-parked": "draft"}
Detail PATCH succeeds, own prefixes accepted, old hash returns 409 with unchanged disk.
Status-only HTTP PATCH preserves notes.
Fit report preview/commit: both markdown files retain original byte prefixes; backups exist.
TEMP DIFF work/bench/projects.json
--- work/bench/projects.json.bak
+++ work/bench/projects.json
@@ -7,7 +7,7 @@
       "prefixes": [
         "CSB"
       ],
-      "status": "done",
+      "status": "draft",
       "device_cards": [
         "docs/devices/lab-rax-4u-post.md"
       ],

TEMP DIFF docs/Fit_Findings.md
--- docs/Fit_Findings.md.bak
+++ docs/Fit_Findings.md
@@ -90,3 +90,4 @@
 - 2026-11-06 MRT-H splitter bosses (Brian, printed): the splitter's ears sit 7 above the face the case rests on (modelled flush), so the bosses stopped 7 short of the ears. MRT-I bosses stand 7 above the riser (12.5 above the floor), inserts at the new top. Splitter device card updated.
 - 2026-11-07 MRT-H rear shoes MRT-C-L/R (Brian, printed): the rear-post mounts work surprisingly well. A beefier pocket-shoe redesign was drafted and dropped at his direction; MRT-I keeps the MRT-H shoes and wall tips unchanged (no reprint). Strength UNKNOWN.
 - 2026-11-07 CSB-C (Brian, via Workshop Bench): Fits. UNKNOWN walls, UNKNOWN infill. Strength UNKNOWN.
+- 2026-11-08 CSB-C (Brian, via Workshop Bench): Fits. Disposable API acceptance only. UNKNOWN walls, UNKNOWN infill. Strength UNKNOWN.

TEMP DIFF work/workbench/Workflow_Log.md
--- work/workbench/Workflow_Log.md.bak
+++ work/workbench/Workflow_Log.md
@@ -37,3 +37,9 @@
 | Date | Step | What happened | Friction | App idea |
 | --- | --- | --- | --- | --- |
 | 2026-11-07 | Report | 2026-11-07 CSB-C (Brian, via Workshop Bench): Fits. UNKNOWN walls, UNKNOWN infill. Strength UNKNOWN. | | |
+
+## Cable management bracket (front to rear posts) (continued)
+
+| Date | Step | What happened | Friction | App idea |
+| --- | --- | --- | --- | --- |
+| 2026-11-08 | Report | 2026-11-08 CSB-C (Brian, via Workshop Bench): Fits. Disposable API acceptance only. UNKNOWN walls, UNKNOWN infill. Strength UNKNOWN. | | |

```

## git status --short — Before

```text
 M IDEAS.md
 M docs/devices/bridgelink-2way-splitter.md
 M outputs/Final_3MF/CM6A_CM1000_M6_bracket_set.3mf
 M tools/bench/README.md
 M tools/bench/bench.py
 M tools/bench/static/bench.css
 M tools/bench/static/bench.js
 M tools/bench/static/index.html
 M tools/bench/test_bench.py
 M work/equipment-models/power_strip/power_strip.scad
 M work/equipment-models/power_strip/power_strip.stl
 M work/moca-rack-tray/MRT.scad
 M work/screen-5in/Dimensions.md
?? outputs/Final_3MF/CHS-A_chess_clock_switch_set.3mf
?? outputs/Final_3MF/SCR5-J4_screen_pi_hue_3port_set.3mf
?? outputs/Final_3MF/WMB-A_flat_wire_bracket.3mf
?? outputs/Screen_Pi_Hue_SCR5-J3_2026-11-03/
?? outputs/Screen_Pi_Hue_SCR5-J4_2026-11-03/
?? rwm1.scad
?? tools/bench/static/viewer-bridge.js
?? work/codex-tasks/55-evidence/task55-after.json
?? work/codex-tasks/55-evidence/task55-before.json
?? work/codex-tasks/55-evidence/task55-browser-results.json
?? work/codex-tasks/55-evidence/task55-feature1-tests.txt
?? work/codex-tasks/55-evidence/task55-feature2-tests.txt
?? work/codex-tasks/55-evidence/task55-feature3-tests.txt
?? work/codex-tasks/55-evidence/task55-feature4-tests.txt
?? work/codex-tasks/55-evidence/task55-feature5-tests.txt
?? work/codex-tasks/55-evidence/task55-run-1.txt
?? work/codex-tasks/55-evidence/task55-run-2.txt
?? work/codex-tasks/55-evidence/task55-run-3.txt
?? work/codex-tasks/55-evidence/task55-temp-root.txt
?? work/chess-clock-switch/
?? work/cm1000-diffuser/parts/
?? work/codex-tasks/55-bench-five-features-REPORT.md
?? work/codex-tasks/55-screens/
?? work/fan-junction-box/concept_stl/
?? work/fan-junction-box/draft_stl/
?? work/fan-junction-box/draft_stl_B/
?? work/gene-success/dishes.png
?? work/mesh-viewer/CBL-A-E_rear_lane_set.html
?? work/mesh-viewer/CBL-A_rear_lane.html
?? work/mesh-viewer/CHS-A_chess_clock_assembled.html
?? work/mesh-viewer/CM1000_1U_Mount_on_modem.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.png
?? work/mesh-viewer/CM1000_icon_stroke_check.png
?? work/mesh-viewer/CM1000_modem_as_understood.html
?? work/mesh-viewer/CM1000_modem_understood_v2.html
?? work/mesh-viewer/CM1000_underside_measure.png
?? work/mesh-viewer/CM1P-A_one_piece_bracket.html
?? work/mesh-viewer/CM1P-B_skeleton_rails.html
?? work/mesh-viewer/CM1P-C_fitment_draft.html
?? work/mesh-viewer/CM1P-D_fitment_draft.html
?? work/mesh-viewer/CM1P-E_clearance.png
?? work/mesh-viewer/CM1P-E_one_piece_bracket.html
?? work/mesh-viewer/CM1P-F_changes.png
?? work/mesh-viewer/CM1P-F_one_piece_bracket.html
?? work/mesh-viewer/CM1P-G_one_piece_bracket.html
?? work/mesh-viewer/CM1P-H_one_piece_bracket.html
?? work/mesh-viewer/CM1P-I_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_front_slope.png
?? work/mesh-viewer/CM1P-J_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_with_modem_see_through.html
?? work/mesh-viewer/CM1P-K_V_section.png
?? work/mesh-viewer/CM1P-K_front_section.png
?? work/mesh-viewer/CM1P-K_print_part.html
?? work/mesh-viewer/CM1P-K_tip_width_measure.png
?? work/mesh-viewer/CM1P-K_with_modem_see_through.html
?? work/mesh-viewer/CM1P-L_screw_at_80.png
?? work/mesh-viewer/CM1P-L_slot_move.png
?? work/mesh-viewer/CM1P-L_with_modem_see_through.html
?? work/mesh-viewer/CM1P-M_slot.png
?? work/mesh-viewer/CM1P-M_with_modem_see_through.html
?? work/mesh-viewer/CM1P-N_with_modem_see_through.html
?? work/mesh-viewer/CM1P-O_pipe_vs_earlier.png
?? work/mesh-viewer/CM1P-O_seated_section.png
?? work/mesh-viewer/CM1P-O_with_modem_see_through.html
?? work/mesh-viewer/CM1P-P_and_modem.html
?? work/mesh-viewer/CM1P-P_icon_options.png
?? work/mesh-viewer/CM1P-P_light_distance.png
?? work/mesh-viewer/CM1P-P_lip_vs_top_edge.png
?? work/mesh-viewer/CM1P-P_logos_now.png
?? work/mesh-viewer/CM1P-P_print_part.html
?? work/mesh-viewer/CM1P-P_vs_forward_2.5_preview.html
?? work/mesh-viewer/CM1P-P_with_modem_see_through.html
?? work/mesh-viewer/CM1P-Q_with_modem.html
?? work/mesh-viewer/CM1P-T1_test_slice.html
?? work/mesh-viewer/CM1P-T2_test_slice.html
?? work/mesh-viewer/CM1P-T3_test_slice.html
?? work/mesh-viewer/CM1P-T4_test_slice.html
?? work/mesh-viewer/CM1P-T5_holes.png
?? work/mesh-viewer/CM1P-T5_on_modem.html
?? work/mesh-viewer/CM1P-T5_print_parts.html
?? work/mesh-viewer/CM1P-T6_on_modem.html
?? work/mesh-viewer/CM1P-T7_on_modem.html
?? work/mesh-viewer/CM1P-T8_look.png
?? work/mesh-viewer/CM1P-T8_look_cups.png
?? work/mesh-viewer/CM1P-T8_on_modem.html
?? work/mesh-viewer/CM1P-T8_print.html
?? work/mesh-viewer/CM1P-diffuser_option_A.png
?? work/mesh-viewer/CM1P-diffuser_option_B.png
?? work/mesh-viewer/CM1P-diffuser_option_C.png
?? work/mesh-viewer/CM1P-diffuser_options.html
?? work/mesh-viewer/CM6A_CM1000_M6.html
?? work/mesh-viewer/CM6A_fitment_review.html
?? work/mesh-viewer/CM6A_review.html
?? work/mesh-viewer/CM6A_vs_CM6B_rev2.html
?? work/mesh-viewer/CM6B_rev3.html
?? work/mesh-viewer/CM6C_assembled.html
?? work/mesh-viewer/CM6C_print_set.html
?? work/mesh-viewer/CRN-A_proposal.html
?? work/mesh-viewer/CRN-B_proposal.html
?? work/mesh-viewer/CRN-C_proposal.html
?? work/mesh-viewer/CRN-D_concept.html
?? work/mesh-viewer/CRN-E_concept.html
?? work/mesh-viewer/CSB-A.html
?? work/mesh-viewer/CSB-B.html
?? work/mesh-viewer/CSB-B_draft_tool_window.html
?? work/mesh-viewer/CSB-B_draft_zip_ties.html
?? work/mesh-viewer/CSB-C.html
?? work/mesh-viewer/CSB-C_draft.html
?? work/mesh-viewer/Cable_Span_concept.html
?? work/mesh-viewer/Cable_Span_styles.html
?? work/mesh-viewer/ER6-A_vs_source.html
?? work/mesh-viewer/ER6-B_with_router.html
?? work/mesh-viewer/ER6-C_with_router.html
?? work/mesh-viewer/ER6-D_with_router.html
?? work/mesh-viewer/ER6-E_with_router.html
?? work/mesh-viewer/ER6-F_with_router.html
?? work/mesh-viewer/ER6-G_with_router.html
?? work/mesh-viewer/ER6-H_with_router.html
?? work/mesh-viewer/HDT-M6-A_mockup.html
?? work/mesh-viewer/HP4-M6-A.html
?? work/mesh-viewer/HP4-M6-A_assembled.html
?? work/mesh-viewer/HP4-M6-A_baseline.html
?? work/mesh-viewer/HP4-M6-A_print-layout.html
?? work/mesh-viewer/HP4-M6-B.html
?? work/mesh-viewer/JB_draft1_junction_box.html
?? work/mesh-viewer/JB_draft2_box_closeup.html
?? work/mesh-viewer/JB_optionB_closeup.html
?? work/mesh-viewer/JB_optionB_in_rack.html
?? work/mesh-viewer/JB_placement_concept.html
?? work/mesh-viewer/Library_plate_and_SG8_tray.html
?? work/mesh-viewer/M6_generator_HDT.html
?? work/mesh-viewer/MRT-A_moca_tray_mockup.html
?? work/mesh-viewer/MRT-B_moca_tray_braces.html
?? work/mesh-viewer/MRT-B_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-C_moca_tray.html
?? work/mesh-viewer/MRT-C_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-D_moca_tray.html
?? work/mesh-viewer/MRT-D_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-E_tray_plate_and_test_prints.html
?? work/mesh-viewer/MRT-F.html
?? work/mesh-viewer/MRT-F_covers_and_jig.html
?? work/mesh-viewer/MRT-F_release_test.3mf
?? work/mesh-viewer/MRT-F_release_test.html
?? work/mesh-viewer/MRT-G.html
?? work/mesh-viewer/MRT-H.html
?? work/mesh-viewer/MRT-H_T5-T7_print_set.html
?? work/mesh-viewer/MRT-H_draft1_walls_keystones.html
?? work/mesh-viewer/MRT-H_draft2_ramps.html
?? work/mesh-viewer/MRT-I_draft1.html
?? work/mesh-viewer/MRT-T4.html
?? work/mesh-viewer/MRT-T4_fit_report.html
?? work/mesh-viewer/MRT-T5-T7_coax_jigs.html
?? work/mesh-viewer/MRT-T5.html
?? work/mesh-viewer/MRT_splitter_coax_review.html
?? work/mesh-viewer/MoCA_RX1_concept.html
?? work/mesh-viewer/MoCA_RX2_bones.html
?? work/mesh-viewer/MoCA_RX3_bones.html
?? work/mesh-viewer/MoCA_RX4-C_tabs.html
?? work/mesh-viewer/MoCA_RX4_bones.html
?? work/mesh-viewer/MoCA_sleeve_rev3.html
?? work/mesh-viewer/MoCA_wall_cleat_seated.html
?? work/mesh-viewer/MoCA_wall_cleat_set.html
?? work/mesh-viewer/OPX-A_concept.html
?? work/mesh-viewer/OPX-A_print_set.html
?? work/mesh-viewer/OPX-B_assembled.html
?? work/mesh-viewer/OPX-C_assembled.html
?? work/mesh-viewer/OPX-D_assembled.html
?? work/mesh-viewer/OPX-D_concept.html
?? work/mesh-viewer/OPX-D_print_set.html
?? work/mesh-viewer/OPX-E_assembled.html
?? work/mesh-viewer/OPX-E_rails_print.html
?? work/mesh-viewer/OPX-F_assembled.html
?? work/mesh-viewer/OPX-F_rails_print.html
?? work/mesh-viewer/OPX-G_assembled.html
?? work/mesh-viewer/OPX-G_channels_print.html
?? work/mesh-viewer/OpenSCAD_old_vs_snapshot.html
?? work/mesh-viewer/OptiPlex_reference_brackets.html
?? work/mesh-viewer/PHX-A_post_hex_concept.html
?? work/mesh-viewer/PHX-B_post_hex_chamfer.html
?? work/mesh-viewer/PHX-C_blank_assembled.html
?? work/mesh-viewer/PSB-A_assembled.html
?? work/mesh-viewer/PSB-A_print_set.html
?? work/mesh-viewer/Power_strip_as_understood.html
?? work/mesh-viewer/RW_rack_wall_mount_print.html
?? work/mesh-viewer/RW_rack_wall_mount_seated.html
?? work/mesh-viewer/RX4-A_print_set.html
?? work/mesh-viewer/RX4-B_print_set.html
?? work/mesh-viewer/RX4-C_print_set.html
?? work/mesh-viewer/RX5-A_print_set.html
?? work/mesh-viewer/RX5-B_assembled.html
?? work/mesh-viewer/RX5-B_print_set.html
?? work/mesh-viewer/RX5_rear_ports_issue.html
?? work/mesh-viewer/RX5_rear_ports_rev2.html
?? work/mesh-viewer/Rack_B_mock_wiring.html
?? work/mesh-viewer/Rack_custom_9U.html
?? work/mesh-viewer/Rack_frame_9U_concept.html
?? work/mesh-viewer/Rack_frame_A_vs_B.html
?? work/mesh-viewer/Rack_order_B.html
?? work/mesh-viewer/Rack_top_fan_TF-B_full_rack.html
?? work/mesh-viewer/Rack_top_fan_draft4_assembled.html
?? work/mesh-viewer/Rack_top_fan_draft4_full_rack_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_draft_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_task53_print_parts.html
?? work/mesh-viewer/SCR5-AP_1_fronts.png
?? work/mesh-viewer/SCR5-AP_2_overview.png
?? work/mesh-viewer/SCR5-AP_3_pi_on_screen.png
?? work/mesh-viewer/SCR5-AP_4_side_cut.png
?? work/mesh-viewer/SCR5-AP_5_joints.png
?? work/mesh-viewer/SCR5-AP_C_top_row.png
?? work/mesh-viewer/SCR5-AP_D_bottom_row.png
?? work/mesh-viewer/SCR5-AP_layout_A.html
?? work/mesh-viewer/SCR5-AP_layout_B.html
?? work/mesh-viewer/SCR5-AP_layout_C.html
?? work/mesh-viewer/SCR5-AP_layout_D.html
?? work/mesh-viewer/SCR5-A_review.html
?? work/mesh-viewer/SCR5-B_review.html
?? work/mesh-viewer/SCR5-C_assembled.html
?? work/mesh-viewer/SCR5-D_assembled.html
?? work/mesh-viewer/SCR5-E_app_placeholder_check.html
?? work/mesh-viewer/SCR5-E_assembled.html
?? work/mesh-viewer/SCR5-E_on_posts.html
?? work/mesh-viewer/SCR5-F_on_posts.html
?? work/mesh-viewer/SCR5-G_review.html
?? work/mesh-viewer/SCR5-H10_assembled.html
?? work/mesh-viewer/SCR5-H10_low_joint.png
?? work/mesh-viewer/SCR5-H11_assembled.html
?? work/mesh-viewer/SCR5-H11_rails_and_fan_mount.png
?? work/mesh-viewer/SCR5-H7.html
?? work/mesh-viewer/SCR5-H8.html
?? work/mesh-viewer/SCR5-H8_assembled.html
?? work/mesh-viewer/SCR5-H8_sag_section.png
?? work/mesh-viewer/SCR5-H9_assembled.html
?? work/mesh-viewer/SCR5-H9_tray.png
?? work/mesh-viewer/SCR5-H_review.html
?? work/mesh-viewer/SCR5-J1_assembled.html
?? work/mesh-viewer/SCR5-J1_hue_cradle.png
?? work/mesh-viewer/SCR5-J1_no_cradle.html
?? work/mesh-viewer/SCR5-J1_views.png
?? work/mesh-viewer/SCR5-J2_assembled.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.png
?? work/mesh-viewer/SCR5-J2_bevel_options.png
?? work/mesh-viewer/SCR5-J2_cutout_as_built.html
?? work/mesh-viewer/SCR5-J2_cutout_as_built.png
?? work/mesh-viewer/SCR5-J2_print_set.html
?? work/mesh-viewer/SCR5-J2_views.png
?? work/mesh-viewer/SCR5-J3_front_frame.html
?? work/mesh-viewer/SCR5-J3_views.png
?? work/mesh-viewer/SCR5-J3_views2.png
?? work/mesh-viewer/SCR5-J4_front.png
?? work/mesh-viewer/SCR5-J4_front_frame.html
?? work/mesh-viewer/SCR5-J4_print_set.html
?? work/mesh-viewer/SCR5-J4_views.png
?? work/mesh-viewer/SCR5-J5_tray_vs_J4.html
?? work/mesh-viewer/SCR5-WP-A_coupon.html
?? work/mesh-viewer/SCR5-swap_3d_C.png
?? work/mesh-viewer/SCR5-swap_3d_H11.png
?? work/mesh-viewer/SCR5-swap_3d_N.png
?? work/mesh-viewer/SCR5-swap_3d_N2.png
?? work/mesh-viewer/SCR5-swap_3d_S1.png
?? work/mesh-viewer/SCR5-swap_3d_S2.png
?? work/mesh-viewer/SCR5-swap_3d_S3.png
?? work/mesh-viewer/SCR5-swap_S3.html
?? work/mesh-viewer/SCR5-swap_S3.png
?? work/mesh-viewer/SCR5-swap_no_keystone.html
?? work/mesh-viewer/SCR5-swap_no_keystone.png
?? work/mesh-viewer/SCR5-swap_options.html
?? work/mesh-viewer/SCR5-swap_plate_fronts.png
?? work/mesh-viewer/SCR5-swap_side_cuts.png
?? work/mesh-viewer/SCR5_border_measure.png
?? work/mesh-viewer/SCR5_frame_rounded_draft.html
?? work/mesh-viewer/SCR5_frame_rounded_draft.png
?? work/mesh-viewer/SG8-C1_coupon.html
?? work/mesh-viewer/SG8-C1_coupon_assembled.html
?? work/mesh-viewer/SG8-C2_boss.html
?? work/mesh-viewer/SG8-M6-A_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_screws_fastened.html
?? work/mesh-viewer/SG8-M6-C_tray.html
?? work/mesh-viewer/SG8-M6-D.html
?? work/mesh-viewer/SG8-M6-E_faceplate_on_D_tray.html
?? work/mesh-viewer/SG8-M6-F_on_posts_LOCAL-ONLY.html
?? work/mesh-viewer/SG8-M6-F_post_cheeks.html
?? work/mesh-viewer/SG8-PB-A_post_brackets.html
?? work/mesh-viewer/SG8_B-plate_on_D-tray.html
?? work/mesh-viewer/TF-A.html
?? work/mesh-viewer/TF-B.html
?? work/mesh-viewer/TF-C.html
?? work/mesh-viewer/TF-D.html
?? work/mesh-viewer/TF-D_draft1.html
?? work/mesh-viewer/WMB-A_vs_original.html
?? work/mesh-viewer/faceplate_baseline_vs_CM6B.html
?? work/mesh-viewer/optiplex_rear_R_vs_O.html
?? work/mesh-viewer/printed_brackets_review_2026-10-28.html
?? work/mesh-viewer/task46-reference-regression.html
?? work/rack-finish/Rack_Finish_3D.html
?? work/rack-plan/Rack_B_Wiring_2026-11-04.png
?? work/rack-plan/Rack_Order_Options_2026-11-04.png
?? work/rack-post-hex/
?? work/rack-top-fan/draft_D/
?? work/scr5-access/png/
?? work/scr5-access/stl/
?? work/scr5-swap/stl/
?? work/wire-bracket/
```

## git status --short — After

```text
 M IDEAS.md
 M docs/devices/bridgelink-2way-splitter.md
 M outputs/Final_3MF/CM6A_CM1000_M6_bracket_set.3mf
 M tools/bench/README.md
 M tools/bench/bench.py
 M tools/bench/static/bench.css
 M tools/bench/static/bench.js
 M tools/bench/static/index.html
 M tools/bench/test_bench.py
 M work/equipment-models/power_strip/power_strip.scad
 M work/equipment-models/power_strip/power_strip.stl
 M work/moca-rack-tray/MRT.scad
 M work/screen-5in/Dimensions.md
?? outputs/Final_3MF/CHS-A_chess_clock_switch_set.3mf
?? outputs/Final_3MF/SCR5-J4_screen_pi_hue_3port_set.3mf
?? outputs/Final_3MF/WMB-A_flat_wire_bracket.3mf
?? outputs/Screen_Pi_Hue_SCR5-J3_2026-11-03/
?? outputs/Screen_Pi_Hue_SCR5-J4_2026-11-03/
?? rwm1.scad
?? tools/bench/static/viewer-bridge.js
?? work/codex-tasks/55-evidence/task55-after.json
?? work/codex-tasks/55-evidence/task55-before.json
?? work/codex-tasks/55-evidence/task55-browser-results.json
?? work/codex-tasks/55-evidence/task55-feature1-tests.txt
?? work/codex-tasks/55-evidence/task55-feature2-tests.txt
?? work/codex-tasks/55-evidence/task55-feature3-tests.txt
?? work/codex-tasks/55-evidence/task55-feature4-tests.txt
?? work/codex-tasks/55-evidence/task55-feature5-tests.txt
?? work/codex-tasks/55-evidence/task55-run-1.txt
?? work/codex-tasks/55-evidence/task55-run-2.txt
?? work/codex-tasks/55-evidence/task55-run-3.txt
?? work/codex-tasks/55-evidence/task55-temp-root.txt
?? work/chess-clock-switch/
?? work/cm1000-diffuser/parts/
?? work/codex-tasks/55-bench-five-features-REPORT.md
?? work/codex-tasks/55-screens/
?? work/fan-junction-box/concept_stl/
?? work/fan-junction-box/draft_stl/
?? work/fan-junction-box/draft_stl_B/
?? work/gene-success/dishes.png
?? work/mesh-viewer/CBL-A-E_rear_lane_set.html
?? work/mesh-viewer/CBL-A_rear_lane.html
?? work/mesh-viewer/CHS-A_chess_clock_assembled.html
?? work/mesh-viewer/CM1000_1U_Mount_on_modem.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.html
?? work/mesh-viewer/CM1000_LEDs_as_understood.png
?? work/mesh-viewer/CM1000_icon_stroke_check.png
?? work/mesh-viewer/CM1000_modem_as_understood.html
?? work/mesh-viewer/CM1000_modem_understood_v2.html
?? work/mesh-viewer/CM1000_underside_measure.png
?? work/mesh-viewer/CM1P-A_one_piece_bracket.html
?? work/mesh-viewer/CM1P-B_skeleton_rails.html
?? work/mesh-viewer/CM1P-C_fitment_draft.html
?? work/mesh-viewer/CM1P-D_fitment_draft.html
?? work/mesh-viewer/CM1P-E_clearance.png
?? work/mesh-viewer/CM1P-E_one_piece_bracket.html
?? work/mesh-viewer/CM1P-F_changes.png
?? work/mesh-viewer/CM1P-F_one_piece_bracket.html
?? work/mesh-viewer/CM1P-G_one_piece_bracket.html
?? work/mesh-viewer/CM1P-H_one_piece_bracket.html
?? work/mesh-viewer/CM1P-I_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_front_slope.png
?? work/mesh-viewer/CM1P-J_one_piece_bracket.html
?? work/mesh-viewer/CM1P-J_with_modem_see_through.html
?? work/mesh-viewer/CM1P-K_V_section.png
?? work/mesh-viewer/CM1P-K_front_section.png
?? work/mesh-viewer/CM1P-K_print_part.html
?? work/mesh-viewer/CM1P-K_tip_width_measure.png
?? work/mesh-viewer/CM1P-K_with_modem_see_through.html
?? work/mesh-viewer/CM1P-L_screw_at_80.png
?? work/mesh-viewer/CM1P-L_slot_move.png
?? work/mesh-viewer/CM1P-L_with_modem_see_through.html
?? work/mesh-viewer/CM1P-M_slot.png
?? work/mesh-viewer/CM1P-M_with_modem_see_through.html
?? work/mesh-viewer/CM1P-N_with_modem_see_through.html
?? work/mesh-viewer/CM1P-O_pipe_vs_earlier.png
?? work/mesh-viewer/CM1P-O_seated_section.png
?? work/mesh-viewer/CM1P-O_with_modem_see_through.html
?? work/mesh-viewer/CM1P-P_and_modem.html
?? work/mesh-viewer/CM1P-P_icon_options.png
?? work/mesh-viewer/CM1P-P_light_distance.png
?? work/mesh-viewer/CM1P-P_lip_vs_top_edge.png
?? work/mesh-viewer/CM1P-P_logos_now.png
?? work/mesh-viewer/CM1P-P_print_part.html
?? work/mesh-viewer/CM1P-P_vs_forward_2.5_preview.html
?? work/mesh-viewer/CM1P-P_with_modem_see_through.html
?? work/mesh-viewer/CM1P-Q_with_modem.html
?? work/mesh-viewer/CM1P-T1_test_slice.html
?? work/mesh-viewer/CM1P-T2_test_slice.html
?? work/mesh-viewer/CM1P-T3_test_slice.html
?? work/mesh-viewer/CM1P-T4_test_slice.html
?? work/mesh-viewer/CM1P-T5_holes.png
?? work/mesh-viewer/CM1P-T5_on_modem.html
?? work/mesh-viewer/CM1P-T5_print_parts.html
?? work/mesh-viewer/CM1P-T6_on_modem.html
?? work/mesh-viewer/CM1P-T7_on_modem.html
?? work/mesh-viewer/CM1P-T8_look.png
?? work/mesh-viewer/CM1P-T8_look_cups.png
?? work/mesh-viewer/CM1P-T8_on_modem.html
?? work/mesh-viewer/CM1P-T8_print.html
?? work/mesh-viewer/CM1P-diffuser_option_A.png
?? work/mesh-viewer/CM1P-diffuser_option_B.png
?? work/mesh-viewer/CM1P-diffuser_option_C.png
?? work/mesh-viewer/CM1P-diffuser_options.html
?? work/mesh-viewer/CM6A_CM1000_M6.html
?? work/mesh-viewer/CM6A_fitment_review.html
?? work/mesh-viewer/CM6A_review.html
?? work/mesh-viewer/CM6A_vs_CM6B_rev2.html
?? work/mesh-viewer/CM6B_rev3.html
?? work/mesh-viewer/CM6C_assembled.html
?? work/mesh-viewer/CM6C_print_set.html
?? work/mesh-viewer/CRN-A_proposal.html
?? work/mesh-viewer/CRN-B_proposal.html
?? work/mesh-viewer/CRN-C_proposal.html
?? work/mesh-viewer/CRN-D_concept.html
?? work/mesh-viewer/CRN-E_concept.html
?? work/mesh-viewer/CSB-A.html
?? work/mesh-viewer/CSB-B.html
?? work/mesh-viewer/CSB-B_draft_tool_window.html
?? work/mesh-viewer/CSB-B_draft_zip_ties.html
?? work/mesh-viewer/CSB-C.html
?? work/mesh-viewer/CSB-C_draft.html
?? work/mesh-viewer/Cable_Span_concept.html
?? work/mesh-viewer/Cable_Span_styles.html
?? work/mesh-viewer/ER6-A_vs_source.html
?? work/mesh-viewer/ER6-B_with_router.html
?? work/mesh-viewer/ER6-C_with_router.html
?? work/mesh-viewer/ER6-D_with_router.html
?? work/mesh-viewer/ER6-E_with_router.html
?? work/mesh-viewer/ER6-F_with_router.html
?? work/mesh-viewer/ER6-G_with_router.html
?? work/mesh-viewer/ER6-H_with_router.html
?? work/mesh-viewer/HDT-M6-A_mockup.html
?? work/mesh-viewer/HP4-M6-A.html
?? work/mesh-viewer/HP4-M6-A_assembled.html
?? work/mesh-viewer/HP4-M6-A_baseline.html
?? work/mesh-viewer/HP4-M6-A_print-layout.html
?? work/mesh-viewer/HP4-M6-B.html
?? work/mesh-viewer/JB_draft1_junction_box.html
?? work/mesh-viewer/JB_draft2_box_closeup.html
?? work/mesh-viewer/JB_optionB_closeup.html
?? work/mesh-viewer/JB_optionB_in_rack.html
?? work/mesh-viewer/JB_placement_concept.html
?? work/mesh-viewer/Library_plate_and_SG8_tray.html
?? work/mesh-viewer/M6_generator_HDT.html
?? work/mesh-viewer/MRT-A_moca_tray_mockup.html
?? work/mesh-viewer/MRT-B_moca_tray_braces.html
?? work/mesh-viewer/MRT-B_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-C_moca_tray.html
?? work/mesh-viewer/MRT-C_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-D_moca_tray.html
?? work/mesh-viewer/MRT-D_on_rear_posts_LOCAL-ONLY.html
?? work/mesh-viewer/MRT-E_tray_plate_and_test_prints.html
?? work/mesh-viewer/MRT-F.html
?? work/mesh-viewer/MRT-F_covers_and_jig.html
?? work/mesh-viewer/MRT-F_release_test.3mf
?? work/mesh-viewer/MRT-F_release_test.html
?? work/mesh-viewer/MRT-G.html
?? work/mesh-viewer/MRT-H.html
?? work/mesh-viewer/MRT-H_T5-T7_print_set.html
?? work/mesh-viewer/MRT-H_draft1_walls_keystones.html
?? work/mesh-viewer/MRT-H_draft2_ramps.html
?? work/mesh-viewer/MRT-I_draft1.html
?? work/mesh-viewer/MRT-T4.html
?? work/mesh-viewer/MRT-T4_fit_report.html
?? work/mesh-viewer/MRT-T5-T7_coax_jigs.html
?? work/mesh-viewer/MRT-T5.html
?? work/mesh-viewer/MRT_splitter_coax_review.html
?? work/mesh-viewer/MoCA_RX1_concept.html
?? work/mesh-viewer/MoCA_RX2_bones.html
?? work/mesh-viewer/MoCA_RX3_bones.html
?? work/mesh-viewer/MoCA_RX4-C_tabs.html
?? work/mesh-viewer/MoCA_RX4_bones.html
?? work/mesh-viewer/MoCA_sleeve_rev3.html
?? work/mesh-viewer/MoCA_wall_cleat_seated.html
?? work/mesh-viewer/MoCA_wall_cleat_set.html
?? work/mesh-viewer/OPX-A_concept.html
?? work/mesh-viewer/OPX-A_print_set.html
?? work/mesh-viewer/OPX-B_assembled.html
?? work/mesh-viewer/OPX-C_assembled.html
?? work/mesh-viewer/OPX-D_assembled.html
?? work/mesh-viewer/OPX-D_concept.html
?? work/mesh-viewer/OPX-D_print_set.html
?? work/mesh-viewer/OPX-E_assembled.html
?? work/mesh-viewer/OPX-E_rails_print.html
?? work/mesh-viewer/OPX-F_assembled.html
?? work/mesh-viewer/OPX-F_rails_print.html
?? work/mesh-viewer/OPX-G_assembled.html
?? work/mesh-viewer/OPX-G_channels_print.html
?? work/mesh-viewer/OpenSCAD_old_vs_snapshot.html
?? work/mesh-viewer/OptiPlex_reference_brackets.html
?? work/mesh-viewer/PHX-A_post_hex_concept.html
?? work/mesh-viewer/PHX-B_post_hex_chamfer.html
?? work/mesh-viewer/PHX-C_blank_assembled.html
?? work/mesh-viewer/PSB-A_assembled.html
?? work/mesh-viewer/PSB-A_print_set.html
?? work/mesh-viewer/Power_strip_as_understood.html
?? work/mesh-viewer/RW_rack_wall_mount_print.html
?? work/mesh-viewer/RW_rack_wall_mount_seated.html
?? work/mesh-viewer/RX4-A_print_set.html
?? work/mesh-viewer/RX4-B_print_set.html
?? work/mesh-viewer/RX4-C_print_set.html
?? work/mesh-viewer/RX5-A_print_set.html
?? work/mesh-viewer/RX5-B_assembled.html
?? work/mesh-viewer/RX5-B_print_set.html
?? work/mesh-viewer/RX5_rear_ports_issue.html
?? work/mesh-viewer/RX5_rear_ports_rev2.html
?? work/mesh-viewer/Rack_B_mock_wiring.html
?? work/mesh-viewer/Rack_custom_9U.html
?? work/mesh-viewer/Rack_frame_9U_concept.html
?? work/mesh-viewer/Rack_frame_A_vs_B.html
?? work/mesh-viewer/Rack_order_B.html
?? work/mesh-viewer/Rack_top_fan_TF-B_full_rack.html
?? work/mesh-viewer/Rack_top_fan_draft4_assembled.html
?? work/mesh-viewer/Rack_top_fan_draft4_full_rack_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_draft_LOCAL-ONLY.html
?? work/mesh-viewer/Rack_top_fan_task53_print_parts.html
?? work/mesh-viewer/SCR5-AP_1_fronts.png
?? work/mesh-viewer/SCR5-AP_2_overview.png
?? work/mesh-viewer/SCR5-AP_3_pi_on_screen.png
?? work/mesh-viewer/SCR5-AP_4_side_cut.png
?? work/mesh-viewer/SCR5-AP_5_joints.png
?? work/mesh-viewer/SCR5-AP_C_top_row.png
?? work/mesh-viewer/SCR5-AP_D_bottom_row.png
?? work/mesh-viewer/SCR5-AP_layout_A.html
?? work/mesh-viewer/SCR5-AP_layout_B.html
?? work/mesh-viewer/SCR5-AP_layout_C.html
?? work/mesh-viewer/SCR5-AP_layout_D.html
?? work/mesh-viewer/SCR5-A_review.html
?? work/mesh-viewer/SCR5-B_review.html
?? work/mesh-viewer/SCR5-C_assembled.html
?? work/mesh-viewer/SCR5-D_assembled.html
?? work/mesh-viewer/SCR5-E_app_placeholder_check.html
?? work/mesh-viewer/SCR5-E_assembled.html
?? work/mesh-viewer/SCR5-E_on_posts.html
?? work/mesh-viewer/SCR5-F_on_posts.html
?? work/mesh-viewer/SCR5-G_review.html
?? work/mesh-viewer/SCR5-H10_assembled.html
?? work/mesh-viewer/SCR5-H10_low_joint.png
?? work/mesh-viewer/SCR5-H11_assembled.html
?? work/mesh-viewer/SCR5-H11_rails_and_fan_mount.png
?? work/mesh-viewer/SCR5-H7.html
?? work/mesh-viewer/SCR5-H8.html
?? work/mesh-viewer/SCR5-H8_assembled.html
?? work/mesh-viewer/SCR5-H8_sag_section.png
?? work/mesh-viewer/SCR5-H9_assembled.html
?? work/mesh-viewer/SCR5-H9_tray.png
?? work/mesh-viewer/SCR5-H_review.html
?? work/mesh-viewer/SCR5-J1_assembled.html
?? work/mesh-viewer/SCR5-J1_hue_cradle.png
?? work/mesh-viewer/SCR5-J1_no_cradle.html
?? work/mesh-viewer/SCR5-J1_views.png
?? work/mesh-viewer/SCR5-J2_assembled.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.html
?? work/mesh-viewer/SCR5-J2_bevel_A_vs_B.png
?? work/mesh-viewer/SCR5-J2_bevel_options.png
?? work/mesh-viewer/SCR5-J2_cutout_as_built.html
?? work/mesh-viewer/SCR5-J2_cutout_as_built.png
?? work/mesh-viewer/SCR5-J2_print_set.html
?? work/mesh-viewer/SCR5-J2_views.png
?? work/mesh-viewer/SCR5-J3_front_frame.html
?? work/mesh-viewer/SCR5-J3_views.png
?? work/mesh-viewer/SCR5-J3_views2.png
?? work/mesh-viewer/SCR5-J4_front.png
?? work/mesh-viewer/SCR5-J4_front_frame.html
?? work/mesh-viewer/SCR5-J4_print_set.html
?? work/mesh-viewer/SCR5-J4_views.png
?? work/mesh-viewer/SCR5-J5_tray_vs_J4.html
?? work/mesh-viewer/SCR5-WP-A_coupon.html
?? work/mesh-viewer/SCR5-swap_3d_C.png
?? work/mesh-viewer/SCR5-swap_3d_H11.png
?? work/mesh-viewer/SCR5-swap_3d_N.png
?? work/mesh-viewer/SCR5-swap_3d_N2.png
?? work/mesh-viewer/SCR5-swap_3d_S1.png
?? work/mesh-viewer/SCR5-swap_3d_S2.png
?? work/mesh-viewer/SCR5-swap_3d_S3.png
?? work/mesh-viewer/SCR5-swap_S3.html
?? work/mesh-viewer/SCR5-swap_S3.png
?? work/mesh-viewer/SCR5-swap_no_keystone.html
?? work/mesh-viewer/SCR5-swap_no_keystone.png
?? work/mesh-viewer/SCR5-swap_options.html
?? work/mesh-viewer/SCR5-swap_plate_fronts.png
?? work/mesh-viewer/SCR5-swap_side_cuts.png
?? work/mesh-viewer/SCR5_border_measure.png
?? work/mesh-viewer/SCR5_frame_rounded_draft.html
?? work/mesh-viewer/SCR5_frame_rounded_draft.png
?? work/mesh-viewer/SG8-C1_coupon.html
?? work/mesh-viewer/SG8-C1_coupon_assembled.html
?? work/mesh-viewer/SG8-C2_boss.html
?? work/mesh-viewer/SG8-M6-A_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_TL-SG108E_M6.html
?? work/mesh-viewer/SG8-M6-B_screws_fastened.html
?? work/mesh-viewer/SG8-M6-C_tray.html
?? work/mesh-viewer/SG8-M6-D.html
?? work/mesh-viewer/SG8-M6-E_faceplate_on_D_tray.html
?? work/mesh-viewer/SG8-M6-F_on_posts_LOCAL-ONLY.html
?? work/mesh-viewer/SG8-M6-F_post_cheeks.html
?? work/mesh-viewer/SG8-PB-A_post_brackets.html
?? work/mesh-viewer/SG8_B-plate_on_D-tray.html
?? work/mesh-viewer/TF-A.html
?? work/mesh-viewer/TF-B.html
?? work/mesh-viewer/TF-C.html
?? work/mesh-viewer/TF-D.html
?? work/mesh-viewer/TF-D_draft1.html
?? work/mesh-viewer/WMB-A_vs_original.html
?? work/mesh-viewer/faceplate_baseline_vs_CM6B.html
?? work/mesh-viewer/optiplex_rear_R_vs_O.html
?? work/mesh-viewer/printed_brackets_review_2026-10-28.html
?? work/mesh-viewer/task46-reference-regression.html
?? work/rack-finish/Rack_Finish_3D.html
?? work/rack-plan/Rack_B_Wiring_2026-11-04.png
?? work/rack-plan/Rack_Order_Options_2026-11-04.png
?? work/rack-post-hex/
?? work/rack-top-fan/draft_D/
?? work/scr5-access/png/
?? work/scr5-access/stl/
?? work/scr5-swap/stl/
?? work/wire-bracket/
```

## Complete final test output — run 1

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_queue_only_two_statuses_and_empty (tools.bench.test_bench.QueueTests) ... ok
test_queue_order_status_days_latest_and_overdue (tools.bench.test_bench.QueueTests) ... ok
test_queue_tie_order_is_stable (tools.bench.test_bench.QueueTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_only_preserves_all_details_and_notes (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 185 tests in 6.593s

OK

```

## Complete final test output — run 2

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_queue_only_two_statuses_and_empty (tools.bench.test_bench.QueueTests) ... ok
test_queue_order_status_days_latest_and_overdue (tools.bench.test_bench.QueueTests) ... ok
test_queue_tie_order_is_stable (tools.bench.test_bench.QueueTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_only_preserves_all_details_and_notes (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 185 tests in 6.099s

OK

```

## Complete final test output — run 3

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_queue_only_two_statuses_and_empty (tools.bench.test_bench.QueueTests) ... ok
test_queue_order_status_days_latest_and_overdue (tools.bench.test_bench.QueueTests) ... ok
test_queue_tie_order_is_stable (tools.bench.test_bench.QueueTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_only_preserves_all_details_and_notes (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 185 tests in 6.106s

OK

```

## Feature-order test outputs


### Feature 1

```text
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 173 tests in 5.313s

OK

```

### Feature 2

```text
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 174 tests in 5.307s

OK

```

### Feature 3

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 181 tests in 5.962s

OK

```

### Feature 4

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_only_preserves_all_details_and_notes (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 182 tests in 5.938s

OK

```

### Feature 5

```text
test_bad_edits_and_create_share_errors (tools.bench.test_bench.DetailTests) ... ok
test_detail_stale_changes_nothing (tools.bench.test_bench.DetailTests) ... ok
test_details_only_projects_and_backup_changed (tools.bench.test_bench.DetailTests) ... ok
test_edit_each_field_and_rescan (tools.bench.test_bench.DetailTests) ... ok
test_id_and_unknown_fields_rejected (tools.bench.test_bench.DetailTests) ... ok
test_own_prefixes_allowed (tools.bench.test_bench.DetailTests) ... ok
test_workflow_validation_and_continued (tools.bench.test_bench.DetailTests) ... ok
test_attention_draft_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_printing_and_release (tools.bench.test_bench.DiscoveryTests) ... ok
test_attention_report_due (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_seed_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_cache_reused_until_refresh (tools.bench.test_bench.DiscoveryTests) ... ok
test_date_from_folder_beats_viewer_mtime (tools.bench.test_bench.DiscoveryTests) ... ok
test_device_unknown_rows_visible (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_matching_whole_id (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_00 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_01 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_02 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_03 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_04 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_05 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_07 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_08 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_09 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_12 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_13 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_14 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_15 (tools.bench.test_bench.DiscoveryTests) ... ok
test_fit_phrase_16 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CBL_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_Q (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM1P_T5A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6A_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_CM6C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_ER6_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HDT_M6_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_HP4_M6_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MOCA_BC_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_E_P (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_H_RIU (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_MRT_T7 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_D_FRONT (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_OPX_G_L (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PHX_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_PSB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RW_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX4_C (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_RX5_B (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H10 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_H11 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_J5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SCR5_WP_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_C1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_M6_F (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SG8_PB_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_SLV_F_REAR_O (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TFG_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TRE_A (tools.bench.test_bench.DiscoveryTests) ... ok
test_id_TSR_T1 (tools.bench.test_bench.DiscoveryTests) ... ok
test_missing_card_is_plain (tools.bench.test_bench.DiscoveryTests) ... ok
test_newest_readme_unknowns (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_2026_11_06 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CM6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_CSB (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_FP44 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_M6 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_NOTCM6A (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_SCR5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_non_revision_U5 (tools.bench.test_bench.DiscoveryTests) ... ok
test_refresh_never_writes (tools.bench.test_bench.DiscoveryTests) ... ok
test_replacement_mention_not_positive_fit (tools.bench.test_bench.DiscoveryTests) ... ok
test_revisions_deduplicate_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_seed_duplicate_prefix_rejected (tools.bench.test_bench.DiscoveryTests) ... ok
test_supersession_evidence (tools.bench.test_bench.DiscoveryTests) ... ok
test_walk_ignores_app_and_frozen_sources (tools.bench.test_bench.DiscoveryTests) ... ok
test_workflow_excludes_other_project (tools.bench.test_bench.DiscoveryTests) ... ok
test_bad_status_http (tools.bench.test_bench.HttpTests) ... ok
test_bind_loopback (tools.bench.test_bench.HttpTests) ... ok
test_create_http (tools.bench.test_bench.HttpTests) ... ok
test_disallowed_method (tools.bench.test_bench.HttpTests) ... ok
test_encoded_document_link (tools.bench.test_bench.HttpTests) ... ok
test_fit_preview_and_commit_http (tools.bench.test_bench.HttpTests) ... ok
test_invalid_json_http (tools.bench.test_bench.HttpTests) ... ok
test_json_list_rejected (tools.bench.test_bench.HttpTests) ... ok
test_oversize_http (tools.bench.test_bench.HttpTests) ... ok
test_patch_http (tools.bench.test_bench.HttpTests) ... ok
test_path_block_00 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_01 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_02 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_03 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_04 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_05 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_06 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_07 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_08 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_09 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_10 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_11 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_12 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_13 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_14 (tools.bench.test_bench.HttpTests) ... ok
test_path_block_15 (tools.bench.test_bench.HttpTests) ... ok
test_refresh_http (tools.bench.test_bench.HttpTests) ... ok
test_standalone_viewer_bridge_and_sandbox (tools.bench.test_bench.HttpTests) ... ok
test_state_and_project (tools.bench.test_bench.HttpTests) ... ok
test_static_offline (tools.bench.test_bench.HttpTests) ... ok
test_symlink_escape (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_http (tools.bench.test_bench.HttpTests) ... ok
test_unknown_project_write (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_response_only (tools.bench.test_bench.HttpTests) ... ok
test_viewer_bridge_without_body (tools.bench.test_bench.HttpTests) ... ok
test_viewer_is_sandboxed (tools.bench.test_bench.HttpTests) ... ok
test_wrong_content_type (tools.bench.test_bench.HttpTests) ... ok
test_wrong_host (tools.bench.test_bench.HttpTests) ... ok
test_wrong_origin (tools.bench.test_bench.HttpTests) ... ok
test_wrong_token (tools.bench.test_bench.HttpTests) ... ok
test_approved_local_link (tools.bench.test_bench.MarkdownTests) ... ok
test_data_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_headings_lists_tables_code (tools.bench.test_bench.MarkdownTests) ... ok
test_https_link_safe (tools.bench.test_bench.MarkdownTests) ... ok
test_javascript_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_onerror_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_script_escaped (tools.bench.test_bench.MarkdownTests) ... ok
test_unapproved_local_link_inert (tools.bench.test_bench.MarkdownTests) ... ok
test_workflow_continuation_merge (tools.bench.test_bench.MarkdownTests) ... ok
test_queue_only_two_statuses_and_empty (tools.bench.test_bench.QueueTests) ... ok
test_queue_order_status_days_latest_and_overdue (tools.bench.test_bench.QueueTests) ... ok
test_queue_tie_order_is_stable (tools.bench.test_bench.QueueTests) ... ok
test_atomic_replace_failure_rolls_back (tools.bench.test_bench.WriteTests) ... ok
test_blank_process_fields_unknown (tools.bench.test_bench.WriteTests) ... ok
test_concurrent_save_one_wins (tools.bench.test_bench.WriteTests) ... ok
test_create_stale (tools.bench.test_bench.WriteTests) ... ok
test_disallowed_write_target (tools.bench.test_bench.WriteTests) ... ok
test_failed_staging_leaves_originals (tools.bench.test_bench.WriteTests) ... ok
test_fit_stale_each_file_preflight (tools.bench.test_bench.WriteTests) ... ok
test_hardlink_target_refused (tools.bench.test_bench.WriteTests) ... ok
test_missing_final_newline_preserves_bytes (tools.bench.test_bench.WriteTests) ... ok
test_missing_hashes (tools.bench.test_bench.WriteTests) ... ok
test_new_project_success (tools.bench.test_bench.WriteTests) ... ok
test_no_workflow_section_no_workflow_write (tools.bench.test_bench.WriteTests) ... ok
test_notes_unicode (tools.bench.test_bench.WriteTests) ... ok
test_preview_writes_nothing (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_result (tools.bench.test_bench.WriteTests) ... ok
test_reject_bad_status (tools.bench.test_bench.WriteTests) ... ok
test_reject_control_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_decimal_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_id (tools.bench.test_bench.WriteTests) ... ok
test_reject_duplicate_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_patch (tools.bench.test_bench.WriteTests) ... ok
test_reject_empty_title (tools.bench.test_bench.WriteTests) ... ok
test_reject_excess_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_extra_key (tools.bench.test_bench.WriteTests) ... ok
test_reject_long_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_missing_card (tools.bench.test_bench.WriteTests) ... ok
test_reject_nan_infill (tools.bench.test_bench.WriteTests) ... ok
test_reject_negative_walls (tools.bench.test_bench.WriteTests) ... ok
test_reject_newline_where (tools.bench.test_bench.WriteTests) ... ok
test_reject_numeric_notes (tools.bench.test_bench.WriteTests) ... ok
test_reject_overlapping_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_prefix_string (tools.bench.test_bench.WriteTests) ... ok
test_reject_repeated_prefix (tools.bench.test_bench.WriteTests) ... ok
test_reject_source_escape (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_project_revision (tools.bench.test_bench.WriteTests) ... ok
test_reject_unknown_revision (tools.bench.test_bench.WriteTests) ... ok
test_report_changed_only_allowlist (tools.bench.test_bench.WriteTests) ... ok
test_report_crlf (tools.bench.test_bench.WriteTests) ... ok
test_report_escape_markdown (tools.bench.test_bench.WriteTests) ... ok
test_report_exact_append_and_backup (tools.bench.test_bench.WriteTests) ... ok
test_status_backup_only_expected_files (tools.bench.test_bench.WriteTests) ... ok
test_status_only_preserves_all_details_and_notes (tools.bench.test_bench.WriteTests) ... ok
test_status_stale (tools.bench.test_bench.WriteTests) ... ok
test_workflow_continuation_visible (tools.bench.test_bench.WriteTests) ... ok

----------------------------------------------------------------------
Ran 185 tests in 6.195s

OK

```

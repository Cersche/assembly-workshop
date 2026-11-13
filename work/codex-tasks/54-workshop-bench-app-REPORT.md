# Task 54 — Workshop Bench completion report

2026-11-07. Verification of the existing implementation; no application, seed, launcher, README, PROJECT.md, test or acceptance-harness edits were needed. No commit, push, pull, HANDOFF edit, installation, production-data write or production export. The explicit task scope supersedes the standing session sync instructions.

## Result

PASS: 171 Bench tests (5.542 s); 25 existing release/library regression tests (13.840 s); real-root HTTP reads; temporary-root writes with every diff, backups and append-only checks. Python 3.10.4. All 21 seeded projects / 183 distinct revision entries loaded. No scan errors. First real HTTP state load 0.664935 s (scan 0.634434 s); cached load 0.009085 s. This meets the one-second API/data-load target on this run; it is not a measured full-browser paint guarantee.

Browser: every one of 21 project screens plus the acceptance-only project clicked at 1280x900 and 375x900. Document scroll widths were respectively 1265 and 360 pixels, with no horizontal page overflow. New project dialog, empty search, revision selection, exact fit preview, invalid revision rejection, and remembered done filter checked. No captured console warnings/errors. Browser writes were not repeated: all three writes were exercised through HTTP against the same disposable root. Browser fit previews were not saved.

## Files

Existing task deliverables verified and left unchanged: tools/bench/bench.py; tools/bench/test_bench.py; tools/bench/acceptance.py; tools/bench/static/index.html; tools/bench/static/bench.css; tools/bench/static/bench.js; tools/bench/start.bat; tools/bench/README.md; work/bench/projects.json; existing Workshop Bench entry in .claude/launch.json and PROJECT.md paragraph.

Created this report and work/codex-tasks/54-screens/finish-* screenshots plus finish-click-through.json. Earlier screenshots and click-through.json were already present and were preserved; their results are not represented as this run. No files in outputs/, data/, lib/, SCAD sources or other tools were edited. The regression tests use their existing dependencies and temporary geometry; the Bench app, tests and acceptance harness use Python standard library only. No dependencies were added.

## Preservation and execution details

Before and after the real HTTP acceptance, and again after temp writes, git status --porcelain and both SHA-256 values matched exactly. They also matched immediately before writing this report, after browser screenshots. The final git status necessarily adds this requested report; that is not an application-side write. The full before/after status appears in the acceptance transcript below.

Initial sandbox runs failed with WinError 5 on temporary os.replace / rename and WinError 10013 on localhost sockets. A second explicitly writable scratch-root run reproduced the sandbox restriction. Running the same unchanged code with approved execution outside the sandbox passed all 171 tests. These were environment errors, not fixed by weakening atomic writes. One subsequent acceptance attempt refused occupied port 8720. The process was identified as the prior task-54 temp server rooted at C:/Users/brian/AppData/Local/Temp/bench54-verification/http3/repo, then stopped; acceptance was rerun successfully.

The metadata copy includes full docs/, work/bench/, work/workbench/, HANDOFF, scanned output READMEs/reports and filenames. Mesh/3MF bytes were not copied. Viewer HTML in the copy is explicitly synthetic, preserving filenames/timestamps, so iframe transport can be tested without copying licensed meshes. Thus real WebGL/geometry rendering is not verified by this browser run.

Evidence retained outside the repository: C:\Users\brian\.codex\visualizations\2026\11\07\01a1b870-4cb4-7e52-871a-ab58cc2023d6\bench54-unrestricted. Successful HTTP evidence and exact per-write diffs are embedded below. Full-copy smoke after acceptance: 22 projects including Acceptance sample; 183 revisions; 0.815811 s. Before mutation the temp copy revision counts equalled all real-root counts.

## Seeded jobs, confidence and revision counts

These are the existing seed decisions, reviewed against current HANDOFF, Fit_Findings, Workflow_Log, all six device cards, Final_3MF README/listing and git history since 2026-10-20. Counts include component IDs, mentions and historical aliases; they are not counts of prints or approved releases. Notes explicitly distinguish inference from evidence.

| Job / prefixes | Status | Revisions | Inference and confidence |
| --- | --- | ---: | --- |
| Cable span bracket (`csb`; CSB) | printing | 2 | Seeded by Codex, check: High: CSB-B released 2026-11-05; CSB-A fits but no driver access. Awaiting B report. HANDOFF and workflow log agree. |
| MoCA rack tray (`mrt`; MRT) | draft | 29 | Seeded by Codex, check: High identity, medium status: spec requests draft; newer HANDOFF says MRT-H and T5-T7 released for printing 2026-11-06. 2U rear-splitter concept remains discussion. Rear keystones dropped; f-keystone-coupler card is historical, not a current dependency. |
| Rack top for a 200 mm fan (`fan`; TFE, TRE, TSR, TFG) | draft | 6 | Seeded by Codex, check: High: draft 4, TFE-A TRE-A TSR-A TFG-A; coupons TFE-T1 TSR-T1. Task 53 dry runs are not releases. No print or release. |
| OptiPlex rear channels (`opx`; OPX, SLV) | draft | 44 | Seeded by Codex, check: High: OPX-G channels unprinted, reuses printed OPX-D sleeve and OPX-F rails (good fit). No dedicated device card found. |
| Screen, Pi and Hue (`scr5`; SCR5) | draft | 18 | Seeded by Codex, check: High: SCR5-J5 tray loosens J4 Hue cradle; J5 unprinted. Other J4/H8 parts retained. Missing dedicated device card; screen dimensions live in work/screen-5in/Dimensions.md. |
| ER605 router bracket (`er6`; ER6) | draft | 8 | Seeded by Codex, check: High: ER6-H three floor slots, unprinted. Measurements in Fit_Findings; no device card. |
| CM1000 modem bracket and lights (`cm1000`; CM1P, CM6) | draft | 36 | Seeded by Codex, check: High: CM1P-Q white liners current and unprinted; O fit report is specimen-specific. CM6A/C do not print; T8 diffuser scratched. No dedicated device card. Referenced source absent: outputs/CM1000_OnePiece_CM1P-Q_2026-11-03/src/CM1P-Q.scad. |
| Power strip bracket (`psb`; PSB) | draft | 1 | Seeded by Codex, check: High: PSB-A first unprinted draft; keyhole lip/foot dimensions and wall details unresolved. No device card. |
| MoCA receiver box (`rx5`; RX4, RX5) | draft | 6 | Seeded by Codex, check: High: RX5-B rear ports, replaces blocked RX5-A. Unprinted; separate from rack and wall box. TL-SG105 card missing. |
| Chess clock switch (`chs`; CHS) | idea | 0 | Seeded by Codex, check: Low: explicitly requested by task 54, but no CHS source, release or device card in this checkout. No revision invented. |
| Flat wire bracket (`wmb`; WMB) | idea | 0 | Seeded by Codex, check: Low: explicitly requested by task 54, but no WMB source, release or card in this checkout. No revision invented. |
| TL-SG108E switch tray (`sg8`; SG8, KD) | done | 15 | Seeded by Codex, check: High identity; done per requested seed. SG8-M6-F tray and M6 screws fit per Brian 2026-11-05; other properties remain UNKNOWN. KD keyhole coupons grouped here from Fit_Findings. |
| Drive tray (`hdt`; HDT) | done | 1 | Seeded by Codex, check: High identity, low physical completion: done is the requested organizational status; HDT-M6-A README/HANDOFF say approved but not printed. Historical 2026-10-25 tray fit does not prove M6 revision. |
| Post hex anti-warp concept (`phx`; PHX) | parked | 3 | Seeded by Codex, check: Medium: HANDOFF identifies PHX-C latest concept, someday rebuild only. work/rack-post-hex is missing in this checkout; no source path invented. Warp benefit UNKNOWN. |
| Rack wall mount (`rw`; RW) | draft | 3 | Seeded by Codex, check: High identity, medium activity: RW-WP-A / RW-RC-A / RW-SO-A cleat and standoffs chosen, not printed; HANDOFF 2026-10-30. U1 conflicts with CBL-B. |
| MoCA wall box and cleat (`moca-wall`; MOCA) | draft | 2 | Seeded by Codex, check: High identity, medium current status: MOCA-BC-A and MOCA-WP-A cleat accepted, unprinted. Earlier sleeve/cradle/porch prints have names rather than revision IDs; not silently numbered. Separate job from RX5. |
| Rear cable management lanes (`cbl`; CBL) | draft | 7 | Seeded by Codex, check: High identity, medium activity: CBL-A through E, unprinted; source README records wall-mount and post-hole conflicts. Separate from front-to-rear CSB. |
| Hue and Pi tray (reference) (`hp4`; HP4) | parked | 2 | Seeded by Codex, check: High history, medium parked classification: HP4-M6-B default was superseded by combined SCR5 unit; Final_3MF keeps A/B references. Frozen source confirmed in its output folder. |
| Rack LED matrix crown (`crn`; CRN) | idea | 0 | Seeded by Codex, check: Medium: CRN-E concept header dated 2026-10-30, MAX7219 carrier in stock top beam, unprinted. Confirm whether still wanted alongside the redesigned fan top. |
| Extrusion rack frame (`frame`; none) | idea | 0 | Seeded by Codex, check: Medium: work/rack-frame/BOM.md records option A chosen 2026-10-31; no reliable revision prefix, so none invented. Alternative metal-corner concept also listed. Confirm activity. |
| Matching bottom intake grille (`bottom`; none) | parked | 0 | Seeded by Codex, check: High intent, medium status: Brian requested matching bottom after the top prints, 2026-11-06. No modeled revision or prefix yet; parked until then. |

### Cards and sources per seed

- **csb** — cards: `docs/devices/lab-rax-4u-post.md`; sources: `work/cable-span-bracket/span_bracket.scad`.
- **mrt** — cards: `docs/devices/screenbeam-ecb7250.md`, `docs/devices/bridgelink-2way-splitter.md`; sources: `work/moca-rack-tray/MRT.scad`.
- **fan** — cards: `docs/devices/lab-rax-top.md`, `docs/devices/fan-200mm.md`; sources: `work/rack-top-fan/rack_top_fan.scad`.
- **opx** — cards: none; sources: `outputs/OptiPlex_Sleeve_Channels_OPX-G_2026-11-04/src/OPX-G.scad`.
- **scr5** — cards: none; sources: `outputs/Screen_Pi_Hue_SCR5-J5_2026-11-05/src/SCR5-J5.scad`.
- **er6** — cards: none; sources: `outputs/ER605_Bracket_ER6-H_2026-11-04/src/ER6-H.scad`.
- **cm1000** — cards: none; sources: none.
- **psb** — cards: none; sources: `outputs/Power_Strip_Bracket_PSB-A_2026-11-03/src/psb_a.scad`.
- **rx5** — cards: `docs/devices/screenbeam-ecb7250.md`; sources: `work/wall-box-wizard/receiver1/rx5.scad`.
- **chs** — cards: none; sources: none.
- **wmb** — cards: none; sources: none.
- **sg8** — cards: `docs/devices/lab-rax-4u-post.md`; sources: `outputs/Chunky_Revisions/TL-SG108E_post_rails_2026-10-30/src/SG8-M6-F.scad`.
- **hdt** — cards: none; sources: `outputs/Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A.scad`.
- **phx** — cards: none; sources: none.
- **rw** — cards: `docs/devices/lab-rax-4u-post.md`; sources: `work/rack-wall-mount/rwm1.scad`.
- **moca-wall** — cards: `docs/devices/screenbeam-ecb7250.md`, `docs/devices/bridgelink-2way-splitter.md`; sources: `work/wall-box-wizard/concept15/cleat16.scad`, `work/wall-box-wizard/concept15/body15.scad`.
- **cbl** — cards: `docs/devices/lab-rax-4u-post.md`; sources: `outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-A.scad`, `outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-BCDE.scad`.
- **hp4** — cards: none; sources: `outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad`.
- **crn** — cards: none; sources: `work/rgb-crown/crn_e.scad`.
- **frame** — cards: none; sources: `work/rack-frame/BOM.md`.
- **bottom** — cards: none; sources: `work/rack-cooling/Decisions.md`.

## Revision audit and IDs not placed

All 183 recognized IDs in the copied scanned output text/listings, HANDOFF, fit/workflow logs and viewer filenames occur in the discovery result; recognized-but-absent list: []. All project revision IDs are distinct within their owning project. The unit suite covers CM6A, whole-token CM1P-T1/T10 and SCR5-H/H10 boundaries and rejection of M6/U5/FP44.

Independent broad uppercase/hyphen candidate extraction across HANDOFF, Final_3MF README and filenames, fit log and workflow log left these tokens unplaced (listed exhaustively for that corpus): `A-D`, `A-H`, `B-E`, `BY-NC-SA`, `LOCAL-ONLY`, `M6-B`, `REAR-O`, `T5-T7`, `TL-SG105`, `TL-SG108E`, `U4-U3`, `U6-U5`, `USB-SATA`, `Z159-196`, `Z171-193`.

Classification: A-D, A-H, B-E and T5-T7 are ranges/shorthand; M6-B and REAR-O are incomplete/context-dependent revision suffixes; BY-NC-SA and LOCAL-ONLY are license/local labels; TL-SG105 and TL-SG108E are equipment model names; U4-U3 and U6-U5 are slot ranges; USB-SATA is an interface label; Z159-196 and Z171-193 are coordinates. Do not silently invent separate revisions from these tokens. Bare M6/U5/FP44 are not project revisions.

Known source-only exception: CRN-E is explicitly referenced by the existing crown seed but has zero discovered revisions because discovery does not read SCAD source contents. Earlier receiver concepts RX1/RX2/RX3 and bare RX4/RX5 are concept names, not complete seeded revision IDs. Historical MoCA sleeve/cradle/porch names and unnumbered builds are not uniquely assignable IDs. An exhaustive semantic inventory of all historic unnamed parts is not claimed.

## Gaps and decisions for Brian or Claude

- Confirm MRT status: requested draft conflicts with newer MRT-H/T5-T7 release-for-printing evidence. Seed deliberately preserves draft and explains the conflict.
- Confirm HDT done as organizational status only: M6 revision remains unprinted in the cited history. SG8 done does not certify strength or all components.
- Confirm grouping KD with SG8; reference HP4 parked; separate RX5, MoCA wall box and MRT jobs; whether crown/extrusion-frame/bottom projects remain wanted. CHS/WMB have no located source/card/revision.
- Decide whether source-only CRN-E, abbreviated ranges and filename aliases deserve explicit curated metadata. No SCAD scan or guessed expansion was added. OPX has 44 entries partly because component/alias IDs remain distinct.
- Device cards remain missing for several jobs; f-keystone-coupler.md is historical after rear keystones were dropped and is intentionally not a current MRT dependency. Missing source mentioned in CM1000 notes and PHX missing folder were not invented.
- Workflow appends use a same-title continued section at EOF, merged for display. Confirm this resolution of append-only versus insertion-in-section requirements. Existing markdown bytes are preserved.
- Each file replacement is atomic, but a multi-file fit report is not crash-atomic as a group; documented rollback handles caught failures, not power loss or the final external-editor race. Confirm this documented limitation for v1.
- Fit labels remain heuristic and can miss descriptive results or overconservatively warn on historical supersession mentions. All matched evidence stays visible; no physical approval or strength is inferred.
- Browser testing used synthetic viewer pages. Real mesh rendering, exhaustive keyboard-only navigation, every touch-target measurement and both light/dark contrast matrices were not separately certified. Existing CSS and offline implementation were left unchanged because executed checks passed.
- The private mockup was not opened in this completion pass; the task-provided layout and existing interface were used. No app redesign was attempted.

## New browser evidence

All screenshots below are this completion run; pre-existing PNGs remain untouched. Raw per-project viewport measurements: [finish-click-through.json](54-screens/finish-click-through.json).

- [finish-1280-empty.jpg](54-screens/finish-1280-empty.jpg)
- [finish-1280-new.jpg](54-screens/finish-1280-new.jpg)
- [finish-1280-preview.jpg](54-screens/finish-1280-preview.jpg)
- [finish-1280-project.jpg](54-screens/finish-1280-project.jpg)
- [finish-375-invalid.jpg](54-screens/finish-375-invalid.jpg)
- [finish-375-new.jpg](54-screens/finish-375-new.jpg)
- [finish-375-preview.jpg](54-screens/finish-375-preview.jpg)
- [finish-375-project.jpg](54-screens/finish-375-project.jpg)

## Bench unittest output

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
Ran 171 tests in 5.542s

OK

```

## HTTP acceptance, checkpoints and every write diff

```text
BEFORE REAL READ ACCEPTANCE
{
  "git_status": " M .claude/launch.json\n M PROJECT.md\n?? tools/bench/\n?? work/bench/\n?? work/codex-tasks/54-screens/\n?? work/mesh-viewer/CM6A_task43_reference.html\n?? work/mesh-viewer/CM6A_vs_CM6B.html\n?? work/mesh-viewer/SCR5-A-assembled.html\n?? work/mesh-viewer/SCR5-A-front.html\n?? work/mesh-viewer/SCR5-A-index.html\n?? work/mesh-viewer/SCR5-A-initial-probe.html\n?? work/mesh-viewer/SCR5-A-print.html\n?? work/mesh-viewer/SCR5-A-probes.html\n?? work/mesh-viewer/SCR5-A-rear.html\n?? work/mesh-viewer/SCR5-A-rejected-bridge.html\n?? work/mesh-viewer/SCR5-A-review.html\n?? work/mesh-viewer/SCR5-B-assembled.html\n?? work/mesh-viewer/SCR5-B-front.html\n?? work/mesh-viewer/SCR5-B-index.html\n?? work/mesh-viewer/SCR5-B-preservation.html\n?? work/mesh-viewer/SCR5-B-print.html\n?? work/mesh-viewer/SCR5-B-probes.html\n?? work/mesh-viewer/SCR5-B-rear.html\n?? work/mesh-viewer/SCR5-B-rear.png\n?? work/mesh-viewer/SCR5-B-review.html\n?? work/mesh-viewer/task44-hdt-preservation.html\n?? work/mesh-viewer/task44-rejected-trial-and-colours.html\n?? work/mesh-viewer/task44-revision2-hdt.html\n?? work/mesh-viewer/task53-rack-top-fan-assembly.html\n?? work/mesh-viewer/task53-rack-top-fan-parts.html\n?? work/rack-top-fan/task53-scratch/\n?? work/screen-5in/local-preservation-20261029/\n?? work/task37-screenshots/\n",
  "markdown": {
    "docs/Fit_Findings.md": "af8b77abcf9a1b76e817bd2cc075d841760d5c4a88f6567a95fba8894ec4f6d7",
    "work/workbench/Workflow_Log.md": "2df2ad2aeb4c632ee677f04ab9d6b8cd7d3f64a0c5d1578a8cfef76257d04434"
  }
}
Workshop Bench: http://127.0.0.1:8720 (root: C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop)
GET /api/state first: 200, 0.664935 s, scan 0.634434 s, 267198 bytes
GET /api/state cached: 200, 0.009085 s
GET /api/health: 200, 0.010984 s, 40 bytes
GET /api/projects: 200, 0.007892 s, 267198 bytes
GET /: 200, 0.001429 s, 2380 bytes
GET /static/bench.css: 200, 0.001316 s, 5445 bytes
GET /static/bench.js: 200, 0.017258 s, 12570 bytes
GET /api/projects/csb: 200, 0.001804 s, 11269 bytes
GET /api/projects/mrt: 200, 0.002467 s, 34504 bytes
GET /api/projects/fan: 200, 0.011352 s, 21487 bytes
GET /api/projects/opx: 200, 0.002131 s, 32485 bytes
GET /api/projects/scr5: 200, 0.025236 s, 23341 bytes
GET /api/projects/er6: 200, 0.001342 s, 11126 bytes
GET /api/projects/cm1000: 200, 0.001814 s, 42619 bytes
GET /api/projects/psb: 200, 0.000981 s, 5490 bytes
GET /api/projects/rx5: 200, 0.001619 s, 12411 bytes
GET /api/projects/chs: 200, 0.001211 s, 873 bytes
GET /api/projects/wmb: 200, 0.001191 s, 865 bytes
GET /api/projects/sg8: 200, 0.001894 s, 16991 bytes
GET /api/projects/hdt: 200, 0.001449 s, 8348 bytes
GET /api/projects/phx: 200, 0.001371 s, 2072 bytes
GET /api/projects/rw: 200, 0.024213 s, 5641 bytes
GET /api/projects/moca-wall: 200, 0.011194 s, 7338 bytes
GET /api/projects/cbl: 200, 0.012117 s, 8000 bytes
GET /api/projects/hp4: 200, 0.001504 s, 7322 bytes
GET /api/projects/crn: 200, 0.001152 s, 951 bytes
GET /api/projects/frame: 200, 0.020015 s, 954 bytes
GET /api/projects/bottom: 200, 0.001308 s, 943 bytes
GET text docs/Fit_Findings.md: 200, 0.001711 s
GET text work/workbench/Workflow_Log.md: 200, 0.001843 s
GET text HANDOFF.md: 200, 0.001376 s
GET text outputs/Final_3MF/README.md: 200, 0.012482 s
POST /api/refresh (read-only): 200, 0.629279 s
POST /api/fit-report/preview (read-only): 200, 0.001451 s
AFTER REAL READ ACCEPTANCE
{
  "git_status": " M .claude/launch.json\n M PROJECT.md\n?? tools/bench/\n?? work/bench/\n?? work/codex-tasks/54-screens/\n?? work/mesh-viewer/CM6A_task43_reference.html\n?? work/mesh-viewer/CM6A_vs_CM6B.html\n?? work/mesh-viewer/SCR5-A-assembled.html\n?? work/mesh-viewer/SCR5-A-front.html\n?? work/mesh-viewer/SCR5-A-index.html\n?? work/mesh-viewer/SCR5-A-initial-probe.html\n?? work/mesh-viewer/SCR5-A-print.html\n?? work/mesh-viewer/SCR5-A-probes.html\n?? work/mesh-viewer/SCR5-A-rear.html\n?? work/mesh-viewer/SCR5-A-rejected-bridge.html\n?? work/mesh-viewer/SCR5-A-review.html\n?? work/mesh-viewer/SCR5-B-assembled.html\n?? work/mesh-viewer/SCR5-B-front.html\n?? work/mesh-viewer/SCR5-B-index.html\n?? work/mesh-viewer/SCR5-B-preservation.html\n?? work/mesh-viewer/SCR5-B-print.html\n?? work/mesh-viewer/SCR5-B-probes.html\n?? work/mesh-viewer/SCR5-B-rear.html\n?? work/mesh-viewer/SCR5-B-rear.png\n?? work/mesh-viewer/SCR5-B-review.html\n?? work/mesh-viewer/task44-hdt-preservation.html\n?? work/mesh-viewer/task44-rejected-trial-and-colours.html\n?? work/mesh-viewer/task44-revision2-hdt.html\n?? work/mesh-viewer/task53-rack-top-fan-assembly.html\n?? work/mesh-viewer/task53-rack-top-fan-parts.html\n?? work/rack-top-fan/task53-scratch/\n?? work/screen-5in/local-preservation-20261029/\n?? work/task37-screenshots/\n",
  "markdown": {
    "docs/Fit_Findings.md": "af8b77abcf9a1b76e817bd2cc075d841760d5c4a88f6567a95fba8894ec4f6d7",
    "work/workbench/Workflow_Log.md": "2df2ad2aeb4c632ee677f04ab9d6b8cd7d3f64a0c5d1578a8cfef76257d04434"
  }
}
PASS: git status and both markdown SHA-256 hashes unchanged.

TEMP COPY ACCEPTANCE
Workshop Bench: http://127.0.0.1:8720 (root: C:\Users\brian\.codex\visualizations\2026\11\07\01a1b870-4cb4-7e52-871a-ab58cc2023d6\bench54-unrestricted\http2\repo)
GET /api/state first: 200, 0.631550 s, scan 0.623036 s, 267198 bytes
GET /api/state cached: 200, 0.008238 s
GET /api/health: 200, 0.001181 s, 40 bytes
GET /api/projects: 200, 0.007798 s, 267198 bytes
GET /: 200, 0.011714 s, 2380 bytes
GET /static/bench.css: 200, 0.012270 s, 5445 bytes
GET /static/bench.js: 200, 0.001435 s, 12570 bytes
GET /api/projects/csb: 200, 0.001094 s, 11269 bytes
GET /api/projects/mrt: 200, 0.026388 s, 34504 bytes
GET /api/projects/fan: 200, 0.012453 s, 21487 bytes
GET /api/projects/opx: 200, 0.001990 s, 32485 bytes
GET /api/projects/scr5: 200, 0.002052 s, 23341 bytes
GET /api/projects/er6: 200, 0.001421 s, 11126 bytes
GET /api/projects/cm1000: 200, 0.002012 s, 42619 bytes
GET /api/projects/psb: 200, 0.001111 s, 5490 bytes
GET /api/projects/rx5: 200, 0.020743 s, 12411 bytes
GET /api/projects/chs: 200, 0.001013 s, 873 bytes
GET /api/projects/wmb: 200, 0.001011 s, 865 bytes
GET /api/projects/sg8: 200, 0.001677 s, 16991 bytes
GET /api/projects/hdt: 200, 0.001246 s, 8348 bytes
GET /api/projects/phx: 200, 0.001178 s, 2072 bytes
GET /api/projects/rw: 200, 0.012347 s, 5641 bytes
GET /api/projects/moca-wall: 200, 0.001061 s, 7338 bytes
GET /api/projects/cbl: 200, 0.012927 s, 8000 bytes
GET /api/projects/hp4: 200, 0.001273 s, 7322 bytes
GET /api/projects/crn: 200, 0.001154 s, 951 bytes
GET /api/projects/frame: 200, 0.001024 s, 954 bytes
GET /api/projects/bottom: 200, 0.016930 s, 943 bytes
GET text docs/Fit_Findings.md: 200, 0.001705 s
GET text work/workbench/Workflow_Log.md: 200, 0.020178 s
GET text HANDOFF.md: 200, 0.012745 s
GET text outputs/Final_3MF/README.md: 200, 0.001524 s
PASS: copy revision counts match the real read-only scan.
PATCH /api/projects/csb: 200, 0.014290 s
{
  "id": "csb",
  "title": "Cable span bracket",
  "prefixes": [
    "CSB"
  ],
  "status": "report-due",
  "device_cards": [
    "docs/devices/lab-rax-4u-post.md"
  ],
  "sources": [
    "work/cable-span-bracket/span_bracket.scad"
  ],
  "workflow_log": "Cable management bracket (front to rear posts)",
  "notes": "Temporary acceptance note; never the real repo.",
  "updated": "2026-11-07"
}

DIFF work/bench/projects.json
--- work/bench/projects.json before
+++ work/bench/projects.json after
@@ -1,336 +1,336 @@
-{

-  "version": 1,

-  "projects": [

-    {

-      "id": "csb",

-      "title": "Cable span bracket",

-      "prefixes": [

-        "CSB"

-      ],

-      "status": "printing",

-      "device_cards": [

-        "docs/devices/lab-rax-4u-post.md"

-      ],

-      "sources": [

-        "work/cable-span-bracket/span_bracket.scad"

-      ],

-      "workflow_log": "Cable management bracket (front to rear posts)",

-      "notes": "Seeded by Codex, check: High: CSB-B released 2026-11-05; CSB-A fits but no driver access. Awaiting B report. HANDOFF and workflow log agree.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "mrt",

-      "title": "MoCA rack tray",

-      "prefixes": [

-        "MRT"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/screenbeam-ecb7250.md",

-        "docs/devices/bridgelink-2way-splitter.md"

-      ],

-      "sources": [

-        "work/moca-rack-tray/MRT.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity, medium status: spec requests draft; newer HANDOFF says MRT-H and T5-T7 released for printing 2026-11-06. 2U rear-splitter concept remains discussion. Rear keystones dropped; f-keystone-coupler card is historical, not a current dependency.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "fan",

-      "title": "Rack top for a 200 mm fan",

-      "prefixes": [

-        "TFE",

-        "TRE",

-        "TSR",

-        "TFG"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/lab-rax-top.md",

-        "docs/devices/fan-200mm.md"

-      ],

-      "sources": [

-        "work/rack-top-fan/rack_top_fan.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: draft 4, TFE-A TRE-A TSR-A TFG-A; coupons TFE-T1 TSR-T1. Task 53 dry runs are not releases. No print or release.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "opx",

-      "title": "OptiPlex rear channels",

-      "prefixes": [

-        "OPX",

-        "SLV"

-      ],

-      "status": "draft",

-      "device_cards": [],

-      "sources": [

-        "outputs/OptiPlex_Sleeve_Channels_OPX-G_2026-11-04/src/OPX-G.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: OPX-G channels unprinted, reuses printed OPX-D sleeve and OPX-F rails (good fit). No dedicated device card found.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "scr5",

-      "title": "Screen, Pi and Hue",

-      "prefixes": [

-        "SCR5"

-      ],

-      "status": "draft",

-      "device_cards": [],

-      "sources": [

-        "outputs/Screen_Pi_Hue_SCR5-J5_2026-11-05/src/SCR5-J5.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: SCR5-J5 tray loosens J4 Hue cradle; J5 unprinted. Other J4/H8 parts retained. Missing dedicated device card; screen dimensions live in work/screen-5in/Dimensions.md.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "er6",

-      "title": "ER605 router bracket",

-      "prefixes": [

-        "ER6"

-      ],

-      "status": "draft",

-      "device_cards": [],

-      "sources": [

-        "outputs/ER605_Bracket_ER6-H_2026-11-04/src/ER6-H.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: ER6-H three floor slots, unprinted. Measurements in Fit_Findings; no device card.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "cm1000",

-      "title": "CM1000 modem bracket and lights",

-      "prefixes": [

-        "CM1P",

-        "CM6"

-      ],

-      "status": "draft",

-      "device_cards": [],

-      "sources": [],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: CM1P-Q white liners current and unprinted; O fit report is specimen-specific. CM6A/C do not print; T8 diffuser scratched. No dedicated device card. Referenced source absent: outputs/CM1000_OnePiece_CM1P-Q_2026-11-03/src/CM1P-Q.scad.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "psb",

-      "title": "Power strip bracket",

-      "prefixes": [

-        "PSB"

-      ],

-      "status": "draft",

-      "device_cards": [],

-      "sources": [

-        "outputs/Power_Strip_Bracket_PSB-A_2026-11-03/src/psb_a.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: PSB-A first unprinted draft; keyhole lip/foot dimensions and wall details unresolved. No device card.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "rx5",

-      "title": "MoCA receiver box",

-      "prefixes": [

-        "RX4",

-        "RX5"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/screenbeam-ecb7250.md"

-      ],

-      "sources": [

-        "work/wall-box-wizard/receiver1/rx5.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High: RX5-B rear ports, replaces blocked RX5-A. Unprinted; separate from rack and wall box. TL-SG105 card missing.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "chs",

-      "title": "Chess clock switch",

-      "prefixes": [

-        "CHS"

-      ],

-      "status": "idea",

-      "device_cards": [],

-      "sources": [],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: Low: explicitly requested by task 54, but no CHS source, release or device card in this checkout. No revision invented.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "wmb",

-      "title": "Flat wire bracket",

-      "prefixes": [

-        "WMB"

-      ],

-      "status": "idea",

-      "device_cards": [],

-      "sources": [],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: Low: explicitly requested by task 54, but no WMB source, release or card in this checkout. No revision invented.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "sg8",

-      "title": "TL-SG108E switch tray",

-      "prefixes": [

-        "SG8",

-        "KD"

-      ],

-      "status": "done",

-      "device_cards": [

-        "docs/devices/lab-rax-4u-post.md"

-      ],

-      "sources": [

-        "outputs/Chunky_Revisions/TL-SG108E_post_rails_2026-10-30/src/SG8-M6-F.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity; done per requested seed. SG8-M6-F tray and M6 screws fit per Brian 2026-11-05; other properties remain UNKNOWN. KD keyhole coupons grouped here from Fit_Findings.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "hdt",

-      "title": "Drive tray",

-      "prefixes": [

-        "HDT"

-      ],

-      "status": "done",

-      "device_cards": [],

-      "sources": [

-        "outputs/Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity, low physical completion: done is the requested organizational status; HDT-M6-A README/HANDOFF say approved but not printed. Historical 2026-10-25 tray fit does not prove M6 revision.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "phx",

-      "title": "Post hex anti-warp concept",

-      "prefixes": [

-        "PHX"

-      ],

-      "status": "parked",

-      "device_cards": [],

-      "sources": [],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: Medium: HANDOFF identifies PHX-C latest concept, someday rebuild only. work/rack-post-hex is missing in this checkout; no source path invented. Warp benefit UNKNOWN.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "rw",

-      "title": "Rack wall mount",

-      "prefixes": [

-        "RW"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/lab-rax-4u-post.md"

-      ],

-      "sources": [

-        "work/rack-wall-mount/rwm1.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity, medium activity: RW-WP-A / RW-RC-A / RW-SO-A cleat and standoffs chosen, not printed; HANDOFF 2026-10-30. U1 conflicts with CBL-B.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "moca-wall",

-      "title": "MoCA wall box and cleat",

-      "prefixes": [

-        "MOCA"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/screenbeam-ecb7250.md",

-        "docs/devices/bridgelink-2way-splitter.md"

-      ],

-      "sources": [

-        "work/wall-box-wizard/concept15/cleat16.scad",

-        "work/wall-box-wizard/concept15/body15.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity, medium current status: MOCA-BC-A and MOCA-WP-A cleat accepted, unprinted. Earlier sleeve/cradle/porch prints have names rather than revision IDs; not silently numbered. Separate job from RX5.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "cbl",

-      "title": "Rear cable management lanes",

-      "prefixes": [

-        "CBL"

-      ],

-      "status": "draft",

-      "device_cards": [

-        "docs/devices/lab-rax-4u-post.md"

-      ],

-      "sources": [

-        "outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-A.scad",

-        "outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-BCDE.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High identity, medium activity: CBL-A through E, unprinted; source README records wall-mount and post-hole conflicts. Separate from front-to-rear CSB.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "hp4",

-      "title": "Hue and Pi tray (reference)",

-      "prefixes": [

-        "HP4"

-      ],

-      "status": "parked",

-      "device_cards": [],

-      "sources": [

-        "outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High history, medium parked classification: HP4-M6-B default was superseded by combined SCR5 unit; Final_3MF keeps A/B references. Frozen source confirmed in its output folder.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "crn",

-      "title": "Rack LED matrix crown",

-      "prefixes": [

-        "CRN"

-      ],

-      "status": "idea",

-      "device_cards": [],

-      "sources": [

-        "work/rgb-crown/crn_e.scad"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: Medium: CRN-E concept header dated 2026-10-30, MAX7219 carrier in stock top beam, unprinted. Confirm whether still wanted alongside the redesigned fan top.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "frame",

-      "title": "Extrusion rack frame",

-      "prefixes": [],

-      "status": "idea",

-      "device_cards": [],

-      "sources": [

-        "work/rack-frame/BOM.md"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: Medium: work/rack-frame/BOM.md records option A chosen 2026-10-31; no reliable revision prefix, so none invented. Alternative metal-corner concept also listed. Confirm activity.",

-      "updated": "2026-11-06"

-    },

-    {

-      "id": "bottom",

-      "title": "Matching bottom intake grille",

-      "prefixes": [],

-      "status": "parked",

-      "device_cards": [],

-      "sources": [

-        "work/rack-cooling/Decisions.md"

-      ],

-      "workflow_log": "",

-      "notes": "Seeded by Codex, check: High intent, medium status: Brian requested matching bottom after the top prints, 2026-11-06. No modeled revision or prefix yet; parked until then.",

-      "updated": "2026-11-06"

-    }

-  ]

-}

+{
+  "version": 1,
+  "projects": [
+    {
+      "id": "csb",
+      "title": "Cable span bracket",
+      "prefixes": [
+        "CSB"
+      ],
+      "status": "report-due",
+      "device_cards": [
+        "docs/devices/lab-rax-4u-post.md"
+      ],
+      "sources": [
+        "work/cable-span-bracket/span_bracket.scad"
+      ],
+      "workflow_log": "Cable management bracket (front to rear posts)",
+      "notes": "Temporary acceptance note; never the real repo.",
+      "updated": "2026-11-07"
+    },
+    {
+      "id": "mrt",
+      "title": "MoCA rack tray",
+      "prefixes": [
+        "MRT"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/screenbeam-ecb7250.md",
+        "docs/devices/bridgelink-2way-splitter.md"
+      ],
+      "sources": [
+        "work/moca-rack-tray/MRT.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity, medium status: spec requests draft; newer HANDOFF says MRT-H and T5-T7 released for printing 2026-11-06. 2U rear-splitter concept remains discussion. Rear keystones dropped; f-keystone-coupler card is historical, not a current dependency.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "fan",
+      "title": "Rack top for a 200 mm fan",
+      "prefixes": [
+        "TFE",
+        "TRE",
+        "TSR",
+        "TFG"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/lab-rax-top.md",
+        "docs/devices/fan-200mm.md"
+      ],
+      "sources": [
+        "work/rack-top-fan/rack_top_fan.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: draft 4, TFE-A TRE-A TSR-A TFG-A; coupons TFE-T1 TSR-T1. Task 53 dry runs are not releases. No print or release.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "opx",
+      "title": "OptiPlex rear channels",
+      "prefixes": [
+        "OPX",
+        "SLV"
+      ],
+      "status": "draft",
+      "device_cards": [],
+      "sources": [
+        "outputs/OptiPlex_Sleeve_Channels_OPX-G_2026-11-04/src/OPX-G.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: OPX-G channels unprinted, reuses printed OPX-D sleeve and OPX-F rails (good fit). No dedicated device card found.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "scr5",
+      "title": "Screen, Pi and Hue",
+      "prefixes": [
+        "SCR5"
+      ],
+      "status": "draft",
+      "device_cards": [],
+      "sources": [
+        "outputs/Screen_Pi_Hue_SCR5-J5_2026-11-05/src/SCR5-J5.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: SCR5-J5 tray loosens J4 Hue cradle; J5 unprinted. Other J4/H8 parts retained. Missing dedicated device card; screen dimensions live in work/screen-5in/Dimensions.md.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "er6",
+      "title": "ER605 router bracket",
+      "prefixes": [
+        "ER6"
+      ],
+      "status": "draft",
+      "device_cards": [],
+      "sources": [
+        "outputs/ER605_Bracket_ER6-H_2026-11-04/src/ER6-H.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: ER6-H three floor slots, unprinted. Measurements in Fit_Findings; no device card.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "cm1000",
+      "title": "CM1000 modem bracket and lights",
+      "prefixes": [
+        "CM1P",
+        "CM6"
+      ],
+      "status": "draft",
+      "device_cards": [],
+      "sources": [],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: CM1P-Q white liners current and unprinted; O fit report is specimen-specific. CM6A/C do not print; T8 diffuser scratched. No dedicated device card. Referenced source absent: outputs/CM1000_OnePiece_CM1P-Q_2026-11-03/src/CM1P-Q.scad.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "psb",
+      "title": "Power strip bracket",
+      "prefixes": [
+        "PSB"
+      ],
+      "status": "draft",
+      "device_cards": [],
+      "sources": [
+        "outputs/Power_Strip_Bracket_PSB-A_2026-11-03/src/psb_a.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: PSB-A first unprinted draft; keyhole lip/foot dimensions and wall details unresolved. No device card.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "rx5",
+      "title": "MoCA receiver box",
+      "prefixes": [
+        "RX4",
+        "RX5"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/screenbeam-ecb7250.md"
+      ],
+      "sources": [
+        "work/wall-box-wizard/receiver1/rx5.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High: RX5-B rear ports, replaces blocked RX5-A. Unprinted; separate from rack and wall box. TL-SG105 card missing.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "chs",
+      "title": "Chess clock switch",
+      "prefixes": [
+        "CHS"
+      ],
+      "status": "idea",
+      "device_cards": [],
+      "sources": [],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: Low: explicitly requested by task 54, but no CHS source, release or device card in this checkout. No revision invented.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "wmb",
+      "title": "Flat wire bracket",
+      "prefixes": [
+        "WMB"
+      ],
+      "status": "idea",
+      "device_cards": [],
+      "sources": [],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: Low: explicitly requested by task 54, but no WMB source, release or card in this checkout. No revision invented.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "sg8",
+      "title": "TL-SG108E switch tray",
+      "prefixes": [
+        "SG8",
+        "KD"
+      ],
+      "status": "done",
+      "device_cards": [
+        "docs/devices/lab-rax-4u-post.md"
+      ],
+      "sources": [
+        "outputs/Chunky_Revisions/TL-SG108E_post_rails_2026-10-30/src/SG8-M6-F.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity; done per requested seed. SG8-M6-F tray and M6 screws fit per Brian 2026-11-05; other properties remain UNKNOWN. KD keyhole coupons grouped here from Fit_Findings.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "hdt",
+      "title": "Drive tray",
+      "prefixes": [
+        "HDT"
+      ],
+      "status": "done",
+      "device_cards": [],
+      "sources": [
+        "outputs/Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity, low physical completion: done is the requested organizational status; HDT-M6-A README/HANDOFF say approved but not printed. Historical 2026-10-25 tray fit does not prove M6 revision.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "phx",
+      "title": "Post hex anti-warp concept",
+      "prefixes": [
+        "PHX"
+      ],
+      "status": "parked",
+      "device_cards": [],
+      "sources": [],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: Medium: HANDOFF identifies PHX-C latest concept, someday rebuild only. work/rack-post-hex is missing in this checkout; no source path invented. Warp benefit UNKNOWN.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "rw",
+      "title": "Rack wall mount",
+      "prefixes": [
+        "RW"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/lab-rax-4u-post.md"
+      ],
+      "sources": [
+        "work/rack-wall-mount/rwm1.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity, medium activity: RW-WP-A / RW-RC-A / RW-SO-A cleat and standoffs chosen, not printed; HANDOFF 2026-10-30. U1 conflicts with CBL-B.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "moca-wall",
+      "title": "MoCA wall box and cleat",
+      "prefixes": [
+        "MOCA"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/screenbeam-ecb7250.md",
+        "docs/devices/bridgelink-2way-splitter.md"
+      ],
+      "sources": [
+        "work/wall-box-wizard/concept15/cleat16.scad",
+        "work/wall-box-wizard/concept15/body15.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity, medium current status: MOCA-BC-A and MOCA-WP-A cleat accepted, unprinted. Earlier sleeve/cradle/porch prints have names rather than revision IDs; not silently numbered. Separate job from RX5.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "cbl",
+      "title": "Rear cable management lanes",
+      "prefixes": [
+        "CBL"
+      ],
+      "status": "draft",
+      "device_cards": [
+        "docs/devices/lab-rax-4u-post.md"
+      ],
+      "sources": [
+        "outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-A.scad",
+        "outputs/Chunky_Revisions/Rear_Cable_Lane_2026-10-31/src/CBL-BCDE.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High identity, medium activity: CBL-A through E, unprinted; source README records wall-mount and post-hole conflicts. Separate from front-to-rear CSB.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "hp4",
+      "title": "Hue and Pi tray (reference)",
+      "prefixes": [
+        "HP4"
+      ],
+      "status": "parked",
+      "device_cards": [],
+      "sources": [
+        "outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High history, medium parked classification: HP4-M6-B default was superseded by combined SCR5 unit; Final_3MF keeps A/B references. Frozen source confirmed in its output folder.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "crn",
+      "title": "Rack LED matrix crown",
+      "prefixes": [
+        "CRN"
+      ],
+      "status": "idea",
+      "device_cards": [],
+      "sources": [
+        "work/rgb-crown/crn_e.scad"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: Medium: CRN-E concept header dated 2026-10-30, MAX7219 carrier in stock top beam, unprinted. Confirm whether still wanted alongside the redesigned fan top.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "frame",
+      "title": "Extrusion rack frame",
+      "prefixes": [],
+      "status": "idea",
+      "device_cards": [],
+      "sources": [
+        "work/rack-frame/BOM.md"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: Medium: work/rack-frame/BOM.md records option A chosen 2026-10-31; no reliable revision prefix, so none invented. Alternative metal-corner concept also listed. Confirm activity.",
+      "updated": "2026-11-06"
+    },
+    {
+      "id": "bottom",
+      "title": "Matching bottom intake grille",
+      "prefixes": [],
+      "status": "parked",
+      "device_cards": [],
+      "sources": [
+        "work/rack-cooling/Decisions.md"
+      ],
+      "workflow_log": "",
+      "notes": "Seeded by Codex, check: High intent, medium status: Brian requested matching bottom after the top prints, 2026-11-06. No modeled revision or prefix yet; parked until then.",
+      "updated": "2026-11-06"
+    }
+  ]
+}

POST /api/projects: 201, 0.014530 s
{
  "id": "acceptance-sample",
  "title": "Acceptance sample",
  "prefixes": [
    "QA54"
  ],
  "status": "idea",
  "notes": "",
  "updated": "2026-11-07",
  "workflow_log": "",
  "device_cards": [],
  "sources": []
}

DIFF work/bench/projects.json
--- work/bench/projects.json before
+++ work/bench/projects.json after
@@ -331,6 +331,19 @@
       "workflow_log": "",
       "notes": "Seeded by Codex, check: High intent, medium status: Brian requested matching bottom after the top prints, 2026-11-06. No modeled revision or prefix yet; parked until then.",
       "updated": "2026-11-06"
+    },
+    {
+      "id": "acceptance-sample",
+      "title": "Acceptance sample",
+      "prefixes": [
+        "QA54"
+      ],
+      "status": "idea",
+      "notes": "",
+      "updated": "2026-11-07",
+      "workflow_log": "",
+      "device_cards": [],
+      "sources": []
     }
   ]
 }

POST /api/fit-report: 200, 0.033990 s
{
  "project": "csb",
  "text": "- 2026-11-07 CSB-A (Brian, via Workshop Bench): Fits. Temporary acceptance fixture only. 2 walls, 10% infill. No physical claim. Strength UNKNOWN."
}

DIFF work/bench/projects.json
--- work/bench/projects.json before
+++ work/bench/projects.json after
@@ -7,7 +7,7 @@
       "prefixes": [
         "CSB"
       ],
-      "status": "report-due",
+      "status": "draft",
       "device_cards": [
         "docs/devices/lab-rax-4u-post.md"
       ],

DIFF docs/Fit_Findings.md
--- docs/Fit_Findings.md before
+++ docs/Fit_Findings.md after
@@ -83,3 +83,4 @@
 - 2026-11-06 ScreenBeam right-angle F and jumper (Brian, measured, not a printed part): crimp sleeve ends 44 behind the port centre line (model had 38.2), the jumper starts to curve 58 behind it (model bent at ~39). Port centre is 22 from the case's rear long side, as modelled. Draft MRT.scad moves the jumper bend and the splitter back 19 (OUT1 at Y 137).

 - 2026-11-06 MRT-T1 ScreenBeam foot pockets (Brian): hold well enough; with the Velcro strap on the final tray it should stay in place. Pockets unchanged. Jumper lengths stay UNKNOWN until everything is installed. MRT-T2 lip gaps not reported.

 - 2026-11-06 MRT-T4 MoCA channel jig (Brian): the bends and everything else look like they should work fine. The coax struggled to get past the sloped lips into the channels, but not enough to be a concern (lip gap 6.8 and 60 deg lead-in kept). The coax puts a lot of tension on the channel walls, so they need reinforcing: draft MRT-H walls 2 -> 3 with base fillets and gussets. He wants an F keystone at both rear coax entrances (draft MRT-H). Not reported: jumper lengths, covers and M3 screw length, walls and infill. Strength UNKNOWN.

+- 2026-11-07 CSB-A (Brian, via Workshop Bench): Fits. Temporary acceptance fixture only. 2 walls, 10% infill. No physical claim. Strength UNKNOWN.


DIFF work/workbench/Workflow_Log.md
--- work/workbench/Workflow_Log.md before
+++ work/workbench/Workflow_Log.md after
@@ -27,3 +27,9 @@
 | 2026-11-05 | CSB-B draft | Floor slots turned into zip-tie pairs (6.5 x 3, one by each wall) with a 1.6 deep groove under the floor so the tie sits flush (Brian) | none |

 | 2026-11-05 | CSB-B released | Brian printing; release_part.py 0 failed, 0 warnings, posts gap 0.22, keep-out clear | none |

 Totals when the part is done: drafts sent ___, revisions released ___, prints ___, prints that failed ___, measurement requests ___.

+

+## Cable management bracket (front to rear posts) (continued)

+

+| Date | Step | What happened | Friction | App idea |

+| --- | --- | --- | --- | --- |

+| 2026-11-07 | Report | 2026-11-07 CSB-A (Brian, via Workshop Bench): Fits. Temporary acceptance fixture only. 2 walls, 10% infill. No physical claim. Strength UNKNOWN. | | |


PASS: only the three allowed files and .bak copies changed; previous markdown bytes preserved; temporary files cleaned.
PASS: real repository checkpoint still unchanged after all temp-copy writes.

```

## Release/library regression output

```text
.........................
----------------------------------------------------------------------
Ran 25 tests in 13.840s

OK

```

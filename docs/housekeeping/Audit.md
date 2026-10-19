# Assembly Workshop housekeeping audit — Phase 1

Prepared for Brian, 2026-10-18 (Pacific). **Audit only; Phase 2 has not started.** This new file is the sole intended repository change made by this pass. No existing file was overwritten, edited, moved or deleted.

## Scope, authority and verification

Read AGENTS.md, PROJECT.md and HANDOFF.md first. AGENTS.md and Brian's present hard rules control this pass. Later handoff claims are evidence to catalogue, not authorization to reopen mounting, expand scope, run code or redistribute assets. Four-corner mounting remains TABLED; left grouping 2C remains provisional. Phase 6 and Phase 7 remain closed with limitations. All unsupported physical claims remain UNKNOWN.

Verified by read-only directory/file inspection, focused text searches, Git listings/status, selected SHA-256 comparisons and path-existence checks. Inspected top-level entries, immediate work/output directories, governing/entry docs, immediate work reports, and specifically referenced evidence. Git's untracked-file listing was used for backup-risk assessment; no general recursive content scan or repository-wide duplicate hunt was performed. Sizes below are bytes. File modification times are local metadata, not proof of authorization or event chronology.

No project scripts, tests, geometry, builds, renders, exports, evidence regeneration, database connections, browser/desktop sessions, process changes, installs, commits or network actions were performed. Existing report PASS statements below are historical claims, not rerun results. Current listener, active data directory, unsaved browser drafts, physical fit and backup completeness were not verified. The snapshot manifest's existence was checked; its full contents and current coverage were not verified.

## 1. Inventory and current/historical map

### Top-level entries and key documents

| Path | Purpose | Status |
| --- | --- | --- |
| `.git/` | Local version history, covering only a small subset of assets | Current; incomplete backup |
| `data/` | Normal-use SQLite, revisions, rack workspace/history and artwork | Current user data; preserve |
| `docs/` | Readiness planning and this housekeeping record | Mixed historical/current |
| `outputs/` | Runnable app, prior app versions, source/mesh deliveries and evidence | Mixed current/historical; protected |
| `work/` | Recovery/development scripts, safety copies, fixtures, reports and evidence | Mixed current/historical; protected |
| `AGENTS.md` | Persistent rules and selected GUI constraints | Current controlling guidance |
| `PROJECT.md` | Product, paths, startup and capability entry point | Current intended entry; operational/scope drift |
| `HANDOFF.md` | Accumulated rack/wizard/export implementation notes | Current intended handoff; internally superseded passages and scope conflicts |
| `START_HERE.md` | Earlier concise entry point, limits and commands | Superseded operational snapshot; useful preservation guidance |
| `GEMINI_HANDOFF.md` | Later renderer/startup/branding transition and data-path warning | Historical snapshot; some pending work superseded by HANDOFF |
| `patch_dialog.py` | One-shot workspace patcher; begins by copying over `workspace.js.bak` | Historical candidate; unsafe as startup procedure |
| `result.json` | Small success/export-style result with zero-valued settings | Unclear provenance; likely historical |
| `docs/housekeeping/Audit.md` | This bounded audit and proposed approval items | Current; new |
| `docs/phase7-readiness/Readiness_Plan.md` | Pre-closeout gates with appended STL-only clarification | Historical planning, not current completion gate |
| `docs/phase7-readiness/Verification_Report.md` | Earlier 39-test snapshot and documentation discrepancies | Historical evidence |
| `docs/phase7-readiness/Evidence_Register.csv` | Historical UNKNOWN/process/physical gate register | Historical evidence; UNKNOWNs preserved |
| `outputs/Mechanical_Design_App/README.md` | App guide with accumulated phase/workspace notes | Mixed; top closeout status current, many older capability passages superseded |
| `outputs/Mechanical_Design_App/hardware-records.md` | Catalog semantics, source limits, phased catalog history | Mixed; later closeout note supersedes older pending acceptance |
| `outputs/Mechanical_Design_App_Beta_Spec.md` | Consolidated earlier beta requirements | Historical specification, not current implementation checklist |
| `outputs/Phase7_Closeout/Closeout_Report.md` | Milestone disposition and specimen-specific limits | Current acceptance authority for that milestone; historical setup/next-step observations |
| `outputs/Session_Handoff_20261018/Preservation_Report.json` | Earlier local snapshot and hash-manifest record | Historical preservation evidence, not proof of current backup |

### Immediate output folders

| Path under `outputs/` | Purpose | Status |
| --- | --- | --- |
| `Mechanical_Design_App/` | Runnable source, launcher, protected references and an additional data directory | Current implementation; support scope disputed in docs |
| `Mechanical_Design_App_Beta_0_1/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_2/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_3/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_5/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_6/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_6_1/` | Earlier app snapshot | Historical |
| `Mechanical_Design_App_Beta_0_7/` | Earlier app/data snapshot | Historical; database exists |
| `Mechanical_Design_App_Beta_0_8/` | Preserved original app/data | Historical baseline; database exists |
| `Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/` | Earlier supplied tray/faceplate mechanical source and meshes | Historical baseline; specimen provenance remains relevant |
| `Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix/` | Earlier mechanical revision | Historical immutable evidence |
| `Normal_Use_Location_Review/` | Data discovery, setup and verification records | Historical; later data-location discrepancy remains unresolved |
| `Phase7_Start/` | Entry configuration, scope clarification and readiness records | Historical; start status superseded by closeout |
| `Phase7_Digital_Acceptance/` | Recorded digital acceptance and integrity/source evidence | Historical evidence supporting current closeout |
| `Phase7_Hardware_Evidence/` | Retained supplier drawing review | Historical reference; niche research parked |
| `Phase7_Physical_Observations/` | Brian's report, photos and recovered specimen provenance | Historical specimen evidence; current limits apply |
| `Phase7_Closeout/` | Closeout, evidence checks, before-doc copies and preservation record | Current disposition plus historical snapshots |
| `Session_Handoff_20261018/` | Handoff snapshot, checks, before-doc copies and preservation record | Historical handoff/preservation |
| `Physical_Test_Coupons_2026-10-18/` | Later coupon artifacts recorded in HANDOFF | Historical artifacts; no testing authorized by this audit |
| `SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/` | Already labeled prior physical kit | Superseded, preserve in place |

Immediate output files also include Pi4 ZIP deliveries, beta ZIPs 0.1–0.8 (including 0.4, whose unpacked peer is absent), `Pi4_fit_inspection.md` and `Pi4_fit_review_REFERENCE_ONLY.3mf`. These are historical delivery/reference evidence, not redundant merely because a folder also exists. ZIP/folder equality was not checked.

### Work report and evidence map

| Path under `work/` | Purpose | Status |
| --- | --- | --- |
| `gui-restoration/` | Recovered intent, initial recreated shell, tests and source safety copy | Historical implementation; appended corrections, many original limits superseded |
| `rack-geometry-recovery/` | Recovered HTML/3MF originals, source mapping and reference viewer | Current provenance reference; activation/state notes historical |
| `startup-repair/` | Earlier inactive-server/direct-file startup repair | Historical |
| `rack-scene/` | Exact source-mesh visual preview and rigid placement evidence | Current provenance; old shared-project/stack/extension notes superseded |
| `workflow-audit/` | Allocation edits, save serialization and then-current backlog | Historical acceptance; several backlog items superseded |
| `assembly-instances/` | Independent assembly records, appearance/artwork, two GUI concepts | Current feature provenance; GUI choice and some save flow superseded |
| `gui-refinement/` | Selected 1C/2C/3A/4A/5A/6A/7A/8A, atomic Save, acceptance | Current selected GUI reference; saved-state/PID observations historical |
| `render-studio/` | Shared renderer, GPU evidence and integration history | Renderer evidence current within scope; shell-preservation claim explicitly superseded |
| `gui-render-repair/` | Restores selected hybrid after renderer integration | Current corrective provenance; activation observations historical |
| `faceplate-selection/` | Rack faceplate selection/highlight | Feature evidence; historical acceptance |
| `assemble-selection/` | Software inspection selection | Historical implementation; renderer replaced by studio with software fallback |
| `assemble-studio/` | Shared WebGL renderer for actual inspection meshes | Current feature provenance; recorded acceptance historical |
| `gui-style-delivery/` | Embedded canonical CSS and repeated-load diagnostics | CSS evidence relevant; unresolved startup diagnosis superseded |
| `startup-reliability/` | Backlog64 and cancelled-response fix with recorded reload checks | Current repair reference; prior process IDs historical |
| `rack-branding/` | Source-derived wordmark color and original U-label implementation | Source provenance relevant; label placement later changed per HANDOFF |
| `hardware-evidence/` | One-shot supplier drawing review utility | Historical research; parked |
| `phase5-browser/` | Earlier browser evidence | Historical |
| `phase5-solid-checks/` | Earlier solid/conversion/clearance evidence | Historical; not fresh physical approval |
| `phase7/` | Entry/scope-clarification utilities | Historical; do not rerun |
| `phase7-digital/` | Digital acceptance utilities/evidence | Historical; do not regenerate |
| `v08-build/` | Earlier isolated build artifacts | Historical cache/evidence |
| Immediate `work/` files (80 observed) | Version patch/package scripts, viewer tests, source/collision artifacts and reports | Mixed historical/support utilities; no general orphan verdict |

Recommended reading map today: AGENTS → PROJECT → this audit → HANDOFF with conflicts below visible → selected GUI report → only the relevant renderer/data/provenance report. Closeout establishes milestone limits, not current running-process state. Report chronology matters more than the generic filename `Report.md`.

## 2. Contradictions and misleading mixed snapshots

Quoted references are relative `file:line`, one-based, from the audit snapshot. “Newer” describes document metadata or an explicit subsequent statement; it does not authenticate historical owner authorization. AGENTS/PROJECT modified 2026-10-18 11:20; START_HERE 11:26; GEMINI_HANDOFF 16:50; HANDOFF 22:15. All remain untouched.

| ID | Earlier/controlling side | Other side | Chronology and disposition |
| --- | --- | --- | --- |
| C1 | `AGENTS.md:6`: “Four-corner mounting remains TABLED”; `PROJECT.md:39`: “Four-corner mounting ... stay parked”; `outputs/Phase7_Closeout/Closeout_Report.md:18`: “mounting matter remains tabled.” | `HANDOFF.md:106–108`: “4 HOLES PER U” and “explicitly raised ... settled as the default.” | HANDOFF is newer and claims owner direction; this audit follows Brian's present explicit TABLED instruction. Record implementation claims without ratifying them or changing geometry. |
| C2 | `AGENTS.md:28`: “Pi4 remains the only manufacturing geometry adapter”; `work/gui-refinement/Report.md:32`: same limit. | `HANDOFF.md:57`: “supersedes ‘Pi4 only adapter’”; `HANDOFF.md:64–91`: P1–P4 built/import claims. | Later handoff claims expand scope. Static inspection found `equipment.py`, `equipment_tray.scad`, `equipment-wizard.js` and routes in `app.py:837–858`; presence is verified, functionality/support approval is not. Keep policy and implementation separate. |
| C3 | `AGENTS.md:28`: “no rack-frame STL adapter”; `PROJECT.md:37`: preview only; `work/workflow-audit/Report.md:41`: “No supported rack-frame STL adapter exists.” | `HANDOFF.md:123–127`: “Rack frame STL export ... supersedes” and `/api/rack-stl`. | Newer HANDOFF plus existing `rack_stl.py` and `app.py:849` establish code presence only. No export was invoked. Rights/support conflict remains visible. |
| C4 | `PROJECT.md:15,43`: normal data `data/normal-use`; `work/gui-refinement/Report.md:19`: recorded process used that folder. | `work/gui-style-delivery/Report.md:7`: process used `outputs/Mechanical_Design_App/data`, “NOT ... data/normal-use”; `work/startup-reliability/Report.md:21` and `GEMINI_HANDOFF.md:8` preserve the discrepancy. | Style/startup/Gemini records are later than GUI refinement. Both databases exist; launcher still targets normal-use, app default is `ROOT / 'data'` (`app.py:897`). Active process not checked; do not switch/merge data. |
| C5 | `HANDOFF.md:8`: “Node is not installed.” | `START_HERE.md:67–68` names bundled Node; `work/rack-branding/Report.md:12` records Node checks. | HANDOFF file is later, but its blanket statement conflicts with existing bundled Node executable (path checked). No claim about PATH/system Node or successful execution today. |
| C6 | `work/gui-restoration/Restoration_Report.md:11`: original HTML “have not been recovered”; `:17` schematic primitives. | Same report `:49` says originals recovered; `work/rack-geometry-recovery/Recovery_Report.md:5` confirms copies; `work/rack-scene/Report.md:7` uses exact components. | Explicit subsequent recovery/preview supersedes initial restoration snapshot; later readers can miss appended correction. |
| C7 | `work/workflow-audit/Report.md:36`: “Every allocation still refers to one shared Pi4 hardware project”; `work/rack-scene/Report.md:11`: “sharing its current hardware project.” | `work/assembly-instances/Report.md:7` independent IDs/snapshots; `work/gui-restoration/Restoration_Report.md:54`: shared limitation superseded; `AGENTS.md:28` independent instances. | Assembly report 10:39 follows workflow 09:57 and scene 09:42. Original statements are historical, not current defects. |
| C8 | `work/assembly-instances/Report.md:3`: “No whole-interface redesign has been selected yet”; `:17–24` proposes Focused studio/Canvas-first. | `work/gui-refinement/Report.md:3`: selected 1C/2C/3A/4A/5A/6A/7A/8A, grouping provisional; `AGENTS.md:33` confirms. | GUI refinement 11:18 follows assembly report 10:39. Choice is settled except Brian's pending 2C review; do not reopen concepts. |
| C9 | `work/gui-style-delivery/Persistence_Test_Report.md:3`: startup “LIMITED by an intermittent workspace initialization failure.” | `work/startup-reliability/Report.md:18,23`: 20 reloads passed and “supersedes the unresolved startup finding.” | Persistence 16:18 precedes startup repair 16:38. Preserve both acceptance scopes; no repeated tests today. |
| C10 | `work/rack-scene/Report.md:10`: extension only in reference viewer; `work/workflow-audit/Report.md:38`: no stack editor. | `HANDOFF.md:25–31,39–41`: movable post levels/extensions, 1U accounting and layout lock. | Later HANDOFF claims partial stack controls. This does not establish the complete per-instance component editor sought in `GEMINI_HANDOFF.md:23`. |
| C11 | `HANDOFF.md:15–16`: logo missing, then fixed in same section; `GEMINI_HANDOFF.md:18` and `work/rack-branding/Report.md:5` already record logo. | `HANDOFF.md:16` claims overwritten/reverted logo version; `HANDOFF.md:19–20` relocates labels vs `work/rack-branding/Report.md:7` between-hole depth-tested markings. | Newer HANDOFF describes another repair and label design. Treat missing-logo headline and branding screenshot as historical stages, not current diagnoses. No UI verified. |
| C12 | `outputs/Phase7_Closeout/Closeout_Report.md:29,38`: establish data location next; databases “were absent.” | `PROJECT.md:15–16` names normal/original data; `outputs/Normal_Use_Location_Review/Review.md:16–22` records setup. | Subsequent setup supersedes closeout's historical path observation. Normal-use/current-app/Beta0.7/Beta0.8 databases all exist now. Acceptance and physical limitations in closeout are unaffected. |
| C13 | `docs/phase7-readiness/Readiness_Plan.md:3`: “PREPARATION ONLY”; `:17` printer/process gate; register P7-009 “NOT_STARTED.” | Plan `:46–48` limits process gates to separately authorized physical work; `AGENTS.md:7,19,23` and closeout `:3,13–14` close milestone with specimen report. | Plan's own appended clarification and later closeout supersede software-gating use. Preserve register UNKNOWNs; not every physical task passed. |
| C14 | `HANDOFF.md:25,31`: extensions at joints, then own 1U; `:65` one slot pair; `:89` P4 “not built”; `:99` radius 8 mm. | Same file `:30–31` supersedes joint model; `:89–91` says STEP BUILT; `:106–109` says four holes/radius 2.5 mm. | Internal chronological narrative is ambiguous when read as current instructions. Static template `equipment_tray.scad:28–29` has 4 mm thickness/2.5 mm radius; no geometry acceptance inferred. |
| C15 | `HANDOFF.md:98`: wizard parts “share the printed geometry.” | `HANDOFF.md:99–104` describes changed plate and unprinted features; closeout `:13,18` prohibits transferring specimen approval. | Later changes supersede geometry-sharing implication. Fit remains specific to the earlier specimen; no wider fit/strength pass. |

Other snapshot drift: `START_HERE.md:32–34` records zero allocations/PID25160; `GEMINI_HANDOFF.md:7–9` records one allocation/PID29100; HANDOFF contains many later PIDs. These are observations at different times, not proof of lost data or current processes. `HANDOFF.md:14` “logo missing” and `:51` “nothing built yet” must not lead a future session to repeat completed repairs. `work/render-studio/Report.md:3` already explicitly retracts its original GUI-preservation claim; preserve that correction.

## 3. Superseded material and non-destructive labeling proposal

Protected evidence must stay in place under this request. Prefer a new external index at `docs/archive/README.md` pointing to it, rather than moving protected files or inserting banners into them.

| Material | Superseding reference | Proposed treatment, approval required |
| --- | --- | --- |
| `docs/phase7-readiness/` (three files) | Closeout and AGENTS STL-only clarification | Move these three docs only to `docs/archive/phase7-readiness/`, leave a README at the former directory with destination and current closeout link; retain every original byte. |
| `work/assembly-instances/rack-studio-options.html`, option PNGs and proposed-layout report passages | `work/gui-refinement/Decisions.json`, Report and AGENTS selected hybrid | Label as unchosen concepts in new archive index; no move/edit under work. |
| Original restoration schematic/shared-project passages, workflow backlog items 1/3/4/6 | Scene, assembly, refinement reports; later disputed HANDOFF claims | Index historical stages and unresolved scope claims; don't rewrite recorded acceptance. |
| `outputs/Mechanical_Design_App_Beta_Spec.md`, beta app folders and ZIPs | Current rack-first product and later restrictions | Index historical beta requirements/deliveries; no moves or edits. |
| Closeout/setup/handoff before-doc copies, old next-chat prompts | Current governing docs plus this audit | Label historical snapshots in index; no protected edits. |
| `START_HERE.md`, `GEMINI_HANDOFF.md` | Consolidated HANDOFF after approval | Archive root snapshots with current-entry pointers; preserve original text. |
| Already superseded physical kit and later coupons | HANDOFF coupon section; present physical-work restrictions | Index only, preserve every artifact; no new physical readiness conclusion. |

## 4. Stale/duplicate/temp/orphan candidates

“Candidate” does not mean disposable. No general duplicate hash scan was performed. No report listed here was proven byte-identical. Most are versioned evidence rather than waste. Confidence describes historical/candidate classification, not safety of removal.

| Path | Bytes | Evidence and confidence | Risk if wrong / treatment |
| --- | ---: | --- | --- |
| `result.json` | 214 | Generic success/export metadata, no identifying source; no reference found in bounded entry/report search. Medium stale, low provenance. | May document an import/conversion result. Preserve; index as unclear. |
| `patch_dialog.py` | 14473 | One-shot patcher directly targets app workspace, copies over `.bak`; later HANDOFF records dialog done. High historical, medium orphan. | May be sole record of a change. Archive only after approval; never execute. |
| `outputs/Mechanical_Design_App/workspace.js.bak` | 49748 | Differs in hash/size from live workspace.js (71453). High safety-copy classification. | Could be unique recovery source. Protected: retain in place, index only. |
| `outputs/Phase7_Closeout/before_HANDOFF.md` | 10535 | Earlier guide copy; hash differs from session copy. High historical, not exact duplicate. | Preserve rollback/provenance. No move/edit. |
| `outputs/Session_Handoff_20261018/before_HANDOFF.md` | 10546 | Similar name/purpose but different SHA-256. High historical. | Distinct snapshot; retain. |
| `outputs/Phase7_Closeout/before_AGENTS.md` | 3333 | Hash differs from both later copies below. High historical. | Unique prior rules; retain. |
| `outputs/Phase7_Closeout/before_final_AGENTS.md` | 4178 | Distinct SHA-256. High historical. | Unique intermediate rules; retain. |
| `outputs/Session_Handoff_20261018/before_AGENTS.md` | 5084 | Distinct SHA-256. High historical. | Unique subsequent rules; retain. |
| `work/assembly-instances/Report.md` | 5991 | Earlier GUI alternatives and acceptance, superseded in part. High. | Feature evidence still relevant; index only. |
| `work/assembly-instances/rack-studio-options.html` | 224271 | Explicit proposed concepts; later hybrid chosen. High. | Visual decision provenance; retain. |
| `work/assembly-instances/Focused_Studio_Option.png` | 73557 | Screenshot of unchosen concept. High. | Decision provenance; retain. |
| `work/assembly-instances/Canvas_First_Option.png` | 42354 | Screenshot of unchosen concept. High. | Decision provenance; retain. |
| `work/app_v03.py`, `app_v04.py`, `app_v05.py`, `app_v06.py`, `app_v061.py`, `app_v07.py`, `app_v08.py` | 2825; 2047; 1845; 1510; 1178; 1476; 3622 respectively | Version-named app mutation utilities beside current app. Medium historical; orphan status unproven. | Could reconstruct revisions; no execution/move. |
| `work/pack_v03.py`, `pack_v04.py`, `pack_v05.py`, `pack_v06.py`, `pack_v061.py`, `pack_v07.py`, `pack_v08.py` | 1659; 1725; 1854; 1980; 1206; 2295; 5211 respectively | Historical packaging utilities by version naming. Medium; not inspected for execution safety. | Could document package provenance; retain, never run for housekeeping. |
| `work/test_viewer.cjs`, `test_viewer_v06.cjs`, `test_viewer_v061.cjs`, `test_viewer_v08.cjs` | 1439; 1957; 2154; 3311 respectively | Similar names, but v08 is still referenced by earlier acceptance. Low orphan confidence. | May remain useful checks; not duplicate/deletion candidates. |
| `work/joint_collision.scad`, `joint_collision.stl` | 3341; 6096 | Names indicate historical collision fixtures/results. Medium historical, no staleness proof. | Original mechanical evidence; protected, retain. |
| `work/pcb_collision.scad`, `pcb_collision.stl` | 3364; 123463 | Same classification. | Same risk; retain. |
| `work/usb_collision.log`, `usb_collision.scad`, `usb_collision.stl` | 359; 181; 19255 | Same classification. | Same risk; retain. |
| `work/v08-build-result.json`, `work/v2_verification.json`, `work/verification.json` | 123; 2017; 1301 | Generic/versioned result names; not established as redundant. Low stale confidence. | Unique verification provenance; retain. |

Log/PID files, before-app trees, acceptance-data directories and `__pycache__` were observed but are not cleanup candidates here. A filename or age alone cannot establish that data is disposable, and caches/work data are explicitly protected.

## 5. Git state and backup risk

Pre-audit HEAD: `f754713` — “Preserve rack-first GUI context and prepare current handoff”. Exactly **14 tracked files** were listed:

- `AGENTS.md`, `PROJECT.md`, `HANDOFF.md`.
- `outputs/Phase7_Closeout/{Closeout_Report.md,Final_Checks.json,Next_Chat_Prompt.md,Preservation_Report.json}`.
- `outputs/Session_Handoff_20261018/{Final_Checks.json,Next_Chat_Prompt.md,Preservation_Report.json}`.
- `work/gui-restoration/{HTTP_Checks.json,Recovered_GUI_Decisions.json,Restoration_Report.md,Verification.json}`.

Four pre-existing tracked modifications: AGENTS, PROJECT, HANDOFF and work/gui-restoration/Restoration_Report. Pre-audit diff stat: 154 insertions/74 deletions across those four files. They were not reverted or adopted into a commit. Git also warned of future LF→CRLF handling for HANDOFF; no normalization performed.

`git ls-files --others --exclude-standard` listed **942 untracked files before this audit**. This excludes Git-ignored files; ignored-file inventory was not performed, so the backup-risk set may be larger. The 942 count is not an inventory of unsaved drafts or a count of only valuable assets. The new audit itself adds another untracked document.

Important assets existing outside tracked history include:

- Entire runnable `outputs/Mechanical_Design_App/`: Python/JS/CSS, baseline SCAD/JSON, equipment template/import code, rack export code, catalog packs, reference meshes/photos and locked manifest assets.
- `data/normal-use/`: database (28672 bytes), rack JSON (9245 bytes), revisions, artwork and rack history.
- `outputs/Mechanical_Design_App/data/`: another database (28672 bytes), rack JSON (2434 bytes), equipment-revisions. Equal database size does not establish identical contents. No migration/merge is proposed.
- Original Beta0.8 and other beta data/sources, immutable historical revisions, mechanical source/STL deliveries and ZIPs.
- Recovered creator HTML/3MFs, Pi/supplier reference assets, physical observation photos/provenance, later coupon and superseded-kit artifacts.
- Most work reports, tests, screenshots, source safety copies, diagnostics and acceptance fixtures; root START_HERE, GEMINI_HANDOFF, patch_dialog and result.json; all pre-existing docs/phase7-readiness files.

`outputs/Session_Handoff_20261018/Preservation_Report.json` records a 492-file/79515714-byte snapshot at `C:/Users/brian/Documents/ChatGPT/Assembly Workshop/outputs/Assembly_Workshop_Handoff_Preservation_20261018` with a manifest and matching hashes at that time. Manifest exists. This audit did not validate all snapshot files or compare today's assets with it. It precedes later work and is a local copy, not verified off-machine coverage. A Git commit/clone cannot replace full asset/data preservation, and disk backups cannot capture unsaved browser drafts.

## 6. Documentation/path drift (looked up, not executed)

| Reference | Observation | Proposed documentation disposition |
| --- | --- | --- |
| `HANDOFF.md:120`, old `outputs/Physical_Test_Kit_2026-10-18/` | Path absent; `HANDOFF.md:117` names existing `outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/`. Coupon folder exists too. | Correct the old-path reference in consolidated handoff; preserve kit/coupons. |
| `docs/phase7-readiness/Verification_Report.md:3`, old `.../referenced-chatgpt-conversation-this-is-an` workspace | Exact directory absent; canonical current root exists. | Preserve historical source path, label former workspace in archive index. |
| `PROJECT.md:43`, `START_HERE.md:61`, launcher data path | Launcher, normal-use DB and current-app DB exist; paths disagree with later active-folder reports, not missing. | Record launcher versus app default separately; no switch/restart. |
| `HANDOFF.md:8` Node absence vs `START_HERE.md:67–68` bundled path | `C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe` exists. | Replace blanket absence claim with existence-only observation; do not infer system install or execution. |
| `START_HERE.md:66–68` focused runners | check_python.py, test_save.cjs and test_appearance_startup.cjs all exist. | Retain as later-development references; no tests run now. |
| `START_HERE.md:53,61`, runtime/render paths | Python310/python.exe and OpenSCAD/openscad.exe exist. HANDOFF's FreeCAD 1.1/bin/freecadcmd.exe also exists. | Existence is verified, versions/functionality not tested; no installs/renders. |
| `PROJECT.md:45`, startup-repair verification | `work/startup-repair/Verification.json` exists. | Label recorded historical startup check; not proof of a listener now. |
| Closeout old absent-database observation | Normal-use, current-app, Beta0.7 and Beta0.8 database paths checked and present. | Mark as historical observation in index, not current setup instruction. |
| Markdown links in root guides, Closeout_Report and immediate `work/*/Report.md` | Checked explicit Markdown link destinations relative to their documents; no missing local Markdown targets found in that bounded set. | Not a full audit of inline paths, code symbols, external URLs, images or all nested docs. |

App README drift is substantive, not only broken paths: `outputs/Mechanical_Design_App/README.md:3` already labels older counts historical, but `:15,84,104,116` still contain five-phase, in-progress, pending, schematic/shared-project/unrecovered-source language. `hardware-records.md:26` pending acceptance is explicitly superseded at `:29,33`. Protected files remain unchanged; index these passages so they cannot become fresh tasks. Historical counts (39/46/31/37) cover different snapshots/suites and are not a test regression by themselves.

## 7. Proposed actions — approval required; none applied

Approval can name individual item numbers. All proposals preserve originals and avoid app/data/geometry changes. “Reversible” assumes the preserved pre-edit bytes are retained and destinations do not already exist; fail on collision. No irreversible actions are proposed.

1. **Reversible — add `docs/archive/README.md`.** Create a linked chronology/index of protected evidence in place: readiness → closeout → source recovery/scene → workflow → instances → selected hybrid → render/repair → CSS/startup → branding → later disputed HANDOFF implementation. Label each link current reference, historical snapshot, superseded concept or unresolved scope claim. No protected report edits/moves.
2. **Reversible — archive readiness docs only.** Move `docs/phase7-readiness/Readiness_Plan.md` → `docs/archive/phase7-readiness/Readiness_Plan.md`; `Verification_Report.md` → same destination directory/name; `Evidence_Register.csv` → same destination directory/name. Add `docs/phase7-readiness/README.md` linking to all three destinations, current closeout and STL-only limits. Preserve file bytes and UNKNOWNs. Update references in root entry docs only; list unchanged historical references in archive index. This item is optional; index-only is sufficient if original paths should stay.
3. **Reversible — preserve and consolidate HANDOFF.** First create `docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md` as a byte-preserving copy of the current HANDOFF (fail if destination exists). Then edit `HANDOFF.md` into a short current-state/next-step/UNKNOWN/location guide. Keep closed phases, specimen-specific evidence, chosen hybrid/2C pending, parked matters and preservation rules. Separate verified file presence from disputed support/authorization claims C1–C3; do not declare those decisions resolved. Remove stale PID/startup assertions and superseded intermediate recipe text from the current guide, retaining their complete archived text. State both data locations and that active-folder/drafts are unverified. No app or protected file changes.
4. **Reversible — align PROJECT.** First preserve current bytes at `docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md`; edit only `PROJECT.md` entry/read order, data-location warning, historical-server/snapshot wording and links to the new evidence map. Distinguish governing support limits from additional code present on disk. Preserve Pi4/M3/baseline boundaries and UNKNOWNs. Do not change AGENTS.
5. **Reversible — remove competing root handoff entry points by archival moves.** `START_HERE.md` → `docs/archive/handoffs/START_HERE_20261018.md`; `GEMINI_HANDOFF.md` → `docs/archive/handoffs/GEMINI_HANDOFF_20261018.md`. Add small new files at both old paths pointing to AGENTS/PROJECT/HANDOFF and their respective archived snapshots, explicitly labeled historical. Preserve originals without rewriting relative links; archive index states their original root-relative link context. Review root links after item 2 if approved.
6. **Reversible — archive root one-shot patcher only.** `patch_dialog.py` → `docs/archive/scripts/patch_dialog.py`; index original execution context and “historical, do not execute” status. No execution, content change or move of its protected `.bak` target. Leave result.json in place because its provenance is unclear; index it. A bounded root/report reference search found no references to either root candidate, but this is not proof of complete dependency absence.
7. **Reversible — add `docs/housekeeping/Changes.md` when approved changes are applied.** Record every file added/edited/moved, exact original→new path, saved pre-edit copy/hash, link updates and inverse operation. Explicitly record zero AGENTS edits if item 4 is approved as proposed. No changes log claiming Phase 2 work should precede actual approval/application.
8. **Reversible — documentation-only link/existence verification after approved edits.** Check changed docs' local links, confirm preserved originals at archival destinations and compare before/after Git status without running app/tests/builds. List pre-existing tracked modifications separately. Do not stage/commit unless Brian separately requests it; never push.

**Not proposed:** deleting anything; moving/editing outputs/work contents, revisions, databases, histories, artwork, caches, pins or drafts; changing AGENTS rules; resolving data-source/support/mounting decisions; altering left grouping; restarting servers; running historical scripts; regenerating evidence; making a backup/release/export; committing or pushing.

Phase 1 stops here. Brian's approval of specific numbered items is required before Phase 2.

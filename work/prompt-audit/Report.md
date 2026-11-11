# Agent instruction audit — 2026-11-11

Nothing has been applied. The proposed edits are in [proposed.diff](proposed.diff).

## Assumptions

- **Scope (as you named it):** `C:\Users\brian\.claude\CLAUDE.md` (global; edits there affect every project), `AGENTS.md` (there is no CLAUDE.md in the repo), the 51 memory files plus `MEMORY.md`, `.claude/skills/new-part/SKILL.md` and the 12 files in `.claude/commands/`. There are no agent definitions. `.claude/settings.local.json` and `.claude/launch.json` are settings, not instructions: not audited, one side note below.
- **Target model:** Claude Fable 5.2 / Opus 5.5 running in Claude Code.
- **Not an API project:** no request code, tool definitions or sub-agent roster, so those parts of the audit are not applicable.
- The diff is written as if the four open questions (end of this report) are answered the recommended way. Hunks that depend on an answer are marked **Q1–Q4** below.

## Summary

The instructions are sound in what they say; the trouble is where they say it and what was never cleaned up.

1. **AGENTS.md still carries rules that later sections overturned.** It says no pushes without authorization (line 7) and also to push every session (line 63). It says most assets are untracked (line 5) and also that the whole project is in the repo (line 60). It tells you to leave the Pi path untouched (line 39) one section after saying the Pi path is retired (line 32). A model that follows text literally has to guess which one wins.
2. **Settled decisions live only on the PC.** The keystone default, OptiPlex orientation, own printed rack, rounded floor corners, never-fudge-the-mock and the sleeve_top 0.8 rule exist only in the memory folder. Cloud sessions and the laptop never see that folder (or the global file). The diff moves the rule into the repo (AGENTS.md or the /new-part skill) and leaves the reason in memory.
3. **Memory has grown to 51 files and about 9,100 words, with heavy overlap.** Six files cover "show it in the viewer", five cover fasteners, four are one-line pointers to the /new-part skill, and several are stale (the CM1000 note still describes a 3-piece bracket in its title; setup facts say git isn't on PATH and "never push"). The diff merges them to 24 files.

Counts: 9 contradictions or overtaken rules, 11 stale facts, 14 duplicate groups, 5 wording findings, 3 flags with no edit.

## Where each rule lives, and its proposed single home

| Rule | Lives now | Proposed home | Others become |
|---|---|---|---|
| Push pre-approved, never force-push | global:26,28 · AGENTS:7,63,64 · memory push-asks-first, cloud-move-plan:14, setup-facts:16, brian-working-style:12 · commands commit-message:12, add-feature:11, wrap-session:10-11 | global (all projects) + one line in AGENTS "Working rules" | memory copies removed; commands updated (Q1) |
| No printing, purchases, publishing without Brian | AGENTS:6,7,19,23 · global:25 · skill:39 | AGENTS "Working rules" | global keeps its one line (other projects) |
| Repo private, no secrets | AGENTS:15,65,67 · global:27,28 · cloud-move-plan | AGENTS "Working rules" + global | memory copy removed |
| UNKNOWN / not validated | AGENTS:6,9,19,23,36,45,53,71,79 · skill:39 · global:50 | AGENTS "Working rules" (general) and beside each standard (specific) | unchanged in skill and global |
| Third-party meshes and licences | AGENTS:12,40,45,65,75 · global:15 · memory third-party, viewer-as-artifact, mesh-viewer-always:15, backup-locations:15, cm1000:14 · lib/README:8 | AGENTS "Third-party meshes and licences" (Q2) | memory keeps Brian's quotes; viewer sections drop their own copy |
| Four-corner mounting, corner holes only | AGENTS:6 · m6-bracket-hardware:17 | AGENTS "Settled standards" | memory file removed |
| 44.4 mm faceplate | AGENTS:69-71 · faceplate-44-standard | AGENTS "Settled standards" | memory file removed |
| Fastener and insert table | global:42-50 · AGENTS:81-83 · fastener-sizes, no-self-tapping, no-drilling-prints, m6-bracket-hardware:14 · skill:22 | global (all projects). AGENTS keeps a matching copy because cloud sessions can't read the global file | two memory files removed; no-drilling stays (incident) |
| M6 bracket hardware | AGENTS:77-79 · m6-bracket-hardware · own-printed-rack (M6 x 10) | AGENTS "Settled standards" (Q3) | memory file removed |
| Keystone default | keystone-settled only · lib/README:5 | AGENTS "Settled standards" (Q4) | memory keeps the why |
| OptiPlex orientation | optiplex-sleeve-settled only | AGENTS "Settled standards" (Q4) | memory keeps measurements and history |
| Own printed rack | own-printed-rack · HANDOFF:296 | AGENTS "Settled standards" (Q4) | memory keeps detail |
| Proven fit clearances | skill:12 · keep-proven-fit-dims · sleeve-height-tight · leave-design-margin | /new-part skill | memory keeps the incidents |
| Keep requested features | skill:11 · keep-requested-features · cm1000:20 | /new-part skill | memory keeps the incidents |
| Rounded floor corners, never fudge the mock, sleeve_top 0.8 | memory only | /new-part skill (added) | memory keeps the incidents |
| Test print IDs | AGENTS:54-56 · skill:24 · test-print-ids | AGENTS "Settled standards" | memory file removed |
| 3D viewer for every STL/3MF | global:13-16 · AGENTS:73-75 · mesh-viewer-always, viewer-as-artifact, viewer-assembled-as-is · skill:17,33 · PROJECT.md:29 | global (all projects); AGENTS keeps two lines for cloud; usage in PROJECT.md | three memory files → one (show-and-ask) |
| Measurement requests | global:18-19 · AGENTS:85-87 · always-diagrams, shop-talk, show-in-3d · skill:13 | global; AGENTS one line | three memory files → show-and-ask |
| Codex workflow and paste-ready prompt | global:32-40 · brian-working-style:8,13 · codex-prompt-delivery · single-prompt-batching · beta-heavy-work-to-codex | global | three memory files removed; beta-heavy stays |
| Gene photo | global:10-11 · gene-simmons-on-commit · skill:40 | global (with the "one per real accomplishment" limit added) | memory file removed |
| Memes, same message twice, efficient turns | global:22-24 · memes-welcome, duplicate-prompt-gif, brian-working-style | global | three memory files removed |
| No phase language | AGENTS:3 · no-phases · brian-working-style:11 | AGENTS "Working rules" | memory file removed |
| OpenSCAD snapshot | AGENTS:89-91, 13 · openscad-snapshot-new-parts · skill:17 | AGENTS "Settled standards" | memory folded into new-part-workflow |
| Cloud repo, devices, sessions | AGENTS:58-67 · global:29-30 · multi-device-setup, cloud-move-plan, setup-facts:12 | AGENTS "Working rules" | two memory files removed |
| Data location, start.bat | AGENTS:41 · setup-facts:13 | AGENTS "Working rules" | setup-facts keeps the commands |

## Findings, highest confidence first

Line numbers are for the files as they stand today. "mem/" is the memory folder.

### High — the repository or a later dated rule contradicts the text

| # | Location | Evidence | Problem | Action |
|---|---|---|---|---|
| H1 | AGENTS.md:7 | "No printing, purchases, uploads, release packaging, publishing, deployments or pushes without explicit authorization. This organization task authorizes none of those." | Contradicts AGENTS:63 and global:26 (push pre-approved 2026-10-22). "This organization task" refers to a housekeeping task from 2026-10-18. | rewrite: push removed from the list, fossil sentence removed (Q1) |
| H2 | mem/cloud-move-plan.md:14 · mem/setup-facts.md:16 · mem/brian-working-style.md:12 | "Each push still needs Brian's go-ahead" · "Commit locally only with Brian's OK; never push" · "confirm outward actions (push, upload, print)" | Same contradiction, three more copies. | remove (files merged or deleted) |
| H3 | .claude/commands/commit-message.md:12 · add-feature.md:11 · wrap-session.md:10-11 | "Never push." · "Don't run exports, builds, prints, pushes or uploads" · "Only write it after I say OK … Don't commit unless I say so." | Written 2026-10-20, before the push rule and the end-of-session rule (global:29). A command you type may be a deliberate careful mode, so this is yours to decide. | rewrite (Q1) |
| H4 | AGENTS.md:5 | "Most assets are untracked: a Git clone/commit alone is not a backup." | 3,040 files under outputs/ are tracked; AGENTS:60 says the whole project is in the repo. | rewrite |
| H5 | AGENTS.md:39 | "a second manufacturing adapter beside Pi4. Leave the Pi4 path untouched." | AGENTS:32 says the Pi path is retired and archived. AGENTS:32 itself has to explain that "older sections … describe the pre-cleanup state". | rewrite to the current rule; the explainer goes |
| H6 | AGENTS.md:12, 40, 45, 75 · global:15 · mem/mesh-viewer-always.md:15 | "Supplier/Pi assets … stay local" · "Creator parts stay local" · "local preview mesh only" · "never commit ones that embed third-party/licensed meshes" · "only our own meshes, never third-party ones" | AGENTS:60 puts them all in the private repo; Brian on 2026-11-03 and 2026-11-06 (mem/third-party-models-in-house.md:16-18) said to stop holding them back for private use. This loosens a prohibition, so it is yours to decide. The limits on redistribution and public release are kept either way. | rewrite into one licence section (Q2) |
| H7 | mem/multi-device-setup.md:11-14 · MEMORY.md:3 · mem/setup-facts.md:12 | "this desktop PC is the only live home … don't propose syncing/copying the project to other devices" | Overtaken by the private GitHub repo (AGENTS:58-66, 2026-10-20). "Don't expose the app on the LAN" is not overtaken and is kept in setup-facts. | remove; keep the LAN line |
| H8 | mem/cm1000-bracket.md:3,11 · MEMORY.md:25 | "3-piece bracket (faceplate + rails v2); files in outputs/STL_Deliveries/…" | Line 50 of the same file says the one-piece CM1P bracket supersedes it; HANDOFF shows CM1P-Q. The file is an 850-word dated changelog that duplicates HANDOFF and Fit_Findings. | rewrite to the durable facts (measured modem, don't-raise-again list, lessons) |
| H9 | mem/pi-is-sample-equipment.md:14 | "Print in color still gated for generic faceplates." | AGENTS:53: extended to wizard-made faceplates on 2026-10-21. | remove (file covered by AGENTS) |
| H10 | mem/setup-facts.md:11,14,16 | old C: copy "left untouched until Brian decides ~2026-10-28" · "52 Py + 47 JS passed 2026-10-19" · "git not on PATH" | Date has passed; test counts rot; git is at C:\Program Files\Git and on PATH. | rewrite |
| H11 | mem/backup-locations.md:15 | "see [[assembly-workshop-data-location]]" | No such memory file. | merge into setup-facts |
| H12 | mem/no-self-tapping.md:14 | "If the insert OD isn't measured, reuse the project's existing insert_pilot value and flag it UNKNOWN." | The insert table was measured the same day (global:45-48). | remove (file covered by global) |
| H13 | mem/optiplex-sleeve-settled.md:16 | "Printed baseline stays SLV-F until he reports a fit." | Same line says OPX-F printed with a good fit on 2026-11-04. | rewrite to point at HANDOFF and Fit_Findings |
| H14 | mem/stl-delivery-combined.md:15 | "any STL hand-off" → plate_layout_stl.py, outputs/STL_Deliveries/ | Since 2026-11-05 new parts get their 3MF from tools/release_part.py (skill:29-30). | rewrite: scope it to app tray + faceplate exports |
| H15 | AGENTS.md:79 | "Insert bore/OD/length come from Brian or a measured part; until then they are UNKNOWN." | AGENTS:83 gives the measured values (2026-10-31). | remove; fit and strength UNKNOWN is kept |
| H16 | AGENTS.md:83 vs global:46-47 | AGENTS: "M6x5x8 → 7.6 bore" · global: "7.6 mm bore, >= 6 mm deep … boss >= 9 mm OD" | Two copies of one table, one missing the depth and the boss size. | rewrite AGENTS to match global |
| H17 | AGENTS.md:79, 83 · global:49 vs mem/own-printed-rack.md:11 · HANDOFF:300 | "M6 x 8 button-head" · "ask before adding a new screw type" vs "Standard screw for this rack: M6 x 10" | A second M6 length exists that the standard table doesn't list. | flag (Q3); diff adds it scoped to the own rack |
| H18 | mem/always-diagrams.md:11 · mem/show-in-3d.md:14 vs global:19 | "answer with a diagram (show_widget SVG)" · "still draw a diagram for measurement requests" vs "never … a flat diagram" | The 2026-11-08 rule made measurement requests 3D. Flat SVG is still allowed for explaining an answer (always-diagrams:15), which only the memory says. | merge into show-and-ask, which states what each form is for |
| H19 | AGENTS.md:75 · global:15 vs mem/mesh-viewer-always.md:17, viewer-as-artifact | "send the page with SendUserFile" (no Artifact) vs "always publish the viewer as an Artifact and give the URL first" | The rule's home files leave out the part Brian got angry about twice. | add to global and AGENTS |
| H20 | global:11 vs mem/gene-simmons-on-commit.md:17 | "after every git commit and every finished task" vs "one Gene per real accomplishment … don't give me Gene when I haven't earned it" | The limit is only in memory. | add to global |

### Medium — duplicates that have drifted, history in rule files, wording

| # | Location | Evidence | Problem | Action |
|---|---|---|---|---|
| M1 | AGENTS.md:21-23, 30-32, 34-36 | "Confirmed specimen and parked research", "Raspberry Pi 4 is history", "These supersede the earlier 'Pi4 only adapter' … restrictions" | History told as narrative, and rules stated as a diff against rules the reader never saw. | move to a short "History" section; current rule stated once |
| M2 | AGENTS.md:6, 7, 23 | "no physical testing without Brian's direction" · "Physical test fitting is a ROADMAP 'Next' item" · "Digital checks pass and Brian confirms qualitative fit of the earlier supplied specimen" | Dozens of parts have been printed and reported since; this reads as if nothing has. The permission rule itself is current. | rewrite: "Brian does the printing … a fit report covers the reported specimen and feature only"; UNKNOWN kept |
| M3 | AGENTS.md:26-28, 47-49 | two GUI sections with "Brian subsequently requested", "These choices supersede the earlier unchosen concepts" | Recovery story, not rules. | rewrite to the final GUI rules plus pointers. Dropped as detail (it is in the decision files): the 1C/2C… option codes, "color presets plus custom picker; local artwork fit/center, size/position/remove; navigation first" |
| M4 | AGENTS.md:45 | "Ports come from a Pi 4 preset plus a wizard Ports step, then mesh-click fine-tuning. … Step 1 status: work/cable-management/Report.md" | A status line from 2026-10-19 with a Pi preset the deep clean targeted. Not checked against the app. | removed from the rewrite; say if you want it kept |
| M5 | AGENTS.md:13 vs :91 | "OpenSCAD.exe is the documented renderer" vs the snapshot rule | Two renderer rules far apart. | merge into one line |
| M6 | AGENTS.md:10 vs :79 | "Preserve M3 x 0.5 adapter limits" vs "This supersedes the M3 x 0.5 limit for new bracket designs only" | Rule and exception 70 lines apart. | merge |
| M7 | global:26 and :28 | "Never force-push" twice in one list | Duplicate. | merge |
| M8 | global:18-19, 39 | "ALWAYS", "ANY time", "No exceptions." | Capitals mostly add nothing for current models. The Codex-prompt line is kept as written: it has a repeated real failure behind it (mem/codex-prompt-delivery.md:13-15). The measurement heading is toned down, rule unchanged. | rewrite the heading only |
| M9 | mem/ six files on showing things | mesh-viewer-always, viewer-as-artifact, viewer-assembled-as-is, always-diagrams, show-in-3d, shop-talk | Each restates the global rule and adds one nuance; two disagree (H18). | merge into show-and-ask |
| M10 | mem/ four pointer files | draft-until-printing, release-part-tool, shared-parts-library, leave-design-margin, plus openscad-snapshot-new-parts | Each says "follow the /new-part skill". | merge into new-part-workflow (keeps the reasons) |
| M11 | mem/ working-style copies | memes-welcome, duplicate-prompt-gif, brian-working-style, gene-simmons-on-commit, push-asks-first, single-prompt-batching, codex-prompt-delivery | Copies of global:10-40. Unique points moved to global: plain language and recommendations, codex/ branches, never write "optional" for an existing feature, save prompts in docs/prompts/codex/, a file path alone is not enough. | remove after the moves |
| M12 | mem/ standards copies | fastener-sizes, no-self-tapping, m6-bracket-hardware, faceplate-44-standard, test-print-ids, no-phases, pi-is-sample-equipment | Copies of AGENTS and global. Unique points moved to AGENTS: corner holes only; tie-ins from behind. | remove after the moves |
| M13 | mem/m5-extrusion-frame.md | whole file | Marked history in the index; replaced 2026-11-09. Its one lasting lesson (check every view before sending) moves to own-printed-rack. | remove |
| M14 | skill new-part | no mention of rounded corners, sleeve_top 0.8 or the device-mock rule | Three part-design rules with incidents behind them are missing from the checklist every part follows. | add three lines |
| M15 | .claude/commands/resume-work.md:7 | "Read AGENTS.md, PROJECT.md and HANDOFF.md." | Skips `git pull` and ROADMAP.md, which AGENTS:3 and :62 require. | rewrite |
| M16 | mem/m6-bracket-hardware.md:11 | "Printed baseline list is at the top of HANDOFF.md." | It is at HANDOFF.md:217 now. | remove with the file; AGENTS says "listed in HANDOFF.md" |

### Low — flagged, no edit proposed

| # | Location | Note |
|---|---|---|
| L1 | mem/cm1000-bracket.md:38 · mem/own-printed-rack.md:11 | "plate 254 x 44.45" and "44.45/U" beside the 252 x 44.4 standard. Probably slot pitch versus plate height, and one part-specific plate. Worth one sentence from you if not. |
| L2 | .claude/launch.json | Two entries are both named "Mesh viewer pages" (ports 8861 and 8890). Starting one by name is ambiguous. Settings file, not edited. |
| L3 | .claude/commands (all 12) | Generic beginner templates with numbered steps ("I'm new to coding"). They work and you invoke them on purpose, so they are left alone apart from H3 and M15. |
| L4 | OptiPlex and CM1000 | Neither device has a card in docs/devices/; their measurements live only in memory and Fit_Findings. Not an instruction problem, but the /new-part skill expects a card. |
| L5 | mem/fresh-session-per-step.md · mem/beta-heavy-work-to-codex.md | "Start every step in a fresh session" overlaps the app's own session rules. Kept as written: it is your stated preference. |

## Nothing lost: where the protected items end up

| Item | After the diff |
|---|---|
| Four-corner mounting, 44.4 plate, fastener table, M6 bracket hardware, keystone default, OptiPlex orientation, own printed rack, test IDs, OpenSCAD rule | AGENTS.md "Settled standards" |
| Proven fit clearances, keep requested features, rounded floor corners, never fudge the mock, sleeve_top 0.8, design margin, no drilling | /new-part skill, with the incident notes kept in memory |
| Every UNKNOWN caveat | AGENTS.md "Working rules", each standard, the app section; skill; global fasteners |
| Licence and redistribution limits | AGENTS.md "Third-party meshes and licences"; memory third-party note; lib/README.md |
| No printing, purchases, publishing; private repo; never force-push; no secrets | AGENTS.md "Working rules"; global |
| Gene, memes, Codex workflow and prompt, efficient turns | global, unchanged apart from additions |
| Shop talk | memory show-and-ask; skill line 8 |

Two things the rewrite drops on purpose, both listed above: the GUI option codes (M3) and the cable planner status line (M4).

## Word counts (rough)

| Surface | Before | After |
|---|---|---|
| Global CLAUDE.md | 880 | 1,000 |
| AGENTS.md | 2,290 | 1,740 |
| Memory, 51 files + index → 24 + index | 9,110 | 4,500 |
| MEMORY.md index alone | 800 | 400 |
| /new-part skill | 860 | 930 |
| Commands | 1,260 | 1,270 |
| **Total** | **14,400** | **9,440** |
| Loaded every session (global + AGENTS + index) | 3,970 | 3,140 |

The global file and the skill grow because rules moved into them from memory.

## Decisions for Brian

Each lists the version that is current by date. The diff assumes the first option.

- **Q1 Pushing and committing.** Current: pre-approved since 2026-10-22, and end every session with handoff, commit and push. Old text: AGENTS:7, three memory files, and the commit-message, add-feature and wrap-session commands. Options: make everything match, or leave the three typed commands asking first.
- **Q2 Third-party meshes in viewer pages.** Current: 2026-11-03 and 2026-11-06, free use inside the private repo and private Artifacts. Old text: AGENTS:12, 40, 45, 75, global:15, one memory line. Options: free inside private repo and Artifacts, or Artifacts yes but keep those pages out of git.
- **Q3 M6 screw length.** M6 x 8 is the standard on hand; the own rack says M6 x 10. Options: x 8 for brackets and x 10 for the own rack only; x 10 for everything new; or x 8 everywhere.
- **Q4 Home for settled decisions now only in memory** (keystone, OptiPlex orientation, own rack; rounded corners, mock rule and sleeve_top into the skill). Options: move the rule into the repo so every device sees it, or leave them in PC memory.

**Brian's answers (2026-11-11):** Q1 pre-approved everywhere, commands included. Q2 free inside the private repo and private Artifacts. Q3 **M6 x 10 for everything new**; printed revisions keep M6 x 8. Q4 move the rules into the repo. The diff now reflects all four.

Approving the diff also confirms the overtaken items where the newer version is not in doubt: H2, H4, H5, H7 to H16.

## How this was checked

Every path, tool and flag named in the audited files was looked up: all exist except the memory link in H11. `tools/release_part.py` has `--against`, `--posts`, `--cuts` and `--keepout`; `tools/mesh_viewer.py` has `--as-is` and `--measure`. No behaviour was tested with the model: removing a rule here is a proposal, and the first few sessions after applying are the real check.

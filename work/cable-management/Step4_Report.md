# Cable management Step 4: routing suggestions (2026-10-19)

Built from Brian's 12 decisions in [Step4_Decisions.md](Step4_Decisions.md). Claude and Codex split the work and never edited the same file at the same time. Suggestions are **advice only**: none blocks Save, and none says a real cable or guide fits. Guide capacity, real bend tolerance, cable size and rear clearance stay **UNKNOWN**. Bend figures are generic guidance on nominal sizes. Everything is planning data in `rack.cabling` and saves only through the explicit Save. Nothing reaches any STL. The Pi 4 is only sample equipment: no rule is Pi-specific.

## What was built
- **Codex [task 11](../codex-tasks/11-cable-suggest-schema-REPORT.md):** `cable_plan.py` accepts and validates `cables[i].carries`, `cables[i].unplug_often`, `settings.power_post` and `settings.ignored_suggestions`. Each is output only when supplied, so older racks load unchanged. Python tests were added.
- **Codex [task 12](../codex-tasks/12-cable-suggest-logic-REPORT.md):** `cable-suggest.js` (`LabRaxCableSuggest`) holds the 11 rules: power/data post, missing guide, one exit, top exit, keystone, service loop, short run, bend, crowding, one-ended, unused ports. It also has the four Apply kinds (move-post, add-guide, set-exit, drop-guides), Ignore/unignore/prune with state signatures, and 20 Node tests. The API matches the frozen contract exactly.
- **Claude:**
  - Review tab: a "Cable suggestions" card with a count, Show me / Done, Apply, Ignore and "Show ignored" with Bring back.
  - Undo for the last Apply, shown in the message and in the card. It is only offered while the cabling hasn't changed since that Apply.
  - Show me turns on Cables mode if needed, lights the cables, guides, ports and exits involved and dims the rest. Done or Esc clears it, and leaving Review clears it too.
  - `rack-studio.js` dims guides, ports and exits flagged `dim`. The asset manifest hash was refreshed with `register_step2.py`.
  - Cable panel: "Carries" (From type (…) / Power / Data) and an "Unplugged often" tick box. The rack settings gain a "Power post" choice (RR default, or RL).
  - Ignored suggestions are pruned in the existing upkeep hook, so they come back when the cables involved change.
  - `index.html` and `app.py` load and serve `cable-suggest.js`. CSS was added to `workspace.css`.
- **Integration edits to Codex's files (after Codex finished):**
  - Wording: the one-exit text named a raw exit id; "power belongs…" started lowercase; "1 tight turns"; the two Pi 4s were indistinguishable in unused-ports, so titles now carry the slot ("Raspberry Pi 4 (U01)").
  - Three test regexes in `js-tests/cable-suggest.js` were updated to the new wording.
  - Codex's originals are in `%TEMP%` only; Codex's own archive copies are in `docs/archive/codex/2026-10-19/task11-12/`.

## Verified
- `run_checks.ps1`: **all checks passed**, 73 Python and 114 JavaScript tests (24 module, 27 page logic, 16 BOM, 9 rebuild, 18 cable routes, 20 cable suggestions).
- Browser check on a disposable copy of `data/normal-use` (server `disposable-cables4-8777`; my scratchpad copy was seeded with 3 guides, 2 exits, 2 endpoints and 4 cables made to trigger rules; the original was only copied, never written). No console errors:
  - All 11 suggestion kinds appeared with plain wording.
  - Show me turned Cables mode on and showed the "Showing …" bar; Esc cleared it and turned Cables mode back off.
  - **Move to RR** applied in the draft ("Unsaved changes"). Undo restored it.
  - **Add guide** added RL U04.
  - **Ignore** hid the keystone suggestion.
  - Save → the file on disk held the new guide and `ignored_suggestions` → reload kept the ignore. Changing C2's Carries to Power brought it back by itself.
  - Swapping the power post to RL changed which cables are flagged.
  - **Use this exit** cleared both exit suggestions. **Drop guides** cleared the short-run and bend items for C3. **Bring back** restored an ignored item.
- `data/normal-use/rack-workspace.json` was not touched (last changed 19:09, before this check).

## Not verified
- **The highlight and dimming in the 3D view was not seen on screen.** The Browser pane was hidden, so the page drew no frames. The `lit`, `dim` and `selected` flags are set in code and the renderer change is small, but no screenshot was taken.
- **Not tried at all:** wizard-equipment cables, keystone pairs and crowding in the browser (Node tests only). The copied data has only two Pi 4s.
- The bend rule uses straight segments between route points with nominal diameters. It is rough guidance, and it may flag many port-to-guide corners on real plans.
- No exports, printing, commits or pushes. The normal 8765 server still runs the old code until Brian restarts it with start.bat.

## Next
Step 5: the wiring sheet (SVG and a printable page), the CSV schedule and labels.

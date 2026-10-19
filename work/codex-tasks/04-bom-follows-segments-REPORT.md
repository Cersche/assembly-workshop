# Task 04 — BOM follows chosen segments: plan only

2026-10-19. Complete as a plan. No implementation, tests, builds or exports run. Only this new report was written; no outside-scope edit is needed to deliver the plan. Future implementation files below are recommendations, not changes made or authorized here.

## Observed code

- `outputs/Mechanical_Design_App/workspace.js:494` renderBom(slots) always uses defaultLevels(slots), ignoring rack.post_levels. setSlots() calls it; openRackDialog() supplies height only. The chips and drop target only increase height; they do not record the selected chip as a chosen post segment. Do not claim they currently preserve arbitrary chip choices.
- defaultLevels():665 constructs an extension-aware default, not a simple 5U-first split of the full height: n=ceil((slots+1)/6), fill posts bottom-up with the largest at the top; sum(posts)+n-1=slots. sideLevels():666 uses each saved side when its height matches, otherwise defaults. stackHeight():658 counts each joint as its own 1U.
- rackFrame():668 places two posts per segment per side, one extension per joint per side and one side panel per post segment when enabled. It removes the older rack-scene frame's posts/side panels before inserting the chosen stacks. moveExtension():822 edits one side in the draft; lock prevents movement, not counting.
- drawRackPreview():506 currently calls rackFrame without the editing rack, so dialog preview also defaults. Rack submission preserves saved stacks/lock only if height is unchanged. A corrected BOM must share the same effective draft as that preview rather than show a different stack.
- downloadRackStl():689 already counts chosen scene parts and has an extension fallback when the preview mesh is unavailable. RACK_PART_SOURCES excludes the local-only cable guide. Export must not depend on preview-asset availability for required part counts.
- `rack_stl.py:37` export(payload) validates submitted component IDs/counts and writes their parts list; it does not derive a rack stack or hardware BOM. `app.py:758` /api/bom is the selected assembly hardware CSV (quantity 2 per selected kind), not a rack BOM; leave that separate Pi4 contract alone.
- `rack_workspace.py:80` validates saved side arrays: integer sizes 1–5, nonempty, sum+joint count=slots; sides may be omitted individually. Schema accepts 1–48 slots while the setup slider clamps to 1–14.

## Proposed exact counting rule

Use a single pure effective-layout/count helper shared by the dialog BOM, dialog preview and rack-frame parts counting. For each side s in {left,right}, take its valid saved/draft stack L_s; use defaultLevels(height) for an absent side only. Reject explicitly malformed stacks for a proposed parts list instead of silently claiming that their default replacements are chosen segments. Do not mutate or save the rack while counting.

- A valid stack has positive integer sizes 1–5 and sum(L_s)+len(L_s)-1=height.
- For each size u, post count P_u = 2 * (occurrences of u in L_left + occurrences of u in L_right). The factor 2 is front/rear on each side; retain the existing four-post topology pending Brian's confirmation.
- Extensions E = (len(L_left)-1)+(len(L_right)-1). Each occupies one U on its own side and is one spanning support extension, not one per front/rear post.
- Retain the existing nominal full-hole provisioning rule: bolts B = inserts I = 3 * 2 * (sum(L_left)+sum(L_right)). This is three holes per post U on both front/rear posts, excluding extension U. Label it "Full-hole hardware allowance; installed quantity UNKNOWN" rather than claiming that every hole requires an installed bolt. The per-faceplate four-hole decision is a distinct rule and must not replace this rack-hole multiplier.
- Extension fastening hardware quantity/type: UNKNOWN; show a separate explicit row, never add zero or invent a multiplier. Other frame/side-panel fastening quantities also remain UNKNOWN unless documented. No purchasing or physical approval follows from these counts.
- With side panels on, size-u side-panel count S_u = occurrences of u in both side stacks (one per side per segment). With them off, S_u=0. Do not create a panel for extension U.
- Fixed source-frame pieces retained from rack-scene.frame: 2 bottom beams, 1 top-front beam, 1 top-rear beam, 4 side rails, 1 bottom panel, 1 top panel, 4 feet, 2 handles. "Include side panels" affects the segmented side panels only in current code; top/bottom remain. Make that scope explicit, do not silently redefine it. Cable guides/ports/artwork are excluded from manufacturing counts.

## Proposed functions and implementation boundaries

1. workspace.js: add pure validated effective-stack/count helper beside defaultLevels/sideLevels. Keep established default generation and four-post topology unchanged. Derive required extension counts independently of loaded meshes.
2. renderBom(): accept the effective editing rack, show size-specific post/panel counts, extension count and explicitly labeled hardware allowance/UNKNOWN rows. Use a shared count result, not a second independent formula.
3. openRackDialog(), setSlots(), drawRackPreview(): maintain an in-memory editing rack; retain stacks at unchanged height, deliberately default/relabel stacks when height changes under existing behavior. Pass this same draft to BOM and preview. Apply/cancel must preserve normal draft/Save semantics.
4. moveExtension()/inspector rendering: refresh any visible BOM after a permitted move; unlocked and locked layouts count identically. If a persistent BOM is added, place it in existing rack settings/Setup, without rearranging the final left groups.
5. downloadRackStl(): consume the same logical part counts so missing optional viewer assets cannot remove required extensions. Keep guide exclusion and local-only creator rights. No server counting equivalent currently needs replacement; retain rack_stl.py's input validation and assembly /api/bom contract. Any future server-side canonical rack BOM would be separate scope.
6. Future tests in a new Node built-in test file registered in run_checks.ps1; server schema tests only if that implementation changes validation. All future source/runner edits require archive copies first and separate implementation authorization.

## Worked examples

Arrays are bottom-up; +1U is implicit at each array boundary. Counts below use the provisional current topology and full-hole allowance, not a certified installed hardware requirement.

| Height | Left / right stacks | Posts by size (both sides total) | Extensions | Bolts / inserts allowance | Side panels on |
| --- | --- | --- | --- | --- | --- |
| 5U default | [5] / [5] | 4 x 5U | 0 | 60 / 60 | 2 x 5U |
| 5U custom | [1,3] / [5] | 2 x 1U, 2 x 3U, 2 x 5U | 1 | 54 / 54 | 1 each of 1U, 3U, 5U |
| 9U default | [3,5] / [3,5] | 4 x 3U, 4 x 5U | 2 | 96 / 96 | 2 x 3U, 2 x 5U |
| 9U custom | [3,5] / [4,4] | 2 x 3U, 4 x 4U, 2 x 5U | 2 | 96 / 96 | 1 x 3U, 2 x 4U, 1 x 5U |
| 14U default | [2,5,5] / [2,5,5] | 4 x 2U, 8 x 5U | 4 | 144 / 144 | 2 x 2U, 4 x 5U |
| 14U custom | [2,5,5] / [4,4,4] | 2 x 2U, 6 x 4U, 4 x 5U | 4 | 144 / 144 | 1 x 2U, 3 x 4U, 2 x 5U |

Every example also has the fixed frame pieces above; side panels off removes only the last column. Extension fasteners and assembled fit/strength remain UNKNOWN. The asymmetric 5U example proves why even total hardware allowances can change at unchanged rack height.

## Edge cases and proposed tests

- Legacy rack has no post_levels: default each side without writes; test exact defaults/counts for 5U, 9U, 14U and minimal 1U.
- One side missing: default only that side; preserve the supplied valid side. Test unequal side segment sizes and unequal numbers of joints.
- Invalid saved/draft arrays: reject empty, fractional, string, boolean, out-of-range, wrong-height and non-array stacks; display diagnostic, no fabricated chosen BOM.
- Locked/unlocked: same counts; allowed moves change only adjacent segment sizes and retain height; lock blocks moves. Test no silent Save.
- Editing height unchanged retains chosen stacks; height change defaults and labels them; cancel leaves the prior rack/draft unchanged. Chips currently alter height only: test this rather than invent a segment-selection capability.
- Test each worked example, size aggregation, allowance formula excluding extension U, explicit UNKNOWN extension fasteners and sorted display rows.
- Side panels off/on: exact S_u counts; top/bottom panels remain. Test fixed frame inventory stays unchanged.
- Required extension mesh absent: logical E remains correct and exporter count input still includes it; preview must keep its existing missing-asset behavior separate from BOM claims.
- Guides/ports/artwork: never appear in rack manufacturing part counts. No meshes need exporting to test count payloads.
- Compare logical post/panel counts against rackFrame's fixture parts with source assets stubbed; default and custom stacks must agree. No server/export invocation in acceptance tests.
- Test setup's 14U limit and server's 48U bound separately; do not silently widen the setup UI in a BOM change.

## Every POSTS identifier use

Targeted whole-word search across runnable app JS/Python found only workspace.js:

| Line | Use |
| --- | --- |
| 485 | Declaration const POSTS = 4, HOLES_PER_U = 3. |
| 498 | Multiplies total default post-U holes by POSTS. |
| 500 | Multiplies each default size's segment count by POSTS, and interpolates POSTS again in the "per post x posts" label. |

No server POSTS identifier found. Separate hard-coded topology exists in rackFrame's two front/rear poses for each of two sides and rack-scene.frame's four placements; report these without changing them. GUIDE_POSTS names four guide positions and is a distinct identifier. Search covered runnable app .js/.py (including reference helpers), not unrelated historical work/output trees.

## Commands, changed files, assumptions and questions

Commands actually run: UTF-8 Get-Content of standing/project/status/task docs; targeted rg for BOM/POSTS/stack/export references; Get-Content source ranges in workspace.js, rack_workspace.py, rack_stl.py, app.py and rack-references/rack-scene.js; Test-Path confirmed reports 04–06 did not exist. Reads only. apply_patch wrote this new UTF-8 report. No tests were run for this plan.

Files changed: only work/codex-tasks/04-bom-follows-segments-REPORT.md; before SHA-256 absent (new). Final after hash recorded in completion tool output; self-hash excluded from its own content. No existing file was edited, so no archive copy required.

Open questions for Brian: confirm four-post topology and whether full-hole bolt/insert allowance should remain visible versus actual installed fastener quantities; extension/frame/panel hardware quantities remain UNKNOWN. No decision is needed to finish this plan. Do not infer printed fit/strength from logical count agreement. Any implementation is future work requiring a task with source edits in its May change list.

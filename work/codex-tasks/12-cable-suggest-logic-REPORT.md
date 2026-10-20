# Task 12 report — 2026-10-19

Completed after task 11. Added the pure suggestion module, twenty Node tests, and runner registration. Final checks: 73 Python + 114 JavaScript passed.

API as built:
- RULES, in the specified eleven-rule order; BEND_FACTOR = {rj45: 4, other: 10}.
- carries(rack, cable, ctx), powerPost(rack), dataPost(rack).
- suggestions(rack, ctx, {includeIgnored = false} = {}), returning the exact id/rule/level/title/detail/involves/apply/applyLabel/sig/ignored shape.
- applySuggestion(rack, suggestion, ctx), returning {ok, message}; supports move-post, add-guide, set-exit and drop-guides only. Checks involved and action references before editing, then calls ctx.cables.upkeep(rack, ctx). Only rack.cabling changes. An upkeep exception restores the prior cabling.
- ignore(rack, suggestion), unignore(rack, id), pruneIgnored(rack, ctx).
- IIFE global LabRaxCableSuggest plus CommonJS module.exports. No DOM, window or fetch. Signature hashing is internal; each suggestion exposes sig. No exported API deviations.

Files (SHA-256 before → after):
- outputs/Mechanical_Design_App/cable-suggest.js: NEW (absent) → 6649CD1BFFE532EA78A7F35AAA34079340CA1E9081128FC02BE49C6E05011DC4
- outputs/Mechanical_Design_App/js-tests/cable-suggest.js: NEW (absent) → D1242BAB92631ACB3D7D0F78C8048D400BF934756F9538622174D73333C929B2
- outputs/Mechanical_Design_App/run_checks.ps1: 5817BA6D84EAC7152B983971F4BA874D91A5FAF2FEA8FB337EB8236CED7DABF7 → DF55390265DEC3EFD679E1E84B0F82C40FDFC6E6667F29B0C6445E7027120B7D

The runner original is archived byte-for-byte in docs/archive/codex/2026-10-19/task11-12/run_checks.ps1. Only its suggestion-test registration changed. All three task files use LF (zero CR bytes).

Commands actually run and results:
- Get-Content -Encoding UTF8 for project/task guidance, Step3/Step4 decisions, cable-routes.js, cable-ports.js, routing tests and run_checks.ps1: successful reads.
- rg -n -A 58 'def _cabling' outputs/Mechanical_Design_App/rack_workspace.py: inspected guide constraints read-only.
- apply_patch: created module/tests, registered tests, then fixed exact-1U subtraction noise and counted all cable users when selecting the top-exit alternative.
- & "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe" --test-reporter=spec outputs/Mechanical_Design_App/js-tests/cable-suggest.js: initial run 19/20 passed; exact-1U test failed because floating-point subtraction yielded just under 44.45. After correction, 20/20 passed.
- Tests invoke C:/Program Files/Python310/python.exe -B -c with JSON on stdin and rack_workspace._cabling: all four apply kinds, random guide ids and the 500-entry ignore list passed the real Python schema. No persisted test data.
- powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1: exit 0, 73 Python and 114 JavaScript passed (24 module, 27 page, 16 BOM, 9 rebuild, 18 routing, 20 suggestion tests).
- ReadAllBytes and Get-FileHash: confirmed LF and collected final hashes for both tasks.
- git diff -- outputs/Mechanical_Design_App/run_checks.ps1 outputs/Mechanical_Design_App/cable_plan.py outputs/Mechanical_Design_App/test_cable_plan.py: no tracked diff output; archive copies are the before-state evidence.

Coverage: every rule firing/not firing; carries and power/data defaults; missing-guide merging, direction/anchor/exit slots; exit target ties and fallback; each apply action and stale references; occupied guide spot and duplicate id refusal; automatic route pickup/manual route preservation; bend right-angle/reversal/straight/repeated-point math; signatures and ignored-state changes; 500 cap; includeIgnored; sorting, complete result shape and read-only idempotence.

Assumptions and limits:
- FNV-1a hashes UTF-8 bytes of JSON.stringify of the specified involved state. Like every 32-bit hash, collisions are mathematically possible; settings and unrelated state are outside the frozen signature inputs.
- A repeated path point has no defined turn angle, so that degenerate corner is skipped. Exact-1U height comparisons suppress only floating-point subtraction noise.
- Rule subjects sort lexically within RULES order; exit ties preserve cabling.exits order.
- Apply operates on schema-valid drafts, refuses stale references, and stages cabling before upkeep. Tests validate resulting shape with the real Python validator.
- UI integration and browser acceptance belong to Claude per task scope; neither was performed here. No UI files, user data, live server, geometry, exports, pins or asset manifests changed.
- Suggestions are planning advice only. Fit, capacity, strength and real bend tolerance remain UNKNOWN.

Open questions: none blocking this API. No additional work started.

# 07 — Rack BOM follows the chosen post segments (implementation)

**Goal:** the rack setup BOM must count the post stacks actually chosen/saved per side, not always the default. Implements the plan in [04-bom-follows-segments-REPORT.md](04-bom-follows-segments-REPORT.md), reviewed and approved by Claude 2026-10-19.

**Decisions (Brian, 2026-10-19):** keep the current four-post topology (front/rear per side) and the existing 3 holes per post U. Show the bolt/insert number as "Full-hole hardware allowance; installed quantity UNKNOWN". Extension and other frame fastener quantities are shown as an explicit UNKNOWN row, never 0 or a guess.

**Do:**
1. In workspace.js, add ONE pure helper (e.g. `rackCounts(rack)`) beside defaultLevels/sideLevels: effective stack per side (saved valid stack, default only for a missing side; invalid stack → error result, no fabricated BOM), posts by size, extensions, side panels by size (when enabled), full-hole allowance, fixed frame pieces as listed in the plan. No mutation, no saving.
2. renderBom() and drawRackPreview() use the same in-memory editing rack and that helper. Height unchanged keeps chosen stacks; height change falls back to defaults (current behavior). moveExtension() refreshes a visible BOM.
3. downloadRackStl() takes required extension/post counts from the helper so a missing preview mesh can't drop parts. Cable guides, ports and artwork never appear in counts. Do not run an export.
4. Leave rack_stl.py, rack_workspace.py validation, /api/bom (Pi4 hardware CSV) and the 14U setup limit unchanged.
5. Tests: a new Node built-in test file in js-tests/ (register it in run_checks.ps1) covering every worked example in the plan's table, missing side, invalid stacks, locked = unlocked counts, side panels on/off, no guides in counts, and helper vs rackFrame agreement with assets stubbed.

**May change:** outputs/Mechanical_Design_App/workspace.js, outputs/Mechanical_Design_App/run_checks.ps1, new files in outputs/Mechanical_Design_App/js-tests/. Archive copies of existing files first.

**Done when:** run_checks.ps1 passes (report new counts), the report lists each worked example's computed result, and no server/export/user data was touched.

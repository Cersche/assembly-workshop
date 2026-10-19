# 04 — Plan: BOM follows the chosen post segments (PLAN ONLY)

**Goal:** ROADMAP "Later". The rack bill of materials splits height largest-first instead of using the segments the user chose (`rack.post_levels`, with each 1U extension taking its own U).

**Do:** read the BOM code (`renderBom()` and helpers in workspace.js, plus any server equivalent) and write a plan: which functions change, the exact new counting rule (posts per segment size, extensions per joint, bolts/inserts), edge cases (no post_levels saved, unlocked layout, side panels), and the tests you would add. Also list every place the four-post assumption (`POSTS`) is used, without changing it.

**May change:** nothing except the report. NO code changes in this task.

**Done when:** the report contains the plan, the test list, and worked examples for 5U, 9U and 14U racks.

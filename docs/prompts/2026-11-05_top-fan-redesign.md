# New session: redesign the rack top for a 200 mm fan

Paste this into a fresh session:

```
New session: start redesigning the top of the rack so it takes a 200 mm exhaust fan.

First: git pull, then read AGENTS.md, HANDOFF.md (top entries) and work/rack-cooling/Decisions.md. That file has everything decided in the cooling session on 2026-11-05: chimney airflow (bottom intake with a filter, low side vents only, 200 mm fan on top blowing up), the saved rack order (CM1000 at the top, right under the fan), fan candidates and power ideas, and the stock Lab Rax top dimensions (top panel 228 x 171.5, only ~170 deep, too shallow for a 200 mm fan, which is why we redesign it).

Goal for this session: plan and draft our own top pieces (top panel and, if needed, new top front/rear edges and side handles) that hold a 200 mm fan, with a grille, mounting for a 12 V adapter (and a 12 to 5 V converter if the fan is ARGB) near the fan, and room for the wiring. Our own design: don't copy the creator's meshes (mklements, BY-NC-SA, local only); use them only to read the mating geometry (post tops, hole positions). Viewer pages that embed them stay uncommitted.

Use the new 3D part workflow: run the /new-part skill and follow its checklist. That means a device card in docs/devices/ for the fan (and the rack top interface) with measurements before the first print, lib/workshop.scad + pinned BOSL2, the OpenSCAD snapshot with --backend=manifold, tools/release_part.py, drafts as viewer pages only until I say I'm printing, a test print ID on every part, and a fit report by ID after printing.

Open questions to settle early (ask with a diagram for any measurement; work/rack-cooling/top_fan_space_measure.svg is a start):
1. Which 200 mm fan (Noctua NF-A20 for quiet vs Cooler Master MF200R ARGB for RGB, or another). Its hole spacing and thickness drive the design.
2. Headroom under the current top panel, and the real inside width/depth of my printed rack top.
3. How the new top attaches to the posts (M6 inserts and M6 x 8 button heads for weight-bearing joints, M3 elsewhere; no self-tapping, no drilling prints).
4. Adapter/converter model and where it mounts.

Offload big mechanical work to Codex (specs in work/codex-tasks/, and give me the ready-to-paste Codex prompt). At the end: update HANDOFF.md, commit and push.
```

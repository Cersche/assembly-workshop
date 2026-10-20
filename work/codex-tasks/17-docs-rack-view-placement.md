# 17 — Docs: rack view now draws each slot's tray

**Goal:** two docs still say the rack view shows the library mesh with a "Placement not rendered yet" note. That is no longer true (`work/equipment-wizard-options/Wizard_Fixes_Report.md`). Update the sentence in each file, plain language, short. No phase numbers.

Facts (read the sources to confirm; do not invent):
- A wizard slot with no tray settings shows the library item's build.
- A slot with tray settings shows an exact render of those settings if one already exists (Place on tray → Render exact preview or Generate); the rack view only looks it up (`/api/equipment-placement-mesh`), it never renders.
- Otherwise it shows a box sketch of those settings (plate U height, tray size/offset/rotation, rear bracket, dark blocks for keystone and port openings) and the inspector says so.
- Keystone faceplates no longer fail the mesh check (same report). Fit, retention, strength stay UNKNOWN.

Files and lines: `outputs/Mechanical_Design_App/README.md` (the "Cable ports and clearance screening…" paragraph, about line 23) and `outputs/Mechanical_Design_App/hardware-records.md` (end of the "equipment wizard records" paragraph, about line 15). Keep every existing scope limit and UNKNOWN.

**May change:** those two files only (archive copies first). Then write `17-docs-rack-view-placement-REPORT.md` per the standing rules.

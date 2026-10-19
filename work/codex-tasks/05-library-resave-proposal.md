# 05 — Proposal: flag and rebuild outdated library items (PROPOSAL ONLY)

**Goal:** ROADMAP "Later". Equipment library items saved before the 4 mm / four-hole plate change (and now keystone v2) keep their old builds until re-saved by hand.

**Do:** investigate how library items store their template version or build (data/equipment-library.json format via equipment.py; read the CODE, not user data). Propose how to detect an outdated item and how a one-click "rebuild with current template" would create a NEW build and never overwrite the old one. Include the UI wording, where the button lives (respect the final left-panel grouping), and the tests needed.

**May change:** nothing except the report. NO code changes. Do not open data/normal-use.

**Done when:** the report gives the detection rule, the rebuild flow, the UI and the test list, plus open questions for Brian.

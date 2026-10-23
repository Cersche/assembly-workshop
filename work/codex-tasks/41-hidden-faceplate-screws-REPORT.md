# Task 41 report — hidden faceplate screws (opt-in `hidden_joint`)

2026-10-22. Done by Claude directly (Brian: "run the codex task yourself"), no subagents. PROPOSED — UNVALIDATED: fit, M3 thread engagement in the 4.0 mm pilot at the new position, strength and driver access are UNKNOWN. No printing, no coupon, no push of renders; disposable data only (scratchpad folders, never data/normal-use).

## What changed
- New opt-in key `hidden_joint` (bool, default false; stored only when true). Sleeve + `joint="screw"` only; mutually exclusive with `insert_bosses` and `tray_follow` (errors in SCAD assert, Python and JS).
- On: the sleeve's FRONT joint is the proven tongue/boss/upright joint, centred at `dev_off_x ± (sl_half + sl_wall + 2 + 9)` (±77.5 mm for a 120 mm device), same Z (tray_z+14), same dimensions. The 3.4 mm holes through the plate front and the sleeve-wall pilots/insert bosses are not generated. Tray half-width = device/2 + 0.5 + 6 + 2 + 18; hard limit 204 mm stays, so devices up to 150 mm wide fit (tray 203 mm); wider ones fail with the existing width message plus "the hidden screw joint adds about 20 mm of tray beside each sleeve wall; turn it off".
- Rear joints (rear_support) unchanged (`joint_x`, ±40). **Assembly order: drive the front screws from behind BEFORE attaching the rear bracket; a fitted bracket plate would block the driver.**
- SCAD: `hj_x`, `jon(r)`, `jxs(r)` and two asserts (needs sleeve+screw+no insert bosses; joint edge ≥ 3 mm from rack-slot capsules). Python: `HJ_REPLACEMENTS` table (the SCAD template and the reversal table are the same pairs) so sources without the key are the old text. `port_openings.sleeve` / `port-openings.js sleeve` return the hidden joint positions with `joint_z=[]`, which also removes the 3.4 mm keep-out circles from Print in color (`faceplate_color.openings`, `equipment-wizard.js openings`, bezel obstacles) with no change to those files.
- Opening checks: a front opening within 9 + 1 mm (+ half its width) of a hidden joint centre and below Z 22.5 + 1 is refused (Python and JS).
- UI: Place on tray shows a "Hidden screws" toggle for sleeve mounts; preview draws floor block, upright and plate boss.

## Acceptance
1. `run_checks.ps1`: **200 Python (1 skipped) OK, all JS suites OK, RESULT: all checks passed.** New: Python `HiddenJointTests` (5), JS 3 tests in `js-tests/sleeve-v2.js`. `asset-manifest.json` hashes updated for `port-openings.js` and `tray-placement.js` (LF-normalized).
2. Exact renders (OpenSCAD, disposable folder): 120 mm 1U, 150 mm 1U, 120 mm 2U, 120 mm with rear support. All faceplate/tray/rear_bracket STLs closed (read_mesh strict). Ray-parity probes on the meshes (trimesh, numpy; not part of the app): plate front solid at the joint axis and at the old screw positions (no holes); boss pilot hollow; tray clearance hole hollow on the same axis (x = ±77.5 / ±(w/2+26.5), z = 14.5); upright solid; tray x-range ±86.5 (120 mm) and ±101.5 (150 mm = 203 mm wide, 11.8 mm clear of the rack-slot capsules).
3. Legacy: `eq.source(eq.clean(spec))` SHA-256 identical, HEAD vs working tree, for 19 specs (7 coupon specs, 2 library items, SLV-B with each and all v2 options, plain/rear/v2top sleeves, inserts). Identical sources mean identical OpenSCAD input, so meshes are identical; no separate triangle comparison was run.
4. Browser (disposable server on port 8710, stopped): page loads without console errors; `TrayPlacement` in the page accepts `hidden_joint`, returns joints ±77.5 and tray 173 mm, and the served `tray-placement.js` contains the toggle. **The toggle was not clicked through in the UI** (no sleeve item in the starter library; not built). Honest gap.
5. Print in color: unit test shows 4 keep-out circles of 3.4 mm without the key and 0 with it. Not exercised through the export endpoint.

## Open / UNKNOWN
Printed fit, M3 into the 4.0 mm pilot (same as the printed non-sleeve joint, new location), strength, driver access with a real driver, wide devices (> 150 mm) have no hidden option, joint only on the first U of multi-U plates (as today).

## Files and SHA-256 (paths relative to outputs/Mechanical_Design_App/)
| File | Before | After |
| --- | --- | --- |
| `equipment.py` | `9509b968e23cb19985481cec4c350bc1eb4131d6653c6466c5e65e3f40a1a3d5` | `f81bbe4d7ba7fb10c9d7a2e105ceba74af672dc60a72b18f33d14f8697828a8f` |
| `equipment_tray.scad` | `f3a4cc67b26a8c82809617723965942a7f70347e10e43f6f7f1113b7d0ee3858` | `14ae1a6f5463e96344512d0f38fc15105238650e6996228fa5e4d53da1d0d17e` |
| `port_openings.py` | `27a04b620c767eeb89fcc469e52960dd5f192cb6b0ab55d3f4afa1f3054e17cc` | `c336b11e705a0acc6d55b5080a1def08d2991b359ea39d82a928f3021b8f50a2` |
| `port-openings.js` | `66b5451c9917dd57f05829d5fcf433bce5eff2932f3bd7f906784c06a1da7265` | `4f67de47b5a1ee91cf286873aefd995555550a97ce8ec5a48030229784a77dd4` |
| `tray-placement.js` | `555e0455d5ac1ed8133753f3620d5ad3788fe68e317cf847dbb9c66c6b1acaab` | `c2a680bdd34150a5fde0fae243782cea36cbcb926987bb157888eed4e18cd9ef` |
| `asset-manifest.json` | `ca712f89618a3a00e54e81de1e06378a9b8ef0e7857bcecea6912ea365090e9d` | `31094e6ccdc517ef0df3e002f889f91b869e29b87044e1da6d7c214d29a3c7d1` |
| `test_tray_placement.py` | `e2020ee475dc595b18f3f01f85a49e13851ae917203b3bf52e434f02d2895a94` | `43f01441285dfb04364364cb883e664329341f67141185d5de642c39e179066d` |
| `test_allocation_tray.py` | `2abb89ae7bb5cdca1fc853e6db715bffd77167b85109efa9c138ac4a58022091` | `ad9903f7db786ec29d82758d2643dbf52c55ff6592b8e845f67c503434817da9` |
| `js-tests/sleeve-v2.js` | `309bbe51950f20f0883d92857631c5b8169161127d849bf4d3831b8f93b3e023` | `042b53214536de8dc2fc385b6532b87b14ab5895ccb27a82618b4973139e2abb` |

# Task 34 · Protrusion and keep-clear polish (follow-up to 32/33)

Claude's review of tasks 32 and 33 (2026-10-20) with Brian's real TP-Link SG108 STEP on disposable data found three small things worth fixing. Standing rules in [README.md](README.md) apply. Fit, cable bend space and strength stay UNKNOWN. Printing and exports are not authorized.

## Build

1. **One question per plug, not per part.** The SG108 STEP has its cable, plug body and plug tip as three separate bodies at the back, so the wizard asked three questions about one plug. Merge candidates on the **same face** whose boxes overlap or touch (name the tolerance, e.g. 0.5 mm) into one question with the union box. Keep the method label ("separate bodies" when merged). The user can still edit the numbers. Tests: three touching cylinders on the back give one question with the union box; two far-apart plugs on the back stay two questions.
2. **Say how much band is left.** A keep-clear opening in the rear bracket can merge into a style window. With the SG108 set back 70 mm on a Reinforced bracket, the cable's opening left only **2.1 mm** between the lower-left and upper windows (the style normally keeps 5 mm). Today the warning only says "check remaining bands and joints". Compute the smallest remaining band/strip around each keep-clear opening (to style windows, vent holes, rack slots, the plate edge and the joint bosses/pilots) in `equipment.py` (beside `keep_clear_openings`) and mirror it in `tray-placement.js`. Show it in the warning, e.g. "…leaves a 2.1 mm band (the Reinforced style normally keeps 5 mm)". If the opening cuts a joint pilot or boss, say so plainly. Warning only; never block, never move the opening.
3. **No duplicate message.** Flush with a flat mount shows "Flat corner stops need a front gap of at least 6.2 mm" twice (the new `positionProblems` text and the old check). Show only the newer, more helpful one when Front position is not As today.

## May change

`equipment-wizard.js`, `equipment.py`, `tray-placement.js`, `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Specs without `protrusions` and with default Front position/Bezel must still give byte-identical SCAD source. Write `work/codex-tasks/34-protrusion-polish-REPORT.md` with files + SHA-256, the merge tolerance, the band rule, check results and open questions. Claude reviews it with the SG108 STEP in the browser on disposable data.

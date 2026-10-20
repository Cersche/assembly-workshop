# Cable planner: final check in Chrome (2026-10-19)

One end-to-end check of the items that the Step 3, 4 and 5 reports listed as "Not verified". It ran in Brian's real Chrome (Claude in Chrome, with Brian's OK). The data was a disposable scratchpad copy of `data/normal-use`, served by the new `.claude/launch.json` entry `disposable-finalcheck-8781`. `data/normal-use` was not touched: `rack-workspace.json` was last changed 2026-10-18 19:09. Nothing was printed, committed or pushed, and no file was downloaded.

Cabling is planning data only. Lengths are estimates. Guide capacity, cable fit, bend tolerance and strength stay **UNKNOWN**.

## Setup on the scratch copy

- **Test Switch:** a wizard-made item in U03 with a front RJ45 port "LAN1" and Keystone 1, which gives a front and rear port pair.
- **Rack setup:** three Rear left guides (U01 to U03), a bottom-rear exit and an "Office wall jack" endpoint. "Warn above" was set to 1 so that crowding would show up.
- **C1:** a keystone rear run from Keystone 1 rear, through RL U03 and the exit, to the Office wall jack.
- **C2:** a front patch cord from Keystone 1 front to Test Switch LAN1.
- **C3:** an unrelated cable from Pi 4 (U01) USB-C power to the Office wall jack. It gives a contrast for the lighting check and a second cable for the crowding check.

**Setup workaround.** The wizard would not save the item with a keystone (see Problems found, item 2). It was saved without one. Then `"keystones": [-75]` was written into that item's spec, in the scratch copy only. Cable ports come from the saved spec, so the cable checks are unaffected. The faceplate mesh of this test item has no keystone hole.

## Verified in Chrome

| Item | Result |
| --- | --- |
| Port-to-port Connect by clicking (Step 3) | **Pass, after a fix.** The first real click in the centre of the LAN1 marker did nothing. See the fix below. After the fix, the same real click made C2. |
| Keystone link (Step 3) | **Pass.** With C2 selected, the panel shows "Linked keystone cable: C1", and C1 and C2 are both lit while C3 is dimmed (Rear view). With C3 selected, C1 and C2 go dark. |
| Crowding warnings (Step 3) | **Pass.** C1 and C3 share RL U03, which is over the setting of 1. Both get "⚠ Guide over the crowding setting; capacity UNKNOWN." in the cable list and the Cable panel. Review also shows "Crowding at RL U03: 2 cables exceeds your setting of 1". |
| Show me highlight and dimming in 3D (Step 4) | **Pass.** A real click on Show me (crowding) turned Cables mode on and showed the "Showing in the rack view: … Done (Esc)" bar. The frame and other parts were dimmed and the crowded cables and guide stayed bright. Esc restored the colours and turned Cables mode off again. |
| Open printable sheet (Step 5) | **Pass.** A real click opened a real new tab, "My Lab Rax · wiring sheet". It shows the Front elevation with C2 as a blue front patch cord, the Rear elevation (mirrored, so the keystone is on the right) with C1 and C3, the exit, "Office wall jack · C1, C3", the legend and both crowding notes. |
| Labels (Step 5) | **Pass.** A real new tab, "My Lab Rax · cable labels", showed 6 labels, one per end. Keystone ends read "K1", for example "C1 · K1 → Office wall jack" and "C2 · K1 → Test Switch". |
| CSV "Linked to" and front patch cord (Step 5) | **Pass.** The real Schedule (CSV) button was clicked. Its file was captured in the page instead of being downloaded. Results: C1 is linked to "C2 via K1", C2 to "C1 via K1", and C2 is listed as "Test Switch · Keystone 1 · front → Test Switch · LAN1 (U03 front)". |

## Fix made (small)

**Port markers were hard to click.** Each connector marker has a real socket hole (`cable-ports.js`, `markerMeshes`). A click in the middle of a marker went through the hole to the faceplate, so Connect said "Click a port marker". Only the thin rim worked.

`outputs/Mechanical_Design_App/workspace.js` now has `portNear()`. When the exact point misses, it tries a small ring of nearby points (6 and 12 px) and uses the first port it finds. It is used for:

- the Connect click;
- the right-click "select and Connect".

A normal click that selects a port still uses the exact point, so a click in a marker's centre selects the slot instead. That was left alone, to keep slot clicks fast.

`run_checks.ps1`: **all checks passed**. That is 73 Python tests, plus the Node groups 24 + 27 + 16 + 9 + 18 + 20 + 10 + 7, with no failures.

## Problems found, not fixed (outside this check)

1. **A rear keystone run is typed "Keystone (pass-through)".** When one end is a keystone and the other is an endpoint, Connect has no real connector type to use, so it falls back to "keystone". C1 then reads as a keystone cable in the panel, the CSV and its labels. The type can be changed in the Cable panel. Whether it should default to RJ45 is Brian's call, because keystones can also be HDMI or USB.
2. **The wizard rejects a 1U item with a keystone:** "Rendered mesh has open or non-manifold edges: faceplate". This happened at X = −75 and X = −100 mm (screw joint, heat-set inserts, one hole). The same item saved fine without the keystone. At X = −50 mm the wizard correctly said to keep keystones at least 60.9 mm from centre. This needs its own look at the golden keystone geometry in `equipment_tray.scad`, which was not changed here.
3. **"View rack" does not return to the rack panel** while a slot is selected (the known backlog item). The rack dropdown still works for that.
4. **After Connect, the rack-level panel opens with the new cable selected**, so you leave the slot you were working on. This is expected from `selectCable`, but noted.

## Not verified

- **Printing or Save as PDF**, at Brian's direction. Brian prints himself.
- **Opening the CSV from disk.** The CSV was captured in the page and never downloaded. Whether the BOM survives was not re-checked, because the browser strips it when text is read.
- **The 3D views page and the PNG snapshots** were not re-tried in Chrome.
- **The Pi 4 front ports.** They have face UNKNOWN and show no markers in the Front or Rear view, so a Pi-to-port click was not tried.
- **The Step 3 label clamp and drawing order for endpoint-first cables** were not on this list and were not looked at.
- **The normal 8765 server** still runs the older code until Brian restarts it with start.bat.

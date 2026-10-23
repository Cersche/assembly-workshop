# Session prompt: U numbering fix + rack-plan loose ends (2026-10-22)

Paste the block below into a fresh session.

```
Assembly Workshop. git pull, then read AGENTS.md, HANDOFF.md, ROADMAP.md and work/rack-plan/Rack_Plan_9U.html (the 9U rack plan I made with Claude on 2026-10-22). Offload big/mechanical work to Codex per my usual workflow (specs in work/codex-tasks/, give me the ready-to-paste Codex prompt). Ask before anything outward-facing; no printing.

1. U NUMBERING (main job). Standard racks count U1 at the BOTTOM. Our app counts slot 1 at the TOP (see workspace.js slotLabel / guide "Move up" = slot-1, cable-sheet-view.js yTop=(slots-slot+1)). Fix it so labels shown to me read U1 = bottom everywhere (rack view, slot list, guides, cable sheet, BOM/exports, any text). Prefer a display-only relabel (label = slots - slot + 1) over changing stored slot numbers; if stored data must change, migrate on load, keep the old document in rack-history/, never move equipment physically. Saved placements must land in the same physical spot before and after. Test on disposable data, never data/normal-use. Run the existing checks (PROJECT.md/HANDOFF.md); note the pre-existing js-tests/rack-bom.js:92 failure separately.

2. SAVE THE 9U PLAN INTO THE APP (after #1, ask me first, back up the current rack to rack-history/). Bottom-up: U1 OptiPlex 7010 Micro (settled sleeve, don't change orientation/mounting), U2 drive tray (HDD only; SSD dead, pad stays empty), U3-U5 7" touch dashboard (3U screen plate), U6 Pi 4 + Hue tray, U7 10-keystone panel (3 USB, 4 Ethernet, 3 blank), U8 TP-Link TL-SG108E switch, U9 modem; router sits on the roof. 9U includes the support extension. All cables enter bottom-rear-left in one sleeve; internet coupler on the rear-left post at U9.

3. DESIGN LOOSE ENDS (spec / Codex tasks, no prints):
   a. U8 switch faceplate + U7 keystone faceplate lined up (option 2: keystones evenly spaced, switch offset ~15 mm right so ports 2-5 sit under the 4 Ethernet keystones). Get TL-SG108E port pitch/dimensions from TP-Link's drawing or ask me to measure.
   b. U6 Pi + Hue tray: Pi USB/Ethernet face front; slot below the Pi USB for a down-angled USB to the screen; micro-HDMI exits the side, hidden.
   c. U3-U5 3U screen plate for Hosyond 7" 1024x600 HDMI touch (ears with holes). Needs my measurements when it arrives; leave the back open for airflow.
   d. Cooling: OptiPlex rear pocket (~34 mm behind the PC, solid rear bracket) traps exhaust. Plan: open the right side of the tray behind the PC (Y ~195-228) + right side panel with 80 mm 5V PWM exhaust fan at U1-U2 rear; optional second exhaust at U8-U9; optional filtered bottom intake at the FRONT (not under the rear floor opening). Rear bracket stays settled except a possible vent/cable window. Fan speed via Pi GPIO + DS18B20 sensors in Home Assistant. Wall-mounted rack with small rear clearance; vented side panels wanted. Needs a photo of the 7010's back/right vents from me.
   e. Open questions to ask me: HDD connection (USB-SATA assumed vs internal SATA); fan count (1 or 2).

4. HOUSEKEEPING. git status shows untracked data/normal-use/equipment-library.json, a new data/normal-use/equipment-revisions/9289a62a.../ and work/gui-refinement/checks-t9iv5v35/. Check what they are and ask me before committing or deleting. Commit work/rack-plan/ and this prompt file.

End: update HANDOFF.md (and ROADMAP.md Now/Next if needed), commit and push to main.
```

# Cable management Step 4: decisions (routing suggestions)

2026-10-19. Brian answered every question below in this session and picked the recommended option each time. Nothing is built yet. Context: [Proposal.html](Proposal.html) ("Routing suggestions"), [Step3_Decisions.md](Step3_Decisions.md), [Step3_Report.md](Step3_Report.md).

These rules carry over unchanged: cabling is planning data only (no geometry, STLs or hardware pins). It saves only through the explicit atomic Save and lands in rack history. The guide mesh is a local preview and never goes into rack STLs. The Pi 4 is only sample equipment, so every rule works for any equipment. Guide and cable fit, capacity, bend tolerance and strength stay UNKNOWN, and lengths are planning estimates. **Suggestions are advice, never checks: none of them blocks Save, and none says a real cable or guide is fine or not fine.**

## Decisions (Brian, 2026-10-19)

1. **Power or data.** Each cable gets a "Carries: power / data" choice in the Cable panel. If the user hasn't set it, it comes from the type: IEC and DC barrel are power; USB-C is power when either connected port's label or id contains "power", otherwise data; everything else is data.
2. **Power post.** A per-rack setting chooses the power post: right rear (RR) by default, left rear (RL) as the alternative. The data post is the other rear post.
3. **Power/data split is a suggestion only.** Automatic routing stays as Step 3 built it (nearest post). A cable whose guides sit on the wrong rear post, or that uses guides on both rear posts, gets a suggestion. Apply moves that one cable onto the right post in the draft (its route becomes manual).
4. **Missing guide.** Where a cable's vertical run goes more than 2U between supports (its ends and guides), suggest a guide on that post at the middle U of the gap. Apply adds the guide to the draft; automatic routes pick it up and manual routes are left alone.
5. **Exits.** If cables to outside endpoints use more than one exit, suggest moving them all to the most-used exit that isn't top-rear. A top-rear exit in use gets its own note: keep the top fan panel clear. Apply sets those cables' exit in the draft (their routes become manual).
6. **Unplugged often.** A new "Unplugged often" tick box in the Cable panel. A ticked cable with no keystone at either end gets a suggestion to use a keystone pass-through. No Apply: splitting a cable is the user's call.
7. **Service loops and short runs.** Flag a cable whose service loop is 0 m (no Apply). Flag a cable whose two port ends are less than 1U apart in height but whose route still passes through a guide; Apply drops the guides from that cable's route in the draft (route becomes manual, exit kept).
8. **Tight bends.** Guidance only, from nominal display diameters: Ethernet (RJ45) uses the commonly published 4 × cable diameter; every other type uses 10 ×, labelled as a generic rule of thumb, not a published figure for that cable. Flags sharp corners in the planned route. Never a check of real cables. No Apply.
9. **Show me.** Switches the rack view to Cables mode if needed, lights the cables, guides, ports and exits involved and dims the rest. The inspector selection is left alone. A "Done" button or Esc clears it.
10. **Apply.** Changes only the unsaved draft and never saves. The message after an Apply offers one Undo for the last Apply. Discard and History work as today.
11. **Other rules.** Each guide above the crowding setting is its own suggestion (capacity UNKNOWN; no Apply). Each cable with a missing end is its own suggestion (no Apply). Unused ports are one line per piece of equipment, such as "Pi 4: 7 of 9 ports unused", so the list isn't flooded.
12. **Ignore.** Each suggestion has Ignore. Ignored suggestions are saved with the rack through the normal Save, can be brought back from a "Show ignored" list, and come back by themselves when the cables, guides or exits involved change.

## Where it shows

A "Cable suggestions" card in the Review tab (rack level), below the existing review. Each item: a short title, one plain sentence of detail, Show me, Apply (only where decided above) and Ignore. A count shows in the card heading. Nothing appears in the normal views unless Show me is active.

## Data shape additions (frozen for the build)

All optional; racks saved without them load unchanged.

```
cabling.cables[i].carries        'power' | 'data'      # absent = default from type (decision 1)
cabling.cables[i].unplug_often   true | false          # absent = false (decision 6)
cabling.settings.power_post      'RR' | 'RL'           # absent = 'RR' (decision 2)
cabling.settings.ignored_suggestions  [{id, sig}]       # at most 500; id ≤ 120 chars, sig ≤ 32 chars (decision 12)
```

## Build plan for Step 4

1. **Codex task 11, schema:** `cable_plan.py` accepts and validates the four new fields; Python round-trip and rejection tests.
2. **Codex task 12, pure logic:** new `cable-suggest.js` (`LabRaxCableSuggest`): `carries`, `suggestions`, `applySuggestion`, `ignore`, `unignore`, `pruneIgnored`, plus Node tests. The exact API is frozen in the task file so the UI can be built in parallel.
3. **Claude, viewport and UI:** Review-tab suggestions card; Show me highlight state in `workspace.js` and `rack-studio.js` (lit/dim for cables, guides, ports and exits); Apply with one Undo (snapshot of `rack.cabling` before Apply); Ignore and Show ignored; Cable panel "Carries" and "Unplugged often"; power post setting next to the crowding setting; `index.html` and `app.py` load and serve `cable-suggest.js`; refresh the asset manifest hash if `rack-studio.js` changes.
4. **Checks:** `run_checks.ps1`, then a browser check on a disposable copy of the data in Claude's scratchpad, never `data/normal-use`. Write `Step4_Report.md` saying what was verified and what was not, and add one HANDOFF.md line.

Claude and Codex never edit the same file. Re-check file times before editing shared files.

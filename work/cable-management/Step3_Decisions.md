# Cable management Step 3: decisions (cables, exits, outside endpoints)

2026-10-19. Brian answered every question below in this session and picked the recommended option each time. Nothing is built yet. Context: [Proposal.html](Proposal.html), [Report.md](Report.md) (Step 1), [Step2_Report.md](Step2_Report.md) (Step 2).

These rules carry over unchanged: cabling is planning data only (no geometry, STLs or hardware pins). It saves only through the explicit atomic Save and lands in rack history. The guide mesh is a local preview and never goes into rack STLs. The Pi 4 is only sample equipment, so everything here works for any equipment. Guide and cable fit, capacity and strength stay UNKNOWN, and lengths are planning estimates.

## Decisions (Brian, 2026-10-19)

1. **Connecting.** Choose Connect on a port (button, right-click or ellipsis), then click the other end: another port, or an outside endpoint picked from a list. Esc cancels. It works the same from the front and the rear.
2. **Keystones.** The rear run and the front patch cord are **two separate cables**, each with its own number, type and length. The app links them at the keystone (`ks-N-rear` ↔ `ks-N-front`). Selecting one lights both, and the schedule lists them together.
3. **Routing.** The app picks a route automatically through the nearest guides on one post. You can then add, remove or reorder guides in the Cable panel. Once you edit a route it is kept as you set it and marked "manual".
4. **Moved or removed guides.** Automatic routes recalculate. A manual route keeps a guide that moved and drops one that was removed, and the cable shows a "route changed" note until you look at it. All of this happens in the unsaved draft.
5. **Exit points.** Allowed at bottom-rear, top-rear, left side and right side, at a U you choose. Each one is drawn as a grommet marker only, and no hole or geometry is added to any STL.
6. **Exit rule.** A cable to an outside endpoint uses the nearest exit automatically, and you can change it. If the rack has no exit yet, the cable still saves but shows a warning.
7. **Outside endpoints.** Each has a kind (wall outlet, UPS, modem/ONT, wall jack, desk, another rack, other) and a name you give it, such as "Office wall outlet". Endpoints are saved once per rack and many cables can use the same one. They have no 3D position: each is drawn as a labelled arrow past its exit.
8. **"Another rack"** is only a named endpoint for now. Linking cables between racks is parked.
9. **Cable fields.**
   - Number: automatic (C1, C2…) and editable.
   - Type: taken from the ports, editable.
   - Colour: the type's colour, which you can override.
   - Service loop: 0.15 m per end by default.
   - Note.

   **Length** is the route length plus the service loops, rounded up to the next 0.1 m and always labelled "planning estimate". For a cable going outside, the app shows only the length to the exit.
10. **Rendering.** Cables are smooth coloured tubes with a slight sag between guides, laid side by side where they pass through a guide. Selecting a cable lights its whole run, both ends and any linked keystone patch, and dims the others. Cables show in Cables mode and the Rear view. In the normal views they stay hidden unless you turn them on.
11. **Ports with face UNKNOWN** (for example the Pi 4 sample preset). When you connect one, the app asks once which side the cable reaches it from: front, rear, or leave it UNKNOWN. Your answer is saved as that port's face (a `rack.cabling.ports` face override). If you leave it UNKNOWN, the cable still saves, routes from the rear by default and shows a "face UNKNOWN" warning.
12. **Guide crowding.** A per-rack setting, "warn above N cables per guide", with a default of 6. It is marked as your own choice, not a measured capacity. Going over it shows a warning and blocks nothing. The full suggestion rule comes in Step 4.
13. **One cable per port.** A port that already has a cable can't take a second one. An outside endpoint can take many.
14. **Moved or removed equipment.** If equipment moves, its cables re-route. If equipment or a port is removed, the cable stays, with that end shown as "unconnected" so you can reattach or delete it. This happens in the draft.

## Open or parked

- **Parked:** linking cables between racks (decision 8).
- **Step 4:** suggestions (power on one post and data on the other, missing guides, bend radius, crowding as a suggestion, one-ended cables).
- **Step 5:** wiring sheet, CSV schedule and labels.
- **Still UNKNOWN:** guide fit and capacity, cable outer diameter and stiffness, connector depth, rear clearance behind equipment, and which face each Pi 4 port is reached from until the user sets it.
- **Not decided, defaults proposed for the build:**
  - Exit markers get their own Setup list next to Cable guides.
  - The service loop default (0.15 m) and the crowding default (6) are editable per rack.
  - Tube diameters are nominal per type and for display only.

## Data shape (proposal for the build, not final code)

This extends `rack.cabling` (today `guides` and `ports`), which `rack_workspace._cabling` validates. `_cabling` currently rejects unknown keys, so it must accept the new ones or Save will fail.

```
cabling: {
  guides: [...], ports: [...],                       # unchanged
  exits:     [{id, position: 'bottom-rear'|'top-rear'|'left'|'right', slot}],
  endpoints: [{id, kind: 'wall-outlet'|'ups'|'modem'|'wall-jack'|'desk'|'other-rack'|'other', name}],
  cables:    [{id, number, type, color?, service_loop_m,
               from: {allocation, port} | {endpoint},  to: same,   # null = unconnected end (decision 14)
               face_assumed?: 'rear',                  # decision 11 when the port face is UNKNOWN
               route: {mode: 'auto'|'manual', guides: [guide ids], exit: exit id|null},
               route_changed?: true, note}],
  settings:  {guide_warn_above: 6, service_loop_m: 0.15}
}
```

The keystone link (decision 2) comes from the existing `passThrough` pairing in `cable-ports.js`, so no extra stored field is needed. Port references use the stable `allocation/port` key from Step 2.

## Build plan for Step 3

1. **Schema:** add `exits`, `endpoints`, `cables` and `settings` to `rack_workspace._cabling`. Check the limits: one cable per port (decision 13), references to guides, exits, endpoints and placements must exist, and unconnected ends are allowed. Add Python round-trip and rejection tests.
2. **Pure logic module** (for example `cable-routes.js`, testable in Node): auto route through the nearest guides on one post; route, exit and length estimate; re-route on guide or equipment changes with the `route_changed` flag; the keystone-pair lookup; the crowding count. Add Node tests.
3. **Draft upkeep:** when guides, equipment or ports change, update cables as decisions 4 and 14 say. When the slot count shrinks, prune exits the same way guides are pruned.
4. **Viewport:** exit grommet markers; tube meshes with sag and bundling; picking for cables and exits; selection highlight and dimming; a cable visibility toggle for the normal views.
5. **UI:** Connect mode (port Connect, click the target, Esc cancels, endpoint picker, face prompt); a Cable panel (fields, route editing, warnings); Setup lists for Exits and Outside endpoints; the crowding setting.
6. **Checks:** run `run_checks.ps1`, then a browser check on a disposable copy of the data, never `data/normal-use`. Write a Step 3 report saying what was verified and what was not.

Coordinate with Codex (`work/codex-tasks/`) before editing `rack-studio.js`, `workspace.js` or the asset manifest. Re-check file times first.

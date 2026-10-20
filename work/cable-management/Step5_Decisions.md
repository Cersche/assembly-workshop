# Cable management Step 5: decisions (wiring sheet, schedule, labels)

2026-10-19. Brian answered every question below in this session. He picked the recommended option each time, except paper size (a choice in the card) and the 3D views, which he added himself. He reviewed a mockup before saying "all recommended". Nothing is built yet. Context: [Proposal.html](Proposal.html) ("The wiring diagram output"), [Step3_Decisions.md](Step3_Decisions.md), [Step4_Decisions.md](Step4_Decisions.md).

These rules carry over unchanged:

- The documents are made from **saved data only**. They never save the draft and never touch any STL, rack STL or hardware pin.
- The guide mesh is a local preview. It is never redistributed, and the schematic draws guides as plain marks.
- The Pi 4 is only sample equipment, so nothing is Pi-specific.
- Lengths are planning estimates. Guide and cable fit, capacity, bend tolerance and strength stay UNKNOWN.
- These are planning documents. The app never prints. Brian prints or uses "Save as PDF" from the browser himself.

## Decisions (Brian, 2026-10-19)

1. **Where.** A "Wiring sheet" card in the rack-level Review tab, below Cable suggestions.
2. **Unsaved changes.** Same rule as the other exports: while the draft has unsaved changes, the buttons say "Save first" and nothing is generated. The documents are built from the saved rack fetched from the server.
3. **Delivery.** Separate buttons: **Open printable sheet** (a print-ready page in a new tab), **Sheet (SVG)** download, **Schedule (CSV)** download, and **Labels** (a print-ready labels page in a new tab).
4. **Drawing.** A clean schematic: front and rear elevations side by side. It shows the rack outline, numbered U's, equipment boxes, posts, guides, exits, cable lines with number tags, and outside endpoints as labelled arrows. Power, data and patch cables are colour-coded, with a legend.
5. **3D views (Brian's addition).** An "Include 3D views" tick box. When it is ticked, the printable sheet gets a second page with front and rear 3D snapshots in Cables mode, tagged with the cable numbers. The same two views also download as PNGs. The SVG stays a pure line drawing.
6. **Paper.** A Letter / A4 choice in the card, Letter by default. The sheet is landscape and the labels are portrait.
7. **Labels.** One per cable end, reading "this end → other end". The keystone end of C7 reads "C7 · K1 → Modem" and the modem end reads "C7 · Modem → K1". A small second line gives the type and the end ("RJ45 (Ethernet) · this end: K1 rear"). They are laid out in a grid with dashed cut lines. An unconnected end gets no label, and the other end's label says "→ unconnected".
8. **Keystone patches in the CSV.** Strictly sorted by cable number (C2 before C10), with a "Linked to" column (C7 shows "C9 via K1").
9. **CSV columns (full set).** Number, From, To, Type, Carries, Colour, Route, Exit, Length estimate (m), Service loop (m), Linked to, Warnings, Note. A first line names the rack and the save time and says that lengths are planning estimates. A cable going outside shows its length as "0.6 to exit".
10. **Warnings on the sheet.** A Notes box lists each cable's open warnings (unconnected end, no exit, face UNKNOWN, route changed, guide over the crowding setting). It always ends with the standing line: lengths are planning estimates, and guide capacity, cable fit, bend tolerance and strength are UNKNOWN. Review suggestions are not copied onto the sheet.
11. **Browser check.** Claude may generate each document once from a throwaway scratchpad copy of the data (never `data/normal-use`) to check it. Nothing is printed.

## Defaults for the build (not asked; obvious from the decisions)

- File names: `<rack name>-wiring-sheet.svg`, `-cable-schedule.csv`, `-front-3d.png`, `-rear-3d.png`, with unsafe characters replaced by `_`.
- The CSV is UTF-8 with a BOM, so Excel shows "·" and "→", and uses CRLF line endings. Fields are quoted when needed, and a cell starting with `= + - @` gets a leading `'` so a spreadsheet won't treat it as a formula.
- Which elevation a cable is drawn in: the front if both ends are front-face ports, otherwise the rear.
- The rear elevation is drawn as seen from behind, so left and right are mirrored compared with the front.

## Build plan

1. **Codex [task 13](../codex-tasks/13-cable-sheet-logic.md), pure logic:** a new `cable-sheet.js` (`LabRaxCableSheet`) with `endName`, `shortName`, `faceOf`, `schedule`, `csv`, `labels` and `notes`, plus Node tests. The exact API is frozen in the task file so the UI can be built in parallel.
2. **Claude, drawing and UI** (files Codex does not touch):
   - a new `cable-sheet-view.js`: the SVG schematic from saved data, the printable sheet and labels pages, and the paper sizes, with its own Node tests;
   - in `workspace.js`, the Review card: the Save-first rule, a fetch of the saved rack, downloads, new tabs, and the 3D snapshots from the rack viewer;
   - `index.html` and `app.py` load and serve the two new scripts;
   - the asset manifest is refreshed only if `rack-studio.js` changes.
3. **Checks:** run `run_checks.ps1`, then a browser check on a disposable scratchpad copy of the data. Write `Step5_Report.md` saying what was verified and what was not, and add one HANDOFF.md line.

Claude and Codex never edit the same file. Re-check file times before editing shared files.

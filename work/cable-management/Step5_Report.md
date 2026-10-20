# Cable management Step 5: wiring sheet, schedule and labels (2026-10-19)

Built from Brian's 11 decisions in [Step5_Decisions.md](Step5_Decisions.md). Claude and Codex split the work and never edited the same file at the same time.

These are **planning documents made from the saved rack only**:

- The app fetches the saved rack from the server. While the draft has unsaved changes, the buttons say "Save first" and generate nothing.
- Nothing here saves, prints or touches any STL, rack STL or hardware pin.
- Lengths are planning estimates. Guide capacity, cable fit, bend tolerance and strength stay **UNKNOWN**.
- The Pi 4 is only sample equipment: nothing is Pi-specific.

## What was built

**Codex, [task 13](../codex-tasks/13-cable-sheet-logic-REPORT.md).** `cable-sheet.js` (`LabRaxCableSheet`) provides the schedule rows, the CSV and the label and note texts:

- The CSV is UTF-8 with a BOM and CRLF line endings, has a formula guard, and is sorted by cable number. It has a "Linked to" column for keystone pairs.
- 10 Node tests. The API matches the frozen contract exactly. I reviewed the code and changed nothing.

**Claude.**

- `cable-sheet-view.js` (`LabRaxCableSheetView`) draws the SVG schematic:
  - front and rear elevations side by side, with the rear seen from behind and mirrored;
  - U numbers, equipment boxes, posts, guides, exits and cable lines, coloured power, data or front patch, with number tags;
  - outside endpoint boxes with arrows from their exits (top and side exits go round the outside of the rack);
  - a legend, a Notes box (overflow points to the CSV) and the standing UNKNOWN line.

  It also builds the print-ready sheet page (with an optional 3D page) and the labels page (Letter or A4, dashed cut grid). 7 Node tests in `js-tests/cable-sheet-view.js`, registered in `run_checks.ps1` after Codex finished.
- `workspace.js`: a "Wiring sheet" card in the rack Review tab with:
  - a Paper choice (remembered per browser) and an "Include 3D views" tick box;
  - buttons: Open printable sheet, Sheet (SVG), Schedule (CSV), Labels, and 3D views (PNG) when ticked;
  - the "Save first" state, kept current from `updateSaveStatus`.

  The 3D views are front and rear snapshots in Cables mode. They are drawn into the rack canvas and the view is restored afterwards.
- If the browser blocks the new tab, the printable sheet or labels page downloads as an `.html` file instead. This was found during the check: the Browser pane blocks all pop-ups.
- `index.html` and `app.py` load and serve the two new scripts. CSS was added to `workspace.css`. Original line endings were kept.

## Verified

- `run_checks.ps1`: **all checks passed**, 73 Python and 137 JavaScript tests:

  | Group | Tests |
  | --- | --- |
  | Module | 24 |
  | Page logic | 27 |
  | BOM | 16 |
  | Rebuild | 9 |
  | Cable routes | 18 |
  | Suggestions | 20 |
  | Cable sheet | 10 |
  | Sheet drawing | 7 |

- Browser check on a disposable scratchpad copy of the Step 4 seeded data (server `disposable-cables5-8779`; 5U, 2 Pi 4s, 4 cables, 2 exits, 2 endpoints). No console errors from the new code. With Brian's OK, each document was generated once in the browser pane and its content was inspected; nothing was printed.
  - **CSV:** 4 rows in number order, with face-UNKNOWN and unconnected warnings, `0.7 to exit`, and the saved version in the first line.
  - **SVG and printable sheet:** both elevations, the top-rear and bottom-rear exits, endpoint boxes "Office wall outlet · C1" and "Modem · C2", and the Notes box. With 3D ticked there is a second page with front and rear snapshots in Cables mode. The app view went back to the 3D view with Cables mode off.
  - **Labels:** 7 labels (one per connected end, C4 "→ unconnected"), wrapping in the A4 grid.
  - **Save first:** after an Ignore in the draft, all buttons read "Save first", clicking generated nothing, and the draft stayed unsaved.
  - **Pop-up blocked:** the fallback downloaded the `.html` file and said so.
- `data/normal-use/rack-workspace.json` was not touched (last changed 2026-10-18 19:09). The scratch copy was never saved during the check.

## Not verified

- **A real new tab was never opened**, because the Browser pane blocks pop-ups. Only the download fallback ran. In Chrome, a click normally allows the tab.
- **Printing or Save as PDF was never tried.** The `@page` Letter/A4 sizes and page breaks are untested on paper. This is Brian's step whenever he wants it.
- The downloaded files' contents were inspected through a debug hook. Opening the downloaded files from disk was not tried.
- **Not tried in the browser:** wizard equipment, keystone pairs (the "Linked to" column) and front patch cords. The scratch data has only two Pi 4s; these are covered by Node tests.
- The 3D snapshots use the current canvas size, so on a narrow window the rack is small on the page. They show the open draft, which equals the saved rack because Save first is enforced. If another tab saved a newer version in between, the schematic and the 3D page could differ.
- Label text wraps to two lines and anything longer is cut. Very long equipment or endpoint names can still be clipped on a label (the schedule has the full names).
- No printing, commits or pushes. The normal 8765 server still runs the old code until Brian restarts it with start.bat.

## Next

The planner's five steps are now built. Backlog ideas (not commitments): a real tab check in Chrome, a quicker way back to the rack panel from a slot, and linking cables between racks (parked).

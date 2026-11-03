# Pi / Hue swap exploration around SCR5-H11 (2026-11-03)

Concept models only, not a revision, nothing to print. Numbers come from the meshes; sag, fit and strength stay UNKNOWN. Hue weight is an assumed 150 g, printed parts are counted solid at 1.24 g/cm3, Pi connector positions are from the published layout.

| | H11 | Swap A (ports front, keystone low) | Swap B (keystone stays, Pi turned, ports rear) | No swap (Hue forward + right) |
|---|---|---|---|---|
| Hue lever behind plate rear | 93 | 64.5 | 64.5 | 77.5 |
| Tray rear Y | 142 | 113.5 | 113.5 | 126.5 |
| Gravity moment at the plate | 100% | 76% | 78% | 85% |
| Twist about the joints (g.mm) | ~0 | 3300 | 3300 | 3800 |
| M6 row to ledge | 58 | 73 | 60 | 58 |
| Ribbon length, modelled | 97 | 87 | 55 | 97 |

Findings: Hue height alone changes nothing for sag (bending at the plate depends on weight x distance back); the gain is the forward move. Lifted straight up, all three Pi openings hit the keystone or an M6 boss. With the Hue under the deck its button is buried, so it shifts to X -34 (finger hole beside the Pi), which also clears the keystone lane and leaves room for a wall at X -83 to replace the H11 inner wall. That shift adds twist.

Clashes (`checks.json`): all 0 except concept leftovers: ribbon vs inner wall where no slot is modelled (A), and the Pi HDMI shells vs a wall flush with the board edge. **H11 itself has that:** floor vs Pi with connectors 22.5 mm3 at the outer wall/grille (shells modelled 1.5 past the board, published layout, not measured).

`python work/scr5-swap/build.py`, `checks.py`, `figures.py`. STLs under `stl/` are not committed (cradle is third-party).

# Beta Hardening Sigma — Workspaces and Inspector

Implemented Design / Assemble / Prepare navigation in the isolated development workbench. Existing functional controls and their DOM identifiers are retained and grouped under workspaces. A contextual selection inspector displays the selected record's label and explicitly states that validation is unknown until checked. Responsive workspace styling is provided. This is not yet the final three-panel CAD UI, nor does it change underlying CAD geometry.

## Verification

- `node --test rev1_shell.test.js rev1_workspaces.test.js`: 10/10 passed.
- `python beta_regression.py --render`: 6/6 gates passed, including OpenSCAD render.
- Original `/mnt/data/files/index.html`: unchanged SHA-256 `0400d9d26ef322fb193d73cc805e731f23231fb03b175171af88c5109cc1533b`.
- Browser navigation, IndexedDB acceptance, and end-to-end human usability remain unverified in a real browser.

## Usage

Run `python start_server.py` and open `http://localhost:8765` in a desktop browser. Use the Design / Assemble / Prepare buttons to navigate. Do not manufacture parts without physical and mechanical verification.

# Workbench workflow log

Real part work, recorded so the Workshop Bench app gets built around what actually happens.
Mockup (private, nothing connected): https://claude.ai/artifact/T1cst7qAqkqus6LSnB8ACC

Add one short row whenever a step starts or ends, or something gets in the way. Record what happened, not what should have.
Steps: Measure, Draft, Print, Report.
"App idea" is optional: what a screen or button could have done here, including something on the mockup that wasn't needed.

## Cable management bracket (front to rear posts)

| Date | Step | What happened | Friction | App idea |
| --- | --- | --- | --- | --- |
| 2026-11-05 | Measure | Started. Read handoff, fit log, cable report; sliced the 4U post mesh; found CBL-A..E source files | Post mesh is inside a nested 3MF, needed a throwaway script to slice it | Post section and hole list one click away |
| 2026-11-05 | Measure | Reading ended; concept SCAD and viewer sent, questions asked. Waiting on Brian's answers before the measuring diagram | Saved layout stores slots from the top, had to convert to U numbers | Show free U's next to the part |
| 2026-11-05 | Draft | Concept: posts clear in the mesh check. Head recess almost broke through the inner edge, moved it 2 mm | My first post placement was one half U off; caught before sending | Place real posts by U automatically |
| 2026-11-05 | Measure | Brian approved the concept as is. Measuring diagram (A-H) sent, device card started with expected values | Shared U with equipment: post-rail brackets use the same front middle hole | Warn when two parts claim the same post hole |
| 2026-11-05 | Draft | C measured 16 (Brian); others kept from the source model. Four style options A-D sent in one viewer, all clear the posts | | Side-by-side style variants from one switch |
| 2026-11-05 | Draft | Brian picked soft + vented; combined into the one draft and the concept viewer updated | Styles were one-of-four, had to turn them into on/off switches to combine | Style options as checkboxes, not a single choice |
| 2026-11-05 | Draft | Drop-outs added near each end (18 x 13.5, outer lane). A fully open cut was very weak sideways (0.7k against 16k+); kept an 8 mm bridge on top, now 8.1k. Lost the two end fingers | Had to compute section stiffness with a throwaway script | Section stiffness readout at any point along a part |
| 2026-11-05 | Draft | Brian circled the drop-outs in the viewer: added a finger over each (now 7 fingers) | Marked picture, no coordinates; read the spot from the image | Pin notes with mm coordinates came back as a picture this time |
| 2026-11-05 | Draft | Brian circled the outer wall vents: they had merged into one long slot (my spacing error). Closed; floor slots stay | My windows overlapped and I didn't catch it | Flag cuts that merge into one opening |
| 2026-11-05 | Print | Brian: "let's print this sucker". Released as CSB-A: ID engraved, release_part.py 0 FAIL / 0 WARN, README and fit report sent. Waiting on his print | The release script can't confirm the ID on the mesh; checked it by hand, and my first check picture missed the text | ID check on the mesh itself |

Totals when the part is done: drafts sent ___, revisions released ___, prints ___, prints that failed ___, measurement requests ___.

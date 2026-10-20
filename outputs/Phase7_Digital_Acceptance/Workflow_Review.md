# Phase 7 — workflow review scope

Reviewed the actual index.html/catalog.js/viewer.js handlers and exercised them through the existing catalog/viewer mocks plus test_phase7_workflow.cjs. No desktop-control or fresh visual browser session occurred.

| User behavior | Evidence/disposition |
|---|---|
| Select and inspect hardware | Source links and exact revision IDs visible; existing catalog/filter tests pass |
| Draft versus saved state | Changes do not save or repin; existing Python store/import tests pass |
| Generate versus source-only export | Distinct controls and descriptions retained |
| Identify displayed revision | Existing viewer model switching and status tests pass |
| Input changes after a build | Actual markDirty handler disables download/proposal and returns viewer to baseline |
| Render completes after inputs changed | Actual handler discards stale completion and leaves download disabled |
| Build fails | Actual handler surfaces error and restores generation control |
| Export integrity fails | Actual download handler displays server integrity error |
| Scale and orientation | UI now states millimeter convention, unencoded STL units and assembly coordinates; printer/slicer integration outside scope |
| Old cache entries | Preserved; UI/README explain explicit regeneration for integrity-checked download |
| Validation limits | PROPOSED/UNVALIDATED labels, nominal screening limits and UNKNOWNs retained |

Point5 disposition: source/automated workflow review complete WITH LIMITATIONS. This does not claim a new visual layout, real mouse/keyboard, browser compatibility or live-user-data acceptance. Those are not silently substituted for the listed checks. Any future desktop-control session requires Brian's separate approval.

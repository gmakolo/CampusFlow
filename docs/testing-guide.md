# Executed tests and local demonstration — Refs #2

Python 3.12.3; standard library only. Run from the repository root.

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -v
python3 -m unittest tests.test_search tests.test_reports tests.test_cli tests.test_understanding -v
python3 -m unittest discover -s integration_checks -v
python3 main.py --demo
```

The first two commands pass the original regressions and implemented Engineer B features. The third runs only B's tests. The separate integration checks currently fail three A-owned shared rules and skip the unavailable real note-boundary check. Do not report a fully integrated assessment pass.

Actual output is saved in `.local/tests.txt`, `.local/default-discovery.txt`, `.local/integration-blockers.txt`, and `.local/demo.txt`. These runtime artifacts are Git-ignored. The baseline suite passed 20 tests; the current main suite passes 67 (20 retained, 47 added).

## Step-by-step interactive demonstration

1. `python3 main.py` starts an in-memory CLI. Choose 6 first: total 0, all groups 0, resolution 0.0%.
2. Choose 1: title `Demo WiFi outage`; category `Network`; urgency `high`; affected users `12`. Record `T001` is critical. Try invalid counts first to see retries.
3. Choose 8: title `wIfI`, category `Network`, status `open`, priority `critical`. Only records satisfying all filters appear. Blank filters are unrestricted. Invalid enums retry.
4. Choose 16 for a separate search-result view ordered by priority and numeric ID. This does not replace queue option 5.
5. Choose 3, `T001`, `Demo Operator`. Choose 4, `T001`, `in_progress`. Queue option 5 excludes it; report option 6 counts it as unresolved.
6. Choose 4, `T001`, `resolved`. Report now shows resolution according to current state. Assignment/note menus reject the resolved ticket at the CLI.
7. Choose 9, `T001`, to explicitly reopen. Reports count it as open, not resolved.
8. Choose 10/11 with `T001`: until A supplies `campusflow.notes`, the CLI clearly reports pending integration and returns to the menu. With the real module present, entry calls `add_note` and viewing calls `get_notes`, sorting note IDs numerically.
9. Choose 12 for the six-question check. Invalid choices retry. After all choices, a score appears; explain Q1 and Q2 in your own words. These explanations are not auto-graded.
10. Choose 13/14: until A supplies `campusflow.storage`, these show pending integration. No fake JSON implementation writes records. After integration, use a separate practice path; save/load must preserve notes and ID continuity.
11. Choose 7 to exit. In-memory-only sessions explicitly warn if changes were not saved. EOF/Ctrl+C exits without a traceback.

The automated subprocess demonstration actually executed creation, combined search, empty-safe reports, assignment, progression, queue exclusion, resolution, reopening, and missing-API feedback. Transcript: `.local/manual-cli-demo.txt`. It did not claim actual notes/JSON persistence or a learner quiz attempt.

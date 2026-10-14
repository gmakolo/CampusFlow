# CampusFlow Next — Engineer B

Upgrade of the existing [gmakolo/CampusFlow](https://github.com/gmakolo/CampusFlow) Python command-line application. Engineer B: **miikese**. Engineer A: **gmakolo**. Work is tracked in [Issue #2](https://github.com/gmakolo/CampusFlow/issues/2), on `feat/2-engineer-b-campusflow-next`.

Python standard library only: no dependency installation, web framework, external API, or database is needed.

## Run on Linux

```bash
cd /home/student/CampusFlow
python3 main.py
```

From a fresh clone of the published branch:

```bash
git clone https://github.com/gmakolo/CampusFlow.git
cd CampusFlow
git switch feat/2-engineer-b-campusflow-next
python3 main.py
```

This is a **CLI**. The local launch script opens it in a terminal:

```bash
./open-local.sh
```

No browser/local web server is required. `python3 main.py --demo` runs a repeatable, fictional, in-memory Engineer B demonstration.

## Implemented Engineer B features

- Case-insensitive title substring search using `casefold()`.
- Optional category, status, and priority filters combined with AND; blank filters mean unrestricted.
- Read-only results with independent nested objects, helpful no-results feedback, and optional priority/numeric-ID result sorting.
- Reports with total, status, priority, and category counts; unresolved/resolved totals; zero-safe resolution percentage.
- CLI retries for invalid menu choices, enums and counts; useful unknown-ID messages; explicit reopening; defensive status/assignment/note checks; open-only queue display.
- Add/View Follow-up Note and save/load **adapters** for Engineer A's documented APIs.
- Six required quiz questions, A/B/C/D validation, scoring independent of the question bank, and two ungraded written explanations.
- Existing creation, priority, workflow, and original tests retained.

## Menu

| Choice | Operation |
| --- | --- |
| 1 / 2 | Create / list tickets |
| 3 / 4 | Assign / progress status |
| 5 / 6 | Original Open Work Queue / quality report |
| 7 | Exit (0 also accepted) |
| 8 / 16 | Search / separately sorted search |
| 9 | Explicitly reopen a resolved ticket |
| 10 / 11 | Add / view follow-up notes through A's API |
| 12 | Engineering Understanding Check |
| 13 / 14 | Save / load JSON through A's API |
| 15 | View ticket details |

Priority rule order remains unchanged: high urgency AND at least 10 affected users is critical; high urgency OR at least 10 is high; medium urgency OR at least 3 is medium; otherwise low. Categories are Network/Hardware/Software/Other; statuses are open/in_progress/resolved.

## Current integration blockers

**Engineer A's notes and JSON modules are not present.** Their menus clearly show this; the application does not pretend to persist records. Until A supplies those modules, records remain in memory and are lost on exit. `--data practice.json` requires A's actual storage module and safely stops if it is absent. There is currently no shared JSON format to document or silently replace.

Three inherited data-layer defects remain: queue inclusion of in-progress records, direct open-to-resolved transitions, and resolved reassignment. The B CLI guards these paths, but the business APIs still require A's correction. [Integration contracts](docs/integration-contracts.md) document exact proposed APIs and separate failing checks. The user explicitly chose B-only work, so A-owned files are unchanged.

`generate_reports` retains original report keys and extends them. Legacy sparse report fixtures that omit category count as Other; explicit invalid enum values are rejected. Real created records already include category. Search is substring matching, not fuzzy spelling or punctuation correction.

## Run tests

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -v
python3 -m unittest tests.test_search tests.test_reports tests.test_cli tests.test_understanding -v
```

Current implemented-feature suite: **67 passing tests**, including the original 20. Notes/storage CLI tests use explicit mocks because A's APIs do not exist. They do not prove actual persistence or note-state safety.

Run the separate assessment integration checks too:

```bash
python3 -m unittest discover -s integration_checks -v
```

Current actual result: **3 failures, 1 skip**. These make the known A-owned defects and missing note implementation visible. This project must not be described as fully assessment-complete or merged-main verified yet.

## Documentation and defence

- [Baseline evidence](docs/baseline-check.md)
- [Integration contracts and blockers](docs/integration-contracts.md)
- [Executed tests and step-by-step demo](docs/testing-guide.md)
- [Explain five B tests](docs/engineer-b-defence.md)
- [AI-assisted study experiments](docs/ai-learning-engineer-b.md)
- Existing [Engineer A learning log](docs/ai-learning-log.md), preserved

All new source/tests were produced with Codex assistance for miikese to review and defend. The study document labels assistant-executed experiments accurately; human reflections, independent quiz attempts, authorship evidence, and substantive reciprocal reviews must come from the engineers themselves.

## Collaboration

No changes are pushed to the old personal or former teammate repositories. No direct feature commit goes to main; no force push, self-approval, or merge is performed. Use the Git log to inspect focused commits:

```bash
git log --oneline origin/main..HEAD
```

PR title: `feat: add CampusFlow Next Engineer B search, analytics and CLI`. Description must include `Refs #2`, real tests, pending A integration, and AI-assistance disclosure; request `gmakolo` for review. Publication status and review evidence are recorded separately, never inferred from local commits.

Publication status: the Engineer B branch is pushed to the official repository. [PR #3](https://github.com/gmakolo/CampusFlow/pull/3) targets `main`, includes `Refs #2`, and requests `gmakolo` for review. Human review and approval are pending; nothing has been merged. See the [completion report](docs/completion-report.md) and [PR description](docs/pull-request-draft.md).

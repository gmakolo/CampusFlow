# Baseline check — 14 October 2026

Official repository: https://github.com/gmakolo/CampusFlow

Baseline commit: `4bca14da6963747a7bd6a2b853c04f669244fe09` (`main`). The fresh clone was clean. Executing tests created additional untracked Python 3.12 bytecode; the repository already tracks some Python 3.14 bytecode. Source files were unchanged during this assessment.

## Commands actually run

```text
git status
git branch -a
git fetch origin
git rev-parse HEAD
git log -8 --format='%h %an %s'
python3 --version
python3 -m unittest discover -s tests -v
python3 -m unittest discover -v
python3 main.py
```

Python version: 3.12.3. Required discovery command: **20 tests passed**, no failures. Default discovery from the repository root found **0 tests** and returned exit status 5 because `tests` was not an importable package. Adding a package marker on the feature branch fixes discovery without changing existing test assertions.

## Three manually checked terminal cases

The existing `main.py` was run in an interactive terminal and supplied these inputs. Output was inspected before source changes:

1. Menu choice `9`, then `6`: invalid choice feedback appeared; the menu continued; an empty report showed total 0 and zero status/priority counts. Category counts and resolution percentage were absent.
2. Create `WiFi down`, `Network`, `high`, `12`, then open the queue: produced `T001`, critical priority, open status, and displayed it in the queue.
3. Create with a blank title, `Network`, `low`, `1`: rejected with `Title cannot be empty`, returned to the menu, then exited cleanly with choice `7`.

## Defects reproduced against the baseline

A separate short Python script imported the actual baseline functions and reproduced:

- Assign `T001`, move it to `in_progress`, call `get_work_queue`: returned `['T001']`. The required Open Work Queue must exclude it.
- Call `update_status` on an unassigned open ticket with `resolved`: accepted the direct jump and changed data.
- Resolve an assigned ticket, then call `assign_ticket` with another staff label: accepted reassignment and changed the resolved ticket.

These are confirmed defects. The script used fresh in-memory fixtures for each case and did not touch any data file.

## Already working

Creation trims the title and validates canonical categories/urgencies. Positive-integer validation rejects booleans. Ticket IDs use the largest existing numeric ID. Priority follows the required four-rule order. Blank assignment and unassigned progression are rejected. A valid assigned lifecycle and the existing report tests pass. Basic invalid CLI selections are handled.

## Missing from this baseline

No notes module, note field on newly created records, search module, category/resolution analytics, understanding quiz, JSON storage module, save/load menus, or corresponding Next tests exist. README explicitly states that records are in memory and lost on exit.

## History and PR inspection

Recent commits by `gmakolo` supply creation, main menu, and ticket tests. PR #1, `feat(workflow): add workflow lifecycle logic and unit tests`, is merged; its commit author is `inakondu1`, so it is not evidence of the new teammate's Next work. No open Engineer A Next PR was found. No review comments were returned for PR #1. Human review/learning evidence must not be inferred from these facts.

## Previous personal repository comparison

Reference: `miikese/campusflow`, commit `dbdd069` (cloned separately in `/tmp/campusflow-personal-reference`). Its actual suite passed **49 tests**. It has strict workflow and validated atomic JSON persistence, but no structured notes. Its creation function appends to the supplied list, unlike the shared repository's function, which returns a record for the caller to append. Its status function takes `(tickets, ticket_id, new_status)`, unlike the shared function's `(ticket, new_status)`. Its report keys are also different.

No wholesale replacement is appropriate. Any reuse needs an explicit compatibility layer, note-schema updates, provenance disclosure, and Engineer A review.

## Access and remaining unconfirmed observations

The connected GitHub identity is `miikese`. Repository metadata reports push access. The integration rejected collaborator-permission lookup and issue creation with GitHub HTTP 403 (`Resource not accessible by integration`). This is an access limitation, not a failed application test. No issue number has been invented.

Malformed JSON behavior, note ID continuity, and 301-character note rejection cannot yet be reproduced against this repository because the corresponding modules do not exist. They remain integration requirements, not passing test claims.

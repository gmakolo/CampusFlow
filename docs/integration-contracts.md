# Engineer B integration contracts — Refs #2

Issue: https://github.com/gmakolo/CampusFlow/issues/2

The user explicitly requested **Engineer B only**. `campusflow/tickets.py`, `campusflow/workflow.py`, `tests/test_tickets.py`, and `tests/test_workflow.py` remain unchanged. These contracts are proposals awaiting Engineer A's confirmation, not a fabricated agreement.

## Existing shared contracts retained

| API | Existing behavior |
| --- | --- |
| `create_ticket(title, category, urgency, affected_users, existing_tickets=None)` | Returns a new dictionary; the caller appends it. |
| `assign_ticket(tickets, ticket_id, staff_name)` | Mutates the selected record, returns `True`, raises `ValueError`. |
| `update_status(ticket, new_status)` | Takes a single mutable record, returns `True`, raises `ValueError`. |
| `get_work_queue(tickets)` | Returns ordered records. The current backend incorrectly includes in-progress tickets. |
| `generate_reports(tickets)` | Original keys retained; added category, unresolved, resolved, and percentage values. |

The previous personal repository has incompatible creation and workflow signatures and an eight-field storage validator. It was inspected and tested but not copied over Engineer A's work.

## Proposed Engineer A notes contract

```python
add_note(tickets, ticket_id, author, message) -> dict
get_notes(tickets, ticket_id) -> list[dict]
```

Module: `campusflow.notes`. Each note is `{"note_id": "N001", "author": "Demo Operator", "message": "Router checked"}`.

A validates status, nonblank author, trimmed message length 5–300, ID uniqueness, and no changes on failure. Only open/in-progress tickets accept notes. Failed calls do not consume IDs. Resolved/reopened transitions preserve notes. IDs are independent for each ticket and continue after reload. A raises `ValueError`-compatible errors; B catches and displays them.

B's entry/view menus call these APIs through `integration_api`. There is **no substitute notes backend**. Tests explicitly mock A's APIs and verify calls, numeric display order, and error feedback; they do not prove absent data-layer rules. The CLI also blocks note entry on resolved tickets before asking for author/message.

## Proposed Engineer A storage contract

```python
load_tickets(path) -> list[dict]
save_tickets(tickets, path) -> None
```

Module: `campusflow.storage`. A parses and validates the complete collection before returning it. B replaces memory only after a successful return. Any parse/validation/save error is `ValueError`-compatible. The source file and existing memory must survive rejected operations.

A must document the actual JSON format and migration policy, validate required fields, duplicate ticket/note IDs, canonical enums, priority consistency, strictly positive non-Boolean counts, assignment/state rules, and notes. Next IDs must follow the highest existing numeric ID, not collection length. Save/reload tests must use temporary files.

The shared baseline has no JSON format. Engineer B does not introduce an independent format while A's implementation is pending. Save/load menus currently show a clear integration message. `--data` requires A's actual module; it stops safely if the module is absent.

## Shared defects requiring A review

- Enforce only open → in_progress → resolved; explicitly allow resolved → open reopening.
- Reject resolved reassignment without mutation.
- Make `get_work_queue` contain only open records.

B adds defensive **CLI** input checks/filtering, not replacements for these business functions. Direct data-layer calls still fail the shared acceptance checks. Correcting the data layer and rerunning those checks are required before claiming assessment completion.

```bash
python3 -m unittest discover -s integration_checks -v
```

Current result: three genuine failures and one skipped note-boundary test because the notes module is absent. The skip is not a pass.

"""Unresolved A-owned acceptance checks. Run separately; failures are real blockers."""
from copy import deepcopy
from importlib.util import find_spec
from unittest import TestCase, skipUnless
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue


class SharedContractChecks(TestCase):
    def setUp(self):
        self.records = [create_ticket("Demo WiFi", "Network", "high", 12)]

    def test_open_queue_excludes_in_progress_at_data_layer(self):
        assign_ticket(self.records, "T001", "Demo Operator")
        update_status(self.records[0], "in_progress")
        self.assertEqual(get_work_queue(self.records), [])

    def test_data_layer_rejects_open_to_resolved_without_mutation(self):
        before = deepcopy(self.records)
        with self.assertRaises(ValueError):
            update_status(self.records[0], "resolved")
        self.assertEqual(self.records, before)

    def test_data_layer_rejects_resolved_reassignment_without_mutation(self):
        assign_ticket(self.records, "T001", "Demo Operator")
        update_status(self.records[0], "in_progress")
        update_status(self.records[0], "resolved")
        before = deepcopy(self.records)
        with self.assertRaises(ValueError):
            assign_ticket(self.records, "T001", "Other Operator")
        self.assertEqual(self.records, before)

    @skipUnless(find_spec("campusflow.notes"), "Engineer A notes module is not implemented yet")
    def test_301_character_note_rejected_without_consuming_next_id(self):
        from campusflow.notes import add_note
        # Real integration test once A's API exists; no fake note implementation.
        self.records[0].setdefault("notes", [])
        first = add_note(self.records, "T001", "Demo Author", "A valid first note")
        self.assertEqual(first["note_id"], "N001")
        before = deepcopy(self.records)
        with self.assertRaises(ValueError):
            add_note(self.records, "T001", "Demo Author", "x" * 301)
        self.assertEqual(self.records, before)
        second = add_note(self.records, "T001", "Demo Author", "A valid second note")
        self.assertEqual(second["note_id"], "N002")

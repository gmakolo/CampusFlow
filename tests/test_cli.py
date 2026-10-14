"""Engineer B CLI tests; A-owned notes/storage are explicitly mocked, not implemented."""
import copy
import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch
import main
from tests.test_search import fixture


class CliTests(TestCase):
    def setUp(self):
        main.tickets = fixture()

    def run_inputs(self, function, inputs):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("sys.stdout", output):
            result = function()
        return result, output.getvalue()

    def test_invalid_menu_choice_retries_then_exits(self):
        result, output = self.run_inputs(lambda: main.run_menu(), ["banana", "99", "7"])
        self.assertEqual(result, 0)
        self.assertEqual(output.count("Invalid choice."), 2)

    def test_input_exhaustion_exits_cleanly(self):
        with patch("builtins.input", side_effect=EOFError), patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(main.run_menu(), 0)
        self.assertIn("Goodbye", output.getvalue())

    def test_invalid_category_and_count_retry_without_consuming_ticket_id(self):
        _, output = self.run_inputs(main.create_new_ticket, ["Test title", "Invalid", "Network", "high", "0", "-1", "1.2", "true", "12"])
        self.assertEqual(len(main.tickets), 5)
        self.assertEqual(main.tickets[-1]["id"], "T005")
        self.assertEqual(main.tickets[-1]["priority"], "critical")
        self.assertIn("Category must be one of", output)

    def test_search_retries_invalid_filter_and_combines_all_choices(self):
        before = copy.deepcopy(main.tickets)
        _, output = self.run_inputs(main.search_existing_tickets, ["wifi", "BadCategory", "Network", "closed", "open", "urgent", "critical"])
        self.assertIn("T001 | WiFi unavailable", output)
        self.assertNotIn("T002 |", output)
        self.assertEqual(main.tickets, before)

    def test_empty_optional_filters_are_unrestricted(self):
        _, output = self.run_inputs(main.search_existing_tickets, ["", "", "", ""])
        for ticket in main.tickets:
            self.assertIn(ticket["id"] + " |", output)

    def test_search_no_results_has_helpful_message(self):
        _, output = self.run_inputs(main.search_existing_tickets, ["not found", "", "", ""])
        self.assertIn("No tickets match all supplied filters", output)

    def test_empty_report_displays_zero_percentage(self):
        main.tickets = []
        _, output = self.run_inputs(main.view_report, [])
        self.assertIn("Resolution percentage: 0.0%", output)
        self.assertIn("Other: 0", output)

    def test_original_queue_display_excludes_in_progress_and_resolved(self):
        _, output = self.run_inputs(main.view_work_queue, [])
        self.assertIn("T001 |", output)
        self.assertIn("T004 |", output)
        self.assertNotIn("T002 |", output)
        self.assertNotIn("T003 |", output)

    def test_unknown_ticket_id_has_useful_feedback(self):
        _, output = self.run_inputs(lambda: main.run_menu(records=fixture()), ["3", "T999", "7"])
        self.assertIn("Unknown ticket ID: T999", output)

    def test_cli_rejects_resolved_assignment_without_changing_data(self):
        before = copy.deepcopy(main.tickets)
        with patch("builtins.input", return_value="T003"), self.assertRaises(ValueError):
            main.assign_existing_ticket()
        self.assertEqual(main.tickets, before)

    def test_status_input_prevents_direct_open_to_resolved(self):
        before = copy.deepcopy(main.tickets)
        with patch("builtins.input", side_effect=["T001", "resolved", EOFError]), patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(EOFError):
                main.update_existing_ticket()
        self.assertEqual(main.tickets, before)

    def test_full_cli_lifecycle_reopens_explicitly(self):
        records = fixture()
        inputs = ["3", "T001", "Demo Operator", "4", "T001", "in_progress", "4", "T001", "resolved", "9", "T001", "7"]
        result, output = self.run_inputs(lambda: main.run_menu(records), inputs)
        self.assertEqual(result, 0)
        self.assertEqual(records[0]["status"], "open")
        self.assertIn("Reopened T001", output)

    def test_notes_entry_calls_engineer_a_api(self):
        backend = Mock(return_value={"note_id": "N001", "author": "Demo Author", "message": "Router checked"})
        with patch("main.integration_api", return_value=backend):
            _, output = self.run_inputs(main.add_follow_up_note, ["T001", "Demo Author", "Router checked"])
        backend.assert_called_once_with(main.tickets, "T001", "Demo Author", "Router checked")
        self.assertIn("Added note N001", output)

    def test_note_backend_errors_preserve_menu_availability(self):
        backend = Mock(side_effect=ValueError("Message must contain 5–300 characters."))
        records = fixture()
        before = copy.deepcopy(records)
        with patch("main.integration_api", return_value=backend):
            result, output = self.run_inputs(lambda: main.run_menu(records), ["10", "T001", "Demo Author", "x" * 301, "7"])
        self.assertEqual(result, 0)
        self.assertIn("5–300 characters", output)
        self.assertEqual(records, before)

    def test_note_display_orders_numeric_ids(self):
        backend = Mock(return_value=[{"note_id": "N1000", "author": "Demo", "message": "Last note"}, {"note_id": "N999", "author": "Demo", "message": "Earlier note"}])
        with patch("main.integration_api", return_value=backend):
            _, output = self.run_inputs(main.view_ticket_notes, ["T001"])
        backend.assert_called_once_with(main.tickets, "T001")
        self.assertLess(output.index("N999"), output.index("N1000"))

    def test_empty_note_list_is_readable(self):
        with patch("main.integration_api", return_value=Mock(return_value=[])):
            _, output = self.run_inputs(main.view_ticket_notes, ["T001"])
        self.assertIn("No follow-up notes for T001", output)

    def test_quiz_menu_calls_check_without_changing_tickets(self):
        records = fixture()
        before = copy.deepcopy(records)
        with patch("main.run_understanding_check", return_value={"score": 6}) as quiz:
            self.run_inputs(lambda: main.run_menu(records), ["12", "7"])
        quiz.assert_called_once_with()
        self.assertEqual(records, before)

    def test_failed_a_storage_load_preserves_in_memory_records(self):
        before = copy.deepcopy(main.tickets)
        backend = Mock(side_effect=ValueError("Corrupted JSON"))
        with patch("main.integration_api", return_value=backend), self.assertRaises(ValueError):
            main.load_records(Path("not-written.json"))
        self.assertEqual(main.tickets, before)

    def test_save_adapter_calls_a_api_without_modifying_records(self):
        before = copy.deepcopy(main.tickets)
        backend = Mock()
        with patch("main.integration_api", return_value=backend):
            self.run_inputs(lambda: main.save_records(Path("not-written.json")), [])
        backend.assert_called_once_with(main.tickets, Path("not-written.json"))
        self.assertEqual(main.tickets, before)

    def test_resolved_note_menu_rejects_before_calling_backend(self):
        records = fixture()
        before = copy.deepcopy(records)
        backend = Mock()
        with patch("main.integration_api", return_value=backend):
            result, output = self.run_inputs(lambda: main.run_menu(records), ["10", "T003", "7"])
        self.assertEqual(result, 0)
        self.assertIn("must be reopened", output)
        backend.assert_not_called()
        self.assertEqual(records, before)

import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import save_tickets, load_tickets
from campusflow.tickets import create_ticket


class TestTicketStorage(unittest.TestCase):

    def test_save_and_load_tickets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = [
                create_ticket("WiFi issue", "Network", "high", 12)
            ]

            save_tickets(tickets, path)
            loaded = load_tickets(path)

            self.assertEqual(loaded, tickets)

    def test_invalid_data_does_not_overwrite_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = [
                create_ticket("WiFi issue", "Network", "high", 12)
            ]
            save_tickets(tickets, path)
            original_content = path.read_text(encoding="utf-8")

            with self.assertRaises(ValueError):
                save_tickets([{"id": "T001"}], path)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                original_content,
            )

    def test_duplicate_ticket_ids_are_rejected(self):
        ticket = create_ticket("WiFi issue", "Network", "high", 12)
        duplicate = ticket.copy()

        with self.assertRaises(ValueError):
            save_tickets([ticket, duplicate], "unused.json")

    def test_corrupt_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("{invalid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_failed_load_preserves_current_tickets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("not valid JSON", encoding="utf-8")

            current = [
                create_ticket("Printer issue", "Hardware", "medium", 2)
            ]
            original = [ticket.copy() for ticket in current]

            with self.assertRaises(ValueError):
                load_tickets(path, current)

            self.assertEqual(current, original)

    def test_notes_survive_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            ticket = create_ticket(
                "WiFi issue", "Network", "high", 12
            )
            ticket["notes"].append({
                "note_id": "N001",
                "author": "Gift",
                "message": "Router needs checking",
            })

            save_tickets([ticket], path)
            loaded = load_tickets(path)

            self.assertEqual(loaded[0]["notes"], ticket["notes"])


if __name__ == "__main__":
    unittest.main()

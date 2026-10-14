import unittest

from campusflow.tickets import (
    calculate_priority,
    validate_ticket,
    generate_ticket_id,
    create_ticket,
    add_note,
)


class TestCalculatePriority(unittest.TestCase):
    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority_from_urgency(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_high_priority_from_affected_users(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class TestValidateTicket(unittest.TestCase):
    def test_valid_ticket(self):
        self.assertTrue(
            validate_ticket("WiFi issue", "Network", "high", 12)
        )

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            validate_ticket("", "Network", "high", 12)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Electricity", "high", 12)

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Network", "urgent", 12)

    def test_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Network", "high", 0)

    def test_negative_affected_users(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Network", "high", -2)

    def test_float_affected_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Network", "high", 2.5)

    def test_boolean_affected_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("WiFi issue", "Network", "high", True)


class TestTicketCreation(unittest.TestCase):
    def test_create_ticket(self):
        ticket = create_ticket("WiFi issue", "Network", "high", 12)

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(ticket["notes"], [])

    def test_unique_ticket_ids(self):
        first = create_ticket("WiFi issue", "Network", "high", 12)
        second = create_ticket(
            "Broken laptop", "Hardware", "medium", 2, [first]
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_invalid_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket("", "Network", "high", 12)


class TestAddNote(unittest.TestCase):
    def setUp(self):
        self.ticket = create_ticket(
            "WiFi issue", "Network", "high", 5
        )
        self.tickets = [self.ticket]

    def test_add_valid_note(self):
        note = add_note(
            self.tickets, "T001", "Alice", "Router restarted"
        )

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Alice")
        self.assertEqual(note["message"], "Router restarted")
        self.assertEqual(len(self.ticket["notes"]), 1)

    def test_note_ids_increase(self):
        first = add_note(
            self.tickets, "T001", "Alice", "First update"
        )
        second = add_note(
            self.tickets, "T001", "Bob", "Second update"
        )

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_empty_author_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "   ", "Valid message")

        self.assertEqual(self.ticket["notes"], [])

    def test_short_message_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", "Hey")

        self.assertEqual(self.ticket["notes"], [])

    def test_long_message_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", "x" * 301)

        self.assertEqual(self.ticket["notes"], [])

    def test_rejected_note_does_not_consume_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", "Bad")

        note = add_note(
            self.tickets, "T001", "Alice", "Valid message"
        )

        self.assertEqual(note["note_id"], "N001")

    def test_resolved_ticket_rejects_note(self):
        self.ticket["status"] = "resolved"

        with self.assertRaises(ValueError):
            add_note(
                self.tickets, "T001", "Alice", "Valid message"
            )

        self.assertEqual(self.ticket["notes"], [])

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note(
                self.tickets, "T999", "Alice", "Valid message"
            )


if __name__ == "__main__":
    unittest.main()

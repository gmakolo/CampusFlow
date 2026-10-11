
import unittest

from campusflow.tickets import (
    calculate_priority,
    validate_ticket,
    generate_ticket_id,
    create_ticket,
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


class TestTicketCreation(unittest.TestCase):
    def test_create_ticket(self):
        ticket = create_ticket("WiFi issue", "Network", "high", 12)

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

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


if __name__ == "__main__":
    unittest.main()

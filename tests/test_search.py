"""Engineer B scope; AI-assisted tests for the learner to review and defend."""
import copy
import unittest
from campusflow.search import search_tickets, sort_search_results
from campusflow.tickets import create_ticket


def fixture():
    records = []
    for title, category, urgency, users in (
        ("WiFi unavailable", "Network", "high", 12),
        ("WIFI slow", "Network", "medium", 4),
        ("WiFi utility installation", "Software", "low", 1),
        ("Laptop screen", "Hardware", "high", 2),
    ):
        records.append(create_ticket(title, category, urgency, users, records))
    records[1]["status"] = "in_progress"
    records[1]["assigned_to"] = "Demo Operator"
    records[2]["status"] = "resolved"
    records[2]["assigned_to"] = "Demo Operator"
    return records


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.records = fixture()

    def test_title_substring_is_case_insensitive(self):
        self.assertEqual([t["id"] for t in search_tickets(self.records, "wIfI")], ["T001", "T002", "T003"])

    def test_casefold_matches_unicode_sharp_s(self):
        self.records[0]["title"] = "Straße connection"
        self.assertEqual(search_tickets(self.records, "STRASSE")[0]["id"], "T001")

    def test_combined_filters_use_and(self):
        result = search_tickets(self.records, "wifi", "network", "OPEN", "critical")
        self.assertEqual([t["id"] for t in result], ["T001"])

    def test_no_results_does_not_modify_records(self):
        before = copy.deepcopy(self.records)
        self.assertEqual(search_tickets(self.records, "screen", "Network"), [])
        self.assertEqual(self.records, before)

    def test_blank_filters_return_all_in_original_order(self):
        self.assertEqual(search_tickets(self.records, " ", "", None, ""), self.records)

    def test_invalid_filters_are_rejected(self):
        for filters in ({"category": "Electrical"}, {"status": "closed"}, {"priority": "urgent"}, {"title": 3}):
            with self.subTest(filters=filters), self.assertRaises(ValueError):
                search_tickets(self.records, **filters)

    def test_results_do_not_alias_nested_notes(self):
        self.records[0]["notes"] = [{"note_id": "N001", "author": "Demo", "message": "Original message"}]
        before = copy.deepcopy(self.records)
        result = search_tickets(self.records)
        result[0]["title"] = "Changed result"
        result[0]["notes"][0]["message"] = "Changed result note"
        self.assertEqual(self.records, before)

    def test_optional_sort_uses_priority_then_numeric_id(self):
        records = [dict(self.records[0], id="T1000"), dict(self.records[0], id="T999"), self.records[1]]
        before = copy.deepcopy(records)
        self.assertEqual([t["id"] for t in sort_search_results(records)], ["T999", "T1000", "T002"])
        self.assertEqual(records, before)

    def test_empty_search_is_empty(self):
        self.assertEqual(search_tickets([]), [])

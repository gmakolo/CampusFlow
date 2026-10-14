"""Engineer B current-state analytics tests, retaining the original API."""
import copy
import unittest
from campusflow.reports import generate_reports
from campusflow.workflow import update_status
from tests.test_search import fixture


class ReportingTests(unittest.TestCase):
    def test_empty_report_has_all_zero_groups_and_zero_percentage(self):
        report = generate_reports([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
        for group in ("status_breakdown", "priority_breakdown", "category_breakdown"):
            self.assertTrue(all(value == 0 for value in report[group].values()))

    def test_known_fixture_has_accurate_totals(self):
        report = generate_reports(fixture())
        self.assertEqual(report["status_breakdown"], {"open": 2, "in_progress": 1, "resolved": 1})
        self.assertEqual(report["category_breakdown"], {"Network": 2, "Hardware": 1, "Software": 1, "Other": 0})
        self.assertEqual(report["priority_breakdown"], {"critical": 1, "high": 1, "medium": 1, "low": 1})
        self.assertEqual(report["unresolved"], 3)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["resolution_percentage"], 25.0)

    def test_each_dimension_sums_to_total(self):
        report = generate_reports(fixture())
        for group in ("status_breakdown", "priority_breakdown", "category_breakdown"):
            self.assertEqual(sum(report[group].values()), report["total"])

    def test_reopened_ticket_counts_its_current_state(self):
        records = fixture()
        update_status(records[2], "open")
        report = generate_reports(records)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["unresolved"], 4)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_resolution_changes_percentage(self):
        records = fixture()
        update_status(records[1], "resolved")
        self.assertEqual(generate_reports(records)["resolution_percentage"], 50.0)

    def test_report_is_read_only(self):
        records = fixture()
        before = copy.deepcopy(records)
        generate_reports(records)
        self.assertEqual(records, before)

    def test_legacy_sparse_records_keep_original_report_compatibility(self):
        report = generate_reports([{"status": "open", "priority": "low"}])
        self.assertEqual(report["category_breakdown"]["Other"], 1)

    def test_explicit_invalid_dimensions_do_not_silently_disappear(self):
        for field, value in (("status", "closed"), ("priority", "urgent"), ("category", "Unknown")):
            records = fixture()
            records[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                generate_reports(records)

import unittest
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports

class TestWorkflowAndReports(unittest.TestCase):
    
    def setUp(self):
        self.tickets = [
            {"id": "T001", "title": "Wi-Fi Down", "priority": "high", "status": "open", "assigned_to": None},
            {"id": "T002", "title": "Broken Screen", "priority": "critical", "status": "open", "assigned_to": "Alice"},
            {"id": "T003", "title": "Printer Jam", "priority": "low", "status": "resolved", "assigned_to": "Bob"}
        ]

    def test_assign_ticket_success(self):
        res = assign_ticket(self.tickets, "T001", "Charlie")
        self.assertTrue(res)
        self.assertEqual(self.tickets[0]["assigned_to"], "Charlie")

    def test_assign_ticket_invalid_staff(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_update_status_unassigned_to_in_progress(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets[0], "in_progress")

    def test_update_status_assigned_lifecycle(self):
        update_status(self.tickets[1], "in_progress")
        self.assertEqual(self.tickets[1]["status"], "in_progress")
        
        update_status(self.tickets[1], "resolved")
        self.assertEqual(self.tickets[1]["status"], "resolved")
        
        update_status(self.tickets[1], "open")
        self.assertEqual(self.tickets[1]["status"], "open")

    def test_get_work_queue(self):
        queue = get_work_queue(self.tickets)
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue[0]["id"], "T002")
        self.assertEqual(queue[1]["id"], "T001")

    def test_generate_reports(self):
        report = generate_reports(self.tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["status_breakdown"]["resolved"], 1)
        self.assertEqual(report["status_breakdown"]["open"], 2)

if __name__ == "__main__":
    unittest.main()
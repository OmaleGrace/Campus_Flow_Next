import unittest
from campusflow.work_queue import get_work_queue


class TestWorkQueue(unittest.TestCase):

    def setUp(self):
        # A standard mock database fixture matching real ticket structures
        self.tickets = {
            "T003": {
                "id": "T003",
                "title": "Slow network",
                "priority": "high",
                "status": "open",
                "assigned_to": "Grace",
            },
            "T001": {
                "id": "T001",
                "title": "Server down",
                "priority": "critical",
                "status": "in_progress",
                "assigned_to": "John",
            },
            "T002": {
                "id": "T002",
                "title": "Computer issue",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            },
            "T004": {
                "id": "T004",
                "title": "Old request",
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Mary",
            },
            "T005": {
                "id": "T005",
                "title": "Software issue",
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            },
        }

    def test_critical_tickets_come_first(self):
        result = get_work_queue(self.tickets)
        self.assertEqual(result[0]["priority"], "critical")

    def test_priority_order(self):
        result = get_work_queue(self.tickets)
        priorities = [ticket["priority"] for ticket in result]
        self.assertEqual(
            priorities,
            ["critical", "high", "high", "medium"],
        )

    def test_same_priority_uses_numeric_ticket_id(self):
        result = get_work_queue(self.tickets)
        ids = [ticket["id"] for ticket in result]
        # T002 should appear before T003 because 2 < 3
        self.assertLess(ids.index("T002"), ids.index("T003"))

    def test_resolved_tickets_are_excluded(self):
        result = get_work_queue(self.tickets)
        ids = [ticket["id"] for ticket in result]
        self.assertNotIn("T004", ids)

    def test_empty_ticket_database(self):
        self.assertEqual(get_work_queue({}), [])

    def test_capitalized_resolved_status_is_excluded(self):
        self.tickets["T006"] = {
            "id": "T006",
            "title": "Completed task",
            "priority": "high",
            "status": "  Resolved  ",
            "assigned_to": "Grace",
        }
        result = get_work_queue(self.tickets)
        ids = [ticket["id"] for ticket in result]
        self.assertNotIn("T006", ids)

    def test_in_progress_status_is_included(self):
        self.tickets["T007"] = {
            "id": "T007",
            "title": "Active task",
            "priority": "high",
            "status": "in_progress",
            "assigned_to": "Grace",
        }
        result = get_work_queue(self.tickets)
        ids = [ticket["id"] for ticket in result]
        self.assertIn("T007", ids)


if __name__ == "__main__":
    unittest.main()

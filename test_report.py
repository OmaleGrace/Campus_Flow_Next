import unittest
from report import report_panel

class TestCampusFlowReportPanel(unittest.TestCase):

    def setUp(self):
        """
        Sets up a mock dictionary matching your function's expectation
        of accessing ticket elements via .values().
        """
        self.mock_ticket_dict = {
            "T001": {"id": "T001", "category": "Network", "priority": "critical", "status": "open"},
            "T002": {"id": "T002", "category": "Network", "priority": "high", "status": "in_progress"},
            "T003": {"id": "T003", "category": "Hardware", "priority": "medium", "status": "open"},
            "T004": {"id": "T004", "category": "Software", "priority": "low", "status": "resolved"}
        }

    def test_report_panel_accurate_totals_and_buckets(self):
        """
        Milestone B3/B6: Verifies your single-loop counters populate status,
        priority, and categories correctly without double counting.
        """
        record = report_panel(self.mock_ticket_dict)
        
        # Verify aggregate metrics matching your custom dictionary keys
        self.assertEqual(record["total_counts"], 4)
        self.assertEqual(record["unresolved_counts"], 3)  # 2 open + 1 in_progress
        self.assertEqual(record["resolved_counts"], 1)
        self.assertEqual(record["resolution_percentage"], 25.0)  # (1 / 4) * 100

        # Verify inner bucket structures
        self.assertEqual(record["status_counts"]["open"], 2)
        self.assertEqual(record["priority_counts"]["critical"], 1)
        self.assertEqual(record["category_counts"]["Network"], 2)

    def test_report_panel_empty_dataset_handling(self):
        """
        Requirement D: Verifies your conditional 'if total > 0' block 
        intercepts an empty dictionary safely and prevents a ZeroDivisionError.
        """
        empty_dictionary = {}
        
        try:
            record = report_panel(empty_dictionary)
            self.assertEqual(record["total_counts"], 0)
            self.assertEqual(record["resolution_percentage"], 0.0)
            self.assertEqual(record["unresolved_counts"], 0)
        except ZeroDivisionError:
            self.fail("report_panel crashed with a ZeroDivisionError on empty data structure!")

    def test_report_panel_skips_malformed_string_records(self):
        """
        Concept 2 / Defensive Programming: Verifies your inner guard block 
        (if isinstance(ticket, str)) intercepts malformed strings safely.
        """
        corrupted_dict = {
            "T001": {"category": "Network", "priority": "low", "status": "open"},
            "T002": "malformed database record line string"  # This should be skipped safely!
        }
        
        record = report_panel(corrupted_dict)
        
        # Total counts reads the structural dictionary keys length (= 2)
        self.assertEqual(record["total_counts"], 2)
        # But only the first valid dictionary ticket passes the counter mutations
        self.assertEqual(record["status_counts"]["open"], 1)
        self.assertEqual(record["status_counts"]["resolved"], 0)


if __name__ == "__main__":
    unittest.main()

import unittest
# Import your search logic function directly from your file layout matrix
from search import search_and_filter_tickets

class TestMultiFilterSearch(unittest.TestCase):

    def setUp(self):
        """
        Creates a clean, isolated database map (Dictionary format) 
        to accurately support the function's internal `.values()` loop layout.
        """
        self.mock_ticket_dict = {
            "T001": {
                "id": "T001",
                "title": "Campus Wi-Fi connectivity is broken",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": "Unassigned"
            },
            "T002": {
                "id": "T002",
                "title": "Slow Wi-Fi connection in block B",
                "category": "Network",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Operator A"
            },
            "T003": {
                "id": "T003",
                "title": "Lab printer hardware paper jam error",
                "category": "Hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": "Unassigned"
            },
            "T004": {
                "id": "T004",
                "title": "MS Word software installation failed",
                "category": "Software",
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Operator B"
            }
        }

    def test_search_title_substring_case_insensitive(self):
        """
        Milestone B1 Test: Verifies substring title search successfully 
        matches despite mixed-case using casefold normalization.
        """
        results = search_and_filter_tickets(self.mock_ticket_dict, title_query="WI-FI")
        self.assertEqual(len(results), 2)
        
        found_ids = [ticket["id"] for ticket in results]
        self.assertIn("T001", found_ids)
        self.assertIn("T002", found_ids)

    def test_combined_filters_strict_and_logic_success(self):
        """
        Milestone B2 Test: Verifies strict AND matching properties.
        Should ONLY return items matching title AND category AND status.
        """
        results = search_and_filter_tickets(
            self.mock_ticket_dict,
            title_query="wi-fi",
            category_filter="Network",
            status_filter="open"
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T001")

    def test_combined_filters_no_match_due_to_single_failure(self):
        """
        Milestone B2 Negative Test: If even a single condition fails to match,
        the ticket must be excluded.
        """
        results = search_and_filter_tickets(
            self.mock_ticket_dict,
            title_query="wi-fi",
            category_filter="Network",
            status_filter="resolved"
        )
        self.assertEqual(len(results), 0)

    def test_empty_filters_behaves_as_wildcard(self):
        """
        Requirement C Test: Verifies that blank arguments default gracefully
        and return all tickets without restriction.
        """
        results = search_and_filter_tickets(
            self.mock_ticket_dict,
            title_query="",
            category_filter="",
            status_filter="",
            priority_filter=""
        )
        self.assertEqual(len(results), 4)

    def test_defensive_whitespace_trimming(self):
        """
        Defensive Programming Test: Verifies filter conditions are trimmed 
        of trailing whitespace before executing matches.
        """
        results = search_and_filter_tickets(
            self.mock_ticket_dict,
            title_query="   printer   ",
            category_filter="  Hardware  ",
            status_filter=" open "
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T003")

if __name__ == "__main__":
    unittest.main()

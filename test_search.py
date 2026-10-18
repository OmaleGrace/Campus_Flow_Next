import unittest

from search import search_and_filter_tickets, sort_search_result


class TestMultiFilterSearch(unittest.TestCase):

    def setUp(self):
        """
        Creates a clean, isolated in-memory dataset before each individual test run.
        This provides a pristine mock environment to safely verify filter combinations.
        """
        self.mock_tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi connectivity is broken",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": "Unassigned"
            },
            {
                "id": "T002",
                "title": "Slow Wi-Fi connection in block B",
                "category": "Network",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Operator A"
            },
            {
                "id": "T003",
                "title": "Lab printer hardware paper jam error",
                "category": "Hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": "Unassigned"
            },
            {
                "id": "T004",
                "title": "MS Word software installation failed",
                "category": "Software",
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Operator B"
            }
        ]

    def test_search_title_substring_case_insensitive(self):
        """
        Milestone B1 Test: Verifies substring title search successfully 
        matches despite mixed-case and punctuation variants using casefold.
        """
        # Searching for mixed case "WI-FI" should match both T001 and T002
        results = search_and_filter_tickets(self.mock_tickets, title_query="WI-FI")
        self.assertEqual(len(results), 2)
        
        found_ids = [ticket["id"] for ticket in results]
        self.assertIn("T001", found_ids)
        self.assertIn("T002", found_ids)

    def test_combined_filters_strict_and_logic_success(self):
        """
        Milestone B2 Test: Verifies strict AND matching.
        Should ONLY return items matching title AND category AND status.
        """
        # Title "wi-fi" (matches T001, T002) + Category "Network" (matches T001, T002) + Status "open" (ONLY matches T001)
        results = search_and_filter_tickets(
            self.mock_tickets,
            title_query="wi-fi",
            category_filter="Network",
            status_filter="open"
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T001")

    def test_combined_filters_no_match_due_to_single_failure(self):
        """
        Milestone B2 Negative Test: If even a single condition fails to match,
        the ticket must be excluded (Strict AND logic compliance).
        """
        # Title matches T001 & T002, Category matches T001 & T002, but status doesn't match either
        results = search_and_filter_tickets(
            self.mock_tickets,
            title_query="wi-fi",
            category_filter="Network",
            status_filter="resolved"
        )
        self.assertEqual(len(results), 0)

    def test_empty_filters_behaves_as_wildcard(self):
        """
        Requirement C Test: Verifies that blank arguments default gracefully
        and do not restrict the search scope (behaving as 'do not filter').
        """
        # Passing completely blank criteria should bypass guards and return all tickets
        results = search_and_filter_tickets(
            self.mock_tickets,
            title_query="",
            category_filter="",
            status_filter="",
            priority_filter=""
        )
        self.assertEqual(len(results), 4)

    def test_defensive_whitespace_trimming(self):
        """
        Defensive Programming Test: Verifies filter conditions are trimmed 
        and cleaned of trailing whitespace before executing structural matches.
        """
        # Passing values padded out with spaces should still match perfectly
        results = search_and_filter_tickets(
            self.mock_tickets,
            title_query="   printer   ",
            category_filter="  Hardware  ",
            status_filter=" open "
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T003")

    def test_sorting_by_priority_descending(self):
        """
        Milestone D Test: Verifies that tickets are sorted primary by priority order
        from highest risk to lowest risk (Critical -> High -> Medium -> Low).
        """
        unsorted_tickets = [
            {"id": "T1", "priority": "low"},
            {"id": "T2", "priority": "critical"},
            {"id": "T3", "priority": "medium"},
            {"id": "T4", "priority": "high"}
        ]
        
        sorted_results = sort_search_result(unsorted_tickets)
        
        # Verify the priority order layout sequences
        self.assertEqual(sorted_results[0]["priority"], "critical")
        self.assertEqual(sorted_results[1]["priority"], "high")
        self.assertEqual(sorted_results[2]["priority"], "medium")
        self.assertEqual(sorted_results[3]["priority"], "low")

    def test_numeric_id_tie_breaker_bug(self):
        """
        Concept 3 / Milestone D Test: Verifies that if multiple tickets share the same
        priority, the tie-breaker cleanly places earlier numeric IDs first.
        This confirms your code defeats the string sorting trap (T10 vs T2).
        """
        # Both tickets are High priority. Mathematically, 2 should come before 10.
        tie_tickets = [
            {"id": "T10", "priority": "high"},
            {"id": "T2", "priority": "high"}
        ]
        
        sorted_results = sort_search_result(tie_tickets)
        
        # Ticket 2 must be placed first chronologically
        self.assertEqual(sorted_results[0]["id"], "T2")
        self.assertEqual(sorted_results[1]["id"], "T10")

    def test_case_insensitivity_and_whitespace_in_sorting(self):
        """
        Defensive Programming Test: Verifies that mixed-case priority strings 
        and padding whitespaces are safely normalized before the sort.
        """
        messy_tickets = [
            {"id": "T5", "priority": "  medium  "},
            {"id": "T6", "priority": "HIGH"},
            {"id": "T7", "priority": "Critical "}
        ]
        
        sorted_results = sort_search_result(messy_tickets)
        
        self.assertEqual(sorted_results[0]["id"], "T7")  # Critical
        self.assertEqual(sorted_results[1]["id"], "T6")  # HIGH
        self.assertEqual(sorted_results[2]["id"], "T5")  # medium

    def test_missing_or_malformed_id_defaults(self):
        """
        State Safety Test: Verifies that a ticket with an unexpected or non-numeric ID format
        defaults safely to 0 and sorts gracefully without raising an exception.
        """
        edge_case_tickets = [
            {"id": "T8", "priority": "low"},
            {"id": "INVALID_ID", "priority": "low"}  # Should extract no digits and default to 0
        ]
        
        sorted_results = sort_search_result(edge_case_tickets)
        
        self.assertEqual(sorted_results[0]["id"], "INVALID_ID")
        self.assertEqual(sorted_results[1]["id"], "T8")


if __name__ == "__main__":
    unittest.main()

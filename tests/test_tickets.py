import os
import sys
import json
import unittest

# Dynamic Path Resolution: Detects the directory containing 'tests/' and binds it to Python's import paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from campusflow.tickets import (
    load_tickets, 
    save_tickets, 
    next_ticket_id, 
    calculate_priority, 
    create_ticket, 
    can_transition, 
    next_note_id
)

TEST_DB_PATH = "test_database.json"

class PureInputSimulator:
    """Simulates raw keyboard entries to satisfy interactive prompt loops without using mock."""
    def __init__(self, inputs_list):
        self.iterator = iter(inputs_list)

    def simulate_read(self, prompt=""):
        try:
            return next(self.iterator)
        except StopIteration:
            return "n"


class TestTicketsLifecycle(unittest.TestCase):

    def setUp(self):
        # Clean local storage trace paths before execution
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        
        # Capture clean global references to avoid side effects
        self.original_input = __builtins__['input'] if isinstance(__builtins__, dict) else getattr(__builtins__, 'input')

    def tearDown(self):
        # Post-test cleanup: delete database traces and restore native user input controls
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
            
        if isinstance(__builtins__, dict):
            __builtins__['input'] = self.original_input
        else:
            setattr(__builtins__, 'input', self.original_input)

    def _inject_inputs(self, commands):
        """Helper to assign simulated response sequences to core console functions."""
        simulator = PureInputSimulator(commands)
        if isinstance(__builtins__, dict):
            __builtins__['input'] = simulator.simulate_read
        else:
            setattr(__builtins__, 'input', simulator.simulate_read)

    def test_next_ticket_id_generation(self):
        """Verifies primary autoincrement sequence operations."""
        db = {}
        self.assertEqual(next_ticket_id(db), "T001")
        
        db["T001"] = {"id": "T001"}
        db["T009"] = {"id": "T009"}
        self.assertEqual(next_ticket_id(db), "T010")

    def test_calculate_priority_matrix(self):
        """Verifies conditional evaluations map out correctly across scale thresholds."""
        self.assertEqual(calculate_priority("high", 12), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("medium", 4), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_create_ticket_interactive_lifecycle(self):
        """Verifies console prompting flow populates expected record properties successfully."""
        db = {}
        # Entry order matches prompt loop dependencies: Title -> Category -> Urgency -> Affected Users
        self._inject_inputs(["Server Down", "1", "3", "14"])

        ticket = create_ticket(db, path=TEST_DB_PATH)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["affected_users"], 14)

    def test_can_transition_assignment_guards(self):
        """Verifies operational process constraints raise errors if tickets are unassigned."""
        unassigned_ticket = {"status": "Open", "assigned_to": None}
        with self.assertRaises(ValueError):
            can_transition(unassigned_ticket, "in_progress")

        assigned_ticket = {"status": "Open", "assigned_to": "Alex (Eng)"}
        self.assertTrue(can_transition(assigned_ticket, "in_progress"))

    def test_next_note_id_increments(self):
        """Verifies child array elements auto-increment predictably."""
        sample_ticket = {"notes": []}
        self.assertEqual(next_note_id(sample_ticket), "N001")
        
        sample_ticket["notes"].append({"note_id": "N001", "message": "Investigating"})
        self.assertEqual(next_note_id(sample_ticket), "N002")


if __name__ == "__main__":
    unittest.main()

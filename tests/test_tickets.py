import os
import json
import unittest
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
    """Simulates console text entry without using the mock module."""
    def __init__(self, inputs_list):
        self.iterator = iter(inputs_list)

    def simulate_read(self, prompt=""):
        try:
            return next(self.iterator)
        except StopIteration:
            return "n"


class TestTicketsLifecycle(unittest.TestCase):

    def setUp(self):
        # Clear out filesystem trace states before every test run
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        
        # Safely preserve original reference to input builtin
        self.original_input = __builtins__['input'] if isinstance(__builtins__, dict) else getattr(__builtins__, 'input')

    def tearDown(self):
        # Clean filesystem states and restore builtins after every test execution
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
            
        if isinstance(__builtins__, dict):
            __builtins__['input'] = self.original_input
        else:
            setattr(__builtins__, 'input', self.original_input)

    def _inject_inputs(self, commands):
        """Helper to inject simulated entries directly into global scope."""
        simulator = PureInputSimulator(commands)
        if isinstance(__builtins__, dict):
            __builtins__['input'] = simulator.simulate_read
        else:
            setattr(__builtins__, 'input', simulator.simulate_read)

    def test_next_ticket_id_generation(self):
        """Test 1: Verifies unique autoincrement ID calculation mechanics."""
        db = {}
        self.assertEqual(next_ticket_id(db), "T001")
        
        db["T001"] = {"id": "T001"}
        db["T009"] = {"id": "T009"}
        self.assertEqual(next_ticket_id(db), "T010")

    def test_calculate_priority_matrix(self):
        """Test 2: Verifies complex conditional logic branches for matrix scaling."""
        self.assertEqual(calculate_priority("high", 12), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("medium", 4), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_create_ticket_interactive_lifecycle(self):
        """Test 3: Verifies console generation pipeline builds valid ticket schema profiles."""
        db = {}
        # Sequenced entries: Title -> Category Option -> Urgency Option -> Affected Users Count
        self._inject_inputs(["Server Down", "1", "3", "14"])

        ticket = create_ticket(db, path=TEST_DB_PATH)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["affected_users"], 14)

    def test_can_transition_assignment_guards(self):
        """Test 4: Verifies status workflows block unassigned movement paths."""
        unassigned_ticket = {"status": "Open", "assigned_to": None}
        with self.assertRaises(ValueError):
            can_transition(unassigned_ticket, "in_progress")

        assigned_ticket = {"status": "Open", "assigned_to": "Alex (Eng)"}
        self.assertTrue(can_transition(assigned_ticket, "in_progress"))

    def test_next_note_id_increments(self):
        """Test 5: Verifies child collection element sequence tagging logic."""
        sample_ticket = {"notes": []}
        self.assertEqual(next_note_id(sample_ticket), "N001")
        
        sample_ticket["notes"].append({"note_id": "N001", "message": "Investigating"})
        self.assertEqual(next_note_id(sample_ticket), "N002")

if __name__ == "__main__":
    unittest.main()

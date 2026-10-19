import os
import json
import unittest
# Import your actual menu file here
from follow_up_note import add_follow_up_menu

class PureInputSimulator:
    """Simulates console text entry without using the mock module."""
    def __init__(self, inputs_list):
        self.iterator = iter(inputs_list)

    def simulate_read(self, prompt=""):
        try:
            return next(self.iterator)
        except StopIteration:
            return ""


class TestAddFollowUpMenu(unittest.TestCase):

    def setUp(self):
        # 1. Setup a clean, temporary test database file
        # Make sure this matches whatever file path load_tickets() reads from!
        self.test_db_path = "tickets.json" 
        
        sample_data = {"T001": {"id": "T001", "notes": []}}
        with open(self.test_db_path, "w") as f:
            json.dump(sample_data, f)

        # 2. Preserve original built-in input function
        self.original_input = __builtins__['input'] if isinstance(__builtins__, dict) else getattr(__builtins__, 'input')

    def tearDown(self):
        # 1. Clean up the test database file so it doesn't leave clutter
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
        # 2. Restore original input functionality
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

    def test_add_follow_up_menu_success(self):
        """Verifies that adding a note to an existing ticket runs without crashing."""
        # Simulate typing: Ticket ID -> Author Name -> Note text
        self._inject_inputs(["t001", "Jane Doe", "Everything looks stable now."])

        # If your code has a validation bug, this call will raise an error and fail the test.
        # If it runs successfully, the test passes (Smoke Test style!).
        add_follow_up_menu()

    def test_add_follow_up_menu_handles_missing_ticket(self):
        """Verifies that typing an invalid ticket ID safely catches the ValueError."""
        # Simulate typing a non-existent ticket ID: T003
        self._inject_inputs(["t003", "Jane Doe", "This should trigger a validation failure."])

        # The function should internally hit the 'except ValueError' block and handle it gracefully
        add_follow_up_menu()


if __name__ == "__main__":
    unittest.main()

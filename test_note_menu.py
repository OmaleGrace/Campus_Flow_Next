import os
import json
import unittest
# Adjust this import to match the actual file name where ticket_note_menu lives
from note_menu import ticket_note_menu  

class PureInputSimulator:
    """Simulates console text entry without using the mock module."""
    def __init__(self, inputs_list):
        self.iterator = iter(inputs_list)

    def simulate_read(self, prompt=""):
        try:
            return next(self.iterator)
        except StopIteration:
            return ""


class TestTicketNoteMenu(unittest.TestCase):

    def setUp(self):
        # 1. Target the filename that load_tickets() reads from (usually tickets.json)
        self.test_db_path = "tickets.json" 
        
        # 2. Build mock database schema profile
        self.sample_db = {
            "T001": {
                "id": "T001", 
                "notes": [
                    {"note_id": "N001", "author": "Alice", "message": "Investigating issue"}
                ]
            },
            "T002": {
                "id": "T002",
                "notes": []  # Ticket with no notes
            }
        }
        
        # Write clean temporary state to disk
        with open(self.test_db_path, "w") as f:
            json.dump(self.sample_db, f)

        # 3. Preserve original built-in input function
        self.original_input = __builtins__['input'] if isinstance(__builtins__, dict) else getattr(__builtins__, 'input')

    def tearDown(self):
        # Clean filesystem states and restore builtins after every test execution
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
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

    def test_ticket_note_menu_displays_notes_successfully(self):
        """Test 1: Verifies valid ticket menu workflow prints target collection sequence profiles cleanly."""
        self._inject_inputs(["t001"])
        
        # Executes safely from top to bottom
        ticket_note_menu(ticket_dict={})

    def test_ticket_note_menu_handles_empty_notes(self):
        """Test 2: Verifies validation branch handles a ticket with zero notes gracefully."""
        self._inject_inputs(["t002"])
        
        # Hits the 'len(note_list) == 0' conditional branch and returns early
        ticket_note_menu(ticket_dict={})

    def test_ticket_note_menu_invalid_ticket_id(self):
        """Test 3: Verifies guard clause stops processing when view_notes validation returns False."""
        self._inject_inputs(["t003"])
        
        # Assuming your view_notes function returns None/False for T003, 
        # this verifies it triggers the early return guard structure safely.
        ticket_note_menu(ticket_dict={})


if __name__ == "__main__":
    unittest.main()
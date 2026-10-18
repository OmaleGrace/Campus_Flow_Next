import os
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
    def __init__(self, inputs_list):
        self.iterator = iter(inputs_list)

    def simulate_read(self, prompt=""):
        try:
            return next(self.iterator)
        except StopIteration:
            return "n" 
def run_test_suite():
    print("==================================================")
    print("   RUNNING PURE BACKEND LIFECYCLE VERIFICATIONS   ")
    print("==================================================")
    
    passed_tests = 0
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    builtin_scope = globals()['__builtins__']
    if isinstance(builtin_scope, dict):
        original_input = builtin_scope['input']
    else:
        original_input = getattr(builtin_scope, 'input')
    try:
        db = {}
        assert next_ticket_id(db) == "T001", "Base ticket ID should be T001"
        db["T001"] = {"id": "T001"}
        db["T009"] = {"id": "T009"}
        assert next_ticket_id(db) == "T010", "Sequence skip failed to find maximum marker"
        print("✔ Test 1: Unique Ticket ID Engine Passed Successfully.")
        passed_tests += 1
    except AssertionError as e:
        print(f"Test 1 Failed: {e}")

    try:
        assert calculate_priority("high", 12) == "critical", "Matrix breakdown on high+12"
        assert calculate_priority("high", 2) == "high", "Matrix breakdown on high isolated"
        assert calculate_priority("medium", 4) == "medium", "Matrix breakdown on medium scale"
        assert calculate_priority("low", 1) == "low", "Matrix breakdown on trivial items"
        print("✔ Test 2: Priority Grid Core Calculations Passed Successfully.")
        passed_tests += 1
    except AssertionError as e:
        print(f"Test 2 Failed: {e}")

    try:
        db = {}
        simulator = PureInputSimulator(["Server Down", "1", "3", "14"])
        
        if isinstance(builtin_scope, dict):
            builtin_scope['input'] = simulator.simulate_read
        else:
            setattr(builtin_scope, 'input', simulator.simulate_read)

        ticket = create_ticket(db, path=TEST_DB_PATH)
        
        if isinstance(builtin_scope, dict):
            builtin_scope['input'] = original_input
        else:
            setattr(builtin_scope, 'input', original_input)

        assert ticket is not None, "Ticket failed to build records properly"
        assert ticket["id"] == "T001", "Wrong baseline initialization"
        assert ticket["category"] == "Network", "Option mapping failed"
        assert ticket["priority"] == "critical", "Calculated priority assignment error"
        print("✔ Test 3: Interactive Console Creation Lifecycle Passed Successfully.")
        passed_tests += 1
    except AssertionError as e:
        if isinstance(builtin_scope, dict):
            builtin_scope['input'] = original_input
        else:
            setattr(builtin_scope, 'input', original_input)
        print(f"Test 3 Failed: {e}")
    try:
        unassigned_ticket = {"status": "Open", "assigned_to": None}
        try:
            can_transition(unassigned_ticket, "in_progress")
            raise AssertionError("Allowed unassigned transition to progress status")
        except ValueError:
            pass

        assigned_ticket = {"status": "Open", "assigned_to": "Alex (Eng)"}
        assert can_transition(assigned_ticket, "in_progress") == True, "Valid workflow blocked"
        print("Test 4: Assignment Transition Guards Passed Successfully.")
        passed_tests += 1
    except AssertionError as e:
        print(f"Test 4 Failed: {e}")
    try:
        sample_ticket = {"notes": []}
        assert next_note_id(sample_ticket) == "N001", "Notes collection base initialization error"
        sample_ticket["notes"].append({"note_id": "N001", "message": "Investigating"})
        assert next_note_id(sample_ticket) == "N002", "Incremental sequence mapping error"
        print("✔ Test 5: Notes Generation Counter Passed Successfully.")
        passed_tests += 1
    except AssertionError as e:
        print(f"Test 5 Failed: {e}")

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    print("\n==================================================")
    print(f"   VERIFICATION COMPLETE: {passed_tests}/5 MODULES PASSED   ")
    print("==================================================")

if __name__ == "__main__":
    run_test_suite()

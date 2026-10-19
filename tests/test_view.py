
import json
import os
import sys
from io import StringIO
from campusflow.view_tickets import view_ticket_details

def setup_test_database(data):
    """Creates a temporary database file for the ticket engine to read."""
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)

def teardown_test_database():
    if os.path.exists("database.json"):
        os.remove("database.json")

def run_test_case(simulated_input, database_payload):
    setup_test_database(database_payload)
    
    # Save original streams
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    
    try:
        # Redirect inputs and capture outputs using pure memory streams
        sys.stdin = StringIO(simulated_input)
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Execute the actual function
        view_ticket_details()
        
        return captured_output.getvalue()
    finally:
        # Restore environment streams safely
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        teardown_test_database()

# ==================== THE TEST SUITE ====================

def test_view_existing_ticket():
    mock_db = {
        "T001": {
            "id": "T001",
            "title": "Database Outage",
            "category": "Software",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "Open",
            "assigned_to": "Alice",
            "notes": ["Investigating replication logs."]
        }
    }
    
    output = run_test_case("T001\n", mock_db)
    
    assert "Database Outage" in output
    assert "CRITICAL" in output
    assert "Alice" in output
    assert "Investigating replication logs." in output
    print("✅ Success: Ticket details extracted and formatted accurately.")

def test_view_missing_ticket():
    mock_db = {
        "T001": {"id": "T001", "title": "Test", "category": "Other", "urgency": "low", "affected_users": 1, "priority": "low", "status": "Open", "assigned_to": None, "notes": []}
    }
    
    output = run_test_case("T999\n", mock_db)
    
    assert "Error: Ticket with ID 'T999' could not be found." in output
    print("✅ Success: Handled missing lookup requests correctly.")

def test_case_insensitivity():
    mock_db = {
        "T001": {"id": "T001", "title": "Case Test", "category": "Other", "urgency": "low", "affected_users": 1, "priority": "low", "status": "Open", "assigned_to": None, "notes": []}
    }
    
    # Test passing lowercase 't001' to look up uppercase key 'T001'
    output = run_test_case("t001\n", mock_db)
    
    assert "Case Test" in output
    print("✅ Success: Verified ID lookup ignores case mismatches.")

if __name__ == "__main__":
    print("Starting integration tests (File Stream Layer)...")
    test_view_existing_ticket()
    test_view_missing_ticket()
    test_case_insensitivity()
    print("All integration tests passed successfully!")


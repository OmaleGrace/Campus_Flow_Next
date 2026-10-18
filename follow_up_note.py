from campusflow.validate_add_note import add_note
from campusflow.tickets import load_tickets

def add_follow_up_menu():
    print("\n--- ADD FOLLOW-UP NOTE---")
    db = load_tickets()
    tick_id = input("Enter Ticket ID (eg T001..): ").strip().upper()
    author_name = input("Enter Your Name: ").strip()
    message_content = input("Enter follow-u Notes:\n> ").strip()

    try:
        success = add_note(tickets_database=db, ticket_id=tick_id, author=author_name, message=message_content)

        if success:
            print(f"Success! Note added to Ticket {tick_id}")
    except ValueError as error_message:
        print(f"\n Validation Rejected: {error_message}")
        print("Please review your input and try again.")
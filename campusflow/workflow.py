import json
from campusflow.tickets import can_transition 

VALID_STATUSES = ("open", "in_progress", "resolved")

def update_ticket_status(tickets, ticket_id, new_status):
    ticket_id = ticket_id.strip().upper()
    new_status = new_status.strip().lower()
    if ticket_id not in tickets:
        raise ValueError("Ticket ID does not exist.")
    ticket = tickets[ticket_id]

    can_transition(ticket, new_status)
    ticket["status"] = new_status

    try:
        with open("database.json", "w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)
    except OSError as error:
        raise ValueError(
            f"Could not save ticket status: {error}"
        ) from error

    return ticket


def change_ticket_status(tickets):
    if not tickets:
        print("No tickets available.")
        return

    ticket_id = input("Enter ticket ID: ").strip().upper()

    if ticket_id not in tickets:
        print("Error: Ticket ID does not exist.")
        return

    print("\nAvailable statuses:")
    print("1. open")
    print("2. in_progress")
    print("3. resolved")

    status_options = {
        "1": "open",
        "2": "in_progress",
        "3": "resolved",
    }

    choice = input("Choose the new status: ").strip()

    if choice not in status_options:
        print("Error: Invalid status selection.")
        return

    new_status = status_options[choice]

    try:
        ticket = update_ticket_status(
            tickets,
            ticket_id,
            new_status,
        )

        print(
            f"Ticket {ticket_id} status updated to "
            f"{ticket['status']} successfully."
        )
    except ValueError as error:
        print(f"Error: {error}")

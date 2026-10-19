from campusflow.tickets import load_tickets

def view_ticket_details():

    tickets_database = load_tickets()
    if not tickets_database:
        print("No tickets found or the database file is empty.")
        return

    target_id = input("Enter Ticket ID to view (e.g., T001): ").strip()

    matching_ticket = None
    for ticket_id, details in tickets_database.items():
        if ticket_id.lower() == target_id.lower():
            matching_ticket = details
            break

    if matching_ticket:
        print(f"\n================ TICKET DETAILS ({matching_ticket['id']}) ================")
        print(f"Title:           {matching_ticket['title']}")
        print(f"Category:        {matching_ticket['category']}")
        print(f"Urgency:         {matching_ticket['urgency']}")
        print(f"Affected Users:  {matching_ticket['affected_users']}")
        print(f"Priority Level:  {matching_ticket['priority'].upper()}")
        print(f"Current Status:  {matching_ticket['status']}")

        assigned = matching_ticket['assigned_to'] if matching_ticket['assigned_to'] else "Unassigned"
        print(f"Assigned To:     {assigned}")

        print("-" * 58)
        print("Notes:")
        if matching_ticket['notes']:
            for note in matching_ticket['notes']:
                print(f" - {note}")
        else:
            print(" No notes added to this ticket yet.")
        print("==========================================================")
    else:
        print(f"Error: Ticket with ID '{target_id}' could not be found.")
if __name__ == "__main__":
    view_ticket_details()

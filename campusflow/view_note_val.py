def view_notes(tickets_database, ticket_id):
    
    ticket_id = ticket_id.strip().upper()

    if not ticket_id:
        print("Ticket ID cannot be blank.")
        
    if ticket_id not in tickets_database:
        print(f"Ticket {ticket_id} not found.")
        
    ticket = tickets_database[ticket_id]
    
    return ticket["notes"]

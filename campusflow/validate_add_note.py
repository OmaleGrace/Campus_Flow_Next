from campusflow.tickets import next_note_id

def add_note(tickets_database, ticket_id, author, message, path="database.json"):

    ticket_id = ticket_id.strip().upper()
    author = author.strip()
    message = message.strip()

    if not ticket_id:
        raise ValueError("Ticket ID cannot be blank.")
        
    if ticket_id not in tickets_database:
        raise KeyError(f"Ticket {ticket_id} not found in database.")
        
    ticket = tickets_database[ticket_id]

    if ticket["status"].strip().lower() == "resolved":
        raise ValueError("Cannot add notes to a Resolved ticket.")

    if not author:
        raise ValueError("Note author cannot be blank.")
        
    if not message:
        raise ValueError("Note message cannot be blank.")
        
    if len(message) < 5 or len(message) > 300:
        raise ValueError("Note message must be between 5 and 300 characters long.")

    note_id = next_note_id(ticket).strip()
    
    note_record = {
        "note_id": note_id,
        "author": author,
        "message": message
    }
    ticket["notes"].append(note_record)
    save_tickets(tickets_database, path) 
    return ticket

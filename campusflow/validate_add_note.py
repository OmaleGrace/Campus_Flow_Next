from campusflow.tickets import next_note_id,save_tickets

def add_note(tickets_database, ticket_id, author, message, path="database.json"):

    ticket_id = ticket_id.strip().upper()
    author = author.strip()
    message = message.strip()

    if not ticket_id:
        print("Ticket ID cannot be blank.")
        return
        
    if ticket_id not in tickets_database:
        print(f"Ticket {ticket_id} not found in database.")
        return
        
    ticket = tickets_database[ticket_id]

    if ticket["status"].strip().lower() == "resolved":
        print("Cannot add notes to a Resolved ticket.")
        return

    if not author:
        print("Note author cannot be blank.")
        return
        
    if not message:
        print("Note message cannot be blank.")
        return
        
    if len(message) < 5 or len(message) > 300:
        print("Note message must be between 5 and 300 characters long.")
        return

    note_id = next_note_id(ticket).strip()
    
    note_record = {
        "note_id": note_id,
        "author": author,
        "message": message
    }
    ticket["notes"].append(note_record)
    save_tickets(tickets_database, path) 
    return ticket

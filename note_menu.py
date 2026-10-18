
def ticket_note_menu(ticket_dict):
    print("\n --- VIEW TICKET NOTES ---")
    ticket_id = input("Enter Ticket Id (eg T001 ...): ").upper()

    ticket_dict
        
        # validate ticket id
    if ticket_id not in ticket_dict:
        print(f"Error: Ticket Id {ticket_id} not found in the system database")
        return
    
    note_list = ticket_dict[ticket_id].get("notes", [])

    # validate the existence of not in a ticket
    if len(note_list) == 0:
        print(f"No notes have been added to Ticket {ticket_id} yet.")
        return
    print(f"\n Follow-up Note for Ticket {ticket_id}:")
    print("-" * 50)
    for note in note_list:
        print(f"Note ID: {note.get('note_id')}")
        print(f"Author: {note.get('author')}")
        print(f"Message: {note.get('message')}")
        print("-" * 50)
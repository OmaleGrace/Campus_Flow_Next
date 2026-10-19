from campusflow.view_note_val import view_notes
from campusflow.tickets import load_tickets

def ticket_note_menu(ticket_dict):
    print("\n --- VIEW TICKET NOTES ---")
    tict_id = input("Enter Ticket Id (eg T001 ...): ").upper()

    ticket_dict= load_tickets()
        
    # validate ticket id
    ticket_note = view_notes(tickets_database=ticket_dict, ticket_id= tict_id)
    if not ticket_note:
        return
    note_list = ticket_dict[tict_id].get("notes", [])

    # validate the existence of note in a ticket
    if len(note_list) == 0:
        print(f"No notes have been added to Ticket {tict_id} yet.")
        return
    print(f"\n Follow-up Note for Ticket {tict_id}:")
    # Display Follow-Up Note 
    print("-" * 50)
    for note in note_list:
        print(f"Note ID: {note.get('note_id')}")
        print(f"Author: {note.get('author')}")
        print(f"Message: {note.get('message')}")
        print("-" * 50)
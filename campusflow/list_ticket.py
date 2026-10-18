from campusflow.tickets import load_tickets

def list_ticket():
    
    tickets_database=load_tickets
    print("**Tickets-ID**:")
    for id_list in tickets_database():
        print(id_list)

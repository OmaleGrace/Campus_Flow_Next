from campusflow.tickets import load_tickets

def view_ticket():
    tickets_database=load_tickets
    while True:
        choose=input("Enter Ticket_ID:").strip().upper()
        if choose in tickets_database() and tickets_database() !={}:
            print(f"\n================ Detail FOR TICKET {choose} ================")
            print(tickets_database()[choose])
            print("==================================================================")
            break
        else:
            print("invalid id number/empty data")
            print("==================================================")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return 
    


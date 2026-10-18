from campusflow.tickets import create_ticket, load_tickets
from campusflow.list_ticket import list_ticket
from campusflow.view_ticket import view_ticket
from campusflow.assign_ticket import assign_ticket
from campusflow.workflow import change_ticket_status
from campusflow.work_queue import display_work_queue
from campusflow.reports import display_report

def campus_flow():
    while True:
        design="🀫"*51
        print()
        print("****Welcome To CampusFlow Helper Desk Service****")
        print(design)
        print("Menu")
        print("᠆᠆᠆᠆᠆")
        print("1. Generate Ticket")
        print("2. List Tickets")
        print("3. View Ticket")
        print("4. Assign Ticket")
        print("5. Reports")
        print("6. Change Ticket Status")
        print("7. Work Queue")
        print("8. Exit")
        option = input("Select option: ")
        db = load_tickets("database.json")
        if option == "1":
            create_ticket(db, "database.json")
        elif option == "2":
            list_ticket()
        elif option == "3":
            view_ticket()
        elif option == "4":
            assign_ticket(db)
        elif option == "5":
            display_report(db)
        elif option == "6":
            change_ticket_status(db)
        elif option == "7":
            display_work_queue(db)
        elif option == "8":
            add_ticket_note(db)
        elif option == "9":
            view_ticket_notes(db)
        elif option == "10":
            print("Exited...")
            break
        else:
            print("invalid option..")  
if __name__ == "__main__":
    campus_flow()
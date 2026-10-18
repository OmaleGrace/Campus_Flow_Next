from campusflow.tickets import create_ticket, load_tickets
from campusflow.list_ticket import list_ticket
from campusflow.assign_ticket import assign_ticket
from campusflow.workflow import change_ticket_status
from campusflow.work_queue import display_work_queue
from campusflow.reports import display_report
from report import print_summary_table
from search_cli import search_menu
from cli_understanding_check import run_cli_understanding_check

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
        print("3. Assign Ticket")
        print("4. Reports")
        print("5. Change Ticket Status")
        print("6. Work Queue")
        print("7. HOC Report")
        print("8. Search")
        print("9. Understanding_Check")
        print("10. Exit")
        option = input("Select option: ")
        db = load_tickets("database.json")
        if option == "1":
            create_ticket(db, "database.json")
        elif option == "2":
            list_ticket()
        elif option == "3":
            assign_ticket(db)
        elif option == "4":
            display_report(db)
        elif option == "5":
            change_ticket_status(db)
        elif option == "6":
            display_work_queue(db)
        elif option == "7":
            print_summary_table()
        elif option == "8":
            search_menu(db)
        elif option == "9":
            run_cli_understanding_check()
        elif option == "10":
            print("Exited...")
            break
        else:
            print("invalid option..")  
if __name__ == "__main__":
    campus_flow()
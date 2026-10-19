from campusflow.tickets import create_ticket, load_tickets
from campusflow.list_ticket import list_ticket
from campusflow.view_tickets import view_ticket_details
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
        print("3. view ticket")
        print("4. Assign Ticket")
        print("5. Reports")
        print("6. Change Ticket Status")
        print("7. Work Queue")
        print("8. HOC Report")
        print("9. Search")
        print("10. Understanding_Check")
        print("11. Exit")
        option = input("Select option: ")
        db = load_tickets("database.json")
        if option == "1":
            create_ticket(db, "database.json")
        elif option == "2":
            list_ticket()
        elif option == "3":
            view_ticket_details()
        elif option == "4":
            assign_ticket(db)
        elif option == "5":
            display_report(db)
        elif option == "6":
            change_ticket_status(db)
        elif option == "7":
            display_work_queue(db)
        elif option == "8":
            print_summary_table()
        elif option == "9":
            search_menu(db)
        elif option == "10":
            run_cli_understanding_check()
        elif option == "11":
            print("Exited...")
            break
        else:
            print("invalid option..")  
if __name__ == "__main__":
    campus_flow()
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
from follow_up_note import add_follow_up_menu
from note_menu import ticket_note_menu

def campus_flow():
    filename = "database.json"
    db = load_tickets(filename)
    menu_design = "🀫" * 51
    menu_display_text = f"""
****Welcome To CampusFlow Helper Desk Service****
{menu_design}
Menu
᠆᠆᠆᠆᠆
1. Generate Ticket
2. List Tickets
3. view Ticket
4. Assign Ticket
5. Reports
6. Change Ticket Status
7. Work Queue
8. HOC Report
9. Search
10. Follow-Up Note
11. View Note Manu
12. Understanding_Check
13. Exit"""
    def execute_menu_action(choice):
        if choice == "1":
            create_ticket(db, filename)
        elif choice == "2":
            list_ticket()
        elif choice == "3":
            view_ticket_details()
        elif choice == "4":
            assign_ticket(db)
        elif choice == "5":
            display_report(db)
        elif choice == "6":
            change_ticket_status(db)
        elif choice == "7":
            display_work_queue(db)
        elif choice == "8":
            print_summary_table()
        elif choice == "9":
            search_menu(db)
        elif choice == "10":
            add_follow_up_menu()
        elif choice == "11":
            ticket_note_menu(db)
        elif choice == "12":
            run_cli_understanding_check()
        else:
            print("Invalid option..")
    while True:
        print(menu_display_text)
        option = input("Select option: ").strip()

        if option == "13":
            print("Exited...")
            break
        execute_menu_action(option)
if __name__ == "__main__":
    campus_flow()
def display_main_menu_interface():
    while True:
        print("\n==============================================")
        print("        CAMPUSFLOW NEXT: MAIN CONSOLE        ")
        print("==============================================")
        print("1. Search & Multi-Filter Tickets ")
        print("2. View Ticket Follow-up Notes ")
        print("3. Add Structured Follow-up Note")
        print("4. View Executive Quality Insights Report")
        print("5. Run Engineering Understanding Check Quiz")
        print("6. Go Back To CampusFlow")
        print("==============================================")
        
        select = input("Select an option (1-6): ").strip()
        if not select:
            print("Option cannot be blank")
            return
        
display_main_menu_interface()
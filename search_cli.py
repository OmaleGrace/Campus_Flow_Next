from search import search_and_filter_tickets, sort_search_result

def search_menu(ticket_list):
    print("\n" + "*" * 35)
    print("    CAMPUSFLOW SEARCH WORKSPACE  ")
    print("*" * 35)

    query = input("Search by title substring: ").strip()
    category = input("Filter by Category (Network/Hardware/Software/Others): ").strip()
    status = input("Filter by Status (open/in_progress/resolved): ").strip()
    priority= input("Filter by Priority (critical/high/medium/low): ").strip()

    res = search_and_filter_tickets(
        tickets = ticket_list,
        title_query = query,
        category_filter = category,
        status_filter = status,
        priority_filter = priority
    )
    if len(res) == 0:
        print("No ticket matched your combined search critaria.")
        return
    # sort by priority 
    sort_choice = input("Sort result by Priority and Numeric Id sequence? (y/n): ").strip()
    if sort_choice =="y":
        res = sort_search_result(res)
    
    print("\n"+ "=" * 85)

    # print layout on the terminal
    print(f"{'ID':<6} | {'TITLE':<25} | {'CATEGORY':<10} | {'PRIORITY':<10} | {'STATUS':<12} | {'ASSIGNED TO'}")
    print("=" * 85)
    
    for ticket in res:
        t_id = ticket.get("id", "N/A")
        t_title = ticket.get("title", "No Title")
        t_category = ticket.get("category", "Other")
        t_priority = ticket.get("priority", "low")
        t_status = ticket.get("status", "open")
        t_assigned = ticket.get("assigned_to", "Unassigned")
        if len(t_title) > 22:
            t_title = t_title[:22] + "..."
            
        print(f"{t_id:<6} | {t_title:<25} | {t_category:<10} | {t_priority:<10} | {t_status:<12} | {t_assigned}")
    
    print("=" * 85 + "\n")

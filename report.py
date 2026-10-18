from campusflow.tickets import load_tickets

def report_panel(ticket_list):

    total = len(ticket_list)

    # create dictionary for counts (status, priority, category)
    status_count = {"open": 0, "in_progress": 0, "resolved": 0}
    priority_count = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    category_count = {"Network": 0, "Hardware": 0, "Software": 0, "Other": 0}


    for ticket in ticket_list.values():
        if isinstance(ticket, str):
            print(f"invalid data entery: {ticket}")
            continue
        # validate keys to avoid case mismatch
        status = ticket.get("status", "").strip().lower()
        priority  = ticket.get("priority", "").strip().lower()
        category = ticket.get("category", "").strip()

        if status in status_count:
            status_count[status] += 1
        if priority in priority_count:
            priority_count[priority] += 1
        if category in category_count:
            category_count[category] += 1
    
    unresolved_ticket = status_count["open"] + status_count["in_progress"]
    resolved_ticket = status_count["resolved"]

    # validate total for resolution percentage to avoid ZeroDivisionError
    resolution_percentage = 0.0
    if total > 0:
        resolution_percentage = round(((resolved_ticket/total) * 100), 2)
    else:
        print("Total can't be less than or equel to zero")
    record = {
        "total_counts": total,
        "status_counts": status_count,
        "priority_counts": priority_count,
        "category_counts": category_count,
        "unresolved_counts": unresolved_ticket,
        "resolved_counts": resolved_ticket,
        "resolution_percentage": resolution_percentage
    }
    return record
def print_summary_table():
    panel = report_panel(load_tickets())
    print(f"\n{'SUMMARY MATRICS' :<25} | {'COUNT / VALUE'}")
    print("-" * 45)

    print(f"{'Total Tickets': <25} | {panel['total_counts']}")
    print(f"{'Resolved Tickets':<25} | {panel['resolved_counts']}")
    print(f"{'Unresolved Tickets':<25} | {panel['unresolved_counts']}")
    print(f"{'Resolution Rate':<25} | {panel['resolution_percentage']}")
    print("-" * 45)

    breakdowns ={
        "Status Breakdown": panel["status_counts"],
        "Priority Breakdown": panel["priority_counts"],
        "Category Breakdown": panel["category_counts"]
    }
    for title, breakdown_dic in breakdowns.items():
        print(f"\n[{title}]")
        for key, value in breakdown_dic.items():
            print(f" {key.capitalize():<23} | {value}")

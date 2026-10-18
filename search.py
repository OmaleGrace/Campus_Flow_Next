
def search_and_filter_tickets(
    tickets: list, 
    title_query: str = "", 
    category_filter: str = "", 
    status_filter: str = "", 
    priority_filter: str = ""
) -> list:
    
    filtered_results = []
    
    clean_query = title_query.strip().casefold()
    
    # Loop through every single ticket in the system one by one
    for ticket in tickets:
        
        if clean_query:
            # Safely grab the title, lowercase it with casefold
            ticket_title = ticket.get("title", "").casefold()
    
            # we reject this ticket immediately and move to the next one.
            if clean_query not in ticket_title:
                continue 

        # Filter by Category Check
        if category_filter and category_filter.strip():
            if ticket.get("category") != category_filter.strip():
                continue

        # Filter by Status Check        
        if status_filter and status_filter.strip():
            if ticket.get("status", "").strip().lower() != status_filter.strip().lower():
                continue  
        
        # Filter by priority check
        if priority_filter and priority_filter.strip():
            if ticket.get("priority", "").strip().lower() != priority_filter.strip().lower():
                continue 
       
        filtered_results.append(ticket)
        
    return filtered_results

def sort_search_result(tickets: list):
    property_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    
    def sorting_key(ticket):
        priority_str = ticket.get("priority", "low").strip().lower()
        weight = property_order.get(priority_str, 1)

        raw_id = ticket.get("id", "0")
        num_id = 0
        clean_id_str = "".join(char for char in str(raw_id) if char.isdigit())
        if clean_id_str:
            num_id = int(clean_id_str)
        return (-weight, num_id)
    
    return sorted(tickets, key=sorting_key)
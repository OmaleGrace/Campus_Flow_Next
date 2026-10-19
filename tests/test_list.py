from campusflow.tickets import load_tickets
from campusflow.list_ticket import list_ticket

tickets_database=load_tickets()
tickets_database["T001"] = {"title": "Wi-Fi Issue"}
tickets_database["T002"] = {"title": "Broken Screen"}

print("--- RUNNING TEST: Listing Tickets ---")
print("Expected output: T001 and T002 should print below\n")
list_ticket()

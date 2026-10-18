from itertools import count
import json
import os

def load_tickets(path="database.json"):
    if not os.path.exists(path):
        return {}   
    with open(path, "r") as file:
        try:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
        except json.JSONDecodeError:
            print("File is corrupted, unreadable, or empty")
            return {}


def save_tickets(tickets_database, path="database.json"):
    with open(path, "w") as file:
        json.dump(tickets_database, file, indent=4)


def next_ticket_id(tickets_database):
    existing_numbers = []
    for ticket_id in tickets_database.keys():
        try:
            if ticket_id.startswith("T"):
                number = int(ticket_id[1:])
                existing_numbers.append(number)
        except ValueError:
            continue
    if existing_numbers:
        start_number = max(existing_numbers) + 1
    else:
        start_number = 1

    gen_id = count(start=start_number)
    return f"T{next(gen_id):03d}"


def validate_ticket_data(category, urgency, affected_users):
    CATEGORIES = ["Network", "Hardware", "Software", "Other"]
    URGENCIES = ["low", "medium", "high"]
    if category not in CATEGORIES:
        print(f"Invalid category. Must be one of: {CATEGORIES}")
        return
    if urgency not in URGENCIES:
        print(f"Invalid urgency level. Must be one of: {URGENCIES}")
        return
    while True:
        if not isinstance(affected_users, int):
            print("Affected users must be a whole number greater than zero.")

def calculate_priority(urgency, affected_users):
    high_urgency = (urgency == "high")
    if high_urgency and affected_users >= 10:
        return "critical"
    elif high_urgency or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def create_ticket(tickets_database, path="database.json"):
    id_number = next_ticket_id(tickets_database)
    print("Ticket_ID:",id_number)
    while True:
        title = input("Enter Title: ").strip()
        if not title:
            print("Title cannot be blank.")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return
        else:
            break 
    while True:
        CATEGORIES = ["Network", "Hardware", "Software", "Other"]
        print("Categories\n1.Network\n2.Hardware\n3.Software\n4.Other")
        category=input("choose category:").strip()
        if category=="1":
            print(CATEGORIES[0])
            category=CATEGORIES[0]
            break
        elif category=="2":
            print(CATEGORIES[1])
            category=CATEGORIES[1]
            break
        elif category=="3":
            print(CATEGORIES[2])
            category=CATEGORIES[2]
            break
        elif category=="4":
            print(CATEGORIES[3])
            category=CATEGORIES[3]
            break
        else:
            print(f"Invalid/emptycategory. Must be one of: {CATEGORIES}")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return
    while True:        
        URGENCIES = ["low", "medium", "high"]   
        print("urgency\n1.low\n2.medium\n3.high")
        urgency = input("Enter Urgency:").strip()
        if urgency=="1":
            print(URGENCIES[0])
            urgency=URGENCIES[0]
            break
        elif urgency=="2":
            print(URGENCIES[1])
            urgency=URGENCIES[1]
            break
        elif urgency=="3":
            print(URGENCIES[2])
            urgency=URGENCIES[2]
            break
        else:
            print(f"Invalid urgency level. Must be one of: {URGENCIES}")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return
    while True:    
        try:
            affected_users = int(input("Enter number of affected users: "))
            if affected_users <=0:
                print("Number of affected users cannot be negative or 0.")
                answer=input("continue? y/n:").lower()
                if answer=="y":
                    continue
                elif answer=="n":
                    return
        except ValueError:
            print("Please enter a valid integer for affected users.")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return
    validate_ticket_data(category, urgency, affected_users)
    priority_level = calculate_priority(urgency, affected_users)

    ticket_data = {
        "id": id_number.strip(),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority_level,
        "status": "Open",
        "assigned_to": None,
        "notes": []
    }
    tickets_database[id_number] = ticket_data
    save_tickets(tickets_database, path)
    return ticket_data


def can_transition(ticket, new_status):
    VALID_STATUSES = ["open", "in_progress", "resolved"]
    target_status = new_status.strip().lower()
    current_status = ticket["status"].strip().lower()

    if target_status not in VALID_STATUSES:
        print("Invalid status. Choose open, in_progress, or resolved.")

    if current_status not in VALID_STATUSES:
       print("The ticket has an invalid current status.")

    if current_status == target_status:
        raise ValueError(f"Ticket is already in {current_status} status.")

    if current_status == "open" and target_status == "in_progress":
        if not ticket["assigned_to"]:
            raise ValueError("Cannot start work on an unassigned ticket.")         
    elif current_status == "in_progress" and target_status == "resolved":
        pass   
    elif current_status == "resolved" and target_status == "open":
        pass  
    else:
        raise ValueError(f"Cannot change status from {current_status} to {target_status}.")
    return True

def next_note_id(ticket):
    start_number = len(ticket["notes"]) + 1
    note_counter = count(start=start_number)
    return f"N{next(note_counter):03d}"

def add_note(tickets_database, path="database.json"):
    while True:
        ticket_id = input("Enter Ticket ID to add note to (e.g., T001): ").strip().upper()
        if not ticket_id:
            print("Ticket ID cannot be blank.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return

        if ticket_id not in tickets_database:
            print(f"Ticket {ticket_id} not found.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        ticket = tickets_database[ticket_id]
        if ticket.get("status", "").lower() == "resolved":
            print("Cannot add notes to a Resolved ticket.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        break
    while True:
        author = input("Enter Note Author: ").strip()
        if not author:
            print("Note author cannot be blank.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        else:
            break
    while True:
        message = input("Enter Note Message: ").strip()
        if not message:
            print("Note message cannot be blank.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        elif len(message) < 5 or len(message) > 300:
            print("message can not be less than 5 characters or greater than 300 characters")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        else:
            break
    note_id = next_note_id(ticket).strip()
    note_record ={
           note_id:{
            "note_id": note_id,
            "author": author,
            "message": message,
        }
    } 
    ticket["notes"].append(note_record)
    save_tickets(tickets_database, path)
    print(f"Success: Note {note_id} added to Ticket {ticket_id}!")
    return ticket

def view_notes(tickets_database):
    while True:
        ticket_id = input("Enter Ticket ID to view notes (e.g., T001): ").strip().upper()
        if not ticket_id:
            print("Ticket ID cannot be blank.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return

        if ticket_id not in tickets_database:
            print(f"Ticket {ticket_id} not found.")
            answer = input("continue? y/n: ").lower()
            if answer=="y":
                continue
            elif answer=="n":
                return
        ticket = tickets_database[ticket_id]
        break

    notes_list = ticket.get("notes", [])

    print(f"\n================ NOTES FOR TICKET {ticket_id} ================")
    if not notes_list:
        print("No notes found for this ticket.")
        print("==================================================")
        return
    for note_wrapper in notes_list:
        for note_id, note_details in note_wrapper.items():
            print(f"Note ID: {note_id}")
            print(f"Author:  {note_details.get('author')}")
            print(f"Message: {note_details.get('message')}")
            print("-" * 50)         
    print("==================================================")


from itertools import count
import json
import os

def read_data():
    if os.path.exists("database.json"):
        with open("database.json", "r") as file:
            try:
                reload_data=json.load(file)
                print("Data successfully reloaded.")
                return reload_data
            except json.JSONDecodeError:
                return {}
    else:
        print("No data stored")
        return {}
tickets_database=read_data()
start_number = 1
existing_numbers = []
for ticket_id in tickets_database.keys():
    numbers=int(ticket_id[1:])
    existing_numbers.append(numbers)
if existing_numbers:
    start_number = max(existing_numbers) + 1
else:
    pass
gen_id=count(start=start_number)
def Create_ticket():
    category=""
    urgent=""
    categories=["Network", "Hardware","Software","Other"]
    urgency_levels=["low", "medium", "high"]
    id_number=f"T{next(gen_id):03d}"
    print("Ticket_ID:",id_number)
    while True:
        title_name=input("Enter Title:").strip()
        if title_name=="":
            print("title cannot be blank")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return     
        else:
            break
    while True:
        print("*Selcet Category*")
        print("1. Network")
        print("2. Hardware")
        print("3. Software")
        print("4. Other")
        category_name=input("choose category:")
        if category_name =="1":
            print(categories[0])
            category=categories[0]
            break
        elif category_name=="2":
            print(categories[1])
            category=categories[1]
            break
        elif category_name=="3":
            print(categories[2])
            category=categories[2]
            break
        elif category_name=="4":
            print(categories[3])
            category=categories[3]
            break
        else:
            print("invalid selection")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return 
    while True:
        print("*Selcet urgency level*")
        print("1. low")
        print("2. medium")
        print("3. high")
        urgency=input("select urgency level:")
        if urgency=="1":
            print(f"urgency:{urgency_levels[0]}")
            urgent=urgency_levels[0]
            break
        elif urgency=="2":
            print(f"urgency:{urgency_levels[1]}")
            urgent=urgency_levels[1]
            break
        elif urgency=="3":
            print(f"urgency:{urgency_levels[2]}")
            urgent=urgency_levels[2]
            break
        else:
            print("invalid selection")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return 
    while True:
        try:
            affected_users=int(input("how many users are affected:"))
            if affected_users <=0:
                print("number must be greater than zero")
                answer=input("continue? y/n:").lower()
                if answer=="y":
                    pass
                elif answer=="n":
                    return 
            else:
                break
        except ValueError:
            print("invalid number")
            answer=input("continue? y/n:").lower()
            if answer=="y":
                pass
            elif answer=="n":
                return  
    priority= urgency
    priorities=""
    if priority=="3" and affected_users >=10:
        print("priority:critical")
        priorities="critical"
    elif priority=="3" or affected_users >=10:
        print("priority:high")
        priorities="high"
    elif priority=="2" or affected_users >=3:
        print("priority:medium")
        priorities="medium"
    else:
        print("priority:low")
        priorities="low"
    status="Open"
    print(f"status:{status}")
    assigned_to=None
    print(f"assigned:{assigned_to}")
    result={
      "id":id_number,
    "title":title_name,
    "category":category,
    "urgency":urgent,
    "affected_users":affected_users,
    "priority":priorities,
    "status":status,
    "assigned_to":assigned_to,
    "notes":[]
    }
    tickets_database[id_number]=result
    with open("database.json", "w") as file:
        store_data= json.dump(tickets_database, file, indent=4)
    return store_data
    if store_data: 
        print("Data successfully saved")
    else:
        pass

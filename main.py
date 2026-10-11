from campusflow.tickets import create_ticket, calculate_priority
from campusflow.workflow import update_status, assign_ticket, get_work_queue
from campusflow.reports import generate_reports
from campusflow.storage import save_tickets, load_tickets

VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
VALID_URGENCIES = ["Low", "Medium", "High"]

def prompt_with_cancel(prompt_text):
    val = input(prompt_text).strip()
    if val.lower() in ["0", "back", "cancel"]:
        return None
    return val

def run_create_ticket(tickets):
    print("\n--- Create Ticket --- (Type '0' or 'cancel' at any time to return to menu)")
    
    title = prompt_with_cancel("Enter ticket title: ")
    if title is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    print(f"Categories: {', '.join(VALID_CATEGORIES)}")
    category_input = prompt_with_cancel("Enter category: ")
    if category_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return
    
    category = next((c for c in VALID_CATEGORIES if c.lower() == category_input.lower()), None)
    if not category:
        print(f"Invalid category '{category_input}'. Must be one of: {', '.join(VALID_CATEGORIES)}")
        return

    print(f"Urgency levels: {', '.join(VALID_URGENCIES)}")
    urgency_input = prompt_with_cancel("Enter urgency: ")
    if urgency_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    urgency = next((u for u in VALID_URGENCIES if u.lower() == urgency_input.lower()), None)
    if not urgency:
        print(f"Invalid urgency '{urgency_input}'. Must be one of: {', '.join(VALID_URGENCIES)}")
        return

    affected_input = prompt_with_cancel("Enter affected users (positive integer): ")
    if affected_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    try:
        affected_users = int(affected_input)
    except ValueError:
        print("Invalid number of affected users. Must be an integer.")
        return

    ticket = create_ticket(tickets, title, category, urgency, affected_users)
    save_tickets(tickets)
    print(f"--> Ticket #{ticket['id']} created successfully!")

def run_list_tickets(tickets):
    print("\n--- All Tickets ---")
    if not tickets:
        print("No tickets found.")
        return
    for t in tickets:
        print(f"[{t.get('id')}] {t.get('title')} | Category: {t.get('category')} | Urgency: {t.get('urgency')} | Status: {t.get('status')} | Assignee: {t.get('assignee', 'None')}")

def run_assign_ticket(tickets):
    print("\n--- Assign Ticket --- (Type '0' or 'cancel' to return)")
    ticket_id_input = prompt_with_cancel("Enter Ticket ID to assign: ")
    if ticket_id_input is None:
        print("--> Action cancelled.")
        return
    
    try:
        ticket_id = int(ticket_id_input)
    except ValueError:
        print("Invalid Ticket ID.")
        return

    assignee = prompt_with_cancel("Enter assignee name: ")
    if assignee is None:
        print("--> Action cancelled.")
        return

    try:
        assign_ticket(tickets, ticket_id, assignee)
        save_tickets(tickets)
        print(f"--> Ticket #{ticket_id} successfully assigned to {assignee}!")
    except Exception as e:
        print(f"--> Error assigning ticket: {e}")

def run_update_status(tickets):
    print("\n--- Update Ticket Status --- (Type '0' or 'cancel' to return)")
    ticket_id_input = prompt_with_cancel("Enter Ticket ID to update: ")
    if ticket_id_input is None:
        print("--> Action cancelled.")
        return
    
    try:
        ticket_id = int(ticket_id_input)
    except ValueError:
        print("Invalid Ticket ID.")
        return

    ticket = next((t for t in tickets if t.get('id') == ticket_id), None)
    if not ticket:
        print(f"--> Ticket #{ticket_id} not found.")
        return

    new_status = prompt_with_cancel("Enter new status (OPEN, IN_PROGRESS, RESOLVED, CLOSED): ")
    if new_status is None:
        print("--> Action cancelled.")
        return

    try:
        update_status(ticket, new_status.upper())
        save_tickets(tickets)
        print(f"--> Ticket #{ticket_id} status updated to {new_status.upper()}!")
    except Exception as e:
        print(f"--> Error updating status: {e}")

def main():
    tickets = load_tickets()
    
    while True:
        print("\n=== CampusFlow Helpdesk Menu ===")
        print("1. Create Ticket")
        print("2. List / View Tickets")
        print("3. Assign Ticket")
        print("4. Update Ticket Status (Workflow)")
        print("5. Show Work Queue")
        print("6. Show Reports & Statistics")
        print("7. Exit")
        print("8. Cancel / Return to Main Menu")

        choice = input("\nSelect an option (1-8): ").strip()

        if choice == "1":
            run_create_ticket(tickets)
        elif choice == "2":
            run_list_tickets(tickets)
        elif choice == "3":
            run_assign_ticket(tickets)
        elif choice == "4":
            run_update_status(tickets)
        elif choice == "5":
            queue = get_work_queue(tickets)
            print("\n--- Current Work Queue ---")
            for t in queue:
                print(t)
        elif choice == "6":
            generate_reports(tickets)
        elif choice == "7":
            print("Exiting CampusFlow. Goodbye!")
            break
        elif choice == "8":
            print("--> Returned to Main Menu.")
            continue
        else:
            print("Invalid selection. Please choose a number between 1 and 8.")

if __name__ == "__main__":
    main()

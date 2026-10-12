from campusflow.tickets import create_ticket, calculate_priority
from campusflow.workflow import update_status, assign_ticket, get_work_queue
from campusflow.reports import generate_reports
from campusflow.storage import save_tickets, load_tickets

VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
VALID_URGENCIES = ["low", "medium", "high"]
STORAGE_FILE = "tickets.json"

def prompt_with_cancel(prompt_text):
    val = input(prompt_text).strip()
    if val.lower() in ["0", "back", "cancel", "8"]:
        return None
    return val

def find_ticket_by_input(tickets, user_input):
    clean_input = user_input.strip().lower().replace("o", "0")
    for t in tickets:
        t_id = str(t.get('id', '')).strip().lower()
        t_digits = ''.join(filter(str.isdigit, t_id))
        input_digits = ''.join(filter(str.isdigit, clean_input))
        
        if (t_id == clean_input or 
            t_id.replace('t', '') == clean_input.replace('t', '') or 
            (t_digits and input_digits and int(t_digits) == int(input_digits))):
            return t
    return None

def run_create_ticket(tickets):
    print("\n--- Create Ticket --- (Type '0' or 'cancel' to return to menu)")
    
    title = prompt_with_cancel("Enter ticket title: ")
    if title is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    print(f"Categories: {', '.join(VALID_CATEGORIES)}")
    category_input = prompt_with_cancel("Enter category (Network, Hardware, Software, Other): ")
    if category_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return
    
    category = next((c for c in VALID_CATEGORIES if c.lower() == category_input.lower()), None)
    if not category:
        print(f"Invalid category '{category_input}'. Must be one of: {', '.join(VALID_CATEGORIES)}")
        return

    print("Urgency levels: low, medium, high")
    urgency_input = prompt_with_cancel("Enter urgency (low, medium, high): ")
    if urgency_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    urgency = next((u for u in VALID_URGENCIES if u.lower() == urgency_input.lower()), None)
    if not urgency:
        print(f"Invalid urgency '{urgency_input}'. Must be one of: low, medium, high")
        return

    affected_input = prompt_with_cancel("Number of affected users: ")
    if affected_input is None:
        print("--> Action cancelled. Returning to main menu.")
        return

    try:
        affected_users = int(affected_input)
    except ValueError:
        print("Invalid number of affected users. Must be an integer.")
        return

    try:
        ticket = create_ticket(title, category, urgency, affected_users, tickets)
        tickets.append(ticket)
        save_tickets(STORAGE_FILE, tickets)
        print(f"Ticket created! ID: {ticket['id']}")
        print(f"Priority: {ticket['priority']}")
    except ValueError as e:
        print(f"Validation Error: {e}")

def run_list_tickets(tickets):
    print("\n--------------------")
    if not tickets:
        print("No tickets found.")
        return
    for t in tickets:
        print(f"id: {t.get('id')}")
        print(f"title: {t.get('title')}")
        print(f"category: {t.get('category')}")
        print(f"urgency: {t.get('urgency')}")
        print(f"affected_users: {t.get('affected_users')}")
        print(f"priority: {t.get('priority')}")
        print(f"status: {t.get('status')}")
        print(f"assigned_to: {t.get('assigned_to') or t.get('assignee', 'None')}")
        print("--------------------")

def run_assign_ticket(tickets):
    print("\n--- Assign Ticket --- (Type '0' or 'cancel' to return)")
    ticket_id_input = prompt_with_cancel("Enter ticket ID (e.g. T001, t001, or 1): ")
    if ticket_id_input is None:
        print("--> Action cancelled.")
        return
    
    ticket = find_ticket_by_input(tickets, ticket_id_input)
    if not ticket:
        print(f"Error: Ticket ID '{ticket_id_input}' not found.")
        return

    staff_name = prompt_with_cancel("Enter staff name: ")
    if staff_name is None:
        print("--> Action cancelled.")
        return

    try:
        assign_ticket(tickets, ticket['id'], staff_name)
        save_tickets(STORAGE_FILE, tickets)
        print(f"--> Ticket #{ticket['id']} successfully assigned to {staff_name}!")
    except Exception as e:
        print(f"Error assigning ticket: {e}")

def run_update_status(tickets):
    print("\n--- Update Ticket Status --- (Type '0' or 'cancel' to return)")
    ticket_id_input = prompt_with_cancel("Enter ticket ID (e.g. T001, t001, or 1): ")
    if ticket_id_input is None:
        print("--> Action cancelled.")
        return
    
    ticket = find_ticket_by_input(tickets, ticket_id_input)
    if not ticket:
        print(f"Error: Ticket ID '{ticket_id_input}' not found.")
        return

    new_status_input = prompt_with_cancel("Enter new status (open, in_progress, resolved): ")
    if new_status_input is None:
        print("--> Action cancelled.")
        return

    normalized_status = new_status_input.lower().replace(" ", "_")

    try:
        update_status(ticket, normalized_status)
        save_tickets(STORAGE_FILE, tickets)
        print(f"--> Ticket #{ticket['id']} status updated to {normalized_status}!")
    except Exception as e:
        print(f"Error updating status: {e}")

def run_generate_reports(tickets):
    report = generate_reports(tickets)
    print("\n==============================")
    print("      CampusFlow Report       ")
    print("==============================")
    print(f"Total Tickets: {report.get('total', 0)}")
    
    print("\nStatus Breakdown:")
    for status, count in report.get('status_breakdown', {}).items():
        print(f"  - {status.capitalize()}: {count}")
        
    print("\nPriority Breakdown:")
    for priority, count in report.get('priority_breakdown', {}).items():
        print(f"  - {priority.capitalize()}: {count}")
    print("==============================")

def main():
    try:
        tickets = load_tickets(STORAGE_FILE) or []
    except Exception:
        tickets = []
    
    while True:
        print("\n===== CampusFlow =====")
        print("1. Create ticket")
        print("2. View all tickets")
        print("3. Assign ticket")
        print("4. Update ticket status")
        print("5. View work queue")
        print("6. Generate report")
        print("7. Exit")
        print("8. Return to Main Menu / Cancel")

        choice = input("Choose an option (1-8): ").strip().lower()

        if choice in ["1", "create ticket"]:
            run_create_ticket(tickets)
        elif choice in ["2", "view all tickets", "list"]:
            run_list_tickets(tickets)
        elif choice in ["3", "assign ticket"]:
            run_assign_ticket(tickets)
        elif choice in ["4", "update ticket status"]:
            run_update_status(tickets)
        elif choice in ["5", "view work queue"]:
            queue = get_work_queue(tickets)
            print("\n--- Current Work Queue ---")
            for t in queue:
                print(f"[{t.get('id')}] {t.get('title')} - Priority: {t.get('priority')}")
        elif choice in ["6", "generate report"]:
            run_generate_reports(tickets)
        elif choice in ["7", "exit"]:
            print("Exiting CampusFlow. Goodbye!")
            break
        elif choice in ["8", "return", "cancel"]:
            print("--> Returned to Main Menu.")
            continue
        else:
            print("Invalid selection. Please choose a number between 1 and 8.")

if __name__ == "__main__":
    main()

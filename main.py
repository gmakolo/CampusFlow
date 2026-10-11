import os
from campusflow.storage import save_tickets, load_tickets
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports

DATA_FILE = "data/tickets.json"

def print_menu():
    print("\n=== CampusFlow Helpdesk Menu ===")
    print("1. Create Ticket")
    print("2. List / View Tickets")
    print("3. Assign Ticket")
    print("4. Update Ticket Status (Workflow)")
    print("5. Show Work Queue")
    print("6. Show Reports & Statistics")
    print("7. Exit")

def main():
    tickets = load_tickets(DATA_FILE)
    
    while True:
        print_menu()
        choice = input("\nSelect an option (1-7): ").strip()
        
        try:
            if choice == "1":
                # Basic creation stub or integration with Engineer A's code
                print("\n[Create Ticket]")
                title = input("Enter ticket title: ").strip()
                if not title:
                    print("Error: Title cannot be blank.")
                    continue
                
                print("Categories: Network, Hardware, Software, Other")
                category = input("Enter category: ").strip()
                
                print("Urgency levels: low, medium, high")
                urgency = input("Enter urgency: ").strip().lower()
                
                try:
                    affected_users = int(input("Enter affected users (positive integer): ").strip())
                except ValueError:
                    print("Error: Affected users must be a valid integer.")
                    continue
                
                # Simple priority calculation engine
                if urgency == "high" and affected_users >= 10:
                    priority = "critical"
                elif urgency == "high" or affected_users >= 10:
                    priority = "high"
                elif urgency == "medium" or affected_users >= 3:
                    priority = "medium"
                else:
                    priority = "low"
                
                # Generate unique ID
                next_num = len(tickets) + 1
                ticket_id = f"T{next_num:03d}"
                # Ensure unique ID check if items were deleted/reloaded
                while any(t["id"] == ticket_id for t in tickets):
                    next_num += 1
                    ticket_id = f"T{next_num:03d}"
                
                new_ticket = {
                    "id": ticket_id,
                    "title": title,
                    "category": category,
                    "urgency": urgency,
                    "affected_users": affected_users,
                    "priority": priority,
                    "status": "open",
                    "assigned_to": None
                }
                tickets.append(new_ticket)
                save_tickets(DATA_FILE, tickets)
                print(f"Success! Created ticket {ticket_id} with priority '{priority}'.")

            elif choice == "2":
                print("\n[All Tickets]")
                if not tickets:
                    print("No tickets found.")
                for t in tickets:
                    print(f"ID: {t['id']} | Title: {t['title']} | Priority: {t['priority']} | Status: {t['status']} | Assigned: {t.get('assigned_to') or 'Unassigned'}")

            elif choice == "3":
                print("\n[Assign Ticket]")
                tid = input("Enter Ticket ID (e.g. T001): ").strip()
                staff = input("Enter staff member name: ").strip()
                assign_ticket(tickets, tid, staff)
                save_tickets(DATA_FILE, tickets)
                print(f"Ticket {tid} successfully assigned to {staff}.")

            elif choice == "4":
                print("\n[Update Status Workflow]")
                tid = input("Enter Ticket ID (e.g. T001): ").strip()
                target_ticket = None
                for t in tickets:
                    if t["id"] == tid:
                        target_ticket = t
                        break
                if not target_ticket:
                    print(f"Error: Ticket ID {tid} not found.")
                    continue
                
                print(f"Current status: {target_ticket['status']}")
                print("Allowed transitions depend on rules (open -> in_progress -> resolved; reopen to open).")
                new_status = input("Enter new status (open, in_progress, resolved): ").strip().lower()
                update_status(target_ticket, new_status)
                save_tickets(DATA_FILE, tickets)
                print(f"Ticket {tid} status updated to '{new_status}'.")

            elif choice == "5":
                print("\n[Sorted Work Queue]")
                queue = get_work_queue(tickets)
                if not queue:
                    print("No active tickets in queue.")
                for t in queue:
                    print(f"ID: {t['id']} | Priority: {t['priority']} | Status: {t['status']} | Title: {t['title']}")

            elif choice == "6":
                print("\n[Reports & Statistics]")
                rep = generate_reports(tickets)
                print(f"Total Tickets: {rep['total']}")
                print("Status Breakdown:", rep['status_breakdown'])
                print("Priority Breakdown:", rep['priority_breakdown'])

            elif choice == "7":
                print("\nExiting CampusFlow. Goodbye!")
                break
            else:
                print("Invalid choice. Please select between 1 and 7.")
                
        except (ValueError, Exception) as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports
from campusflow.storage import load_tickets, save_tickets


tickets = []
STORAGE_FILE = "tickets.json"


def show_menu():
    print("\n===== CampusFlow =====")
    print("1. Create ticket")
    print("2. View all tickets")
    print("3. Assign ticket")
    print("4. Update ticket status")
    print("5. View work queue")
    print("6. Generate report")
    print("7. Exit")
    print("8. Return to menu")


def find_ticket(ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None


def save_changes():
    try:
        save_tickets(tickets, STORAGE_FILE)
        return True
    except (OSError, ValueError) as error:
        print(f"Warning: Could not save tickets: {error}")
        return False


def create_new_ticket():
    try:
        title = input("Enter ticket title: ")
        category = input(
            "Enter category (Network, Hardware, Software, Other): "
        ).strip().title()
        urgency = input(
            "Enter urgency (low, medium, high): "
        ).strip().lower()
        affected_users = int(input("Number of affected users: "))

        ticket = create_ticket(
            title, category, urgency, affected_users, tickets
        )
        tickets.append(ticket)

        if not save_changes():
            tickets.pop()
            print("Ticket creation cancelled because it could not be saved.")
            return

        print(f"Ticket created! ID: {ticket['id']}")
        print(f"Priority: {ticket['priority']}")

    except ValueError as error:
        print(f"Error: {error}")


def view_tickets():
    if not tickets:
        print("No tickets created yet.")
        return

    for ticket in tickets:
        print("\n--------------------")
        for key, value in ticket.items():
            print(f"{key}: {value}")


def assign_existing_ticket():
    ticket_id = input("Enter ticket ID: ").strip()
    staff_name = input("Enter staff name: ")
    ticket = find_ticket(ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    old_assignee = ticket["assigned_to"]

    try:
        assign_ticket(tickets, ticket_id, staff_name)

        if not save_changes():
            ticket["assigned_to"] = old_assignee
            return

        print("Ticket assigned successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def update_existing_ticket():
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    print("Statuses: open, in_progress, resolved")
    status = input("Enter new status: ").strip().lower()
    old_status = ticket["status"]

    try:
        update_status(ticket, status)

        if not save_changes():
            ticket["status"] = old_status
            return

        print("Ticket status updated successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def view_work_queue():
    queue = get_work_queue(tickets)

    if not queue:
        print("No tickets in the work queue.")
        return

    print("\n===== Work Queue =====")
    for ticket in queue:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']}"
        )


def view_report():
    report = generate_reports(tickets)

    print("\n===== CampusFlow Report =====")
    for key, value in report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")


def main():
    try:
        load_tickets(STORAGE_FILE, tickets)
        print(f"Loaded {len(tickets)} saved ticket(s).")
    except ValueError as error:
        print(f"Could not load saved tickets: {error}")
        print("Please fix the JSON file before continuing.")
        return

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            create_new_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            assign_existing_ticket()
        elif choice == "4":
            update_existing_ticket()
        elif choice == "5":
            view_work_queue()
        elif choice == "6":
            view_report()
        elif choice == "7":
            print("Thank you for using CampusFlow!")
            break
        elif choice == "8":
            print("Returning to the main menu...")
        else:
            print("Invalid choice. Choose a number from 1 to 8.")


if __name__ == "__main__":
    main()

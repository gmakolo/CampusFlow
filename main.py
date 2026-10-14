"""CampusFlow Next Engineer B CLI, preserving the shared repository's APIs.

AI-assisted implementation for miikese; A-owned modules are not replaced.
"""

import argparse
from pathlib import Path
import re

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports
from campusflow.search import CATEGORIES, PRIORITIES, STATUSES, normalize_filter, search_tickets, sort_search_results
from campusflow.integration import integration_api
from campusflow.understanding_check import run_understanding_check


tickets = []
MENU = """
===== CampusFlow Next =====
 1. Create ticket                 9. Reopen resolved ticket
 2. View all tickets            10. Add Follow-up Note
 3. Assign ticket               11. View Ticket Notes
 4. Update ticket status        12. Engineering Understanding Check
 5. Open Work Queue             13. Save JSON (Engineer A API)
 6. Generate report             14. Load JSON (Engineer A API)
 7. Exit                        15. View ticket details
 8. Search Tickets              16. Search sorted by priority
"""


def show_menu():
    print(MENU)


def find_ticket(ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id.strip().upper():
            return ticket
    raise ValueError(f"Unknown ticket ID: {ticket_id.strip().upper()}.")


def ask_choice(prompt, choices, label, optional=False):
    while True:
        try:
            value = normalize_filter(input(prompt), choices, label)
            if value or optional:
                return value
            print(f"{label} cannot be blank.")
        except ValueError as error:
            print(f"Error: {error}")


def ask_nonblank(prompt, label):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{label} cannot be blank.")


def ask_count():
    while True:
        value = input("Number of affected users (positive integer): ").strip()
        if re.fullmatch(r"[0-9]+", value) and int(value) > 0:
            return int(value)
        print("Affected users must be a positive whole number, not text or decimals.")


def display_records(records, empty_message="No tickets found."):
    if not records:
        print(empty_message)
        return
    print("Ticket ID | Title | Category | Priority | Status | Assigned Staff")
    for ticket in records:
        print(f"{ticket['id']} | {ticket['title']} | {ticket.get('category', 'Other')} | "
              f"{ticket['priority']} | {ticket['status']} | {ticket.get('assigned_to') or 'Unassigned'}")


def create_new_ticket():
    title = ask_nonblank("Enter ticket title: ", "Title")
    category = ask_choice("Category (Network/Hardware/Software/Other): ", CATEGORIES, "Category")
    urgency = ask_choice("Urgency (low/medium/high): ", ("low", "medium", "high"), "Urgency")
    affected_users = ask_count()
    # Shared creation returns a record; it does not append, unlike the old personal repo.
    ticket = create_ticket(title, category, urgency, affected_users, tickets)
    tickets.append(ticket)
    print(f"Ticket created! ID: {ticket['id']} | Priority: {ticket['priority']}")
    return True


def view_tickets():
    display_records(tickets, "No tickets created yet.")


def assign_existing_ticket():
    ticket = find_ticket(input("Enter ticket ID: "))
    if ticket["status"] == "resolved":
        raise ValueError("Reopen this resolved ticket with option 9 before changing its assignment.")
    staff = ask_nonblank("Enter staff name: ", "Staff name")
    assign_ticket(tickets, ticket["id"], staff)
    print("Ticket assigned successfully.")
    return True


def update_existing_ticket():
    ticket = find_ticket(input("Enter ticket ID: "))
    allowed = {"open": "in_progress", "in_progress": "resolved"}
    if ticket["status"] not in allowed:
        raise ValueError("Use option 9 to explicitly reopen a resolved ticket.")
    next_status = allowed[ticket["status"]]
    status = ask_choice(f"Next status ({next_status}): ", (next_status,), "Next status")
    update_status(ticket, status)
    print(f"Ticket {ticket['id']} is now {ticket['status']}.")
    return True


def reopen_existing_ticket():
    ticket = find_ticket(input("Resolved ticket ID: "))
    if ticket["status"] != "resolved":
        raise ValueError("Only a resolved ticket can be reopened.")
    # This is the shared baseline's existing reopening API, not a replacement backend.
    update_status(ticket, "open")
    print(f"Reopened {ticket['id']}; status is open.")
    return True


def view_work_queue():
    # Defensive B-side display filter; A's get_work_queue defect remains documented.
    queue = [ticket for ticket in get_work_queue(tickets) if ticket["status"] == "open"]
    print("\n===== Open Work Queue =====")
    display_records(queue, "No open tickets in the work queue.")


def view_report():
    report = generate_reports(tickets)
    print("\n===== CampusFlow Quality Insights =====")
    print(f"Total tickets: {report['total']}")
    for heading, key in (("Status", "status_breakdown"), ("Priority", "priority_breakdown"), ("Category", "category_breakdown")):
        print(f"{heading}:")
        for label, count in report[key].items():
            print(f"  {label}: {count}")
    print(f"Unresolved total: {report['unresolved']}")
    print(f"Resolved total: {report['resolved']}")
    print(f"Resolution percentage: {report['resolution_percentage']:.1f}%")


def search_existing_tickets(sorted_results=False):
    title = input("Title contains (blank for any): ")
    category = ask_choice("Category (blank for any): ", CATEGORIES, "Category", optional=True)
    status = ask_choice("Status (blank for any): ", STATUSES, "Status", optional=True)
    priority = ask_choice("Priority (blank for any): ", PRIORITIES, "Priority", optional=True)
    result = search_tickets(tickets, title, category, status, priority)
    if sorted_results:
        result = sort_search_results(result)
    display_records(result, "No tickets match all supplied filters. Try fewer or different filters.")


def add_follow_up_note():
    ticket = find_ticket(input("Enter ticket ID: "))
    if ticket["status"] == "resolved":
        raise ValueError("Resolved ticket must be reopened before adding a note.")
    api = integration_api("notes", "add_note")
    author = ask_nonblank("Note author: ", "Author")
    message = input("Note message (5–300 characters after trimming): ")
    note = api(tickets, ticket["id"], author, message)
    print(f"Added note {note['note_id']} to {ticket['id']}.")
    return True


def view_ticket_notes():
    ticket = find_ticket(input("Enter ticket ID: "))
    notes = integration_api("notes", "get_notes")(tickets, ticket["id"])
    if not notes:
        print(f"No follow-up notes for {ticket['id']}.")
        return
    # Ordering is a display concern; note creation/validation remains Engineer A's API.
    for note in sorted(notes, key=lambda item: int(item["note_id"][1:])):
        print(f"{note['note_id']} | {note['author']} | {note['message']}")


def view_ticket_details():
    ticket = find_ticket(input("Enter ticket ID: "))
    display_records([ticket])
    print(f"Urgency: {ticket['urgency']} | Affected users: {ticket['affected_users']}")


def save_records(path=None):
    api = integration_api("storage", "save_tickets")
    if path is None:
        path = Path(ask_nonblank("JSON path: ", "Path"))
    api(tickets, path)
    print(f"Saved {len(tickets)} ticket(s) to {path}.")
    return path


def load_records(path=None):
    api = integration_api("storage", "load_tickets")
    if path is None:
        path = Path(ask_nonblank("JSON path: ", "Path"))
    loaded = api(path)
    # A must parse and validate the complete collection before returning it.
    tickets[:] = loaded
    print(f"Loaded {len(tickets)} ticket(s) from {path}.")
    return path


def run_menu(records=None, data_path=None):
    global tickets
    tickets = [] if records is None else records
    if data_path is not None:
        try:
            load_records(data_path)
        except ValueError as error:
            print(f"Startup stopped: {error}")
            return 1
    else:
        print("In-memory session. Notes and JSON require Engineer A's pending APIs.")
    actions = {"1": create_new_ticket, "2": view_tickets, "3": assign_existing_ticket,
               "4": update_existing_ticket, "5": view_work_queue, "6": view_report,
               "8": search_existing_tickets, "9": reopen_existing_ticket,
               "10": add_follow_up_note, "11": view_ticket_notes,
               "12": run_understanding_check, "15": view_ticket_details,
               "16": lambda: search_existing_tickets(sorted_results=True)}
    dirty = False
    while True:
        show_menu()
        try:
            choice = input("Choose an option (1–16; 7 to exit): ").strip()
            if choice in ("0", "7"):
                if dirty and data_path is not None:
                    save_records(data_path)
                elif dirty:
                    print("In-memory records were not saved; JSON integration is pending.")
                print("Thank you for using CampusFlow!")
                return 0
            if choice == "13":
                data_path = save_records(data_path)
                dirty = False
            elif choice == "14":
                if dirty:
                    confirm = ask_choice("Replace unsaved in-memory tickets? (yes/no): ", ("yes", "no"), "Confirmation")
                    if confirm == "no":
                        print("Load cancelled; in-memory records preserved.")
                        continue
                data_path = load_records(data_path)
                dirty = False
            elif choice in actions:
                if actions[choice]() is True:
                    dirty = True
            else:
                print("Invalid choice. Choose 1–16, or 7 to exit.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended.")
            if dirty and data_path is not None:
                try:
                    save_records(data_path)
                except ValueError as error:
                    print(f"Error: {error} Unsaved changes could not be written.")
                    return 1
            elif dirty:
                print("In-memory records were not saved; JSON integration is pending.")
            print("Goodbye.")
            return 0
        except ValueError as error:
            print(f"Error: {error}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="CampusFlow Next Engineer B CLI")
    parser.add_argument("--data", type=Path, help="A-validated JSON file; requires Engineer A's storage module")
    parser.add_argument("--demo", action="store_true", help="Run the Engineer B demonstration without writing ticket files")
    args = parser.parse_args(argv)
    if args.demo:
        from campusflow.demo import run_demo
        return run_demo()
    return run_menu(data_path=args.data)


if __name__ == "__main__":
    raise SystemExit(main())

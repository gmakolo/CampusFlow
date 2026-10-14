import json
from pathlib import Path

from campusflow.tickets import validate_ticket, calculate_priority


def validate_tickets(tickets):
    """Validate the complete ticket collection before saving or loading."""
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a list.")

    seen_ticket_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a dictionary.")

        required = {
            "id", "title", "category", "urgency",
            "affected_users", "priority", "status",
            "assigned_to", "notes",
        }

        if not required.issubset(ticket):
            raise ValueError("A ticket is missing required fields.")

        ticket_id = ticket["id"]

        if (
            not isinstance(ticket_id, str)
            or len(ticket_id) < 2
            or not ticket_id.startswith("T")
            or not ticket_id[1:].isdigit()
        ):
            raise ValueError("Invalid ticket ID.")

        if ticket_id in seen_ticket_ids:
            raise ValueError("Duplicate ticket ID.")

        seen_ticket_ids.add(ticket_id)

        validate_ticket(
            ticket["title"],
            ticket["category"],
            ticket["urgency"],
            ticket["affected_users"],
        )

        expected_priority = calculate_priority(
            ticket["urgency"],
            ticket["affected_users"],
        )

        if ticket["priority"] != expected_priority:
            raise ValueError("Ticket priority does not match its details.")

        if ticket["status"] not in ("open", "in_progress", "resolved"):
            raise ValueError("Invalid ticket status.")

        assigned_to = ticket["assigned_to"]
        if assigned_to is not None and (
            not isinstance(assigned_to, str) or not assigned_to.strip()
        ):
            raise ValueError("Invalid assigned staff name.")

        notes = ticket["notes"]
        if not isinstance(notes, list):
            raise ValueError("Ticket notes must be a list.")

        seen_note_ids = set()

        for note in notes:
            if not isinstance(note, dict):
                raise ValueError("Each note must be a dictionary.")

            if not {"note_id", "author", "message"}.issubset(note):
                raise ValueError("A note is missing required fields.")

            note_id = note["note_id"]
            author = note["author"]
            message = note["message"]

            if (
                not isinstance(note_id, str)
                or len(note_id) < 2
                or not note_id.startswith("N")
                or not note_id[1:].isdigit()
            ):
                raise ValueError("Invalid note ID.")

            if note_id in seen_note_ids:
                raise ValueError("Duplicate note ID.")

            seen_note_ids.add(note_id)

            if not isinstance(author, str) or not author.strip():
                raise ValueError("Invalid note author.")

            if (
                not isinstance(message, str)
                or not 5 <= len(message.strip()) <= 300
            ):
                raise ValueError("Invalid note message.")


def save_tickets(tickets, filename="tickets.json"):
    """Validate and save tickets as JSON."""
    validate_tickets(tickets)

    path = Path(filename)
    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(filename="tickets.json", current_tickets=None):
    """Load tickets only after validating the complete JSON collection."""
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded_tickets = json.load(file)

        validate_tickets(loaded_tickets)

    except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
        raise ValueError(f"Could not load tickets: {error}") from error

    if current_tickets is not None:
        current_tickets.clear()
        current_tickets.extend(loaded_tickets)
        return current_tickets

    return loaded_tickets

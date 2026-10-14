def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_ticket(title, category, urgency, affected_users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be empty")

    if category not in ["Network", "Hardware", "Software", "Other"]:
        raise ValueError("Invalid category")

    if urgency not in ["low", "medium", "high"]:
        raise ValueError("Invalid urgency")

    if (
        type(affected_users) is not int
        or affected_users <= 0
    ):
        raise ValueError("Affected users must be a positive integer")

    return True


def generate_ticket_id(existing_tickets=None):
    existing_tickets = existing_tickets or []
    highest_number = 0

    for ticket in existing_tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            try:
                number = int(ticket_id[1:])
                highest_number = max(highest_number, number)
            except ValueError:
                pass

    return f"T{highest_number + 1:03d}"


def create_ticket(
    title, category, urgency, affected_users, existing_tickets=None
):
    validate_ticket(title, category, urgency, affected_users)

    existing_tickets = existing_tickets or []

    return {
        "id": generate_ticket_id(existing_tickets),
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }


def add_note(tickets, ticket_id, author, message):
    """Add a validated note to an open or in-progress ticket."""
    ticket = next(
        (item for item in tickets if item.get("id") == ticket_id),
        None,
    )

    if ticket is None:
        raise ValueError(f"Ticket ID {ticket_id} not found.")

    if ticket.get("status") not in ("open", "in_progress"):
        raise ValueError("Cannot add notes to a resolved ticket.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Author cannot be empty.")

    if not isinstance(message, str):
        raise ValueError("Message must be text.")

    message = message.strip()
    if not 5 <= len(message) <= 300:
        raise ValueError("Message must be between 5 and 300 characters.")

    notes = ticket.setdefault("notes", [])
    highest_number = 0

    for note in notes:
        note_id = note.get("note_id", "")
        if isinstance(note_id, str) and note_id.startswith("N"):
            number_text = note_id[1:]
            if number_text.isdigit():
                highest_number = max(highest_number, int(number_text))

    new_note = {
        "note_id": f"N{highest_number + 1:03d}",
        "author": author.strip(),
        "message": message,
    }

    notes.append(new_note)
    return new_note

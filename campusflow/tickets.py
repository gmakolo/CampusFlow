
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
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
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
    }

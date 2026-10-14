def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a valid staff member."""
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] == "resolved":
                raise ValueError("Reopen the ticket before assigning it.")

            ticket["assigned_to"] = staff_name.strip()
            return True

    raise ValueError(f"Ticket ID {ticket_id} not found.")


def update_status(ticket, new_status):
    """Validate ticket status transitions before updating."""
    valid_statuses = ["open", "in_progress", "resolved"]

    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status: {new_status}")

    current_status = ticket["status"]

    if current_status == "open":
        if new_status == "resolved":
            raise ValueError("An open ticket must be in progress before resolving.")

        if new_status == "in_progress" and not ticket.get("assigned_to"):
            raise ValueError("Cannot move an unassigned ticket to in_progress.")

    elif current_status == "in_progress":
        if new_status == "open":
            raise ValueError("Reopen is only allowed from resolved status.")

    elif current_status == "resolved":
        if new_status != "open":
            raise ValueError("Resolved tickets can only be reopened.")

    ticket["status"] = new_status
    return True


def get_work_queue(tickets):
    """Return only open tickets, sorted by priority and numeric ID."""
    priority_weight = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    def sort_key(ticket):
        priority = priority_weight.get(ticket.get("priority", "low"), 1)
        ticket_id = ticket.get("id", "")

        number = (
            int(ticket_id[1:])
            if ticket_id.startswith("T") and ticket_id[1:].isdigit()
            else 0
        )

        return (-priority, number)

    return sorted(open_tickets, key=sort_key)

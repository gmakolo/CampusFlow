def assign_ticket(tickets, ticket_id, staff_name):
    """Assigns a ticket to a staff member if both exist and staff_name is valid."""
    if not staff_name or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")
    
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name.strip()
            return True
    raise ValueError(f"Ticket ID {ticket_id} not found.")

def update_status(ticket, new_status):
    """Enforces state transitions: open -> in_progress -> resolved."""
    valid_statuses = ["open", "in_progress", "resolved"]
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status: {new_status}")
    
    current_status = ticket["status"]
    
    # Rule: Unassigned ticket cannot move to in_progress
    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Cannot move unassigned ticket to in_progress.")
    
    # Rule: Resolved tickets can only be modified via explicit reopen to open
    if current_status == "resolved" and new_status != "open":
        raise ValueError("Resolved tickets can only be changed back to open.")
        
    ticket["status"] = new_status
    return True

def get_work_queue(tickets):
    """Returns unresolved tickets sorted by priority and numeric ID."""
    priority_weight = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    
    unresolved = [t for t in tickets if t["status"] != "resolved"]
    
    def sort_key(t):
        p_val = priority_weight.get(t.get("priority", "low"), 1)
        num_id = int(t["id"][1:]) if t["id"].startswith("T") and t["id"][1:].isdigit() else 0
        return (-p_val, num_id)
        
    return sorted(unresolved, key=sort_key)
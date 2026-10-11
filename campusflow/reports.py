def generate_reports(tickets):
    """Returns total tickets and breakdowns by status and priority."""
    total = len(tickets)
    status_counts = {"open": 0, "in_progress": 0, "resolved": 0}
    priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    
    for t in tickets:
        s = t.get("status", "open")
        p = t.get("priority", "low")
        if s in status_counts:
            status_counts[s] += 1
        if p in priority_counts:
            priority_counts[p] += 1
            
    return {
        "total": total,
        "status_breakdown": status_counts,
        "priority_breakdown": priority_counts
    }
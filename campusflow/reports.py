"""Engineer B: testable current-state analytics, retaining original report keys."""

from .search import CATEGORIES, PRIORITIES, STATUSES


def generate_reports(tickets):
    """Count each record exactly once per dimension; an empty report is 0%.

    Legacy sparse workflow fixtures omit category. They are counted as Other,
    preserving the original API; real created records always contain category.
    Explicit invalid categories/statuses/priorities are rejected, not discarded.
    """
    status_counts = dict.fromkeys(STATUSES, 0)
    priority_counts = dict.fromkeys(PRIORITIES, 0)
    category_counts = dict.fromkeys(CATEGORIES, 0)
    for ticket in tickets:
        status = ticket.get("status", "open")
        priority = ticket.get("priority", "low")
        category = ticket.get("category", "Other")
        for field, value, counts in (
            ("status", status, status_counts),
            ("priority", priority, priority_counts),
            ("category", category, category_counts),
        ):
            if value not in counts:
                raise ValueError(f"Invalid {field} in report: {value!r}.")
            counts[value] += 1
    total = len(tickets)
    resolved = status_counts["resolved"]
    return {
        "total": total,
        "status_breakdown": status_counts,
        "priority_breakdown": priority_counts,
        "category_breakdown": category_counts,
        "unresolved": status_counts["open"] + status_counts["in_progress"],
        "resolved": resolved,
        "resolution_percentage": resolved / total * 100 if total else 0.0,
    }

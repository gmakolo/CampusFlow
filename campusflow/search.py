"""Engineer B: pure title search and combined optional filters.

AI-assisted implementation prepared for miikese's review and explanation.
"""

from copy import deepcopy

CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def normalize_filter(value, choices, label):
    """A blank filter is unrestricted; a supplied choice must be valid."""
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text.")
    value = value.strip()
    if not value:
        return ""
    for choice in choices:
        if value.casefold() == choice.casefold():
            return choice
    raise ValueError(f"{label} must be one of: {', '.join(choices)}; or blank.")


def search_tickets(tickets, title="", category="", status="", priority=""):
    """Return independent results matching ALL nonempty filters, in input order."""
    if title is None:
        title = ""
    if not isinstance(title, str):
        raise ValueError("Title search must be text.")
    needle = title.strip().casefold()
    category = normalize_filter(category, CATEGORIES, "Category")
    status = normalize_filter(status, STATUSES, "Status")
    priority = normalize_filter(priority, PRIORITIES, "Priority")
    matches = [
        ticket for ticket in tickets
        if (not needle or needle in ticket["title"].casefold())
        and (not category or ticket["category"] == category)
        and (not status or ticket["status"] == status)
        and (not priority or ticket["priority"] == priority)
    ]
    # Deep copies also protect nested notes from edits made to a search result.
    return deepcopy(matches)


def sort_search_results(results):
    """Optional result ordering; never changes the original Open Work Queue."""
    ranks = {label: index for index, label in enumerate(PRIORITIES)}
    return deepcopy(sorted(results, key=lambda t: (ranks[t["priority"]], int(t["id"][1:]))))

"""Read-only Engineer B demonstration using clearly fictional in-memory tickets."""
from .tickets import create_ticket
from .search import search_tickets, sort_search_results
from .reports import generate_reports
from .integration import integration_api, IntegrationPendingError


def run_demo():
    records = []
    for title, category, urgency, users in (
        ("WiFi outage in Demo Lab", "Network", "high", 12),
        ("WiFi slow in Practice Room", "Network", "medium", 4),
        ("Demo laptop screen", "Hardware", "low", 1),
    ):
        records.append(create_ticket(title, category, urgency, users, records))
    print("CampusFlow Next — Engineer B demo (fictional, in memory)")
    result = search_tickets(records, "WIFI", "Network", "open", "critical")
    print("Combined AND search:", [(t["id"], t["title"]) for t in result])
    print("Optional sorted search:", [t["id"] for t in sort_search_results(search_tickets(records))])
    empty = generate_reports([])
    print(f"Empty resolution percentage: {empty['resolution_percentage']:.1f}%")
    report = generate_reports(records)
    print("Category totals:", report["category_breakdown"])
    print("Unresolved total:", report["unresolved"])
    for module, function in (("notes", "add_note"), ("storage", "load_tickets")):
        try:
            integration_api(module, function)
            print(f"{module} API available; exercise it through the CLI.")
        except IntegrationPendingError as error:
            print(f"Integration pending: {error}")
    print("Run python3 main.py and choose 12 to take the quiz yourself.")
    print("No ticket files written. Human learning/review evidence is still required.")
    return 0

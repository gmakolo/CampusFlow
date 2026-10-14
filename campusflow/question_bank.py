"""Assessment question bank; scoring is implemented separately.

Correct choices exist in source for testing, but are not displayed before input.
"""

QUESTIONS = (
    {"prompt": "An open ticket is unassigned. Someone moves it to in_progress.",
     "choices": {"A": "Accept.", "B": "Reject and preserve data.", "C": "Resolve automatically.", "D": "Delete ticket."}, "correct": "B"},
    {"prompt": "The system contains zero tickets. What is the resolution percentage?",
     "choices": {"A": "Crash.", "B": "100%.", "C": "0%.", "D": "Divide by one."}, "correct": "C"},
    {"prompt": "Search title='wifi', category='Network', status='open'. What matches?",
     "choices": {"A": "Any one filter.", "B": "All supplied filters.", "C": "All Network tickets.", "D": "All open tickets."}, "correct": "B"},
    {"prompt": "A resolved ticket receives a new note.",
     "choices": {"A": "Accept.", "B": "Delete previous notes.", "C": "Reject until reopened.", "D": "Change status silently."}, "correct": "C"},
    {"prompt": "JSON contains two tickets with the same ID.",
     "choices": {"A": "Keep both.", "B": "Replace memory with duplicates.", "C": "Reject loading without modifying existing memory.", "D": "Rename IDs silently."}, "correct": "C"},
    {"prompt": "A pull request changes validation without negative-case tests.",
     "choices": {"A": "Approve.", "B": "Request focused tests and reasoning.", "C": "Merge immediately.", "D": "Ask AI to approve."}, "correct": "B"},
)

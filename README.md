# CampusFlow

CampusFlow is a Python command-line ticket management system designed to help manage campus support requests.

## Features

- Create and view support tickets.
- Assign tickets to staff members.
- Update ticket statuses.
- View the work queue.
- Generate ticket reports.
- Validate inputs and handle errors.

## Technologies

- Python 3
- Git and GitHub
- Python `unittest`

## Project Structure

```text
CampusFlow/
├── campusflow/
│   ├── tickets.py
│   ├── workflow.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   └── test_workflow.py
├── docs/
│   └── ai-learning-log.md
├── main.py
└── README.md
```

## How to Run the Application

Open a terminal in the project folder and run:

```powershell
py main.py
```

## How to Run the Tests

```powershell
py -m unittest discover -s tests -v
```

## Team Contributions

- **Engineer A:** Ticket creation and management, main menu, and ticket tests.
- **Engineer B:** Ticket assignment, status updates, work queue, reports, and workflow tests.

## Limitation

Tickets are stored in memory and are cleared when the program exits.

## Purpose

CampusFlow helps campus support teams organize requests, track progress, and generate reports.
 **# CampusFlow — Engineer B: Workflow Lifecycle & Automation**

This module forms the core workflow engine for **\*\*CampusFlow\*\***, an automated helpdesk and ticketing system designed to streamline campus support requests.&#x20;

As **\*\*Engineer B\*\***, this component focuses on managing ticket status transitions, handling resolution lifecycle logic, enforcing state rules, and executing automated task triggers.

\---

**## 🛠 Tech Stack & Tools**

\- **\*\*Language:\*\*** Python 3.10+
\- **\*\*Testing:\*\*** \`unittest\` / \`pytest\`
\- **\*\*Environment:\*\*** Visual Studio Code / Linux CLI
\- **\*\*Version Control:\*\*** Git & GitHub (\`campusflow-team\`)

\---

**## 🚀 Key Features & Responsibilities**

**### 1. Ticket State Machine & Status Transitions**
\- Enforces valid status transitions across the ticket lifecycle:
  - \`OPEN\` ➔ \`IN_PROGRESS\`
  - \`IN_PROGRESS\` ➔ \`RESOLVED\` / \`ON_HOLD\`
  - \`RESOLVED\` ➔ \`CLOSED\`
\- Prevents invalid or illegal status jumps (e.g., direct transition from \`OPEN\` to \`CLOSED\` without resolution notes).

**### 2. Workflow Validation & Exception Handling**
\- Handles edge cases such as missing ticket parameters, unauthorized status changes, and missing resolution details.
\- Raises structured exceptions to maintain data integrity across the system.

**### 3. Automated Lifecycle Actions**
\- Auto-assigns timestamps when tickets transition to \`RESOLVED\` or \`CLOSED\`.
\- Triggers notification hooks when high-priority or urgent support tickets are submitted or escalated.

\---

**## 📁 Repository & Branch Structure**

\`\`\`text
campusflow-team/
├── src/
│   ├── workflow\.py       # Core workflow state & transition logic
│   └── utils.py          # Helper functions & validation rules
├── tests/
│   └── test_workflow\.py  # Unit tests for workflow lifecycle
└── README.md             # Engineer B documentation

''' I ise this to run the unit testing '''

''' python3 -m unittest discover -s tests'''
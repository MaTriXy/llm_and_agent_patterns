# Agent

The agent excels in scenarios where traditional programming approaches fall short—specifically when dealing with open-ended problems that require flexible, multi-step solutions that can't be predetermined by a workflow.

For this example, I created a business financial assistant agent.

You can read an execution example in the [example document](/workflows/7_agent/EXAMPLE.MD).

## Architecture Components

### 1. Database

The system uses a JSON-based database (`db.json`) to store invoice records. Each invoice contains:

- ID
- Amount
- Date
- Type (`IN`/`OUT`)
- Description

### 2. Agent Tools

The agent has access to the following tools:

1. `get_todays_date()`

   - Returns current date in YYYY-MM-DD format

2. `get_all_invoices()`

   - Retrieves all invoices from the database

3. `get_highest_outgoing_invoice()`

   - Finds the largest outgoing (OUT) invoice

4. `get_highest_incoming_invoice()`

   - Finds the largest incoming (IN) invoice

5. `get_total_amount_of_invoices()`

   - Calculates sum of all invoice amounts

6. `create_invoice(amount, date, type, description)`
   - Adds new invoice to the database

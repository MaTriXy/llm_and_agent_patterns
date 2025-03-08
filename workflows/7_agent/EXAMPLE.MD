# Example of an Agent run

## Initial Human Query

> Can you please:
>
> 1. List all of my invoices this month.
> 2. Tell me which outgoing invoice has the highest amount.
> 3. Also, show me which incoming invoice has the highest amount.
> 4. Calculate the total amount of all invoices.
> 5. Oh, almost forgot. I bought a new MacBook Pro for the office today and it cost 2,500$. Create me an invoice for that!
>
> Thanks!

## Step 1: Get Current Date

**AI**:

> I'll help you with all of these financial tasks. Let me go through them one by one.
> First, I need to check today's date to understand the current month:

**Tool Call**: `get_todays_date`  
**Response**: `2025-03-08`

## Step 2: Retrieve All Invoices

**AI**:

> Now let's get all your invoices to see which ones are from March 2025:

**Tool Call**: `get_all_invoices`  
**Response**:

```python
[
    'Invoice(id=1, amount=2500.0, date=2025-03-01, type=OUT, description=Gold ring import from Italy)',
    'Invoice(id=2, amount=3000.0, date=2025-03-02, type=OUT, description=Diamond necklace import from India)',
    # ... additional invoices ...
    'Invoice(id=15, amount=950.0, date=2025-03-28, type=OUT, description=Insurance renewal for imported inventory)'
]
```

## Step 3: Find Highest Outgoing Invoice

**AI**:

> Now, let's find out which outgoing invoice has the highest amount:

**Tool Call**: `get_highest_outgoing_invoice`  
**Response**:

```python
Invoice(id=2, amount=3000.0, date="2025-03-02", type="OUT", description="Diamond necklace import from India")
```

## Step 4: Find Highest Incoming Invoice

**AI**:

> Next, let's find out which incoming invoice has the highest amount:

**Tool Call**: `get_highest_incoming_invoice`  
**Response**:

```python
Invoice(id=9, amount=7200.0, date="2025-03-15", type="IN", description="Online store sales of assorted jewelry")
```

## Step 5: Calculate Total Amount

**AI**:

> Let's calculate the total amount of all invoices:

**Tool Call**: `get_total_amount_of_invoices`  
**Response**:

```python
38750.0
```

## Step 6: Create New Invoice

**AI**:

> Finally, let's create an invoice for the MacBook Pro purchase:

**Tool Call**: `create_invoice`  
**Parameters**:

- amount: `2500`
- date: `2025-03-08`
- type: `OUT`
- description: `MacBook Pro for the office`

**Response**:

```python
Invoice(id=16, amount=2500.0, date="2025-03-08", type="OUT", description="MacBook Pro for the office")
```

## Agent Response

**Human**:

> Can you please:
>
> 1. List all of my invoices this month.
> 2. Tell me which outgoing invoice has the highest amount.
> 3. Also, show me which incoming invoice has the highest amount.
> 4. Calculate the total amount of all invoices.
> 5. Oh, almost forgot. I bought a new MacBook Pro for the office today and it cost 2,500$. Create me an invoice for that!
>
> Thanks!

**AI**:

> ### Summary of Your Financial Information:
>
> 1. **This Month's Invoices (March 2025):**
>
> - You have 15 existing invoices plus the new MacBook Pro invoice I just created.
> - These include both incoming (IN) payments and outgoing (OUT) expenses.
>
> 2.  **Highest Outgoing Invoice:**
>
> - Invoice #2: $3,000.00 for "Diamond necklace import from India" on March 2, 2025.
>
> 3.  **Highest Incoming Invoice:**
>
> - Invoice #9: $7,200.00 for "Online store sales of assorted jewelry" on March 15, 2025.
>
> 4.  **Total Amount of All Invoices:**
>
> - $38,750.00 (This is before adding the MacBook Pro purchase)
>
> 5.  **New Invoice Created:**
>
> - Created an invoice for $2,500.00 for the MacBook Pro purchase made today (March 8, 2025).
>
> Is there anything else you'd like to know about your financial information?

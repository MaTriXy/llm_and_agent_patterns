from datetime import datetime
from typing import Literal

from langchain_core.tools import tool

from .db import Database, Invoice

db = Database()


@tool
def get_todays_date() -> str:
    """Get the current date, formatted as YYYY-MM-DD."""

    return datetime.now().strftime("%Y-%m-%d")


@tool
def get_all_invoices() -> list[str]:
    """Get all invoices."""

    return [str(invoice) for invoice in db.get_invoices()]


@tool
def get_highest_outgoing_invoice() -> str:
    """Get the invoice with the highest amount and type `OUT`."""

    invoices = db.get_invoices()
    outgoing_invoices = [invoice for invoice in invoices if invoice.type == "OUT"]
    max_outgoing_invoice = max(outgoing_invoices, key=lambda x: x.amount)

    return str(max_outgoing_invoice)


@tool
def get_highest_incoming_invoice() -> str:
    """Get the invoice with the highest amount and type `IN`."""

    invoices = db.get_invoices()
    incoming_invoices = [invoice for invoice in invoices if invoice.type == "IN"]
    max_incoming_invoice = max(incoming_invoices, key=lambda x: x.amount)

    return str(max_incoming_invoice)


@tool
def get_total_amount_of_invoices() -> float:
    """Get the total amount of all invoices."""

    return db.get_total_amount()


@tool(
    description="Add an invoice to the database. `date` must be in YYYY-MM-DD format."
)
def create_invoice(
    amount: float, date: str, type: Literal["IN", "OUT"], description: str
) -> Invoice:
    invoice = Invoice(
        id=db.count_invoices() + 1,
        amount=amount,
        date=date,
        type=type,
        description=description,
    )
    db.add_invoice(invoice)

    return str(invoice)


tools = [
    get_todays_date,
    get_all_invoices,
    get_highest_outgoing_invoice,
    get_highest_incoming_invoice,
    get_total_amount_of_invoices,
    create_invoice,
]
tools_by_name = {tool.name: tool for tool in tools}

import json
import os
from typing import Literal

from pydantic import BaseModel


class Invoice(BaseModel):
    id: int
    amount: float
    date: str
    type: Literal["IN", "OUT"]
    description: str

    def __str__(self) -> str:
        return f"Invoice(id={self.id}, amount={self.amount}, date={self.date}, type={self.type}, description={self.description})"


class Database:
    path = os.path.join(os.path.dirname(__file__), "db.json")

    def __init__(self):
        self.load()

    def load(self):
        with open(self.path, "r") as f:
            db = json.load(f)
            self.invoices = [Invoice(**invoice) for invoice in db]

    def get_invoices(self):
        return self.invoices

    def get_total_amount(self):
        return sum(invoice.amount for invoice in self.invoices)

    def count_invoices(self):
        return len(self.invoices)

    def add_invoice(self, invoice: Invoice):
        self.invoices.append(invoice)
        self.save()

        return invoice

    def save(self):
        db = [invoice.model_dump() for invoice in self.invoices]

        with open(self.path, "w") as f:
            json.dump(db, f)

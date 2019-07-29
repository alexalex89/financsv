from dataclasses import dataclass, field
from typing import List


@dataclass
class Category(object):

    name: str
    parent: "Category" = None

    @property
    def path(self):
        parent_path = ""
        if self.parent:
            parent_path = self.parent.path + "/"
        return f"{parent_path}{self.name}"

    def __str__(self):
        return f"Category: {self.path}"


@dataclass
class Payment(object):

    receiver_or_sender_name: str
    date: str
    usage: str
    amount: float

    def __post_init__(self):
        self.amount = float(self.amount.replace(",", "."))

    def is_outgoing(self):
        return self.amount < 0

    def __str__(self):
        return f"ReceiverOrSenderName: {self.receiver_or_sender_name}, Date: {self.date}, Usage: {self.usage}, Amount: {self.amount}"


@dataclass
class ReceiverOrSender(object):

    name: str
    category: Category
    payments: List[Payment] = field(default_factory=list)
    alias: List[str] = field(default_factory=list)

    def does_payment_match(self, payment: Payment) -> bool:
        if (self.name.lower() in payment.receiver_or_sender_name.lower() or
                self.name.lower() in payment.usage.lower()
        or any(alias.lower() in payment.receiver_or_sender_name.lower() for alias in self.alias)):
            return True
        return False

    def get_sum(self, only_outgoing) -> float:
        if only_outgoing:
            return sum(p.amount for p in self.payments if p.is_outgoing())
        return sum(p.amount for p in self.payments)

    def __str__(self):
        return f"ReceiverOrSender: {self.name}, {str(self.category)}, Sum of Payments: {self.get_sum()}"

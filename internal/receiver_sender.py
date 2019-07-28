from dataclasses import dataclass, field
from typing import List


@dataclass
class Category(object):

    name: str
    parent: "Category" = None

    def __str__(self):
        return f"Category: {self.name}, Parent: {self.parent}"


@dataclass
class Payment(object):

    receiver_or_sender_name: str
    date: str
    usage: str
    amount: float

    def __post_init__(self):
        self.amount = float(self.amount.replace(",", "."))

    def __str__(self):
        return f"ReceiverOrSenderName: {self.receiver_or_sender_name}, Date: {self.date}, Usage: {self.usage}, Amount: {self.amount}"


@dataclass
class ReceiverOrSender(object):

    name: str
    category: Category
    payments: List[Payment] = field(default_factory=list)

    def does_payment_match(self, payment: Payment) -> bool:
        if self.name.lower() in payment.receiver_or_sender_name.lower():
            return True
        return False

    def get_sum(self) -> float:
        return sum(p.amount for p in self.payments)

    def __str__(self):
        return f"ReceiverOrSender: {self.name}, {str(self.category)}, Sum of Payments: {self.get_sum()}"

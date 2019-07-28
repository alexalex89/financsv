from dataclasses import dataclass, field


@dataclass
class Category(object):

    name: str
    parent: "Category" = None
    children: list = field(default_factory=list)

    def add_child(self, child):
        self.children.append(child)

    def get_sum(self):
        return sum(rs.get_sum() for rs in self.children)

    def __str__(self):
        return f"Category: {self.name}, Sum: {self.get_sum()}, Parent: {self.parent}, Children: {self.children}"


@dataclass
class Payment(object):

    receiver_or_sender_name: str
    date: str
    cause: str
    amount: float

    def __post_init__(self):
        self.amount = float(self.amount.replace(",", "."))

    def __str__(self):
        return f"ReceiverOrSenderName: {self.receiver_or_sender_name}, Date: {self.date}, Cause: {self.cause}, Amount: {self.amount}"


@dataclass
class ReceiverOrSender(object):

    name: str
    category: Category
    payments: list = field(default_factory=list)

    def add_payment(self, payment: Payment):
        self.payments.append(payment)

    def does_payment_match(self, payment: Payment):
        if self.name.lower() in payment.receiver_or_sender_name.lower():
            return True
        return False

    def get_sum(self):
        return sum(p.amount for p in self.payments)

    def __str__(self):
        return f"ReceiverOrSender: {self.name}, {str(self.category)}, Sum of Payments: {self.get_sum()}"

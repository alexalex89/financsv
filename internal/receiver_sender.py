class Category(object):

    def __init__(self, name, parent=None):
        self._name = name
        self._parent = parent
        self._children = []

    def get_name(self):
        return self._name

    def add_child(self, child):
        self._children.append(child)

    def get_sum(self):
        return sum(rs.get_sum() for rs in self._children)

    def __str__(self):
        return f"Category: {self._name}, Sum: {self.get_sum()}, Parent: {self._parent}, Children: {self._children}"

    def __repr__(self):
        return str(self)

# TODO: Dataclass
class Payment(object):

    def __init__(self, receiver_or_sender_name, date, cause, amount):
        self._receiver_or_sender_name = receiver_or_sender_name
        self._date = date
        self._cause = cause
        self._amount = float(amount.replace(",", "."))

    def get_receiver_or_sender_name(self):
        return self._receiver_or_sender_name

    def get_date(self):
        return self._date

    def get_cause(self):
        return self._cause

    def get_amount(self):
        return self._amount

    def __str__(self):
        return f"ReceiverOrSenderName: {self._receiver_or_sender_name}, Date: {self._date}, Cause: {self._cause}, Amount: {self._amount}"

    def __repr__(self):
        return str(self)


class ReceiverOrSender(object):

    def __init__(self, name, category: Category):
        self._name = name
        self._category = category
        self._payments = []

    def get_name(self):
        return self._name

    def add_payment(self, payment: Payment):
        self._payments.append(payment)

    def does_payment_match(self, payment: Payment):
        if self._name.lower() in payment.get_receiver_or_sender_name().lower():
            return True
        return False

    def get_sum(self):
        return sum(p.get_amount() for p in self._payments)

    def __str__(self):
        return f"ReceiverOrSender: {self._name}, {str(self._category)}, Sum of Payments: {self.get_sum()}"

    def __repr__(self):
        return str(self)
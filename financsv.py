import csv
import optparse
import yaml

from typing import List
from internal.receiver_sender import Category, ReceiverOrSender, Payment


def eval_payments(input_filename: str, receivers_filename: str) -> List[ReceiverOrSender]:
    with open(receivers_filename) as f_receivers:
        receivers_data = yaml.safe_load(f_receivers)
    parsed_receivers = create_tree(receiver_list=receivers_data)

    with open(input_filename, encoding="latin1") as f_input:
        fieldnames = ["_", "_", "date", "_", "usage", "receiver_or_sender_name", "_", "_", "amount", "_", "_"]
        csv_reader = csv.DictReader(f_input, fieldnames=fieldnames, delimiter=";", quotechar='"')
        next(csv_reader)

        for line in csv_reader:
            # Remove unused column(s)
            line.pop("_")

            payment = Payment(**line)
            for receiver in parsed_receivers:
                if receiver.does_payment_match(payment):
                    receiver.payments.append(payment)
                    break
            else:
                print(f"Unmatched payment {payment}")

    return parsed_receivers


def create_tree(receiver_list: list, category: Category = None) -> List[ReceiverOrSender]:
    result = []
    for entry in receiver_list:
        if type(entry) == str:
            receiver_or_sender = ReceiverOrSender(name=entry, category=category)
            result.append(receiver_or_sender)
        elif type(entry) == dict:
            new_category = Category(list(entry.keys())[0], parent=category)
            result.extend(create_tree(receiver_list=list(entry.values())[0], category=new_category))
    return result


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="input", help="Path to CSV file from the bank containing payment data", type="string")
    parser.add_option("-r", "--receivers", dest="receivers", help=".yml file containing grouping of receivers", type="string")

    options, _ = parser.parse_args()

    for element in eval_payments(input_filename=options.input, receivers_filename=options.receivers):
        print(element)

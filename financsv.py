import csv
import argparse
import yaml

from itertools import groupby
from collections import Counter
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
        unmatched = []

        for line in csv_reader:
            # Remove unused column(s)
            line.pop("_")

            payment = Payment(**line)
            for receiver in parsed_receivers:
                if receiver.does_payment_match(payment):
                    receiver.payments.append(payment)
                    break
            else:
                unmatched.append(payment.receiver_or_sender_name)
                """if payment.receiver_or_sender_name == "":
                    print(f"Unmatched payment from/to {payment.receiver_or_sender_name}, {payment.usage}")"""
        print(f"Unmatched (Total {len(unmatched)}): {Counter(unmatched).most_common()}")

    return parsed_receivers


def create_tree(receiver_list: list, category: Category = None) -> List[ReceiverOrSender]:
    receiver_sender_list = []
    for entry in receiver_list:
        if type(entry) == str:
            receiver_or_sender = ReceiverOrSender(name=entry, category=category)
            receiver_sender_list.append(receiver_or_sender)
        elif type(entry) == dict:
            new_category = Category(list(entry.keys())[0], parent=category)
            receiver_sender_list.extend(create_tree(receiver_list=list(entry.values())[0], category=new_category))
        elif type(entry) == list:
            receiver_or_sender = ReceiverOrSender(name=entry[0], category=category)
            del entry[0]
            receiver_or_sender.alias = entry
            receiver_sender_list.append(receiver_or_sender)
    return receiver_sender_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Path to CSV file from the bank containing payment data", type=str)
    parser.add_argument("-r", "--receivers", dest="receivers", help=".yml file containing grouping of receivers", type=str)
    parser.add_argument("-o", "--only-outgoing", dest="only_outgoing", help="Only consider outgoing payments for overview", default=False, action="store_true")

    args = parser.parse_args()

    result = eval_payments(input_filename=args.input, receivers_filename=args.receivers)

    for element in groupby(result, lambda x: x.category):
        print(f"{element[0]}, Sum: {sum(subel.get_sum(only_outgoing=args.only_outgoing) for subel in element[1]):.2f}")

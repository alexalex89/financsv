import csv
import optparse
import yaml

from internal.receiver_sender import Category, ReceiverOrSender, Payment


def eval_data(input_file, receivers):
    input_data = []
    results = {}
    with open(input_file, encoding="latin1") as f_input:
        csv_reader = csv.DictReader(f_input, delimiter=";", quotechar='"')
        for line in csv_reader:
            input_data.append({"date": line["Valutadatum"],
                         "receiver_or_sender_name": line["Beguenstigter/Zahlungspflichtiger"],
                         "cause": line["Verwendungszweck"],
                         "amount": line["Betrag"]})

    with open(receivers) as f_receivers:
        receivers_data = yaml.safe_load(f_receivers)

    parsed_receivers = create_tree(receiver_list=receivers_data)
    for line in input_data:
        payment = Payment(**line)
        for receiver in parsed_receivers:
            if receiver.does_payment_match(payment):
                receiver.add_payment(payment)
                break

    for element in parsed_receivers:
        print(element)


def create_tree(receiver_list, category=None):
    result = []
    for entry in receiver_list:
        if type(entry) == str:
            result.append(ReceiverOrSender(name=entry, category=category))
        elif type(entry) == dict:
            result.extend(create_tree(receiver_list=list(entry.values())[0], category=Category(list(entry.keys())[0], parent=category)))
    return result


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="input", help="Path to CSV file from the bank containing payment data", type="string")
    parser.add_option("-r", "--receivers", dest="receivers", help=".yml file containing grouping of receivers", type="string")

    options, _ = parser.parse_args()

    eval_data(input_file=options.input, receivers=options.receivers)

import unittest
import financsv
import yaml
import subprocess

from internal.receiver_sender import Category, ReceiverOrSender, Payment


class FinanCSVTest(unittest.TestCase):

    def setUp(self) -> None:
        lebenshaltung = Category(name="Lebenshaltung")
        drogerie = Category(name="Drogerie", parent=lebenshaltung)
        lebensmittel = Category(name="Lebensmittel", parent=lebenshaltung)
        restaurant = Category(name="FastFood/Restaurant", parent=lebensmittel)
        kleidung = Category(name="Kleidung", parent=lebenshaltung)

        drogeriemann = ReceiverOrSender(name="Drogeriemann", category=drogerie, alias=["DRM"])
        supermarkt = ReceiverOrSender(name="Ein Supermarkt", category=lebensmittel)
        pizza_venezia = ReceiverOrSender(name="Pizza Venezia", category=restaurant)
        a_b = ReceiverOrSender(name="A&B", category=kleidung)
        gucksi = ReceiverOrSender(name="gucksi", category=kleidung)

        self._receiver_or_sender_list = [drogeriemann, supermarkt, pizza_venezia, a_b, gucksi]

    def test_eval_payments(self):
        payment_supermarkt = Payment(receiver_or_sender_name="Ein Supermarkt GmbH", date="11.07.19",
                usage="SVWZ+2019-07-10T21.32 Debitk.1 2020-10ABWA+Ein Supermarkt SAGT DANKE. 43655361//Berlin/DE", amount="-0,89")
        payment_drogeriemann = Payment(receiver_or_sender_name="Drogeriemann VIELEN DANK", date="09.07.19",
                usage="EREF+12345678909877654332342352352356666MREF+2345654467876567654345CRED+DE11ZZZ12345678976SVWZ+123456434512312312312312312 ELV11111111 05.07 16.40 ME2",
                amount="-9,12")
        payment_drm = Payment(receiver_or_sender_name="DRM VIELEN DANK", date="09.07.19",
                                       usage="EREF+12345678909877654332342352352356666MREF+2345654467876567654345CRED+DE11ZZZ12345678976SVWZ+123456434512312312312312312 ELV11111111 05.07 16.40 ME2",
                                       amount="-9,12")
        payment_pizza_venezia = Payment(receiver_or_sender_name="11111 Pizza Venezia", date="05.07.19",
                usage="SVWZ+2019-07-04T12.09 Debitk.1 2020-10ABWA+11111 Pizza Venezia//BERLIN/DE", amount="-7,45")
        payment_a_b = Payment(receiver_or_sender_name="1271 A&B.BERLIN", date="14.06.19",
                usage="EREF+12345678909877654332342352352356666MREF+2345654467876567654345CRED+DE11ZZZ12345678976SVWZ+123456434512312312312312314 ELV11111111 12.06 15.24 ME1",
                amount="-36,96")
        payment_gucksi = Payment(receiver_or_sender_name="gucksi", date="18.02.19",
                usage="KREF+1231231231-12312312312312SVWZ+12312312 111111111111DATUM 18.02.2019, 06.44 UHR1.TAN 111171",
                                  amount="-78,06")

        self._receiver_or_sender_list[1].payments.append(payment_supermarkt)
        self._receiver_or_sender_list[0].payments.append(payment_drogeriemann)
        self._receiver_or_sender_list[0].payments.append(payment_drm)
        self._receiver_or_sender_list[2].payments.append(payment_pizza_venezia)
        self._receiver_or_sender_list[3].payments.append(payment_a_b)
        self._receiver_or_sender_list[4].payments.append(payment_gucksi)

        self.assertEqual(self._receiver_or_sender_list, financsv.eval_payments(input_filename="umsaetze.csv", receivers_filename="receivers.yml"))

    def test_command_line(self):
        process_result = subprocess.run(["python3.7", "../financsv.py", "-i", "umsaetze.csv", "-r", "receivers.yml"],
                                        capture_output=True)
        expected = (b"Unmatched (Total 1): [('KLAUWELT', 1)]\nCategory: Lebenshaltung/Drogerie,"
 b' Sum: -18.24\nCategory: Lebenshaltung/Lebensmittel, Sum: -0.89\nCategory: '
 b'Lebenshaltung/Lebensmittel/FastFood/Restaurant, Sum: -7.45\nCategory: Leb'
 b'enshaltung/Kleidung, Sum: -115.02\n')
        self.assertEqual(expected, process_result.stdout)
        self.assertEqual(0, process_result.returncode)

    def test_create_tree(self):
        with open("receivers.yml") as f_receivers:
            receivers_data = yaml.safe_load(f_receivers)

        self.assertEqual(self._receiver_or_sender_list,
                         financsv.create_tree(receivers_data))

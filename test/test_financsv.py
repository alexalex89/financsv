import unittest
import financsv
import yaml

from internal.receiver_sender import Category, ReceiverOrSender


class FinanCSVTest(unittest.TestCase):

    def test_create_tree(self):
        with open("receivers.yml") as f_receivers:
            receivers_data = yaml.safe_load(f_receivers)

        lebenshaltung = Category(name="Lebenshaltung")
        drogerie = Category(name="Drogerie", parent=lebenshaltung)
        lebensmittel = Category(name="Lebensmittel", parent=lebenshaltung)
        restaurant = Category(name="FastFood/Restaurant", parent=lebensmittel)
        kleidung = Category(name="Kleidung", parent=lebenshaltung)

        rossmann = ReceiverOrSender(name="ROSSMANN", category=drogerie)
        rewe = ReceiverOrSender(name="REWE", category=lebensmittel)
        mcdonalds = ReceiverOrSender(name="McDonald", category=restaurant)
        ernstings = ReceiverOrSender(name="ERNSTINGS", category=kleidung)
        bonprix = ReceiverOrSender(name="bonprix", category=kleidung)

        self.assertEqual([rossmann, rewe, mcdonalds, ernstings, bonprix],
                         financsv.create_tree(receivers_data))

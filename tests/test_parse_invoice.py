from unittest import TestCase


class ParseInvoice(TestCase):
    def setUp(self) -> None:
        self.file = open('source.txt', 'r')

    def test_parse_invoice(self):
        self.fail()

    def tearDown(self) -> None:
        self.file.close()

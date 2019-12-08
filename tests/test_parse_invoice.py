import unittest
import invoice_mole.invoice_parser as invoice_parser
import invoice_mole.config as config


class ParseInvoice(unittest.TestCase):

    def setUp(self) -> None:
        self.file = open('source.txt', 'r')
        self.text = self.file.read()

    def tearDown(self) -> None:
        self.file.close()

    def test_parse_existing_source_invoice(self):
        d = {'Fakturaperiod': '2018 11 01 - 2018 12 01',
             'Anl.nr': '41910608',
             'Mätarnr': '113474',
             'Summa exkl. moms': '16 783,81',
             'Summa inkl. moms': '20 979,77',
             'Energipris': '8 639,90',
             'Effektpris': '6 757,50',
             'Flödespris': '1 386,41'}
        result = invoice_parser.parse_invoice(self.text)
        self.assertDictEqual(result, d)

    def test_proper_price_hundred(self):
        key = 'Summa exkl. moms'
        text = 'Summa exkl. moms                                                                                      ' \
               ' 783,81 kr '
        expected_result = ['783,81']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)

    def test_proper_price_thousand(self):
        key = 'Summa exkl. moms'
        text = 'Summa exkl. moms                                                                                      ' \
               ' 16 783,81 kr '
        expected_result = ['16 783,81']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)

    def test_proper_price_million(self):
        key = 'Summa exkl. moms'
        text = 'Summa exkl. moms                                                                                      ' \
               '234 163 783,81 kr '
        expected_result = ['234 163 783,81']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)

    def test_price_with_two_spaces(self):
        key = 'Summa exkl. moms'
        text = 'Summa exkl. moms                                                                                      ' \
               '2  163 783,81 kr '
        expected_result = ['163 783,81']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)


if __name__ == '__main__':
    unittest.main()

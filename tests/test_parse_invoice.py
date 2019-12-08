import unittest
import invoice_mole.invoice_parser as invoice_parser


class ParseInvoice(unittest.TestCase):

    def setUp(self) -> None:
        self.file = open('source.txt', 'r')
        self.text = self.file.read()

    def tearDown(self) -> None:
        self.file.close()

    def test_parse_existing_source_invoice(self):
        expected_result = {
            'Fakturaperiod': '2018 11 01 - 2018 12 01',
            'Anl.nr': '41910608','Mätarnr': '113474',
            'Summa exkl. moms': '16 783,81',
            'Summa inkl. moms': '20 979,77',
            'Energipris': '8 639,90',
            'Effektpris': '6 757,50',
            'Flödespris': '1 386,41'
        }
        result = invoice_parser.parse_invoice(self.text)
        self.assertDictEqual(result, expected_result)

    def test_parse_invoice_with_missing_reult(self):
        text = """
        Fakturaperiod   : 2018 11 01 - 2018 12 01
        Anl.nr          : 41910608 kr
        Mätarnr         : 113474 kr
        Summa exkl. moms: 16 783,81
        Summa inkl. mom : 20 979 ,77 kr
        Energipris      : 
                        : 6 757,50
        Flödespris      : 1 386,41 kr

        """

        expected_result = {
            'Fakturaperiod': '2018 11 01 - 2018 12 01',
            'Anl.nr': '41910608', 'Mätarnr': '113474',
            'Summa exkl. moms': '',
            'Summa inkl. moms': '',
            'Energipris': '',
            'Effektpris': '',
            'Flödespris': '1 386,41'
        }
        result = invoice_parser.parse_invoice(text)
        self.assertDictEqual(result, expected_result)

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

    def test_price_without_currency_id(self):
        key = 'Summa exkl. moms'
        text = 'Summa exkl. moms                                                                                      ' \
               '163 783,81'
        self.assertIsNone(invoice_parser.find_key(key, text))

    def test_wrong_anl_nr(self):
        key = 'Anl.nr'
        text = 'Anl.nr: 4191060'
        self.assertIsNone(invoice_parser.find_key(key, text))

    def test_wrong_meter_nr(self):
        key = 'Mätarnr'
        text = 'Mätarnr  1234 5'
        self.assertIsNone(invoice_parser.find_key(key, text))

    def test_date_range_without_space(self):
        key = 'Fakturaperiod'
        text = 'Fakturaperiod 2018 11 01-2018 12 01'
        expected_result = ['2018 11 01-2018 12 01']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)

    def test_date_different_delimiters(self):
        key = 'Fakturaperiod'
        text = 'Fakturaperiod 2018/11/01 - 2018/12/01'
        expected_result = ['2018/11/01 - 2018/12/01']
        self.assertEqual(invoice_parser.find_key(key, text), expected_result)

    def test_validate_start(self):
        prices = ['0,123', '01,12', '0,31']
        expected_output = ['0,31']
        result = invoice_parser.validate_price(prices)
        self.assertEquals(result, expected_output)


if __name__ == '__main__':
    unittest.main()

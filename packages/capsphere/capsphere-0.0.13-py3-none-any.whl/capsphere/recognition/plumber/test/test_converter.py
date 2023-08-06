from capsphere.recognition.plumber.converter import func_ambank, func_cimb
import unittest
from decimal import Decimal
from capsphere.common.utils import get_test_resource_path


class TestConverter(unittest.TestCase):

    path_ambank = get_test_resource_path('ambank.pdf')
    path_cimb = get_test_resource_path('cimb.pdf')

    def test_func_ambank(self):
        output = func_ambank(self.path_ambank)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('83407.48'))
        self.assertEqual(end_balance, Decimal('49863.77'))
        self.assertEqual(total_debit, Decimal('227306.69'))
        self.assertEqual(total_credit, Decimal('193762.98'))
        self.assertEqual(average_debit, Decimal('1612.10'))
        self.assertEqual(average_credit, Decimal('9688.15'))
        self.assertEqual(month, '31Mar')

    def test_func_cimb(self):
        # TODO Add cimb.pdf, then write CIMB resources here for func_cimb
        output = func_cimb(self.path_cimb)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('686.21'))
        self.assertEqual(end_balance, Decimal('924.55'))
        self.assertEqual(total_debit, Decimal('34642.24'))
        self.assertEqual(total_credit, Decimal('34880.58'))
        self.assertEqual(average_debit, Decimal('314.93'))
        self.assertEqual(average_credit, Decimal('352.33'))
        self.assertEqual(month, '30/11/2021')

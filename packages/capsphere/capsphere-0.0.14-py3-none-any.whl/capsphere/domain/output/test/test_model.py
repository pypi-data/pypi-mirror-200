from unittest import TestCase
from capsphere.domain.output.model import Cf
from decimal import Decimal


class TestExceptions(TestCase):

    def test_cf_validation(self):
        with self.assertRaises(TypeError) as cm:
            Cf('Andrew Lee',
               'Ambank',
                'Mar 22',
               2502.23,
               Decimal('25'),
               Decimal('25'),
               Decimal('25'),
               Decimal('25'),
               Decimal('25'))
        self.assertEqual("Field 'start_balance' must be of type 'Decimal'.",
                         str(cm.exception))

    # def test_monthly_cf_validation(self):
    #     with self.assertRaises(TypeError) as cm:
    #         MultiCf('Andy', 'Rhb', 'invalid cf')
    #     self.assertEqual("Field 'cash_flow' must be a list of type 'Cf'.",
    #                      str(cm.exception))
    #
    #     with self.assertRaises(ValueError) as cm:
    #         MultiCf('Andy', 'Rhb', [])
    #     self.assertEqual("Field 'cash_flow' must have one or more items.",
    #                      str(cm.exception))
    #
    # def test_cf_aggregations(self):
    #     pass

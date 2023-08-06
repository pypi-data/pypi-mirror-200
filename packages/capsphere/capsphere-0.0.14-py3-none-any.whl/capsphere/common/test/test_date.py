import re
import unittest
from capsphere.common.date import convert_date


class TestConvertDate(unittest.TestCase):

    date1 = '01Aug'
    date2 = '01/08/2022'
    date3 = '01/08'
    date4 = '10822'
    date5 = '101122'
    date6 = '01-08-2022'

    def test_convert_date(self):
        ambank_date = convert_date(self.date1)
        cimb_date = convert_date(self.date2)
        maybank_date = convert_date(self.date3)
        alliance_date = convert_date(self.date4)
        alliance_date2 = convert_date(self.date5)
        hl_date = convert_date(self.date6)

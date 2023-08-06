from capsphere.recognition.plumber.reader import extract_bank_name
import unittest
from capsphere.common.utils import get_test_resource_path


class TestReader(unittest.TestCase):

    path_ambank = get_test_resource_path('ambank.pdf')
    path_cimb = get_test_resource_path('cimb.pdf')

    def test_extract_ambank_name(self):
        output = extract_bank_name(self.path_ambank)
        self.assertEqual(output, 'AmBank')

    def test_extract_cimb_name(self):
        output = extract_bank_name(self.path_cimb)
        self.assertEqual(output, 'CIMB')


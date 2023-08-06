import unittest
from capsphere.common.utils import flatten_list, get_file_format, process_text, read_config
from capsphere.resources.test.data import FILE_NAME_1, FILE_NAME_2, FILE_NAME_3


class TestUtils(unittest.TestCase):

    banks = ["AmBank", "CIMB", "Maybank",
             "Maybank Islamic", "Alliance", "Hong Leong",
             "RHB", "RHB Islamic", "Public Bank"]

    def test_valid_file_split(self):
        pdf_file = get_file_format(FILE_NAME_1)
        img_file = get_file_format(FILE_NAME_2)
        self.assertEqual(pdf_file, 'pdf')
        self.assertEqual(img_file, 'img')

    def test_invalid_file_split(self):
        with self.assertRaises(ValueError) as cm:
            get_file_format(FILE_NAME_3)
        self.assertEqual("Unrecognised filename format 'invalid.file.extension': "
                         "Unable to split strings",
                         str(cm.exception))

    # def test_read_config(self):
    #     data = read_config()
    #     with open('./resources/test_schema.json') as f:
    #         test_data = json.load(f)
    #         self.assertEqual(data, test_data)

    def test_decimal_encoder(self):
        # TODO add resources here
        pass

    def test_process_text(self):
        headers_ambank = process_text(["date", "transaction", "cheque no.", "debit", "credit", "balance"])
        headers_cimb = process_text(["date", "description", "cheque / ref no", "withdrawal", "deposits", "balance"])

        self.assertEqual(headers_ambank, ["date", "transaction", "cheque_no", "debit", "credit", "balance"])
        self.assertEqual(headers_cimb, ["date", "description", "cheque_ref_no", "withdrawal", "deposits", "balance"])

    def test_flatten_list(self):
        data = [["date", "transaction", "cheque no.", "debit", "credit", "balance"]]
        expected = ["date", "transaction", "cheque no.", "debit", "credit", "balance"]
        actual = flatten_list(data)
        self.assertEqual(len(actual),  6)
        self.assertEqual(actual, expected)




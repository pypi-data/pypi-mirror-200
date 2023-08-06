import unittest
from capsphere.resources.test.data import CF, CF2
from capsphere.domain.output.excel import _generate_average_rcf, create_worksheet
import pandas as pd


class TestExcel(unittest.TestCase):
    single_cashflow = [CF]
    multi_cashflow = [CF, CF2]
    headers = ['start_balance', 'end_balance', 'total_debit', 'total_credit',
               'average_debit', 'average_credit']
    labels = ['Mar 2022', 'Apr 2022', 'Total', 'Average']

    def test_single_cashflow(self):
        df = _generate_average_rcf(self.single_cashflow)
        actual_totals = df.loc['Total']
        actual_averages = df.loc['Average']
        expected_totals = [133271.25, 99927.34, 228106.89, 194762.98, 3660.80, 7041.59]
        expected_averages = [66635.63, 49963.67, 114053.45, 97381.49, 1830.40, 3520.80]
        df_rows = 4
        self.__assert_dataframes(df)
        self.assertEqual(len(df.index), df_rows)
        self.__assert_data_row(actual_totals, expected_totals)
        self.__assert_data_row(actual_averages, expected_averages)

    def test_multi_cashflow(self):
        df = _generate_average_rcf(self.multi_cashflow)
        actual_totals = df.loc['Total']
        actual_averages = df.loc['Average']
        expected_totals = [266542.5, 199854.68, 456213.78, 389525.96, 7321.6, 14083.18]
        expected_averages = [133271.25, 99927.34, 228106.89, 194762.98, 3660.80, 7041.59]
        df_rows = 4
        self.__assert_dataframes(df)
        self.assertEqual(len(df.index), df_rows)
        self.__assert_data_row(actual_totals, expected_totals)
        self.__assert_data_row(actual_averages, expected_averages)

    def __assert_dataframes(self, df: pd.DataFrame) -> None:

        if len(df.index) != len(self.labels):
            raise ValueError(f'{len(df.index)} total labels supplied, expected {len(self.labels)}')

        if len(df.columns) != len(self.headers):
            raise ValueError(f'{len(df.columns)} total labels supplied, expected {len(self.headers)}')

        self.assertEqual(len(df.columns), 6)

        for header in self.headers:
            self.assertTrue(header in df.columns)

        for label in self.labels:
            self.assertTrue(label in df.index)

        # TODO assert using numpy instead once the series has been sorted in month order
        # index_array = np.array(df.index)
        # columns_array = np.array(df.columns)
        #
        # if self.assertFalse(index_array, self.labels):
        #     mask = index_array != self.labels
        #     raise ValueError(f"Different elements: {index_array[mask]} (in lst1) and {self.labels[mask]} (in lst2).")
        #
        # if self.assertFalse(columns_array, self.headers): mask = columns_array != self.headers raise ValueError(
        # f"Different elements: {columns_array[mask]} (in lst1) and {self.headers[mask]} (in lst2).")

    def __assert_data_row(self, data_row: pd.Series, expected_values: list[float]) -> None:
        if len(data_row) != len(expected_values):
            raise ValueError(f'data row has {len(data_row)} elements, expected {len(expected_values)}')
        diff_list = [{"index": index, "actual": x, "expected": y} for index, (x, y)
                     in enumerate(zip(data_row, expected_values)) if abs(x - y) >= 0.00001]
        self.assertFalse(diff_list, f"Lists are not equal: {diff_list}")

    # TODO write up a unit resources for excel file somehow, output looks good
    # def test_worksheet_single_cashflow(self):
    #     data = create_worksheet(self.single_cashflow)
    #     with open("single.xlsx", "wb") as f:
    #         f.write(data.getvalue())
    #
    # def test_worksheet_multi_cashflow(self):
    #     data = create_worksheet(self.multi_cashflow)
    #     with open("multi.xlsx", "wb") as f:
    #         f.write(data.getvalue())

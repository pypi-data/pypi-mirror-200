from dataclasses import dataclass
from decimal import Decimal
from dataclass_wizard import JSONWizard
from typing import Type

BANKS = ['Maybank', 'CIMB', 'Ambank', 'Hong Leong', 'Alliance', 'Public Bank', 'RHB']


@dataclass(unsafe_hash=True)
class Cf(JSONWizard):
    customer_name: str
    bank_name: str
    month: str
    start_balance: Decimal
    end_balance: Decimal
    total_debit: Decimal
    total_credit: Decimal
    average_debit: Decimal
    average_credit: Decimal

    def __post_init__(self):
        if not isinstance(self.customer_name, str):
            raise TypeError("Field 'customer_name' must be of type 'str'.")
        if not isinstance(self.bank_name, str):
            raise TypeError("Field 'bank_name' must be of type 'str'.")
        if not isinstance(self.month, str):
            raise TypeError("Field 'month' must be of type 'str'.")
        if not isinstance(self.start_balance, Decimal):
            raise TypeError("Field 'start_balance' must be of type 'Decimal'.")
        if not isinstance(self.end_balance, Decimal):
            raise TypeError("Field 'end_balance' must be of type 'Decimal'.")
        if not isinstance(self.total_debit, Decimal):
            raise TypeError("Field 'total_debit' must be of type 'Decimal'.")
        if not isinstance(self.total_credit, Decimal):
            raise TypeError("Field 'total_credit' must be of type 'Decimal'.")
        if not isinstance(self.average_debit, Decimal):
            raise TypeError("Field 'average_debit' must be of type 'Decimal'.")
        if not isinstance(self.average_credit, Decimal):
            raise TypeError("Field 'average_credit' must be of type 'Decimal'.")


@dataclass(unsafe_hash=True)
class MultiCf(JSONWizard):
    cf_list: list[Type[Cf]]

    def aggregate(self):
        pass


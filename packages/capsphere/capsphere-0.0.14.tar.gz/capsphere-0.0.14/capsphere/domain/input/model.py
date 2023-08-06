import abc
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from abc import ABC, ABCMeta, abstractmethod

HEADERS = {
    'ambank': ['date', 'transaction', 'cheque no.', 'debit', 'credit', 'balance'],
    'cimb': ['date', 'description', 'cheque / ref no', 'withdrawal', 'deposits', 'balance'],
    'rhb': ['date', 'branch', 'description', 'sender''s beneficiary''s name', 'reference 1 / recipient''s reference',
            'reference 2 / other payment details', 'refnum', 'amount (dr)', 'amount (cr)', 'balance'],
    'maybank': ['entry_date', 'value_date', 'transaction description', 'transaction amount', 'statement balance']
}


@dataclass(unsafe_hash=True)
class Transaction(JSONWizard):

    """
    Single transaction schema that all banks need to adhere to. The best way to think of this is as a generic row
    from a bank statement
    """

    date: str
    description: str
    reference: str
    debit: str
    credit: str
    balance: str


class TransactionConverter(ABC):

    @abstractmethod
    def to_transaction(self) -> Transaction:
        raise NotImplementedError


def create_dataclass(fields, base_class=None):

    """
    Dynamically creates a dataclass with the given field names.
    """

    # Remove any invalid characters from the field names
    field_names = [name.replace(" ", "_").replace("'", "").replace("\\", "")
                   .replace("//", "").replace(",", "").replace(".", "") for name in fields]

    # Define the dataclass with the given field names
    @dataclass(unsafe_hash=True)
    class _DataRow(base_class or object, JSONWizard):
        __slots__ = ()
        # Define the fields with default values of None
        __annotations__ = {name: str for name in field_names}
    if base_class:
        _DataRow.__bases__ = (base_class,)
    if issubclass(base_class, ABC):
        ABCMeta.register(_DataRow)
    return dataclass(_DataRow)


def create_transaction_class(class_name: str, base_class: type, class_fields: list[str]):

    """
    Dynamically creates a class that inherits from a given base class and has the given fields as instance variables.

    :param class_name: Name of the class to be created.
    :param base_class: Abstract base class that the created class should inherit from.
    :param class_fields: List of strings representing the instance variables that the created class should have.
    :return: A dynamically created class that inherits from the given base class and has the given fields as instance variables.
    """

    non_strings = [item for item in class_fields if not isinstance(item, str)]

    if non_strings:
        raise ValueError(f"Found non-string elements in class_fields: {non_strings}")

    field_names = [name.replace(" ", "_").replace("'", "").replace("\\", "")
                   .replace("//", "").replace(",", "").replace(".", "") for name in class_fields]

    class_dict = {}
    for field in field_names:
        class_dict[field] = None

    def to_transaction(self):
        return base_class(*[getattr(self, field_name) for field_name in field_names])

    class_dict["to_transaction"] = to_transaction

    return abc.ABCMeta(class_name, (base_class,), class_dict)


class TransactionConverterMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        if name in HEADERS:
            fields = HEADERS[name]

            @abstractmethod
            def to_transaction(self) -> Transaction:
                pass

            for i, field in enumerate(fields):
                attrs[field] = property(lambda self, i=i: getattr(self, f"_data[{i}]"))

            attrs['__annotations__'] = {field: str for field in fields}
            attrs['_fields'] = tuple(fields)

        return super().__new__(cls, name, bases, attrs)

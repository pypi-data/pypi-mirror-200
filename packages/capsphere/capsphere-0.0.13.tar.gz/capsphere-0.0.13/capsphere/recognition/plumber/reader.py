import pdfplumber
from typing import Union
from capsphere.common.utils import read_config
from pdfplumber.page import Page


def extract_bank_name(file_path: Union[str, bytes]) -> str:

    pdf = pdfplumber.open(file_path)

    bank_name = _search_for_text(pdf.pages[0])

    if not bank_name:
        bank_name = _search_for_text(pdf.pages[-1])

    if not bank_name:
        raise ValueError(f'Unable to get bank name from {file_path}')

    return bank_name


def _search_for_text(image: Page) -> str:
    bank_schemas = read_config()
    for bank in bank_schemas:
        for identifier in bank['identifiers']:
            if image.search(identifier, regex=True, case=False):
                return bank['name']
    return ""



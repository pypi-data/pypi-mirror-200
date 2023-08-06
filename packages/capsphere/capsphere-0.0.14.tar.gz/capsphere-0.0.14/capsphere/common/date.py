# ddmmm	01Aug
# dd/mm/yyyy	01/08/2022
# dd/mm	01/08
# ddmyy 10822
# ddmmyy 101122

import calendar
import re
from typing import Any


def convert_month(date_range: str) -> list[tuple[Any, Any, Any]]:
    pattern = r"(\b(0?[1-9]|[12]\d|3[01])\b)/(\b(0?[1-9]|1[0-2])\b)/(\d{4})"
    dates = re.findall(pattern, date_range)
    if dates:
        return [(t[0], t[2], t[4]) for t in dates]
    else:
        raise Exception(f"Unable to match date range {date_range}")


def convert_date(date: str) -> str:
    pass

from pprint import pprint as __pprint
import typing as __typing

import requests as __requests

from .connection.repeated_call import request_or_repeat as __request_or_repeat
from . import package_consts as __Const


def parse_rows(
    schema: list[str], data: list[list[str]], verbose=False
) -> list[__typing.Any]:
    """parses from (look below) to list of dict (look even more below)
    >>> schema = [header1, header2, ...]
    >>> data = [
        [cell1_value, cell2_value, ...],  # 1st row
        [Cell1_value, Cell2_value, ...],  # 2nd row
        ...
    ]

    returns list of dict:
    >>> return_value = [
        {header1: cell1_value, header2: cell2_value}, # 1st row
        {header2: Cell1_value, header2: Cell2_value}, # 2nd row
        ...
    ]

    :param schema: list of headers (eg price, area, floor, id, balcony, status, ...)
    :param data: two-dimensional list of data; It will be parsed as `data[row][column]`
    :param verbose: shall error text be printed?"""
    data = {
        "schema": schema,
        "data": data,
    }
    response = __request_or_repeat(
        __requests.post,
        url=f"{__Const.BACKEND_UTILS_URL}/parse",
        json=data,
        params={"cell_cnt": len(schema) * len(data)},
    )

    try:
        json_data: dict = response.json()
        is_success = json_data["is_success"]
        if not is_success and verbose:
            __pprint(json_data.get("error"))
        return json_data.get("results", [])
    except Exception:
        raise RuntimeError(
            "Could not understand remote server response for rows-parsing. "
            f"Try updating {__Const.PACKAGE_NAME} and try again"
        )

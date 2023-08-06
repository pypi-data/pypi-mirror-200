import requests as __requests


def response_ok_or_raise(response: __requests.Response) -> None:
    """Raises ValueError if response returned failure code"""
    try:
        response.raise_for_status()
    except Exception as ex:
        raise ValueError(
            "The response was not ok. "
            f"Response code: {response.status_code} "
            f"response text: {response.text}"
        ) from ex

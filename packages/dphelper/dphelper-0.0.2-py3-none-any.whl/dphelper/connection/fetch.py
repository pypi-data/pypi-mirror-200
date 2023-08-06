import requests as __requests


def fetch_html(
    url: str,
    *,
    provider: str | None = None,
    params: None | dict = None,
    headers: None | dict = None,
    cookies: None | dict = None,
):
    if provider is None:
        # should it use method request_or_repeat?
        return __requests.get(url=url, params=params, headers=headers, cookies=cookies)
    raise NotImplementedError("Sorry, no provider choice is supported")


def from_url(url, verify=True, headers={}):
    response = __requests.get(url, verify=verify, headers=headers)
    return "".join([line.decode("utf-8").strip() for line in response.iter_lines()])

""" 
This setter module works only for:
 * current execution, 
 * multi-threading (usually shall),
 * current process;

The setters will not effect child processes, parent processes
(shall it be addressed using environs?) 
"""

from . import package_consts as __Const


def set_backend_url(new_backend_url: str) -> None:
    """Sets backend url. Do not forget http, https thingies.
    It alters all backend url entries. new backend url shall not end with '/'

    :param new_backend_url: the url where backend is located
    """
    if new_backend_url is None or new_backend_url == "":
        raise ValueError("Cannot set backend url to None or empty string")

    # prepare backend url
    new_backend_url = new_backend_url.strip()
    new_backend_url = (
        new_backend_url.removesuffix("/")
        if new_backend_url.endswith("/")
        else new_backend_url
    )

    # change backend url and its children
    backend_url_keys = [
        key for key in __Const.__dict__.keys() if "BACKEND_" in key and "_URL" in key
    ]
    old_backend_url = __Const.BACKEND_URL
    for key in backend_url_keys:
        url: str = getattr(__Const, key)
        setattr(__Const, key, url.replace(old_backend_url, new_backend_url, 1))

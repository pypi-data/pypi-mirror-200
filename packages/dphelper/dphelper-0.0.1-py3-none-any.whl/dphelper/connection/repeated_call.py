from requests import Response
from requests.exceptions import ConnectionError
from time import sleep

from .. import package_consts as _Const


def request_or_repeat(function: callable, *args, **kwargs) -> Response:
    """Makes a request (call provided function with args and kwargs).
    * If it fails because of ConnectionError, retries;
    * If it fails because status_code >= 500, retries;
    retry count and sleep times are specified in package_consts.py

    :param function: function to call; expected to get response object from it.
    :param *args: what args to pass to function.
    :param **kwargs: what kwargs to pass to function.
    :return: `Response` or raises RuntimeError after all failures
    """

    failures_count = 0
    sleep_time = _Const.REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S

    def _handle_failure():
        nonlocal failures_count, sleep_time
        sleep_time = (
            sleep_time**_Const.REQUEST_SLEEP_INCREASE_POWER
            if failures_count > 0
            else sleep_time
        )
        failures_count = failures_count + 1

    while failures_count < _Const.REQUEST_DROP_ON_FAILURE_COUNT:
        if failures_count > 0:
            sleep(sleep_time)
        try:
            response: Response = function(*args, **kwargs)
            if response.status_code >= 500:
                # server tripped, not we (internal server error)
                raise RuntimeError
            else:
                return response
        except ConnectionError:
            _handle_failure()
        except RuntimeError:
            _handle_failure()

    raise RuntimeError(
        f"[internal] Could not make connection for {_Const.REQUEST_DROP_ON_FAILURE_COUNT} times."
    )

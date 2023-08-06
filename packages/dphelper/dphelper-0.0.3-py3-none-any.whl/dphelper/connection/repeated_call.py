from requests import Response as __Response
from requests.exceptions import ConnectionError as __ConnectionError
from time import sleep as __sleep

from .. import package_consts as __Const


def request_or_repeat(function: callable, *args, **kwargs) -> __Response:
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
    sleep_time = __Const.REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S

    def _handle_failure():
        nonlocal failures_count, sleep_time
        sleep_time = (
            sleep_time**__Const.REQUEST_SLEEP_INCREASE_POWER
            if failures_count > 0
            else sleep_time
        )
        failures_count = failures_count + 1

    while failures_count < __Const.REQUEST_DROP_ON_FAILURE_COUNT:
        if failures_count > 0:
            __sleep(sleep_time)
        try:
            response: __Response = function(*args, **kwargs)
            if response.status_code >= 500:
                # server tripped, not we (internal server error)
                raise RuntimeError
            else:
                return response
        except __ConnectionError:
            _handle_failure()
        except RuntimeError:
            _handle_failure()

    raise RuntimeError(
        f"[internal] Could not make connection for {__Const.REQUEST_DROP_ON_FAILURE_COUNT} times."
    )

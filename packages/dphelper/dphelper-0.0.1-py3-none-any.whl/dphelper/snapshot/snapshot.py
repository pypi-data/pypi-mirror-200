import requests as _requests

from .. import package_consts as _Const
from ..connection.repeated_call import request_or_repeat as _request_or_repeat

_KEY_FILE_URL = "json_data_file_url"
_KEY_IS_LOADABLE = "is_json_data_loadable"


def get_meta_by_id(snapshot_id: int) -> dict:
    response = _request_or_repeat(
        _requests.get, url=f"{_Const.BACKEND_SNAPSHOT_URL}/{snapshot_id}/head"
    )
    response.raise_for_status()
    return response.json()


def _get_body_by_url_or_id(
    *,
    is_loadable: None | bool = None,
    body_file_url: None | str = None,
    snapshot_id: None | int = None,
):
    if body_file_url is None and snapshot_id is None:
        raise ValueError(
            "Cant get snapshot body without args. Please give file url of snapshot data or snapshot_id"
        )
    if is_loadable == False:
        # why bother downloading if it will be blank / corrupted / etc. ?
        # or should exception be raised?
        return {}
    if body_file_url is None:
        # maybe old snapshot, so ask for preview, expecting to get full snapshot body
        body_file_url = f"{_Const.BACKEND_SNAPSHOT_URL}/{snapshot_id}/preview"
    response = _request_or_repeat(_requests.get, url=body_file_url)
    response.raise_for_status()
    return response.json()


def get_body_by_id(snapshot_id: int):
    # get meta
    meta = get_meta_by_id(snapshot_id)
    # now body
    return _get_body_by_url_or_id(
        is_loadable=meta.get(_KEY_IS_LOADABLE, None),
        body_file_url=meta.get(_KEY_FILE_URL, None),
        snapshot_id=snapshot_id,
    )


def _raise_if_not_implemented_filter(
    *,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    **_,
) -> None:
    if by_is_verified is not None:
        raise NotImplemented("Sorry, filter is_verified not implemented")
    elif by_validation_statuses is not None:
        raise NotImplemented("Sorry, filter validation_statuses not implemented")


def _args_to_filter_params(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
    **_,
) -> dict:
    return {
        "challenge_id": by_challenge_id,
        "user_id": by_user_id,
        "is_verified": by_is_verified,
        "validation_statuses": by_validation_statuses,
        "is_from_code_run": by_is_from_robot,
    }


def get_latest_meta(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
) -> dict:
    # check, is each filter supported / implemented.
    # at this point locals() will have dict of supplied args and their values
    _raise_if_not_implemented_filter(**locals())
    response = _request_or_repeat(
        _requests.get,
        url=f"{_Const.BACKEND_SNAPSHOT_URL}/latest/",
        params=_args_to_filter_params(**locals()),
    )
    response.raise_for_status()
    return response.json()


def get_latest_body(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
):
    # at this point locals() will have dict of supplied args and their values
    meta = get_latest_meta(**locals())
    return _get_body_by_url_or_id(
        is_loadable=meta.get(_KEY_IS_LOADABLE, None),
        body_file_url=meta.get(_KEY_FILE_URL, None),
        snapshot_id=meta.get("id"),
    )

import typing as __typing

import requests as __requests

from .. import package_consts as __Const
from ..connection.repeated_call import request_or_repeat as __request_or_repeat
from ..connection.error import response_ok_or_raise as __response_ok_or_raise
from .. import schemas as __schemas


def get_meta_by_id(snapshot_id: int) -> __schemas.SnapshotMeta:
    "gets meta info about snapshot (by snapshot id)"
    response = __request_or_repeat(
        __requests.get, url=f"{__Const.BACKEND_SNAPSHOT_URL}/{snapshot_id}/head"
    )
    __response_ok_or_raise(response)
    return __schemas.SnapshotMeta(**response.json())


def __get_body_by_url_or_id(
    *,
    is_loadable: None | bool = None,
    body_file_url: None | str = None,
    snapshot_id: None | int = None,
) -> __typing.Any:
    "gets snapshot body by file url or id. if body is not loadable, {} will be returned"
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
        body_file_url = f"{__Const.BACKEND_SNAPSHOT_URL}/{snapshot_id}/preview"
    response = __request_or_repeat(__requests.get, url=body_file_url)
    __response_ok_or_raise(response)
    return response.json()


def get_body_by_id(snapshot_id: int) -> __typing.Any:
    "gets snapshot body by snapshot id. Body might be any type but usually it is a list of objects"
    # get meta
    meta = get_meta_by_id(snapshot_id)
    # now body
    return __get_body_by_url_or_id(
        is_loadable=meta.is_json_data_loadable,
        body_file_url=meta.json_data_file_url,
        snapshot_id=snapshot_id,
    )


def get_by_id(snapshot_id: int) -> __schemas.Snapshot:
    "gets snapshot meta + snapshot body as a whole object. snapshot body is placed inside `json_data`"
    meta = get_meta_by_id(snapshot_id)
    return __schemas.Snapshot(
        **meta.dict(),
        json_data=__get_body_by_url_or_id(
            is_loadable=meta.is_json_data_loadable,
            body_file_url=meta.json_data_file_url,
            snapshot_id=snapshot_id,
        ),
    )


def __raise_if_not_implemented_filter(
    *,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    **_,
) -> None:
    "raises NotImplemented if one of the filters is not implemented"
    if by_is_verified is not None:
        raise NotImplementedError("Sorry, filter is_verified not implemented")
    elif by_validation_statuses is not None:
        raise NotImplementedError("Sorry, filter validation_statuses not implemented")


def __args_to_filter_params(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
    **_,
) -> dict:
    "remaps kwargs so key names match backend names"
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
) -> __schemas.SnapshotMeta:
    """gets latest snapshot meta by specified filters.

    :param by_challenge_id: to what challenge shall snapshot belong? If None, any will match.
    :param by_user_id: to what user shall snapshot belong? If None, any will match.
    :param by_is_verified: shall the snapshot be moderator-approved? If None, any will match.
    :param by_validation_statuses: searched statuses of snapshot validation. If None, any will match.
    :param by_is_from_robot: shall the snapshot be generated from robot code run (True) or uploaded by human (False)? If None, any will match."""
    # check, is each filter supported / implemented.
    # at this point locals() will have dict of supplied args and their values
    __raise_if_not_implemented_filter(**locals())
    response = __request_or_repeat(
        __requests.get,
        url=f"{__Const.BACKEND_SNAPSHOT_URL}/latest/head/",
        params=__args_to_filter_params(**locals()),
    )
    __response_ok_or_raise(response)
    return __schemas.SnapshotMeta(**response.json())


def get_latest_body(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
) -> __typing.Any:
    """gets latest snapshot body by specified filters

    :param by_challenge_id: to what challenge shall snapshot belong? If None, any will match.
    :param by_user_id: to what user shall snapshot belong? If None, any will match.
    :param by_is_verified: shall the snapshot be moderator-approved? If None, any will match.
    :param by_validation_statuses: searched statuses of snapshot validation. If None, any will match.
    :param by_is_from_robot: shall the snapshot be generated from robot code run (True) or uploaded by human (False)? If None, any will match."""
    # at this point locals() will have dict of supplied args and their values
    meta = get_latest_meta(**locals())
    return __get_body_by_url_or_id(
        is_loadable=meta.is_json_data_loadable,
        body_file_url=meta.json_data_file_url,
        snapshot_id=meta.id,
    )


def get_latest(
    *,
    by_challenge_id: None | int = None,
    by_user_id: None | int = None,
    by_is_verified: None | bool = None,
    by_validation_statuses: None | list[str] = None,
    by_is_from_robot: None | bool = None,
) -> __schemas.Snapshot:
    """gets latest snapshot meta+body by specified filters. body is stored inside `json_data` attribute

    :param by_challenge_id: to what challenge shall snapshot belong? If None, any will match.
    :param by_user_id: to what user shall snapshot belong? If None, any will match.
    :param by_is_verified: shall the snapshot be moderator-approved? If None, any will match.
    :param by_validation_statuses: searched statuses of snapshot validation. If None, any will match.
    :param by_is_from_robot: shall the snapshot be generated from robot code run (True) or uploaded by human (False)? If None, any will match."""
    # at this point locals() will have dict of supplied args and their values
    meta = get_latest_meta(**locals())
    return __schemas.Snapshot(
        **meta.dict(),
        json_data=__get_body_by_url_or_id(
            is_loadable=meta.is_json_data_loadable,
            body_file_url=meta.json_data_file_url,
            snapshot_id=meta.id,
        ),
    )

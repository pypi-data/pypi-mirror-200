from datetime import datetime as _datetime
import typing as _typing

from pydantic import BaseModel as __BaseModel


class SnapshotMeta(__BaseModel):
    user_id: int
    challenge_id: int
    is_verified: bool = False
    verified_message: str | None
    date_created: _datetime
    internal_error: str | None  # might be removed in future. moderator attribute
    id: int
    is_from_code_run: bool
    challenge_name: str
    is_json_data_loadable: None | bool
    json_data_file_url: None | str


class Snapshot(SnapshotMeta):
    json_data: _typing.Any

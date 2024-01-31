from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from backend.core.config.const import max_change_num
from bson.objectid import ObjectId
from pydantic import Field, BaseConfig

@dataclass
class MainRes:
    @dataclass
    class Setting:
        subject: str
        period: int
        page: int
        start_time: list
        for_hours: int
        change_num: int
    @dataclass
    class Writing:
        id: str
        idx: int
        title: str
        created_at: str

    setting: Setting
    writings: list[Writing]
    can_write: bool
    total_writing: int
    max_change_num: int = max_change_num

@dataclass
class Writing:
    title: str
    desc: str

@dataclass
class WritingRes:
    idx: int
    title: str
    desc: str
    created_at: str
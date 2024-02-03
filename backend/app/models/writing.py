from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from backend.core.config.const import max_change_num
from bson.objectid import ObjectId
from pydantic import Field, BaseConfig
from pydantic import BaseModel

@dataclass
class MainRes:
    @dataclass
    class Setting:
        subject: str
        period: int
        page: int
        start_time: list
        for_hours: list
        change_num: int
    @dataclass
    class Writing:
        id: str
        idx: int
        created_at: list
        title: str|None=None
        desc: str|None=None

    setting: Setting
    writings: list[Writing]
    # can_write: bool
    total_writing: int
    start_date: str
    end_date: str
    d_day: str
    max_change_num: int = max_change_num

class Writing(BaseModel):
    title: str|None=None
    desc: str|None=None

@dataclass
class WritingRes:
    idx: int
    title: str
    desc: str
    created_at: str

@dataclass
class WritingInsertRes:
    idx: int = 0
    achieve_rate: int|None = None
    issued_badge: str|None = None
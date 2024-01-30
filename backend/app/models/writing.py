from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from backend.core.config.const import max_change_num

@dataclass
class MainRes:
    @dataclass
    class Setting:
        subject: str
        period: int
        page: int
        start_time: str
        for_hours: int
        change_num: int
    @dataclass
    class Writing:
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

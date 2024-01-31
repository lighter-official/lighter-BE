from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from backend.core.config.const import max_change_num

@dataclass
class Item:
    subject: str
    period: int
    page: int
    start_time: list
    for_hours: int

@dataclass
class Res:
    subject: str
    period: int
    page: int
    start_time: list
    for_hours: int
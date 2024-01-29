from dataclasses import dataclass, field
from datetime import datetime
from typing import Union

@dataclass
class Item:
    subject: str
    period: int
    page: int
    start_time: datetime
    for_hours: int

@dataclass
class Res:
    subject: str
    period: int
    page: int
    start_time: datetime
    for_hours: int

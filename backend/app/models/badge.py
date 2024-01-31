from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from backend.core.config.const import max_change_num
from bson.objectid import ObjectId
from pydantic import Field, BaseConfig

@dataclass
class Badge:
    user_id: str
    type: str
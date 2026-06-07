from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FileDTO:
    owner_id: int
    file_id: int
    file: str
    visible: bool
    created_at: datetime

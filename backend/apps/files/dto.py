from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FileDTO:
    owner_id: int
    id: int
    file: str
    visible: bool

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FileRepoDTO:
    owner_id: int
    id: int
    name: str
    file: str
    thumbnail: str | None
    created_at: datetime
    visible: bool

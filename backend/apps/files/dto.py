from dataclasses import dataclass
from datetime import datetime

from django.db.models import FileField


@dataclass(frozen=True)
class FileDTO:
    owner_id: int
    file_id: int
    file: FileField
    vizible: bool
    created_at: datetime

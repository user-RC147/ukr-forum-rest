from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReferralCodeOutDTO:
    owner: int
    code: str
    created_at: datetime
    expires_at: datetime
    is_active: datetime
    max_uses: int
    used_count: int

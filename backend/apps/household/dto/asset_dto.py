from dataclasses import dataclass

@dataclass(frozen=True)
class CreateAssetDTO:
    name:str
    group_id:int
    user_id: int                     # ID користувача, який створює (created_by)
    address_line: str | None = None  # Може бути рядком або None, за замовчуванням None

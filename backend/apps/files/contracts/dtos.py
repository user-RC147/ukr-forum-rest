from dataclasses import dataclass, field


@dataclass(frozen=True)
class FileDTO:
    owner_id: int
    id: int
    file: str
    thumbnail: str | None
    visible: bool


@dataclass(frozen=True)
class FileUpdatePlan:
    """Describes what to do with existing item_ids: keep as-is or update content."""

    keep_ids: list[int] = field(default_factory=list)
    update_ids: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        overlap = set(self.keep_ids) & set(self.update_ids)
        if overlap:
            raise ValueError(f"keep_ids and update_ids overlap: {overlap}")

    def touched_ids(self) -> set[int]:
        return set(self.keep_ids) | set(self.update_ids)

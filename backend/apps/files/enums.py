from enum import Enum


class FileExtentions(Enum):
    IMAGE = {
        "jpg",
        "png",
        "svg",
    }


EXT_TO_TYPE = {ext: member for member in FileExtentions for ext in member.value}

from enum import StrEnum, auto


class BaseStrEnum(StrEnum):

    @classmethod
    def values(cls):
        return [item.value for item in cls]


class RootEndpoints(BaseStrEnum):

    INDEX = auto()


class FileEndpoints(BaseStrEnum):

    DOWNLOAD = auto()
    UPLOAD = auto()

from enum import Enum


class Status(str, Enum):
    created = "CREATED"
    deleted = "DELETED"
    edited = "CHANGES_APPLIED"

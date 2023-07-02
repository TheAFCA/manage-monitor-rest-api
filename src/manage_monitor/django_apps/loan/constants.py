from enum import Enum


class Status(int, Enum):
    PENDING = 1
    ACTIVE = 2
    REJECTED = 3
    PAID = 4
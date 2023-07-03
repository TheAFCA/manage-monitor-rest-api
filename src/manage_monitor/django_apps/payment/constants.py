from enum import Enum

class Status(int, Enum):
    COMPLETED = 1
    REJECTED = 2
    PENDING = 3
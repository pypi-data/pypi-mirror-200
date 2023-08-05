from enum import Enum


class GateState(Enum):
    OPEN = 0
    ADJUSTING = 1
    CLOSED = 2
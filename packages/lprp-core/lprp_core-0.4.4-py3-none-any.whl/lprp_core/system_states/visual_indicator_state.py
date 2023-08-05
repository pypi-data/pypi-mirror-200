from enum import Enum


class VisualIndicatorState(Enum):
    OPEN = 0
    PROCESSING = 1
    CLOSED = 2
    ERROR = 3
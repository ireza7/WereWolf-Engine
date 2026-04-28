from enum import Enum, auto

class Phase(Enum):
    LOBBY = auto()
    NIGHT = auto()
    DAY = auto()
    END = auto()
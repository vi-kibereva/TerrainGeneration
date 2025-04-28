from enum import Enum
from typing import Any


class CellTypes(Enum):
    WATER = 0
    SAND = 1
    GRASS = 2
    FOREST = 3
    PLATEAU = 4


CELL_RANGES: dict[Any, tuple[int, int]] = {
    CellTypes.WATER: (0, 7),
    CellTypes.SAND: (8, 14),
    CellTypes.GRASS: (15, 23),
    CellTypes.FOREST: (24, 28),
    CellTypes.PLATEAU: (29, 36),
}

MAX_RANGE = 36


class Cell:
    """
    Class for cells
    """

    MAX_AGE = 10

    def __init__(self, type_=CellTypes.WATER, age=0):
        self.type_ = type_
        self.age = age

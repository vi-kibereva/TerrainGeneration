from enum import Enum
from typing import Any


class CellTypes(Enum):
    WATER = 0
    LAND = 1
    MOUNTAIN = 2


CELL_RANGES: dict[Any, tuple[int, int]] = {
    CellTypes.WATER: (0, 6),
    CellTypes.LAND: (7, 12),
    CellTypes.MOUNTAIN: (13, 18)
}

MAX_RANGE = 36


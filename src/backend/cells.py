from enum import IntEnum
from typing import Any

import numpy as np


class CellTypes(IntEnum):
    WATER = 0
    LAND = 2
    MOUNTAIN = 3



CELL_RANGES: dict[Any, tuple[int, int]] = {
    CellTypes.WATER: (0, 6),
    CellTypes.LAND: (7, 12),
    CellTypes.MOUNTAIN: (13, 18),
}

MAX_RANGE = 36


CELL_LUT = np.empty(MAX_RANGE + 1, dtype=np.int8)

CELL_LUT[0 : 10] = CellTypes.WATER.value
CELL_LUT[10 : 20 ] = CellTypes.LAND.value
CELL_LUT[20 : 999] = CellTypes.MOUNTAIN.value

class WaterType(IntEnum):
    VERYDEEP = 0
    DEEP = 1
    MODERATE = 2
    SHALLOW = 3

class LandType(IntEnum):
    SAND = 0
    GRASS = 1
    FOREST = 2
    HILL = 3

class MountainType(IntEnum):
    LOW = 0
    MODERATE = 1
    HIGH = 2
    SNOWY = 3
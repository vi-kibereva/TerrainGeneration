from enum import IntEnum
from typing import Any

import numpy as np


class CellTypes(IntEnum):
    WATER = 0
    LAND = 3
    MOUNTAIN = 4


CELL_RANGES: dict[Any, tuple[int, int]] = {
    CellTypes.WATER: (0, 6),
    CellTypes.LAND: (7, 12),
    CellTypes.MOUNTAIN: (13, 18),
}

MAX_RANGE = 36


CELL_LUT = np.empty(MAX_RANGE + 1, dtype=np.int8)

CELL_LUT[0 : 11 + 1] = CellTypes.WATER.value
CELL_LUT[12 : 26 + 1] = CellTypes.LAND.value
CELL_LUT[27 : 63 + 1] = CellTypes.MOUNTAIN.value

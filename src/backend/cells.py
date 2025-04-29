from enum import IntEnum
from typing import Any

import numpy as np


class CellTypes(IntEnum):
    WATER = 0
    LAND = 1
    MOUNTAIN = 2


CELL_RANGES: dict[Any, tuple[int, int]] = {
    CellTypes.WATER: (0, 6),
    CellTypes.LAND: (7, 12),
    CellTypes.MOUNTAIN: (13, 18),
}

MAX_RANGE = 36


CELL_LUT = np.empty(MAX_RANGE + 1, dtype=np.int8)

CELL_LUT[0 : 6 + 1] = CellTypes.WATER.value
CELL_LUT[7 : 12 + 1] = CellTypes.LAND.value
CELL_LUT[13 : 18 + 1] = CellTypes.MOUNTAIN.value

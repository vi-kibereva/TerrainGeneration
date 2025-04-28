from enum import IntEnum
from typing import Any

import numpy as np


class CellTypes(IntEnum):
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

CELL_LUT = np.empty(MAX_RANGE + 1, dtype=np.int8)

CELL_LUT[0 : 7 + 1] = CellTypes.WATER.value
CELL_LUT[8 : 14 + 1] = CellTypes.SAND.value
CELL_LUT[15 : 23 + 1] = CellTypes.GRASS.value
CELL_LUT[24 : 28 + 1] = CellTypes.FOREST.value
CELL_LUT[29 : 36 + 1] = CellTypes.PLATEAU.value

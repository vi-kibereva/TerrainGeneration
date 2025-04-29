"""the chunk module"""

import random
from enum import Enum, auto
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike

from src.utils import Singleton
from .evolution import generate_chunk
from .cells import MAX_RANGE, CELL_LUT

if TYPE_CHECKING:
    from .grid import Grid

"""the size of the side of the chunk"""
CHUNK_SIZE: int = 16


class ChunkStates(Enum):
    GENERATED = auto()
    NOT_GENERATED = auto()
    VOID = auto()


class Chunk:
    def __init__(self, density: float = 0.5) -> None:
        self.__cells: np.ndarray = np.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype=np.int8)
        self.__generate_random(density)

        self.state = ChunkStates.NOT_GENERATED

    @property
    def cells(self) -> ArrayLike:
        return self.__cells

    def __generate_random(self, density: float) -> None:
        mask: np.ndarray = np.random.random((CHUNK_SIZE, CHUNK_SIZE)) < density

        raw = np.random.randint(0, MAX_RANGE + 1, size=mask.sum(), dtype=np.int8)
        self.__cells[mask] = CELL_LUT[raw]

    def generate_self(self, grid: Grid, pos: tuple[int, int]) -> None:
        x, y = pos

        lu_chunk: Chunk = grid[x - 1, y + 1]
        lm_chunk: Chunk = grid[x - 1, y]
        ld_chunk: Chunk = grid[x - 1, y - 1]

        left_stripe: np.ndarray = np.concat(
            (lu_chunk.cells, lm_chunk.cells, ld_chunk.cells), axis=1
        )

        mu_chunk: Chunk = grid[x, y + 1]
        md_chunk: Chunk = grid[x, y - 1]

        middle_stripe: np.ndarray = np.concat(
            (mu_chunk.cells, self.cells, md_chunk.cells), axis=1
        )

        ru_chunk: Chunk = grid[x + 1, y + 1]
        rm_chunk: Chunk = grid[x + 1, y + 1]
        rd_chunk: Chunk = grid[x + 1, y + 1]

        right_stripe: np.ndarray = np.concat(
            (ru_chunk.cells, rm_chunk.cells, rd_chunk.cells), axis=1
        )

        concatenated: np.ndarray = np.concat(
            (left_stripe, middle_stripe, right_stripe), axis=0
        )

        self.__cells = generate_chunk(concatenated)
        self.state = ChunkStates.GENERATED


class NoneChunk(Chunk, metaclass=Singleton):
    def __init__(self) -> None:
        self.__cells: ArrayLike = np.empty((0, 0))
        self.state = ChunkStates.VOID

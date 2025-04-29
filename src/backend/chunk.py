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
    def cells(self) -> np.ndarray:
        return self.__cells

    def __generate_random(self, density: float) -> None:
        mask: np.ndarray = np.random.random((CHUNK_SIZE, CHUNK_SIZE)) < density

        raw = np.random.randint(0, MAX_RANGE + 1, size=mask.sum(), dtype=np.int8)
        self.__cells[mask] = CELL_LUT[raw]

    def generate_self(self, grid: "Grid", pos: tuple[int, int]) -> None:
        x, y = pos
        padded = np.zeros((CHUNK_SIZE + 2, CHUNK_SIZE + 2), dtype=np.int8)

        # 1) copy your existing random cells into the center
        padded[1:-1, 1:-1] = self.__cells

        # 2) overwrite the edges from neighbours (as you already do)
        padded[0, 1:-1] = grid[x, y + 1].cells[-1, :]
        padded[-1, 1:-1] = grid[x, y - 1].cells[0, :]
        padded[1:-1, 0] = grid[x - 1, y].cells[:, -1]
        padded[1:-1, -1] = grid[x + 1, y].cells[:, 0]
        padded[0, 0] = grid[x - 1, y + 1].cells[-1, -1]
        padded[0, -1] = grid[x + 1, y + 1].cells[-1, 0]
        padded[-1, 0] = grid[x - 1, y - 1].cells[0, -1]
        padded[-1, -1] = grid[x + 1, y - 1].cells[0, 0]

        print(f"generating chunk{self.state}: {padded}")

        # 3) evolve it
        self.__cells = generate_chunk(padded)
        self.state = ChunkStates.GENERATED

        print(f"Complete chunk{self.state}: {padded}")


class NoneChunk(Chunk, metaclass=Singleton):
    def __init__(self) -> None:
        self.__cells: ArrayLike = np.empty((0, 0))
        self.state = ChunkStates.VOID

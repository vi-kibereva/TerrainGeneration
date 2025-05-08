"""the chunk module"""

from enum import Enum, auto
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike

from src.utils import Singleton
from .evolution import pre_generate_chunk, generate_chunk_biome, textures
from .cells import MAX_RANGE, CELL_LUT

if TYPE_CHECKING:
    from .grid import Grid

"""the size of the side of the chunk"""
CHUNK_SIZE: int = 16


class ChunkStates(Enum):
    GENERATED = auto()
    PRE_GENERATED = auto()
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

    def generate_self(
        self, grid: "Grid", pos: tuple[int, int], texture_density: float = 0.3
    ) -> None:
        x, y = pos

        padded = np.zeros((CHUNK_SIZE + 2, CHUNK_SIZE + 2), dtype=np.int8)
        padded[1:-1, 1:-1] = self.__cells

        padded[0, 1:-1] = grid[x, y + 1].cells[-1, :]
        padded[-1, 1:-1] = grid[x, y - 1].cells[0, :]
        padded[1:-1, 0] = grid[x - 1, y].cells[:, -1]
        padded[1:-1, -1] = grid[x + 1, y].cells[:, 0]
        padded[0, 0] = grid[x - 1, y + 1].cells[-1, -1]
        padded[0, -1] = grid[x + 1, y + 1].cells[-1, 0]
        padded[-1, 0] = grid[x - 1, y - 1].cells[0, -1]
        padded[-1, -1] = grid[x + 1, y - 1].cells[0, 0]

        self.__cells = generate_chunk_biome(padded)
        self.__cells = textures(self.__cells, density=texture_density)

        self.state = ChunkStates.GENERATED

    def pre_generate_self(self, grid: "Grid", pos: tuple[int, int]) -> None:
        x, y = pos

        padded = np.zeros((CHUNK_SIZE + 2, CHUNK_SIZE + 2), dtype=np.int8)
        padded[1:-1, 1:-1] = self.__cells

        padded[0, 1:-1] = grid[x, y + 1].cells[-1, :]
        padded[-1, 1:-1] = grid[x, y - 1].cells[0, :]
        padded[1:-1, 0] = grid[x - 1, y].cells[:, -1]
        padded[1:-1, -1] = grid[x + 1, y].cells[:, 0]
        padded[0, 0] = grid[x - 1, y + 1].cells[-1, -1]
        padded[0, -1] = grid[x + 1, y + 1].cells[-1, 0]
        padded[-1, 0] = grid[x - 1, y - 1].cells[0, -1]
        padded[-1, -1] = grid[x + 1, y - 1].cells[0, 0]

        self.__cells = pre_generate_chunk(padded)
        self.state = ChunkStates.PRE_GENERATED


class NoneChunk(Chunk, metaclass=Singleton):
    def __init__(self) -> None:
        self.__cells: ArrayLike = np.empty((0, 0))
        self.state = ChunkStates.VOID

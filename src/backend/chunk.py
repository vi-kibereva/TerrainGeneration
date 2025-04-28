"""the chunk module"""

import random
from enum import Enum, auto
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike

from src.utils import Singleton
from .evolution import generate_chunk

if TYPE_CHECKING:
    from .grid import Grid

"""the size of the side of the chunk"""
CHUNK_SIZE: int = 16


class ChunkStates(Enum):
    GENERATED = auto()
    NOT_GENERATED = auto()
    VOID = auto()


class Chunk:
    def __init__(self) -> None:
        self.__cells: ArrayLike = np.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype=np.int8)
        self.state = ChunkStates.NOT_GENERATED

    @property
    def cells(self) -> ArrayLike:
        return self.__cells

    def generate_self(self, grid: Grid) -> None:
        self.state = ChunkStates.GENERATED

    def __generate_random(self, density: float) -> None:
        mask = np.random.random((CHUNK_SIZE, CHUNK_SIZE)) < density
        random = np.random.randint(())


class NoneChunk(Chunk, metaclass=Singleton):
    def __init__(self) -> None:
        self.__cells: ArrayLike = np.empty((0, 0))
        self.state = ChunkStates.VOID

from typing import TYPE_CHECKING

from numpy.typing import ArrayLike

if TYPE_CHECKING:
    from .chunk import Chunk, NoneChunk


class Grid:
    def __init__(self) -> None:
        self.__chunks: dict[tuple[int, int], Chunk] = dict()

    def __getitem__(self, item: tuple[int, int]) -> Chunk:
        return self.__chunks.get(item, NoneChunk())

    @property
    def chunks(self) -> dict[tuple[int, int], Chunk]:
        return self.__chunks

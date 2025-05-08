from collections.abc import Generator

from .chunk import ChunkStates, Chunk, NoneChunk


class Grid:
    def __init__(self, density: float) -> None:
        self.__chunks: dict[tuple[int, int], Chunk] = dict()
        self.__density: float = density

    def __getitem__(self, item: tuple[int, int]) -> Chunk:
        return self.__chunks.get(item, NoneChunk())

    @property
    def chunks(self) -> dict[tuple[int, int], Chunk]:
        return self.__chunks

    def generate_around(self, pos: tuple[int, int], generated_radius: int) -> None:
        if generated_radius <= 1:
            raise ValueError("generated_radius must be at least 2")

        pre_generated_radius = generated_radius + 4
        noise_radius = pre_generated_radius + 2

        self._create_random_chunks(pos, noise_radius)
        self._pre_generate_chunks(pos, pre_generated_radius)
        self._generate_chunks(pos, generated_radius)

    def _create_random_chunks(self, pos: tuple[int, int], radius: int):
        for chunk, pos in self._get_chunks_in_radius(pos, radius):
            if chunk is NoneChunk():
                self.__chunks[pos] = Chunk(self.__density)

    def _pre_generate_chunks(self, pos: tuple[int, int], radius: int):
        for chunk, pos in self._get_chunks_in_radius(pos, radius):
            if chunk.state.value == ChunkStates.NOT_GENERATED.value:
                chunk.pre_generate_self(self, pos)

    def _generate_chunks(self, pos: tuple[int, int], radius: int):
        for chunk, pos in self._get_chunks_in_radius(pos, radius):
            if chunk.state.value == ChunkStates.PRE_GENERATED.value:
                chunk.generate_self(self, pos)

    def _get_chunks_in_radius(
        self, pos: tuple[int, int], radius: int
    ) -> Generator[tuple[Chunk, tuple[int, int]]]:
        """get chunks in radius (diamond shape)"""
        x, y = pos

        for i in range(1, radius):
            for j in range(-radius + i + 1, radius - i):
                yield self[x - i, y + j], (x - i, y + j)

        for i in range(radius):
            for j in range(-radius + i + 1, radius - i):
                yield self[x + i, y + j], (x + i, y + j)

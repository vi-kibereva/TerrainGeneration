import numpy as np
from scipy.signal import convolve2d
from .cells import CELL_LUT
from copy import copy


NUMBER_OF_ITERATIONS = 10
KERNEL = np.ones((3, 3), dtype=np.int8)
BIOME_KERNEL = np.full((5, 5), 1 / 25, dtype=np.float32)
BIOME_KERNEL_GAUSS = np.array(
    [
        [0.00390625, 0.015625, 0.0234375, 0.015625, 0.00390625],
        [0.015625, 0.0625, 0.09375, 0.0625, 0.015625],
        [0.0234375, 0.09375, 0.140625, 0.09375, 0.0234375],
        [0.015625, 0.0625, 0.09375, 0.0625, 0.015625],
        [0.00390625, 0.015625, 0.0234375, 0.015625, 0.00390625],
    ]
)
CHUNK_SIZE = 16
DENSITY = 0.7


def evolve(bigger_chunk: np.ndarray) -> None:
    """
    Generates terrain
    """
    convolved = convolve2d(bigger_chunk, KERNEL, mode="valid")
    bigger_chunk[1:-1, 1:-1] = CELL_LUT[convolved]


def pre_generate_chunk(
    bigger_chunk: np.ndarray, iterations: int = NUMBER_OF_ITERATIONS
) -> np.ndarray:
    """Runs evolve a number of times"""
    for _ in range(iterations):
        evolve(bigger_chunk)
    return bigger_chunk[1:-1, 1:-1]


def get_biome(terrain: int, value: np.ndarray) -> int:
    """
    Generates biome for the cell
    """
    probs = value / value.sum()
    biome = np.random.choice((0, 1, 2, 3), p=probs)

    return (biome << 2) | terrain


def biome_evolve(bigger_chunk: np.ndarray) -> None:
    """
    Convolution-like generation for biome
    """
    bigger_chunk = copy(bigger_chunk)
    terrain: np.ndarray = bigger_chunk & 0b11
    biome = (bigger_chunk & 0b1100) >> 2
    size = CHUNK_SIZE
    result = np.zeros((size, size), dtype=np.int8)
    for i in range(size):
        for j in range(size):
            value = np.zeros(4, dtype=np.float32)
            for k in range(0, 5):
                for m in range(0, 5):
                    if terrain[i, j] != terrain[i + k, j + m]:
                        biome_idx: np.int8 = biome[i, j]
                    else:
                        biome_idx: np.int8 = biome[i + k, j + m]
                    value[biome_idx] += 1 * BIOME_KERNEL[k, m]
            result = get_biome(bigger_chunk[i, j], value)
    bigger_chunk[2:-2, 2:-2] = result


def generate_chunk_biome(bigger_chunk: np.ndarray) -> np.ndarray:
    """
    Generates chunk biome
    """
    noise = np.random.randint(0, 4, size=(CHUNK_SIZE+4, CHUNK_SIZE+4))
    bigger_chunk = (noise << 2) | bigger_chunk
    for _ in range(NUMBER_OF_ITERATIONS):
        biome_evolve(bigger_chunk)
    return bigger_chunk[2:-2, 2:-2]

def textures(chunk: np.ndarray, density: float) -> np.ndarray:
    """
    Adds textures
    """
    mask: np.ndarray = np.random.rand(CHUNK_SIZE, CHUNK_SIZE) < density
    textures: np.ndarray = (
        np.random.choice((1, 2, 3), size=(CHUNK_SIZE, CHUNK_SIZE)) << 4
    )

    return chunk | textures * mask

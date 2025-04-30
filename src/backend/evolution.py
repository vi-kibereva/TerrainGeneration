import numpy as np
from scipy.signal import convolve2d
# from .cells import CELL_LUT
from numba import njit, prange

NUMBER_OF_ITERATIONS = 10
KERNEL = np.ones((3, 3), dtype=int)
KERNEL2 = np.full((5, 5), 1/25)
CHUNK_SIZE = 16


def evolve(bigger_chunk: np.ndarray) -> None:
    convolved = convolve2d(bigger_chunk, KERNEL, mode="valid")
    bigger_chunk[1:-1, 1:-1] = CELL_LUT[convolved]


def generate_chunk(bigger_chunk: np.ndarray) -> np.ndarray:
    """Runs evolve a number of times"""
    for _ in range(NUMBER_OF_ITERATIONS):
        evolve(bigger_chunk)
    return bigger_chunk[1:-1, 1:-1]

def get_biome(terrain:int, value:np.ndarray) -> int:
    return 1


@njit(parallel=True, fastmath=True)
def biome_evolution(bigger_chunk:np.ndarray) -> np.ndarray:
    terrain = bigger_chunk & 0b11
    biome = (bigger_chunk & 0b1100) >> 2
    size = CHUNK_SIZE
    result = np.zeros((size, size), dtype=np.int8)
    for i in prange(size):
        for j in range(size):
            value = np.zeros(4, dtype=np.float32)
            for ii in range(0, 5):
                for jj in range(0, 5):
                    # acc += bigger_chunk[i + ii, j + jj] * KERNEL2[5 - 1 - ii, 5 - 1 - jj]
                    biome_idx = int(biome[i + ii, j + jj])
                    value[biome_idx] += 1 * KERNEL2[ii, jj]
            # result[i, j] = get_biome(terrain[i, j], value)
    return result

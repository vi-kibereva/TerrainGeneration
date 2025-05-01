import numpy as np
from scipy.signal import convolve2d
from .cells import CELL_LUT, CellTypes
from numba import njit, prange

NUMBER_OF_ITERATIONS = 10
KERNEL = np.ones((3, 3), dtype=np.int8)
BIOME_KERNEL = np.full((5, 5), 1/25, dtype=np.float32)
BIOME_KERNEL_GAUSS = np.array([
    [0.00390625, 0.015625  , 0.0234375 , 0.015625  , 0.00390625],
    [0.015625  , 0.0625    , 0.09375   , 0.0625    , 0.015625  ],
    [0.0234375 , 0.09375   , 0.140625  , 0.09375   , 0.0234375 ],
    [0.015625  , 0.0625    , 0.09375   , 0.0625    , 0.015625  ],
    [0.00390625, 0.015625  , 0.0234375 , 0.015625  , 0.00390625]
])
CHUNK_SIZE = 16
DENSITY = 0.7


def evolve(bigger_chunk: np.ndarray) -> None:
    convolved = convolve2d(bigger_chunk, KERNEL, mode="valid")
    bigger_chunk[1:-1, 1:-1] = CELL_LUT[convolved]


def generate_chunk(bigger_chunk: np.ndarray) -> np.ndarray:
    """Runs evolve a number of times"""
    for _ in range(NUMBER_OF_ITERATIONS):
        evolve(bigger_chunk)
    return bigger_chunk[1:-1, 1:-1]

def get_biome(terrain:int, value:np.ndarray) -> int:
    probs = value / value.sum()
    biome = np.random.choice(4, p=probs)
    return (biome << 2) | terrain
    

@njit(parallel=True, fastmath=True)
def biome_evolve(bigger_chunk:np.ndarray) -> np.ndarray:
    terrain: np.ndarray = bigger_chunk & 0b11
    biome = (bigger_chunk & 0b1100) >> 2
    size = CHUNK_SIZE
    result = np.zeros((size, size), dtype=np.int8)
    for i in prange(size):
        for j in range(size):
            value = np.zeros(4, dtype=np.float32)
            for k in range(0, 5):
                for m in range(0, 5):
                    # acc += bigger_chunk[i + k, j + m] * BIOME_KERNEL[5 - 1 - k, 5 - 1 - m]
                    if terrain[i, j] != terrain[i+k, j+k]:
                        result[i, j] = biome[i, j]
                    else:
                        biome_idx: np.int8 = biome[i + k, j + m]
                        value[biome_idx] += 1 * BIOME_KERNEL[k, m]
    bigger_chunk[1:-1, 1:-1] = result

def generate_chunk_biome(bigger_chunk:np.ndarray) -> np.ndarray:
    for _ in range(NUMBER_OF_ITERATIONS):
        biome_evolve(bigger_chunk)
    return bigger_chunk


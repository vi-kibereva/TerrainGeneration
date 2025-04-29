import numpy as np
from scipy.signal import convolve2d
from .cells import CELL_LUT

NUMBER_OF_ITERATIONS = 10
KERNEL = np.ones((3, 3), dtype=int)


def evolve(bigger_chunk: np.ndarray) -> None:
    convolved = convolve2d(bigger_chunk, KERNEL, mode="valid")
    bigger_chunk[1:-1, 1:-1] = CELL_LUT[convolved]


def generate_chunk(bigger_chunk: np.ndarray) -> np.ndarray:
    """Runs evolve a number of times"""
    for _ in range(NUMBER_OF_ITERATIONS):
        evolve(bigger_chunk)
    return bigger_chunk[1:-1, 1:-1]

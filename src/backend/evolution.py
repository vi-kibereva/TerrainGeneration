import numpy as np
from scipy.signal import convolve2d
from .cells import CELL_RANGES
NUMBER_OF_ITERATIONS = 20

def evolve(bigger_chunk):
    '''
    Takes bigger_chunk and changes it to the next gen
    '''
    kernel = np.ones((3, 3), dtype=int)
    convolved = convolve2d(bigger_chunk, kernel, mode='valid')
    smaller_chunk = bigger_chunk[1:-1, 1:-1]
    for cell_type, (low, high) in CELL_RANGES.items():
        mask = (convolved >= low) & (convolved <= high)
        smaller_chunk[mask] = cell_type.value

def generate_chunk(bigger_chunk):
    '''
    Runs evolve a number of times
    '''
    for _ in range(NUMBER_OF_ITERATIONS):
        evolve(bigger_chunk)
    return bigger_chunk[1:-1, 1:-1]


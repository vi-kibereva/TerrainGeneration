from numpy.typing import ArrayLike
import numpy as np
def evolve(bigger_chunk):
    CHUNK_SIZE = 16
    result = np.array((CHUNK_SIZE, CHUNK_SIZE), dtype=np.int8)
    NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1) ,(0, -1)]
    for i in range(1, CHUNK_SIZE-1):
        for j in range(1, CHUNK_SIZE-1):
            counter = sum(bigger_chunk[k][m].type_ for (k, m) in NEIGHBORS)

def generate_chunk(bigger_chunk): 
    ...
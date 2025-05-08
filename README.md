# TerrainGeneration

A customizable Minecraft-inspired application that simulates procedural terrain generation using cellular automata in Python. This project leverages discrete mathematics principles, specifically automata theory, to create diverse and realistic terrain with various biomes. Users can generate unique worlds using seed mechanics and adjust generation parameters for a personalized experience.

## Contents

* [Features](#features)
* [Installation](#installation)
* [How It Works](#how-it-works)
* [Developers and Responsibilities](#developers-and-responsibilities)

## Features

* **Procedural Terrain Generation**: Uses cellular automata to simulate the creation of diverse terrain.
* **Biome Variety**: Different biomes can be generated, offering realistic and varied landscapes.
* **Seed Mechanics**: Allows users to create unique worlds based on specific seeds.
* **Customizable Parameters**: Users can adjust terrain generation parameters for different effects.

## Installation

To install and run the application, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/vi-kibereva/TerrainGeneration.git
   ```

2. Navigate to the project directory:

   ```bash
   cd TerrainGeneration
   ```

3. Install the required dependencies:

   ```bash
   pip install -r pyproject.toml
   ```

4. Run the application:

   ```bash
   python3 -m src.main
   ```

## How It Works

### Architecture Overview

The project consists of three main modules:

1. **`grid.py`** – Manages a grid of chunks (16×16 cell blocks) and coordinates their generation around a given position.
2. **`chunk.py`** – Defines the `Chunk` class, which holds cell data and supports two-stage generation: pre-generation and final generation.
3. **`evolution.py`** – Implements terrain evolution, biome formation, and texture layering using convolution-based cellular automata.

---

### 1. Grid (`grid.py`)

* **Initialization**
  On `Grid(density: float)`, the density parameter determines the initial fill probability for each chunk, and an internal dictionary `__chunks` is created to store generated chunks.

* **Accessing Chunks**

  * `grid[(x, y)]` returns the `Chunk` at coordinates `(x, y)` or a `NoneChunk` if none exists.
  * The `chunks` property provides the map of all generated chunks as `{(x, y): Chunk}`.

* **generate\_around(pos, generated\_radius)**
  Generates chunks in three phases around the center `pos = (x, y)` with an active radius `generated_radius` (must be ≥ 2):

  1. **\_create\_random\_chunks**: Fills empty positions in a diamond-shaped radius of `generated_radius + 6` with new `Chunk` instances initialized with random cells based on the grid’s density.
  2. **\_pre\_generate\_chunks**: For each newly created chunk within `generated_radius + 4`, calls `pre_generate_self`, which applies initial smoothing (10 iterations of a 3×3 convolution).
  3. **\_generate\_chunks**: Within the active `generated_radius`, calls `generate_self` on each chunk to finalize biome and texture generation.

* **\_get\_chunks\_in\_radius(pos, radius)**
  A private generator that yields `(chunk, (x, y))` pairs over a diamond-shaped area defined by `radius`, used in the above phases.

---

### 2. Chunk (`chunk.py`)

* **States**

  ```python
  class ChunkStates(Enum):
      GENERATED = auto()
      PRE_GENERATED = auto()
      NOT_GENERATED = auto()
      VOID = auto()
  ```

* **Initialization**

  * Allocates a `16×16` integer array `__cells`.
  * Populates it randomly based on the density parameter (`__generate_random`).
  * Sets `state = NOT_GENERATED`.

* **pre\_generate\_self(grid, pos)**

  * Pads `__cells` to size `18×18` by sampling one-row/one-column strips from neighbors in the grid.
  * Calls `pre_generate_chunk`, which performs 10 iterations of a 3×3 convolution-based smoothing, then extracts the central `16×16` back into `__cells`.
  * Updates `state = PRE_GENERATED`.

* **generate\_self(grid, pos, texture\_density=0.3)**

  * Pads to `20×20` by taking two rows/columns from each of the eight neighboring chunks.
  * Runs `generate_chunk_biome`, which adds 2 bits of random noise and performs 100 iterations of a 5×5 convolution-based biome evolution.
  * Applies `textures`, layering random texture markers (upper bits) according to `texture_density`.
  * Updates `state = GENERATED`.

* **NoneChunk**
  A singleton representing absent chunks, with empty cell data and `state = VOID`.

---

### 3. Evolution Algorithms (`evolution.py`)

* **Constants**

  * `NUMBER_OF_ITERATIONS = 10` (initial smoothing passes)
  * `KERNEL = np.ones((3,3))` for terrain evolution
  * `BIOME_KERNEL` (uniform 5×5) and `BIOME_KERNEL_GAUSS` (Gaussian weights) for biome blending

* **evolve(bigger\_chunk)**
  Applies a valid-mode 3×3 convolution to `bigger_chunk`, updating its central region using a cell lookup table (`CELL_LUT`).

* **pre\_generate\_chunk(bigger\_chunk, iterations)**
  Repeats `evolve` for the given number of iterations, then returns the central `16×16` slice.

* **generate\_chunk\_biome(bigger\_chunk)**

  * Adds 2 bits of random noise to each cell.
  * Runs 100 passes of `biome_evolve`, which computes weighted biome probabilities over a 5×5 neighborhood and randomly selects a biome for each cell.
  * Returns the central `16×16` slice with both terrain and biome bits.

* **textures(chunk, density)**
  Creates a boolean mask of size `16×16` by sampling `< density`, then overlays random texture bits (`1<<4`, `2<<4`, or `3<<4`) on masked positions.

---

## Example Usage

```python
from src.grid import Grid

# Create a grid with 60% fill density
grid = Grid(density=0.6)

# Generate chunks within radius 5 around (0, 0)
grid.generate_around(pos=(0, 0), generated_radius=5)

# Access the cell array of the center chunk
center_cells = grid[(0, 0)].cells
print(center_cells)
```


## Developers and Responsibilities

* **Viktoria Kibyeryeva** ([@vi-kibereva](https://github.com/vi-kibereva)) - Backend
* **Stanislav Konovalenko** ([@weqpro](https://github.com/weqpro)) - Backend
* **Daryna Nychyporuk** ([@dd8ria](https://github.com/dd8ria)) - UI
* **Anastasia Liubenchuk** ([@saudeawd](https://github.com/saudeawd)) - UI

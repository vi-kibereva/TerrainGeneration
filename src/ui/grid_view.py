from PySide6 import QtCore, QtGui, QtWidgets
from typing import TYPE_CHECKING
from math import floor
import random

if TYPE_CHECKING:
    from src.backend.grid import Grid
from src.backend.chunk import CHUNK_SIZE, ChunkStates, MAX_RANGE

class GridView(QtWidgets.QWidget):
    """
    Відображає сітку та персонажа з камерою, що слідує за ним.
    Додає можливість зуму та догенерацію чанків.
    """
    PLAYER_SCALE = 4.5
    GENERATE_RADIUS = 2
    NOISE_RADIUS = 5
    WATER_THRESHOLD = MAX_RANGE * 0.3

    def __init__(self, grid: 'Grid', cells_w=50, cells_h=50, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.cells_w = cells_w
        self.cells_h = cells_h
        self.player_pixmap = QtGui.QPixmap("src/ui/chelik.png")
        self.zoom = 1.0
        self.player_position = self.find_land_position()
        self.current_chunk = (0, 0)

        # Початкова генерація навколо в main перед створенням GridView
        self._ensure_chunks()
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def set_zoom(self, value: float):
        self.zoom = value
        self.update()

    def generate_grid(self, seed, density):
        random.seed(seed)
        if hasattr(self.grid, 'density'):
            self.grid.density = density
        if hasattr(self.grid, 'clear'):
            self.grid.clear()
        self.current_chunk = (0, 0)
        self._ensure_chunks()  # генеруємо навколо (0, 0)
        self.player_position = self.find_land_position()  # лише після генерації!
        self.current_chunk = (
            floor(self.player_position[0] / CHUNK_SIZE),
            floor(self.player_position[1] / CHUNK_SIZE)
        )
        self._ensure_chunks()  # вдруг щось нове
        self.update()

    def clear_grid(self):
        if hasattr(self.grid, 'clear'):
            self.grid.clear()
        self.current_chunk = (0, 0)
        self._ensure_chunks()  # Спочатку генеруємо чанки
        self.player_position = self.find_land_position()  # Потім шукаємо сушу
        self.current_chunk = (
            floor(self.player_position[0] / CHUNK_SIZE),
            floor(self.player_position[1] / CHUNK_SIZE)
        )
        self._ensure_chunks()  # Генеруємо навколо нової позиції
        self.update()

    def _is_water(self, gx, gy) -> bool:
        cx, cy = floor(gx / CHUNK_SIZE), floor(gy / CHUNK_SIZE)
        ix, iy = int(gx - cx * CHUNK_SIZE), int(gy - cy * CHUNK_SIZE)
        try:
            chunk = self.grid[(cx, cy)]
        except KeyError:
            return True
        if chunk.state == ChunkStates.VOID:
            return True
        return int(chunk.cells[ix, iy]) < self.WATER_THRESHOLD

    def _ensure_chunks(self):
        # Генеруємо чанки навколо поточної позиції
        self.grid.generate_around(
            self.current_chunk,
            generated_radius=self.GENERATE_RADIUS,
            noise_radius=self.NOISE_RADIUS
        )

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)  # << ДОДАЙ ЦЕ, щоб не малювалися контури
        w, h = self.width(), self.height()
        base_w, base_h = w / self.cells_w, h / self.cells_h
        cw, ch = base_w * self.zoom, base_h * self.zoom

        center_x, center_y = w / 2, h / 2
        ox = self.player_position[0] - (center_x / cw)
        oy = self.player_position[1] - (center_y / ch)

        num_cols = int(w / cw) + 2
        num_rows = int(h / ch) + 2
        start_col = int(floor(ox))
        start_row = int(floor(oy))

        for row in range(num_rows):
            for col in range(num_cols):
                gx = start_col + col
                gy = start_row + row
                cx, cy = floor(gx / CHUNK_SIZE), floor(gy / CHUNK_SIZE)
                ix, iy = int(gx - cx * CHUNK_SIZE), int(gy - cy * CHUNK_SIZE)
                try:
                    chunk = self.grid[(cx, cy)]
                except KeyError:
                    chunk = None
                if not chunk or chunk.state == ChunkStates.VOID:
                    color = QtGui.QColor(50, 50, 50)
                else:
                    val = int(chunk.cells[ix, iy])
                    t = val / (MAX_RANGE / 9)
                    if t < 0.5:
                        u = t / 0.5
                        color = QtGui.QColor(0, int(255 * u), int(255 * (1 - u)))
                    else:
                        u = (t - 0.5) / 0.5
                        color = QtGui.QColor(int(139 * u), int(255 - 186 * u), 0)

                px = (col * cw) - ((ox - start_col) * cw)
                py = (row * ch) - ((oy - start_row) * ch)
                # Малюємо клітинку без сітки
                painter.fillRect(QtCore.QRectF(px, py, cw + 1, ch + 1), color)  # +1 — щоб не лишався міжпіксельний проміжок
        size = int(min(cw, ch) * self.PLAYER_SCALE)
        scaled = self.player_pixmap.scaled(
            size, size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(
            int(center_x - size/2), int(center_y - size/2), scaled
        )

    def keyPressEvent(self, event):
        moves = {
            QtCore.Qt.Key_Up: (0, -1),
            QtCore.Qt.Key_Down: (0, 1),
            QtCore.Qt.Key_Left: (-1, 0),
            QtCore.Qt.Key_Right: (1, 0)
        }
        if event.key() in moves:
            dx, dy = moves[event.key()]
            self.player_position[0] += dx
            self.player_position[1] += dy
            new_chunk = (
                floor(self.player_position[0] / CHUNK_SIZE),
                floor(self.player_position[1] / CHUNK_SIZE)
            )
            if new_chunk != self.current_chunk:
                self.current_chunk = new_chunk
                self._ensure_chunks()
            self.update()

    def find_land_position(self):
        """Шукає найближчу клітинку не на воді, після генерації."""
        radius = 10  # або більший, якщо потрібно
        for r in range(radius):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    gx = dx
                    gy = dy
                    cx, cy = floor(gx / CHUNK_SIZE), floor(gy / CHUNK_SIZE)
                    ix, iy = gx - cx * CHUNK_SIZE, gy - cy * CHUNK_SIZE
                    try:
                        chunk = self.grid[(cx, cy)]
                    except KeyError:
                        continue
                    if chunk.state != ChunkStates.VOID:
                        val = int(chunk.cells[ix, iy])
                        if val >= self.WATER_THRESHOLD:
                            return [gx, gy]
        return [float(gx), float(gy)]
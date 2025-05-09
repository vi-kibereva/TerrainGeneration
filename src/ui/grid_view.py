from math import floor
import random

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor

from src.backend.chunk import CHUNK_SIZE, ChunkStates, MAX_RANGE

TERRAIN_BASE = {
    0b00: QColor(0,   0,   128),  # WATER
    0b10: QColor(34,  139, 34),   # LAND
    0b11: QColor(139, 137, 137),  # MOUNTAIN
}

SUBTYPE_COLORS = {
    0b00: {  # WATER
        0b00: QColor(0,   0,   100),  # VERYDEEP
        0b01: QColor(0,   0,   140),  # DEEP
        0b10: QColor(0,   0,   180),  # MODERATE
        0b11: QColor(0,   0,   220),  # SHALLOW
    },
    0b10: {  # LAND
        0b00: QColor(194, 178, 128),  # SAND
        0b01: QColor(34,  139, 34),   # GRASS
        0b10: QColor(0,   100, 0),    # FOREST
        0b11: QColor(85,  107, 47),   # HILL
    },
    0b11: {  # MOUNTAIN
        0b00: QColor(160, 160, 160),  # LOW
        0b01: QColor(130, 130, 130),  # MODERATE
        0b10: QColor(100, 100, 100),  # HIGH
        0b11: QColor(255, 250, 250),  # SNOWY
    },
}

DEFAULT_COLOR = QColor(50, 50, 50)

def get_color(raw: int) -> QColor:
    terrain = raw & 0b11
    subtype = (raw >> 2) & 0b11
    return SUBTYPE_COLORS.get(terrain, {}).get(subtype, DEFAULT_COLOR)


class GridView(QtWidgets.QWidget):
    """
    Відображає сітку та персонажа з камерою, що слідує за ним.
    Додає можливість зуму, діагональні рухи та догенерацію чанків.
    """
    PLAYER_SCALE = 4.5
    GENERATE_RADIUS = 2
    WATER_THRESHOLD = MAX_RANGE * 0.3

    def __init__(self, grid, cells_w=50, cells_h=50, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.cells_w = cells_w
        self.cells_h = cells_h
        self.player_pixmap = QtGui.QPixmap("src/ui/chelik.png")
        self.zoom = 1.0

        self.player_position = self.find_land_position()
        self.current_chunk = (
            floor(self.player_position[0] / CHUNK_SIZE),
            floor(self.player_position[1] / CHUNK_SIZE)
        )
        self._ensure_chunks()

        self.pressed_keys = set()
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def set_zoom(self, value: float):
        """Задає рівень зуму і оновлює відображення"""
        self.zoom = max(0.1, value)
        self.update()

    def generate_grid(self, seed: int, density: float):
        """Генерує нову мапу за seed і density"""
        random.seed(seed)
        if hasattr(self.grid, 'density'):
            self.grid.density = density
        if hasattr(self.grid, 'clear'):
            self.grid.clear()
        self.current_chunk = (0, 0)
        self._ensure_chunks()
        self.player_position = self.find_land_position()
        self.current_chunk = (
            floor(self.player_position[0] / CHUNK_SIZE),
            floor(self.player_position[1] / CHUNK_SIZE)
        )
        self._ensure_chunks()
        self.update()

    def clear_grid(self):
        """Очищує мапу та генерує заново"""
        if hasattr(self.grid, 'clear'):
            self.grid.clear()
        self.current_chunk = (0, 0)
        self._ensure_chunks()
        self.player_position = self.find_land_position()
        self.current_chunk = (
            floor(self.player_position[0] / CHUNK_SIZE),
            floor(self.player_position[1] / CHUNK_SIZE)
        )
        self._ensure_chunks()
        self.update()

    def _is_water(self, gx: float, gy: float) -> bool:
        """Повертає True, якщо вказані world-координати на воді"""
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
        """Генерує чанки навколо current_chunk"""
        self.grid.generate_around(
            self.current_chunk,
            generated_radius=self.GENERATE_RADIUS
        )

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)

        w, h = self.width(), self.height()
        base_w, base_h = w / self.cells_w, h / self.cells_h
        cw, ch = base_w * self.zoom, base_h * self.zoom

        center_x, center_y = w / 2.0, h / 2.0
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
                    color = DEFAULT_COLOR
                else:
                    raw = int(chunk.cells[ix, iy])
                    color = get_color(raw)
                px = (col * cw) - ((ox - start_col) * cw)
                py = (row * ch) - ((oy - start_row) * ch)
                painter.fillRect(QtCore.QRectF(px, py, cw + 1, ch + 1), color)

        size = int(min(cw, ch) * self.PLAYER_SCALE)
        scaled = self.player_pixmap.scaled(
            size, size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(
            int(center_x - size/2), int(center_y - size/2),
            scaled
        )

    def keyPressEvent(self, event):
        moves = {
            QtCore.Qt.Key_Up: (0, -1),
            QtCore.Qt.Key_Down: (0, 1),
            QtCore.Qt.Key_Left: (-1, 0),
            QtCore.Qt.Key_Right: (1, 0)
        }
        key = event.key()
        if key in moves:
            self.pressed_keys.add(key)
            dx = sum(moves[k][0] for k in self.pressed_keys if k in moves)
            dy = sum(moves[k][1] for k in self.pressed_keys if k in moves)
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

    def keyReleaseEvent(self, event):
        if event.key() in self.pressed_keys:
            self.pressed_keys.remove(event.key())

    def find_land_position(self):
        """Шукає найближчу до (0,0) сушу"""
        radius = 10
        for r in range(radius + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    gx, gy = dx, dy
                    cx, cy = floor(gx / CHUNK_SIZE), floor(gy / CHUNK_SIZE)
                    ix, iy = int(gx - cx * CHUNK_SIZE), int(gy - cy * CHUNK_SIZE)
                    try:
                        chunk = self.grid[(cx, cy)]
                    except KeyError:
                        continue
                    if chunk.state != ChunkStates.VOID and int(chunk.cells[ix, iy]) >= self.WATER_THRESHOLD:
                        return [float(gx), float(gy)]
        return [0.0, 0.0]

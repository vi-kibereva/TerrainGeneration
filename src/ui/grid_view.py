# grid_view.py
from math import floor

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor
import numpy as np

from src.backend.chunk import CHUNK_SIZE, ChunkStates

# --- Base and subtype colors definitions ---
TERRAIN_BASE = {
    0b00: QColor(0,   0,   128),  # WATER
    0b10: QColor(34,  139, 34),   # LAND
    0b11: QColor(139, 137, 137),  # MOUNTAIN
}

SUBTYPE_COLORS = {
    0b00: {  # WATER
        0b00: QColor(0,   0,   75),   # VERYDEEP
        0b01: QColor(0,   0,   150),  # DEEP
        0b10: QColor(0,   100, 200),  # MODERATE
        0b11: QColor(100, 200, 255),  # SHALLOW
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

TEXTURE_OVERLAY = QColor(255, 255, 255)
TEXTURE_ALPHA   = 0.2

def blend(base: QColor, overlay: QColor, alpha: float) -> QColor:
    """Overlay 'overlay' on top of 'base' with given alpha."""
    r = int(base.red()   * (1 - alpha) + overlay.red()   * alpha)
    g = int(base.green() * (1 - alpha) + overlay.green() * alpha)
    b = int(base.blue()  * (1 - alpha) + overlay.blue()  * alpha)
    return QColor(r, g, b)


DEFAULT_COLOR = QColor(50, 50, 50)

def get_color(raw: int) -> QColor:
    terrain =  raw         & 0b11
    subtype = (raw >> 2)   & 0b11


    return SUBTYPE_COLORS.get(terrain, {}).get(subtype, DEFAULT_COLOR)


class GridView(QtWidgets.QWidget):
    def __init__(self, grid, cells_w=50, cells_h=50, parent=None):
        super().__init__(parent)
        self.grid       = grid
        self.cells_w    = cells_w
        self.cells_h    = cells_h
        self.origin     = (-(cells_w // 2), -(cells_h // 2))
        self.player_position = [0, 0]
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        w, h   = self.width(), self.height()
        cw, ch = w / self.cells_w, h / self.cells_h
        ox, oy = self.origin

        for row in range(self.cells_h):
            for col in range(self.cells_w):
                x, y = ox + col, oy + row
                cx, cy = floor(x / CHUNK_SIZE), floor(y / CHUNK_SIZE)
                ix, iy = x - cx * CHUNK_SIZE, y - cy * CHUNK_SIZE
                chunk = self.grid[(cx, cy)]
                if chunk.state == ChunkStates.VOID:
                    color = DEFAULT_COLOR
                else:
                    raw: np.int  = chunk.cells[ix, iy]
                    color = get_color(raw)
                painter.fillRect(col * cw, row * ch, cw, ch, color)

        # draw player
        px = (self.player_position[0] - ox) * cw + cw / 2
        py = (self.player_position[1] - oy) * ch + ch / 2
        size = cw * 0.8
        painter.setBrush(QtGui.QBrush(QColor(255, 0, 0)))
        painter.drawEllipse(int(px - size / 2), int(py - size / 2), int(size), int(size))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.player_position[1] -= 1
        elif event.key() == QtCore.Qt.Key_Down:
            self.player_position[1] += 1
        elif event.key() == QtCore.Qt.Key_Left:
            self.player_position[0] -= 1
        elif event.key() == QtCore.Qt.Key_Right:
            self.player_position[0] += 1
        self.update()

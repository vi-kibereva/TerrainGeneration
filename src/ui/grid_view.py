from typing import TYPE_CHECKING
from PySide6 import QtCore, QtGui, QtWidgets
from math import floor
from src.backend.chunk import CHUNK_SIZE, ChunkStates, MAX_RANGE

if TYPE_CHECKING:
    from src.backend.grid import Grid

# import your CHUNK_SIZE, Grid and NoneChunk here
# from src.grid import Grid, CHUNK_SIZE, NoneChunk

blue = QtGui.QColor(0, 0, 255)
green = QtGui.QColor(0, 255, 0)
brown = QtGui.QColor(139, 69, 19)


class GridView(QtWidgets.QWidget):
    def __init__(
        self,
        grid: "Grid",
        origin: tuple[int, int] = (0, 0),
        cells_w: int = 50,
        cells_h: int = 50,
        parent=None,
    ):
        super().__init__(parent)
        self.grid = grid
        self.origin = origin  # top-left cell coordinate (in world cells)
        self.cells_w = cells_w  # how many cells wide to draw
        self.cells_h = cells_h  # how many cells tall to draw
        self.setMinimumSize(200, 200)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        w, h = self.width(), self.height()
        cw = w / self.cells_w  # cell-width in pixels
        ch = h / self.cells_h  # cell-height in pixels
        ox, oy = self.origin

        for row in range(self.cells_h):
            for col in range(self.cells_w):
                # world cell coordinates
                cell_x = ox + col
                cell_y = oy + row

                # map to chunk coordinates + in-chunk indices
                # floor-divide handles negatives correctly:
                cx = floor(cell_x / CHUNK_SIZE)
                cy = floor(cell_y / CHUNK_SIZE)
                ix = cell_x - cx * CHUNK_SIZE
                iy = cell_y - cy * CHUNK_SIZE

                chunk = self.grid[(cx, cy)]
                if chunk.state == ChunkStates.VOID:
                    color = QtGui.QColor(0, 0, 0)  # background
                else:
                    val = int(chunk.cells[ix, iy])

                    t = val / (MAX_RANGE / 9)
                    if t < 0.5:
                        # 0.0 → 0.5  : blue → green
                        u = t / 0.5
                        r = int(blue.red() + (green.red() - blue.red()) * u)
                        g = int(blue.green() + (green.green() - blue.green()) * u)
                        b = int(blue.blue() + (green.blue() - blue.blue()) * u)
                    else:
                        # 0.5 → 1.0  : green → brown
                        u = (t - 0.5) / 0.5
                        r = int(green.red() + (brown.red() - green.red()) * u)
                        g = int(green.green() + (brown.green() - green.green()) * u)
                        b = int(green.blue() + (brown.blue() - green.blue()) * u)

                    color = QtGui.QColor(r, g, b)

                rect = QtCore.QRectF(col * cw, row * ch, cw, ch)
                painter.fillRect(rect, color)

        painter.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 1))
        # optional: draw grid lines
        for i in range(self.cells_w + 1):
            x = i * cw
            painter.drawLine(int(x), 0, int(x), h)
        for j in range(self.cells_h + 1):
            y = j * ch
            painter.drawLine(0, int(y), w, int(y))
        painter.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 1))
        # thin 1-cell grid lines
        painter.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 1))
        # vertical
        for i in range(self.cells_w + 1):
            x = i * cw
            painter.drawLine(int(x), 0, int(x), h)
        # horizontal
        for j in range(self.cells_h + 1):
            y = j * ch
            painter.drawLine(0, int(y), w, int(y))

        # thick chunk boundaries
        chunk_pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 2)
        painter.setPen(chunk_pen)

        # vertical chunk lines
        for col in range(self.cells_w + 1):
            if (ox + col) % CHUNK_SIZE == 0:
                x = col * cw
                painter.drawLine(int(x), 0, int(x), h)

        # horizontal chunk lines
        for row in range(self.cells_h + 1):
            if (oy + row) % CHUNK_SIZE == 0:
                y = row * ch
                painter.drawLine(0, int(y), w, int(y))
        painter.end()

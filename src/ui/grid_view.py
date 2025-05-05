from PySide6 import QtCore, QtGui, QtWidgets
import random
from typing import TYPE_CHECKING
from math import floor
from src.backend.chunk import CHUNK_SIZE, ChunkStates, MAX_RANGE
from src.ui.panel_view import ControlPanel

if TYPE_CHECKING:
    from src.backend.grid import Grid

blue = QtGui.QColor(0, 0, 255)
green = QtGui.QColor(0, 255, 0)
brown = QtGui.QColor(139, 69, 19)


class GridView(QtWidgets.QWidget):
    def __init__(self, grid, cells_w=50, cells_h=50, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.cells_w = cells_w
        self.cells_h = cells_h
        self.origin = (-(cells_w // 2), -(cells_h // 2))

        # Позиція персонажа
        self.player_position = [0, 0]  # Список, бо потрібно змінювати значення

        # Завантаження зображення персонажа
        self.player_pixmap = QtGui.QPixmap("src/ui/chelik.png")

        # Лейаут тільки для полотна
        layout = QtWidgets.QVBoxLayout(self)
        self.canvas = QtWidgets.QWidget(self)
        self.canvas.paintEvent = self.paintEvent
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumSize(800, 600)

        # Встановлення фокусу на це вікно для обробки клавіатурних подій
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def generate_grid(self, seed, density):
        random.seed(seed)
        self.grid.generate(seed, density)
        self.update()

    def clear_grid(self):
        self.grid.clear()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        w, h = self.width(), self.height()
        cw = w / self.cells_w
        ch = h / self.cells_h
        ox, oy = self.origin

        for row in range(self.cells_h):
            for col in range(self.cells_w):
                x = ox + col
                y = oy + row
                cx = floor(x / CHUNK_SIZE)
                cy = floor(y / CHUNK_SIZE)
                ix, iy = x - cx * CHUNK_SIZE, y - cy * CHUNK_SIZE
                chunk = self.grid[(cx, cy)]
                if chunk.state == ChunkStates.VOID:
                    color = QtGui.QColor(50, 50, 50)
                else:
                    val = int(chunk.cells[ix, iy])
                    color = self.calculate_color(val)
                painter.fillRect(col * cw, row * ch, cw, ch, color)

        # Сітка
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 1))
        for i in range(self.cells_w + 1):
            painter.drawLine(int(i * cw), 0, int(i * cw), h)
        for j in range(self.cells_h + 1):
            painter.drawLine(0, int(j * ch), w, int(j * ch))

        # Малюємо персонажа
        if self.player_position is not None:
            # Центр клітинки
            px = (self.player_position[0] - ox) * cw + cw / 2
            py = (self.player_position[1] - oy) * ch + ch / 2

            # Фіксований розмір персонажа (зробимо його більшим за клітинку)
            size = 60
            scaled_pixmap = self.player_pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            # Центрування картинки
            px -= size / 2
            py -= size / 2

            painter.drawPixmap(int(px), int(py), scaled_pixmap)

    def calculate_color(self, val):
        t = val / (MAX_RANGE / 9)
        if t < 0.5:
            u = t / 0.5
            g = int(255 * u)
            b = int(255 * (1 - u))
            r = 0
        else:
            u = (t - 0.5) / 0.5
            r = int(139 * u)
            g = int(255 - 186 * u)
            b = 0
        return QtGui.QColor(r, g, b)

    def keyPressEvent(self, event):
        key = event.key()

        # Рух персонажа
        if key == QtCore.Qt.Key_Up:  # Стрілка вгору
            self.player_position[1] -= 1
        elif key == QtCore.Qt.Key_Down:  # Стрілка вниз
            self.player_position[1] += 1
        elif key == QtCore.Qt.Key_Left:  # Стрілка вліво
            self.player_position[0] -= 1
        elif key == QtCore.Qt.Key_Right:  # Стрілка вправо
            self.player_position[0] += 1

        # Перемалювати сітку після зміни позиції
        self.update()

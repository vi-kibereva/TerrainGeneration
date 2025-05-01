from PySide6 import QtCore, QtGui, QtWidgets
import random
from typing import TYPE_CHECKING
from math import floor
from src.backend.chunk import CHUNK_SIZE, ChunkStates, MAX_RANGE


if TYPE_CHECKING:
    from src.backend.grid import Grid

blue = QtGui.QColor(0, 0, 255)
green = QtGui.QColor(0, 255, 0)
brown = QtGui.QColor(139, 69, 19)

class ControlPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QtWidgets.QLabel("Settings")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        seed_label = QtWidgets.QLabel("Seed:")
        seed_label.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(seed_label)

        self.seed_input = QtWidgets.QLineEdit(self)
        self.seed_input.setPlaceholderText("Enter seed (Integer, e.g., 1234)")
        self.seed_input.setStyleSheet("""
            padding: 10px; 
            font-size: 16px; 
            border: 2px solid #4CAF50; 
            border-radius: 8px; 
            background-color: #f4f4f4;
            color: #333;
        """)
        layout.addWidget(self.seed_input)

        # Label and input for Density
        density_label = QtWidgets.QLabel("Density:")
        density_label.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(density_label)

        self.density_input = QtWidgets.QLineEdit(self)
        self.density_input.setPlaceholderText("Enter density (Float, 0 to 1)")
        self.density_input.setStyleSheet("""
            padding: 10px; 
            font-size: 16px; 
            border: 2px solid #4CAF50; 
            border-radius: 8px; 
            background-color: #f4f4f4;
            color: #333;
        """)
        layout.addWidget(self.density_input)

        buttons_layout = QtWidgets.QVBoxLayout()

        self.start_button = QtWidgets.QPushButton("Start", self)
        self.start_button.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            font-size: 20px; 
            padding: 15px;
            border-radius: 8px; 
            transition: background-color 0.3s ease;
        """)
        self.start_button.clicked.connect(self.start_generation)
        self.start_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.start_button.setFixedHeight(50)
        self.start_button.setStyleSheet(self.start_button.styleSheet() + """
            background-color: #4CAF50; 
        """)
        self.start_button.setStyleSheet(self.start_button.styleSheet() + """
            background-color: #66bb6a;
        """)
        self.start_button.setStyleSheet(self.start_button.styleSheet() + """
            background-color: #81c784;
        """)
        buttons_layout.addWidget(self.start_button)

        self.regenerate_button = QtWidgets.QPushButton("Regenerate", self)
        self.regenerate_button.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            font-size: 20px; 
            padding: 15px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        """)
        self.regenerate_button.clicked.connect(self.regenerate_grid)
        self.regenerate_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.regenerate_button.setFixedHeight(50)
        buttons_layout.addWidget(self.regenerate_button)

        self.random_seed_button = QtWidgets.QPushButton("Random Seed", self)
        self.random_seed_button.setStyleSheet("""
            background-color: #FF5722; 
            color: white; 
            font-size: 20px; 
            padding: 15px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        """)
        self.random_seed_button.clicked.connect(self.generate_random_seed)
        self.random_seed_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.random_seed_button.setFixedHeight(50)
        buttons_layout.addWidget(self.random_seed_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def start_generation(self):
        seed = self.seed_input.text()
        density = self.density_input.text()

        try:
            seed = int(seed) if seed else random.randint(0, 1000)
            density = float(density) if density else 0.5

            print(f"Starting generation with seed: {seed}, density: {density}")
            random.seed(seed)

        except ValueError:
            self.show_error_message("Invalid input values! Please enter valid numbers.")

    def regenerate_grid(self):
        print("Regenerating the grid...")
        self.seed_input.clear()
        self.density_input.clear()

    def generate_random_seed(self):
        random_seed = random.randint(0, 1000)
        self.seed_input.setText(str(random_seed))
        print(f"Generated random seed: {random_seed}")

    def show_error_message(self, message):
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()



class GridView(QtWidgets.QWidget):
    def __init__(self, grid: "Grid", origin: tuple[int, int] = (0, 0), cells_w: int = 50, cells_h: int = 50, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.cells_w = cells_w
        self.cells_h = cells_h

        # Центрування грида
        self.origin = (
            -(cells_w // 2),
            -(cells_h // 2),
        )

        self.setMinimumSize(800, 800)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        w, h = self.width(), self.height()

        cw = w / self.cells_w
        ch = h / self.cells_h

        ox, oy = self.origin

        for row in range(self.cells_h):
            for col in range(self.cells_w):
                cell_x = ox + col
                cell_y = oy + row

                cx = floor(cell_x / CHUNK_SIZE)
                cy = floor(cell_y / CHUNK_SIZE)
                ix = cell_x - cx * CHUNK_SIZE
                iy = cell_y - cy * CHUNK_SIZE

                chunk = self.grid[(cx, cy)]

                if chunk.state == ChunkStates.VOID:
                    color = QtGui.QColor(50, 50, 50)
                else:
                    val = int(chunk.cells[ix, iy])
                    color = self.calculate_color(val)

                rect = QtCore.QRectF(col * cw, row * ch, cw, ch)
                painter.fillRect(rect, color)

        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 1))

        for i in range(self.cells_w + 1):
            x = i * cw
            painter.drawLine(int(x), 0, int(x), h)
        for j in range(self.cells_h + 1):
            y = j * ch
            painter.drawLine(0, int(y), w, int(y))

        painter.end()

    def calculate_color(self, val):
        t = val / (MAX_RANGE / 9)
        if t < 0.5:
            u = t / 0.5
            r = int(0 + (0 - 0) * u)
            g = int(0 + (255 - 0) * u)
            b = int(255 + (0 - 255) * u)
        else:
            u = (t - 0.5) / 0.5
            r = int(0 + (139 - 0) * u)
            g = int(255 + (69 - 255) * u)
            b = int(0 + (19 - 0) * u)

        return QtGui.QColor(r, g, b)

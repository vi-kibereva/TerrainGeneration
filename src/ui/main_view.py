from PySide6 import QtWidgets
from src.backend.grid import Grid
from src.ui.grid_view import ControlPanel, GridView


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, grid):
        super().__init__()
        self.setWindowTitle("Terrain generation")

        # Головний лейаут
        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)

        # Панель керування зліва
        self.control_panel = ControlPanel(parent=self)
        layout.addWidget(self.control_panel)

        # Візуалізація грида справа
        self.grid_view = GridView(grid, parent=self)
        layout.addWidget(self.grid_view, stretch=1)

        self.setCentralWidget(central)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Ініціалізуємо модель і створюємо сітку початково
    grid = Grid(density=0.5)
    grid.generate_around((0, 0), generated_radius=2)

    # Створюємо головне вікно
    window = MainWindow(grid)
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec())

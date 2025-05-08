from PySide6 import QtWidgets
from src.backend.grid import Grid
from src.ui.grid_view import GridView
from src.ui.panel_view import ControlPanel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, grid, radius: int):
        super().__init__()
        self.setWindowTitle("Terrain generation")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)

        # Панель керування
        self.control_panel = ControlPanel(parent=self)
        layout.addWidget(self.control_panel)

        # Візуалізація
        self.grid_view = GridView(grid, parent=self)
        layout.addWidget(self.grid_view, stretch=1)

        self.setCentralWidget(central)

        # Ініціалізація генерації
        self.grid = grid
        self.radius = radius
        self.control_panel.start_generation()  # автоматичний старт

    def generate(self, seed: int, density: float, radius: int):
        self.grid = Grid(density=density)
        self.grid.generate_around((0, 0), generated_radius=radius)
        self.grid_view.grid = self.grid
        self.grid_view.origin = (-(self.grid_view.cells_w // 2), -(self.grid_view.cells_h // 2))
        self.grid_view.update()


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    initial_radius = 2
    grid = Grid(density=0.5)
    window = MainWindow(grid, radius=initial_radius)
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())
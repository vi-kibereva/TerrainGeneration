from PySide6 import QtWidgets
from src.backend.grid import Grid
from src.ui.grid_view import GridView
from src.ui.panel_view import ControlPanel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, grid):
        super().__init__()
        self.setWindowTitle("Terrain generation")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)

        self.control_panel = ControlPanel(parent=self)
        layout.addWidget(self.control_panel)

        self.grid_view = GridView(grid, parent=self)
        layout.addWidget(self.grid_view, stretch=1)

        self.setCentralWidget(central)

    # Передаємо виклики від панелі до GridView
    def generate_grid(self, seed, density):
        self.grid_view.generate_grid(seed, density)

    def clear_grid(self):
        self.grid_view.clear_grid()


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    grid = Grid(density=0.5)
    grid.generate_around((0, 0), generated_radius=2, noise_radius=5)

    window = MainWindow(grid)
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())
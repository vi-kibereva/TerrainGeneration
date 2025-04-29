from PySide6 import QtWidgets
from .grid_view import GridView
from src.backend.grid import Grid


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, grid: Grid):
        super().__init__()
        self.view = GridView(grid, origin=(0, 0), cells_w=40, cells_h=30)
        self.setCentralWidget(self.view)
        self.resize(800, 600)


def main():
    import sys

    # create and populate your Grid however you like:
    grid = Grid(density=0.5)

    app = QtWidgets.QApplication(sys.argv)
    grid.generate_around((0, 0), generated_radius=2, noise_radius=5)
    w = MainWindow(grid)
    w.show()
    sys.exit(app.exec())

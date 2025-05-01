from PySide6 import QtWidgets
from src.backend.grid import Grid
from src.ui.grid_view import ControlPanel, GridView


class MainWindow(QtWidgets.QWidget):
    def __init__(self, grid):
        super().__init__()

        layout = QtWidgets.QHBoxLayout(self)

        self.control_panel = ControlPanel(self)
        layout.addWidget(self.control_panel)

        self.grid_view = GridView(grid, self)
        layout.addWidget(self.grid_view)

        self.setLayout(layout)



def main():
    import sys

    grid = Grid(density=0.5)

    app = QtWidgets.QApplication(sys.argv)
    grid.generate_around((0, 0), generated_radius=2, noise_radius=5)
    w = MainWindow(grid)
    w.show()
    sys.exit(app.exec())

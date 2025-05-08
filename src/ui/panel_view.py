from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QHBoxLayout, QSlider, QMessageBox
)
from PySide6.QtCore import Qt
import random

class ControlPanel(QWidget):
    """Side panel with seed, zoom slider, and generate button"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ = parent
        self.setObjectName("control_panel")
        self.setFixedWidth(300)

        self.setStyleSheet(
            "#control_panel { background-color: #333; }"
            " QLabel { color: #fff; font-size: 14px; }"
            " QLineEdit { padding: 6px; border-radius: 4px; border: 1px solid #555; background: #555; color: #fff;}"
            " QPushButton { padding: 8px; border-radius: 4px; background-color: #555; color: #fff; }"
            " QPushButton:hover { background-color: #777; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QLabel("Settings")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)

        # Seed input
        layout.addWidget(QLabel("Seed:"))
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Enter integer or leave blank")
        layout.addWidget(self.seed_input)

        # Zoom slider
        layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.valueChanged.connect(self.on_zoom_change)
        layout.addWidget(self.zoom_slider)

        # Generate button
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.start_generation)
        layout.addWidget(self.generate_btn)

        layout.addStretch()

    def start_generation(self):
        seed_text = self.seed_input.text()
        try:
            seed = int(seed_text) if seed_text else random.randint(0, 999999)
        except ValueError:
            QMessageBox.warning(self, "Invalid Seed", "Seed must be an integer.")
            return

        self.parent_.grid_view.generate_grid(seed=seed, density=0.5)  # фіксована густина

    def on_zoom_change(self, value):
        self.parent_.grid_view.set_zoom(value / 100.0)

    def random_seed(self):
        value = random.randint(0, 100000)
        self.seed_input.setText(str(value))

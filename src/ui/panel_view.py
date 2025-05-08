from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QSlider
from PySide6.QtCore import Qt
import random

class ControlPanel(QWidget):
    """Side panel with seed, zoom, and action buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ = parent
        self.setObjectName("control_panel")
        self.setFixedWidth(300)
        # Styles
        self.setStyleSheet(
            "#control_panel { background-color: #333; }"
            " QLabel { color: #fff; font-size: 14px; }"
            " QLineEdit { padding: 6px; border-radius: 4px; border: 1px solid #555; background: #555; color: #fff;}"
            " QPushButton { padding: 8px; border-radius: 4px; background-color: #555; color: #fff; }"
            " QPushButton:hover { background-color: #777; }"
            " QSlider::groove:horizontal { height: 6px; background: #444; }"
            " QSlider::handle:horizontal { width: 14px; background: #888; margin: -4px 0; border-radius: 7px; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QLabel("Settings")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)

        # Seed
        layout.addWidget(QLabel("Seed:"))
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Enter integer or leave blank")
        layout.addWidget(self.seed_input)

        # Zoom slider
        layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(1, 5)  # 1x to 5x zoom
        self.zoom_slider.setValue(1)
        self.zoom_slider.valueChanged.connect(self.zoom_changed)
        layout.addWidget(self.zoom_slider)

        # Buttons layout
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.start_generation)
        btn_layout.addWidget(self.generate_btn)

        self.random_btn = QPushButton("Random Seed")
        self.random_btn.clicked.connect(self.random_seed)
        btn_layout.addWidget(self.random_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def start_generation(self):
        try:
            seed = int(self.seed_input.text()) if self.seed_input.text() else random.randint(0, 100000)
        except ValueError:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid integer for the seed.")
            return

        default_density = 0.5
        default_radius = 2

        if hasattr(self.parent_, 'generate'):
            self.parent_.generate(seed, default_density, default_radius)

    def random_seed(self):
        value = random.randint(0, 100000)
        self.seed_input.setText(str(value))

    def zoom_changed(self, value):
        if hasattr(self.parent_, 'set_zoom'):
            self.parent_.set_zoom(value)

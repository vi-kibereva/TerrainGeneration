from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
import random

class ControlPanel(QWidget):
    """Side panel with seed, density, radius, and action buttons"""
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

        # Optional: Add input fields for density and radius if needed
        self.density_input = QLineEdit()
        self.density_input.setPlaceholderText("Enter density (e.g. 0.5)")
        layout.addWidget(QLabel("Density:"))
        layout.addWidget(self.density_input)

        self.radius_input = QLineEdit()
        self.radius_input.setPlaceholderText("Enter radius (e.g. 2)")
        layout.addWidget(QLabel("Radius:"))
        layout.addWidget(self.radius_input)

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
            density = float(self.density_input.text()) if self.density_input.text() else 0.5
            radius = int(self.radius_input.text()) if self.radius_input.text() else 2
            if radius < 2:
                raise ValueError("Radius must be >= 2")
        except ValueError:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Invalid Input", "Please enter valid numeric values.")
            return

        if self.parent_ and hasattr(self.parent_, 'generate'):
            self.parent_.generate(seed, density, radius)

    def random_seed(self):
        value = random.randint(0, 100000)
        self.seed_input.setText(str(value))

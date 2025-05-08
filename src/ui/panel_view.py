import random
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtCore import Qt

class ControlPanel(QWidget):
    """Side panel with seed, density and action buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ = parent

        # Основні стилі
        self.setStyleSheet("""
            QWidget#control_panel { background-color: #f5f5f5; }
            QLabel { font-size: 14px; color: #333; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
            QPushButton { padding: 10px; border: none; border-radius: 4px; background-color: #525252; color: white; font-size: 15px; }
            QPushButton:hover { background-color: #45a049; }
        """
        )
        self.setObjectName("control_panel")
        self.setFixedWidth(280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Опис полів для вводу
        description = QLabel("Settings")
        description.setStyleSheet("color: white; font-weight: bold; font-size: 18px; margin-bottom: 8px;")
        layout.addWidget(description)

        # Seed input
        label_seed = QLabel("Seed:")
        label_seed.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(label_seed)
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("10101010")
        layout.addWidget(self.seed_input)

        # Density input
        label_density = QLabel("Density (0–1):")
        label_density.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(label_density)
        self.density_input = QLineEdit()
        self.density_input.setPlaceholderText("0.3")
        layout.addWidget(self.density_input)

        # Кнопки дій у стовпець
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_generation)
        layout.addWidget(self.start_btn)

        self.regen_btn = QPushButton("Regenerate")
        self.regen_btn.clicked.connect(self.regenerate)
        layout.addWidget(self.regen_btn)

        self.random_btn = QPushButton("Random seed")
        self.random_btn.clicked.connect(self.random_seed)
        layout.addWidget(self.random_btn)

        layout.addStretch()

    def start_generation(self):
        try:
            seed = int(self.seed_input.text()) if self.seed_input.text() else random.randint(0, 100000)
            density = float(self.density_input.text()) if self.density_input.text() else 0.5
        except ValueError:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", "Please enter valid value.")
            return
        if hasattr(self.parent_, 'generate_grid'):
            self.parent_.generate_grid(seed=seed, density=density)

    def regenerate(self):
        self.seed_input.clear()
        self.density_input.clear()
        if hasattr(self.parent_, 'clear_grid'):
            self.parent_.clear_grid()

    def random_seed(self):
        value = random.randint(0, 100000)
        self.seed_input.setText(str(value))

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QDialog,
    QDialogButtonBox
)

class LossDialog(QDialog):
    goBackSignal = pyqtSignal()
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        title = QLabel("Maybe Next Time :(")
        layout.addWidget(title)
        
        button_box = QDialogButtonBox()
        back_button = button_box.addButton("Go Back", QDialogButtonBox.ButtonRole.ActionRole)
        back_button.setFixedWidth(120)
        show_button = button_box.addButton("Show Solution", QDialogButtonBox.ButtonRole.ActionRole)
        show_button.setFixedWidth(160)

        back_button.clicked.connect(self.on_back_clicked)
        back_button.clicked.connect(self.accept)
        show_button.clicked.connect(self.accept)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def on_back_clicked(self):
        self.goBackSignal.emit()
        
class WinDialog(QDialog):
    goBackSignal = pyqtSignal()
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        title = QLabel("Yay You Won!")
        layout.addWidget(title)
        button_box = QDialogButtonBox()
        back_button = button_box.addButton("Go Back", QDialogButtonBox.ButtonRole.ActionRole)
        back_button.setFixedWidth(120)
        show_button = button_box.addButton("Show Solution", QDialogButtonBox.ButtonRole.ActionRole)
        show_button.setFixedWidth(160)

        back_button.clicked.connect(self.on_back_clicked)
        back_button.clicked.connect(self.accept)
        show_button.clicked.connect(self.accept)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def on_back_clicked(self):
        self.goBackSignal.emit()
        
import sys
from play_screen_gui import PlayScreen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
)

from sudoku_solver import Sudoku

class MainMenu(QMainWindow):
    def __init__(self, stack_widget):
        super().__init__()

        self.stack_widget = stack_widget
        self.sudoku = None
        self.init_ui()

    def init_ui(self):
        main_menu_layout = QVBoxLayout()
        main_menu_widget = QWidget()
        
        main_menu_layout.addStretch()

        main_title = QLabel("Welcome To Sudoku Game")
        main_title.setFixedHeight(40)
        main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_menu_layout.addWidget(main_title)
        main_menu_layout.addStretch()
        
        buttons = [
            ("easy", self.go_to_play_screen_easy),
            ("medium", self.go_to_play_screen_medium),
            ("hard", self.go_to_play_screen_hard)
        ]

        for text, handler in buttons:
            button = QPushButton(text.capitalize())
            button.setObjectName(text)
            button.setFixedWidth(350)
            button.clicked.connect(handler)
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(button)
            button_layout.addStretch()
            main_menu_layout.addLayout(button_layout)
            main_menu_layout.addStretch()

        main_menu_layout.addStretch()

        main_menu_widget.setLayout(main_menu_layout)
        
        self.setCentralWidget(main_menu_widget)
    
    def create_sudoku(self, difficulty):
        self.sudoku = Sudoku(difficulty) 
        self.stack_widget.widget(1).set_sudoku_board(self.sudoku.playable_board)
        
    def go_to_play_screen_easy(self):
        self.create_sudoku(1)
        
        self.stack_widget.setCurrentIndex(1)
        
    def go_to_play_screen_medium(self):
        self.create_sudoku(2)
        
        self.stack_widget.setCurrentIndex(1)
        

    def go_to_play_screen_hard(self):
        self.create_sudoku(3)
                
        self.stack_widget.setCurrentIndex(1)



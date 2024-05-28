from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QWidget,
)
from PyQt6.QtGui import QIntValidator
from dialog import WinDialog,LossDialog

class PlayScreen(QMainWindow):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget
        
        self.setWindowTitle("Sudoku")
        self.grid_widgets = [[None for _ in range(9)] for _ in range(9)]
        self.positions = {}
        main_layout = QVBoxLayout()

        top_side_widget = self.top_side()
        main_layout.addWidget(top_side_widget)

        bottom_side_widget = self.create_bottom_side()
        main_layout.addWidget(bottom_side_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def losing_dialog(self):
        loss_dialog= LossDialog()
        loss_dialog.goBackSignal.connect(self.go_back_to_main_menu)
        loss_dialog.exec()
    
    def wining_dialog(self):
        win_dialog = WinDialog()
        win_dialog.goBackSignal.connect(self.go_back_to_main_menu)
        win_dialog.exec()
        
    def top_side(self):
        top_side_widget = QWidget()
        top_side_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_widget = QWidget()

        back_button = QPushButton("Back")
        back_button.setObjectName("back")
        back_button.setFixedWidth(60)
        back_button.clicked.connect(self.go_back_to_main_menu)
        header_layout.addWidget(back_button)
        header_layout.addStretch()

        title = QLabel("Sudoku Board           ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:30px;padding-bottom:5px;")
        header_layout.addWidget(title)

        header_layout.addStretch()
        header_widget.setLayout(header_layout)

        top_side_layout.addWidget(header_widget)

        sudoku_board_layout = QHBoxLayout()
        sudoku_board_layout.addStretch()
        sudoku_board = QWidget()
        grid_board = self.create_sudoku_grid()
        sudoku_board.setLayout(grid_board)
        sudoku_board.setFixedSize(500, 500)
        sudoku_board_layout.addWidget(sudoku_board)
        sudoku_board_layout.addStretch()
        top_side_layout.addLayout(sudoku_board_layout)

        top_side_widget.setLayout(top_side_layout)
        return top_side_widget

    def create_bottom_side(self):
        bottom_side_widget = QWidget()
        bottom_side_layout = QHBoxLayout()
        left_side_widget = QPushButton("I Give Up!")
        left_side_widget.clicked.connect(self.show_full_solution)
        left_side_widget.setObjectName("giveup")
        left_side_widget.setFixedSize(250, 92)
        bottom_side_layout.addStretch()
        bottom_side_layout.addWidget(left_side_widget)
        bottom_side_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        bottom_side_layout.addStretch()
        bottom_side_widget.setLayout(bottom_side_layout)
        return bottom_side_widget

    def show_full_solution(self):
        self.set_sudoku_board(self.stack_widget.widget(0).sudoku.board)
        self.losing_dialog()
    
    def correct_block_text(self):
        sender = self.sender()
        i, j = self.positions[sender]
        value = sender.text()
        if not value:
            self.stack_widget.widget(0).sudoku.remove_from_playing_assignmnet(i, j)
            # ensures no style gets removed
            current_style = self.grid_widgets[i][j].styleSheet()
            updated_style = current_style + "color:black;"
            self.grid_widgets[i][j].setStyleSheet(updated_style)
            self.check_all_for_inconsistancy()
        
    def set_block_text(self):
        sender = self.sender()
        i, j = self.positions[sender]
        value = sender.text()

        if value.isdigit() and 1 <= int(value) <= 9:
            if self.stack_widget.widget(0).sudoku.place_number_on_board(i, j, int(value)):
                color = "green"
            else:
                color = "red"
            bg_color = "#FFF" if (i // 3 + j // 3) % 2 == 0 else "#E0E0E0"
            sender.setStyleSheet(f"background-color: {bg_color}; font-size: 22px; color: {color};")
        else:
            sender.setText('')  # Clear invalid input

            
        self.check_all_for_inconsistancy()
        if self.stack_widget.widget(0).sudoku.check_finished():
            self.wining_dialog()
            
    def check_all_for_inconsistancy(self):
        for row in self.grid_widgets:
            for widget in row:
                if widget.isReadOnly():
                    continue
                
                i, j = self.positions[widget]
                value = widget.text()
                if value.isdigit() and 1 <= int(value) <= 9:
                    if self.stack_widget.widget(0).sudoku.place_number_on_board(i, j, int(value)):
                        color = "green"
                    else:
                        color = "red"
                    bg_color = "#FFF" if (i // 3 + j // 3) % 2 == 0 else "#E0E0E0"
                    widget.setStyleSheet(f"background-color: {bg_color}; font-size: 22px; color: {color};")

    def create_sudoku_grid(self):
        grid = QGridLayout()

        for i in range(9):
            for j in range(9):
                widget = QLineEdit()
                widget.setMaxLength(1)
                widget.returnPressed.connect(self.set_block_text)
                widget.textChanged.connect(self.correct_block_text)
                widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget.setFixedSize(50, 50)
                widget.setStyleSheet("font-size: 22px;")
                if (i // 3 + j // 3) % 2 == 0:
                    widget.setStyleSheet("background-color: #FFF; font-size: 22px;")
                else:
                    widget.setStyleSheet("background-color: #E0E0E0; font-size: 22px;")
                int_validator = QIntValidator(1, 9)
                widget.setValidator(int_validator)

                grid.addWidget(widget, i, j)
                self.grid_widgets[i][j] = widget
                self.positions[widget] = (i, j)
        grid.setSpacing(0)

        return grid

    def set_sudoku_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != -1:
                    self.grid_widgets[i][j].setText(str(board[i][j]))
                    self.grid_widgets[i][j].setReadOnly(True)
                    
                    # ensures no style gets removed
                    current_style = self.grid_widgets[i][j].styleSheet()
                    updated_style = current_style + "color:black;"
                    self.grid_widgets[i][j].setStyleSheet(updated_style)
                    
                    
    def reset_sudoku_board(self):
        for i in range(9):
            for j in range(9):
                self.grid_widgets[i][j].setText('')
                self.grid_widgets[i][j].setReadOnly(False)
                if (i // 3 + j // 3) % 2 == 0:
                    self.grid_widgets[i][j].setStyleSheet("background-color: #FFF; font-size: 22px; color:#000;")
                else:
                    self.grid_widgets[i][j].setStyleSheet("background-color: #E0E0E0; font-size: 22px; color:000;")
              
    
    def go_back_to_main_menu(self):
        self.reset_sudoku_board()
        self.stack_widget.widget(0).sudoku = None
        self.stack_widget.setCurrentIndex(0)

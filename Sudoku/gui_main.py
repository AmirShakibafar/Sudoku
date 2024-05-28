import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
)
from PyQt6.QtGui import QIcon
from menu_screen_gui import MainMenu
from play_screen_gui import PlayScreen

app = QApplication(sys.argv)
app.setStyleSheet(
    """
    * {
        background-color: #EFF5FA;
        font-family: Arial;
        font-weight: 700;
    }
    
    QPushButton {
        border: 2px solid #393E41;
        background-color: #3F88C5;
        color: #FFF;
        font-size: 18px;
        border-radius: 5px;
        font-weight: 800;
        height:40px;
    }
    
    QPushButton:hover {
        background-color: #3881BC; 
    }

    QPushButton:pressed {
        background-color: #3476AD; 
        margin-top: 2px; 
        margin-bottom: -2px; 
    }

    QPushButton:focus {
        outline: none;
    }

    QPushButton#easy {
        background-color: #78BC61;
    }

    QPushButton#easy:hover {
        background-color: #6CB654; 
    }

    QPushButton#easy:pressed {
        background-color: #62AB49; 
        margin-top: 2px; 
        margin-bottom: -2px; 
    }
    QPushButton#medium {
        background-color: #FFAA00;
    }
    QPushButton#medium:hover {
        background-color: #E09900; 
    }
    QPushButton#medium:pressed {
        background-color: #CC8800; 
        margin-top: 2px; 
        margin-bottom: -2px; 
    }
    
    QPushButton#hard {
        background-color: #C1292E;
    }
    
    QPushButton#hard:hover {
        background-color: #B9272C; 
    }

    QPushButton#giveup, QPushButton#back {
        background-color:#C1292E;
        color:white;
    }

    QPushButton#giveup:hover,  QPushButton#back:hover {
        background-color: #B9272C;
    }
    QPushButton#hard:pressed {
        background-color: #A82428; 
        margin-top: 2px; 
        margin-bottom: -2px; 
    }
    QLabel {
        border-radius: 5px;
        padding: 4px;
        font-size: 30px;
        color:#001427;
    }

    QLineEdit {
        border: 1px solid #393E41;
        border-radius: 5px;
        padding: 4px;
        background-color: #FFF;
        
    }
    """
)


stack_widget = QStackedWidget()
main_menu = MainMenu(stack_widget)
play_screen = PlayScreen(stack_widget)

stack_widget.addWidget(main_menu)
stack_widget.addWidget(play_screen)

main_window = QMainWindow()
main_window.setWindowTitle("Sudoku")
main_window.setCentralWidget(stack_widget)
main_window.show()
app.setWindowIcon(QIcon("./sudoku.ico"))
sys.exit(app.exec())

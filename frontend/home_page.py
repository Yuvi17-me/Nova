from turtle import title

from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtWidgets import QPushButton


class HomePage(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background:#2B2B2B;")

        title = QLabel("Welcome to Nova", self)
        title.move(40, 40)
        title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
         """)

        subtitle = QLabel(
            "Your personal AI assistant for everyday tasks.",
            self
        )
        subtitle.move(42, 82)
        subtitle.setStyleSheet("""
            color: #A7A7A7;
            font-size: 15px;
        """)

        quick_action = QPushButton("⚡  Quick Task", self)
        quick_action.move(40, 130)
        quick_action.resize(160, 45)

        quick_action.setStyleSheet("""
            QPushButton {
                color: white;
                background: #35363A;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }

            QPushButton:hover {
            background: #424348;
            }
        """)
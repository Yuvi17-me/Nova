from PySide6.QtWidgets import QFrame, QLabel


class SettingsPage(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background:#2B2B2B;")

        title = QLabel("Settings", self)
        title.move(40, 40)
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton


class Sidebar(QFrame):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QFrame {
            background: #1C1D20;
            border-right: 1px solid #303136;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(6)

        title = QLabel("Nova")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
        """)

        layout.addWidget(title)

        buttons = [
            "🏠 Home",
            "💬 Chats",
            "📄 Documents",
            "🧠 Memory",
            "⚙️ Settings"
        ]

        for text in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, name=text: self.change_page(name))
            btn.setStyleSheet("""
                QPushButton{
                    color:white;
                    background:transparent;
                    border:none;
                    text-align:left;
                    padding:10px 14px;
                    font-size:16px;
                }

                QPushButton:hover{
                    background:#35363A;
                    border-radius:8px;
                }
            """)
            layout.addWidget(btn)

        layout.addStretch()

    def change_page(self, page_name):
        if "Home" in page_name:
            self.window.pages.setCurrentIndex(0)

        elif "Chats" in page_name:
            self.window.pages.setCurrentIndex(1)

        elif "Documents" in page_name:
            self.window.pages.setCurrentIndex(2)

        elif "Memory" in page_name:
            self.window.pages.setCurrentIndex(3)

        elif "Settings" in page_name:
            self.window.pages.setCurrentIndex(4)
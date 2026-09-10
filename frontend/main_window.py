from PySide6.QtWidgets import (
    QStackedWidget,
    QPushButton,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel
)

from PySide6.QtGui import QFont

from frontend.sidebar import Sidebar
from frontend.home_page import HomePage
from frontend.chat_page import ChatPage
from frontend.documents_page import DocumentsPage
from frontend.memory_page import MemoryPage
from frontend.settings_page import SettingsPage

class NovaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        app_font = QFont("Segoe UI", 10)
        self.setFont(app_font)

        self.setWindowTitle("Nova")
        self.resize(1200, 750)

        # Main Widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        central.setStyleSheet("background:#242424;")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = Sidebar(self)
        
        # Main Area
        self.pages = QStackedWidget()

        self.home = HomePage()
        self.chat = ChatPage()
        self.documents = DocumentsPage()
        self.memory = MemoryPage()
        self.settings = SettingsPage()

        self.pages.addWidget(self.home)        # Index 0
        self.pages.addWidget(self.chat)        # Index 1
        self.pages.addWidget(self.documents)   # Index 2
        self.pages.addWidget(self.memory)      # Index 3
        self.pages.addWidget(self.settings)    # Index 4
        main = self.pages
       
        
        layout.addWidget(sidebar)
        layout.addWidget(main)
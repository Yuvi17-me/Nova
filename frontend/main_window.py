from PySide6.QtWidgets import (
    QStackedWidget,
    QMainWindow,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QFont

from frontend.styles import COLOR_BG_CANVAS, GLOBAL_STYLESHEET
from frontend.sidebar import Sidebar
from frontend.home_page import HomePage
from frontend.chat_page import ChatPage
from frontend.documents_page import DocumentsPage
from frontend.memory_page import MemoryPage
from frontend.settings_page import SettingsPage


class NovaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # App-wide font
        app_font = QFont("Segoe UI", 10)
        self.setFont(app_font)

        self.setWindowTitle("Nova — Privacy-First AI Workspace")
        self.resize(1300, 840)
        self.setMinimumSize(1020, 660)

        # Apply global styles
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Central Widget
        central = QWidget()
        central.setStyleSheet(f"background: {COLOR_BG_CANVAS};")
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar navigation
        self.sidebar = Sidebar(self)

        # Page container
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background: transparent;")

        self.home = HomePage(self)
        self.chat = ChatPage()
        self.documents = DocumentsPage()
        self.memory = MemoryPage()
        self.settings = SettingsPage()

        self.pages.addWidget(self.home)        # Index 0: Home
        self.pages.addWidget(self.chat)        # Index 1: Chats
        self.pages.addWidget(self.documents)   # Index 2: Documents
        self.pages.addWidget(self.memory)      # Index 3: Memory
        self.pages.addWidget(self.settings)    # Index 4: Settings

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)
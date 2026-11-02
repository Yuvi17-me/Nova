from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from frontend.styles import (
    COLOR_BG_SIDEBAR,
    COLOR_BORDER_SUBTLE,
    COLOR_ACCENT_PRIMARY,
    COLOR_ACCENT_HOVER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
)
from frontend.components.nova_logo import NovaLogoWidget


class Sidebar(QFrame):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setFixedWidth(244)
        self.setStyleSheet(f"""
            .Sidebar {{
                background: {COLOR_BG_SIDEBAR};
                border-right: 1px solid {COLOR_BORDER_SUBTLE};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 22, 16, 20)
        layout.setSpacing(10)

        # ----------------------------------------------------
        # BRAND SECTION
        # ----------------------------------------------------
        brand = QFrame()
        brand.setStyleSheet("background: transparent; border: none;")
        brand_layout = QVBoxLayout(brand)
        brand_layout.setContentsMargins(6, 4, 6, 14)
        brand_layout.setSpacing(6)

        title_row = QHBoxLayout()
        title_row.setSpacing(10)

        # Custom Celestial Nova Logo Widget
        self.logo = NovaLogoWidget(size=26)
        title_row.addWidget(self.logo)

        title = QLabel("NOVA")
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 3px;
                background: transparent;
                border: none;
            }}
        """)
        title_row.addWidget(title)
        title_row.addStretch()

        brand_layout.addLayout(title_row)

        status_pill = QLabel("●  LOCAL INTELLIGENCE")
        status_pill.setStyleSheet(f"""
            QLabel {{
                color: #818CF8;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
                background: #151828;
                border: 1px solid #252D48;
                border-radius: 8px;
                padding: 3px 8px;
                max-width: 155px;
            }}
        """)
        brand_layout.addWidget(status_pill)
        layout.addWidget(brand)

        # ----------------------------------------------------
        # SECTION HEADER
        # ----------------------------------------------------
        section = QLabel("WORKSPACE")
        section.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_MUTED};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.2px;
                padding: 10px 10px 4px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(section)

        # ----------------------------------------------------
        # NAVIGATION BUTTONS
        # ----------------------------------------------------
        nav_items = [
            ("⌂", "Home", "Home"),
            ("💬", "Chats", "Chat Assistant"),
            ("📄", "Documents", "Documents"),
            ("◈", "Memory", "Memory"),
            ("⚙", "Settings", "Settings"),
        ]

        self.buttons = []
        for icon, page_id, display_label in nav_items:
            btn = QPushButton(f"  {icon}   {display_label}")
            btn.setProperty("page", page_id)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, page=page_id: self.change_page(page))
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {COLOR_TEXT_SECONDARY};
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 9px;
                    text-align: left;
                    padding: 11px 12px;
                    font-size: 13px;
                    font-weight: 500;
                }}

                QPushButton:hover {{
                    color: {COLOR_TEXT_PRIMARY};
                    background: #171A28;
                }}

                QPushButton:checked {{
                    color: {COLOR_TEXT_PRIMARY};
                    background: #1C2035;
                    border: 1px solid #2F3759;
                    font-weight: 600;
                }}
            """)
            btn.setCheckable(True)
            self.buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # ----------------------------------------------------
        # PRIVACY BADGE FOOTER
        # ----------------------------------------------------
        footer_card = QFrame()
        footer_card.setStyleSheet(f"""
            .QFrame {{
                background: #111420;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 10px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        footer_layout = QVBoxLayout(footer_card)
        footer_layout.setContentsMargins(12, 10, 12, 10)
        footer_layout.setSpacing(4)

        f_title = QLabel("🔒  100% Private & Local")
        f_title.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 11px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)

        f_desc = QLabel("On-device AI • Offline ready\nNova v2.0")
        f_desc.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_MUTED};
                font-size: 10px;
                line-height: 140%;
                background: transparent;
                border: none;
            }}
        """)

        footer_layout.addWidget(f_title)
        footer_layout.addWidget(f_desc)
        layout.addWidget(footer_card)

        # Set Home active initially
        self.buttons[0].setChecked(True)

    def change_page(self, page_name):
        indexes = {"Home": 0, "Chats": 1, "Documents": 2, "Memory": 3, "Settings": 4}
        if page_name in indexes:
            idx = indexes[page_name]
            self.window.pages.setCurrentIndex(idx)
            current_widget = self.window.pages.widget(idx)
            if hasattr(current_widget, "refresh_data"):
                current_widget.refresh_data()
            for button in self.buttons:
                button.setChecked(button.property("page") == page_name)
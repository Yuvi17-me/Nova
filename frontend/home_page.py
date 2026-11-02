from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSizePolicy,
    QWidget,
)

from frontend.styles import (
    COLOR_BG_CANVAS,
    COLOR_BORDER_SUBTLE,
    COLOR_BORDER_MEDIUM,
    COLOR_ACCENT_PRIMARY,
    COLOR_ACCENT_HOVER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
)
from frontend.components.nova_logo import NovaLogoWidget


class HomePage(QFrame):
    def __init__(self, window=None):
        super().__init__()
        self.window = window

        self.setStyleSheet(f"""
            .HomePage {{
                background: {COLOR_BG_CANVAS};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        # Outer layout with center alignment to prevent widescreen stretching
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(32, 28, 32, 28)
        outer_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Centered content container (max-width 860px)
        content_wrapper = QWidget()
        content_wrapper.setMaximumWidth(860)
        content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_wrapper.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(content_wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # ----------------------------------------------------
        # DATE & GREETING
        # ----------------------------------------------------
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        logo_mini = NovaLogoWidget(size=18)
        top_row.addWidget(logo_mini)

        today_str = datetime.now().strftime("%A  /  %B %d, %Y").upper()
        eyebrow = QLabel(today_str)
        eyebrow.setStyleSheet("color: #818CF8; font-size: 10px; font-weight: 700; letter-spacing: 1.5px;")
        top_row.addWidget(eyebrow)
        top_row.addStretch()
        layout.addLayout(top_row)

        hour = datetime.now().hour
        if hour < 12:
            time_greeting = "Good morning,\nYuvraj."
        elif hour < 18:
            time_greeting = "Good afternoon,\nYuvraj."
        else:
            time_greeting = "Good evening,\nYuvraj."

        title = QLabel(time_greeting)
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 34px;
                font-weight: 800;
                line-height: 110%;
                letter-spacing: -0.6px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(title)

        subtitle = QLabel("A private, local AI environment to think, create, and automate your desktop.")
        subtitle.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; background: transparent; border: none;")
        layout.addWidget(subtitle)

        # ----------------------------------------------------
        # HERO BANNER (COMPACT & PROPORTIONAL)
        # ----------------------------------------------------
        hero = QFrame()
        hero.setStyleSheet(f"""
            .QFrame {{
                background: #121522;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 14px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(22, 18, 22, 18)
        hero_layout.setSpacing(18)

        hero_text = QVBoxLayout()
        hero_text.setSpacing(4)
        hero_title = QLabel("What are we building today?")
        hero_title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 17px; font-weight: 700; background: transparent; border: none;")
        hero_copy = QLabel("Nova can find your resume, manage desktop playback, search documents, or code with you.")
        hero_copy.setWordWrap(True)
        hero_copy.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; background: transparent; border: none;")
        hero_text.addWidget(hero_title)
        hero_text.addWidget(hero_copy)
        hero_layout.addLayout(hero_text, 1)

        quick_action = QPushButton("Open Assistant  →")
        quick_action.setCursor(Qt.PointingHandCursor)
        quick_action.setMinimumSize(155, 42)
        quick_action.setStyleSheet(f"""
            QPushButton {{
                color: #FFFFFF;
                background: {COLOR_ACCENT_PRIMARY};
                border: none;
                border-radius: 9px;
                font-size: 13px;
                font-weight: 700;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background: #4F46E5;
            }}
        """)
        quick_action.clicked.connect(self.go_to_chat)
        hero_layout.addWidget(quick_action)
        layout.addWidget(hero)

        # ----------------------------------------------------
        # WORKSPACE CARDS
        # ----------------------------------------------------
        section = QLabel("YOUR WORKSPACE")
        section.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; margin-top: 4px; background: transparent; border: none;")
        layout.addWidget(section)

        cards = QGridLayout()
        cards.setSpacing(14)

        card_data = [
            ("💬", "Recent conversations", "Pick up previous tasks & thoughts", "#6366F1", "Chats"),
            ("📄", "Document intelligence", "Search your local knowledge base", "#38BDF8", "Documents"),
            ("◈", "Long-term memory", "Inspect context Nova has retained", "#A855F7", "Memory"),
        ]

        for index, (icon, heading, detail, accent, target_page) in enumerate(card_data):
            card = QPushButton()
            card.setCursor(Qt.PointingHandCursor)
            card.setMinimumHeight(120)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card.setStyleSheet(f"""
                QPushButton {{
                    background: #111420;
                    border: 1px solid {COLOR_BORDER_SUBTLE};
                    border-radius: 12px;
                    text-align: left;
                    padding: 16px;
                }}
                QPushButton:hover {{
                    background: #171B2B;
                    border: 1px solid {COLOR_BORDER_MEDIUM};
                }}
                QPushButton:pressed {{
                    background: #0E101A;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
            card.clicked.connect(lambda chk=False, p=target_page: self.navigate_to(p))

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(2, 2, 2, 2)
            card_layout.setSpacing(6)

            top_row = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet(f"font-size: 15px; color: {accent}; background: transparent; border: none;")
            top_row.addWidget(icon_lbl)
            top_row.addStretch()
            card_layout.addLayout(top_row)

            card_title = QLabel(heading)
            card_title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px; font-weight: 600; background: transparent; border: none;")
            card_detail = QLabel(detail)
            card_detail.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px; background: transparent; border: none;")
            card_detail.setWordWrap(True)

            card_layout.addWidget(card_title)
            card_layout.addWidget(card_detail)
            card_layout.addStretch()

            cards.addWidget(card, 0, index)

        layout.addLayout(cards)
        layout.addStretch()

        outer_layout.addWidget(content_wrapper)

    def go_to_chat(self):
        self.navigate_to("Chats")

    def navigate_to(self, page_name):
        if self.window and hasattr(self.window, "sidebar"):
            self.window.sidebar.change_page(page_name)
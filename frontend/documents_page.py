from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QSizePolicy,
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


class DocumentsPage(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            .DocumentsPage {{
                background: {COLOR_BG_CANVAS};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        # Center alignment
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(32, 28, 32, 28)
        outer_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Centered container (max-width 820px)
        content_wrapper = QWidget()
        content_wrapper.setMaximumWidth(820)
        content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_wrapper.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(content_wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title = QLabel("Documents")
        title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; background: transparent; border: none;")
        subtitle = QLabel("A private local index of the files and notes Nova can search and understand.")
        subtitle.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; background: transparent; border: none;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ----------------------------------------------------
        # TOOLBAR
        # ----------------------------------------------------
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)

        search = QLineEdit()
        search.setPlaceholderText("Search your local documents...")
        search.setStyleSheet(f"""
            QLineEdit {{
                color: {COLOR_TEXT_PRIMARY};
                background: #121522;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 9px;
                padding: 11px 14px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLOR_ACCENT_PRIMARY};
            }}
        """)

        upload = QPushButton("Add Document  +")
        upload.setCursor(Qt.PointingHandCursor)
        upload.setStyleSheet(f"""
            QPushButton {{
                color: #FFFFFF;
                background: {COLOR_ACCENT_PRIMARY};
                border: none;
                border-radius: 9px;
                padding: 11px 18px;
                font-weight: 700;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background: #4F46E5;
            }}
        """)

        toolbar.addWidget(search, 1)
        toolbar.addWidget(upload)
        layout.addLayout(toolbar)

        # ----------------------------------------------------
        # EMPTY STATE DROPZONE
        # ----------------------------------------------------
        empty = QFrame()
        empty.setObjectName("dropzone_box")
        empty.setStyleSheet(f"""
            QFrame#dropzone_box {{
                background: #111420;
                border: 1px dashed {COLOR_BORDER_MEDIUM};
                border-radius: 14px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        empty_layout = QVBoxLayout(empty)
        empty_layout.setContentsMargins(32, 44, 32, 44)
        empty_layout.setSpacing(8)

        empty_icon = QLabel("📄")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon.setStyleSheet("font-size: 32px; background: transparent; border: none;")
        empty_layout.addWidget(empty_icon)

        empty_title = QLabel("Knowledge Base Ready")
        empty_title.setAlignment(Qt.AlignCenter)
        empty_title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 18px; font-weight: 700; background: transparent; border: none;")

        empty_copy = QLabel("Drop PDFs, resumes, research notes, or code to chat with your local documents.")
        empty_copy.setAlignment(Qt.AlignCenter)
        empty_copy.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 13px; background: transparent; border: none;")

        empty_layout.addWidget(empty_title)
        empty_layout.addWidget(empty_copy)
        layout.addWidget(empty)
        layout.addStretch()

        outer_layout.addWidget(content_wrapper)
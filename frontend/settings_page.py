from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
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


class SettingsPage(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            .SettingsPage {{
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

        # Centered container (max-width 800px)
        content_wrapper = QWidget()
        content_wrapper.setMaximumWidth(800)
        content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_wrapper.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(content_wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title = QLabel("Settings")
        title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; background: transparent; border: none;")
        subtitle = QLabel("Configure models, privacy policies, and automation controls for Nova.")
        subtitle.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; background: transparent; border: none;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ----------------------------------------------------
        # SETTINGS PANEL
        # ----------------------------------------------------
        panel = QFrame()
        panel.setObjectName("settings_panel")
        panel.setStyleSheet(f"""
            QFrame#settings_panel {{
                background: #111420;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 14px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 22, 24, 22)
        panel_layout.setSpacing(18)

        heading = QLabel("Assistant Preferences")
        heading.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 16px; font-weight: 700; background: transparent; border: none;")
        panel_layout.addWidget(heading)

        options = [
            ("Local execution first", "Always process system tasks and file actions directly on this PC.", QCheckBox()),
            ("Persistent memory", "Allow Nova to retain context across restarts.", QCheckBox()),
            ("Audio & media controls", "Enable shortcut commands for media playback and system controls.", QCheckBox()),
        ]

        for label, description, control in options:
            row = QHBoxLayout()
            text = QVBoxLayout()
            text.setSpacing(2)

            name = QLabel(label)
            name.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            detail = QLabel(description)
            detail.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px; background: transparent; border: none;")

            text.addWidget(name)
            text.addWidget(detail)

            control.setChecked(True)
            control.setCursor(Qt.PointingHandCursor)
            control.setStyleSheet(f"""
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                    border-radius: 5px;
                    border: 1px solid #2B334E;
                    background: #181C2B;
                }}
                QCheckBox::indicator:hover {{
                    border: 1px solid {COLOR_ACCENT_PRIMARY};
                }}
                QCheckBox::indicator:checked {{
                    background: {COLOR_ACCENT_PRIMARY};
                    border: 1px solid {COLOR_ACCENT_PRIMARY};
                }}
            """)

            row.addLayout(text, 1)
            row.addWidget(control)
            panel_layout.addLayout(row)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background: {COLOR_BORDER_SUBTLE}; max-height: 1px;")
        panel_layout.addWidget(divider)

        # Model Selector Row
        model_row = QHBoxLayout()
        model_text = QVBoxLayout()
        model_text.setSpacing(2)

        model_label = QLabel("Default Intelligence Engine")
        model_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        model_desc = QLabel("Primary local LLM used when queries aren't handled by AgentCore.")
        model_desc.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px; background: transparent; border: none;")
        model_text.addWidget(model_label)
        model_text.addWidget(model_desc)

        model = QComboBox()
        model.addItems([
            "Ollama: qwen3:1.7b (Fast & Lightweight)",
            "Ollama: qwen3:4b (High Intelligence)",
            "Ollama: llama3.2",
            "AgentCore Direct Only"
        ])
        model.setStyleSheet(f"""
            QComboBox {{
                color: {COLOR_TEXT_PRIMARY};
                background: #181C2B;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                min-width: 240px;
            }}
            QComboBox:hover {{
                border: 1px solid {COLOR_ACCENT_PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)

        model_row.addLayout(model_text, 1)
        model_row.addWidget(model)
        panel_layout.addLayout(model_row)

        layout.addWidget(panel)
        layout.addStretch()

        outer_layout.addWidget(content_wrapper)
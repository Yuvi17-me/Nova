import html
import re
from datetime import datetime

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QWidget,
    QGraphicsOpacityEffect,
    QSizePolicy,
    QApplication,
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QThread,
    Signal,
    QObject,
    QTimer,
)

from PySide6.QtGui import QTextDocument

from backend.ai.ollama_engine import OllamaEngine
from backend.agent.agent_core import AgentCore
from frontend.styles import (
    COLOR_BG_CANVAS,
    COLOR_BORDER_SUBTLE,
    COLOR_BORDER_MEDIUM,
    COLOR_ACCENT_PRIMARY,
    COLOR_ACCENT_HOVER,
    COLOR_ACCENT_CYAN,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_USER_BUBBLE_BG,
    COLOR_USER_BUBBLE_BORDER,
    COLOR_AI_BUBBLE_BG,
    COLOR_AI_BUBBLE_BORDER,
    COLOR_CODE_BG,
    COLOR_CODE_BORDER,
)
from frontend.components.nova_logo import NovaLogoWidget


# ============================================================
# AI WORKER
# ============================================================

class AIWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, message, history=None):
        super().__init__()
        self.message = message
        self.history = history or []

    def run(self):
        try:
            # ------------------------------------------------
            # First try AgentCore (Fast system/file actions, memory, utilities)
            # ------------------------------------------------
            agent = AgentCore()
            result = agent.process(self.message)

            # If AgentCore handled the command
            if result is not None:
                success, response = result
                self.finished.emit(str(response))
                return

            # ------------------------------------------------
            # Otherwise use Ollama LLM with history & personalized memory
            # ------------------------------------------------
            engine = OllamaEngine()
            response = engine.chat(self.message, history=self.history)
            self.finished.emit(str(response))

        except Exception as e:
            self.error.emit(str(e))


# ============================================================
# ANIMATED THINKING INDICATOR WIDGET
# ============================================================

class ThinkingIndicatorWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("thinking_widget")
        self.setStyleSheet(f"""
            QFrame#thinking_widget {{
                background: {COLOR_AI_BUBBLE_BG};
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 14px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        self.setMaximumWidth(400)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 16, 10)
        layout.setSpacing(10)

        # Custom Nova Mini Logo
        logo = NovaLogoWidget(size=20)
        layout.addWidget(logo)

        # Text label
        self.label = QLabel("Nova is processing")
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.label)
        layout.addStretch()

        # Dot animation timer
        self.dot_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(300)

    def _animate(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.label.setText(f"Nova is processing{dots}")

    def stop(self):
        self.timer.stop()


# ============================================================
# SUGGESTION CHIP WIDGET
# ============================================================

class SuggestionChip(QPushButton):
    def __init__(self, icon, title, description, parent=None):
        super().__init__(parent)
        self.title_text = title
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(64)

        self.setStyleSheet(f"""
            QPushButton {{
                background: #111420;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 12px;
                text-align: left;
                padding: 10px 14px;
            }}
            QPushButton:hover {{
                background: #181C2C;
                border: 1px solid {COLOR_ACCENT_PRIMARY};
            }}
            QPushButton:pressed {{
                background: #0E101A;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                background: #181C2B;
                border-radius: 8px;
                padding: 6px 8px;
                border: none;
            }}
        """)
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)

        d_lbl = QLabel(description)
        d_lbl.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_MUTED};
                font-size: 11px;
                background: transparent;
                border: none;
            }}
        """)

        text_layout.addWidget(t_lbl)
        text_layout.addWidget(d_lbl)
        layout.addLayout(text_layout, 1)


# ============================================================
# CHAT PAGE
# ============================================================

class ChatPage(QFrame):

    def __init__(self):
        super().__init__()

        self.ai_thread = None
        self.ai_worker = None
        self.thinking_widget = None
        self.message_count = 0
        self.conversation_history = []
        self.last_user_message = ""

        self.setStyleSheet(f"""
            .ChatPage {{
                background: {COLOR_BG_CANVAS};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        # Outer layout: Centers the chat column (max-width 840px) on widescreen
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(32, 20, 32, 20)
        outer_layout.setAlignment(Qt.AlignHCenter)

        # Centered container
        chat_wrapper = QWidget()
        chat_wrapper.setMaximumWidth(840)
        chat_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chat_wrapper.setStyleSheet("background: transparent; border: none;")

        main_layout = QVBoxLayout(chat_wrapper)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # ----------------------------------------------------
        # TOP HEADER
        # ----------------------------------------------------
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 4)
        header_layout.setSpacing(12)

        # Nova Brand icon
        header_logo = NovaLogoWidget(size=24)
        header_layout.addWidget(header_logo)

        # Left title & status
        title_group = QVBoxLayout()
        title_group.setSpacing(2)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        title_label = QLabel("Nova Assistant")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 800;
                letter-spacing: -0.3px;
                background: transparent;
                border: none;
            }}
        """)
        title_row.addWidget(title_label)

        version_pill = QLabel("v2.0 Local")
        version_pill.setStyleSheet(f"""
            QLabel {{
                color: #818CF8;
                background: #171A2E;
                border: 1px solid #283052;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 7px;
            }}
        """)
        title_row.addWidget(version_pill)
        title_row.addStretch()

        title_group.addLayout(title_row)

        status_row = QHBoxLayout()
        status_row.setSpacing(6)

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #6366F1; font-size: 10px;")
        status_row.addWidget(self.status_dot)

        self.status_text = QLabel("Local intelligence ready")
        self.status_text.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px; font-weight: 500;")
        status_row.addWidget(self.status_text)
        status_row.addStretch()

        title_group.addLayout(status_row)
        header_layout.addLayout(title_group)
        header_layout.addStretch()

        # Right action: New Chat Button
        self.new_chat_btn = QPushButton("+  New Chat")
        self.new_chat_btn.setCursor(Qt.PointingHandCursor)
        self.new_chat_btn.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_TEXT_SECONDARY};
                background: #131622;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 9px;
                font-size: 12px;
                font-weight: 600;
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                color: {COLOR_TEXT_PRIMARY};
                background: #1C2133;
                border: 1px solid {COLOR_BORDER_MEDIUM};
            }}
            QPushButton:pressed {{
                background: #0E101A;
            }}
        """)
        self.new_chat_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(self.new_chat_btn)

        main_layout.addWidget(header_widget)

        # ----------------------------------------------------
        # SCROLL AREA
        # ----------------------------------------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget {
                background: transparent;
                border: none;
            }
        """)

        # Chat container inside scroll
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background: transparent; border: none;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 6, 0, 14)
        self.chat_layout.setSpacing(14)

        # Welcome Empty State Hero
        self.welcome_widget = self._create_welcome_hero()
        self.chat_layout.addWidget(self.welcome_widget)

        # Bottom stretch to push bubbles upward
        self.chat_layout.addStretch(1)

        self.scroll.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll, 1)

        # ----------------------------------------------------
        # FLOATING INPUT CONTAINER
        # ----------------------------------------------------
        input_container = QFrame()
        input_container.setObjectName("input_box_frame")
        input_container.setStyleSheet(f"""
            QFrame#input_box_frame {{
                background: #111420;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 16px;
            }}
            QFrame#input_box_frame:hover {{
                border: 1px solid #384364;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(14, 8, 10, 8)
        input_layout.setSpacing(4)

        entry_row = QHBoxLayout()
        entry_row.setSpacing(10)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Message Nova (e.g. 'find my resume', 'open downloads', 'resume music')...")
        self.input_box.setStyleSheet(f"""
            QLineEdit {{
                color: {COLOR_TEXT_PRIMARY};
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 6px 2px;
            }}
            QLineEdit:disabled {{
                color: {COLOR_TEXT_MUTED};
            }}
        """)

        self.send_button = QPushButton("➤")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setFixedSize(36, 36)
        self.send_button.setStyleSheet(f"""
            QPushButton {{
                color: #FFFFFF;
                background: {COLOR_ACCENT_PRIMARY};
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
                padding-left: 2px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background: #4F46E5;
            }}
            QPushButton:disabled {{
                background: #1C2133;
                color: #4B5570;
            }}
        """)

        entry_row.addWidget(self.input_box, 1)
        entry_row.addWidget(self.send_button)
        input_layout.addLayout(entry_row)

        # Footer helper info
        footer_row = QHBoxLayout()
        footer_row.setContentsMargins(2, 0, 2, 0)
        footer_label = QLabel("Press Enter to send  •  Agent automation and local AI ready")
        footer_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 11px;")
        footer_row.addWidget(footer_label)
        footer_row.addStretch()

        input_layout.addLayout(footer_row)
        main_layout.addWidget(input_container)

        # Add centered wrapper to outer layout
        outer_layout.addWidget(chat_wrapper)

        # ----------------------------------------------------
        # CONNECTIONS
        # ----------------------------------------------------
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

    # ========================================================
    # CREATE WELCOME HERO
    # ========================================================

    def _create_welcome_hero(self):
        hero = QWidget()
        layout = QVBoxLayout(hero)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Nova Custom Emblem
        emblem_container = QHBoxLayout()
        emblem = NovaLogoWidget(size=54)
        emblem_container.addWidget(emblem)
        emblem_container.setAlignment(Qt.AlignCenter)
        layout.addLayout(emblem_container)

        # Dynamic greeting based on hour
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning, Yuvraj"
        elif hour < 18:
            greeting = "Good afternoon, Yuvraj"
        else:
            greeting = "Good evening, Yuvraj"

        title = QLabel(greeting)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 26px;
                font-weight: 800;
                letter-spacing: -0.4px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(title)

        subtitle = QLabel("What would you like Nova to find, automate, or write for you today?")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_SECONDARY};
                font-size: 14px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(subtitle)

        # Starter Chips Grid
        chips_grid = QGridLayout()
        chips_grid.setSpacing(12)

        suggestions = [
            ("📄", "Find my resume", "Search Downloads & Documents for resume files"),
            ("📂", "Open Downloads folder", "Quickly open your local downloads folder"),
            ("🎵", "Resume music", "Toggle Windows media playback for music or video"),
            ("🔒", "Lock my computer", "Secure your desktop workstation instantly"),
            ("🔊", "Mute sound", "Toggle computer audio mute"),
            ("⚡", "What can you do?", "Explore Nova's tools, system commands, and AI"),
        ]

        for idx, (icon, prompt, desc) in enumerate(suggestions):
            chip = SuggestionChip(icon, prompt, desc)
            chip.clicked.connect(lambda chk=False, p=prompt: self.submit_prompt(p))
            row = idx // 2
            col = idx % 2
            chips_grid.addWidget(chip, row, col)

        layout.addLayout(chips_grid)
        return hero

    # ========================================================
    # PROMPT SUBMISSION
    # ========================================================

    def submit_prompt(self, text):
        self.input_box.setText(text)
        self.send_message()

    def send_message(self):
        message = self.input_box.text().strip()
        if not message:
            return

        if self.ai_thread is not None:
            return

        # Hide welcome hero on first message
        if self.welcome_widget is not None and self.welcome_widget.isVisible():
            self.welcome_widget.hide()

        # Add User message
        self.add_message(message, user=True)
        self.input_box.clear()

        # Show animated Thinking widget
        self.show_thinking_message()

        # Update status
        self.status_dot.setStyleSheet("color: #F59E0B; font-size: 10px;")
        self.status_text.setText("Nova is working...")

        # Store user message for conversation history
        self.last_user_message = message

        # Disable input while processing
        self.input_box.setEnabled(False)
        self.send_button.setEnabled(False)

        # Run AI Thread with multi-turn history
        self.ai_thread = QThread()
        self.ai_worker = AIWorker(message, history=list(self.conversation_history))
        self.ai_worker.moveToThread(self.ai_thread)

        self.ai_thread.started.connect(self.ai_worker.run)
        self.ai_worker.finished.connect(self.handle_ai_response)
        self.ai_worker.error.connect(self.handle_ai_error)

        self.ai_worker.finished.connect(self.ai_thread.quit)
        self.ai_worker.error.connect(self.ai_thread.quit)
        self.ai_thread.finished.connect(self.cleanup_ai_thread)

        self.ai_thread.start()

    # ========================================================
    # HANDLE AI RESPONSE
    # ========================================================

    def handle_ai_response(self, response):
        self.remove_thinking_message()

        if response is None:
            response = ""
        response = str(response).strip()
        if not response:
            response = "I completed the request."

        # Record turns in conversation history (capped at 20)
        if self.last_user_message:
            self.conversation_history.append({"role": "user", "content": self.last_user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

        self.add_message(response, user=False)

        self.status_dot.setStyleSheet("color: #6366F1; font-size: 10px;")
        self.status_text.setText("Local intelligence ready")

        self.input_box.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_box.setFocus()

        QTimer.singleShot(60, self.scroll_to_bottom)

    def handle_ai_error(self, error):
        self.remove_thinking_message()

        self.add_message(
            f"⚠️ **Could not complete request**\n\n```text\n{error}\n```",
            user=False
        )

        self.status_dot.setStyleSheet("color: #EF4444; font-size: 10px;")
        self.status_text.setText("Error encountered")

        self.input_box.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_box.setFocus()

        QTimer.singleShot(60, self.scroll_to_bottom)

    # ========================================================
    # THINKING INDICATOR
    # ========================================================

    def show_thinking_message(self):
        self.remove_thinking_message()
        self.thinking_widget = ThinkingIndicatorWidget()

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.addWidget(self.thinking_widget)
        row_layout.addStretch(1)

        # Insert before bottom stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, row)
        self.thinking_row = row

        QTimer.singleShot(40, self.scroll_to_bottom)

    def remove_thinking_message(self):
        if self.thinking_widget is not None:
            self.thinking_widget.stop()
            self.thinking_widget = None

        if hasattr(self, "thinking_row") and self.thinking_row is not None:
            self.chat_layout.removeWidget(self.thinking_row)
            self.thinking_row.deleteLater()
            self.thinking_row = None

        self.chat_layout.activate()
        self.chat_container.adjustSize()

    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(self, text, user=True):
        self.message_count += 1

        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)

        bubble = QFrame()
        bubble_id = f"bubble_{self.message_count}"
        bubble.setObjectName(bubble_id)

        if user:
            # User styling
            bubble.setStyleSheet(f"""
                QFrame#{bubble_id} {{
                    background: {COLOR_USER_BUBBLE_BG};
                    border: 1px solid {COLOR_USER_BUBBLE_BORDER};
                    border-radius: 14px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
            bubble.setMaximumWidth(680)

            bubble_layout = QVBoxLayout(bubble)
            bubble_layout.setContentsMargins(16, 12, 16, 12)
            bubble_layout.setSpacing(4)

            # Sender tag
            tag_label = QLabel("You")
            tag_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 11px; font-weight: 600; background: transparent; border: none;")
            bubble_layout.addWidget(tag_label)

            content_label = QLabel(text)
            content_label.setWordWrap(True)
            content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLOR_TEXT_PRIMARY};
                    font-size: 14px;
                    line-height: 140%;
                    background: transparent;
                    border: none;
                }}
            """)
            bubble_layout.addWidget(content_label)

            row_layout.addStretch(1)
            row_layout.addWidget(bubble, 0, Qt.AlignRight)

        else:
            # Assistant styling
            bubble.setStyleSheet(f"""
                QFrame#{bubble_id} {{
                    background: {COLOR_AI_BUBBLE_BG};
                    border: 1px solid {COLOR_AI_BUBBLE_BORDER};
                    border-radius: 14px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
            bubble.setMaximumWidth(780)

            bubble_layout = QVBoxLayout(bubble)
            bubble_layout.setContentsMargins(18, 14, 18, 14)
            bubble_layout.setSpacing(10)

            # Assistant Header Row (Nova Logo, Name, Copy Button)
            hdr_layout = QHBoxLayout()
            hdr_layout.setSpacing(8)

            nova_mini = NovaLogoWidget(size=16)
            hdr_layout.addWidget(nova_mini)

            nova_tag = QLabel("Nova")
            nova_tag.setStyleSheet(f"""
                QLabel {{
                    color: #818CF8;
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                    background: transparent;
                    border: none;
                }}
            """)
            hdr_layout.addWidget(nova_tag)
            hdr_layout.addStretch()

            # Copy button
            copy_btn = QPushButton("Copy")
            copy_btn.setCursor(Qt.PointingHandCursor)
            copy_btn.setStyleSheet(f"""
                QPushButton {{
                    color: {COLOR_TEXT_MUTED};
                    background: transparent;
                    border: 1px solid {COLOR_BORDER_SUBTLE};
                    border-radius: 6px;
                    font-size: 11px;
                    padding: 3px 8px;
                }}
                QPushButton:hover {{
                    color: {COLOR_TEXT_PRIMARY};
                    background: #1C2133;
                    border: 1px solid {COLOR_BORDER_MEDIUM};
                }}
            """)
            copy_btn.clicked.connect(lambda chk=False, t=text, b=copy_btn: self._copy_text(t, b))
            hdr_layout.addWidget(copy_btn)

            bubble_layout.addLayout(hdr_layout)

            # Format text/markdown
            formatted_html = self.format_markdown(text)

            content_label = QLabel()
            content_label.setWordWrap(True)
            content_label.setTextFormat(Qt.RichText)
            content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_label.setText(formatted_html)
            content_label.setStyleSheet("""
                QLabel {{
                    color: #E2E8F0;
                    font-size: 14px;
                    line-height: 155%;
                    background: transparent;
                    border: none;
                }}
            """)
            bubble_layout.addWidget(content_label)

            row_layout.addWidget(bubble, 0, Qt.AlignLeft)
            row_layout.addStretch(1)

        # Insert before bottom stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, row_widget)

        # Fade in animation
        effect = QGraphicsOpacityEffect(bubble)
        bubble.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(160)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        bubble._anim = anim
        anim.start()

        self.chat_layout.activate()
        row_widget.adjustSize()
        self.chat_container.adjustSize()

        QTimer.singleShot(40, self.scroll_to_bottom)
        return row_widget

    def _copy_text(self, text, button):
        QApplication.clipboard().setText(text)
        button.setText("✓ Copied")
        button.setStyleSheet(f"""
            QPushButton {{
                color: #818CF8;
                background: #171A2E;
                border: 1px solid #283052;
                border-radius: 6px;
                font-size: 11px;
                padding: 3px 8px;
            }}
        """)
        QTimer.singleShot(1600, lambda: self._reset_copy_btn(button))

    def _reset_copy_btn(self, button):
        button.setText("Copy")
        button.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_TEXT_MUTED};
                background: transparent;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 6px;
                font-size: 11px;
                padding: 3px 8px;
            }}
            QPushButton:hover {{
                color: {COLOR_TEXT_PRIMARY};
                background: #1C2133;
                border: 1px solid {COLOR_BORDER_MEDIUM};
            }}
        """)

    # ========================================================
    # FORMAT MARKDOWN WITH CODE BLOCK ENHANCEMENT
    # ========================================================

    def format_markdown(self, text):
        raw_text = str(text)

        # If it contains code blocks, wrap them in styled HTML table boxes
        def code_block_replacer(match):
            lang = (match.group(1) or "code").strip().upper()
            raw_code = match.group(2).strip()
            escaped = html.escape(raw_code)

            # Preserve indentation and line breaks cleanly in Qt rich text
            lines = escaped.split("\n")
            formatted_lines = []
            for line in lines:
                stripped = line.lstrip(" ")
                num_leading = len(line) - len(stripped)
                indent = "&nbsp;" * num_leading
                formatted_lines.append(indent + stripped)
            formatted_code = "<br>".join(formatted_lines)

            return (
                f'<table width="100%" bgcolor="#0A0C14" cellpadding="12" cellspacing="0" '
                f'style="border: 1px solid #1E253B; border-radius: 8px; margin: 10px 0;">'
                f'<tr><td>'
                f'<div style="color: #818CF8; font-family: Consolas, monospace; font-size: 11px; '
                f'font-weight: bold; margin-bottom: 8px; letter-spacing: 0.6px;">● {lang}</div>'
                f'<div style="font-family: Consolas, \'Courier New\', monospace; font-size: 13px; '
                f'color: #38BDF8; line-height: 145%;">'
                f'{formatted_code}'
                f'</div>'
                f'</td></tr></table>'
            )

        # Extract and replace ```lang ... ``` blocks using markdown-safe alphanumeric token
        code_blocks = []
        def stash_code(match):
            idx = len(code_blocks)
            code_blocks.append(code_block_replacer(match))
            return f"NOVACODEBLOCKTOKEN{idx}END"

        processed = re.sub(r'```([a-zA-Z0-9_-]+)?\n?(.*?)```', stash_code, raw_text, flags=re.DOTALL)

        # Convert remaining markdown to HTML using QTextDocument
        doc = QTextDocument()
        doc.setMarkdown(processed)
        doc_html = doc.toHtml()

        # Restore code blocks (cleanly replacing paragraph tags or isolated token)
        for idx, block_html in enumerate(code_blocks):
            token = f"NOVACODEBLOCKTOKEN{idx}END"
            doc_html = re.sub(rf'<p[^>]*>\s*{token}\s*</p>', block_html, doc_html)
            doc_html = doc_html.replace(token, block_html)

        # Custom inline style tweaks
        doc_html = doc_html.replace("<code>", "<code style='background-color: #171A28; color: #38BDF8; font-family: Consolas, monospace; font-size: 12px; padding: 2px 6px; border-radius: 4px;'>")
        doc_html = doc_html.replace("<blockquote>", "<blockquote style='border-left: 3px solid #6366F1; margin: 8px 0; padding-left: 12px; color: #94A3B8;'>")
        doc_html = doc_html.replace("<li>", "<li style='margin-bottom: 4px;'>")
        return doc_html

    # ========================================================
    # CLEAR CHAT
    # ========================================================

    def clear_chat(self):
        # Clear multi-turn history
        self.conversation_history = []
        self.last_user_message = ""

        # Remove all message rows
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                if item.widget() == self.welcome_widget:
                    continue
                item.widget().deleteLater()

        # Show welcome hero again
        if self.welcome_widget is not None:
            self.welcome_widget.show()

        self.message_count = 0
        self.status_dot.setStyleSheet("color: #6366F1; font-size: 10px;")
        self.status_text.setText("Local intelligence ready")
        self.input_box.clear()
        self.input_box.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_box.setFocus()

    # ========================================================
    # THREAD CLEANUP & SCROLL
    # ========================================================

    def cleanup_ai_thread(self):
        if self.ai_worker is not None:
            self.ai_worker.deleteLater()
        if self.ai_thread is not None:
            self.ai_thread.deleteLater()
        self.ai_worker = None
        self.ai_thread = None

    def scroll_to_bottom(self):
        if self.scroll is not None:
            v_bar = self.scroll.verticalScrollBar()
            if v_bar is not None:
                v_bar.setValue(v_bar.maximum())
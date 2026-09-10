from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QWidget,
    QGraphicsOpacityEffect
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QThread,
    Signal,
    QObject
)

from backend.ai.ollama_engine import OllamaEngine
from backend.agent.agent_core import AgentCore


# ============================================================
# AI WORKER
# ============================================================

class AIWorker(QObject):

    chunk = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):

        try:

            # =================================================
            # FIRST: CHECK FOR A TASK
            # =================================================

            agent = AgentCore()

            result = agent.process(
                self.message
            )

            # =================================================
            # TASK FOUND
            # =================================================

            if result is not None:

                success, response = result

                if success:
                    self.chunk.emit(
                        response
                    )

                else:
                    self.chunk.emit(
                        response
                    )

                self.finished.emit()

                return

            # =================================================
            # NORMAL CONVERSATION
            # =================================================

            engine = OllamaEngine()

            for chunk in engine.chat_stream(
                self.message
            ):

                self.chunk.emit(
                    chunk
                )

            self.finished.emit()

        except Exception as e:

            self.error.emit(
                str(e)
            )


# ============================================================
# CHAT PAGE
# ============================================================

class ChatPage(QFrame):

    def __init__(self):

        super().__init__()

        # ====================================================
        # AI THREAD VARIABLES
        # ====================================================

        self.ai_thread = None
        self.ai_worker = None

        # ====================================================
        # STREAMING VARIABLES
        # ====================================================

        self.thinking_widget = None

        self.streaming_widget = None
        self.streaming_label = None
        self.streaming_text = ""

        # ====================================================
        # MAIN BACKGROUND
        # ====================================================

        self.setStyleSheet("""
            QFrame {
                background: #242529;
            }
        """)

        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            35,
            28,
            35,
            25
        )

        main_layout.setSpacing(15)

        # ====================================================
        # HEADER
        # ====================================================

        header = QVBoxLayout()
        header.setSpacing(3)

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = QLabel("Assistant")

        title.setStyleSheet("""
            QLabel {
                color: #F5F5F5;
                font-size: 26px;
                font-weight: 600;
                background: transparent;
            }
        """)

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.status = QLabel(
            "Nova is ready"
        )

        self.status.setStyleSheet("""
            QLabel {
                color: #8F929A;
                font-size: 13px;
                background: transparent;
            }
        """)

        header.addWidget(title)
        header.addWidget(self.status)

        main_layout.addLayout(header)

        # ====================================================
        # CHAT AREA
        # ====================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # ----------------------------------------------------
        # Chat container
        # ----------------------------------------------------

        self.chat_container = QWidget()

        self.chat_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        self.chat_layout = QVBoxLayout(
            self.chat_container
        )

        self.chat_layout.setContentsMargins(
            5,
            15,
            5,
            15
        )

        self.chat_layout.setSpacing(
            12
        )

        # Keeps messages at the top
        self.chat_layout.addStretch()

        self.scroll.setWidget(
            self.chat_container
        )

        main_layout.addWidget(
            self.scroll
        )

        # ====================================================
        # INPUT AREA
        # ====================================================

        input_frame = QFrame()

        input_frame.setStyleSheet("""
            QFrame {
                background: #303136;
                border: 1px solid #41434A;
                border-radius: 14px;
            }
        """)

        input_layout = QHBoxLayout(
            input_frame
        )

        input_layout.setContentsMargins(
            12,
            8,
            8,
            8
        )

        input_layout.setSpacing(
            8
        )

        # ====================================================
        # INPUT BOX
        # ====================================================

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            "Ask Nova to help, search, or perform a task..."
        )

        self.input_box.setStyleSheet("""
            QLineEdit {
                color: #F5F5F5;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 10px;
            }

            QLineEdit:disabled {
                color: #777A82;
            }
        """)

        # ====================================================
        # SEND BUTTON
        # ====================================================

        self.send_button = QPushButton(
            "↑"
        )

        self.send_button.setFixedSize(
            38,
            38
        )

        self.send_button.setStyleSheet("""
            QPushButton {
                color: white;
                background: #6C5CE7;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #7B6AF0;
            }

            QPushButton:pressed {
                background: #5A4BC7;
            }

            QPushButton:disabled {
                background: #45464D;
                color: #888A91;
            }
        """)

        input_layout.addWidget(
            self.input_box
        )

        input_layout.addWidget(
            self.send_button
        )

        main_layout.addWidget(
            input_frame
        )

        # ====================================================
        # CONNECTIONS
        # ====================================================

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input_box.returnPressed.connect(
            self.send_message
        )

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(self):

        message = self.input_box.text().strip()

        # Ignore empty messages
        if not message:
            return

        # ----------------------------------------------------
        # Display user message
        # ----------------------------------------------------

        self.add_message(
            message,
            True
        )

        # Clear input
        self.input_box.clear()

        # ----------------------------------------------------
        # Show thinking indicator
        # ----------------------------------------------------

        self.thinking_widget = self.add_message(
            "Thinking...",
            False
        )

        # ----------------------------------------------------
        # Update status
        # ----------------------------------------------------

        self.status.setText(
            "Thinking..."
        )

        # ----------------------------------------------------
        # Disable input
        # ----------------------------------------------------

        self.input_box.setEnabled(
            False
        )

        self.send_button.setEnabled(
            False
        )

        # ----------------------------------------------------
        # Reset streaming state
        # ----------------------------------------------------

        self.streaming_widget = None
        self.streaming_label = None
        self.streaming_text = ""

        # ====================================================
        # CREATE AI THREAD
        # ====================================================

        self.ai_thread = QThread()

        self.ai_worker = AIWorker(
            message
        )

        # Move worker to background thread
        self.ai_worker.moveToThread(
            self.ai_thread
        )

        # ====================================================
        # THREAD CONNECTIONS
        # ====================================================

        self.ai_thread.started.connect(
            self.ai_worker.run
        )

        # Streaming chunks
        self.ai_worker.chunk.connect(
            self.handle_ai_chunk
        )

        # Finished
        self.ai_worker.finished.connect(
            self.handle_ai_finished
        )

        # Error
        self.ai_worker.error.connect(
            self.handle_ai_error
        )

        # Stop thread after completion
        self.ai_worker.finished.connect(
            self.ai_thread.quit
        )

        self.ai_worker.error.connect(
            self.ai_thread.quit
        )

        # Cleanup after thread finishes
        self.ai_thread.finished.connect(
            self.cleanup_ai_thread
        )

        # ====================================================
        # START AI
        # ====================================================

        self.ai_thread.start()

    # ========================================================
    # HANDLE STREAMING CHUNK
    # ========================================================

    def handle_ai_chunk(
        self,
        chunk
    ):

        # ----------------------------------------------------
        # First chunk
        # ----------------------------------------------------

        if self.streaming_widget is None:

            # Remove "Thinking..."
            self.remove_thinking_message()

            # Reset response
            self.streaming_text = ""

            # Create streaming bubble
            self.streaming_widget = (
                self.create_streaming_message()
            )

        # ----------------------------------------------------
        # Add chunk
        # ----------------------------------------------------

        self.streaming_text += chunk

        # Update text
        self.streaming_label.setText(
            self.streaming_text
        )

        # ----------------------------------------------------
        # Update status
        # ----------------------------------------------------

        self.status.setText(
            "Generating..."
        )

        # ----------------------------------------------------
        # Scroll down
        # ----------------------------------------------------

        self.scroll_to_bottom()

    # ========================================================
    # CREATE STREAMING MESSAGE
    # ========================================================

    def create_streaming_message(self):

        # ----------------------------------------------------
        # Row
        # ----------------------------------------------------

        row_widget = QWidget()

        row_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        row = QHBoxLayout(
            row_widget
        )

        row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ----------------------------------------------------
        # Bubble
        # ----------------------------------------------------

        bubble = QFrame()

        bubble.setStyleSheet("""
            QFrame {
                background: #303136;
                border: 1px solid #3D3F46;
                border-radius: 14px;
            }
        """)

        bubble_layout = QVBoxLayout(
            bubble
        )

        bubble_layout.setContentsMargins(
            14,
            10,
            14,
            10
        )

        # ----------------------------------------------------
        # Streaming label
        # ----------------------------------------------------

        self.streaming_label = QLabel(
            ""
        )

        self.streaming_label.setWordWrap(
            True
        )

        self.streaming_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.streaming_label.setStyleSheet("""
            QLabel {
                color: #F5F5F5;
                font-size: 14px;
                border: none;
                background: transparent;
            }
        """)

        bubble_layout.addWidget(
            self.streaming_label
        )

        # ----------------------------------------------------
        # Alignment
        # ----------------------------------------------------

        row.addWidget(
            bubble
        )

        row.addStretch()

        # ----------------------------------------------------
        # Add to chat
        # ----------------------------------------------------

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row_widget
        )

        # ----------------------------------------------------
        # Fade-in animation
        # ----------------------------------------------------

        effect = QGraphicsOpacityEffect(
            bubble
        )

        bubble.setGraphicsEffect(
            effect
        )

        animation = QPropertyAnimation(
            effect,
            b"opacity"
        )

        animation.setDuration(
            180
        )

        animation.setStartValue(
            0.0
        )

        animation.setEndValue(
            1.0
        )

        bubble._animation = animation

        animation.start()

        return row_widget

    # ========================================================
    # HANDLE AI FINISHED
    # ========================================================

    def handle_ai_finished(self):

        # ----------------------------------------------------
        # Update status
        # ----------------------------------------------------

        self.status.setText(
            "Nova is ready"
        )

        # ----------------------------------------------------
        # Enable input
        # ----------------------------------------------------

        self.input_box.setEnabled(
            True
        )

        self.send_button.setEnabled(
            True
        )

        self.input_box.setFocus()

        # ----------------------------------------------------
        # Reset streaming references
        # ----------------------------------------------------

        self.streaming_widget = None
        self.streaming_label = None
        self.streaming_text = ""

    # ========================================================
    # HANDLE AI ERROR
    # ========================================================

    def handle_ai_error(
        self,
        error
    ):

        # Remove Thinking bubble
        self.remove_thinking_message()

        # Remove streaming bubble if one exists
        if self.streaming_widget is not None:

            self.chat_layout.removeWidget(
                self.streaming_widget
            )

            self.streaming_widget.deleteLater()

            self.streaming_widget = None
            self.streaming_label = None
            self.streaming_text = ""

        # ----------------------------------------------------
        # Display error
        # ----------------------------------------------------

        self.add_message(
            "Sorry, I couldn't process that request.\n\n"
            f"Error: {error}",
            False
        )

        # ----------------------------------------------------
        # Update status
        # ----------------------------------------------------

        self.status.setText(
            "AI connection error"
        )

        # ----------------------------------------------------
        # Enable input
        # ----------------------------------------------------

        self.input_box.setEnabled(
            True
        )

        self.send_button.setEnabled(
            True
        )

        self.input_box.setFocus()

    # ========================================================
    # REMOVE THINKING MESSAGE
    # ========================================================

    def remove_thinking_message(self):

        if self.thinking_widget is None:
            return

        # Remove from layout
        self.chat_layout.removeWidget(
            self.thinking_widget
        )

        # Delete widget
        self.thinking_widget.deleteLater()

        self.thinking_widget = None

    # ========================================================
    # CLEANUP AI THREAD
    # ========================================================

    def cleanup_ai_thread(self):

        if self.ai_worker is not None:

            self.ai_worker.deleteLater()

        if self.ai_thread is not None:

            self.ai_thread.deleteLater()

        self.ai_worker = None
        self.ai_thread = None

    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        text,
        user
    ):

        # ----------------------------------------------------
        # Message row
        # ----------------------------------------------------

        row_widget = QWidget()

        row_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        row = QHBoxLayout(
            row_widget
        )

        row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ----------------------------------------------------
        # Message bubble
        # ----------------------------------------------------

        bubble = QFrame()

        if user:

            bubble.setStyleSheet("""
                QFrame {
                    background: #6C5CE7;
                    border-radius: 14px;
                }
            """)

        else:

            bubble.setStyleSheet("""
                QFrame {
                    background: #303136;
                    border: 1px solid #3D3F46;
                    border-radius: 14px;
                }
            """)

        # ----------------------------------------------------
        # Bubble layout
        # ----------------------------------------------------

        bubble_layout = QVBoxLayout(
            bubble
        )

        bubble_layout.setContentsMargins(
            14,
            10,
            14,
            10
        )

        # ----------------------------------------------------
        # Message text
        # ----------------------------------------------------

        label = QLabel(
            text
        )

        label.setWordWrap(
            True
        )

        label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        label.setStyleSheet("""
            QLabel {
                color: #F5F5F5;
                font-size: 14px;
                border: none;
                background: transparent;
            }
        """)

        bubble_layout.addWidget(
            label
        )

        # ----------------------------------------------------
        # Alignment
        # ----------------------------------------------------

        if user:

            row.addStretch()

            row.addWidget(
                bubble
            )

        else:

            row.addWidget(
                bubble
            )

            row.addStretch()

        # ----------------------------------------------------
        # Add row to chat
        # ----------------------------------------------------

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row_widget
        )

        # ----------------------------------------------------
        # Fade-in animation
        # ----------------------------------------------------

        effect = QGraphicsOpacityEffect(
            bubble
        )

        bubble.setGraphicsEffect(
            effect
        )

        animation = QPropertyAnimation(
            effect,
            b"opacity"
        )

        animation.setDuration(
            220
        )

        animation.setStartValue(
            0.0
        )

        animation.setEndValue(
            1.0
        )

        # Keep animation alive
        bubble._animation = animation

        animation.start()

        # ----------------------------------------------------
        # Scroll
        # ----------------------------------------------------

        self.scroll_to_bottom()

        # ----------------------------------------------------
        # Return widget
        # ----------------------------------------------------

        return row_widget

    # ========================================================
    # SCROLL TO BOTTOM
    # ========================================================

    def scroll_to_bottom(self):

        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )
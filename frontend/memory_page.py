from PySide6.QtCore import Qt
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
    QSizePolicy,
    QMessageBox,
)

from backend.memory.memory_manager import MemoryManager
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


class MemoryPage(QFrame):
    """
    Nova Personal Memory & Learning Management Hub.
    Provides complete visibility, control, and editing over learned preferences,
    facts, and the user profile stored in SQLite.
    """

    def __init__(self):
        super().__init__()
        self.memory = MemoryManager()

        self.setStyleSheet(f"""
            .MemoryPage {{
                background: {COLOR_BG_CANVAS};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        # Outer centering layout (840px max width to prevent widescreen stretching)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(32, 24, 32, 24)
        outer_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        content_wrapper = QWidget()
        content_wrapper.setMaximumWidth(840)
        content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_wrapper.setStyleSheet("background: transparent; border: none;")

        self.main_layout = QVBoxLayout(content_wrapper)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(18)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------
        header_row = QHBoxLayout()
        header_text = QVBoxLayout()
        header_text.setSpacing(4)

        title = QLabel("Personal Memory & Knowledge")
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
        subtitle = QLabel("Context Nova autonomously learns and retains across sessions with 100% privacy on your device.")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_SECONDARY};
                font-size: 13px;
                background: transparent;
                border: none;
            }}
        """)
        header_text.addWidget(title)
        header_text.addWidget(subtitle)
        header_row.addLayout(header_text, 1)

        # Refresh button
        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_TEXT_SECONDARY};
                background: #131622;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                color: {COLOR_TEXT_PRIMARY};
                background: #1C2133;
                border: 1px solid {COLOR_BORDER_MEDIUM};
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        header_row.addWidget(refresh_btn)

        self.main_layout.addLayout(header_row)

        # ----------------------------------------------------
        # SUMMARY METRIC CARDS
        # ----------------------------------------------------
        self.metrics_layout = QHBoxLayout()
        self.metrics_layout.setSpacing(12)
        self._build_metric_cards()
        self.main_layout.addLayout(self.metrics_layout)

        # ----------------------------------------------------
        # "TEACH NOVA" DIRECT INPUT PANEL
        # ----------------------------------------------------
        teach_panel = QFrame()
        teach_panel.setObjectName("teach_panel")
        teach_panel.setStyleSheet(f"""
            QFrame#teach_panel {{
                background: #111420;
                border: 1px solid {COLOR_BORDER_MEDIUM};
                border-radius: 14px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        teach_layout = QVBoxLayout(teach_panel)
        teach_layout.setContentsMargins(18, 14, 18, 14)
        teach_layout.setSpacing(10)

        teach_header = QLabel("Teach Nova a New Fact or Rule")
        teach_header.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px; font-weight: 700;")
        teach_layout.addWidget(teach_header)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.teach_input = QLineEdit()
        self.teach_input.setPlaceholderText("e.g. 'I prefer Modern C++20 with CMake' or 'Always keep responses concise'...")
        self.teach_input.setStyleSheet(f"""
            QLineEdit {{
                color: {COLOR_TEXT_PRIMARY};
                background: #0A0C14;
                border: 1px solid {COLOR_BORDER_SUBTLE};
                border-radius: 10px;
                font-size: 13px;
                padding: 10px 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLOR_ACCENT_PRIMARY};
            }}
        """)
        self.teach_input.returnPressed.connect(self.add_custom_memory)
        input_row.addWidget(self.teach_input, 1)

        add_btn = QPushButton("+ Remember")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                color: #FFFFFF;
                background: {COLOR_ACCENT_PRIMARY};
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
                padding: 10px 18px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background: #4F46E5;
            }}
        """)
        add_btn.clicked.connect(self.add_custom_memory)
        input_row.addWidget(add_btn)

        teach_layout.addLayout(input_row)
        self.main_layout.addWidget(teach_panel)

        # ----------------------------------------------------
        # ACTIVE MEMORIES LIST SECTION
        # ----------------------------------------------------
        list_header_row = QHBoxLayout()
        list_title = QLabel("Saved Memories & Learnings")
        list_title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 15px; font-weight: 700;")
        list_header_row.addWidget(list_title)
        list_header_row.addStretch()

        clear_all_btn = QPushButton("Clear All Memories")
        clear_all_btn.setCursor(Qt.PointingHandCursor)
        clear_all_btn.setStyleSheet(f"""
            QPushButton {{
                color: #EF4444;
                background: transparent;
                border: 1px solid #3B1E28;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background: #2D151F;
                border: 1px solid #EF4444;
            }}
        """)
        clear_all_btn.clicked.connect(self.clear_all_memories)
        list_header_row.addWidget(clear_all_btn)

        self.main_layout.addLayout(list_header_row)

        # Scroll area for memory list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget {
                background: transparent;
                border: none;
            }
        """)

        self.memories_container = QWidget()
        self.memories_container.setStyleSheet("background: transparent; border: none;")
        self.memories_list_layout = QVBoxLayout(self.memories_container)
        self.memories_list_layout.setContentsMargins(0, 0, 0, 0)
        self.memories_list_layout.setSpacing(8)

        self.scroll_area.setWidget(self.memories_container)
        self.main_layout.addWidget(self.scroll_area, 1)

        outer_layout.addWidget(content_wrapper)

        # Initial load
        self.refresh_data()

    # ========================================================
    # METRIC CARDS BUILDER
    # ========================================================

    def _build_metric_cards(self):
        # Clear existing
        while self.metrics_layout.count():
            item = self.metrics_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        profile = self.memory.get_profile()
        count = self.memory.get_memory_count()
        user_name = profile.get("user_name", "Yuvraj")
        stack = profile.get("preferred_languages", "C++, Python")

        cards_data = [
            (str(count), "SAVED MEMORIES", "#6366F1"),
            (user_name, "USER IDENTITY", "#38BDF8"),
            (stack, "PREFERRED STACK", "#A855F7"),
            ("Encrypted", "LOCAL SQLITE", "#10B981"),
        ]

        for idx, (val, label, col) in enumerate(cards_data):
            card = QFrame()
            card.setObjectName(f"m_card_{idx}")
            card.setStyleSheet(f"""
                QFrame#m_card_{idx} {{
                    background: #121522;
                    border: 1px solid {COLOR_BORDER_SUBTLE};
                    border-radius: 12px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
            c_lay = QVBoxLayout(card)
            c_lay.setContentsMargins(16, 12, 16, 12)
            c_lay.setSpacing(3)

            v_lbl = QLabel(val)
            v_lbl.setStyleSheet(f"color: {col}; font-size: 18px; font-weight: 800; background: transparent; border: none;")
            l_lbl = QLabel(label)
            l_lbl.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 9px; font-weight: 700; letter-spacing: 0.8px; background: transparent; border: none;")

            c_lay.addWidget(v_lbl)
            c_lay.addWidget(l_lbl)
            self.metrics_layout.addWidget(card)

    # ========================================================
    # REFRESH DATA & MEMORY LIST
    # ========================================================

    def refresh_data(self):
        self._build_metric_cards()

        # Clear existing list items
        while self.memories_list_layout.count():
            item = self.memories_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        memories = self.memory.get_memories(limit=100)

        if not memories:
            # Empty state
            empty_card = QFrame()
            empty_card.setObjectName("empty_memory_card")
            empty_card.setStyleSheet(f"""
                QFrame#empty_memory_card {{
                    background: #111420;
                    border: 1px dashed {COLOR_BORDER_MEDIUM};
                    border-radius: 12px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
            e_lay = QVBoxLayout(empty_card)
            e_lay.setContentsMargins(24, 30, 24, 30)
            e_lay.setSpacing(8)
            e_lay.setAlignment(Qt.AlignCenter)

            e_icon = QLabel("🧠")
            e_icon.setAlignment(Qt.AlignCenter)
            e_icon.setStyleSheet("font-size: 28px;")
            e_lay.addWidget(e_icon)

            e_title = QLabel("No Learned Memories Yet")
            e_title.setAlignment(Qt.AlignCenter)
            e_title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 15px; font-weight: 700;")
            e_lay.addWidget(e_title)

            e_desc = QLabel("Chat with Nova or use the box above to teach Nova your personal coding stack, rules, or habits.")
            e_desc.setAlignment(Qt.AlignCenter)
            e_desc.setWordWrap(True)
            e_desc.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 13px;")
            e_lay.addWidget(e_desc)

            self.memories_list_layout.addWidget(empty_card)
            self.memories_list_layout.addStretch()
            return

        # Category color map
        cat_colors = {
            "preference": ("#38BDF8", "#0C2336"),
            "project": ("#A855F7", "#251238"),
            "identity": ("#10B981", "#0D2E24"),
            "instruction": ("#F59E0B", "#33220A"),
            "user_instruction": ("#6366F1", "#171A36"),
            "general": ("#818CF8", "#171A2E"),
        }

        for mem in memories:
            m_id = mem["id"]
            cat = mem.get("category", "general").lower()
            content = mem.get("content", "")
            created = mem.get("created_at", "")

            badge_fg, badge_bg = cat_colors.get(cat, ("#818CF8", "#171A2E"))

            card = QFrame()
            card.setObjectName(f"mem_item_{m_id}")
            card.setStyleSheet(f"""
                QFrame#mem_item_{m_id} {{
                    background: #111420;
                    border: 1px solid {COLOR_BORDER_SUBTLE};
                    border-radius: 10px;
                }}
                QFrame#mem_item_{m_id}:hover {{
                    border: 1px solid {COLOR_BORDER_MEDIUM};
                    background: #141826;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)

            card_lay = QHBoxLayout(card)
            card_lay.setContentsMargins(14, 10, 14, 10)
            card_lay.setSpacing(12)

            # Left Category Badge
            cat_label = QLabel(cat.upper())
            cat_label.setStyleSheet(f"""
                QLabel {{
                    color: {badge_fg};
                    background: {badge_bg};
                    border: 1px solid {badge_fg}44;
                    border-radius: 6px;
                    font-size: 10px;
                    font-weight: 700;
                    padding: 3px 8px;
                }}
            """)
            card_lay.addWidget(cat_label)

            # Memory Content
            text_lay = QVBoxLayout()
            text_lay.setSpacing(2)

            content_lbl = QLabel(content)
            content_lbl.setWordWrap(True)
            content_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_lbl.setStyleSheet(f"""
                QLabel {{
                    color: {COLOR_TEXT_PRIMARY};
                    font-size: 13px;
                    line-height: 140%;
                }}
            """)
            text_lay.addWidget(content_lbl)

            if created:
                date_lbl = QLabel(f"Learned: {created[:16]}")
                date_lbl.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 10px;")
                text_lay.addWidget(date_lbl)

            card_lay.addLayout(text_lay, 1)

            # Delete button
            del_btn = QPushButton("✕")
            del_btn.setToolTip("Delete this memory")
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setFixedSize(26, 26)
            del_btn.setStyleSheet(f"""
                QPushButton {{
                    color: {COLOR_TEXT_MUTED};
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    color: #EF4444;
                    background: #2D151F;
                    border: 1px solid #7F1D1D;
                }}
            """)
            del_btn.clicked.connect(lambda chk=False, target_id=m_id: self.delete_single_memory(target_id))
            card_lay.addWidget(del_btn)

            self.memories_list_layout.addWidget(card)

        self.memories_list_layout.addStretch()

    # ========================================================
    # ACTIONS
    # ========================================================

    def add_custom_memory(self):
        text = self.teach_input.text().strip()
        if not text:
            return

        self.memory.add_memory(text, category="user_instruction", importance=2)
        self.teach_input.clear()
        self.refresh_data()

    def delete_single_memory(self, memory_id):
        self.memory.delete_memory(memory_id)
        self.refresh_data()

    def clear_all_memories(self):
        reply = QMessageBox.question(
            self,
            "Clear All Memories?",
            "Are you sure you want to erase all learned memories from Nova's database?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            memories = self.memory.get_memories(limit=500)
            for m in memories:
                self.memory.delete_memory(m["id"])
            self.refresh_data()
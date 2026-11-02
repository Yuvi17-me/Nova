"""
Nova Design System & Theme Tokens
Theme: Cosmic Electric Indigo & Cyber Slate
"""

# Color Palette — Cosmic Deep Dark
COLOR_BG_CANVAS = "#090A0F"       # Deepest cosmic space obsidian
COLOR_BG_SIDEBAR = "#0E1017"      # Sleek sidebar surface
COLOR_BG_CARD = "#131622"         # Elevated card surface
COLOR_BG_CARD_HOVER = "#1A1E2E"   # Card hover state
COLOR_BG_INPUT = "#131622"        # Floating input background

# Borders
COLOR_BORDER_SUBTLE = "#1C2132"   # Inactive/subtle borders
COLOR_BORDER_MEDIUM = "#262E44"   # Card & divider borders
COLOR_BORDER_ACTIVE = "#3D486B"   # Active / hover borders
COLOR_BORDER_ACCENT = "#6366F1"   # Accent / focus borders (Electric Indigo)

# Accents — Electric Indigo, Violet & Cyber Blue (No Green)
COLOR_ACCENT_PRIMARY = "#6366F1"  # Electric Indigo
COLOR_ACCENT_HOVER = "#818CF8"    # Soft radiant indigo
COLOR_ACCENT_MUTED = "#1E2238"    # Subtle indigo background
COLOR_ACCENT_CYAN = "#38BDF8"     # Cyber Cyan
COLOR_ACCENT_AMBER = "#F59E0B"    # Amber warning / memory
COLOR_ACCENT_PURPLE = "#A855F7"   # Royal purple

# Text Hierarchy
COLOR_TEXT_PRIMARY = "#F8FAFC"    # Headings & primary white
COLOR_TEXT_SECONDARY = "#94A3B8"  # Body & descriptions (slate)
COLOR_TEXT_MUTED = "#64748B"      # Subtitles & captions
COLOR_TEXT_FAINT = "#475569"      # Very faint hints

# User Bubble
COLOR_USER_BUBBLE_BG = "#1A1E30"  # Deep indigo slate
COLOR_USER_BUBBLE_BORDER = "#2B3352"

# AI Bubble
COLOR_AI_BUBBLE_BG = "#12141F"    # Dark obsidian surface
COLOR_AI_BUBBLE_BORDER = "#1E2436"

# Code Block
COLOR_CODE_BG = "#0A0C14"
COLOR_CODE_BORDER = "#1E253B"


GLOBAL_STYLESHEET = f"""
QWidget {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: {COLOR_TEXT_PRIMARY};
}}

/* Ensure QLabels never inherit QFrame borders */
QLabel {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    width: 6px;
    background: transparent;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #232A3E;
    border-radius: 3px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: #3B4766;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}

QToolTip {{
    background-color: #171A28;
    color: #F8FAFC;
    border: 1px solid #2B334E;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}
"""

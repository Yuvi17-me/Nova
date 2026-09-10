import sys
from PySide6.QtWidgets import QApplication

from frontend.main_window import NovaWindow


app = QApplication(sys.argv)

window = NovaWindow()
window.show()

sys.exit(app.exec())
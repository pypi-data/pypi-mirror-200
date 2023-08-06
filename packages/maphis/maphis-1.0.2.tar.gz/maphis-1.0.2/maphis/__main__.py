import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from maphis.app import MAPHIS


app = QApplication([])
window = MAPHIS()
app.focusChanged.connect(window.handle_focus_changed)
QTimer.singleShot(100, window.showMaximized)
sys.exit(app.exec())

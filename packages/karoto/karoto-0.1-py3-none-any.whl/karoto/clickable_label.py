from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal
from time import time


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    _last_press = 0

    @property
    def _press_duration(self) -> float:
        return time() - self._last_press

    def mousePressEvent(self, event):
        self._last_press = time()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._press_duration < 0.2:  # TODO: steal value from QPushButton?
            self.clicked.emit()

        super().mouseReleaseEvent(event)

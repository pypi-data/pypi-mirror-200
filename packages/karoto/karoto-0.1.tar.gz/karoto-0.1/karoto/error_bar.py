#!/usr/bin/python3

from dataclasses import dataclass
from time import time
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QTimer


@dataclass
class ErrorBarError:
    message: str
    expiration_time: float = 5
    severity: str = "WARNING"

    @property
    def is_dead(self):
        return time() > self.expiration_time


class ErrorBar(QWidget):
    def __init__(self):
        super().__init__()
        self.errors = list()
        self.init_ui()
        self.init_timer()
        self.setHidden(True)

    def init_ui(self):
        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)

    def init_timer(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_errors)
        self.timer.start(1000)

    def clear_layout(self) -> None:
        while not self.layout_.isEmpty():
            del_item = self.layout_.itemAt(0)
            self.layout_.removeItem(del_item)
            del_item.widget().deleteLater()

    def reload(self) -> None:
        if not self.errors and not self.isHidden():
            self.setHidden(True)

        self.clear_layout()
        for error in self.errors:
            lbl = QLabel(error.message)
            lbl.setWordWrap(True)
            lbl.setProperty("class", error.severity)
            self.layout_.addWidget(lbl)

    def show_error(self,
                   message: str,
                   ttl: float = 5,
                   ) -> None:
        self.show_generic_error(
            message=message,
            ttl=ttl,
            severity="ERROR",
        )

    def show_warning(self,
                     message: str,
                     ttl: float = 3.5,
                     ) -> None:
        self.show_generic_error(
            message=message,
            ttl=ttl,
            severity="WARNING",
        )

    def show_generic_error(self,
                           message: str,
                           severity: str,
                           ttl: float = 5,
                           ) -> None:

        self.errors.append(
            ErrorBarError(
                message=message,
                expiration_time=time() + ttl,
                severity=severity,
            )
        )
        self.setHidden(False)
        self.reload()

    def check_errors(self):
        if not self.errors:
            return
        for error in self.errors:
            if error.is_dead:
                self.errors.remove(error)
                self.reload()

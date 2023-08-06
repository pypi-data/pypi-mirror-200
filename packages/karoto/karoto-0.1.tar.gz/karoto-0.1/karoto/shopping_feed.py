import sys
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScroller,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal, Qt
from karoto.backend import CartItem
from karoto.clickable_label import ClickableLabel
from karoto.base_feed import BaseFeed


class ShoppingFeedItemDetails(QWidget):
    item_changed = pyqtSignal()
    warn_message = pyqtSignal(str)

    def __init__(self, item: CartItem) -> None:
        super().__init__()
        self.item = item

        self.init_ui()

    def init_ui(self) -> None:
        self.minus_button = QPushButton("-")
        self.minus_button.clicked.connect(self.decrease)
        self.minus_button.setProperty("class", "single_char_button")

        self.missing_edit = QLineEdit("ERROR")
        self.missing_edit.editingFinished.connect(self.update_missing)
        self.missing_edit.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            self.missing_edit.sizePolicy().verticalPolicy(),
        )
        self.missing_edit.setProperty("class", "short_line_edit")

        self.wanted_label = QLabel(f"/ {self.item.wanted}")

        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self.increase)
        self.plus_button.setProperty("class", "single_char_button")

        self.layout_ = QHBoxLayout()
        self.layout_.addStretch()
        self.layout_.addWidget(self.minus_button)
        self.layout_.addWidget(self.missing_edit)
        self.layout_.addWidget(self.wanted_label)
        self.layout_.addWidget(self.plus_button)
        self.setLayout(self.layout_)

    def reload(self) -> None:
        self.missing_edit.setText(str(self.item.missing))
        self.plus_button.setEnabled(self.item.in_stock > 0)

    def update_missing(self) -> None:
        try:
            new = float(self.missing_edit.text())

            if self.item.missing == new:
                return

            if new > self.item.wanted:
                self.warn_message.emit(
                    "You can't go higher than the wanted amount ("
                    f"{self.item.wanted} {self.item.unit})",
                )
                # TODO: Maybe introduce something like only once wanted that
                #       allows this? Is it worth it?

            if new < 0:
                self.warn_message.emit("Negative numbers not supported!")
                self.missing_edit.setText(str(self.item.missing))
                return

            self.item.missing = new

        except ValueError as e:
            self.warn_message.emit(str(e))
            self.missing_edit.setText(str(self.item.missing))
            return

        self.item_changed.emit()

    def increase(self) -> None:
        self.item.missing += 1
        self.item_changed.emit()

    def decrease(self) -> None:
        self.item.missing -= 1
        self.item_changed.emit()


class ShoppingFeedItem(QGroupBox):
    item_changed = pyqtSignal()
    bought_all = pyqtSignal()
    warn_message = pyqtSignal(str)

    def __init__(self, item: CartItem) -> None:
        super().__init__()
        self.item = item

        self.init_ui()

    def init_ui(self) -> None:
        self.name_label = ClickableLabel("ERROR")
        self.name_label.setWordWrap(True)
        self.name_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            self.name_label.sizePolicy().verticalPolicy(),
        )
        self.name_label.clicked.connect(self.toggle_details)

        self.more_button = QPushButton("\u2B0E")
        self.more_button.setProperty("class", "single_char_button")
        self.more_button.clicked.connect(self.toggle_details)
        self.more_button.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            self.more_button.sizePolicy().verticalPolicy(),
        )

        self.bought_button = QPushButton("bought")
        self.bought_button.clicked.connect(self.buy_all)
        self.bought_button.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            self.bought_button.sizePolicy().verticalPolicy(),
        )

        self.details = None  # see self._init_details()

        self.layout_ = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.name_label)
        self.top_layout.addWidget(self.more_button)
        self.top_layout.addWidget(self.bought_button)
        self.layout_.addLayout(self.top_layout)
        # do not simplify self.layout_ as details get added later
        self.setLayout(self.layout_)

        self.reload()

    def _init_details(self) -> None:
        """details get initialized when needed only to speed up the app"""
        self.details = ShoppingFeedItemDetails(self.item)
        self.details.item_changed.connect(self.item_changed)
        self.details.item_changed.connect(self.check_bought_all)
        self.details.item_changed.connect(self.reload)
        self.details.warn_message.connect(self.warn_message)
        self.details.setHidden(True)
        self.layout_.addWidget(self.details)

    def check_bought_all(self) -> None:
        if not self.item.needs_restock:
            self.bought_all.emit()

    def reload(self) -> None:
        self.name_label.setText(
            f"{self.item.name}: {self.item.missing} {self.item.unit}"
        )

        if self.details is None:
            return

        if self.details.isHidden():
            self.more_button.setText("\u2B0E")
        else:
            self.more_button.setText("\u2B11")

        self.details.reload()

    def buy_all(self) -> None:
        self.item.bought_all()
        self.bought_all.emit()
        self.item_changed.emit()

    def toggle_details(self) -> None:
        if self.details is None:
            self._init_details()

        self.details.setHidden(not self.details.isHidden())
        self.reload()


class ShoppingFeed(BaseFeed):
    item_changed = pyqtSignal(CartItem)
    warn_message = pyqtSignal(str)

    def init_ui(self) -> None:
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.item_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.item_layout)
        self.scroll_layout.addStretch(1)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.setWidget(self.scroll_widget)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        QScroller.grabGesture(
            self.viewport(), QScroller.ScrollerGestureType.TouchGesture
        )

    def _create_ui_item(self, item: CartItem) -> ShoppingFeedItem:
        si = ShoppingFeedItem(item)
        si.item_changed.connect(lambda x=item: self.item_changed.emit(x))
        si.bought_all.connect(lambda x=item: self.remove_item(x))
        si.warn_message.connect(self.warn_message)
        return si


def main() -> None:
    app = QApplication(sys.argv)
    cart_items = [
        CartItem(
            name="Kräutersalz",
            wanted=1,
            in_stock=0,
            unit="Stk",
            only_once=False,
        ),
        CartItem(
            name="Kartoffeln",
            wanted=2.5,
            in_stock=1,
            unit="kg",
            only_once=False,
        ),
    ]
    for i in range(40):
        i += 1
        cart_items.append(
            CartItem(
                name=f"Item {i}",
                wanted=2 * i,
                in_stock=i,
                unit="Stk",
                only_once=False,
            )
        )

    shopping_feed = ShoppingFeed(cart_items)
    shopping_feed.item_changed.connect(print)
    shopping_feed.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

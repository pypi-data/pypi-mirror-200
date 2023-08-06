import sys
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
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


class StorageFeedItemDetails(QWidget):
    item_saved = pyqtSignal()
    item_deleted = pyqtSignal()
    name_changed = pyqtSignal(str)

    def __init__(self, item: CartItem, is_for_wizzard=False) -> None:
        super().__init__()
        self.item = item
        self.is_for_wizzard = is_for_wizzard

        self.init_ui()

    def init_ui(self) -> None:
        self.layout_ = QGridLayout()
        self.setLayout(self.layout_)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit("ERROR")

        self.in_stock_label = QLabel("In stock:")
        self.in_stock_edit = QLineEdit("ERROR")

        self.wanted_label = QLabel("Wanted:")
        self.wanted_edit = QLineEdit("ERROR")

        self.unit_label = QLabel("Unit:")
        self.unit_edit = QLineEdit("ERROR")

        self.only_once_label = QLabel("Only Once:")
        self.only_once_check = QCheckBox()

        self.save_button = QPushButton(
            "Create Item" if self.is_for_wizzard else "Save"
        )
        self.save_button.clicked.connect(self.save_changes)

        if not self.is_for_wizzard:
            self.delete_button = QPushButton("Delete")
            self.delete_button.clicked.connect(self.item_deleted)

        self.layout_.addWidget(self.name_label, 0, 0)
        self.layout_.addWidget(self.name_edit, 0, 1)
        self.layout_.addWidget(self.in_stock_label, 1, 0)
        self.layout_.addWidget(self.in_stock_edit, 1, 1)
        self.layout_.addWidget(self.wanted_label, 2, 0)
        self.layout_.addWidget(self.wanted_edit, 2, 1)
        self.layout_.addWidget(self.unit_label, 3, 0)
        self.layout_.addWidget(self.unit_edit, 3, 1)
        self.layout_.addWidget(self.only_once_label, 4, 0)
        self.layout_.addWidget(self.only_once_check, 4, 1)
        self.layout_.addWidget(self.save_button, 5, 1)
        if not self.is_for_wizzard:
            self.layout_.addWidget(self.delete_button, 6, 1)

        self.reload()

    def reload(self) -> None:
        self.name_edit.setText(self.item.name)
        self.in_stock_edit.setText(str(self.item.in_stock))
        self.wanted_edit.setText(str(self.item.wanted))
        self.unit_edit.setText(self.item.unit)
        self.only_once_check.setChecked(self.item.only_once)

    def save_changes(self) -> None:
        new_name = self.name_edit.text()
        if self.is_for_wizzard:
            self.item.name = new_name
        elif self.item.name != new_name:
            self.name_changed.emit(new_name)

        self.item.in_stock = self.in_stock_edit.text()
        self.item.wanted = self.wanted_edit.text()
        self.item.unit = self.unit_edit.text()
        self.item.only_once = self.only_once_check.isChecked()

        self.item_saved.emit()


class StorageFeedItem(QGroupBox):
    item_changed = pyqtSignal()
    item_deleted = pyqtSignal()
    name_changed = pyqtSignal(str)
    warn_message = pyqtSignal(str)

    def __init__(self, item: CartItem) -> None:
        super().__init__()
        self.item = item

        self.init_ui()

    def init_ui(self) -> None:
        self.details = None  # see self._init_details()

        self.layout_ = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.layout_.addLayout(self.top_layout)
        # details get added to self.layout_ too so don't simplify the layout
        self.setLayout(self.layout_)

        self.name_label = ClickableLabel("ERROR")
        self.name_label.setWordWrap(True)
        self.name_label.clicked.connect(self.toggle_details)
        self.name_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            self.name_label.sizePolicy().verticalPolicy(),
        )

        self.minus_button = QPushButton("-")
        self.minus_button.clicked.connect(self.decrease)
        self.minus_button.setProperty("class", "single_char_button")

        self.in_stock_edit = QLineEdit("ERROR")
        self.in_stock_edit.editingFinished.connect(self.update_in_stock)
        self.in_stock_edit.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            self.in_stock_edit.sizePolicy().verticalPolicy(),
        )
        self.in_stock_edit.setProperty("class", "short_line_edit")

        self.wanted_label = QLabel("ERROR")

        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self.increase)
        self.plus_button.setProperty("class", "single_char_button")

        self.top_layout.addWidget(self.name_label)
        self.top_layout.addWidget(self.minus_button)
        self.top_layout.addWidget(self.in_stock_edit)
        self.top_layout.addWidget(self.wanted_label)
        self.top_layout.addWidget(self.plus_button)

        self.reload()

    def _init_details(self) -> None:
        """details get initialized only when needed to speed up the app"""

        self.details = StorageFeedItemDetails(item=self.item)
        self.details.item_saved.connect(self.item_changed)
        self.details.item_deleted.connect(self.item_deleted)
        self.details.name_changed.connect(self.name_changed)
        self.details.setHidden(True)
        self.layout_.addWidget(self.details)

    def reload(self) -> None:
        self.name_label.setText(self.item.name)
        self.wanted_label.setText(f"/ {self.item.wanted} {self.item.unit}")
        self.in_stock_edit.setText(str(self.item.in_stock))
        self.minus_button.setEnabled(self.item.in_stock != 0)

        if self.details is not None:
            self.details.reload()

    def toggle_details(self) -> None:
        if self.details is None:
            self._init_details()
        self.details.setHidden(not self.details.isHidden())

    def increase(self) -> None:
        self.item.in_stock += 1
        self.on_changes()

    def decrease(self) -> None:
        try:
            self.item.in_stock -= 1
        except ValueError:
            self.item.in_stock = 0
        self.on_changes()

    def update_in_stock(self) -> None:
        try:
            new = float(self.in_stock_edit.text())

            if new == self.item.in_stock:
                return

            self.item.in_stock = new

        except ValueError as e:
            self.warn_message.emit(str(e))
            self.in_stock_edit.setText(str(self.item.in_stock))
            return

        self.on_changes()

    def on_changes(self) -> None:
        self.reload()
        self.item_changed.emit()


class CreateItemWizzard(QGroupBox):
    new_item = pyqtSignal(CartItem)

    def __init__(self) -> None:
        super().__init__()
        self.item = CartItem()
        self.init_ui()

    def init_ui(self) -> None:
        self.plus_button = QPushButton("+ Create Item +")
        self.plus_button.clicked.connect(self.toggle_details)

        self.details = StorageFeedItemDetails(self.item, is_for_wizzard=True)
        self.details.item_saved.connect(self.save_item)
        self.details.setHidden(True)

        plus_layout = QHBoxLayout()
        plus_layout.addStretch()
        plus_layout.addWidget(self.plus_button)
        plus_layout.addStretch()
        self.layout_ = QVBoxLayout()
        self.layout_.addLayout(plus_layout)
        self.layout_.addWidget(self.details)

        self.setLayout(self.layout_)

    def toggle_details(self) -> None:
        self.details.setHidden(not self.details.isHidden())
        if self.details.isHidden():
            self.plus_button.setText("+ Create Item +")
        else:
            self.plus_button.setText("- Collapse -")

    def save_item(self) -> None:
        self.new_item.emit(self.item)
        self.item = CartItem()
        self.details.item = self.item
        self.details.reload()
        self.toggle_details()


class StorageFeed(BaseFeed):
    item_changed = pyqtSignal(CartItem)
    item_deleted = pyqtSignal(CartItem)
    new_item = pyqtSignal(CartItem)
    name_changed = pyqtSignal(CartItem, str)
    warn_message = pyqtSignal(str)

    def init_ui(self) -> None:
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.item_layout = QVBoxLayout()

        self.wizzard = CreateItemWizzard()
        self.wizzard.new_item.connect(self.new_item)

        self.scroll_layout.addWidget(self.wizzard)
        self.scroll_layout.addLayout(self.item_layout)
        self.scroll_layout.addStretch(1)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.setWidget(self.scroll_widget)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        QScroller.grabGesture(
            self.viewport(), QScroller.ScrollerGestureType.TouchGesture
        )

    def _create_ui_item(self, item: CartItem) -> StorageFeedItem:
        si = StorageFeedItem(item)
        si.item_changed.connect(lambda x=item: self.item_changed.emit(x))
        si.item_deleted.connect(lambda x=item: self.item_deleted.emit(x))
        si.name_changed.connect(lambda n, i=item: self.name_changed.emit(i, n))
        si.warn_message.connect(self.warn_message)
        return si


def main() -> None:
    app = QApplication(sys.argv)
    cart_items = [
        CartItem(
            name="Salt",
            wanted=1,
            in_stock=0,
            unit="Stk",
            only_once=False,
        ),
        CartItem(
            name="Potatoes",
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

    storage_feed = StorageFeed(cart_items)
    storage_feed.item_changed.connect(print)
    storage_feed.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

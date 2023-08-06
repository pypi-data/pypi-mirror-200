#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from karoto.backend import Backend, CartItem, DuplicateError
from karoto.storage_feed import StorageFeed
from karoto.shopping_feed import ShoppingFeed
from karoto.error_bar import ErrorBar
from karoto import style


class MainWindow(QWidget):
    searchterm = None

    def __init__(self, backend: Backend):
        super().__init__()

        self.backend = backend
        self.initUI()

    def initUI(self) -> None:
        self.setStyleSheet(style.default)

        topbar = QHBoxLayout()

        self.menu_button = QPushButton("ERROR")
        self.menu_button.clicked.connect(self.toggle_view)
        self.menu_button.setObjectName("menu_button")
        topbar.addWidget(self.menu_button)

        searchfield = QLineEdit()
        searchfield.textChanged.connect(self.on_search)
        searchfield.setPlaceholderText("\U0001F50D Search...")
        searchfield.setObjectName("search_field")
        topbar.addWidget(searchfield)

        self.error_bar = ErrorBar()
        self.error_bar.setObjectName("error_bar")

        self.shopping_feed = ShoppingFeed()
        self.storage_feed = StorageFeed()

        self.shopping_feed.item_changed.connect(self.on_item_changed)
        self.shopping_feed.warn_message.connect(self.error_bar.show_warning)
        self.storage_feed.item_changed.connect(self.on_item_changed)
        self.storage_feed.item_deleted.connect(self.delete)
        self.storage_feed.new_item.connect(self.on_new_item)
        self.storage_feed.name_changed.connect(self.on_name_changed)
        self.storage_feed.warn_message.connect(self.error_bar.show_warning)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.shopping_feed)
        self.stack.addWidget(self.storage_feed)

        vbox = QVBoxLayout()
        vbox.addLayout(topbar)
        vbox.addWidget(self.error_bar)
        vbox.addWidget(self.stack)

        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

        self.refresh()
        self.show()

    def refresh(self) -> None:
        if self.stack.currentWidget() == self.storage_feed:
            self.menu_button.setText("Go shopping")
            self.storage_feed.show_items(
                self.backend.get_items_in_stock(self.searchterm),
            )
        else:
            self.menu_button.setText("Manage storage")
            self.shopping_feed.show_items(
                self.backend.get_items_to_buy(self.searchterm),
            )

    def on_new_item(self, item: CartItem) -> None:
        try:
            self.backend.add_item(item)
        except DuplicateError:
            self.error_bar.show_warning(
                f'Item "{item.name}" already exists. Aborting...'
            )
            return

        self.backend.save_list()
        self.refresh()

    def on_search(self, searchterm: str) -> None:
        if searchterm == "":
            self.searchterm = None
        self.searchterm = searchterm
        self.refresh()

    def on_item_changed(self, item: CartItem) -> None:
        if item.is_dead:
            self.delete(item)
        else:
            self.backend.save_list()

    def on_name_changed(self, item: CartItem, new_name: str) -> None:
        if self.backend.get_item_by_name(new_name) is not None:
            self.error_bar.show_warning(
                f'Tried to rename "{item.name}" to "{new_name}"'
                " which already exists. Aborting..."
            )
            return
        item.name = new_name

    def delete(self, item: CartItem) -> None:
        self.backend.delete(item)
        self.backend.save_list()
        self.refresh()

    def toggle_view(self) -> None:
        if self.stack.currentWidget() == self.storage_feed:
            self.stack.setCurrentWidget(self.shopping_feed)
        else:
            self.stack.setCurrentWidget(self.storage_feed)
        self.refresh()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--list", "-l",
        type=str,
        help="Use an alternative list by name (without extension)",
        default="default",
    )
    parser.add_argument(
        "--list-file",
        type=str,
        help="Use an alternative list file",
        default=None,
    )
    args = parser.parse_args()
    app = QApplication(sys.argv)
    backend = Backend(list_name=args.list, list_file=args.list_file)
    gui = MainWindow(backend=backend)  # noqa: F841
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

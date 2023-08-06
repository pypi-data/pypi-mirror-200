from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
)
from karoto.backend import CartItem


class BaseFeed(QScrollArea):  # TODO: Make ABC?!
    def __init__(self):
        super().__init__()

        self.cart_items = list()
        self.ui_items = list()
        self._n_items_scrollbar_range = None

        self.init_ui()

        self.verticalScrollBar().valueChanged.connect(
            self.on_scrollbar_value_changed
        )
        self.verticalScrollBar().rangeChanged.connect(
            self.on_scrollbar_range_changed
        )

    # @abstractmethod
    def init_ui(self) -> None:
        raise NotImplementedError()

    # @abstractmethod
    def _create_ui_item(self, item: CartItem) -> QWidget:
        raise NotImplementedError()

    def on_scrollbar_value_changed(self, value: int) -> None:
        if self._range_didnt_change_yet:
            # This gets triggered too early and we'd load too many items
            return

        if value > (self.verticalScrollBar().maximum()
                    - self._n_items_scrollbar_range):
            self._range_didnt_change_yet = True
            self.load_n_items()

    def on_scrollbar_range_changed(self, min_: int, max_: int) -> None:
        self._range_didnt_change_yet = False

        if max_ == 0:
            return  # on start the range is always 0

        if self._n_items_scrollbar_range is None:  # only once executed
            self._n_items_scrollbar_range = max_

            # Now we know the scrollbar range so we can load another n items
            self.load_n_items()

    def clear_layout(self) -> None:
        while not self.item_layout.isEmpty():
            del_item = self.item_layout.itemAt(0)
            self.item_layout.removeItem(del_item)
            del_item.widget().deleteLater()

    def show_items(self, items: list[CartItem]) -> None:
        self.cart_items = items
        self.reload_items()

    def reload_items(self) -> None:
        self.clear_layout()
        self.load_n_items()

    def load_n_items(self) -> None:
        """only load a fraction of all items to lower loading times"""
        num_items_to_load = 20

        old_item_count = self.item_layout.count()
        if old_item_count >= len(self.cart_items):
            return

        for count, item in enumerate(self.cart_items):
            if count < old_item_count:
                continue  # item was already loaded
            if count >= old_item_count + num_items_to_load:
                break  # we loaded n items and are ready

            new_item = self._create_ui_item(item)
            self.item_layout.addWidget(new_item)

    def remove_item(self, item: CartItem) -> None:
        self.cart_items.remove(item)
        self.reload_items()

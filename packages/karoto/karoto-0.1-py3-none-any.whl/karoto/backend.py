#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import json
from dataclasses import dataclass, field
from time import time


@dataclass
class CartItem:
    name: str = ""
    _name: str = field(init=False, repr=False, default="")
    wanted: float
    _wanted: float = field(init=False, repr=False, default=1)
    in_stock: float
    _in_stock: float = field(init=False, repr=False, default=0)
    unit: str = ""
    only_once: bool = False
    mtime: float | None = None

    def __post_init__(self) -> None:
        if self.mtime is None:
            self._on_change()

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "wanted": self.wanted,
            "in_stock": self.in_stock,
            "unit": self.unit,
            "only_once": self.only_once,
            "mtime": self.mtime,
        }

    @classmethod
    def from_dict(cls, d) -> "CartItem":
        return cls(
            name=d["name"],
            wanted=d["wanted"],
            in_stock=d["in_stock"],
            unit=d["unit"],
            only_once=d.get("only_once", False),
            mtime=d.get("mtime", 0),
        )

    def __eq__(self, other) -> bool:
        """Attention: Ignores mtime!"""
        if self.name != other.name:
            return False
        if self.wanted != other.wanted:
            return False
        if self.in_stock != other.in_stock:
            return False
        if self.unit != other.unit:
            return False
        if self.only_once != other.only_once:
            return False
        return True

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new: str) -> None:
        if type(new) is property:
            # initial value not specified, use default
            new = CartItem._name

        if type(new) != str:
            raise ValueError()

        if self._name == new:
            return

        self._name = new
        self._on_change()

    @property
    def in_stock(self) -> float | int:
        return self._int_if_possible(self._in_stock)

    @in_stock.setter
    def in_stock(self, new: any) -> None:
        if type(new) is property:
            # initial value not specified, use default
            new = CartItem._in_stock

        new = self._to_float(new)

        if new < 0:
            raise ValueError("Negative numbers are not supported!")

        if new == self.in_stock:
            return

        self._in_stock = new
        self._on_change()

    @property
    def wanted(self) -> float | int:
        return self._int_if_possible(self._wanted)

    @wanted.setter
    def wanted(self, new):
        if type(new) is property:
            # initial value not specified, use default
            new = CartItem._wanted

        new = self._to_float(new)

        if self._wanted == new:
            return

        if new <= 0:
            raise ValueError("You can not want nothing or less than nothing")

        self._wanted = new
        self._on_change()

    @property
    def missing(self) -> float | int:
        if self.wanted < self.in_stock:
            return 0
        return self._int_if_possible(self.wanted - self.in_stock)

    @missing.setter
    def missing(self, new) -> None:
        new = self._to_float(new)

        if self.wanted < new:
            self.in_stock = 0
            return

        self.in_stock = self.wanted - new

    @property
    def needs_restock(self) -> bool:
        return self.wanted > self.in_stock

    @property
    def is_dead(self) -> bool:
        return self.only_once and not self.needs_restock

    def _on_change(self) -> None:
        self.mtime = time()

    def bought_all(self) -> None:
        self.in_stock = self.wanted

    def _int_if_possible(self, value: float) -> float | int:
        """str(1.0) looks worse than str(1) so we convert if possible"""

        # float is not always exact and we don't need more than 6 digits
        value = round(value, 6)

        if int(value) == value:
            return int(value)
        return value

    def _to_float(self, value: any) -> float:
        if type(value) is str:
            if value == "":
                float(value)  # raises exception
            if value[-1] == ".":
                raise ValueError("String ends with a dot")
        return float(value)


class DuplicateError(Exception):
    pass


class FileManager:
    app_name: str = "karoto"
    list_extension: str = ".json"

    def _get_list_path(self, name: str, full_path: str = None) -> Path:
        if full_path is not None:
            return Path(full_path)
        elif name is not None:
            xdg_data_home = os.environ.get('XDG_DATA_HOME') or \
                Path.home() / '.local' / 'share'
            return Path(xdg_data_home) / self.app_name / (name +
                                                          self.list_extension)
        else:
            return self.list_path

    def load_list(self, name: str = "default", full_path: str = None) -> list:
        self.list_path = self._get_list_path(name=name, full_path=full_path)

        storage_dict = json.load(open(self.list_path))

        ret = list()
        for d_item in storage_dict["items"]:
            item = CartItem.from_dict(d_item)
            ret.append(item)
        return ret

    def _storage_to_dict(self, storage: list) -> dict:
        d = dict(items=list())
        for item in storage:
            d["items"].append(item.__dict__())
        return d

    def save_list(self,
                  storage: list,
                  name: str = None,
                  full_path: str = None,
                  ) -> None:
        list_path = self._get_list_path(name=name, full_path=full_path)

        storage = self._storage_to_dict(storage)

        list_path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(storage, open(list_path, "w"), indent=4)


class Backend:
    def __init__(self,
                 list_name: str = "defaut",
                 list_file: str = None,
                 ) -> None:
        super().__init__()
        self.fm = FileManager()

        self.load_list(list_name=list_name, full_path=list_file)

    def load_list(self, list_name: str = None, full_path: str = None) -> None:
        try:
            self.storage = self.fm.load_list(
                name=list_name,
                full_path=full_path,
            )
        except FileNotFoundError:
            self.storage = list()

    def save_list(self, list_name: str = None, full_path: str = None) -> None:
        self.fm.save_list(
            self.storage,
            name=list_name,
            full_path=full_path,
        )

    def _get_filtered_items(self, search: str = None) -> list:
        if not search:
            ret = self.storage
            ret.sort(key=lambda k: k.mtime, reverse=True)
            return ret

        new_list = list()
        for item in self.storage:
            if item.name.lower().find(search.lower()) != -1:
                new_list.append(item)
        new_list.sort(key=lambda k: k.mtime, reverse=True)
        return new_list

    def get_items_in_stock(self, search: str = None) -> list:
        return self._get_filtered_items(search=search)

    def get_items_to_buy(self, search: str = None) -> list:
        items = list()
        for item in self._get_filtered_items(search=search):
            if item.needs_restock:
                items.append(item)
        return items

    def add_item(self, item: CartItem):
        if self.get_item_by_name(item.name) is not None:
            raise DuplicateError("A item with this name already exists")
        self.storage.append(item)

    def delete(self, item: CartItem) -> None:
        self.storage.remove(item)

    def get_item_by_name(self, name: str) -> CartItem:
        for item in self.storage:
            if name == item.name:
                return item

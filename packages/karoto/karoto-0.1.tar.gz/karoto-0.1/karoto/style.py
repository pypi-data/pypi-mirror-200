_item_height = 18
_sixty = "white"
_thirty = "#fdc033"
_ten = "#80e241"

default = f"""
* {{
    background-color: {_sixty};
    font-size: 14px;
    color: black;
}}

QPushButton {{
    height: {_item_height}px;
    background-color: {_ten};
    border: 1px solid grey;
    border-radius: {_item_height/2}px;
    padding-top: 3px;
    padding-bottom: 3px;
    padding-left: 10px;
    padding-right: 10px;
}}

QLineEdit {{
    border-radius: 10px;
    padding: 2px;
    background-color: {_sixty};
}}

QLabel, QCheckBox {{
    background-color: {_thirty};
}}

#menu_button, #search_field {{
    min-height: 40px;
}}

#error_bar QLabel {{
    min-height: 40px;
    font-weight: bold;
    padding-top: 3px;
    padding-bottom: 3px;
    padding-left: 10px;
    padding-right: 10px;
}}

.WARNING {{
    background-color: yellow;
}}

.ERROR {{
    background-color: red;
}}

#menu_button {{
    min-width: 150px;
}}

#search_field {{
    padding-left: 6px;
    border: 1px solid grey;
}}

QGroupBox {{
    background-color: {_thirty};
    border-radius: 6px;
}}

.short_line_edit {{
    width: 40px;
}}

.single_char_button {{
    padding: 2px;
    border: 1px solid grey;
    border-radius: {_item_height/2}px;
    width: {_item_height}px;
    height: {_item_height}px;
    font-weight: bold;
}}

QPushButton:disabled {{
    border: 1px solid #77AA77;
    background-color: #88BB88;
    color: #777777;
}}
"""

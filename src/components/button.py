from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
def build_button(text: str, font_size: int = 12, font_weight: int = 500, font_color: str = "black", background_color: str = "white", on_click: callable = None):
    button =  QPushButton(text)
    button.setFont(QFont("Arial", font_size, font_weight))
    button.setStyleSheet(f"color: {font_color}; background-color: {background_color};")
    button.clicked.connect(on_click if on_click else lambda: None)
    return button





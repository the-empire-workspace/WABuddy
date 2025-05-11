from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont

def build_text_input(text: str, font_size: int = 12, font_weight: int = 500, font_color: str = "black", background_color: str = "white", on_text_changed: callable = None):
    text_input = QTextEdit(text)
    text_input.setFont(QFont("Arial", font_size, font_weight))
    text_input.setStyleSheet(f"color: {font_color}; background-color: {background_color};")
    return text_input
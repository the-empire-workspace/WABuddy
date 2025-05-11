from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
def build_label(text: str, font_size: int = 12, font_weight: int = 500, font_color: str = "black", background_color: str = "transparent"):
    label = QLabel(text)
    label.setFont(QFont("Arial", font_size, font_weight))
    label.setStyleSheet(f"color: {font_color}; background-color: {background_color};")
    return label



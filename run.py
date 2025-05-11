import sys
from PyQt5.QtWidgets import QApplication
from src.index import ExcelApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelApp()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication
from src.index import DashboardApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec_())

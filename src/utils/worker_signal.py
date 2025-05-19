from PyQt5.QtCore import QObject, pyqtSignal
from pandas import Series
class WorkerSignals(QObject):
    result = pyqtSignal(Series, str, bool)

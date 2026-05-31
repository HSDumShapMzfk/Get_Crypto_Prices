from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QMainWindow, 
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget, 
    QScrollArea,
    QStatusBar,
    QMenuBar,
    )
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QColor


class APIKeyEnteringScreen(QWidget):
    entering = pyqtSignal()
    reject = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: #101010")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Авторизация"))

        enter_btn = QPushButton("Авторизоваться")
        enter_btn.clicked.connect(self._enter)

        reject_btn = QPushButton("Отклонить")
        reject_btn.clicked.connect(self._reject)

        layout.addWidget(enter_btn)
        layout.addWidget(reject_btn)

    def _enter(self, event):
        self.entering.emit()

    def _reject(self, event):
        self.reject.emit()


class ContentScreen(QWidget):
    to_entering = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pass
































# class ContentScreen(QWidget):
#     def __init__(self, window: QMainWindow):
#         super()__init__()
#         self.grid_view = GridView()
#         self.status_bar = QStatusBar()
#         self.menu_bar = QMenuBar()
#         window.setCentralWidget(self.grid_view)
#         window.setStatusBar(self.status_bar)
#         window.setMenuBar(self.menu_bar)

# class GridController(QObject):
#     """ Handling columns in GridView widget """
#     columns_changed = pyqtSignal(int)

#     def __init__(self):
#         super().__init__()
#         self._columns = 0

#     def set_columns(self, columns: int):
#         if columns != self._columns:
#             self.columns = columns
#             self.columns_changed.emit(columns)

# class GridView(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.columns = 3
#         self.container = QWidget()
#         self.container.setStyleSheet("background-color: #101010")
#         self.grid = QGridLayout(self.container)
#         self.grid.setSpacing(12)
#         self.scroll = QScrollArea()
#         self.scroll.setWidgetResizable(True)
#         self.scroll.setWidget(self.container)
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.scroll)

#     def set_data(self, dataset: list[dict], columns=3):
#         self.columns = columns
#         while self.grid.count():
#             item = self.grid.takeAt(0)
#             widget = item.widget()
#             if widget:
#                 widget.deleteLater()
#         if not dataset:
#             return
#         for index, item in enumerate(dataset):
#             row = index // self.columns
#             column = index % self.columns
#             card = ItemCard(item)
#             self.grid.addWidget(card, row, column)

# class ItemCard(QFrame):
#     def __init__(self, item: dict, parent=None):
#         super().__init__(parent)

#         # r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
#         # bg_color = QColor(r, g, b)
#         # yiq = (r*299 + g*587 + b*114) / 1000 
#         # if yiq >= 128: 
#         #     text_color = QColor("black") 
#         # else: 
#         #     text_color = QColor("white")
#         # self.setStyleSheet(f"background-color: {bg_color.name()}; color: {text_color.name()}")
        
#         self.title = QLabel(item["symbol"])
#         self.market_rank = QLabel(item["market_rank"])
#         self.price = QLabel(item["price"])
#         self.high_24h = QLabel(item["high_24h"])
#         self.low_24h = QLabel(item["low_24h"])
#         self.price_change_24h = QLabel(item["price_change_percentage_24h"])
#         gradient_color = QColor(0, 150, 0) if float(item["price_change_percentage_24h"]) > 0 else QColor(150, 0, 0)
#         self.setStyleSheet(f"background-color: {gradient_color.name()}; color: white")

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.title)
#         layout.addWidget(self.market_rank)
#         layout.addWidget(self.price)
#         layout.addWidget(self.high_24h)
#         layout.addWidget(self.low_24h)
#         layout.addWidget(self.price_change_24h)


from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout, 
    QLabel, 
    QMainWindow, 
    QPushButton,
    QVBoxLayout,
    QWidget, 
    )
from PyQt6.QtCore import Qt

class MainWindowUI:
    def setup_ui(self, window: QMainWindow):
        main_widget = QWidget()
        main_layout = QGridLayout()

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white")
        
        self.change_currency_btn = QPushButton("Button", content_widget)
        self.change_currency_btn.setStyleSheet("background-color: black")

        self.label_currency = QLabel(content_widget)
        self.label_currency.setStyleSheet("background-color: black")
        self.label_currency.adjustSize()
        self.label_currency.move(10,80)

        self.label_data = QLabel(content_widget)
        self.label_data.setStyleSheet("background-color: black")
        self.label_data.adjustSize()
        self.label_data.move(10,100)

        bottom_widget = QWidget()
        bottom_widget.setStyleSheet("background-color: grey")
        buttom_layout = QGridLayout()
        bottom_widget.setLayout(buttom_layout)

        main_layout.addWidget(content_widget)
        main_layout.addWidget(bottom_widget)
        main_widget.setLayout(main_layout)
        window.setCentralWidget(main_widget)

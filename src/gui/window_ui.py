from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class MainWindowUI:
    def setup_ui(self, window: QMainWindow):
        central_widget = QWidget()
        main_layout = QGridLayout()

        # Четыре контейнера
        widget_one = QWidget()
        widget_two = QWidget()
        widget_three = QWidget()
        widget_four = QWidget()

        # Для каждого контейнера создаём layout и лейбл
        for widget, color, text_color in [
            (widget_one, "cyan", 'black'),
            (widget_two, "magenta", 'black'),
            (widget_three, "yellow", 'black'),
            (widget_four, "black", 'white'),
        ]:
            layout = QVBoxLayout(widget)
            label = QLabel("in development", widget)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(f"color: {text_color};") 
            layout.addWidget(label)
            widget.setStyleSheet(f"background-color: {color};")

        # Добавляем контейнеры в сетку
        main_layout.addWidget(widget_one, 0, 0)
        main_layout.addWidget(widget_two, 0, 1)
        main_layout.addWidget(widget_three, 1, 0)
        main_layout.addWidget(widget_four, 1, 1)

        central_widget.setLayout(main_layout)
        window.setCentralWidget(central_widget)
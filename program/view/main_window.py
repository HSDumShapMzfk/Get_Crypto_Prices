import sys

from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit


class MainWindow(QMainWindow):

	"""
	Класс создания окна
    ToDo:
        * Ограничить минимальный размер окна до [~300px X ~600px]
        * Разработать адптивный дизайн: При растягивании окна по Y > ~900px, справа появится журнал истории операций
        * Разработать дизайн окна, стилизованное под windows 11
    """

	def __init__(self):

		super().__init__()
		self.setWindowsTitle("Ёк макарёк!")

	def setup_ui(self, main_window):
		main_window.
		
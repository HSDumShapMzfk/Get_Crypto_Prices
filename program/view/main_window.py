from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from .window_ui import MainWindowUI

class MainWindow(QMainWindow):
	"""Класс создания окна
    ToDo:
        * Разработать адптивный дизайн, стилизованный под windows 11 (возможно с полупрозрачным фоном)"""

	def __init__(self):
		super().__init__()
		ui = MainWindowUI()
		ui.setup_ui(self)

		# Изменение в заголовке окна
		self.setWindowTitle('Get crypto prices')
		self.setWindowIcon(QIcon("media/currency_bitcoin_64dp_F3F3F3_2.png"))

		# Изменение размера и положения окна
		self.resize(900, 600)
		self.setMinimumSize(600, 400)

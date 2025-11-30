from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
import logging

from src.view.ui import MainWindowUI
from src.model.cache import state_instance

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
	"""Класс создания окна
    ToDo:
        * Разработать адптивный дизайн, стилизованный под windows 11 (возможно с полупрозрачным фоном)"""

	def __init__(self):
		super().__init__()
		self.ui = MainWindowUI()
		self.ui.setup_ui(self)

		# Изменение в заголовке окна
		self.setWindowTitle('Get crypto prices')
		self.setWindowIcon(QIcon("media/gui_icons/currency_bitcoin_64dp_F3F3F3.png"))

		# Изменение размера и положения окна
		self.resize(900, 600)
		self.setMinimumSize(600, 400)

	def closeEvent(self, event):
		state_instance.write_state()
		logger.info(f"lsc: {state_instance.last_selected_currency} is saved!")
		event.accept()
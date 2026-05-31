from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
import logging
from pathlib import Path

from src.infrastructure.loader import loader_instance as load
from src.ui.screens import APIKeyEnteringScreen, ContentScreen
from src.ui.screen_manager import ScreenManager

# logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
	""" Handles events and displays screens """
	WD_PATH = Path(__file__).parent.parent.parent
	ICON_PATH = WD_PATH / "media/static/Bitcoin_icon_2.png"

	def __init__(self):
		super().__init__()

		self.setWindowTitle('Crypto prices')
		self.setWindowIcon(QIcon(str(self.ICON_PATH)))
		self.resize(900, 600)
		self.setMinimumSize(600, 400)

	def closeEvent(self, event):
		load.write_state()
		# logger.info(f"lsc: {load.state.get("last_selected_currency")} is saved!")
		event.accept()

	def resizeEvent(self, event):
		# width = self.width()
		# columns = width // 200
		# logger.info(f"Window size is: {self.width()}x{self.height()} now. columns = {columns}")
		super().resizeEvent(event)
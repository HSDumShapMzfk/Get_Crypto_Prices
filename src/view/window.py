from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
import logging

from src.view.ui import MainWindowUI
from src.loader import loader_instance as load

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
	"""  """

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
		load.write_state()
		logger.info(f"lsc: {load.state.get("last_selected_currency")} is saved!")
		event.accept()
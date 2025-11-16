from src.model.data_handler import DataHandler
from src.gui.main_window import MainWindow
from src.config import (
	LAST_SELECTED_CURRENCY,
	)

class MainController:
	""" Класс создания саязи между интерфейсом и логикой """

	def __init__(self, model: DataHandler, gui: MainWindow):
		self.model = model
		self.gui = gui

		self.valid_dataset = model.generate_valid_dataset(LAST_SELECTED_CURRENCY)

	def func(self):
		pass
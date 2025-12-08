from random import choice

from src.model.base_model import BaseModel
from src.view.window import MainWindow


class MainController:
	""" Класс создания саязи между интерфейсом и логикой """

	def __init__(self, 
			base_model: BaseModel, 
			view: MainWindow
		):

		self.base_model = base_model
		self.view = view

		self.view.ui.change_currency_btn.clicked.connect(self.choice_random_currency)

		self.set_last_selected_currency()

	def set_last_selected_currency(self):
		self.view.ui.label_currency.setText(str(self.base_model.current_currency))
		self.view.ui.label_currency.adjustSize()

		self.view.ui.label_data.setText(str(self.base_model.dataset[0]))
		self.view.ui.label_data.adjustSize()

	def update_model(self):
		self.base_model.update_data()

	def choice_random_currency(self):
		self.base_model.change_currency(f"{choice(list(self.base_model.exchangerate_data.keys()))}")

		self.view.ui.label_currency.setText(str(self.base_model.current_currency))
		self.view.ui.label_currency.adjustSize()

		self.view.ui.label_data.setText(str(self.base_model.dataset[0]))
		self.view.ui.label_data.adjustSize()

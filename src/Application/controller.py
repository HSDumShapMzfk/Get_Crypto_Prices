from src.infrastructure.loader import loader_instance as load
from src.domain.model import Model
from src.ui.screen_manager import ScreenManager
from src.application.services import APIKeyService


class Controller:
	""" Класс создания саязи между интерфейсом и логикой """

	def __init__(self, 
			model: Model, 
			manager: ScreenManager,
			api_key_service: APIKeyService
		):
		self.model = model
		self.manager = manager
		self.api_key_service = api_key_service
		
	def initialize(self):
		""" Checking the presence and correctness of the exchange rate API key 
		when launching the application """

		if self.api_key_service.has_key():
			manager.show()

		if self.api_key_service.is_valid_key()

		self.manager.stack.setCurrentWidget(self.manager.content)
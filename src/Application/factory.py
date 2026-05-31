from src.infrastructure.loader import loader_instance as load
from src.infrastructure.cache import JSONCacheHandler
from src.infrastructure.api import CoingeckoHandler, ExchangerateHandler
from src.domain.model import Model
from src.ui.window import MainWindow
from src.application.controller import Controller


class ApplicationFactory:
	""" Building the application """
	def build(self):
		# Cache
		coingecko_cache = JSONCacheHandler(
			load.config["cache"].get("coingecko_cache_file_name"),
			load.config["cache"].get("coingecko_time_to_live"))
		exchangerate_cache = JSONCacheHandler(
			load.config["cache"].get("exchangerate_cache_file_name"),
			load.config["cache"].get("exchangerate_time_to_live"))

		# API
		coingecko_handler = APIHandler(
			load.config['api'].get("coingecko_url")
			load.config['api'].get("coingecko_params")
		)
		exchangerate_handler = APIHandler(
			load.config['api'].get("exchangerate_url"))

		# Repository
		coingecko_repo = Repository(coingecko_handler, coingecko_cache)
		exchangerate_repo = Repository(exchangerate_handler)
 
		# Model
		model = Model(coingecko_repo, exchangerate_repo)

		# UI
		window = MainWindow()
		screen_manager = ScreenManager(window)

		# Service
		api_key_service = APIKeyService()



		# Controllers
		startup_controller = StartupController()
		controller = Controller(model, screen_manager, api_key_service)

		return window
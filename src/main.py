import asyncio
import sys
import logging
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from src.model.cache import JSONCacheHandler
from src.model.api import CoingeckoHandler, ExchangerateHandler
from src.model.base_model import BaseModel
from src.view.window import MainWindow
from src.controller.main_controller import MainController
from src.loader import loader_instance as load

# Initializing logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main():
	# Qt event loop manager
	logger.info("Starting app...")
	app = QApplication(sys.argv)

	# Application interface
	logger.info("Initialize gui...")
	gui = MainWindow()

	# Displaying a window on the screen
	gui.show()
	logger.info("Showing window")

	# Getting data from the Coingecko API
	logger.info("Initialize Coingecko API handler...")
	coingecko_cache_handler = JSONCacheHandler(
		load.config["cache"].get("coingecko_cache_file_name"), 
		load.config["cache"].get("coingecko_time_to_live"))
	coingecko_api_handler = CoingeckoHandler(coingecko_cache_handler)
	logger.info('Coingecko API handler initialized')

	# Getting data from the Exchangerate API
	logger.info("Initialize Exchangerate API handler...")
	exchangerate_cache_handler = JSONCacheHandler(
		load.config["cache"].get("exchangerate_cache_file_name"),
		load.config["cache"].get("exchangerate_time_to_live"))
	exchangerate_api_handler = ExchangerateHandler(exchangerate_cache_handler)
	logger.info('Exchangerate API handler initialized')

	# Data processing model
	logger.info("Initialize model...")
	model = BaseModel(coingecko_api_handler, exchangerate_api_handler)
	logger.info('Model initialized')

	# Linking the interface to the model
	logger.info("Initialize controller...")
	main_controller = MainController(model, gui)
	logger.info('Controller initialized')

	# Connection of async event loop to the Qt event loop
	loop = QEventLoop(app)
	asyncio.set_event_loop(loop)
	with loop: 
		loop.run_forever()


if __name__ == "__main__":
	asyncio.run(main())
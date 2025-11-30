import asyncio
import sys
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
import logging

from src.model.cache import JSONCacheHandler
from src.model.api import CoingeckoHandler, ExchangerateHandler
from src.model.base_model import BaseModel
from src.view.window import MainWindow
from src.controller.main_controller import MainController
from src.config import (
	COINGECKO_CACHE_FILE_NAME,
	COINGECKO_TIME_TO_LIVE,
	EXCHANGERATE_CACHE_FILE_NAME,
	EXCHANGERATE_TIME_TO_LIVE
	)

# Initializing logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
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
	coingecko_cache_handler = JSONCacheHandler(COINGECKO_CACHE_FILE_NAME, COINGECKO_TIME_TO_LIVE)
	coingecko_api_handler = CoingeckoHandler(coingecko_cache_handler)
	logger.info('Coingecko API handler initialized')

	# Getting data from the Exchangerate API
	logger.info("Initialize Exchangerate API handler...")
	exchangerate_cache_handler = JSONCacheHandler(EXCHANGERATE_CACHE_FILE_NAME, EXCHANGERATE_TIME_TO_LIVE)
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
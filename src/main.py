import sys
from PyQt6.QtWidgets import QApplication

from src.api.cache import CacheHandler
from src.api.api_client import CoingeckoHandler, ExchangerateHandler
from src.model.data_handler import DataHandler
from src.gui.main_window import MainWindow
from src.controllers.main_controller import MainController
from src.config import (
	COINGECKO_CACHE_FILE_NAME,
	COINGECKO_TIME_TO_LIVE,
	EXCHANGERATE_CACHE_FILE_NAME,
	EXCHANGERATE_TIME_TO_LIVE
	)

def main():
	# Создание главного окна
	print("Starting app...", flush=True)
	app = QApplication(sys.argv)

	# Получение данных от Coingecko API
	print("Fetching Coingecko API...", flush=True)
	coingecko_cache_handler = CacheHandler(COINGECKO_CACHE_FILE_NAME, COINGECKO_TIME_TO_LIVE)
	coingecko_api_handler = CoingeckoHandler(coingecko_cache_handler)
	coingecko_data = coingecko_api_handler.fetch()
	print("Coingecko data:", coingecko_data, "...", flush=True)

	# Получение данных от Exchangerate API
	print("Fetching Exchangerate API...", flush=True)
	exchangerate_cache_handler = CacheHandler(EXCHANGERATE_CACHE_FILE_NAME, EXCHANGERATE_TIME_TO_LIVE)
	exchangerate_api_handler = ExchangerateHandler(exchangerate_cache_handler)
	exchangerate_data = exchangerate_api_handler.fetch()
	print("Exchangerate data:", exchangerate_data , "...", flush=True)

	# Модель обработки данных
	print("Initialize model...", flush=True)
	model = DataHandler(coingecko_data, exchangerate_data)

	# Интерфейс
	print("Initialize gui...", flush=True)
	gui = MainWindow()

	# Связь интерфейса с моделью
	print("Initialize controller...", flush=True)
	main_controller = MainController(model, gui)

	# Вывод окна на экран
	print("Showing window", flush=True)
	gui.show()
	app.exec()

if __name__ == "__main__":
	main()
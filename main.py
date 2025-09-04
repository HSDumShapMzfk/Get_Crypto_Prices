import sys
from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

from program.model.get_crypto_prices import GetCryptoPrices
from program.view.main_window import MainWindow

def main():
	# Загрузка параметров из .env
	load_dotenv()

	# Создание объекта класса, получающего список с данными о криптовалютах
	prices = GetCryptoPrices()
	prices.get_crypto_prices()
	prices.change_currency('rub')

	print('Crypto dataset:')
	for coin, values in prices.pricelist.items():
	    usd = values["usd"]
	    rub = values["selected_currency"]
	    print(f"\t{coin}: usd: {usd}, rub: {rub}")

	# Создание главного окна
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	app.exec()

if __name__ == "__main__":
	main()
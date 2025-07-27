from program.model.get_crypto_prices import GetCryptoPrices
from program.view.main_window import MainWindow

from PyQt6.QtWidgets import QApplication
import sys

def main():
	# Создание объекта класса, получающего список с данными о криптовалютах
	prices = GetCryptoPrices()
	prices.get_crypto_prices()

	# Создание главного окна
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	app.exec()

if __name__ == "__main__":
	main()
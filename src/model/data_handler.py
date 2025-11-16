# from src.api.api_client import fetch_image

class DataHandler:
	
	def __init__(self, coingecko_data: list[dict], exchangerate_data: dict) -> None:
		self.coingecko_data = coingecko_data
		self.exchangerate_data = exchangerate_data

	def _price_formatting(self, price: int | float, currency: str) -> str:
		""" Форматирование списка цен """
		new_price = price * self.exchangerate_data[currency]

		# Decimal places
		if new_price >= 100_000:
			return f"{new_price:.0f}"
		elif new_price >= 1:
			return f"{new_price:.2f}"
		else:
			return f"{new_price:.5f}"

	def generate_valid_dataset(self, currency: str = 'USD') -> list[dict]:
		""" Generating a dataset based on selected currency """
		dataset = list()
		for item in self.coingecko_data:
			new_item = {
				"market_rank" : str(item["market_cap_rank"]),
				"symbol" : item["symbol"],
				"price" : self._price_formatting(item["current_price"], currency),
				"high_24h" : str(item["high_24h"]),
				"low_24h" : str(item["low_24h"]),
				"price_change_percentage_24h" : str(item["price_change_percentage_24h"]),
				#"image" : fetch_image(item["symbol"], item["image"])
			}
			dataset.append(new_item)
		return dataset
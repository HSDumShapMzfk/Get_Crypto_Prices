# from src.api.api_client import fetch_image
import logging

from src.infrastructure.loader import loader_instance as load
from src.infrastructure.api import CoingeckoHandler, ExchangerateHandler

# logger = logging.getLogger(__name__)


class Model:
	
	def __init__(self, 
			coingecko_handler: CoingeckoHandler, 
			exchangerate_handler: ExchangerateHandler
	) -> None:
		self.coingecko_handler = coingecko_handler
		self.exchangerate_handler = exchangerate_handler
		self.current_currency = load.state.get("last_selected_currency")
		self.dataset = self.generate_dataset(self.current_currency)

	def get_data(self):
		self.coingecko_data = self.coingecko_handler.fetch()
		self.exchangerate_data = self.exchangerate_handler.fetch()

	def _price_formatting(self, price: int | float, currency: str) -> str:
		""" Formats the price in the selected currency """

		try:
			new_price = price * self.exchangerate_data[currency]
		except KeyError:
			logger.warning(f"Selected currency \"{self.current_currency}\" is not defined in the list of exchange rates.")
			logger.info(f"State: last_selected_currency - was chacnged to \"USD\"")
			load.state['last_selected_currency'] = "USD"
			self.current_currency = "USD"

			new_price = price
		# Decimal places
		if new_price >= 100_000: 
			decimal_value = 0
		elif new_price >= 1: 
			decimal_value = 2
		else: 
			decimal_value = 5
		return f"{new_price:.{decimal_value}f}"

	def _percentage_formatting(self, percentage, currency):
		new_percentage = percentage

	def generating_dataset_element(self, item: dict, currency: str) -> dict[str, str]:
		""" Generated a element of dataset  """

		formatted_price = self._price_formatting(item["current_price"], currency)
		new_item = {
				"market_rank" : str(item["market_cap_rank"]),
				"symbol" : item["symbol"].upper(),
				"price" : formatted_price,
				"high_24h" : str(item["high_24h"]),
				"low_24h" : str(item["low_24h"]),
				"price_change_percentage_24h" : str(item["price_change_percentage_24h"])
		}
		return new_item

	def generate_dataset(self, currency: str = 'USD') -> list[dict]:
		""" Generating a dataset based on selected currency """

		dataset = list()
		for item in self.coingecko_data:
			dataset.append(self.generating_dataset_element(item, currency))
		return dataset

	def change_currency(self, currency: str) -> None:
		""" Generates a dataset for the selected currency """

		self.current_currency = currency
		load.state["last_selected_currency"] = currency
		self.dataset = self.generate_dataset(self.current_currency)
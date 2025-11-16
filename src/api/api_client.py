from abc import ABC, abstractmethod
import requests
import asyncio
import aiohttp
import qasync

from src.api.cache import CacheHandler
from src.config import (
	COINGECKO_URL, 
	COINGECKO_PARAMS, 
	COINGECKO_CACHE_FILE_NAME, 
	COINGECKO_TIME_TO_LIVE,
	COINGECKO_DATA_TEMPLATE,
	EXCHANGERATE_KEY, 
	EXCHANGERATE_URL, 
	EXCHANGERATE_PARAMS,
	EXCHANGERATE_CACHE_FILE_NAME,
	EXCHANGERATE_TIME_TO_LIVE,
	EXCHANGERATE_DATA_TEMPLATE,
	RESPONSE_TIMEOUT, 
	DOWNLOADED_IMAGES_DIR,
	FILE_FORMAT,
	)


class APIHandler(ABC):
	""" An abstract class - API request handler 

		:param cache: CacheHandler class object
		"""

	def __init__(self, cache: CacheHandler) -> None:
		self.cache = cache

	def make_response(self, url: str, params: dict[str, str], timeout : tuple[int, int]) -> list | dict:
		""" Creating a data request from the API
			Returns raw data """
		try:
			response = requests.get(url, params=params, timeout=timeout)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			print(f'HTTP error: {e.response.status_code}')
		except requests.exceptions.ConnectionError:
			print(f'Server connection error!')
		except requests.exceptions.Timeout:
			print(f'Response timeout!')
		except requests.exceptions.RequestException as e:
			raise Exception(f"Произошла чудовищная ошибка: {e}!")
		else:
			return response.json()

	def fetch(self) -> list | dict:
		""" Choose between getting data from the cache or creating a new request """
		if self.cache.is_file_exist() and self.cache.is_time_to_live():
			# Getting cached data
			return self.cache.read_cahce()
			
		# Getting new data from the request
		response = self.make_response(self.url, self.params, RESPONSE_TIMEOUT)
		data = self.processing(response, self.template)
		self.cache.write_cache(data)
		return data

	@abstractmethod
	def processing(self, data, template):
		pass


class CoingeckoHandler(APIHandler):
	""" Class - coingecko api handler 

		:param cache: CacheHandler class object
		"""

	def __init__(self, cache: CacheHandler) -> None:
		super().__init__(cache)
		self.url = COINGECKO_URL
		self.params = COINGECKO_PARAMS
		self.template = COINGECKO_DATA_TEMPLATE

	def processing(self, data: list[dict], template: list[str]) -> list[dict]:
		""" Processing of received data 

			:param data: data received from the API
			:param template: data filtering template
		"""
		processed_data = [
		    {key: item[key] for key in template}
		    for item in data
		]
		return processed_data


class ExchangerateHandler(APIHandler):
	""" Class - exchangerate api handler 

		:param cache: CacheHandler class object
		"""

	def __init__(self, cache: CacheHandler) -> None:
		super().__init__(cache)
		self.url = EXCHANGERATE_URL
		self.params = EXCHANGERATE_PARAMS
		self.template = EXCHANGERATE_DATA_TEMPLATE

	def processing(self, data: dict[dict], template: str) -> dict:
		""" Processing of received data 

			:param data: data received from the API
			:param template: data filtering template
		"""
		processed_data = data[template]
		return processed_data


class ImageManager:

	def __init__(self):
		pass

	def forming_tasks(self, item: list):
		pass
		# tasks = [
		# 	async_download_png(item['symbol'], item['image'])
		# 	for item in dataset
		# ]
		# await asyncio.gather(*tasks)

	async def async_download_image(file_name: str, url: str) -> bool:
		""" Downloads an image of the transferred cryptocurrency
			Saves the directory specified in config.py
			Returns a bool depending on success """
		pass
		
		# url = url.replace("coin-images", 'assets')
		# async with aiohttp.ClientSession() as session:
		# 	async with session.get(url) as resp:
		# 		if resp.status == 200:
		# 			content = await resp.read()
		# 			with open(f"{DOWNLOADED_IMAGES_DIR}\\{file_name}.{FILE_FORMAT}", "wb") as f:
		# 				f.write(content)
		# 		else:
		# 			print(f"Ошибка: статус {resp.status}")

	def fetch(self):
		pass
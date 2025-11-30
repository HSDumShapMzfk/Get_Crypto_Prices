from abc import ABC, abstractmethod
import requests
import asyncio
import aiohttp
import qasync
import logging

from src.model.cache import JSONCacheHandler
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
	LOGO_DIR,
	LOGOS_EXTENSION,
	)

logger = logging.getLogger(__name__)


class APIHandler(ABC):
	""" An abstract class - API request handler """
		
	def __init__(self, cache: JSONCacheHandler) -> None:
		self.cache = cache

	def make_response(self, url: str, params: dict[str, str], timeout : tuple[int, int]) -> list | dict:
		""" Creating a request to receive data from the API
			Returns raw data """
		try:
			response = requests.get(url, params=params, timeout=timeout)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			logger.error(f'HTTP error: {e.response.status_code}')
		except requests.exceptions.ConnectionError:
			logger.error('Server connection error!')
		except requests.exceptions.Timeout:
			logger.error('Response timeout!')
		except requests.exceptions.RequestException as e:
			raise Exception(f"Произошла чудовищная ошибка: {e}!")
		else:
			return response.json()

	@abstractmethod
	def processing(self, data, template):
		pass

	def fetch(self) -> list | dict:
		""" Choose between getting data from the cache or creating a new request """
		if self.cache.is_file_exist() and self.cache.is_time_to_live():
			# Getting cached data
			logger.info('Retrieving saved data from the cache')
			return self.cache.read_cahce()
			
		# Getting new data from the request
		logger.info('Getting new data from the API')
		response = self.make_response(self.url, self.params, RESPONSE_TIMEOUT)
		data = self.processing(response, self.template)
		self.cache.write_cache(data)
		return data


class CoingeckoHandler(APIHandler):
	""" Class - coingecko api handler """
	url = COINGECKO_URL
	params = COINGECKO_PARAMS
	template = COINGECKO_DATA_TEMPLATE

	def __init__(self, cache: JSONCacheHandler) -> None:
		super().__init__(cache)

	def processing(self, data: list[dict], template: list[str]) -> list[dict]:
		""" Processing of received data """
		processed_data = [
		    {key: item[key] for key in template}
		    for item in data
		]
		return processed_data


class ExchangerateHandler(APIHandler):
	""" Class - exchangerate api handler """
	url = EXCHANGERATE_URL
	params = EXCHANGERATE_PARAMS
	template = EXCHANGERATE_DATA_TEMPLATE

	def __init__(self, cache: JSONCacheHandler) -> None:
		super().__init__(cache)
		
	def processing(self, data: dict[dict], template: str) -> dict:
		""" Processing of received data 

			:param data: data received from the API
			:param template: data filtering template
		"""
		processed_data = data[template]
		return processed_data


class ImageManager:

	def __init__(self):
		# Checking the existence of the images folder
		if not LOGO_DIR.exists():
			LOGO_DIR.mkdir()

	def forming_tasks(self, item: list):
		# tasks = [
		# 	async_download_logos(item['symbol'], item['image'])
		# 	for item in dataset
		# ]
		# await asyncio.gather(*tasks)
		pass
		

	async def async_download_logos(file_name: str, url: str) -> bool:
		""" Downloads an image of the transferred cryptocurrency
			Saves the directory specified in config.py
			Returns a bool depending on success """
		# url = url.replace("coin-images", 'assets')
		# async with aiohttp.ClientSession() as session:
		# 	async with session.get(url) as resp:
		# 		if resp.status == 200:
		# 			content = await resp.read()
		# 			with open(f"{LOGO_DIR}\\{file_name}.{LOGOS_EXTENSION}", "wb") as f:
		# 				f.write(content)
		# 		else:
		# 			print(f"Ошибка: статус {resp.status}")
		pass

	def fetch(self):
		pass
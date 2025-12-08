from abc import ABC, abstractmethod
import requests
import asyncio
import aiohttp
import qasync
import logging
from typing import Optional, Union
from pathlib import Path

from src.model.cache import JSONCacheHandler
from src.loader import loader_instance as load

logger = logging.getLogger(__name__)


class APIHandler(ABC):
	""" An abstract class - API request handler """
		
	def __init__(
		self, 
		cache: JSONCacheHandler,
		url: str,
		params: dict[str, str],
		template: Optional[Union[str, list[str]]]
	):
		self.cache = cache
		self.url = url
		self.params = params
		self.template = template

	def make_response(
		self, 
		url: str, 
		params: dict[str, str], 
		timeout : tuple[int, int]
	) -> list | dict:
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
			return self.cache.read_cahce()
			
		# Getting new data from the request
		response = self.make_response(
			self.url, 
			self.params, 
			tuple(load.config["api"].get("response_timeout")))
		data = self.processing(response, self.template)
		self.cache.write_cache(data)
		return data


class CoingeckoHandler(APIHandler):
	""" Class - coingecko api handler """
	url = load.config["api"].get("coingecko_url")
	params = load.config["api"].get("coingecko_params")
	template = load.config["api"].get("coingecko_data_template")

	def __init__(
		self, 
		cache: JSONCacheHandler,
		# url: str,
		# params: dict[str, str],
		# template: Optional[Union[str, list[str]]]
	):
		super().__init__(cache, self.url, self.params, self.template)

	def processing(self, data: list[dict], template: list[str]) -> list[dict]:
		""" Processing of received data """
		processed_data = [
		    {key: item[key] for key in template}
		    for item in data
		]
		return processed_data


class ExchangerateHandler(APIHandler):
	""" Class - exchangerate api handler """

	# Inserting an API key into a URL
	url_parts = load.config["api"].get("exchangerate_url")
	url = "".join([url_parts[0], load.env.get("EXCHANGERATE_KEY"), url_parts[1]])
	params = load.config["api"].get("exchangerate_params")
	template = load.config["api"].get("exchangerate_data_template")

	def __init__(
		self, 
		cache: JSONCacheHandler,
		# url: str,
		# params: dict[str, str],
		# template: Optional[Union[str, list[str]]]
	):
		super().__init__(cache, self.url, self.params, self.template)
		
	def processing(self, data: dict[dict], template: str) -> dict:
		""" Processing of received data 

			:param data: data received from the API
			:param template: data filtering template
		"""
		processed_data = data[template]
		return processed_data


class ImageManager:
	""" """
	LOGO_DIR = Path().cwd().joinpath("media\\crypto_images")

	def __init__(self):
		# Checking the existence of the images folder
		if not self.LOGO_DIR.exists():
			self.LOGO_DIR.mkdir()

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
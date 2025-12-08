from datetime import datetime, timedelta
import json
from pathlib import Path
import logging

from src.loader import loader_instance as load

logger = logging.getLogger(__name__)


class JSONCacheHandler:
	""" Reading and writing data into named .json files """
	CACHE_DIR = Path().cwd().joinpath("cache")
	DATETIME_FORMAT = load.config["cache"].get("datetime_format")

	def __init__(self, cache_file_name: str, time_to_live: int) -> None:
		# Checking the existence of the cache folder
		if not self.CACHE_DIR.exists():
			self.CACHE_DIR.mkdir()
		self.cache_file_name = cache_file_name
		self.cache_file_path = Path(self.CACHE_DIR).joinpath(self.cache_file_name).with_suffix('.json')
		self.time_to_live = time_to_live

	def is_file_exist(self) -> bool:
		""" Checks if a file exists
			Returns True if the file is exist """
		return self.cache_file_path.exists()

	def is_time_to_live(self) -> bool:
		""" Checks the time to live parameter in the file
			Returns True if the data is still current """
		with open(self.cache_file_path, 'r') as file:
			file_content = json.load(file)
		return datetime.strptime(file_content['time_to_live'], self.DATETIME_FORMAT) > datetime.now()

	def write_cache(self, data: list | dict) -> None:
		""" Writes data to the cache
			Also records the cached at and time to live """
		logger.debug(f"Write cache to {self.cache_file_path}")
		file_content = {
			'cached_at' : str(datetime.now().strftime(self.DATETIME_FORMAT)),
			'time_to_live' : str((datetime.now() + timedelta(minutes=self.time_to_live)).strftime(self.DATETIME_FORMAT)),
			'data' : data
		}
		with open(self.cache_file_path, 'w') as file:
			json.dump(file_content, file, ensure_ascii=False, indent=4)

	def read_cahce(self) -> list | dict:
		""" Reading a .json file 
			Returns cached data """
		logger.debug(f"Read cache from {self.cache_file_path}")
		with open(self.cache_file_path, 'r') as file:
			file_data = json.load(file)
		return file_data['data']
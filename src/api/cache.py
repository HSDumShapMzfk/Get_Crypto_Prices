from datetime import datetime, timedelta
import json
from pathlib import Path

from src.config import (
	CACHE_DIR,
	DATETIME_FORMAT
	)


class CacheHandler:
	""" Simple caching handler ;) """

	def __init__(self, cache_file_name: str, time_to_live: int) -> None:
		self.cache_file_name = cache_file_name
		self.time_to_live = time_to_live

	def is_file_exist(self) -> bool:
		""" Checks if a file exists
			Returns True if the file is exist """
		return (Path(CACHE_DIR) / self.cache_file_name).exists()

	def is_time_to_live(self) -> bool:
		""" Checks the time to live parameter in the file
			Returns True if the data is still current """
		with open(Path(CACHE_DIR).joinpath(self.cache_file_name), 'r') as file:
			file_content = json.load(file)
		return datetime.strptime(file_content['time_to_live'], DATETIME_FORMAT) > datetime.now()

	def write_cache(self, data: list | dict) -> None:
		""" Writes data to the cache
			Also records the cached at and time to live """
		file_content = {
			'cached_at' : str(datetime.now().strftime(DATETIME_FORMAT)),
			'time_to_live' : str((datetime.now() + timedelta(minutes=self.time_to_live)).strftime(DATETIME_FORMAT)),
			'data' : data
		}
		with open(Path(CACHE_DIR).joinpath(self.cache_file_name), 'w') as file:
			json.dump(file_content, file, ensure_ascii=False, indent=4)

	def read_cahce(self) -> list | dict:
		""" Returns cached data """
		with open(Path(CACHE_DIR).joinpath(self.cache_file_name), 'r') as file:
			file_data = json.load(file)
		return file_data['data']
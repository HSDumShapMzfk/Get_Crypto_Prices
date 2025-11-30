from datetime import datetime, timedelta
import json
from pathlib import Path
import logging

from src.config import (
	CACHE_DIR,
	STATE_DIR,
	STATE_FILE_NAME,
	DATETIME_FORMAT
	)

logger = logging.getLogger(__name__)


class JSONCacheHandler:
	""" Reading and writing data into named .json files """

	def __init__(self, cache_file_name: str, time_to_live: int) -> None:
		# Checking the existence of the cache folder
		if not CACHE_DIR.exists():
			CACHE_DIR.mkdir()
		self.cache_file_name = cache_file_name
		self.cache_file_path = Path(CACHE_DIR).joinpath(self.cache_file_name).with_suffix('.json')
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
		return datetime.strptime(file_content['time_to_live'], DATETIME_FORMAT) > datetime.now()

	def write_cache(self, data: list | dict) -> None:
		""" Writes data to the cache
			Also records the cached at and time to live """
		file_content = {
			'cached_at' : str(datetime.now().strftime(DATETIME_FORMAT)),
			'time_to_live' : str((datetime.now() + timedelta(minutes=self.time_to_live)).strftime(DATETIME_FORMAT)),
			'data' : data
		}
		with open(self.cache_file_path, 'w') as file:
			json.dump(file_content, file, ensure_ascii=False, indent=4)

	def read_cahce(self) -> list | dict:
		""" Reading a .json file 
			Returns cached data """
		with open(self.cache_file_path, 'r') as file:
			file_data = json.load(file)
		return file_data['data']


class State:
	""" Saving user attributes for use in subsequent sessions """
	state_file_name = STATE_FILE_NAME
	state_file_path = Path(STATE_DIR).joinpath(state_file_name).with_suffix('.json')

	def __init__(self) -> None:
		self.initialize_state()

	def is_dir_exist(self) -> None:
		""" Checks if a dir exists
			Create dir if it does not exist """
		if not STATE_DIR.exists():
			STATE_DIR.mkdir()

	def is_file_exist(self) -> None:
		""" Checks if a file exists
			Create file if it does not exist """
		if not self.state_file_path.exists():
			self.generate_default_state()
			self.write_state()

	def generate_default_state(self) -> None:
		""" Generates data for the default state """
		self.last_selected_currency = "USD"

	def read_state(self) -> None:
		""" """
		with open(self.state_file_path, 'r') as file:
			file_data = json.load(file)
		self.last_selected_currency = file_data["last_selected_currency"]

	def write_state(self) -> None:
		""" """
		with open(self.state_file_path, 'w') as file:
			file_content = {
				"last_selected_currency" : self.last_selected_currency
			}
			json.dump(file_content, file, ensure_ascii=False, indent=4)


	def initialize_state(self) -> None:
		""" """
		self.is_dir_exist()
		self.is_file_exist()
		self.read_state()


state_instance = State()
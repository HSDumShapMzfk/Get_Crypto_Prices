from dotenv import dotenv_values
import os
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class Loader:
    """ Provides access to data from config.json, state.json, and .env
        Allows writing data to writable files """
    CONFIG_PATH = Path().cwd().joinpath("config.json")
    STATE_PATH = Path().cwd().joinpath("state.json")
    ENV_PATH = Path().cwd().joinpath(".env")

    def __init__(self) -> None:
        self.config = self._read_config()
        self.state = self._load_state()
        self.env = self._load_env()

    """ Config
        Read-only """
    def _read_config(self) -> dict[dict]:
        """ Returns the read data from config.json """
        with open(self.CONFIG_PATH, "r") as file:
            file_content = json.load(file)
        logger.debug("The config has ben read")
        return file_content


    """ State
        Generate default, read, write """
    def _load_state(self) -> dict:
        """ Choosing between reading data and default generation """
        if not self.STATE_PATH.exists():
            self._generate_state()
        return self.read_state()

    def _generate_state(self) -> None:
        """ Generates state.json with default content """
        state_default_content = {"last_selected_currency": "USD"}
        with open(self.STATE_PATH, 'w') as file:
            json.dump(state_default_content, file, ensure_ascii=False, indent=4)
        logger.debug(f"The state has been generated")

    def read_state(self) -> dict:
        """ Returns the read data from state.json """
        with open(self.STATE_PATH, "r") as file:
            file_content = json.load(file)
        logger.debug("The state has ben read")
        return file_content

    def write_state(self) -> None:
        """ Writes data from self.state to state.json """
        with open(self.STATE_PATH, "w") as file:
            json.dump(self.state, file, ensure_ascii=False, indent=4)
        logger.debug("The state was written")


    """ Env
        Read and write """
    def _load_env(self) -> dict[str, str | None]:
        """ Choosing between reading data and default generation """
        if not self.ENV_PATH.exists():
            return {}
        return self.read_env()

    def read_env(self) -> dict[str, str]:
        """ Returns the read data from .env """
        file_data = dotenv_values(self.ENV_PATH)
        logger.debug("The dotenv has ben read")
        return file_data    

    def write_env(self) -> None:
        """ Writes data from self.env to .env """
        with open(self.ENV_PATH, 'w') as file:
            file.writelines(f"{key.upper()}={value}\n" for key, value in self.env.items() if value)
        logger.debug("The dotenv was written")


loader_instance = Loader()
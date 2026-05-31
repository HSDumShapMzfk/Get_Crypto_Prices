from dotenv import dotenv_values
import os
from pathlib import Path
import json
import logging
from typing import Any

# logger = logging.getLogger(__name__)


class Loader:
    """ Provides access to data from config.json, state.json, and .env
    Allows writing data to writable files """
    WD_PATH = Path(__file__).parent.parent.parent
    CONFIG_PATH = WD_PATH / "config.json"
    STATE_PATH = WD_PATH / "state.json"
    ENV_PATH = WD_PATH / ".env"

    def __init__(self) -> None:
        self.config = self._read_config()
        self.state = self._load_state()
        self.env = self._load_env()

    """ Config
    Read-only """
    def _read_config(self) -> dict[str, Any]:
        """ Returns the read data from config.json """
        with open(self.CONFIG_PATH, "r") as file:
            file_content = json.load(file)
        # logger.debug("The config has ben read")
        return file_content


    """ State
    Generate default, read, write """
    def write_state(self) -> None:
        """ Writes data from self.state to state.json """
        with open(self.STATE_PATH, "w") as file:
            json.dump(self.state, file, ensure_ascii=False, indent=4)
        # logger.debug("The state was written")

    def read_state(self) -> dict[str, Any]:
        """ Returns the read data from state.json """
        with open(self.STATE_PATH, "r") as file:
            file_content = json.load(file)
        # logger.debug("The state has ben read")
        return file_content

    def _generate_state(self) -> None:
        """ Generates state.json with default content """
        state_default_content = {"last_selected_currency": "USD"}
        with open(self.STATE_PATH, 'w') as file:
            json.dump(state_default_content, file, ensure_ascii=False, indent=4)
        # logger.debug(f"The state has been generated")

    def _load_state(self) -> dict[str, Any]:
        """ Choosing between reading data and default generation """
        if not self.STATE_PATH.exists():
            self._generate_state()
        return self.read_state()


    """ Env
    Read and write """
    def read_env(self) -> dict[str, str]:
        """ Returns the read data from .env """
        file_data = dotenv_values(self.ENV_PATH)
        # logger.debug("The dotenv has ben read")
        return file_data    

    def write_env(self) -> None:
        """ Writes data from self.env to .env """
        with open(self.ENV_PATH, 'w') as file:
            file.writelines(f"{key.upper()}={value}\n" for key, value in self.env.items() if value)
        # logger.debug("The dotenv was written")

    def _load_env(self) -> dict[str, str] | None:
        """ Choosing between reading data and default generation """
        if not self.ENV_PATH.exists():
            return {}
        return self.read_env()


loader_instance = Loader()
import requests
import logging
from typing import Optional, Any
from pathlib import Path
from enum import Enum, auto
from dataclass import dataclass
from abc import ABC, abstractmethod

# logger = logging.getLogger(__name__)

class APIError(Enum):
	INVALID_API_KEY = auto()
    TIMEOUT = auto()
    NETWORK = auto()
    SERVER = auto()
    UNKNOWN = auto()


@dataclass(frozen=True)
class APIResponse:
	sucsess: bool
	payload: Optional[Any] = None
	error: Optional[APIError] = None


class APIRequest(ABC):
    @abstractmethod
    def make_response(self, url: str, params: dict[str, str], timeout: tuple[int, int]) -> APIResponse:
        pass


class CoinGeckoAPI(APIRequest):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "per_page": "200"}
    timeout = (5, 15)

    def __init__(self):
        self. 
    def make_response(self, )
import requests
import logging
from typing import Optional, Any
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass

from src.infrastructure.loader import loader_instance as load

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


class APIHandler:

	def __init__(
		self, 
		url: str,
		params: dict[str, str],
		timeout: tuple[int, int],
	):
		self.url = url
		self.params = params
		self.timeout = timeout

	def make_request(self) -> APIResponse:
		""" Makes a request to the API
		Returns a API data transfer object """
        try:
            response = requests.get(self.url, params=self.params, timeout=self.timeout)

            if response.status_code in (401, 403):
                return APIResponse(
                    success=False,
                    error=ApiError.INVALID_API_KEY
                )

            if response.status_code >= 500:
                return APIResponse(
                    success=False,
                    error=ApiError.SERVER
                )

            response.raise_for_status()

            return APIResponse(
                success=True,
                payload=response.json()
            )

        except requests.exceptions.Timeout:
            # logger.error("Request timeout")
            return APIResponse(
                success=False,
                error=ApiError.TIMEOUT
            )

        except requests.exceptions.ConnectionError:
            # logger.error("Network error")
            return APIResponse(
                success=False,
                error=ApiError.NETWORK
            )

        except requests.exceptions.RequestException:
            # logger.exception("Unknown request error")
            return APIResponse(
                success=False,
                error=ApiError.UNKNOWN
            )
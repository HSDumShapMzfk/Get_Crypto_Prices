from src.infrastructure.loader import loader_instance as load


class APIKeyService:
	""" """

	def has_key(self) -> bool:
		return load.env.get("EXCHANGERATE_KEY")

	def is_valid_key(self) -> bool:
		pass
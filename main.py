import sys
from program.model.get_crypto_prices import GetCryptoPrices

def main():
	prices = GetCryptoPrices()
	prices.get_crypto_prices()

if __name__ == "__main__":
	main()
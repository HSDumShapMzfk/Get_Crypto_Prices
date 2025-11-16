from dotenv import load_dotenv
import os
from pathlib import Path

# Загрузка данных из окружения (.env)
load_dotenv()

# --- API ---
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_PARAMS = {"vs_currency": "usd", "per_page": "200"}

EXCHANGERATE_KEY = os.getenv("EXCHANGERATE_KEY")
EXCHANGERATE_URL = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_KEY}/latest/USD' if EXCHANGERATE_KEY else None
EXCHANGERATE_PARAMS = None

# Время (сек), необходимое для установления соединения и ожидания ответа, соответственно
RESPONSE_TIMEOUT = (5, 15)

# Параметры для скачиваемых изображений криптовалют
DOWNLOADED_IMAGES_DIR = Path().cwd().joinpath('media').joinpath('Crypto_images')
FILE_FORMAT = 'png'

# --- Cache ---
CACHE_DIR = Path().cwd().joinpath('cache')

COINGECKO_CACHE_FILE_NAME = "coingecko.json"
COINGECKO_DATA_TEMPLATE = [
    "id",
    "symbol",
    "name",
    "image",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "fully_diluted_valuation",
    "total_volume",
    "high_24h",
    "low_24h",
    "price_change_24h",
    "price_change_percentage_24h",
    "market_cap_change_24h",
    "market_cap_change_percentage_24h"
]

EXCHANGERATE_CACHE_FILE_NAME = "exchangerate.json"
EXCHANGERATE_DATA_TEMPLATE = "conversion_rates"

# Формат сохранения даты
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Время (мин), по истечении которого данные в файле считаются устаревшими
COINGECKO_TIME_TO_LIVE = 15

EXCHANGERATE_TIME_TO_LIVE = 600

# Минимальное время (мин) принудительного обновления данных
FORCED_UPDATE = 1

# --- Controller ---

LAST_SELECTED_CURRENCY = "USD"
import requests
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

class GetCryptoPrices:
    """ Управление запросами к Coingecko и ExchangeRate, форматирование цен """

    def __init__(self):
        self.current_dir = Path(__file__).resolve().parent
        self.time_now = datetime.now()
        self.time_last_update_status = False

        with open(f'{self.current_dir}\\cryptocurrencies.json', 'r') as file: 
            self.cryptocurrencies = json.load(file)
        self.pricelist = {}
        self.ids = []
        for i in range(len(self.cryptocurrencies)):
            self.pricelist[self.cryptocurrencies[i]['name']] = {}
            self.pricelist[self.cryptocurrencies[i]['name']]['usd'] = self.cryptocurrencies[i]['current_price']
            self.pricelist[self.cryptocurrencies[i]['name']]['selected_currency'] = self.cryptocurrencies[i]['current_price']
            self.ids.append(self.cryptocurrencies[i]['id'])

        with open(f'{self.current_dir}\\currencies.json', 'r') as file: 
            self.iso_currencies = json.load(file)

        with open(f'{self.current_dir}\\time last update api.json', 'r') as file: 
            self.time_last_update_dataset = json.load(file)

    def show_time_last_update_dataset(self, firs_line=False):
        # Выводит в консоль словарь self.time_last_update_dataset

        if firs_line: print('Dataset of last API update times:')
        else: print('\nDataset of last API update times:')
        for i in range(len(self.time_last_update_dataset)):
            key = list(self.time_last_update_dataset.keys())[i]
            print(f'\t{key.title().replace("_", " ")}\t{self.time_last_update_dataset[key]}')

    def check_last_api_update(self, api_title, timedelta_hours=0):
        if api_title in self.time_last_update_dataset:
            print(f'\nStarting to check_last_api_update({api_title}):')
            try:
                # Срабатывает когда удалось распарсить дату из json
                time_last_update = datetime.strptime(self.time_last_update_dataset[api_title], '%Y-%m-%d %H:%M:%S.%f')
            except:
                # Срабатывает когда не удалось распарсить дату, она была введена некорректно, или она отсутствовала в значении ключа
                print(f'\tFailed to get data about the latest update of "{api_title}".')
                return True

            elapsed = self.time_now - time_last_update
            print(f'\tDelta time is: {elapsed}')

            if elapsed >= timedelta(hours=timedelta_hours):
                print(f'\tEnough time has passed ({timedelta_hours} hours) for a new request to the {api_title}')
                return True
            else:
                print(f'\tNot enough time has passed ({timedelta_hours} hours) to request the {api_title}')
                return False

        else: 
            print(f'\n\tThere is no API named "{api_title}" in the dataset.')
            return False

    def save_time_last_update(self):
        print('\nThe API dataset is being updated...')
        with open(f'{self.current_dir}\\time last update api.json', 'w') as file: 
            json.dump(self.time_last_update_dataset, file, ensure_ascii=False, indent=4)
        print('\tAPI dataset update successful\n')

    def fetch_coingecko(self):
        """ Запрос к Coingecko API 
            сохранение полученных данных в переменную pricelist и файл ticker_symbols.json """
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
        "vs_currency": "usd",
        "ids": ','.join(self.ids)}
        response = requests.get(url, params=params)
    
        # Обработка ошибок
        if response.status_code == 200:
            self.cryptocurrencies = response.json()
        elif response.status_code == 429:
            print("Превышен лимит получения запросов от API. Попробуйте позже.")
            return False
        else:
            print("Не удалось получить данные от Coingecko API")
            return False

        # Очищение неактуальных данных из pricelist
        self.pricelist = {}

        # Присоединение name/current_price в словарь pricelist
        for i in range(len(self.cryptocurrencies)):
            self.pricelist[self.cryptocurrencies[i]['name']] = {}
            self.pricelist[self.cryptocurrencies[i]['name']]['usd'] = self.cryptocurrencies[i]['current_price']
            self.pricelist[self.cryptocurrencies[i]['name']]['selected_currency'] = self.cryptocurrencies[i]['current_price']

        # Сохранение полученных данных в файл cryptocurrencies.json
        with open(f'{self.current_dir}\\cryptocurrencies.json', 'w') as file:
            json.dump(self.cryptocurrencies, file, ensure_ascii=False, indent=4)

        # Сохранение времени запроса
        self.time_last_update_dataset['coingecko_api'] = f'{self.time_now}'
        self.time_last_update_status = True
        return True

    def fetch_exchangerate(self):
        """ Запрос к Exchange Rate API 
            сохранение полученных данных в переменную iso_currencies и файл currencies.json """
        EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
        url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Очищение неактуальных данных из iso_currencies
            self.iso_currencies = {}

            # Заполнение iso_currencies новыми данными, полученными от Exchange Rate API
            for i in range(len(data['conversion_rates'])):
                key = list(data['conversion_rates'].keys())[i]
                self.iso_currencies[key] = data['conversion_rates'][key]

            # Сохранение полученных данных в файл currencies.json
            with open(f'{self.current_dir}\\currencies.json', 'w') as file:
                json.dump(self.iso_currencies, file, ensure_ascii=False, indent=4)

            # Сохранение времени запроса данных от Exchange Rate API
            self.time_last_update_dataset['exchangerate_api'] = f'{self.time_now}'
            self.time_last_update_status = True

            return True
        else:
            print("Не удалось получить данные от Exchange rate API")
            return False

    def normalize_value(self):
        unnormalize_pricelist = []

        for i in self.pricelist:
            unnormalize_pricelist.append(self.pricelist[i]['selected_currency'])
            
        normalize_pricelist = [] 

        for i in range(len(unnormalize_pricelist)):
            if unnormalize_pricelist[i] >= 100_000:
                float_part_size = 0
            elif unnormalize_pricelist[i] >= 1:
                float_part_size = 2
            else:
                float_part_size = 4

            #исключение научной натации (9.48e-06 -> 0.00000948)
            price = f"{unnormalize_pricelist[i]:.20f}".rstrip("0").rstrip(".")  
            # price = str(unnormalize_pricelist[i])

            # Разделение цены на целую часть, и часть после точки
            split_price = price.split(".") 

            # Целая часть
            integer_part = str(split_price[0])

            # Дробная часть
            if len(split_price) == 2:
                float_part = str(split_price[1])
            else:
                float_part = None

            # Разбиение целой части на элементы списка. Пример: 2450 -> ['2', '4', '5', '0']
            buffer = list(integer_part)
                
            # Разделение на разряды в целой части цены
            buffer.reverse()
            result = list() 
            k = 0
            for i in range(len(buffer)):
                if k < 3:
                    result.append(buffer[i])
                    k += 1
                else:
                    result.append(",")
                    result.append(buffer[i])
                    k = 1

            result.reverse()

            # Присоединение списка целой части, и дробной части (если есть), к normalized_price. 
            # Пример: ['2', '.', '4', '5', '0'] -> 2.450
            normalized_price = "".join(result)

            if float_part_size == 0:
                pass

            elif float_part_size == 2:
                '''
                    ToDo: fix this shit someday ↓↓↓
                '''
                try: 
                    normalized_price += "." + "".join(float_part[:2])
                except:
                    normalized_price += "." + "00"

            elif float_part_size == 4:
                normalized_price += '.'

                first_nonzero = next((i for i, x in enumerate(float_part) if x != "0"), None)

                if first_nonzero is not None:
                    # до первой ненулевой строки (только нули в начале)
                    for num in float_part[:first_nonzero]:
                        normalized_price += num

                    # начиная с первой ненулевой строки и дальше
                    c = 0
                    for num in range(len(float_part[first_nonzero:])-1):
                        if c < float_part_size:
                            if float_part[first_nonzero:][num] != '0':
                                normalized_price += float_part[first_nonzero:][num]
                                c += 1
                            else:
                                if float_part[first_nonzero:][num] != '0' or float_part[first_nonzero:][num+1] != '0':
                                    normalized_price += float_part[first_nonzero:][num]
                                    c += 1
                                else: 
                                    break

            normalize_pricelist.append(normalized_price)

        # Цикл перебора списка отсортированных цен - normalize_pricelist, и изменение значений self.pricelis.
        for i in range(len(normalize_pricelist)):
            key = list(self.pricelist.keys())[i]
            self.pricelist[key]['selected_currency'] = normalize_pricelist[i]

    # ----------------- Смена валюты -----------------
    def change_currency(self, currency):
        rate = self.iso_currencies[currency.upper()]

        for i in self.pricelist:
            self.pricelist[i]['selected_currency'] = self.pricelist[i]['usd'] * rate

        self.normalize_value()

    # ----------------- Основной рабочий процесс -----------------
    def get_crypto_prices(self):
        self.show_time_last_update_dataset(firs_line=True)

        if self.check_last_api_update('coingecko_api', timedelta_hours=1):
            if self.fetch_coingecko():
                print('\nData from Coingecko API successfully received')
        if self.check_last_api_update('exchangerate_api', timedelta_hours=6):
            if self.fetch_exchangerate():
                print('\nData from Exchange Rate API successfully received')

        self.show_time_last_update_dataset()

        if self.time_last_update_status: self.save_time_last_update()
        else: print('\nThe API dataset json has not been updated.\n')

        self.normalize_value()
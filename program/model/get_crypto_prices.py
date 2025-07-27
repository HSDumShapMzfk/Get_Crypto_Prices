import requests

class GetCryptoPrices:
    """Класс, получающий прайслист популярных криптовалют, и отдающий его в виде списка.
    ToDo:
        ~ Реализовать возможность функционирования класса с переданным ему списком криптовалют и банковских кодов. 
            Пример: GetCryptoPrices(ids=['dogecoin', 'litecoin'], currencies=['kzt', 'cny', 'eur'])
        ~ Оптимизировать работу класса."""

    def __init__(self):
        self.url = 'https://api.coingecko.com/api/v3/simple/price'
        self.ids = ['bitcoin', 'ethereum', 'tron']
        self.currencies = ['rub', 'usd']
        self.pricelist = {}

    def fetch_prices(self):
        # Получает данные от coingeco api, и отдаёт их в self.pricelist

        params = {
            'ids': ','.join(self.ids),
            'vs_currencies': ','.join(self.currencies)
        }

        response = requests.get(self.url, params=params)
    
        if response.status_code == 200:

            data = response.json()

            self.pricelist = {
                'btc_usd': data['bitcoin']['usd'],
                'btc_rub': data['bitcoin']['rub'],

                'eth_usd': data['ethereum']['usd'],
                'eth_rub': data['ethereum']['rub'],

                'trx_usd': data['tron']['usd'],
                'trx_rub': data['tron']['rub']
            }   

            return True

        else:
            print("Не удалось получить данные от API")
            return False

    def normalize_value(self):
        # Получает список self.pricelist, изменяет вид записи цен, и обратно перезаписывает в self.pricelist.
        # Добавляет точки, разделяющие цену на разряды. 
        # Заменяет точку, разделяющую дробную часть цены от целой, на запятую.
        # Пример: 1000000.00 -> 100.000,00

        # Список с неотсортированными ценами. Пример: [117384, 9162554, 2944.27, 229820, 0.302358, 23.6]
        unnormalize_pricelist = [] 

        # Перебираем значения self.pricelist и добавляем их в unnormalize_pricelist
        for i in self.pricelist:
            unnormalize_pricelist.append(self.pricelist[i])

        # Список с сортированными ценами. Пример: ['117.384', '9.162.554', '2.944,27', '229.820', '0,302358', '23,6']
        normalize_pricelist = [] 

        # Цикл перебора списка unnormalize_pricelist
        for item in unnormalize_pricelist:
            price = str(item)
            buffer = list()
            normalized_price = ""
        
            # Замена ".", разделяющую дробную чать от целой, на ","
            price = price.replace(".", ",")

            # Разделение цены на целую часть, и часть после запятой
            split_price = price.split(",") 

            # Целая часть
            integer_part = str(split_price[0])

            # Дробная часть
            if len(split_price) == 2:
                float_part = str(split_price[1])

            else:
                float_part = None

            # Разбиение целой части на элементы списка. Пример: 2450 -> ['2', '4', '5', '0']
            for char in integer_part:
                buffer.append(char)
                
            # Разделение на разряды в целой части цены
            buffer.reverse()
            result = list() 
            k=0
            for i in range(len(buffer)):
                if k < 3:
                    result.append(buffer[i])
                    k += 1
                else:
                    result.append(".")
                    result.append(buffer[i])
                    k = 1

            result.reverse()

            # Присоединение списка целой части, и дробной части (если есть), к normalized_price. 
            # Пример: ['2', '.', '4', '5', '0'] -> 2.450
            normalized_price = "".join(result)
            if float_part:
                normalized_price += ","
                normalized_price += float_part

            normalize_pricelist.append(normalized_price)

        # Цикл перебора списка отсортированных цен - normalize_pricelist, и изменение значений self.pricelis.
        for i in range(len(normalize_pricelist)):
            key = list(self.pricelist.keys())[i]
            self.pricelist[key] = normalize_pricelist[i]

    def get_crypto_prices(self):
        if self.fetch_prices():
            self.normalize_value()
            print(self.pricelist)
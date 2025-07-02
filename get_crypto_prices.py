# Программа, которая выводит курс криптовалют

import requests

def get_response():
    pass

#---------------------------------------------------
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {
    'ids': 'bitcoin,ethereum,tron',
    'vs_currencies': 'rub,usd'
}

response = requests.get(url, params=params)

if response.status_code == 200:

    data = response.json()
    btc_price_usd = data['bitcoin']['usd']
    btc_price_rub = data['bitcoin']['rub']

    eth_price_usd = data['ethereum']['usd']
    eth_price_rub = data['ethereum']['rub']
    
    trx_price_usd = data['tron']['usd']
    trx_price_rub = data['tron']['rub']

else:
    print("Не удалось получить данные от API")
#---------------------------------------------------

def normalize_value(price):
    #Функция добавляет запятые, разделяющие цену на разряды. Пример: 100.000,00

    price = str(price)
    buffer = list()
    normalized_price = ""
    
    #Замена ".", разделяющую дробную чать от целой, на ","
    price = price.replace(".", ",")

    #Разделение цены на целую часть, и часть после запятой
    split_price = price.split(",") 
    # print(f"split_price {split_price}\n")

    #Целая часть
    integer_part = str(split_price[0])
    # print(f"integer_part {integer_part}\n")

    #Дробная часть
    if len(split_price) == 2:
        float_part = str(split_price[1])
        # print(f"float_part {float_part}\n")
    else:
        float_part = None

    #Разбиение целой части на элементы списка. Пример: 2450 -> ['2', '4', '5', '0']
    for char in integer_part:
        buffer.append(char)
    # print(f'Массив = {buffer}')
        
    #Разделение на разряды в целой части цены
    buffer.reverse()
    result = list() 
    k=0
    for i in range(len(buffer)):
        # print(f'buffer {buffer}')
        if k < 3:
            result.append(buffer[i])
            k += 1
        else:
            result.append(".")
            result.append(buffer[i])
            k = 1

    result.reverse()

    #Присоединение списка целой части, и дробной части (если есть), к normalized_price. Пример: ['2', '.', '4', '5', '0'] -> 2.450
    normalized_price = "".join(result)
    if float_part:
        normalized_price += ","
        normalized_price += float_part
    # print(f"Результат {normalized_price}")

    return normalized_price

print(f"Цена BTC: \n\t${normalize_value(btc_price_usd)}\n\t₽{normalize_value(btc_price_rub)}\n")
print(f"Цена ETH: \n\t${normalize_value(eth_price_usd)}\n\t₽{normalize_value(eth_price_rub)}\n")
print(f"Цена TRX: \n\t${normalize_value(trx_price_usd)}\n\t₽{normalize_value(trx_price_rub)}\n")

# print(f"Нормализированная цена:\nЦена ETH: \n${normalize_value(eth_price_usd)}\n{normalize_value(eth_price_rub)}₽\n")
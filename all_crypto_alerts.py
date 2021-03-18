#!/usr/local/bin/python3

import requests
from datetime import datetime
from slack import WebClient

api_token = 'c16p74f48v6ppg7f0utg'
cryptos_symbols = ['BINANCE:HBARBUSD', 'BINANCE:MANABUSD', 'BINANCE:ONEBUSD', 'BINANCE:ADABUSD']

cryptos_bought = {
    'HBARBUSD': {'high': '0.500'},
    'MANABUSD': {'high': '1.210'},
    'ONEBUSD': {'high': '0.108'},
    'ADABUSD': {'high': '2.00'}
}

def alert(crypto_name):

    if crypto_name in cryptos_bought:
        val = cryptos_bought.get(crypto_name)
        return float(val.get('high'))


datetime_object = str(datetime.now())
current = datetime_object.split(' ')
current_year = int(current[0].split('-')[0])
current_month = int(current[0].split('-')[1])
current_date = int(current[0].split('-')[2])
current_hour = int(current[1].split(':')[0])
current_minute = int(current[1].split(':')[1])

to_unix_timestamp = int(datetime(current_year, current_month, current_date, current_hour, current_minute).timestamp())
from_unix_timestamp = to_unix_timestamp - 60

# Finnhub api endpoint
crypto_price_url = "https://finnhub.io/api/v1/crypto/candle"
client = WebClient(token='xoxb-1053066397318-1814920326242-r5GiSyZMOwxSkCCUoM37apSZ')

for cryptos in cryptos_symbols:
    crypto_params = {"symbol": cryptos, "token": api_token, "resolution": "1", "from": from_unix_timestamp, "to": to_unix_timestamp}
    response = requests.get(crypto_price_url, crypto_params)
    if response.status_code == 429:
        client.chat_postMessage(channel='#crypto_alerts',
                                text=f" Around {datetime_object} -> API Limits exceeded for Finnhub api in {crypto_params['symbol']} alert")
    else:
        try:
            json_data = response.json()
            response.raise_for_status()
            closing_price_json = json_data['c']
            closing_price = closing_price_json[0]
            price_data = round(closing_price, 3)
            crypto = cryptos.split(':')[1]
            if price_data >= alert(crypto):
                client.chat_postMessage(channel='#crypto_alerts',
                                        text=f" Around {datetime_object} -> {crypto_params['symbol']} price: {price_data}")

        except KeyError as err:
            client.chat_postMessage(channel='#crypto_alerts',
                                    text=f" Around {datetime_object} -> check the crypto_params-{err} in {crypto_params['symbol']} alert")

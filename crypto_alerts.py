#!/usr/local/bin/python3

import requests
from datetime import datetime
from slack import WebClient
import os

SLACK_API_TOKEN = os.getenv('SLACK_TOKEN')
FINN_API_TOKEN = os.getenv('FINN_TOKEN')

# Finnhub api endpoint
crypto_price_url = "https://finnhub.io/api/v1/crypto/candle"
client = WebClient(token=SLACK_API_TOKEN)
datetime_object = str(datetime.now())
current = datetime_object.split(' ')
current_year = int(current[0].split('-')[0])
current_month = int(current[0].split('-')[1])
current_date = int(current[0].split('-')[2])
current_hour = int(current[1].split(':')[0])
current_minute = int(current[1].split(':')[1])


to_unix_timestamp = int(datetime(current_year, current_month, current_date, current_hour, current_minute).timestamp())
from_unix_timestamp = to_unix_timestamp - 900


crypto_params = {
    "symbol": "KRAKEN:ADAUSD",
    "resolution": "15",
    "from": from_unix_timestamp,
    "to": to_unix_timestamp,
    "token": FINN_API_TOKEN

}

response = requests.get(crypto_price_url, crypto_params)
json_data = response.json()
closing_price = json_data['c']

client.chat_postMessage(channel='#crypto_alerts', text=f" Around {datetime_object} -> {crypto_params['symbol']} price: {closing_price}")


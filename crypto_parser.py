import urllib.request
import json
import time
import requests
from db_functions import add_coin_cost, add_coin_name
from config import crypto_tickets
from db_driver import Crypto_coin_cost

# crypto_tickets = {Bitcoin:'BTCUSD', Dash:'dashusd', Etherium:'ethusd',
#                   IOTA:'iotusd', Litecoin:'ltcusd', Monero:'xmrusd',Ripple:'xrpusd',Zcash:'zecusd'}



def get_data_from_bcs(ticket):
    start_date = int(time.mktime(time.localtime()))
    stop_date = start_date - (3600 * 2)
    bcs_url = 'https://api.bcs.ru/udfdatafeed/v1/history?symbol={0}&resolution=30&from={1}&to={2}'.format(ticket, str(start_date), str(stop_date))
    print(bcs_url)
    raw_data = requests.get(bcs_url).text
    return json.loads(raw_data).get('c'), json.loads(raw_data).get('t')


if __name__ == '__main__':
    while True:
        for coin in crypto_tickets.keys():
            cost, date = get_data_from_bcs(crypto_tickets.get(coin))
            add_coin_name(coin)
            add_coin_cost(coin, date, cost)
        time.sleep(1800)

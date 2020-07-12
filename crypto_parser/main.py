import urllib.request
import json
import time
import requests
from db_functions import add_coin_cost
from db_driver import Bitcoin
from db_driver import Dash
from db_driver import Etherium
from db_driver import IOTA
from db_driver import Litecoin
from db_driver import Monero
from db_driver import Ripple
from db_driver import Zcash


crypto_tickets = {Bitcoin:'BTCUSD', Dash:'dashusd', Etherium:'ethusd',
                  IOTA:'iotusd', Litecoin:'ltcusd', Monero:'xmrusd',Ripple:'xrpusd',Zcash:'zecusd'}


def get_data_from_bcs(ticket):
    start_date = int(time.mktime(time.localtime()))
    stop_date = start_date - (3600 * 24)
    bcs_url = 'https://api.bcs.ru/udfdatafeed/v1/history?symbol=' + ticket + \
              '&resolution=60&from=' + str(start_date) + '&to=' + str(stop_date)
    print(bcs_url)
    raw_data = requests.get(bcs_url).text
    return json.loads(raw_data).get('c'), json.loads(raw_data).get('t')


for coin in crypto_tickets.keys():
    cost, date = get_data_from_bcs(crypto_tickets.get(coin))
    add_coin_cost(coin, date, cost)

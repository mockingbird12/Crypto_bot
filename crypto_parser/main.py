import urllib.request
import json
import time
import requests
from db_functions import write_coin_cost
from db_functions import Bitcoin_work as Bitcoin
from db_functions import Dash_work as Dash
from db_functions import Etherium_work as Etherium
from db_functions import Iota_work as IOTA
from db_functions import Litecoin_work as Litecoin
from db_functions import Monero_work as Monero
from db_functions import Ripple_work as Ripple
from db_functions import Zcash_work as Zcash


crypto_tickets = {Bitcoin:'BTCUSD', Dash:'dashusd', Etherium:'ethusd',
                  IOTA:'iotusd', Litecoin:'ltcusd', Monero:'xmrusd',Ripple:'xrpusd',Zcash:'zecusd'}


def get_data_from_bcs(ticket):
    start_date = int(time.mktime(time.localtime()))
    stop_date = start_date - (3600 * 24)
    bcs_url = 'https://api.bcs.ru/udfdatafeed/v1/history?symbol=' + ticket + \
              '&resolution=60&from=' + str(start_date) + '&to=' + str(stop_date)
    print(bcs_url)
    raw_data = requests.get(bcs_url).text
    return json.loads(raw_data).get('c')[-1], json.loads(raw_data).get('t')[-1]

class Crypto_parser():

    def __init__(self, name, ticket, db_crypt):
        self.name = name
        self.ticket = ticket
        self.db_crypt = db_crypt
        self.quotes_data = None


    def print_data(self):
        cost = self.quotes_data.get('c')[-1]
        print(cost)



for coin in crypto_tickets.keys():
    crypto_coin = coin()
    data, date = get_data_from_bcs(crypto_tickets.get(coin))
    crypto_coin.write_data(data, date)
   # crypta = Crypto_parser(i[0], i[1])
   # crypta.get_data_from_bcs()
   # crypta.write_to_database()
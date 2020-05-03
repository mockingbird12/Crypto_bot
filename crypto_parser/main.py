import urllib.request
import json
import time
import requests
from db_functions import write_coin_cost


crypto_tickets = {'Bitcoin':'BTCUSD', 'Dash':'dashusd', 'Etherium Classic':'etcusd', 'Etherium':'ethusd',
                  'IOTA':'iotusd', 'LITECOIN':'ltcusd', 'MONERO':'xmrusd','RIPPLE':'xrpusd','ZCASH':'zecusd'}

class Crypto_parser():

    def __init__(self, name, ticket):
        self.name = name
        self.ticket = ticket
        self.quotes_data = None

    def get_data_from_bcs(self):
        start_date = int(time.mktime(time.localtime()))
        stop_date = start_date - (3600 * 24)
        bcs_url = 'https://api.bcs.ru/udfdatafeed/v1/history?symbol=' + self.ticket + \
                 '&resolution=60&from=' + str(start_date) + '&to=' + str(stop_date)
        print (bcs_url)
        raw_data = requests.get(bcs_url).text
        self.quotes_data = json.loads(raw_data)

    def print_data(self):
        cost = self.quotes_data.get('c')[-1]
        print(cost)

    def write_to_database(self):
        cost = self.quotes_data.get('c')[-1]
        print(cost)
        # if write_coin_cost(coin_name=self.name, ticket=self.ticket, cost=None):
        #     print('Write succesfull')
        # else:
        #     print('Error writing')


for i in crypto_tickets:
    crypta = Crypto_parser(i)
    crypta.get_data_from_bcs()
    crypta.print_data()
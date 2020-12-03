from telebot import types
from db_functions import get_all_coin_id, get_coin_name, get_coin_cost
from config import crypto_tickets


def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('My portfolio'), types.KeyboardButton('Buy coin'),
             types.KeyboardButton('Watch course'), types.KeyboardButton('Sell coin')]
    for item in items:
        markup.add(item)
    return markup


def choose_coin():
    coin_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = []
    # for coin in get_all_coin_id():
    #     buttons.append()
    buttons = [types.KeyboardButton('{0} - {1}'.format(get_coin_name(coin.id), get_coin_cost(coin.id))) for coin in get_all_coin_id()]
    for button in buttons:
        coin_markup.add(button)
    return coin_markup

    # coin_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # buttons = [types.KeyboardButton(item) for item in crypto_tickets.keys()]
    # for button in buttons:
    #     coin_markup.add(button)
    # return coin_markup


def hider():
    return types.ReplyKeyboardRemove()
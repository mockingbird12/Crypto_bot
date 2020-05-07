from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('My portfolio'), types.KeyboardButton('Buy coin'),
             types.KeyboardButton('Watch course'), types.KeyboardButton('Sell coin')]
    for item in items:
        markup.add(item)
    return markup

def choose_coin():
    coin_list = ['Bitcoin', 'Dash', 'Etherium Classic', 'Etherium', 'IOTA', 'LITECOIN', 'MONERO', 'RIPPLE', 'ZCASH']
    coin_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = [types.KeyboardButton(item) for item in coin_list]
    for button in buttons:
        coin_markup.add(button)
    return coin_markup
# Наверно эта клавиатура не нужна
# def login():
#     markup = types.InlineKeyboardMarkup()
#     items = [types.InlineKeyboardButton('Новый пользователь', callback_data='new_user'),
#              types.InlineKeyboardButton('Старый пользователь', callback_data='old_user')]
#     for item in items:
#         markup.add(item)
#     return markup

def hider():
    return types.ReplyKeyboardRemove()
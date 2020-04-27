from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton('Просмотр потрфеля')
    items = [types.KeyboardButton('Просмотр потрфеля'), types.KeyboardButton('Купить монету'),
             types.KeyboardButton('Курс криптовалют'), types.KeyboardButton('Продать монету')]
    for item in items:
        markup.add(item)
    return markup

def login():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = types.InlineKeyboardMarkup()
    items = [types.InlineKeyboardButton('Новый пользователь', callback_data='new_user'),
             types.InlineKeyboardButton('Старый пользователь', callback_data='old_user')]
    for item in items:
        markup.add(item)
    return markup

def hider():
    return types.ReplyKeyboardRemove()
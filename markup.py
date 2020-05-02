from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('Просмотр потрфеля'), types.KeyboardButton('Buy'),
             types.KeyboardButton('Crypto'), types.KeyboardButton('Продать монету')]
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
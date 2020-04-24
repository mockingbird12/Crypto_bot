import telebot
from telebot import apihelper
import conversation
import config
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['coin_count'])
def coin_count(message):
    bot.send_message(message.chat.id, conversation.coin_count)

@bot.message_handler(commands=['chose_coin'])
def chouse_coin(message):
    bot.send_message(message.chat.id, conversation.chouse_coin)

@bot.message_handler(commands=['sell_coin'])
def sell_coin(message):
    bot.send_message(message.chat.id, conversation.sell_coin)


@bot.message_handler(commands=['buy_coin'])
def buy_coin(message):
    bot.send_message(message.chat.id, conversation.buy_coin)


@bot.message_handler(commands=['watch_portfolio'])
def watch_portfolio(message):
    bot.send_message(message.chat.id, conversation.watch_portfolio)


@bot.message_handler(commands=['watch_course'])
def watch_course(message):
    bot.send_message(message.chat.id, conversation.watch_course)

@bot.message_handler(commands=['loged_user'])
def logged_user(message):
    bot.send_message(message.chat.id, conversation.hello_logged)

@bot.message_handler(commands=['unloged_user'])
def unloged_user(message):
    bot.send_message(message.chat.id, conversation.hello_unlogged)

@bot.message_handler(commands=['start'])
def main_start(message):
    bot.send_message(message.chat.id, conversation.hello_message)


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5h://192.168.77.130:9100'}
    print('Start Bot')
    bot.polling()
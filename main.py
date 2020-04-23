import telebot
from telebot import apihelper
import config

bot = telebot.TeleBot(config.token)


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5://192.168.77.130:9050'}
    print('Start Bot')
    bot.polling()
import telebot
from telebot import apihelper
import config
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def main_start(message):
    hello_message = 'Hello'
    bot.send_message(message.chat.id, hello_message)


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5h://192.168.77.130:9100'}
    print('Start Bot')
    while True:
        try:
            bot.polling()
        except Exception:
            print('Error')
            time.sleep(5)
import telebot
from telebot import apihelper
import conversation
import config
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands='logged_user')
def logged_user(message):
    bot.send_message(message.chat.id, conversation.hello_logged)

@bot.message_handler(commands='unloged_user')
def unloged_user(message):
    bot.send_message(message.chat.id, conversation.hello_unlogged)

@bot.message_handler(content_types=['text'])
def main_start(message):
    bot.send_message(message.chat.id, conversation.hello_message)


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5h://192.168.77.130:9100'}
    print('Start Bot')
    while True:
        try:
            bot.polling()
        except Exception:
            print('Error')
            time.sleep(5)
import telebot
import conversation
import config
import markup
from db_functions import add_user, is_exsist


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['coin_count'])
def coin_count(message):
    bot.send_message(message.chat.id, conversation.coin_count)

@bot.message_handler(commands=['chose_coin'])
def chouse_coin(message):
    bot.send_message(message.chat.id, conversation.chouse_coin)

@bot.message_handler(func=lambda message: message.text == 'My portfolio')
def watch_portfolio(message):
    bot.send_message(message.chat.id, conversation.watch_portfolio)

@bot.message_handler(func=lambda message: message.text == 'Sell coin')
def sell_coin(message):
    bot.send_message(message.chat.id, conversation.sell_coin)

@bot.message_handler(func=lambda message: message.text == 'Buy coin')
def buy_coin(message):
    bot.send_message(message.chat.id, conversation.buy_coin)

@bot.message_handler(func=lambda message: message.text == 'Watch course')
def watch_course(message):
    bot.send_message(message.chat.id, conversation.watch_course)

@bot.message_handler(commands=['old_user'])
def logged_user(message):
    bot.send_message(message.chat.id, conversation.hello_logged)

@bot.message_handler(commands=['new_user'])
def unloged_user(message):
    bot.send_message(message.chat.id, conversation.hello_unlogged)

# @bot.callback_query_handler(func=lambda call:True)
# def main_menu(call):
#     if call.data == 'new_user':
#         bot.send_message(call.message.chat.id, conversation.hello_unlogged, reply_markup=markup.main_menu())
#     if call.data == 'old_user':
#         bot.send_message(call.message.chat.id, conversation.hello_logged, reply_markup=markup.main_menu())


@bot.message_handler(commands=['help','start'])
def main_start(message):
    print(message.from_user)
    if not is_exsist(user_id=message.from_user.id):
        add_user(message.from_user.first_name, message.from_user.username, message.from_user.id)
        bot.send_message(message.chat.id, conversation.welcome_message%message.from_user.username, reply_markup=markup.login())
    else:
        bot.send_message(message.chat.id, conversation.welcome_message%message.from_user.username, reply_markup=markup.main_menu())



# @bot.message_handler(content_types=['text'])
# def text_function(message):
#     bot.send_message(message.chat.id, 'Ответ: {0}'.format(message.text), reply_markup=markup.hider())


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5h://192.168.77.130:9100'}
    print('Start Bot')
    bot.polling()
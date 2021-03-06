import telebot
import conversation
import config
import markup
import cherrypy
from db_functions import add_user, is_exsist, get_cash, change_user_state, get_user_state, clear_user_state
from db_functions import setup_user_operation, get_all_coin_id, get_coin_cost, get_coin_name, get_all_user_coin
from db_functions import get_coin_id, get_coin_count
from db_functions import buy_sell_coin, clear_user_operation


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['coin_count'])
def coin_count(message):
    bot.send_message(message.chat.id, conversation.coin_count)


@bot.message_handler(commands=['chose_coin'])
def chouse_coin(message):
    bot.send_message(message.chat.id, conversation.chouse_coin)


@bot.message_handler(func=lambda message: message.text == 'My portfolio')
def watch_portfolio(message):
    user_cash = get_cash(message.chat.id)
    bot.send_message(message.chat.id, conversation.watch_portfolio.format(user_cash))
    res = ''
    crypto_cash = 0
    for coin_id in get_all_user_coin(message.from_user.id):
        count = get_coin_count(coin_id, message.from_user.id)
        res += '{0} - {1} - \t{2}\n'.format(get_coin_name(coin_id), count , count * round(get_coin_cost(coin_id), 2))
        crypto_cash += count * get_coin_cost(coin_id)
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, conversation.crypto_cash.format(str(crypto_cash)))
    bot.send_message(message.chat.id, conversation.total_cash.format(str(user_cash + crypto_cash)))


@bot.message_handler(func=lambda message: message.text == 'Sell coin')
def sell_coin(message):
    change_user_state(message.from_user.id, config.state_sel_coin)
    bot.send_message(message.chat.id, conversation.sell_coin, reply_markup=markup.choose_coin())


@bot.message_handler(func=lambda message: message.text == 'Buy coin')
def choose_coin(message):
    change_user_state(message.from_user.id, config.state_buy_coin )
    # Изменить состояние пользователя
    bot.send_message(message.chat.id, conversation.buy_coin, reply_markup=markup.choose_coin())


@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == config.state_buy_coin or
                                          get_user_state(message.from_user.id) == config.state_sel_coin)
def choose_count(message):
    coin = message.text.split()[0]
    if not get_coin_id(coin):
        bot.send_message(message.from_user.id, conversation.wrong_coin)
        clear_user_state(message.from_user.id)
        return None
    setup_user_operation(message.from_user.id, get_coin_id(coin), get_user_state(message.from_user.id))
    change_user_state(message.from_user.id, config.choose_coin)
    bot.send_message(message.chat.id, 'Монета: {0} стоимость {1}'.format(coin, get_coin_cost(get_coin_id(coin))))
    bot.send_message(message.chat.id, conversation.coin_count)


@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == config.choose_coin)
def make_deal(message):
    print(get_user_state(message.from_user.id))
    try:
        coin_count = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, conversation.wrong_count)
        return None
    if buy_sell_coin(message.from_user.id, coin_count=coin_count):
        bot.send_message(message.chat.id, conversation.buy_deal.format(str(coin_count)),
                         reply_markup=markup.main_menu())
        clear_user_state(message.from_user.id)
        clear_user_operation(message.from_user.id)
    else:
        bot.send_message(message.chat.id, conversation.error_deal)


@bot.message_handler(func=lambda message: message.text == 'Watch course')
def watch_course(message):
    bot.send_message(message.chat.id, conversation.watch_course)
    coins = get_all_coin_id()
    cost_info = ''
    for coin in coins:
        cost_info = cost_info + '{0} - {1}\n'.format(get_coin_name(coin.id), get_coin_cost(coin.id))
    bot.send_message(message.chat.id, cost_info)


@bot.message_handler(commands=['help','start'])
def main_start(message):
    print(message.from_user)
    if not is_exsist(user_id=message.from_user.id):
        add_user(message.from_user.first_name, message.from_user.username, message.from_user.id)
    bot.send_message(message.chat.id, conversation.welcome_message%message.from_user.username, reply_markup=markup.main_menu())


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and \
                               cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


if __name__ == '__main__':
    print('Start Bot')
    if config.working_mode == 'host':
        bot.remove_webhook()
        bot.polling()
    if config.working_mode == 'server':
        bot.remove_webhook()
        bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                        certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
        cherrypy.config.update({
            'server.socket_host': config.WEBHOOK_LISTEN,
            'server.socket_port': config.WEBHOOK_PORT,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
            'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
        })
        cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/':{}})

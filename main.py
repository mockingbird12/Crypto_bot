import telebot
import conversation
import config
import markup
import cherrypy
from db_functions import add_user, is_exsist, get_cash, change_user_state, get_user_state, clear_user_state
from db_functions import setup_user_operation
from db_functions import get_coin_id
from db_functions import crypto_value


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
    print('Запрос к базе о портфеле')

@bot.message_handler(func=lambda message: message.text == 'Sell coin')
def sell_coin(message):
    change_user_state(message.from_user.id, config.state_sel_coin)
    bot.send_message(message.chat.id, conversation.sell_coin, reply_markup=markup.choose_coin())

@bot.message_handler(func=lambda message: message.text == 'Buy coin')
def choose_coin(message):
    # TODO: Нужно что-то придумать со слежением состояния пользователя
    change_user_state(message.from_user.id, config.state_buy_coin )
    # Изменить состояние пользователя
    bot.send_message(message.chat.id, conversation.buy_coin, reply_markup=markup.choose_coin())

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == config.state_buy_coin or
                                          get_user_state(message.from_user.id) == config.state_sel_coin)
def choose_count(message):
    coin = message.text
    setup_user_operation(message.from_user.id, get_coin_id(coin), get_user_state(message.from_user.id))
    change_user_state(message.from_user.id, config.choose_coin)
    bot.send_message(message.chat.id, 'Монета: {0}'.format(coin))
    bot.send_message(message.chat.id, conversation.coin_count)

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == config.choose_coin)
def make_deal(message):
    print(get_user_state(message.from_user.id))
    coin_count = int(message.text)
    bot.send_message(message.chat.id, conversation.buy_deal.format(str(coin_count)), reply_markup=markup.main_menu())
    clear_user_state(message.from_user.id)


@bot.message_handler(func=lambda message: message.text == 'Watch course')
def watch_course(message):
    bot.send_message(message.chat.id, conversation.watch_course)

@bot.message_handler(commands=['old_user'])
def logged_user(message):
    bot.send_message(message.chat.id, conversation.hello_logged)

@bot.message_handler(commands=['new_user'])
def unloged_user(message):
    bot.send_message(message.chat.id, conversation.hello_unlogged)


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

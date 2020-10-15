token = '1238244677:AAE0CQraYtpWvooXUVbgfp9tO1l_bartmx0'

WEBHOOK_HOST = '80.87.193.164'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = 'https://{0}:{1}'.format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{0}/'.format(token)

db_user = 'crypto_user'
db_passwd = '111111'
#db_host = '192.168.77.130' # localhost
db_host = '172.17.0.1'   # docker interface
db_name = 'crypto_bot'

# working_mode = 'host'
working_mode = 'server'

state_buy_coin = 141
state_sel_coin = 142
choose_coin = 143
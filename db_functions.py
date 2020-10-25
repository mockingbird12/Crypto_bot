from sqlalchemy import desc
from db_driver import session
from db_driver import Users
from db_driver import User_cash
from db_driver import User_Status
from db_driver import User_operation
from db_driver import User_portfolio
from db_driver import Crypto_coin_cost, Crypto_coin_name
import config


def add_coin_name(name):
    coin_name = session.query(Crypto_coin_name).filter(Crypto_coin_name.name == name).first()
    if coin_name:
        print('Coin with this name exsist')
    else:
        coin_name = Crypto_coin_name()
        coin_name.name = name
        session.add(coin_name)
        session.commit()


def get_coin_name(coin_id):
    coin_name = session.query(Crypto_coin_name).filter(Crypto_coin_name.id == coin_id).first()
    if coin_name:
        return coin_name.name
    else:
        return None


def get_all_user_coin(user_id):
    coins_id = session.query(User_portfolio.crypto_id).filter(User_portfolio.user_id == user_id).all()
    return coins_id

def get_coin_course(coin):
    result = session.query(coin).last()
    if result:
        return result.cost
    else:
        return None


def add_coin_cost(coin_name, date, cost):
    coin_id = get_coin_id(coin_name)
    while date:
        one_date = date.pop(0)
        one_cost = cost.pop(0)
        result = session.query(Crypto_coin_cost).filter(Crypto_coin_cost.name == coin_id, Crypto_coin_cost.date == one_date).first()
        if not result:
            coin = Crypto_coin_cost()
            coin.name = get_coin_id(coin_name)
            coin.date = one_date
            coin.cost = one_cost
            session.add(coin)
        else:
            print('Date {0} in coin {1} already exsist in table'.format(one_date, coin_name))
    session.commit()


def get_coin_cost(coin_id):
    result = session.query(Crypto_coin_cost).filter(Crypto_coin_cost.name == coin_id).order_by(desc(Crypto_coin_cost.date)).first()
    if result:
        return result.cost
    else:
        return None


def is_exsist(**kwargs):
    """
    Функция для провекри существования каких-либо сущностей
    (пользователей и т.д)
    :param kwargs:
    :return:
    """
    if len(kwargs) > 1:
        raise SystemError('Too many args')
    if 'user_id' in kwargs.keys():
        if session.query(Users).filter(Users.user_id == kwargs.get('user_id')).first():
            return True
        else:
            return False
    if 'coin_id' in kwargs.keys():
        print('Find coin')
        return True


def get_coin_id(coin_name):
    coin = session.query(Crypto_coin_name).filter(Crypto_coin_name.name == coin_name).first()
    if coin:
        return coin.id
    else:
        return None

def get_coin_count(coin_id, user_id):
    user_coins = session.query(User_portfolio).filter(User_portfolio.crypto_id == coin_id, User_portfolio.user_id == user_id).first()
    if user_coins:
        return user_coins.count
    else:
        return None

def get_all_coin_id():
    coins = session.query(Crypto_coin_name).all()
    return coins


def crypto_value(coin_name, coin_count):
    coin = session.query(Crypto_coin_cost).filter(Crypto_coin_cost.name == coin_name).first()
    return coin.cost * coin_count


def __add_user_cash(user_id, cash=None):
    user_cash = User_cash(user_id, cash)
    session.add(user_cash)
    session.commit()


def get_cash(user_id=None):
    if user_id == None:
        raise Exception('user id should\'nt be empty')
    user_cash = session.query(User_cash).filter(User_cash.id == user_id).first()
    return user_cash.cash


def change_user_state(user_id=None, state=None):
    if session.query(User_Status).filter(User_Status.user_id == user_id).first():
        user = session.query(User_Status).filter(User_Status.user_id == user_id).first()
        session.delete(user)
    user_state = User_Status(user_id, state)
    session.add(user_state)
    session.commit()


def buy_sell_coin(user_id=None, coin_count=None):
    user_cash = get_cash(user_id)
    coin_id, operation = get_user_operation(user_id)
    user_coins = get_coin_count(coin_id, user_id)
    total_cost = get_coin_cost(coin_id) * coin_count
    if operation == config.state_buy_coin:
        if user_cash > total_cost:
            print('Buy coin')
            user_portfolio = User_portfolio()
            user_portfolio.user_id = user_id
            user_portfolio.crypto_id = coin_id
            if user_coins:
                user_portfolio.count = user_coins + coin_count
            else:
                user_portfolio.count = coin_count
            session.add(user_portfolio)
            new_user_cash = session.query(User_cash).filter(User_cash.id == user_id).first()
            new_user_cash.cash -= total_cost
            session.commit()
            return True
        else:
            print('Not enough cash')
            return False
    if operation == config.state_sel_coin:
        if user_coins:
            if coin_count < user_coins:
                print('Sell coin')
                user_portfolio = User_portfolio()
                user_portfolio.user_id = user_id
                user_portfolio.crypto_id = coin_id
                user_portfolio.count = user_coins - coin_count
                session.add(user_portfolio)
                new_user_cash = User_cash(user_id, user_cash + total_cost)
                session.add(new_user_cash)
                session.commit()
            else:
                print('Not enough coins')
                return False
        else:
            print('No coin {0} in user portfolio'.format(get_coin_name(coin_id)))
            return False
    else:
        print('No such operation {0}'.format(operation))
        return False


def clear_user_state(user_id=None):
    if session.query(User_Status).filter(User_Status.user_id == user_id).first():
        user = session.query(User_Status).filter(User_Status.user_id == user_id).first()
        session.delete(user)
        session.commit()


def setup_user_operation(user_id=None, coin_id=None, operation=None):
    """Записывает в базу какое действие выполнил пользователь"""
    user_operation = session.query(User_operation).filter(User_operation.user_id == user_id).first()
    if not user_operation:
        user_operation = User_operation(user_id, coin_id, operation)
        session.add(user_operation)
    else:
        user_operation.coin_id = coin_id
        user_operation.operation = operation
        session.add(user_operation)
    session.commit()

def clear_user_operation(user_id):
    user_operation = session.query(User_operation).filter(User_operation.user_id == user_id).first()
    if user_operation:
        session.delete(user_operation)
        session.commit()
    else:
        print('No user operation for user {0}'.format(user_id))
        return True


def get_user_operation(user_id=None):
    """Возвращает user_oeration из которого можно вязть coin_id и user_operation"""
    if user_id:
        user_operation = session.query(User_operation).filter(User_operation.user_id == user_id).first()
        return user_operation.coin_id, int(user_operation.operation)
    else:
        print('Params are empty')
        return None

def get_user_state(user_id):
    state = session.query(User_Status).filter(User_Status.user_id == user_id).first()
    if state != None:
        return state.state
    else:
        return None


def add_user(first_name, username, user_id):
    user = Users(first_name, username, user_id)
    user_cash = User_cash(user_id, 1000)
    session.add(user)
    session.commit()
    session.add(user_cash)
    session.commit()


if __name__ == "__main__":
    for coin in get_all_coin_id():
        print(get_coin_cost(coin.id))
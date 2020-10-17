from db_driver import session
from db_driver import Users
from db_driver import User_cash
from db_driver import User_Status
from db_driver import User_operation
from db_driver import Crypto_coin, Crypto_coin_name
import datetime

def add_coin_name(name):
    coin_name = session.query(Crypto_coin_name).filter(Crypto_coin_name.name == name).first()
    if coin_name:
        print('Coin with this name exsist')
    else:
        coin_name = Crypto_coin_name()
        coin_name.name = name
        session.add(coin_name)
        session.commit()

def get_coin_course(coin):
    result = session.query(coin).last()
    if result:
        return result.cost
    else:
        return None

def add_coin_cost(coin_name, date, cost):
    coin = Crypto_coin()
    coin.name = coin_name
    coin.date = date[-1]
    coin.cost = cost[-1]
    session.add(coin)
    session.commit()

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
    coin = session.query(Crypto_coin).filter(Crypto_coin.name == coin_name).first()
    if coin:
        return coin.id
    else:
        return None


def crypto_value(coin_name, coin_count):
    coin = session.query(Crypto_coin).filter(Crypto_coin.name == coin_name).first()
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

def clear_user_state(user_id=None):
    if session.query(User_Status).filter(User_Status.user_id == user_id).first():
        user = session.query(User_Status).filter(User_Status.user_id == user_id).first()
        session.delete(user)
        session.commit()

def setup_user_operation(user_id=None, coin_id=None, operation=None):
    user_operation = session.query(User_operation).filter(User_operation.user_id == user_id).first()
    if not user_operation:
        user_operation = User_operation(user_id, coin_id, operation)
        session.add(user_operation)
    else:
        user_operation.coin_id = coin_id
        user_operation.operation = operation
        session.add(user_operation)
    session.commit()

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
    change_user_state(279305709, None)
    setup_user_operation(279305709, 5,'buy')
from db_driver import session
from db_driver import Users
from db_driver import Crypro_coin
from db_driver import User_cash

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

def write_coin_cost(**kwargs):
    # TODO: обновлять информацию в базе(удалять старое значение и записывать новое)
    coin_name = kwargs.get('coin_name')
    ticket = kwargs.get('ticket')
    cost = kwargs.get('cost')
    crypto_coin = Crypro_coin(coin_name, ticket, cost)
    session.add(crypto_coin)
    session.commit()
    return True

def __add_user_cash(user_id, cash=None):
    user_cash = User_cash(user_id, cash)
    session.add(user_cash)
    session.commit()

def get_cash(user_id=None):
    if user_id == None:
        raise Exception('user id should\'nt be empty')
    user_cash = session.query(User_cash).filter(User_cash.id == user_id).first()
    return user_cash.cash

def add_user(first_name, username, user_id):
    user = Users(first_name, username, user_id)
    user_cash = User_cash(user_id, 1000)
    session.add(user)
    session.commit()
    session.add(user_cash)
    session.commit()


if __name__ == "__main__":
    print(get_cash(user_id=11122))
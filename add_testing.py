from db_driver import session
from db_driver import Users
from db_driver import Crypro_coin


def addUser(tel, name):
    user = Users(first_name=tel, username=name)
    session.add(user)
    session.commit()

def delUser(tel):
    user = session.querry(Users).filter(Users.first_name == tel).one()
    session.delete(user)
    session.commit()


if __name__ == '__main__':
    addUser('+719828429', 'user1')
    # addCryptoCoin('BitcoinT', 'BTN', '100')
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


def addCryptoCoin(coin_name, coin_abberv, coin_cost):
    coin = Crypro_coin(name=coin_name, abberv=coin_abberv, cost=coin_cost)
    session.add(coin)
    session.commit()


def delCryptoCoin(coin_name):
    coin = session.querry(Crypro_coin).filter(Crypro_coin.name == coin_name).one()
    session.delete(coin)
    session.commit()


if __name__ == '__main__':
    addUser('+719828429', 'user1')
    addCryptoCoin('BitcoinT', 'BTN', '100')
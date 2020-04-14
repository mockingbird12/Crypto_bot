import config
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Sequence
from sqlalchemy import Text
from sqlalchemy import ForeignKey

user = config.db_user
passwd = config.db_passwd
host = config.db_host
dbname = config.db_name

Base = declarative_base()
engine = create_engine("postgresql://{0}:{1}@{2}/{3}".format(user, passwd, host, dbname))

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    tel_number = Column(Text)
    login = Column(Text)


class Crypro_coin(Base):
    __tablename__ = 'crypto_coin'
    id = Column(Integer, Sequence('crypto_id_seq'), primary_key=True)
    name = Column(Text)
    abberv = Column(Text)
    cost = Column(Float)

class User_cash(Base):
    __tablename__ = 'user_cash'
    id = Column(Integer, Sequence('cash_seq'), primary_key=True)
    cash = Column(Float)

class User_portfolio(Base):
    __tablename__ = 'user_portfolio'
    id = Column(Integer, Sequence('user_portfolio_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crypto_id = Column(Integer, ForeignKey('crypto_coin.id'))


if __name__ == '__main__':
    Base.metadata.create_all(engine)


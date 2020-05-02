from db_driver import session
from db_driver import Users

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


def add_user(first_name, username, user_id):
    # TODO: разобраться с UnicodeEncodeError: 'ascii' codec can't encode...
    user = Users(first_name, username, user_id)
    session.add(user)
    session.commit()


if __name__ == "__main__":
    if is_exsist(user_id=2819374):
        print('yes')
    else: print('No')
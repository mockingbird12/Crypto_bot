from db_driver import session
from db_driver import Users

def check_exsist(data):

    pass

def add_user(first_name, username, user_id):
    # TODO: разобраться с UnicodeEncodeError: 'ascii' codec can't encode...
    if not session.query(Users).filter(Users.user_id == user_id).first():
        user = Users(first_name, username, user_id)
        session.add(user)
        session.commit()
    else:
        print('{0} already exsist'.format(user_id))
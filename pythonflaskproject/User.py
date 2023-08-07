import flask_login

import shelve


class User(flask_login.UserMixin):
    count_id = 0

    def __init__(self, first_name, last_name, password, email, birth_date, admin=False):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__password = password
        self.__email = email
        self.__birth_date = birth_date
        self.__admin = admin

    def get_id(self):
        return str(self.__email)

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__first_name + ' ' + self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_birth_date(self, date_format="%d/%m/%Y"):
        return self.__birth_date.strftime(date_format)

    def get_admin(self):
        return self.__admin

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_birth_date(self, birth_date):
        self.__birth_date = birth_date

    def set_admin(self, admin):
        self.__admin = admin

    @staticmethod
    def get_all_users():
        users_dict = {}

        db = shelve.open('storage.db', 'c')
        try:
            users_dict = db['Users']
        except NameError:
            print("Error in retrieving Users from storage.db.")

        return [user for key, user in users_dict.items()]

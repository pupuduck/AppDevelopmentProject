from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, id):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__id = id
        self.__birthday = None
        self.__phone = None
        self.__location = None

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_id(self, id):
        self.__id = id

    def set_birthdate(self, birthday):
        self.__birthday = birthday

    def set_phone(self, phone):
        self.__phone = phone

    def set_location(self, location):
        self.__location = location

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_id(self):
        return str(self.__id)

    def get_birthday(self):
        return self.__birthday

    def get_phone(self):
        return self.__phone

    def get_location(self):
        return self.__location

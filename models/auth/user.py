from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, id, role, status):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__id = id
        self.__birthday = None
        self.__phone = None
        self.__location = None
        self.__role = role
        self.__image = None
        self.__status = status
        self.__payment_methods = []
        self.__cart = []
        self.__transaction_history = []

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_id(self, id):
        self.__id = id

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def set_phone(self, phone):
        self.__phone = phone

    def set_location(self, location):
        self.__location = location

    def set_role(self, role):
        self.__role = role

    def set_image(self, image):
        self.__image = image

    def set_status(self, status):
        self.__status = status

    def set_payment_methods(self, payment_method):
        self.__payment_methods = payment_method

    def set_cart(self, cart):
        self.__cart = cart

    def set_transaction_history(self, transaction_history):
        self.__transaction_history = transaction_history

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

    def get_role(self):
        return self.__role

    def get_image(self):
        return self.__image

    def get_status(self):
        return self.__status

    def get_payment_methods(self):
        return self.__payment_methods

    def get_cart(self):
        return self.__cart

    def get_transaction_history(self):
        return self.__transaction_history

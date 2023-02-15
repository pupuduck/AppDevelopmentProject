from flask_login import UserMixin
import jwt
from config import app
import shelve


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

    def get_reset_token(self):
        payload = {'user_id': self.__id}
        token = jwt.encode(payload=payload, key=app.config['SECRET_KEY'])

        return token

    @staticmethod
    def verify_reset_token(token):
        users_dict = {}
        # try:
        user_id = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']

        db = shelve.open('DB/Customer/customer')
        if 'customer' in db:
            users_dict = db['customer']
        else:
            db['customer'] = users_dict
        db.close()
        # except IOError:
        #     print("IOError")
        # except Exception as ex:
        #     print(f"Exception Error as {ex} 2")
        #     return None
        return users_dict.get(str(user_id))


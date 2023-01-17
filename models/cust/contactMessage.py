# User class
class Message:
    message_id = 0

    # initializer method
    def __init__(self, name, email, subject, message):
        Message.message_id += 1
        self.__message_id = Message.message_id
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__message = message

    # accessor methods
    def get_message_id(self):
        return self.__message_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message

    # mutator methods
    def set_message_id(self, user_id):
        self.__message_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

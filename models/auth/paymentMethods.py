class paymentMethods:
    def __init__(self, card_id, full_name, number, cvv, expiry_date):
        self.__card_id = card_id
        self.__full_name = full_name
        self.__number = number
        self.__cvv = cvv
        self.__expiry_date = expiry_date

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_number(self, number):
        self.__number = number

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_card_id(self, card_id):
        self.__card_id = card_id

    def get_full_name(self):
        return self.__full_name

    def get_number(self):
        return self.__number

    def get_cvv(self):
        return self.__cvv

    def get_expiry_date(self):
        return self.__expiry_date

    def get_card_id(self):
        return self.__card_id

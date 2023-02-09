class paymentMethods:
    def __init__(self, card_id, full_name, number, cvv, expiry_date, street_address, unit_number, country, postal_code):
        self.__card_id = card_id
        self.__full_name = full_name
        self.__number = number
        self.__cvv = cvv
        self.__expiry_date = expiry_date
        self.__street_address = street_address
        self.__unit_number = unit_number
        self.__country = country
        self.__postal_code = postal_code

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

    def set_street_address(self, street_address):
        self.__street_address = street_address

    def set_unit_number(self, unit_number):
        self.__unit_number = unit_number

    def set_country(self, country):
        self.__country = country

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

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

    def get_street_address(self):
        return self.__street_address

    def get_unit_number(self):
        return self.__unit_number

    def get_country(self):
        return self.__country

    def get_postal_code(self):
        return self.__postal_code



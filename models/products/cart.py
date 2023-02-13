class cartItems:
    def __init__(self, product, quantity, price, item_id, cart_id):
        self.__product = product
        self.__quantity = quantity
        self.__price = price
        self.__item_id = item_id
        self.__cart_id = cart_id

    def set_product(self, product):
        self.__product = product

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, price):
        self.__price = price

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def set_cart_id(self, cart_id):
        self.__cart_id = cart_id

    def get_product(self):
        return self.__product

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def get_item_id(self):
        return self.__item_id

    def get_cart_id(self):
        return self.__cart_id

    def get_total_item_price(self):
        return self.__quantity * self.__price

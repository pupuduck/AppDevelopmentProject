class Product:

    # initializer method
    def __init__(self, name, rating, description, price, image, id):
        self.__product_id = id
        self.__name = name
        self.__rating = rating
        self.__description = description
        self.__price = price
        self.__image = image

    # accessor methods
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_rating(self):
        return self.__rating

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_image(self):
        return self.__image

    # mutator methods
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, name):
        self.__name = name

    def set_rating(self, rating):
        self.__rating = rating

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_image(self, image):
        self.__image = image

class transactionHistory:
    def __init__(self, transaction_id, date, amount):
        self.__transaction_id = transaction_id
        self.__date = date
        self.__amount = amount

    def set_transaction_id(self, transaction_id):
        self.__transaction_id = transaction_id

    def set_date(self, date):
        self.__date = date

    def set_amount(self, amount):
        self.__amount = amount

    def get_transaction_id(self):
        return self.__transaction_id

    def get_date(self):
        return self.__date

    def get_amount(self):
        return self.__amount

# Hiring class
class Resumes:

    # initializer method
    def __init__(self, first_name, last_name, email, sgorpr,citizenship, address,contactno,preferredjob,uploadfile, id):
        self.__resumes_id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__sgorpr = sgorpr
        self.__citizenship = citizenship
        self.__address = address
        self.__contactno = contactno
        self.__preferredjob = preferredjob
        self.__uploadfile = uploadfile
    # accessor methods

    def get_uploadfile(self):
        return self.__uploadfile

    def set_uploadfile(self,uploadfile):
        self.__uploadfile = uploadfile

    def get_resumes_id(self):
        return self.__resumes_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_sgorpr(self):
        return self.__sgorpr

    def get_citizenship(self):
        return self.__citizenship

    def get_contactno(self):
        return self.__contactno

    def get_preferredjob(self):
        return self.__preferredjob

    # mutator methods
    def set_resumes_id(self, resumes_id):
        self.__resumes_id = resumes_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_sgorpr(self, sgorpr):
        self.__sgorpr = sgorpr

    def set_citizenship(self,citizenship):
        self.__citizenship = citizenship

    def set_address(self, address):
        self.__address = address

    def set_contactno(self,contactno):
        self.__contactno = contactno

    def set_preferredjob(self,preferredjob):
        self.__preferredjob = preferredjob

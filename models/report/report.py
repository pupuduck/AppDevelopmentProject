# Report class
class Report:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name, gender, membership, remarks):
        Report.count_id += 1
        self.__report_id = Report.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__membership = membership
        self.__remarks = remarks

    # accessor methods
    def get_report_id(self):
        return self.__report_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    # mutator methods
    def set_report_id(self, report_id):
        self.__report_id = report_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, remarks):
        self.__remarks = remarks

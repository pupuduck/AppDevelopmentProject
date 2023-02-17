class JobPositions:

    def __init__(self, job_name, job_availability, job_responsibility, job_salary, job_image, id):
        self.__id = id
        self.__job_name = job_name
        self.__job_availability = job_availability
        self.__job_responsibility = job_responsibility
        self.__job_salary = job_salary
        self.__job_image = job_image

    # accessor methods
    def get_id(self):
        return self.__id

    def get_job_name(self):
        return self.__job_name

    def get_job_availability(self):
        return self.__job_availability

    def get_job_responsibility(self):
        return self.__job_responsibility

    def get_job_salary(self):
        return self.__job_salary

    def get_job_image(self):
        return self.__job_image

    # mutator methods

    def set_id(self, id):
        self.__id = id

    def set_job_name(self, job_name):
        self.__job_name = job_name

    def set_job_availability(self, job_availability):
        self.__job_availability = job_availability

    def set_job_responsibility(self, job_responsiblity):
        self.__job_responsibility = job_responsiblity

    def set_job_salary(self, job_salary):
        self.__job_salary = job_salary

    def set_job_image(self, job_image):
        self.__job_image = job_image

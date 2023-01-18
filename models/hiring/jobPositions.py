class JobPositions:
    count_id = 0

    def __init__(self, jobname, jobavailability, jobrequirements, jobresponsibility, jobsalary):
        JobPositions.count_id += 1
        self.__id = JobPositions.count_id
        self.__jobname = jobname
        self.__jobavailability = jobavailability
        self.__jobrequirements = jobrequirements
        self.__jobresponsibility = jobresponsibility
        self.__jobsalary = jobsalary

    # accessor methods
    def get_id(self):
        return self.__id

    def get_jobname(self):
        return self.__jobname

    def get_jobavailability(self):
        return self.__jobavailability

    def get_jobrequirements(self):
        return self.__jobrequirements

    def get_jobresponsibility(self):
        return self.__jobresponsibility

    def get_jobsalary(self):
        return self.__jobsalary

    # mutator methods

    def set_id(self, id):
        self.__id = id

    def set_jobname(self, jobname):
        self.__jobname = jobname

    def set_jobavailability(self, jobavailability):
        self.__jobavailability = jobavailability

    def set_jobrequirements(self, jobrequirements):
        self.__jobrequirements = jobrequirements

    def set_jobresponsibility(self,jobresponsiblity):
        self.__jobresponsibility = jobresponsiblity

    def set_jobsalary(self,jobsalary):
        self.__jobsalary = jobsalary

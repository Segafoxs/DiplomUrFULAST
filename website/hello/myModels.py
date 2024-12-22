from django.db import models

# Create your models here.

class Work_is_mymodel(models.Model):
    name: str
    dateStart: str
    timeStart: str
    dateEnd: str
    timeEnd: str

class Worker_is_mymodel(models.Model):

    def __init__(self, name, role):
        self.name = name
        self.role = role


class Manager_is_mymodel(Worker_is_mymodel):
    pass


class Executor_is_mymodel(Worker_is_mymodel):
    pass

class Director_is_mymodel(Worker_is_mymodel):
    pass


class Permit_is_mymodel():
    #номер наряда будет равен id в базе данных
    dateDelivery: str
    timeDelivery: str
    conditions: str


class ShiftManager_is_mymodel(Worker_is_mymodel):
   pass




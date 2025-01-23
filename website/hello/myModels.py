from django.db import models

# Create your models here.

class Master:
    name = None
    sign = None
    block_tx = None
    date_sign = None


class Director(Master):
    pass

class StateEngineer(Master):
    pass

class DailyManager(Master):
    pass

class Executor(Master):
    pass
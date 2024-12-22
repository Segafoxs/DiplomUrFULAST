from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from docxtpl import DocxTemplate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import hashlib
import os

from .myFunc import return_members

# Create your models here.

# class Employee(models.Model):
#     name = models.CharField(max_length=100)
#     postemploee = models.CharField(max_length=50)



class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    create_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TypeOfWork(models.Model):
    name = models.CharField(max_length=255, unique=True)

    create_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    
class Employee(AbstractBaseUser, PermissionsMixin):
    roles = {
        "DIRECTOR": "Начальник цеха",
        "MASTER": "Мастер",
        "WORKER": "Работник",
        "DAILYMANAGER": "Ежедневный менеджер",
        "STATIONENGINEER": "Инженер станции",
    }

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=255, choices=[(key, value) for key, value in roles.items()])
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    token = models.CharField(max_length=32, editable=False, unique=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    def generate_token(self):
        salt = os.urandom(16).hex()
        data = f"{self.email}{salt}{self.password}"
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):

        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)



class Permit(models.Model):
    statusPermit = {
        "approval": "На согласовании",
        "work": "В работе",
        "closed": "Закрыт",
    }

    number = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=255, choices=statusPermit, default=statusPermit["approval"])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Департамент")
    master_of_work = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="masterofwork")
    executor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="executorofwork")
    countWorker = models.CharField(max_length=255, null=False)
    # employ = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="employofwork")
    #master_signature = models.CharField(max_length=255)
    workers = ArrayField(
        ArrayField(
            models.CharField(max_length=100, blank=True),
            size=10,
        ),
        size=8,
    )
    work_description = models.CharField(max_length=255)
    start_of_work = models.DateTimeField(max_length=255)
    end_of_work = models.DateTimeField(max_length=255)
    signature_director = models.CharField(max_length=255, null=True, blank=True, verbose_name="Подпись директора")
    signature_dailymanager = models.CharField(max_length=255, null=True, blank=True, verbose_name="Подпись DailyManager")
    signature_stationengineer = models.CharField(max_length=255, null=True, blank=True, verbose_name="Подпись StationEngineer")
    safety = ArrayField(
          ArrayField(
             models.CharField(max_length=100, blank=True),
            size=10,
    ),
     size=8,
    )
    condition = models.CharField(max_length=255)

    director = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="time")
    #signature_from_director = models.CharField(max_length=255)

    daily_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="dailymanager")
    #signature_from_daily_manager = models.CharField(max_length=255)

    station_engineer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="statengineer")
    #signature_from_station_engineer = models.CharField(max_length=255)

    #create_at = models.DateTimeField()
    #updated_at = models.DateTimeField()

    # file_name = models.CharField(max_length=255)
    # file_path = models.CharField(max_length=255)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
    #     # if self.signature_from_daily_manager:
    #     #     hp = HistoryPermit(
    #     #
    #     #     )
    #     #     hp.save()
        super(Permit, self).save(*args)

    def __str__(self):
        return self.type_of_permit

    def to_docx(self, result):
        doc = DocxTemplate(r"C:\\Users\\Сергей\\Desktop\\Шаблоны для ЭНД\\test.docx")
        context = {
            'number': self.number,
            'department': self.department,
            'manager': self.master_of_work,
            'managerPost': self.master_of_work,
            'executor': self.executor,
            'executorPost': self.executor,
            'countMember': self.countWorker,
            'workers': result,
            'work': self.work_description,
            'dateStart': self.start_of_work,
            'timeStart': self.start_of_work,
            'dateEnd': self.end_of_work,
            'timeEnd': self.end_of_work,
            'safety': self.safety,
            'conditions': self.condition,
            'director': self.director,
            'directorPost': self.director,
            'dailyManager': self.daily_manager,
            'personalPost': self.daily_manager,
            'stateEngineer': self.station_engineer,
        }
        doc.render(context)

        doc.save(self.generate_file_name())

    def generate_file_name(self) -> str:
        return self.number.__str__() + ".docx"

    def print_docx(self):
        pass

    def signature(self): #-> #State:
        pass
        #
        # # if self.master_signature is None:
        # #     return State{
        # #         self.master
        # #     }
        # # if self.signature_from_daily_manager
        # MOCK_ADDRESS = constants.ZERO_ADDRESS
        # DEFAULT_INITIAL_BALANCE = to_wei(10000, 'ether')
        #
        # GENESIS_PARAMS = {
        #     'difficulty': constants.GENESIS_DIFFICULTY,
        # }
        #
        # GENESIS_STATE = {
        #     MOCK_ADDRESS: {
        #         "balance": DEFAULT_INITIAL_BALANCE,
        #         "nonce": 0,
        #         "code": b'',
        #         "storage": {}
        #     }
        # }
        #
        # chain = BaseMainnetChain.vm_configuration(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)
        #
        # mock_address_balance = chain.get_vm().state.get_balance(MOCK_ADDRESS)
        #
        # print(f"The balance of address {encode_hex(MOCK_ADDRESS)} is {mock_address_balance} wei")

        # return State

class State:
    permit: Permit
    who_notify: [Employee]


class HistoryPermit(models.Model):
    type_of_permit = {
        "SIMPLE": "simple",
        "LINEAR": "linear",
        "FIRE": "fire",
    }

    department_name = models.CharField(max_length=255)
    type_of = models.CharField(max_length=255, choices=type_of_permit)
    number = models.CharField(max_length=255, null=False)
    master_of_work = models.CharField(max_length=255)
    worker = models.CharField(max_length=255)
    # employ =
    master = models.CharField(max_length=255)
    work_description = models.CharField(max_length=255)
    start_of_work = models.DateTimeField(max_length=255)
    end_of_work = models.DateTimeField(max_length=255)
    #    type_of_work = ArrayField(
    #       ArrayField(
    #          models.CharField(max_length=10, blank=True),
    #         size=8,
    #     ),
    #     size=8,
    # )
    condition = models.CharField(max_length=255)

    time_of_permit = models.CharField(max_length=255, verbose_name="Наряд выдал")
    signature_from_director = models.CharField(max_length=255)
    signature_from_daily_manager = models.CharField(max_length=255)

    create_at = models.DateTimeField()
    updated_at = models.DateTimeField()




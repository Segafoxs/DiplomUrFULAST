from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from docxtpl import DocxTemplate
from .myModels import Work_is_mymodel, Manager_is_mymodel, Executor_is_mymodel, Director_is_mymodel, Permit_is_mymodel, ShiftManager_is_mymodel
import random

def return_members(members: list):


    return ",".join(members)





from django.shortcuts import render
from datetime import datetime

def return_date(timestamp):

    dt_object = datetime.fromtimestamp(timestamp)
    string_datetime = dt_object.strftime("%d-%m-%Y, %H:%M:%S")

    return string_datetime


roles = {
            "DIRECTOR": "Начальник цеха",
            "MASTER": "Мастер",
            "EXECUTOR": "Бригадир",
            "WORKER": "Рабочий",
            "DAILYMANAGER": "Начальник смены",
            "STATIONENGINEER": "Инженер станции",
        }

rolesCreatePermit = {
    "DIRECTOR": "Начальник цеха",
    "MASTER": "Мастер",
}


def return_members(members: list):
    return ",".join(members)





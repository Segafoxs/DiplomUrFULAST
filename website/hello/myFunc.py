from django.shortcuts import render


roles = {
            "DIRECTOR": "Начальник цеха",
            "MASTER": "Мастер",
            "WORKER": "Работник",
            "DAILYMANAGER": "Начальник смены",
            "STATIONENGINEER": "Инженер станции",
        }


def return_members(members: list):
    return ",".join(members)





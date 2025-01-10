from django.shortcuts import render


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





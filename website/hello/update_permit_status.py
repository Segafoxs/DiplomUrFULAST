import logging

import minio
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Permit, HistoryPermit, PrivateKeys

from .notary import blockchain, signature
from .s3 import minio

@login_required
@csrf_exempt
def update_permit_status(request):
    if request.method == "POST":
        private_key = request.POST.get("private_key")
        permit_id = request.POST.get("permit_number")

        permit = get_object_or_404(Permit, number=permit_id)
        # Обработать ошибку если не нашли приватный ключ
        private_key_obj = get_object_or_404(PrivateKeys, private_key=private_key)

        current_user = request.user
        if current_user.role == "MASTER":
            permit.signature_master = signature
        elif current_user.role == "DIRECTOR":
            permit.signature_director = signature
        elif current_user.role == "DAILYMANAGER":
            permit.signature_dailymanager = signature
        elif current_user.role == "STATIONENGINEER":
            permit.signature_stationengineer = signature
        elif current_user.role == "EXECUTOR":
            permit.signature_executor = signature
        else:
            return HttpResponse("У вас нет прав для подписи.", status=403)

        try:
            response = minio.get_object(permit.generate_file_name())
        except minio.S3Error as e:
            logging.error(e)
            return HttpResponse("Ошибка работы с хранилищем", status=405)

        digest, sig, public_key = signature.generate_signature(response.data, private_key_obj.private_key)
        blockchain.write_to_blockchain(permit.number, digest, sig, public_key, current_user.name)

        if permit.action == "ОТКРЫТИЕ":
            if permit.status == "На согласовании с руководителем работ":
                permit.status = "На согласовании с начальником цеха"
            elif permit.status == "На согласовании с начальником цеха":
                permit.status = "На согласовании с дежурным инженером станции"
            elif permit.status == "На согласовании с дежурным инженером станции":
                permit.status = "На согласовании с начальником смены"
            elif permit.status == "На согласовании с начальником смены":
                permit.status = "Подпись производителя работ"
            elif permit.status == "Подпись производителя работ":
                permit.status = "В работе"
                permit.action = "ОТКРЫТ"

        if permit.action == "ЗАКРЫТИЕ":
            if permit.status == "На согласовании с руководителем работ":
                permit.status = "На согласовании с начальником смены"
            elif permit.status == "На согласовании с начальником смены":
                permit.status = "Подпись производителя работ"
            elif permit.status == "Подпись производителя работ":
                permit.status = "Закрыт"
                his_perm = HistoryPermit.objects.create(number=permit.number,
                                                        status=permit.status,
                                                        reason="Работа полностью закончена",
                                                        department_name=permit.department,
                                                        master_of_work=permit.master_of_work,
                                                        signature_master=permit.signature_master,
                                                        executor=permit.executor,
                                                        countWorker=permit.countWorker,
                                                        workers=permit.workers,
                                                        work_description=permit.work_description,
                                                        start_of_work=permit.start_of_work,
                                                        end_of_work=permit.end_of_work,
                                                        signature_director=permit.signature_director,
                                                        signature_dailymanager=permit.signature_dailymanager,
                                                        signature_stationengineer=permit.signature_stationengineer,
                                                        safety=permit.safety,
                                                        condition=permit.condition,
                                                        director=permit.director,
                                                        daily_manager=permit.daily_manager,
                                                        station_engineer=permit.station_engineer,
                                                        )
                permit.delete()
                return redirect('/currentPermit')

            else:
                return HttpResponse("Невозможно обновить статус.", status=400)
        permit.save()
        return redirect("docsSign")

    else:
        return HttpResponse("Метод не поддерживается.", status=405)
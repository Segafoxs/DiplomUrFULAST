import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView
from django_filters import FilterSet
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin
from django.forms import formset_factory
from .dbFunc import select_in_db
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Employee, Permit, Department, HistoryPermit, PrivateKeys
from django.contrib.auth.decorators import login_required
from .forms import LinePermit, LoginForm, ChoiceManager, DepartmentForm, WorkerGroup, DirectorSearch, \
    ManagerSearch, ExecutorSearch, StateEngineerSearch, DailyManagerSearch
from .tables import PermitTable
from .filters import MyFilter
from django.http import JsonResponse
from .myFunc import return_members, rolesCreatePermit, roles, return_date
from minio import Minio
from .notary.blockchain import read_all_chain_by_doc_id, read_all_documents, get_block_pop, get_block_number
from .myModels import Master, Director, DailyManager, Executor, StateEngineer


user_from_permit = {}

class ListViews(SingleTableMixin, FilterView):
    model = Permit
    table_class = PermitTable
    template_name = 'hello/currentWorkPermits/currentWork.html'
    filterset_class = MyFilter


def view_permit(request):

        backet = []
        list_sign = []
        number = request.POST.get("number")

        permit = get_object_or_404(Permit, number=number)

        context = {"permit": permit,
                   "master": None,
                   "director": None,
                   "stateEng": None,
                   "dailyMan": None,
                   "executor": None
                   }
            #Нужно достать подписи всех участников,
            # закинуть в функцию  get_block_number,
            # достать дату и вывести всё на экран



        try:
            result = read_all_documents()
            for i in range(len(result)):
                if result[i][0] == int(number):
                    backet.append(result[i])
                else:
                    continue

                if len(backet) == 0:
                    return HttpResponse("{message: Документ не найден}")



            for i in range(len(backet)):

                for j in range(len(backet[0])):
                    if j == 5:
                        list_sign.append(backet[i][j])




            if len(list_sign) > 0:
                master = Master()
                master.name = list_sign[0]
                master.sign = permit.signature_master
                master.block_tx = get_block_number(int(master.sign))
                master.date_sign = return_date(master.block_tx["timestamp"])
                context["master"] = master


            if len(list_sign) > 1:
                director = Director()
                director.name = list_sign[1]
                director.sign = permit.signature_director
                director.block_tx = get_block_number(int(director.sign))
                director.date_sign = return_date(director.block_tx["timestamp"])
                context["director"] = director

            if len(list_sign) > 2:
                stateEng = StateEngineer()
                stateEng.name = list_sign[2]
                stateEng.sign = permit.signature_stationengineer
                stateEng.block_tx = get_block_number(int(stateEng.sign))
                stateEng.date_sign = return_date(stateEng.block_tx["timestamp"])
                context["stateEng"] = stateEng

            if len(list_sign) > 3:
                dailyMan = DailyManager()
                dailyMan.name = list_sign[3]
                dailyMan.sign = permit.signature_dailymanager
                dailyMan.block_tx = get_block_number(int(dailyMan.sign))
                dailyMan.date_sign = return_date(dailyMan.block_tx["timestamp"])
                context["dailyMan"] = dailyMan

            if len(list_sign) > 4:
                executor = Executor()
                executor.name = list_sign[4]
                executor.sign = permit.signature_executor
                executor.block_tx = get_block_number(int(executor.sign))
                executor.date_sign = return_date(executor.block_tx["timestamp"])
                context["executor"] = executor


            # sign_director = permit.signature_director
            # sign_stateEng = permit.signature_stationengineer
            # sign_dailyMan = permit.signature_dailymanager
            # sign_executor = permit.signature_executor
            #
            # block = get_block_number(int(sign_master))
            # timestmp = block["timestamp"]
            # date = return_date(timestmp)



        except Exception as err:
            return HttpResponse(f"Транзакции по наряду {number} не найдены")

        return render(request, 'hello/currentWorkPermits/viewCurrentPermit.html', context)


def create_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        queryDepartment = Department.objects.filter(name=request.POST.get('department'))
        department_id = 0
        for department in queryDepartment:
            department_id = department.id

        employee = Employee.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role,
            department=Department.objects.get(id=department_id)
        )

        return redirect('/workPermit/')



    # return render(request, 'hello/createUser/create_user.html')

def authFunc(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/currentPermit/')
    else:
        form = LoginForm()
    return render(request, 'hello/authorization/index.html', {'form': form})


def logoutFunc(request):
    logout(request)
    return redirect('/login/')


def first_page(request):
    return render(request, 'hello/firstPage/firstPage.html')

def work_permit(request):

    form_department = DepartmentForm()

    form_directorSearch = DirectorSearch()
    form_managerSearch = ManagerSearch()
    form_executorSearch = ExecutorSearch()
    form_stateEngineerSearch = StateEngineerSearch()
    form_dailyManagerSearch = DailyManagerSearch()

    context = {
        "form_department": form_department,
        "form_directorSearch": form_directorSearch,
        "form_managerSearch": form_managerSearch,
        "form_executorSearch": form_executorSearch,
        "form_stateEngineerSearch": form_stateEngineerSearch,
        "form_dailyManagerSearch": form_dailyManagerSearch,
    }
    return render(request, 'hello/workPermit/workPermit.html', context)


def docx_sign(request):
    latest_permit_list = Permit.objects.filter(status="approval")
    if latest_permit_list:
        for id in latest_permit_list:
            id_master = id.master_of_work_id
            master = Employee.objects.get(id=id_master)

            context = {
                "permit_list": latest_permit_list,
                "master": master
            }
            return render(request, 'hello/docsSign/docsSign.html', context)
    return render(request, 'hello/docsSign/docsSign.html')




def lists(request):
    model = Permit.objects.all()
    filterset_class = MyFilter(request.GET, model)
    table = PermitTable(filterset_class.qs)



    return render(request=request, template_name='hello/currentWorkPermits/currentWork.html',
                  context={"model":model, "table":table, "filterset_class":filterset_class, })

@login_required
def docx_sign(request):
    current_user = request.user

    status_map = {
        'MASTER': "На согласовании с руководителем работ",
        'DIRECTOR': "На согласовании с начальником цеха",
        'STATIONENGINEER': "На согласовании с дежурным инженером станции",
        'DAILYMANAGER': "На согласовании с начальником смены",
        'EXECUTOR': "Подпись производителя работ"
    }

    status_filter = status_map.get(current_user.role)

    if not status_filter:
        return render(request, 'hello/docsSign/docsSign.html', {"permit_list": []})

    latest_permit_list = Permit.objects.filter(status=status_filter, action="ОТКРЫТИЕ").select_related(
        'daily_manager', 'master_of_work', 'director', 'station_engineer'
    )

    close_permit = Permit.objects.filter(status=status_filter, action="ЗАКРЫТИЕ")

    context = {
        "permit_list_open": latest_permit_list,
        "permit_list_close": close_permit,
        "role": current_user.role
    }

    return render(request, 'hello/docsSign/docsSign.html', context)


def resultPermit(request):

    list_user = []

    try:

        if request.method == "POST":

            new_permit = Permit()
            new_permit.department = Department.objects.get(id=request.POST.get("department"))

            #Участники наряда

            new_permit.director = Employee.objects.get(id=request.POST.get("directorPermit"))
            new_permit.master_of_work = Employee.objects.get(id=request.POST.get("managerPermit"))
            new_permit.executor = Employee.objects.get(id=request.POST.get("executorPermit"))
            new_permit.countWorker = request.POST.get("countMember")
            new_permit.station_engineer = Employee.objects.get(id=request.POST.get("stateEngineerPermit"))
            new_permit.daily_manager = Employee.objects.get(id=request.POST.get("dailyManagerPermit"))

            #Работа по наряду
            new_permit.work_description = request.POST.get("work")
            d_start = request.POST.get("dateStart")
            t_start = request.POST.get("timeStart")
            start_datetime = datetime.strptime(f"{d_start} {t_start}", "%Y-%m-%d %H:%M")
            new_permit.start_of_work = make_aware(start_datetime)
            d_end = request.POST.get("dateEnd")
            t_end = request.POST.get("timeEnd")
            end_datetime = datetime.strptime(f"{d_end} {t_end}", "%Y-%m-%d %H:%M")
            new_permit.end_of_work = make_aware(end_datetime)

            dateDelivery = request.POST.get("dateDelivery")
            timeDelivery = request.POST.get("timeDelivery")
            d_Delivery = datetime.strptime(f"{dateDelivery} {timeDelivery}", "%Y-%m-%d %H:%M")
            new_permit.date_delivery = make_aware(d_Delivery)
            new_permit.condition = request.POST.get("conditions")
            new_permit.safety = request.POST.getlist("source")

            members = []
            for key in request.POST:
                if key.startswith("members["):
                    members.append(request.POST[key])


            new_permit.workers = members
            result = return_members(members)


            data = Permit(master_of_work=new_permit.master_of_work,
                          executor=new_permit.executor, director=new_permit.director, daily_manager=new_permit.daily_manager,
                          station_engineer=new_permit.station_engineer, work_description=new_permit.work_description,
                          start_of_work=new_permit.start_of_work, end_of_work=new_permit.end_of_work, date_delivery=new_permit.date_delivery,
                          condition=new_permit.condition ,countWorker=new_permit.countWorker, department=new_permit.department,
                          safety=new_permit.safety, workers=new_permit.workers
                          )
            data.save()

            data.to_docx(result, d_start, t_start, d_end, t_end, dateDelivery, timeDelivery)
            # TODO move client to setting
            client = Minio("127.0.0.1:9000",
                           access_key="YOUR_ACCESS_KEY",
                           secret_key="YOUR_SECRET_KEY",
                           secure=False,
                           )
            bucket_name = "docs"

            found = client.bucket_exists(bucket_name)
            if not found:
                client.make_bucket(bucket_name)
                print("Created bucket", bucket_name)
            else:
                print("Bucket", bucket_name, "already exists")

            # Upload the file, renaming it in the process
            client.fput_object(
                bucket_name, data.generate_file_name(), data.generate_file_name(),
            )
            print(
                data.generate_file_name(), "successfully uploaded as object",
                data.generate_file_name(), "to bucket", bucket_name,
            )

            os.remove(data.generate_file_name())



            return JsonResponse({f"success": f"Наряд успешно сформирован! Ваш номер наряда {data.number}"}, status=200)

    except KeyError as err:
        return JsonResponse({f"<h1>Заполните все поля<h1>{err}"})

    except Exception as err:
        return JsonResponse({f"{err}"})


def close_permit(request):
    safetyPermit = {
        'wrong': "Не правильно оформлен наряд.",
        'endWork': "Работа полностью закончена.",

    }

    list_user = {'MASTER': 'MASTER', 'DIRECTOR':'DIRECTOR',}

    if request.method == "POST":
        current_user = request.user

        temp = list_user.get(current_user.role)


        if not temp:
            return redirect('/currentPermit/')
        number = request.POST.get('number')
        safety = request.POST.get('safetyRequirements')
        try:
            permit = Permit.objects.get( number=number)

            if permit is not None:
                if safetyPermit[safety] == safetyPermit['wrong'] and permit.status=="В работе":
                    historyPermit = HistoryPermit.objects.create(number=permit.number,
                                                                 status="Закрыт",
                                                                 reason=safetyPermit[safety],
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

                elif safetyPermit[safety] == safetyPermit['endWork'] and permit.status == "В работе":
                    permit.action = "ЗАКРЫТИЕ"
                    permit.status = "На согласовании с руководителем работ"
                    permit.save()
                    return redirect('/currentPermit')
                else:
                    permit.delete()
                    return redirect('/currentPermit')

            return render(request, 'hello/currentWorkPermits/currentWork.html')

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)


def firePermit(request):

    if request.method == "POST":
        name = request.POST.get("your_name")
        post = request.POST.get("your_post")
        return HttpResponse(f"<h1>{name} {post}</h1>")
    else:
        userForm = LinePermit()
        return render(request, "hello/firePermit/firePermit.html", {"forms": userForm})






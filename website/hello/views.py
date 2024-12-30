from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django_filters import FilterSet
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin
from django.forms import formset_factory
from django.contrib.auth.hashers import make_password
from .myModels import Work_is_mymodel, Manager_is_mymodel, Executor_is_mymodel, Director_is_mymodel, Permit_is_mymodel, ShiftManager_is_mymodel
from .dbFunc import select_in_db
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Employee, Permit, Department, HistoryPermit
from django.contrib.auth.decorators import login_required
from .forms import LinePermit, LoginForm, ChoiceManager, DepartmentForm, WorkerGroup
from .tables import PermitTable
from .filters import MyFilter
from django.http import JsonResponse
from .myFunc import return_members



user_from_permit = {}

class ListViews(SingleTableMixin, FilterView):
    model = Permit
    table_class = PermitTable
    template_name = 'hello/currentWorkPermits/currentWork.html'
    filterset_class = MyFilter


def view_permit(request):
    if request.method == "POST":
        number = request.POST.get("number")

        permit = Permit.objects.filter(number=number)
        return render(request, 'hello/currentWorkPermits/viewCurrentPermit.html', context={"permit": permit})

def example(request):
    form = DepartmentForm()
    context = {
        "form": form
    }

    return render(request, 'hello/example', context)

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



    return render(request, 'hello/createUser/create_user.html')

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




def first_page(request):
    values = {"count": 5}
    return render(request, 'hello/firstPage/firstPage.html', values)

def work_permit(request):

    form_department = DepartmentForm()

    #TestForm = formset_factory(WorkerGroup, extra=4)
    #testForm = TestForm()

    context = {
        "form_department": form_department,

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

    permit = Permit.objects.filter(number=1345)


    return render(request=request, template_name='hello/currentWorkPermits/currentWork.html',
                  context={"model":model, "table":table, "filterset_class":filterset_class, "permit": permit})

@login_required
def docx_sign(request):
    current_user = request.user

    status_map = {
        'MASTER': "На согласовании с руководителем работ",
        'DIRECTOR': "На согласовании с начальником цеха",
        'STATIONENGINEER': "На согласовании с дежурным инженером станции",
        'DAILYMANAGER': "На согласовании с начальником смены"
    }

    status_filter = status_map.get(current_user.role)

    if not status_filter:
        return render(request, 'hello/docsSign/docsSign.html', {"permit_list": []})

    latest_permit_list = Permit.objects.filter(status=status_filter).select_related(
        'daily_manager', 'master_of_work', 'director', 'station_engineer'
    )

    close_permit = Permit.objects.filter(status="Закрытие")

    context = {
        "permit_list_open": latest_permit_list,
        "permit_list_close": close_permit,
        "role": current_user.role
    }

    return render(request, 'hello/docsSign/docsSign.html', context)


@login_required
@csrf_exempt
def update_permit_status(request):
    if request.method == "POST":
        permit_id = request.POST.get("permit_number")
        permit = get_object_or_404(Permit, number=permit_id)

        current_user = request.user

        if current_user.role == "MASTER":
            permit.signature_master = current_user.token
        elif current_user.role == "DIRECTOR":
            permit.signature_director = current_user.token
        elif current_user.role == "DAILYMANAGER":
            permit.signature_dailymanager = current_user.token
        elif current_user.role == "STATIONENGINEER":
            permit.signature_stationengineer = current_user.token
        else:
            return HttpResponse("У вас нет прав для подписи.", status=403)
        
        if permit.status == "На согласовании с руководителем работ":
            permit.status = "На согласовании с начальником цеха"
        elif permit.status == "На согласовании с начальником цеха":
            permit.status = "На согласовании с дежурным инженером станции"
        elif permit.status == "На согласовании с дежурным инженером станции":
            permit.status = "На согласовании с начальником смены"
        elif permit.status == "На согласовании с начальником смены":
            permit.status = "В работе"
        else:
            return HttpResponse("Невозможно обновить статус.", status=400)

        permit.save()

        return redirect("docsSign")
    else:
        return HttpResponse("Метод не поддерживается.", status=405)
    


def postDirector(request):
    try:
        if request.method == "POST":
            search_query = request.POST.get('search_director')
            user_from_db = select_in_db(search_query)
            if user_from_db is not None:
                for user in user_from_db:
                    post = user.role
                    if user.role != "DIRECTOR":
                        return JsonResponse({"error": f"{post} не может выдавать наряд-допуск"}, status=400)
                    director_id = user.id
                    user_from_permit['director'] = director_id
                    print(f'{user.id} {user.name} {user.role}')
                return JsonResponse({"success": "Начальник цеха добавлен успешно", "users": list(user_from_db.values())})
            else:
                return JsonResponse({"error": "USER IS NOT FOUND"}, status=404)
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)



def postManager(request):
    try:
        if request.method == "POST":
            search_query = request.POST.get('search_manager')
            user_from_db = select_in_db(search_query)
            if user_from_db is not None:
                for user in user_from_db:
                    if user.role != "MASTER":
                        return JsonResponse({"error": "Руководитель не может быть из числа рабочих"}, status=400)
                    manager_id = user.id
                    user_from_permit['manager'] = manager_id
                    print(f'{user.id} {user.name} {user.role}')
                return JsonResponse({"success": "Руководитель добавлен успешно", "users": list(user_from_db.values())})
            else:
                return JsonResponse({"error": "USER IS NOT FOUND"}, status=404)
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)



def postExecutor(request):
    try:
        if request.method == "POST":
            search_query = request.POST.get('search_executor')
            count_worker = request.POST.get('count_member')
            user_from_db = select_in_db(search_query)
            if user_from_db is not None:
                for user in user_from_db:
                    executor_id = user.id
                    user_from_permit['executor'] = executor_id
                    print(f'{user.id} {user.name} {user.role}')
                return JsonResponse({"success": "Исполнитель добавлен успешно", "users": list(user_from_db.values())})
            else:
                return JsonResponse({"error": "USER IS NOT FOUND"}, status=404)
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)



def postShiftManager(request):
    try:
        if request.method == "POST":
            search_query = request.POST.get('search_shiftManager')
            users = select_in_db(search_query)
            if users is not None:
                for user in users:
                    if user.role != "DAILYMANAGER":
                        return JsonResponse({"error": f"{user.role} не может быть начальником смены"}, status=400)

                    shiftManager_id = user.id
                    user_from_permit['shiftManager'] = shiftManager_id
                    print(f'{user.id} {user.name} {user.role}')
                
                return JsonResponse({"success": "Начальник смены добавлен успешно", "users": list(users.values())})
            else:
                return JsonResponse({"error": "USER IS NOT FOUND"}, status=404)
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)


def postStateEngineer(request):
    try:
        if request.method == "POST":
            search_query = request.POST.get('search_state_engineer')
            users = select_in_db(search_query)
            if users is not None:
                for user in users:
                    if user.role != "STATIONENGINEER":
                        return JsonResponse({"error": f"{user.role} не может быть дежурным инженером станции"}, status=400)

                    stateEngineer_id = user.id
                    user_from_permit['stateEngineer'] = stateEngineer_id
                    print(f'{user.id} {user.name} {user.role}')
                
                return JsonResponse({"success": "Дежурный инженер станции добавлен успешно", "users": list(users.values())})
            else:
                return JsonResponse({"error": "USER IS NOT FOUND"}, status=404)
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)


def postWorker(request):

    try:
        if request.method == "POST":
            search_query = request.POST.get('search_worker')
            users = select_in_db(search_query)
            if users is not None:
                for user in users:
                    worker_id = user.id

                    user_from_permit['worker'] = worker_id

                    # insert_into_doc(executor)
                    print(f'{user.id} {user.name} {user.role}')
            else:
                return HttpResponse("USER IS NOT FOUND")

            return render(request, "hello/workPermit/searchUser.html", {'query': search_query, 'user': users})
        return render(request, "hello/workPermit/searchUser.html", {})
    except Exception as err:
        return HttpResponse(f"{err}")

def resultPermit(request):

    list_user = {}

    try:

        if request.method == "POST":

            new_permit = Permit()
            new_permit.department = Department.objects.get(id=request.POST.get("department"))

            #Участники наряда
            new_permit.master_of_work = Employee.objects.get(id=user_from_permit['manager'])
            # list_user['manager']=Employee.objects.get(id=)
            # #new_permit.master_signature
            new_permit.executor = Employee.objects.get(id=user_from_permit['executor'])
            new_permit.countWorker = request.POST.get("countMember")
            new_permit.daily_manager = Employee.objects.get(id=user_from_permit['shiftManager'])
            new_permit.station_engineer = Employee.objects.get(id=user_from_permit['stateEngineer'])
            new_permit.director = Employee.objects.get(id=user_from_permit['director'])

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
            data.to_docx(result, )
            return HttpResponse({"success": "Наряд успешно сформирован!"})





    except KeyError as err:
        return HttpResponse(f"<h1>Заполните все поля<h1>{err}")

    except Exception as err:
        return HttpResponse(f"{err}")


def close_permit(request):
    safetyPermit = {
        'wrong': "Не правильно оформлен наряд.",
        'endWork': "Работа полностью закончена.",

    }


    if request.method == "POST":
        number = request.POST.get('number')
        safety = request.POST.get('safetyRequirements')
        try:
            permit = Permit.objects.get(number=number)

            if permit is not None:
                if safetyPermit[safety] == safetyPermit['endWork'] and permit.status=="В работе" or safetyPermit[safety] == safetyPermit['wrong'] and permit.status=="В работе":
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






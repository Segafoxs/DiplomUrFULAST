from django import forms
from . import models
from django_select2.forms import Select2Widget




# class DirectorSearchsss(forms.Form):
#     name = forms.ModelChoiceField(label="Выдающий наряд-допуск", queryset=models.Employee.objects.all(),
#                                   widget=Select2Widget(attrs={"required id": "director",
#                                                               "name": "director"}))

class DirectorSearch(forms.ModelForm):

    directorPermit = forms.ModelChoiceField(label="Выдающий наряд-допуск", queryset=models.Employee.objects.filter(role="DIRECTOR"),
                                  widget=Select2Widget(attrs={"required id": "director",
                                                              }))
    class Meta:
        model = models.Employee
        fields = ('directorPermit',)



class ManagerSearch(forms.ModelForm):

    managerPermit = forms.ModelChoiceField(label="Руководитель работ", queryset=models.Employee.objects.filter(role="MASTER"),
                                  widget=Select2Widget(attrs={"required id": "manager"}))

    class Meta:
        model = models.Employee
        fields = ('managerPermit',)


class ExecutorSearch(forms.ModelForm):
    executorPermit = forms.ModelChoiceField(label="Исполнитель работ", queryset=models.Employee.objects.all(),
                                  widget=Select2Widget(attrs={"required id": "executor",
                                                              }))

    class Meta:
        model = models.Employee
        fields = ('executorPermit',)


class StateEngineerSearch(forms.ModelForm):
    stateEngineerPermit = forms.ModelChoiceField(label="Дежурный инженер станции", queryset=models.Employee.objects.filter(role="STATIONENGINEER"),
                                  widget=Select2Widget(attrs={"required id": "stateEngineer",
                                                              }))

    class Meta:
        model = models.Employee
        fields = ('stateEngineerPermit',)


class DailyManagerSearch(forms.ModelForm):
    dailyManagerPermit = forms.ModelChoiceField(label="Допускающий (Начальник смены)", queryset=models.Employee.objects.filter(role="DAILYMANAGER"),
                                  widget=Select2Widget(attrs={"required id": "dailyManager",
                                                              "class": "form-select form-select-lg",
                                                              }))

    class Meta:
        model = models.Employee
        fields = ('dailyManagerPermit',)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control border-top-2 border-left-0 border-right-0"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control border-top-2 border-left-0 border-right-0"}))



class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(label="Подразделение", queryset=models.Department.objects.all(), widget=forms.Select(attrs={"class": "form-select form-select-lg mb-2",
                                                                                                                          "name": "department"}))



# class Status(forms.Form):
#     state = forms.ChoiceField(choices=Permit.statusPermit, widget=forms.Select(attrs={"class": "form-select form-select-lg mb-3"}))

class ChoiceDirector(forms.Form):
    name = forms.CharField(label="director name", max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))

class ChoiceManager(forms.Form):
    name = forms.CharField(label="manager name", max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
class LinePermit(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))
    your_post = forms.CharField(label="Your post", max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))


class WorkerGroup(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={"class":"form-control form-control-lg"}))

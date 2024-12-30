from django import forms
from .models import Department, Permit




class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control border-top-2 border-left-0 border-right-0"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control border-top-2 border-left-0 border-right-0"}))





class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(label="Подразделение", queryset=Department.objects.all(), widget=forms.Select(attrs={"class": "form-select form-select-lg mb-3",
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

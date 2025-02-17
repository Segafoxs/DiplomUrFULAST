import secrets
import string

import django.db.models
from django.contrib import admin
from .models import Post, Employee, Permit, Department, TypeOfWork, HistoryPermit, PrivateKeys

from ajax_select import make_ajax_field



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(TypeOfWork)
class TypeOfWorkAdmin(admin.ModelAdmin):
    pass

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.action(description="Generate docx file")
def generate_docx(modeladmin, request, queryset: django.db.models.QuerySet):
    for obj in queryset:
        obj.to_docx()


@admin.action(description="Signature")
def signature(modeladmin, request, queryset: django.db.models.QuerySet):
    for obj in queryset:
        obj.signature()

@admin.register(Permit)
class PermitAdmin(admin.ModelAdmin):
    actions = [generate_docx, signature]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['master_of_work'].queryset = Employee.objects.filter(role="MASTER")
        form.base_fields['executor'].queryset = Employee.objects.filter(role="WORKER")
        form.base_fields['workers'].queryset = Employee.objects.filter(role="WORKER")
        form.base_fields['master_of_work'].queryset = Employee.objects.filter(role="MASTER")
        form.base_fields['director'].queryset = Employee.objects.filter(role="DIRECTOR")
        form.base_fields['daily_manager'].queryset = Employee.objects.filter(role="DAILYMANAGER")
        form.base_fields['station_engineer'].queryset = Employee.objects.filter(role="STATIONENGINEER")
        return form

@admin.register(HistoryPermit)
class HistoryPermitAdmin(admin.ModelAdmin):
    actions = [generate_docx]

@admin.register(PrivateKeys)
class PrivateKeysAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(32))
        initial_data['private_key'] = password
        return initial_data



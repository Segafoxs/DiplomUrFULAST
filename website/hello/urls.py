from django.urls import path
from . import views
from .views import ListViews, create_employee
from .update_permit_status import update_permit_status

urlpatterns = [
    path("login/", views.authFunc, name="authFunc"),
    path("logout/", views.logoutFunc, name="logout"),
    path("welcomePage/", views.first_page, name="welcomePage"),
    path("workPermit/", views.work_permit, name="workPermit"),
    path("currentPermit/", views.lists, name="currentPermit"),
    path("viewPermit/", views.view_permit, name="view_permit"),
    path("docsSign/", views.docx_sign, name="docsSign"),
    path("workPermit/resultWorkPermit/", views.resultPermit, name="resultPermit"),
    path("closePermit/", views.close_permit, name="closePermit"),
    path("firePermit/", views.firePermit, name="firePermit"),
    path('create-employee/', create_employee, name='create_employee'),
    path('update-permit-status/', update_permit_status, name='update_permit_status'),
    # path("firePermit/postDirector", views)
]
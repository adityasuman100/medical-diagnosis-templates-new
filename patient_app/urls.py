from django.urls import path

from . import views

app_name="patient_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_patient, name="create_patient"),
    path("read/", views.read_patient, name="read_patient"),
    path("update/", views.update_patient, name="update_patient"),
    # path("payment/", views.payment, name="payment"),
    path("print_report/", views.print_report, name="print_report"),



    # Echo payment
]
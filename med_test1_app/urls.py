from django.urls import path

from . import views

app_name='med_test1_app'

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_med_test1_report, name="create_med_test1_report"),
    path("read/", views.read_med_test1_report, name="read_med_test1_report"),
    path("update/", views.update_med_test1_report, name="update_med_test1_report"),
    path("delete/", views.delete_med_test1_report, name="delete_med_test1_report"),
    path('validate/', views.validate, name='validate'),
    path('test/', views.test, name='test'),

    path("print_report/", views.print_report, name="print_report"),
    # path("generate_pdf/", views.generate_pdf_new, name="generate_pdf_new"),
    path("generate_pdf/", views.generate_pdf_new, name="generate_pdf_new"),



    # echo payment
]
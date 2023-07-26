from turtle import heading
from django.urls import path

from med_test2_app.models import Med_test2_1_report, Med_test2_2_report, Med_test2_3_report, Med_test2_4_report, Med_test2_5_report
from med_test2_app.views import Create, Read, Update, Validate, Pdf

from . import views

app_name='med_test2_app'

urlpatterns = [
    path("", views.index, name="index"),

    path("create_1/", Create.as_view(report=Med_test2_1_report), name="Create_1"),
    path("create_2/", Create.as_view(report=Med_test2_2_report), name="Create_2"),
    path("create_3/", Create.as_view(report=Med_test2_3_report), name="Create_3"),
    path("create_4/", Create.as_view(report=Med_test2_4_report), name="Create_4"),
    path("create_5/", Create.as_view(report=Med_test2_5_report), name="Create_5"),

    path("read_1/", Read.as_view(report=Med_test2_1_report), name="Read_1"),
    path("read_2/", Read.as_view(report=Med_test2_2_report), name="Read_2"),
    path("read_3/", Read.as_view(report=Med_test2_3_report), name="Read_3"),
    path("read_4/", Read.as_view(report=Med_test2_4_report), name="Read_4"),
    path("read_5/", Read.as_view(report=Med_test2_5_report), name="Read_5"),

    path("update_1/", Update.as_view(report=Med_test2_1_report), name="Update_1"),
    path("update_2/", Update.as_view(report=Med_test2_2_report), name="Update_2"),
    path("update_3/", Update.as_view(report=Med_test2_3_report), name="Update_3"),
    path("update_4/", Update.as_view(report=Med_test2_4_report), name="Update_4"),
    path("update_5/", Update.as_view(report=Med_test2_5_report), name="Update_5"),

    path("validate_1/", Validate.as_view(report=Med_test2_1_report), name="Validate_1"),
    path("validate_2/", Validate.as_view(report=Med_test2_2_report), name="Validate_2"),
    path("validate_3/", Validate.as_view(report=Med_test2_3_report), name="Validate_3"),
    path("validate_4/", Validate.as_view(report=Med_test2_4_report), name="Validate_4"),
    path("validate_5/", Validate.as_view(report=Med_test2_5_report), name="Validate_5"),

    path("pdf_1/", Pdf.as_view(report=Med_test2_1_report, heading="USG ABDOMEN"), name="Pdf_1"),
    path("pdf_2/", Pdf.as_view(report=Med_test2_2_report, heading="USG BREAST"), name="Pdf_2"),
    path("pdf_3/", Pdf.as_view(report=Med_test2_3_report, heading="USG PELVIS"), name="Pdf_3"),
    path("pdf_4/", Pdf.as_view(report=Med_test2_4_report, heading="USG KUB"), name="Pdf_4"),
    path("pdf_5/", Pdf.as_view(report=Med_test2_5_report, heading="DOPPLER LOWER LIMB"), name="Pdf_5"),



]
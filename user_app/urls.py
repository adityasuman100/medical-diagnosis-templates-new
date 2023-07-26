from django.urls import path

from . import views

app_name='user_app'

urlpatterns = [
    path("", views.index, name="index"),
    path("user/create/", views.create_user, name="create_user"),
    path("user/read/", views.read_user, name="read_user"),
    path("user/update/", views.update_user, name="update_user"),
    path("user/delete/", views.delete_user, name="delete_user"),



    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("accounts/login/", views.login_user, name="login_user"),


    # path("user/receipt/", views.receipt, name="receipt"),
    # path("user/constant/", views.constant, name="constant"),
    

]
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from patient_app.models import Patient
import datetime


# from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
# Create your views here.


# @permission_required('user_app.view_user')


def index(request):
    """
    index page for authentication
    """
    return redirect(reverse("user_app:login_user"))


def login_user(request):
    """
    login user
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            # print(request.user)
            return redirect(reverse("patient_app:create_patient"))
        return render(request, "login.html")
    elif request.method == "POST":
        # formData=request.POST
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "User logged in successfully.")
            return redirect(reverse("patient_app:create_patient"))
        else:
            # Display an error message or handle the failed login attempt
            messages.error(request, "Not a valid user")
            return render(request, "login.html")


def logout_user(request):
    """
    logout user
    """
    if request.method == "POST":
        logout(request)
        return redirect(reverse("user_app:login_user"))
    else:
        messages.error(request, "Method not allowed")
        # Perform some logic or fetch data
        # Create an HTTP response
        response = HttpResponse("Loged out successfully.")
        # You can set headers if needed
        # response['Custom-Header'] = 'Some value'
        return response


def create_user(request):
    method = request.method
    match method:
        case "GET":
            users=User.objects.all()
            users_=[]
            for user in users:
                users_.append({'id':user.id, 'username':user.username, 'first_name':user.first_name, 'last_name':user.last_name, 'groups':user.groups.all()})
            messages.success(request, 'users fetched successfully.')
            return render(request, "user_app/create_user.html", {'users':users_})
        case "POST":
            form_data = request.POST
            username = form_data.get("username", None)
            password = form_data.get("password", None)
            name = form_data.get("name", None)
            group=form_data.get('group', None)
            if not name or not group:
                messages.error(request, "Name or group not provided")
                return redirect(reverse('user_app:create_user'))
            

            try:
                # Check if the user with the provided username already exists
                user = User.objects.get(username=username)
                messages.error(request, "Username already exists.")
                return redirect(reverse('user_app:create_user'))
            except Exception:
                try:

                    group=Group.objects.get(name=group)
                    # Create the user
                    user = User.objects.create_user(
                        username=username, password=password)
                    user.first_name = name
                    user.groups.add(group)
                    user.save()

                    messages.success(request, "User created successfully.")
                    return redirect(reverse('user_app:create_user'))
                except Exception:
                    messages.error(request, 'group does not exist.')
                    return redirect(reverse('user_app:create_user'))

        case default:
            messages.error(request, "Method not allowed")
            return redirect(reverse('user_app:create_user'))


def read_user(request):
    match request.method:
        case "GET":
            form_data = request.GET
            id = form_data.get('id', None)
            user = User.objects.get(id=id)
            return render(request, "user_app/read_user.html", {'user': user})
        case default:
            messages.error(request, "Method not allowed")
            return redirect(reverse('user_app:create_user'))
    return render(request, "user_app/read_user.html")


def update_user(request):
    return HttpResponse('nothing here')
    return render(request, "user_app/update_user.html")


def delete_user(request):
    if request.method == "POST":
        formData = request.POST
        id = formData.get("id", None)
        try:
            User.objects.get(id=id).delete()
            messages.success(request, "User deleted successfully.")
            return redirect(reverse('user_app:create_user'))
        except Exception:
            messages.error(request, "User not found.")
            return redirect(reverse('user_app:create_user'))

    messages.error(request, "Method not allowed")
    return render(request, "error.html")


# def receipt(request):

#     match request.method:
#         case 'GET':
#             form_data = request.GET
#             date = form_data.get('date', None)
#             username = form_data.get('username', None)
#             if date and username:
#                 receipts = Receipt.objects.filter(
#                     created_date=date, done_by=username)
#             elif date:
#                 receipts = Receipt.objects.filter(created_date=date)
#             elif username:
#                 receipts = Receipt.objects.filter(done_by=username)
#             else:
#                 receipts = Receipt.objects.filter(
#                     created_date=datetime.date.today())

#             messages.success(request, 'receipts fetched successfully.')
#             return render(request, 'user_app/receipts.html', {'receipts': receipts})
#         case 'POST':
#             messages.error(request, 'method not allowed')
#             return redirect(reverse('user_app:receipts'))
#         case default:
#             messages.error(request, 'method not allowed')
#             return redirect(reverse('user_app:receipts'))


def patients(request):
    match request.method:
        case 'GET':
            form_data = request.GET
            date = form_data.get('date', None)
            if not date:
                date = datetime.date.today()
            patients = Patient.objects.filter(created_date=date)
            messages.success(request, 'patients fetched successfully.')
            return render(request, 'user_app/patients.html', {'patients': patients})
        case default:
            messages.error(request, 'method not allowed')
            return HttpResponse('method not allowed')


def all(request):
    match request.method:
        case 'GET':
            form_data = request.GET
            date = form_data.get('date', None)
            if not date:
                date = datetime.date.today()
            users = User.objects.filter(created_date=date)
            messages.success(request, 'users fetched successfully.')
            return render(request, 'user_app/users.html', {'users': users})
        case default:
            messages.error(request, 'method not allowed')
            return HttpResponse('method not allowed')


# def constant(request):
#     match request.method:
#         case 'GET':
#             constants=Constant.objects.all()
#             return render(request, 'user_app/constant.html', {'constants':constants})
#         case 'POST':
#             form_data=request.POST
#             med_test1_cost=form_data.get('med_test1_cost', None)
#             med_test2_cost=form_data.get('med_test2_cost', None)
#             if med_test1_cost:
#                 const=Constant.objects.get(name='med_test1_cost')
#                 const.value=med_test1_cost
#                 const.save()
#                 messages.success(request, 'constant updated successfully.')
#                 return redirect(reverse('user_app:constant'))
#             if med_test2_cost:
#                 const=Constant.objects.get(name='med_test2_cost')
#                 const.value=med_test2_cost
#                 const.save()
#                 messages.success(request, 'constant updated successfully.')
#                 return redirect(reverse('user_app:constant'))
            
#             return redirect(reverse('user_app:constants'))
#         case default:
#             messages.error(request, 'method not allowed.')
#             return redirect(reverse('user_app:constants'))
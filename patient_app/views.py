import datetime
# import utils.utils as utils
from django.shortcuts import render, redirect, reverse

# Create your views here.
# from django.http import HttpResponse
from django.contrib import messages
# from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

from django.contrib.auth.models import User, Permission

from .models import Patient
# CRUD


# index function
# @login_required(login_url='/login/')
# @permission_required('patient_app.view_patient')
def index(request):
    form_data=request.GET
    date=form_data.get('date', None)
    if date is None:
        date=datetime.date.today()
    try:
        p=Patient.objects.filter(created_date=date)
        return render(request, 'patient_app/index.html', {'patients':p})
    except Exception:
        messages.error(request, 'provide valid date')
        return redirect('index')

# @permission_required('patient_app.add_patient')
def create_patient(request):
    method=request.method
    match method:
        case 'GET':
            # send form for creating patient
            date=request.GET.get('date', None)
            if not date:
                date=datetime.date.today()
            p=Patient.objects.filter(created_date=date)
            return render(request, 'patient_app/create_patient.html', {'patients':p})
        case 'POST':
            # create patient in db
            form_data=request.POST
            name=form_data.get('name', None)
            age=form_data.get('age', None)
            gender=form_data.get('gender', None)
            mob_no=form_data.get('mob_no', None)
            address=form_data.get('address', None)
            try:
                p=Patient()
                # p=Patient.objects.create(name=name, age=age, gender=gender)
                # p.id=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(Patient.objects.count()+1)
                p.name=name
                p.age=age
                p.gender=gender
                p.mob_no=mob_no
                p.address=address
                p.med_test1=form_data.get('med_test1', False)
                p.med_test2_1=form_data.get('med_test2_1', False)
                p.med_test2_2=form_data.get('med_test2_2', False)
                p.med_test2_3=form_data.get('med_test2_3', False)
                p.med_test2_4=form_data.get('med_test2_4', False)
                p.med_test2_5=form_data.get('med_test2_5', False)
                p.save()
                messages.success(request, 'Patient Saved successfully')
                return redirect(reverse('patient_app:create_patient'))
            except Exception:
                messages.error(request, 'Error creating patient')
                return redirect(reverse('patient_app:create_patient'))
        case default:
            messages.error(request, 'Method not allowed')
            return redirect(reverse('patient_app:create_patient'))



# @permission_required('patient_app.view_patient')
def read_patient(request):
    method=request.method
    match method:
        case 'GET':
            id=request.GET.get('id', None)
            p=Patient.objects.get(id=id)
            
            messages.success(request, 'patient fetched successfully')
            return render(request, 'patient_app/read_patient.html', {'patient':p})

        case default:
            messages.error(request, 'Method not allowed')
            return redirect('create_patient')


# @permission_required('patient_app.change_patient')
def update_patient(request):
    method=request.method
    match method:
        case 'GET':
            id=request.GET.get('id')
            try:
                p=Patient.objects.get(id=id)
                return render(request, 'patient_app/update_patient.html', {'patient':p})
            except Exception:
                messages.error(request, 'Patient not found or provide a valid id')
                return redirect('create_patient')
        
        case 'POST':
            form_data=request.POST
            id=form_data.get('id', None)


            p=Patient.objects.get(id=id)
 
            
            if not p.med_test1:
                p.med_test1=form_data.get('med_test1', False)
            if not p.med_test2_1:
                p.med_test2_1=form_data.get('med_test2_1', False)
            if not p.med_test2_2:
                p.med_test2_2=form_data.get('med_test2_2', False)
            if not p.med_test2_3:
                p.med_test2_3=form_data.get('med_test2_3', False)
            if not p.med_test2_4:
                p.med_test2_4=form_data.get('med_test2_4', False)
            if not p.med_test2_5:
                p.med_test2_5=form_data.get('med_test2_5', False)

            # update attributes
            p.save()
            messages.success(request, 'Patient updated successfully')
            return redirect(f'/patient/read/?id={id}')
        case default:
            messages.error(request, 'Method not allowed')
            return redirect('create_patient')


# @permission_required('patient_app.delete_patient')
def delete_patient(request):
    '''
    delete Patient
    '''
    id=request.POST.get('id', None)
    if request.method=='POST':
        try:
            p=Patient.objects.get(id=id)
            p.delete()
            messages.success(request, 'Patient deleted successfully')
            return redirect('index')
        except Exception:
            messages.error(request, 'Patient not found or provide a valid id')
            return redirect('index')
        

    else:
        messages.error(request, 'Method not allowed')
        return render(request, 'error.html')


       



def print_report(request):
    form_data=request.GET
    date=form_data.get('date', None)
    if date is None:
        date=datetime.date.today()
    patients=Patient.objects.all()
    return render(request, 'patient_app/print_report.html', {'patients':patients})
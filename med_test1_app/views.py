from django.shortcuts import render, redirect, reverse
from django.conf import settings
import os
from django.utils.html import linebreaks
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

from django.db.models import Q
from django.core.serializers import serialize
# Create your views here.

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

import json
from django.http import JsonResponse

from django.contrib import messages
import datetime
# from patient_app.models import Patient
from patient_app.models import Patient
from .models import Med_test1_report

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors, utils
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO



# @permission_required('patient_app.view_patient')
def index(request):
    return redirect(reverse('patient_app:create_patient'))
    # print(request.user.get_all_permissions())
    form_data=request.GET
    date=form_data.get('date', None)
    if date==None:
        date=datetime.date.today()

    
    # receipts=Receipt.objects.filter(Q(created_date=date) & ~Q(med_test1__isnull=True))
    # serialised_data=serialize('json', receipts)
    # return JsonResponse(serialised_data, safe=False)
    
    return render(request, 'med_test1_app/index.html')
    

# @permission_required('med_test1_app.add_echoreport')
# def create_med_test1_report(request):
def create_med_test1_report(request):

    if request.method=='GET':
        id=request.GET.get('id', None)
        try:
            p=Patient.objects.get(id=id)
        except Exception:
            messages.error(request, 'Patient not found')
            return redirect(reverse('patient_app:create_patient'))
        if p.med_test1_report:
            messages.error(request, 'report already existed please update or take print')
            return redirect(reverse('patient_app:read_patient')+f'?id={id}')
        return render(request, 'med_test1_app/create.html', {'patient':p})
        # return render(request, 'med_test1_app/create_med_test1_report.html', {'patient':p})


    elif request.method=='POST':

        # return render(request, 'med_test1_app/helper/read.html', {'t1_1':request.POST.get('t1_1', None)})
        # create echo report with id
        form_data=request.POST
        # print(form_data)
        # return render(request, 'error.html', {'form_data':form_data})
        id=form_data.get('id', None)
        try:
            p=Patient.objects.get(id=id)
        except Exception:

            messages.error(request, 'Patient not found')
            return render(request, 'error.html')
        if p.med_test1_report:
            messages.error(request, 'report already existed please update or take print')
            return redirect(reverse('patient_app:read_patient')+f'?id={id}')
        

        
        latest_id=Med_test1_report.objects.latest('id')
        echo=Med_test1_report()
        echo.lab_no=latest_id.id+1
        # echo.validated_by=request.user.username

        echo.t1_1=form_data.get('t1_1', None)

        echo.t1=form_data.get('t1', None)
        echo.t2=form_data.get('t2', None)
        echo.t3=form_data.get('t3', None)
        echo.t4=form_data.get('t4', None)
        echo.t5=form_data.get('t5', None)
        echo.t6=form_data.get('t6', None)
        echo.t7=form_data.get('t7', None)
        echo.t8=form_data.get('t8', None)
        echo.t9=form_data.get('t9', None)
        echo.t10=form_data.get('t10', None)
        echo.t11=form_data.get('t11', None)
        echo.t12=form_data.get('t12', None)
        echo.t13=form_data.get('t13', None)

        # RWMA
        echo.t14=form_data.get('t14', None)
        # if echo.t14!='Absent':
        echo.t14_1=', '.join(form_data.getlist('t14_1', None)) if form_data.getlist('t14_1', None) else ''
        echo.t14_2=', '.join(form_data.getlist('t14_2', None)) if form_data.getlist('t14_2', None) else ''
        echo.t14_3=', '.join(form_data.getlist('t14_3', None)) if form_data.getlist('t14_3', None) else ''
        echo.t14_4=', '.join(form_data.getlist('t14_4', None)) if form_data.getlist('t14_4', None) else ''

        # mitral morphology
        echo.t15=', '.join(form_data.getlist('t15', None)) if form_data.getlist('t15', None) else ''
        if 'Normal' in echo.t15:
            echo.t15='Normal'

        # if echo.t15 != 'Normal':
        echo.t15_1=', '.join(form_data.getlist('t15_1', None)) if form_data.getlist('t15_1', None) else ''
        echo.t15_2=', '.join(form_data.getlist('t15_2', None)) if form_data.getlist('t15_2', None) else ''
        
        echo.t16=form_data.get('t16', None)
        echo.t17=form_data.get('t17', None)
        echo.t18=form_data.get('t18', None)
        echo.t19=form_data.get('t19', None)
        echo.t20=form_data.get('t20', None)
        echo.t21=form_data.get('t21', None)
        echo.t22=form_data.get('t22', None)

        # Mitral Stenosis
        echo.t23=form_data.get('t23', None)
        # if echo.t23 != 'Absent':
        echo.t23_1=form_data.get('t23_1', '')
        echo.t23_2=form_data.get('t23_2', '')
        echo.t23_3=form_data.get('t23_3', '')
        echo.t23_4=form_data.get('t23_4', '')
        echo.t23_5=form_data.get('t23_5', '')

        # Mitral Regurgitation
        echo.t24=form_data.get('t24', None)
        echo.t24_1=form_data.get('t24_1', None)
        echo.t24_2=form_data.get('t24_2', None)

        # Aortic Morphology
        echo.t25=', '.join(form_data.getlist('t25', None)) if form_data.getlist('t25', None) else ''
        echo.t25.replace('Abnormal', '')

        echo.t26=form_data.get('t26', None)

        # Aortic stenosis
        echo.t27=form_data.get('t27', None)
        echo.t27_1=form_data.get('t27_1', None)
        echo.t27_2=form_data.get('t27_2', None)
        echo.t27_3=form_data.get('t27_3', None)
        echo.t27_4=form_data.get('t27_4', None)
        echo.t27_5=form_data.get('t27_5', None)
        echo.t27_6=form_data.get('t27_6', None)

        # Aortic regurgitation
        echo.t28=form_data.get('t28', None)
        echo.t28_1=form_data.get('t28_1', None)
        echo.t28_2=form_data.get('t28_2', None)
        echo.t28_3=form_data.get('t28_3', None)

        # TRISCUPID Morphology
        echo.t29=', '.join(form_data.getlist('t29', None)) if form_data.getlist('t29', None) else ''
        echo.t29.replace('Abnormal', '')

        # Triscupid Stenosis
        echo.t30=form_data.get('t30', None)
        echo.t30_1=form_data.get('t30_1', None)
        echo.t30_2=form_data.get('t30_2', None)

        # Triscupid Regurgitation
        echo.t31=form_data.get('t31', None)
        echo.t31_1=form_data.get('t31_1', None)
        echo.t31_2=form_data.get('t31_2', None)
        echo.t31_3=form_data.get('t31_3', None)
        echo.t31_4=form_data.get('t31_4', None)

        # Pulmonary Morphology
        echo.t32=', '.join(form_data.getlist('t32', None)) if form_data.getlist('t32', None) else ''
        echo.t32.replace('Abnormal', '')

        echo.t33=form_data.get('t33', None)

        # Pulmonary Stenosis
        echo.t34=form_data.get('t34', None)
        echo.t34_1=form_data.get('t34_1', None)
        echo.t34_2=form_data.get('t34_2', None)

        # Pulmonary Regurgitation
        echo.t35=form_data.get('t35', None)
        echo.t35_1=form_data.get('t35_1', None)
        echo.t35_2=form_data.get('t35_2', None)

        # Pulmonary Artery
        echo.t36=form_data.get('t36', None)
        echo.t36_1=form_data.get('t36_1', None)
        echo.t36_2=form_data.get('t36_2', None)
        echo.t36_3=form_data.get('t36_3', None)

        echo.t37=form_data.get('t37', "")
        echo.t38=form_data.get('t38', "")
        echo.t39=form_data.get('t39', "")

        echo.save()
        p.med_test1_report=echo
        p.save()

        messages.success(request, 'report created successfully.')
        return redirect(reverse('med_test1_app:read_med_test1_report')+f'?id={id}')
    else:
        # print('method not allowed')
        messages.error(request, 'Method not allowed')
        return render(request, 'error.html')



# @permission_required('med_test1_app.view_echoreport')
# def read_med_test1_report(request):
def read_med_test1_report(request):
    if request.method=='GET':
        id=request.GET.get('id')
        try:
            p=Patient.objects.get(id=id)
        except Exception:
            messages.error(request, 'Patient not found')
            return redirect(reverse('patient_app:create_patient'))
        if p.med_test1_report:
            # print(p.med_test1_report.t37)
            if p.med_test1_report.t1_1:
                return render(request, 'med_test1_app/helper/read.html', {'patient':p})
            return render(request, 'med_test1_app/read_med_test1_report.html', {'patient':p})
        else:
            messages.error(request, 'report does not found')
            return redirect(reverse('patient_app:read_patient')+f'?id={id}')
    else:
        messages.error(request, 'Method not allowed')
        return render(request, 'error.html')
        


# @permission_required('med_test1_app.change_echoreport')

def update_med_test1_report(request):
    if request.method=='GET':
        id=request.GET.get('id')
        try:
            p=Patient.objects.get(id=id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        if p.med_test1_report:
            if p.med_test1_report.t1_1:
                return render(request, 'med_test1_app/helper/update.html', {'patient':p})
            return render(request, 'med_test1_app/update_med_test1_report.html', {'patient':p})
        else:
            messages.error(request, 'report does not found please create first')
            return redirect(reverse('patient_app:read_patient')+f'?id={id}')


    elif request.method=='POST':
        # create echo report with id
        form_data=request.POST
        # print(form_data)
        # return render(request, 'error.html', {'form_data':form_data})
        id=form_data.get('id', None)
        try:
            p=Patient.objects.get(id=id)
        except Exception:

            messages.error(request, 'Patient not found')
            return render(request, 'error.html')
        if not p.med_test1_report:
            messages.error(request, 'report does not existed')
            return redirect(reverse('med_test1_app:index'))
        
        # latest_id=Med_test1_report.objects.latest('id')
        # echo=Med_test1_report()
        echo=p.med_test1_report
        # echo.lab_no=latest_id.id+1
        # echo.validated_by=request.user.username

        echo.t1_1=form_data.get('t1_1', None)

        echo.t1=form_data.get('t1', None)
        echo.t2=form_data.get('t2', None)
        echo.t3=form_data.get('t3', None)
        echo.t4=form_data.get('t4', None)
        echo.t5=form_data.get('t5', None)
        echo.t6=form_data.get('t6', None)
        echo.t7=form_data.get('t7', None)
        echo.t8=form_data.get('t8', None)
        echo.t9=form_data.get('t9', None)
        echo.t10=form_data.get('t10', None)
        echo.t11=form_data.get('t11', None)
        echo.t12=form_data.get('t12', None)
        echo.t13=form_data.get('t13', None)

        # RWMA
        echo.t14=form_data.get('t14', None)
        # if echo.t14!='Absent':
        echo.t14_1=', '.join(form_data.getlist('t14_1', None)) if form_data.getlist('t14_1', None) else ''
        echo.t14_2=', '.join(form_data.getlist('t14_2', None)) if form_data.getlist('t14_2', None) else ''
        echo.t14_3=', '.join(form_data.getlist('t14_3', None)) if form_data.getlist('t14_3', None) else ''
        echo.t14_4=', '.join(form_data.getlist('t14_4', None)) if form_data.getlist('t14_4', None) else ''

        # mitral morphology
        echo.t15=', '.join(form_data.getlist('t15', None)) if form_data.getlist('t15', None) else ''
        if echo.t15!='Abnormal':
            echo.t15.replace('Abnormal,', '')
        # if echo.t15 != 'Normal':
        echo.t15_1=', '.join(form_data.getlist('t15_1', None)) if form_data.getlist('t15_1', None) else ''
        echo.t15_2=', '.join(form_data.getlist('t15_2', None)) if form_data.getlist('t15_2', None) else ''

        echo.t16=form_data.get('t16', None)
        echo.t17=form_data.get('t17', None)
        echo.t18=form_data.get('t18', None)
        echo.t19=form_data.get('t19', None)
        echo.t20=form_data.get('t20', None)
        echo.t21=form_data.get('t21', None)
        echo.t22=form_data.get('t22', None)

        # Mitral Stenosis
        echo.t23=form_data.get('t23', None)
        # if echo.t23 != 'Absent':
        echo.t23_1=form_data.get('t23_1', '')
        echo.t23_2=form_data.get('t23_2', '')
        echo.t23_3=form_data.get('t23_3', '')
        echo.t23_4=form_data.get('t23_4', '')
        echo.t23_5=form_data.get('t23_5', '')

        # Mitral Regurgitation
        echo.t24=form_data.get('t24', None)
        echo.t24_1=form_data.get('t24_1', None)
        echo.t24_2=form_data.get('t24_2', None)

        # Aortic Morphology
        echo.t25=', '.join(form_data.getlist('t25', None)) if form_data.getlist('t25', None) else ''
        echo.t25.replace('Abnormal', '')

        echo.t26=form_data.get('t26', None)

        # Aortic stenosis
        echo.t27=form_data.get('t27', None)
        echo.t27_1=form_data.get('t27_1', None)
        echo.t27_2=form_data.get('t27_2', None)
        echo.t27_3=form_data.get('t27_3', None)
        echo.t27_4=form_data.get('t27_4', None)
        echo.t27_5=form_data.get('t27_5', None)
        echo.t27_6=form_data.get('t27_6', None)

        # Aortic regurgitation
        echo.t28=form_data.get('t28', None)
        echo.t28_1=form_data.get('t28_1', None)
        echo.t28_2=form_data.get('t28_2', None)
        echo.t28_3=form_data.get('t28_3', None)

        # TRISCUPID Morphology
        echo.t29=', '.join(form_data.getlist('t29', None)) if form_data.getlist('t29', None) else ''
        echo.t29.replace('Abnormal', '')

        # Triscupid Stenosis
        echo.t30=form_data.get('t30', None)
        echo.t30_1=form_data.get('t30_1', None)
        echo.t30_2=form_data.get('t30_2', None)

        # Triscupid Regurgitation
        echo.t31=form_data.get('t31', None)
        echo.t31_1=form_data.get('t31_1', None)
        echo.t31_2=form_data.get('t31_2', None)
        echo.t31_3=form_data.get('t31_3', None)
        echo.t31_4=form_data.get('t31_4', None)

        # Pulmonary Morphology
        echo.t32=', '.join(form_data.getlist('t32', None)) if form_data.getlist('t32', None) else ''
        echo.t32.replace('Abnormal', '')

        echo.t33=form_data.get('t33', None)

        # Pulmonary Stenosis
        echo.t34=form_data.get('t34', None)
        echo.t34_1=form_data.get('t34_1', None)
        echo.t34_2=form_data.get('t34_2', None)

        # Pulmonary Regurgitation
        echo.t35=form_data.get('t35', None)
        echo.t35_1=form_data.get('t35_1', None)
        echo.t35_2=form_data.get('t35_2', None)

        # Pulmonary Artery
        echo.t36=form_data.get('t36', None)
        echo.t36_1=form_data.get('t36_1', None)
        echo.t36_2=form_data.get('t36_2', None)
        echo.t36_3=form_data.get('t36_3', None)

        # t37=form_data.get('t37', None)
        # t37=linebreaks(t37)
        echo.t37=form_data.get('t37', None)
        # echo.t37=t37

        echo.t38=form_data.get('t38', None)
        echo.t39=form_data.get('t39', None)

        echo.save()
        # p.med_test1_report=echo
        p.save()

        messages.success(request, 'report updated successfully.')
        return redirect(reverse('med_test1_app:read_med_test1_report')+f'?id={id}')
    else:
        # print('method not allowed')
        messages.error(request, 'Method not allowed')
        return render(request, 'error.html')


# @permission_required('med_test1_app.delete_echoreport')
def delete_med_test1_report(request):
    if request.method=='GET':
        return render(request, 'med_test1_app/delete_med_test1_report.html')
    elif request.method=='POST':
        id=request.POST.get('id')
        # delete report in db
        p=Patient.objects.get(id=id)
        # p.echoJson={}
        p.save()
        messages.success(request, 'report deleted successfully')
        return render(request, 'index.html')
    else:
        print('method not allowed')
        return render(request, 'error.html')

def print_report(request):
    date=datetime.datetime.now()
    # reports=Med_test1_report.objects.filter(created_date=date)
    patients=Patient.objects.filter(Q(med_test1_report__isnull=False) & Q(med_test1_report__validated_by__isnull=False))
    return render(request, 'med_test1_app/print_report.html', {'patients':patients})



def validate(request):
    if request.method=='POST':
        form_data=request.POST
        id=form_data.get('id', None)
        try:
            p=Patient.objects.get(id=id)
            username=request.user.username
            # print(p)
            # print(p.Med_test1_report.validated_by)
            p.med_test1_report.validated_by=username
            p.med_test1_report.save()
            p.save()
            # print(p.Med_test1_report.validated_by)

            messages.success(request, 'Report validated successfully.')
            return redirect(reverse('med_test1_app:read_med_test1_report')+f'?id={id}')
            
        except Exception:
            print('patient or echo report does not exist')
            messages.error(request, 'patient or echo report does not exist')
            # return redirect(request.META.get('HTTP_REFERER'))
            return render(request, 'error.html')


# views.py

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_pdf(request):
    # Example data, replace this with your actual data
    id=request.GET.get('id')
    p=Patient.objects.get(id=id)
    # try:
    # except Exception:
    #     messages.error(request, 'Patient not found')
    #     return redirect(reverse('patient_app:create_patient'))
    data = {
        'patient': p,
        
    }

    # Render the Django template to HTML
    html_string = render_to_string('test.html', data)

    # Create a PDF buffer and render the HTML into PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sample_pdf.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response





def generate_pdf_new(request):
    # Create a file-like buffer to receive PDF data.
    id=request.GET.get('id', None)
    if not id:
        messages.error(request, 'provide patient id')
        return redirect(reverse('patient_app:print_report'))
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        # print('some error')
        messages.error(request, 'patient does not exist')
        return redirect(reverse('patient_app:print_report'))
    if not p.med_test1_report:
        messages.error(request, 'report does not exist')
        return redirect(reverse('patient_app:print_report'))
    
    r=p.med_test1_report


    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50)


    # header image
    # # Get the relative path to the image within the static folder
    # image_relative_path = 'hn.jpg'

    # # Construct the full image path using STATIC_ROOT
    # image_path = os.path.join(settings.STATICFILES_DIRS[0], image_relative_path)
    # # image_path='static/hn.jpg'
    # img = utils.ImageReader(image_path)
    # img_width, img_height = img.getSize()

    # # Calculate the desired width and height of the image in the PDF
    # pdf_width = 400  # Replace this with your desired width in points (1 inch = 72 points)
    # pdf_height = (img_height * pdf_width) / img_width

    # # Create the Image object with the calculated dimensions
    # # image = Image(image_path, width=pdf_width, height=pdf_height)
    # image = Image(image_path)

    # table as header of the page
    # Define heading text and style
    heading_text = "HN DIAGNOSTIC CENTER"
    heading_style = getSampleStyleSheet()["Heading1"]
    heading_style.alignment = 1  # Set alignment to center

    # Define image path and size
    # image_path = "/content/aiimslogo2.jpeg"  # Replace with your image path
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'aiimslogo2.jpeg')
    l_path = os.path.join(settings.STATICFILES_DIRS[0], 'l.jpg')
    r_path = os.path.join(settings.STATICFILES_DIRS[0], 'r.jpg')
    image_width = 80
    image_height = 80

    # Create a Paragraph object for the heading
    heading1 = Paragraph(heading_text, style=heading_style)

    text="Phulwari Sharif, Patna, Bihar <br/> PIN 800001 <br/> Mob. no. 99999999"
    hs=getSampleStyleSheet()["Heading3"]
    hs.alignment=1
    h2=Paragraph(text,style=hs)


    # Create an Image object for the image
    # image = Image(image_path, width=image_width, height=image_height)
    image = Image(image_path, width=image_width, height=image_height)
    l_image=Image(l_path, width=image_width, height=image_height)
    r_image=Image(r_path, width=image_width, height=image_height)

    # Create a Table to hold the image and the heading
    # data = [[image, [heading1, h2]], ["", h2]]
    data = [[l_image, [heading1, h2], r_image]]
    table = Table(data)

    # Define table style
    style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Align the image to the left
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all cells
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ])

    # Apply table style
    table.setStyle(style)

    # Set column widths to control positioning
    table._argW = [image_width, doc.width - 2*image_width, image_width]


    data=[
        ['Patient ID', p.id, 'Accession No. ', r.lab_no, 'Registration Date', p.created_date],
        ['Patient Name', p.name, 'Age/Sex', f'{p.age} Yr /{p.gender}', 'Procedure Date', r.created_date],
        ['Mob no.', p.mob_no, '', 'Reffered By', r.reffered_by, ''],
        ['Address', p.address, '', '', '', ''],

    ]

    # Define table style
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ])



    t=Table(data, colWidths=[doc.width / 6.0] * 6)
    t.setStyle(style)

    heading_text = "Echocardiography"
    heading_style = getSampleStyleSheet()["Heading2"]
    heading_style.alignment = 1  # Set alignment to center

    # Create a Paragraph object for the heading
    heading = Paragraph(heading_text, style=heading_style)



    # mitral valve

    # Define heading text and style
    heading_text = "Mitral Valve"
    heading_style = getSampleStyleSheet()["Heading4"]
    heading_style.alignment = 1  # Set alignment to center

    # Create a Paragraph object for the heading
    heading1 = Paragraph(heading_text, style=heading_style)

    t1_data=[]
    t1_data.append(['Morphology', r.t15, '', ''])
    if r.t15!='Normal':
        t1_data.append(['AML', r.t15_1, '', ''])
        t1_data.append(['PML', r.t15_2, '', ''])
    t1_data.append(['Doppler', 'E Wave (cm/s)', 'A wave (cm/s)', 'DT'])
    t1_data.append(['', r.t16, r.t17, r.t18])
    t1_data.append(['Tissue Doppler', 'E"', 'A"', 'E/e"'])
    t1_data.append(['', r.t19, r.t20, r.t21])
    t1_data.append(['Diastolic Function', r.t22,'', ''])
    t1_data.append(['Mitral stenosis', r.t23, '', ''])
    if r.t23!='Absent':
        t1_data.append(['', 'Gradient', 'Peak Diastolic', 'Mean Diastolic (mmHg)'])
        t1_data.append(['', '', r.t23_1, r.t23_2])
        t1_data.append(['', 'MVA', 'By Planimetry(cmsq)', 'By PHT(cmsq)'])
        t1_data.append(['', '', r.t23_3, r.t23_4])
        t1_data.append(['Mitral Annulus(cm)', r.t23_5, '', ''])
    t1_data.append(['Mitral Regurgitation', r.t24, '', ''])
    if r.t24!='Absent':
        t1_data.append(['', 'A4C LA Area(cmsq)', 'JetArea(cmsq)', ''])
        t1_data.append(['', r.t24_1, r.t24_2, ''])

    t1=Table(t1_data, colWidths=[doc.width / 4.0] * 4)
    t1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))

    for i in range(len(t1_data)):
        t1.setStyle(
            TableStyle([
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (0, i), colors.black),
            ])
        )

    # aortic valve

    # Define heading text and style
    heading_text = "Aortic Valve"
    heading_style = getSampleStyleSheet()["Heading4"]
    heading_style.alignment = 1  # Set alignment to center


    # Create a Paragraph object for the heading
    heading2 = Paragraph(heading_text, style=heading_style)

    t2_data=[]
    t2_data.append(['Morphology', r.t25, '', ''])
    t2_data.append(['Doppler', 'Aortic peak systolic velocity (cm/sec)', '', ''])
    t2_data.append(['', r.t26, '', ''])
    t2_data.append(['Aortic Stenosis', r.t27, '', ''])
    if r.t27!='Absent':
        t2_data.append(['', 'Gradient', 'Peak Systolic(mmHg)', 'Mean Systolic(mmHg)'])
        t2_data.append(['', '', r.t27_1, r.t27_2])
        t2_data.append(['', 'AVA', 'By Planimetry(cmsq)', 'Aortic Annulus(cm)'])
        t2_data.append(['', '', r.t27_3, r.t27_4])
        t2_data.append(['', '', 'Aorta at Sinus (cm)', 'Ascending Arota at STJ (cm)'])
        t2_data.append(['', '', r.t27_5, r.t27_6])
    t2_data.append(['Aortic Regurgitation', r.t28, '', ''])
    if r.t28!='Absent':
        t2_data.append(['', 'AR Jet PHT(msec)', 'AR Vena Contractra(mm)', 'AR Jet(msec)'])
        t2_data.append(['', r.t28_1, r.t28_2, r.t28_3])

    t2=Table(t2_data, colWidths=[doc.width / 4.0] * 4)
    t2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))

    for i in range(len(t2_data)):
        t2.setStyle(
            TableStyle([
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (0, i), colors.black),
            ])
        )

    # triscupid valve

    # Define heading text and style
    heading_text = "Triscupid Valve"
    heading_style = getSampleStyleSheet()["Heading4"]
    heading_style.alignment = 1  # Set alignment to center


    # Create a Paragraph object for the heading
    heading3 = Paragraph(heading_text, style=heading_style)

    t3_data=[]
    t3_data.append(['Morphology', r.t29, '', ''])
    # t3_data.append(['Doppler', 'Peak Systolic Velocity (cm/sec)', '', ''])
    # t3_data.append(['', '222', '', ''])
    t3_data.append(['Triscupid Stenosis', r.t30, '', ''])
    if r.t30!='Absent':
        t3_data.append(['', 'Gradient', 'Peak Diastolic(mmHg)', 'Mean Diastolic(mmHg)'])
        t3_data.append(['', '', r.t30_1, r.t30_2])
    t3_data.append(['Triscupid  Regurgitation', r.t31, '', ''])
    if r.t31!='Absent':
        t3_data.append(['', 'RVSP(mmHg)=RAP+', 'TRJV(cm/sec)', ''])
        t3_data.append(['', r.t31_1, r.t31_2, ''])
        t3_data.append(['', 'Pulmonary Hypertension', 'Triscupid Annulus(cm)', ''])
        t3_data.append(['', r.t31_3, r.t31_4, ''])


    t3=Table(t3_data, colWidths=[doc.width / 4.0] * 4)
    t3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))

    for i in range(len(t3_data)):
        t3.setStyle(
            TableStyle([
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (0, i), colors.black),
            ])
        )


    # PULMONARY VALVE
    heading_text = "Pulmonary Valve"
    heading_style = getSampleStyleSheet()["Heading4"]
    heading_style.alignment = 1  # Set alignment to center


    # Create a Paragraph object for the heading
    heading4 = Paragraph(heading_text, style=heading_style)

    t4_data=[]
    t4_data.append(['Morphology', r.t32, '', ''])
    t4_data.append(['Doppler', r.t33, '', ''])
    t4_data.append(['Pulmonary Stenosis', r.t34, '', ''])
    if r.t34!='Absent':
        t4_data.append(['', 'Gradient', 'Peak Systolic(mmHg)', 'Mean Systolic(mmHg)'])
        t4_data.append(['', '', r.t34_1, r.t34_2])
    t4_data.append(['Pulmonary Regurgitation', r.t35, '', ''])
    if r.t35!='Absent':
        t4_data.append(['', 'Early DG(mmHg)', 'End DG(mmHg)', ''])
        t4_data.append(['', r.t35_1, r.t35_2, ''])
    t4_data.append(['Pulmonary Artery', r.t36, '', ''])
    if r.t36!='Normal':
        t4_data.append(['', 'MPA(mm)', 'RPA(mm)', 'LPA(mm)'])
        t4_data.append(['', r.t36_1, r.t36_2, r.t36_3])
    # t4_data.append(['Remarks', Paragraph(r.t37.replace('</p>', '</p><br/>')), '', ''])
    # t4_data.append(['Impression', Paragraph(r.t38.replace('</p>', '</p><br/>')), '', ''])
    # t4_data.append(['Plan', Paragraph(r.t39.replace('</p>', '</p><br/>')), '', ''])



    t4=Table(t4_data, colWidths=[doc.width / 4.0] * 4)
    t4.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))

    for i in range(len(t4_data)):
        t4.setStyle(
            TableStyle([
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (0, i), colors.black),
            ])
        )


    # MEASUREMENTS	VALUES

    # t5_data=[]
    # t5_data.append(['MEASUREMENTS', 'VALUES', 'NORMAL Val.', 'MEASUREMENTS', 'VALUES', 'NORMAL Val.'])
    # t5_data.append(['IVsd', r.t1, '(0.6-1.0)cm', 'Aorta', r.t2, '(2.0-4.0)cm'])
    # t5_data.append(['LVIDd', r.t3, '(3.6-5.5)cm', 'LA', r.t4, '(2.0-4.0)cm'])
    # t5_data.append(['LVPWd', r.t6, '(0.6-1.0)cm', 'RVIDd(Basal)', r.t6, '(2.5-4.1)cm'])
    # t5_data.append(['IVss', r.t7, '', 'RVIDd(Mid)', r.t8, '(1.9-3.5)cm'])
    # t5_data.append(['LVIDs', r.t9, '(2.0-4.0)cm', 'TAPSE', r.t10, '(>=1.7)cm'])
    # t5_data.append(['LVPWs', r.t11, '', 'FS', r.t12, '(>=25%)'])
    # t5_data.append(['LVEF', r.t13, '(>=50%)', '', '', ''])

    t5_data=[]
    t5_data.append(['MEASUREMENTS', 'VALUES', 'NORMAL Val.', 'MEASUREMENTS', 'VALUES', 'NORMAL Val.'])
    t5_data.append(['IVsd', r.t1, '(0.6-1.0)cm', 'IVss', r.t7, '(0.7-1.2)cm'])
    t5_data.append(['LVIDd', r.t3, '(3.6-5.5)cm', 'LVIDs', r.t9, '(2.0-4.0)cm'])
    t5_data.append(['LVPWd', r.t6, '(0.6-1.0)cm', 'LVPWs', r.t11, '(0.8-1.2)cm'])
    t5_data.append(['LVEF', r.t13, '(>=50%)', 'FS', r.t12, '(>=25%)'])

    t5_data.append(['RWMA', r.t14, '', '', '', ''])
    if r.t14!='Absent':
        t5_data.append(['BASAL LV', r.t14_1, '', '', '', ''])
        t5_data.append(['MID LV', r.t14_2, '', '', '', ''])
        t5_data.append(['APICAL LV', r.t14_3, '', '', '', ''])
        t5_data.append(['LV APEX', r.t14_4, '', '', '', ''])

    t5_data.append(['Aorta', r.t2, '(2.0-4.0)cm', 'LA', r.t4, '(2.0-4.0)cm'])
    t5_data.append(['TAPSE', r.t10, '(>=1.7)cm', '', '', ''])

    

    t5=Table(t5_data, colWidths=[doc.width / 6.0] * 6)
    t5.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))

    for i in range(len(t5_data)):
        t5.setStyle(
            TableStyle([
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (0, i), colors.black),
            ])
        )

    # Define a style for the paragraph
    my_style = ParagraphStyle(
        name='MyStyle',
        fontName='Helvetica',
        fontSize=12,
        leading=14,
        textColor='black',
        leftIndent=20,
        rightIndent=20,
    )
    # my_style= getSampleStyleSheet()['Normal']
    # text=f"<pre>{r.t37}</pre>"
    # text=f"<html><body>{r.t37}</body></html>"
    # para = Paragraph(text, my_style)
    # text=add_br_after_closing_tags(r.t37)
    # print(text)
    # text=r.t37.replace('</p>', '</p><br/>')
    # print(text)
    # para = Paragraph(text)


    # '<p><strong>Remarks : </strong></p><br/>'+
    para1=Paragraph('<p><strong>Remarks : </strong></p><br/>'+r.t37.replace('</p>', '</p><br/>'))
    para2=Paragraph('<p><strong>Impression : </strong></p><br/>'+r.t38.replace('</p>', '</p><br/>'))
    para3=Paragraph('<p><strong>Plan : </strong></p><br/>'+r.t39.replace('</p>', '</p><br/>'))






    # Build the document with the table
    elements=[]
    elements = [table, Spacer(1, 12), t, heading, Spacer(1, 12), t5, heading1, t1, heading2, t2, heading3, t3, heading4, t4, para1, para2, para3]
    if r.t1_1:
        elements=[table, Spacer(1, 15), t, heading, Spacer(1, 12), Paragraph(r.t1_1.replace('<br>', '<br/>').replace('<p>&nbsp;</p>', '<br/>').replace('</p>', '</p><br/>'))]
    doc.build(elements)

    # File buffer is now at position 0, so we can "rewind" it.
    buffer.seek(0)

    # Create a PDF response object, specifying the content type as PDF.
    response = HttpResponse(content_type='application/pdf')

    # Set the filename of the PDF.
    response['Content-Disposition'] = f'attachment; filename="{p.id}.pdf"'

    # Write the PDF buffer to the response.
    response.write(buffer.getvalue())

    return response


def test(request):
    if request.method=='GET':
        messages.error(request, 'some test messages get')
        return render(request, 'test.html')
    if request.method=='POST':
        messages.error(request, 'some test messages post')
        return HttpResponse('ok', status=505)
    
# def add_br_after_closing_tags(html_content):
#     new_html = ""
#     for i in range(len(html_content)):
#         if html_content[i] == ">" and i > 0 and html_content[i - 1] == "/":
#             new_html += " /><br>"
#         else:
#             new_html += html_content[i]
#     return new_html



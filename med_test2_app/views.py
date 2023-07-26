from doctest import REPORT_CDIFF
from typing import Self
from django.views import View

from cgi import test
from email import message
from email.policy import default
from django.shortcuts import render, redirect, reverse, resolve_url
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
# from symbol import arglist
from .models import Med_test2_1_report, Med_test2_2_report, Med_test2_3_report, Med_test2_4_report, Med_test2_5_report


from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


def index(request):
    return render(request, 'med_test2_app/index.html')


def create(request, n):
    if n==1:
        return create_med_test2_1_report(request)
    return HttpResponse('method not allowed.')
    

def read(request, n):
    if n==1:
        return read_med_test2_1_report(request)
    return HttpResponse('method not allowed.')

def update(request, n):
    if n==1:
        return update_med_test2_1_report(request)
    return HttpResponse("method not allowed")

def validate(request, n):
    if n==1:
        return validate_med_test2_1_report(request)
    return HttpResponse("method not allowed.")

def pdf(request, n):
    if n==1:
        return generate_pdf_med_test2_1_report(request)
    return HttpResponse("method not allowed.")




def get_read_url(self):
    if self.report==Med_test2_1_report:
        return reverse('med_test2_app:Read_1')+f"?id={self.id}"
    if self.report==Med_test2_2_report:
        return reverse('med_test2_app:Read_2')+f"?id={self.id}"
    if self.report==Med_test2_3_report:
        return reverse('med_test2_app:Read_3')+f"?id={self.id}"
    if self.report==Med_test2_4_report:
        return reverse('med_test2_app:Read_4')+f"?id={self.id}"
    if self.report==Med_test2_5_report:
        return reverse('med_test2_app:Read_5')+f"?id={self.id}"
def get_create_url(self):
    if self.report==Med_test2_1_report:
        return reverse('med_test2_app:Create_1')+f"?id={self.id}"
    if self.report==Med_test2_2_report:
        return reverse('med_test2_app:Create_2')+f"?id={self.id}"
    if self.report==Med_test2_3_report:
        return reverse('med_test2_app:Create_3')+f"?id={self.id}"
    if self.report==Med_test2_4_report:
        return reverse('med_test2_app:Create_4')+f"?id={self.id}"
    if self.report==Med_test2_5_report:
        return reverse('med_test2_app:Create_5')+f"?id={self.id}"


class Create(View):
    id=None
    report=Med_test2_1_report
    def get(self, request):
        self.id=request.GET.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        # if hasattr(p, self.report):
        #     messages.error(request, 'report already existed please update or take print')
        #     return redirect(reverse('med_test2_app:read_med_test2_1_report'))
        try:
            r=self.report.objects.get(patient=p)
            messages.error(request, 'report already existed please update or take print')
            return redirect(self.read_url())
        except Exception:
            return render(request, self.get_template(), {'patient':p})
    def post(self, request):
        self.id=request.POST.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            messages.error(request, 'report already existed please update or take print')
            return redirect(self.read_url())
        except Exception:
            r=self.report.objects.create(patient=p)
            try:
                latest_id=self.report.objects.latest('id').id
            except Exception:
                latest_id=0
            r.lab_no=latest_id+1
            r.t1=request.POST.get('t1', None)
            r.save()
            messages.success(request, 'report created successfully.')
            return redirect(self.read_url())
    def get_template(self):
        if self.report==Med_test2_1_report:
            return 'med_test2_app/create_med_test2_1_report.html'
        if self.report==Med_test2_2_report:
            return 'med_test2_app/create_med_test2_2_report.html'
        if self.report==Med_test2_3_report:
            return 'med_test2_app/create_med_test2_3_report.html'
        if self.report==Med_test2_4_report:
            return 'med_test2_app/create_med_test2_4_report.html'
        if self.report==Med_test2_5_report:
            return 'med_test2_app/create_med_test2_5_report.html'
        return 'error.html'
        # match self.report:
        #     case Med_test2_1_report:
        #         return 'med_test2_app/create_med_test2_1_report.html'
        #     case Med_test2_2_report:
        #         return 'med_test2_app/create_med_test2_2_report.html'
        #     case Med_test2_3_report:
        #         return 'med_test2_app/create_med_test2_3_report.html'
        #     case Med_test2_4_report:
        #         return 'med_test2_app/create_med_test2_4_report.html'
        #     case Med_test2_5_report:
        #         return 'med_test2_app/create_med_test2_5_report.html'
        #     case _:
        #         return 'error.html'

    def read_url(self):
        if self.report==Med_test2_1_report:
            return reverse('med_test2_app:Read_1')+f"?id={self.id}"
        if self.report==Med_test2_2_report:
            return reverse('med_test2_app:Read_2')+f"?id={self.id}"
        if self.report==Med_test2_3_report:
            return reverse('med_test2_app:Read_3')+f"?id={self.id}"
        if self.report==Med_test2_4_report:
            return reverse('med_test2_app:Read_4')+f"?id={self.id}"
        if self.report==Med_test2_5_report:
            return reverse('med_test2_app:Read_5')+f"?id={self.id}"

class Read(View):
    id=None
    report=Med_test2_1_report
    def get(self, request):
        self.id=request.GET.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            return render(request, self.get_template(), {'patient':p})
        except Exception:
            messages.error(request, 'report not found')
            return redirect(self.create_url())
    

    def get_template(self):
        if self.report==Med_test2_1_report:
            return 'med_test2_app/read_med_test2_1_report.html'
        if self.report==Med_test2_2_report:
            return 'med_test2_app/read_med_test2_2_report.html'
        if self.report==Med_test2_3_report:
            return 'med_test2_app/read_med_test2_3_report.html'
        if self.report==Med_test2_4_report:
            return 'med_test2_app/read_med_test2_4_report.html'
        if self.report==Med_test2_5_report:
            return 'med_test2_app/read_med_test2_5_report.html'
        return 'error.html'
    
    def create_url(self):
        if self.report==Med_test2_1_report:
            return reverse('med_test2_app:Create_1')+f"?id={self.id}"
        if self.report==Med_test2_2_report:
            return reverse('med_test2_app:Create_2')+f"?id={self.id}"
        if self.report==Med_test2_3_report:
            return reverse('med_test2_app:Create_3')+f"?id={self.id}"
        if self.report==Med_test2_4_report:
            return reverse('med_test2_app:Create_4')+f"?id={self.id}"
        if self.report==Med_test2_5_report:
            return reverse('med_test2_app:Create_5')+f"?id={self.id}"


class Update(View):
    id=None
    report=Med_test2_1_report
    def get(self, request):
        self.id=request.GET.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            return render(request, self.get_template(), {'patient':p})
        except Exception:
            messages.error(request, 'report not found')
            return redirect(get_create_url({'id':self.id, 'report':self.report}))
    def post(self, request):
        self.id=request.POST.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            r.t1=request.POST.get('t1', r.t1)
            r.save()
            messages.success(request, 'report updated successfully.')
            return redirect(get_read_url({'id':self.id, 'report':self.report}))
        except Exception:
            messages.error(request, 'report not found')
            return redirect(get_create_url({'id':self.id, 'report':self.report}))
    def get_template(self):
        if self.report==Med_test2_1_report:
            return 'med_test2_app/update_med_test2_1_report.html'
        if self.report==Med_test2_2_report:
            return 'med_test2_app/update_med_test2_2_report.html'
        if self.report==Med_test2_3_report:
            return 'med_test2_app/update_med_test2_3_report.html'
        if self.report==Med_test2_4_report:
            return 'med_test2_app/update_med_test2_4_report.html'
        if self.report==Med_test2_5_report:
            return 'med_test2_app/update_med_test2_5_report.html'
        return 'error.html'
    

class Validate(View):
    id=None
    report=Med_test2_1_report
    def post(self, request):
        self.id=request.POST.get('id', None)
        try:
            p=Patient.objects.get(id=id)
        except Exception:
            messages.error(request, 'Patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            r.validated_by=request.user.username
            r.save()
            messages.success(request, 'report validated successfully.')
            return redirect(self.get_read_url())
        except Exception:
            messages.error(request, 'report not found')
            return redirect(self.get_create_url())
        
    def get_read_url(self):
        if self.report==Med_test2_1_report:
            return reverse('med_test2_app:Read_1')+f"?id={self.id}"
        if self.report==Med_test2_2_report:
            return reverse('med_test2_app:Read_2')+f"?id={self.id}"
        if self.report==Med_test2_3_report:
            return reverse('med_test2_app:Read_3')+f"?id={self.id}"
        if self.report==Med_test2_4_report:
            return reverse('med_test2_app:Read_4')+f"?id={self.id}"
        if self.report==Med_test2_5_report:
            return reverse('med_test2_app:Read_5')+f"?id={self.id}"
    def get_create_url(self):
        if self.report==Med_test2_1_report:
            return reverse('med_test2_app:Create_1')+f"?id={self.id}"
        if self.report==Med_test2_2_report:
            return reverse('med_test2_app:Create_2')+f"?id={self.id}"
        if self.report==Med_test2_3_report:
            return reverse('med_test2_app:Create_3')+f"?id={self.id}"
        if self.report==Med_test2_4_report:
            return reverse('med_test2_app:Create_4')+f"?id={self.id}"
        if self.report==Med_test2_5_report:
            return reverse('med_test2_app:Create_5')+f"?id={self.id}"
                
            
        
import os
from django.conf import settings
from reportlab.platypus import Image

class Pdf(View):
    id=None
    report=Med_test2_1_report
    heading='some heading'
    def post(self, request):
        self.id=request.POST.get('id', None)
        try:
            p=Patient.objects.get(id=self.id)
        except Exception:
            messages.error(request, 'patient not found')
            return redirect(reverse('patient_app:create_patient'))
        try:
            r=self.report.objects.get(patient=p)
            return self.get_pdf(p, r)
        except Exception:
            messages.error(request, 'report not found')
            return redirect(get_create_url({'id':self.id, 'report':self.report}))
    def get_pdf(self, p, r):
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50)

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
            ['Patient ID', p.id, 'Lab No.', r.lab_no, 'Registration Date', p.created_date],
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

        # Define heading text and style
        heading_text = self.heading
        heading_style = getSampleStyleSheet()["Heading4"]
        heading_style.alignment = 1  # Set alignment to center

        # Create a Paragraph object for the heading
        heading1 = Paragraph(heading_text, style=heading_style)

        para=Paragraph(r.t1.replace('<br>', '<br/>').replace('<p>&nbsp;</p>', '<br/>').replace('</p>', '</p><br/>'))
        
        
        # Build the document with the table
        elements = [table, Spacer(0, 20), t, Spacer(0, 20), heading1, para]
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


def create_med_test2_1_report(request):
    id=request.GET.get('id', None)
    if id is None:
        id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report already existed please update or take print')
        return redirect(reverse('med_test2_app:read_med_test2_1_report'))
    match request.method:
        case 'GET':
            messages.success(request, 'create report')
            return render(request, 'med_test2_app/create_med_test2_1_report.html', {'patient':p})
        case 'POST':
            
            try:
                latest_id=Med_test2_1_report.objects.latest('id')
                latest_id=latest_id.id
            except Exception:
                latest_id=0
            r=Med_test2_1_report.objects.create(patient=p)
            r.lab_no=latest_id+1
            r.t1=request.POST.get('t1', None)
            r.save()
            return redirect(reverse('med_test2_app:read')+f'1/?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        
def read_med_test2_1_report(request):
    match request.method:
        case 'GET':
            id=request.GET.get('id', None)
            try:
                p=Patient.objects.get(id=id)
            except Exception:
                messages.error(request, 'Patient not found')
                return redirect(reverse('med_test2_app:create_med_test2_1_report'))
            if not hasattr(p, 'med_test2_1_report'):
                messages.error(request, 'report does not existed')
                return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
            messages.success(request, 'fetched report')
            return render(request, 'med_test2_app/read_med_test2_1_report.html', {'patient':p})
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        
def update_med_test2_1_report(request):
    id=request.GET.get('id', None)
    if id is None:
        id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create')+f'1/?id={id}')
    match request.method:
        case 'GET':
            messages.success(request, 'update report')
            return render(request, 'med_test2_app/update_med_test2_1_report.html', {'patient':p})
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)
            r.t1=request.POST.get('t1', r.t1)
            r.save()
            return redirect(f'/us/read/1/?id={id}')
            url=resolve_url('med_test2_app:read', args=[1])+f'?id={id}'
            return HttpResponse(url)
            return redirect(resolve_url('med_test2_app:read', kwargs={'n':1})+f'?id={id}')
            return redirect(reverse('med_test2_app:read')+f'?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))


def validate_med_test2_1_report(request):
    id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
    match request.method:
        case 'GET':
            messages.error(request, 'method not allowed.')
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)
            # r.t1=request.POST.get('t1', r.t1)
            r.validated_by=request.user.username
            r.save()
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        



def generate_pdf_med_test2_1_report(request):
    id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
    match request.method:
        case 'GET':
            messages.error(request, 'method not allowed.')
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)

            return get_pdf(p, r, 'some heading')
            buffer = BytesIO()

            doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50)

            

            data=[
                ['Patient ID', p.id, 'Lab No.', r.lab_no, 'Registration Date', p.created_date],
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

            # Define heading text and style
            heading_text = "Mitral Valve"
            heading_style = getSampleStyleSheet()["Heading4"]
            heading_style.alignment = 1  # Set alignment to center

            # Create a Paragraph object for the heading
            heading1 = Paragraph(heading_text, style=heading_style)

            para=Paragraph(r.t1.replace('<br>', '<br/>').replace('<p>&nbsp;</p>', '<br/>').replace('</p>', '</p><br/>'))
            
            
            # Build the document with the table
            elements = [t, para]
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
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        

def create_med_test2_2_report(request):
    id=request.GET.get('id', None)
    if id is None:
        id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report already existed please update or take print')
        return redirect(reverse('med_test2_app:read_med_test2_1_report'))
    match request.method:
        case 'GET':
            messages.success(request, 'create report')
            return render(request, 'med_test2_app/create_med_test2_1_report.html', {'patient':p})
        case 'POST':
            
            try:
                latest_id=Med_test2_1_report.objects.latest('id')
                latest_id=latest_id.id
            except Exception:
                latest_id=0
            r=Med_test2_1_report.objects.create(patient=p)
            r.lab_no=latest_id+1
            r.t1=request.POST.get('t1', None)
            r.save()
            return redirect(reverse('med_test2_app:read')+f'1/?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        
def read_med_test2_2_report(request):
    match request.method:
        case 'GET':
            id=request.GET.get('id', None)
            try:
                p=Patient.objects.get(id=id)
            except Exception:
                messages.error(request, 'Patient not found')
                return redirect(reverse('med_test2_app:create_med_test2_1_report'))
            if not hasattr(p, 'med_test2_1_report'):
                messages.error(request, 'report does not existed')
                return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
            messages.success(request, 'fetched report')
            return render(request, 'med_test2_app/read_med_test2_1_report.html', {'patient':p})
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        
def update_med_test2_2_report(request):
    id=request.GET.get('id', None)
    if id is None:
        id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create')+f'1/?id={id}')
    match request.method:
        case 'GET':
            messages.success(request, 'update report')
            return render(request, 'med_test2_app/update_med_test2_1_report.html', {'patient':p})
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)
            r.t1=request.POST.get('t1', r.t1)
            r.save()
            return redirect(f'/us/read/1/?id={id}')
            url=resolve_url('med_test2_app:read', args=[1])+f'?id={id}'
            return HttpResponse(url)
            return redirect(resolve_url('med_test2_app:read', kwargs={'n':1})+f'?id={id}')
            return redirect(reverse('med_test2_app:read')+f'?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))


def validate_med_test2_2_report(request):
    id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
    match request.method:
        case 'GET':
            messages.error(request, 'method not allowed.')
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)
            # r.t1=request.POST.get('t1', r.t1)
            r.validated_by=request.user.username
            r.save()
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
            
        case default:
           messages.error(request, 'method not allowed.')
           return redirect(reverse('patient_app:create_patient'))
        



def generate_pdf_med_test2_2_report(request):
    id=request.POST.get('id', None)
    try:
        p=Patient.objects.get(id=id)
    except Exception:
        messages.error(request, 'Patient not found')
        return redirect(reverse('patient_app:create_patient'))
    if not hasattr(p, 'med_test2_1_report'):
        messages.error(request, 'report does not existed please create first.')
        return redirect(reverse('med_test2_app:create_med_test2_1_report')+f'?id={id}')
    match request.method:
        case 'GET':
            messages.error(request, 'method not allowed.')
            return redirect(reverse('med_test2_app:read_med_test2_1_report')+f'?id={id}')
        case 'POST':
            
            r=Med_test2_1_report.objects.get(patient=p)

            return get_pdf(p, r, 'some heading')
        

   
def get_pdf(p, r, heading):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50)

    data=[
        ['Patient ID', p.id, 'Lab No.', r.lab_no, 'Registration Date', p.created_date],
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

    # Define heading text and style
    heading_text = heading
    heading_style = getSampleStyleSheet()["Heading4"]
    heading_style.alignment = 1  # Set alignment to center

    # Create a Paragraph object for the heading
    heading1 = Paragraph(heading_text, style=heading_style)

    para=Paragraph(r.t1.replace('<br>', '<br/>').replace('<p>&nbsp;</p>', '<br/>').replace('</p>', '</p><br/>'))
    
    
    # Build the document with the table
    elements = [t, para]
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
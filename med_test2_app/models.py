from pyexpat import model
from django.db import models
from django.utils import timezone
from patient_app.models import Patient

# Create your models here.


class Med_test2_1_report(models.Model):
    """
    Model representing an Echo report.
    """
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='EchoReport')
    patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test2_1_report')
    id=models.AutoField(primary_key=True)
    reffered_by=models.CharField(max_length=200, null=True)
    validated_by=models.CharField(max_length=200, null=True)
    created_date=models.DateField(default=timezone.now)
    lab_no=models.IntegerField(null=True)

    t1=models.TextField(null=True)

    
class Med_test2_2_report(models.Model):
    """
    Model representing an Echo report.
    """
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='EchoReport')
    # patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test1_report')
    patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test2_2_report')

    id=models.AutoField(primary_key=True)
    reffered_by=models.CharField(max_length=200, null=True)
    validated_by=models.CharField(max_length=200, null=True)
    created_date=models.DateField(default=timezone.now)
    lab_no=models.IntegerField(null=True)

    t1=models.TextField(null=True)

class Med_test2_3_report(models.Model):
    """
    Model representing an Echo report.
    """
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='EchoReport')
    # patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test1_report')
    patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test2_3_report')

    id=models.AutoField(primary_key=True)
    reffered_by=models.CharField(max_length=200, null=True)
    validated_by=models.CharField(max_length=200, null=True)
    created_date=models.DateField(default=timezone.now)
    lab_no=models.IntegerField(null=True)

    t1=models.TextField(null=True)

class Med_test2_4_report(models.Model):
    """
    Model representing an Echo report.
    """
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='EchoReport')
    # patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test1_report')
    patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test2_4_report')

    id=models.AutoField(primary_key=True)
    reffered_by=models.CharField(max_length=200, null=True)
    validated_by=models.CharField(max_length=200, null=True)
    created_date=models.DateField(default=timezone.now)
    lab_no=models.IntegerField(null=True)

    t1=models.TextField(null=True)

class Med_test2_5_report(models.Model):
    """
    Model representing an Echo report.
    """
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='EchoReport')
    # patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test1_report')
    patient=models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='med_test2_5_report')

    id=models.AutoField(primary_key=True)
    reffered_by=models.CharField(max_length=200, null=True)
    validated_by=models.CharField(max_length=200, null=True)
    created_date=models.DateField(default=timezone.now)
    lab_no=models.IntegerField(null=True)

    t1=models.TextField(null=True)


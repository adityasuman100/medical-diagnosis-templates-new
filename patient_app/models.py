from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# from med_test1_app.models import Echo_report, Echo_payment
from med_test1_app.models import Med_test1_report

# class Constant(models.Model):
#     name = models.CharField(max_length=200, primary_key=True)
#     value=models.IntegerField()

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    # id=models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mob_no=models.CharField(max_length=10, null=True)
    address=models.CharField(max_length=200, null=True)
    med_test1_report=models.OneToOneField(Med_test1_report, on_delete=models.CASCADE, null=True, related_name='med_test1_report')
    created_date = models.DateField(default=timezone.now)
    created_time = models.TimeField(default=timezone.now)

    ## tests
    med_test1=models.BooleanField(default=False)
    med_test2_1=models.BooleanField(default=False)
    med_test2_2=models.BooleanField(default=False)
    med_test2_3=models.BooleanField(default=False)
    med_test2_4=models.BooleanField(default=False)
    med_test2_5=models.BooleanField(default=False)
    


# class Receipt(models.Model):
#     # id=models.CharField(max_length=200, primary_key=True)
#     id=models.AutoField(primary_key=True)
#     patient=models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='receipt')
#     med_test1=models.IntegerField(null=True) # medical test 1
#     med_test2=models.IntegerField(null=True) # medical test 2
#     med_test3=models.IntegerField(null=True) # medical test 3
#     med_test4=models.IntegerField(null=True) # medical test 4
#     done_by=models.CharField(max_length=200, null=True)
#     created_date=models.DateField(default=timezone.now)
#     created_time=models.TimeField(default=timezone.now)


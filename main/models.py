from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=50)
    patient_age = models.IntegerField()
    patient_img = models.ImageField(upload_to = 'images/',default = 'No Image')

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.IntegerField()
    doctor_name = models.CharField(max_length=50)
    doctor_desc = models.CharField(max_length=200)


class Prescription(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescription_date = models.DateField(default=timezone.now)
    prescription_medicine = models.TextField(max_length=200)
    prescription_img = models.ImageField()



from django.db import models

class Prescription(models.Model):
    prescription_date = models.DateField()
    prescription = models.TextField(max_length=200)

class Patient(models.Model):
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=50)
    patient_age = models.IntegerField()
    appointment_date = models.DateField(auto_now_add=True)
    patient_img = models.ImageField()

class Doctor(models.Model):
    doctor_id = models.ForeignKey(Patient,on_delete=models.CASCADE)



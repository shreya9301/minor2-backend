from django.urls import path
from . import views

urlpatterns = [
    path('registerDoctor/', views.register_doctor, name='register_doctor'),
    path('registerPatient/', views.register_patient, name='register_patient'),
    path('addPrescription/', views.addPrescription, name='add_prescription'),
]

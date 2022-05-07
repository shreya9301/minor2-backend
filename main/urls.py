from django.urls import path
from . import views

urlpatterns = [
    path('register_doctor/', views.register_doctor, name='register'),
    path('register_patient/', views.register_patient, name='register'),
    # path('', views.index, name='index'),
]

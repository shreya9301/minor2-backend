from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from matplotlib import path
from rest_framework import permissions, status
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import (
    api_view, permission_classes
)
from rest_framework.response import Response
import datetime
from django.contrib.auth.models import User
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, PrescriptionSerializer
from .models import Doctor,Patient,Prescription
from .utility import handle_uploaded_image


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def register_doctor(request):
	"""For doctor registration """

	serializer = DoctorSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def register_patient(request):
	"""For patient registration """

	serializer = PatientSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def addPrescription(request):
	doctor_id = request.data['doctor_id']
	Curr_Doc = Doctor.objects.get(doctor_id=doctor_id)
	patient_id = request.data['patient_id']
	Curr_pati = Patient.objects.get(patient_id=patient_id)
	list_of_medicine = request.data['prescription_medicine']
	# parser_classes = [FileUploadParser]
	# print(list_of_medicine)

	img = request.data["prescription_img"]
	presctiption_object = Prescription(doctor_id=Curr_Doc,patient_id=Curr_pati,prescription_medicine=list_of_medicine,prescription_img=img)
	presctiption_object.save()
	path_of_file = presctiption_object.prescription_img.path
	number_of_divisons = len(list_of_medicine.split(','))
	patient_name = Curr_pati.patient_name
	print(path_of_file,number_of_divisons,patient_name)
	handle_uploaded_image(path_of_file,number_of_divisons,patient_name)
	return Response(status=status.HTTP_201_CREATED)
	# return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def get_prescription(request):
	"""For getting the prescription of a patient"""
	# print(request.GET['doctor_id'])
	# Doctor and date => patient id, medicines 
	doctor_id = request.GET['doctor_id']
	Curr_Doc = Doctor.objects.get(doctor_id=doctor_id)
	patient_id = request.GET['patient_id']
	Curr_pati = Patient.objects.get(patient_id=patient_id)
	choosen_date = request.GET['date']
	# print(choosen_date)
	Prescription_list = Prescription.objects.filter(doctor_id=Curr_Doc,patient_id=Curr_pati,prescription_date=choosen_date)
	# Prescription_list = Prescription.objects.filter(doctor_id=Curr_Doc)
	raw_image = Prescription_list[0].prescription_img
	# return HttpResponse("Hello")

	return HttpResponse(raw_image, content_type="image/png")


# view preciption for paitent input id => presctipton ,images ,medicines 
# when decrpt called return the imahge 
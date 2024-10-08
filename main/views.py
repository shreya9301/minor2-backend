from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from matplotlib import path
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
from datetime import datetime
import os
from PIL import Image
from .utility_2 import decrypted, decryption_test

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
	doctor_id = request.data['doctor_username']
	user_doc = User.objects.get(username=doctor_id)
	Curr_Doc = Doctor.objects.get(user=user_doc)
	patient_id = request.data['patient_username']
	user_pat = User.objects.get(username=patient_id)
	Curr_pati = Patient.objects.get(user=user_pat)
	list_of_medicine = request.data['prescription_medicine']
	# parser_classes = [FileUploadParser]
	# print(list_of_medicine)

	img = request.data["prescription_img"]
	presctiption_object = Prescription(doctor_id=Curr_Doc,patient_id=Curr_pati,prescription_medicine=list_of_medicine,prescription_img=img)
	presctiption_object.save()
	path_of_file = presctiption_object.prescription_img.path
	number_of_divisons = len(list_of_medicine.split(','))
	patient_name = patient_id
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
	doctor_id = request.data['username']
	user_doc = User.objects.get(username=doctor_id)
	Curr_Doc = Doctor.objects.get(user=user_doc)
	# patient_id = request.GET['patient_id']
	# Curr_pati = Patient.objects.get(patient_id=patient_id)
	choosen_date = request.GET['date']
	# print(choosen_date)
	choosen_date = datetime.strptime(choosen_date, '%Y-%m-%d')
	# print(choosen_date)
	Prescription_list = Prescription.objects.filter(doctor_id=Curr_Doc,prescription_date=choosen_date)
	# Prescription_list = Prescription.objects.filter(doctor_id=Curr_Doc)
	# raw_image = Prescription_list[0].prescription_img
	Prescription_well = PrescriptionSerializer(Prescription_list, many=True)
	print(Prescription_well.data[0]['prescription_img'])
	return Response(Prescription_well.data, status=status.HTTP_200_OK)

	# return HttpResponse(raw_image, content_type="image/png")


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def get_all_prescription(request):
	username = request.data['username']
	user = User.objects.get(username=username)
	patient = Patient.objects.get(user=user)
	prescrip = Prescription.objects.filter(patient_id=patient)
	prescrip_well = PrescriptionSerializer(prescrip, many=True)
	return Response(prescrip_well.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def img(request):
	print(request.GET['val'])
	dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print(dir_name)
	path = os.path.join(dir_name, request.GET['val'])
	with open(path, 'rb') as f:
		return HttpResponse(f.read(), content_type="image/jpeg")


# only decrypted images are left
@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def get_decrypted_img(request):
	username = request.data['username']
	user = User.objects.get(username=username)
	patient = Patient.objects.get(user=user)
	in_date = request.data['date']
	date = datetime.strptime(in_date, '%Y-%m-%d')
	prescrip = Prescription.objects.filter(patient_id=patient,prescription_date=date)
	Image_path = prescrip[0].prescription_img.path
	# print(Image_type)
	# decrypted(Image_type,username,date)
	file_saved = decryption_test(Image_path,username,in_date)
	with open(file_saved, 'rb') as f:
		return HttpResponse(f.read(), content_type="image/jpeg")
	# return HttpResponse("hello")
	# return HttpResponse(Image_type+"_noise.jpeg",content="image/jpeg")

	# prescrip_well = PrescriptionSerializer(prescrip, many=True)
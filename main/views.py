from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
def register(request):
	"""For user registration """

	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def addPrescription(request):
	username = request.POST.get('username')
	patientID = request.POST.get('patient_id')
	parser_classes = [FileUploadParser]

	img = request.FILES["patient_img"]
	if len(img) != 0:
		handle_uploaded_image(img, username, patientID)
		response = {
            "User": username
        }
		return Response(response, status=204)
	else:
		user = User.objects.get(username=username)
		user.delete()
		return Response(status=status.HTTP_400_BAD_REQUEST)


	
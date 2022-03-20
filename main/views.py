from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view, permission_classes
)
from rest_framework.response import Response
import datetime
from django.contrib.auth.models import User
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer

@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def register(request):
	"""For user registration """

	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


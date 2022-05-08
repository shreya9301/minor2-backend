from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import Patient, Doctor, Prescription

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'passwords': 'Passwords must match'})

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Patient
        fields = ('user', 'patient_id', 'patient_name', 'patient_age')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(),validated_data=user_data)
        patient = Patient(user=user,patient_id=validated_data['patient_id'],patient_name=validated_data['patient_name'],patient_age=validated_data['patient_age'])
        patient.save()
        return patient


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Doctor
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(),validated_data=user_data)
        doctor = Doctor(user=user,doctor_id=validated_data['doctor_id'],doctor_name=validated_data['doctor_name'],doctor_desc=validated_data['doctor_desc'])
        doctor.save()
        return doctor

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

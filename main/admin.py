from django.contrib import admin
from .models import *

admin.site.register(Prescription)
admin.site.register(Patient)
admin.site.register(Doctor)
# Register your models here.

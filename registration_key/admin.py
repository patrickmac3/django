from django.contrib import admin
from .models import CondoRegistrationKey, ParkingRegistrationKey, RegistrationKey, StorageRegistrationKey
# Register your models here.


admin.site.register(CondoRegistrationKey)
admin.site.register(ParkingRegistrationKey)
admin.site.register(StorageRegistrationKey)
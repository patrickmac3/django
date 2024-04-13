from django.contrib import admin
from .models import PropertyProfile, CondoUnit, ParkingUnit, StorageUnit
# Register your models here.

admin.site.register(PropertyProfile)
admin.site.register(CondoUnit)
admin.site.register(ParkingUnit)
admin.site.register(StorageUnit)
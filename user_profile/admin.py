from django.contrib import admin

from django.db import models

from .models import *
    
admin.site.register(User)
admin.site.register(PublicProfile)
admin.site.register(EmployeeProfile)
admin.site.register(CompanyProfile)
from django.contrib import admin

# Register your models here.
from .models import Reports, ReportsConfig
   
admin.site.register(ReportsConfig)
admin.site.register(Reports)

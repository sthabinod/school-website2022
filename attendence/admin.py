from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AdminAttend(admin.ModelAdmin):
    pass
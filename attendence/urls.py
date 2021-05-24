from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('attendance',views.attendence,name="attendance"),
    path('add_attendance',views.add_attendence,name="add_attendance"),
]
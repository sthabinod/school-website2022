from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing_page, name = "landing-page"),
    path('connect',views.connect, name = "connect"),
    path('about',views.about, name = "about"),
    path('admission',views.admission, name = "admission"),
    path('contact',views.contact, name = "contact"),
]
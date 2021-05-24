from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('gallery', views.gallery, name="event-gallery"),
    path('', views.events, name="event"),
    path('event-details/<id>', views.event_details, name="event_details"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
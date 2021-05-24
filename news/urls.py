from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('news_details/<id>', views.news_details, name="news_details"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
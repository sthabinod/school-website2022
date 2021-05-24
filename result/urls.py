from django.urls import path
from . import views

urlpatterns = (
    path('result-report', views.result_report, name="result_report"),
    path('add-result', views.add_result, name="add_result"),
    path('view-result', views.view_result, name="view_result"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('result', views.result, name="result"),
    path('result-event', views.result_event, name="result_event"),
    path('publish-result', views.publish_result, name="publish_result"),
    path('publish/<id>', views.publish, name="publish"),
    path('send-result', views.send_result_data, name="send_result")
)
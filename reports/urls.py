from django.urls import path

from . import views
#from .views import DocumentCreateView

urlpatterns = [
    path('', views.index, name='index'),
    path("reports/<int:report_id>/", views.generate_report, name="reports"),
    path('upload/', views.upload_file, name='upload'),
]
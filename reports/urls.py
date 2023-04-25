from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("reports/<int:report_id>/", views.generate_report, name="reports"),
    path("api/data-pull", views.pull_data_from_dune)
]
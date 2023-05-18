from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("reports/<int:report_id>/", views.generate_report, name="reports"),
    path('upload/', views.upload_file, name='upload'),
     path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
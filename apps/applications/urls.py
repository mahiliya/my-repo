from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.apply_internship, name='apply_internship'),
    path('submit/', views.internship_application, name='internship_application'),
    path('success/', views.application_success, name='application_success'),
    path('check-email/', views.check_email, name='check_email'),
]
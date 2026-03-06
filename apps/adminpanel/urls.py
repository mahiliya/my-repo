from django.urls import path
from .views import admin_login, admin_home

urlpatterns = [
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/home/', admin_home, name='admin_home'),  # Admin dashboard
]

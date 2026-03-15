from django.urls import path
from . import views

# The Job: This defines the sub-urls for your Super Admin app.
# By using 'app_name', we can call these urls using 'super_core:dashboard' 
# in our templates, making the code much cleaner.

app_name = 'super_core'

urlpatterns = [
   path('dashboard/', views.super_dashboard, name='super_dashboard'),
    # Adding placeholders for the links you just put in the sidebar:
    path('staff-control/', views.manage_admins, name='manage_admins'),
    path('infrastructure/', views.manage_departments, name='manage_departments'),
    path('global-oversight/', views.intern_oversight, name='intern_oversight'),
    path('security-logs/', views.access_logs, name='access_logs'),
]
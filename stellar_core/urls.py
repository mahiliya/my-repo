from django.contrib import admin
from django.urls import path, include
from apps.accounts import views as account_views # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ADD THIS LINE: This maps the URL you typed to the function we wrote
    path('staff-portal/login/', account_views.unified_staff_login, name='staff_login'),
    
    # Ensure your other apps are included correctly
    path('super-admin/', include('apps.super_core.urls')),
    path('adminpanel/', include('apps.adminpanel.urls')),
    
    # Your existing paths...
    path('accounts/', include('apps.accounts.urls')),
    # ...
]
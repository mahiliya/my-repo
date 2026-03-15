from django.shortcuts import render,get_object_or_404, redirect
from .decorators import superadmin_required
from apps.applications.models import Application # Import from existing apps
from apps.accounts.models import User
from apps.departments.models import Department

@superadmin_required
def super_dashboard(request):
    # Professional apps should use 'select_related' or 'count()' 
    # for speed rather than loading all objects.
    context = {
        'total_interns': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'total_admins': User.objects.filter(is_staff=True, is_superuser=False).count(),
        'all_departments': Department.objects.all(),
        'pending_apps': Application.objects.filter(status='pending').count(),
        'latest_apps': Application.objects.all().order_by('-id')[:10],
        'recent_logs': [], # We will build the Audit Log next
    }
    return render(request, 'superadmin/dashboard.html', context)

@superadmin_required
def manage_admins(request):
    return render(request, 'superadmin/manage_admins.html')

@superadmin_required
def manage_departments(request):
    return render(request, 'superadmin/manage_departments.html')

@superadmin_required
def intern_oversight(request):
    return render(request, 'superadmin/intern_oversight.html')

@superadmin_required
def access_logs(request):
    return render(request, 'superadmin/access_logs.html')
    
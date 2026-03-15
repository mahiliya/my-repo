# ==========================================
# IMPORTS
# ==========================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.departments.models import Department
from apps.applications.models import InternshipApplication
from apps.adminpanel.models import Admin, ActivityLog
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

# ==========================================
# DECORATORS
# ==========================================
def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

# ==========================================
# 1. PUBLIC WORLD (Corrected Logic)
# ==========================================
def applicant_form(request):
    """Checks deadlines and quotas before showing available units to students."""
    all_depts = Department.objects.filter(is_accepting_applications=True)
    available_depts = []

    for d in all_depts:
        # Check Deadline
        if d.application_deadline and timezone.now() > d.application_deadline:
            continue 
            
        # Check Quota
        current_approved_count = InternshipApplication.objects.filter(
            department=d, 
            status='Approved'
        ).count()
        
        if current_approved_count < d.intern_limit:
            available_depts.append(d)

    return render(request, 'public/apply.html', {'departments': available_depts})

# ==========================================
# 2. STAFF GATEWAY (Unified Login)
# ==========================================
@ensure_csrf_cookie
def unified_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('superadmin_dashboard')
            else:
                return redirect('admin_home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'registration/login.html')

def applicant_success(request):
    return render(request, 'public/success.html')

def admin_logout(request):
    logout(request)
    return redirect('staff_login')

# ==========================================
# 3. SUPERADMIN COMMAND CENTER (Unified)
# ==========================================
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    """The High-Level Overview with Stats and Logs"""
    context = {
        'stats': {
            'total_users': User.objects.count(),
            'total_apps': InternshipApplication.objects.count(),
            'total_depts': Department.objects.count(),
            'total_admins': Admin.objects.count(),
        },
        'logs': ActivityLog.objects.order_by('-timestamp')[:10],
        'dept_stats': Department.objects.annotate(app_count=Count('internshipapplication')).values('name', 'app_count')
    }
    return render(request, 'superadmin/superadmin_dashboard.html', context)

# ==========================================
# 3. INFRASTRUCTURE & CONTROLS (Fixed Field Names)
# ==========================================
@user_passes_test(is_superadmin)
def update_dept_controls(request, dept_id):
    """Set deadlines and limits (Ensure names match your Model fields)"""
    dept = get_object_or_404(Department, id=dept_id)
    
    if request.method == 'POST':
        # Make sure these field names match your Department Model exactly!
        dept.intern_limit = request.POST.get('intern_limit')
        dept.application_deadline = request.POST.get('deadline')
        dept.max_file_size_mb = request.POST.get('file_size')
        dept.is_accepting_applications = 'is_active' in request.POST
        dept.save()
        
        ActivityLog.objects.create(
            admin_name=request.user.username,
            action=f"Updated rules for {dept.name}"
        )
        messages.success(request, f"Controls updated for {dept.name}")
        return redirect('manage_departments')
    
    return render(request, 'superadmin/dept_control_panel.html', {'dept': dept})

# ==========================================
# 4. MANUAL INTERN ENTRY (Fixed Variable Order)
# ==========================================
@user_passes_test(is_superadmin)
def add_intern_manual(request):
    depts = Department.objects.all()
    
    if request.method == 'POST':
        # ... [Your validation logic here] ...
        
        # CREATE THE OBJECT FIRST
        new_intern = InternshipApplication.objects.create(
            full_name=request.POST.get('full_name'),
            department_id=request.POST.get('department_id'),
            status='Approved'
        )
        
        # NOW YOU CAN LOG IT
        ActivityLog.objects.create(
            admin_name=request.user.username,
            action=f"MANUAL ENTRY: Added {new_intern.full_name}"
        )
        messages.success(request, f"Intern {new_intern.full_name} registered.")
        return redirect('global_intern_oversight')

    return render(request, 'superadmin/add_intern_manual.html', {'depts': depts})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Admin, ActivityLog
from .forms import AdminLoginForm
from .decorators import superadmin_required
from django.contrib.auth.models import User
from apps.applications.models import InternshipApplication
from apps.departments.models import Department
from apps.departments.models import Department # Ensure the path is correct
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = Admin.objects.get(username=username)
                if admin.check_password(password):
                    # 1. Save session (Same as your original)
                    request.session['admin_username'] = admin.username
                    
                    # 2. THE ROUTER: This is the ONLY place that changes logic
                    # If it's the Superadmin, send to the NEW dashboard
                    # Otherwise, send them to your ORIGINAL admin_home
                    if hasattr(admin, 'role') and admin.role == 'superadmin':
                        return redirect('superadmin_dashboard')
                    else:
                        return redirect('admin_home') 
                else:
                    return render(request, 'AdminLogin.html', {'form': form, 'error': 'Invalid password'})
            except Admin.DoesNotExist:
                return render(request, 'AdminLogin.html', {'form': form, 'error': 'User not found'})
    else:
        form = AdminLoginForm()
    return render(request, 'AdminLogin.html', {'form': form})

# --- YOUR ORIGINAL ADMIN HOME (UNTOUCHED) ---
def admin_home(request):
    if 'admin_username' not in request.session:
        return redirect('admin_login')
    return render(request, 'admin.html') # This keeps your existing design

# --- THE NEW SUPERADMIN DASHBOARD (ISOLATED) ---
@superadmin_required
def superadmin_dashboard(request):
    # This logic only runs for this specific page
    stats = {
        'total_users': User.objects.count(),
        'total_apps': InternshipApplication.objects.count(),
        'total_admins': Admin.objects.count(),
        'total_depts': Department.objects.count(),
    }
    logs = ActivityLog.objects.order_by('-timestamp')[:10]
    
    # Points to the new folder you created in screenshot 1
    return render(request, 'superadmin/superadmin_dashboard.html', {
        'stats': stats, 
        'logs': logs,
        'admin_name': request.session.get('admin_username')
    })

# 1. LIST ALL ADMINS
@superadmin_required
def manage_admins(request):
    all_admins = Admin.objects.all()
    return render(request, 'superadmin/manage_admins.html', {'all_admins': all_admins})

# 2. DELETE ADMIN
@superadmin_required
def delete_admin(request, admin_id):
    admin_to_delete = get_object_or_404(Admin, id=admin_id)
    
    # Safety Check: Don't let them delete themselves
    if admin_to_delete.username == request.session.get('admin_username'):
        messages.error(request, "You cannot delete your own account!")
    else:
        admin_to_delete.delete()
        messages.success(request, f"Admin {admin_to_delete.username} deleted successfully.")
    
    return redirect('manage_admins')

# 3. DISABLE/ENABLE ACCOUNT (Toggle Status)
@superadmin_required
def toggle_admin_status(request, admin_id):
    admin = get_object_or_404(Admin, id=admin_id)
    # Assuming your model has an 'is_active' field
    if hasattr(admin, 'is_active'):
        admin.is_active = not admin.is_active
        admin.save()
        status = "enabled" if admin.is_active else "disabled"
        messages.success(request, f"Account {admin.username} has been {status}.")
    return redirect('manage_admins')

# 4. RESET ADMIN PASSWORD
@superadmin_required
def reset_admin_password(request, admin_id):
    admin_user = get_object_or_404(Admin, id=admin_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            # Hash the password before saving
            admin_user.set_password(new_password)
            admin_user.save()
            
            # Log the action
            ActivityLog.objects.create(
                admin_name=request.session.get('admin_username'),
                action=f"Reset password for Admin: {admin_user.username}"
            )
            
            messages.success(request, f"Password for {admin_user.username} updated successfully.")
            return redirect('manage_admins')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'superadmin/reset_password_standalone.html', {'admin_user': admin_user})

@superadmin_required
def add_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if username already exists
        if Admin.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            # Create the new admin and HASH the password
            new_admin = Admin.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role,
                is_active=True
            )
            
            # Record the activity
            ActivityLog.objects.create(
                admin_name=request.session.get('admin_username'),
                action=f"Created new Admin account: {username}"
            )
            
            messages.success(request, f"Admin {username} created successfully!")
            return redirect('manage_admins')
            
    return render(request, 'superadmin/add_admin.html')

@superadmin_required
def manage_departments(request):
    depts = Department.objects.all()
    return render(request, 'superadmin/manage_departments.html', {'depts': depts})

@superadmin_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        Department.objects.create(name=name, description=description)
        
        ActivityLog.objects.create(
            admin_name=request.session.get('admin_username'),
            action=f"Created new department: {name}"
        )
        messages.success(request, f"Department '{name}' added successfully!")
        return redirect('manage_departments')
        
    return render(request, 'superadmin/add_department.html')

@superadmin_required
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    dept_name = dept.name
    dept.delete()
    
    ActivityLog.objects.create(
        admin_name=request.session.get('admin_username'),
        action=f"Deleted department: {dept_name}"
    )
    messages.success(request, f"Department '{dept_name}' removed successfully.")
    return redirect('manage_departments')

@superadmin_required
def manage_departments(request):
    depts = Department.objects.all()
    return render(request, 'superadmin/manage_departments.html', {'depts': depts})

# 2. Add Department
@superadmin_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        Department.objects.create(name=name, description=description)
        
        ActivityLog.objects.create(
            admin_name=request.session.get('admin_username'),
            action=f"Created new department: {name}"
        )
        messages.success(request, f"Department '{name}' added successfully!")
        return redirect('manage_departments')
        
    return render(request, 'superadmin/add_department.html')

# 3. Delete Department
@superadmin_required
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    dept_name = dept.name
    dept.delete()
    
    ActivityLog.objects.create(
        admin_name=request.session.get('admin_username'),
        action=f"Deleted department: {dept_name}"
    )
    messages.success(request, f"Department '{dept_name}' removed successfully.")
    return redirect('manage_departments')
    
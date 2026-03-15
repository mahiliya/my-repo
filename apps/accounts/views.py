from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from apps.departments.models import Department
from django.contrib import messages

# Create your views here.

# def home(request):
#     department = Department.objects.first()  # or get the relevant department
#     return render(request, 'departments.html', {'department': department})

def home(request):
    return render(request, 'public/interns.html')
def interns(request):
    return render(request, 'interns.html')
@login_required
def departments(request):
    return render(request, 'departments.html')
def unified_staff_login(request):
    """
    The Job: A single login view for ALL staff (Super, Regular, and Dept).
    It acts as a traffic controller based on database flags.
    """
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            login(request, user)
            
            # --- THE DYNAMIC REDIRECTOR ---
            
            if user.is_superuser:
                # Sends to apps/super_core/urls.py
                return redirect('super_core:super_dashboard')
                
            elif user.is_regular_admin:
                # Sends to apps/adminpanel/urls.py (General Admin)
                return redirect('adminpanel:admin_dashboard')
                
            elif user.is_department_admin:
                # Sends to apps/adminpanel/urls.py (Dept Admin)
                return redirect('departments:department_dashboard')
            
            else:
                # If a student tries to log in through the staff portal, kick them out
                from django.contrib.auth import logout
                logout(request)
                messages.error(request, "Access Denied: This portal is for Staff only.")
                return redirect('accounts:staff_login')
        else:
            messages.error(request, "Invalid staff credentials")
            
    return render(request, 'registration/staff_login.html')
def logout_view(request):
    """
    The Job: Clears the session entirely for security.
    """
    logout(request)
    return redirect('accounts:login')

# from django.shortcuts import render
# from apps.departments.models import Department
# from apps.applications.models import InternshipApplication
# from django.contrib.auth.decorators import login_required, user_passes_test

# # Optional: only allow superusers (admins)
# def is_admin(user):
#     return user.is_superuser

# @login_required
# @user_passes_test(is_admin)  # Optional restriction to admin users only
# def home(request):
#     departments = Department.objects.all()
#     applications = InternshipApplication.objects.all()
#     return render(request, 'admin.html', {
#         'departments': departments,
#         'applications': applications
#     })

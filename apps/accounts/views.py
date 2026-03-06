from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.departments.models import Department


# Create your views here.

# def home(request):
#     department = Department.objects.first()  # or get the relevant department
#     return render(request, 'departments.html', {'department': department})

def home(request):
    return render(request, 'home.html')
def interns(request):
    return render(request, 'interns.html')
@login_required
def departments(request):
    return render(request, 'departments.html')

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

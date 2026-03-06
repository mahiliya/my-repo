import json
from django.shortcuts import render, redirect
from .models import Department
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from .forms import DepartmentForm
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from .decorators import departments_open_required, department_user_required
from .utils import normalize_fields_and_counts

@login_required
@department_user_required
@departments_open_required
def department_submission(request):
    if request.method == 'POST':
        data = request.POST

        try:
            fields_and_counts = json.loads(data.get('fields_and_counts')) if data.get('fields_and_counts') else []
        except json.JSONDecodeError:
            fields_and_counts = []

        fields_and_counts = normalize_fields_and_counts(fields_and_counts)


        # Create the department entry
        department = Department.objects.create(
            department=data.get('department'),
            intern_count=int(data.get('internCount') or 0),
            fields_and_counts=fields_and_counts,
            skills=data.get('skills'),
            potential_project=data.get('potential_project'),
            mentor=data.get('mentor')
        )

        request.session['department_saved'] = True

        return redirect('department_success')  # redirect to success page

    # GET request (first page load)
    return render(request, 'departments.html', {
        'success': request.session.get('department_saved')
    })

def department_success(request):
    return render(request, 'depsuccess.html')

@login_required
@department_user_required
@departments_open_required
def apply_requirements(request):
    return render(request, 'departments.html')

@csrf_exempt
def department_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        submission_id = data.get('id')
        try:
            department = Department.objects.get(id=submission_id)
            department.department = data.get('department')
            department.intern_count = int(data.get('internCount') or 0)
            department.fields_and_counts = normalize_fields_and_counts(data.get('fields'))
            department.skills = data.get('skills')
            department.potential_project = data.get('potential_project')
            department.mentor = data.get('mentor')
            department.save()
            return JsonResponse({'success': True})
        except Department.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Submission not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@method_decorator(login_required, name='dispatch')
@method_decorator(department_user_required, name='dispatch')
@method_decorator(departments_open_required, name='dispatch')
class DepartmentUpdate(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments.html'  # Use your actual template path
    success_url = '/departments/'       # Redirect after successful update

# class DepartmentLoginView(LoginView):
#     template_name = 'dep_login.html'

# @login_required(login_url='/departments/login/')
# def department_requirements(request):
#     return render(request, 'departments.html')

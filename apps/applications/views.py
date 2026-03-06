
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import InternshipApplication

def internship_application(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        # Save application
        application = InternshipApplication.objects.create(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            age=data.get('age'),
            email=data.get('email'),
            phone=data.get('phone'),
            city=data.get('city'),
            university=data.get('university'),
            college_name=data.get('collegeName'),
            nationality=data.get('nationality'),
            address=data.get('address'),
            education_level=data.get('educationLevel'),
            cgpa=data.get('cgpa') or None,
            passport_id=files.get('passportId'),
            department=data.get('department'),
            current_year=data.get('currentYear'),
            expected_graduation=data.get('expectedGraduation'),
            duration=data.get('duration'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            skills=data.get('skills'),
            interests=data.get('interests'),
            motivation_letter=files.get('motivationLetter'),
            resume=files.get('resume'),
            recommendation_letter=files.get('recommendationLetter'),
        )

        # Store status in session so it can be read in interns.html later
        request.session['application_status'] = 'pending'

        return redirect('application_success')  # success.html

    return render(request, 'interns.html', {
        'status': request.session.get('application_status')  # in case user returns
    })

def application_success(request):
    return render(request, 'success.html')

def apply_internship(request):
    return render(request, 'interns.html', {
        'status': request.session.get('application_status')
    })

def check_email(request):
    email = request.GET.get('email', '').strip().lower()
    exists = InternshipApplication.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})


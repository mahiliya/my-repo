from django import forms
from .models import InternshipApplication
from adminpanel.models import Approved  # or wherever Approved lives

def update_approved_entry(student, department, start_date, end_date):
    try:
        approved_entry = Approved.objects.get(student_name=student, department_name=department)
        approved_entry.start_date = start_date
        approved_entry.end_date = end_date
        approved_entry.registered = True
        approved_entry.save()
    except Approved.DoesNotExist:
        pass  # Optionally log this
class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = '__all__'
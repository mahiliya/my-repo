from django import forms
from .models import Department
from django.views.generic import UpdateView


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields ='__all__'

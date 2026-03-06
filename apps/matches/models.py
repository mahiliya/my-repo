# matches/models.py
from django.db import models
from django.utils import timezone
from apps.applications.models import InternshipApplication
from apps.departments.models import Department

class Match(models.Model):
    application = models.ForeignKey(InternshipApplication, on_delete=models.CASCADE, related_name='matched_departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='matched_applications')

    student_name = models.CharField(max_length=100, blank=True, null=True)
    student_department = models.CharField(max_length=100, blank=True, null=True)
    student_skill = models.TextField(max_length=500, blank=True, null=True)

    institution_department = models.CharField(max_length=100, blank=True, null=True)
    fields_and_counts = models.JSONField(blank=True, null=True)   # remove max_length
    department_skills = models.TextField(max_length=500, blank=True, null=True)
    department_potential_project = models.TextField(max_length=500, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('waitlist', 'Waitlist'), ('rejected', 'Rejected'), ('approved', 'Approved')],
        default='pending'
    )

    # prefer explicit created/updated fields; matched_on used as 'last matched at'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    matched_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('application', 'department')

    def save(self, *args, **kwargs):
        # Populate snapshot fields from related objects before saving
        if self.application_id:
            app = self.application  # will hit DB for the FK
            self.student_name = f"{app.first_name} {app.last_name}"
            self.student_department = app.department
            self.student_skill = app.skills or ''

        if self.department_id:
            dept = self.department
            self.institution_department = dept.department
            self.fields_and_counts = dept.fields_and_counts
            self.department_skills = dept.skills or ''
            self.department_potential_project = dept.potential_project or ''

        # If you want matched_on to be "last matched/updated", set it every save:
        self.matched_on = timezone.now()
        # If you want matched_on only on first match:
        # if not self.matched_on:
        #     self.matched_on = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} MATCHED TO {self.institution_department} ({self.status})"

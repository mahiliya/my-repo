from django.db import models
from matches.models import Match
from datetime import date

class Approved(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    approved_on = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=False)

    # Snapshot fields to store student name and department name
    student_name = models.CharField(max_length=255, blank=True)
    department_name = models.CharField(max_length=255, blank=True)

    # Optional: Progress tracking fields
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Populate snapshot fields from related Match and Application on creation
        if not self.pk:  # only on first save (creation)
            student = self.match.application
            dept = self.match.department
            self.student_name = f"{student.first_name} {student.last_name}"
            self.department_name = dept.department
            self.start_date = student.start_date  # ✅ Copy from Application
            self.end_date = student.end_date
        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        """Return remaining days until end_date."""
        if self.end_date:
            remaining = (self.end_date - date.today()).days
            return remaining if remaining > 0 else 0
        return None

    def __str__(self):
        return f"Approved: {self.student_name} - Department: {self.department_name} - Registered: {self.registered}"
from django.db import models

# Create your models here.


class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('application', 'Application Submitted'),
        ('review', 'Under Review'),
        ('interview', 'Interview Scheduled'),
        ('approval', 'Approved'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    university = models.CharField(max_length=200, blank=True, null=True)
    college_name = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=100, default='Not Provided')
    address = models.CharField(max_length=200, default='Not Provided')
    education_level = models.CharField(max_length=50, default='Not Provided')
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    passport_id = models.FileField(upload_to='passport_ids/', default='Not Provided')
    department = models.CharField(max_length=100, default='Not Provided')
    current_year = models.CharField(max_length=10, default='Not Provided')
    expected_graduation = models.CharField(max_length=20, default='Not Provided')
    duration = models.CharField(max_length=10, choices=[(f"{i} month", f"{i} month{'s' if i > 1 else ''}") for i in range(1, 13)], null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    skills = models.TextField(blank=True, default='Not Provided')
    interests = models.TextField(default='Not Provided')
    motivation_letter = models.FileField(upload_to='motivation_letters/')
    resume = models.FileField(upload_to='resumes/')
    recommendation_letter = models.FileField(upload_to='recommendations/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def duration_display(self):
        if self.duration:
            return f"{self.duration} month{'s' if self.duration > 1 else ''}"
        return ""


from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # hashed password

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username



class EmailTemplate(models.Model):
    TEMPLATE_CHOICES = [
        ('approval', 'Approval Email'),
        ('rejection', 'Rejection Email'),
    ]

    type = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="Use placeholders like {applicant_name}, {department}, {report_day}")
    report_day = models.DateField(null=True, blank=True, help_text="Date students must come to SSGI")

    def __str__(self):
        return self.get_type_display()


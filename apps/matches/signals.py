from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from matches.models import Match
from adminpanel.models import EmailTemplate
from apps.approved.models import Approved

@receiver(post_save, sender=Match)
def handle_status_change(sender, instance, created, **kwargs):
    student_email = instance.application.email
    student_name = f"{instance.application.first_name} {instance.application.last_name}"
    department_name = instance.department.department

    if instance.status == 'approved':
        Approved.objects.get_or_create(match=instance)

        try:
            template = EmailTemplate.objects.get(type='approval')
            report_day = template.report_day.strftime('%B %d, %Y') if template.report_day else "TBD"
            subject = template.subject.format(
                applicant_name=student_name,
                department=department_name,
                report_day=report_day
            )
            body = template.body.format(
                applicant_name=student_name,
                department=department_name,
                report_day=report_day
            )
        except EmailTemplate.DoesNotExist:
            subject = "Internship Application Approved"
            body = (
                f"Dear {student_name},\n\n"
                f"Congratulations! Your internship application has been approved for the {department_name} department.\n\n"
                f"Please come to SSGI on TBD to submit your application letter physically and complete your registration.\n\n"
                "Best regards,\nInternship Team"
            )

    elif instance.status == 'rejected':
        Approved.objects.filter(match=instance).delete()

        try:
            template = EmailTemplate.objects.get(type='rejection')
            subject = template.subject.format(
                applicant_name=student_name,
                department=department_name
            )
            body = template.body.format(
                applicant_name=student_name,
                department=department_name
            )
        except EmailTemplate.DoesNotExist:
            subject = "Internship Application Result"
            body = (
                f"Dear {student_name},\n\n"
                f"We regret to inform you that your internship application was not successful this time.\n\n"
                "Best wishes,\nInternship Team"
            )

    else:
        # For other statuses, don't send emails
        return

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student_email],
        fail_silently=False,
    )

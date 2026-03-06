from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.applications.models import InternshipApplication
from apps.departments.models import Department
from apps.departments.utils import required_fields_map
from matches.models import Match

@receiver(post_save, sender=InternshipApplication)
def auto_match_intern(sender, instance, created, **kwargs):
    if not created:
        return

    student_major = instance.department
    if student_major is None:
        return

    if isinstance(student_major, Department):
        student_major_value = student_major.department
    else:
        student_major_value = student_major

    if student_major_value is None:
        return

    student_major_lower = str(student_major_value).strip().lower()
    if not student_major_lower:
        return
    student_major_str = student_major_lower
    matching_depts = []
    all_departments = Department.objects.all()

    for dept in all_departments:
        required_fields = required_fields_map(dept.fields_and_counts)

        if student_major_lower in required_fields:
            matching_depts.append((dept, required_fields[student_major_lower]))

    if not matching_depts:
        print("❌ No matching department found for this intern.")
        return

    available_depts = []
    for dept, field_capacity in matching_depts:
        current_field_count = Match.objects.filter(
            department=dept,
            status__in=['pending', 'approved'],
            student_department__iexact=student_major_str
        ).count()

        print(f"Dept: {dept.department}, Field: {student_major_str}, Capacity: {field_capacity}, Current count: {current_field_count}")

        if current_field_count < field_capacity:
            available_depts.append((dept, current_field_count))

    if available_depts:
        dept = sorted(available_depts, key=lambda x: x[1])[0][0]
        status = 'pending'
    else:
        dept = matching_depts[0][0]
        status = 'waitlist'

    match, was_created = Match.objects.get_or_create(
        application=instance,
        department=dept,
        defaults={
            'status': status,
            'student_department': student_major_str
        }
    )

    if not was_created and match.status != status:
        match.status = status
        match.save()

    if was_created:
        print(f"✅ Match created: {match} with status {status}")

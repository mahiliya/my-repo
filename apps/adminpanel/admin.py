from django.contrib import admin
from apps import approved
from apps.applications.models import InternshipApplication
from matches.models import Match
from apps.approved.models import Approved
from progress.models import ProgressView
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
import openpyxl
from django.http import HttpResponse
from django.utils.encoding import smart_str
from apps.departments.models import Department
from apps.departments.utils import normalize_fields_and_counts

from .models import EmailTemplate

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'age', 'email', 'phone', 'city', 'university', 'college_name',
        'nationality', 'address', 'education_level', 'cgpa', 'passport_id', 'department',
        'current_year', 'expected_graduation', 'duration', 'start_date', 'end_date', 'skills',
        'interests', 'motivation_letter', 'resume', 'recommendation_letter', 'submitted_at'
    ]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'get_student_name',
        'get_student_department',
        'get_student_skill',
        'get_department_name',
        'get_department_fields',
        'get_department_skills',
        'get_department_info',
        'status',
    )

    actions = ['run_matching_algorithm', 'approve_selected', 'waitlist_selected', 'reject_selected']

    # Display methods for admin columns
    def get_student_name(self, obj):
        return f"{obj.application.first_name} {obj.application.last_name}"
    get_student_name.short_description = 'Student Name'

    def get_student_department(self, obj):
        return obj.application.department
    get_student_department.short_description = 'Student Department'

    def get_student_skill(self, obj):
        return obj.application.skills
    get_student_skill.short_description = 'Student Skill'

    def get_department_name(self, obj):
        return obj.department.department
    get_department_name.short_description = 'Institution Department'

    def get_department_fields(self, obj):
        fields = normalize_fields_and_counts(obj.department.fields_and_counts)
        if not fields:
            return "—"
        return ", ".join(
            f"{item['field']}: {item['count']}"
            for item in fields
        )
    get_department_fields.short_description = 'Fields and Counts'

    def get_department_skills(self, obj):
        return obj.department.skills
    get_department_skills.short_description = 'Department Skills Requirement'

    def get_department_info(self, obj):
        return obj.department.potential_project
    get_department_info.short_description = 'Department Potential Project'

    # Main Matching Algorithm Action
    def run_matching_algorithm(self, request, queryset):
        applications = InternshipApplication.objects.filter(status='pending')
        departments = Department.objects.all()
        created = 0
        updated = 0

        for dept in departments:
            required_majors = [
                item['field'].strip().lower()
                for item in normalize_fields_and_counts(dept.fields_and_counts)
            ]

            for app in applications:
                if not app.department:
                    continue

                studentdept = app.department.strip().lower()

                if studentdept in required_majors:
                    match, was_created = Match.objects.get_or_create(
                        application=app,
                        department=dept,
                        defaults={'status': 'pending'}
                    )

                    if was_created:
                        created += 1
                    else:
                        updated += 1

                    # Always call save() to trigger model's own matched_on & snapshot logic
                    match.save()

        self.message_user(
            request,
            f"Matching complete. {created} new matches created. {updated} existing matches updated."
        )
    run_matching_algorithm.short_description = "Run Matching Algorithm"

    # Approve Selected Matches
    def approve_selected(self, request, queryset):
        for match in queryset:
            match.status = 'approved'
            match.save()
            Approved.objects.get_or_create(match=match)
        self.message_user(request, "Selected matches approved.")
    approve_selected.short_description = "Approve selected"

    # Waitlist Selected Matches
    def waitlist_selected(self, request, queryset):
        queryset.update(status='waitlist')
        self.message_user(request, "Selected matches waitlisted.")
    waitlist_selected.short_description = "Waitlist selected"

    # Reject Selected Matches
    def reject_selected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected matches rejected.")
    reject_selected.short_description = "Reject selected"


@admin.register(Approved)
class ApprovedAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'department_name',
        'approved_on',
        'registered',
        'get_start_date',
        'get_end_date',
        'register_button'
    )

    actions = ['mark_as_registered', 'export_as_excel']

    def mark_as_registered(self, request, queryset):
        updated = queryset.update(registered=True)
        self.message_user(request, f"{updated} students marked as registered.")
    mark_as_registered.short_description = "Mark selected students as registered"

    def register_button(self, obj):
        if not obj.registered:
            return format_html(
                '<a class="button" href="{}">Register</a>',
                f'./{obj.pk}/register/'
            )
        return "Registered"
    register_button.short_description = 'Register Student'
    register_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:approved_id>/register/',
                self.admin_site.admin_view(self.process_register),
                name='approved-register',
            ),
        ]
        return custom_urls + urls

    def process_register(self, request, approved_id, *args, **kwargs):
        approved_obj = self.get_object(request, approved_id)
        if approved_obj and not approved_obj.registered:
            approved_obj.registered = True
            approved_obj.save()
            self.message_user(request, f"Student '{approved_obj.match}' marked as registered.")
        return redirect(request.META.get('HTTP_REFERER', 'admin:approved_approved_changelist'))
    
    def export_as_excel(self, request, queryset):
        # Create workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Approved Students"

        # Define headers
        headers = ['Student Name', 'Department', 'Approved On', 'Start Date', 'End Date', 'Registered']

        ws.append(headers)

        for approved in queryset:
            student_name = f"{approved.match.application.first_name} {approved.match.application.last_name}"
            department = approved.match.department.department
            approved_on = approved.approved_on.strftime("%Y-%m-%d %H:%M:%S")
            registered = "Yes" if approved.registered else "No"

            start_date = approved.start_date.strftime("%Y-%m-%d") if approved.start_date else ""
            end_date = approved.end_date.strftime("%Y-%m-%d") if approved.end_date else ""

            ws.append([student_name, department, approved_on, start_date, end_date, registered])


        # Prepare HTTP response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename=approved_students.xlsx'
        wb.save(response)
        return response

    export_as_excel.short_description = "Download selected as Excel"

    def get_start_date(self, obj):
        return obj.start_date
    get_start_date.short_description = "Start Date"

    def get_end_date(self, obj):
        return obj.end_date
    get_end_date.short_description = "End Date"





@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = ['type', 'subject', 'body']
        if obj and obj.type == 'approval':
            fields.append('report_day')
        return fields



@admin.register(ProgressView)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "department_name",
        "approved_on",
        "registered",
        "get_start_date",
        "get_end_date",
        "days_remaining_display",
    )
    readonly_fields = (
        "student_name",
        "department_name",
        "approved_on",
        "registered",
        "get_start_date",
        "get_end_date",
        "days_remaining_display",
    )

    def get_start_date(self, obj):
        return obj.start_date
    get_start_date.short_description = "Start Date"

    def get_end_date(self, obj):
        return obj.end_date
    get_end_date.short_description = "End Date"
    def get_queryset(self, request):
        # Only show registered students
        qs = super().get_queryset(request)
        return qs.filter(registered=True)

    # No adding/editing/deleting from this view
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def days_remaining_display(self, obj):
        if obj.days_remaining is not None:
            return f"{obj.days_remaining} day{'s' if obj.days_remaining != 1 else ''}"
        return "N/A"
    days_remaining_display.short_description = "Days Remaining"

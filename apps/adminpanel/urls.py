from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # ZONE 1: APPLICANT PORTAL (Public)
    # ==========================================
    path('apply/', views.applicant_form, name='applicant_form'),
    path('apply/success/', views.applicant_success, name='applicant_success'),

    # ==========================================
    # ZONE 2: STAFF GATEWAY (Unified Login)
    # ==========================================
    path('staff/login/', views.unified_login, name='staff_login'),
    path('staff/logout/', views.admin_logout, name='admin_logout'),

    # ==========================================
    # ZONE 3: SUPERADMIN (System-Wide Control)
    # ==========================================
    path('staff/superadmin/dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    
    # Manager User Management
    # path('staff/superadmin/manage-admins/', views.manage_admins, name='manage_admins'),
    # path('staff/superadmin/add-admin/', views.add_admin, name='add_admin'),
    # path('staff/superadmin/delete-admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    # path('staff/superadmin/toggle-admin/<int:admin_id>/', views.toggle_admin_status, name='toggle_admin'),
    # path('staff/superadmin/reset-password/<int:admin_id>/', views.reset_admin_password, name='reset_password'),
    
    # Infrastructure Management (Fixed to match your HTML links)
    # path('staff/superadmin/departments/', views.manage_departments, name='manage_departments'),
    # path('staff/superadmin/departments/add/', views.add_department, name='add_department'),
    # path('staff/superadmin/departments/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    # path('staff/superadmin/departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    
    # Intern Management & Oversight
    # path('staff/superadmin/intern-oversight/', views.global_intern_oversight, name='global_intern_oversight'),
    # path('staff/superadmin/intern-profile/<int:app_id>/', views.intern_profile_view, name='intern_profile_view'),
    path('staff/superadmin/add-intern-manual/', views.add_intern_manual, name='add_intern_manual'),
    # path('staff/superadmin/update-intern-status/<int:app_id>/', views.update_intern_status, name='update_intern_status'),
    # path('staff/superadmin/intern-action/<int:app_id>/<str:action>/', views.superadmin_action, name='superadmin_action'),

    # ==========================================
    # ZONE 4: DEPT MANAGERS (Department Level)
    # ==========================================
    # path('staff/dept-admin/dashboard/', views.admin_home, name='admin_home'),
    path('staff/superadmin/dept-control/<int:dept_id>/', views.update_dept_controls, name='update_dept_controls'),
]
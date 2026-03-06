# apps/departments/decorators.py
from functools import wraps
from django.shortcuts import render
from django.utils import timezone
from .models import DepartmentPortalConfig
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

def departments_open_required(viewfunc):
    @wraps(viewfunc)
    def _wrapped(request, *args, **kwargs):
        cfg = DepartmentPortalConfig.get_solo()
        if not cfg.is_effectively_open:
            # Show a friendly “closed” page; use 403 to avoid indexing
            return render(
                request,
                "closed.html",
                {"config": cfg, "now": timezone.now()},
                status=403,
            )
        return viewfunc(request, *args, **kwargs)
    return _wrapped


def department_user_required(viewfunc):
    """Allow only users in the 'department' group (created by admin)."""
    @wraps(viewfunc)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # Let login_required handle redirects upstream
            return viewfunc(request, *args, **kwargs)

        # Group name that admins should assign to department accounts
        required_group_name = 'department'

        try:
            in_group = user.groups.filter(name=required_group_name).exists()
        except Exception:
            in_group = False

        if not in_group and not user.is_superuser:
            return HttpResponseForbidden("You don't have department access.")
        return viewfunc(request, *args, **kwargs)
    return _wrapped

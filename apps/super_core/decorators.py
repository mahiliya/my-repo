from django.core.exceptions import PermissionDenied
from functools import wraps

def superadmin_required(view_func):
    """
    The Job: Custom decorator that only allows users 
    with is_superuser = True to access the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # If they aren't a superuser, show the 'Forbidden' page
            raise PermissionDenied
    return _wrapped_view